#!/usr/bin/env python3
"""Test the LFO-detuning hypothesis for the CONCERT growing mode.

(1) STATIC sweep: shift the modulated taps (56,57 / 107,108) by a fixed integer
    delta and measure the structural lambda. If lambda dips below 1 for part of the
    +-47 range, the LFO (which sweeps through that range) can average the mode below 1.
(2) LFO sweep: apply the real triangle modulation (anti-phase pairs, +-depth) and
    measure whether the time-varying system decays (and the RT60).

lambda estimator = float-exact datapath (no sat / no quant), asymptotic log-energy slope.
"""
import sys, os, math
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import aru_datapath as A

DMASK = A.DMASK
NATIVE_HZ = 34130.0
PAIR_A = {56, 57}
PAIR_B = {107, 108}


def run_float_mod(prog, pick, nsamp, imp, delta_fn, saturate=False):
    """delta_fn(n) -> integer delta applied to PAIR_A offsets (+delta) and PAIR_B
    offsets (-delta), i.e. anti-phase. Returns per-sample esum."""
    R = [0.0]*4; ACC = 0.0; RES = 0.0
    DM = [0.0]*(DMASK+1); pos = 0; out = []
    for n in range(nsamp):
        pos = (pos+1) & DMASK
        delta = delta_fn(n)
        esum = 0.0
        for st in prog:
            off = st['offset']
            if st['s'] in PAIR_A: off = (off + delta) & DMASK
            elif st['s'] in PAIR_B: off = (off - delta) & DMASK
            addr = (pos - off) & DMASK
            dab = RES if st['b3'] else DM[addr]
            if n == 0 and st is prog[0]:
                dab += imp
            mag = abs(st['coeff']); Cs = -(mag>>1) if st['coeff']<0 else (mag>>1)
            x = R[pick(st)]; R[st['WA']] = dab
            if st['ZERO']: ACC = 0.0
            ACC += x*8.0*Cs/64.0
            if saturate: ACC = max(-524287.0, min(524287.0, ACC))
            if st['XFER']:
                RES = ACC/8.0
                if saturate: RES = max(-32768.0, min(32767.0, RES))
            if st['b3']: DM[addr] = RES
            if st['XFER']: esum += abs(RES)
        out.append(esum)
    return out


def slope(esum, lo, hi):
    xs = [i for i in range(lo, hi) if esum[i] > 0]
    if len(xs) < 8: return None
    ys = [math.log(esum[i]) for i in xs]
    m=len(xs); sx=sum(xs); sy=sum(ys); sxx=sum(x*x for x in xs); sxy=sum(x*y for x,y in zip(xs,ys))
    return (m*sxy - sx*sy)/(m*sxx - sx*sx)


def lam_static(prog, pick, delta, nsamp=6000):
    e = run_float_mod(prog, pick, nsamp, 20000, lambda n: delta, saturate=False)
    s = slope(e, nsamp//5, nsamp*4//5)
    return math.exp(s) if s is not None else float('nan')


def triangle(n, period, depth):
    """Symmetric triangle in [-depth, +depth], integer-rounded."""
    ph = (n % period) / period          # 0..1
    tri = 4*ph - 1 if ph < 0.5 else 3 - 4*ph   # -1 -> +1 -> -1
    return int(round(tri * depth))


def main():
    prog = A.load_microcode(0x01)
    pick = lambda st: (st['b5']<<1)|st['b4']

    print("structural lambda (float-exact) at static modulated-tap offset delta:")
    print("  delta:  lambda   (>1 grows, <1 decays)")
    best = None
    for d in range(-50, 51, 5):
        lam = lam_static(prog, pick, d)
        mark = "  <-- DECAYS" if lam < 1.0 else ""
        print(f"   {d:+4d}: {lam:.7f}{mark}")
    # finer near zero
    print("\n  fine sweep near center:")
    for d in range(-12, 13, 1):
        lam = lam_static(prog, pick, d)
        mark = "  <-- DECAYS" if lam < 1.0 else ""
        print(f"   {d:+4d}: {lam:.7f}{mark}")

    # geometric mean of lambda over the +-47 triangle range (uniform-ish sampling)
    print("\nGeometric-mean lambda over a +-depth uniform offset sweep:")
    for depth in (8, 20, 30, 47):
        lams = [lam_static(prog, pick, d) for d in range(-depth, depth+1, 2)]
        gm = math.exp(sum(math.log(l) for l in lams)/len(lams))
        print(f"  depth +-{depth}: geo-mean lambda = {gm:.7f}  "
              f"{'NET DECAY' if gm<1 else 'net grow'}")


if __name__ == '__main__':
    main()
