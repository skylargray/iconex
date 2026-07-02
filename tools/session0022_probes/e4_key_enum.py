#!/usr/bin/env python3
"""E4a (plan 023) — enumerate the 32 LARC serial key codes on the verified core.

Key event byte = 0x20 | (bit<<2) | column (press), same without 0x20 (release) —
the boot8080 PGM-2 encoding (0x30/0x10). For each key: send press+release into a
settled CONCERT boot, run, record the display line + the param-block header 0x3CA2 +
apply-page 0x3C34 + program id — the display names the key (the header shows
'CONCERT HALLB1 P1 V1'). Fresh boot per key would be cleanest; one boot with drift
is enough for IDENTIFICATION (a targeted pass then uses the found keys).
"""
import sys, os, json

TOOLS = r"d:\OneDrive\Gray Instruments\iconex\tools"
sys.path.insert(0, TOOLS)
HERE = os.path.dirname(os.path.abspath(__file__))
CACHE = os.path.join(HERE, "key_map.json")

import boot8080
from probe_run import run_ticks, _fire_int


class SerialIO:
    def __init__(self, m):
        self.rx = []
        self.tx = []

        def on_input(port):
            p = port & 0xFF
            if p == 0xEF:
                return 0x01 | (0x02 if self.rx else 0)
            if p == 0xEE:
                return self.rx.pop(0) if self.rx else 0xFF
            if p in (0x06, 0x07):
                return 0xFF
            return 0x00

        def on_output(port, v):
            if (port & 0xFF) == 0xEE:
                self.tx.append(v & 0xFF)

        m.set_input_callback(on_input)
        m.set_output_callback(on_output)


def disp(m):
    b = bytes(m.memory[0x3F4F:0x3F81])
    return "".join(chr(c & 0x7F) if 32 <= (c & 0x7F) < 127 else " " for c in b).rstrip()


def send_key(m, io, press):
    io.rx.append(press)
    run_ticks(m, 1_500_000)
    io.rx.append(press & ~0x20)
    run_ticks(m, 3_000_000)


def main():
    print("booting ...", flush=True)
    m, ms = boot8080.boot(verbose=False, extra_ticks_after_mainloop=4_000_000)
    assert "mainloop" in ms
    io = SerialIO(m)
    result = {}
    print(f"settled: {disp(m)!r}")
    for bit in range(8):
        for col in range(4):
            press = 0x20 | (bit << 2) | col
            before = disp(m)
            hdr_b = m.memory[0x3CA2]
            send_key(m, io, press)
            after = disp(m)
            rec = dict(bit=bit, col=col, press=hex(press),
                       display=after, changed=(after != before),
                       hdr=m.memory[0x3CA2], page34=m.memory[0x3C34])
            result[hex(press)] = rec
            print(f"key 0x{press:02X} (bit{bit} col{col}): "
                  f"{'*' if rec['changed'] else ' '} {after!r}  "
                  f"hdr=0x{rec['hdr']:02X} p34={rec['page34']}", flush=True)
    json.dump(result, open(CACHE, "w"), indent=1)
    print(f"\ncached -> {CACHE}")


if __name__ == "__main__":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass
    main()
