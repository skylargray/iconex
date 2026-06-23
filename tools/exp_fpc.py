#!/usr/bin/env python3
"""Test the FPC-I/O modeling discrepancy's effect on loop gain.

Both aru_datapath.py and 224xl.hpp treat EVERY step as a plain DMEM access. But
per tech-ref doc 12, steps with offset bit15 set are FPC analog I/O, not DMEM:
  - INPUT read  : bit15 set, low14 == 0x3FFF, WA==2  -> reads the external ADC.
  - OUTPUT write: bit15 set, WA==3                   -> writes the external DAC.
In the homogeneous (eigenvalue / no-external-input) analysis the ADC input is 0.
The model instead reads DMEM[pos-0xFFFF]=DMEM[pos+1] for the input step -> a
SPURIOUS feedback tap that the hardware does not have. This script identifies the
FPC steps in the live CONCERT WCS and measures the converged structural lambda
with the FPC input steps correctly sourced as 0 (and optionally the FPC output
steps not driving the register from DMEM).
"""
import sys, os, math
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import aru_datapath as A

DMASK = A.DMASK
PICK = lambda st: (st['b5'] << 1) | st['b4']


def classify(prog):
    fin, fout = [], []
    for p in prog:
        off = p['offset']
        if off & 0x8000:
            if (off & 0x3FFF) == 0x3FFF and p['WA'] == 2:
                fin.append(p['s'])
            elif p['WA'] == 3:
                fout.append(p['s'])
    return fin, fout


def conv_lambda(prog, fpc_in=(), fpc_out=(), nsamp=44000, K=128, tail=40, seed=1e4):
    """Float-exact linear map; if a step is an FPC input, source dab=0 (external
    input is 0 in the homogeneous mode); if an FPC output, the result leaves the
    system (model it as a normal DMEM access UNLESS in fpc_out, then dab=0 too)."""
    fin = set(fpc_in); fout = set(fpc_out)
    R = [0.0]*4; ACC = 0.0; RES = 0.0
    DM = [0.0]*(DMASK+1); pos = 0; nz = set(); seeded = False
    traj = []
    for n in range(nsamp):
        pos = (pos+1) & DMASK
        for st in prog:
            addr = (pos - st['offset']) & DMASK
            if st['s'] in fin or st['s'] in fout:
                dab = 0.0                          # external I/O, no DMEM feedback
            elif st['b3']:
                dab = RES
            else:
                dab = DM[addr]
            if not seeded and st is prog[0]:
                dab += seed; seeded = True
            mag = abs(st['coeff']); Cs = -(mag>>1) if st['coeff']<0 else (mag>>1)
            x = R[PICK(st)]; R[st['WA']] = dab
            if st['ZERO']: ACC = 0.0
            ACC = ACC + x*8.0*Cs/64.0
            if st['XFER']: RES = ACC/8.0
            if st['b3']: DM[addr] = RES; nz.add(addr)
        if (n+1) % K == 0:
            s = math.sqrt(ACC*ACC + RES*RES + sum(v*v for v in R)
                          + sum(DM[i]*DM[i] for i in nz)) + 1e-300
            traj.append((n+1, math.exp(math.log(s)/K)))
            f = 1.0/s; R = [v*f for v in R]; ACC*=f; RES*=f
            for i in nz: DM[i]*=f
    vals = sorted(l for _, l in traj[-tail:])
    return vals[len(vals)//2]


def main():
    prog = A.load_microcode(0x01)
    fin, fout = classify(prog)
    print(f"FPC input-read steps (bit15, low14=0x3FFF, WA=2): {fin}")
    print(f"FPC output-write steps (bit15, WA=3):            {fout}")
    for p in prog:
        if p['s'] in fin or p['s'] in fout:
            print(f"   s{p['s']:<3} offset=0x{p['offset']:04x} coeff={p['coeff']} "
                  f"WA={p['WA']} RA={PICK(p)} b3={p['b3']} XFER={p['XFER']} "
                  f"role={'INPUT' if p['s'] in fin else 'OUTPUT'}")
    print()
    base = conv_lambda(prog)
    print(f"baseline (FPC steps as DMEM, current model):   lambda={base:.7f} ({(base-1)*1e6:+.0f} ppm)")
    li = conv_lambda(prog, fpc_in=fin)
    print(f"FPC INPUT steps sourced as 0 (hardware-faithful): lambda={li:.7f} ({(li-1)*1e6:+.0f} ppm)")
    lio = conv_lambda(prog, fpc_in=fin, fpc_out=fout)
    print(f"FPC INPUT+OUTPUT steps as external I/O:         lambda={lio:.7f} ({(lio-1)*1e6:+.0f} ppm)")
    print(f"\ntarget lambda = 0.9999899 (-10 ppm)")


if __name__ == '__main__':
    main()
