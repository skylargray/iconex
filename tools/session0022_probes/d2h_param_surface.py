#!/usr/bin/env python3
"""d2h (session 0026) — the COMPLETE parameter surface: all 5 LARC pages x 6 sliders.

Netlist §7.1/§7.3: every page's parameter values live in the flat array
`0x3CA3 + page*6 + slider` (recalled from the program record at load); the apply engine
**0xA791** compiles the FULL WCS image from it. So any parameter on any page can be driven
directly: write the array byte -> direct-call 0xA791 -> capture the image. No page keys,
no de-zipper wait.

Outputs:
  1. the RECALLED DEFAULTS (variation-1 preset bytes, all 30 slots + the 0x3CCD toggles);
  2. built-in route validation: rebuilding with the untouched array must reproduce the boot
     image byte-identically (movers 56/57/107/108 masked);
  3. the param -> WCS-word map: for each slot, lo (0x02) and hi (0xF0) rebuild diffs
     (words + lanes + decoded cmag/cs/ofst changes);
  4. cache: d2h_param_wcs.json {"p{page}s{slider}-{lo|hi}": wcs hex} for the render probe.

CONCERT page map (ch.4 Table 4.2): P1 LF/Mid/XOV/Treble/Depth/PDL; P2 StopLF/StopMid/
Chorus/HFBW/Diffusion/Definition; P3 PE-Level 1-4 (5,6 inactive); P4 PE-Delay 1-4 +
Fine-Predelay L/R; P5 Size/-/Gate.
"""
import sys, os, json

TOOLS = r"d:\OneDrive\Gray Instruments\iconex\tools"
sys.path.insert(0, TOOLS)
HERE = os.path.dirname(os.path.abspath(__file__))
CACHE = os.path.join(HERE, "d2h_param_wcs.json")

import boot8080
from probe_run import run_ticks
from aru_freerun22_rtl import decode_word

PARAM_BASE = 0x3CA3
APPLY = 0xA791
MOVERS = {4 * w + l for w in (56, 57, 107, 108) for l in range(4)}
NAMES = [["LF-Decay", "Mid-Decay", "Crossover", "Treble-Dcy", "Depth", "Predelay"],
         ["LF-Stop", "Mid-Stop", "Chorus", "HF-BW", "Diffusion", "Definition"],
         ["PE-Lvl1", "PE-Lvl2", "PE-Lvl3", "PE-Lvl4", "(inact)", "(inact)"],
         ["PE-Dly1", "PE-Dly2", "PE-Dly3", "PE-Dly4", "FinePD-L", "FinePD-R"],
         ["Size", "(s2)", "Gate", "(s4)", "(s5)", "(s6)"]]

print("booting CONCERT to mainloop + settle ...", flush=True)
m, ms = boot8080.boot(verbose=False, extra_ticks_after_mainloop=6_000_000)
assert "mainloop" in ms


def wcs():
    return bytes(m.memory[0x4000:0x4200])


def call_apply(budget=30_000_000):
    """Direct-call the full-image apply engine (d1a sentinel pattern)."""
    sp = (m.sp - 2) & 0xFFFF
    m.memory[sp] = 0xFF
    m.memory[(sp + 1) & 0xFFFF] = 0xFF
    m.sp = sp
    m.pc = APPLY
    m.set_breakpoint(0xFFFF)
    ticks = 0
    while ticks < budget:
        m.ticks_to_stop = 200_000
        ev = m.run()
        ticks += 200_000 - m.ticks_to_stop
        if ev & m._BREAKPOINT_HIT:
            if m.pc == 0xFFFF:
                m.clear_breakpoint(0xFFFF)
                return True
            m.clear_breakpoint(m.pc)
            m.ticks_to_stop = 1
            m.run()
    raise RuntimeError(f"0xA791 did not return (PC=0x{m.pc:04X})")


def dw(a, b):
    return sorted({x // 4 for x in range(0x200) if a[x] != b[x] and x not in MOVERS})


# ---- 1. the recalled defaults ----
hdr = m.memory[0x3CA2]
params = [[m.memory[PARAM_BASE + p * 6 + s] for s in range(6)] for p in range(5)]
toggles = m.memory[0x3CCD]
print(f"\nrecalled param block: header=0x{hdr:02X}  toggles(0x3CCD)=0x{toggles:02X} "
      f"(DynDecay={toggles & 1}, ModeEnh={(toggles >> 6) & 1}, DecayOpt={(toggles >> 7) & 1})")
for p in range(5):
    print(f"  page {p + 1}: " + "  ".join(f"{NAMES[p][s]}=0x{params[p][s]:02X}"
                                          for s in range(6)))

# ---- 2. route validation: untouched rebuild == boot image (mod movers) ----
base = wcs()
call_apply()
rebuilt = wcs()
d0 = dw(base, rebuilt)
print(f"\nuntouched 0xA791 rebuild vs boot image: {len(d0)} word diffs (mod movers) "
      f"{'== VALID' if not d0 else d0}")
base = rebuilt                       # the canonical apply-built baseline

# ---- 3/4. the lo/hi sweep ----
cache = {"base": base.hex(), "defaults": params, "toggles": toggles}
print(f"\n{'slot':>10} {'name':>10} {'dflt':>5}  words moved (lo | hi)")
for p in range(5):
    for s in range(6):
        if NAMES[p][s].startswith("("):
            continue
        a = PARAM_BASE + p * 6 + s
        orig = m.memory[a]
        res = {}
        for tag, v in (("lo", 0x02), ("hi", 0xF0)):
            m.memory[a] = v
            call_apply()
            img = wcs()
            res[tag] = dw(base, img)
            cache[f"p{p + 1}s{s + 1}-{tag}"] = img.hex()
        m.memory[a] = orig
        call_apply()
        back = dw(base, wcs())
        flag = "" if not back else f"  !! residual {back}"
        print(f"  p{p + 1}s{s + 1:>5} {NAMES[p][s]:>10} 0x{orig:02X}  "
              f"{res['lo']} | {res['hi']}{flag}", flush=True)

json.dump(cache, open(CACHE, "w"))
print(f"\ncache -> {CACHE}")
