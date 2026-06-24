#!/usr/bin/env python3
"""Reliable per-step sensitivity: seed the STATE (R/RES/DMEM) before iterating instead of
injecting at step 0, so zeroing the early output taps (0/1) doesn't disrupt the seed (which
made the first sweep mis-rank steps 0/1). Confirms where the unstable mode REALLY lives."""
import sys, os, math
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np
import exp_live as E
DMASK = E.DMASK

def lam(prog, nsamp=45000):
    # seed state independent of prog order: small energy in registers + RES + a few DMEM cells
    R=[1.0,1.0,1.0,1.0]; ACC=0.0; RES=1.0; DM=[0.0]*(DMASK+1); pos=0
    nz=set()
    for st in prog:                              # pre-seed every b3 write address so the loop is excited
        if st['b3']:
            a=(0-st['offset'])&DMASK; DM[a]=1.0; nz.add(a)
    logs=[]
    for n in range(nsamp):
        pos=(pos+1)&DMASK
        for st in prog:
            addr=(pos-st['offset'])&DMASK
            dab=RES if st['b3'] else DM[addr]
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
lb=lam(b)
print(f"baseline (state-seeded) lambda={lb:.7f} ({(lb-1)*1e6:+.1f} ppm)")

def zero(steps):
    p=[dict(st) for st in b]
    for st in p:
        if st['s'] in steps: st['cs']=0
    return lam(p)

for label, S in [("steps 0,1 (output taps)", {0,1}), ("step 1 only", {1}),
                 ("MOD taps 56/57/107/108", {56,57,107,108}),
                 ("closer 69", {69}), ("closer 46", {46}), ("closer 54", {54})]:
    lm=zero(S); print(f"  zero {label:26}: lambda={lm:.7f} dlam={(lm-lb)*1e6:+9.1f} ppm")

# full reliable top-15
print("\nreliable top-15 by |dlam| (state-seeded, nsamp=30000):")
sens=[]
for st in b:
    if st['cs']==0: continue
    p=[dict(x) for x in b]
    for x in p:
        if x['s']==st['s']: x['cs']=0
    lm=lam(p, nsamp=30000)
    sens.append((abs(lm-lb), st['s'], (lm-lb)*1e6, st['cs'], st['b3'], st['XFER']))
sens.sort(reverse=True)
for ad,s,dl,cs,b3,xf in sens[:15]:
    print(f"  step {s:3d}: dlam={dl:+9.1f} ppm  (cs={cs:+3d} b3={b3} XFER={xf})")
