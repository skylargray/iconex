#!/usr/bin/env python3
"""Crux: is the sustain a LINEAR instability (gain trim fixes it) or a SATURATION/
overflow LIMIT CYCLE (clamping sustains it regardless of small-signal gain)?

For each eps (uniform effective-gain reduction), compare:
  - linear lambda  : float-exact power iteration (no sat) -> small-signal loop gain
  - sat decay      : saturating integer model (small impulse) -> dB/s of the envelope
If they tip below 1 / into decay at the SAME eps -> linear. If the saturating model
needs far more eps -> saturation limit cycle.
"""
import sys, os, math
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import aru_datapath as A

DMASK=A.DMASK; NATIVE_HZ=34130.0; BLK=256


def lin_lambda(prog, pick, eps, nsamp=15000, renorm=128):
    R=[0.0]*4; ACC=0.0; RES=0.0; DM=[0.0]*(DMASK+1); nz=set(); pos=0
    logg=0.0; seeded=False; g=1.0-eps
    for n in range(nsamp):
        pos=(pos+1)&DMASK
        for st in prog:
            addr=(pos-st['offset'])&DMASK
            dab=RES if st['b3'] else DM[addr]
            if not seeded and st is prog[0]: dab+=20000.0; seeded=True
            mag=abs(st['coeff']); Cs=-(mag>>1) if st['coeff']<0 else (mag>>1)
            x=R[pick(st)]; R[st['WA']]=dab
            if st['ZERO']: ACC=0.0
            ACC += x*8.0*Cs*g/64.0
            if st['XFER']: RES=ACC/8.0
            if st['b3']: DM[addr]=RES; nz.add(addr)
        if (n+1)%renorm==0:
            s=abs(ACC)+abs(RES)+sum(abs(v) for v in R)+sum(abs(DM[i]) for i in nz)+1e-30
            f=1e6/s; R=[v*f for v in R]; ACC*=f; RES*=f
            for i in nz: DM[i]*=f
            logg += -math.log(f)
    return math.exp(logg/nsamp)


def sat_decay(prog, pick, eps, nsamp=80000, imp=200):
    R=[0,0,0,0]; ACC=0; RES=0; DM=[0]*(DMASK+1); pos=0
    block=[]; env=[]; g=1.0-eps; use=(eps!=0)
    for n in range(nsamp):
        pos=(pos+1)&DMASK; esum=0
        for st in prog:
            addr=(pos-st['offset'])&DMASK
            dab=RES if st['b3'] else DM[addr]
            if n==0 and st is prog[0]: dab+=imp
            mag=abs(st['coeff']); Cs=-(mag>>1) if st['coeff']<0 else (mag>>1)
            x=R[pick(st)]; R[st['WA']]=dab
            if st['ZERO']: ACC=0
            prod=int(math.floor((x<<3)*Cs*g/64.0)) if use else (((x<<3)*Cs)>>6)
            ACC=A.sat20(ACC+prod)
            if st['XFER']: RES=A.sat16(ACC>>3)
            if st['b3']: DM[addr]=RES
            if st['XFER']: esum+=abs(RES)
        block.append(esum)
        if len(block)==BLK: env.append(math.sqrt(sum(v*v for v in block)/BLK)); block=[]
    skip=int(len(env)*0.25)
    xs=[i for i in range(skip,len(env)) if env[i]>0]
    ys=[20*math.log10(env[i]) for i in xs]
    m=len(xs); sx=sum(xs); sy=sum(ys); sxx=sum(x*x for x in xs); sxy=sum(x*y for x,y in zip(xs,ys))
    db_s=((m*sxy-sx*sy)/(m*sxx-sx*sx))*NATIVE_HZ/BLK
    return db_s, max(env)


def main():
    prog=A.load_microcode(0x01); pick=lambda st:(st['b5']<<1)|st['b4']
    print("eps      lin_lambda   sat dB/s   peakEnv   verdict")
    for eps in (0.0, 0.005, 0.01, 0.02, 0.05, 0.1, 0.2):
        lam=lin_lambda(prog,pick,eps)
        dbs,pk=sat_decay(prog,pick,eps)
        v=[]
        v.append("linGROW" if lam>1 else "linDECAY")
        v.append("satGROW" if dbs>-0.05 else "satDECAY")
        print(f"{eps:<7g} {lam:.7f}   {dbs:+8.4f}   {pk:>8.0f}  {' '.join(v)}")


if __name__ == '__main__':
    main()
