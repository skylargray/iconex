#!/usr/bin/env python3
"""Mechanism test (encoding-safe): does the unstable mode have support on the modulated
taps? Perturb/remove them in the static frame0 float map and measure the lambda shift.
Contrast with the in-loop HF-damp taps (40/41/92/93 = manual 'Treble Decay')."""
import sys, os, math
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np
import exp_live as E

DMASK = E.DMASK

def lam_static(prog, nsamp=80000):
    R=[0.0]*4; ACC=0.0; RES=0.0; DM=[0.0]*(DMASK+1); pos=0; nz=set(); seeded=False; logs=[]
    for n in range(nsamp):
        pos=(pos+1)&DMASK
        for j,st in enumerate(prog):
            addr=(pos-st['offset'])&DMASK
            dab=RES if st['b3'] else DM[addr]
            if not seeded and j==0: dab+=1e4; seeded=True
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
        p.append(dict(s=s,offset=offset,cs=cs,ZERO=(ctl>>7)&1,b3=(ctl>>3)&1,XFER=(ctl>>2)&1,WA=ctl&3,RA=(ctl>>4)&3))
    return p

b=prog_with_s(fr0)
lb=lam_static(b)
print(f"baseline frame0:             lambda={lb:.7f} ({(lb-1)*1e6:+.1f} ppm)")

def run_mut(label, mut):
    p=[dict(st) for st in b]
    mut(p)
    lm=lam_static(p)
    print(f"  {label:30}: lambda={lm:.7f} ({(lm-1)*1e6:+.1f} ppm)  dlam={(lm-lb)*1e6:+.1f} ppm")

MOD={56,57,107,108}; HFD={40,41,92,93}
run_mut("MOD taps cs->0", lambda p:[st.update(cs=0) for st in p if st['s'] in MOD])
run_mut("MOD taps offset +40", lambda p:[st.update(offset=(st['offset']+40)&0xFFFF) for st in p if st['s'] in MOD])
run_mut("MOD taps offset -40", lambda p:[st.update(offset=(st['offset']-40)&0xFFFF) for st in p if st['s'] in MOD])
run_mut("HFD taps(40/41/92/93) cs->0", lambda p:[st.update(cs=0) for st in p if st['s'] in HFD])
run_mut("HFD taps cs*0.5 (more damp)", lambda p:[st.update(cs=int(st['cs']*0.5)) for st in p if st['s'] in HFD])
run_mut("HFD taps cs*1.5 (less damp)", lambda p:[st.update(cs=int(st['cs']*1.5)) for st in p if st['s'] in HFD])

# per-step sensitivity: zero each active step's cs, rank by |dlam| to locate the mode
if len(sys.argv) > 1 and sys.argv[1] == 'sweep':
    print("\ntop-20 steps by |dlam| when their cs is zeroed (where the unstable mode lives):", flush=True)
    sens=[]
    for st in b:
        if st['cs']==0: continue
        p=[dict(x) for x in b]
        for x in p:
            if x['s']==st['s']: x['cs']=0
        lm=lam_static(p, nsamp=24000)
        sens.append((abs(lm-lb), st['s'], (lm-lb)*1e6, st['cs'], st['offset']))
    sens.sort(reverse=True)
    for ad,s,dl,cs,off in sens[:20]:
        print(f"  step {s:3d}: dlam={dl:+9.1f} ppm  (cs={cs:+3d} off={off})", flush=True)
