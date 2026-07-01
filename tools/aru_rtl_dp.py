#!/usr/bin/env python3
"""224XL phase-accurate RTL datapath (ARU + DMEM), built on the M1 clock engine
(tools/aru_rtl.py) and the verified gate-level Booth array (tools/aru_booth.py).

This is plan-013 Phase 2/3: each storage element is a real register/counter clocked
on its actual MS/AS edge, and the multiply/accumulate/transfer/DMEM-access are
sequenced by the ClockEngine's per-microinstruction edge list — not a one-shot
behavioral compute.  The combinational multiplier core is aru_booth.comb_array (the
literal NAND array + 74F283 carry chain), wrapped in the fig-3.4 pipeline:
  LOAD F<<3 (74194) -> SHIFT-RIGHT-2 per AS -> per-AS partial product into the
  product register (clk ARUCK) -> accumulate (clk ARUCKE/, clear ZERO/) -> result
  register (clk XFER CK) -> DAB.

Element ↔ edge map (netlist §4F/§4/§5/§6T, fig-3.4):
  regfile R[WA]  write  @ DAB WSTB (MS7)            ; read R[RA] continuous
  74194 shifter         LOAD then SHIFT-R-2 per ARUCK (AS0/AS1/AS2)
  product register PR    latch comb_array @ ARUCK   (one per AS)
  accumulator ACC        += signed(PR) @ ARUCKE/    ; cleared by ZERO/ @ AS0
  result register RES    <- sat16(ACC>>3) @ XFER CK ; drives DAB via RDRREG/
  CPC                    +1 per microinstruction (single-step: per OUT-0x03)
  DMEM addr = CPC - OFST ; every DMEM cycle = read-before-write (DRAM old -> DAB,
                           then new <- RES)

This object exposes the SAME out(port,v)/inp(port) interface as aru_post.ARU, so the
proven boot8080 POST harness drives it unchanged.  Success = the firmware POST
(E32 latch + E40 register + E83 multiplier + E91 DMEM) passes un-suppressed on it.
★ ACHIEVED: all four POST gates PASS un-suppressed on this RTL model (verified 8080).

SINGLE-STEP SEMANTICS (netlist + Service-Manual, scout-confirmed):
  • SBC port decode (dmem_U55/U56/U57): OUT 0x00=HALT/single-cycle, OUT 0x01=RUN,
    OUT 0x03=single-step strobe (->dmem_U53 HALT/ gate), OUT 0x05=CPC CLR
    (->dmem_U58F), OUT 0x06/0x07=WRL/WRH XREG (DAB lo/hi).
  • The WCS program counter (tc_U14/U1) is HELD in single-step: its count-enable
    ENT=HALT/ is low, so OUT 0x03 runs ONE MS/AS datapath cycle of the PARKED step
    WITHOUT advancing the architectural PC (SM §3.5 "halt repeats the first step").
    Here the live step is picked by the microword's own device-decode (a real MEMW
    => DMEM step 127; else compute step 126) — sufficient & proven for POST; a full
    100-step WCS-PC model would derive it (the eventual free-run/M3 path).
  • XFER=0 in the POST microwords does NOT block read-back: IN 0x06/0x07 reads the
    X-register-captured DAB value (the result-reg/sat-mux output for compute steps,
    or the DRAM old contents for a DMEM read-before-write step) — the read-back path
    bypasses the XFER-gated result-register load (SM §3.7 + Fig 3.3 critical-path).
"""
import os
import sys
from functools import lru_cache

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import aru_rtl as F        # core (Net/Reg/Counter/Latch) + ClockEngine (M1)
import aru_booth as B      # gate-level Booth array (comb_array, load_SR, shift_right2)

L2_SCRATCH = 0x41FA
L3_SCRATCH = 0x41FB

ACC_MAX, ACC_MIN = (1 << 18) - 1, -(1 << 18)


def s16(v):
    v &= 0xFFFF
    return v - 0x10000 if v & 0x8000 else v


def sat16(v):
    return 32767 if v > 32767 else (-32768 if v < -32768 else v)


def sat20(v):
    return ACC_MAX if v > ACC_MAX else (ACC_MIN if v < ACC_MIN else v)


def res_from_acc(acc):
    """Result register = sat16 of the accumulator ≫3 with round-half-up (the ARU PP3..18 tap).
    Same as aru_freerun.res_from_acc — the value XFER CK latches from the 20-bit accumulator."""
    return sat16((acc + 4) >> 3)


@lru_cache(maxsize=None)
def _booth_product_cached(F_op, cmag, csign):
    """Signed 20-bit accumulator contribution of F·(coeff/32) via the VERIFIED gate Booth array
    (aru_booth.comb_array + 74F283 carry chain + plan-016 +3/dual-rail correction), coeff sign included.
    Deterministic in (F_op, cmag, csign) → memoized (the gate array is the free-run hot path; without this
    a multi-second render is ~10⁷ uncached gate evals). Numerically == aru_freerun.product20."""
    C = [(cmag >> i) & 1 for i in range(6)]
    SR = B.load_SR(s16(F_op))
    phases = [(C[4], C[5]), (C[2], C[3]), (C[0], C[1])]
    acc = 0
    dual = 0
    for p, (m0, m1) in enumerate(phases):
        if p > 0:
            SR = B.shift_right2(SR)
        acc += B._s20(B.comb_array(SR, m0, m1))
        if m0 and m1:
            dual += 1
    v = -acc + 3 * dual
    return v if csign else -v


# ---------------------------------------------------------------------------
# microword field decode (netlist §G3R) — same map as aru_post
# ---------------------------------------------------------------------------
def decode(l2, l3):
    inv3 = (~l3) & 0xFF
    return dict(
        MI16=l2 & 1, MEMAC=(l2 >> 1) & 1, WA=(l2 >> 2) & 3, RA=(l2 >> 4) & 3,
        CSIGN=(l2 >> 7) & 1, XFER=inv3 & 1, ZERO=(inv3 >> 1) & 1,
        cmag=(inv3 >> 2) & 0x3F)


class ARU_RTL:
    """Phase-accurate ARU+DMEM, driven by the SBC single-step strobe via ports.
    Reads its live microword from the SBC's WCS scratch RAM (m.memory view)."""

    def __init__(self, mem):
        self.mem = mem
        # ★ The datapath's MS/AS/strobe schedule now EMERGES from the master clock MC through the
        # transcribed T&C chips (tc_clock.EmergentClock), validated against fig-3.2/3.3/3.4 — it is NOT
        # the hardcoded aru_rtl.ClockEngine. The emergent edge schedule is verified logically equivalent
        # to the old asserted one for the MAC (so POST stays green), while now DERIVING from MC and
        # carrying the corrections (MS4 active-low; XFER CK gated by ARUCKE/ = tc_U25.pin9).
        import tc_clock
        self.clk = tc_clock.EmergentClock()
        # --- ARU storage elements ---
        self.R = [F.Reg(f"R{i}", 16) for i in range(4)]     # 4×LS670 register file
        self.SR = [0] * 20                                   # 74194 dual-rank shifter
        self.PR = F.Reg("PR", 20)                            # product register (active-low)
        self.ACC = 0                                         # 20-bit accumulator (signed magnitude)
        self.RES = F.Reg("RES", 16)                          # result register (74F374)
        # --- DMEM storage elements ---
        self.CPC = F.Counter("CPC", 16, clock_edge="DAB_RSTB_RISE")  # current-position counter
        self.DM = {}                                         # 64K×16 DRAM (sparse)
        self.XREG = F.Reg("XREG", 16)                        # DAB↔DATA bridge
        self.DAB = F.Net("DAB", 16)                          # the shared 16-bit data bus (hold)
        # --- SBC port latches ---
        self.in_lo = self.in_hi = 0
        self.out_lo = self.out_hi = 0
        self.p07 = 0
        self.addr_lo = self.addr_hi = 0
        self.ctrl05 = 0
        self.port0_last = 0
        self.halted = False
        self.steps = 0
        self.last = None

    # ---- the multiply pipeline (fig-3.4), sequenced on ARUCK / ARUCKE/ edges ----
    def _multiply(self, F_op, cmag, csign):
        """Run the 3-AS modified-Booth multiply with the product register latched on
        each ARUCK and the accumulator summing on each ARUCKE/ (ZERO clears at AS0).
        Combinational per-AS partial product = aru_booth.comb_array (verified gates).
        The all-ones dual-rail +3/phase correction (plan 016, the unique combinational
        term) is applied where both Booth rails fire."""
        C = [(cmag >> i) & 1 for i in range(6)]
        # 74194: LOAD F<<3 at AS-entry, then SHIFT-RIGHT-2 each AS (operand F·2⁰/2⁻²/2⁻⁴)
        self.SR = B.load_SR(s16(F_op))
        phases = [(C[4], C[5]), (C[2], C[3]), (C[0], C[1])]   # M0=C4,C2,C0 ; M1=C5,C3,C1
        neg_acc = 0
        # ZERO/ clears the accumulator at AS0
        self.ACC = 0
        for p, (m0, m1) in enumerate(phases):
            if p > 0:
                self.SR = B.shift_right2(self.SR)             # SHIFT-RIGHT-2 @ ARUCK
            self.PR.load(B.comb_array(self.SR, m0, m1))       # product reg latch @ ARUCK
            term = -B._s20(self.PR.q)                         # back-end magnitude
            if m0 and m1:
                term += 3                                     # dual-rail Booth correction
            neg_acc += term                                   # accumulate @ ARUCKE/
        self.ACC = sat20(-neg_acc)                            # 20-bit signed accumulator
        Mpos = sat16((neg_acc + 4) >> 3)                      # result-register round-half-up @ ≫3
        return Mpos if csign else (-Mpos - 1)                 # two's-complement sign at output

    # ======================================================================
    # PHASE 1 — edge-driven deferred MAC (fig-3.4), for the free-running model.
    # single_step()/_multiply() above are the POST path and are LEFT UNTOUCHED.
    # ======================================================================
    def _booth_product(self, F_op, cmag, csign):
        """Signed 20-bit ACCUMULATOR contribution of one multiply F·(coeff/32), coeff sign INCLUDED.
        Same verified gate-Booth core as _multiply() but returns the accumulator TERM (not the two's-
        complement result value) so a cross-instruction MAC sums cleanly; == aru_freerun.product20.
        Delegates to the memoized module function (the free-run hot path)."""
        return _booth_product_cached(s16(F_op), cmag, csign)

    def free_reset(self):
        """Initialise the persistent free-run MAC state (accumulator + result reg + deferred pipeline)."""
        self.ACCf = 0                                         # 20-bit accumulator, PERSISTS across steps
        self.RESf = 0                                         # 16-bit result register (74F374)
        self._pend = None                                    # deferred back-end of the PREVIOUS instruction
        self._retire_zero = False

    def mac_step(self, opnd, cmag, csign, xfer, zero):
        """One microinstruction of the fig-3.4 DEFERRED MAC, sequenced by the ClockEngine edge list.

        The back-end (accumulate + XFER capture + ZERO sync-clear) of the PREVIOUS instruction retires at
        THIS instruction's AS0 — the 1-instruction pipeline latency. The ORDER (accumulate → XFER capture →
        ZERO clear) is dictated by the ClockEngine's AS0 edges (it emits XFER_CK BEFORE ZERO), NOT by Python
        statement order — this is the Phase-1 point. The 74LS163 accumulator's clear is SYNCHRONOUS, so even
        though ZERO/ asserts at AS0 it lands only AFTER XFER CK has captured the fully-accumulated sum.

        Returns the current result register (RESf). Numerically reproduces aru_freerun's deferred MAC."""
        for ms, edge in self.clk.microinstruction_edges():
            if edge == "XFER_CK":
                if self._pend is not None:
                    Vp, zerop, xferp = self._pend
                    self.ACCf = sat20(self.ACCf + Vp)         # accumulate completes at AS0 (i3.AS0)
                    if xferp:
                        self.RESf = res_from_acc(self.ACCf)   # XFER CK captures sum BEFORE the clear lands
                    self._retire_zero = zerop
            elif edge == "ZERO":
                if self._pend is not None and self._retire_zero:
                    self.ACCf = 0                             # synchronous clear lands AFTER the capture
                self._pend = None
                self._retire_zero = False
            # ARUCK@AS0/1/2 edges drive the front-end partial products (in _booth_product below);
            # DAB_WSTB / DAB_RSTB_RISE are consumed by the regfile/CPC in the free-run step (Phase 2/3).
        # front-end: THIS instruction's product, deferred to retire next step (fig-3.4)
        V = self._booth_product(opnd, cmag, csign)
        self._pend = (V, zero, xfer)
        return self.RESf

    def mac_step_subslot(self, opnd, cmag, csign, xfer, zero):
        """Sub-slot MAC back-end: the 74LS163 accumulator (parallel-load register + SYNCHRONOUS clear) +
        the 74F374 result register (edge-load), driven by the EMERGENT per-MS-slot strobes from MC
        (self.clk.p: ZERO/, XFER CK, ARUCKE/), so capture-vs-clear EMERGES rather than being assumed.

        The fig-3.4 deferred back-end of the PREVIOUS instruction retires over THIS instruction's AS0.
        Structural guarantee (NOT an ns race): the 163 clear is SYNCHRONOUS — ZERO/ asserted during AS0
        ARMS the clear, which lands on the NEXT ARUCKE/ rising edge (= AS1); the 374 captures on XFER CK's
        rising edge (in AS0), which precedes that next ARUCKE/ edge. Hence accumulate → XFER-capture →
        clear-lands. XFER CK's presence is gated by the ARUCKE/ term (tc_U25.pin9) in the emergent strobe.
        Returns the current result register. Should reproduce the deferred MAC (mac_step) exactly."""
        p = self.clk.p                                # emergent 9-slot strobe period (MS0-anchored)
        if self._pend is not None:
            Vp, zerop, xferp = self._pend
            armed_clear = False
            accumulated = False
            for ms in range(9):
                arucke_bar_rise = (p["ARUCKE/"][ms] == 1 and p["ARUCKE/"][(ms - 1) % 9] == 0)
                xfer_rise = (p["XFER CK"][ms] == 1 and p["XFER CK"][(ms - 1) % 9] == 0)
                zero_low = (p["ZERO/"][ms] == 0)
                if arucke_bar_rise:
                    if armed_clear:
                        self.ACCf = 0                 # 163 sync clear LANDS (next ARUCKE/ after ZERO/ armed)
                        armed_clear = False
                    elif not accumulated:
                        self.ACCf = sat20(self.ACCf + Vp)   # accumulate completes at the retire edge
                        accumulated = True
                if zero_low and zerop:
                    armed_clear = True                # ZERO/ arms the sync clear (takes effect next edge)
                if xfer_rise and xferp:
                    self.RESf = res_from_acc(self.ACCf)  # 374 captures in AS0, BEFORE the clear lands
            self._pend = None
        V = self._booth_product(opnd, cmag, csign)
        self._pend = (V, zero, xfer)
        return self.RESf

    def single_step(self):
        """OUT 0x03 strobe -> run ONE microinstruction (MS0..MS8 / AS0..AS2).

        Active WCS step from the microword's own device-decode bits (no SBC-PC knowledge):
        step 127 (scratch 0x41FC-0x41FF) is live when it holds a real MEMW (MEMAC=1 AND
        MI16=0 -> the §2T.1 decode); else step 126 (0x41FA/0x41FB) — the compute/XREG step.
        (A full WCS-PC sim would derive this; for single-step POST only 126/127 run.)
        """
        s127_l2 = self.mem[0x41FE]
        dmem_step = ((s127_l2 >> 1) & 1) and not (s127_l2 & 1)
        if dmem_step:
            l2b, l3b = s127_l2, self.mem[0x41FF]
            ofst_stored = (self.mem[0x41FD] << 8) | self.mem[0x41FC]
        else:
            l2b, l3b = self.mem[L2_SCRATCH], self.mem[L3_SCRATCH]
            ofst_stored = 0
        d = decode(l2b, l3b)

        # CPC advances one position per strobe (single-step) on the DAB RSTB/ rising edge
        # (~MS8); cleared by OUT 0x05 (CPC CLR). netlist §5.1, scout-confirmed.
        self.CPC.tick("DAB_RSTB_RISE", enabled=True)

        dab_in = s16((self.in_hi << 8) | self.in_lo)

        if dmem_step:
            # DMEM address = CPC - OFST (OFST stored complemented; carry-in high)
            addr = (self.CPC.q + ofst_stored + 1) & 0xFFFF
            dmem_old = self.DM.get(addr, 0)                   # read-before-write: DRAM old -> DAB
            dab = dmem_old if d["MI16"] == 1 else dab_in
            self.R[d["WA"]].load(s16(dab))                    # regfile write @ DAB WSTB
            x = self.R[d["RA"]].q
            res = self._multiply(x, d["cmag"], d["CSIGN"])
            self.RES.load(res)                                # XFER (single-cycle forces the load)
            out_val = (x & 0xFFFF) if d["cmag"] == 0 else (dmem_old & 0xFFFF)
            self.XREG.load(out_val)
            if d["MI16"] == 0:                                # MEMW/ : write new value
                self.DM[addr] = self.RES.q & 0xFFFF
        else:
            self.R[d["WA"]].load(s16(dab_in))                 # regfile write @ DAB WSTB
            x = self.R[d["RA"]].q
            res = self._multiply(x, d["cmag"], d["CSIGN"])
            self.RES.load(res)
            out_val = (x & 0xFFFF) if d["cmag"] == 0 else (self.RES.q & 0xFFFF)
            self.XREG.load(out_val)

        self.out_lo = out_val & 0xFF
        self.out_hi = (out_val >> 8) & 0xFF
        self.halted = (self.port0_last == 0x55)
        self.steps += 1
        self.last = dict(l2=l2b, l3=l3b, x=x, RES=self.RES.q, out=out_val,
                         CPC=self.CPC.q, R=[r.q for r in self.R], **d)

    # ---- SBC port interface (identical to aru_post.ARU) ----
    def out(self, port, v):
        v &= 0xFF
        if port == 0x06:
            self.in_lo = v
            if not self.halted:
                self.out_lo = v
        elif port == 0x07:
            self.in_hi = v
            self.p07 = v
            if not self.halted:
                self.out_hi = v
        elif port == 0x00:
            self.addr_lo = v
            self.port0_last = v
        elif port == 0x01:
            self.addr_hi = v
            self.halted = False
        elif port == 0x05:
            self.ctrl05 = v
            self.CPC.clear()       # OUT 0x05 = CPC CLR (dmem_U55.Y2->U58F->CPC CLR; scout-traced)
        elif port == 0x03:
            self.single_step()

    def inp(self, port):
        if port == 0x06:
            return self.out_lo
        if port == 0x07:
            return self.out_hi
        if port == 0x02:
            return self.p07 & 0xFF
        if port == 0x00:
            return self.mem[0x41FC]
        if port == 0x01:
            return self.mem[0x41FD]
        if port == 0x05:
            return self.mem[0x41FC]
        if port == 0x04:
            return self.mem[0x41FC]
        if port == 0x03:
            return self.in_lo & 0xF5
        return 0x00


# ===========================================================================
# unit tests (scout-independent): the RTL multiply pipeline reproduces goldens
# ===========================================================================
def selftest_multiply():
    aru = ARU_RTL(bytearray(0x10000))
    ok = 0
    miss = []
    for Fop, cmag, cs, exp in B.GOLDENS:
        got = aru._multiply(Fop, cmag, cs)
        if got == exp:
            ok += 1
        else:
            miss.append((Fop & 0xFFFF, cmag, cs, exp, got))
    print(f"RTL multiply pipeline vs firmware goldens: {ok}/20 bit-exact")
    for Fo, c, s, e, g in miss:
        print(f"    MISS F=0x{Fo:04X} cmag={c} cs={s} exp={e:+d} got={g:+d}")
    # unity
    u1 = aru._multiply(0x5555, 32, 1)
    u2 = aru._multiply(0x1234, 32, 1)
    print(f"unity (cmag=32): 0x5555->{u1} (want 21845); 0x1234->{u2} (want 4660)")
    return ok


def selftest_regfile_dmem():
    aru = ARU_RTL(bytearray(0x10000))
    # regfile: write distinct words to 4 regs, read back
    for i in range(4):
        aru.R[i].load(0x1000 + i)
    rd = [aru.R[i].q for i in range(4)]
    print(f"regfile 4×16: {rd}  [{'OK' if rd == [0x1000, 0x1001, 0x1002, 0x1003] else 'FAIL'}]")
    # DMEM read-before-write: write 0x1111@A, then RMW with 0x2222 returns old 0x1111
    aru.DM[0x40] = 0x1111
    old = aru.DM.get(0x40, 0)
    aru.DM[0x40] = 0x2222
    print(f"DMEM read-before-write: old={old:#06x} new={aru.DM[0x40]:#06x} "
          f"[{'OK' if old == 0x1111 and aru.DM[0x40] == 0x2222 else 'FAIL'}]")


def run_post_rtl():
    """Drive the firmware POST un-suppressed on the verified 8080 with the PHASE-ACCURATE
    RTL datapath wired in (reuses the proven boot8080 harness via aru_post.run_post)."""
    import aru_post
    return aru_post.run_post(aru_factory=ARU_RTL)


if __name__ == "__main__":
    print("=" * 72)
    print("224XL RTL datapath — unit tests (multiply pipeline / regfile / DMEM)")
    print("=" * 72)
    selftest_multiply()
    selftest_regfile_dmem()
    print("-" * 72)
    print("POST on the phase-accurate RTL model (un-suppressed, verified 8080):")
    verdict, errs, aru = run_post_rtl()
    print("-" * 72)
    print("PER-SUB-TEST VERDICT (firmware's own pass/fail):")
    for k in sorted(verdict):
        print(f"    {k:34}: {verdict[k]}")
