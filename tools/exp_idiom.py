#!/usr/bin/env python3
"""Test the roadmap's ARU-arithmetic hazard: rounding-toward-zero / sign-magnitude
multiply, vs our naive floor-of-signed-product.

Hardware (per the CSIGN-XOR-after-multiply finding): compute the MAGNITUDE product,
truncate toward zero (>>6 of a positive magnitude), THEN apply the combined sign.
Our model: (operand * signed_Cs) >> 6  (floor toward -inf of the signed product).
They differ by up to 1 LSB on NEGATIVE products -- floor gives larger magnitude.
On a sign-alternating mode this is the difference between sustaining and damping.

Measure the integer model's decay (block-RMS EDC -> RT60) under each idiom, at a
moderate impulse, and the structural growth via small-signal slope.
"""
import sys, os, math
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import aru_datapath as A
DMASK=A.DMASK; NATIVE=34130.0; BLK=512


def mul_floor(op, Cs):                 # current model
    return (op * Cs) >> 6

def mul_sm(op, Cs):                    # sign-magnitude: truncate magnitude toward zero, then sign
    mag = (abs(op) * abs(Cs)) >> 6
    neg = (op < 0) ^ (Cs < 0)
    return -mag if neg else mag

def res_floor(acc):                    # current: floor >>3
    return acc >> 3

def res_sm(acc):                       # toward-zero >>3
    return acc >> 3 if acc >= 0 else -((-acc) >> 3)


def run(prog, pick, nsamp, imp, mulfn, resfn):
    R=[0,0,0,0]; ACC=0; RES=0; DM=[0]*(DMASK+1); pos=0
    block=[]; env=[]
    for n in range(nsamp):
        pos=(pos+1)&DMASK; esum=0
        for st in prog:
            addr=(pos-st['offset'])&DMASK
            dab=RES if st['b3'] else DM[addr]
            if n==0 and st is prog[0]: dab+=imp
            mag=abs(st['coeff']); Cs=-(mag>>1) if st['coeff']<0 else (mag>>1)
            x=R[pick(st)]; R[st['WA']]=dab
            if st['ZERO']: ACC=0
            ACC=A.sat20(ACC + mulfn(x<<3, Cs))
            if st['XFER']: RES=A.sat16(resfn(ACC))
            if st['b3']: DM[addr]=RES
            if st['XFER']: esum+=abs(RES)
        block.append(esum)
        if len(block)==BLK: env.append(math.sqrt(sum(v*v for v in block)/BLK)); block=[]
    return env


def analyze(env):
    pk=max(env); npk=env.index(pk)
    lo=npk+max(1,(len(env)-npk)//8)
    xs=[i for i in range(lo,len(env)) if env[i]>0]
    if len(xs)<8: return pk,npk,None,None
    ys=[20*math.log10(env[i]) for i in xs]
    m=len(xs);sx=sum(xs);sy=sum(ys);sxx=sum(x*x for x in xs);sxy=sum(x*y for x,y in zip(xs,ys))
    dbblk=(m*sxy-sx*sy)/(m*sxx-sx*sx); dbs=dbblk*NATIVE/BLK
    rt=(-60.0/dbs) if dbs<-1e-3 else float('inf')
    return pk,npk,dbs,rt


def main():
    nsamp=int(sys.argv[1]) if len(sys.argv)>1 else 120000
    prog=A.load_microcode(0x01); pick=lambda st:(st['b5']<<1)|st['b4']
    print(f"nsamp={nsamp} ({nsamp/NATIVE:.1f}s). Comparing multiply/result idioms.\n")
    variants=[("floor/floor (CURRENT)", mul_floor, res_floor),
              ("sign-mag mul / floor res", mul_sm, res_floor),
              ("floor mul / toward0 res", mul_floor, res_sm),
              ("sign-mag mul / toward0 res", mul_sm, res_sm)]
    for imp in (2000, 20000):
        print(f"impulse={imp}:")
        for name,mf,rf in variants:
            env=run(prog,pick,nsamp,imp,mf,rf)
            pk,npk,dbs,rt=analyze(env)
            rts='SUSTAIN/GROW' if (rt is None or rt==float('inf')) else f'{rt:.2f}s'
            dss=f'{dbs:+.3f}' if dbs is not None else 'n/a'
            print(f"  {name:<28} peak={pk:>7.0f}@{npk:<4} dB/s={dss:>8} RT60={rts}")
        print()


if __name__ == '__main__':
    main()
