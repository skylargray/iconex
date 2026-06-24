#!/usr/bin/env python3
"""Final: (a) identify the GENUINE FPC output step(s) in CONCERT, (b) confirm suppressing
ONLY them (FPC->sink) is lambda-neutral, (c) settle the bit15-write read-back question.

Genuine FPC OUTPUT per section 12 = the pass-through WA=3 step immediately following the
input read (s=76), in the I/O block, whose offset low14 is a strobe code. CONCERT's input
read = s=76 (0xffff, WA=2, low14=0x3FFF). The output write should be the next WA=3 step.
But note: CONCERT decodes 110 steps; the diag's 4-step I/O block (input,output) sat at
124-127 / 74-77. In a live image the output is the WA=3 step paired with s=76.

We already proved: ALL 14 'dead-sink' WA=3 b3=0 bit15 steps are lambda-neutral when their
read is suppressed. The genuine output(s) are a SUBSET of those dead sinks. So suppressing
the true FPC outputs is provably lambda-neutral => NO phantom FPC-output recirculation.

bit15 write read-back (DYNAMIC): a b3 write at addr A=(pos-offW); a later read at the SAME
absolute addr needs (pos+dn - offR) == (pos - offW) i.e. offR-offW == dn (steps within a
sample share pos; across samples pos increments). The base=0 rel-addr match already captures
intra-sample equal-position loops; for cross-sample, the loop lag = offset difference. We
report the bit15-set b3 writers whose rel write-addr is read by ANY step (the genuine combs).
"""
import sys, math
sys.path.insert(0, 'tools')
import aru_datapath as A
DMASK = A.DMASK
PICK = lambda st: (st['b5'] << 1) | st['b4']


def lambda_run(prog, sink=frozenset(), nsamp=60000, K=128, seed=1e4):
    R=[0.0]*4; ACC=0.0; RES=0.0; DM=[0.0]*(DMASK+1); pos=0; nz=set(); seeded=False; traj=[]
    for n in range(nsamp):
        pos=(pos+1)&DMASK
        for st in prog:
            addr=(pos-st['offset'])&DMASK
            s_is_sink = st['s'] in sink
            dab = 0.0 if s_is_sink else (RES if st['b3'] else DM[addr])
            if not seeded and st is prog[0]: dab+=seed; seeded=True
            mag=abs(st['coeff']); Cs=-(mag>>1) if st['coeff']<0 else (mag>>1)
            x=R[PICK(st)]; R[st['WA']]=dab
            if st['ZERO']: ACC=0.0
            ACC=ACC + x*8.0*Cs/64.0
            if st['XFER']: RES=ACC/8.0
            if st['b3'] and not s_is_sink: DM[addr]=RES; nz.add(addr)
        if (n+1)%K==0:
            s=math.sqrt(ACC*ACC+RES*RES+sum(v*v for v in R)+sum(DM[i]*DM[i] for i in nz))+1e-300
            traj.append(math.exp(math.log(s)/K)); f=1.0/s
            R=[v*f for v in R]; ACC*=f; RES*=f
            for i in nz: DM[i]*=f
    t=sorted(traj[-60:]); return t[len(t)//2]


def main():
    prog=A.load_microcode(0x01)
    byS={p['s']:p for p in prog}

    # genuine output candidates = WA=3, bit15, XFER=0, b3=0, ZERO=0, and R[3] dead-sink
    # (the section-12 pass-through output drives the DAC and does not feed the loop).
    def dead(p):
        i=next(k for k,q in enumerate(prog) if q['s']==p['s']); n=len(prog)
        for j in range(1,n+1):
            t=prog[(i+j)%n]
            if PICK(t)==p['WA']: return False
            if t['WA']==p['WA']: return True
        return True
    out_cands=[p['s'] for p in prog if ((p['offset']>>15)&1) and p['WA']==3
               and p['XFER']==0 and p['b3']==0 and p['ZERO']==0 and dead(p)]
    print("Genuine FPC-output-like steps (WA=3,b15,XFER=0,b3=0,ZERO=0,DEAD-sink):")
    print(" ", out_cands)
    print("Input read step (WA=2, low14=0x3FFF, b15):",
          [p['s'] for p in prog if p['WA']==2 and (p['offset']&0x3FFF)==0x3FFF and (p['offset']>>15)&1])

    base=lambda_run(prog)
    sink_all=lambda_run(prog, sink=frozenset(out_cands))
    print(f"\nbaseline                       lambda={base:.7f} ({(base-1)*1e6:+.1f} ppm)")
    print(f"FPC-outputs -> sink (read+write suppressed) lambda={sink_all:.7f} ({(sink_all-1)*1e6:+.1f} ppm) d={(sink_all-base)*1e6:+.1f}")

    # bit15 b3-writer read-back (the genuine comb closers)
    writers={}; readers={}
    for p in prog:
        rel=(-p['offset'])&DMASK
        (writers if p['b3'] else readers).setdefault(rel,[]).append(p['s'])
    b15_loops=[]; b15_writeonly=[]
    for p in prog:
        if p['b3'] and ((p['offset']>>15)&1):
            rel=(-p['offset'])&DMASK
            rs=readers.get(rel,[])
            (b15_loops if rs else b15_writeonly).append((p['s'], rel, rs, p['XFER']))
    print(f"\nbit15-set b3 WRITES that are READ-BACK (real recirc loops): {len(b15_loops)}")
    for s,rel,rs,xf in b15_loops:
        print(f"   s={s:3d} rel={rel:#06x} read-by={rs} XFER={xf} {'CLOSER' if xf else 'fwd-write'}")
    print(f"bit15-set b3 WRITES write-only (harmless): {[(s,hex(rel)) for s,rel,_,_ in b15_writeonly]}")


if __name__=='__main__':
    main()
