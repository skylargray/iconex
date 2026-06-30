#!/usr/bin/env python3
"""Boot the real 224XL firmware to CONCERT under the full write+I/O tracer (verified core), and
DISCOVER — not assume — where the firmware writes microcode and what it streams over I/O.

Run:
  python tools/trace_concert.py                 # discovery report (write histogram + I/O)
  python tools/trace_concert.py --window        # + full per-write log of prog_load->mainloop,
                                                #   saved to scratchpad for byte-exact reconstruction
"""
import os
import sys
import json

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
sys.stdout.reconfigure(encoding="utf-8")
import boot8080 as B
from trace8080 import Trace8080

SCR = (r"C:/Users/Skylar/AppData/Local/Temp/claude/"
       r"d--OneDrive-Gray-Instruments-iconex/f950f5a4-d96d-4fdd-899a-08b03ca853c7/scratchpad")

window = "--window" in sys.argv
# Capture the full per-write log across the WHOLE post-handshake run so we can see the microcode
# build wherever it happens; the window form additionally isolates prog_load->mainloop.
tr = Trace8080(full_writes=window, capture_window=("prog_load", "mainloop") if window else None)

print("booting v8.2.1 to CONCERT under full write+I/O trace (verified kosarev core)...")
m, ms = B.boot(verbose=True, trace=tr)
print(f"\nmilestones: {ms}")
print(f"reached mainloop: {'mainloop' in ms}, prog_load: {'prog_load' in ms}")

tr.print_report(region_detail=(0x4000, 64))

# Save the aggregate histogram + I/O for downstream analysis
hist = tr.write_histogram()
out = {
    "total_writes": tr.n,
    "markers": tr.markers,
    "pages": [{"base": r["base"], "count": r["count"], "first": r["first"], "last": r["last"],
               "phases": r["phases"], "writers": [f"{p:04X}" for p in r["writers"]]} for r in hist],
    "io": [(o, d, p, v) for (o, d, p, v) in tr.io],
}
with open(os.path.join(SCR, "trace_concert_aggregate.json"), "w") as f:
    json.dump(out, f, indent=1)
print(f"\nwrote aggregate -> {SCR}/trace_concert_aggregate.json")

if window and tr.writes:
    # Full per-write log of the build window: (order, writer_pc, addr, val)
    with open(os.path.join(SCR, "trace_concert_buildlog.json"), "w") as f:
        json.dump(tr.writes, f)
    print(f"wrote {len(tr.writes)} windowed writes -> {SCR}/trace_concert_buildlog.json")
