#!/usr/bin/env python3
"""d2j (session 0026) — the decay-generator parameters the bare 0xA791 walker does not
recompile (d2h showed [] for LF/Mid/Stops/Chorus/PDL): drive them through the SLIDER route
(scan 0x8185 -> handler 0x85F2 -> decay generator + de-zipper), with the page selected by
writing the derived page index 0x3C34 (netlist §7.1) — no LARC page-key emulation needed.

  PDL    (page1 slider6, 0x3C05): words 42/94 delay lanes; documented 24.0 -> 216 ms.
  Chorus (page2 slider3, 0x3C02 @ 0x3C34=1): the LFO depth byte 0x3CD4 (+ rate 0x3CD3);
         documented 0..97, default 50 (byte 0x80 -> depth?).
  LF-Stop (page2 slider1 @ page=1): with DynDecay OFF must change NOTHING (gate 0x83B4 —
         documented: stop decays act when Dynamic Decay is on); with 0x3CCD bit0 SET the
         path opens — record what moves.
"""
import sys, os, json

TOOLS = r"d:\OneDrive\Gray Instruments\iconex\tools"
sys.path.insert(0, TOOLS)
HERE = os.path.dirname(os.path.abspath(__file__))

import boot8080
from probe_run import run_ticks
from aru_freerun22_rtl import decode_word

MOVERS = {4 * w + l for w in (56, 57, 107, 108) for l in range(4)}

print("booting CONCERT to mainloop + settle ...", flush=True)
m, ms = boot8080.boot(verbose=False, extra_ticks_after_mainloop=6_000_000)
assert "mainloop" in ms


def wcs():
    return bytes(m.memory[0x4000:0x4200])


def dw(a, b):
    return sorted({x // 4 for x in range(0x200) if a[x] != b[x] and x not in MOVERS})


def wdec(b, w):
    return decode_word((b[4*w], b[4*w+1], b[4*w+2], b[4*w+3]))


base = wcs()
fs0 = 32508.0
print(f"LFO bytes at settle: rate(0x3CD3)=0x{m.memory[0x3CD3]:02X} "
      f"depth(0x3CD4)=0x{m.memory[0x3CD4]:02X}")

# ---------------- PDL (page 1 slider 6) ----------------
print("\n### Predelay via slider 0x3C05 (page 1) ###")
d42b, d94b = wdec(base, 42), wdec(base, 94)
print(f"  base: w42 ofst=0x{d42b['ofst']:04X}  w94 ofst=0x{d94b['ofst']:04X}")
for tag, v in (("lo", 0x02), ("hi", 0xF0)):
    m.memory[0x3C05] = v
    run_ticks(m, 6_000_000)
    img = wcs()
    d42, d94 = wdec(img, 42), wdec(img, 94)
    moved = dw(base, img)
    print(f"  {tag} (0x{v:02X}): words {moved}; w42 ofst 0x{d42['ofst']:04X} "
          f"(D{(d42['ofst'] - d42b['ofst']):+d} fr = {(d42['ofst'] - d42b['ofst']) / fs0 * 1000:+7.2f} ms); "
          f"w94 ofst 0x{d94['ofst']:04X} ({(d94['ofst'] - d94b['ofst']) / fs0 * 1000:+7.2f} ms)"
          f"   [doc: 24.0 min .. 216 ms max]", flush=True)
m.memory[0x3C05] = 0x00
run_ticks(m, 6_000_000)
base2 = wcs()
print(f"  restore 0x00: residual vs base = {dw(base, base2)}")

# ---------------- Chorus (page 2 slider 3) ----------------
print("\n### Chorus via page-switched slider (0x3C34=1, 0x3C02) ###")
m.memory[0x3C34] = 1
for tag, v in (("lo", 0x02), ("hi", 0xF0)):
    m.memory[0x3C02] = v
    run_ticks(m, 6_000_000)
    print(f"  {tag} (0x{v:02X}): depth(0x3CD4)=0x{m.memory[0x3CD4]:02X} "
          f"rate(0x3CD3)=0x{m.memory[0x3CD3]:02X}  array(p2s3)=0x{m.memory[0x3CA3 + 8]:02X}  "
          f"wcs-diff={dw(base2, wcs())}", flush=True)

# ---------------- LF-Stop (page 2 slider 1) with/without DynDecay ----------------
print("\n### LF Stop Decay (0x3C34=1, 0x3C00) — DynDecay gate check ###")
m.memory[0x3C00] = 0xF0
run_ticks(m, 6_000_000)
print(f"  DynDecay OFF (0x3CCD=0x{m.memory[0x3CCD]:02X}): wcs-diff={dw(base2, wcs())} "
      f"array(p2s1)=0x{m.memory[0x3CA3 + 6]:02X}   [doc: stop decays act when DynDecay ON]")
snap = wcs()
m.memory[0x3CCD] |= 0x01
m.memory[0x3C00] = 0x40
run_ticks(m, 8_000_000)
print(f"  DynDecay ON  (0x3CCD=0x{m.memory[0x3CCD]:02X}): wcs-diff vs pre-toggle = "
      f"{dw(snap, wcs())}")
m.memory[0x3C34] = 0
