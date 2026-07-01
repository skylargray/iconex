#!/usr/bin/env python3
"""Plan 020 — offset-convention probe. The Phase-0.5 RES-death root cause is that the MEMR reads and
MEMW writes address DISJOINT memory regions under `addr = CPC + ofst + 1`, so the loop closes only at
long (~1–1.6 s) separations → sparse late output, never a dense build-up. This probe asks: does a
DIFFERENT interpretation of the MI0-15 offset field make the MEMR reads and MEMW writes share a region
(closing the loop at SHORT separations), and does the emitted output then become dense?

For each candidate convention it reports, on the static CONCERT WCS:
  • the shortest MEMR↔MEMW address separation (short ⇒ short-separation feedback is possible),
  • how many read/write pairs sit within 0.1 s of each other,
  • whether the MEMR reads actually return signal in a warmed sample (loop closes),
  • the reverb_metrics three-state verdict on the emitted D/A output (P1/P5 enforced).

Measured on the emitted WR DA/ output only; control battery asserted first (P5). No DSP-role labels —
everything is described by the mechanism (MEMR/MEMW address, separation in samples).

Run:  python tools/offset_convention_probe.py
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np

import aru_whole as W
import aru_freerun as FR
import stimulus as ST

FS = W.FS
BURST_S, TOTAL_S = 0.30, 1.6
SHORT_S = 0.10                         # "short separation" threshold
SHORT_N = int(SHORT_S * FS)


# --- candidate conventions: field (l0,l1,l2,l3) -> V, where addr = CPC + V (mod 2^16) ---
def _F(step):
    return step[0] | (step[1] << 8)


CONVENTIONS = {
    "baseline  addr=CPC+F+1 (=CPC-OFST)": lambda s: (_F(s) + 1) & 0xFFFF,
    "raw       addr=CPC+F":               lambda s: _F(s) & 0xFFFF,
    "neg       addr=CPC-F":               lambda s: (-_F(s)) & 0xFFFF,
    "comp      addr=CPC+~F (=CPC-F-1)":   lambda s: (~_F(s)) & 0xFFFF,
    "bswap+1   addr=CPC+swap(F)+1":       lambda s: (((s[1] | (s[0] << 8)) + 1) & 0xFFFF),
    "bswap_neg addr=CPC-swap(F)":         lambda s: (-((s[1] | (s[0] << 8)))) & 0xFFFF,
    "lowbyte   addr=CPC+l0+1":            lambda s: (s[0] + 1) & 0xFFFF,
    "lowbyte_neg addr=CPC-l0":            lambda s: (-s[0]) & 0xFFFF,
    "signed    addr=CPC+s16(F)+1":        lambda s: (FR.s16(_F(s)) + 1) & 0xFFFF,
}


def mem_steps(wcs):
    """Return (memr_steps, memw_steps): step indices that read / write DMEM (0..99)."""
    memr, memw = [], []
    for k in range(100):
        d = FR.decode(wcs[k][2], wcs[k][3])
        if d["MEMAC"] and d["MI16"]:
            memr.append(k)
        elif d["MEMAC"] and not d["MI16"]:
            memw.append(k)
    return memr, memw


def separation_stats(wcs, Vf, memr, memw):
    """Shortest MEMR↔MEMW address separation (samples) and count of pairs within SHORT_N.
    Separation is CPC-independent (both addresses shift +1/sample together)."""
    ra = [Vf(wcs[k]) for k in memr]
    wa = [Vf(wcs[k]) for k in memw]
    best = 1 << 16
    n_short = 0
    for r in ra:
        for w in wa:
            sep = min((r - w) & 0xFFFF, (w - r) & 0xFFFF)     # nearest wrap
            best = min(best, sep)
            if sep <= SHORT_N:
                n_short += 1
    return best, n_short, len(ra) * len(wa)


def loop_closes(wcs, offsets, warm=250):
    """Warm the engine under this convention; does any MEMR read return |v|>10 (signal recirculated)?"""
    aru = FR.FreeRunARU()
    exc = ST.noise_burst(BURST_S, (warm + 20) / FS, fs=int(FS))
    for s in range(warm):
        aru.run_sample(wcs, int(exc[s]) & 0xFFFF, offsets=offsets)
    probe = []
    aru.run_sample(wcs, int(exc[warm]) & 0xFFFF, offsets=offsets, probe=probe)
    reads = [FR.s16(r["dab"]) for r in probe
             if r["drv"] == FR.DRV_MEMR]
    nz = sum(1 for v in reads if abs(v) > 10)
    return nz, len(reads), (max((abs(v) for v in reads), default=0))


def best_channel(cap, exc, name):
    res = W.measure_output(cap, exc, name, channels=("A", "B", "C", "D"), burst_end_s=BURST_S)
    best = None
    for c, v in res.items():
        if v["verdict"] == "INDETERMINATE" and v["subverdict"] == "empty":
            continue
        key = (v["density"] == "DENSE", v["is_wet"], v["ned_max"])
        if best is None or key > best[0]:
            best = (key, c, v)
    return best[1:] if best else (None, None)


def main():
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass
    print("=" * 78)
    print("224XL plan-020 — offset-convention probe")
    print("=" * 78)
    W.assert_metric_trusted()
    print("P5 control battery: TRUSTED")
    wcs = W.load_concert_wcs()
    memr, memw = mem_steps(wcs)
    exc = ST.noise_burst(BURST_S, TOTAL_S, fs=int(FS))
    print(f"MEMR steps={memr}\nMEMW steps={memw}\n")
    print(f"{'convention':36s} {'minSep(s)':>9s} {'#short':>6s} {'loopMEMR nz/max':>16s}  verdict")
    print("-" * 78)
    results = {}
    for name, Vf in CONVENTIONS.items():
        offsets = [Vf(wcs[k]) for k in range(128)]
        minsep, nshort, npair = separation_stats(wcs, Vf, memr, memw)
        nz, nreads, mx = loop_closes(wcs, offsets)
        cap = W.run_capture(wcs, exc, offsets=offsets)
        c, v = best_channel(cap, exc, f"offconv_{name.split()[0]}")
        vs = f"{v['verdict']}/{v['density']} ch{c} rt60={v['rt60_s']}" if v else "(all empty)"
        print(f"{name:36s} {minsep/FS:9.3f} {nshort:6d} {f'{nz}/{mx}':>16s}  {vs}")
        results[name] = dict(minsep=minsep, nshort=nshort, nz=nz, best_c=c, verdict=v)

    print("-" * 78)
    print("Reading: a convention with a SMALL minSep(s) + #short>0 + loop MEMR nz>0 is one where the")
    print("MEMR reads and MEMW writes share a region and the loop closes at short separations. If its")
    print("output verdict is WET/DENSE, the offset convention is the lever (targeted fix). If EVERY")
    print("convention keeps minSep large / MEMR reads at 0, the missing tail is NOT a simple offset")
    print("re-interpretation — escalate to the cmag=0 block (plan 016) / real tap pattern.")


if __name__ == "__main__":
    main()
