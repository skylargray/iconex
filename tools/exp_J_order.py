#!/usr/bin/env python3
"""Variant J (symmetric band-split ZERO decode) + intra-sample ordering test.

Workflow wmvw1uocc found variant J — move the band-split ZERO-open to s40/s92 and
drop the spurious clears at s44/s96/s46/s98 — gives all four decay controls loop
authority (HFD -92, LOW -77, MID -668, XOV -33 ppm) and symmetric halves, but still
grows +556 ppm. The untested highest-prior combination is J + PRE-XFER (1-sample-
delayed) writeback on the band-split closers s46/s98 (and optionally s45/s97/s38/s90):
does it reach ~unity WITH authority retained (=> bug fully contained in the band-split)
or not (=> a uniform per-pass deficit lives outside it)?

This implements a float-exact linear map (exp_lambda_clean style) parametrised by:
  - edits: {step: {field: value}}  (applied via setfields)
  - prexfer: set of steps whose b3 write-back uses the PRE-XFER RES (delayed feedback)
and reports converged lambda + HFD/LOW/MID/XOV coupling.
"""
import sys, os, math
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import aru_datapath as A

DMASK = A.DMASK
PICK = lambda st: (st['b5'] << 1) | st['b4']
HFD = {40, 41, 92, 93}; LOW = {43, 95}; MID = {44, 96}; XOV = {45, 46, 97, 98}

# Variant J: symmetric ZERO decode for the band-split.
J_EDITS = {40: {'ZERO': 1}, 92: {'ZERO': 1},
           44: {'ZERO': 0}, 96: {'ZERO': 0},
           46: {'ZERO': 0}, 98: {'ZERO': 0}}


def clone(prog): return [dict(p) for p in prog]


def setfields(prog, edits):
    p2 = clone(prog)
    for st in p2:
        if st['s'] in edits:
            st.update(edits[st['s']])
    return p2


def lam(prog, prexfer=frozenset(), nsamp=30000, K=128, seed=1e4, tail=40):
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
            if st['ZERO']: ACC = 0.0
            ACC = ACC + x*8.0*Cs/64.0
            res_for_write = RES                       # pre-XFER value
            if st['XFER']: RES = ACC/8.0
            if st['b3']:
                w = res_for_write if st['s'] in prexfer else RES
                DM[addr] = w; nz.add(addr)
        if (n+1) % K == 0:
            ssq = math.sqrt(ACC*ACC + RES*RES + sum(v*v for v in R)
                            + sum(DM[i]*DM[i] for i in nz)) + 1e-300
            traj.append(math.exp(math.log(ssq)/K))
            f = 1.0/ssq
            R = [v*f for v in R]; ACC *= f; RES *= f
            for i in nz: DM[i] *= f
    t = sorted(traj[-tail:])
    return t[len(t)//2]


def coupling(prog, prexfer=frozenset()):
    base = lam(prog, prexfer)
    out = {'base': base}
    for nm, steps in [('HFD', HFD), ('LOW', LOW), ('MID', MID), ('XOV', XOV)]:
        p2 = setfields(prog, {s: {'coeff': 0} for s in steps})
        out[nm] = (lam(p2, prexfer) - base) * 1e6
    return out


def report(name, prog, prexfer=frozenset()):
    c = coupling(prog, prexfer)
    print(f"\n{name}")
    print(f"  lambda = {c['base']:.7f}  ({(c['base']-1)*1e6:+.0f} ppm)  "
          f"{'GROW' if c['base']>1 else 'DECAY'}")
    print(f"  authority (d-ppm coeff->0):  HFD {c['HFD']:+.0f}  LOW {c['LOW']:+.0f}  "
          f"MID {c['MID']:+.0f}  XOV {c['XOV']:+.0f}")


def main():
    prog = A.load_microcode(0x01)
    print("target lambda = 0.9999899 (-10 ppm)")
    report("BASELINE", prog)
    J = setfields(prog, J_EDITS)
    report("J (symmetric ZERO decode)", J)
    report("J + preXFER{46,98}", J, prexfer=frozenset({46, 98}))
    report("J + preXFER{45,46,97,98}", J, prexfer=frozenset({45, 46, 97, 98}))
    report("J + preXFER{38,46,90,98}", J, prexfer=frozenset({38, 46, 90, 98}))


if __name__ == '__main__':
    main()
