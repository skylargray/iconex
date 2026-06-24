#!/usr/bin/env python3
"""Item 7 / decay test: the FPC INPUT-read step (CONCERT step 76, offset 0xFFFF, WA=2,
low14=0x3FFF) is the ADC port. The current model wrongly treats it as a DMEM/tank tap
(reads DMEM[pos+1]); in hardware it reads the external input (=0 when silent). If that
spurious feedback inflates the loop, removing it should drop lambda toward decay."""
import sys, os, math
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np
import exp_live as E
DMASK = E.DMASK

dd=np.load(E.NPZ); fr0=dd['frames'][0].astype(np.uint8)
def prog_with_s(img):
    p=[]
    for s in range(128):
        l0,l1,l2,l3=int(img[s*4]),int(img[s*4+1]),int(img[s*4+2]),int(img[s*4+3])
        if l2==0xFF and l3==0xFF: continue
        ctl=(~l2)&0xFF; offset=(~(l0|(l1<<8)))&0xFFFF
        coeff=(-(l3&0x7F) if l3&0x80 else (l3&0x7F))
        cs=-(abs(coeff)>>1) if coeff<0 else (abs(coeff)>>1)
        p.append(dict(s=s,offset=offset,cs=cs,coeff=coeff,ZERO=(ctl>>7)&1,b3=(ctl>>3)&1,
                      XFER=(ctl>>2)&1,WA=ctl&3,RA=(ctl>>4)&3))
    return p
b=prog_with_s(fr0)

# identify FPC steps in the live image
inp=[p['s'] for p in b if (p['offset']&0x8000) and p['WA']!=3 and (p['offset']&0x3FFF)==0x3FFF]
print(f"FPC input-read step(s) (WA!=3, low14=0x3FFF, bit15): {inp}")

def lam(prog, fpc_input_steps=(), nsamp=60000):
    R=[0.0]*4; ACC=0.0; RES=0.0; DM=[0.0]*(DMASK+1); pos=0; nz=set(); seeded=False; logs=[]
    fin=set(fpc_input_steps)
    for n in range(nsamp):
        pos=(pos+1)&DMASK
        for st in prog:
            addr=(pos-st['offset'])&DMASK
            if st['s'] in fin:
                dab=0.0          # FPC input port: external ADC, silent => 0 (NOT a DMEM tap)
            else:
                dab=RES if st['b3'] else DM[addr]
            if not seeded and st is prog[0]: dab+=1e4; seeded=True
            x=R[st['RA']]; R[st['WA']]=dab
            if st['ZERO']: ACC=0.0
            ACC=ACC+x*8.0*st['cs']/64.0
            if st['XFER']: RES=ACC/8.0
            if st['b3']: DM[addr]=RES; nz.add(addr)
        if (n+1)%128==0:
            s=math.sqrt(ACC*ACC+RES*RES+sum(v*v for v in R)+sum(DM[i]*DM[i] for i in nz))+1e-300
            logs.append(math.log(s)); f=1.0/s
            R=[v*f for v in R]; ACC*=f; RES*=f
            for i in nz: DM[i]*=f
    tail=logs[len(logs)//3:]
    return math.exp(sum(tail)/len(tail)/128)

l_old=lam(b, fpc_input_steps=())
l_new=lam(b, fpc_input_steps=inp)
print(f"\ncurrent model (step76 = DMEM tap):     lambda={l_old:.7f} ({(l_old-1)*1e6:+.1f} ppm) {'GROW' if l_old>1 else 'DECAY'}")
print(f"faithful (step76 = silent input port): lambda={l_new:.7f} ({(l_new-1)*1e6:+.1f} ppm) {'GROW' if l_new>1 else 'DECAY'}")
print(f"  delta = {(l_new-l_old)*1e6:+.1f} ppm")
