#!/usr/bin/env python3
"""Lean minimal-fix search (faster: nsamp=12000, focused changes).

Decisive question: does ANY single principled decode correction reach a physical
RT60 band lambda in [0.99990, 1.00000]? Tests:
  1. uniform coeff scale s* (bisection) -> the distributed/physical answer
  2. single-step coeff +-1, sign flip, drop -> coolest single change reachable
Reports the coolest single-change lambda vs the uniform s*.
"""
import sys, os, math
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import aru_datapath as A
import exp_lambda_clean as L
DMASK = A.DMASK; PICK = L.PICK; TARGET = 0.9999899
NS = 12000; K = 128


def lam(prog, gscale=1.0, override=None, nsamp=NS, seed=1e4):
    R=[0.0]*4; ACC=0.0; RES=0.0; DM=[0.0]*(DMASK+1); pos=0; nz=set(); seeded=False; traj=[]
    ov = override or {}
    for n in range(nsamp):
        pos=(pos+1)&DMASK
        for st in prog:
            o = ov.get(st['s'])
            if o == 'DROP':
                if not seeded and st is prog[0]: seeded=True
                continue
            addr=(pos-st['offset'])&DMASK
            dab = RES if st['b3'] else DM[addr]
            if not seeded and st is prog[0]: dab+=seed; seeded=True
            coeff = o if (o is not None) else st['coeff']
            mag=abs(coeff); Cs = -(mag>>1) if coeff<0 else (mag>>1)
            x=R[PICK(st)]; R[st['WA']]=dab
            if st['ZERO']: ACC=0.0
            ACC = ACC + x*8.0*(Cs*gscale)/64.0
            if st['XFER']: RES=ACC/8.0
            if st['b3']: DM[addr]=RES; nz.add(addr)
        if (n+1)%K==0:
            s=math.sqrt(ACC*ACC+RES*RES+sum(v*v for v in R)+sum(DM[i]*DM[i] for i in nz))+1e-300
            traj.append(math.exp(math.log(s)/K)); f=1.0/s
            R=[v*f for v in R]; ACC*=f; RES*=f
            for i in nz: DM[i]*=f
    tail=sorted(traj[-40:]); return tail[len(tail)//2]


def main():
    prog=A.load_microcode(0x01)
    lam0=lam(prog); print(f"baseline lambda={lam0:.7f} ({(lam0-1)*1e6:+.1f} ppm) target {TARGET}",flush=True)

    lo,hi=0.80,1.0
    for _ in range(22):
        mid=0.5*(lo+hi)
        if lam(prog,gscale=mid)>TARGET: hi=mid
        else: lo=mid
    s_star=0.5*(lo+hi)
    print(f"[1] uniform s*={s_star:.5f} => {100*(1-s_star):.2f}% attenuation, lam={lam(prog,gscale=s_star):.7f}",flush=True)

    coolest=(lam0,'none')
    print("[2] single coeff +-1 ...",flush=True)
    for st in prog:
        for dc in (-1,+1):
            lm=lam(prog,override={st['s']:st['coeff']+dc})
            if lm<coolest[0]: coolest=(lm,f"coeff s={st['s']} {st['coeff']:+d}->{st['coeff']+dc:+d}")
    print(f"    coolest after coeff+-1: lam={coolest[0]:.7f} ({(coolest[0]-1)*1e6:+.1f}) via {coolest[1]}",flush=True)

    print("[3] single sign flip ...",flush=True)
    cool_flip=(lam0,'none')
    for st in prog:
        lm=lam(prog,override={st['s']:-st['coeff']})
        if lm<cool_flip[0]: cool_flip=(lm,f"signflip s={st['s']}")
        if lm<coolest[0]: coolest=(lm,f"signflip s={st['s']}")
    print(f"    coolest sign flip: lam={cool_flip[0]:.7f} ({(cool_flip[0]-1)*1e6:+.1f}) via {cool_flip[1]}",flush=True)

    print("[4] single drop ...",flush=True)
    cool_drop=(lam0,'none')
    for st in prog:
        lm=lam(prog,override={st['s']:'DROP'})
        if lm<cool_drop[0]: cool_drop=(lm,f"drop s={st['s']}")
        if lm<coolest[0]: coolest=(lm,f"drop s={st['s']}")
    print(f"    coolest drop: lam={cool_drop[0]:.7f} ({(cool_drop[0]-1)*1e6:+.1f}) via {cool_drop[1]}",flush=True)

    print("\n=== VERDICT ===",flush=True)
    print(f"  COOLEST single principled change: lam={coolest[0]:.7f} ({(coolest[0]-1)*1e6:+.1f} ppm) via {coolest[1]}",flush=True)
    if 0.99990<=coolest[0]<=1.00000:
        print("  => a SINGLE principled change reaches a physical RT60 band -> LOCALIZABLE.",flush=True)
    else:
        print(f"  => NO single change reaches [0.99990,1.0]; even the coolest leaves "
              f"{(coolest[0]-TARGET)*1e6:+.0f} ppm. Only the uniform {100*(1-s_star):.1f}% "
              f"attenuation hits target -> DISTRIBUTED.",flush=True)


if __name__=='__main__':
    main()
