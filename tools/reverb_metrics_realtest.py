#!/usr/bin/env python3
"""Validate tools/reverb_metrics.py against a REAL reverb algorithm (not synthetic decaying noise).

The selftest battery uses an ideal exp-decay-noise IR (known RT60) to calibrate estimator ACCURACY.
This adds the harder question: does the metric hold up on an actual reverberator with real features —
comb coloration, allpass diffusion, dense early→late buildup, and (damped variant) frequency-dependent
decay? Reverb = a Schroeder–Moorer / Freeverb network (8 parallel feedback combs + 4 series allpass),
whose broadband RT60 is set analytically by the comb feedback gains, so we still have a known target.

Run:  python tools/reverb_metrics_realtest.py
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
sys.stdout.reconfigure(encoding="utf-8")
import numpy as np

import stimulus as S
import reverb_metrics as RM

FS = 34130
SCR = (r"C:/Users/Skylar/AppData/Local/Temp/claude/"
       r"d--OneDrive-Gray-Instruments-iconex/ae30a9a1-b02b-4706-a6d3-7d89d4cefad3/scratchpad/renders")

# Freeverb tunings (44.1 kHz) scaled to FS.
_SC = FS / 44100.0
COMB_D = [int(round(d * _SC)) for d in (1116, 1188, 1277, 1356, 1422, 1491, 1557, 1617)]
ALLP_D = [int(round(d * _SC)) for d in (556, 441, 341, 225)]


def _feedback_comb(x, D, g, damp=0.0):
    """y[n] = x[n] + g*((1-damp)*y[n-D] + damp*lp), lowpass-damped feedback (Freeverb comb)."""
    y = np.zeros(len(x))
    buf = np.zeros(D)
    lp = 0.0
    idx = 0
    for n in range(len(x)):
        yn = buf[idx]
        lp = yn * (1.0 - damp) + lp * damp
        buf[idx] = x[n] + g * lp
        y[n] = yn
        idx += 1
        if idx == D:
            idx = 0
    return y


def _allpass(x, D, g=0.5):
    y = np.zeros(len(x))
    buf = np.zeros(D)
    idx = 0
    for n in range(len(x)):
        bufout = buf[idx]
        yn = -x[n] + bufout
        buf[idx] = x[n] + g * bufout
        y[n] = yn
        idx += 1
        if idx == D:
            idx = 0
    return y


def schroeder_reverb(x, rt60_s, fs=FS, damp=0.0):
    """Real reverberator: 8 parallel damped feedback combs (each tuned to rt60_s) + 4 series allpass."""
    x = x.astype(np.float64)
    acc = np.zeros(len(x))
    for D in COMB_D:
        g = 10.0 ** (-3.0 * D / (fs * rt60_s))      # comb RT60 = -3D/(fs·log10 g)  -> g for target
        acc += _feedback_comb(x, D, g, damp)
    acc /= len(COMB_D)
    for D in ALLP_D:
        acc = _allpass(acc, D)
    return acc


def _to_i16(x, level_dbfs=-3.0):
    x = x / (np.max(np.abs(x)) + 1e-12) * S.dbfs_to_amp(level_dbfs)
    return np.clip(np.round(x), -32768, 32767).astype(np.int16)


def main():
    os.makedirs(SCR, exist_ok=True)
    print("### reverb_metrics validated on a REAL reverb (Freeverb / Schroeder–Moorer) ###\n")
    results = []

    def check(name, cond, detail):
        results.append(bool(cond))
        print(f"  [{'PASS' if cond else 'FAIL'}] {name}: {detail}")

    # A: impulse -> reverb, undamped, design RT60 = 2.0 s -> WET-PASS/DENSE, RT60 within ±20%, broadband
    for rt in (1.0, 2.0, 3.0):
        n = int(max(1.6 * rt, rt + 0.6) * FS)
        exc = S.unit_impulse(-3.0, n, FS)
        wet = schroeder_reverb(exc, rt, damp=0.0)
        out = _to_i16(wet)
        v = RM.analyze(out, exc, FS, f"real_freeverb_rt{rt}", out_dir=SCR)
        err = (abs(v["rt60_s"] - rt) / rt * 100) if v["rt60_s"] else float("nan")
        check(f"impulse→Freeverb RT60={rt}s → WET-PASS/DENSE, RT60 within ±20%",
              v["verdict"] == "WET-PASS" and v["density"] == "DENSE"
              and v["rt60_s"] and abs(v["rt60_s"] - rt) / rt <= 0.20,
              f"verdict={v['verdict']} density={v['density']} rt60={v['rt60_s']} err={err:.1f}% "
              f"sfm={v.get('spectral_flatness')} ned={v['ned_max']:.2f}")

    # B: noise burst -> reverb -> WET-PASS/DENSE (a different excitation)
    nb = S.noise_burst(0.30, 3.5, FS, seed=0x1234)
    wet = schroeder_reverb(nb, 2.0, damp=0.0)
    out = _to_i16(wet)
    v = RM.analyze(out, nb, FS, "real_freeverb_burst", out_dir=SCR, burst_end_s=0.30)
    check("burst→Freeverb RT60=2.0s → WET (dense)",
          v["verdict"] in ("WET-PASS",) and v["density"] == "DENSE",
          f"verdict={v['verdict']} density={v['density']} rt60={v['rt60_s']}")

    # C: damped (frequency-dependent decay) -> still WET-PASS/DENSE, plausible RT60
    n = int(3.5 * FS)
    exc = S.unit_impulse(-3.0, n, FS)
    wet = schroeder_reverb(exc, 2.5, damp=0.4)
    out = _to_i16(wet)
    v = RM.analyze(out, exc, FS, "real_freeverb_damped", out_dir=SCR)
    check("impulse→Freeverb damped → WET-PASS/DENSE, plausible RT60",
          v["verdict"] == "WET-PASS" and v["density"] == "DENSE" and v["rt60_s"] and 0.3 < v["rt60_s"] < 4.0,
          f"verdict={v['verdict']} density={v['density']} rt60={v['rt60_s']} sfm={v.get('spectral_flatness')}")

    # D: REAL reverb available but mixed 0% wet (pure dry) -> DRY (the safety case)
    n = int(2.0 * FS)
    exc = S.unit_impulse(-3.0, n, FS)
    out = exc.copy()                                  # 0% wet
    v = RM.analyze(out, exc, FS, "real_freeverb_drymix", out_dir=SCR)
    check("impulse, 0% wet (reverb bypassed) → DRY",
          v["verdict"] == "DRY", f"verdict={v['verdict']} wetness={v['wetness']:.4f}")

    # E: 30% wet / 70% dry mix -> WET (not falsely DRY); a real partial-wet send
    n = int(3.0 * FS)
    exc = S.unit_impulse(-3.0, n, FS)
    wet = schroeder_reverb(exc, 2.0, damp=0.2)
    mix = 0.30 * wet / (np.max(np.abs(wet)) + 1e-12) + 0.70 * exc.astype(np.float64) / (np.max(np.abs(exc)) + 1e-12)
    out = _to_i16(mix)
    v = RM.analyze(out, exc, FS, "real_freeverb_mix30", out_dir=SCR)
    check("impulse, 30% wet mix → WET (is_wet, not DRY)",
          v["is_wet"] and v["verdict"] != "DRY",
          f"verdict={v['verdict']} is_wet={v['is_wet']} density={v['density']} rt60={v['rt60_s']}")

    print(f"\n{'=' * 64}\nREAL-REVERB VALIDATION: {sum(results)}/{len(results)} passed")
    print("=" * 64)
    return all(results)


if __name__ == "__main__":
    sys.exit(0 if main() else 1)
