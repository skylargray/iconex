#!/usr/bin/env python3
"""E3a exploration (plan 023) — find how the firmware renders parameter VALUE strings
(the LARC display), so slider bytes can be calibrated against the firmware's own
formatter ("2.0 SEC", "720 HZ", "24.0 MS", ...).

Watch: (a) serial TX bytes after a slider injection, (b) the display/message buffers
0x3F4F..0x3F80 and 0x3F8E.., (c) if silent, direct-call the display milestone 0x82CF.
"""
import sys, os

TOOLS = r"d:\OneDrive\Gray Instruments\iconex\tools"
sys.path.insert(0, TOOLS)
HERE = os.path.dirname(os.path.abspath(__file__))

import boot8080
from probe_run import run_ticks


class TXTap:
    def __init__(self, m):
        self.tx = []
        self.rx_queue = []

        def on_input(port):
            p = port & 0xFF
            if p == 0xEF:
                return 0x01 | (0x02 if self.rx_queue else 0)
            if p == 0xEE:
                return self.rx_queue.pop(0) if self.rx_queue else 0xFF
            if p in (0x06, 0x07):
                return 0xFF
            return 0x00

        def on_output(port, v):
            if (port & 0xFF) == 0xEE:
                self.tx.append(v & 0xFF)

        m.set_input_callback(on_input)
        m.set_output_callback(on_output)


def ascii_of(bs):
    return "".join(chr(c) if 32 <= (c & 0x7F) < 127 else "." for c in bs)


def dump_bufs(m, label):
    b1 = bytes(m.memory[0x3F4F:0x3F81])
    b2 = bytes(m.memory[0x3F8E:0x3FBE])
    print(f"  [{label}] 0x3F4F: {ascii_of(b1)!r}")
    print(f"  [{label}] 0x3F8E: {ascii_of(b2)!r}")


def main():
    print("booting ...", flush=True)
    m, ms = boot8080.boot(verbose=False, extra_ticks_after_mainloop=6_000_000)
    assert "mainloop" in ms
    tap = TXTap(m)
    dump_bufs(m, "settled")

    print("\ninject Mid Decay slider 0x3C01 <- 0x80 (page 1) ...")
    m.memory[0x3C34] = 0
    m.memory[0x3C01] = 0x80
    n0 = len(tap.tx)
    run_ticks(m, 8_000_000)
    print(f"  TX bytes after injection: {len(tap.tx)-n0}")
    if len(tap.tx) > n0:
        raw = tap.tx[n0:]
        print(f"  raw: {[hex(c) for c in raw[:64]]}")
        print(f"  ascii(&0x7F): {ascii_of(raw[:96])!r}")
    dump_bufs(m, "post-inject")

    print("\ndirect-call 0x82CF (display milestone) ...")
    sp = (m.sp - 2) & 0xFFFF
    m.memory[sp] = 0xFF
    m.memory[(sp + 1) & 0xFFFF] = 0xFF
    m.sp = sp
    save_pc = m.pc
    m.pc = 0x82CF
    n1 = len(tap.tx)
    m.set_breakpoint(0xFFFF)
    for _ in range(200):
        m.ticks_to_stop = 20_000
        ev = m.run()
        if ev & m._BREAKPOINT_HIT:
            if m.pc == 0xFFFF:
                print("  returned via sentinel")
                break
            m.clear_breakpoint(m.pc)
            m.ticks_to_stop = 1
            m.run()
    print(f"  PC=0x{m.pc:04X}; TX bytes: {len(tap.tx)-n1}")
    if len(tap.tx) > n1:
        raw = tap.tx[n1:]
        print(f"  ascii(&0x7F): {ascii_of(raw[:96])!r}")
    dump_bufs(m, "post-82CF")


if __name__ == "__main__":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass
    main()
