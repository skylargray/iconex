#!/usr/bin/env python3
"""D0 — cross-program oracle sweep: all 13 buildable factory programs through the RTL engine
and the metric harness (burst stimulus). If the traced alignment is right, EVERY factory
program should render as a coherent reverb (wet, dense-ish, decaying, program-specific RT60)
— 12 independent structural checks beyond CONCERT.
"""
import sys, os, json, math
TOOLS = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, TOOLS)
import numpy as np
import reverb_metrics as RM
import reverb_metrics_selftest as RMS
from aru_freerun22_rtl import RTL22, program_rows22, fs22

HERE = os.path.dirname(os.path.abspath(__file__))
RENDERS = os.path.join(HERE, "renders")
os.makedirs(RENDERS, exist_ok=True)

ok = RMS.run_battery(out_dir=RENDERS, verbose=False)
assert ok, "metric battery FAILED"
print("metric battery OK\n")

cache = json.load(open(os.path.join(HERE, "wcs_cache.json")))
rng = np.random.default_rng(224)

print(f"{'id':>3} {'L':>4} {'fs':>6} | {'verdict A':>10} {'wet':>5} {'RT60':>5} | peakA")
for pid in sorted(cache, key=int):
    rec = cache[pid]
    b = bytes.fromhex(rec["wcs"])
    if len(b) < 512:
        continue
    wcs = [(b[4*k], b[4*k+1], b[4*k+2], b[4*k+3]) for k in range(128)]
    try:
        rows, L, w_reset = program_rows22(wcs)
    except ValueError:
        continue
    fs = fs22(L)
    n = int(3.5 * fs)
    nb = int(0.30 * fs)
    exc = np.zeros(n, dtype=np.int16)
    exc[:nb] = rng.integers(-8000, 8001, nb).astype(np.int16)
    engB = RTL22()
    chans = engB.run_free(rows, exc, n)
    engS = RTL22()
    sil = engS.run_free(rows, np.zeros(n, dtype=np.int16), n)
    out = np.asarray(chans["A"], dtype=np.int16)
    v = RM.analyze(out, exc, int(round(fs)), f"d0_id{pid}_chA", out_dir=RENDERS, burst_end_s=0.30)
    verdict = v.get("verdict") if isinstance(v, dict) else "?"
    wet = v.get("wetness") if isinstance(v, dict) else None
    # floor-subtracted RT60 (same method as c5)
    d = np.asarray(chans["A"], dtype=np.float64) - np.asarray(sil["A"], dtype=np.float64)
    tail = d[nb:]
    blk = int(0.050 * fs)
    m = len(tail) // blk
    rms = np.array([np.sqrt(np.mean(tail[i*blk:(i+1)*blk] ** 2)) for i in range(m)])
    db = 20 * np.log10(np.maximum(rms, 1e-9))
    pk = db[:4].max()
    pts = [(i * 0.05, val) for i, val in enumerate(db) if pk - 40 <= val <= pk - 5]
    rt60 = None
    if len(pts) >= 4:
        xs = np.array([p[0] for p in pts]); ys = np.array([p[1] for p in pts])
        A = np.vstack([xs, np.ones_like(xs)]).T
        slope, _ = np.linalg.lstsq(A, ys, rcond=None)[0]
        if slope < -1:
            rt60 = 60.0 / -slope
    print(f"{pid:>3} {L:>4} {fs:6.0f} | {str(verdict):>10} {wet if wet is None else round(wet,2):>5} "
          f"{'--' if rt60 is None else f'{rt60:4.2f}':>5} | {int(np.abs(out).max())}")
print("\nrenders ->", RENDERS)
