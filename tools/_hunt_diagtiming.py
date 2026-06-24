#!/usr/bin/env python3
"""Discipline gate B: a CORRECT hardware timing must keep the ZERO-DELAY diagnostic
passthrough at EXACTLY unity gain (output == input) and the .5s-DELAY line at gain ~1.

If the candidate timing (acc_latch+reg_wbr, etc.) corrupts the passthrough away from
unity, it is physically wrong regardless of what it does to CONCERT's eigenvalue.
Reuses the diagnostic WCS images from _hunt_diagunity; runs an impulse with the timing
flags applied to the SAME float datapath."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import aru_datapath as A
import _hunt_diagunity as D
DMASK = A.DMASK
PICK = D.PICK


def run_capture_timed(prog, nsamp, imp, res_latch=False, acc_latch=False,
                      reg_wbr=False, mac_pipe=False):
    """Float capture of FPC-output (WA=3,bit15) steps, with timing flags. Mirrors
    _hunt_diagunity.run_capture(mode='float') + the _hunt_timing2 flag semantics."""
    R = [0.0]*4; ACC = 0.0; RES = 0.0; RESc = 0.0; ACCc = 0.0; pend = 0.0
    DM = [0.0]*(DMASK+1); pos = 0
    in_step = A.fpc_input_step(prog)
    out_steps = [st['s'] for st in prog if st['WA'] == 3 and (st['offset'] & 0x8000)]
    out_log = {s: [] for s in out_steps}
    for n in range(nsamp):
        pos = (pos+1) & DMASK
        for st in prog:
            addr = (pos - st['offset']) & DMASK
            mag = abs(st['coeff']); Cs = -(mag>>1) if st['coeff']<0 else (mag>>1)
            cf = 8.0*Cs/64.0
            res_for_b3 = RESc if res_latch else RES
            if in_step is not None and st['s'] == in_step:
                dab = float(imp) if n == 0 else 0.0
            else:
                dab = res_for_b3 if st['b3'] else DM[addr]
            if reg_wbr:
                R[st['WA']] = dab; x = R[PICK(st)]
            else:
                x = R[PICK(st)]; R[st['WA']] = dab
            if st['ZERO']: ACC = 0.0
            if mac_pipe:
                ACC += pend; pend = x*cf
            else:
                ACC += x*cf
            xfer_src = (ACCc if acc_latch else ACC)
            if st['XFER']:
                newRES = xfer_src/8.0
                if res_latch:
                    if st['b3']: DM[addr] = res_for_b3
                    RESc = newRES; RES = newRES
                else:
                    RES = newRES
                    if st['b3']: DM[addr] = RES
            else:
                if st['b3']:
                    DM[addr] = res_for_b3 if res_latch else RES
            if acc_latch: ACCc = ACC
            if st['WA'] == 3 and (st['offset'] & 0x8000):
                out_log[st['s']].append(RES)
    return out_log, out_steps, in_step


def passthrough_gain(variant_kw):
    img = D.build_image(zero_delay=True)
    prog = D.decode(img)
    imp = 20000
    out_log, out_steps, in_step = run_capture_timed(prog, 200, imp, **variant_kw)
    gains = {}
    for s in out_steps:
        seq = out_log[s]
        nz = [(i, v) for i, v in enumerate(seq) if abs(v) > 1e-9]
        gains[s] = (nz[0][1] / imp) if nz else 0.0
    return gains


def main():
    variants = {
        'base': dict(),
        'res_latch': dict(res_latch=True),
        'acc_latch': dict(acc_latch=True),
        'reg_wbr': dict(reg_wbr=True),
        'acc_latch+reg_wbr': dict(acc_latch=True, reg_wbr=True),
        'res+acc+reg': dict(res_latch=True, acc_latch=True, reg_wbr=True),
    }
    print("=== ZERO-DELAY passthrough gain per FPC-output step (must be EXACTLY 1.0) ===\n")
    for name, kw in variants.items():
        g = passthrough_gain(kw)
        gs = "  ".join(f"s{s}:{v:+.6f}" for s, v in g.items())
        ok = all(abs(v - 1.0) < 1e-6 for v in g.values())
        print(f"  {name:20s} {gs}   {'UNITY-OK' if ok else '*** NOT UNITY ***'}")
    print("\n  Any variant marked NOT UNITY corrupts the passthrough -> physically wrong.")


if __name__ == '__main__':
    main()
