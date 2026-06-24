#!/usr/bin/env python3
"""HFD = Treble Decay reframe test (Session 4).

Owner's manual + block diagram Fig 4.1 prove the CONCERT page-1 slider 4 ("HFD" in
the firmware = "HF Decay" = "Treble Decay") is an IN-LOOP air-absorption HF damping,
NOT the HF Bandwidth input filter (that is a separate page-2 slider, "HFB").
The param sweep maps HFD -> coeff steps 40,41,92,93.

This script:
  1. Measures converged structural lambda (proper L2 norm, exp_lambda_clean method).
  2. HFD coupling: zero / scale / idx7 the HFD steps and see if lambda moves at all.
  3. XOV / LOW / MID comparison.
  4. Static structure dump of the band-split region (steps ~37-46, 89-98):
     ZERO-group boundaries, b3 write-backs (closers), and the actual DMEM tap
     addresses each reads/writes -- to localise where HFD's contribution goes.
"""
import sys, os, math
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import aru_datapath as A
from exp_lambda_clean import lambda_trajectory

HFD_STEPS = [40, 41, 92, 93]
XOV_STEPS = [45, 46, 97, 98]
LOW_STEPS = [43, 95]
MID_STEPS = [44, 96]


def conv_lambda(prog, nsamp=30000, K=128, tail=40):
    traj = lambda_trajectory(prog, nsamp=nsamp, K=K)
    vals = sorted(l for _, l in traj[-tail:])
    return vals[len(vals) // 2]


def clone(prog):
    return [dict(p) for p in prog]


def set_coeff(prog, steps, fn):
    p2 = clone(prog)
    for st in p2:
        if st['s'] in steps:
            st['coeff'] = fn(st['coeff'])
    return p2


def main():
    prog = A.load_microcode(0x01)
    base = conv_lambda(prog)
    print(f"target lambda = 0.9999899")
    print(f"baseline (default)               lambda={base:.7f}  ({(base-1)*1e6:+.0f} ppm)\n")

    print("=== HFD (Treble Decay) coupling test: steps 40,41,92,93 ===")
    for name, fn in [
        ("HFD coeff -> 0 (remove)",          lambda c: 0),
        ("HFD coeff x0.5",                    lambda c: int(c * 0.5)),
        ("HFD coeff x2 (stronger)",           lambda c: max(-127, min(127, c * 2))),
        ("HFD coeff -> idx7 extreme",         None),   # handled below
    ]:
        if fn is None:
            # idx7 from the sweep: step40/92 -> -127, step41/93 -> -124
            p2 = clone(prog)
            for st in p2:
                if st['s'] in (40, 92): st['coeff'] = -127
                if st['s'] in (41, 93): st['coeff'] = -124
        else:
            p2 = set_coeff(prog, HFD_STEPS, fn)
        lam = conv_lambda(p2)
        print(f"  {name:32} lambda={lam:.7f}  ({(lam-1)*1e6:+.0f} ppm)  d={ (lam-base)*1e6:+.0f} ppm")

    print("\n=== comparison: XOV / LOW / MID coeff->0 ===")
    for name, steps in [("XOV->0 (45,46,97,98)", XOV_STEPS),
                        ("LOW->0 (43,95)", LOW_STEPS),
                        ("MID->0 (44,96)", MID_STEPS)]:
        p2 = set_coeff(prog, steps, lambda c: 0)
        lam = conv_lambda(p2)
        print(f"  {name:32} lambda={lam:.7f}  ({(lam-1)*1e6:+.0f} ppm)  d={(lam-base)*1e6:+.0f} ppm")

    print("\n=== band-split region structure (steps 37-47, 89-99) ===")
    print(f"  {'S':>3} {'offset':>6} {'addr-pos':>8} {'coeff':>6} {'WA':>2} {'RA':>2} "
          f"{'b3':>2} {'XF':>2} {'ZR':>2}   role")
    bystep = {p['s']: p for p in prog}
    for s in list(range(37, 48)) + list(range(89, 100)):
        st = bystep.get(s)
        if st is None:
            print(f"  {s:>3}  (NOP/inactive)")
            continue
        # addr relative to position: addr = pos - offset; print as signed delta mod 65536
        d = (-st['offset']) & 0xFFFF
        d_signed = d - 65536 if d > 32768 else d
        role = []
        if st['ZERO']: role.append("ZERO-open")
        if st['XFER']: role.append("XFER")
        if st['b3']: role.append("b3-writeback(closer)")
        else: role.append("read")
        if s in HFD_STEPS: role.append("<<HFD/TrebleDecay")
        if s in XOV_STEPS: role.append("<<XOV")
        if s in LOW_STEPS: role.append("<<LOW")
        if s in MID_STEPS: role.append("<<MID")
        print(f"  {s:>3} {st['offset']:>6} {d_signed:>8} {st['coeff']:>6} {st['WA']:>2} "
              f"{(st['b5']<<1)|st['b4']:>2} {st['b3']:>2} {st['XFER']:>2} {st['ZERO']:>2}   "
              f"{' '.join(role)}")


if __name__ == '__main__':
    main()
