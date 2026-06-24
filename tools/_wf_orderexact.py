#!/usr/bin/env python3
"""WF: EXACT intra-sample ordering test.

The model's default ordering: XFER updates RES, THEN b3 writes the (new) RES to DM.
Alternative ordering: b3 writes the OLD RES (pre-XFER) to DM, THEN XFER updates RES.
This makes the feedback writeback a 1-sample-delayed copy WITHOUT killing RES for
downstream readers (unlike just disabling XFER).

We implement a parametrised trajectory where `pre_steps` = set of steps that write
DM with the pre-XFER RES. Measures converged lambda (float L2) + coupling.
"""
import sys, os, math
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import aru_datapath as A

DMASK = A.DMASK
HFD = {40, 41, 92, 93}; LOW = {43, 95}; MID = {44, 96}


def lam_traj(prog, pre_steps=(), nsamp=30000, K=128, seed=1e4):
    pre = set(pre_steps)
    R = [0.0]*4; ACC = 0.0; RES = 0.0
    DM = [0.0]*(DMASK+1); pos = 0
    nz = set(); seeded = False; traj = []
    for n in range(nsamp):
        pos = (pos+1) & DMASK
        for st in prog:
            addr = (pos - st['offset']) & DMASK
            dab = RES if st['b3'] else DM[addr]
            if not seeded and st is prog[0]:
                dab += seed; seeded = True
            mag = abs(st['coeff']); Cs = -(mag>>1) if st['coeff']<0 else (mag>>1)
            x = R[(st['b5']<<1)|st['b4']]; R[st['WA']] = dab
            if st['ZERO']: ACC = 0.0
            # pre-xfer writeback uses the CURRENT (old) RES
            if st['b3'] and st['s'] in pre:
                DM[addr] = RES; nz.add(addr)
            ACC = ACC + x*8.0*Cs/64.0
            if st['XFER']: RES = ACC/8.0
            if st['b3'] and st['s'] not in pre:
                DM[addr] = RES; nz.add(addr)
        if (n+1) % K == 0:
            s = math.sqrt(ACC*ACC + RES*RES + sum(v*v for v in R)
                          + sum(DM[i]*DM[i] for i in nz)) + 1e-300
            traj.append((n+1, math.exp(math.log(s)/K)))
            f = 1.0/s
            R = [v*f for v in R]; ACC *= f; RES *= f
            for i in nz: DM[i] *= f
    return traj


def conv(prog, pre_steps=(), nsamp=30000, tail=40):
    traj = lam_traj(prog, pre_steps, nsamp=nsamp)
    vals = sorted(l for _, l in traj[-tail:])
    return vals[len(vals)//2]


def zero_param(prog, steps):
    p2 = [dict(p) for p in prog]
    for st in p2:
        if st['s'] in steps: st['coeff'] = 0
    return p2


def coupling(prog, pre_steps=()):
    base = conv(prog, pre_steps)
    out = {'base': base}
    for nm, steps in [('HFD', HFD), ('LOW', LOW), ('MID', MID)]:
        out[nm] = conv(zero_param(prog, steps), pre_steps) - base
    return out


def main():
    prog = A.load_microcode(0x01)
    base = conv(prog)
    print("BASELINE (default order) %.7f (%+.0f ppm)\ntarget 0.9999899\n" % (base, (base-1)*1e6))

    cases = [
        ("PRE s46,s98 (XOV closers pre-xfer)", (46, 98)),
        ("PRE s38,s90 (HFD closers pre-xfer)", (38, 90)),
        ("PRE s45,s97 (XOV b3-only pre-xfer)", (45, 97)),
        ("PRE s46,98,38,90 (all closers)",     (46, 98, 38, 90)),
        ("PRE s46 only (1st half)",            (46,)),
        ("PRE s98 only (2nd half)",            (98,)),
        ("PRE all 4 b3 in region",             (38, 45, 46, 90, 97, 98, 39, 91)),
    ]
    res = []
    for name, pre in cases:
        l = conv(prog, pre)
        tag = "DECAY" if l < 1 else "grow"
        print("%-38s %.7f (%+.0f ppm) %s" % (name, l, (l-1)*1e6, tag))
        res.append((name, pre, l))

    print("\n--- coupling for DECAY/promising ---")
    for name, pre, l in res:
        if l < 1 or abs((l-1)*1e6) < abs((base-1)*1e6)*0.5:
            c = coupling(prog, pre)
            print("%-38s base %.7f | HFD %+.0f LOW %+.0f MID %+.0f" %
                  (name, c['base'], c['HFD']*1e6, c['LOW']*1e6, c['MID']*1e6))


if __name__ == '__main__':
    main()
