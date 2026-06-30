#!/usr/bin/env python3
"""Boot 224XL v8.2.1 to CONCERT on the CLEAN-ROOM tools/i8080_ref.I8080 core (plan 019 Phase 2c).

A faithful port of tools/boot8080.boot's driver logic (8251 serial model, power-up handshake, RST-7
serial interrupt by hand, PGM-2 'skip diagnostics' bypass) onto the independent ref core. Reaching
mainloop here and reading 0x4000 lets us cross-validate the WCS — especially the reverb-critical
lane-3 coefficients — on a second 8080 that does NOT share the kosarev implementation.

Timing is in INSTRUCTIONS (the ref core counts instructions, not clock ticks); the few delays only
need to be 'long enough for the firmware to settle into its wait loop', so generous instruction
thresholds are used and confirmed empirically by reaching mainloop.
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from i8080_ref import I8080
import boot8080 as B          # reuse load_mem() + milestone PCs

HANDSHAKE = B.HANDSHAKE       # 0x0089
DIAG_E    = B.DIAG_E          # 0x021D
DIAG_H    = B.DIAG_H          # 0x0217
NORMAL_OP = B.NORMAL_OP       # 0x813B
PROG_LOAD = B.PROG_LOAD       # 0x13B6
MAINLOOP  = B.MAINLOOP        # 0x8169
PGM2_PRESS, PGM2_RELEASE = B.PGM2_PRESS, B.PGM2_RELEASE   # 0x30 / 0x10

MILE = {HANDSHAKE: "handshake", DIAG_E: "DIAG_E", DIAG_H: "DIAG_H",
        NORMAL_OP: "normal_op", PROG_LOAD: "prog_load", MAINLOOP: "mainloop"}

# instruction-count analogues of boot8080's tick thresholds
HANDSHAKE_DELAY = 1500        # deliver power-up 0xC8 this many instrs after the 0xE0 request
DIAG_SETTLE     = 700_000     # inject PGM-2 this many instrs after the diagnostic error appears
SERVICE_EVERY   = 400         # run the serial/interrupt service every N instructions


def boot(verbose=True, hw_stub=None, max_instr=80_000_000, snapshot_at=None):
    """Boot to mainloop on the ref core. Returns (cpu, milestones). If snapshot_at is a PC, also
    returns the full state captured the first time that PC is reached (for diagnostics)."""
    cpu = I8080()
    cpu.memory[:] = B.load_mem()
    cpu.pc = 0

    st = {"rx": [], "rx_at": 0, "tx": [], "tx_en": True, "ei": False,
          "diag": None, "phase": 0}

    def rx_ready():
        return bool(st["rx"]) and cpu.instr_count >= st["rx_at"]

    def on_input(port):
        p = port & 0xFF
        if p == 0xEF:
            return 0x01 | (0x02 if rx_ready() else 0)
        if p == 0xEE:
            return st["rx"].pop(0) if rx_ready() else 0xFF
        if p in (0x06, 0x07):
            return 0xFF if hw_stub is None else (hw_stub & 0xFF)
        return 0x00 if hw_stub is None else (hw_stub & 0xFF)

    def on_output(port, v):
        p = port & 0xFF
        if p == 0xEE:
            st["tx"].append(v & 0x7F)
            if v == 0xE0 and not st["rx"]:
                st["rx"].append(0xC8); st["rx_at"] = cpu.instr_count + HANDSHAKE_DELAY
        elif p == 0xEF and v != 0xCE:
            st["tx_en"] = bool(v & 0x01)

    cpu.in_cb = on_input
    cpu.out_cb = on_output

    seen = {}
    snap = {}

    nxt_service = SERVICE_EVERY
    while cpu.instr_count < max_instr:
        pc = cpu.pc
        if pc in MILE and pc not in seen:
            seen[pc] = cpu.instr_count
            if verbose:
                print(f"  ~{cpu.instr_count:>11} instr: {MILE[pc]}")
            if pc == HANDSHAKE:
                st["ei"] = True
            if pc in (DIAG_E, DIAG_H) and st["diag"] is None:
                st["diag"] = cpu.instr_count
            if pc == MAINLOOP and PROG_LOAD in seen:
                break
        if snapshot_at is not None and pc == snapshot_at and not snap:
            snap = _grab(cpu)

        cpu.step()

        if cpu.instr_count >= nxt_service:
            nxt_service = cpu.instr_count + SERVICE_EVERY
            # fire the RST-7 serial interrupt when the firmware is ready for it
            if st["ei"] and (st["tx_en"] or rx_ready()) and cpu.iff:
                cpu.request_interrupt(0x38)
            # PGM-2 'skip diagnostics' bypass, once the diagnostic error has settled
            if st["diag"] and cpu.instr_count > st["diag"] + DIAG_SETTLE:
                if st["phase"] == 0:
                    st["rx"].append(PGM2_PRESS); st["rx_at"] = cpu.instr_count; st["phase"] = 1
                elif st["phase"] == 1 and not st["rx"]:
                    st["rx"].append(PGM2_RELEASE); st["rx_at"] = cpu.instr_count; st["phase"] = 2

    if verbose:
        tx = "".join(chr(c) if 32 <= c < 127 else "." for c in st["tx"])
        print(f"  final PC=0x{cpu.pc:04X}  instr={cpu.instr_count}  LARC tail: {tx[-48:]!r}")
    ms = {MILE[a]: t for a, t in seen.items()}
    return (cpu, ms, snap) if snapshot_at is not None else (cpu, ms)


def _grab(cpu):
    return dict(a=cpu.a, b=cpu.b, c=cpu.c, d=cpu.d, e=cpu.e, h=cpu.h, l=cpu.l,
                sp=cpu.sp, pc=cpu.pc, f=cpu.get_psw(), iff=cpu.iff,
                mem=bytes(cpu.memory))


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    print("### 224XL boot on the CLEAN-ROOM ref 8080 (POST run, PGM-2 bypass) ###")
    cpu, ms = boot()
    print("\nmilestones:", ms)
    if "mainloop" in ms and "prog_load" in ms:
        print("reached program-load + mainloop -> WCS built on the independent core.")
        print("0x4000[:16]:", bytes(cpu.memory[0x4000:0x4010]).hex())
    else:
        print("DID NOT reach mainloop — adjust serial/interrupt timing.")
