#!/usr/bin/env python3
"""Does a small systematic gain reduction yield a CLEAN exponential decay when the
signal never saturates? Run with a SMALL impulse + effective-gain x(1-eps); measure
whether energy decays exponentially (and RT60) without hitting the sat rails.
"""
import sys, os, math
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import aru_datapath as A

DMASK=A.DMASK; NATIVE_HZ=34130.0; BLK=256


def run(prog, pick, nsamp, imp, eps):
    R=[0,0,0,0]; ACC=0; RES=0; DM=[0]*(DMASK+1); pos=0
    block=[]; env=[]; satcount=0; g=1.0-eps
    for n in range(nsamp):
        pos=(pos+1)&DMASK; esum=0
        for st in prog:
            addr=(pos-st['offset'])&DMASK
            dab=RES if st['b3'] else DM[addr]
            if n==0 and st is prog[0]: dab+=imp
            mag=abs(st['coeff']); Cs=-(mag>>1) if st['coeff']<0 else (mag>>1)
            x=R[pick(st)]; R[st['WA']]=dab
            if st['ZERO']: ACC=0
            prod = (((x<<3)*Cs)>>6) if eps==0 else int(math.floor((x<<3)*Cs*g/64.0))
            a=ACC+prod
            if a>524287 or a<-524287: satcount+=1
            ACC=A.sat20(a)
            if st['XFER']:
                r=ACC>>3
                if r>32767 or r<-32768: satcount+=1
                RES=A.sat16(r)
            if st['b3']: DM[addr]=RES
            if st['XFER']: esum+=abs(RES)
        block.append(esum)
        if len(block)==BLK:
            env.append(math.sqrt(sum(v*v for v in block)/BLK)); block=[]
    return env, satcount


def rt60(env):
    skip=int(len(env)*0.2)
    xs=[i for i in range(skip,len(env)) if env[i]>0]
    if len(xs)<8: return None,None
    ys=[20*math.log10(env[i]) for i in xs]
    m=len(xs); sx=sum(xs); sy=sum(ys); sxx=sum(x*x for x in xs); sxy=sum(x*y for x,y in zip(xs,ys))
    db_blk=(m*sxy-sx*sy)/(m*sxx-sx*sx); db_s=db_blk*NATIVE_HZ/BLK
    return db_s, ((-60.0/db_s) if db_s<-1e-4 else float('inf'))


def main():
    nsamp=int(sys.argv[1]) if len(sys.argv)>1 else 120000
    prog=A.load_microcode(0x01); pick=lambda st:(st['b5']<<1)|st['b4']
    print(f"Small-impulse decay test, nsamp={nsamp} ({nsamp/NATIVE_HZ:.1f}s)\n")
    for imp in (50, 500):
        print(f"impulse={imp}:")
        for eps in (0.0, 1e-4, 3e-4, 1e-3, 2e-3, 3e-3, 5e-3):
            env,sat=run(prog,pick,nsamp,imp,eps)
            dbs,rt=rt60(env)
            rts="SUSTAIN/GROW" if rt==float('inf') else (f"{rt:.2f}s" if rt else "n/a")
            dss=f"{dbs:+.4f}" if dbs is not None else "n/a"
            print(f"  eps={eps:<6g} peakEnv={max(env):>8.0f} sat_events={sat:<7} dB/s={dss:>9} RT60={rts}")
        print()


if __name__ == '__main__':
    main()
