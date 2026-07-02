#!/usr/bin/env python3
"""D2a follow-up — which parameter state does the settled image hold for the params whose
words the power-up transient did NOT touch (LOW 43/95, XOV 45/46/97/98, HFD 40/41/92/93,
DEP 29-32/81-84)?

Hypothesis to kill: the power-up apply only writes params whose preset differs from the
record's baked bytes; if so, un-moved words already hold the documented preset state
(baked == applied). Test by INJECTION + RESTORE (verification of the capture point per
D2a — not parameter fitting):
  1. read the power-up slider bytes 0x3C00-05 (the firmware's own variation-1 preset
     positions) and the settled WCS;
  2. per slider: write a different byte -> run -> which WCS words move? (proves the
     apply path reaches them);
  3. write the power-up byte back -> run -> the WCS must return byte-identical outside
     the 8 modulation movers (idempotence => the settled image IS the preset-applied
     state for that param).
"""
import sys, os, json

TOOLS = r"d:\OneDrive\Gray Instruments\iconex\tools"
sys.path.insert(0, TOOLS)
HERE = os.path.dirname(os.path.abspath(__file__))

import boot8080
from probe_run import run_ticks

MOVERS = {4 * w + l for w in (56, 57, 107, 108) for l in range(4)}

print("booting CONCERT to mainloop + settle ...", flush=True)
m, ms = boot8080.boot(verbose=False, extra_ticks_after_mainloop=6_000_000)
assert "mainloop" in ms

def run(n):
    run_ticks(m, n)                     # boot()-equivalent: serves the serial RST-7

def wcs():
    return bytes(m.memory[0x4000:0x4200])

def dw(a, b):
    return sorted({x // 4 for x in range(0x200) if a[x] != b[x] and x not in MOVERS})

sliders = bytes(m.memory[0x3C00:0x3C06])
print(f"power-up slider bytes 0x3C00-05 (variation-1 presets): "
      f"{[hex(v) for v in sliders]}  (labels LOW MID XOV HFD DEP PDL)")
base = wcs()

EXPECT = {0: ("LOW", [43, 95]), 2: ("XOV", [45, 46, 97, 98]),
          3: ("HFD", [40, 41, 92, 93]), 4: ("DEP", [29, 30, 31, 32, 81, 82, 83, 84])}
for idx, (label, words) in EXPECT.items():
    orig = sliders[idx]
    probe = 0x80 if orig < 0x60 or orig > 0xA0 else 0x30
    m.memory[0x3C00 + idx] = probe
    run(4_000_000)
    moved = dw(base, wcs())
    m.memory[0x3C00 + idx] = orig
    run(4_000_000)
    back = dw(base, wcs())
    ok = not back
    print(f"  {label} (0x3C0{idx}): {hex(orig)} -> {hex(probe)} moves words {moved}; "
          f"restore -> {'byte-identical (settled image = preset-applied state)' if ok else f'RESIDUAL DIFFS {back}'}")

print("\nconclusion: for each param above, 'moves expected words + restores identically'"
      "\n= the apply path reaches them AND the record-baked bytes equal the preset-applied"
      "\nbytes; the settled image represents the documented variation-1 state.")
