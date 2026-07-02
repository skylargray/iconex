#!/usr/bin/env python3
"""E1b (plan 023) — predict the ARU no-feedback signature window length from the diag-3
WCS + the 0023/0024 alignment, BEFORE running the co-sim. The manual's +5V reference
'29F3' calibrates at N = 62 ARUCK edges (sig224); the prediction must land there.

Timing facts (engine header, traced):
  ARUCK rising edges at slots ~0.58 / 3.58 / 6.58 of every step (3 per step; PR latches).
  RESET/ low during slots 0..6 of the POST-reset step (falls at slot-0 boundary of step
  r_reset+1, rises at slot 7); RESET fires during the reset word's fields-live step r_reset.
  XFER CK rises at slot ~3.06 of step n iff w_{n-1}.XFER.

The HP-5004A gates synchronously: the window = ARUCK edges strictly after the START edge
up to and including / excluding the STOP-qualified edge (convention enumerated below —
the SAME convention must give N=62 (no-feedback: START=RESET/, STOP=XFERCK) AND N=90
(feedback: START=STOP=RESET/, one frame = 30 steps x 3 edges)).
"""
import sys, os, json

TOOLS = r"d:\OneDrive\Gray Instruments\iconex\tools"
sys.path.insert(0, TOOLS)
HERE = os.path.dirname(os.path.abspath(__file__))

from aru_freerun22_rtl import program_rows22

cache = json.load(open(os.path.join(HERE, "wcs_diag.json")))
img = bytes.fromhex(cache["sig3"]["wcs"])
wcs = [(img[4*k], img[4*k+1], img[4*k+2], img[4*k+3]) for k in range(128)]
rows, L, w_reset = program_rows22(wcs)
F = L + 1
r_reset = 127 - w_reset
print(f"diag-3: reset word {w_reset} -> L={L}, F={F} steps, reset row r={r_reset}")

xfer_rows = [n for n, d in enumerate(rows) if d["XFER"]]
zero_rows = [n for n, d in enumerate(rows) if d["ZERO"]]
print(f"XFER rows (w_{{n-1}}.XFER -> XFERCK rise at slot 3.06 of step n): {xfer_rows}")
print(f"  -> XFERCK rises during steps: {[(n + 1) % F for n in xfer_rows]}")
print(f"ZERO rows: {zero_rows}")

# per-row summary for the record
print("\nrow | typ sel cmag cs XFER ZERO ofst")
for n, d in enumerate(rows):
    print(f" {n:3d} | {d['typ']} {d.get('sel','-')} {d['cmag']:2d} {d['cs']} "
          f"{int(d['XFER'])} {int(d['ZERO'])} 0x{d['ofst']:04X}"
          + ("   <RESET word>" if n == r_reset else "")
          + ("   <extra idle row L>" if n == L else ""))

# ---------------------------------------------------------------- edge timeline
# Slot-time coordinates: step n spans [9n, 9(n+1)) in MS slots. ARUCK RISING edges at
# 9n + {0.58, 3.58, 6.58} (the PR latch edges, tc_clock calibration); FALLING edges half
# an ARUCK period (1.5 slots) later at 9n + {2.08, 5.08, 8.08}. RESET/ low during slots
# 0..6 of the post-reset step: fall at 9*(r_reset+1)+0.0, rise at 9*(r_reset+1)+7.0.
# XFERCK rise at 9*s + 3.06 (fall ~1.06) for each step s with w_{s-1}.XFER.
GRIDS = {"ARUCK rise": (0.58, 3.58, 6.58), "ARUCK fall": (2.08, 5.08, 8.08)}

def edges_of(grid, n_frames=3):
    return [9*(F*f + s) + o for f in range(n_frames) for s in range(F) for o in grid]

def reset_fall(f):  return 9*(F*f + r_reset + 1) + 0.0
def reset_rise(f):  return 9*(F*f + r_reset + 1) + 7.0

def xferck_rises(n_frames=3):
    return [9*(F*f + s) + 3.06 for f in range(n_frames) for s in range(F)
            if rows[(s - 1) % F]["XFER"]]

xrises = xferck_rises()

print("\n### window-length enumeration (clock grid x START polarity x stop side) ###")
winners = []
for gname, grid in GRIDS.items():
    edges = edges_of(grid)
    for start_name, start_t in (("RESET/ fall", reset_fall(0)), ("RESET/ rise", reset_rise(0))):
        stop_t = min(x for x in xrises if x > start_t)          # first XFERCK rise
        fstop = (reset_fall(1) if "fall" in start_name else reset_rise(1))
        for side, pred in (("(start,stop]", lambda e, s: start_t < e <= s),
                           ("(start,stop)", lambda e, s: start_t < e < s)):
            n_nfb = sum(1 for e in edges if pred(e, stop_t))
            n_fb = sum(1 for e in edges if pred(e, fstop))
            hit = (n_nfb, n_fb) == (62, 90)
            print(f"  {gname:10s} START={start_name:11s} {side}: "
                  f"no-feedback N={n_nfb:3d}  feedback N={n_fb:3d}"
                  + ("   <== BOTH TARGETS" if hit else ""))
            if hit:
                winners.append((gname, start_name, side))

print("\nTARGETS: no-feedback N=62 (29F3), feedback N=90 (3696)")
print(f"conventions hitting BOTH: {winners if winners else 'NONE'}")
print("\nStructural content independent of the +-1 gating convention: the first XFERCK")
print("rise after the RESET/ edge is at step 20 of the NEXT frame (rows 19-24/26/28 carry")
print("XFER; steps 20-25/27/29 get the CK). 20 steps x 3 edges + the slot-3.06 fraction")
print("=> N in {61,62} by gating; a wrong XFER placement (step 19/21) would give ~59/65.")
