#!/usr/bin/env python3
"""Test the one remaining structural lever: comb-closer intra-step pipeline ordering
(brief next-step 3). Clean converged power-iteration structural lambda, reused across
ordering variants. Float-exact (no sat/quant) so we read the pure structural gain.

Variants on the closer (XFER) steps only:
  base    : read x; R[WA]=dab; MAC; XFER RES; b3 write   (current model)
  newdab  : MAC uses the just-written dab as multiplicand (read-AFTER-write on WA==RA)
  preXfer : b3 writes the PRE-XFER RES (closer stores stale result)
  resfromprod : RES = this step's product only (ignore carried ACC) -- isolates closer
"""
import sys, os, math
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import aru_datapath as A

DMASK = A.DMASK
NATIVE_HZ = 34130.0
CLOSERS = {65, 88}


def power_lambda(prog, pick, variant='base', nsamp=40000, renorm=128):
    R=[0.0]*4; ACC=0.0; RES=0.0
    DM=[0.0]*(DMASK+1); nz=set(); pos=0
    logg=0.0; seeded=False
    for n in range(nsamp):
        pos=(pos+1)&DMASK
        for st in prog:
            addr=(pos-st['offset'])&DMASK
            dab=RES if st['b3'] else DM[addr]
            if not seeded and st is prog[0]:
                dab+=20000.0; seeded=True
            mag=abs(st['coeff']); Cs=-(mag>>1) if st['coeff']<0 else (mag>>1)
            isc = st['s'] in CLOSERS
            ra=pick(st)
            xold=R[ra]
            R[st['WA']]=dab
            x = dab if (variant=='newdab' and isc and ra==st['WA']) else xold
            if st['ZERO']: ACC=0.0
            prod = x*8.0*Cs/64.0
            ACC += prod
            if st['XFER']:
                if variant=='resfromprod' and isc:
                    newres = prod/8.0
                else:
                    newres = ACC/8.0
                if variant=='preXfer' and isc:
                    # b3 writes the stale (pre-XFER) RES
                    if st['b3']: DM[addr]=RES; nz.add(addr)
                    RES=newres
                else:
                    RES=newres
                    if st['b3']: DM[addr]=RES; nz.add(addr)
            else:
                if st['b3']: DM[addr]=RES; nz.add(addr)
        if (n+1)%renorm==0:
            s=abs(ACC)+abs(RES)+sum(abs(v) for v in R)+sum(abs(DM[i]) for i in nz)+1e-30
            f=1e6/s
            R=[v*f for v in R]; ACC*=f; RES*=f
            for i in nz: DM[i]*=f
            logg += -math.log(f)
    return math.exp(logg/nsamp)


def main():
    prog=A.load_microcode(0x01)
    pick=lambda st:(st['b5']<<1)|st['b4']
    print("Converged structural lambda (power iteration, float-exact) by closer ordering:\n")
    for v in ('base','newdab','preXfer','resfromprod'):
        lam=power_lambda(prog,pick,variant=v)
        gap=lam-0.9999899
        print(f"  {v:<12} lambda={lam:.7f}  gap_to_20s_target={gap:+.2e}  "
              f"{'GROW' if lam>1 else 'DECAY'}")


if __name__ == '__main__':
    main()
