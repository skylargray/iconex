#!/usr/bin/env python3
"""WF2: test the synchronous-CLR (74LS163) vs 374-latches-PP-bus semantic.

Hardware (schematic 060-01318, crops aru_botctrl.png + aru_resreg_ctrl.png, agent-1):
  - Accumulator = 5x 74LS163 with SYNCHRONOUS clear (CLR/ = ZERO/ = A49), clocked by
    XFER CK = A27. Pin9 L/=GND (always LOAD), so each XFER edge the LS163 loads the adder
    sum PP unless ZERO/=0, in which case the synchronous CLR OVERRIDES load and writes 0.
  - Result register U43/U44 = 74F374, D = PP3..PP18 (the COMBINATIONAL adder/sat bus
    = ACC_old + this-step product, >>3), clock = XFER CK A27, OE = RDRREG/ A50. It has
    NO clear and does NOT read the LS163 Q.

Consequence the committed model gets WRONG only when ZERO & XFER coincide (CONCERT s46):
  hardware: RES <= (ACC_old + product) >> 3 ; LS163 accumulator <= 0 on the same edge.
  model   : ACC=0; ACC += product; RES = ACC>>3  =>  RES = product-only (loses ACC_old).
And the accumulator value SEEN BY THE NEXT STEP is 0 in BOTH (clear wins for next step),
so the only divergence is the value transferred at the ZERO+XFER step.

This builds the float-exact linear map (exp_J_order.lam style) with a `syncclr` flag that,
for steps where ZERO&XFER both set, latches RES from the PRE-clear sum, then zeros ACC.
Reports converged lambda + HFD/LOW/MID/XOV coupling for: baseline, syncclr, and J for ref.
"""
import sys, os, math
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import aru_datapath as A

DMASK = A.DMASK
PICK = lambda st: (st['b5'] << 1) | st['b4']
HFD = {40, 41, 92, 93}; LOW = {43, 95}; MID = {44, 96}; XOV = {45, 46, 97, 98}


def clone(prog): return [dict(p) for p in prog]


def setfields(prog, edits):
    p2 = clone(prog)
    for st in p2:
        if st['s'] in edits:
            st.update(edits[st['s']])
    return p2


def lam(prog, syncclr=False, nsamp=30000, K=128, seed=1e4, tail=40):
    """syncclr=True => when ZERO&XFER both set on a step, RES latches the PRE-clear
    adder sum (ACC_old + product), matching the 74F374-reads-PP / LS163-sync-CLR HW."""
    R = [0.0]*4; ACC = 0.0; RES = 0.0
    DM = [0.0]*(DMASK+1); pos = 0; nz = set(); seeded = False
    traj = []
    for n in range(nsamp):
        pos = (pos+1) & DMASK
        for st in prog:
            addr = (pos - st['offset']) & DMASK
            dab = RES if st['b3'] else DM[addr]
            if not seeded and st is prog[0]:
                dab += seed; seeded = True
            mag = abs(st['coeff']); Cs = -(mag>>1) if st['coeff']<0 else (mag>>1)
            x = R[PICK(st)]; R[st['WA']] = dab
            # adder combinational sum = ACC_old + product (this is what the 374 sees)
            prod = x*8.0*Cs/64.0
            summ = ACC + prod
            if st['ZERO'] and st['XFER'] and syncclr:
                # 374 latches the pre-clear sum; LS163 synchronously clears to 0
                RES = summ/8.0
                ACC = 0.0
            else:
                if st['ZERO']:
                    ACC = 0.0
                    summ = ACC + prod   # cleared-then-accumulate (model's old behavior)
                ACC = summ
                if st['XFER']:
                    RES = ACC/8.0
            if st['b3']:
                DM[addr] = RES; nz.add(addr)
        if (n+1) % K == 0:
            ssq = math.sqrt(ACC*ACC + RES*RES + sum(v*v for v in R)
                            + sum(DM[i]*DM[i] for i in nz)) + 1e-300
            traj.append(math.exp(math.log(ssq)/K))
            f = 1.0/ssq
            R = [v*f for v in R]; ACC *= f; RES *= f
            for i in nz: DM[i] *= f
    t = sorted(traj[-tail:])
    return t[len(t)//2]


def coupling(prog, syncclr=False):
    base = lam(prog, syncclr)
    out = {'base': base}
    for nm, steps in [('HFD', HFD), ('LOW', LOW), ('MID', MID), ('XOV', XOV)]:
        p2 = setfields(prog, {s: {'coeff': 0} for s in steps})
        out[nm] = (lam(p2, syncclr) - base) * 1e6
    return out


def report(name, prog, syncclr=False):
    c = coupling(prog, syncclr)
    print(f"\n{name}")
    print(f"  lambda = {c['base']:.7f}  ({(c['base']-1)*1e6:+.0f} ppm)  "
          f"{'GROW' if c['base']>1 else 'DECAY'}")
    print(f"  authority (d-ppm coeff->0):  HFD {c['HFD']:+.0f}  LOW {c['LOW']:+.0f}  "
          f"MID {c['MID']:+.0f}  XOV {c['XOV']:+.0f}")


def main():
    prog = A.load_microcode(0x01)
    print("target lambda = 0.9999899 (-10 ppm)")
    report("BASELINE (model: ZERO clears then accumulate; RES=product-only at s46)", prog)
    report("SYNCCLR (HW: 374 latches pre-clear sum at ZERO+XFER step s46)", prog, syncclr=True)
    # which steps in CONCERT actually have ZERO & XFER both set?
    zx = [p['s'] for p in prog if p['ZERO'] and p['XFER']]
    print(f"\n  steps with ZERO&XFER both set (where syncclr differs): {zx}")


if __name__ == '__main__':
    main()
