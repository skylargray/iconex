#!/usr/bin/env python3
"""E3d — tank-vs-output fork under csinv=1 (the stable sign).

Impulse -6 dBFS, 3 s. Every 0.05 s: DMEM RMS (the tank), end-of-frame |RES|, and the
per-channel output RMS. Decides: tank holds energy but outputs miss it (capture problem)
vs tank drains fast (loop gain/sign still wrong)."""
import sys, os, json
TOOLS = r"d:\OneDrive\Gray Instruments\iconex\tools"
sys.path.insert(0, TOOLS)
SCRATCH = os.path.dirname(os.path.abspath(__file__))

import numpy as np
from aru_freerun22 import FreeRun22, program_from_wcs, fs_for

cache = json.load(open(os.path.join(SCRATCH, "wcs_cache.json")))
b = bytes.fromhex(cache["1"]["wcs"])
wcs = [(b[4*k], b[4*k+1], b[4*k+2], b[4*k+3]) for k in range(128)]
prog, L, w_reset = program_from_wcs(wcs)
fs = int(round(fs_for(L)))
N = int(3.0 * fs)
K = int(0.05 * fs)

eng = FreeRun22(csign_invert=True)
outs = {c: [] for c in "ABCD"}
print(f"{'t(s)':>5} {'DM_rms':>9} {'DM_n':>7} {'|RES|':>6} | out RMS A/B/C/D (last 50ms)")
for n in range(N):
    x = 16422 if n == 0 else 0
    da = dict(eng.run_sample(prog, x & 0xFFFF))
    for c in "ABCD":
        outs[c].append(da.get(c, 0))
    if n % K == 0 or n == N - 1:
        vals = np.fromiter((v - 0x10000 if v & 0x8000 else v for v in eng.DM.values()),
                           dtype=np.float64, count=len(eng.DM))
        dmr = float(np.sqrt(np.mean(vals**2))) if len(vals) else 0.0
        orms = [float(np.sqrt(np.mean(np.asarray(outs[c][-K:], dtype=np.float64)**2)))
                for c in "ABCD"]
        print(f"{n/fs:5.2f} {dmr:9.1f} {len(eng.DM):7d} {abs(eng.RES):6d} | "
              + " ".join(f"{r:8.1f}" for r in orms), flush=True)
