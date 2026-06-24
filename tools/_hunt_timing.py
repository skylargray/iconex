#!/usr/bin/env python3
"""LEAD 2 (software-testable part): does a PHYSICALLY-PLAUSIBLE pipeline/latch timing
variant bring the collective eigenvalue to ~1.0 or below?

_hunt_coupling showed the core is wildly non-normal (sigma_max(C)=3.3, rho(C)=1.75)
yet lambda=1.0011 -- so the eigenvalue is delay/ordering sensitive, exactly what a
1-microstep pipeline error perturbs. The model (exp_lambda_clean.lambda_trajectory)
makes specific timing assumptions; here we vary them ONE at a time and measure the
converged float lambda. Any variant that yields lambda<=~1 is a candidate for the
real hardware timing -- to be confirmed against the schematic (which signals to trace
are printed at the end).

Variants (each a single, named, physically-motivated change vs the model):
  base   : exact mirror of lambda_trajectory (XFER-then-write; immediate RES; same-step MAC)
  C_wrXFER : when a step has BOTH XFER and b3, DMEM write stores the PRE-XFER (old) RES
             (result register latches at cycle END, after the DRAM write strobe).
  B_resLatch : RES from XFER is visible (to b3 read AND b3 write) only on the NEXT step
               (result register is a clocked latch, one microstep behind).
  A_macPipe : multiplier has 1-cycle latency: the product formed at step N is accumulated
              at step N+1 (XFER at step N therefore reads ACC WITHOUT step N's own product).
  A2_macPipe_xferlast : A_macPipe but XFER reads ACC AFTER adding step N's product too
                        (product pipelined into ACC but bypassed to the XFER read).
  D_wbDelay : the b3 DMEM write-back is issued one step late (write address+data latched).
"""
import sys, os, math
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import aru_datapath as A
DMASK = A.DMASK
PICK = lambda st: (st['b5'] << 1) | st['b4']


def lam(prog, variant='base', nsamp=40000, K=128, seed=1e4):
    R = [0.0]*4; ACC = 0.0; RES = 0.0
    DM = [0.0]*(DMASK+1); pos = 0
    nz = set(); seeded = False; traj = []
    RES_committed = 0.0       # for B_resLatch
    pend_prod = 0.0           # for A_macPipe
    pend_wb = None            # for D_wbDelay: (addr, value) to write next step
    for n in range(nsamp):
        pos = (pos+1) & DMASK
        for st in prog:
            addr = (pos - st['offset']) & DMASK
            mag = abs(st['coeff']); Cs = -(mag>>1) if st['coeff']<0 else (mag>>1)
            cf = 8.0*Cs/64.0

            if variant == 'base':
                dab = RES if st['b3'] else DM[addr]
                if not seeded and st is prog[0]: dab += seed; seeded = True
                x = R[PICK(st)]; R[st['WA']] = dab
                if st['ZERO']: ACC = 0.0
                ACC += x*cf
                if st['XFER']: RES = ACC/8.0
                if st['b3']: DM[addr] = RES; nz.add(addr)

            elif variant == 'C_wrXFER':
                dab = RES if st['b3'] else DM[addr]
                if not seeded and st is prog[0]: dab += seed; seeded = True
                x = R[PICK(st)]; R[st['WA']] = dab
                if st['ZERO']: ACC = 0.0
                ACC += x*cf
                if st['b3']: DM[addr] = RES; nz.add(addr)   # write OLD RES first
                if st['XFER']: RES = ACC/8.0                  # then latch new RES

            elif variant == 'B_resLatch':
                dab = RES_committed if st['b3'] else DM[addr]
                if not seeded and st is prog[0]: dab += seed; seeded = True
                x = R[PICK(st)]; R[st['WA']] = dab
                if st['ZERO']: ACC = 0.0
                ACC += x*cf
                if st['b3']: DM[addr] = RES_committed; nz.add(addr)
                if st['XFER']: RES_committed = ACC/8.0        # becomes visible NEXT step

            elif variant == 'A_macPipe':
                dab = RES if st['b3'] else DM[addr]
                if not seeded and st is prog[0]: dab += seed; seeded = True
                x = R[PICK(st)]; R[st['WA']] = dab
                if st['ZERO']: ACC = 0.0
                ACC += pend_prod                              # add PREVIOUS step's product
                pend_prod = x*cf                              # this step's product -> next
                if st['XFER']: RES = ACC/8.0                  # misses this step's product
                if st['b3']: DM[addr] = RES; nz.add(addr)

            elif variant == 'A2_macPipe_xferlast':
                dab = RES if st['b3'] else DM[addr]
                if not seeded and st is prog[0]: dab += seed; seeded = True
                x = R[PICK(st)]; R[st['WA']] = dab
                if st['ZERO']: ACC = 0.0
                ACC += pend_prod
                pend_prod = x*cf
                if st['XFER']: RES = (ACC + pend_prod)/8.0    # bypass current product to XFER
                if st['b3']: DM[addr] = RES; nz.add(addr)

            elif variant == 'D_wbDelay':
                if pend_wb is not None:
                    DM[pend_wb[0]] = pend_wb[1]; nz.add(pend_wb[0]); pend_wb = None
                dab = RES if st['b3'] else DM[addr]
                if not seeded and st is prog[0]: dab += seed; seeded = True
                x = R[PICK(st)]; R[st['WA']] = dab
                if st['ZERO']: ACC = 0.0
                ACC += x*cf
                if st['XFER']: RES = ACC/8.0
                if st['b3']: pend_wb = (addr, RES)            # deferred to next step
            else:
                raise ValueError(variant)

        if (n+1) % K == 0:
            s = math.sqrt(ACC*ACC + RES*RES + RES_committed*RES_committed
                          + sum(v*v for v in R) + sum(DM[i]*DM[i] for i in nz)) + 1e-300
            traj.append(math.exp(math.log(s)/K))
            f = 1.0/s
            R = [v*f for v in R]; ACC *= f; RES *= f; RES_committed *= f
            pend_prod *= f
            if pend_wb is not None: pend_wb = (pend_wb[0], pend_wb[1]*f)
            for i in nz: DM[i] *= f
    tail = sorted(traj[-60:])
    return tail[len(tail)//2]


def main():
    prog = A.load_microcode(0x01)
    variants = ['base','C_wrXFER','B_resLatch','A_macPipe','A2_macPipe_xferlast','D_wbDelay']
    print("=== timing-variant converged lambda (target 0.9999899, baseline ~1.0011266) ===\n")
    base = None
    for v in variants:
        l = lam(prog, v)
        if v == 'base': base = l
        verdict = 'GROW' if l > 1 else 'DECAY'
        dppm = (l-1)*1e6
        rel = '' if base is None else f"   d(base)={(l-base)*1e6:+8.1f} ppm"
        print(f"  {v:22s} lambda={l:.7f}  ({dppm:+8.1f} ppm, {verdict}){rel}")
    print("\n  A variant that yields lambda<=~1.0 (esp. ~0.99999) is a TIMING candidate.")
    print("  Confirm against schematic: which microstep result is the b3 DMEM write/read")
    print("  using -- the just-computed (post-XFER) RES, or the previous cycle's latched RES?")


if __name__ == '__main__':
    main()
