#!/usr/bin/env python3
"""Adversarial independent reproduction of the band-split framing.

Goal: try to REFUTE these three claims with raw numbers:
  (A) baseline converged lambda ~ 1.00112 (+1121 ppm, GROWS)
  (B) coupling: MID ~ -1232 ppm (zeroing MID makes it DECAY); HFD/LOW ~ +10 ppm (inert)
  (C) V3: ZERO=1 on s96 AND s98 (both halves discard) -> lambda ~ -112 ppm (DECAYS)

I deliberately re-derive everything from aru_datapath + exp_lambda_clean primitives
and print signed ppm to 7 decimals. I also dump the actual decoded band-split steps
so the param->step mapping is independently checked, not taken on faith.
"""
import sys, os
sys.path.insert(0, 'tools')
import aru_datapath as A
from exp_symfix import conv_lambda, zero_param, setfields, clone, HFD, LOW, MID, XOV

def ppm(lam):
    return (lam - 1.0) * 1e6

def show_band_steps(prog):
    band = {37,38,39,40,41,42,43,44,45,46, 89,90,91,92,93,94,95,96,97,98}
    print("=== decoded band-split steps (independent dump) ===")
    by_s = {st['s']: st for st in prog}
    for s in sorted(band):
        st = by_s.get(s)
        if st is None:
            print(f"  s{s}: (inactive/absent)")
            continue
        ra = (st['b5']<<1)|st['b4']
        print(f"  s{s:3d}: coeff={st['coeff']:+4d} RA={ra} ZERO={st['ZERO']} "
              f"XFER={st['XFER']} b3={st['b3']} WA={st['WA']} offset={st['offset']}")

def main():
    prog = A.load_microcode(0x01)
    print(f"active steps: {len(prog)}")
    print(f"HFD={sorted(HFD)} LOW={sorted(LOW)} MID={sorted(MID)} XOV={sorted(XOV)}")
    show_band_steps(prog)

    print("\n=== (A) BASELINE ===")
    base = conv_lambda(prog)
    print(f"  baseline lambda = {base:.7f}  ({ppm(base):+.1f} ppm)  "
          f"{'GROW' if base>1 else 'DECAY'}")

    print("\n=== (B) COUPLING (zero each param's coeff, delta vs baseline) ===")
    for nm, steps in [('HFD', HFD), ('LOW', LOW), ('MID', MID), ('XOV', XOV)]:
        lam = conv_lambda(zero_param(prog, steps))
        d = lam - base
        print(f"  {nm:4s}: lambda={lam:.7f}  delta={d*1e6:+.1f} ppm  "
              f"(zeroed -> {'GROW' if lam>1 else 'DECAY'})")

    print("\n=== (C) V3: ZERO=1 on s96 AND s98 (both halves discard) ===")
    v3 = setfields(prog, {96: {'ZERO': 1}, 98: {'ZERO': 1}})
    lam_v3 = conv_lambda(v3)
    print(f"  V3 lambda = {lam_v3:.7f}  ({ppm(lam_v3):+.1f} ppm)  "
          f"{'GROW' if lam_v3>1 else 'DECAY'}")

    print("\n=== summary vs claimed ===")
    print(f"  (A) baseline   claimed ~+1121 ppm   got {ppm(base):+.1f} ppm")
    print(f"  (C) V3         claimed ~ -112 ppm    got {ppm(lam_v3):+.1f} ppm")

if __name__ == '__main__':
    main()
