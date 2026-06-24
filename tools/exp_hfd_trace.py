#!/usr/bin/env python3
"""Is the register that HFD/LOW read (RA=0) live signal or stale/DC?

Hypothesis: HFD (40,41) and LOW (43) are inert on lambda because they read
register R0 (RA=0), which is NOT updated inside the band-split block -- so their
multiply adds a quasi-DC term (no feedback pole) rather than damping the loop.
The coupled steps MID(44,RA=3)/XOV(45,46,RA=2/3) read the live feedback registers.

This traces, over a window of warmed-up samples:
  - for each band-split step: RA, the register value it reads (x), and the
    step/sample that last wrote that register (its 'age' in steps & samples);
  - whether R0's value at steps 40/41/43 is changing sample-to-sample (live) or
    static (stale/DC).
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import aru_datapath as A

DMASK = A.DMASK
PICK = lambda st: (st['b5'] << 1) | st['b4']
WATCH = [40, 41, 42, 43, 44, 45, 46]


def trace(prog, nsamp=60, window=(40, 50), imp=20000):
    R = [0, 0, 0, 0]
    ACC = 0; RES = 0
    DM = [0] * (DMASK + 1)
    pos = 0
    # last writer of each register: (sample, step)
    rwrite = [(-1, -1)] * 4
    log = {s: [] for s in WATCH}
    r0_series = []
    for n in range(nsamp):
        pos = (pos + 1) & DMASK
        for st in prog:
            s = st['s']
            addr = (pos - st['offset']) & DMASK
            dab = RES if st['b3'] else DM[addr]
            if n == 0 and st is prog[0]:
                dab += imp
            mag = abs(st['coeff']); Cs = -(mag >> 1) if st['coeff'] < 0 else (mag >> 1)
            ra = PICK(st)
            x = R[ra]
            if s in WATCH and window[0] <= n < window[1]:
                log[s].append((n, ra, x, rwrite[ra][0], rwrite[ra][1]))
            R[st['WA']] = dab
            rwrite[st['WA']] = (n, s)
            if st['ZERO']: ACC = 0
            ACC = A.sat20(ACC + (((x << 3) * Cs) >> 6))
            if st['XFER']: RES = A.sat16(ACC >> 3)
            if st['b3']: DM[addr] = RES
        if window[0] <= n < window[1]:
            r0_series.append(R[0])
    return log, r0_series


def main():
    prog = A.load_microcode(0x01)
    log, r0 = trace(prog)
    print("band-split reads over warmed-up samples 40..49")
    print("(x = value read from R[RA]; last-write = sample/step that wrote that reg)\n")
    names = {40: 'HFD', 41: 'HFD', 42: 'PDL', 43: 'LOW', 44: 'MID', 45: 'XOV', 46: 'XOV'}
    for s in WATCH:
        print(f"  step {s} ({names[s]}, reads RA): "
              + ", ".join(f"n{n}:RA{ra} x={x} (wrote n{ws}/s{wstep})"
                          for (n, ra, x, ws, wstep) in log[s][:5]))
    print("\nIs R0 changing sample-to-sample at end-of-sample? (last 10):")
    print("  R0 =", r0[-10:])
    print("  -> if constant/tiny vs the tank amplitude, HFD/LOW reads are quasi-DC (decoupled).")

    # what is the typical recirculating amplitude (R3) for comparison?
    print("\nFor scale: register values at end of sample 49:")
    # re-run to grab end-state regs
    R = [0, 0, 0, 0]; ACC = 0; RES = 0; DM = [0]*(DMASK+1); pos = 0
    for n in range(50):
        pos = (pos+1) & DMASK
        for st in prog:
            addr = (pos - st['offset']) & DMASK
            dab = RES if st['b3'] else DM[addr]
            if n == 0 and st is prog[0]: dab += 20000
            mag = abs(st['coeff']); Cs = -(mag>>1) if st['coeff']<0 else (mag>>1)
            x = R[PICK(st)]; R[st['WA']] = dab
            if st['ZERO']: ACC = 0
            ACC = A.sat20(ACC + (((x<<3)*Cs)>>6))
            if st['XFER']: RES = A.sat16(ACC>>3)
            if st['b3']: DM[addr] = RES
    print(f"  R0={R[0]} R1={R[1]} R2={R[2]} R3={R[3]}  RES={RES}")


if __name__ == '__main__':
    main()
