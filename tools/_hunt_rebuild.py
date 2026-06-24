#!/usr/bin/env python3
"""Rebuild the microword decode from the owner's schematic trace and test all-programs-lossless.

Confirmed bit map (by MI bit; l2=MI16-23, l3=MI24-31 stored bytes):
  DMEM-op = MI17 (l2.b1), DMEM read(1)/write(0) = MI16 (l2.b0)   [U47 LS139: MEMW/=MI17&!MI16, MEMR/=MI17&MI16]
  WA0=MI18(l2.b2) WA1=MI19(l2.b3) ; RA0=MI20(l2.b4) RA1=MI21(l2.b5) ; CSIGN=MI23(l2.b7)
  XFER=MI24(l3.b0) ; ZERO=MI25(l3.b1) ; coeff C0..C5 = MI26..MI31 (l3.b2..b7)
  offset = l0,l1 (kept from old decode; OFST trace pending)
Polarities/inversions per byte are swept (the trace gives bit POSITIONS; the old model established
inversions only for its mis-assigned fields). Recirc model: a step reads DMEM only if DMEM-op & read,
writes RES->DMEM if DMEM-op & write, else DAB source = result register. acc_latch timing (manual-confirmed).
Objective: which coherent inversion choice makes ALL clean programs lossless?
"""
import sys, os, math, random
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import _hunt_rawcache as RC
MASK = 0xFFFF


def decode(steps, inv2, inv3):
    prog = []
    for (s, l0, l1, l2, l3) in steps:
        v2 = (~l2 & 0xFF) if inv2 else (l2 & 0xFF)
        v3 = (~l3 & 0xFF) if inv3 else (l3 & 0xFF)
        offset = (~(l0 | (l1 << 8))) & MASK              # old convention (delays verified before)
        dmem_rw = v2 & 1                                  # MI16
        dmem_op = (v2 >> 1) & 1                           # MI17
        WA = (v2 >> 2) & 3                                # MI18,19
        RA = (v2 >> 4) & 3                                # MI20,21
        csign = (v2 >> 7) & 1                             # MI23
        xfer = v3 & 1                                     # MI24
        zero = (v3 >> 1) & 1                              # MI25
        cmag = (v3 >> 2) & 0x3F                           # MI26-31
        Cs = -cmag if csign else cmag
        prog.append(dict(s=s, offset=offset, dmem_rw=dmem_rw, dmem_op=dmem_op,
                         WA=WA, RA=RA, XFER=xfer, ZERO=zero, Cs=Cs))
    return prog


def lam(prog, read_val=1, reg_wbr=True, nsamp=40000, K=128, warmup=10000, rseed=1):
    """acc_latch float power iteration with the corrected DMEM/DAB recirculation.
    read_val = the dmem_rw value that means READ (so write = 1-read_val)."""
    rng = random.Random(rseed)
    R = [rng.uniform(-1, 1) for _ in range(4)]
    ACC = rng.uniform(-1, 1); RES = rng.uniform(-1, 1); ACCc = ACC
    DM = [0.0]*(MASK+1); pos = 0; nz = set(); traj = []
    for n in range(nsamp):
        pos = (pos+1) & MASK
        for st in prog:
            addr = (pos - st['offset']) & MASK
            is_read = st['dmem_op'] and (st['dmem_rw'] == read_val)
            is_write = st['dmem_op'] and not is_read
            dab = DM[addr] if is_read else RES            # else: result register drives DAB
            if reg_wbr:
                R[st['WA']] = dab; x = R[st['RA']]
            else:
                x = R[st['RA']]; R[st['WA']] = dab
            if st['ZERO']: ACC = 0.0
            ACC += x * 8.0 * st['Cs'] / 64.0
            if st['XFER']: RES = ACCc / 8.0               # acc_latch: pre-product group sum
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
    cache = RC.load()
    clean = [p for p in sorted(cache) if cache[p]['clean']]
    print(f"corrected-decode all-programs test, {len(clean)} clean programs, acc_latch\n")
    print(f"{'inv2':5s} {'inv3':5s} {'readVal':7s} {'reg_wbr':7s}  #loss  hot(ppm)")
    import itertools
    for inv2, inv3, read_val, rwbr in itertools.product((True, False), (True, False), (0, 1), (True, False)):
        progs = {p: decode(cache[p]['steps'], inv2, inv3) for p in clean}
        nloss = 0; hot = []
        for p in clean:
            l = lam(progs[p], read_val=read_val, reg_wbr=rwbr, nsamp=int(os.environ.get('NS','16000')),
                    warmup=int(os.environ.get('WU','4000')), rseed=1)
            if abs(l-1) < 5e-4: nloss += 1
            elif l > 1: hot.append(f"{p:#x}:{(l-1)*1e6:+.0f}" if abs(l-1)<2 else f"{p:#x}:{l:.1f}x")
        print(f"{str(inv2):5s} {str(inv3):5s} {read_val:7d} {str(rwbr):7s}  {nloss:2d}/{len(clean)}  "
              f"{'ALL LOSSLESS' if not hot else ' '.join(hot[:5])}")


if __name__ == '__main__':
    main()
