#!/usr/bin/env python3
"""E3 first light — CONCERT (static WCS) on the session-0022 corrected engine.

Runs the S1 impulse (-6 dBFS) and an S2-style seeded noise burst through FreeRun22 and
measures every D/A channel with the trusted reverb_metrics harness (calibration battery
asserted in-process first). WAVs land in ./renders (timestamped by the harness)."""
import sys, os, json, time

TOOLS = r"d:\OneDrive\Gray Instruments\iconex\tools"
sys.path.insert(0, TOOLS)
SCRATCH = os.path.dirname(os.path.abspath(__file__))
RENDERS = os.path.join(SCRATCH, "renders")
os.makedirs(RENDERS, exist_ok=True)

import numpy as np
import reverb_metrics as RM
import reverb_metrics_selftest as RMS
from aru_freerun22 import FreeRun22, program_from_wcs, fs_for

# --- 0. trust the metric ---------------------------------------------------
print("### metric calibration battery ###")
ok = RMS.run_battery(out_dir=RENDERS, verbose=False)
assert ok, "metric battery FAILED"
print("  all controls classified correctly — metric TRUSTED\n")

# --- 1. load CONCERT -------------------------------------------------------
cache = json.load(open(os.path.join(SCRATCH, "wcs_cache.json")))
b = bytes.fromhex(cache["1"]["wcs"])
wcs = [(b[4*k], b[4*k+1], b[4*k+2], b[4*k+3]) for k in range(128)]
prog, L, w_reset = program_from_wcs(wcs)
fs = int(round(fs_for(L)))
print(f"CONCERT: L={L} steps, reset word {w_reset}, fs={fs} Hz\n")

def run(signal, n, tag):
    t0 = time.time()
    eng = FreeRun22()
    chans = eng.run_free(prog, signal, n)
    print(f"  [{tag}] {n} samples in {time.time()-t0:.1f}s "
          f"(peaks: " + " ".join(f"{c}={max(abs(min(v)), abs(max(v)))}" for c, v in sorted(chans.items())) + ")")
    return chans

def report(tag, chans, exc, burst_end_s=0.0):
    print(f"\n=== {tag} ===")
    for c in "ABCD":
        out = np.asarray(chans[c], dtype=np.int16)
        v = RM.analyze(out, exc, fs, f"e3_concert22_{tag}_ch{c}", out_dir=RENDERS,
                       burst_end_s=burst_end_s)
        keys = ("verdict", "wetness", "late_ratio_db", "rt60", "t20", "t30",
                "ned_max", "mixing_time_s", "density", "reason")
        info = {k: v[k] for k in keys if isinstance(v, dict) and k in v}
        print(f"  ch{c}: {info if info else v}")

# --- 2. S1 impulse, -6 dBFS, 4.0 s ----------------------------------------
N1 = int(4.0 * fs)
exc1 = np.zeros(N1, dtype=np.int16)
exc1[0] = 16422                                   # -6 dBFS
ch1 = run(exc1, N1, "imp-6dBFS")
report("imp-6dBFS", ch1, exc1)

# --- 3. S2 noise burst: +-8000 for 0.30 s, then silence; 4.5 s total ------
N2 = int(4.5 * fs)
rng = np.random.default_rng(224)
exc2 = np.zeros(N2, dtype=np.int16)
nb = int(0.30 * fs)
exc2[:nb] = rng.integers(-8000, 8001, nb).astype(np.int16)
ch2 = run(exc2, N2, "burst")
report("burst", ch2, exc2, burst_end_s=0.30)

print("\nrenders ->", RENDERS)
