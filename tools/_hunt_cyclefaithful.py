#!/usr/bin/env python3
"""Cycle-faithful ARU model built from the 060-01318 pinouts (topology now KNOWN):

  regfile F=R[RA] (LS670, write strobe DAB WSTB) -> multiplier (F*coeff, combinational)
  -> PRODUCT REGISTER PR (U10/11/12, clocked ARUCK) -> adder Sigma=AC+(+/-PR) (U19-23, comb)
  -> sat-mux PP=Sigma (U33-37) -> ACCUMULATOR AC<-PP (U45-49, clocked ARUCKE/, cleared ZERO/)
  RESULT REG RES<-PP>>3 (U43/44 74F374, clocked XFER CK); DAB = RES(if dmem-sel) else DMEM.

The ONLY unknowns are the relative CLOCK PHASES within one microstep and the RA wiring.
We parametrize exactly those and sweep against the all-programs-lossless objective; the
winning ordering tells the owner the single timing fact to confirm on the clock generator.

DOFs:
  P_post  : product register ARUCK fires AFTER the accumulate (so the accumulate uses the
            PREVIOUS cycle's product, PR is a true pipeline stage) vs before (same-cycle).
  W_first : regfile DAB WSTB write happens BEFORE the read (write-through) vs after (read-first).
  DW_pre  : the b3 DMEM write-back stores the PRE-XFER (old) RES vs post-XFER (new) RES.
  ra/dsel : decode (which control bits are RA, which is the DMEM select).
"""
import sys, os, math, random
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import _hunt_progcache as PC
MASK = 0xFFFF


def lam(prog, ra, dsel, P_post, W_first, DW_pre,
        nsamp=40000, K=128, warmup=10000, rseed=1):
    rng = random.Random(rseed)
    R = [rng.uniform(-1, 1) for _ in range(4)]
    AC = rng.uniform(-1, 1); RES = rng.uniform(-1, 1); PR = rng.uniform(-1, 1)
    DM = [0.0]*(MASK+1); pos = 0
    nz = set(); traj = []
    for n in range(nsamp):
        pos = (pos+1) & MASK
        for st in prog:
            addr = (pos - st['offset']) & MASK
            mag = abs(st['coeff']); Cs = -(mag>>1) if st['coeff']<0 else (mag>>1)
            cf = 8.0*Cs/64.0
            b3 = dsel(st)
            # regfile read/write ordering (DAB = RES if dmem-sel else DMEM read)
            if W_first:
                dab = RES if b3 else DM[addr]
                R[st['WA']] = dab; F = R[ra(st)]
            else:
                F = R[ra(st)]
                dab = RES if b3 else DM[addr]
                R[st['WA']] = dab
            Mmul = F * cf                         # combinational multiplier output
            res_old = RES
            if not P_post:                        # same-cycle product
                PR = Mmul
                if st['ZERO']: AC = 0.0
                AC = AC + PR
                if st['XFER']: RES = AC/8.0
            else:                                 # pipelined product (PR is one cycle behind)
                if st['ZERO']: AC = 0.0
                AC = AC + PR
                if st['XFER']: RES = AC/8.0
                PR = Mmul
            if b3:                                # DMEM write-back
                DM[addr] = res_old if DW_pre else RES
                nz.add(addr)
        if (n+1) % K == 0:
            s = math.sqrt(AC*AC+RES*RES+PR*PR+sum(v*v for v in R)
                          + sum(DM[i]*DM[i] for i in nz))+1e-300
            if (n+1) > warmup: traj.append(math.exp(math.log(s)/K))
            f = 1.0/s
            R=[v*f for v in R]; AC*=f; RES*=f; PR*=f
            for i in nz: DM[i]*=f
    tail = sorted(traj[-50:])
    return tail[len(tail)//2] if tail else float('nan')


RA = {'(b5,b4)': lambda s:(s['b5']<<1)|s['b4'], '(b3,b4)': lambda s:(s['b3']<<1)|s['b4']}
DS = {'b3': lambda s:s['b3'], 'b5': lambda s:s['b5']}


def main():
    import itertools
    cache = PC.load()
    clean = [p for p in sorted(cache) if cache[p]['clean']]
    NS = int(os.environ.get('NS', '15000')); WU = int(os.environ.get('WU', '4000'))
    print(f"cycle-faithful clock-phase sweep, {len(clean)} clean programs, nsamp={NS}\n")
    print(f"{'ra':9s} {'dsel':5s} {'P_post':7s} {'W_first':8s} {'DW_pre':7s}  #loss  off(ppm)")
    best = []
    # only physically-sensible decode pairings: (b5,b4)/b3 [current], (b3,b4)/b3 [b3 dual-use]
    pairs = [('(b5,b4)', RA['(b5,b4)'], 'b3', DS['b3']),
             ('(b3,b4)', RA['(b3,b4)'], 'b3', DS['b3'])]
    for raname, ra, dsname, ds in pairs:
        for P_post, W_first, DW_pre in itertools.product((False, True), repeat=3):
            nloss = 0; offs = []
            for p in clean:
                l = lam(cache[p]['prog'], ra, ds, P_post, W_first, DW_pre, nsamp=NS, warmup=WU, rseed=1)
                if abs(l-1) < 5e-4: nloss += 1
                else: offs.append(f"{p:#x}:{(l-1)*1e6:+.0f}" if abs(l-1)<2 else f"{p:#x}:{l:.2f}x")
            tag = f"{raname:9s} {dsname:5s} {str(P_post):7s} {str(W_first):8s} {str(DW_pre):7s}"
            print(f"{tag}  {nloss:2d}/{len(clean)}  {'ALL' if not offs else ' '.join(offs[:6])}")
            best.append((nloss, tag))
    best.sort(key=lambda t: -t[0])
    print(f"\nBEST: {best[0][0]}/{len(clean)}  ->  {best[0][1]}")


if __name__ == '__main__':
    main()
