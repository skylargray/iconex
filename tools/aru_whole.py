#!/usr/bin/env python3
"""224XL whole-machine free-run scaffold (plan 020 Phase 0.3; plan 024 F1d re-sync).

Hosts a free-running 224XL machine and captures the EMITTED D/A output (`WR DA/`) so it can be
measured by the proven `reverb_metrics` harness. This is the scaffold every later phase plugs into:

    load a WCS image  ->  run N samples with a defined stimulus  ->  capture the WR DA/ stream
    per channel (A/B/C/D)  ->  hand it (and the exact excitation) to reverb_metrics.analyze.

★ ENGINE (plan 024 F1d): the default engine is now the PIN-LOCKED RTL engine
`aru_freerun22_rtl.RTL22` (session-0022 coordinates, L+1 frame, complement-domain MAC law —
1469/1469 ARU signature pins) behind the `RTL22Engine` adapter below. The behavioral
`aru_freerun.FreeRunARU` remains reachable via the `engine=` parameter for archaeology only —
its audio verdicts are void (session 0022). The frame rate is program-defined (fs22(L)); each
capture reports its own 'fs'.

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
import aru_freerun22_rtl as R22
from aru_freerun22 import enc_io, enc_idle, SRC_RDAD, SRC_RDRREG
import reverb_metrics as RM
import reverb_metrics_selftest as RMST
import stimulus as ST

FS = FR.FS                                  # legacy nominal (34130 Hz); captures carry their own fs


class RTL22Engine:
    """The plan-024 default engine behind the capture boundary: aru_freerun22_rtl.RTL22
    (complement-domain physical MAC law, pin-locked 1469/1469). Presents the FreeRunARU
    run_sample surface (raw 128-word WCS in, (chan_index, value) tuples out); decodes each
    distinct image once (keyed by its bytes) so per-frame `mutate` modulation stays cheap."""

    def __init__(self, fpc_enabled=False):
        self.eng = R22.RTL22(fpc_enabled=fpc_enabled)
        self.fault = None                   # RTL22 has no fault model; kept for surface parity
        self.L = None
        self._rows_cache = {}

    def _rows(self, wcs):
        key = bytes(b for w in wcs for b in w)
        hit = self._rows_cache.get(key)
        if hit is None:
            rows, L, _w_reset = R22.program_rows22(wcs)
            hit = self._rows_cache[key] = (rows, L)
        self.L = hit[1]
        return hit[0]

    @property
    def fs(self):
        return R22.fs22(self.L) if self.L is not None else None

    def run_sample(self, wcs, audio_in, offsets=None):
        assert offsets is None, ("per-step offset tables are a behavioral-era concept; "
                                 "the RTL path derives addresses from the stored lanes")
        return [("ABCD".index(c), v) for c, v in self.eng.run_sample(self._rows(wcs), audio_in)]

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
    engine     : the machine to run. None → the pin-locked RTL22Engine (plan 024 default).
                 Pass aru_freerun.FreeRunARU(...) explicitly for behavioral-era archaeology only.
                 Must expose run_sample(wcs, audio_in, offsets=...) -> list of (chan, value) + .fault.

    Returns a dict: 'A'..'D' int16 arrays (per-channel D/A output), 'mono' int16 (sum of writes),
    'n' samples, 'fault', and 'fs' (program-defined rate when the engine exposes one, else the
    legacy nominal FS). NOTHING internal (buf_RMS/DMEM/ACC) leaves this function — P1."""
    aru = engine if engine is not None else RTL22Engine(fpc_enabled=fpc)
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
                mono=clip(mono), n=n, fault=aru.fault,
                fs=float(getattr(aru, "fs", None) or FS))


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
                   burst_end_s=0.0, out_dir=RENDERS, fs=None):
    """Measure the captured D/A output per channel with reverb_metrics.analyze (renders a WAV each).
    Returns {channel: verdict-dict}. Asserts the control battery first (P5). fs defaults to the
    capture's own program-defined rate (run_capture stamps 'fs')."""
    assert_metric_trusted()
    exc = np.asarray(excitation, dtype=np.int16)
    fs_hz = fs or captured.get("fs", FS)
    results = {}
    for c in channels:
        out = captured[c]
        results[c] = RM.analyze(out, exc, fs_hz, f"{name}_ch{c}", out_dir=out_dir, burst_end_s=burst_end_s)
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

    # A same-frame passthrough WCS in the 0022 convention (execution order 127 down to the
    # reset word; the RTL passthrough idiom: RD-AD -> unity MAC -> XFER -> RDRREG out, padded
    # with idles to L=99 so fs matches the canonical 100-step frame). Feed an S1 impulse; the
    # metric must call the emitted output DRY (a pure passthrough is not reverb — P3 dry-gate).
    # This proves the capture boundary + the metric wiring end-to-end on the RTL engine.
    wcs = [enc_idle()] * 128
    wcs[127] = enc_io(sel=SRC_RDAD, wa=1, cmag=0, zero=1, csign=0)
    wcs[126] = enc_idle(ra=1, cmag=32, csign=1)
    wcs[125] = enc_idle(xfer=1)
    wcs[29] = enc_io(sel=SRC_RDRREG, wrda=True, chans="A", reset=True)   # w_reset=29 -> L=99
    exc = ST.unit_impulse(-6.0, int(0.3 * FS))
    cap = run_capture(wcs, exc)
    print(f"  program-defined fs = {cap['fs']:.1f} Hz (L+1 frame)")
    res = measure_output(cap, exc, "f1d_selfcheck_zerodelay", channels=("A",))
    v = res["A"]
    print(f"  zero-delay passthrough -> ch A verdict={v['verdict']} (expect DRY), wav={os.path.basename(v['wav'])}")
    ok = v["verdict"] == "DRY"
    print(f"  scaffold end-to-end (RTL22 engine): {'OK' if ok else 'FAIL'}")
    return ok


if __name__ == "__main__":
    _selfcheck()
