#!/usr/bin/env python3
"""C3 — the floor-subtracted impulse response. The RTL machine has a deterministic Booth
residue floor (each (0,0) serializer phase contributes ±1 to the ACC; the factory program's
sign mix leaves a small perpetual limit cycle ~2-5 LSB RMS). The C1 metrics saw that floor
(verdict TONAL) — the machine's LINEAR response rides underneath.

The engine is linear modulo rounding, so: render silence (pure floor) and impulse (floor +
response) from the same initial state, subtract, and measure the difference tail:
block RMS + crude RT60 of (y_impulse - y_silence) per channel, boot AND run images.
"""
import sys, os, json, math
TOOLS = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, TOOLS)
import numpy as np
from aru_freerun22_rtl import RTL22, program_rows22, fs22

HERE = os.path.dirname(os.path.abspath(__file__))
RENDERS = os.path.join(HERE, "renders")
os.makedirs(RENDERS, exist_ok=True)


def load_rows(path, key=None):
    rec = json.load(open(path))
    hexs = rec[key]["wcs"] if key else rec["wcs"]
    b = bytes.fromhex(hexs)
    wcs = [(b[4*k], b[4*k+1], b[4*k+2], b[4*k+3]) for k in range(128)]
    return program_rows22(wcs)


def render(rows, n, impulse):
    eng = RTL22()
    sig = (lambda i: 16422 if (impulse and i == 0) else 0)
    return eng.run_free(rows, sig, n)


for img_tag, key, path in (("boot", "1", os.path.join(HERE, "wcs_cache.json")),
                           ("run", None, os.path.join(HERE, "wcs_run_concert.json"))):
    rows, L, w_reset = load_rows(path, key)
    fs = fs22(L)
    n = int(4.0 * fs)
    sil = render(rows, n, False)
    imp = render(rows, n, True)
    print(f"\n##### {img_tag}: floor-subtracted IR (4.0 s, fs={fs:.0f}) #####")
    blk = int(0.125 * fs)
    for c in "AC":
        d = np.asarray(imp[c], dtype=np.float64) - np.asarray(sil[c], dtype=np.float64)
        nb = len(d) // blk
        rms = [float(np.sqrt(np.mean(d[i*blk:(i+1)*blk] ** 2))) for i in range(nb)]
        peak = float(np.max(np.abs(d)))
        print(f"  ch{c}: diff peak={peak:.0f}")
        print("    blk(125ms) RMS: " + " ".join(f"{r:7.2f}" for r in rms))
        # crude RT60 fit over blocks 1..k where RMS > 0.05
        db = [20 * math.log10(max(r, 1e-6)) for r in rms]
        pts = [(i * 0.125 + 0.0625, v) for i, v in enumerate(db) if i >= 1 and rms[i] > 0.05]
        if len(pts) >= 3:
            xs = np.array([p[0] for p in pts]); ys = np.array([p[1] for p in pts])
            A = np.vstack([xs, np.ones_like(xs)]).T
            slope, _ = np.linalg.lstsq(A, ys, rcond=None)[0]
            if slope < -0.5:
                print(f"    decay slope {slope:+.1f} dB/s  =>  RT60 ~ {60/-slope:.2f} s "
                      f"(over {len(pts)} blocks)")
            else:
                print(f"    decay slope {slope:+.1f} dB/s (flat/rising — no classical tail)")
        # save the difference as a wav for listening
        w = np.clip(d * 64.0, -32767, 32767).astype(np.int16)   # +36 dB gain to hear it
        import reverb_metrics as RM
        RM.write_wav(RENDERS, f"c3_{img_tag}_diff_ch{c}_x64", w, int(round(fs)))
print("\nwavs ->", RENDERS)
