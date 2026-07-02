#!/usr/bin/env python3
"""E4 (plan 023) — the variation oracle: recall Concert Hall V1-V7 through the REAL
LARC variation keys (key map from e4_key_enum), capture the recalled param blocks +
the settled WCS, and score the w43/95 shelf-injection sign law (0025) against the
DOCUMENTED per-variation LF-vs-Mid relations — predictions declared BEFORE reading.

Documented (ch.4/ch.8, Concert Hall B1P1): V1 LF3.0/Mid2.0; V2 1.7/1.7; V3 3.8/2.4;
V4 3.0/3.0; V5 avg 6.5 s; V6/V7 DynDecay mirror pair (5.7/1.7 with dynamics).

The 0025 apply law (w43/w95, lane 3): LF > Mid -> BOOST sign (stored bit7 = 1 under
E83 = cs 1? — V1 measured cmag 5, cs=0 stored... the LAW: LF>Mid boost, LF~Mid ~zero
injection, Mid>>LF cut; sign lane flips between the boost and cut sides).
"""
import sys, os, json

TOOLS = r"d:\OneDrive\Gray Instruments\iconex\tools"
sys.path.insert(0, TOOLS)
HERE = os.path.dirname(os.path.abspath(__file__))
CACHE = os.path.join(HERE, "variation_params.json")

import boot8080
from probe_run import run_ticks
from aru_freerun22_rtl import decode_word

# Modal UI (this session's debug): 0x26 arms VARIATION-select; then the NUMBER keys
# 1..7 = 0x2C/0x30/0x34/0x38/0x3C/0x2D/0x31 pick the variation.
VARMODE = 0x26
VKEYS = [("V2", 0x30), ("V3", 0x34), ("V4", 0x38), ("V5", 0x3C),
         ("V6", 0x2D), ("V7", 0x31), ("V1", 0x2C)]     # V1 last (return home)

PREDICT = {
    "V1": "LF 3.0 > Mid 2.0  -> BOOST (small; measured cmag 5)",
    "V2": "LF 1.7 = Mid 1.7  -> ~ZERO injection (cmag ~0) — the shelf-zero test",
    "V3": "LF 3.8 > Mid 2.4  -> BOOST, cmag > V1's 5 (bigger ratio 1.58 vs 1.5)",
    "V4": "LF 3.0 = Mid 3.0  -> ~ZERO injection",
    "V5": "avg 6.5 s         -> long everything; LF-vs-Mid per presets (expect boost)",
    "V6": "dyn 5.7/1.7 pair  -> per its RUNNING presets",
    "V7": "dyn mirror of V6  -> per its RUNNING presets",
}


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


def w4395(m):
    img = bytes(m.memory[0x4000:0x4200])
    out = {}
    for w in (43, 95, 44, 96, 45, 97):
        d = decode_word((img[4*w], img[4*w+1], img[4*w+2], img[4*w+3]))
        out[w] = dict(cmag=d["cmag"], cs=d["cs"], ofst=d["ofst"], typ=d["typ"])
    return out


def main():
    print("### PREDICTIONS (w43/95 shelf injection; declared BEFORE reading) ###")
    for k, v in PREDICT.items():
        print(f"  {k}: {v}")

    print("\nbooting ...", flush=True)
    m, ms = boot8080.boot(verbose=False, extra_ticks_after_mainloop=6_000_000)
    assert "mainloop" in ms
    io = SerialIO(m)

    result = {}

    def capture(tag):
        blk = bytes(m.memory[0x3CA2:0x3CD2]).hex()
        wc = w4395(m)
        img = bytes(m.memory[0x4000:0x4200]).hex()
        d43, d95 = wc[43], wc[95]
        result[tag] = dict(display=disp(m), block=blk, w=wc, wcs=img,
                           toggles=m.memory[0x3CCD])
        print(f"[{tag}] {disp(m)!r}")
        print(f"   w43 cmag={d43['cmag']:2d} cs={d43['cs']}   "
              f"w95 cmag={d95['cmag']:2d} cs={d95['cs']}   "
              f"w44 cmag={wc[44]['cmag']:2d}  w45 cmag={wc[45]['cmag']:2d}  "
              f"toggles=0x{m.memory[0x3CCD]:02X}", flush=True)

    capture("V1-boot")
    for tag, key in VKEYS:
        send_key(m, io, VARMODE)                      # arm variation-select mode
        send_key(m, io, key)
        run_ticks(m, 6_000_000)                       # settle the apply + de-zipper
        capture(tag)

    json.dump(result, open(CACHE, "w"), indent=1)
    print(f"\ncached -> {CACHE}")


if __name__ == "__main__":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass
    main()
