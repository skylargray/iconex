#!/usr/bin/env python3
"""Brief next-step 4 cross-check: sweep the MID (and LOW) decay sliders per the
param-sweep table and measure the model's RT60 at each setting. A sensible monotonic
RT60 curve (longest at idx0/default, shortening as the slider rises) validates the
arithmetic and shows the booted default is simply the longest/near-marginal setting.
"""
import sys, os, math, json
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import aru_datapath as A

DMASK=A.DMASK; NATIVE_HZ=34130.0; BLK=512

SW=json.load(open(os.path.join(os.path.dirname(__file__),
              '..','docs','reference','224','224XL_param_sweep_01.json')))
TBL={}   # param -> {step:[8 vals]}
for p in SW['params']:
    TBL[p['param']]={int(k):v for k,v in p['coeff_table'].items()}


def apply_idx(prog, idx, params=(1,)):
    """Return a copy of prog with the given params' coeffs set to slider index idx."""
    out=[dict(p) for p in prog]
    bystep={p['s']:p for p in out}
    for par in params:
        for step,vals in TBL.get(par,{}).items():
            if step in bystep:
                bystep[step]['coeff']=vals[idx]
    return out


def run_sat(prog, pick, nsamp, imp):
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
            ACC=A.sat20(ACC + (((x<<3)*Cs)>>6))
            if st['XFER']: RES=A.sat16(ACC>>3)
            if st['b3']: DM[addr]=RES
            if st['XFER']: esum+=abs(RES)
        block.append(esum)
        if len(block)==BLK:
            env.append(math.sqrt(sum(v*v for v in block)/BLK)); block=[]
    return env


def rt60(env):
    skip=int(len(env)*0.35)
    xs=[i for i in range(skip,len(env)) if env[i]>0]
    if len(xs)<8: return None,None
    ys=[20*math.log10(env[i]) for i in xs]
    m=len(xs); sx=sum(xs); sy=sum(ys); sxx=sum(x*x for x in xs); sxy=sum(x*y for x,y in zip(xs,ys))
    db_per_blk=(m*sxy-sx*sy)/(m*sxx-sx*sx)
    db_per_s=db_per_blk*NATIVE_HZ/BLK
    return db_per_s, ((-60.0/db_per_s) if db_per_s<-1e-4 else float('inf'))


def main():
    nsamp=int(sys.argv[1]) if len(sys.argv)>1 else 100000
    prog=A.load_microcode(0x01); pick=lambda st:(st['b5']<<1)|st['b4']
    print(f"MID slider sweep, nsamp={nsamp} ({nsamp/NATIVE_HZ:.1f}s). idx0=default(longest)\n")
    print("  idx  MID-feedback-coeff(s64)  dB/s     RT60")
    for idx in range(8):
        prog2=apply_idx(prog, idx, params=(1,))      # MID only
        s64=next(p['coeff'] for p in prog2 if p['s']==64)
        env=run_sat(prog2,pick,nsamp,20000)
        dbs,rt=rt60(env)
        rts="SUSTAIN/GROW" if rt==float('inf') else (f"{rt:.2f}s" if rt else "n/a")
        dss=f"{dbs:+.3f}" if dbs is not None else "n/a"
        print(f"   {idx}   s64={s64:<5} Cs={-(abs(s64)>>1)}     {dss:>8}  {rts}")
    print("\n  + LOW together (params 0,1):")
    for idx in range(8):
        prog2=apply_idx(prog, idx, params=(0,1))
        env=run_sat(prog2,pick,nsamp,20000)
        dbs,rt=rt60(env)
        rts="SUSTAIN/GROW" if rt==float('inf') else (f"{rt:.2f}s" if rt else "n/a")
        dss=f"{dbs:+.3f}" if dbs is not None else "n/a"
        print(f"   {idx}   {dss:>8}  {rts}")


if __name__ == '__main__':
    main()
