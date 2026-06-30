#!/usr/bin/env python3
"""Run tools/reverb_metrics.py on REAL impulse responses from IR/ — including the actual target,
the Lexicon 224XL Concert Hall (the CONCERT program plan 020 is trying to reproduce).

An IR *is* the system's output to a unit impulse, so we feed the IR as `output` and a unit impulse
(at the IR's direct-sound level) as `excitation`. This both (a) validates the metric on genuine
reverbs with all their real-world features, and (b) MEASURES the target RT60/echo-density the
whole-machine emulator must hit (grounds plan 020 AC4 in a real measurement, not a spec number).

Dense halls/plates should read WET-PASS / DENSE with a sensible RT60. Character presets (slap echo,
doubler) are SPARSE by design — reading them as such is the metric discriminating correctly, not
failing.

Run:  python tools/reverb_metrics_irtest.py
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
sys.stdout.reconfigure(encoding="utf-8")
import numpy as np
import soundfile as sf

import reverb_metrics as RM

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SCR = (r"C:/Users/Skylar/AppData/Local/Temp/claude/"
       r"d--OneDrive-Gray-Instruments-iconex/ae30a9a1-b02b-4706-a6d3-7d89d4cefad3/scratchpad/renders")

# (path, expected — 'dense' for halls/plates, 'sparse' for slap/doubler, None = report only)
IRS = [
    ("IR/Lexicon 224XL/Concert Hall V1.1.L.wav", "dense"),
    ("IR/Lexicon 224XL/Concert Hall V7.2.L.wav", "dense"),
    ("IR/Lexicon 224XL/P85 - 20.0 Seconds A.wav", "dense"),
    ("IR/Lexicon 480L/Big Gee's Lexicon 480L/Large Hall.aif", "dense"),
    ("IR/Lexicon 480L/Big Gee's Lexicon 480L/A Plate.aif", "dense"),
    ("IR/Lexicon 480L/Big Gee's Lexicon 480L/Large Plate.aif", "dense"),
    ("IR/Lexicon 480L/Big Gee's Lexicon 480L/Medium Hall.aif", "dense"),
    ("IR/Lexicon 480L/Big Gee's Lexicon 480L/Large Room.aif", "dense"),
    ("IR/Lexicon 480L/Big Gee's Lexicon 480L/Slap Plate.aif", None),
    ("IR/Lexicon 480L/Big Gee's Lexicon 480L/Doubler.aif", None),
]


def load_mono(path):
    x, fs = sf.read(path, always_2d=True)
    return x[:, 0].astype(np.float64), int(fs)


def main():
    os.makedirs(SCR, exist_ok=True)
    print("### reverb_metrics on REAL impulse responses (IR/) ###\n")
    print(f"{'IR':40} {'fs':>6} {'dur':>5}  {'verdict':>13} {'density':>7} {'RT60':>7} {'mix(ms)':>7} {'pkfrac':>7}")
    results = []
    for rel, expect in IRS:
        path = os.path.join(ROOT, rel)
        if not os.path.exists(path):
            print(f"{rel.split('/')[-1]:40} (missing)")
            continue
        x, fs = load_mono(path)
        peak = float(np.max(np.abs(x))) + 1e-12
        out = np.clip(np.round(x / peak * 32000.0), -32768, 32767).astype(np.int16)
        exc = np.zeros(len(out), dtype=np.int16)
        exc[0] = 32000                                   # unit impulse at the direct-sound level
        name = "ir_" + os.path.splitext(os.path.basename(rel))[0].replace(" ", "_").replace(".", "_")
        v = RM.analyze(out, exc, fs, name, out_dir=SCR)

        # NED mixing time (ms to reach diffuse), for the density characterisation
        mix_ms = ""
        rt = f"{v['rt60_s']:.2f}s" if v["rt60_s"] else "—"
        dur = len(out) / fs
        print(f"{os.path.basename(rel):40} {fs:>6} {dur:>4.1f}s  {v['verdict']:>13} "
              f"{str(v['density']):>7} {rt:>7} {mix_ms:>7} {v.get('dominant_peak_frac', 0):>7.4f}")

        ok = True
        if expect == "dense":
            ok = (v["verdict"] == "WET-PASS" and v["density"] == "DENSE")
        results.append((rel, expect, v["verdict"], v["density"], ok))

    print()
    dense = [r for r in results if r[1] == "dense"]
    passed = sum(1 for r in dense if r[4])
    print(f"dense halls/plates classified WET-PASS/DENSE: {passed}/{len(dense)}")
    for rel, expect, verdict, density, ok in results:
        if expect == "dense" and not ok:
            print(f"  [INVESTIGATE] {rel.split('/')[-1]}: {verdict}/{density} (expected WET-PASS/DENSE)")
    print("\n(slap/doubler reported only — they are SPARSE by design; SPARSE there = correct discrimination)")
    return passed == len(dense)


if __name__ == "__main__":
    sys.exit(0 if main() else 1)
