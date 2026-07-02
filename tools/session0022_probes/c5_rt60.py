#!/usr/bin/env python3
"""C5 — RT60 of the first tail, floor-subtracted (the Booth-residue limit cycle is additive
and deterministic; subtract the silence render), Schroeder-free block-RMS slope fit on the
post-burst decay, per channel, boot + run images. Reference: benchmark IR RT60 ~ 2.5 s."""
import sys, os, json, math
TOOLS = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, TOOLS)
import numpy as np
from aru_freerun22_rtl import RTL22, program_rows22, fs22

HERE = os.path.dirname(os.path.abspath(__file__))

def load_rows(path, key=None):
    rec = json.load(open(path))
    b = bytes.fromhex((rec[key] if key else rec)["wcs"])
    wcs = [(b[4*k], b[4*k+1], b[4*k+2], b[4*k+3]) for k in range(128)]
    return program_rows22(wcs)

rng = np.random.default_rng(224)

for img_tag, key, path in (("boot", "1", os.path.join(HERE, "wcs_cache.json")),
                           ("run", None, os.path.join(HERE, "wcs_run_concert.json"))):
    rows, L, w_reset = load_rows(path, key)
    fs = fs22(L)
    n = int(4.5 * fs)
    nb = int(0.30 * fs)
    exc = np.zeros(n, dtype=np.int64)
    exc[:nb] = rng.integers(-8000, 8001, nb)
    def run(sig):
        eng = RTL22()
        return eng.run_free(rows, list(sig), n)
    ch_b = run(exc)
    ch_s = run(np.zeros(n, dtype=np.int64))
    print(f"\n##### {img_tag} (fs={fs:.0f}) — burst 0.30 s, floor-subtracted tail #####")
    for c in "ABCD":
        d = np.asarray(ch_b[c], dtype=np.float64) - np.asarray(ch_s[c], dtype=np.float64)
        tail = d[nb:]
        blk = int(0.050 * fs)
        m = len(tail) // blk
        rms = np.array([np.sqrt(np.mean(tail[i*blk:(i+1)*blk] ** 2)) for i in range(m)])
        db = 20 * np.log10(np.maximum(rms, 1e-9))
        peak_db = db[:4].max()
        # fit the clean decay: from peak-5 dB down to peak-40 dB (above the residual noise)
        lo, hi = peak_db - 5.0, peak_db - 40.0
        pts = [(i * 0.05 + 0.025, v) for i, v in enumerate(db) if hi <= v <= lo]
        if len(pts) >= 4:
            xs = np.array([p[0] for p in pts]); ys = np.array([p[1] for p in pts])
            A = np.vstack([xs, np.ones_like(xs)]).T
            slope, icpt = np.linalg.lstsq(A, ys, rcond=None)[0]
            rt60 = 60.0 / -slope if slope < 0 else float("inf")
            print(f"  ch{c}: peak(after burst)={rms.max():8.1f}  slope={slope:+7.1f} dB/s  "
                  f"RT60={rt60:5.2f} s  (fit {len(pts)} x 50ms blocks, {lo:.0f}..{hi:.0f} dBr)")
        else:
            print(f"  ch{c}: insufficient decay range (peak {peak_db:.1f} dB)")
