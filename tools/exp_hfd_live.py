#!/usr/bin/env python3
"""Does HFD/LOW (RA=0) read LIVE recirculating signal, in the converged mode?

Float linear map (exp_lambda_clean style: seed prog[0], renormalise every 128
samples). In the converged tail, record the mean |multiplicand| each band-split
step reads (x = R[RA]) and the mean |value| of each register. If HFD steps
(40,41 read R0) carry ~0 while MID/XOV (read R2/R3) carry the mode amplitude,
HFD is structurally decoupled from the growing eigenmode.

Also: trace R0's writer chain -- which step writes R0 and what it reads -- to see
whether R0 is part of the recirculation or an input/predelay-only node.
"""
import sys, os, math
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import aru_datapath as A

DMASK = A.DMASK
PICK = lambda st: (st['b5'] << 1) | st['b4']
WATCH = {40: 'HFD', 41: 'HFD', 43: 'LOW', 44: 'MID', 45: 'XOV', 46: 'XOV'}


def run(prog, nsamp=30000, K=128, seed=1e4, tail_frac=0.1):
    R = [0.0]*4; ACC = 0.0; RES = 0.0
    DM = [0.0]*(DMASK+1); pos = 0
    nz = set(); seeded = False
    tail_start = int(nsamp*(1-tail_frac))
    read_abs = {s: 0.0 for s in WATCH}; read_n = {s: 0 for s in WATCH}
    reg_abs = [0.0]*4; reg_n = 0
    for n in range(nsamp):
        pos = (pos+1) & DMASK
        for st in prog:
            s = st['s']
            addr = (pos - st['offset']) & DMASK
            dab = RES if st['b3'] else DM[addr]
            if not seeded and st is prog[0]:
                dab += seed; seeded = True
            mag = abs(st['coeff']); Cs = -(mag>>1) if st['coeff']<0 else (mag>>1)
            x = R[PICK(st)]; R[st['WA']] = dab
            if st['ZERO']: ACC = 0.0
            ACC = ACC + x*8.0*Cs/64.0
            if st['XFER']: RES = ACC/8.0
            if st['b3']: DM[addr] = RES; nz.add(addr)
            if n >= tail_start and s in WATCH:
                read_abs[s] += abs(x); read_n[s] += 1
        if n >= tail_start:
            for i in range(4): reg_abs[i] += abs(R[i])
            reg_n += 1
        if (n+1) % K == 0:
            ssq = math.sqrt(ACC*ACC + RES*RES + sum(v*v for v in R)
                            + sum(DM[i]*DM[i] for i in nz)) + 1e-300
            f = 1.0/ssq
            R = [v*f for v in R]; ACC *= f; RES *= f
            for i in nz: DM[i] *= f
    return read_abs, read_n, reg_abs, reg_n


def main():
    prog = A.load_microcode(0x01)
    read_abs, read_n, reg_abs, reg_n = run(prog)
    print("Mean |register value| in converged tail (relative scale):")
    rms = [reg_abs[i]/reg_n for i in range(4)]
    mx = max(rms) or 1
    for i in range(4):
        print(f"  R{i}: {rms[i]:.3e}  ({rms[i]/mx*100:5.1f}% of max)")
    print("\nMean |multiplicand x=R[RA]| each band-split step reads (converged tail):")
    vals = {s: (read_abs[s]/read_n[s] if read_n[s] else 0) for s in WATCH}
    mxr = max(vals.values()) or 1
    bystep = {p['s']: p for p in prog}
    for s in sorted(WATCH):
        ra = PICK(bystep[s])
        print(f"  step {s:>3} {WATCH[s]:<4} RA={ra}:  {vals[s]:.3e}  ({vals[s]/mxr*100:5.1f}% of max)")
    print("\n  -> HFD(40,41)/LOW(43) read R0; MID(44)/XOV(45,46) read R2/R3.")
    print("     If R0 amplitude << R2/R3, HFD/LOW are reading a near-dead node = decoupled.")

    # who writes R0, and what does that step read?
    print("\nR0 writer chain (steps with WA=0):")
    for st in prog:
        if st['WA'] == 0:
            d = (-st['offset']) & 0xFFFF; ds = d-65536 if d > 32768 else d
            print(f"  step {st['s']:>3}: WA=0 reads RA={PICK(st)} tap(addr-pos={ds}) coeff={st['coeff']} "
                  f"b3={st['b3']} XFER={st['XFER']} ZERO={st['ZERO']}")


if __name__ == '__main__':
    main()
