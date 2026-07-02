#!/usr/bin/env python3
"""D2c (plan 022) — cross-program documented-decay check on SETTLED images + the D0 anomalies.

D2a lesson applied bank-wide: the e1/D0 renders used MAINLOOP-snapshot (pre-apply) images.
Here every D0-covered selector id is re-captured AFTER the de-zipper settles (+6M ticks),
the LARC display NAME is read from the firmware itself (0x3F8E display image), and the
render verdicts are scored against what ch.4 says each program IS (variation 1):

  selector (dec) -> record: 1=CONCERT HALL(2.6s avg) 2=PLATE(1.8s) 5=DARK HALL 6=HALL/HALL
  8=CHAMBER 10=PLATE/PLATE 12=CHORUS&ECHO(effect) 16=CD PLATE B(1.8s) 17=RICH PLATE
  18=PLATE/HALL 20=RES CHORDS(effect); 3 and 4 have NO record with that first byte in the
  0xB800 array (record map) — the display name shows what the firmware actually loads.

Anomaly classification target (plan): (a) documented behavior, (b) capture-point artifact,
(c) needs-modulation (D4), (d) genuine engine discrepancy.
"""
import sys, os, json, time

TOOLS = r"d:\OneDrive\Gray Instruments\iconex\tools"
sys.path.insert(0, TOOLS)
HERE = os.path.dirname(os.path.abspath(__file__))
RENDERS = os.path.join(HERE, "renders")
CACHE = os.path.join(HERE, "wcs_settled_all.json")

import numpy as np
import boot8080
import reverb_metrics as RM
from aru_freerun22_rtl import RTL22, program_rows22, fs22

IDS = [1, 2, 3, 4, 5, 6, 8, 10, 12, 16, 17, 18, 20]
DOC = {1: ("CONCERT HALL", "avg 2.6 s (LF 3.0/mid 2.0)"),
       2: ("PLATE", "avg 1.8 s (var1)"),
       3: ("<no 0x03 record>", "invalid selector?"),
       4: ("<no 0x04 record>", "SMALL PLATE? (name missing from record map)"),
       5: ("DARK HALL", "hall-family reverb"),
       6: ("HALL/HALL", "split: two independent halls"),
       8: ("CHAMBER", "reverb (1 variation; SIZE-based)"),
       10: ("PLATE/PLATE", "split: two plates"),
       12: ("CHORUS&ECHO", "EFFECT — chorus+echo, modulation-driven"),
       16: ("CD PLATE B", "avg 1.8 s (var1)"),
       17: ("RICH PLATE", "dense plate reverb"),
       18: ("PLATE/HALL", "split: plate + hall"),
       20: ("RES CHORDS", "EFFECT — tuned resonators")}

ORIG_LOAD = boot8080.load_mem


def ascii7(b):
    return "".join(chr(x & 0x7F) if 0x20 <= (x & 0x7F) < 0x7F else "." for x in b)


def capture(pid):
    def patched():
        mem = ORIG_LOAD()
        assert bytes(mem[0x8160:0x8163]) == b"\x3a\x00\xb8"
        mem[0x8160:0x8163] = bytes([0x3E, pid & 0xFF, 0x00])
        return mem
    boot8080.load_mem = patched
    try:
        m, ms = boot8080.boot(verbose=False, extra_ticks_after_mainloop=6_000_000)
        ok = "mainloop" in ms and "prog_load" in ms
        name = ascii7(m.memory[0x3F8E:0x3F9A]).strip(". ")
        return dict(ok=ok, wcs=bytes(m.memory[0x4000:0x4200]).hex(), name=name)
    finally:
        boot8080.load_mem = ORIG_LOAD


cache = json.load(open(CACHE)) if os.path.exists(CACHE) else {}
for pid in IDS:
    if str(pid) in cache:
        continue
    print(f"[id {pid:2d}] booting + settling ...", flush=True)
    try:
        cache[str(pid)] = capture(pid)
        print(f"   name='{cache[str(pid)]['name']}'")
    except Exception as e:
        cache[str(pid)] = dict(ok=False, error=repr(e))
        print(f"   EXCEPTION {e!r}")
    json.dump(cache, open(CACHE, "w"))

print("\n### settled cross-program renders (burst, floor-subtracted, chA) ###")
print(f"{'id':>3} {'display name':14} {'doc':32} {'verdict':14} {'RT60':>6}  {'peak':>6}")
rng_seed = 224
for pid in IDS:
    rec = cache[str(pid)]
    if not rec.get("ok"):
        print(f"{pid:>3} {'<no build>':14} {DOC[pid][1]:32} -")
        continue
    b = bytes.fromhex(rec["wcs"])
    try:
        rows, L, w_reset = program_rows22([(b[4*k], b[4*k+1], b[4*k+2], b[4*k+3])
                                           for k in range(128)])
    except Exception as e:
        print(f"{pid:>3} {rec['name']:14} {DOC[pid][1]:32} EXTRACT-FAIL {e}")
        continue
    fs = fs22(L)
    n = int(4.5 * fs)
    nb = int(0.30 * fs)
    exc = np.zeros(n, dtype=np.int64)
    exc[:nb] = np.random.default_rng(rng_seed).integers(-8000, 8001, nb)
    sil = RTL22().run_free(rows, [0] * n, n)
    bur = RTL22().run_free(rows, list(int(v) for v in exc), n)
    out = np.asarray(bur["A"], np.int16)
    v = RM.analyze(out, exc.astype(np.int16), fs, f"d2c_id{pid:02d}_chA",
                   out_dir=RENDERS, burst_end_s=0.30)
    d = np.asarray(bur["A"], np.float64) - np.asarray(sil["A"], np.float64)
    t = RM._noise_floor_truncate(d[nb:], fs)
    rt, r2, npts = RM._fit_decay(RM._schroeder_db(t), fs, -5.0, -35.0)
    if rt is None:
        rt, r2, npts = RM._fit_decay(RM._schroeder_db(t), fs, -5.0, -25.0)
    pk = int(np.max(np.abs(out)))
    print(f"{pid:>3} {rec['name']:14} {DOC[pid][1]:32} "
          f"{str(v.get('verdict')) + '/' + str(v.get('density')):14} "
          f"{rt if rt else float('nan'):>6.2f} {pk:>6}")
print("\n(D0 boot-image verdicts for contrast: 8 near-silent, 3 FAIL, 12/20 indeterminate)")
