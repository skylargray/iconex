#!/usr/bin/env python3
"""d2g (session 0025) — LOCALIZATION probe: is the w43/w95 state-injection POLARITY the
LF mechanism? (Diagnostic A/B, NOT adopted semantics — owner rule.)

The firmware's apply law (d2b2 byte anatomy) makes w43/w95 a SIGN-BEARING correction:
recall preset (LF 3.0 > Mid 2.0) -> cmag 5, stored-cs 0; inverted relation (Mid >> LF)
-> cmag 10, cs 1. The engine renders the recall bytes as a negative MAC of the 0x100/0x102
state cells and measures NO LF extension (d2b2: LOW cmag 5->19 leaves LF at ~1.5 s).

A/B: render the settled default vs the same image with ONLY the stored bit7 of lane 2 on
CPU words 43 and 95 flipped (the injection sign), everything else identical. Per-band RT60.
  LF jumps toward ~2.9 s -> the injection polarity is THE LF lever (a sign-path finding on
  this chain to resolve against wiring/ARU tables — not by adoption);
  LF unmoved -> polarity is not the mechanism either; the hunt moves to the operand/group
  routing of the injection chain.
Also renders the flip with LOW at cmag 19 (the LOW-hi capture) — under the boost reading,
MORE cmag must now LENGTHEN LF (the lever comes alive)."""
import sys, os, json

TOOLS = r"d:\OneDrive\Gray Instruments\iconex\tools"
sys.path.insert(0, TOOLS)
HERE = os.path.dirname(os.path.abspath(__file__))

import numpy as np
from scipy.signal import butter, sosfiltfilt
import reverb_metrics as RM
from aru_freerun22_rtl import RTL22, program_rows22, fs22

XOV = 720.0


def flip_sign(img, words):
    b = bytearray(img)
    for w in words:
        b[4 * w + 2] ^= 0x80                     # stored lane-2 bit7 = the CSIGN source
    return bytes(b)


def bands(img, tag):
    wcs = [(img[4*k], img[4*k+1], img[4*k+2], img[4*k+3]) for k in range(128)]
    rows, L, w_reset = program_rows22(wcs)
    fs = fs22(L)
    n = int(6.5 * fs)
    nb = int(0.30 * fs)
    exc = np.zeros(n, dtype=np.int64)
    exc[:nb] = np.random.default_rng(224).integers(-8000, 8001, nb)
    sil = RTL22().run_free(rows, [0] * n, n)
    bur = RTL22().run_free(rows, list(int(v) for v in exc), n)
    out = {}
    for c in "AC":
        d = np.asarray(bur[c], np.float64) - np.asarray(sil[c], np.float64)
        tail = d[nb:]
        vals = []
        for kind, f0 in (("lowpass", XOV), ("highpass", XOV), (None, None)):
            x = tail if kind is None else sosfiltfilt(
                butter(4, f0 / (fs / 2), kind, output="sos"), tail)
            t = RM._noise_floor_truncate(np.asarray(x, np.float64), fs)
            edc = RM._schroeder_db(t)
            rt, r2, npts = RM._fit_decay(edc, fs, -5.0, -35.0)
            if rt is None:
                rt, r2, npts = RM._fit_decay(edc, fs, -5.0, -25.0)
            vals.append(rt)
        out[c] = vals
    print(f"  {tag:28} " + "   ".join(
        f"ch{c}: LF={v[0] if v[0] else float('nan'):5.2f} mid={v[1] if v[1] else float('nan'):5.2f} "
        f"bb={v[2] if v[2] else float('nan'):5.2f}" for c, v in out.items()))
    return out


settled = bytes.fromhex(json.load(open(os.path.join(HERE, "wcs_settled_concert.json")))["wcs"])
low_hi = bytes.fromhex(json.load(open(os.path.join(HERE, "d2b2_lever_wcs.json")))["LOW-hi"])

print("### injection-sign A/B on words 43/95 (benchmark: LF 2.85 / mid 1.92 / bb 1.99) ###")
bands(settled, "settled (cmag5, cs stored)")
bands(flip_sign(settled, (43, 95)), "settled + SIGN FLIP 43/95")
bands(low_hi, "LOW-hi (cmag19, cs stored)")
bands(flip_sign(low_hi, (43, 95)), "LOW-hi + SIGN FLIP 43/95")
