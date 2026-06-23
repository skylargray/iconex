#!/usr/bin/env python3
"""Full parameter-space structural-lambda sweep.

exp_slider only swept MID and LOW+MID. This sweeps EVERY CONCERT parameter
(LOW MID XOV HFD DEP) individually across its 8 characterized slider points and
several joint combinations, measuring the clean float-exact structural lambda
(exp_eig.power_iter) at each. Question: can ANY reachable parameter setting bring
the model to a clean decaying lambda (~0.99999, the P85 20 s target)? If yes, the
deficit may be a parameter/boot-state issue; if no (model stays >1 or only decays
at extreme/implausible settings), the deficit is structural/arithmetic.

idx0 == booted default (verified == param-sweep idx0). Slider positions below 0x20
clamp to idx0 per the characterized tables.
"""
import sys, os, json
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import aru_datapath as A
from exp_eig import power_iter

LBL = {0: 'LOW', 1: 'MID', 2: 'XOV', 3: 'HFD', 4: 'DEP'}
SW = json.load(open(os.path.join(os.path.dirname(__file__),
               '..', 'docs', 'reference', '224', '224XL_param_sweep_01.json')))
TBL = {}   # param -> {step:[8 vals]}
for p in SW['params']:
    TBL[p['param']] = {int(k): v for k, v in p['coeff_table'].items()}

PICK = lambda st: (st['b5'] << 1) | st['b4']


def apply(prog, settings):
    """settings: dict param_idx -> slider index 0..7. Returns modified prog copy."""
    out = [dict(p) for p in prog]
    bystep = {p['s']: p for p in out}
    for par, idx in settings.items():
        for step, vals in TBL.get(par, {}).items():
            if step in bystep:
                bystep[step]['coeff'] = vals[idx]
    return out


def lam_of(prog, settings, nsamp=8000):
    p2 = apply(prog, settings)
    lam, _ = power_iter(p2, PICK, nsamp=nsamp)
    return lam


def main():
    prog = A.load_microcode(0x01)
    base, _ = power_iter(prog, PICK, nsamp=8000)
    print(f"baseline (idx0 default) lambda = {base:.7f}  ({'GROW' if base>1 else 'DECAY'})")
    print("target = 0.9999899\n")

    print("== individual parameter sweeps (idx0..7) ==")
    for par in (0, 1, 2, 3, 4):
        row = []
        for idx in range(8):
            lam = lam_of(prog, {par: idx})
            row.append(f"{lam:.5f}")
        print(f"  {LBL[par]:3} (p{par}): " + "  ".join(row))

    print("\n== joint combos ==")
    combos = [
        ("all damping max (LOW MID XOV HFD DEP =7)", {0:7,1:7,2:7,3:7,4:7}),
        ("MID+HFD max", {1:7,3:7}),
        ("MID+XOV max", {1:7,2:7}),
        ("HFD max only", {3:7}),
        ("HFD idx6", {3:6}),
        ("MID+HFD+XOV idx4 (mid-scale)", {1:4,2:4,3:4}),
        ("all params idx3", {0:3,1:3,2:3,3:3,4:3}),
    ]
    for name, s in combos:
        lam = lam_of(prog, s)
        print(f"  {name:42}: lambda={lam:.7f}  ({'GROW' if lam>1 else 'DECAY'})")


if __name__ == '__main__':
    main()
