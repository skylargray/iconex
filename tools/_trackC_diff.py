#!/usr/bin/env python3
"""Track C.1 -- formal pipeline reconcile.

Diff the TWO 224XL offset/microcode decoders across ALL 20 real programs:

  (A) aru224_emulate.tap_map(base)  -- reads the 0x3F4D offset buffer DOWNWARD
        (the VALIDATED source; delay = -offset). FE: B55B computes ptr-writeptr
        and moves 0x3cf1; non-FE: B55B copies a baked 128-entry table to 0x3F4D.
  (B) aru_datapath.load_microcode(power_up_id=ID) -- boots the firmware and reads
        mem[0x4000:0x4200], decoding offset = ~(l0|(l1<<8)) & 0xFFFF per 4-byte step.
        SESSION-11 SUSPECT: claimed-wrong source.

For each program tabulate: FE vs non-FE; whether 0x4000 is empty/all-zero/all-FF;
how many ACTIVE steps each decoder sees; whether their offset *sets* agree at all.
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import aru224_emulate as A
import aru_datapath as D
import boot_xl as B
import harvest_xl as H

MEM = A.load_mem()

# 20 real programs (drop the 0xFF terminator record)
BASES = [b for b in H.record_bases() if H.MEM[b] != 0xFF]


def emulate_offsets(base):
    """(A) tap_map offsets. Active = up to the first >=6-long run of -1 (0xFFFF) fill."""
    offs = A.tap_map(base, verbose=False)
    fs = len(offs); run = 0
    for i, v in enumerate(offs):
        if v == -1:
            run += 1
            if run >= 6:
                fs = i - run + 1; break
        else:
            run = 0
    active = offs[:fs]
    return offs, active


def datapath_offsets(power_up_id):
    """(B) boot firmware, read 0x4000:0x4200, decode active steps + their offsets.
    Returns (raw_img, prog, offsets, n_nonzero, n_ff_bytes)."""
    cpu, mem, *_ = B.boot(power_up_id=power_up_id, verbose=False)
    img = bytes(mem[0x4000:0x4200])
    prog = D.decode_image(img)                 # skips l2==l3==0xFF NOP/fill steps
    offsets = [p['offset'] for p in prog]
    n_nonzero = sum(1 for b in img if b != 0x00)
    n_ff = sum(1 for b in img if b == 0xFF)
    return img, prog, offsets, n_nonzero, n_ff


def set_overlap(a, b):
    """How many distinct values the two offset sets share (as magnitudes too)."""
    sa, sb = set(a), set(b)
    raw = sa & sb
    # also compare as delay magnitudes (tap_map reports signed offset; datapath
    # reports ~lane = a different 16-bit complement). Compare |value| sets.
    ma = set(abs(x) for x in a)
    mb = set(abs(x) for x in b)
    mag = ma & mb
    return len(raw), len(mag)


def main():
    rows = []
    print("Track C.1: two-decoder diff over 20 real programs\n")
    hdr = ("idx  recbase  ID    name(short)        FE   0x4000     "
           "A_act  B_act  rawShar magShar  verdict")
    for k, base in enumerate(BASES):
        pid = H.MEM[base]
        fe = MEM[(base + 0x30) & 0xFFFF] == 0xFE
        offs, active = emulate_offsets(base)
        try:
            img, prog, b_offs, nnz, nff = datapath_offsets(pid)
        except Exception as e:
            rows.append((k, base, pid, fe, "ERR", len(active), 0, 0, 0, f"boot fail: {e}"))
            continue
        # describe 0x4000 content
        if nnz == 0:
            mem4000 = "ALL-ZERO"
        elif nff == 512:
            mem4000 = "ALL-FF"
        else:
            mem4000 = f"{nnz}nz/{nff}ff"
        raw_shar, mag_shar = set_overlap(active, b_offs)
        rows.append((k, base, pid, fe, mem4000, len(active), len(prog),
                     raw_shar, mag_shar, ""))
    return rows


if __name__ == "__main__":
    rows = main()
    print(f"{'idx':>3} {'recbase':>7} {'ID':>4} {'FE':>5} {'0x4000':>10} "
          f"{'A_act':>5} {'B_act':>5} {'rawShar':>7} {'magShar':>7}  conclusion")
    n_b_empty = 0
    n_disagree = 0
    for (k, base, pid, fe, mem4000, a_act, b_act, raw_shar, mag_shar, err) in rows:
        if err:
            print(f"{k:3d} 0x{base:04X} 0x{pid:02X} {'FE' if fe else 'non':>5} {err}")
            continue
        # per-program one-line conclusion
        if b_act == 0 or mem4000 == "ALL-ZERO":
            concl = "0x4000 EMPTY -> datapath sees nothing"
            n_b_empty += 1
        elif mag_shar == 0:
            concl = "DISAGREE: 0 shared offset magnitudes"
            n_disagree += 1
        elif mag_shar < min(a_act, b_act) * 0.5:
            concl = f"MOSTLY DISAGREE ({mag_shar} shared mags)"
            n_disagree += 1
        else:
            concl = f"partial overlap ({mag_shar} shared mags)"
        print(f"{k:3d} 0x{base:04X} 0x{pid:02X} {'FE' if fe else 'non':>5} "
              f"{mem4000:>10} {a_act:5d} {b_act:5d} {raw_shar:7d} {mag_shar:7d}  {concl}")
    print()
    print(f"SUMMARY: {len(rows)} programs; "
          f"{n_b_empty} with empty 0x4000; {n_disagree} with material disagreement.")
    # quantify how garbage the 0x4000 offsets are vs tap_map's sane range
    print("\nB(0x4000) offset sanity per program (frac of active steps with |offset|>16384):")
    for k, base in enumerate(BASES):
        pid = H.MEM[base]
        _, prog, b_offs, _, _ = datapath_offsets(pid)
        big = sum(1 for o in b_offs if o > 16384)
        _, active = emulate_offsets(base)
        abig = sum(1 for v in active if abs(v) > 16384)
        print(f"  0x{base:04X} ID0x{pid:02X}: B {big:3d}/{len(b_offs):3d} >16384  | "
              f"A {abig:2d}/{len(active):3d} >16384")
