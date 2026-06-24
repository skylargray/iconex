#!/usr/bin/env python3
"""WF2b: per-program, align the two band-split halves as MIRROR PAIRS and report
the EXACT lane2 byte differences (and which bit differs).

For CONCERT the established fact is: the two halves' lane2 control bytes are
byte-identical EXCEPT lane2 bit7 (ZERO) at the XOV closers s44/s96 and s46/s98.
Here we test, for every hall: when we align half1 step k with half2 step k+off,
are the halves byte-identical-except-bit7, or do they differ structurally
(=> serial stages, not stereo mirrors)?

We focus on the CONTIGUOUS band-split block = param2(XOV) ∪ param3(HFD) ∪ param0(LOW)
∪ the param1 steps adjacent to them (the local LOW/MID/XOV/HFD cluster), NOT the
distant param1-only comb taps. We take the contiguous run that contains the XOV
steps.
"""
import sys, os, json
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import boot_xl as B

REF = os.path.join(os.path.dirname(__file__), '..', 'docs', 'reference', '224')
PROGRAMS = [
    (0x01, "CONCERT HALL"), (0x20, "BRIGHT HALL"), (0x05, "DARK HALL"),
    (0x80, "RICH CHAMBER"), (0x40, "SMALL ROOM"), (0x08, "CHAMBER"),
    (0x81, "INVERSE ROOM"), (0x06, "HALL/HALL"), (0x41, "DARK CHAMBER"),
]


def load_wcs(pid):
    cpu, mem, *_ = B.boot(power_up_id=pid, verbose=False)
    return bytes(mem[0x4000:0x4200])


def sweep(pid):
    with open(os.path.join(REF, f'224XL_param_sweep_{pid:02x}.json')) as f:
        return json.load(f)


def contiguous_run(steps_set, anchor):
    """Return the maximal contiguous run (gap<=1) of steps_set containing anchor."""
    lo = anchor
    while (lo - 1) in steps_set:
        lo -= 1
    hi = anchor
    while (hi + 1) in steps_set:
        hi += 1
    return lo, hi


def main():
    for pid, name in PROGRAMS:
        img = load_wcs(pid)
        sw = sweep(pid)
        pp = {pr['param']: sorted(set(pr['coeff_steps'])) for pr in sw['params']}
        # all decay-param steps as a set
        allset = set()
        for p in (0, 1, 2, 3):
            allset |= set(pp.get(p, []))
        # XOV steps define the two halls' band-split anchors
        xov = pp.get(2, [])
        if len(xov) < 2:
            print(f"\n0x{pid:02x} {name}: <2 XOV steps; skip")
            continue
        # group xov into two halves by gap
        xov_h1 = [s for s in xov if s < (xov[0] + xov[-1]) / 2]
        xov_h2 = [s for s in xov if s not in xov_h1]
        a1, a2 = xov_h1[0], xov_h2[0]
        lo1, hi1 = contiguous_run(allset, a1)
        lo2, hi2 = contiguous_run(allset, a2)
        off = lo2 - lo1
        print(f"\n{'='*72}\n0x{pid:02x} {name}")
        print(f"  band-split block half1 = s{lo1}..s{hi1}  half2 = s{lo2}..s{hi2}  off={off}")
        n = max(hi1 - lo1, hi2 - lo2) + 1
        diffs = []
        for k in range(n):
            s1, s2 = lo1 + k, lo2 + k
            b1 = img[s1*4+2] if s1 <= 127 else None
            b2 = img[s2*4+2] if s2 <= 127 else None
            c1 = img[s1*4+3] if s1 <= 127 else None
            c2 = img[s2*4+3] if s2 <= 127 else None
            if b1 is None or b2 is None:
                continue
            mark = ""
            if b1 != b2:
                x = b1 ^ b2
                bits = [str(i) for i in range(8) if (x >> i) & 1]
                mark = f"  <-- lane2 DIFF bits {bits}"
            print(f"    s{s1:3d}/s{s2:3d}: l2 0x{b1:02x}/0x{b2:02x}  "
                  f"l3 0x{c1:02x}/0x{c2:02x}{mark}")
            if b1 != b2:
                diffs.append((s1, s2, b1, b2, b1 ^ b2))
        if not diffs:
            print("  => halves byte-IDENTICAL in lane2 (perfect stereo mirror)")
        else:
            only7 = all(d[4] == 0x80 for d in diffs)
            print(f"  => {len(diffs)} lane2 diffs; "
                  f"{'ALL are bit7(ZERO)-only' if only7 else 'NOT all bit7 — structural differences'}")


if __name__ == '__main__':
    main()
