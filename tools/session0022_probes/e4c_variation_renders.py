#!/usr/bin/env python3
"""E4c (plan 023) — render Concert Hall V2/V3/V5 (+V1 reference) from the captured
settled WCS images (e4_variations cache) and score per-band RT60 against ch.4:
  V1 LF 3.0 / Mid 2.0        V2 1.7 / 1.7        V3 3.8 / 2.4        V5 avg 6.5 s
Static settled images (one frozen LFO phase; quote the +-0.2-0.3 s spread). V5 gets a
longer render (12 s) + a T15 fit fallback for the long-decay end.
"""
import sys, os, json

TOOLS = r"d:\OneDrive\Gray Instruments\iconex\tools"
sys.path.insert(0, TOOLS)
HERE = os.path.dirname(os.path.abspath(__file__))
RENDERS = os.path.join(HERE, "renders")

import numpy as np
from scipy.signal import butter, sosfiltfilt
import reverb_metrics as RM
from aru_freerun22_rtl import RTL22, program_rows22, fs22

cache = json.load(open(os.path.join(HERE, "variation_params.json")))

DOC = {"V1": (3.0, 2.0), "V2": (1.7, 1.7), "V3": (3.8, 2.4), "V5": (None, None)}
REN = {"V1": 6.5, "V2": 5.0, "V3": 8.0, "V5": 13.0}


def rt(tail, fs, lo=-5.0, hi=-35.0):
    t = RM._noise_floor_truncate(np.asarray(tail, np.float64), fs)
    edc = RM._schroeder_db(t)
    r, r2, npts = RM._fit_decay(edc, fs, lo, hi)
    if r is None:
        r, r2, npts = RM._fit_decay(edc, fs, lo, -20.0)
    if r is None:
        r, r2, npts = RM._fit_decay(edc, fs, lo, -15.0)
    return r


def render_tag(tag):
    img = bytes.fromhex(cache[tag]["wcs"])
    wcs = [(img[4*k], img[4*k+1], img[4*k+2], img[4*k+3]) for k in range(128)]
    rows, L, w_reset = program_rows22(wcs)
    fs = fs22(L)
    N = int(REN[tag] * fs)
    nb = int(0.30 * fs)
    rng = np.random.default_rng(224)
    exc = np.zeros(N, dtype=np.int64)
    exc[:nb] = rng.integers(-8000, 8001, nb)
    outs = {}
    for name, sig in (("sil", np.zeros(N, dtype=np.int64)), ("bur", exc)):
        eng = RTL22()
        ch = {c: np.zeros(N, dtype=np.int32) for c in "AC"}
        for n in range(N):
            for c, v in eng.run_sample(rows, int(sig[n]) & 0xFFFF):
                if c in ch:
                    ch[c][n] = v
        outs[name] = ch
    res = {}
    for c in "AC":
        d = np.asarray(outs["bur"][c], np.float64) - np.asarray(outs["sil"][c], np.float64)
        tail = d[nb:]
        lf = rt(sosfiltfilt(butter(4, 720/(fs/2), "lowpass", output="sos"), tail), fs)
        mid = rt(sosfiltfilt(butter(4, 720/(fs/2), "highpass", output="sos"), tail), fs)
        bb = rt(tail, fs)
        res[c] = (lf, mid, bb)
        RM.write_wav(RENDERS, f"e4c_{tag}_ch{c}",
                     np.clip(outs["bur"][c], -32768, 32767).astype(np.int16), int(fs))
    return res


print(f"{'var':5}{'ch':3}{'LF(<720)':>10}{'mid(>720)':>11}{'broadband':>11}   documented")
for tag in ("V1", "V2", "V3", "V5"):
    res = render_tag(tag)
    doc = DOC[tag]
    for c in "AC":
        lf, mid, bb = res[c]
        docs = (f"LF {doc[0]} / Mid {doc[1]}" if doc[0] else "avg 6.5 s")
        print(f"{tag:5}{c:3}" +
              "".join(f"{v if v else float('nan'):>11.2f}" for v in (lf, mid, bb)) +
              f"   {docs}", flush=True)
print("\n(static settled images; frozen-LFO phase spread +-0.2-0.3 s applies)")
print("WAVs -> renders/e4c_*")
