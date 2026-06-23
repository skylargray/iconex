#!/usr/bin/env python3
"""#2: LIVE (continuously-swept) chorus modulation of the CONCERT tank.

Unlike the earlier STATIC detune test (which froze each modulated tap at a fixed
offset and found lambda unmoved), this sweeps the modulated taps' delays every
sample with a triangle LFO and reads them with fractional (linear) interpolation.
A time-varying delay is parametric, not LTI -- it can decorrelate a frozen-unstable
mode in ways a static offset cannot. We measure the saturating integer model's
energy-envelope decay (EDC) under live modulation.

Modulated steps (CONCERT): 56,57 (pair A) and 107,108 (pair B), anti-phase.
"""
import sys, os, math
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import aru_datapath as A

DMASK = A.DMASK; NATIVE_HZ = 34130.0; BLK = 512
PAIR_A = {56, 57}; PAIR_B = {107, 108}


def triangle(n, period, depth):
    ph = (n % period) / period
    tri = (4*ph - 1) if ph < 0.5 else (3 - 4*ph)    # -1..+1..-1
    return tri * depth                               # float, fractional


def run_live(prog, pick, nsamp, imp, depth, period):
    R=[0,0,0,0]; ACC=0; RES=0; DM=[0]*(DMASK+1); pos=0
    block=[]; env=[]
    for n in range(nsamp):
        pos=(pos+1)&DMASK
        d=triangle(n, period, depth)
        esum=0
        for st in prog:
            s=st['s']
            if s in PAIR_A or s in PAIR_B:
                # fractional, swept delay with linear interpolation (reads only)
                off = st['offset'] + (d if s in PAIR_A else -d)
                af = pos - off
                ai = math.floor(af); frac = af - ai
                a0 = ai & DMASK; a1 = (ai+1) & DMASK
                dab = DM[a0]*(1.0-frac) + DM[a1]*frac
                dab = int(dab)
            else:
                addr=(pos-st['offset'])&DMASK
                dab = RES if st['b3'] else DM[addr]
            if n==0 and st is prog[0]: dab+=imp
            mag=abs(st['coeff']); Cs=-(mag>>1) if st['coeff']<0 else (mag>>1)
            x=R[pick(st)]; R[st['WA']]=dab
            if st['ZERO']: ACC=0
            ACC=A.sat20(ACC + (((x<<3)*Cs)>>6))
            if st['XFER']: RES=A.sat16(ACC>>3)
            # write-back uses the integer addr (writes aren't modulated)
            if st['b3']:
                addr=(pos-st['offset'])&DMASK
                DM[addr]=RES
            if st['XFER']: esum+=abs(RES)
        block.append(esum)
        if len(block)==BLK:
            env.append(math.sqrt(sum(v*v for v in block)/BLK)); block=[]
    return env


def rt60(env):
    skip=int(len(env)*0.3)
    xs=[i for i in range(skip,len(env)) if env[i]>0]
    if len(xs)<8: return None,None
    ys=[20*math.log10(env[i]) for i in xs]
    m=len(xs); sx=sum(xs); sy=sum(ys); sxx=sum(x*x for x in xs); sxy=sum(x*y for x,y in zip(xs,ys))
    db_s=((m*sxy-sx*sy)/(m*sxx-sx*sx))*NATIVE_HZ/BLK
    return db_s, ((-60.0/db_s) if db_s<-1e-4 else float('inf'))


def main():
    nsamp=int(sys.argv[1]) if len(sys.argv)>1 else 120000
    prog=A.load_microcode(0x01); pick=lambda st:(st['b5']<<1)|st['b4']
    print(f"LIVE modulation EDC, nsamp={nsamp} ({nsamp/NATIVE_HZ:.1f}s)\n")
    print("  no modulation (baseline):")
    env=run_live(prog,pick,nsamp,20000,depth=0,period=17000)
    dbs,rt=rt60(env); print(f"    dB/s={dbs:+.3f}  RT60={'SUSTAIN/GROW' if rt==float('inf') else f'{rt:.1f}s'}")
    print("  swept (period ~ sub-2Hz = 17000 samp; and faster), depth ±20 and ±47:")
    for period in (17000, 4000, 1000):
        for depth in (20, 47):
            env=run_live(prog,pick,nsamp,20000,depth=depth,period=period)
            dbs,rt=rt60(env)
            rts='SUSTAIN/GROW' if rt==float('inf') else f'{rt:.1f}s'
            print(f"    period={period:<6} depth=±{depth:<3} dB/s={dbs:+.3f}  RT60={rts}")


if __name__ == '__main__':
    main()
