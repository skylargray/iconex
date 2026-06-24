#!/usr/bin/env python3
"""WF2: is the band-split ZERO asymmetry a universal template or CONCERT-specific?

For each Fig-4.1 hall + relatives, boot the real firmware, read the WCS image at
0x4000, locate the band-split / decay region (the steps the LOW/MID/XOV/HFD params
drive, from the per-program 224XL_param_sweep_<id>.json), split it into the two
mirror halves, and dump the RAW lane2 control byte + decoded ZERO bit for each step.

Then check: does one half carry an EXTRA accumulator clear (ZERO) vs the other?
This is exactly the CONCERT asymmetry (first half 3 clears, second half 1).

We report RAW bytes. lane2 control = (~stored) & 0xFF; ZERO = bit7 of control =
NOT(stored bit7).  So stored-byte bit7 SET => ZERO clear (no clear); stored bit7
CLEAR => ZERO asserted (accumulator cleared).
"""
import sys, os, json
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import boot_xl as B

REF = os.path.join(os.path.dirname(__file__), '..', 'docs', 'reference', '224')

# Fig-4.1 halls + relatives (id -> name)
PROGRAMS = [
    (0x01, "CONCERT HALL"),
    (0x20, "BRIGHT HALL"),
    (0x05, "DARK HALL"),
    (0x80, "RICH CHAMBER"),
    (0x40, "SMALL ROOM"),
    (0x08, "CHAMBER"),
    (0x81, "INVERSE ROOM"),
    (0x06, "HALL/HALL"),
    (0x41, "DARK CHAMBER"),
]


def load_wcs(pid):
    cpu, mem, *_ = B.boot(power_up_id=pid, verbose=False)
    return bytes(mem[0x4000:0x4200])


def decode_step(img, s):
    l0, l1, l2, l3 = img[s*4], img[s*4+1], img[s*4+2], img[s*4+3]
    if l2 == 0xFF and l3 == 0xFF:
        return None
    ctl = (~l2) & 0xFF
    coeff = (-(l3 & 0x7F) if l3 & 0x80 else (l3 & 0x7F))
    return dict(s=s, l2=l2, ctl=ctl,
                ZERO=(ctl >> 7) & 1, PROT=(ctl >> 6) & 1,
                RA=(ctl >> 4) & 3, b3=(ctl >> 3) & 1, XFER=(ctl >> 2) & 1,
                WA=ctl & 3, coeff=coeff)


def bandsplit_steps(pid):
    """Union of param0-3 (LOW/MID/XOV/HFD) coeff steps + the delay (param5) steps."""
    path = os.path.join(REF, f'224XL_param_sweep_{pid:02x}.json')
    if not os.path.exists(path):
        return None, None
    with open(path) as f:
        sw = json.load(f)
    decay = set()
    delay = set()
    pmap = {}
    for pr in sw['params']:
        p = pr['param']
        pmap[p] = sorted(pr['coeff_steps']) + sorted(pr['delay_steps'])
        if p in (0, 1, 2, 3):     # LOW, MID/?, XOV, HFD coeff params
            decay |= set(pr['coeff_steps'])
        if p == 5:
            delay |= set(pr['delay_steps'])
    return sorted(decay), pmap


def split_halves(steps):
    """Split a sorted step list into two halves at the largest gap."""
    if not steps:
        return [], []
    gaps = [(steps[i+1]-steps[i], i) for i in range(len(steps)-1)]
    if not gaps:
        return steps, []
    _, gi = max(gaps)
    return steps[:gi+1], steps[gi+1:]


def main():
    print(f"{'='*78}")
    print("Band-split ZERO asymmetry survey (RAW lane2 + decoded ZERO)")
    print(f"{'='*78}")
    summary = []
    for pid, name in PROGRAMS:
        decay, pmap = bandsplit_steps(pid)
        try:
            img = load_wcs(pid)
        except Exception as e:
            print(f"\n0x{pid:02x} {name}: BOOT FAILED: {e}")
            continue
        print(f"\n{'-'*78}")
        print(f"0x{pid:02x} {name}")
        if decay is None:
            print("  no param_sweep json; skipping band-split id")
            continue
        # param -> steps map for reference
        for p in sorted(pmap):
            lbl = {0:'LOW', 1:'MID?', 2:'XOV', 3:'HFD', 4:'p4', 5:'DLY'}.get(p, f'p{p}')
            print(f"    param{p} ({lbl}): {pmap[p]}")
        h1, h2 = split_halves(decay)
        print(f"  decay steps: half1={h1}  half2={h2}")
        # Per-half decode dump
        def dump(half, lbl):
            zeros = []
            print(f"  {lbl}:")
            for s in half:
                d = decode_step(img, s)
                if d is None:
                    print(f"    s{s:3d}: INACTIVE")
                    continue
                if d['ZERO']:
                    zeros.append(s)
                print(f"    s{s:3d}: l2=0x{d['l2']:02x} ctl=0x{d['ctl']:02x} "
                      f"ZERO={d['ZERO']} XFER={d['XFER']} b3={d['b3']} "
                      f"RA={d['RA']} WA={d['WA']} coeff={d['coeff']:+d}")
            return zeros
        z1 = dump(h1, "HALF 1")
        z2 = dump(h2, "HALF 2")
        # Compare ZERO positions, aligned by offset (half2 - half1 step delta)
        off = (h2[0] - h1[0]) if (h1 and h2) else None
        z1n = set(z1)
        z2n = set(s - off for s in z2) if off is not None else set()
        asym = (z1n != z2n)
        print(f"  ZERO in half1 (steps): {z1}")
        print(f"  ZERO in half2 (steps): {z2}   (offset half2-half1 = {off})")
        print(f"  ZERO count: half1={len(z1)} half2={len(z2)}  "
              f"=> {'ASYMMETRIC' if asym else 'SYMMETRIC'}")
        if asym and off is not None:
            only1 = sorted(z1n - z2n)
            only2 = sorted(s + off for s in (z2n - z1n))
            print(f"    extra clears in half1 (no mirror): {only1}")
            print(f"    extra clears in half2 (no mirror): {only2}")
        summary.append((pid, name, len(z1), len(z2), asym, off))
    print(f"\n{'='*78}\nSUMMARY")
    print(f"{'id':>5} {'name':<14} {'h1Z':>3} {'h2Z':>3} {'asym':>5} {'off':>4}")
    for pid, name, n1, n2, asym, off in summary:
        print(f"0x{pid:02x} {name:<14} {n1:>3} {n2:>3} {str(asym):>5} {str(off):>4}")


if __name__ == '__main__':
    main()
