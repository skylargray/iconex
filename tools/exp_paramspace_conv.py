#!/usr/bin/env python3
"""Param-space lambda sweep using the CONVERGED measurement (exp_lambda_clean),
correcting exp_paramspace.py which used a non-converged nsamp=8000 power_iter.

Reports converged structural lambda (proper L2 norm, tail of a long run) for the
key parameter settings. Tells us the TRUE gain landscape: which settings actually
cross unity, and how far the default (idx0) really is from decaying.
"""
import sys, os, json
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import aru_datapath as A
from exp_lambda_clean import lambda_trajectory

SW = json.load(open(os.path.join(os.path.dirname(__file__),
               '..', 'docs', 'reference', '224', '224XL_param_sweep_01.json')))
TBL = {}
for p in SW['params']:
    TBL[p['param']] = {int(k): v for k, v in p['coeff_table'].items()}
LBL = {0: 'LOW', 1: 'MID', 2: 'XOV', 3: 'HFD', 4: 'DEP'}


def apply(prog, settings):
    out = [dict(p) for p in prog]
    bystep = {p['s']: p for p in out}
    for par, idx in settings.items():
        for step, vals in TBL.get(par, {}).items():
            if step in bystep:
                bystep[step]['coeff'] = vals[idx]
    return out


def conv_lambda(prog, settings, nsamp=42000, K=128, tail=40):
    p2 = apply(prog, settings)
    traj = lambda_trajectory(p2, nsamp=nsamp, K=K)
    vals = sorted(l for _, l in traj[-tail:])
    return vals[len(vals)//2]


def main():
    prog = A.load_microcode(0x01)
    settings = [
        ("baseline idx0 (DEFAULT)", {}),
        ("MID idx7 (max)", {1: 7}),
        ("XOV idx6", {2: 6}),
        ("HFD idx7", {3: 7}),
        ("DEP idx7", {4: 7}),
        ("LOW idx7", {0: 7}),
        ("all-damping idx7", {0: 7, 1: 7, 2: 7, 3: 7, 4: 7}),
        ("all params idx3", {0: 3, 1: 3, 2: 3, 3: 3, 4: 3}),
    ]
    print("CONVERGED structural lambda (proper L2 norm, tail of 42k-sample run)")
    print("target = 0.9999899\n")
    print(f"  {'setting':30} {'lambda':>11}   verdict")
    for name, s in settings:
        lam = conv_lambda(prog, s)
        print(f"  {name:30} {lam:.7f}   {'GROW' if lam>1 else 'DECAY'} ({(lam-1)*1e6:+.0f} ppm)")


if __name__ == '__main__':
    main()
