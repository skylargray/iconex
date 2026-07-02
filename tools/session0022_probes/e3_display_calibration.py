#!/usr/bin/env python3
"""E3a (plan 023) — the LARC display calibration: byte <-> displayed value from the
firmware's OWN value formatter (registry #28's named next tool).

Method: slider injection (0x3C00-05, page select = write 0x3C34 — the d2j route)
triggers the firmware's display render into the message buffer 0x3F4F..; parse the
value string ("MID DECAY    3.0  SEC"). One boot; ~500 injections; cache
display_map.json. The LARC's physical full-scale byte is whatever displays the
documented maximum (ch.4 Table 4.2).
"""
import sys, os, json, re

TOOLS = r"d:\OneDrive\Gray Instruments\iconex\tools"
sys.path.insert(0, TOOLS)
HERE = os.path.dirname(os.path.abspath(__file__))
CACHE = os.path.join(HERE, "display_map.json")

import boot8080
from probe_run import run_ticks

PAGES = {
    0: ["LF Decay", "Mid Decay", "Crossover", "Treble Dcy", "Depth", "Predelay"],
    1: ["LF Stop", "Mid Stop", "Chorus", "HF Bwidth", "Diffusion", "Definition"],
    2: ["PE1 Level", "PE2 Level", "PE3 Level", "PE4 Level", "sl5", "sl6"],
    3: ["PE1 Delay", "PE2 Delay", "PE3 Delay", "PE4 Delay", "FinePD L", "FinePD R"],
    4: ["Size", "sl2", "Gate", "sl4", "sl5", "sl6"],
}
# Ascending pass achieves PICKUP (soft takeover: the slider is ignored until it
# crosses the recalled preset — discovered this session); the descending pass then
# reads the true f(byte) over the WHOLE range including below the preset.
UP = [0x02, 0x20, 0x40, 0x60, 0x80, 0xA0, 0xC0, 0xE0, 0xFE]
DOWN = [0xF8, 0xF0, 0xE0, 0xD0, 0xC0, 0xB0, 0xA0, 0x90, 0x80, 0x70, 0x60, 0x50,
        0x40, 0x30, 0x20, 0x18, 0x10, 0x08, 0x02]
SETTLE = 3_000_000


def disp(m):
    b = bytes(m.memory[0x3F4F:0x3F68])
    return "".join(chr(c & 0x7F) if 32 <= (c & 0x7F) < 127 else " " for c in b).rstrip()


def main():
    print("booting CONCERT to mainloop + settle ...", flush=True)
    m, ms = boot8080.boot(verbose=False, extra_ticks_after_mainloop=6_000_000)
    assert "mainloop" in ms
    print(f"settled display: {disp(m)!r}", flush=True)

    result = {}
    for page, names in PAGES.items():
        m.memory[0x3C34] = page
        for sl in range(6):
            key = f"p{page+1}s{sl+1}"
            up, down = [], []
            for v in UP:                       # pickup pass (crosses the preset)
                m.memory[0x3C00 + sl] = v
                run_ticks(m, SETTLE)
                up.append((v, disp(m)))
            for v in DOWN:                     # post-pickup: true f(byte), full range
                m.memory[0x3C00 + sl] = v
                run_ticks(m, SETTLE)
                down.append((v, disp(m)))
            result[key] = dict(name=names[sl], up=up, down=down)
            print(f"[{key}] {names[sl]} (descending, post-pickup):", flush=True)
            for v, txt in down:
                print(f"   0x{v:02X}: {txt!r}")
            json.dump(result, open(CACHE, "w"), indent=1)
    m.memory[0x3C34] = 0
    print(f"\ncached -> {CACHE}")


if __name__ == "__main__":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass
    main()
