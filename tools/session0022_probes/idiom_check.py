#!/usr/bin/env python3
"""Smoking-gun test for the RTL alignment (plan 021 Phase A pre-check).

The traced control pipeline (netlist 3.7/3.8/3.9/3.10 + 2T.3 + 4.9 + fig-3.4) gives:
  - XFER on word W captures the MAC complete through word W-1 (W's own product EXCLUDED,
    it lands at slots 4/7 of W+1 and slot 1 of W+2);
  - ZERO on word Z clears the ACC at slot 4 of Z's own step, DISCARDING pp_A(w_{Z-1})
    (the pairA partial of the previous word) while pp_B/pp_C(w_{Z-1}) still accumulate after.

For factory microcode to compute cleanly under this alignment, the word IMMEDIATELY BEFORE
a ZERO word must have a zero product contribution: cmag == 0 (full-clean) or at least
pairA-free (cmag < 16, partial). Under the BEHAVIORAL alignment (capture+clear both retire
with the word's own pend), no such constraint exists - a ZERO word would typically BE a MAC
word starting a new sum, and the previous word would be the XFER word of the old sum with
arbitrary cmag.

So: score P(cmag[prev]==0 | ZERO) across all 13 factory programs vs the base rate P(cmag==0).
Also report XFER-word cmag distribution + XFER/ZERO co-occurrence + row-L (extra word) decode.
"""
import json, os, sys
TOOLS = r"d:\OneDrive\Gray Instruments\iconex\tools"
sys.path.insert(0, TOOLS)
from aru_freerun22 import decode22

cache = json.load(open(os.path.join(TOOLS, "session0022_probes", "wcs_cache.json")))

def rows_for(wcs):
    """Physical-row order: row r = CPU word 127-r. Executed rows 0..L inclusive (L+1 steps,
    the fetch-pipeline extra word at row L = CPU word w_reset-1)."""
    firing = [k for k, w in enumerate(wcs) if (w[2] & 3) == 2 and ((w[0] >> 3) & 1) == 0]
    w_reset = max(firing)
    L = 128 - w_reset
    return [wcs[127 - r] for r in range(L + 1)], L, w_reset

tot_zero = 0; tot_zero_prev_cmag0 = 0; tot_zero_prev_pairAfree = 0
tot_xfer = 0; tot_xfer_cmag0 = 0
tot_words = 0; tot_cmag0 = 0
co_xz = 0
viol = []
for pid in sorted(cache, key=int):
    b = bytes.fromhex(cache[pid]["wcs"])
    if len(b) < 512:
        print(f"id {pid:>2}: SKIP (empty/short image, {len(b)} bytes)")
        continue
    wcs = [(b[4*k], b[4*k+1], b[4*k+2], b[4*k+3]) for k in range(128)]
    firing = [k for k, w in enumerate(wcs) if (w[2] & 3) == 2 and ((w[0] >> 3) & 1) == 0]
    if not firing:
        print(f"id {pid:>2}: SKIP (no reset word)")
        continue
    rows, L, w_reset = rows_for(wcs)
    dec = [decode22(*w) for w in rows]
    n = len(dec)
    tot_words += n
    tot_cmag0 += sum(1 for d in dec if d["cmag"] == 0)
    extra = dec[L]
    print(f"id {pid:>2}: L={L:3d} reset_word={w_reset:3d}  extra row{L} (CPU w{w_reset-1}): "
          f"typ={extra['typ']} cmag={extra['cmag']:2d} XFER={extra['XFER']} ZERO={extra['ZERO']} "
          f"ofst={extra['ofst']:5d} WA={extra['WA']} RA={extra['RA']}")
    for i, d in enumerate(dec):
        prev = dec[(i - 1) % n]        # continuous pipeline: row0's prev = row L of prev frame
        if d["ZERO"]:
            tot_zero += 1
            if prev["cmag"] == 0:
                tot_zero_prev_cmag0 += 1
            if prev["cmag"] < 16:
                tot_zero_prev_pairAfree += 1
            if prev["cmag"] != 0:
                viol.append((pid, i, prev["cmag"], d["typ"]))
        if d["XFER"]:
            tot_xfer += 1
            if d["cmag"] == 0:
                tot_xfer_cmag0 += 1
        if d["XFER"] and d["ZERO"]:
            co_xz += 1

print()
print(f"total executed words (incl. extra): {tot_words}; cmag==0 base rate: "
      f"{tot_cmag0}/{tot_words} = {tot_cmag0/tot_words:.2%}")
print(f"ZERO words: {tot_zero}")
print(f"  prev-word cmag==0   : {tot_zero_prev_cmag0}/{tot_zero} = "
      f"{tot_zero_prev_cmag0/max(1,tot_zero):.2%}   <-- RTL-alignment prediction ~100%")
print(f"  prev-word pairA-free (cmag<16): {tot_zero_prev_pairAfree}/{tot_zero}")
print(f"XFER words: {tot_xfer}; of which cmag==0: {tot_xfer_cmag0} "
      f"({tot_xfer_cmag0/max(1,tot_xfer):.2%})")
print(f"XFER & ZERO same word: {co_xz}")
if viol:
    print(f"\nviolations (ZERO with prev cmag!=0), first 20 of {len(viol)}:")
    for pid, i, c, t in viol[:20]:
        print(f"  id {pid} row {i}: prev cmag={c} (this typ={t})")
