#!/usr/bin/env python3
"""E3b (plan 023) — formal D2d range-endpoint verification at CALIBRATED bytes
(display_map, this session): the engine must reproduce what the firmware's own
display formatter says the byte means.

  Mid Decay byte 0x02 -> display 0.6 SEC   (documented range floor 0.6 s)
  Mid Decay byte 0xF8 -> display 70 SEC    (documented range top 70 s; T-early fit)
  Predelay  byte 0x60 -> display 230 MSEC  (beyond the documented 216 max — the
                          formatter tracks it; measure the actual arrival)
Pickup discipline (this session): ascend past the preset to take over, then move to
the target. Capture the settled WCS per state; render offline.
"""
import sys, os, json

TOOLS = r"d:\OneDrive\Gray Instruments\iconex\tools"
sys.path.insert(0, TOOLS)
HERE = os.path.dirname(os.path.abspath(__file__))
RENDERS = os.path.join(HERE, "renders")

import numpy as np
from scipy.signal import butter, sosfiltfilt
import reverb_metrics as RM
import boot8080
from probe_run import run_ticks
from aru_freerun22_rtl import RTL22, program_rows22, fs22

print("booting + settle ...", flush=True)
m, ms = boot8080.boot(verbose=False, extra_ticks_after_mainloop=6_000_000)
assert "mainloop" in ms


def disp(m):
    b = bytes(m.memory[0x3F4F:0x3F68])
    return "".join(chr(c & 0x7F) if 32 <= (c & 0x7F) < 127 else " " for c in b).rstrip()


def set_slider(sl, path):
    for v in path:
        m.memory[0x3C00 + sl] = v
        run_ticks(m, 3_000_000)
    run_ticks(m, 4_000_000)
    return disp(m)


def snap():
    return bytes(m.memory[0x4000:0x4200])


m.memory[0x3C34] = 0
states = {}

# Mid hi: ascend to 0xF8 (pickup crosses the 2.0 preset on the way)
txt = set_slider(1, [0x20, 0x60, 0xA0, 0xF8])
print(f"mid-hi display: {txt!r}")
states["mid_hi"] = snap().hex()

# Mid lo: descend to 0x02 (already picked up)
txt = set_slider(1, [0x80, 0x30, 0x02])
print(f"mid-lo display: {txt!r}")
states["mid_lo"] = snap().hex()

# restore mid to preset-ish (display 2.0 at ~0x58)
set_slider(1, [0x58])

# PDL 0x60 -> display 230 MSEC (pickup: preset 24ms = byte ~0x00, ascend direct)
txt = set_slider(5, [0x10, 0x30, 0x60])
print(f"pdl-230 display: {txt!r}")
states["pdl_230"] = snap().hex()

json.dump(states, open(os.path.join(HERE, "e3b_states.json"), "w"))

# ---------------------------------------------------------------- renders
def rt(tail, fs, lo=-5.0, hi=-35.0):
    t = RM._noise_floor_truncate(np.asarray(tail, np.float64), fs)
    edc = RM._schroeder_db(t)
    for h in (hi, -20.0, -12.0, -9.0):
        r, r2, npts = RM._fit_decay(edc, fs, lo, h)
        if r is not None:
            return r, h
    return None, None


def render(img_hex, seconds, name):
    img = bytes.fromhex(img_hex)
    wcs = [(img[4*k], img[4*k+1], img[4*k+2], img[4*k+3]) for k in range(128)]
    rows, L, w_reset = program_rows22(wcs)
    fs = fs22(L)
    N = int(seconds * fs)
    nb = int(0.30 * fs)
    rng = np.random.default_rng(224)
    exc = np.zeros(N, dtype=np.int64)
    exc[:nb] = rng.integers(-8000, 8001, nb)
    out = {}
    for nm, sig in (("sil", np.zeros(N, dtype=np.int64)), ("bur", exc)):
        eng = RTL22()
        ch = np.zeros(N, dtype=np.int32)
        for n in range(N):
            for c, v in eng.run_sample(rows, int(sig[n]) & 0xFFFF):
                if c == "A":
                    ch[n] = v
        out[nm] = ch
    d = np.asarray(out["bur"], np.float64) - np.asarray(out["sil"], np.float64)
    RM.write_wav(RENDERS, name, np.clip(out["bur"], -32768, 32767).astype(np.int16), int(fs))
    return d, nb, fs


print("\nrender mid-lo (expect mid-band ~0.6 s) ...", flush=True)
d, nb, fs = render(states["mid_lo"], 4.0, "e3b_mid_lo")
tail = d[nb:]
midb = sosfiltfilt(butter(4, 720/(fs/2), "highpass", output="sos"), tail)
r, h = rt(midb, fs)
print(f"  mid(>720) RT60 = {r:.2f} s (fit to {h} dB)   [display 0.6 SEC]")

print("render mid-hi (expect mid-band ~70 s; early-slope fit) ...", flush=True)
d, nb, fs = render(states["mid_hi"], 15.0, "e3b_mid_hi")
tail = d[nb:]
midb = sosfiltfilt(butter(4, 720/(fs/2), "highpass", output="sos"), tail)
r, h = rt(midb, fs, hi=-12.0)
print(f"  mid(>720) RT60 = {r:.1f} s (fit to {h} dB)   [display 70 SEC]")

print("render pdl-230 (expect main arrival ~230 ms) ...", flush=True)
img = bytes.fromhex(states["pdl_230"])
wcs = [(img[4*k], img[4*k+1], img[4*k+2], img[4*k+3]) for k in range(128)]
rows, L, w_reset = program_rows22(wcs)
fs = fs22(L)
N = int(1.2 * fs)
eng = RTL22()
ch = {c: np.zeros(N) for c in "AC"}
sig = np.zeros(N, dtype=np.int64)
sig[0] = 12000
for n in range(N):
    for c, v in eng.run_sample(rows, int(sig[n]) & 0xFFFF):
        if c in ch:
            ch[c][n] = v
for c in "AC":
    x = np.abs(ch[c])
    if x.max() > 0:
        first = np.argmax(x > x.max() * 0.25)
        print(f"  ch{c}: first significant arrival at {first/fs*1000:.1f} ms "
              f"[display 230 MSEC; V1 preset measured 23.99 ms]")
