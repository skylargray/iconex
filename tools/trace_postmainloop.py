#!/usr/bin/env python3
"""Boot to CONCERT, then run PAST mainloop for audio-frame processing, watching the 0x4000 WCS
region. Question: does the diffuser block (0x4010+, = B3 1A FF FF / cmag=0 at mainloop) get
REWRITTEN per-frame with live coefficients, or does it stay constant? Answered by observation."""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
sys.stdout.reconfigure(encoding="utf-8")
import boot8080 as B
from trace8080 import Trace8080
from aru_rtl_dp import decode

EXTRA = int(sys.argv[sys.argv.index("--extra") + 1]) if "--extra" in sys.argv else 8_000_000

tr = Trace8080(watch_range=(0x4000, 0x41FF))
print(f"booting to CONCERT, then +{EXTRA} ticks past mainloop, watching 0x4000-0x41FF...")
m, ms = B.boot(verbose=True, trace=tr, extra_ticks_after_mainloop=EXTRA)
print(f"\nmilestones: {ms}")

# mainloop order boundary
ml_order = next((o for o, l in tr.markers if l == "mainloop"), None)
pre = [w for w in tr.watch if ml_order is None or w[0] <= ml_order]
post = [w for w in tr.watch if ml_order is not None and w[0] > ml_order]
print(f"\nwrites to 0x4000-0x41FF: {len(tr.watch)} total; {len(pre)} up to mainloop, {len(post)} AFTER mainloop")

if post:
    addrs = sorted(set(a for _, _, a, _ in post))
    print(f"AFTER-mainloop write addresses ({len(addrs)}): " +
          " ".join(f"{a:04X}" for a in addrs[:48]) + (" ..." if len(addrs) > 48 else ""))
    pcs = sorted(set(pc for _, pc, _, _ in post))
    print(f"AFTER-mainloop writer PCs: " + " ".join(f"{p:04X}" for p in pcs[:24]))
    # which WCS steps (4-byte) are touched, and do lane2/3 (coeff/control) change?
    steps = sorted(set((a - 0x4000) // 4 for _, _, a, _ in post))
    print(f"AFTER-mainloop WCS steps touched: {steps[:40]}")
    diff_steps = [s for s in steps if 5 <= s <= 23]
    print(f"  of which diffuser steps (5-23): {diff_steps}")
else:
    print("NO writes to the WCS region after mainloop in this window.")

# show the final diffuser block decode
print("\nfinal 0x4000 WCS, steps 0-26 (lane bytes -> cmag/XFER/ZERO):")
mem = m.memory
for s in range(27):
    a = 0x4000 + s * 4
    l0, l1, l2, l3 = mem[a], mem[a + 1], mem[a + 2], mem[a + 3]
    d = decode(l2, l3)
    print(f"  step {s:3d}: {l0:02X} {l1:02X} {l2:02X} {l3:02X}  cmag={d['cmag']:2d} XFER={d['XFER']} ZERO={d['ZERO']}")
