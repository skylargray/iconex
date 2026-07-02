#!/usr/bin/env python3
"""E3c (plan 023) — program names via the REAL program-select keys (modal UI: 0x21 arms
program-select; number keys 1..7 = 0x2C/0x30/0x34/0x38/0x3C/0x2D/0x31; banks via 0x22).
Names land in the display buffer 0x3F4F (the d2c 0x3F8E readback was the wrong buffer).
Record (bank, program) -> name + record id (0x3CA2 header) for the D2c table; identify
the 'unlisted record' (D2c id 4) and what selector 3 is.
"""
import sys, os, json

TOOLS = r"d:\OneDrive\Gray Instruments\iconex\tools"
sys.path.insert(0, TOOLS)
HERE = os.path.dirname(os.path.abspath(__file__))

import boot8080
from probe_run import run_ticks
from e4_variations import SerialIO, disp, send_key

NUM = {1: 0x2C, 2: 0x30, 3: 0x34, 4: 0x38, 5: 0x3C, 6: 0x2D, 7: 0x31, 8: 0x35}
PGM, BANK = 0x21, 0x22

print("booting ...", flush=True)
m, ms = boot8080.boot(verbose=False, extra_ticks_after_mainloop=4_000_000)
assert "mainloop" in ms
io = SerialIO(m)

result = {}
for bank in (1, 2, 3, 4):
    send_key(m, io, BANK)
    send_key(m, io, NUM[bank])
    run_ticks(m, 2_000_000)
    bank_txt = disp(m)
    for pgm in range(1, 9):
        send_key(m, io, PGM)
        send_key(m, io, NUM[pgm])
        run_ticks(m, 4_000_000)
        txt = disp(m)
        rid = m.memory[0x3CA2]
        result[f"B{bank}P{pgm}"] = dict(display=txt, id=rid)
        print(f"B{bank}P{pgm}: id=0x{rid:02X} {txt!r}", flush=True)

json.dump(result, open(os.path.join(HERE, "program_names.json"), "w"), indent=1)
print("\ncached -> program_names.json")
