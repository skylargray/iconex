#!/usr/bin/env python3
"""Pin the physical interpretation of the universal-lossless candidate.

The candidate (RA=(b3,b4) + timing acc_latch+reg_wbr) makes all 13 clean programs
lossless. But RA=(b3,b4) with b3 ALSO the DMEM read/write select makes b3 do double
duty. This sweeps decode interpretations -- (RA bits) x (which bit is DMEM-select) --
to find the most physically-coherent field map that still gives universal losslessness:

  A: RA=(b3,b4), DMEM-select=b3      (b3 dual-use; the candidate as first found)
  B: RA=(b3,b4), DMEM-select=b5      (clean single-use: b5<->b3 roles swapped)
  C: RA=(b4,b3), DMEM-select=b3
  D: RA=(b4,b3), DMEM-select=b5
  cur: RA=(b5,b4), DMEM-select=b3    (current model, base decode)

All with timing acc_latch+reg_wbr. Counts how many of the 13 clean programs are lossless.
"""
import sys, os, math, random
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import _hunt_progcache as PC
DMASK = 0xFFFF


def lam(prog, pick, dsel, acc_latch=True, reg_wbr=True, res_latch=False,
        nsamp=40000, K=128, warmup=10000, rseed=1):
    """Fully parametrized float power-iteration. pick(st)->0..3 is RA; dsel(st)->0/1 is
    the DMEM read/write select (replaces the hardwired st['b3'])."""
    rng = random.Random(rseed)
    R = [rng.uniform(-1, 1) for _ in range(4)]
    ACC = rng.uniform(-1, 1); RES = rng.uniform(-1, 1)
    RESc = RES; ACCc = ACC
    DM = [0.0]*(DMASK+1); pos = 0
    nz = set(); traj = []
    for n in range(nsamp):
        pos = (pos+1) & DMASK
        for st in prog:
            addr = (pos - st['offset']) & DMASK
            mag = abs(st['coeff']); Cs = -(mag>>1) if st['coeff']<0 else (mag>>1)
            cf = 8.0*Cs/64.0
            b3 = dsel(st)
            res_for_b3 = RESc if res_latch else RES
            dab = res_for_b3 if b3 else DM[addr]
            pk = pick(st)
            if reg_wbr:
                R[st['WA']] = dab; x = R[pk]
            else:
                x = R[pk]; R[st['WA']] = dab
            if st['ZERO']: ACC = 0.0
            ACC += x*cf
            xfer_src = ACCc if acc_latch else ACC
            if st['XFER']:
                newRES = xfer_src/8.0
                if res_latch:
                    if b3: DM[addr] = res_for_b3; nz.add(addr)
                    RESc = newRES; RES = newRES
                else:
                    RES = newRES
                    if b3: DM[addr] = RES; nz.add(addr)
            else:
                if b3: DM[addr] = res_for_b3 if res_latch else RES; nz.add(addr)
            if acc_latch: ACCc = ACC
        if (n+1) % K == 0:
            s = math.sqrt(ACC*ACC+RES*RES+RESc*RESc+ACCc*ACCc
                          + sum(v*v for v in R)+sum(DM[i]*DM[i] for i in nz))+1e-300
            if (n+1) > warmup: traj.append(math.exp(math.log(s)/K))
            f = 1.0/s
            R=[v*f for v in R]; ACC*=f; RES*=f; RESc*=f; ACCc*=f
            for i in nz: DM[i]*=f
    tail = sorted(traj[-50:])
    return tail[len(tail)//2] if tail else float('nan')


CFG = {
    'cur RA(b5,b4) D=b3': (lambda s:(s['b5']<<1)|s['b4'], lambda s:s['b3']),
    'A RA(b3,b4) D=b3':   (lambda s:(s['b3']<<1)|s['b4'], lambda s:s['b3']),
    'B RA(b3,b4) D=b5':   (lambda s:(s['b3']<<1)|s['b4'], lambda s:s['b5']),
    'C RA(b4,b3) D=b3':   (lambda s:(s['b4']<<1)|s['b3'], lambda s:s['b3']),
    'D RA(b4,b3) D=b5':   (lambda s:(s['b4']<<1)|s['b3'], lambda s:s['b5']),
}


def main():
    cache = PC.load()
    clean = [p for p in sorted(cache) if cache[p]['clean']]
    print("decode interpretation sweep, timing=acc_latch+reg_wbr, all clean programs")
    print(f"{'config':22s} #lossless   off-programs (ppm)")
    for name, (pk, ds) in CFG.items():
        nloss = 0; offs = []
        for p in clean:
            l = max(lam(cache[p]['prog'], pk, ds, rseed=1),
                    lam(cache[p]['prog'], pk, ds, rseed=7))
            if abs(l-1) < 5e-4: nloss += 1
            else:
                offs.append(f"{p:#x}:{(l-1)*1e6:+.0f}" if abs(l-1)<2 else f"{p:#x}:{l:.2f}x")
        print(f"{name:22s} {nloss:2d}/{len(clean)}      {'  '.join(offs) if offs else 'ALL LOSSLESS'}")


if __name__ == '__main__':
    main()
