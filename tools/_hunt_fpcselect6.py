#!/usr/bin/env python3
"""ANGLE pt6 (final): does routing ONLY the TRUE minimal FPC set (1 ADC read + the
few genuine D/A output writes) fix lambda? If NOT, the 'model adds spurious DMEM
accesses the hardware skips' explanation does NOT account for +1126 ppm.

The 224X has exactly: 1 input read per channel (RD AD/) and up to 4 output writes
(OUT A-D, WR DA/) per sample = at most ~5 FPC accesses/sample (diag programs use
1 input + 1 output per channel). Identify the minimal genuine set and route only it.

Read-only.
"""
import sys, os, math
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import aru_datapath as A
DMASK=A.DMASK; PICK=lambda st:(st['b5']<<1)|st['b4']; prog=A.load_microcode(0x01)

def lam(prog, fpc, nsamp=40000, K=128, seed=1e4):
    R=[0.0]*4; ACC=0.0; RES=0.0; DM=[0.0]*(DMASK+1); pos=0
    nz=set(); seeded=False; traj=[]
    for n in range(nsamp):
        pos=(pos+1)&DMASK
        for st in prog:
            addr=(pos-st['offset'])&DMASK; is_fpc=st['s'] in fpc
            dab=0.0 if is_fpc else (RES if st['b3'] else DM[addr])
            if not seeded and st is prog[0]: dab+=seed; seeded=True
            mag=abs(st['coeff']); Cs=-(mag>>1) if st['coeff']<0 else (mag>>1)
            x=R[PICK(st)]; R[st['WA']]=dab
            if st['ZERO']: ACC=0.0
            ACC=ACC+x*8.0*Cs/64.0
            if st['XFER']: RES=ACC/8.0
            if st['b3'] and not is_fpc: DM[addr]=RES; nz.add(addr)
        if (n+1)%K==0:
            ss=math.sqrt(ACC*ACC+RES*RES+sum(v*v for v in R)+sum(DM[i]*DM[i] for i in nz))+1e-300
            traj.append(math.exp(math.log(ss)/K)); f=1.0/ss
            R=[v*f for v in R]; ACC*=f; RES*=f
            for i in nz: DM[i]*=f
    t=sorted(traj[-50:]); return t[len(t)//2]

# input read = bit15 & WA!=3 & low14==0x3FFF (base-invariant). There may be L+R.
inreads = [p['s'] for p in prog if (p['offset']&0x8000) and p['WA']!=3 and (p['offset']&0x3FFF)==0x3FFF]
# genuine D/A output writes: the diag fingerprint is WA==3, bit15, AND low14 a small
# strobe code (diag used 0x0000). The LIVE output writes go to the 4 channels; expect
# ~4. Heuristic for the *true* outputs: WA==3, bit15, b3=0 (pass-through, no feedback),
# offset near top => computed addr in the I/O window.
print(f"input-read steps (RD AD/ fingerprint)        : {inreads}")
outs_b3_0 = [p['s'] for p in prog if (p['offset']&0x8000) and p['WA']==3 and not p['b3']]
print(f"WA==3 & bit15 & b3==0 (pure pass-through out) : {outs_b3_0}  (n={len(outs_b3_0)})")
outs_b3_1 = [p['s'] for p in prog if (p['offset']&0x8000) and p['WA']==3 and p['b3']]
print(f"WA==3 & bit15 & b3==1 (writes DM in model)    : {outs_b3_1}  (n={len(outs_b3_1)})")

base = lam(prog, set())
print(f"\nbaseline                                   lambda={base:.7f} ppm={(base-1)*1e6:+.1f}")
A1 = lam(prog, set(inreads))
print(f"route input reads only                     lambda={A1:.7f} ppm={(A1-1)*1e6:+.1f}")
A2 = lam(prog, set(inreads)|set(outs_b3_0))
print(f"+ pure pass-through outputs (b3=0)         lambda={A2:.7f} ppm={(A2-1)*1e6:+.1f}")
# A realistic device has <=4 output writes. Take the 4 b3=0 WA==3 steps with the
# largest computed addr (deepest in the FPC window) as the genuine D/A writes:
def addr0(s):
    p=[p for p in prog if p['s']==s][0]; return (0 - p['offset'])&DMASK
top4 = sorted(outs_b3_0, key=lambda s:-addr0(s))[:4]
A3 = lam(prog, set(inreads)|set(top4))
print(f"+ only top-4-address b3=0 outputs {top4} lambda={A3:.7f} ppm={(A3-1)*1e6:+.1f}")

print("\nINTERPRETATION:")
print(" If a minimal, physically-plausible FPC set (<=2 reads + <=4 writes) leaves")
print(" lambda still ~+1100 ppm, then 'the model performs DMEM accesses the hardware")
print(" routes to the FPC' does NOT explain the over-unity decay. The earlier full")
print(" collapse needed routing ~28-51 b3=1 *feedback* steps (the actual tank closers)")
print(" away from DMEM, which the hardware does NOT do -- those are real comb writes.")
