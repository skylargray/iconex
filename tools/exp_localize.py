#!/usr/bin/env python3
"""Localize the +1130 ppm excess loop gain: uniform or one block?

For each loop closer (a step with b3=1 AND XFER=1 -> writes RES back to DMEM and
closes a recirculation), scale ONLY that closer's coefficient by (1-delta) and
measure the converged lambda shift. A single dominant closer => localized
topology/delay issue there. Roughly equal shifts across closers => uniform
arithmetic/timing excess. Uses the converged measurement (exp_lambda_clean).
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import aru_datapath as A
from exp_lambda_clean import lambda_trajectory


def conv_lambda(prog, nsamp=26000, K=128, tail=30):
    traj = lambda_trajectory(prog, nsamp=nsamp, K=K)
    vals = sorted(l for _, l in traj[-tail:])
    return vals[len(vals)//2]


def scaled(prog, step_s, factor):
    out = [dict(p) for p in prog]
    for p in out:
        if p['s'] == step_s:
            p['coeff'] = int(round(p['coeff'] * factor))
    return out


def main():
    prog = A.load_microcode(0x01)
    closers = [p['s'] for p in prog if p['b3'] == 1 and p['XFER'] == 1]
    print(f"loop closers (b3=1 & XFER=1): {closers}\n")
    base = conv_lambda(prog)
    print(f"baseline lambda = {base:.7f} ({(base-1)*1e6:+.0f} ppm)\n")
    print(f"  {'closer':>7} {'coeff':>6}  {'lambda(x0.90)':>14}  {'d_ppm':>8}")
    rows = []
    for s in closers:
        c = next(p['coeff'] for p in prog if p['s'] == s)
        lam = conv_lambda(scaled(prog, s, 0.90))
        d = (lam - base) * 1e6
        rows.append((d, s, c, lam))
        print(f"  {s:>7} {c:>6}  {lam:.7f}  {d:>+8.0f}")
    rows.sort()
    print("\nmost-sensitive closers (largest lambda reduction per -10% coeff):")
    for d, s, c, lam in rows[:6]:
        print(f"  s{s}: coeff={c}  lambda->{lam:.7f}  ({d:+.0f} ppm)")


if __name__ == '__main__':
    main()
