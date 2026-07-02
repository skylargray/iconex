#!/usr/bin/env python3
"""Self-calibration battery for tools/reverb_metrics.py (plan 020, AC0-M).

The metric is trusted ONLY if it classifies signals whose answer is KNOWN. These controls are the
executable spec: each is a synthetic signal with a pre-registered required verdict. If any control
misclassifies, the metric is broken and must NOT be used to judge CONCERT. Real CONCERT runs import
`run_battery()` and assert it passes in the SAME process before reporting any number.

Required classifications (plan 020 § Metric):
  dry impulse (click)            -> DRY
  dry passthrough of noise burst -> DRY
  single delay x+0.5·x[n-D]      -> WET but SPARSE, RT60 INDETERMINATE
  exp-decay noise reverb         -> WET-PASS, DENSE, RT60 within ±15% of {0.8, 2.6, 5.0}s
  growing feedback (gain>1)      -> FAIL (over-unity)
  silence                        -> INDETERMINATE (empty)
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


# ---- synthetic TEST FIXTURES (known answers; not the production stimulus) ----
def _rng(seed):
    return np.random.default_rng(seed)


def fixture_single_echo(level_dbfs=-6.0, delay_s=0.20, total_s=1.0, g=0.5):
    n = int(total_s * FS)
    exc = S.unit_impulse(level_dbfs, n, FS)
    out = exc.astype(np.float64).copy()
    d = int(delay_s * FS)
    out[d:] += g * exc.astype(np.float64)[:n - d]
    return np.clip(np.round(out), -32768, 32767).astype(np.int16), exc


def fixture_reverb(rt60_s, level_dbfs=-1.0, total_s=None, seed=7):
    total_s = total_s if total_s else max(1.2 * rt60_s, rt60_s + 0.5)
    n = int(total_s * FS)
    t = np.arange(n) / FS
    env = np.exp(-t * (3.0 * np.log(10.0)) / rt60_s)        # amplitude -60 dB at t=rt60
    noise = _rng(seed).standard_normal(n)
    amp = S.dbfs_to_amp(level_dbfs)
    h = noise * env
    h = h / (np.max(np.abs(h)) + 1e-12) * amp
    out = np.clip(np.round(h), -32768, 32767).astype(np.int16)
    exc = S.unit_impulse(level_dbfs, n, FS)                  # impulse excitation
    return out, exc


def fixture_growing(level_dbfs=-20.0, total_s=1.0, rt_grow=0.6, seed=3):
    n = int(total_s * FS)
    t = np.arange(n) / FS
    env = np.exp(+t * (3.0 * np.log(10.0)) / rt_grow)        # GROWS 60 dB per rt_grow
    noise = _rng(seed).standard_normal(n)
    h = noise * env
    h = h / (np.max(np.abs(h)) + 1e-12) * 32000.0            # rails at full scale (over-unity)
    out = np.clip(np.round(h), -32768, 32767).astype(np.int16)
    exc = S.unit_impulse(level_dbfs, n, FS)
    return out, exc


def fixture_dry_impulse(level_dbfs=-6.0, total_s=1.0):
    n = int(total_s * FS)
    exc = S.unit_impulse(level_dbfs, n, FS)
    return exc.copy(), exc                                   # output == excitation (pure passthrough)


def fixture_dry_burst(seed=0x1234, total_s=1.0):
    exc = S.noise_burst(0.30, total_s, FS, seed)
    return exc.copy(), exc


def fixture_silence(total_s=1.0):
    n = int(total_s * FS)
    exc = S.unit_impulse(-6.0, n, FS)
    return np.zeros(n, dtype=np.int16), exc


def fixture_decaying_sine(freq=800.0, rt60_s=2.0, level_dbfs=-6.0, total_s=2.0):
    """A ringing tonal resonance — decays exponentially but is NOT a diffuse reverb. The metric must
    NOT pass it as WET-PASS/DENSE (a sine sits above its own σ ~50% of the time, fooling raw NED)."""
    n = int(total_s * FS)
    t = np.arange(n) / FS
    env = np.exp(-t * (3.0 * np.log(10.0)) / rt60_s)
    sig = np.sin(2 * np.pi * freq * t) * env * S.dbfs_to_amp(level_dbfs)
    out = np.clip(np.round(sig), -32768, 32767).astype(np.int16)
    return out, S.unit_impulse(level_dbfs, n, FS)


def fixture_delayed_passthrough(delay_s=0.010, gain=0.9, total_s=1.0):
    """Output is a delayed, scaled copy of the excitation — still 100% dry. Stresses lag estimation."""
    n = int(total_s * FS)
    exc = S.noise_burst(0.30, total_s, FS, seed=0x55)
    d = int(delay_s * FS)
    out = np.zeros(n, dtype=np.float64)
    out[d:] = gain * exc.astype(np.float64)[:n - d]
    return np.clip(np.round(out), -32768, 32767).astype(np.int16), exc


# ---- battery ----
def run_battery(out_dir=SCR, verbose=True):
    os.makedirs(out_dir, exist_ok=True)
    results = []

    def check(name, cond, detail):
        results.append((name, bool(cond), detail))
        if verbose:
            print(f"  [{'PASS' if cond else 'FAIL'}] {name}: {detail}")

    # 1. dry impulse -> DRY
    out, exc = fixture_dry_impulse()
    v = RM.analyze(out, exc, FS, "ctrl_dry_impulse", out_dir=out_dir)
    check("dry impulse -> DRY", v["verdict"] == "DRY", f"verdict={v['verdict']} wetness={v['wetness']:.4f}")

    # 2. dry burst passthrough -> DRY
    out, exc = fixture_dry_burst()
    v = RM.analyze(out, exc, FS, "ctrl_dry_burst", out_dir=out_dir, burst_end_s=0.30)
    check("dry burst -> DRY", v["verdict"] == "DRY", f"verdict={v['verdict']} wetness={v['wetness']:.4f}")

    # 3. single echo -> WET, SPARSE, RT60 indeterminate
    out, exc = fixture_single_echo()
    v = RM.analyze(out, exc, FS, "ctrl_single_echo", out_dir=out_dir)
    check("single echo -> WET & SPARSE & RT60 indeterminate",
          v["is_wet"] and v["density"] == "SPARSE" and v["rt60_s"] is None,
          f"verdict={v['verdict']} is_wet={v['is_wet']} density={v['density']} rt60={v['rt60_s']}")

    # 4. exp-decay reverbs -> WET-PASS, DENSE, RT60 within ±15%
    for rt in (0.8, 2.6, 5.0):
        out, exc = fixture_reverb(rt)
        v = RM.analyze(out, exc, FS, f"ctrl_reverb_rt{rt}", out_dir=out_dir)
        ok = (v["verdict"] == "WET-PASS" and v["density"] == "DENSE"
              and v["rt60_s"] is not None and abs(v["rt60_s"] - rt) / rt <= 0.15)
        err = (abs(v["rt60_s"] - rt) / rt * 100) if v["rt60_s"] else float("nan")
        check(f"reverb RT60={rt}s -> WET-PASS/DENSE within ±15%",
              ok, f"verdict={v['verdict']} density={v['density']} rt60={v['rt60_s']} err={err:.1f}%")

    # 5. growing feedback -> FAIL (over-unity)
    out, exc = fixture_growing()
    v = RM.analyze(out, exc, FS, "ctrl_growing", out_dir=out_dir)
    check("growing feedback -> FAIL (over-unity)",
          v["verdict"] == "FAIL" and v["subverdict"] == "over-unity",
          f"verdict={v['verdict']} sub={v['subverdict']} rt60={v['rt60_s']}")

    # 6. silence -> INDETERMINATE (empty)
    out, exc = fixture_silence()
    v = RM.analyze(out, exc, FS, "ctrl_silence", out_dir=out_dir)
    check("silence -> INDETERMINATE (empty)",
          v["verdict"] == "INDETERMINATE" and v["subverdict"] == "empty",
          f"verdict={v['verdict']} sub={v['subverdict']}")

    # 7. decaying sine (tonal ringing) -> must NOT be WET-PASS/DENSE (false-positive guard)
    out, exc = fixture_decaying_sine()
    v = RM.analyze(out, exc, FS, "ctrl_decaying_sine", out_dir=out_dir)
    check("decaying sine -> NOT WET-PASS, NOT DENSE (tonal, not diffuse)",
          v["verdict"] != "WET-PASS" and v["density"] != "DENSE",
          f"verdict={v['verdict']} density={v['density']} ned_max={v['ned_max']:.2f} "
          f"sfm={v.get('spectral_flatness')}")

    # 8. delayed dry passthrough -> DRY (lag estimation)
    out, exc = fixture_delayed_passthrough()
    v = RM.analyze(out, exc, FS, "ctrl_delayed_dry", out_dir=out_dir, burst_end_s=0.30)
    check("delayed dry passthrough -> DRY",
          v["verdict"] == "DRY", f"verdict={v['verdict']} wetness={v['wetness']:.4f}")

    # 9. floor-subtraction pair (plan 024 F5): a reverb riding a DC-dominated idle
    #    floor (the engine's measured signature: DC ~+12 LSB, slow small AC) must be
    #    recovered by analyze_pair from its burst/silence twins, with the floor named.
    rt = 2.6
    out, exc = fixture_reverb(rt)
    n = len(out)
    wander = np.cumsum(_rng(41).normal(0.0, 0.02, n))
    floor = np.round(12.0 + np.clip(wander - wander.mean(), -3, 3)).astype(np.int32)
    burst_tw = np.clip(out.astype(np.int32) + floor, -32768, 32767).astype(np.int16)
    sil_tw = floor.astype(np.int16)
    v = RM.analyze_pair(burst_tw, sil_tw, exc, FS, "ctrl_floor_pair", out_dir=out_dir)
    okp = (v["verdict"] == "WET-PASS" and v["density"] == "DENSE"
           and v["rt60_s"] is not None and abs(v["rt60_s"] - rt) / rt <= 0.15
           and 10.0 <= v["floor"]["dc"] <= 14.0)
    check("floor pair -> WET-PASS recovered + floor reported", okp,
          f"verdict={v['verdict']} rt60={v['rt60_s']} floor dc={v['floor']['dc']:.1f}")

    passed = sum(1 for _, ok, _ in results if ok)
    total = len(results)
    if verbose:
        print(f"\n{'=' * 64}\nCONTROL BATTERY: {passed}/{total} passed")
        print("VERDICT:", "METRIC TRUSTED" if passed == total else "METRIC BROKEN — DO NOT USE")
        print("=" * 64)
    return passed == total


if __name__ == "__main__":
    ok = run_battery()
    sys.exit(0 if ok else 1)
