#!/usr/bin/env python3
"""D2b (plan 022) — the DOCUMENTED-DEFAULTS oracle. NO parameter tweaking anywhere.

Concert Hall Variation 1 (the power-up preset) is documented (224X ch.4/ch.8):
  LF Decay 3.0 s / Mid Decay 2.0 s / Crossover 720 Hz / Treble Decay 6.30 kHz /
  Depth 33 / Predelay 24.0 ms; HF Bandwidth 9.00 kHz; Diffusion 25; preechoes 00;
  "average running reverb decay time is 2.6 seconds"; stereo outputs A=left, C=right.

Method (per plan §7, comparisons are PER-BAND at the documented crossover):
  octave-band (125..8k) + two-band (720 Hz split) RT60, block-RMS slope fit on the
  floor-subtracted burst tail (c3/c5 convention). The method is FIRST validated on the
  benchmark IR `IR/Lexicon 224XL/Concert Hall V1.1.L.wav` — a real 224XL at these same
  documented presets: if the method reproduces the documented numbers there, a model
  mismatch is a real finding (capture point / engine), not band-measurement error.

Images rendered (the D2a capture-point result):
  settled = wcs_settled_concert.json (fresh, de-zipper quiescent — THE default state)
  run40M  = wcs_run_concert.json     (same state, different frozen LFO phase)
  boot    = wcs_cache.json id 1      (mainloop snapshot, PRE-apply — for contrast)
"""
import sys, os, json

TOOLS = r"d:\OneDrive\Gray Instruments\iconex\tools"
sys.path.insert(0, TOOLS)
HERE = os.path.dirname(os.path.abspath(__file__))
RENDERS = os.path.join(HERE, "renders")
os.makedirs(RENDERS, exist_ok=True)

import numpy as np
from scipy.signal import butter, sosfiltfilt
import reverb_metrics as RM
import reverb_metrics_selftest as RMS
from aru_freerun22_rtl import RTL22, program_rows22, fs22

print("### metric calibration battery ###")
assert RMS.run_battery(out_dir=RENDERS, verbose=False), "metric battery FAILED"
print("  all controls classified correctly — metric TRUSTED\n")

DOC = {"LF": 3.0, "mid": 2.0, "avg": 2.6, "xov": 720.0, "predelay_ms": 24.0}
OCT = [125, 250, 500, 1000, 2000, 4000, 8000]


# ------------------------------------------------------------------ measurement
def band(x, fs, kind, f0, f1=None):
    ny = fs / 2
    if kind == "low":
        sos = butter(4, f0 / ny, "lowpass", output="sos")
    elif kind == "high":
        sos = butter(4, f0 / ny, "highpass", output="sos")
    else:
        sos = butter(4, [f0 / ny, min(f1 / ny, 0.98)], "bandpass", output="sos")
    return sosfiltfilt(sos, x)


def rt60_band(tail, fs, lo_db=-5.0, hi_db=-35.0):
    """Schroeder T30 on the noise-truncated tail (reverb_metrics' calibrated primitives:
    Lundeby-lite knee cut -> backward-integrated EDC -> -5..-35 dB fit; T20 fallback)."""
    t = RM._noise_floor_truncate(np.asarray(tail, np.float64), fs)
    edc = RM._schroeder_db(t)
    rt, r2, npts = RM._fit_decay(edc, fs, lo_db, hi_db)
    rng = (lo_db, hi_db)
    if rt is None:
        rt, r2, npts = RM._fit_decay(edc, fs, -5.0, -25.0)
        rng = (-5.0, -25.0)
    return dict(rt60=rt, r2=r2, npts=npts, rng=rng) if rt else None


def band_table(tail, fs):
    """Octave-band + two-band RT60s of a decay tail (float array starting at decay onset)."""
    out = {}
    for c in OCT:
        f0, f1 = c / 2 ** 0.5, c * 2 ** 0.5
        if f1 >= fs / 2 * 0.98:
            continue
        out[f"{c}Hz"] = rt60_band(band(tail, fs, "band", f0, f1), fs)
    out["LF(<720)"] = rt60_band(band(tail, fs, "low", DOC["xov"]), fs)
    out["mid(>720)"] = rt60_band(band(tail, fs, "high", DOC["xov"]), fs)
    out["broadband"] = rt60_band(tail, fs)
    return out


def show(tag, tab):
    cells = []
    for k in list(f"{c}Hz" for c in OCT) + ["LF(<720)", "mid(>720)", "broadband"]:
        r = tab.get(k)
        cells.append(f"{k}={r['rt60']:4.2f}" if r else f"{k}= -- ")
    print(f"  {tag:14} " + " ".join(cells))


# ------------------------------------------------------------------ benchmark IR first
print("### method validation on the benchmark IR (real unit, documented presets) ###")
import soundfile as sf
ir_path = os.path.join(os.path.dirname(TOOLS), "IR", "Lexicon 224XL", "Concert Hall V1.1.L.wav")
ir, ir_fs = sf.read(ir_path)
if ir.ndim > 1:
    ir = ir[:, 0]
pk = int(np.argmax(np.abs(ir)))
print(f"  {os.path.basename(ir_path)}: fs={ir_fs}, {len(ir)/ir_fs:.2f} s, peak at {pk/ir_fs*1000:.1f} ms")
ir_tab = band_table(ir[pk:].astype(np.float64), ir_fs)
show("benchmark", ir_tab)
bm = {k: (ir_tab[k]["rt60"] if ir_tab.get(k) else None) for k in ("LF(<720)", "mid(>720)", "broadband")}
print(f"  documented: LF 3.0 / mid 2.0 / avg 2.6  ->  benchmark measures "
      f"LF {bm['LF(<720)']:.2f} / mid {bm['mid(>720)']:.2f} / broadband {bm['broadband']:.2f}")
meth_ok = (bm["LF(<720)"] and abs(bm["LF(<720)"] - DOC["LF"]) / DOC["LF"] < 0.25 and
           bm["mid(>720)"] and abs(bm["mid(>720)"] - DOC["mid"]) / DOC["mid"] < 0.25)
print(f"  METHOD {'VALIDATED (bands reproduce the documented values on the real unit)' if meth_ok else 'QUESTIONABLE — investigate before trusting model comparisons'}\n")

# ------------------------------------------------------------------ model renders
def load_rows(path, key=None):
    rec = json.load(open(path))
    b = bytes.fromhex((rec[key] if key else rec)["wcs"])
    return program_rows22([(b[4 * k], b[4 * k + 1], b[4 * k + 2], b[4 * k + 3])
                           for k in range(128)])


IMAGES = [("settled", None, os.path.join(HERE, "wcs_settled_concert.json")),
          ("run40M", None, os.path.join(HERE, "wcs_run_concert.json")),
          ("boot", "1", os.path.join(HERE, "wcs_cache.json"))]

REN_S = 6.5
BURST_S = 0.30
rng = np.random.default_rng(224)

model = {}
for tag, key, path in IMAGES:
    rows, L, w_reset = load_rows(path, key)
    fs = fs22(L)
    n = int(REN_S * fs)
    nb = int(BURST_S * fs)
    exc = np.zeros(n, dtype=np.int64)
    exc[:nb] = np.random.default_rng(224).integers(-8000, 8001, nb)
    sil = RTL22().run_free(rows, [0] * n, n)
    bur = RTL22().run_free(rows, list(int(v) for v in exc), n)
    print(f"### {tag} (L={L}, fs={fs:.0f} Hz) — burst 0.30 s, floor-subtracted, per-band ###")
    model[tag] = {}
    for c in "AC":
        d = np.asarray(bur[c], np.float64) - np.asarray(sil[c], np.float64)
        model[tag][c] = band_table(d[nb:], fs)
        show(f"ch{c}", model[tag][c])
        RM.write_wav(RENDERS, f"d2_{tag}_burst_ch{c}", np.clip(bur[c], -32768, 32767).astype(np.int16), int(fs))
    # headline metric verdict on the raw burst render (battery already asserted)
    v = RM.analyze(np.asarray(bur["A"], np.int16), exc.astype(np.int16), fs,
                   f"d2_{tag}_chA", out_dir=RENDERS, burst_end_s=BURST_S)
    print(f"  chA metric verdict: {v.get('verdict')} density={v.get('density')} "
          f"rt60={v.get('rt60')}\n")

# ------------------------------------------------------------------ predelay (settled)
print("### predelay (settled image, impulse, floor-subtracted) ###")
rows, L, w_reset = load_rows(os.path.join(HERE, "wcs_settled_concert.json"))
fs = fs22(L)
T0 = 2000
n = T0 + int(1.2 * fs)
sil = RTL22().run_free(rows, [0] * n, n)
imp_in = [0] * n
imp_in[T0] = 16000
imp = RTL22().run_free(rows, imp_in, n)
for c in "AC":
    d = np.asarray(imp[c], np.float64) - np.asarray(sil[c], np.float64)
    seg = d[T0:]
    pre_rms = float(np.sqrt(np.mean(d[:T0] ** 2))) if np.any(d[:T0]) else 0.5
    th = max(6 * pre_rms, 0.02 * np.max(np.abs(seg)))
    first = int(np.argmax(np.abs(seg) > th))
    # main arrival = first block where the 2ms envelope reaches 25% of its max
    blk = max(4, int(0.002 * fs))
    env = np.sqrt([np.mean(seg[i * blk:(i + 1) * blk] ** 2) for i in range(min(60, len(seg) // blk))])
    main = int(np.argmax(env > 0.25 * env.max())) * blk
    print(f"  ch{c}: first arrival {first / fs * 1000:6.2f} ms; main arrival {main / fs * 1000:6.2f} ms "
          f"(documented Predelay 24.0 ms; fine predelays 0.36/10.2 ms)")

# ------------------------------------------------------------------ verdict
print("\n### D2b verdict (documented values, NO tweaking) ###")
print(f"{'':14}{'LF(<720)':>10}{'mid(>720)':>11}{'broadband':>11}")
print(f"{'documented':14}{DOC['LF']:>10.2f}{DOC['mid']:>11.2f}{DOC['avg']:>11.2f}")
print(f"{'benchmark IR':14}{bm['LF(<720)']:>10.2f}{bm['mid(>720)']:>11.2f}{bm['broadband']:>11.2f}")
for tag in ("settled", "run40M", "boot"):
    for c in "AC":
        t = model[tag][c]
        vals = [t[k]["rt60"] if t.get(k) else float("nan") for k in ("LF(<720)", "mid(>720)", "broadband")]
        print(f"{tag + ' ch' + c:14}{vals[0]:>10.2f}{vals[1]:>11.2f}{vals[2]:>11.2f}")

ok = True
for c in "AC":
    t = model["settled"][c]
    for k, doc in (("LF(<720)", DOC["LF"]), ("mid(>720)", DOC["mid"])):
        r = t.get(k)
        good = r and abs(r["rt60"] - doc) / doc <= 0.20
        ok &= bool(good)
        print(f"  {'PASS' if good else 'FAIL'}  settled ch{c} {k}: "
              f"{r['rt60'] if r else float('nan'):.2f} s vs documented {doc:.1f} s")
print(f"\nD2b: {'DOCUMENTED DEFAULTS REPRODUCED' if ok else 'MISMATCH — a model/capture-point finding to diagnose (do NOT fit it away)'}")
