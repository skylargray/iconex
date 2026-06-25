#!/usr/bin/env python3
"""Full-device-decode rebuild (owner's complete T&C trace) + all-reverbs-lossless test.

Device decode (confirmed):
  MEMAC = MI17  -> DRAM op iff MI17=1 ; MI16=1 read / MI16=0 write (DRAM addr = pos-offset, 16-bit).
  sub-decoder (MI17=0 & MI16=1), DAB read source by (MI13,MI12):
     00 idle(0) ; 01 RDRREG/ -> result reg ; 10 RD XREG/ -> X reg(0) ; 11 RD AD/ -> A/D input.
  (MI17=0 & MI16=0) -> idle. WR DA/ (D/A out) from MI16/MI17 first-half (output side).
  MI12,MI13 = microword bits 12,13 (l1). offset = MI0-15 (l0,l1). XFER=MI24, ZERO=MI25, coeff=MI26-31, CSIGN=MI23.
Closed-loop reverb: RD AD/ injects 0 (no audio in); RDRREG/ feeds the result register back; idle/X-reg = 0.
acc_latch timing. Sweep byte inversions to find all-reverbs-lossless (then diagnostics pin the exact one).
"""
import sys, os, math, random
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import _hunt_rawcache as RC
MASK = 0xFFFF


def decode(steps, inv_l2, inv_l3, inv_l1=True):
    prog = []
    for (s, l0, l1, l2, l3) in steps:
        vl1 = (~l1 & 0xFF) if inv_l1 else (l1 & 0xFF)
        v2 = (~l2 & 0xFF) if inv_l2 else (l2 & 0xFF)
        v3 = (~l3 & 0xFF) if inv_l3 else (l3 & 0xFF)
        offset = (~(l0 | (l1 << 8))) & MASK
        MI16 = v2 & 1; MI17 = (v2 >> 1) & 1
        WA = (v2 >> 2) & 3; RA = (v2 >> 4) & 3; csign = (v2 >> 7) & 1
        MI12 = (vl1 >> 4) & 1; MI13 = (vl1 >> 5) & 1
        xfer = v3 & 1; zero = (v3 >> 1) & 1; cmag = (v3 >> 2) & 0x3F
        Cs = -cmag if csign else cmag
        prog.append(dict(s=s, offset=offset, MI16=MI16, MI17=MI17, WA=WA, RA=RA,
                         XFER=xfer, ZERO=zero, Cs=Cs, sub=(MI13 << 1) | MI12))
    return prog


def lam(prog, read_bit=1, nsamp=40000, K=128, warmup=10000, rseed=1, ad_input=None):
    """read_bit = MI16 value meaning READ. ad_input: callable(n)->float for RD AD/ (else 0)."""
    rng = random.Random(rseed)
    R = [rng.uniform(-1, 1) for _ in range(4)]
    ACC = rng.uniform(-1, 1); RES = rng.uniform(-1, 1); ACCc = ACC
    DM = [0.0]*(MASK+1); pos = 0; nz = set(); traj = []
    for n in range(nsamp):
        pos = (pos+1) & MASK
        for st in prog:
            addr = (pos - st['offset']) & MASK
            is_dram = st['MI17'] == 1
            is_read = is_dram and (st['MI16'] == read_bit)
            is_write = is_dram and not is_read
            is_sub = (st['MI17'] == 0) and (st['MI16'] == 1)
            if is_read:
                dab = DM[addr]
            elif is_sub and st['sub'] == 1:        # RDRREG/  -> result reg
                dab = RES
            elif is_sub and st['sub'] == 3:        # RD AD/   -> audio input
                dab = (ad_input(n) if ad_input else 0.0)
            elif is_write:
                dab = RES                          # DRAM write data = result register
            else:
                dab = 0.0                          # RD XREG / idle
            x = R[st['RA']]; R[st['WA']] = dab
            if st['ZERO']: ACC = 0.0
            ACC += x * 8.0 * st['Cs'] / 64.0
            if st['XFER']: RES = ACCc / 8.0        # acc_latch
            if is_write: DM[addr] = RES; nz.add(addr)
            ACCc = ACC
        if (n+1) % K == 0:
            s = math.sqrt(ACC*ACC+RES*RES+ACCc*ACCc+sum(v*v for v in R)+sum(DM[i]*DM[i] for i in nz))+1e-300
            if (n+1) > warmup: traj.append(math.exp(math.log(s)/K))
            f = 1.0/s
            R=[v*f for v in R]; ACC*=f; RES*=f; ACCc*=f
            for i in nz: DM[i]*=f
    tail = sorted(traj[-50:])
    return tail[len(tail)//2] if tail else float('nan')


def main():
    import itertools
    cache = RC.load()
    clean = [p for p in sorted(cache) if cache[p]['clean']]
    NS = int(os.environ.get('NS', '16000')); WU = int(os.environ.get('WU', '4000'))
    print(f"full-device-decode all-reverbs test, {len(clean)} clean programs (RD AD=0)\n")
    print(f"{'inv_l2':6s} {'inv_l3':6s} {'read_bit':8s}  #loss  hot/dead")
    for inv_l2, inv_l3, rb in itertools.product((True, False), (True, False), (0, 1)):
        nloss = 0; bad = []
        for p in clean:
            prog = decode(cache[p]['steps'], inv_l2, inv_l3)
            l = lam(prog, read_bit=rb, nsamp=NS, warmup=WU, rseed=1)
            if abs(l-1) < 5e-4: nloss += 1
            elif l > 1: bad.append(f"{p:#x}:{(l-1)*1e6:+.0f}" if abs(l-1)<2 else f"{p:#x}:{l:.1f}x")
            elif l < 0.5: bad.append(f"{p:#x}:dead")
        print(f"{str(inv_l2):6s} {str(inv_l3):6s} {rb:8d}  {nloss:2d}/{len(clean)}  "
              f"{'all<=1 (no hot)' if not any(':' in b and 'dead' not in b for b in bad) else ' '.join(bad[:5])}")


if __name__ == '__main__':
    main()
