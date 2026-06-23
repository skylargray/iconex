#!/usr/bin/env python3
"""Decisive structural test: run the datapath in EXACT float (no saturation, no
truncation) and measure the linear growth rate. This isolates the STRUCTURAL loop
gain from all integer/quantization effects.

If the float-exact model grows (lambda>1), the instability is structural (topology/
coefficients/missing-damping), NOT arithmetic rounding -> the fix is a damping
mechanism, not a sub-LSB tweak.

Also: verify run_r(floor/floor) == reference run() (harness faithfulness).
"""
import sys, os, math
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import aru_datapath as A
import exp_rounding as E

DMASK = A.DMASK


def run_float(prog, pick, nsamp, imp, saturate=False, quantize=False):
    """Exact-float datapath. saturate/quantize off => pure linear structure."""
    R = [0.0, 0.0, 0.0, 0.0]; ACC = 0.0; RES = 0.0
    DM = [0.0] * (DMASK + 1); pos = 0; out = []
    BIG = 1e18
    for n in range(nsamp):
        pos = (pos + 1) & DMASK
        esum = 0.0
        for st in prog:
            addr = (pos - st['offset']) & DMASK
            dab = RES if st['b3'] else DM[addr]
            if n == 0 and st is prog[0]:
                dab += imp
            mag = abs(st['coeff']); csign = st['coeff'] < 0
            Cs = -(mag >> 1) if csign else (mag >> 1)
            ra = pick(st); x = R[ra]; R[st['WA']] = dab
            if st['ZERO']:
                ACC = 0.0
            operand = x * 8.0
            prod = operand * Cs / 64.0          # exact x*Cs/8, no floor
            if quantize:
                prod = math.floor(prod)
            ACC = ACC + prod
            if saturate:
                ACC = max(-524287.0, min(524287.0, ACC))
            if st['XFER']:
                RES = ACC / 8.0                 # exact, no floor
                if quantize:
                    RES = math.floor(RES)
                if saturate:
                    RES = max(-32768.0, min(32767.0, RES))
            if st['b3']:
                DM[addr] = RES
            if st['XFER']:
                esum += abs(RES)
        out.append(esum)
        if esum > BIG:                          # diverged enough to measure slope
            break
    return out


def early_slope(esum, lo_frac=0.1, hi_frac=0.6):
    n = len(esum)
    lo, hi = int(n * lo_frac), int(n * hi_frac)
    xs = [i for i in range(lo, hi) if esum[i] > 0]
    if len(xs) < 5:
        return None
    ys = [math.log(esum[i]) for i in xs]
    m = len(xs); sx = sum(xs); sy = sum(ys)
    sxx = sum(x * x for x in xs); sxy = sum(x * y for x, y in zip(xs, ys))
    return (m * sxy - sx * sy) / (m * sxx - sx * sx)


def main():
    prog = A.load_microcode(0x01)
    pick = lambda st: (st['b5'] << 1) | st['b4']

    # Faithfulness: run_r(floor/floor) must equal the reference run().
    ref = A.run(prog, pick, nsamp=500)
    mine = E.run_r(prog, pick, 500, 20000, 'floor', 'floor')
    print(f"run_r(floor/floor) == reference run(): {ref == mine}")

    print("\nFLOAT-EXACT structural runs (lambda = exp(slope) per sample):")
    for label, sat, quant in [
        ("pure linear   (no sat, no quant)", False, False),
        ("linear + floor quant (no sat)   ", False, True),
        ("linear + saturation (no quant)  ", True,  False),
        ("full integer-equiv (sat+quant)  ", True,  True),
    ]:
        e = run_float(prog, pick, 4000, 20000, saturate=sat, quantize=quant)
        s = early_slope(e)
        lam = math.exp(s) if s is not None else float('nan')
        diverged = (len(e) < 4000)
        print(f"  {label}  slope={s:+.4e}  lambda={lam:.7f}  "
              f"{'DIVERGED@'+str(len(e)) if diverged else 'n=4000'}  last={e[-1]:.3g}")


if __name__ == '__main__':
    main()
