#!/usr/bin/env python3
"""aru_freerun22 — free-run engine under the SESSION-0022 corrected coordinate system.

Session 0022 (docs/sessions/0022) proved, pin-level + 13/13-program data confirmation:
  • EXECUTION ORDER IS REVERSED: the SBC address lines are active-low (Multibus) and the WCS
    word-address mux (tc_U42/U28) is uncompensated, so CPU word k = physical row 127-k. The DSP
    executes CPU words 127, 126, ... down to the reset word (128-L). Words below = staging.
  • ALL FOUR LANES read through the Multibus data complement (lane 3 always did — ~l3):
      type = stored l2&3:  0=MEMR  1=MEMW  2=IO(tcWR)  3=idle
      IO command bits assert when the STORED bit == 0:
        bit3=RESET  bit4=DP  bit5=TEST  bit6=WR XREG  bit7=WR DA
        bits8-11 = SDA channels D,C,B,A (independent enables)
        DAB-source select = (~bits13..12)&3: 0=none 1=RDRREG 2=XREG 3=RD-AD
  • DELAY = the stored offset value DIRECTLY: addr = CPC - stored (the OFST/ bus lines carry the
    complement; the adder does CPC + line + 1). B55B's window [1447,6004] = 42-176 ms taps.
  • KEPT from the POST-anchored calibration (absolute anchors, remap-invariant or golden-checked):
    WA/RA stored-direct (pure slot relabeling — inert), CSIGN = stored l2 bit7 (E83 ±goldens 20/20),
    cmag/XFER/ZERO = ~l3 (same complement as always), deferred MAC + sync-clear capture-then-clear,
    RDRREG drives the DAB on MEMW steps, DAB bus-hold, regfile write every step.

The MAC arithmetic is imported from the verified stack (aru_booth via aru_freerun.product20).
Frame length L is program-defined (reset word); fs = 30.72 MHz / 9 / L.

Run:  python tools/aru_freerun22.py     (self-tests: decode, passthrough, feedback comb, CONCERT census)
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from aru_freerun import (product20, res_from_acc, fpc_input_float_to_fixed,
                         fpc_output_fixed_to_float)
from aru_rtl_dp import s16, sat16, sat20

MC_HZ = 30_720_000.0
MS_PER_STEP = 9

CHAN_BIT = {"A": 11, "B": 10, "C": 9, "D": 8}          # SDA = OFST11/..OFST8/ (reversed one-hot)
SRC_NONE, SRC_RDRREG, SRC_XREG, SRC_RDAD = 0, 1, 2, 3


def decode22(l0, l1, l2, l3):
    """Full corrected decode of one STORED word (CPU-byte domain)."""
    ofst = ((l1 << 8) | l0) & 0xFFFF
    inv3 = (~l3) & 0xFF
    d = {
        "typ": l2 & 3,                       # 0=MEMR 1=MEMW 2=IO 3=idle
        "WA": (l2 >> 2) & 3,                 # stored-direct (relabeling-inert, POST-calibrated)
        "RA": (l2 >> 4) & 3,
        "CSIGN": (l2 >> 7) & 1,              # 1 = positive (E83 golden-anchored)
        "XFER": inv3 & 1,
        "ZERO": (inv3 >> 1) & 1,
        "cmag": (inv3 >> 2) & 0x3F,
        "ofst": ofst,                        # delay/write offset = stored value DIRECTLY
    }
    if d["typ"] == 2:                        # IO command word: bits assert on stored==0
        bit = lambda n: ((ofst >> n) & 1) == 0
        d["RESET"] = bit(3)
        d["DP"] = bit(4)
        d["TEST"] = bit(5)
        d["WRX"] = bit(6)
        d["WRDA"] = bit(7)
        d["chans"] = [c for c, n in CHAN_BIT.items() if bit(n)]
        d["sel"] = ((((~ofst) >> 13) & 1) << 1) | (((~ofst) >> 12) & 1)
    return d


# ---------------------------------------------------------------------------
# Encoders (hand-built test programs in the NEW convention)
# ---------------------------------------------------------------------------
def _l3(cmag, xfer, zero):
    return (~((xfer & 1) | ((zero & 1) << 1) | ((cmag & 0x3F) << 2))) & 0xFF

def enc_memr(delay, wa=0, ra=0, cmag=0, csign=1, xfer=0, zero=0):
    l2 = 0 | ((wa & 3) << 2) | ((ra & 3) << 4) | ((csign & 1) << 7)
    return (delay & 0xFF, (delay >> 8) & 0xFF, l2, _l3(cmag, xfer, zero))

def enc_memw(offset, wa=0, ra=0, cmag=0, csign=1, xfer=0, zero=0):
    l2 = 1 | ((wa & 3) << 2) | ((ra & 3) << 4) | ((csign & 1) << 7)
    return (offset & 0xFF, (offset >> 8) & 0xFF, l2, _l3(cmag, xfer, zero))

def enc_idle(wa=0, ra=0, cmag=0, csign=1, xfer=0, zero=0):
    l2 = 3 | ((wa & 3) << 2) | ((ra & 3) << 4) | ((csign & 1) << 7)
    return (0xFF, 0xFF, l2, _l3(cmag, xfer, zero))

def enc_io(sel=SRC_NONE, wrda=False, chans="", reset=False, wrx=False,
           wa=0, ra=0, cmag=0, csign=1, xfer=0, zero=0):
    ofst = 0xFFFF                                        # all command lines deasserted (stored 1s)
    if reset:
        ofst &= ~(1 << 3)
    if wrx:
        ofst &= ~(1 << 6)
    if wrda:
        ofst &= ~(1 << 7)
    for c in chans:
        ofst &= ~(1 << CHAN_BIT[c])
    ofst = (ofst & ~(3 << 12)) | ((((~sel) & 3)) << 12)  # stored sel bits = complement of value
    l2 = 2 | ((wa & 3) << 2) | ((ra & 3) << 4) | ((csign & 1) << 7)
    return (ofst & 0xFF, (ofst >> 8) & 0xFF, l2, _l3(cmag, xfer, zero))


# ---------------------------------------------------------------------------
# Program extraction: reversed window, reset-terminated
# ---------------------------------------------------------------------------
def program_from_wcs(wcs):
    """wcs = 128 stored (l0,l1,l2,l3) tuples (CPU word order). Returns (prog, L, w_reset):
    prog = the executed sequence, words 127 down to the reset word inclusive."""
    firing = [k for k, (l0, l1, l2, l3) in enumerate(wcs)
              if (l2 & 3) == 2 and ((l0 >> 3) & 1) == 0]
    if not firing:
        raise ValueError("no reset microword found (IO-typed with stored bit3==0)")
    w_reset = max(firing)
    L = 128 - w_reset
    if any(w_reset < k for k in firing):
        raise ValueError("multiple resets in the executed window")
    prog = [wcs[k] for k in range(127, w_reset - 1, -1)]
    return prog, L, w_reset


def fs_for(L):
    return MC_HZ / MS_PER_STEP / L


# ---------------------------------------------------------------------------
# The engine (state + semantics mirror aru_freerun.FreeRunARU; only the decode differs)
# ---------------------------------------------------------------------------
class FreeRun22:
    def __init__(self, fpc_enabled=False, csign_invert=False, immediate_backend=False):
        self.R = [0, 0, 0, 0]
        self.ACC = 0
        self.RES = 0
        self.DAB = 0
        self.DM = {}
        self.CPC = 0
        self.XREG = 0
        self.pend = None                    # (product, ZERO, XFER) retired next step
        self.fpc_enabled = fpc_enabled
        self.csign_invert = csign_invert            # probe: global coefficient-sign flip
        self.immediate_backend = immediate_backend  # probe: MAC retires same-step (vs fig-3.4 deferred)
        self.step_count = 0
        self.sample_count = 0

    def step(self, w, audio_in, probe=None):
        l0, l1, l2, l3 = w
        d = decode22(l0, l1, l2, l3)

        # (1) retire the previous instruction's deferred back-end (accumulate -> XFER capture -> sync clear)
        if not self.immediate_backend and self.pend is not None:
            Vp, zerop, xferp = self.pend
            self.ACC = sat20(self.ACC + Vp)
            if xferp:
                self.RES = res_from_acc(self.ACC)
            if zerop:
                self.ACC = 0

        # (2) operand read before the regfile write
        opnd = self.R[d["RA"]]
        if self.immediate_backend:
            # session-9 owner correction variant: this step's MAC lands before the DAB/consume phase
            V = product20(opnd, d["cmag"], d["CSIGN"] ^ (1 if self.csign_invert else 0))
            self.ACC = sat20(self.ACC + V)
            if d["XFER"]:
                self.RES = res_from_acc(self.ACC)
            if d["ZERO"]:
                self.ACC = 0

        # (3) DMEM address: addr = CPC - stored offset (delay = stored value directly)
        addr = (self.CPC - d["ofst"]) & 0xFFFF

        # (4) drive the DAB (one driver, else hold)
        typ = d["typ"]
        out_da = []
        if typ == 0:                                        # MEMR
            self.DAB = self.DM.get(addr, 0) & 0xFFFF
        elif typ == 1:                                      # MEMW: RDRREG drives the DAB
            self.DAB = self.RES & 0xFFFF
        elif typ == 2:                                      # IO: source per sel
            sel = d["sel"]
            if sel == SRC_RDRREG:
                self.DAB = self.RES & 0xFFFF
            elif sel == SRC_RDAD:
                self.DAB = (fpc_input_float_to_fixed(audio_in) if self.fpc_enabled
                            else (audio_in & 0xFFFF))
            elif sel == SRC_XREG:
                self.DAB = 0                                # host bridge; 8080 writes nothing in free-run
            # SRC_NONE: bus hold
        # typ 3 idle: bus hold

        # (5) consume the DAB
        self.R[d["WA"]] = s16(self.DAB)                     # regfile write every step (¬MS7)
        if typ == 1:
            self.DM[addr] = self.DAB & 0xFFFF               # DIN = DAB (= RES via RDRREG)
        if typ == 2:
            if d["WRX"]:
                self.XREG = self.DAB & 0xFFFF
            if d["WRDA"]:
                ov = (fpc_output_fixed_to_float(self.DAB) if self.fpc_enabled
                      else s16(self.DAB))
                out_da = [(c, ov) for c in d["chans"]]

        # (6) this instruction's product, deferred one step (unless immediate_backend already applied it)
        if not self.immediate_backend:
            self.pend = (product20(opnd, d["cmag"], d["CSIGN"] ^ (1 if self.csign_invert else 0)),
                         d["ZERO"], d["XFER"])
        self.step_count += 1
        if probe is not None:
            probe.append(dict(d=d, addr=addr, dab=self.DAB, opnd=opnd,
                              ACC=self.ACC, RES=self.RES, out_da=out_da))
        return out_da

    def run_sample(self, prog, audio_in, probe=None):
        outs = []
        for w in prog:
            outs.extend(self.step(w, audio_in, probe=probe))
        self.CPC = (self.CPC + 1) & 0xFFFF                  # CPC counts on the frame RESET event
        self.sample_count += 1
        return outs

    def run_free(self, prog, input_signal, n_samples):
        """input_signal: list/array or callable(n)->int16. Returns dict chan -> list of int16
        (per-frame last-write-wins; unwritten frame -> 0)."""
        chans = {c: [0] * n_samples for c in "ABCD"}
        get = input_signal if callable(input_signal) else (lambda n: input_signal[n] if n < len(input_signal) else 0)
        for n in range(n_samples):
            for c, v in self.run_sample(prog, int(get(n)) & 0xFFFF):
                chans[c][n] = v
        return chans


# ---------------------------------------------------------------------------
# Self-tests
# ---------------------------------------------------------------------------
def _test_decode_roundtrip():
    w = enc_io(sel=SRC_RDAD, wrda=True, chans="AC", reset=True, wa=1, ra=2, cmag=32)
    d = decode22(*w)
    assert d["typ"] == 2 and d["sel"] == SRC_RDAD and d["WRDA"] and d["RESET"]
    assert sorted(d["chans"]) == ["A", "C"] and d["WA"] == 1 and d["RA"] == 2 and d["cmag"] == 32
    d = decode22(*enc_memr(0x1234, cmag=16))
    assert d["typ"] == 0 and d["ofst"] == 0x1234 and d["cmag"] == 16
    d = decode22(*enc_memw(0x0002))
    assert d["typ"] == 1 and d["ofst"] == 2
    assert decode22(*enc_idle())["typ"] == 3
    print("  decode22 roundtrip           OK")


def _test_passthrough():
    prog = [
        enc_io(sel=SRC_RDAD, wa=1, cmag=0, zero=1),          # DAB=in; R1<-in; pend(0,ZERO)
        enc_idle(ra=1, cmag=32, xfer=1),                     # pend(in*1.0, XFER); retire clears ACC
        enc_idle(),                                          # retire: ACC=in*8; XFER -> RES=in
        enc_io(sel=SRC_RDRREG, wrda=True, chans="A", reset=True),
    ]
    eng = FreeRun22()
    xs = [1000, -2000, 12345, -30000, 0, 7]
    ys = [dict(eng.run_sample(prog, x & 0xFFFF)).get("A", 0) for x in xs]
    assert ys == xs, f"passthrough mismatch: {ys} vs {xs}"
    print("  zero-delay passthrough       OK (out == in, same frame)")


def _test_feedback_comb(D=40, n=200):
    prog = [
        enc_io(sel=SRC_RDAD, wa=0, cmag=0, zero=1),          # R0<-x; pend(0,ZERO)
        enc_memr(D, wa=1, ra=0, cmag=32),                    # DAB=y[n-D]; R1<-y[n-D]; pend x*1.0
        enc_idle(ra=1, cmag=16, xfer=1),                     # pend 0.5*y[n-D] +XFER; retire: ACC=x
        enc_idle(),                                          # retire: ACC=x+0.5y; XFER -> RES
        enc_memw(0x0000),                                    # DM[CPC] <- RES  (y[n])
        enc_io(sel=SRC_RDRREG, wrda=True, chans="A", reset=True),
    ]
    eng = FreeRun22()
    out = []
    for i in range(n):
        x = 16000 if i == 0 else 0
        out.append(dict(eng.run_sample(prog, x & 0xFFFF)).get("A", 0))
    peaks = [(i, v) for i, v in enumerate(out) if abs(v) > 50]
    exp = [(0, 16000), (D, 8000), (2 * D, 4000), (3 * D, 2000), (4 * D, 1000)]
    for (pi, pv), (ei, ev) in zip(peaks, exp):
        assert pi == ei and abs(pv - ev) <= 8, f"comb peak {(pi, pv)} != {(ei, ev)}"
    assert len(peaks) >= 5, f"too few comb echoes: {peaks}"
    print(f"  feedback comb (D={D}, g=0.5)  OK ({[(i, v) for i, v in peaks[:5]]})")


def _test_concert_extraction():
    import json
    cand = [os.path.join(os.environ.get("E1_CACHE_DIR", ""), "wcs_cache.json")]
    cand = [p for p in cand if p and os.path.exists(p)]
    if not cand:
        print("  CONCERT extraction           SKIPPED (no wcs_cache.json; set E1_CACHE_DIR)")
        return
    rec = json.load(open(cand[0]))["1"]
    b = bytes.fromhex(rec["wcs"])
    wcs = [(b[4 * k], b[4 * k + 1], b[4 * k + 2], b[4 * k + 3]) for k in range(128)]
    prog, L, w_reset = program_from_wcs(wcs)
    types = [decode22(*w)["typ"] for w in prog]
    cnt = {t: types.count(t) for t in range(4)}
    assert (L, w_reset) == (104, 24), (L, w_reset)
    assert (cnt[0], cnt[1], cnt[2], cnt[3]) == (55, 36, 10, 3), cnt
    last = decode22(*prog[-1])
    assert last["typ"] == 2 and last["RESET"] and last["WRDA"] and last["chans"] == ["C"]
    print(f"  CONCERT extraction           OK (L={L}, reset word {w_reset}, "
          f"census MEMR/MEMW/IO/idle = {cnt[0]}/{cnt[1]}/{cnt[2]}/{cnt[3]}, fs={fs_for(L):.1f} Hz)")


if __name__ == "__main__":
    print("### aru_freerun22 self-tests (session-0022 decode) ###")
    _test_decode_roundtrip()
    _test_passthrough()
    _test_feedback_comb()
    _test_concert_extraction()
    print("ALL PASS")
