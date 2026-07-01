#!/usr/bin/env python3
"""Plan 020 (post-M3.X, output-capture investigation) — XFER-gating hypothesis probe.

The output steps read a dead result register because late microprogram steps overwrite it (repeated
XFER=1, near-zero operands). The netlist gates XFER CK = NAND(AS0, XFER, tc_U25.pin9); the third term is
an "unused"-FF output (§3.11) → provisionally constant, i.e. XFER fires on every XFER bit (the faithful
default, which gives the dead output). This probe tests whether a DIFFERENT XFER-gating rule (some class
of steps does NOT latch the result register) revives the CONCERT output — a concrete test of the
output-capture hypothesis. If some rule → WET/DENSE, that localizes the semantics; if none does, the whole
XFER-gating class is ruled out.

Measured on the emitted D/A output only (P1); control battery asserted first (P5). No DSP-role labels.
Run:  python tools/xfer_gate_probe.py
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np

import aru_whole as W
import aru_freerun_rtl as RTL
import stimulus as ST

FS = W.FS
BURST_S, TOTAL_S = 0.30, 2.2


def is_idle(d):
    return d["MEMAC"] == 0 and d["MI16"] == 0


def is_io(d):
    return d["MEMAC"] == 0 and d["MI16"] == 1


def is_memw(d):
    return d["MEMAC"] == 1 and d["MI16"] == 0


def is_memr(d):
    return d["MEMAC"] == 1 and d["MI16"] == 1


# XFER-gating hypotheses: gate(d, dev) -> True = XFER latches the result reg this step.
GATES = {
    "baseline (always)":        None,
    "only cmag>0":              lambda d, dev: d["cmag"] > 0,
    "only MEMW steps":          lambda d, dev: is_memw(d),
    "only compute (idle-dev)":  lambda d, dev: is_idle(d),
    "not on IO steps":          lambda d, dev: not is_io(d),
    "only MEMAC steps":         lambda d, dev: d["MEMAC"] == 1,
    "not on idle steps":        lambda d, dev: not is_idle(d),
    "only when RDRREG drives":  lambda d, dev: dev["driver"] == RTL.FR.DRV_RDRREG,
}


def best(cap, exc, name):
    res = W.measure_output(cap, exc, name, channels=("A", "B", "C", "D"), burst_end_s=BURST_S)
    b = None
    for c, v in res.items():
        if v["verdict"] == "INDETERMINATE" and v["subverdict"] == "empty":
            continue
        key = (v["density"] == "DENSE", v["is_wet"], v["ned_max"])
        if b is None or key > b[0]:
            b = (key, c, v)
    return b[2] if b else None, res


def main():
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass
    print("=" * 78)
    print("XFER-gating hypothesis probe — does any result-reg-load rule revive the CONCERT output?")
    print("=" * 78)
    W.assert_metric_trusted()
    print("P5 control battery: TRUSTED")
    wcs = W.load_concert_wcs()
    exc = ST.noise_burst(BURST_S, TOTAL_S, fs=int(FS))
    print(f"{'gate hypothesis':28s}  bestCh  verdict/density   wet     rt60    peak")
    print("-" * 78)
    hits = []
    for name, gate in GATES.items():
        eng = RTL.FreeRunRTL(modulus=100, xfer_gate=gate)
        cap = W.run_capture(wcs, exc, engine=eng)
        v, res = best(cap, exc, f"xfergate_{name.split()[0]}")
        # find the channel of the best verdict
        ch = next((c for c in "ABCD" if res[c] is v), "?")
        line = (f"{name:28s}  ch{ch:<4}  {str(v['verdict']) if v else '—':<13} "
                f"{str(v['density']) if v else '—':<7} {v['wetness'] if v else 0:.3f}  "
                f"{str(v['rt60_s']) if v else '—':<7} {v['peak'] if v else 0}")
        print(line)
        if v and v["verdict"] == "WET-PASS" and v["density"] == "DENSE":
            hits.append(name)
    print("-" * 78)
    if hits:
        print(f"⇒ REVIVED by: {hits} — an XFER-gating rule produces the tail. Trace this against §G3T.")
    else:
        print("⇒ NO XFER-gating rule produces WET/DENSE. The output-capture death is NOT a simple XFER-gate.")
        print("  Remaining unresolved microword semantics: PROT (MI22, effect untraced) + cmag=0 (plan 016)")
        print("  + whether the 0x4000 snapshot is the running program. This is the L7 ceiling (physical unit).")


if __name__ == "__main__":
    main()
