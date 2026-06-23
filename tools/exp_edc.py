#!/usr/bin/env python3
"""Long-run envelope characterization: block-RMS trend of the saturating integer
model over many seconds -> dB/s -> RT60. Properly distinguishes SUSTAIN (flat) from
a slow ~20 s decay. Also reports a control (effective-gain reduced by eps) to find
the gain reduction that yields ~20 s.
"""
import sys, os, math
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import aru_datapath as A

DMASK=A.DMASK; NATIVE_HZ=34130.0; BLK=1024


def run_sat(prog, pick, nsamp, imp, gain=1.0):
    R=[0,0,0,0]; ACC=0; RES=0; DM=[0]*(DMASK+1); pos=0
    block=[]; benergy=[]
    use_gain = (gain!=1.0)
    for n in range(nsamp):
        pos=(pos+1)&DMASK; esum=0
        for st in prog:
            addr=(pos-st['offset'])&DMASK
            dab=RES if st['b3'] else DM[addr]
            if n==0 and st is prog[0]: dab+=imp
            mag=abs(st['coeff']); Cs=-(mag>>1) if st['coeff']<0 else (mag>>1)
            x=R[pick(st)]; R[st['WA']]=dab
            if st['ZERO']: ACC=0
            if use_gain:
                ACC=A.sat20(ACC + int(math.floor((x<<3)*Cs*gain/64.0)))
            else:
                ACC=A.sat20(ACC + (((x<<3)*Cs)>>6))
            if st['XFER']: RES=A.sat16(ACC>>3)
            if st['b3']: DM[addr]=RES
            if st['XFER']: esum+=abs(RES)
        block.append(esum)
        if len(block)==BLK:
            benergy.append(math.sqrt(sum(v*v for v in block)/BLK))
            block=[]
    return benergy


def fit_rt60(benergy, skip_blocks):
    xs=[i for i in range(skip_blocks,len(benergy)) if benergy[i]>0]
    if len(xs)<10: return None
    ys=[20*math.log10(benergy[i]) for i in xs]
    m=len(xs); sx=sum(xs); sy=sum(ys); sxx=sum(x*x for x in xs); sxy=sum(x*y for x,y in zip(xs,ys))
    db_per_block=(m*sxy-sx*sy)/(m*sxx-sx*sx)
    db_per_s=db_per_block*NATIVE_HZ/BLK
    rt60=(-60.0/db_per_s) if db_per_s<-1e-6 else float('inf')
    return db_per_s, rt60


def report(label, benergy, secs):
    skip=int(len(benergy)*0.3)   # skip the buildup transient
    r=fit_rt60(benergy, skip)
    pk=max(benergy); first=benergy[0]; last=benergy[-1]
    if r:
        dbs, rt = r
        rts = f"{rt:.1f}s" if rt!=float('inf') else "SUSTAIN/GROW"
        print(f"  {label:<22} {secs:.1f}s blkRMS first={first:.0f} peak={pk:.0f} last={last:.0f}  "
              f"dB/s={dbs:+.3f} RT60={rts}")
    else:
        print(f"  {label:<22} insufficient data")


def main():
    nsamp=int(sys.argv[1]) if len(sys.argv)>1 else 700000
    prog=A.load_microcode(0x01); pick=lambda st:(st['b5']<<1)|st['b4']
    secs=nsamp/NATIVE_HZ
    print(f"CONCERT long-run EDC: nsamp={nsamp} ({secs:.1f}s), block={BLK}\n")
    print("CURRENT model:")
    report("floor (current)", run_sat(prog,pick,nsamp,20000), secs)
    print("\nControl: effective gain reduced by eps (find ~20 s):")
    for eps in (1e-4, 3e-4, 1e-3, 3e-3):
        report(f"gain x(1-{eps:g})", run_sat(prog,pick,nsamp,20000,gain=1.0-eps), secs)


if __name__ == '__main__':
    main()
