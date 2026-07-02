#!/usr/bin/env python3
"""D4-lite (plan 022 D2b diagnosis) — replay the firmware's own LFO WCS-write trajectory
into the RTL engine, per-frame, and measure what modulation does to the per-band RT60.

D2b found: settled static image LF(<720) ~ 1.4 s vs documented 3.0 / benchmark 2.85 s
(mid within tolerance). Method validated on the benchmark IR, capture point pinned by D2a
— remaining suspects: (a) engine semantics vs (b) the STATIC-image approximation (the
always-on tank modulation is parked at one frozen LFO phase; the real unit sweeps pairs
(56,57)/(107,108) continuously, sum-preserving coeffs).

This probe discriminates: boot the verified core, snapshot the WCS every 50k ticks
(~12k instructions ~ 1/28 LFO period; triangle period ~345k instructions per
224XL_modulation_lfo.md) over the full render span, then render with the engine
hot-swapping the 4 modulated words per frame (frame n <-> tick n*62 — the 0022-measured
62-CPU-ticks-per-frame budget). Burst + silence replays share the schedule, so the
floor subtraction stays valid. Same Schroeder T30 band method as d2_param_rt60.

  LF jumps toward ~2.9 s  -> the static approximation was the gap: D4 co-sim = the fix.
  LF unchanged            -> engine-semantics finding: STOP and investigate the datapath.
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
from aru_freerun22_rtl import RTL22, program_rows22, fs22, decode_word

TICKS_PER_FRAME = 62.0
REN_S = 6.5
BURST_S = 0.30
MOVER_WORDS = (56, 57, 107, 108)
CACHE = os.path.join(HERE, "d4lite_snapshots.json")

# ---------------------------------------------------------------- capture the trajectory
if os.path.exists(CACHE):
    snaps = [(t, bytes.fromhex(h)) for t, h in json.load(open(CACHE))]
    print(f"[cache] {len(snaps)} snapshots")
else:
    need_ticks = int(REN_S * 32508 * TICKS_PER_FRAME * 1.15)
    snaps = []
    print(f"booting + capturing WCS every 50k ticks for {need_ticks/1e6:.0f}M ticks ...")
    m, ms = boot8080.boot(verbose=False, extra_ticks_after_mainloop=need_ticks,
                          snapshot_cb=lambda img, tick: snaps.append((tick, img)),
                          snapshot_every=50_000)
    assert "mainloop" in ms
    t0 = snaps[0][0]
    snaps = [(t - t0, img) for t, img in snaps]
    json.dump([(t, img.hex()) for t, img in snaps], open(CACHE, "w"))
    print(f"  {len(snaps)} snapshots cached")

# LFO sanity: how do the mover bytes actually move across snapshots?
mv_bytes = sorted(b for w in MOVER_WORDS for b in (4 * w, 4 * w + 3))
tr = [[img[b] for _, img in snaps[:200]] for b in mv_bytes]
print("mover-byte trajectories (first 24 snapshots):")
for b, t in zip(mv_bytes, tr):
    print(f"  0x{0x4000+b:04X} (w{b//4} l{b%4}): {t[:24]}")

# ---------------------------------------------------------------- rows + per-snapshot movers
base = snaps[-1][1]
wcs = [(base[4*k], base[4*k+1], base[4*k+2], base[4*k+3]) for k in range(128)]
rows, L, w_reset = program_rows22(wcs)
fs = fs22(L)
N = int(REN_S * fs)
row_of = {w: 127 - w for w in MOVER_WORDS}
pre = []                                     # per snapshot: {row: decoded word}
for _, img in snaps:
    pre.append({row_of[w]: decode_word((img[4*w], img[4*w+1], img[4*w+2], img[4*w+3]))
                for w in MOVER_WORDS})
snap_ticks = np.array([t for t, _ in snaps])


def render(sig):
    eng = RTL22()
    chans = {c: [0] * N for c in "ABCD"}
    si = 0
    for n in range(N):
        t = n * TICKS_PER_FRAME
        while si + 1 < len(snap_ticks) and snap_ticks[si + 1] <= t:
            si += 1
        for r, d in pre[si].items():
            rows[r] = d
        for c, v in eng.run_sample(rows, int(sig[n]) & 0xFFFF):
            chans[c][n] = v
    return chans


rng = np.random.default_rng(224)
exc = np.zeros(N, dtype=np.int64)
nb = int(BURST_S * fs)
exc[:nb] = rng.integers(-8000, 8001, nb)
print(f"\nrendering with live modulation replay (L={L}, fs={fs:.0f}, {N} frames) ...")
sil = render(np.zeros(N, dtype=np.int64))
bur = render(exc)

# ---------------------------------------------------------------- measure (d2 method)
DOCXOV = 720.0

def band(x, kind, f0):
    ny = fs / 2
    sos = butter(4, f0 / ny, kind, output="sos")
    return sosfiltfilt(sos, x)

def rt60(tail):
    t = RM._noise_floor_truncate(np.asarray(tail, np.float64), fs)
    edc = RM._schroeder_db(t)
    rt, r2, npts = RM._fit_decay(edc, fs, -5.0, -35.0)
    if rt is None:
        rt, r2, npts = RM._fit_decay(edc, fs, -5.0, -25.0)
    return rt

print("\n### modulation-replay render, per-band RT60 (Schroeder T30) ###")
print(f"{'':8}{'LF(<720)':>10}{'mid(>720)':>11}{'broadband':>11}   "
      f"[static settled was: LF ~1.4 / mid ~1.64 / bb ~1.64; benchmark 2.85/1.92/1.99]")
for c in "AC":
    d = np.asarray(bur[c], np.float64) - np.asarray(sil[c], np.float64)
    tail = d[nb:]
    vals = (rt60(band(tail, "lowpass", DOCXOV)), rt60(band(tail, "highpass", DOCXOV)),
            rt60(tail))
    RM.write_wav(RENDERS, f"d4lite_mod_ch{c}", np.clip(bur[c], -32768, 32767).astype(np.int16), int(fs))
    print(f"ch{c:6}" + "".join(f"{v if v else float('nan'):>11.2f}" for v in vals))
print("\nWAVs -> renders/d4lite_mod_ch*.wav")
