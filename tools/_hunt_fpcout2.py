#!/usr/bin/env python3
"""Refine: distinguish genuine FPC-OUTPUT writes from ordinary WA=3 b3=0 reads.

The strict bit15+WA=3+XFER=0+b3=0 fingerprint caught 21 steps -- far too many for a
4-channel DAC. Real FPC outputs are RARE and DEAD-END (drive DAC, do not feed the loop).

Distinguishers to test:
 (A) register-flow: a WA=3 step writes R[3]; is R[3] ever READ (via PICK) by a later step
     before being overwritten?  An ordinary read FEEDS the next MAC (R[3] read soon);
     a true output is a SINK (R[3] never read, or pass-through scratch).
 (B) the FPC-output's *purpose* is pass-through of RES; but these steps have b3=0 so dab
     comes from DM[addr], NOT RES. A genuine WR DA/ output drives RES to the DAC -- in the
     diag the WA=3 step had b3=0 and dab=DM but the analog write takes the RESULT register.
 (C) does the step's DM READ (dab=DM[addr]) actually matter to lambda? Suppress read only
     (force dab=0) vs suppress nothing.

We separate the lambda effect of each candidate into READ-suppression effect, to see if the
+1126 ppm flip is a phantom READ (DMEM tap that shouldn't exist) rather than a write.
"""
import sys, math
sys.path.insert(0, 'tools')
import aru_datapath as A

DMASK = A.DMASK
PICK = lambda st: (st['b5'] << 1) | st['b4']


def reg_flow(prog):
    """For each step, does its WA-written register get READ by a later step (PICK) before
    being overwritten by another step writing the same WA? Returns dict s -> (read_by, dead)."""
    # linear order is the program order, wrapping each sample; treat one sample's sequence.
    info = {}
    n = len(prog)
    for i, st in enumerate(prog):
        wa = st['WA']
        read_by = None
        overwritten = False
        # scan forward (wrap-around to model next-sample continuation)
        for j in range(1, n+1):
            t = prog[(i+j) % n]
            if PICK(t) == wa:
                read_by = t['s']
                break
            if t['WA'] == wa:
                overwritten = True
                break
        info[st['s']] = dict(wa=wa, read_by=read_by, overwritten=overwritten,
                             dead=(read_by is None))
    return info


def lambda_run(prog, suppress_read=frozenset(), suppress_write=frozenset(),
               nsamp=60000, K=128, seed=1e4):
    """suppress_read: dab forced 0 for that step (no DMEM read).
    suppress_write: no DM[addr]=RES for that step.
    (A genuine FPC output -> suppress BOTH; this lets us isolate read vs write.)"""
    R = [0.0]*4; ACC = 0.0; RES = 0.0
    DM = [0.0]*(DMASK+1); pos = 0
    nz = set(); seeded = False; traj = []
    for n in range(nsamp):
        pos = (pos+1) & DMASK
        for st in prog:
            addr = (pos - st['offset']) & DMASK
            if st['s'] in suppress_read:
                dab = 0.0
            else:
                dab = RES if st['b3'] else DM[addr]
            if not seeded and st is prog[0]:
                dab += seed; seeded = True
            mag = abs(st['coeff']); Cs = -(mag>>1) if st['coeff']<0 else (mag>>1)
            x = R[PICK(st)]; R[st['WA']] = dab
            if st['ZERO']: ACC = 0.0
            ACC = ACC + x*8.0*Cs/64.0
            if st['XFER']: RES = ACC/8.0
            if st['b3'] and st['s'] not in suppress_write:
                DM[addr] = RES; nz.add(addr)
        if (n+1) % K == 0:
            s = math.sqrt(ACC*ACC + RES*RES + sum(v*v for v in R)
                          + sum(DM[i]*DM[i] for i in nz)) + 1e-300
            traj.append(math.exp(math.log(s)/K))
            f = 1.0/s
            R = [v*f for v in R]; ACC *= f; RES *= f
            for i in nz: DM[i] *= f
    tail = sorted(traj[-60:]); return tail[len(tail)//2]


def main():
    prog = A.load_microcode(0x01)
    info = reg_flow(prog)
    # candidate output steps = bit15, WA=3, XFER=0, b3=0, ZERO=0
    cand = [p for p in prog if ((p['offset']>>15)&1) and p['WA']==3
            and p['XFER']==0 and p['b3']==0 and p['ZERO']==0]
    print("=== WA=3 b3=0 bit15 candidates: register-flow analysis ===")
    print(" s   off    low14  coeff  R[3]read_by  dead?  (dead=sink=output-like)")
    dead = []; live = []
    for p in cand:
        f = info[p['s']]
        flag = "DEAD-SINK" if f['dead'] else f"->s{f['read_by']}"
        if f['dead']:
            dead.append(p['s'])
        else:
            live.append(p['s'])
        print(f"  {p['s']:3d} {p['offset']:#06x} {p['offset']&0x3FFF:#06x} {p['coeff']:5d}  {flag}")
    print(f"\n  DEAD-SINK (output-like, R[3] never read): {dead}")
    print(f"  LIVE-READ (feeds a later MAC, NOT output): {live}")

    base = lambda_run(prog)
    print(f"\n=== lambda decomposition ===")
    print(f"  baseline lambda={base:.7f} ({(base-1)*1e6:+.1f} ppm)")

    if dead:
        d_read = lambda_run(prog, suppress_read=frozenset(dead))
        print(f"  suppress READ of DEAD-SINK steps {dead}: lambda={d_read:.7f} ({(d_read-1)*1e6:+.1f} ppm) d={(d_read-base)*1e6:+.1f}")
    if live:
        l_read = lambda_run(prog, suppress_read=frozenset(live))
        print(f"  suppress READ of LIVE steps {live}: lambda={l_read:.7f} ({(l_read-1)*1e6:+.1f} ppm) d={(l_read-base)*1e6:+.1f}")

    # Also: how many of the 'dead' steps actually have a NONZERO coeff path? a true output
    # contributes its product to ACC. Check individual read-suppress for each dead step.
    print("\n=== per-step READ-suppress (DEAD-SINK candidates) ===")
    for s in dead:
        lam = lambda_run(prog, suppress_read=frozenset([s]))
        print(f"  suppress read s={s:3d}: lambda={lam:.7f} ({(lam-1)*1e6:+.1f} ppm) d={(lam-base)*1e6:+.1f} ppm")

    print("\n=== per-step READ-suppress (LIVE candidates, for contrast) ===")
    for s in live:
        lam = lambda_run(prog, suppress_read=frozenset([s]))
        print(f"  suppress read s={s:3d}: lambda={lam:.7f} ({(lam-1)*1e6:+.1f} ppm) d={(lam-base)*1e6:+.1f} ppm")


if __name__ == '__main__':
    main()
