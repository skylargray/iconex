#!/usr/bin/env python3
"""F3b hunt (plan 024) — WHICH WCS bytes does the DynDecay machinery move?

f3_stop_decay run A showed: the level feedback works (0x3E10 tracks), the STOP-side
scheduler stages (0x3E11 -> 1, 0x3E12 counts, 0x3E14 -> 15) on the true-silence tail
and stays quiet on the forced-loud control — but the w44-family lane-3 bytes never
moved. Either the switch targets OTHER words/lanes, or the executor never ran.

This probe re-runs V6 burst->silence with the live feed and logs EVERY 0x4000-0x41FF
byte change (frame, CPU word, lane, old->new) + snapshots of 0x3C50-0x3C5F and
0x3E00-0x3E1F at phase boundaries + every 0x3E11/0x3E12/0x3E14/0x3C51 transition
with its frame stamp.
"""
import sys, os

TOOLS = r"d:\OneDrive\Gray Instruments\iconex\tools"
sys.path.insert(0, TOOLS)
HERE = os.path.dirname(os.path.abspath(__file__))

import numpy as np
import boot8080
from probe_run import run_ticks
from aru_freerun22_rtl import RTL22, program_rows22, fs22, decode_word
from e4_variations import SerialIO, send_key

TICKS_PER_FRAME = 62
SETTLE = 6_000_000
BURST_S, TAIL_S = 0.60, 4.00
AMP = 28000


def main():
    m, ms = boot8080.boot(verbose=False)
    assert "mainloop" in ms
    run_ticks(m, SETTLE)
    io = SerialIO(m)
    send_key(m, io, 0x26)
    send_key(m, io, 0x2D)                      # variation 6
    run_ticks(m, SETTLE)
    print(f"V6: toggles=0x{m.memory[0x3CCD]:02X}")

    base = bytes(m.memory[0x4000:0x4200])
    wcs = [(base[4*k], base[4*k+1], base[4*k+2], base[4*k+3]) for k in range(128)]
    rows, L, w_reset = program_rows22(wcs)
    fs = fs22(L)
    nb, n = int(BURST_S * fs), int((BURST_S + TAIL_S) * fs)
    rng = np.random.default_rng(224)
    exc = np.zeros(n, dtype=np.int64)
    exc[:nb] = rng.integers(-AMP, AMP + 1, nb)

    eng = RTL22()
    state = {"xw": 0}

    def on_input(port):
        p = port & 0xFF
        if p == 0x06:
            return state["xw"] & 0xFF
        if p == 0x07:
            return (state["xw"] >> 8) & 0xFF
        return 0x01 if p == 0xEF else (0xFF if p == 0xEE else 0x00)

    m.set_input_callback(on_input)

    prev = base
    changes = []
    watch = {0x3E11: None, 0x3E12: None, 0x3E14: None, 0x3C51: None, 0x3E10: None}
    trans = []
    for i in range(n):
        for _ in eng.run_sample(rows, int(exc[i]) & 0xFFFF):
            pass
        state["xw"] = eng.XREG_wr
        m.memory[0x3C14] = 0x80
        run_ticks(m, TICKS_PER_FRAME, chunk=TICKS_PER_FRAME)
        cur = bytes(m.memory[0x4000:0x4200])
        if cur != prev:
            for a in range(0x200):
                if cur[a] != prev[a]:
                    w, lane = a >> 2, a & 3
                    changes.append((i, w, lane, prev[a], cur[a]))
                    r = 127 - w
                    if 0 <= r < len(rows):
                        o = 4 * w
                        rows[r] = decode_word((cur[o], cur[o+1], cur[o+2], cur[o+3]))
            prev = cur
        for a in watch:
            v = m.memory[a]
            if v != watch[a]:
                trans.append((i, hex(a), watch[a], v))
                watch[a] = v
        if i == nb or i == n - 1:
            tag = "end of burst" if i == nb else "end of tail"
            print(f"--- {tag} (frame {i}) ---")
            print("  0x3C50-5F:", " ".join(f"{m.memory[0x3C50+k]:02X}" for k in range(16)))
            print("  0x3E00-1F:", " ".join(f"{m.memory[0x3E00+k]:02X}" for k in range(32)))

    print(f"\nWCS byte changes: {len(changes)} total")
    seen = {}
    for i, w, lane, old, new in changes:
        seen.setdefault((w, lane), []).append((i, old, new))
    for (w, lane), evs in sorted(seen.items()):
        phase = lambda fr: "burst" if fr < nb else "tail"
        first, last = evs[0], evs[-1]
        print(f"  w{w:03d} lane{lane}: {len(evs)} changes; first @f{first[0]} ({phase(first[0])}) "
              f"0x{first[1]:02X}->0x{first[2]:02X}; last @f{last[0]} 0x{last[1]:02X}->0x{last[2]:02X}")
    print(f"\nstate transitions ({len(trans)}):")
    for i, a, old, new in trans[:60]:
        print(f"  f{i:6d} ({'burst' if i < nb else 'tail'}): {a} "
              f"{'--' if old is None else f'{old:02X}'} -> {new:02X}")


if __name__ == "__main__":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass
    main()
