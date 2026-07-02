#!/usr/bin/env python3
"""d2f — measure the REAL 224XL's CONCERT frame rate from the benchmark IR (owner challenge,
session 0024): is fs program-length-dependent (105 steps -> 32,508 Hz, the L+1 model) or
fixed at the quoted 34.125 kHz (= exactly a 100-step frame)?

Method: the model render and the real unit execute the SAME WCS, so every delay is a fixed
number of FRAMES. The benchmark IR (Concert Hall V1.1.L.wav) is a real unit on a 96 kHz
recording timebase. Time-warp the model IR's envelope by a scale s and correlate against the
real IR's envelope: the s that aligns the early-reflection structure measures

    fs_real = 32508 * s        (s = 1.000 -> the L+1 model;  s = 1.050 -> 34,133 Hz)

Two independent estimators:
  1. warped-envelope cross-correlation (shift-tolerant, uses the whole early pattern);
  2. envelope autocorrelation lag ratio (trim-invariant): matching periodicity peaks in
     model vs real; ratio of lags = fs_real/32508.
"""
import sys, os, json

TOOLS = r"d:\OneDrive\Gray Instruments\iconex\tools"
sys.path.insert(0, TOOLS)
HERE = os.path.dirname(os.path.abspath(__file__))

import numpy as np
import soundfile as sf
from scipy.signal import butter, sosfiltfilt
from aru_freerun22_rtl import RTL22, program_rows22, fs22

MODEL_FS = None   # set from L below

# ---------------------------------------------------------------- model IR (floor-subtracted)
rec = json.load(open(os.path.join(HERE, "wcs_settled_concert.json")))
b = bytes.fromhex(rec["wcs"])
rows, L, w_reset = program_rows22([(b[4*k], b[4*k+1], b[4*k+2], b[4*k+3]) for k in range(128)])
MODEL_FS = fs22(L)
N = int(3.5 * MODEL_FS)
imp_in = [0] * N
imp_in[0] = 16000
sil = RTL22().run_free(rows, [0] * N, N)
imp = RTL22().run_free(rows, imp_in, N)
model = np.asarray(imp["A"], np.float64) - np.asarray(sil["A"], np.float64)
print(f"model IR: settled CONCERT, chA (left), {N} frames @ {MODEL_FS:.1f} Hz")

# ---------------------------------------------------------------- real IR
ir_path = os.path.join(os.path.dirname(TOOLS), "IR", "Lexicon 224XL", "Concert Hall V1.1.L.wav")
real, real_fs = sf.read(ir_path)
if real.ndim > 1:
    real = real[:, 0]
print(f"real IR: {os.path.basename(ir_path)} @ {real_fs} Hz, {len(real)/real_fs:.2f} s")

# ---------------------------------------------------------------- envelopes on an 8 kHz grid
GRID = 8000.0

def envelope(x, fs):
    e = np.abs(x.astype(np.float64))
    sos = butter(4, 300.0 / (fs / 2), "lowpass", output="sos")
    e = sosfiltfilt(sos, e)
    t_out = np.arange(0, len(x) / fs, 1.0 / GRID)
    return np.interp(t_out, np.arange(len(x)) / fs, e)

env_m = envelope(model, MODEL_FS)
env_r = envelope(real, real_fs)

# analysis window: early structure (skip the very first ms of recording-chain junk)
W0, W1 = int(0.004 * GRID), int(0.700 * GRID)
r_seg = env_r[W0:W1]
r_seg = (r_seg - r_seg.mean()) / (r_seg.std() + 1e-12)

def corr_at(s):
    """max normalized correlation of model-env warped by s against the real early window,
    over shifts +-25 ms."""
    t = (np.arange(W0, W1) / GRID) * s
    m = np.interp(t, np.arange(len(env_m)) / GRID, env_m)
    best = -2.0
    for sh in range(-int(0.025 * GRID), int(0.025 * GRID) + 1):
        a, bb = (W0 + sh, W1 + sh)
        if a < 0 or bb > len(env_r):
            continue
        rr = env_r[a:bb]
        rr = (rr - rr.mean()) / (rr.std() + 1e-12)
        mm = (m - m.mean()) / (m.std() + 1e-12)
        c = float(np.mean(rr * mm))
        if c > best:
            best = c
    return best

print("\n### estimator 1: warped-envelope correlation (0.004-0.700 s window) ###")
print(f"{'s':>7} {'fs_real':>9} {'corr':>7}")
scan = np.arange(0.94, 1.0801, 0.005)
cs = [corr_at(s) for s in scan]
for s, c in zip(scan, cs):
    mark = " <-- 32,508 (L+1 model)" if abs(s - 1.0) < 1e-9 else (
           " <-- 34,133 (100-step / 34.125k)" if abs(s - 1.05) < 0.0026 else "")
    print(f"{s:>7.3f} {32508 * s:>9.0f} {c:>7.3f}{mark}")
s0 = scan[int(np.argmax(cs))]
fine = np.arange(max(0.94, s0 - 0.01), min(1.08, s0 + 0.01) + 1e-9, 0.001)
cf = [corr_at(s) for s in fine]
s_best = fine[int(np.argmax(cf))]
print(f"fine scan around peak: s = {s_best:.3f} -> fs_real = {32508 * s_best:.0f} Hz "
      f"(corr {max(cf):.3f})")

# ---------------------------------------------------------------- estimator 2: autocorr lags
print("\n### estimator 2: envelope-autocorrelation periodicities ###")

def top_lags(env, lo_ms=120, hi_ms=230, k=5):
    seg = env[:int(1.2 * GRID)]
    seg = seg - seg.mean()
    ac = np.correlate(seg, seg, "full")[len(seg) - 1:]
    ac /= ac[0] + 1e-12
    lo, hi = int(lo_ms / 1000 * GRID), int(hi_ms / 1000 * GRID)
    win = ac[lo:hi]
    idx = np.argsort(win)[::-1]
    out, used = [], []
    for i in idx:
        if all(abs(i - u) > int(0.004 * GRID) for u in used):
            used.append(i)
            out.append(((lo + i) / GRID * 1000, float(win[i])))
        if len(out) >= k:
            break
    return out

lm = top_lags(env_m)
lr = top_lags(env_r)
print("model autocorr peaks (ms, corr):", [(f"{t:.1f}", f"{c:.2f}") for t, c in lm])
print("real  autocorr peaks (ms, corr):", [(f"{t:.1f}", f"{c:.2f}") for t, c in lr])
print(f"(the CONCERT recirc tap = 6008 frames = {6008 / MODEL_FS * 1000:.1f} ms @32508 "
      f"vs {6008 / 34133.3 * 1000:.1f} ms @34133)")
if lm and lr:
    ratio = lm[0][0] / lr[0][0]
    print(f"dominant-lag ratio model/real = {ratio:.4f} -> fs_real = {32508 * ratio:.0f} Hz")

print("\nverdict: fs_real per estimator 1 = %.0f Hz (s=%.3f); the L+1 model predicts 32508, "
      "the fixed-34.125k hypothesis predicts 34133." % (32508 * s_best, s_best))
