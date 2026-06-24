#!/usr/bin/env python3
"""Test MID-as-loss decode variants under J, per workflow task.

Baseline: J grows +556 ppm, MID is the sole decay element but nets +556 ppm gain.
Goal: find a plausible decode of the comb-closer FF taps / closers that turns MID into
a small net LOSS WITHOUT re-decoupling HFD/LOW/MID/XOV (i.e. authority retained, all
negative = loss direction). Report conv_lambda + coupling per variant.

Hypotheses from task:
  (a) third-FF tap source/RA: s64,68,115,119 read R2 -> try R3 / R0 / R1
  (b) closer feedback coeff vs FF coeff balance (the +124 closer vs -75 FF)
  (c) sign of the cross-block term (the -37*d_b over-recovery term)
  (d) +-1-sample delay on the closer feedback
"""
import sys, os, math
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import aru_datapath as A
from exp_J_order import setfields, J_EDITS, lam

DMASK = A.DMASK
HFD = {40, 41, 92, 93}; LOW = {43, 95}; XOV = {45, 46, 97, 98}
MID = {43,44,62,63,64,66,67,68,95,96,113,114,115,117,118,119}

# step sets
THIRD_FF = {64, 68, 115, 119}      # third FF tap, reads R2
FIRST_FF = {62, 66, 113, 117}      # first FF tap (ZERO-open), reads R3
SECOND_FF = {63, 67, 114, 118}     # second FF tap, reads R2
CLOSERS = {65, 69, 116, 120}  # the +124 closers that close the MID comb blocks A/B

def clone(prog): return [dict(p) for p in prog]

def conv_lam(prog, **kw):
    return lam(prog, **kw)

def coupling(prog):
    base = conv_lam(prog)
    out = {'base': base}
    for nm, steps in [('HFD', HFD), ('LOW', LOW), ('MID', MID), ('XOV', XOV)]:
        p2 = setfields(prog, {s: {'coeff': 0} for s in steps})
        out[nm] = (conv_lam(p2) - base) * 1e6
    return out

def report(name, prog):
    c = coupling(prog)
    sign = 'GROW' if c['base']>1 else 'DECAY'
    print(f"{name}")
    print(f"  lambda={c['base']:.7f} ({(c['base']-1)*1e6:+.1f} ppm) {sign}  "
          f"auth: HFD {c['HFD']:+.0f} LOW {c['LOW']:+.0f} MID {c['MID']:+.0f} XOV {c['XOV']:+.0f}")
    return c

def set_ra(prog, steps, b5, b4):
    return setfields(prog, {s: {'b5': b5, 'b4': b4} for s in steps})

def main():
    J = setfields(A.load_microcode(0x01), J_EDITS)
    print("target lambda = 0.9999899 (-10 ppm); retain authority = all four negative\n")
    report("J (reference)", J)
    print()

    # (a) third-FF tap source RA: currently R2 (b5=1,b4=0). Try R0,R1,R3
    print("--- (a) third-FF tap (s64,68,115,119) RA reassignment ---")
    report("  third-FF read R0", set_ra(J, THIRD_FF, 0, 0))
    report("  third-FF read R1", set_ra(J, THIRD_FF, 0, 1))
    report("  third-FF read R3", set_ra(J, THIRD_FF, 1, 1))
    print()

    # (b) closer feedback coeff vs FF coeff balance: scale closers' +124 down a hair
    print("--- (b) closer +124 vs FF -75 balance ---")
    for c in (123, 122, 120):
        report(f"  closers coeff +{c}", setfields(J, {s: {'coeff': c} for s in CLOSERS}))
    print()

    # (c) sign of cross-block term: the third FF tap -75 -> flip sign on third FF
    print("--- (c) cross-block term sign (third-FF coeff sign flip) ---")
    report("  third-FF coeff +75 (flip)", setfields(J, {s: {'coeff': 75} for s in THIRD_FF}))
    print()

    # (d) +-1-sample delay on closer feedback: offset +-1 on the closer read
    print("--- (d) +-1-sample delay on closer feedback (offset +-1) ---")
    def off_shift(prog, steps, d):
        p2 = clone(prog)
        for st in p2:
            if st['s'] in steps:
                st['offset'] = (st['offset'] + d) & DMASK
        return p2
    report("  closers offset +1", off_shift(J, CLOSERS, 1))
    report("  closers offset -1", off_shift(J, CLOSERS, -1))

if __name__ == '__main__':
    main()
