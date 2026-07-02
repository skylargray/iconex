#!/usr/bin/env python3
"""C4 — re-derive the two non-wiring-pinned calibrations ON the RTL alignment:

(a) effective CSIGN polarity. E3b's verdict ("stored-direct self-oscillates, Multibus level
    stable") was measured on the BEHAVIORAL engine — the verdict is engine-relative, so it
    must be re-derived here. Registry note: this re-opens dead-ends #1/#2 DELIBERATELY,
    because those entries were scored in the pre-RTL alignment frame; the plan's own logic
    (all pre-0022 audio verdicts void when the frame moves) applies one level down.
    Test: silence-only self-excitation + impulse response, both polarities.

(b) PROT (MI22, stage-1 QC, consumer untraced). Census across the 13 programs; if asserted,
    try the netlist-plausible action (write-protect: suppress the MEMW) on CONCERT.
"""
import sys, os, json, math
TOOLS = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, TOOLS)
import numpy as np
from aru_freerun22_rtl import RTL22, program_rows22, fs22
from aru_freerun22 import decode22
from aru_rtl_dp import s16

HERE = os.path.dirname(os.path.abspath(__file__))
cache = json.load(open(os.path.join(HERE, "wcs_cache.json")))


def get_rows(pid="1", cs_stored_direct=False):
    b = bytes.fromhex(cache[pid]["wcs"])
    wcs = [(b[4*k], b[4*k+1], b[4*k+2], b[4*k+3]) for k in range(128)]
    rows, L, w_reset = program_rows22(wcs)
    if cs_stored_direct:
        for k, d in enumerate(rows):
            d["cs"] ^= 1
    return rows, L


# ---------- (b) PROT census ----------
print("--- PROT (l2 bit 6) census, 13 programs ---")
tot = {}
for pid in sorted(cache, key=int):
    b = bytes.fromhex(cache[pid]["wcs"])
    if len(b) < 512:
        continue
    wcs = [(b[4*k], b[4*k+1], b[4*k+2], b[4*k+3]) for k in range(128)]
    firing = [k for k, w in enumerate(wcs) if (w[2] & 3) == 2 and ((w[0] >> 3) & 1) == 0]
    if not firing:
        continue
    w_reset = max(firing)
    L = 128 - w_reset
    # MI22 = the Multibus level of stored l2 bit 6: asserted (PROT=1) when stored bit == 0
    ex = [(r, (( wcs[127-r][2] >> 6) & 1)) for r in range(L + 1)]
    n_prot_mi = sum(1 for r, sb in ex if sb == 0)
    tot[pid] = (n_prot_mi, L + 1)
    print(f"  id {pid:>2}: stored-bit6==0 (MI22 high) on {n_prot_mi}/{L+1} executed rows")

# ---------- (a) CSIGN polarity on the RTL engine ----------
rows_inv, L = get_rows(cs_stored_direct=False)   # cs = ~stored bit7 (current engine)
rows_dir, _ = get_rows(cs_stored_direct=True)    # cs = stored bit7
FS = fs22(L)
n = int(2.5 * FS)
blk = int(0.25 * FS)

def run_case(rows, impulse, tag):
    eng = RTL22()
    acc = 0; cnt = 0; blocks = []; peak = 0
    for i in range(n):
        outs = eng.run_sample(rows, 16422 if (impulse and i == 0) else 0)
        for c, v in outs:
            if c in "AC":
                acc += v * v
                peak = max(peak, abs(v))
        cnt += 1
        if cnt == blk:
            blocks.append(math.sqrt(acc / (2 * blk)))
            acc = 0; cnt = 0
    tank = sum(s16(v) * s16(v) for v in eng.DM.values())
    print(f"  [{tag}] peak={peak:6d}  tank(2.5s)={tank:.2e}")
    print("    blk(0.25s) RMS A+C: " + " ".join(f"{r:8.1f}" for r in blocks))
    return blocks, peak

print("\n--- CSIGN polarity on the RTL alignment (CONCERT boot) ---")
print("cs = ~stored bit7 (the E3b-behavioral 'stable' convention; current engine):")
run_case(rows_inv, False, "silence ")
run_case(rows_inv, True,  "impulse ")
print("cs = stored bit7 (stored-direct):")
run_case(rows_dir, False, "silence ")
run_case(rows_dir, True,  "impulse ")
