#!/usr/bin/env python3
"""Search the decode/timing space against the ALL-PROGRAMS-LOSSLESS objective.

The base model makes 8/21 programs over-unity. A CORRECT model (the real hardware
behavior is program-independent) must make EVERY clean-booting program lossless
(lambda ~ 1.0, the reverb prototype) -- NOT just CONCERT. This is a far stronger,
less overfit-prone constraint than the CONCERT-only test the frontier doc used.

Uses the cached booted programs (_hunt_progcache). For each candidate decode (RA/PICK
assignment) and timing-flag set, measures random-start lambda for every clean program
and counts how many are lossless. The candidate that makes ALL clean programs lossless
(if any) is the real correction.
"""
import sys, os, math, random
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import aru_datapath as A
import _hunt_progcache as PC
DMASK = A.DMASK


def lam(prog, pick, res_latch=False, acc_latch=False, reg_wbr=False, mac_pipe=False,
        nsamp=16000, K=128, warmup=3000, rseed=1):
    rng = random.Random(rseed)
    R = [rng.uniform(-1, 1) for _ in range(4)]
    ACC = rng.uniform(-1, 1); RES = rng.uniform(-1, 1)
    RESc = RES; ACCc = ACC; pend = 0.0
    DM = [0.0]*(DMASK+1); pos = 0
    nz = set(); traj = []
    for n in range(nsamp):
        pos = (pos+1) & DMASK
        for st in prog:
            addr = (pos - st['offset']) & DMASK
            mag = abs(st['coeff']); Cs = -(mag>>1) if st['coeff']<0 else (mag>>1)
            cf = 8.0*Cs/64.0
            res_for_b3 = RESc if res_latch else RES
            dab = res_for_b3 if st['b3'] else DM[addr]
            pk = pick(st)
            if reg_wbr:
                R[st['WA']] = dab; x = R[pk]
            else:
                x = R[pk]; R[st['WA']] = dab
            if st['ZERO']: ACC = 0.0
            if mac_pipe:
                ACC += pend; pend = x*cf
            else:
                ACC += x*cf
            xfer_src = (ACCc if acc_latch else ACC)
            if st['XFER']:
                newRES = xfer_src/8.0
                if res_latch:
                    if st['b3']: DM[addr] = res_for_b3; nz.add(addr)
                    RESc = newRES; RES = newRES
                else:
                    RES = newRES
                    if st['b3']: DM[addr] = RES; nz.add(addr)
            else:
                if st['b3']: DM[addr] = res_for_b3 if res_latch else RES; nz.add(addr)
            if acc_latch: ACCc = ACC
        if (n+1) % K == 0:
            s = math.sqrt(ACC*ACC+RES*RES+RESc*RESc+ACCc*ACCc+pend*pend
                          + sum(v*v for v in R)+sum(DM[i]*DM[i] for i in nz))+1e-300
            if (n+1) > warmup: traj.append(math.exp(math.log(s)/K))
            f = 1.0/s
            R=[v*f for v in R]; ACC*=f; RES*=f; RESc*=f; ACCc*=f; pend*=f
            for i in nz: DM[i]*=f
    tail = sorted(traj[-50:])
    return tail[len(tail)//2] if tail else float('nan')


# RA candidate decodes: 2 ordered bits from the control byte {b5,b4,b3}
PICKS = {
    '(b5,b4)': lambda st: (st['b5']<<1)|st['b4'],     # current
    '(b4,b5)': lambda st: (st['b4']<<1)|st['b5'],
    '(b5,b3)': lambda st: (st['b5']<<1)|st['b3'],
    '(b3,b5)': lambda st: (st['b3']<<1)|st['b5'],
    '(b4,b3)': lambda st: (st['b4']<<1)|st['b3'],
    '(b3,b4)': lambda st: (st['b3']<<1)|st['b4'],
}


def main():
    cache = PC.load()
    clean = [pid for pid in sorted(cache) if cache[pid]['clean']]
    print(f"clean programs: {[hex(p) for p in clean]}  ({len(clean)} of {len(cache)})\n")
    print(f"=== lambda (ppm) per clean program, by RA decode (base timing) ===")
    hdr = "decode      " + " ".join(f"{hex(p):>7s}" for p in clean) + "   #lossless"
    print(hdr)
    for name, pk in PICKS.items():
        cells = []; nloss = 0
        for p in clean:
            l = lam(cache[p]['prog'], pk)
            loss = abs(l-1) < 5e-4
            if loss: nloss += 1
            if l < 0.5: cells.append("dead")
            elif abs(l-1) < 5e-4: cells.append("  ~1 ")
            elif l > 1: cells.append(f"+{min((l-1)*1e6,9e5):.0f}")
            else: cells.append(f"{(l-1)*1e6:.0f}")
        print(f"{name:11s} " + " ".join(f"{c:>7s}" for c in cells) + f"     {nloss}/{len(clean)}")
    print("\n  A decode with #lossless == all-clean would be the real (software) fix.")
    print("  '+N' = N ppm over unity (hot); '~1' = lossless; numbers are per-program lambda.")


if __name__ == '__main__':
    main()
