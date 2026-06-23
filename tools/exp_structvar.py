#!/usr/bin/env python3
"""Probe intra-pass EXECUTION-TIMING semantics (the one class not independently
verifiable from the docs). Measure structural lambda (float-exact power iteration)
under hardware-plausible timing variants of the datapath:

  base        : immediate DMEM writes; registers persist across passes (current model)
  defer_dmem  : DMEM writes buffered, applied at END of pass (same-pass reads see OLD)
  defer_reg   : register writes buffered to end of pass (read-before-write taken to extreme)
  reg_reset   : register file cleared at the start of each pass
  pos_predec  : position taken as (pos) for reads but (pos) for writes already same -> n/a
"""
import sys, os, math
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import aru_datapath as A
DMASK=A.DMASK


def power_lambda_var(prog, pick, variant, nsamp=15000, renorm=200):
    R=[0.0]*4; ACC=0.0; RES=0.0; DM=[0.0]*(DMASK+1); nz=set(); pos=0
    logg=0.0; seeded=False
    for n in range(nsamp):
        pos=(pos+1)&DMASK
        pending_dm=[]   # (addr,val) for defer_dmem
        pending_rg=[]   # (wa,val) for defer_reg
        if variant=='reg_reset':
            R=[0.0,0.0,0.0,0.0]
        for st in prog:
            addr=(pos-st['offset'])&DMASK
            dab=RES if st['b3'] else DM[addr]
            if not seeded and st is prog[0]: dab+=20000.0; seeded=True
            mag=abs(st['coeff']); Cs=-(mag>>1) if st['coeff']<0 else (mag>>1)
            x=R[pick(st)]
            if variant=='defer_reg':
                pending_rg.append((st['WA'],dab))
            else:
                R[st['WA']]=dab
            if st['ZERO']: ACC=0.0
            ACC += x*8.0*Cs/64.0
            if st['XFER']: RES=ACC/8.0
            if st['b3']:
                if variant=='defer_dmem':
                    pending_dm.append((addr,RES))
                else:
                    DM[addr]=RES; nz.add(addr)
        if variant=='defer_dmem':
            for a,v in pending_dm: DM[a]=v; nz.add(a)
        if variant=='defer_reg':
            for wa,v in pending_rg: R[wa]=v
        if (n+1)%renorm==0:
            s=abs(ACC)+abs(RES)+sum(abs(v) for v in R)+sum(abs(DM[i]) for i in nz)+1e-30
            f=1e6/s; R=[v*f for v in R]; ACC*=f; RES*=f
            for i in nz: DM[i]*=f
            logg += -math.log(f)
    return math.exp(logg/nsamp)


def main():
    prog=A.load_microcode(0x01); pick=lambda st:(st['b5']<<1)|st['b4']
    print("structural lambda by execution-timing variant:\n")
    for v in ('base','defer_dmem','defer_reg','reg_reset'):
        lam=power_lambda_var(prog,pick,v)
        print(f"  {v:<12} lambda={lam:.7f}  {'GROW' if lam>1 else 'DECAY <<<'}")


if __name__ == '__main__':
    main()
