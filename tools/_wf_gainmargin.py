#!/usr/bin/env python3
"""Gain-margin probe: how far is the CONCERT loop from unity, and is the +1126 ppm a
plausible single systematic (global coeff scale) or step-1-specific? Sweep (a) a global
cs scale and (b) step-1's cs, find where the float lambda crosses 1.0."""
import sys, os, math
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np
import exp_live as E
DMASK = E.DMASK

def lam(prog, nsamp=50000):
    R=[0.0]*4; ACC=0.0; RES=0.0; DM=[0.0]*(DMASK+1); pos=0; nz=set(); seeded=False; logs=[]
    for n in range(nsamp):
        pos=(pos+1)&DMASK
        for j,st in enumerate(prog):
            addr=(pos-st['offset'])&DMASK
            dab=RES if st['b3'] else DM[addr]
            if not seeded and j==0: dab+=1e4; seeded=True
            x=R[st['RA']]; R[st['WA']]=dab
            if st['ZERO']: ACC=0.0
            ACC=ACC+x*8.0*st['csf']/64.0     # csf = float coeff (allow fractional scaling)
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
        p.append(dict(s=s,offset=offset,cs=cs,csf=float(cs),coeff=coeff,
                      ZERO=(ctl>>7)&1,b3=(ctl>>3)&1,XFER=(ctl>>2)&1,WA=ctl&3,RA=(ctl>>4)&3))
    return p
b=prog_with_s(fr0)

print("decoded fields of the mode-critical steps:")
crit={0,1,2,60,69,70,96}
for st in b:
    if st['s'] in crit:
        print(f"  step {st['s']:3d}: coeff7={st['coeff']:+4d} cs={st['cs']:+3d} off={st['offset']:5d} "
              f"Z={st['ZERO']} X={st['XFER']} b3={st['b3']} WA={st['WA']} RA={st['RA']}")

lb=lam(b)
print(f"\nbaseline lambda={lb:.7f} ({(lb-1)*1e6:+.1f} ppm)")

# (a) GLOBAL coeff scale -> find critical scale where lambda crosses 1
print("\nglobal cs-scale sweep (uniform multiplicative gain on ALL coeffs):")
for g in (1.0, 0.999, 0.998, 0.997, 0.996, 0.995, 0.99, 0.98):
    p=[dict(st) for st in b]
    for st in p: st['csf']=st['cs']*g
    lm=lam(p)
    print(f"  scale={g:.3f}: lambda={lm:.7f} ({(lm-1)*1e6:+.1f} ppm) {'GROW' if lm>1 else 'DECAY'}")

# (b) step-1 cs sweep
print("\nstep-1 cs sweep (its decoded cs=-5; what value gives unity?):")
for c1 in (-5.0, -4.8, -4.6, -4.4, -4.2, -4.0, -3.5, -3.0):
    p=[dict(st) for st in b]
    for st in p:
        if st['s']==1: st['csf']=c1
    lm=lam(p)
    print(f"  step1 cs={c1:+.1f}: lambda={lm:.7f} ({(lm-1)*1e6:+.1f} ppm) {'GROW' if lm>1 else 'DECAY'}")
