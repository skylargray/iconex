#!/usr/bin/env python3
"""ANGLE: coefficient/alignment scaling + independent lambda verification.

Three tasks:
 (1) Re-derive per-MAC and RES scaling analytically from the confirmed arithmetic.
 (2) lambda sensitivity to single-bit perturbations of each scaling factor.
 (3) Independent re-measurement of CONCERT lambda by methods OTHER than the
     existing power iteration:
       (3a) long float64 impulse run, late log-amplitude slope,
       (3b) explicit sparse state-transition matrix -> scipy.sparse eigs + my own
            power method on the matrix (totally independent of exp_lambda_clean).
"""
import sys, os, math
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import aru_datapath as A

DMASK = A.DMASK
PICK = lambda st: (st['b5'] << 1) | st['b4']


# ----------------------------------------------------------------------------
# Parameterized float datapath: every scaling factor is an explicit knob so we
# can perturb one bit at a time. Baseline factors reproduce exp_lambda_clean.
#   operand   = x * OPSH         (baseline OPSH = 8   = <<3)
#   prod      = operand * Cs / PRSH   (baseline PRSH = 64 = >>6)
#   RES       = ACC / RESSH      (baseline RESSH = 8  = >>3)
#   Cs        = sign * (mag >> CSH)   (baseline CSH = 1 -> >>1)
# Net per-MAC contribution to ACC = x * Cs * OPSH / PRSH.
# ----------------------------------------------------------------------------
def lambda_traj(prog, pick=PICK, nsamp=60000, K=128, seed=1e4,
                OPSH=8.0, PRSH=64.0, RESSH=8.0, CSH=1):
    R = [0.0]*4; ACC = 0.0; RES = 0.0
    DM = [0.0]*(DMASK+1); pos = 0
    nz = set(); seeded = False; traj = []
    for n in range(nsamp):
        pos = (pos+1) & DMASK
        for st in prog:
            addr = (pos - st['offset']) & DMASK
            dab = RES if st['b3'] else DM[addr]
            if not seeded and st is prog[0]:
                dab += seed; seeded = True
            mag = abs(st['coeff'])
            Cs = -(mag >> CSH) if st['coeff'] < 0 else (mag >> CSH)
            x = R[pick(st)]; R[st['WA']] = dab
            if st['ZERO']: ACC = 0.0
            ACC = ACC + x*OPSH*Cs/PRSH
            if st['XFER']: RES = ACC/RESSH
            if st['b3']: DM[addr] = RES; nz.add(addr)
        if (n+1) % K == 0:
            s = math.sqrt(ACC*ACC + RES*RES + sum(v*v for v in R)
                          + sum(DM[i]*DM[i] for i in nz)) + 1e-300
            traj.append(math.exp(math.log(s)/K))
            f = 1.0/s
            R = [v*f for v in R]; ACC *= f; RES *= f
            for i in nz: DM[i] *= f
    return traj


def converged(traj, tail=60):
    t = sorted(traj[-tail:]); return t[len(t)//2]


# ----------------------------------------------------------------------------
# (3a) Independent: long float64 impulse run, measure late envelope slope.
#      No renormalization, no eigenvalue assumption -- just watch the L2 state
#      norm vs sample and fit a line to log(norm).
# ----------------------------------------------------------------------------
def impulse_norm_slope(prog, pick=PICK, nsamp=200000, K=256, seed=1.0):
    """Return list of (sample, log10(norm)) sampled every K, plus a robust
    least-squares per-sample log-growth from the late portion."""
    R = [0.0]*4; ACC = 0.0; RES = 0.0
    DM = [0.0]*(DMASK+1); pos = 0
    nz = set(); seeded = False
    samples = []
    for n in range(nsamp):
        pos = (pos+1) & DMASK
        for st in prog:
            addr = (pos - st['offset']) & DMASK
            dab = RES if st['b3'] else DM[addr]
            if not seeded and st is prog[0]:
                dab += seed; seeded = True
            mag = abs(st['coeff'])
            Cs = -(mag >> 1) if st['coeff'] < 0 else (mag >> 1)
            x = R[pick(st)]; R[st['WA']] = dab
            if st['ZERO']: ACC = 0.0
            ACC = ACC + x*8.0*Cs/64.0
            if st['XFER']: RES = ACC/8.0
            if st['b3']: DM[addr] = RES; nz.add(addr)
        if (n+1) % K == 0:
            s = math.sqrt(ACC*ACC + RES*RES + sum(v*v for v in R)
                          + sum(DM[i]*DM[i] for i in nz))
            if s > 0:
                samples.append((n+1, math.log(s)))
    # fit log(norm) = a*n + b on the late half (state subspace settled)
    half = samples[len(samples)//2:]
    m = len(half)
    sx = sum(p[0] for p in half); sy = sum(p[1] for p in half)
    sxx = sum(p[0]*p[0] for p in half); sxy = sum(p[0]*p[1] for p in half)
    slope_per_sample = (m*sxy - sx*sy)/(m*sxx - sx*sx)  # natural-log growth per sample
    lam = math.exp(slope_per_sample)
    return samples, lam


# ----------------------------------------------------------------------------
# (3b) Independent: assemble the EXPLICIT sparse linear state-transition matrix
#      and estimate spectral radius. The state vector is [R0..R3, ACC, RES, DM[nz]].
#      We discover the active DM addresses first, then build the matrix column by
#      column by running the datapath on each unit basis vector for exactly one
#      full sample (128 steps), with NO seed/impulse. This is a fundamentally
#      different mechanism than the power iteration in exp_lambda_clean.
# ----------------------------------------------------------------------------
def build_state_index(prog, pick=PICK):
    """Discover which DM addresses are touched in steady state (over a few full
    samples) so the linear map is closed over a finite state set."""
    touched = set()
    pos = 0
    # we must know which (pos,offset) addresses recur. Since pos cycles 0..DMASK,
    # but the program only ever touches addr = (pos-offset)&DMASK and pos advances
    # by 1 each sample, the set of addresses touched within ONE sample at a given
    # pos is fixed relative to pos. To get a closed linear map we PIN pos and look
    # at one sample. The eigen-mode is the per-sample map at a representative pos.
    return touched


def step_once(prog, state, idx, dm_addrs, pos, pick=PICK):
    """Apply one full sample (128 steps) of the LINEAR (float) datapath to a
    given state vector, at a fixed pos. state layout:
        [R0,R1,R2,R3, ACC, RES, DM[a] for a in dm_addrs]
    Returns the new state vector (same layout). No seed."""
    nR = 4
    R = list(state[0:4]); ACC = state[4]; RES = state[5]
    DM = {a: state[6+i] for i, a in enumerate(dm_addrs)}
    for st in prog:
        addr = (pos - st['offset']) & DMASK
        dab = RES if st['b3'] else DM.get(addr, 0.0)
        mag = abs(st['coeff'])
        Cs = -(mag >> 1) if st['coeff'] < 0 else (mag >> 1)
        x = R[pick(st)]; R[st['WA']] = dab
        if st['ZERO']: ACC = 0.0
        ACC = ACC + x*8.0*Cs/64.0
        if st['XFER']: RES = ACC/8.0
        if st['b3']: DM[addr] = RES
    out = [0.0]*(6+len(dm_addrs))
    out[0:4] = R; out[4] = ACC; out[5] = RES
    for i, a in enumerate(dm_addrs):
        out[6+i] = DM.get(a, 0.0)
    return out


def discover_dm_addrs(prog, pos, pick=PICK):
    """Which DM addresses are read or written within one sample at this pos."""
    addrs = set()
    for st in prog:
        addr = (pos - st['offset']) & DMASK
        addrs.add(addr)
    return sorted(addrs)


def matrix_spectral_radius(prog, pos, pick=PICK):
    """Build the dense one-sample linear map at fixed pos via basis probing,
    then get spectral radius two ways: numpy.eig and my own power method."""
    import numpy as np
    dm_addrs = discover_dm_addrs(prog, pos, pick)
    dim = 6 + len(dm_addrs)
    M = np.zeros((dim, dim))
    for j in range(dim):
        e = [0.0]*dim; e[j] = 1.0
        col = step_once(prog, e, None, dm_addrs, pos, pick)
        for i in range(dim):
            M[i, j] = col[i]
    # numpy eig
    ev = np.linalg.eigvals(M)
    sr_eig = max(abs(ev))
    # my own power method on M (independent of numpy eig AND of exp_lambda_clean)
    v = np.random.RandomState(0).randn(dim)
    v /= np.linalg.norm(v)
    lam_pm = 0.0
    for _ in range(20000):
        w = M @ v
        nw = np.linalg.norm(w)
        if nw == 0: break
        lam_pm = nw
        v = w / nw
    return dim, sr_eig, lam_pm, dm_addrs


def main():
    prog = A.load_microcode(0x01)
    print(f"CONCERT: {len(prog)} active steps\n")

    # ---------- TASK 1: analytic per-MAC / RES scaling ----------
    print("="*70)
    print("TASK 1: analytic re-derivation of per-tap / per-loop linear gain")
    print("="*70)
    print(" operand = x<<3              => x * 8")
    print(" prod    = (operand*Cs)>>6   => x*8*Cs/64 = x*Cs/8")
    print(" ACC accumulates prod")
    print(" RES     = ACC>>3            => ACC/8")
    print(" Cs      = sign*(|coeff7|>>1)")
    print(" => net per-MAC contribution to ACC = x * Cs / 8")
    print(" => for a single XFER tap with one MAC: RES = (x*Cs/8)/8 = x*Cs/64")
    print(" => effective tap COEFFICIENT seen by a recirculating sample = Cs/64")
    print("    = (|coeff7|>>1)/64  (matches tech-ref 12 C = (|coeff7|>>1)/64)")
    # quick numeric sanity on a representative closer (step 69 family)
    closers = [st for st in prog if st['b3'] and st['XFER']]
    print(f"\n {len(closers)} steps are b3&XFER (comb closers, the recirculation set).")
    mags = sorted({abs(st['coeff']) for st in closers})
    print(f"   |coeff7| values among closers: {mags}")
    print(f"   effective Cs/64 gains: "
          + ", ".join(f"{(m>>1)/64:.4f}" for m in mags))

    # ---------- TASK 2: single-bit scaling sensitivity ----------
    print("\n" + "="*70)
    print("TASK 2: single-bit perturbation of each scaling factor -> lambda")
    print("="*70)
    base = converged(lambda_traj(prog, nsamp=40000))
    print(f" BASELINE (OPSH=8,PRSH=64,RESSH=8,CSH=1): "
          f"lambda={base:.7f}  ({(base-1)*1e6:+.1f} ppm)")
    perturbs = [
        ("operand <<2 (OPSH=4)",   dict(OPSH=4.0)),
        ("operand <<4 (OPSH=16)",  dict(OPSH=16.0)),
        ("prod >>5 (PRSH=32)",     dict(PRSH=32.0)),
        ("prod >>7 (PRSH=128)",    dict(PRSH=128.0)),
        ("RES >>2 (RESSH=4)",      dict(RESSH=4.0)),
        ("RES >>4 (RESSH=16)",     dict(RESSH=16.0)),
        ("coeff >>0 (CSH=0)",      dict(CSH=0)),
        ("coeff >>2 (CSH=2)",      dict(CSH=2)),
    ]
    for name, kw in perturbs:
        lam = converged(lambda_traj(prog, nsamp=40000, **kw))
        # net loop-gain scale relative to baseline
        scale = ((kw.get('OPSH',8.0)/8.0) * (64.0/kw.get('PRSH',64.0))
                 * (8.0/kw.get('RESSH',8.0)))
        cnote = "" if 'CSH' not in kw else f"  (coeff shift, not a clean global scale)"
        print(f"  {name:24s}: lambda={lam:.7f}  ({(lam-1)*1e6:+.1f} ppm)"
              f"  loopscale x{scale:g}{cnote}  {'<<< DECAY' if lam<1 else ''}")
    # what uniform coeff scale gives unity?  lambda ~ scale on a 1st-order loop,
    # so needed scale ~ 1/base near unity. Show the empirical curve.
    print("\n  uniform global gain sweep (g multiplies every MAC), bracket unity:")
    for g in [0.86, 0.88, 0.89, 0.895, 0.90, 0.92, 1.0]:
        lam = converged(lambda_traj(prog, nsamp=40000, OPSH=8.0*g))
        print(f"    g={g:.3f}: lambda={lam:.7f}  ({(lam-1)*1e6:+.1f} ppm)"
              f"  {'<<< DECAY' if lam<1 else ''}")

    # ---------- TASK 3a: independent long impulse slope ----------
    print("\n" + "="*70)
    print("TASK 3a: INDEPENDENT long float64 impulse, late log-norm slope")
    print("="*70)
    samples, lam_imp = impulse_norm_slope(prog, nsamp=200000, K=256)
    print(f"  late-half log-norm slope => lambda = {lam_imp:.7f}  "
          f"({(lam_imp-1)*1e6:+.1f} ppm)")
    # show a few norm points to confirm monotone growth
    show = samples[::max(1, len(samples)//8)]
    for n, ln in show:
        print(f"    n={n:7d}  log(norm)={ln:+.4f}")

    # ---------- TASK 3b: independent explicit-matrix spectral radius ----------
    print("\n" + "="*70)
    print("TASK 3b: INDEPENDENT explicit one-sample matrix spectral radius")
    print("="*70)
    # probe at a few representative pos values; the per-sample recirculation map
    # is pos-shifted but its spectral radius (the decay rate) should be invariant.
    for pos in [1, 1000, 30000]:
        dim, sr_eig, lam_pm, dm_addrs = matrix_spectral_radius(prog, pos)
        print(f"  pos={pos:6d}: dim={dim:4d}  "
              f"numpy|eig|max={sr_eig:.7f} ({(sr_eig-1)*1e6:+.1f}ppm)  "
              f"myPM={lam_pm:.7f} ({(lam_pm-1)*1e6:+.1f}ppm)")


if __name__ == '__main__':
    main()
