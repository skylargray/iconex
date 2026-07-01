#!/usr/bin/env python3
"""224XL plan-020 Phase 0.5 — cheap discriminating experiments (localize the cause of the missing
dense tail BEFORE the expensive Phase-1..3 timing rebuild).

The three real unknowns — what `cmag=0` does, whether modulation is required for density, and
loop-gain/scaling — are NOT "timing fidelity" and can be probed in minutes on the EXISTING behavioral
free-run engine (`aru_freerun.FreeRunARU`), measured by the now-proven `reverb_metrics` harness via
the Phase-0.3 scaffold (`aru_whole`). This script runs:

  BASELINE  — static CONCERT WCS, measured (expected SPARSE / single echo per prior findings).
  0.5.1 COEFFICIENT probe — force cmag>0 into the steps 5–22 `cmag=0` block (and the recirc taps);
        does density appear? → is the static zero-coefficient block the blocker?
  0.5.2 MODULATION probe — apply a per-frame LFO to the modulated taps' delay offsets (no timing
        change to the engine); does density appear? → is modulation the lever, independent of timing?
  0.5.3 LOOP-GAIN probe — sweep an overall gain on the recirculating feedback taps; find the
        decay↔over-unity boundary → is it gain/scaling (FPC) vs topology?

Every audio number is a reverb_metrics three-state verdict on the EMITTED WR DA/ output (P1), with a
timestamped WAV (P2), and the control battery is asserted in-process first (P5). Stimulus is ONLY the
tools/stimulus.py S1/S2 battery. No buf_RMS, no internal energy, no improvised input.

Run:  python tools/phase05_probes.py
"""
import os
import sys
import time

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np

import aru_whole as W
import aru_freerun as FR
import stimulus as ST

FS = W.FS


# ---------------------------------------------------------------------------
# WCS field editors (preserve every field except the one being probed)
# ---------------------------------------------------------------------------
def get_cmag(step):
    return (((~step[3]) & 0xFF) >> 2) & 0x3F


def with_cmag(step, cmag):
    """Return step with a new cmag, preserving XFER/ZERO (lane-3 active-low)."""
    l0, l1, l2, l3 = step
    inv3 = (~l3) & 0xFF
    xfer, zero = inv3 & 1, (inv3 >> 1) & 1
    inv3n = xfer | (zero << 1) | ((cmag & 0x3F) << 2)
    return (l0, l1, l2, (~inv3n) & 0xFF)


def scale_cmag(step, factor):
    c = get_cmag(step)
    return with_cmag(step, max(0, min(63, int(round(c * factor)))))


def with_offset_delta(step, delta):
    """Shift a step's stored DMEM offset by `delta` samples (addr = CPC + ofst + 1 → addr shifts +delta)."""
    l0, l1, l2, l3 = step
    ofst = ((l1 << 8) | l0)
    ofst = (ofst + delta) & 0xFFFF
    return (ofst & 0xFF, (ofst >> 8) & 0xFF, l2, l3)


def dev_class(step):
    d = FR.decode(step[2], step[3])
    if d["MEMAC"] == 1 and d["MI16"] == 0:
        return "MEMW"
    if d["MEMAC"] == 1 and d["MI16"] == 1:
        return "MEMR"
    if d["MEMAC"] == 0 and d["MI16"] == 1:
        return "IO"
    return "idle"


# Dataflow roles (from tools/decode_concert_program.py, gate+dataflow grounded)
INERT_BLOCK = list(range(5, 23))          # 19 identical cmag=0+PROT=1 MEMR — the "diffuser" block
RECIRC_READ = [0, 1, 2, 3, 51]            # cmag>0 MEMR reading recirculated DMEM (the feedback taps)
MOD_TAPS = [42, 56, 57, 62, 63, 64, 65, 66, 67, 68, 94]  # per-frame-modulated taps that are ≤99


# ---------------------------------------------------------------------------
# Stimulus (S2 primary decay probe; S1 -6 dBFS IR cross-check)
# ---------------------------------------------------------------------------
BURST_S = 0.30
TOTAL_S = 2.2


def s2():
    return ST.noise_burst(BURST_S, TOTAL_S, fs=int(FS))


def s1(level=-6.0):
    return ST.unit_impulse(level, int(TOTAL_S * FS), fs=int(FS))


# ★ Measure the REAL D/A channels A/B/C/D SEPARATELY. Never `mono` — the decode shows dry-clobber on
# overlapping channels, so summing them is a measurement artifact (an early pass mis-read a railed
# mono sum as "over-unity"; plan 020 says measure each channel separately, do not sum blindly).
CHANNELS = ("A", "B", "C", "D")


def measure(cap, exc, name, burst_end_s=0.0):
    return W.measure_output(cap, exc, name, channels=CHANNELS, burst_end_s=burst_end_s)


def cap_diff(cap_a, cap_b):
    """Max abs per-channel difference between two captures — the INERTNESS GUARD. A probe whose output
    is identical to baseline changed nothing that reaches the D/A (a no-op probe, not a real result)."""
    return {c: int(np.max(np.abs(cap_a[c].astype(np.int64) - cap_b[c].astype(np.int64)))) for c in CHANNELS}


def verdict_line(tag, res):
    print(f"  {tag}")
    print(W.summarize(res))


def densest(res):
    """Return the 'best' channel verdict for a quick lever read: prefer DENSE, then WET, then any."""
    best = None
    for c, v in res.items():
        if v["verdict"] == "INDETERMINATE" and v["subverdict"] == "empty":
            continue
        key = (v["density"] == "DENSE", v["is_wet"], v["ned_max"])
        if best is None or key > best[1]:
            best = (c, key, v)
    return best[2] if best else None


# ---------------------------------------------------------------------------
# probes
# ---------------------------------------------------------------------------
def baseline(wcs):
    print("\n" + "=" * 74)
    print("BASELINE — static CONCERT WCS (expected: SPARSE / dry-clobber + sparse echoes)")
    print("=" * 74)
    exc = s2()
    cap = W.run_capture(wcs, exc)
    res = measure(cap, exc, "phase05_baseline_S2", burst_end_s=BURST_S)
    verdict_line("S2 noise burst (per real channel A/B/C/D):", res)
    return densest(res), cap


def _report(name, w, base_cap, mutate=None):
    """Render a probed WCS, print the inertness guard + per-channel verdicts, return the best verdict."""
    exc = s2()
    cap = W.run_capture(w, exc, mutate=mutate)
    diff = cap_diff(cap, base_cap)
    inert = all(v == 0 for v in diff.values())
    res = measure(cap, exc, name, burst_end_s=BURST_S)
    print(f"  Δ-vs-baseline per channel {diff}  {'← INERT (no effect on D/A!)' if inert else ''}")
    verdict_line(f"{name}:", res)
    return densest(res), inert


def probe_coeff(wcs, base_cap):
    print("\n" + "=" * 74)
    print("0.5.1 COEFFICIENT probe — force cmag>0 into the steps 5–22 block + recirc taps")
    print("=" * 74)
    outcomes = {}
    for cval in (16, 32):
        w = list(wcs)
        for k in INERT_BLOCK + RECIRC_READ:
            w[k] = with_cmag(w[k], cval)
        outcomes[cval] = _report(f"phase05_coeff_cmag{cval}_S2", w, base_cap)
    return outcomes


def probe_mod(wcs, base_cap):
    print("\n" + "=" * 74)
    print("0.5.2 MODULATION probe — per-frame LFO on the modulated taps (no engine-timing change)")
    print("=" * 74)
    # The firmware rewrites taps [42,56,57,62–68,94,...] per frame. Without the exact rewrite values we
    # apply a slow LFO to the modulatable field of EACH modulated tap: delay-offset for MEMR/MEMW taps,
    # coefficient (cmag) for the rest. This tests "does time-variation densify?" independent of timing.
    lfo_hz = 1.0
    d_off, d_cmag = 12, 8
    kinds = {k: dev_class(wcs[k]) for k in MOD_TAPS}
    print(f"  modulated taps + device class: {kinds}")

    def mutate(s):
        w = list(wcs)
        ph = np.sin(2 * np.pi * lfo_hz * s / FS)
        for k in MOD_TAPS:
            if kinds[k] in ("MEMR", "MEMW"):
                w[k] = with_offset_delta(wcs[k], int(round(d_off * ph)))
            else:
                w[k] = with_cmag(wcs[k], max(0, min(63, get_cmag(wcs[k]) + int(round(d_cmag * ph)))))
        return w

    return _report("phase05_mod_lfo_S2", wcs, base_cap, mutate)


def probe_gain(wcs, base_cap):
    print("\n" + "=" * 74)
    print("0.5.3 LOOP-GAIN probe — sweep an overall gain on the recirculating feedback taps")
    print("=" * 74)
    outcomes = {}
    for factor in (0.5, 1.0, 2.0):
        w = list(wcs)
        for k in RECIRC_READ:
            w[k] = scale_cmag(w[k], factor)
        cmags = [get_cmag(w[k]) for k in RECIRC_READ]
        print(f"  --- recirc-tap cmag×{factor} → {cmags} ---")
        outcomes[factor] = _report(f"phase05_gain_x{factor}_S2", w, base_cap)
    return outcomes


# ---------------------------------------------------------------------------
def main():
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass
    print("=" * 74)
    print("224XL plan-020 Phase 0.5 — discriminating experiments")
    print("=" * 74)
    W.assert_metric_trusted()
    print("P5 control battery: TRUSTED")

    print("loading CONCERT WCS…")
    wcs = W.load_concert_wcs()

    # runtime benchmark (size expectations)
    t0 = time.time()
    _ = W.run_capture(wcs, ST.unit_impulse(-6.0, int(0.2 * FS)))
    dt = time.time() - t0
    print(f"  timing: 0.2 s render = {dt:.2f}s  →  ~{dt/0.2*TOTAL_S:.1f}s per {TOTAL_S}s render")

    base, base_cap = baseline(wcs)
    coeff = probe_coeff(wcs, base_cap)
    mod, mod_inert = probe_mod(wcs, base_cap)
    gain = probe_gain(wcs, base_cap)

    # ---- 0.5.4 decision summary ----
    print("\n" + "=" * 74)
    print("0.5.4 DECISION GATE — which lever moves density?")
    print("=" * 74)

    def dv(v):
        return f"{(v['density'] if v else '—')} / {(v['verdict'] if v else '—')}"

    print(f"  BASELINE (static)   : {dv(base)}")
    print(f"  0.5.1 coeff cmag=16 : {dv(coeff[16][0])}   inert={coeff[16][1]}")
    print(f"  0.5.1 coeff cmag=32 : {dv(coeff[32][0])}   inert={coeff[32][1]}")
    print(f"  0.5.2 modulation    : {dv(mod)}   inert={mod_inert}")
    for f, (v, inert) in gain.items():
        print(f"  0.5.3 gain ×{f:<4}     : {dv(v)}   inert={inert}   rt60={v['rt60_s'] if v else '—'}")
    print("\n  → A lever that flips SPARSE→DENSE (and is NOT inert) localizes the cause. An INERT probe")
    print("    (Δ=0 vs baseline) proves that knob does not reach the D/A on this behavioral engine —")
    print("    which is itself evidence about where fidelity must improve (Phase 1 timing / output path).")


if __name__ == "__main__":
    main()
