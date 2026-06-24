#!/usr/bin/env python3
"""WF2c: converged lambda + param coupling for the other long halls.

Does BRIGHT/DARK/etc share CONCERT's pathology: net per-pass GAIN (lambda>1),
all-pass tank lossless, MID (param1) the sole decay control?

We reuse the float-exact linear map from exp_J_order.lam, but parametrise the
decay-param steps per program from the param_sweep json (so HFD/LOW/MID/XOV
coupling is measured against the RIGHT steps for each hall).
"""
import sys, os, json, math
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import aru_datapath as A
from exp_J_order import lam, clone, setfields

REF = os.path.join(os.path.dirname(__file__), '..', 'docs', 'reference', '224')
HALLS = [(0x01, "CONCERT"), (0x20, "BRIGHT HALL"), (0x05, "DARK HALL"),
         (0x40, "SMALL ROOM"), (0x08, "CHAMBER")]


def psteps(pid):
    with open(os.path.join(REF, f'224XL_param_sweep_{pid:02x}.json')) as f:
        sw = json.load(f)
    pp = {pr['param']: set(pr['coeff_steps']) for pr in sw['params']}
    return pp


def conv(pid):
    prog = A.load_microcode(pid)
    pp = psteps(pid)
    base = lam(prog)
    print(f"\n0x{pid:02x}  lambda = {base:.7f}  ({(base-1)*1e6:+.0f} ppm)  "
          f"{'GROW' if base>1 else 'DECAY'}")
    names = {0: 'LOW', 1: 'MID', 2: 'XOV', 3: 'HFD'}
    for p in (0, 1, 2, 3):
        steps = pp.get(p, set())
        if not steps:
            continue
        p2 = setfields(prog, {s: {'coeff': 0} for s in steps})
        d = (lam(p2) - base) * 1e6
        print(f"     {names[p]:<3} coeff->0: d {d:+.0f} ppm   (steps {sorted(steps)})")


def main():
    print("target lambda = 0.9999899 (-10 ppm, RT60 ~20s)")
    for pid, name in HALLS:
        print(f"\n{'='*60}\n{name}")
        conv(pid)


if __name__ == '__main__':
    main()
