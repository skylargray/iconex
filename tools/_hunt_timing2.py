#!/usr/bin/env python3
"""LEAD 2 part 2: systematic timing-DOF map (flag-based), singles + coherent combos.

_hunt_timing found the RES result-register latch (74F374 latches at cycle-end edge)
HALVES the excess: +1126 -> +564 ppm. That is the single most plausible 1-microstep
pipeline change. Here we model each datapath latch as a flag and sweep independent +
combined settings to locate which PHYSICALLY-COHERENT timing makes lambda ~ 1.0.

Synchronous-hardware reality: each microstep is one clock edge. A latch flagged True
means "this element latches at the cycle-end edge, so within the cycle reads see the
PREVIOUS cycle's value":
  res_latch : result register RES (74F374, XFER CK) is one microstep behind for b3 read/write.
  acc_latch : the accumulator sum is available to XFER only one microstep later.
  reg_wbr   : register file is WRITE-before-read in a cycle (pick==WA sees new dab).
              (model assumes read-before-write; LS670 timing question, DAB WSTB/.)
  mac_pipe  : multiplier product register (ARUCK) is one cycle behind (product N -> acc N+1).
Only physically-coherent combos are reported; mac_pipe collapses the loop (dead tank)
so it is shown but flagged.
"""
import sys, os, math, itertools
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import aru_datapath as A
DMASK = A.DMASK
PICK = lambda st: (st['b5'] << 1) | st['b4']


def lam(prog, res_latch=False, acc_latch=False, reg_wbr=False, mac_pipe=False,
        nsamp=40000, K=128, seed=1e4):
    R = [0.0]*4; ACC = 0.0; RES = 0.0
    DM = [0.0]*(DMASK+1); pos = 0
    nz = set(); seeded = False; traj = []
    RESc = 0.0          # committed (latched) RES if res_latch
    ACCc = 0.0          # committed ACC visible to XFER if acc_latch
    pend = 0.0          # pipelined product if mac_pipe
    for n in range(nsamp):
        pos = (pos+1) & DMASK
        for st in prog:
            addr = (pos - st['offset']) & DMASK
            mag = abs(st['coeff']); Cs = -(mag>>1) if st['coeff']<0 else (mag>>1)
            cf = 8.0*Cs/64.0
            res_for_b3 = RESc if res_latch else RES

            dab = res_for_b3 if st['b3'] else DM[addr]
            if not seeded and st is prog[0]: dab += seed; seeded = True

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
                    if st['b3']: DM[addr] = res_for_b3; nz.add(addr)   # write OLD latched RES
                    RESc = newRES                                       # latch -> next step
                    RES = newRES
                else:
                    RES = newRES
                    if st['b3']: DM[addr] = RES; nz.add(addr)
            else:
                if st['b3']:
                    DM[addr] = res_for_b3 if res_latch else RES; nz.add(addr)
            if acc_latch:
                ACCc = ACC

        if (n+1) % K == 0:
            s = math.sqrt(ACC*ACC + RES*RES + RESc*RESc + ACCc*ACCc + pend*pend
                          + sum(v*v for v in R) + sum(DM[i]*DM[i] for i in nz)) + 1e-300
            traj.append(math.exp(math.log(s)/K))
            f = 1.0/s
            R = [v*f for v in R]; ACC*=f; RES*=f; RESc*=f; ACCc*=f; pend*=f
            for i in nz: DM[i] *= f
    tail = sorted(traj[-60:])
    return tail[len(tail)//2]


def main():
    prog = A.load_microcode(0x01)
    flags = ['res_latch','acc_latch','reg_wbr','mac_pipe']
    combos = [dict()]                                  # base
    for f in flags: combos.append({f: True})           # singles
    # coherent pairs (skip mac_pipe pairs except with res_latch, since mac alone kills loop)
    for a,b in itertools.combinations(['res_latch','acc_latch','reg_wbr'], 2):
        combos.append({a: True, b: True})
    combos.append({'res_latch': True, 'acc_latch': True, 'reg_wbr': True})
    combos.append({'res_latch': True, 'mac_pipe': True})

    print("=== timing-DOF lambda map (target 0.9999899; base ~1.0011266) ===\n")
    base = lam(prog)
    for c in combos:
        l = lam(prog, **c)
        name = '+'.join(k for k in c) or 'base'
        verdict = 'GROW' if l > 1 else 'DECAY'
        print(f"  {name:32s} lambda={l:.7f}  ({(l-1)*1e6:+9.1f} ppm, {verdict})"
              f"   d(base)={(l-base)*1e6:+9.1f}")
    print("\n  Coherent combo nearest lambda=1.0 (without collapsing to the dead-tank 0.0045)")
    print("  is the timing hypothesis to confirm on the schematic.")


if __name__ == '__main__':
    main()
