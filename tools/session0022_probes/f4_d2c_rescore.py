#!/usr/bin/env python3
"""F4d (plan 024) — the d2c re-score: settled cross-program renders through the
re-synced (complement-domain) RTL22, floor-subtracted, per-band at the documented
crossover, with the TRUE name column from program_names.json (ids are BIT-CODED record
tags — 0x03 = SMALL PLATE, a real program; 0x04 = ROOM; registry #34 closed the old
'invalid selector' reading).

Settled images come from the existing cache wcs_settled_all.json (captured 0024-era:
id patch at 0x8160 + mainloop + 6M-tick settle). Only ids MISSING from the cache are
booted here (CD PLATE A = 0x21 = 33, needed for its documented 1.8 s row).

Spec rows scored (ch.4, +-20%): CONCERT V1 LF 3.0/mid 2.0 @720; ROOM V1 1.4 s;
PLATE 0.6/1.8 @ XOV 170 (the documented row is labeled 'Plate V2' — the cached image
is the boot-recalled variation; caveat printed); CD PLATE A/B 1.8 s. Programs without
documented numbers report measured values, no verdict.
"""
import sys, os, json, time

TOOLS = r"d:\OneDrive\Gray Instruments\iconex\tools"
sys.path.insert(0, TOOLS)
HERE = os.path.dirname(os.path.abspath(__file__))
RENDERS = os.path.join(HERE, "renders")
CACHE = os.path.join(HERE, "wcs_settled_all.json")
NAMES = os.path.join(HERE, "program_names.json")

import numpy as np
from scipy.signal import butter, sosfiltfilt
import boot8080
import reverb_metrics as RM
from aru_freerun22_rtl import RTL22, program_rows22, fs22

IDS = [1, 2, 3, 4, 5, 6, 8, 10, 12, 16, 17, 18, 20, 33]

# documented ch.4 rows: id -> (kind, values, xov, label)
DOC = {
    1: ("bands", (3.0, 2.0), 720.0, "LF 3.0/mid 2.0 @720 (V1)"),
    2: ("bands", (0.6, 1.8), 170.0, "0.6/1.8 @170 ('Plate V2' row)"),
    4: ("bb", 1.4, 720.0, "1.4 s (V1)"),
    16: ("bb", 1.8, 720.0, "1.8 s"),
    33: ("bb", 1.8, 720.0, "1.8 s"),
}
# ids the LARC key enumeration (program_names.json) does not reach — record-map names
RECMAP = {6: "HALL/HALL", 10: "PLATE/PLATE", 18: "PLATE/HALL"}
TOL = 0.20

ORIG_LOAD = boot8080.load_mem


def ascii7(b):
    return "".join(chr(x & 0x7F) if 0x20 <= (x & 0x7F) < 0x7F else " " for x in b)


def capture(pid):
    """d2c's settled capture (id patch at 0x8160), name read from the RIGHT buffer
    (0x3F4F — the 0x3F8E readback was the wrong buffer, hence the cache's empty names)."""
    def patched():
        mem = ORIG_LOAD()
        assert bytes(mem[0x8160:0x8163]) == b"\x3a\x00\xb8"
        mem[0x8160:0x8163] = bytes([0x3E, pid & 0xFF, 0x00])
        return mem
    boot8080.load_mem = patched
    try:
        m, ms = boot8080.boot(verbose=False, extra_ticks_after_mainloop=6_000_000)
        ok = "mainloop" in ms and "prog_load" in ms
        name = ascii7(m.memory[0x3F4F:0x3F5B]).rstrip()
        rid = m.memory[0x3CA2]
        return dict(ok=ok and rid == (pid & 0xFF), wcs=bytes(m.memory[0x4000:0x4200]).hex(),
                    name=name, rid=rid, route="id-patch 0x8160 + 6M settle (f4d)")
    finally:
        boot8080.load_mem = ORIG_LOAD


def rt(tail, fs, lo=-5.0):
    """e4c's Schroeder-fit convention: T30, relaxing the floor for short/noisy tails."""
    t = RM._noise_floor_truncate(np.asarray(tail, np.float64), fs)
    edc = RM._schroeder_db(t)
    for hi in (-35.0, -25.0, -20.0, -15.0):
        r, r2, npts = RM._fit_decay(edc, fs, lo, hi)
        if r is not None:
            return r
    return None


def name_of(pid, names):
    if pid in names:
        return names[pid]
    if pid in RECMAP:
        return RECMAP[pid] + " *"
    return f"<id {pid}>"


def fmt3(vals):
    return "/".join(f"{v:.2f}" if v is not None else "nan " for v in vals)


def main():
    names = {}
    for rec in json.load(open(NAMES)).values():
        names[rec["id"]] = rec["display"][:12].rstrip()

    cache = json.load(open(CACHE)) if os.path.exists(CACHE) else {}
    for pid in IDS:
        if str(pid) in cache:
            continue
        print(f"[id {pid:2d}] missing from cache — booting + settling ...", flush=True)
        cache[str(pid)] = capture(pid)
        rec = cache[str(pid)]
        print(f"   ok={rec['ok']} name={rec.get('name')!r} rid=0x{rec.get('rid', 0):02X} "
              f"(expect {name_of(pid, names)!r} / 0x{pid:02X})", flush=True)
        json.dump(cache, open(CACHE, "w"))

    print("\n### settled renders, re-synced RTL22, floor-subtracted (burst - silence) ###")
    hdr = (f"{'id':>3} {'name':13} {'documented':30} {'xov':>4} "
           f"{'chA LF/mid/bb':>17} {'chC LF/mid/bb':>17}  verdict")
    print(hdr)
    print("-" * len(hdr))
    rows_out = []
    for pid in IDS:
        rec = cache[str(pid)]
        nm = name_of(pid, names)
        kind, docval, xov, doclbl = DOC.get(pid, (None, None, 720.0, "-"))
        if not rec.get("ok"):
            print(f"{pid:>3} {nm:13} {doclbl:30} <capture not ok — skipped>")
            continue
        b = bytes.fromhex(rec["wcs"])
        try:
            rows, L, w_reset = program_rows22([(b[4*k], b[4*k+1], b[4*k+2], b[4*k+3])
                                               for k in range(128)])
        except Exception as e:
            print(f"{pid:>3} {nm:13} {doclbl:30} EXTRACT-FAIL {e}")
            continue
        fs = fs22(L)
        dur = 6.5 if pid == 1 else 4.5
        n = int(dur * fs)
        nb = int(0.30 * fs)
        exc = np.zeros(n, dtype=np.int64)
        exc[:nb] = np.random.default_rng(224).integers(-8000, 8001, nb)
        t0 = time.time()
        sil = RTL22().run_free(rows, [0] * n, n)
        bur = RTL22().run_free(rows, [int(v) for v in exc], n)
        meas = {}
        for c in "AC":
            out16 = np.clip(np.asarray(bur[c]), -32768, 32767).astype(np.int16)
            RM.analyze(out16, exc.astype(np.int16), fs, f"f4d_id{pid:02d}_ch{c}",
                       out_dir=RENDERS, burst_end_s=0.30)
            d = np.asarray(bur[c], np.float64) - np.asarray(sil[c], np.float64)
            tail = d[nb:]
            lf = rt(sosfiltfilt(butter(4, xov / (fs / 2), "lowpass", output="sos"),
                                tail), fs)
            hi = rt(sosfiltfilt(butter(4, xov / (fs / 2), "highpass", output="sos"),
                                tail), fs)
            bb = rt(tail, fs)
            meas[c] = (lf, hi, bb)

        verdict = "—"
        if kind == "bands":
            marks = []
            for c in "AC":
                for want, got in zip(docval, meas[c][:2]):
                    marks.append(got is not None and abs(got - want) <= TOL * want)
            verdict = "PASS" if all(marks) else "FAIL"
        elif kind == "bb":
            marks = [meas[c][2] is not None and abs(meas[c][2] - docval) <= TOL * docval
                     for c in "AC"]
            verdict = "PASS" if all(marks) else "FAIL"
        rows_out.append((pid, nm, doclbl, xov, meas, verdict))
        print(f"{pid:>3} {nm:13} {doclbl:30} {int(xov):>4} "
              f"{fmt3(meas['A']):>17} {fmt3(meas['C']):>17}  {verdict}"
              f"   ({time.time()-t0:.0f}s)", flush=True)

    print("\nnotes:")
    print(" - names from program_names.json (bit-coded record ids; 0x03 = SMALL PLATE,")
    print("   0x04 = ROOM — registry #34);  * = record-map name (not reached by the")
    print("   LARC B/P key enumeration)")
    print(" - id 2 PLATE: the documented 0.6/1.8 @170 row is labeled 'Plate V2' in ch.4;")
    print("   the cached settled image is the boot-recalled variation (display V1) —")
    print("   scored as instructed, caveat stands")
    print(" - verdicts: both channels within +-20% of every documented number; static")
    print("   settled images carry the frozen-LFO spread (+-0.2-0.3 s, 0024/0027)")
    print(f" - WAVs -> {RENDERS}\\f4d_id*_ch*.wav")


if __name__ == "__main__":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass
    main()
