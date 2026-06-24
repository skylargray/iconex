#!/usr/bin/env python3
"""WF2d: for each hall's band-split block, identify the XFER closers and the
ZERO-bearing steps, and report bit7(ZERO) in BOTH halves, aligned.

This pins down: CONCERT's first half asserts ZERO at the XOV-closer (and an
interior step) where every OTHER mirrored hall asserts NO ZERO in EITHER half.
i.e. is CONCERT-half1 the lone outlier, and do all symmetric halls match
CONCERT-half2?
"""
import sys, os, json
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import boot_xl as B

REF = os.path.join(os.path.dirname(__file__), '..', 'docs', 'reference', '224')
PROGRAMS = [(0x01, "CONCERT"), (0x20, "BRIGHT HALL"), (0x05, "DARK HALL"),
            (0x40, "SMALL ROOM"), (0x08, "CHAMBER")]


def load_wcs(pid):
    cpu, mem, *_ = B.boot(power_up_id=pid, verbose=False)
    return bytes(mem[0x4000:0x4200])


def sweep(pid):
    with open(os.path.join(REF, f'224XL_param_sweep_{pid:02x}.json')) as f:
        return json.load(f)


def contiguous(sset, anchor):
    lo = hi = anchor
    while (lo-1) in sset: lo -= 1
    while (hi+1) in sset: hi += 1
    return lo, hi


def main():
    for pid, name in PROGRAMS:
        img = load_wcs(pid)
        sw = sweep(pid)
        pp = {pr['param']: sorted(set(pr['coeff_steps'])) for pr in sw['params']}
        allset = set()
        for p in (0,1,2,3): allset |= set(pp.get(p, []))
        xov = pp.get(2, [])
        mid = (xov[0]+xov[-1])/2 if xov else 0
        x1 = [s for s in xov if s < mid]; x2 = [s for s in xov if s >= mid]
        if not x1 or not x2:
            print(f"\n0x{pid:02x} {name}: single block (no two halves)"); continue
        lo1,hi1 = contiguous(allset, x1[0]); lo2,hi2 = contiguous(allset, x2[0])
        off = lo2-lo1
        print(f"\n0x{pid:02x} {name}  block s{lo1}..{hi1} | s{lo2}..{hi2}  off={off}")
        for k in range(hi1-lo1+1):
            s1, s2 = lo1+k, lo2+k
            c1 = (~img[s1*4+2])&0xFF; c2=(~img[s2*4+2])&0xFF
            z1=(c1>>7)&1; z2=(c2>>7)&1
            xf1=(c1>>2)&1; b31=(c1>>3)&1
            role = "XFER-closer" if (xf1 and b31) else ("XFER" if xf1 else "")
            tag = "  <== ZERO asym" if z1!=z2 else ""
            print(f"   s{s1:3d}/s{s2:3d}  ZERO={z1}/{z2}  XFER={xf1} b3={b31} {role}{tag}")


if __name__ == '__main__':
    main()
