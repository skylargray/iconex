#!/usr/bin/env python3
"""ORACLE MAP: model-authority sweep of each CONCERT decay control vs manual-expected.

For each control (LOW/MID/XOV/HFD) load 224XL_param_sweep_01.json, set ALL of that
param's coeff_steps to the value at each idx 0..7, and measure conv_lambda. This is
the REAL authority curve of each control in OUR (current-decode) model. Compare to
what the manual says the control SHOULD do.
"""
import sys, os, json
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import aru_datapath as A
from exp_symfix import conv_lambda, clone

SWEEP = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                     '..', 'docs', 'reference', '224', '224XL_param_sweep_01.json')

# param index -> control name (per firmware page-1 labels LOW MID XOV HFD DEP PDL)
PARAM_NAME = {0: 'LOW', 1: 'MID', 2: 'XOV', 3: 'HFD', 4: 'DEP', 5: 'PDL'}


def set_coeffs(prog, step_to_coeff):
    p2 = clone(prog)
    for st in p2:
        if st['s'] in step_to_coeff:
            st['coeff'] = step_to_coeff[st['s']]
    return p2


def main():
    data = json.load(open(SWEEP))
    prog = A.load_microcode(0x01)
    base = conv_lambda(prog)
    print(f"BASELINE conv_lambda = {base:.7f}  ({(base-1)*1e6:+.0f} ppm)  target 0.9999899")

    # build per-param coeff tables
    params = {p['param']: p for p in data['params']}
    controls = [(0, 'LOW'), (1, 'MID'), (2, 'XOV'), (3, 'HFD')]

    results = {}
    for pidx, name in controls:
        p = params[pidx]
        ctab = {int(k): v for k, v in p['coeff_table'].items()}
        steps = sorted(ctab.keys())
        print(f"\n=== {name} (param {pidx}) coeff steps {steps} ===")
        # show the per-idx coeff for the band-split (non-comb) authority steps
        curve = []
        for idx in range(8):
            step_to_coeff = {st: ctab[st][idx] for st in steps}
            pv = set_coeffs(prog, step_to_coeff)
            lam = conv_lambda(pv)
            curve.append((idx, lam))
            # representative coeff (the primary band-split step) for display
            print(f"  idx{idx}: lambda={lam:.7f} ({(lam-1)*1e6:+.0f} ppm)  coeffs="
                  + ",".join(f"s{st}={ctab[st][idx]}" for st in steps))
        results[name] = curve

    # gap summary
    print("\n\n=== AUTHORITY SUMMARY (range of lambda over idx0..7) ===")
    for name in ('LOW', 'MID', 'XOV', 'HFD'):
        lams = [l for _, l in results[name]]
        span_ppm = (max(lams) - min(lams)) * 1e6
        print(f"  {name}: lambda {min(lams):.7f}..{max(lams):.7f}  "
              f"span={span_ppm:.0f} ppm   (idx0={lams[0]:.7f})")


if __name__ == '__main__':
    main()
