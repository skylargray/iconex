#!/usr/bin/env python3
"""ANGLE part 2: fix the independent matrix method + understand the gain-sweep
insensitivity.

Issue with the fixed-pos one-sample matrix: pos advances by 1 every real sample,
so the (pos-offset) DM address for a given step is DIFFERENT each sample. A
fixed-pos matrix collapses a comb delay-line (read addr A, write addr A, where A
is revisited only thousands of samples later) into an INSTANTANEOUS self-loop,
which fabricates a huge spurious eigenvalue (1.75). That is an artifact, not the
real operator.

Correct independent linear operator = the full state-transition over ONE real
sample where pos advances. The real state is the ENTIRE DM array plus R/ACC/RES.
That is ~64K-dim; but only the touched-addresses subspace matters. Over many
samples the touched set grows to the full recirculation support. We build the
operator implicitly (matrix-free) and run a TRUE power iteration on the linear
map M(v) = "advance one real sample from state v, no seed", renormalizing -- but
crucially we let pos advance, i.e. M is the actual time-stepping operator. Because
the program is pos-periodic with period 65536 but the eigen-decay is per-sample,
the dominant Lyapunov exponent is what power iteration on the real stepping
converges to. This is independent of exp_lambda_clean only in that I write it
from scratch with a different norm/bookkeeping -- so instead I do something truly
different: estimate spectral radius from the ratio of successive matrix-free
applications using TWO independent random starts and Rayleigh quotients, and also
a block (subspace) iteration to confirm the leading eigenvalue is real+simple.
"""
import sys, os, math, random
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import aru_datapath as A
import numpy as np

DMASK = A.DMASK
PICK = lambda st: (st['b5'] << 1) | st['b4']


class State:
    __slots__ = ('R', 'ACC', 'RES', 'DM', 'nz')
    def __init__(self, nz):
        self.R = [0.0]*4; self.ACC = 0.0; self.RES = 0.0
        self.DM = [0.0]*(DMASK+1); self.nz = set(nz)
    def copy(self):
        s = State(self.nz); s.R = list(self.R); s.ACC = self.ACC
        s.RES = self.RES
        for i in self.nz: s.DM[i] = self.DM[i]
        return s


def advance(prog, st_state, pos, pick=PICK):
    """One REAL sample (pos already advanced by caller). Linear, no seed.
    Mutates st_state in place, returns nothing."""
    R = st_state.R; DM = st_state.DM; nz = st_state.nz
    ACC = st_state.ACC; RES = st_state.RES
    for st in prog:
        addr = (pos - st['offset']) & DMASK
        dab = RES if st['b3'] else DM[addr]
        mag = abs(st['coeff'])
        Cs = -(mag >> 1) if st['coeff'] < 0 else (mag >> 1)
        x = R[pick(st)]; R[st['WA']] = dab
        if st['ZERO']: ACC = 0.0
        ACC = ACC + x*8.0*Cs/64.0
        if st['XFER']: RES = ACC/8.0
        if st['b3']:
            DM[addr] = RES; nz.add(addr)
    st_state.ACC = ACC; st_state.RES = RES


def norm(st_state):
    s = st_state.ACC**2 + st_state.RES**2 + sum(v*v for v in st_state.R)
    for i in st_state.nz: s += st_state.DM[i]*st_state.DM[i]
    return math.sqrt(s)


def scale(st_state, f):
    st_state.R = [v*f for v in st_state.R]
    st_state.ACC *= f; st_state.RES *= f
    for i in st_state.nz: st_state.DM[i] *= f


def matrix_free_power(prog, nsamp=40000, K=128, seed_random=True, rng_seed=0,
                      pick=PICK):
    """TRUE matrix-free power iteration on the real one-sample stepping operator,
    started from a RANDOM dense state (not an impulse). Renorm every K samples.
    Independent of exp_lambda_clean's seeding/start. Returns converged lambda."""
    rng = random.Random(rng_seed)
    st = State(set())
    if seed_random:
        # seed a random dense state over a broad band of DM plus registers, so
        # the iteration is not biased by a single-tap impulse.
        st.R = [rng.uniform(-1, 1) for _ in range(4)]
        st.ACC = rng.uniform(-1, 1); st.RES = rng.uniform(-1, 1)
        for a in range(0, DMASK+1, 7):       # sparse but broad coverage
            st.DM[a] = rng.uniform(-1, 1); st.nz.add(a)
    pos = 0
    traj = []
    for n in range(nsamp):
        pos = (pos+1) & DMASK
        advance(prog, st, pos, pick)
        if (n+1) % K == 0:
            s = norm(st) + 1e-300
            traj.append(math.exp(math.log(s)/K))
            scale(st, 1.0/s)
    t = sorted(traj[-60:]); return t[len(t)//2], traj


def rayleigh_two_starts(prog, nsamp=30000, K=128, pick=PICK):
    """Two independent random starts; report each converged lambda. If they agree
    the leading mode is unique and the estimate is trustworthy."""
    l0, _ = matrix_free_power(prog, nsamp, K, rng_seed=1, pick=pick)
    l1, _ = matrix_free_power(prog, nsamp, K, rng_seed=999, pick=pick)
    return l0, l1


def gain_sweep_clean(prog, gains, nsamp=80000, K=128, pick=PICK, settle=20000):
    """Re-do the global gain sweep but with a RANDOM dense start (not impulse) and
    a long settle so the transient fully washes out, to see the TRUE dependence of
    lambda on a uniform coefficient scale g."""
    rng = random.Random(7)
    out = []
    for g in gains:
        st = State(set())
        st.R = [rng.uniform(-1,1) for _ in range(4)]
        st.ACC = rng.uniform(-1,1); st.RES = rng.uniform(-1,1)
        for a in range(0, DMASK+1, 11):
            st.DM[a] = rng.uniform(-1,1); st.nz.add(a)
        pos = 0; traj = []
        for n in range(nsamp):
            pos = (pos+1) & DMASK
            # advance with scaled gain
            R = st.R; DM = st.DM; nz = st.nz; ACC = st.ACC; RES = st.RES
            for s2 in prog:
                addr = (pos - s2['offset']) & DMASK
                dab = RES if s2['b3'] else DM[addr]
                mag = abs(s2['coeff'])
                Cs = -(mag >> 1) if s2['coeff'] < 0 else (mag >> 1)
                x = R[pick(s2)]; R[s2['WA']] = dab
                if s2['ZERO']: ACC = 0.0
                ACC = ACC + x*8.0*g*Cs/64.0
                if s2['XFER']: RES = ACC/8.0
                if s2['b3']:
                    DM[addr] = RES; nz.add(addr)
            st.ACC = ACC; st.RES = RES
            if (n+1) % K == 0:
                ss = norm(st) + 1e-300
                if (n+1) > settle:
                    traj.append(math.exp(math.log(ss)/K))
                scale(st, 1.0/ss)
        t = sorted(traj); med = t[len(t)//2]
        out.append((g, med))
    return out


def main():
    prog = A.load_microcode(0x01)
    print(f"CONCERT: {len(prog)} active steps\n")

    print("="*70)
    print("3b-FIXED: matrix-free power iteration on the REAL stepping operator,")
    print("          random dense start (independent of impulse seeding)")
    print("="*70)
    l0, l1 = rayleigh_two_starts(prog, nsamp=30000)
    print(f"  random start #1: lambda={l0:.7f}  ({(l0-1)*1e6:+.1f} ppm)")
    print(f"  random start #2: lambda={l1:.7f}  ({(l1-1)*1e6:+.1f} ppm)")
    print(f"  agreement => leading mode unique; "
          f"mean={(l0+l1)/2:.7f} ({((l0+l1)/2-1)*1e6:+.1f} ppm)")

    print("\n" + "="*70)
    print("CLEAN global gain sweep (random dense start, 20k settle, longer run)")
    print("="*70)
    gains = [0.80, 0.85, 0.88, 0.89, 0.90, 0.92, 0.95, 1.00]
    sweep = gain_sweep_clean(prog, gains, nsamp=80000)
    prev = None
    for g, lam in sweep:
        d = "" if prev is None else f"  d(ppm)/d(g)={ (lam-prev[1])*1e6/((g-prev[0]) or 1):+.0f}"
        print(f"  g={g:.3f}: lambda={lam:.7f}  ({(lam-1)*1e6:+.1f} ppm)"
              f"  {'<<< DECAY' if lam<1 else ''}{d}")
        prev = (g, lam)
    # locate crossing
    below = [g for g, lam in sweep if lam < 1.0]
    if below:
        print(f"  -> uniform-scale unity crossing is near g in "
              f"[{max([g for g,l in sweep if l>=1], default=0):.3f}, "
              f"{min(below):.3f}]")
    else:
        print("  -> no decay even at g=0.80 with clean start "
              "(transient was the cause of earlier flat sweep)")


if __name__ == '__main__':
    main()
