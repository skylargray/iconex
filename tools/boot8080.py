#!/usr/bin/env python3
"""Faithful 224XL v8.2.1 boot harness on a VERIFIED 8080 core (kosarev/z80 I8080Machine).

This replaces the home-grown tools/z80emu.py (which had an 8080 parity-vs-overflow bug:
it set the P/V flag to *overflow* on ADD/SUB like a Z80; the 8080 sets *parity* there, and
the firmware uses parity branches). The I8080Machine core passes the canonical 8080 exercisers
(cputest / 8080pre / 8080exm) — see docs/plans/224XL-interp-stack.md (L1 ✅).

Boot path is FAITHFUL — POST is RUN, not suppressed. With no faithful ARU yet, POST fails its
ARU latch test (DIAG ERROR TYPE E32) and the firmware waits for a front-panel button. We inject
the real LARC "skip diagnostics" key (PGM-2 = serial code 0x30 press / 0x10 release, found
empirically: it is the only one of the 32 button codes that bypasses to normal operation),
exactly as a user pressing PGM-2 would. The firmware then loads its default power-up program
(mem[0xB800] = 0x01 = CONCERT HALL) and reaches the main loop.

Verified (L2): the offset table at 0x3F4D and lanes 0-2 of the 0x4000 WCS image are byte-identical
to the old (POST-suppressed, buggy-core) pipeline; only the modulated lane-3 bytes differ, and
those change frame-to-frame from the LFO regardless of core.

The 8080 only sees the ARU through I/O ports; a benign stub suffices to reach program-load (the
program BUILD is pure 8080 computation and does not use the ARU). A faithful ARU + un-suppressed
POST pass is deferred to the L6 work.
"""
import os
import numpy as np
import z80

DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                   "ROMs", "Lexicon 224", "224XL v8_21")

# Boot milestones (PC addresses).
HANDSHAKE = 0x0089
DIAG_E    = 0x021D
DIAG_H    = 0x0217
NORMAL_OP = 0x813B
PROG_LOAD = 0x13B6
MAINLOOP  = 0x8169

# LARC "skip diagnostics" (PGM-2) button: a key event is one serial byte
#   0x20 | (bit<<2) | column ; bit5 = press.  0x30 = col0,bit4,press ; 0x10 = release.
PGM2_PRESS, PGM2_RELEASE = 0x30, 0x10


def load_mem():
    mem = bytearray(0x10000)
    for n, base in [(1, 0), (2, 0x800), (3, 0x1000)]:
        b = np.fromfile(f"{DIR}/SBC{n} 2716.BIN", dtype=np.uint8)
        mem[base:base + len(b)] = b.tobytes()
    for n in range(1, 9):
        b = np.fromfile(f"{DIR}/NVS{n} 2732.BIN", dtype=np.uint8)
        base = 0x8000 + (n - 1) * 0x1000
        mem[base:base + len(b)] = b.tobytes()
    return mem


def boot(max_ticks=200_000_000, verbose=True, trace=None, extra_ticks_after_mainloop=0,
         snapshot_cb=None, snapshot_every=0, hw_stub=None):
    """Boot reset -> handshake -> POST -> (PGM-2 bypass) -> program-load -> mainloop.

    Returns (machine, milestones) where milestones maps name->tick. Read the firmware-built
    data straight from machine.memory afterwards (0x3F4D offset buffer, 0x4000 WCS image).

    trace: optional tools.trace8080.Trace8080 — when given, EVERY memory write and EVERY I/O is
    captured on this verified core (the write callback then OWNS the write, so it must perform it;
    see Trace8080.attach). Milestones are forwarded as phase markers. Lets us DISCOVER where the
    firmware writes microcode instead of asserting an address range.

    hw_stub: if not None, every NON-serial input port (the ARU latch 0x06/0x07 and the else-branch
    ports such as 0x02) returns this byte instead of the defaults (0xFF for 0x06/0x07, 0x00 else).
    The serial 8251 (0xEE/0xEF) is untouched so the LARC handshake/PGM-2 bypass still work. Used by
    tools/verify_build_hwindep.py for the Phase-1.3 STUB-VARIATION test: if the 0x4000 WCS image is
    byte-identical across hw_stub in {0x00,0xFF,0x55,0xAA}, the build provably ignores those ports."""
    m = z80.I8080Machine()
    m.set_memory_block(0, bytes(load_mem()))
    m.pc = 0
    if trace is not None:
        trace.attach(m)               # installs the write callback (perform + log)

    st = {"ic": 0, "rx": [], "rx_at": 0, "tx": [], "tx_en": True, "ei": False,
          "diag": None, "phase": 0}

    def rx_ready():
        return bool(st["rx"]) and st["ic"] >= st["rx_at"]

    def on_input(port):
        p = port & 0xFF
        if p == 0xEF:                                   # 8251 status: TxRDY + RxRDY
            ret = 0x01 | (0x02 if rx_ready() else 0)
        elif p == 0xEE:                                 # 8251 data
            ret = st["rx"].pop(0) if rx_ready() else 0xFF
        elif p in (0x06, 0x07):                         # ARU latch readback (stub)
            ret = 0xFF if hw_stub is None else (hw_stub & 0xFF)
        else:
            ret = 0x00 if hw_stub is None else (hw_stub & 0xFF)
        if trace is not None:
            trace.on_io("IN", p, ret)
        return ret

    def on_output(port, v):
        p = port & 0xFF
        if trace is not None:
            trace.on_io("OUT", p, v)
        if p == 0xEE:                                   # serial TX (LARC display)
            st["tx"].append(v & 0x7F)
            if v == 0xE0 and not st["rx"]:              # power-up handshake request
                st["rx"].append(0xC8); st["rx_at"] = st["ic"] + 5000
        elif p == 0xEF and v != 0xCE:                   # 8251 command (ignore mode word 0xCE)
            st["tx_en"] = bool(v & 0x01)

    m.set_input_callback(on_input)
    m.set_output_callback(on_output)

    def fire_int():
        """Assert the RST-7 serial interrupt by hand (the i8080 binding can't): push PC,
        jump to 0x0038, clear INTE — exactly what the 8080 does on interrupt acknowledge."""
        if m._I8080State__iff[0] == 0:                  # interrupts disabled -> ignored
            return
        sp = (m.sp - 2) & 0xFFFF
        m.memory[sp] = m.pc & 0xFF
        m.memory[(sp + 1) & 0xFFFF] = (m.pc >> 8) & 0xFF
        m.sp = sp
        m.pc = 0x0038
        m._I8080State__iff[0] = 0

    MILE = {HANDSHAKE: "handshake", DIAG_E: "DIAG_E", DIAG_H: "DIAG_H",
            NORMAL_OP: "normal_op", PROG_LOAD: "prog_load", MAINLOOP: "mainloop"}
    for a in MILE:
        m.set_breakpoint(a)
    seen = {}

    def step(n):
        m.ticks_to_stop = n
        ev = m.run()
        st["ic"] += n - m.ticks_to_stop
        return ev

    while st["ic"] < max_ticks:
        ev = step(1500 if st["ei"] else 30000)
        if ev & m._BREAKPOINT_HIT:                      # breakpoint hit (event = 2)
            pc = m.pc
            if pc in MILE and pc not in seen:
                seen[pc] = st["ic"]
                if trace is not None:
                    trace.mark(MILE[pc])
                if verbose:
                    print(f"  ~{st['ic']:>10} ticks: {MILE[pc]}")
            if pc == HANDSHAKE:
                st["ei"] = True
            if pc in (DIAG_E, DIAG_H) and st["diag"] is None:
                st["diag"] = st["ic"]
            m.clear_breakpoint(pc); m.ticks_to_stop = 1; m.run()
            if pc == MAINLOOP and PROG_LOAD in seen and extra_ticks_after_mainloop == 0:
                break
        # periodic WCS snapshot once past mainloop (for per-frame co-simulation)
        if snapshot_cb is not None and snapshot_every and MAINLOOP in seen:
            if st["ic"] - st.get("last_snap", 0) >= snapshot_every:
                snapshot_cb(bytes(m.memory[0x4000:0x4200]), st["ic"])
                st["last_snap"] = st["ic"]
        # run past mainloop for audio-frame processing if requested
        if extra_ticks_after_mainloop and "mainloop" in {MILE.get(a) for a in seen} \
                and st["ic"] > seen[MAINLOOP] + extra_ticks_after_mainloop:
            break
        else:                                           # ticks limit
            if st["ei"] and (st["tx_en"] or rx_ready()):
                fire_int()
            # inject the PGM-2 bypass once the diagnostic error has settled
            if st["diag"] and st["ic"] > st["diag"] + 3_000_000:
                if st["phase"] == 0:
                    st["rx"].append(PGM2_PRESS); st["rx_at"] = st["ic"]; st["phase"] = 1
                elif st["phase"] == 1 and not st["rx"]:
                    st["rx"].append(PGM2_RELEASE); st["rx_at"] = st["ic"]; st["phase"] = 2

    if verbose:
        tx = "".join(chr(c) if 32 <= c < 127 else "." for c in st["tx"])
        print(f"  final PC=0x{m.pc:04X}  LARC display tail: {tx[-48:]!r}")
    return m, {MILE[a]: t for a, t in seen.items()}


def read_offsets(m, n=128):
    """Read the firmware's 0x3F4D offset buffer downward (hi@a, lo@a-1); signed."""
    offs = []
    for s in range(n):
        a = 0x3F4D - 2 * s
        v = (m.memory[a] << 8) | m.memory[a - 1]
        offs.append(v - 0x10000 if v & 0x8000 else v)
    return offs


if __name__ == "__main__":
    print("### 224XL faithful boot on verified 8080 (POST run, PGM-2 bypass) ###")
    m, ms = boot()
    print("\nmilestones:", ms)
    if "prog_load" in ms:
        print("offset table 0x3F4D (first 12):", read_offsets(m, 12))
        print("reached program-load + mainloop -> WCS built. L2 OK.")
