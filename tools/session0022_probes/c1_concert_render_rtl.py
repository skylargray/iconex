#!/usr/bin/env python3
"""C1 (plan 021) — CONCERT first-tail render on the RTL-aligned engine (aru_freerun22_rtl).

Discipline unchanged: metric calibration battery asserted in-process, all four channels
through reverb_metrics, WAVs written. Renders BOTH the boot-image WCS (mainloop snapshot)
and the RUN-state capture (LFO mid-phase; its 16 modulated lane-3 ladder coefficients are
the parameter-applied state) — the parameter-state lever is plan C3/D2.
"""
import sys, os, json, time

TOOLS = r"d:\OneDrive\Gray Instruments\iconex\tools"
sys.path.insert(0, TOOLS)
HERE = os.path.dirname(os.path.abspath(__file__))
RENDERS = os.path.join(HERE, "renders")
os.makedirs(RENDERS, exist_ok=True)

import numpy as np
import reverb_metrics as RM
import reverb_metrics_selftest as RMS
from aru_freerun22_rtl import RTL22, program_rows22, fs22

print("### metric calibration battery ###")
ok = RMS.run_battery(out_dir=RENDERS, verbose=False)
assert ok, "metric battery FAILED"
print("  all controls classified correctly — metric TRUSTED\n")


def load_rows(path, key=None):
    rec = json.load(open(path))
    hexs = rec[key]["wcs"] if key else rec["wcs"]
    b = bytes.fromhex(hexs)
    wcs = [(b[4*k], b[4*k+1], b[4*k+2], b[4*k+3]) for k in range(128)]
    return program_rows22(wcs)


def run(rows, signal, n, tag):
    t0 = time.time()
    eng = RTL22()
    chans = eng.run_free(rows, signal, n)
    print(f"  [{tag}] {n} samples in {time.time()-t0:.1f}s "
          f"(peaks: " + " ".join(f"{c}={max(abs(min(v)), abs(max(v)))}"
                                 for c, v in sorted(chans.items())) + ")")
    return chans


def report(tag, chans, exc, fs, burst_end_s=0.0):
    print(f"\n=== {tag} ===")
    verdicts = {}
    for c in "ABCD":
        out = np.asarray(chans[c], dtype=np.int16)
        v = RM.analyze(out, exc, fs, f"c1_rtl_{tag}_ch{c}", out_dir=RENDERS,
                       burst_end_s=burst_end_s)
        keys = ("verdict", "wetness", "late_ratio_db", "rt60", "t20", "t30",
                "ned_max", "mixing_time_s", "density", "reason")
        info = {k: v[k] for k in keys if isinstance(v, dict) and k in v}
        print(f"  ch{c}: {info if info else v}")
        verdicts[c] = v.get("verdict") if isinstance(v, dict) else None
    return verdicts


for img_tag, key, path in (("boot", "1", os.path.join(HERE, "wcs_cache.json")),
                           ("run", None, os.path.join(HERE, "wcs_run_concert.json"))):
    try:
        rows, L, w_reset = load_rows(path, key)
    except Exception as e:
        print(f"[{img_tag}] SKIP: {e}")
        continue
    fs = int(round(fs22(L)))
    print(f"\n##### image={img_tag}: L={L}, {len(rows)}-step frame, fs={fs} Hz #####")

    # S1 impulse, -6 dBFS, 4.0 s
    N1 = int(4.0 * fs)
    exc1 = np.zeros(N1, dtype=np.int16)
    exc1[0] = 16422
    ch1 = run(rows, exc1, N1, f"{img_tag}-imp")
    report(f"{img_tag}-imp-6dBFS", ch1, exc1, fs)

    # S2 noise burst 0.30 s, 4.5 s total
    N2 = int(4.5 * fs)
    rng = np.random.default_rng(224)
    exc2 = np.zeros(N2, dtype=np.int16)
    nb = int(0.30 * fs)
    exc2[:nb] = rng.integers(-8000, 8001, nb).astype(np.int16)
    ch2 = run(rows, exc2, N2, f"{img_tag}-burst")
    report(f"{img_tag}-burst", ch2, exc2, fs, burst_end_s=0.30)

print("\nrenders ->", RENDERS)
