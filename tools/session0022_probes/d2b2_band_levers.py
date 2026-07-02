#!/usr/bin/env python3
"""D2b diagnosis — are the band-shaping levers CONNECTED through the engine?

D2b (fixed engine): mid(>720) matches the benchmark within 4%, but LF shows no extension
(1.5 vs 2.85 s) and 8 kHz runs long (1.86 vs 1.51 s). The suspect words are the small-cmag
corrective MACs (LOW 43/95, HFD 40/41/92/93). This probe drives each slider to its extremes
on the live firmware (injection at 0x3C00+idx, de-zipper settle), captures the settled WCS,
renders, and measures the TARGET band:

  LOW  (0x3C00): LF(<720)-band RT60 must move (documented range 0.6..70 s)
  HFD  (0x3C03): 8 kHz-octave RT60 must move (treble decay 1.5k..22.5k)
  MID  (0x3C01): mid(>720) must move (0.6..70 s) — positive control (mid already matches)

'lever moves the band' -> the apply chain + decode + engine express the parameter (a
D2b-FAIL then points at the DEFAULT state or arithmetic detail of that band's filter);
'lever is inert' -> the engine drops that word's contribution — a topology/decode finding.
"""
import sys, os, json

TOOLS = r"d:\OneDrive\Gray Instruments\iconex\tools"
sys.path.insert(0, TOOLS)
HERE = os.path.dirname(os.path.abspath(__file__))
CACHE = os.path.join(HERE, "d2b2_lever_wcs.json")

import numpy as np
from scipy.signal import butter, sosfiltfilt
import reverb_metrics as RM
from aru_freerun22_rtl import RTL22, program_rows22, fs22

MOVERS = {4 * w + l for w in (56, 57, 107, 108) for l in range(4)}


def capture_lever_images():
    import boot8080
    from probe_run import run_ticks
    print("booting CONCERT to mainloop + settle ...", flush=True)
    m, ms = boot8080.boot(verbose=False, extra_ticks_after_mainloop=6_000_000)
    assert "mainloop" in ms

    def run(n):
        run_ticks(m, n)                 # boot()-equivalent: serves the serial RST-7

    out = {"base": bytes(m.memory[0x4000:0x4200]).hex(),
           "sliders": list(bytes(m.memory[0x3C00:0x3C06]))}
    for idx, label in ((0, "LOW"), (1, "MID"), (3, "HFD")):
        orig = m.memory[0x3C00 + idx]
        for tag, v in (("lo", 0x02), ("hi", 0xF0)):
            m.memory[0x3C00 + idx] = v
            run(5_000_000)
            out[f"{label}-{tag}"] = bytes(m.memory[0x4000:0x4200]).hex()
            print(f"  captured {label}-{tag} (slider 0x{v:02X})")
        m.memory[0x3C00 + idx] = orig
        run(5_000_000)
    json.dump(out, open(CACHE, "w"))
    return out


imgs = json.load(open(CACHE)) if os.path.exists(CACHE) else capture_lever_images()
base = bytes.fromhex(imgs["base"])
print(f"power-up sliders: {[hex(v) for v in imgs['sliders']]}")


def rows_of(hexs):
    b = bytes.fromhex(hexs)
    return program_rows22([(b[4*k], b[4*k+1], b[4*k+2], b[4*k+3]) for k in range(128)])


def band_rt60(tail, fs, kind, f0, f1=None):
    ny = fs / 2
    if kind == "low":
        sos = butter(4, f0 / ny, "lowpass", output="sos")
    elif kind == "high":
        sos = butter(4, f0 / ny, "highpass", output="sos")
    else:
        sos = butter(4, [f0 / ny, min(f1 / ny, 0.98)], "bandpass", output="sos")
    x = sosfiltfilt(sos, tail)
    t = RM._noise_floor_truncate(np.asarray(x, np.float64), fs)
    edc = RM._schroeder_db(t)
    rt, r2, npts = RM._fit_decay(edc, fs, -5.0, -35.0)
    if rt is None:
        rt, r2, npts = RM._fit_decay(edc, fs, -5.0, -25.0)
    if rt is None:
        rt, r2, npts = RM._fit_decay(edc, fs, -3.0, -15.0)   # very long decays: T12 estimate
    return rt


BANDS = {"LOW": ("low", 720.0, None), "MID": ("high", 720.0, None),
         "HFD": ("band", 8000 / 2**0.5, 8000 * 2**0.5)}

for label in ("LOW", "MID", "HFD"):
    kind, f0, f1 = BANDS[label]
    print(f"\n### {label} lever ###")
    for tag in ("lo", "hi"):
        img = bytes.fromhex(imgs[f"{label}-{tag}"])
        dw = sorted({a // 4 for a in range(0x200) if img[a] != base[a] and a not in MOVERS})
        rows, L, w_reset = rows_of(imgs[f"{label}-{tag}"])
        fs = fs22(L)
        n = int((7.5 if tag == "hi" and label in ("LOW", "MID") else 5.0) * fs)
        nb = int(0.30 * fs)
        exc = np.zeros(n, dtype=np.int64)
        exc[:nb] = np.random.default_rng(224).integers(-8000, 8001, nb)
        sil = RTL22().run_free(rows, [0] * n, n)
        bur = RTL22().run_free(rows, list(int(v) for v in exc), n)
        d = np.asarray(bur["A"], np.float64) - np.asarray(sil["A"], np.float64)
        rt = band_rt60(d[nb:], fs, kind, f0, f1)
        print(f"  {tag} (words moved vs base: {dw}): target-band RT60 = "
          f"{rt if rt else float('nan'):.2f} s")
