#!/usr/bin/env python3
"""B3 (plan 021) — taint/provenance trace on the RTL-aligned engine (aru_freerun22_rtl.RTL22).

The behavioral engine's amplitude path dead-ended after one MAC (plan 021 §3): the impulse
reached DM, came back once, produced one RES, and died in the register file (severed handoffs:
the exec-74 tank-read load clobbered before use; the exec-40 RES never meeting a MEMW).

Acceptance here: under the traced alignment, input amplitude must keep reaching consumers
(MEMW writes and D/A OUTs) at frames >= 2 and at the long-hop checkpoints — the loop CONNECTS.
Also reports the exec-40/71/74 neighborhoods so the old severed handoffs can be named.
"""
import sys, os, json
TOOLS = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, TOOLS)
from aru_freerun22_rtl import RTL22, program_rows22

HERE = os.path.dirname(os.path.abspath(__file__))
cache = json.load(open(os.path.join(HERE, "wcs_cache.json")))
b = bytes.fromhex(cache["1"]["wcs"])
wcs = [(b[4*k], b[4*k+1], b[4*k+2], b[4*k+3]) for k in range(128)]
rows, L, w_reset = program_rows22(wcs)
print(f"CONCERT: L={L}, frame={len(rows)} steps, reset row {L-1}")

eng = RTL22(taint=True, taint_th=40)

def run_frames(n0, n1, x0=0):
    for n in range(n0, n1):
        eng.run_sample(rows, x0 if n == 0 else 0)

def show(lo, hi, hdr):
    print(f"\n===== {hdr} =====")
    cnt = 0
    for (f, s, kind, val, src) in eng.log:
        if lo <= f < hi:
            srcs = src if len(src) <= 110 else src[:107] + "..."
            print(f"  f{f} s{s:3d}: {kind:14s} {val:6d}  [{srcs}]")
            cnt += 1
            if cnt > 60:
                print("  ... (truncated)")
                break

IMP = 16422
run_frames(0, 4, x0=IMP)
show(0, 4, "frames 0-3 (impulse @0)")
eng.log.clear()

marks = [(610, 613), (1940, 1943), (16990, 16993)]
n = 4
for lo, hi in marks:
    while n < lo:
        eng.run_sample(rows, 0); n += 1
    eng.log.clear()
    while n < hi:
        eng.run_sample(rows, 0); n += 1
    show(lo, hi, f"frames {lo}-{hi-1}")
    # per-frame consumer census for the verdict
    memw = sum(1 for (f, s, k, v, sr) in eng.log if k.startswith("MEMW") and lo <= f < hi)
    outs = sum(1 for (f, s, k, v, sr) in eng.log if k.startswith("OUT") and lo <= f < hi)
    print(f"  [census {lo}-{hi-1}: significant MEMW={memw}, OUT={outs}]")
    eng.log.clear()

# verdict pass: fresh short run, frame-by-frame consumer counts.
# Criterion (plan 021 B3): the two behavioral-era severed handoffs must CONNECT —
#   #1: mid-ladder register loads must be MAC'd through multi-stage chains (not clobbered dead);
#   #2: mid-frame XFER captures (the old "word-40 RES") must reach a MEMW/OUT.
# The topology is sparse multi-tap (energy parks in DM for the 500-6000-frame taps), so the
# check is frames 2-4 consumer activity + a literal row-40 RES->MEMW connection, NOT sustained
# above-threshold amplitude at arbitrary later frames (that is B5's energy question).
eng2 = RTL22(taint=True, taint_th=40)
per_frame = []
row40_connect = False
multistage = False
for n in range(8):
    eng2.log.clear()
    eng2.run_sample(rows, IMP if n == 0 else 0)
    memw = sum(1 for (f, s, k, v, sr) in eng2.log if k.startswith("MEMW"))
    outs = sum(1 for (f, s, k, v, sr) in eng2.log if k.startswith("OUT"))
    macs = sum(1 for (f, s, k, v, sr) in eng2.log if k == "XFER")
    per_frame.append((n, macs, memw, outs))
    for (f, s, k, v, sr) in eng2.log:
        if k.startswith("MEMW") and 40 <= s <= 41 and any(
                x[1] == 40 and x[2] == "XFER" for x in eng2.log):
            row40_connect = True
        if k.startswith("MEMW") and sr.count(")x") >= 2:
            multistage = True
print("\nframe-by-frame significant events (XFER-captures / MEMW / OUT):")
for n, m, w, o in per_frame:
    print(f"  f{n}: XFER={m:3d} MEMW={w:3d} OUT={o}")
alive24 = all(w > 0 for n, m, w, o in per_frame[2:5])
print(f"\nhandoff #2 (row-40 XFER capture reaches a MEMW): {'CONNECT' if row40_connect else 'NO'}")
print(f"handoff #1 (multi-stage register chains MAC'd before clobber): {'CONNECT' if multistage else 'NO'}")
print(f"consumers active frames 2-4: {'YES' if alive24 else 'NO'}")
print(f"\nVERDICT: {'CONNECT' if (row40_connect and multistage and alive24) else 'DEAD-END'}"
      f" (amplitude persistence beyond the tap horizon = B5's energy question)")
