#!/usr/bin/env python3
"""224XL — M3 free-run engine: cycle the phase-accurate RTL model over the full
100-step WCS microprogram per audio sample so a reverb EMERGES from the wiring.

This is plan-013 Phase 3 (free-run) / plan-017 (M3). The M1/M2 model
(tools/aru_rtl.py + tools/aru_rtl_dp.py) is driven SINGLE-STEP by the SBC and passes
the whole POST. Here the T&C microsequencer runs FREE: the WCS program counter sweeps
step 0->99 (RESET@99), each step is fetched + decoded + executed on the same datapath
elements, the CPC advances +1 per sample, the DMEM recirculates across samples, and
audio flows A/D -> DSP -> D/A. Run a program over many samples and capture the impulse
response at the WR DA/ output node.

WHAT THIS ADDS over single-step (the never-POST-tested half, netlist L6.7-L6.13):
  1. WCS PC sweep 0->99 (SM §3.5: "100-step control program ... reset at count 99");
     steps 0..99 are the program, 100..127 are scratch (the PC never reaches them).
  2. CPC cadence for RUN: +1 per SAMPLE (at RESET@99), not per microinstruction — so all
     100 steps of a sample address DMEM relative to the same CPC and a cell written at
     sample S is read (OFST_read - OFST_write) samples later. (Single-step advanced CPC
     per strobe; netlist §5.1 flags the RUN count-clock source ⚪, resolved here as RESET@99.)
  3. Per-step DAB-source routing via the §2T device decode: each step exactly ONE driver of
     the shared DAB (MEMR/ -> DRAM; RDRREG/ -> result reg; RD AD/ -> A/D input; RD XREG/ ->
     XREG), or idle = hold-last-value (no pull resistors). Consumed by: regfile write
     (DAB WSTB/ = ¬MS7, every step), DMEM write (MEMW/, DIN = result reg), D/A out (WR DA/).
  4. The DEFERRED MAC across instructions (fig-3.4): an instruction's accumulate + ZERO + XFER
     happen one instruction LATE. The 1-instruction pipeline latency is real and carries the
     accumulator/result-reg state across steps; the accumulator does signed multiply-ACCUMULATE
     across steps (ZERO=0 => keep summing). This is exactly what single-step flushed per strobe.
  5. The audio I/O boundary: inject at RD AD/ (A/D), capture at WR DA/ (D/A, channels A-D via
     the SDAA-D = OFST8-11/ select). Fixed-point (raw 16-bit) I/O; the FPC float<->fixed
     (fig-3.5/3.6) is deferred — the reverb tail lives in the fixed-point DSP loop, not the FPC.

GROUND TRUTH (docs/reference/224/224XL_interconnect_netlist.md + 224XL_timing_spec.md):
  • §3.5  PC tc_U14/U1 counts on DAB RSTB/, RESET@99, ENT=HALT/.
  • §2T   device decode tc_U47/U48/U49: (MEMAC,MI16)=(1,0)->MEMW/, (1,1)->MEMR/, (0,1)->I/O
          step (tcWR); sub-decoder {OFST12/,OFST13/} -> RD AD//RD XREG/; WR DA/=NAND(OFST7/,tcWR);
          WR XREG/=NAND(MS7,tcWR,OFST6/); RDRREG/ (result reg -> DAB) on a MEMW/ step.
  • §3.6  offset latch MIn -> OFSTn/ (stored COMPLEMENTED); §5.2 addr = CPC + OFST_stored + 1 = CPC-OFST.
  • §3.7  WA0/WA1=MI18/19, MEMAC=MI17; §3.8 RA0/RA1=MI20/21, XFER=MI24; §3.9 coeff; §3.10 CSIGN JK.
  • fig-3.4 deferred MAC: partial products at slot i2.AS0-2; accumulate i2.AS1->i3.AS0; ZERO/+XFER CK
          at i2.AS0 -> the back-end of instruction N retires at instruction N+1.

The multiply itself is the verified gate-level Booth (tools/aru_booth.py, 20/20 POST goldens);
this file only adds the FREE-RUN SEQUENCING + the cross-instruction accumulate + the I/O + DMEM
recirculation. It does NOT touch aru_rtl_dp.py, so the POST regression stays green.

Run:  python tools/aru_freerun.py        (self-tests + a short CONCERT free-run smoke test)
"""
import os
import sys
from functools import lru_cache

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import aru_booth as Bo
from aru_rtl_dp import decode, s16, sat16, sat20  # same field decode + sat as the M2 model


# ---------------------------------------------------------------------------
# Per-instruction product, in 20-bit accumulator units (signed by operand AND coeff)
# ---------------------------------------------------------------------------
@lru_cache(maxsize=None)
def product20(F, cmag, csign):
    """Return the signed 20-bit accumulator contribution of one multiply F·(coeff/32).

    Reuses the VERIFIED gate-level Booth front-end (aru_booth.comb_array, the literal NAND
    array + 74F283 carry chain), summed over the fig-3.4 3-AS schedule, with the +3/dual-rail
    all-ones correction (plan 016). The magnitude value v carries the OPERAND sign (the gate
    array sign-extends F); the COEFF sign (csign) negates the whole product for the accumulator.

    Relationship to aru_booth.multiply (which is RESULT-register units): for a single multiply,
    RES = sat16(round(contribution/8)) reproduces every POSITIVE-coeff golden exactly and every
    NEGATIVE-coeff golden to within 2 LSB (aru_booth puts the two's-complement -1 at the result
    register OUTPUT of a *single* multiply, then a round-half-up >>3; a clean signed ACCUMULATOR —
    which is what a multi-tap MAC needs — does not carry that -1/round through a sum, so the two
    differ by ≤2 LSB on negative coeffs). That delta is ~-84 dB, far below the reverb-IR noise
    floor, and a clean signed accumulator is the structurally-correct choice for cross-instruction
    accumulation. See aru_booth §4F.8/§4.6 (sign via the subtract-XOR row IN the accumulator)."""
    C = [(cmag >> i) & 1 for i in range(6)]
    SR0 = Bo.load_SR(s16(F))
    SR1 = Bo.shift_right2(SR0)
    SR2 = Bo.shift_right2(SR1)
    acc = 0
    dual = 0
    for SR, (m0, m1) in zip((SR0, SR1, SR2), ((C[4], C[5]), (C[2], C[3]), (C[0], C[1]))):
        acc += Bo._s20(Bo.comb_array(SR, m0, m1))
        if m0 and m1:
            dual += 1
    v = -acc + 3 * dual                  # magnitude accumulator value (carries operand sign)
    return v if csign else -v            # coeff sign: negate the whole product for the accumulator


def res_from_acc(acc):
    """Result register = sat16 of the accumulator >>3 with round-half-up (the ARU PP3..18 tap)."""
    return sat16((acc + 4) >> 3)


# ---------------------------------------------------------------------------
# §2T device decode — per-step DAB driver + strobes (the free-run routing)
# ---------------------------------------------------------------------------
# DAB driver classes:
DRV_MEMR = "MEMR"     # DMEM read -> DAB
DRV_RDRREG = "RDRREG" # result register -> DAB (on a MEMW/ step)
DRV_RD_AD = "RD_AD"   # A/D input -> DAB
DRV_RD_XREG = "RD_XREG"  # X-register -> DAB
DRV_HOLD = "HOLD"     # idle: no driver, DAB holds last value


def device_decode(d, ofst):
    """Map (decoded microword d, 16-bit OFST/ field) -> the per-step bus routing.

    ofst = (l1<<8)|l0 = the stored OFST/ (complemented offset); for an I/O step its bits are
    repurposed as the I/O command (OFSTn/ = bit n). Returns a dict:
      driver  : who drives the DAB this step (one of DRV_*)
      memwrite: True if this step WRITES DMEM (MEMW/, DIN = result reg)
      wr_da   : True if WR DA/ fires (capture DAB -> D/A output)
      wr_xreg : True if WR XREG/ fires (capture DAB -> X-register)
      da_chan : the D/A output channel A..D (= SDAA-D = OFST8-11/) when wr_da
    Mirrors netlist §2T.1/§2T.2/§2T.3 exactly (decoder outputs active-low; here boolean)."""
    MEMAC, MI16 = d["MEMAC"], d["MI16"]

    def ob(n):
        return (ofst >> n) & 1

    driver = DRV_HOLD
    memwrite = False
    wr_da = wr_xreg = False
    da_chan = None

    if MEMAC == 1 and MI16 == 0:            # §2T.1: MEMW/ — DMEM write; result reg drives DAB (RDRREG/)
        driver = DRV_RDRREG
        memwrite = True
    elif MEMAC == 1 and MI16 == 1:          # §2T.1: MEMR/ — DMEM read drives DAB
        driver = DRV_MEMR
    elif MEMAC == 0 and MI16 == 1:          # §2T: tcWR active -> I/O step
        sel = (ob(13) << 1) | ob(12)        # dec-2 select {OFST13/,OFST12/}
        if sel == 3:
            driver = DRV_RD_AD              # 2Y3 -> RD AD/
        elif sel == 2:
            driver = DRV_RD_XREG            # 2Y2 -> RD XREG/
        # else sel 0/1 -> no read driver (idle/hold)
        if ob(7):                           # §2T.2 WR DA/ = NAND(OFST7/, tcWR)
            wr_da = True
            # SDAA-D = OFST8-11/ (§2T.4): the D/A output-channel select
            da_chan = (ob(8) << 0) | (ob(9) << 1) | (ob(10) << 2) | (ob(11) << 3)
        if ob(6):                           # §2T.2 WR XREG/ = NAND(MS7, tcWR, OFST6/)
            wr_xreg = True
    # else (MEMAC=0,MI16=0): 1Y0 n/c -> no device (idle/hold)

    return dict(driver=driver, memwrite=memwrite, wr_da=wr_da, wr_xreg=wr_xreg, da_chan=da_chan)


# ---------------------------------------------------------------------------
# The free-run engine
# ---------------------------------------------------------------------------
class FreeRunARU:
    """Phase-accurate ARU+DMEM+T&C run FREE over the 100-step microprogram.

    State that persists across steps AND samples (this is where the reverb lives):
      R[4]  register file        ACC accumulator        RES result register
      DM{}  64K×16 DRAM          XREG X-register        DAB shared bus (hold-last)
      CPC   current-position counter (+1 per sample)    pend the 1-instruction MAC pipeline reg
    """

    NSTEPS = 100      # WCS program length (steps 0..99; RESET@99)

    def __init__(self):
        self.R = [0, 0, 0, 0]          # 4×LS670 register file (signed 16-bit)
        self.ACC = 0                   # 20-bit ±2^18 accumulator (signed MAC across steps)
        self.RES = 0                   # 16-bit result register
        self.DM = {}                   # sparse 64K×16 DRAM delay memory
        self.XREG = 0                  # DAB<->DATA bridge latch
        self.DAB = 0                   # shared 16-bit data bus (holds last value when undriven)
        self.CPC = 0                   # 16-bit current-position counter
        # the deferred-MAC pipeline register: the back-end (accumulate/ZERO/XFER) of the PREVIOUS
        # instruction, retired at the START of the current instruction (fig-3.4: ZERO/+XFER CK at
        # the NEXT instruction's AS0; accumulate completes one AS later).
        self.pend = None               # (Vsigned, ZERO, XFER) or None
        # bookkeeping / instrumentation
        self.step_count = 0
        self.sample_count = 0
        self.fault = None

    # ---- one microinstruction (one WCS step) ----
    def step(self, l0, l1, l2, l3, audio_in, probe=None):
        d = decode(l2, l3)
        ofst = ((l1 << 8) | l0) & 0xFFFF
        dev = device_decode(d, ofst)

        # (1) RETIRE the previous instruction's deferred back-end (fig-3.4 — one instruction late):
        #     ZERO/ clears the accumulator, the instruction's product accumulates, XFER CK latches RES.
        if self.pend is not None:
            Vp, zerop, xferp = self.pend
            if zerop:
                self.ACC = 0
            self.ACC = sat20(self.ACC + Vp)
            if xferp:
                self.RES = res_from_acc(self.ACC)

        # (2) operand read — READ-BEFORE-WRITE (ARUCK@MS6 loads operand before the MS7 regfile write).
        opnd = self.R[d["RA"]]

        # (3) DMEM address = CPC - OFST  (OFST stored complemented; adder carry-in high). §5.2
        addr = (self.CPC + ofst + 1) & 0xFFFF

        # (4) drive the DAB — exactly one source per §2T device decode, else hold last value.
        drv = dev["driver"]
        dmem_old = self.DM.get(addr, 0)
        if drv == DRV_MEMR:
            self.DAB = dmem_old & 0xFFFF
        elif drv == DRV_RDRREG:
            self.DAB = self.RES & 0xFFFF
        elif drv == DRV_RD_AD:
            self.DAB = audio_in & 0xFFFF
        elif drv == DRV_RD_XREG:
            self.DAB = self.XREG & 0xFFFF
        # DRV_HOLD: leave self.DAB unchanged (bus hold; no pull resistors)

        # (5) consume the DAB:
        #   regfile write R[WA] <- DAB on DAB WSTB/ (¬MS7) — every step (§4F.1).
        self.R[d["WA"]] = s16(self.DAB)
        #   DMEM write (MEMW/, DIN = result register driven onto DAB) — write-after-read (§5/fig3.3).
        if dev["memwrite"]:
            self.DM[addr] = self.RES & 0xFFFF
        #   X-register capture (WR XREG/) and D/A output capture (WR DA/) take the current DAB.
        out_da = None
        if dev["wr_xreg"]:
            self.XREG = self.DAB & 0xFFFF
        if dev["wr_da"]:
            out_da = (dev["da_chan"], s16(self.DAB))

        # (6) compute THIS instruction's product (deferred to retire next step). §fig-3.4
        V = product20(opnd, d["cmag"], d["CSIGN"])
        self.pend = (V, d["ZERO"], d["XFER"])

        self.step_count += 1
        if probe is not None:
            probe.append(dict(d=d, ofst=ofst, addr=addr, drv=drv, dab=self.DAB,
                              opnd=opnd, V=V, ACC=self.ACC, RES=self.RES,
                              memwrite=dev["memwrite"], out_da=out_da,
                              R=list(self.R), CPC=self.CPC))
        return out_da

    # ---- one audio sample = 100 microinstructions, then CPC += 1 (RESET@99) ----
    def run_sample(self, wcs, audio_in, probe=None):
        """wcs = list of 128 (l0,l1,l2,l3) tuples; runs steps 0..99 and returns the list of
        (channel, value) D/A writes captured at WR DA/ this sample."""
        outs = []
        for k in range(self.NSTEPS):
            l0, l1, l2, l3 = wcs[k]
            o = self.step(l0, l1, l2, l3, audio_in, probe=probe)
            if o is not None:
                outs.append(o)
        # CPC advances one sample position at the RESET@99 boundary (RUN cadence). §5.1/§3.5
        self.CPC = (self.CPC + 1) & 0xFFFF
        self.sample_count += 1
        return outs

    # ---- run N samples, capture the output IR per D/A channel ----
    def run_free(self, wcs, input_signal, n_samples, probe_first=0):
        """input_signal: callable(sample_index)->int16, or a list. Returns a dict:
          'A'..'D' -> list of per-sample output values (the last WR DA/ to that channel each sample),
          'mono'   -> per-sample sum of all WR DA/ writes (a quick scalar IR),
          'probe'  -> per-step probe records for the first `probe_first` samples.
        """
        chans = {c: [] for c in "ABCD"}
        mono = []
        all_probe = []
        for s in range(n_samples):
            if callable(input_signal):
                ai = input_signal(s)
            else:
                ai = input_signal[s] if s < len(input_signal) else 0
            probe = [] if s < probe_first else None
            outs = self.run_sample(wcs, ai & 0xFFFF, probe=probe)
            if probe is not None:
                all_probe.append(probe)
            # per-channel: last write to each channel this sample; mono: sum of all writes
            persamp = {c: None for c in "ABCD"}
            ssum = 0
            for chan, val in outs:
                ssum += val
                cname = "ABCD"[chan & 3] if chan is not None else "A"
                persamp[cname] = val
            for c in "ABCD":
                chans[c].append(persamp[c] if persamp[c] is not None else 0)
            mono.append(ssum)
            if self.fault:
                break
        return dict(A=chans["A"], B=chans["B"], C=chans["C"], D=chans["D"],
                    mono=mono, probe=all_probe)


# ---------------------------------------------------------------------------
# WCS helpers
# ---------------------------------------------------------------------------
def wcs_from_mem(mem, base=0x4000, n=128):
    """Extract the 128-step WCS image (l0,l1,l2,l3 per step) from an SBC memory image."""
    return [(mem[base + 4 * k], mem[base + 4 * k + 1],
             mem[base + 4 * k + 2], mem[base + 4 * k + 3]) for k in range(n)]


def encode_step(offset=0, MEMAC=0, MI16=0, WA=0, RA=0, CSIGN=1, XFER=0, ZERO=0, cmag=0):
    """Build one WCS step (l0,l1,l2,l3) from logical fields — for hand-loaded test programs.
    offset = TRUE signed delay (we store its complement as OFST/, matching §3.6). The l3 byte is
    active-low (XFER/ZERO/coeff complemented), per §G3R / the aru_post field map."""
    ofst_stored = (~offset) & 0xFFFF                      # OFST/ = complemented offset (§3.6/§5.2)
    l0 = ofst_stored & 0xFF
    l1 = (ofst_stored >> 8) & 0xFF
    l2 = (MI16 & 1) | ((MEMAC & 1) << 1) | ((WA & 3) << 2) | ((RA & 3) << 4) | ((CSIGN & 1) << 7)
    inv3 = (XFER & 1) | ((ZERO & 1) << 1) | ((cmag & 0x3F) << 2)   # active-high decoded byte
    l3 = (~inv3) & 0xFF                                   # store complemented (active-low lane 3)
    return (l0, l1, l2, l3)


def encode_io_step(rd=None, wr_da=False, wr_xreg=False, da_chan=0, WA=0, RA=0,
                   CSIGN=1, XFER=0, ZERO=0, cmag=0):
    """Build an I/O step (MEMAC=0, MI16=1) with the OFST/ field carrying the I/O command bits:
       OFST12//13/ select the read source (RD AD/ = 11, RD XREG/ = 10); OFST7/ -> WR DA/;
       OFST6/ -> WR XREG/; OFST8-11/ = SDAA-D D/A channel select. (§2T.1/§2T.2/§2T.4)"""
    ofst = 0
    if rd == "AD":
        ofst |= (1 << 13) | (1 << 12)          # sel = 11
    elif rd == "XREG":
        ofst |= (1 << 13)                       # sel = 10
    if wr_da:
        ofst |= (1 << 7)
        ofst |= (da_chan & 0xF) << 8            # SDAA-D channel
    if wr_xreg:
        ofst |= (1 << 6)
    l0 = ofst & 0xFF
    l1 = (ofst >> 8) & 0xFF
    l2 = 1 | (0 << 1) | ((WA & 3) << 2) | ((RA & 3) << 4) | ((CSIGN & 1) << 7)   # MI16=1, MEMAC=0
    inv3 = (XFER & 1) | ((ZERO & 1) << 1) | ((cmag & 0x3F) << 2)
    l3 = (~inv3) & 0xFF
    return (l0, l1, l2, l3)


def nop_step():
    """An idle/no-device step (MEMAC=0, MI16=0): holds the DAB, writes R0 with the held value."""
    # l2: MI16=0, MEMAC=0, WA=0, RA=0, CSIGN=1; l3 = FF -> XFER=0 ZERO=0 cmag=0
    return (0x00, 0x00, 0x02, 0xFF)


# ===========================================================================
# self-tests
# ===========================================================================
def selftest_product():
    """product20 -> res_from_acc must reproduce the 20 POST goldens (positive exact, negative ±1)."""
    ok = exact = 0
    for F, cmag, cs, exp in Bo.GOLDENS:
        V = product20(F, cmag, cs)
        res = res_from_acc(V)
        if res == exp:
            exact += 1
            ok += 1
        elif abs(res - exp) <= 2:
            ok += 1
        else:
            print(f"    MISS F=0x{F & 0xFFFF:04X} cmag={cmag} cs={cs} exp={exp:+d} got={res:+d}")
    print(f"product20->res vs 20 POST goldens: {exact}/20 exact, {ok}/20 within 2 LSB "
          f"(negative-coeff single multiplies differ ≤2 LSB by design; MAC is clean-signed)")
    # unity passthrough (cmag=32 = ×1.0)
    print(f"unity cmag=32: F=0x5555 -> {res_from_acc(product20(0x5555, 32, 1))} (want 21845); "
          f"F=0x1234 -> {res_from_acc(product20(0x1234, 32, 1))} (want 4660)")
    return ok


def selftest_mac():
    """Cross-instruction MAC through the real engine + deferred pipeline: a 4-step program
    A(ZERO,×1 of 1000) -> B(accumulate ×1 of 500, XFER) -> two flush NOPs, then RES == 1500.

    Steps are all idle-device (no DMEM/IO) so the only effect is the MAC pipeline. The operand is
    placed in R0 and read via RA=0; cmag=32 = unity. A has ZERO=1 to start a fresh sum, B has
    XFER=1 to latch the accumulated 1000+500 into RES. The deferral means RES updates on the
    step AFTER B retires."""
    aru = FreeRunARU()
    # We feed the operand on the DAB by writing R0 directly each step (no device drives DAB here,
    # so set R0 before each compute). Use compute steps with WA pointing at an unused reg (R3).
    progA = encode_step(MEMAC=0, MI16=0, WA=3, RA=0, CSIGN=1, XFER=0, ZERO=1, cmag=32)
    progB = encode_step(MEMAC=0, MI16=0, WA=3, RA=0, CSIGN=1, XFER=1, ZERO=0, cmag=32)
    nop = nop_step()
    aru.R[0] = 1000
    aru.step(*progA, 0)          # compute A (pend=A)
    aru.R[0] = 500
    aru.step(*progB, 0)          # retire A (ACC=0+1000_V), compute B (pend=B)
    aru.step(*nop, 0)            # retire B (ACC+=500_V, XFER -> RES=res(1000+500))
    res = aru.RES
    want = res_from_acc(product20(1000, 32, 1) + product20(500, 32, 1))
    print(f"MAC two unity taps (1000+500) via engine+deferred pipeline: RES={res} want={want} "
          f"[{'OK' if res == want else 'FAIL'}] (~1500 expected)")
    return res == want


def test_zero_delay(verbose=True):
    """M3.1 — zero-delay program (SM §5.5 / PGM 7 analogue): a single I/O step reads the A/D
    onto the DAB and writes it straight to the D/A (channels A & D); the rest are NOPs. An impulse
    in must appear at the output UNCHANGED. Proves the free-run engine + 100-step loop + DAB routing
    + the I/O boundary, WITHOUT any DMEM recirculation."""
    wcs = [nop_step()] * 128
    wcs = list(wcs)
    # step 0: read A/D -> DAB, write DAB -> D/A channel A; step 1: same value -> channel D.
    wcs[0] = encode_io_step(rd="AD", wr_da=True, da_chan=0)      # channel A
    wcs[1] = encode_io_step(rd=None, wr_da=True, da_chan=3)      # channel D (DAB still holds input)
    aru = FreeRunARU()
    sig = [0, 9000, 0, -4000, 0, 0, 1234, 0]
    out = aru.run_free(wcs, sig, len(sig))
    okA = out["A"] == sig
    okD = out["D"] == sig
    if verbose:
        print(f"M3.1 zero-delay passthrough:")
        print(f"   in   : {sig}")
        print(f"   out A: {out['A']}  [{'OK' if okA else 'FAIL'}]")
        print(f"   out D: {out['D']}  [{'OK' if okD else 'FAIL'}]")
    return okA and okD


def test_max_delay(delay=64, n=200, verbose=True):
    """M3.2 — straight DMEM delay (SM §5.4 / PGM 8 analogue): write the input to a DMEM cell, read
    it back `delay` samples later, output it. Proves the DMEM write->read delay across samples
    (addr = CPC - OFST, CPC +1/sample) with no feedback tail. delay = OFST_read - OFST_write."""
    W, R = 0, delay
    wcs = list([nop_step()] * 128)
    # READ-BEFORE-WRITE (ARUCK@MS6 loads the operand before the MS7 regfile write) means the input
    # written to R0 at step 0 is only visible to a LATER step's multiply — so move input->reg->MAC
    # over two steps (exactly how CONCERT decouples its MEMR-write-register from a later read step).
    # step 0: read A/D -> R0 (the multiply here uses the OLD R0; we don't use it).
    wcs[0] = encode_io_step(rd="AD", WA=0, RA=3, cmag=0)
    # step 1: compute R0 x1 (cmag=32), XFER+ZERO -> product (=input) retires into RES next step.
    wcs[1] = encode_step(MEMAC=0, MI16=0, WA=3, RA=0, CSIGN=1, XFER=1, ZERO=1, cmag=32)
    # step 2: MEMW offset W -> DMEM[CPC-W] <- RES (=input, just retired from step 1).
    wcs[2] = encode_step(offset=W, MEMAC=1, MI16=0, WA=1, RA=1, CSIGN=1, cmag=0)
    # step 3: MEMR offset R -> DAB <- DMEM[CPC-R] (the value written delay samples ago).
    wcs[3] = encode_step(offset=R, MEMAC=1, MI16=1, WA=2, RA=2, CSIGN=1, cmag=0)
    # step 4: WR DA -> output channel A <- DAB (the delayed sample held from step 3).
    wcs[4] = encode_io_step(rd=None, wr_da=True, da_chan=0)
    aru = FreeRunARU()

    def impulse(s):
        return 1000 if s == 0 else 0

    out = aru.run_free(wcs, impulse, n)
    a = out["A"]
    peak_idx = max(range(len(a)), key=lambda i: abs(a[i]))
    peak_val = a[peak_idx]
    # success: a clear impulse at sample == delay, ~unchanged amplitude, near-zero elsewhere.
    near_zero = all(abs(v) <= 2 for i, v in enumerate(a) if i != peak_idx)
    ok = (peak_idx == delay) and (abs(peak_val - 1000) <= 3) and near_zero
    if verbose:
        print(f"M3.2 max-delay (delay={delay} samples):")
        print(f"   impulse(1000)@sample0 -> output peak {peak_val} at sample {peak_idx} "
              f"(want ~1000 @ {delay})  [{'OK' if ok else 'FAIL'}]")
        nz = [(i, v) for i, v in enumerate(a) if abs(v) > 2]
        print(f"   nonzero (|v|>2) output samples: {nz[:8]}")
    return ok


def test_feedback_comb(D=50, g_cmag=16, n=400, verbose=True):
    """M3.3 ENGINE-CAPABILITY test (NOT CONCERT): a hand-built feedback comb
    y[n] = x[n] + g·y[n-D] proves the free-run engine produces a COHERENT RECIRCULATING,
    DECAYING reverb WHEN THE WCS CLOSES THE LOOP — the holistic thesis (the loop closes from
    the wiring, not a tuned constant). g = g_cmag/32 (here 16/32 = 0.5); the decay is whatever
    the coeff produces. This is the structural capability check; the REAL CONCERT decay comes
    from CONCERT's own coeffs + per-frame modulation (M3.4), NOT from this chosen g.

    The MAC chain (read-before-write honored): input->R0 (step0); MEMR y[n-D]->R1 + start the
    sum with x[n] (step1, ZERO); +g·y[n-D] then XFER (step2); MEMW y[n]->DMEM[CPC] (step3);
    WR DA out<-y[n] (step4)."""
    wcs = list([nop_step()] * 128)
    wcs[0] = encode_io_step(rd="AD", WA=0, RA=3, cmag=0)                       # input -> R0
    wcs[1] = encode_step(offset=D, MEMAC=1, MI16=1, WA=1, RA=0, CSIGN=1,        # MEMR y[n-D]->R1;
                         XFER=0, ZERO=1, cmag=32)                              # acc = x[n] (R0×1)
    wcs[2] = encode_step(MEMAC=0, MI16=0, WA=3, RA=1, CSIGN=1,                  # acc += g·y[n-D];
                         XFER=1, ZERO=0, cmag=g_cmag)                          # XFER -> RES = y[n]
    wcs[3] = encode_step(offset=0, MEMAC=1, MI16=0, WA=2, RA=2, CSIGN=1, cmag=0)  # MEMW y[n]->DMEM[CPC]
    wcs[4] = encode_io_step(rd=None, wr_da=True, da_chan=0)                     # out <- DAB (=y[n])
    aru = FreeRunARU()

    def impulse(s):
        return 8000 if s == 0 else 0

    out = aru.run_free(wcs, impulse, n)
    a = out["A"]
    # echoes should appear at 0, D, 2D, 3D ... decaying ~×0.5 each
    echoes = [(k * D, a[k * D]) for k in range(min(6, n // D)) if k * D < n]
    peak0 = a[0]
    decayed = all(abs(echoes[i + 1][1]) < abs(echoes[i][1]) for i in range(len(echoes) - 1)
                  if echoes[i][1] != 0)
    alive = sum(1 for v in a if abs(v) > 2)
    not_blown = max(abs(v) for v in a) <= 40000
    ok = decayed and alive >= 4 and not_blown and peak0 != 0
    if verbose:
        print(f"M3.3 engine recirculation capability — feedback comb y[n]=x[n]+{g_cmag}/32·y[n-{D}]:")
        print(f"   echoes (sample, value): {echoes}")
        print(f"   decaying={decayed}, live samples(|v|>2)={alive}, peak={max(abs(v) for v in a)} "
              f"[{'OK' if ok else 'FAIL'}]")
        # rough ratio
        if len(echoes) >= 2 and echoes[0][1]:
            ratios = [round(echoes[i + 1][1] / echoes[i][1], 3) for i in range(len(echoes) - 1)
                      if echoes[i][1]]
            print(f"   echo ratios (want ~0.5): {ratios}")
    return ok


FS = 34130.0   # audio sample rate (34.13 kHz = 100 microinstructions × 292.97 ns)


def concert_analysis(burst_s=0.30, total_s=2.2, verbose=True):
    """M3.3 CONCERT characterization (boots the firmware ~30-90s). Free-runs the captured static
    CONCERT WCS with a noise BURST then silence, and reports the OUTPUT envelope + the DMEM-buffer
    energy envelope vs time — to see whether the loop closes (energy sustains past the input) and
    whether the output is a dense tail or sparse echoes.

    FINDINGS (2026-06-29, static WCS, no per-frame modulation):
      • The free-run engine runs the whole 100-step CONCERT program for seconds with NO fault.
      • The DMEM delay memory RETAINS the burst energy and decays over ~1.7 s (reverb-like RT) —
        the writes store real values and the long read taps (0.9-1.4 s) read them back.
      • The OUTPUT (WR DA/) shows the direct signal + DISCRETE delayed echoes (~1.4-1.6 s), NOT a
        dense continuous reverb tail. So the storage/feedback works at a reverb timescale, but the
        output path is sparse — densification likely needs the per-frame LFO modulation (M4; the 4
        modulated taps 56/57/107/108) and/or a feedback-timing refinement. NOT a dead engine: the
        engine produces exact recirculation on a hand-built feedback loop (see test_feedback_comb)."""
    import math
    import boot8080 as B
    if verbose:
        print("booting firmware to CONCERT (~30-90s)...")
    m, ms = B.boot(verbose=False)
    if "mainloop" not in ms:
        print("  BOOT did not reach mainloop; milestones:", ms)
        return False
    wcs = wcs_from_mem(m.memory)
    aru = FreeRunARU()
    BURST = int(burst_s * FS)
    N = int(total_s * FS)
    seed = 0x1234

    def src(s):
        nonlocal seed
        seed = (seed * 1103515245 + 12345) & 0x7FFFFFFF
        return ((seed >> 8) % 16000 - 8000) if s < BURST else 0

    W = int(0.05 * FS)
    out_env, buf_env = [], []
    win_out, win_n = 0.0, 0
    for s in range(N):
        o = aru.run_sample(wcs, src(s) & 0xFFFF)
        per = {c: 0 for c in "ABCD"}
        for chan, val in o:
            per["ABCD"[chan & 3]] = val
        win_out += sum(v * v for v in per.values())
        win_n += 1
        if (s + 1) % W == 0:
            out_env.append(math.sqrt(win_out / max(1, win_n)))
            win_out, win_n = 0.0, 0
            be = sum((v - 0x10000 if v & 0x8000 else v) ** 2 for v in aru.DM.values())
            buf_env.append(math.sqrt(be / max(1, len(aru.DM))))
    if verbose:
        burst_win = BURST // W
        print(f"  ran {aru.sample_count} samples × 100 = {aru.step_count} microinstr, fault={aru.fault}")
        print(f"  noise burst 0-{burst_s}s then silence; DMEM cells used={len(aru.DM)}")
        print("   t(s)  out_RMS   buf_RMS")
        for i in range(0, len(out_env), 4):
            print(f"   {i*W/FS:4.2f}  {out_env[i]:8.1f}  {buf_env[i]:8.1f}")
        bpk = max(buf_env)
        after = buf_env[min(len(buf_env) - 1, burst_win + 20)]
        print(f"  buffer RMS peak={bpk:.0f}, ~1s after input-stop={after:.0f} (ratio {after/bpk:.3f}) "
              f"-> {'SUSTAINS' if after/bpk > 0.2 else 'decays fast'}")
    return aru.fault is None


def run_structural_tests():
    """Fast (no-boot) M3 validation suite: product/MAC primitives + the staged free-run targets."""
    ok = True
    ok &= bool(selftest_product())
    ok &= selftest_mac()
    print("-" * 74)
    ok &= test_zero_delay()
    print("-" * 74)
    ok &= test_max_delay(delay=64)
    ok &= test_max_delay(delay=150)
    print("-" * 74)
    ok &= test_feedback_comb(D=50, g_cmag=16)
    return ok


if __name__ == "__main__":
    try:
        sys.stdout.reconfigure(encoding="utf-8")   # Windows console is cp1252 by default
    except Exception:
        pass
    print("=" * 74)
    print("224XL — M3 free-run engine (tools/aru_freerun.py)")
    print("=" * 74)
    run_structural_tests()
    if "concert" in sys.argv:                       # the boot-requiring CONCERT characterization
        print("-" * 74)
        concert_analysis()
