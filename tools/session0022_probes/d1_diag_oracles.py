#!/usr/bin/env python3
"""D1c (plan 022) — the firmware's own known-answer delay oracles, end-to-end.

The SM (ch.5) fully specifies diag programs 7/8: "Left input passes to outputs A and D,
and Right input passes to outputs B and C"; program 8 interposes ~0.5 s of DMEM delay,
program 7 none. The firmware BUILT the WCS (d1a_capture_diag.py, verified core); the RTL
engine RUNS it (program_rows22 + RTL22 — no byte interpretation anywhere in between).

Runs (per program, per plan §7 both polarities):
  half-1-only stimulus (tuple (x,0)) and half-2-only ((0,x));
  impulse run  -> exact frame lag, peak gain, polarity per channel;
  burst run    -> RMS channel separation (>40 dB) + through-gain, WAVs to renders/.

The L/R <-> half binding is CLOSED here, not assumed: the engine only knows "first RD-AD
read in execution order = half-1". The SM says LEFT -> A,D. Whichever half feeds A,D is
therefore the LEFT input. Expected mechanically (from the captured bytes): word 127
(exec row 0, half-1) chains to the A,D output word 124 (row 3) => half-1 = LEFT.

Expected lags from the captured offsets (read - write): MAX 0x7FFF-0x4000 = 0x3FFF and
0x3FFF-0 = 0x3FFF => 16383 frames = 0.4800 s @ fs 34,133 Hz (the SM's "0.5 s", rounded);
ZERO 0x4001-0x4000 = 1 and 0x0001-0 = 1 => one frame = 29 us ("0 seconds").
"""
import sys, os, json, wave

TOOLS = r"d:\OneDrive\Gray Instruments\iconex\tools"
sys.path.insert(0, TOOLS)
HERE = os.path.dirname(os.path.abspath(__file__))
RENDERS = os.path.join(HERE, "renders")
os.makedirs(RENDERS, exist_ok=True)

import numpy as np
from aru_freerun22_rtl import RTL22, program_rows22, fs22

# ---------------------------------------------------------------- POST green (plan §7)
print("### POST (untouched single-step path) ###")
import aru_post
verdict, diag_errors, _aru = aru_post.run_post(verbose=False)
subs = {k: v for k, v in verdict.items() if "(E" in k and "reached" not in k}
for k in sorted(subs):
    print(f"  {k:34}: {subs[k]}")
assert len(subs) == 4 and all(v == "PASS" for v in subs.values()) and not diag_errors, \
    f"POST NOT GREEN: {subs} diag_errors={diag_errors}"
assert verdict.get("_reached_mainloop"), "POST: mainloop not reached"
print("  POST GREEN (E32/E40/E83/E91), mainloop reached\n")

# ---------------------------------------------------------------- programs
cache = json.load(open(os.path.join(HERE, "wcs_diag.json")))
progs = {}
for name in ("zero", "max"):
    b = bytes.fromhex(cache[name]["wcs"])
    rows, L, w_reset = program_rows22([(b[4*k], b[4*k+1], b[4*k+2], b[4*k+3])
                                       for k in range(128)])
    assert (L, w_reset) == (99, 29) and len(rows) == 100, (name, L, w_reset)
    progs[name] = rows
fs = fs22(99)
print(f"programs: zero + max, L=99, 100-step frame, fs = {fs:.1f} Hz\n")

EXPECT_LAG = {"zero": 1, "max": 0x3FFF}


def write_wav(path, x, fs_hz):
    with wave.open(path, "wb") as w:
        w.setnchannels(1)
        w.setsampwidth(2)
        w.setframerate(int(round(fs_hz)))
        w.writeframes(np.asarray(x, dtype="<i2").tobytes())


def run(rows, sig, n):
    return RTL22().run_free(rows, sig, n)


def stereo(mono, side):
    """mono int array -> list of (h1, h2) tuples with only one half driven."""
    z = np.zeros_like(mono)
    h1, h2 = (mono, z) if side == "h1" else (z, mono)
    return list(zip((int(v) for v in h1), (int(v) for v in h2)))


results = {}
for name in ("zero", "max"):
    rows = progs[name]
    lag_exp = EXPECT_LAG[name]
    for side in ("h1", "h2"):
        tag = f"{name}-{side}only"

        # ---- impulse: exact lag / gain / polarity ----
        AMP, T0 = 16000, 50
        Ni = T0 + lag_exp + 600
        imp = np.zeros(Ni, dtype=np.int64)
        imp[T0] = AMP
        ch = run(rows, stereo(imp, side), Ni)
        lagrow = {}
        for c in "ABCD":
            out = np.asarray(ch[c], dtype=np.int64)
            pk = int(np.argmax(np.abs(out)))
            lagrow[c] = (pk - T0, int(out[pk]))

        # ---- burst: separation + through-gain; WAVs ----
        BURST_S = 0.25
        nb = int(BURST_S * fs)
        Nb = lag_exp + nb + 2000
        rng = np.random.default_rng(224)
        bur = np.zeros(Nb, dtype=np.int64)
        bur[:nb] = rng.integers(-8000, 8001, nb)
        chb = run(rows, stereo(bur, side), Nb)
        w0, w1 = lag_exp, lag_exp + nb                    # the delayed-burst window
        rms = {c: float(np.sqrt(np.mean(np.asarray(chb[c][w0:w1], dtype=np.float64) ** 2)))
               for c in "ABCD"}
        in_rms = float(np.sqrt(np.mean(bur[:nb].astype(np.float64) ** 2)))
        for c in "ABCD":
            write_wav(os.path.join(RENDERS, f"d1_{tag}_ch{c}.wav"),
                      np.clip(chb[c], -32768, 32767), fs)

        live = sorted(c for c in "ABCD" if rms[c] > in_rms * 0.25)
        dead = sorted(set("ABCD") - set(live))
        sep_db = 20 * np.log10(min(rms[c] for c in live) / max(max(rms[c] for c in dead), 1e-9))
        gain = {c: rms[c] / in_rms for c in live}
        results[tag] = dict(live=live, dead=dead, sep_db=sep_db, gain=gain,
                            lags={c: lagrow[c] for c in live},
                            dead_peak={c: lagrow[c][1] for c in dead})

        print(f"[{tag}] live={live} dead={dead}")
        for c in live:
            lg, pv = lagrow[c]
            print(f"   ch{c}: lag={lg} frames ({lg / fs * 1000:.2f} ms), peak={pv:+d} "
                  f"(gain {pv / AMP:+.3f}), burst gain {gain[c]:.3f}")
        print(f"   separation (min live / max dead RMS): {sep_db:.1f} dB; "
              f"dead peaks {[results[tag]['dead_peak'][c] for c in dead]}")

# ---------------------------------------------------------------- the known answers
print("\n### SM ch.5 known answers ###")
ok = True

def check(cond, msg):
    global ok
    print(f"  {'PASS' if cond else 'FAIL'}  {msg}")
    ok &= bool(cond)

for name in ("zero", "max"):
    lag_exp = EXPECT_LAG[name]
    r1, r2 = results[f"{name}-h1only"], results[f"{name}-h2only"]
    check(r1["live"] == ["A", "D"], f"{name}: half-1 input -> outputs A,D (SM: Left -> A,D)")
    check(r2["live"] == ["B", "C"], f"{name}: half-2 input -> outputs B,C (SM: Right -> B,C)")
    for r, side in ((r1, "h1"), (r2, "h2")):
        check(all(lg == lag_exp for lg, _ in r["lags"].values()),
              f"{name}-{side}: exact lag {lag_exp} frames on both live channels "
              f"({lag_exp / fs:.4f} s)")
        check(all(0.9 <= abs(pv) / 16000 <= 1.1 for _, pv in r["lags"].values()),
              f"{name}-{side}: through-gain ~1.0 (impulse peaks "
              f"{[pv for _, pv in r['lags'].values()]})")
        check(r["sep_db"] > 40, f"{name}-{side}: channel separation {r['sep_db']:.1f} dB > 40")

print(f"\nD1 ORACLE: {'CLOSED — build -> decode -> engine -> I/O all reproduce the SM' if ok else 'FAILED'}")
print("binding pinned by the SM answer: half-1 (first RD-AD read in execution order) = LEFT")
print(f"MAX delay measured {EXPECT_LAG['max']} frames = {EXPECT_LAG['max'] / fs:.4f} s "
      f"(SM '0.5 s'; = read-write offset 0x3FFF exactly)")
sys.exit(0 if ok else 1)
