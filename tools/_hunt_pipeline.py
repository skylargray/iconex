#!/usr/bin/env python3
"""Manual-grounded pipelined ARU model (from Service Manual 3.7 + Fig 3.4 + Fig 3.3).

Facts used (verbatim from the manual):
 - Register file write R[WA]=DAB EVERY system cycle (DAB WSTB/); WA=3 = scratch.        (3.7 p2)
 - 16x6 multiply+accumulate every 293 ns; result PIPELINED.                              (3.7 p1)
 - "the final result of the multiply and accumulate does not become available until the
    very end of AS0 of the NEXT system cycle. If a transfer command is present the result
    register is loaded at this time by XFER CK. If the zero command is given the
    accumulator is also cleared at this instant."                                        (3.7, line 400)
 - Fig 3.4: XFER CK & ZERO/ pulse at AS0 while the microinstruction's own product only
    builds over AS0->AS1->AS2  => XFER captures ACC BEFORE this step's product.
 - DMEM write data DIN = result register via XFER CK.                                     (Fig 3.3 note)

So per microinstruction M, the OUTPUT side (finish accumulate, XFER->RES, b3 DMEM write,
ZERO->clear) is DEFERRED one cycle relative to its register read / product formation.
Parametrized by: RA decode; xfer_before_product (acc_latch); defer (1-cycle pipeline on
the output side); reg_wbr (register file write-before-read). Tested vs all-programs-lossless.
"""
import sys, os, math, random
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import _hunt_progcache as PC
MASK = 0xFFFF


def lam(prog, ra, xfer_before_product, defer, reg_wbr,
        nsamp=40000, K=128, warmup=10000, rseed=1):
    rng = random.Random(rseed)
    R = [rng.uniform(-1, 1) for _ in range(4)]
    ACC = rng.uniform(-1, 1); RES = rng.uniform(-1, 1)
    DM = [0.0]*(MASK+1); pos = 0
    nz = set(); traj = []
    # pipeline latch (M-1's deferred output): product, XFER, ZERO, b3, addr
    pipe = (0.0, 0, 0, 0, 0)

    def apply_output(prod, xfer, zero, b3, addr):
        nonlocal ACC, RES
        # RES = result register = PP[3:18] = ACC>>3  (the /8 result-register shift)
        if xfer_before_product:
            if xfer: RES = ACC/8.0             # capture group sum BEFORE this step's product
            ACC = ACC + prod
        else:
            ACC = ACC + prod
            if xfer: RES = ACC/8.0             # capture incl this step's product
        if b3: DM[addr] = RES; nz.add(addr)    # DMEM write = XFER'd RES (Fig 3.3)
        if zero: ACC = 0.0                      # clear after XFER (Fig 3.4)

    for n in range(nsamp):
        pos = (pos+1) & MASK
        for st in prog:
            addr = (pos - st['offset']) & MASK
            mag = abs(st['coeff']); Cs = -(mag>>1) if st['coeff']<0 else (mag>>1)
            cf = 8.0*Cs/64.0
            b3 = st['b3']
            if defer:
                # apply previous microinstruction's deferred output FIRST (start of cycle)
                apply_output(*pipe)
            # M's input side
            dab = RES if b3 else DM[addr]
            if reg_wbr:
                R[st['WA']] = dab; x = R[ra(st)]
            else:
                x = R[ra(st)]; R[st['WA']] = dab
            prod = x*cf
            if defer:
                pipe = (prod, st['XFER'], st['ZERO'], b3, addr)
            else:
                apply_output(prod, st['XFER'], st['ZERO'], b3, addr)
        if (n+1) % K == 0:
            s = math.sqrt(ACC*ACC+RES*RES+pipe[0]*pipe[0]+sum(v*v for v in R)
                          + sum(DM[i]*DM[i] for i in nz))+1e-300
            if (n+1) > warmup: traj.append(math.exp(math.log(s)/K))
            f = 1.0/s
            R=[v*f for v in R]; ACC*=f; RES*=f; pipe=(pipe[0]*f,)+pipe[1:]
            for i in nz: DM[i]*=f
    tail = sorted(traj[-50:])
    return tail[len(tail)//2] if tail else float('nan')


RA = {'(b5,b4)': lambda s:(s['b5']<<1)|s['b4'], '(b3,b4)': lambda s:(s['b3']<<1)|s['b4']}


def main():
    cache = PC.load()
    clean = [p for p in sorted(cache) if cache[p]['clean']]
    print(f"manual-grounded pipeline model, {len(clean)} clean programs, 2-seed max\n")
    print(f"{'decode':9s} {'xfer_pre':9s} {'defer':6s} {'reg_wbr':8s}  #loss   hot(ppm)")
    import itertools
    NS = int(os.environ.get('NS', '16000')); WU = int(os.environ.get('WU', '4000'))
    for raname, ra in RA.items():
        for xbp, defer, rwbr in itertools.product((True, False), repeat=3):
            nloss = 0; hot = []
            for p in clean:
                l = lam(cache[p]['prog'], ra, xbp, defer, rwbr, nsamp=NS, warmup=WU, rseed=1)
                if abs(l-1) < 5e-4: nloss += 1
                elif l > 1: hot.append(f"{p:#x}:{(l-1)*1e6:+.0f}" if abs(l-1)<2 else f"{p:#x}:{l:.2f}x")
            print(f"{raname:9s} {str(xbp):9s} {str(defer):6s} {str(rwbr):8s}  {nloss:2d}/{len(clean)}  "
                  f"{' '.join(hot[:5]) if hot else 'ALL LOSSLESS (no hot)'}")


if __name__ == '__main__':
    main()
