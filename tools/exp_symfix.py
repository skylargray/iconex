#!/usr/bin/env python3
"""Test band-split decode variants that symmetrise the two tank halves.

The only raw-byte difference between the two CONCERT band-split halves is lane2
bit7 (ZERO) at s44/s96 and s46/s98: first half decodes to THREE accumulator
clears (s37,44,46), second half to ONE (s89). A symmetric tank should match.

For each variant, report converged lambda AND whether HFD/LOW/MID now couple
(does zeroing each param's coeff move lambda?). The correct decode should make
the decay controls actually control the loop.
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import aru_datapath as A
from exp_lambda_clean import lambda_trajectory

HFD = {40, 41, 92, 93}; LOW = {43, 95}; MID = {44, 96}; XOV = {45, 46, 97, 98}


def conv_lambda(prog, nsamp=30000, K=128, tail=40):
    traj = lambda_trajectory(prog, nsamp=nsamp, K=K)
    vals = sorted(l for _, l in traj[-tail:])
    return vals[len(vals) // 2]


def clone(prog): return [dict(p) for p in prog]


def setfields(prog, edits):
    """edits: {step: {field: value}}"""
    p2 = clone(prog)
    for st in p2:
        if st['s'] in edits:
            st.update(edits[st['s']])
    return p2


def zero_param(prog, steps):
    p2 = clone(prog)
    for st in p2:
        if st['s'] in steps:
            st['coeff'] = 0
    return p2


def coupling(prog):
    base = conv_lambda(prog)
    out = {'base': base}
    for nm, steps in [('HFD', HFD), ('LOW', LOW), ('MID', MID)]:
        out[nm] = conv_lambda(zero_param(prog, steps)) - base
    return out


def report(name, prog):
    c = coupling(prog)
    print(f"\n{name}")
    print(f"  lambda = {c['base']:.7f}  ({(c['base']-1)*1e6:+.0f} ppm)  "
          f"{'GROW' if c['base']>1 else 'DECAY'}")
    print(f"  coupling (d-ppm when coeff->0):  HFD {c['HFD']*1e6:+.0f}   "
          f"LOW {c['LOW']*1e6:+.0f}   MID {c['MID']*1e6:+.0f}")


def main():
    prog = A.load_microcode(0x01)
    print("target lambda = 0.9999899")
    report("BASELINE (as decoded)", prog)

    # V2: symmetrise first half to match second -> remove ZERO at s44, s46
    v2 = setfields(prog, {44: {'ZERO': 0}, 46: {'ZERO': 0}})
    report("V2: s44,s46 ZERO->0 (first half matches second)", v2)

    # V3 (sanity): symmetrise the OTHER way -> add ZERO at s96, s98
    v3 = setfields(prog, {96: {'ZERO': 1}, 98: {'ZERO': 1}})
    report("V3 (sanity): s96,s98 ZERO->1 (second half matches first)", v3)


if __name__ == '__main__':
    main()
