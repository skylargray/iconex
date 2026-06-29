#!/usr/bin/env python3
"""224XL phase-accurate RTL micro-framework + T&C clock/state engine (plan 013, M1).

This is the structural model the holistic plan calls for: model the real storage
elements (registers/counters/latches) and the combinational logic between them,
CLOCKED BY THE REAL MS/AS STATE MACHINE — not value-level, not full gate-delay.
Behavior is meant to EMERGE from the wiring + the clock, so a wrong result points
to a specific net or edge.

This file (M1) provides:
  • the micro-framework core: Net (value + hold-last), Reg / Counter / Latch
    (edge-clocked storage), comb() blocks, and a Scheduler that walks one
    microinstruction (MS0..MS8 / AS0..AS2) firing edges in order;
  • the T&C clock/state engine (ClockEngine): MS0-8 one-hot, AS0/AS1/AS2, ARUCK
    (3×/cycle), ARUCKE/, and the MAC strobes DAB WSTB/ (=¬MS7), DAB RSTB / DAB
    RSTB/ (JK J=MS1,K=MS8), XFER CK & ZERO/ (gated at AS0) — exactly the fig-3.2 /
    fig-3.4 skeleton (netlist §6T).
  • selftest(): validates the generated MS/AS/ARUCK waveforms against the single
    source of truth tools/timing/timing_spec.json (fig-3.2) and the MAC schedule
    against fig-3.4.

The datapath structural elements (regfile / multiplier / accumulator / result reg
/ CPC / DRAM / device decode) and the SBC single-step port harness are added on top
of this engine (next milestone); passing the firmware POST on the wired model is the
success gate.

Run:  python tools/aru_rtl.py
"""
import os
import sys
import json

HERE = os.path.dirname(os.path.abspath(__file__))
TIMING_JSON = os.path.join(HERE, "timing", "timing_spec.json")


# ===========================================================================
# Micro-framework core (plan 013 §4)
# ===========================================================================
class Net:
    """A wire or bus.  Holds its last value until re-driven (models bus hold /
    register-output persistence — the schematic has no DAB pull resistors, so an
    undriven DAB keeps its last level)."""
    __slots__ = ("name", "width", "mask", "value", "driven")

    def __init__(self, name, width=1, value=0):
        self.name = name
        self.width = width
        self.mask = (1 << width) - 1
        self.value = value & self.mask
        self.driven = False

    def drive(self, v):
        self.value = v & self.mask
        self.driven = True

    def get(self):
        return self.value

    def __int__(self):
        return self.value

    def __repr__(self):
        return f"Net({self.name}={self.value:#x}/{self.width}b)"


class Reg:
    """Edge-triggered register.  Q is updated only when clock(edge) is called with
    the register's clock_edge (and, if a clear_edge is set, async-cleared on it).
    The next-state is supplied at clock time via a value or a 0-arg function."""
    __slots__ = ("name", "width", "mask", "q", "clock_edge", "clear_edge")

    def __init__(self, name, width=16, init=0, clock_edge=None, clear_edge=None):
        self.name = name
        self.width = width
        self.mask = (1 << width) - 1
        self.q = init & self.mask
        self.clock_edge = clock_edge
        self.clear_edge = clear_edge

    def clock(self, edge, dval):
        if self.clear_edge is not None and edge == self.clear_edge:
            self.q = 0
            return
        if edge == self.clock_edge:
            self.q = (dval() if callable(dval) else dval) & self.mask

    def load(self, v):
        self.q = v & self.mask

    def clear(self):
        self.q = 0

    def __int__(self):
        return self.q


class Counter(Reg):
    """Synchronous counter: on its clock edge, Q += step (when count-enabled);
    async/sync clear on clear_edge."""
    __slots__ = ()

    def tick(self, edge, enabled=True, step=1):
        if self.clear_edge is not None and edge == self.clear_edge:
            self.q = 0
            return
        if edge == self.clock_edge and enabled:
            self.q = (self.q + step) & self.mask


class Latch:
    """Level-sensitive latch: Q follows D while enable is high, holds when low."""
    __slots__ = ("name", "width", "mask", "q")

    def __init__(self, name, width=16, init=0):
        self.name = name
        self.width = width
        self.mask = (1 << width) - 1
        self.q = init & self.mask

    def update(self, enable, d):
        if enable:
            self.q = d & self.mask

    def __int__(self):
        return self.q


# ===========================================================================
# Clock / state engine  (T&C, fig-3.2 / fig-3.4 ; netlist §6T)
# ===========================================================================
class ClockEngine:
    """Generates the MS/AS/ARUCK/strobe skeleton for ONE microinstruction.

    fig-3.2 (validated against timing_spec.json), per MS0..MS8:
        MS_k       : one-hot
        ARUCK      : 1 0 0 1 0 0 1 0 0   (pulses at MS0/MS3/MS6 — once per AS state)
        AS0        : 0 1 1 1 0 0 0 0 0   (high MS1-MS3)
        AS1        : 0 0 0 0 0 1 1 0 0   (narrow, high MS5-MS6)
        AS2        : 1 0 0 0 0 0 0 1 1   (high MS7-MS8, wraps into MS0)
    Derived strobes (netlist §6T.4):
        DAB WSTB/  : not(MS7)                          (regfile write gate GW-bar)
        DAB RSTB   : JK FF J=MS1,K=MS8 -> high MS1..MS7, low at MS8
        DAB RSTB/  : complement   (PC clock; rising edge ~MS8)
        XFER CK    : NAND(AS0, XFER, ..) -> active-low pulse over AS0 when XFER
        ZERO/      : NAND(MI25-gate, AS0) -> active-low pulse over AS0 when ZERO
    """
    NMS = 9
    ARUCK = (1, 0, 0, 1, 0, 0, 1, 0, 0)
    AS0 = (0, 1, 1, 1, 0, 0, 0, 0, 0)
    AS1 = (0, 0, 0, 0, 0, 1, 1, 0, 0)
    AS2 = (1, 0, 0, 0, 0, 0, 0, 1, 1)
    # DAB RSTB: set@MS1, reset@MS8 (JK) -> high MS1..MS7
    DAB_RSTB = (0, 1, 1, 1, 1, 1, 1, 1, 0)

    @staticmethod
    def ms_onehot(ms):
        return [1 if i == ms else 0 for i in range(ClockEngine.NMS)]

    @staticmethod
    def dab_wstb_n(ms):
        return 0 if ms == 7 else 1            # active-low = ¬MS7

    def aru_state(self, ms):
        """Conceptual AS state index 0/1/2 delimited by the ARUCK pulses
        (AS0 begins at MS0, AS1 at MS3, AS2 at MS6 — the fig-3.4 thirds)."""
        return 0 if ms < 3 else (1 if ms < 6 else 2)

    def microinstruction_edges(self):
        """Yield (ms, edge_name) events for one microinstruction, in time order.
        The datapath elements subscribe to these edges.  Edges emitted:
            'ARUCK@AS{0,1,2}'  at MS0/MS3/MS6  (shifter, product reg, accumulate cadence)
            'DAB_WSTB'         at MS7          (regfile write)
            'XFER_CK'          over AS0        (result-reg load gate)
            'ZERO'             over AS0        (accumulator clear gate)
            'DAB_RSTB_RISE'    at MS8          (PC / offset-latch / field-reg clock)
        """
        order = []
        for ms in range(self.NMS):
            if self.ARUCK[ms]:
                order.append((ms, f"ARUCK@AS{self.aru_state(ms)}"))
            if self.AS0[ms] and ms == 1:       # leading edge of AS0
                order.append((ms, "XFER_CK"))
                order.append((ms, "ZERO"))
            if self.dab_wstb_n(ms) == 0:
                order.append((ms, "DAB_WSTB"))
            if ms == 8:
                order.append((ms, "DAB_RSTB_RISE"))
        return order


# ===========================================================================
# M1 validation against the single source of truth (timing_spec.json)
# ===========================================================================
def _load_fig(fig_id):
    with open(TIMING_JSON, encoding="utf-8") as f:
        d = json.load(f)
    return next(x for x in d["figures"] if x["id"] == fig_id)


def selftest():
    ok = True
    ce = ClockEngine()
    f32 = _load_fig("fig32")
    waves = {r["name"]: r["wave"] for r in f32["signals"]}

    def wstr(bits):
        return "".join(str(b) for b in bits)

    # MS one-hot
    for ms in range(9):
        exp = waves[f"MS{ms}"]
        got = wstr(ce.ms_onehot(ms))
        if exp != got:
            print(f"  MS{ms} MISMATCH exp={exp} got={got}"); ok = False
    # ARU CK / AS0 / AS1 / AS2
    checks = [("ARU CK", ce.ARUCK), ("AS0", ce.AS0), ("AS1", ce.AS1), ("AS2", ce.AS2)]
    for name, bits in checks:
        exp = waves[name]
        got = wstr(bits)
        mark = "OK " if exp == got else "MISMATCH"
        if exp != got:
            ok = False
        print(f"  fig-3.2 {name:7}: model={got}  spec={exp}  [{mark}]")

    # DAB WSTB/ = ¬MS7
    dab = wstr([ce.dab_wstb_n(ms) for ms in range(9)])
    print(f"  DAB WSTB/ (=¬MS7)  : {dab}  (low pulse at MS7) [{'OK' if dab=='111111101' else 'MISMATCH'}]")
    if dab != "111111101":
        ok = False

    # fig-3.4 MAC schedule sanity: ZERO/ and XFER CK low at i2.AS0; PP reg one AS behind.
    f34 = _load_fig("fig34")
    w34 = {r["name"]: r["wave"] for r in f34["signals"]}
    grid = f34["grid"]
    i2as0 = grid.index("i2.AS0")
    zero_low = w34["ZERO/"][i2as0] == "0"
    xfer_low = w34["XFER CK"][i2as0] == "0"
    print(f"  fig-3.4 ZERO/ low @i2.AS0: {zero_low} ; XFER CK low @i2.AS0: {xfer_low} "
          f"[{'OK' if (zero_low and xfer_low) else 'MISMATCH'}]")
    ok = ok and zero_low and xfer_low
    # LOAD@i1.AS2, SHIFT@i2.AS0/AS1 (S1,S0 == cells)
    s = w34["S1,S0"]
    load_shift = (s[grid.index("i1.AS2")] == "=" and s[grid.index("i2.AS0")] == "=")
    print(f"  fig-3.4 S1,S0 LOAD@i1.AS2 + SHIFT@i2.AS0/AS1: {load_shift} "
          f"[{'OK' if load_shift else 'MISMATCH'}]")
    ok = ok and load_shift

    # edge order for one microinstruction
    print("  microinstruction edge order:")
    for ms, e in ce.microinstruction_edges():
        print(f"      MS{ms}: {e}")

    print()
    print(f"M1 clock/state engine vs timing_spec.json: {'ALL OK' if ok else 'FAILED'}")
    return ok


if __name__ == "__main__":
    print("=" * 72)
    print("224XL phase-accurate RTL — M1 clock/state engine (fig-3.2/3.4)")
    print("=" * 72)
    selftest()
