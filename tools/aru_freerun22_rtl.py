#!/usr/bin/env python3
"""aru_freerun22_rtl — THE RTL ARBITER (plan 021 Phase A; plan 024 F1 re-sync): the free-running
224XL ARU/T&C/DMEM under the session-0022 coordinate system with the MAC/register/XFER alignment
taken from the TRACED control pipeline (netlist §3.5-3.11, §2T, §4.7-4.9, §4F, §6D + fig-3.3/3.4),
and — since session 0027 — the MAC ARITHMETIC taken from the COMPLEMENT-DOMAIN physical law locked
per-pin by the §5.7 ARU signature tables (1467/1469 pins; feedback table 710/710). No knobs: every
capture point sits at its traced edge, every bit at its measured level.

★ THE COMPLEMENT DOMAIN (session 0027, e1c_backend_resolve + e1_aru_signatures; registry #29/#30):
  The DAB physically carries ACTIVE-LOW values (the XREG write bridge dmem_U39/U41 puts the SBC's
  complemented DATA0-7/ levels on the DAB with no inversion, §5.6; every boundary — XREG readback
  U38/U40, the FPC — complements back). The regfile, shifter, Booth array, delay memory, DAB, and
  result register all carry phys (complemented) patterns, and in that domain the EXACTLY-TRACED
  wiring reproduces the E83 goldens by PURE TRUNCATION:

    per accumulate:  rail = cs_eff (= inv(CSIGN/), the aru_U2 inverters)
                     B    = PR ^ (rail ? 0xFFFFF : 0)        (the sub-XOR row)
                     cin  = 1 - rail                          (traced: cin = inv(rail))
                     sum  = (ACC + B + cin) & 0xFFFFF         (20-bit chain, no wrap-out)
                     SAT  = sum19 ^ sum18
                     PP   = SAT ? clamp : sum;  clamp = topB ? 0xC0000 : 0x3FFFF, topB = B bit19
    the sat-mux PP feeds BOTH the result path AND the accumulator D inputs — the '163 loads the
    CLAMP (registry #35; pinned by the diag-3 tail saturation in the feedback table);
    PR = comb_array output loaded RAW (active-low, no complement);  '163 sync clear = 0;
    capture: RES = (PP >> 3) & 0xFFFF — a pure bit tap of PP3..18, NO rounding hardware.

  The engine's former CPU-domain value model (product20 terms, res_from_acc((ACC+ppC+4)>>3),
  the '+3 dual-rail' and '-M-1' laws) DISSOLVES into CPU-domain bookkeeping of these bits
  (registry #30); it sat ±1-2 LSB off the physical law on most captures (registry #31,
  e5_engine_vs_physical.py = the spec + regression for this re-sync). booth3/product20 remain
  in this file as VALUE-LEVEL identities (self-test bridge + historical probes), not the datapath.

  CPU-domain boundaries of this engine (the public API is unchanged):
    RD-AD injects ~x;  WR-DA emits s16(~DAB);  WR XREG readback = ~DAB;  the host->DSP latch
    XREG_host (CPU value) drives ~XREG_host onto the DAB;  unwritten DMEM reads phys 0xFFFF
    (= CPU 0, matching the pre-resync engine's silence default).
  The value-view of the law (derivable, used by the self-tests): with π(phase) = s20(raw)+1 for
  the raw comb output of the PHYS operand, each accumulate adds +π (cs=1) or -π (cs=0) to the
  value V = s20(~ACC); the ZERO clear sets V = -1; capture y = V >> 3 (arithmetic floor — the
  sat-mux rails ±2^18 guarantee the PP3..18 tap never wraps, so no sat16 is ever needed).
  Zero-coefficient phases have π = 0 exactly (the comb zero-rail baseline 0xFFFFF) — the old
  '±3 residue' idioms were CPU-domain artifacts.

THE EMERGENT ALIGNMENT (discrete MS-slot convention, calibrated by tc_clock vs fig-3.3/3.4;
"step n" = the step during which word w_n's stage-1 fields + offset latch are live):

  fetch pipeline   PC (tc_U14/U1, CLK=DAB RSTB/) points at w_{n+1} during step n; stage-1
                   (tc_U17/U18/U4/U5, CLK=DAB RSTB/) + offset latch (tc_U45/U31) latch the
                   PREVIOUS fetch at each step boundary => a word's fields are live one step
                   after its fetch. The reset word R fires RESET during its own fields-live
                   step; the PC sync-clears one boundary later, SO THE ROW AFTER THE RESET
                   WORD EXECUTES TOO: the hardware frame is L+1 steps (rows 0..L).
                   Confirmed from the program bytes: ALL 13 factory programs park an idle
                   word at row L, and L=99 programs give dale's canonical 100 steps/34.13 kHz.
  stage 2          tc_U19 (74LS377, CP=ARUCKE, /E=AS0/) loads {RA, XFER, ZERO, MI23} at the
                   slot-3 edge of each step from stage-1 => holds w_n from slot3(n)..slot2(n+1).
  CSIGN JK         tc_U20 (74S112, CLK=ARUCKE/, J/K = AS0-gated tc_U19.Q4): follows Q4's
                   PRE-load value at the slot-3 edge => holds w_{n-1}'s MI23 during
                   slot3(n)..slot2(n+1). Effective sign = the Multibus level (~stored bit7):
                   E3b-stable, and the traced chain (stored -> MI23 -> JK -> sub-ctrl)
                   natively carries it.
                   ** SIGN SCHEDULE = OWN-SIGN AT EVERY PP (falsification-tested, session
                   0025). ** The JK window [3.0(n), 3.0(n+1)) nominally covers
                   ppC(w_{n-2})@4.43(n) + ppA(w_{n-1})@7.43(n) + ppB(w_{n-1})@1.43(n+1) —
                   i.e. the LIVE level at the pairC edges belongs to the NEXT word. But the
                   sub-XOR control (§4.6) feeds the SAME settle-limited adder as the data
                   (~1.4-slot propagation, the constant that defers the ACC): a control
                   flip at 3.0 has not propagated by 3.06 (capture) and is marginal at
                   4.43 — and the EMPIRICAL arbiter (the factory program under the
                   documented-defaults oracle) REJECTS next-sign pairC at either consumer:
                   live-sign register adds collapse CONCERT to a ~0.8 s TONAL husk, while
                   own-sign renders the coherent 1.5-1.9 s bank. The control path defers
                   one AS exactly like the data path (fig-3.4), so every pp is signed by
                   its own word. RTL22(csign_lag=True) keeps the falsified live-sign
                   register variant for the record (dead-end registry #23).
  serializer       tc_U11/U10 (74195, CLK=ARUCKE, SH//LD=AS1/, P3=Q2 feedback): loads w_n's
                   C-bits at the slot-6 edge of step n; w_n's Booth pairs (C4,C5),(C2,C3),
                   (C0,C1) are live during AS0/AS1/AS2 OF STEP n+1 (the third pair via the
                   P3=Q2 feedback at the next load edge). The multiply of word W executes
                   physically during step W+1.
  operand SR       74194s (CLK=ARUCK, S1/S0 mode = LOAD during AS2 per fig-3.4): the load
                   EDGE is the slot-0 edge of step n+1, sampling regfile[RA(w_n)] AFTER
                   step n's MS7 write => WRITE-THROUGH: a word's operand sees its own step's
                   regfile write. Shifts at the slot-3/slot-6 edges keep F, F>>2, F>>4
                   aligned with pairs A/B/C (golden-exact pairing). The SR loads the PHYS
                   (complemented) regfile pattern — the complement of the operand is what
                   makes the cs=1 rail (B = ~PR) come out POSITIVE in value terms.
  product reg      aru_U10/U11/U12 (CLK=ARUCK): latches each partial product at slots 0/3/6:
                   PR@3.58(W+1)=ppA(W), PR@6.58(W+1)=ppB(W), PR@0.58(W+2)=ppC(W).
                   PR = the RAW comb_array output (active-low product bits, §4.7/§4F.9).
  accumulator      aru_U45-49 (74LS163 always-load, CP=ARUCKE/, sync /CLR=ZERO/), fed by the
                   back-end adder chain (aru_U19-23 + sub-XOR) THROUGH THE SAT-MUX: the adder
                   needs ~1.4 slots to settle after a PR change, so each ACC edge captures the
                   sum formed from the PREVIOUS PR value — the accumulate lags the PR latch by
                   one full ARUCKE/ edge (fig-3.4, owner-read: "the accumulate runs
                   i2.AS1->i3.AS0, one AS behind the partial products = the pipeline register").
                   => ACC edges of step n: @1.43 <- BE(ACC+ppB(w_{n-2})); @4.43 <-
                      BE(·+ppC(w_{n-2})) or the ZERO clear; @7.43 <- BE(·+ppA(w_{n-1})).
                   Each edge loads the SAT-MUX OUTPUT (clamp included, registry #35) — the
                   pre-0028 wrap-only ACC was an erratum whenever SAT fired transiently
                   mid-group (the diag-3 tail proves the clamp path at pins).
  XFER CK          NAND(AS0, tc_U19.Q5, ARUCKE/): low slots 1-2 of step n iff w_{n-1}.XFER;
                   the result reg (74F374) captures on its RISE at the slot-3 edge.
                   ** THE RESULT REG D-INPUTS ARE ON THE PP BUS (netlist §4.2: PP3..PP18 ->
                   aru_U43/U44 D pins) = the SAT-MUX / ADDER OUTPUT, not the accumulator
                   register. ** At 3.06(n) the adder holds ACC_registered (through
                   ppB(w_{n-2}), loaded @1.43) + PR (= ppC(w_{n-2}), latched @0.58):
                   => RES <- (BE(ACC + ppC(w_{n-2})) >> 3) & 0xFFFF — the FULL group MAC,
                   pairC INCLUDED via the combinational path, PURE BIT TAP (no rounding).
                   (Session 0024: the register-read variant was an assumption no prior
                   oracle could see; session 0027: the '+4 round' dissolved.)
  ZERO/            NAND(tc_U19.Q6, AS0), 163 sync clear landing at the 4.43 edge of step n
                   iff w_{n-1}.ZERO (same owner as the capture, one edge after it;
                   the no-lag owner w_n is EMPIRICALLY DEAD — c2 probe: zero output).
                   The clear replaces the ppC(w_{n-2}) REGISTER load — the value already
                   reached RES through the PP bus; the clear just resets the accumulator
                   for the next group (phys 0 = value -1). fig-3.4 verbatim: "ZERO/ clears
                   it at i2.AS0 so it reads 0 at i2.AS1."
                   => An XFER+ZERO word X (the dominant factory idiom, 473/486) captures
                   the group MAC through w_{X-1} COMPLETE — every stored cmag acts at
                   full weight.
  DMEM             addr = CPC - stored offset; CAS falls at slot 4 (early-write DIN latch =
                   the JUST-captured RES on MEMW); DOUT lands ~slot 7 on MEMR (the MS7
                   regfile write captures it; nothing samples it earlier). DMEM stores the
                   PHYS patterns straight off the DAB.
  regfile write    DAB WSTB/ = ~MS7: R[WA(w_n)] <- DAB level at slot 7, every step.
  FPC out          FPC CK = MS5: the D/A double buffer captures the DAB at slot 5 of a WR-DA
                   step (RES is post-capture by then); the FPC boundary complements back to
                   the CPU/value domain (§5.6 mirror of the input path).
  CPC              +1 per frame on the RESET/ event (during the row-L step; all row
                   addresses of the frame use the pre-bump value).

Run:  python tools/aru_freerun22_rtl.py   (self-tests, each with its expectation derived from
      the physical law by hand in the comments: raw3/booth3 value bridge, passthrough EXACT,
      negative-unity -x-2 law, feedback comb closed form incl. multi-pair cmag + flag-sign
      inertness, CSIGN split own/lag variants, SAT-clamp-into-ACC (#35), CONCERT extraction)
"""
import os
import sys
from functools import lru_cache

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import aru_booth as B
from aru_freerun import product20, res_from_acc, fpc_input_float_to_fixed, fpc_output_fixed_to_float
from aru_rtl_dp import s16, sat16
from aru_freerun22 import (decode22, enc_memr, enc_memw, enc_idle, enc_io,
                           SRC_NONE, SRC_RDRREG, SRC_XREG, SRC_RDAD)

MC_HZ = 30_720_000.0
MS_PER_STEP = 9
MASK20 = 0xFFFFF
_WRAP = 1 << 20
_HALF = 1 << 19


def wrap20(v):
    """VALUE-LEVEL HISTORY (pre-0028 engine + c2 probe): signed mod-2^20 wrap. The physical
    accumulator does NOT wrap — the '163 loads the sat-mux output (see backend20 / registry
    #35). Kept for the historical probes' imports; not in the datapath."""
    v &= _WRAP - 1
    return v - _WRAP if v >= _HALF else v


@lru_cache(maxsize=None)
def booth3(F, cmag, cs):
    """VALUE-LEVEL identity (registry #30): the three per-phase signed CPU-domain partial
    products of one multiply, from the gate Booth array with the +3 dual-rail correction.
    Identity: sum(booth3(F,c,s)) == aru_freerun.product20(F,c,s) for all inputs.
    History + self-test bridge only — the datapath carries raw3() patterns."""
    C = [(cmag >> i) & 1 for i in range(6)]
    SR0 = B.load_SR(s16(F))
    SR1 = B.shift_right2(SR0)
    SR2 = B.shift_right2(SR1)
    pps = []
    for SR, (m0, m1) in zip((SR0, SR1, SR2), ((C[4], C[5]), (C[2], C[3]), (C[0], C[1]))):
        t = -B._s20(B.comb_array(SR, m0, m1)) + (3 if (m0 and m1) else 0)
        pps.append(t if cs else -t)
    return tuple(pps)


@lru_cache(maxsize=None)
def raw3(opnd_phys, cmag):
    """The three RAW comb-array outputs (phys active-low 20-bit patterns) of one multiply of
    the PHYS operand — the actual product-register loads, pairs A/B/C in fig-3.4 order.
    This IS the datapath front end (e1c: PRLOAD=raw, champion 1467/1469)."""
    C = [(cmag >> i) & 1 for i in range(6)]
    SR = B.load_SR(s16(opnd_phys))
    out = []
    for p, (m0, m1) in enumerate(((C[4], C[5]), (C[2], C[3]), (C[0], C[1]))):
        if p:
            SR = B.shift_right2(SR)
        out.append(B.comb_array(SR, m0, m1))
    return tuple(out)


# The zero-rail comb baseline (M0=M1=0 -> every NAND high -> PR = 0xFFFFF, operand-independent):
# the value-inert phase (π = s20(0xFFFFF)+1 = 0). Power-on pipeline fill.
RAW_IDLE = raw3(0xFFFF, 0)
assert RAW_IDLE == (MASK20, MASK20, MASK20)


def backend20(acc, raw, cs):
    """One traced back-end adder + sat-mux evaluation (phys domain; e1c champion convention):
    rail = cs, B = raw ^ rail-mask (sub-XOR row), cin = inv(rail), 20-bit sum, SAT = s19^s18,
    clamp = topB ? 0xC0000 : 0x3FFFF (aru_U33-37 + U2; topB = B bit19). The RETURN VALUE feeds
    both the result path and the '163 accumulator D inputs (registry #35)."""
    xorb = raw ^ (MASK20 if cs else 0)
    ssum = (acc + xorb + (1 - cs)) & MASK20
    if ((ssum >> 19) ^ (ssum >> 18)) & 1:
        return 0xC0000 if (xorb >> 19) & 1 else 0x3FFFF
    return ssum


def cs_eff(l2):
    """Effective coefficient sign = STORED l2 bit 7 DIRECTLY, 1 = positive (session 0025).

    THE ANCHOR: the POST E83 multiplier test — the firmware's own ROM golden table of signed
    products, checked against the real ARU at every hardware boot — passes 20/20 bit-exact in
    aru_post with CSIGN = stored bit7 (1=pos). Session 0022 recorded the same. 0023's port to
    this engine complemented it ('the Multibus line level'), a free choice at the time because
    every output oracle is double-negation-blind to a GLOBAL flip: D1 unity gain, POST, the
    combs, and broadband RT60 (|g| unchanged) all pass either way. What the flip DOES change
    is each recursion's per-frame sign alternation — z=+0.875 lowpass poles vs z=-0.875
    HF-alternators — i.e. WHICH BAND each state cell shapes: the complemented convention was
    the crossover band-inversion (0024 §7). d2g localized it (the w43/95 injection worked
    mid-band under either injection sign); E83 adjudicates the convention. Session 0027 closed
    the loop at pins: rail = cs_eff exactly (aru_U2), 1467/1469."""
    return (l2 >> 7) & 1


def decode_word(w):
    """decode22 + the fields the RTL engine needs precomputed."""
    d = decode22(*w)
    d["cs"] = cs_eff(w[2])
    return d


def program_rows22(wcs):
    """Physical-row execution order under the 0022 coordinate system + the fetch pipeline:
    rows 0..L INCLUSIVE (L+1 steps; row r = CPU word 127-r; L = 128 - reset word; row L =
    the pipeline's extra word — an idle in all 13 factory programs). Returns (rows, L, w_reset)
    with rows = decoded dicts (decode_word)."""
    firing = [k for k, (l0, l1, l2, l3) in enumerate(wcs)
              if (l2 & 3) == 2 and ((l0 >> 3) & 1) == 0]
    if not firing:
        raise ValueError("no reset microword")
    w_reset = max(firing)
    L = 128 - w_reset
    rows = [decode_word(wcs[127 - r]) for r in range(L + 1)]
    return rows, L, w_reset


def fs22(L):
    """Sample rate under the L+1 hardware frame."""
    return MC_HZ / MS_PER_STEP / (L + 1)


class RTL22:
    """Free-running engine at the traced alignment, computing in the COMPLEMENT (phys) domain
    with CPU-domain boundaries. Same run_sample/run_free surface as before the re-sync (rows
    are pre-decoded dicts; run_sample returns CPU-domain ints).

    INTERNAL STATE IS PHYS (active-low DAB domain; plan 024 F1a): R / DM / RES / DAB / ACC all
    carry the complemented patterns the hardware carries (CPU value = s16(~pattern) for the
    16-bit buses; ACC has no CPU-domain value reading — that is the point of the domain).
    Pre-0028 probes that read these attributes directly see the complement of what they saw.

    XREG_host = the host->DSP latch as a CPU-domain value (drives ~XREG_host onto the DAB on
    SRC_XREG reads; static 0 in free-run; the diag bench parks 0x607F — set it for co-sims).

    Stereo input (plan 022 D1b): audio_in may be an int (mono: both halves) or a
    (in_h1, in_h2) pair — the FPC A/D mux alternates channel per half-frame (fig-3.5),
    so RD-AD steps in EXECUTION ORDER alternate halves: first read -> half-1, second ->
    half-2. Which half is LEFT is pinned by the D1 diag oracle (d1_diag_oracles.py)."""

    def __init__(self, fpc_enabled=False, taint=False, taint_th=40, csign_lag=False):
        self.R = [0xFFFF] * 4            # phys ~0 (CPU 0 each)
        self.ACC = 0                     # phys pattern (value -1 = the cleared state)
        self.RES = 0xFFFF                # phys ~0 (CPU 0)
        self.DAB = 0xFFFF                # phys ~0 (CPU 0)
        self.DM = {}                     # phys patterns; unwritten -> 0xFFFF (CPU 0)
        self.CPC = 0
        self.XREG_host = 0               # host->DSP latch, CPU value (bench: 0x607F)
        self.XREG_wr = 0                 # DSP->host latch readback, CPU value (WR XREG)
        self.fpc_enabled = fpc_enabled
        self.csign_lag = csign_lag       # True = FALSIFIED live-sign register variant (#23)
        self._rdad_n = 0                 # per-frame RD-AD occurrence counter (stereo halves)
        # cross-step pipeline registers
        self.wp = None                   # w_{n-1}: gates this step's capture/clear; its operand
                                         # loads at this step's slot-0; its ppA lands @7.43 here
        self.pipe = (RAW_IDLE[1], RAW_IDLE[2], 1)   # (rawB, rawC, cs) of w_{n-2}
        self.step_count = 0
        self.sample_count = 0
        # optional taint tracking (operand provenance) — B3 probe support
        self.taint = taint
        self.taint_th = taint_th
        if taint:
            self.Rsrc = ["init"] * 4
            self.RESsrc = "init"
            self.DABsrc = "init"
            self.DMsrc = {}
            self.ACCsrc = []             # significant contributions since last clear
            self.ppB_src = ""
            self.ppC_src = ""
            self.log = []

    # ---- one microinstruction (one WCS row), events in traced slot order ----
    def step(self, d, audio_in, probe=None, fidx=0, sidx=0):
        wp = self.wp
        R = self.R

        # slot-0 edge: operand SR loads regfile[RA(wp)] POST-write (write-through); the three
        # raw partial products of w_{n-1} are determined here (pairs live AS0/1/2 this step).
        if wp is not None:
            opnd = R[wp["RA"]]
            rawA, rawB, rawC = raw3(opnd, wp["cmag"])
            csw = wp["cs"]
        else:
            opnd = 0xFFFF
            rawA, rawB, rawC = RAW_IDLE
            csw = 1
        rawB2, rawC2, cs2 = self.pipe    # w_{n-2}'s pairs B/C retire this step, OWN sign

        # slot-1.43 edge: ACC <- BE(ACC + ppB(w_{n-2})) — the sat-mux output loads (#35)
        sum0 = backend20(self.ACC, rawB2, cs2)
        if self.taint and self.ppB_src:
            self.ACCsrc.append(self.ppB_src)

        # slot-3.06: XFER CK rise — result reg D = PP bus = BE(sum0 + ppC(w_{n-2})), own sign;
        # RES = PP3..18 pure bit tap (no rounding hardware; the rails keep the tap wrap-free)
        sum1 = backend20(sum0, rawC2, cs2)
        if wp is not None and wp["XFER"]:
            self.RES = (sum1 >> 3) & 0xFFFF
            if self.taint:
                self.RESsrc = "+".join(self.ACCsrc[-4:]) if self.ACCsrc else "acc0"
                res_cpu = s16((~self.RES) & 0xFFFF)
                if abs(res_cpu) > self.taint_th:
                    self.log.append((fidx, sidx, "XFER", res_cpu, self.RESsrc))

        # slot-4.43 edge: sync clear (owner = wp) replaces the ppC(w_{n-2}) register load —
        # the value already reached RES via the PP bus. Default (own-sign schedule): the '163
        # loads the SAME sat-mux output the capture read. csign_lag=True keeps the FALSIFIED
        # live-sign register variant (#23): the register consumes pairC under the RELOADED
        # sub-XOR control cs(w_n) instead of its own word's sign.
        if wp is not None and wp["ZERO"]:
            acc4 = 0
            if self.taint:
                self.ACCsrc = []
        else:
            acc4 = backend20(sum0, rawC2, d["cs"]) if self.csign_lag else sum1
            if self.taint and self.ppC_src:
                self.ACCsrc.append(self.ppC_src)

        # device phase for word w_n (stage-1 fields live all step); the DAB carries phys
        addr = (self.CPC - d["ofst"]) & 0xFFFF
        typ = d["typ"]
        out_da = []
        if typ == 0:                                     # MEMR: DOUT -> DAB (~slot 7)
            self.DAB = self.DM.get(addr, 0xFFFF)
            if self.taint:
                self.DABsrc = self.DMsrc.get(addr, "dm0")
                dab_cpu = s16((~self.DAB) & 0xFFFF)
                if abs(dab_cpu) > self.taint_th:
                    self.log.append((fidx, sidx, f"MEMR of={d['ofst']}", dab_cpu, self.DABsrc))
        elif typ == 1:                                   # MEMW: RDRREG drives; DIN latches @slot4
            self.DAB = self.RES                          # (post-capture RES: capture was slot 3)
            self.DM[addr] = self.DAB
            if self.taint:
                self.DABsrc = self.RESsrc
                self.DMsrc[addr] = f"w@f{fidx}s{sidx}({self.RESsrc})"
                dab_cpu = s16((~self.DAB) & 0xFFFF)
                if abs(dab_cpu) > self.taint_th:
                    self.log.append((fidx, sidx, f"MEMW of={d['ofst']}", dab_cpu, self.RESsrc))
        elif typ == 2:                                   # IO: one driver per sel, else hold
            sel = d["sel"]
            if sel == SRC_RDRREG:
                self.DAB = self.RES
                if self.taint:
                    self.DABsrc = self.RESsrc
            elif sel == SRC_RDAD:
                ain = audio_in
                if isinstance(ain, (tuple, list)):       # stereo: A/D mux alternates halves
                    ain = ain[self._rdad_n & 1]
                self._rdad_n += 1
                fixed = (fpc_input_float_to_fixed(ain) if self.fpc_enabled
                         else (ain & 0xFFFF))
                self.DAB = (~fixed) & 0xFFFF             # the A/D drives the complement (§5.6)
                if self.taint:
                    self.DABsrc = f"INPUT@f{fidx}"
            elif sel == SRC_XREG:
                self.DAB = (~self.XREG_host) & 0xFFFF    # host latch, complemented onto the DAB
                if self.taint:
                    self.DABsrc = "xreg"
            if d["WRDA"]:                                # FPC captures the DAB at slot 5,
                v_cpu = (~self.DAB) & 0xFFFF             # complementing back (§5.6 mirror)
                ov = (fpc_output_fixed_to_float(v_cpu) if self.fpc_enabled
                      else s16(v_cpu))
                out_da = [(c, ov) for c in d["chans"]]
                if self.taint and abs(s16(v_cpu)) > self.taint_th:
                    self.log.append((fidx, sidx, f"OUT {''.join(d['chans'])}", s16(v_cpu), self.DABsrc))
        # typ 3 idle: bus hold

        # slot-7.43 edge: ACC <- BE(acc4 + ppA(w_{n-1})); regfile write @MS7 (unconditional);
        # WR XREG captures the DAB (readback pair complements back to the CPU domain)
        self.ACC = backend20(acc4, rawA, csw)
        if self.taint and wp is not None:
            piA = B._s20(rawA) + 1
            if abs(piA) > self.taint_th * 8:
                self.ACCsrc.append(f"R{wp['RA']}({self.Rsrc[wp['RA']]})x"
                                   f"{'+' if csw else '-'}{wp['cmag']}/32")
        R[d["WA"]] = self.DAB
        if self.taint:
            self.Rsrc[d["WA"]] = f"{self.DABsrc}>R{d['WA']}@f{fidx}s{sidx}"
        if typ == 2 and d["WRX"]:
            self.XREG_wr = (~self.DAB) & 0xFFFF

        # carry the pipeline: w_{n-1}'s pairs B/C retire next step under its own sign
        self.pipe = (rawB, rawC, csw)
        if self.taint:
            tag = (f"R{wp['RA']}({self.Rsrc[wp['RA']]})x{'+' if csw else '-'}{wp['cmag']}/32"
                   if wp is not None else "")
            piB = B._s20(rawB) + 1
            piC = B._s20(rawC) + 1
            self.ppB_src = tag + ":B" if (wp is not None and abs(piB) > self.taint_th * 8) else ""
            self.ppC_src = tag + ":C" if (wp is not None and abs(piC) > self.taint_th * 8) else ""
        self.wp = d
        self.step_count += 1
        if probe is not None:
            probe.append(dict(d=d, addr=addr, dab=(~self.DAB) & 0xFFFF,
                              opnd=s16((~opnd) & 0xFFFF), ACC=self.ACC,
                              RES=s16((~self.RES) & 0xFFFF), out_da=out_da,
                              R=[s16((~v) & 0xFFFF) for v in R]))
        return out_da

    # ---- one frame = len(rows) steps (L+1 for factory programs), then CPC += 1 ----
    def run_sample(self, rows, audio_in, probe=None):
        outs = []
        fidx = self.sample_count
        self._rdad_n = 0                                 # new frame: A/D mux back to half-1
        for i, d in enumerate(rows):
            outs.extend(self.step(d, audio_in, probe=probe, fidx=fidx, sidx=i))
        self.CPC = (self.CPC + 1) & 0xFFFF               # RESET/ event -> CPC +1 per frame
        self.sample_count += 1
        return outs

    def run_free(self, rows, input_signal, n_samples):
        """Returns dict chan -> list of int (per-frame last write wins; unwritten -> 0).
        input_signal elements: int (mono) or (in_h1, in_h2) stereo pairs."""
        chans = {c: [0] * n_samples for c in "ABCD"}
        get = (input_signal if callable(input_signal)
               else (lambda n: input_signal[n] if n < len(input_signal) else 0))
        for n in range(n_samples):
            x = get(n)
            if isinstance(x, (tuple, list)):
                x = (int(x[0]) & 0xFFFF, int(x[1]) & 0xFFFF)
            else:
                x = int(x) & 0xFFFF
            for c, v in self.run_sample(rows, x):
                chans[c][n] = v
        return chans


# ---------------------------------------------------------------------------
# Self-tests — every expectation DERIVED from the physical law (plan 024 F1b), never
# patched to match the code. The value view used throughout (derived in the module
# docstring): π(phase) = s20(raw)+1 on the PHYS operand ~x; accumulate adds ±π by cs;
# ZERO clear -> value -1; capture y = V >> 3 (arithmetic floor; rails ±2^18 make the
# PP3..18 tap wrap-free). Word sum: Σπ(F,c) = 3·dual(c) + 3 - product20(-F-1, c, 1).
# ---------------------------------------------------------------------------
def _pi_phases(F_cpu, cmag):
    """Per-phase value increments π_k of a word whose CPU-domain operand is F_cpu —
    computed straight from the gate array on the complemented operand (independent
    of the engine's raw3/backend walk)."""
    C = [(cmag >> i) & 1 for i in range(6)]
    SR = B.load_SR(s16((~F_cpu) & 0xFFFF))
    out = []
    for p, (m0, m1) in enumerate(((C[4], C[5]), (C[2], C[3]), (C[0], C[1]))):
        if p:
            SR = B.shift_right2(SR)
        out.append(B._s20(B.comb_array(SR, m0, m1)) + 1)
    return out


def _dual(cmag):
    C = [(cmag >> i) & 1 for i in range(6)]
    return sum(1 for m0, m1 in ((C[4], C[5]), (C[2], C[3]), (C[0], C[1])) if m0 and m1)


def _test_value_bridge():
    """The raw3/booth3/product20 value bridge (registry #30: the CPU-domain laws are
    value-level identities of the same bits):
      (a) sum(booth3(F,c,s)) == product20(F,c,s)              (the historical identity)
      (b) Σ_k (3·dual_k - s20(raw3(F,c)_k)) == product20(F,c,1)  (raw patterns <-> value)
      (c) Σπ(F,c) == 3·dual(c) + 3 - product20(~F value, c, 1)   (the π word-sum law)
      (d) zero-coefficient phases are value-inert: π == 0 exactly (the 0xFFFFF baseline)."""
    import random
    rnd = random.Random(22)
    n = 0
    for _ in range(2000):
        F = rnd.randint(-32768, 32767)
        c = rnd.randint(0, 63)
        s = rnd.randint(0, 1)
        assert sum(booth3(F, c, s)) == product20(F, c, s), (F, c, s)
        C = [(c >> i) & 1 for i in range(6)]
        duals = [(1 if (m0 and m1) else 0)
                 for m0, m1 in ((C[4], C[5]), (C[2], C[3]), (C[0], C[1]))]
        rr = raw3(F & 0xFFFF, c)
        assert sum(3 * dk - B._s20(r) for dk, r in zip(duals, rr)) == product20(F, c, 1), (F, c)
        assert (sum(_pi_phases(F, c))
                == 3 * _dual(c) + 3 - product20(s16((~F) & 0xFFFF), c, 1)), (F, c)
        n += 1
    for F, c, s, _exp in B.GOLDENS:
        assert sum(booth3(s16(F), c, s)) == product20(s16(F), c, s)
        n += 1
    assert _pi_phases(12345, 0) == [0, 0, 0]     # (d) zero rails are exactly inert
    assert _pi_phases(-1, 0) == [0, 0, 0]
    print(f"  value bridge (raw3/booth3/π)  OK ({n} cases incl. goldens; zero-rail π == 0)")


def _rows(words):
    return [decode_word(w) for w in words]


def _test_passthrough():
    """RTL-authored positive-unity passthrough. Law derivation (docstring value view):
    the ZERO clear (owner w0) lands at step1 -> V = -1; the unity word w1 (cmag 32, cs 1,
    operand phys ~x) contributes Σπ(x,32) = 0 + 3 - product20(-x-1,32,1) = 3 - (8(-x-1)+3)
    = 8x+8 across steps 2-3; capture (wp = w2.XFER) at step 3 reads V1 = 8x+7;
    y = (8x+7)>>3 = x for ALL x (floor eats the +7; at x=+32767 V1 = 262143 = the rail
    exactly, still in range). The w0 flag-word sign is INERT (cmag-0 -> π = 0) — the old
    'opposite-sign residue cancellation' idiom dissolved (registry #30)."""
    rows = _rows([
        enc_io(sel=SRC_RDAD, wa=1, cmag=0, zero=1, csign=0),   # DAB=~x; R1<-~x; ZERO @step1
        enc_idle(ra=1, cmag=32, csign=1),                      # MAC: x * 1.0
        enc_idle(xfer=1),                                      # capture @step3 slot-3.06
        enc_io(sel=SRC_RDRREG, wrda=True, chans="A", reset=True),
    ])
    eng = RTL22()
    xs = [1000, -2000, 12345, -30000, 0, 7, 32767, -32768]
    ys = [dict(eng.run_sample(rows, x & 0xFFFF)).get("A", 0) for x in xs]
    assert ys == xs, f"passthrough mismatch: {ys} vs {xs}"
    # the XREG host-latch boundary: read SRC_XREG through the same unity MAC
    rows_x = _rows([
        enc_io(sel=SRC_XREG, wa=1, cmag=0, zero=1, csign=0),
        enc_idle(ra=1, cmag=32, csign=1),
        enc_idle(xfer=1),
        enc_io(sel=SRC_RDRREG, wrda=True, chans="A", reset=True),
    ])
    eng = RTL22()
    eng.XREG_host = 0x607F
    ys = [dict(eng.run_sample(rows_x, 0)).get("A", 0) for _ in range(3)]
    assert ys == [0x607F] * 3, f"XREG passthrough mismatch: {ys}"
    print("  RTL passthrough               OK (out == in incl. ±full-scale; XREG host latch "
          "0x607F reads back exactly)")


def _test_negative_unity():
    """The lone NEGATIVE unity — the territory no factory oracle covered, where the physical
    law differs from the old value engine (the e5 census: 'consistently -2'). Derivation:
    w1 = cmag 32 cs 0 -> V1 = -1 - Σπ(x,32) = -1 - (8x+8) = -8x-9; y = (-8x-9)>>3 = -x-2
    (floor(-9/8) = -2). At x = +32767 the single accumulate lands at value -262145 <
    -2^18 -> SAT fires and the '163 loads the clamp -> V1 = -262144, y = -32768 (the rail).
    The old CPU-domain engine returned -x (and sat16(-x) at the rail) — this test pins the
    REAL hardware law and would catch any regression to the value model (registry #31)."""
    rows = _rows([
        enc_io(sel=SRC_RDAD, wa=1, cmag=0, zero=1, csign=1),
        enc_idle(ra=1, cmag=32, csign=0),                      # MAC: x * (-1.0)
        enc_idle(xfer=1),
        enc_io(sel=SRC_RDRREG, wrda=True, chans="A", reset=True),
    ])
    eng = RTL22()
    xs = [1000, -2000, 12345, -30000, 0, 7, 16383, -16384, -32768, 32767]
    ys = [dict(eng.run_sample(rows, x & 0xFFFF)).get("A", 0) for x in xs]
    exp = [(-x - 2) if x != 32767 else -32768 for x in xs]
    assert ys == exp, f"negative unity mismatch: {ys} vs {exp}"
    print("  RTL negative unity            OK (y = -x-2, the physical -2LSB law; "
          "+full-scale clamps to -32768 via the sat-mux)")


def _comb_rows(D, g, flag_csign=1):
    return _rows([
        enc_io(sel=SRC_RDAD, wa=0, cmag=0, zero=1, csign=0),   # R0<-~x; ZERO
        enc_memr(D, wa=1, ra=0, cmag=32, csign=1),             # DAB=~y[n-D]; R1<-it; MAC x*1.0
        enc_idle(ra=1, cmag=g, csign=1),                       # MAC +g/32 * y[n-D]
        enc_idle(xfer=1, csign=flag_csign),                    # capture @step4
        enc_memw(0x0000),                                      # DM[CPC] <- RES (phys)
        enc_io(sel=SRC_RDRREG, wrda=True, chans="A", reset=True),
    ])


def _test_feedback_comb(D=40, g=16, n=200, opposite=False):
    """Exact vs the closed-form recurrence DERIVED from the physical law:
        V1[n] = -1 + Σπ(x[n],32) + Σπ(y[n-D],g)
              = 8·x[n] + 10 + 3·dual(g) - product20(-y[n-D]-1, g, 1)
        y[n]  = V1[n] >> 3          (arithmetic floor; no +4, no sat16 — rails suffice)
    (Σπ(x,32) = 8x+8 as in the passthrough; unwritten DMEM reads phys ~0 -> y' = 0 early.)
    The flag word's sign is INERT under the physical law (cmag-0 phases have π = 0 exactly),
    so opposite=True must give the IDENTICAL sequence — the dissolved-'residue' pin."""
    rows = _comb_rows(D, g, flag_csign=(0 if opposite else 1))
    eng = RTL22()
    out, exp, ym = [], [], {}
    for i in range(n):
        x = 16000 if i == 0 else 0
        out.append(dict(eng.run_sample(rows, x & 0xFFFF)).get("A", 0))
        yd = ym.get(i - D, 0)
        e = (8 * x + 10 + 3 * _dual(g) - product20(-yd - 1, g, 1)) >> 3
        ym[i] = e
        exp.append(e)
    assert out == exp, ("comb closed-form mismatch",
                        [(i, a, b) for i, (a, b) in enumerate(zip(out, exp)) if a != b][:5])
    peaks = [(i, v) for i, v in enumerate(out) if abs(v) > 50]
    ideal = [(k * D, int(16000 * (g / 32) ** k)) for k in range(5)]
    for (pi, pv), (ei, ev) in zip(peaks, ideal):
        assert pi == ei and abs(pv - ev) <= 10, f"comb peak {(pi, pv)} vs ideal {(ei, ev)}"
    tag = "OPPOSITE-sign flag (inert: π=0)" if opposite else "same-sign flag"
    print(f"  RTL feedback comb g={g}/32     OK (phys closed-form EXACT; FULL g; {tag}; "
          f"peaks {peaks[:4]})")


def _test_csign_split():
    """Regression-pin BOTH sign schedules against the physical law: the default own-sign
    engine and the FALSIFIED live-sign-register variant (csign_lag=True, dead-end #23).
    Under the physical law a zero-coefficient word's sign is INERT (π = 0), so the old
    discriminator (flag-word residues) dissolves; the discriminating structure is a
    cmag-5 word (pairC = ×1, πC != 0) whose pairC RETIRES during a step executing an
    OPPOSITE-sign word (w3, csign=0 — free to choose: its own cmag is 0 = inert):
      capture#1 (step3, wp=w2.XFER):  V1 = -1 + πB(w1) + πC(w1)   [capture is ALWAYS own-sign]
      register @step3: own-sign -> the '163 loads the SAME sat-mux value V1;
                       lag      -> re-evaluated under cs(w3)=0:  V = -1 + πB(w1) - πC(w1)
      capture#2 (step4, wp=w3.XFER; w2's phases π=0): own -> capB == capA;
                       lag -> capB = (-1 + πB - πC) >> 3."""
    rows = _rows([
        enc_io(sel=SRC_RDAD, wa=0, cmag=0, zero=1, csign=1),
        enc_idle(ra=0, cmag=5, csign=1),                       # +5/32, pairC = ×1 (πC != 0)
        enc_idle(cmag=0, xfer=1, csign=1),                     # capture#1 owner
        enc_io(sel=SRC_RDRREG, wrda=True, chans="A", xfer=1, csign=0),  # OPPOSITE; cap#2 owner
        enc_io(sel=SRC_RDRREG, wrda=True, chans="B", reset=True),
    ])

    def expect(x, lag):
        piA, piB, piC = _pi_phases(x, 5)
        assert piA == 0                                        # pair A of cmag 5 is a zero pair
        v1 = -1 + piB + piC
        capA = v1 >> 3
        v2 = (-1 + piB - piC) if lag else v1
        return capA, v2 >> 3

    eng = RTL22(csign_lag=True)          # the falsified live-sign register variant
    eng_own = RTL22()                    # default: own-sign everywhere
    n_diff = 0
    for x in (1000, -2000, 12345, 32767, -32768, 7):
        outs = dict(eng.run_sample(rows, x & 0xFFFF))
        outs_own = dict(eng_own.run_sample(rows, x & 0xFFFF))
        eA, eB = expect(x, True)
        oA, oB = expect(x, False)
        assert (outs.get("A", 0), outs.get("B", 0)) == (eA, eB), (x, outs, (eA, eB), "lag")
        assert (outs_own.get("A", 0), outs_own.get("B", 0)) == (oA, oB), (x, outs_own, (oA, oB), "own")
        assert oB == oA                  # own-sign: the register loaded the captured PP value
        if oB != eB:
            n_diff += 1
    assert n_diff >= 4, "variants should differ at capture#2 (the register-consumed pairC)"
    print("  CSIGN split (cap=own/reg=live) OK (own: register == capture; lag variant differs "
          "at capture#2 by the re-signed pairC)")


def _test_sat_clamp_feeds_acc():
    """Registry #35: the sat-mux clamp FEEDS THE ACCUMULATOR (the '163 loads the clamp) —
    pinned at pins by the diag-3 tail (feedback table U42.3 = 000P); this is the engine-level
    regression. Program: +unity, +unity, -unity on x, then capture. Value walk at x=+32767
    (πA(unity) = 8x+8 = 262144):
      clear -> -1;  +262144 -> 262143 (the +rail EXACTLY, in range, no SAT);
      +262144 -> 524287: SAT fires -> the '163 loads the CLAMP +262143;
      -262144 -> -1;  capture y = -1 >> 3 = -1.
    A wrap-only ACC (the pre-0028 engine) would hold 524287 (fits 20 bits, s19==s18 never
    trips on the STORED value) and produce y = +32767 — maximally wrong. The in-range
    control (x=16000) exercises the same walk without SAT: V1 = 8x+7 -> y = x."""
    rows = _rows([
        enc_io(sel=SRC_RDAD, wa=0, cmag=0, zero=1, csign=1),
        enc_idle(ra=0, cmag=32, csign=1),                      # +1.0
        enc_idle(ra=0, cmag=32, csign=1),                      # +1.0 (transient SAT here)
        enc_idle(ra=0, cmag=32, csign=0),                      # -1.0 (returns in range)
        enc_idle(xfer=1),
        enc_io(sel=SRC_RDRREG, wrda=True, chans="A", reset=True),
    ])
    eng = RTL22()
    ys = [dict(eng.run_sample(rows, 32767)).get("A", 0) for _ in range(4)]
    assert ys == [-1] * 4, f"SAT-clamp-into-ACC mismatch: {ys} (wrap-only would give +32767)"
    eng = RTL22()
    ys = [dict(eng.run_sample(rows, 16000)).get("A", 0) for _ in range(4)]
    assert ys == [16000] * 4, f"in-range control mismatch: {ys}"
    print("  SAT clamp feeds ACC (#35)     OK (transient mid-group SAT converges to the rail: "
          "y = -1, not the wrap ghost +32767; in-range control exact)")


def _test_concert_extraction():
    import json
    cand = os.path.join(os.environ.get("E1_CACHE_DIR",
                        os.path.join(os.path.dirname(os.path.abspath(__file__)), "session0022_probes")),
                        "wcs_cache.json")
    if not os.path.exists(cand):
        print("  CONCERT extraction            SKIPPED (no wcs_cache.json)")
        return None
    rec = json.load(open(cand))["1"]
    b = bytes.fromhex(rec["wcs"])
    wcs = [(b[4 * k], b[4 * k + 1], b[4 * k + 2], b[4 * k + 3]) for k in range(128)]
    rows, L, w_reset = program_rows22(wcs)
    assert (L, w_reset) == (104, 24), (L, w_reset)
    assert len(rows) == 105
    cnt = {t: sum(1 for d in rows if d["typ"] == t) for t in range(4)}
    assert (cnt[0], cnt[1], cnt[2], cnt[3]) == (55, 36, 10, 4), cnt   # +1 idle = row 104
    xtr = rows[104]
    assert xtr["typ"] == 3 and xtr["cmag"] == 0 and not xtr["XFER"] and not xtr["ZERO"]
    rst = rows[103]
    assert rst["typ"] == 2 and rst["RESET"] and rst["WRDA"] and rst["chans"] == ["C"]
    print(f"  CONCERT extraction            OK (L={L}, {len(rows)}-step frame, census "
          f"{cnt[0]}/{cnt[1]}/{cnt[2]}/{cnt[3]}, fs={fs22(L):.1f} Hz, row-{L} idle confirmed)")
    return rows


if __name__ == "__main__":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass
    print("### aru_freerun22_rtl self-tests (traced alignment, complement-domain law) ###")
    _test_value_bridge()
    _test_passthrough()
    _test_negative_unity()
    _test_feedback_comb(D=40, g=16)
    _test_feedback_comb(D=37, g=21)     # multi-pair cmag: three ×1 digits span all 3 phases
    _test_feedback_comb(D=37, g=21, opposite=True)   # flag-word sign inertness (π = 0)
    _test_csign_split()                 # pins own-sign default vs the falsified #23 variant
    _test_sat_clamp_feeds_acc()         # pins the #35 clamp-into-ACC path
    _test_concert_extraction()
    print("ALL PASS")
