#!/usr/bin/env python3
"""224XL whole-machine free-run scaffold (plan 020 Phase 0.3).

Hosts a free-running 224XL machine and captures the EMITTED D/A output (`WR DA/`) so it can be
measured by the proven `reverb_metrics` harness. This is the scaffold every later phase plugs into:

    load a WCS image  ->  run N samples with a defined stimulus  ->  capture the WR DA/ stream
    per channel (A/B/C/D)  ->  hand it (and the exact excitation) to reverb_metrics.analyze.

★ FIDELITY HONESTY (read this): at Phase 0.3 the datapath underneath is the BEHAVIORAL free-run
engine `aru_freerun.FreeRunARU` — NOT yet the edge-driven ClockEngine datapath. That is deliberate
and matches plan 020's recommended order: Phase 0.5's cheap discriminating experiments run on the
*existing* behavioral engine (measured by the now-proven metric) to localize the cause BEFORE the
expensive Phase-1..3 timing rebuild. Phases 1–3 replace the engine here with the edge-driven
`aru_rtl.ClockEngine` + `aru_rtl_dp` datapath while keeping this capture/measure boundary identical.

WHAT IS ENFORCED HERE (the anti-"dry reported as reverb" guarantees):
  • P1 — the ONLY signal handed to the metric is the WR DA/ capture (the D/A output stream). This
    scaffold NEVER passes buf_RMS / DMEM contents / accumulator state to a metric. Structurally.
  • P2 — every measurement renders a timestamped WAV (reverb_metrics.write_wav does the naming).
  • P5 — measure_output() refuses to judge unless reverb_metrics_selftest.run_battery() passes in
    THIS process first. A metric that can't tell dry from wet is not trusted for anything.
  • Stimulus comes ONLY from tools/stimulus.py (S1/S2/S3); never an improvised one-off.

Run:  python tools/aru_whole.py            (self-check: battery + a zero-delay passthrough render)
"""
import os
import sys
import json

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np

import aru_freerun as FR
import reverb_metrics as RM
import reverb_metrics_selftest as RMST
import stimulus as ST

FS = FR.FS                                  # 34130 Hz (100 microinstr × 292.97 ns)

# CONCERT WCS cache (booting the firmware is ~30–90 s; cache the 0x4000 image to our scratchpad).
_SCR = (r"C:/Users/Skylar/AppData/Local/Temp/claude/"
        r"d--OneDrive-Gray-Instruments-iconex/f518c0e2-0da8-45ca-b9f2-9763aee91411/scratchpad")
_WCS_CACHE = os.path.join(_SCR, "concert_wcs_0x4000.json")
RENDERS = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "renders")


# ---------------------------------------------------------------------------
# WCS loading
# ---------------------------------------------------------------------------
def load_concert_wcs(use_cache=True):
    """Return the 128-step CONCERT WCS as a list of (l0,l1,l2,l3), booting the firmware once and
    caching the 0x4000..0x41FF image. This is the PROVEN-genuine static CONCERT program (plan 019)."""
    if use_cache and os.path.exists(_WCS_CACHE):
        img = json.load(open(_WCS_CACHE))
    else:
        import boot8080 as B
        print("  booting v8.2.1 firmware to CONCERT (~30–90 s)…", flush=True)
        m, ms = B.boot(verbose=False)
        assert "mainloop" in ms, f"boot did not reach mainloop: {ms}"
        img = [m.memory[0x4000 + i] for i in range(0x200)]
        os.makedirs(_SCR, exist_ok=True)
        json.dump(img, open(_WCS_CACHE, "w"))
        print("  captured + cached 0x4000..0x41FF from the verified boot.", flush=True)
    return [(img[4 * k], img[4 * k + 1], img[4 * k + 2], img[4 * k + 3]) for k in range(128)]


# ---------------------------------------------------------------------------
# Free-run + capture (P1: capture ONLY the WR DA/ output stream)
# ---------------------------------------------------------------------------
def run_capture(wcs, excitation, offsets=None, fpc=False, mutate=None, probe_first=0, engine=None):
    """Free-run the machine over `excitation` (int16 array/list) and capture the WR DA/ output.

    wcs        : 128-step list of (l0,l1,l2,l3). If `mutate` is given it is IGNORED as the base and
                 mutate(sample_index) must return the wcs to use for that sample (per-frame modulation).
    excitation : int16 sequence injected at RD AD/ (the A/D input), one value per sample.
    offsets    : optional per-step DMEM offset table; None = static WCS lanes-0/1 (addr = CPC − OFST),
                 the POST-grounded convention settled for the static CONCERT program.
    fpc        : apply the FPC float↔fixed codec at the I/O boundary (default OFF → pure fixed-point).
    mutate     : optional callable(sample_index)->wcs for time-varying (modulated) programs.
    engine     : the machine to run. None → behavioral aru_freerun.FreeRunARU (the M3.X behavioral
                 column / oracle). Pass a tools.aru_freerun_rtl.FreeRunRTL instance for the timed column.
                 Must expose run_sample(wcs, audio_in, offsets=...) -> list of (chan, value) + .fault.

    Returns a dict: 'A'..'D' int16 arrays (per-channel D/A output), 'mono' int16 (sum of writes),
    'n' samples, 'fault'. NOTHING internal (buf_RMS/DMEM/ACC) leaves this function — P1."""
    aru = engine if engine is not None else FR.FreeRunARU(fpc_enabled=fpc)
    n = len(excitation)
    chans = {c: np.zeros(n, dtype=np.int64) for c in "ABCD"}
    mono = np.zeros(n, dtype=np.int64)
    for s in range(n):
        w = mutate(s) if mutate is not None else wcs
        ai = int(excitation[s]) & 0xFFFF
        outs = aru.run_sample(w, ai, offsets=offsets)
        persamp = {c: None for c in "ABCD"}
        ssum = 0
        for chan, val in outs:
            ssum += val
            persamp["ABCD"[chan & 3]] = val
        for c in "ABCD":
            if persamp[c] is not None:
                chans[c][s] = persamp[c]
        mono[s] = ssum
        if aru.fault:
            break
    clip = lambda a: np.clip(a, -32768, 32767).astype(np.int16)
    return dict(A=clip(chans["A"]), B=clip(chans["B"]), C=clip(chans["C"]), D=clip(chans["D"]),
                mono=clip(mono), n=n, fault=aru.fault)


# ---------------------------------------------------------------------------
# Measurement (P5: battery must pass in-process before any judgement)
# ---------------------------------------------------------------------------
_BATTERY_OK = None


def assert_metric_trusted():
    """P5 trust anchor: run the control battery once per process; refuse to proceed if it fails."""
    global _BATTERY_OK
    if _BATTERY_OK is None:
        _BATTERY_OK = RMST.run_battery(out_dir=_SCR, verbose=False)
    if not _BATTERY_OK:
        raise RuntimeError("reverb_metrics control battery FAILED — metric not trusted; refusing to "
                           "measure. Fix the metric before any audio claim (plan 020 P5/AC0-M).")


def measure_output(captured, excitation, name, channels=("A", "B", "C", "D", "mono"),
                   burst_end_s=0.0, out_dir=RENDERS):
    """Measure the captured D/A output per channel with reverb_metrics.analyze (renders a WAV each).
    Returns {channel: verdict-dict}. Asserts the control battery first (P5)."""
    assert_metric_trusted()
    exc = np.asarray(excitation, dtype=np.int16)
    results = {}
    for c in channels:
        out = captured[c]
        results[c] = RM.analyze(out, exc, FS, f"{name}_ch{c}", out_dir=out_dir, burst_end_s=burst_end_s)
    return results


def summarize(results, only_nonempty=True):
    """One-line-per-channel summary of a measure_output() result."""
    lines = []
    for c, v in results.items():
        if only_nonempty and v["verdict"] == "INDETERMINATE" and v["subverdict"] == "empty":
            continue
        rt = v["rt60_s"]
        lines.append(f"    ch{c:<4} {v['verdict']:<13} {str(v['subverdict']):<18} "
                     f"dens={str(v['density']):<6} wet={v['wetness']:.3f} "
                     f"rt60={rt if rt is not None else '—'} peak={v['peak']} "
                     f"ned={v['ned_max']:.2f}")
    return "\n".join(lines) if lines else "    (all channels empty)"


# ---------------------------------------------------------------------------
# self-check
# ---------------------------------------------------------------------------
def _selfcheck():
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass
    print("=" * 74)
    print("aru_whole.py — Phase 0.3 scaffold self-check")
    print("=" * 74)
    print("P5 control battery (must pass before any measurement)…")
    assert_metric_trusted()
    print("  battery: TRUSTED")

    # A zero-delay passthrough WCS: read A/D -> DAB -> WR DA (chan A). Feed an S1 impulse; the metric
    # must call the emitted output DRY (a pure passthrough is not reverb — P3 dry-gate). This proves
    # the capture boundary + the metric wiring end-to-end on the free-run scaffold.
    wcs = [FR.nop_step()] * 128
    wcs = list(wcs)
    wcs[0] = FR.encode_io_step(rd="AD", wr_da=True, da_chan=0)
    exc = ST.unit_impulse(-6.0, int(0.3 * FS))
    cap = run_capture(wcs, exc)
    res = measure_output(cap, exc, "phase03_selfcheck_zerodelay", channels=("A",))
    v = res["A"]
    print(f"  zero-delay passthrough -> ch A verdict={v['verdict']} (expect DRY), wav={os.path.basename(v['wav'])}")
    ok = v["verdict"] == "DRY"
    print(f"  scaffold end-to-end: {'OK' if ok else 'FAIL'}")
    return ok


if __name__ == "__main__":
    _selfcheck()
