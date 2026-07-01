#!/usr/bin/env python3
"""Plan 020 Milestone M3.X — does the CONCERT tail EMERGE on the timing-faithful model?

Established before running (value-identity, not a render):
  • FreeRunRTL (Phase 1 edge-MAC + Phase 2 PC free-run + Phase 3 read-before-write DMEM) is NUMERICALLY
    IDENTICAL to the behavioral aru_freerun on the real CONCERT program, all channels. So aru_freerun was
    already timing-faithful for the recirculation-relevant timing → the "timed vs behavioral" columns are
    the same. (This corroborates the Phase-0.5 finding that timing is not the lever.)

So the milestone tests the ONE thing the rebuild enables that aru_freerun could NOT: the WCS PC MODULUS.
aru_freerun hardcodes NSTEPS=100; FreeRunRTL makes it a parameter, so steps 100..127 — including the
per-frame-modulated taps 107..119 — can execute (modulus=128). Cells:

  A100  timed, static,      modulus=100   (== behavioral baseline; the proven-identical cell)
  A128  timed, static,      modulus=128   (steps 100..127 execute — NEW, impossible on aru_freerun)
  C128  timed, modulated,   modulus=128   (per-frame LFO on taps 107..119 + the ≤99 modulated taps — NEW)

Every measurement is reverb_metrics on the EMITTED D/A output only (P1), control battery asserted first
(P5), WAV rendered (P2). Stimulus = S2 noise burst (primary) from tools/stimulus.py. No DSP-role labels.

Run:  python tools/milestone_m3x.py
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np

import aru_whole as W
import aru_freerun as FR
import aru_freerun_rtl as RTL
import stimulus as ST

FS = W.FS
BURST_S, TOTAL_S = 0.30, 2.2

# per-frame-modulated taps (memory [[224xl-m4-output-path-and-static-wcs]]); 107..119 need modulus>=120
MOD_TAPS = [42, 56, 57, 62, 63, 64, 65, 66, 67, 68, 94, 107, 108, 109, 110, 111, 112, 113, 114, 115,
            116, 117, 118, 119]


def get_cmag(step):
    return (((~step[3]) & 0xFF) >> 2) & 0x3F


def with_cmag(step, cmag):
    l0, l1, l2, l3 = step
    inv3 = (~l3) & 0xFF
    xfer, zero = inv3 & 1, (inv3 >> 1) & 1
    return (l0, l1, l2, (~(xfer | (zero << 1) | ((cmag & 0x3F) << 2))) & 0xFF)


def with_offset_delta(step, delta):
    l0, l1, l2, l3 = step
    ofst = (((l1 << 8) | l0) + delta) & 0xFFFF
    return (ofst & 0xFF, (ofst >> 8) & 0xFF, l2, l3)


def dev_class(step):
    d = FR.decode(step[2], step[3])
    return ("MEMR" if (d["MEMAC"] and d["MI16"]) else "MEMW" if (d["MEMAC"] and not d["MI16"])
            else "IO" if d["MI16"] else "idle")


def measure_cell(name, cap, exc):
    res = W.measure_output(cap, exc, name, channels=("A", "B", "C", "D"), burst_end_s=BURST_S)
    print(f"  [{name}]")
    print(W.summarize(res))
    # best channel for the go/no-go
    best = None
    for c, v in res.items():
        if v["verdict"] == "INDETERMINATE" and v["subverdict"] == "empty":
            continue
        key = (v["density"] == "DENSE", v["is_wet"], v["ned_max"])
        if best is None or key > best[0]:
            best = (key, c, v)
    return best[2] if best else None


def modulator(wcs, modulus):
    """Per-frame LFO on the modulated taps' modulatable field (offset for MEMR/MEMW, cmag otherwise).
    Only taps < modulus are rewritten (others are not fetched)."""
    taps = [k for k in MOD_TAPS if k < modulus]
    kinds = {k: dev_class(wcs[k]) for k in taps}

    def mutate(s):
        w = list(wcs)
        ph = np.sin(2 * np.pi * 1.0 * s / FS)
        for k in taps:
            if kinds[k] in ("MEMR", "MEMW"):
                w[k] = with_offset_delta(wcs[k], int(round(12 * ph)))
            else:
                w[k] = with_cmag(wcs[k], max(0, min(63, get_cmag(wcs[k]) + int(round(8 * ph)))))
        return w
    return mutate, taps


def main():
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass
    print("=" * 78)
    print("Plan 020 Milestone M3.X — does the CONCERT tail emerge? (timing-faithful FreeRunRTL)")
    print("=" * 78)
    W.assert_metric_trusted()
    print("P5 control battery: TRUSTED")
    wcs = W.load_concert_wcs()
    exc = ST.noise_burst(BURST_S, TOTAL_S, fs=int(FS))

    print("\n--- A100: timed static modulus=100 (== behavioral baseline) ---")
    a100 = measure_cell("m3x_A100_timed_static_mod100_S2",
                        W.run_capture(wcs, exc, engine=RTL.FreeRunRTL(modulus=100)), exc)

    print("\n--- A128: timed static modulus=128 (steps 100..127 execute — NEW) ---")
    a128 = measure_cell("m3x_A128_timed_static_mod128_S2",
                        W.run_capture(wcs, exc, engine=RTL.FreeRunRTL(modulus=128)), exc)

    print("\n--- C128: timed modulated modulus=128 (LFO on taps 107..119 + ≤99 — NEW) ---")
    mut, taps = modulator(wcs, 128)
    print(f"  modulated taps (<128): {taps}")
    c128 = measure_cell("m3x_C128_timed_mod_mod128_S2",
                        W.run_capture(wcs, exc, mutate=mut, engine=RTL.FreeRunRTL(modulus=128)), exc)

    print("\n" + "=" * 78)
    print("M3.X DECISION")
    print("=" * 78)

    def dv(v):
        return f"{v['density'] if v else '—'}/{v['verdict'] if v else '—'} rt60={v['rt60_s'] if v else '—'}"
    print(f"  A100 timed static mod100 : {dv(a100)}")
    print(f"  A128 timed static mod128 : {dv(a128)}")
    print(f"  C128 timed modulated     : {dv(c128)}")
    dense = [n for n, v in [("A100", a100), ("A128", a128), ("C128", c128)]
             if v and v["density"] == "DENSE" and v["verdict"] == "WET-PASS"]
    print()
    if dense:
        print(f"  ⇒ WET-PASS/DENSE in: {dense} — a cell produced the tail; investigate which lever.")
    else:
        print("  ⇒ NO cell is WET-PASS/DENSE. The timing-faithful model + modulus=128 + modulation does")
        print("     NOT produce the tail. Per the plan decision table this is 'nothing densifies' →")
        print("     STOP Phase 4-6; re-open cmag=0/PROT + output-capture semantics (plan 016). The")
        print("     Phase-0.5 output-capture root cause stands: the RDRREG output steps read a dead RES.")


if __name__ == "__main__":
    main()
