#!/usr/bin/env python3
"""Is the +556 ppm J residual localized in the MID closers, or a uniform structural offset?

Tests:
 1. all-pass-flat probe: scale ALL coeffs by (1-eps); d(lambda)/d(eps). A localized
    loss-deficit moves a lot; a lossless-allpass-at-unity barely moves (structural).
 2. MID-only excess under J: zero full MID set -> lambda should be exactly 1.0 (per notes).
    Then sweep ONLY a global scale on the MID coeffs to see if any uniform MID gain change
    lands -10 ppm WITHOUT killing authority.
 3. cross-program: does BRIGHT HALL (id 0x?) also grow ~+the same under its own structure?
    (the notes say BRIGHT HALL +1198 ppm baseline.) Confirms uniform deficit hypothesis.
"""
import sys, os, math
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import aru_datapath as A
from exp_J_order import setfields, J_EDITS, lam

MID = {43,44,62,63,64,66,67,68,95,96,113,114,115,117,118,119}

def clone(prog): return [dict(p) for p in prog]

def scale_coeffs(prog, steps, factor):
    p2 = clone(prog)
    for st in p2:
        if steps is None or st['s'] in steps:
            st['coeff'] = int(round(st['coeff']*factor))
    return p2

def main():
    J = setfields(A.load_microcode(0x01), J_EDITS)
    base = lam(J)
    print(f"J baseline lambda = {base:.7f} ({(base-1)*1e6:+.1f} ppm)\n")

    print("=== 1. all-pass-flat probe: scale ALL coeffs by (1-eps) ===")
    for eps in (0.0, 0.001, 0.002, 0.005, 0.01):
        l = lam(scale_coeffs(J, None, 1-eps))
        print(f"  eps={eps:.3f}  lambda={l:.7f} ({(l-1)*1e6:+.1f} ppm)  d={(l-base)*1e6:+.1f}")

    print("\n=== 2. MID-only scale (does a uniform MID gain trim hit -10 ppm?) ===")
    for f in (1.0, 0.99, 0.98, 0.95, 0.90):
        p = scale_coeffs(J, MID, f)
        l = lam(p)
        # authority: zero MID
        l0 = lam(setfields(p, {s:{'coeff':0} for s in MID}))
        print(f"  MIDx{f:.2f}  lambda={l:.7f} ({(l-1)*1e6:+.1f} ppm)  MID-auth={(l0-l)*1e6:+.0f} ppm")

    print("\n=== 3. cross-program baseline (no J edits applied; structure-as-decoded) ===")
    # discover program ids present
    for pid in (0x01, 0x02, 0x03, 0x04):
        try:
            prog = A.load_microcode(pid)
        except Exception as e:
            print(f"  id {pid:#x}: load failed ({e})"); continue
        l = lam(prog)
        print(f"  id {pid:#x}: {len(prog)} steps  lambda={l:.7f} ({(l-1)*1e6:+.1f} ppm)")

if __name__ == '__main__':
    main()
