#!/usr/bin/env python3
"""aru_freerun22_rtl — THE RTL ARBITER (plan 021 Phase A): the free-running 224XL ARU/T&C/DMEM
under the session-0022 coordinate system with the MAC/register/XFER alignment taken from the
TRACED control pipeline (netlist §3.5-3.11, §2T, §4.7-4.9, §4F, §6D + fig-3.3/3.4), not from
behavioral convention. No knobs: every capture point sits at its traced edge.

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
                   slot3(n)..slot2(n+1) — exactly aligned with w_{n-1}'s partial products.
                   Effective sign = the Multibus level (~stored bit7): E3b-stable, and the
                   traced chain (stored -> MI23 -> JK -> sub-ctrl) natively carries it.
  serializer       tc_U11/U10 (74195, CLK=ARUCKE, SH//LD=AS1/, P3=Q2 feedback): loads w_n's
                   C-bits at the slot-6 edge of step n; w_n's Booth pairs (C4,C5),(C2,C3),
                   (C0,C1) are live during AS0/AS1/AS2 OF STEP n+1 (the third pair via the
                   P3=Q2 feedback at the next load edge). The multiply of word W executes
                   physically during step W+1.
  operand SR       74194s (CLK=ARUCK, S1/S0 mode = LOAD during AS2 per fig-3.4): the load
                   EDGE is the slot-0 edge of step n+1, sampling regfile[RA(w_n)] AFTER
                   step n's MS7 write => WRITE-THROUGH: a word's operand sees its own step's
                   regfile write. Shifts at the slot-3/slot-6 edges keep F, F>>2, F>>4
                   aligned with pairs A/B/C (golden-exact pairing).
  product reg      aru_U10/U11/U12 (CLK=ARUCK): latches each partial product at slots 0/3/6:
                   PR@3.58(W+1)=ppA(W), PR@6.58(W+1)=ppB(W), PR@0.58(W+2)=ppC(W).
  accumulator      aru_U45-49 (74LS163 always-load, CP=ARUCKE/, sync /CLR=ZERO/), fed by the
                   back-end adder chain (aru_U19-23 + sub-XOR): the adder needs ~1.4 slots to
                   settle after a PR change, so each ACC edge captures the sum formed from the
                   PREVIOUS PR value — the accumulate lags the PR latch by one full ARUCKE/
                   edge (fig-3.4, owner-read: "the accumulate runs i2.AS1->i3.AS0, one AS
                   behind the partial products = the pipeline register").
                   => ACC edges of step n: @4.43 += ppC(w_{n-2}); @7.43 += ppA(w_{n-1});
                      @1.43(n+1) += ppB(w_{n-1}).  The 20-bit chain WRAPS (mod 2^20) —
                   saturation lives in the sat-mux on the result path only.
  XFER CK          NAND(AS0, tc_U19.Q5, ARUCKE/): low slots 1-2 of step n iff w_{n-1}.XFER;
                   the result reg (74F374) captures on its RISE at the slot-3 edge.
                   ** THE RESULT REG D-INPUTS ARE ON THE PP BUS (netlist §4.2: PP3..PP18 ->
                   aru_U43/U44 D pins) = the SAT-MUX / ADDER OUTPUT, not the accumulator
                   register. ** At 3.06(n) the adder holds ACC_registered (through
                   ppB(w_{n-2}), added @1.43) + PR (= ppC(w_{n-2}), latched @0.58):
                   => RES <- sat16((ACC + ppC(w_{n-2}) + 4)>>3) — the FULL group MAC,
                   pairC INCLUDED via the combinational path. (Session 0024 correction:
                   0023 read the register instead of the PP bus — an assumption no prior
                   oracle could see: POST/D1/comb tests all had cmag&3==0 at captures.)
  ZERO/            NAND(tc_U19.Q6, AS0), 163 sync clear landing at the 4.43 edge of step n
                   iff w_{n-1}.ZERO (same owner as the capture, one edge after it;
                   the no-lag owner w_n is EMPIRICALLY DEAD — c2 probe: zero output).
                   The clear replaces the ppC(w_{n-2}) REGISTER add — the value already
                   reached RES through the PP bus; the clear just resets the accumulator
                   for the next group. fig-3.4 verbatim: "ZERO/ clears it at i2.AS0 so it
                   reads 0 at i2.AS1."
                   => An XFER+ZERO word X (the dominant factory idiom, 473/486) captures
                   the group MAC through w_{X-1} COMPLETE — every stored cmag acts at
                   full weight (the mirrored cmag 13/10/6 pre-capture words in the factory
                   programs are live values, not don't-care LSBs).
  DMEM             addr = CPC - stored offset; CAS falls at slot 4 (early-write DIN latch =
                   the JUST-captured RES on MEMW); DOUT lands ~slot 7 on MEMR (the MS7
                   regfile write captures it; nothing samples it earlier).
  regfile write    DAB WSTB/ = ~MS7: R[WA(w_n)] <- DAB level at slot 7, every step.
  FPC out          FPC CK = MS5: the D/A double buffer captures the DAB at slot 5 of a WR-DA
                   step (RES is post-capture by then).
  CPC              +1 per frame on the RESET/ event (during the row-L step; all row
                   addresses of the frame use the pre-bump value).

Run:  python tools/aru_freerun22_rtl.py   (self-tests: booth3 identity, RTL-authored
      passthrough EXACT, feedback comb EXACT incl. multi-pair cmag, CONCERT extraction)
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
_WRAP = 1 << 20
_HALF = 1 << 19


def wrap20(v):
    """The 74LS163 accumulator chain wraps mod 2^20 (signed). Saturation is in the sat-mux
    on the result path (res_from_acc), NOT the accumulator."""
    v &= _WRAP - 1
    return v - _WRAP if v >= _HALF else v


@lru_cache(maxsize=None)
def booth3(F, cmag, cs):
    """The three per-phase signed partial products of one multiply, from the VERIFIED gate
    Booth array (aru_booth) with the +3 dual-rail correction applied per phase.
    Identity: sum(booth3(F,c,s)) == aru_freerun.product20(F,c,s) for all inputs."""
    C = [(cmag >> i) & 1 for i in range(6)]
    SR0 = B.load_SR(s16(F))
    SR1 = B.shift_right2(SR0)
    SR2 = B.shift_right2(SR1)
    pps = []
    for SR, (m0, m1) in zip((SR0, SR1, SR2), ((C[4], C[5]), (C[2], C[3]), (C[0], C[1]))):
        t = -B._s20(B.comb_array(SR, m0, m1)) + (3 if (m0 and m1) else 0)
        pps.append(t if cs else -t)
    return tuple(pps)


def cs_eff(l2):
    """Effective coefficient sign = the Multibus level of stored bit 7 (E3b-stable; the traced
    chain stored -> MI23 -> tc_U20 JK -> sub-ctrl natively inverts the stored bit)."""
    return ((l2 >> 7) & 1) ^ 1


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
    """Free-running engine at the traced alignment. Same run_sample/run_free surface as
    aru_freerun22.FreeRun22 (rows are pre-decoded dicts here).

    Stereo input (plan 022 D1b): audio_in may be an int (mono: both halves) or a
    (in_h1, in_h2) pair — the FPC A/D mux alternates channel per half-frame (fig-3.5),
    so RD-AD steps in EXECUTION ORDER alternate halves: first read -> half-1, second ->
    half-2. Which half is LEFT is pinned by the D1 diag oracle (d1_diag_oracles.py)."""

    def __init__(self, fpc_enabled=False, taint=False, taint_th=40):
        self.R = [0, 0, 0, 0]
        self.ACC = 0
        self.RES = 0
        self.DAB = 0
        self.DM = {}
        self.CPC = 0
        self.XREG_wr = 0                 # DSP->host latch (WR XREG captures the DAB; readback only)
        self.fpc_enabled = fpc_enabled
        self._rdad_n = 0                 # per-frame RD-AD occurrence counter (stereo halves)
        # cross-step pipeline registers
        self.wp = None                   # w_{n-1}: gates this step's capture/clear; its operand
                                         # loads at this step's slot-0; its ppA lands @7.43 here
        self.ppB_pend = 0                # w_{n-2}'s ppB (lands @1.43 of this step)
        self.ppC_pend = 0                # w_{n-2}'s ppC (lands @4.43, or dies to the clear)
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

        # slot-0 edge: operand SR loads regfile[RA(wp)] POST-write (write-through); wp's three
        # partial products are fixed here (CSIGN JK carries wp's sign for all three).
        if wp is not None:
            opnd = R[wp["RA"]]
            ppA, ppB, ppC = booth3(opnd, wp["cmag"], wp["cs"])
        else:
            opnd, ppA, ppB, ppC = 0, 0, 0, 0

        # slot-1.43 edge: += ppB(w_{n-2}) (the adder-pipeline lag: fig-3.4 "one AS behind")
        self.ACC = wrap20(self.ACC + self.ppB_pend)
        if self.taint and self.ppB_src:
            self.ACCsrc.append(self.ppB_src)

        # slot-3.06: XFER CK rise — result reg D = PP bus (sat-mux/adder out, §4.2):
        # ACC_registered + PR(= ppC(w_{n-2})) — the FULL group MAC via the comb path
        if wp is not None and wp["XFER"]:
            self.RES = res_from_acc(wrap20(self.ACC + self.ppC_pend))
            if self.taint:
                self.RESsrc = "+".join(self.ACCsrc[-4:]) if self.ACCsrc else "acc0"
                if abs(self.RES) > self.taint_th:
                    self.log.append((fidx, sidx, "XFER", self.RES, self.RESsrc))

        # slot-4.43 edge: sync clear (owner = wp) replaces the ppC(w_{n-2}) REGISTER add —
        # the value already reached RES via the PP bus; else ppC(w_{n-2}) accumulates
        if wp is not None and wp["ZERO"]:
            self.ACC = 0
            if self.taint:
                self.ACCsrc = []
        else:
            self.ACC = wrap20(self.ACC + self.ppC_pend)
            if self.taint and self.ppC_src:
                self.ACCsrc.append(self.ppC_src)

        # device phase for word w_n (stage-1 fields live all step)
        addr = (self.CPC - d["ofst"]) & 0xFFFF
        typ = d["typ"]
        out_da = []
        if typ == 0:                                     # MEMR: DOUT -> DAB (~slot 7)
            self.DAB = self.DM.get(addr, 0) & 0xFFFF
            if self.taint:
                self.DABsrc = self.DMsrc.get(addr, "dm0")
                if abs(s16(self.DAB)) > self.taint_th:
                    self.log.append((fidx, sidx, f"MEMR of={d['ofst']}", s16(self.DAB), self.DABsrc))
        elif typ == 1:                                   # MEMW: RDRREG drives; DIN latches @slot4
            self.DAB = self.RES & 0xFFFF                 # (post-capture RES: capture was slot 3)
            self.DM[addr] = self.DAB
            if self.taint:
                self.DABsrc = self.RESsrc
                self.DMsrc[addr] = f"w@f{fidx}s{sidx}({self.RESsrc})"
                if abs(s16(self.DAB)) > self.taint_th:
                    self.log.append((fidx, sidx, f"MEMW of={d['ofst']}", s16(self.DAB), self.RESsrc))
        elif typ == 2:                                   # IO: one driver per sel, else hold
            sel = d["sel"]
            if sel == SRC_RDRREG:
                self.DAB = self.RES & 0xFFFF
                if self.taint:
                    self.DABsrc = self.RESsrc
            elif sel == SRC_RDAD:
                ain = audio_in
                if isinstance(ain, (tuple, list)):       # stereo: A/D mux alternates halves
                    ain = ain[self._rdad_n & 1]
                self._rdad_n += 1
                self.DAB = (fpc_input_float_to_fixed(ain) if self.fpc_enabled
                            else (ain & 0xFFFF))
                if self.taint:
                    self.DABsrc = f"INPUT@f{fidx}"
            elif sel == SRC_XREG:
                self.DAB = 0                             # host->DSP latch; static in free-run
                if self.taint:
                    self.DABsrc = "xreg0"
            if d["WRDA"]:                                # FPC captures the DAB at slot 5
                ov = (fpc_output_fixed_to_float(self.DAB) if self.fpc_enabled
                      else s16(self.DAB))
                out_da = [(c, ov) for c in d["chans"]]
                if self.taint and abs(s16(self.DAB)) > self.taint_th:
                    self.log.append((fidx, sidx, f"OUT {''.join(d['chans'])}", s16(self.DAB), self.DABsrc))
        # typ 3 idle: bus hold

        # slot-7.43 edge: += ppA(w_{n-1}); regfile write @MS7 (unconditional); WR XREG
        self.ACC = wrap20(self.ACC + ppA)
        if self.taint and wp is not None and abs(ppA) > self.taint_th * 8:
            self.ACCsrc.append(f"R{wp['RA']}({self.Rsrc[wp['RA']]})x{'+' if wp['cs'] else '-'}{wp['cmag']}/32")
        R[d["WA"]] = s16(self.DAB)
        if self.taint:
            self.Rsrc[d["WA"]] = f"{self.DABsrc}>R{d['WA']}@f{fidx}s{sidx}"
        if typ == 2 and d["WRX"]:
            self.XREG_wr = self.DAB & 0xFFFF

        # carry the pipeline
        self.ppB_pend = ppB
        self.ppC_pend = ppC
        if self.taint:
            tag = (f"R{wp['RA']}({self.Rsrc[wp['RA']]})x{'+' if wp['cs'] else '-'}{wp['cmag']}/32"
                   if wp is not None else "")
            self.ppB_src = tag + ":B" if (wp is not None and abs(ppB) > self.taint_th * 8) else ""
            self.ppC_src = tag + ":C" if (wp is not None and abs(ppC) > self.taint_th * 8) else ""
        self.wp = d
        self.step_count += 1
        if probe is not None:
            probe.append(dict(d=d, addr=addr, dab=self.DAB, opnd=opnd,
                              ACC=self.ACC, RES=self.RES, out_da=out_da, R=list(R)))
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
# Self-tests
# ---------------------------------------------------------------------------
def _test_booth3_identity():
    import random
    rnd = random.Random(22)
    n = 0
    for _ in range(4000):
        F = rnd.randint(-32768, 32767)
        c = rnd.randint(0, 63)
        s = rnd.randint(0, 1)
        assert sum(booth3(F, c, s)) == product20(F, c, s), (F, c, s)
        n += 1
    for F, c, s, _exp in B.GOLDENS:
        assert sum(booth3(s16(F), c, s)) == product20(s16(F), c, s)
        n += 1
    print(f"  booth3 per-phase identity     OK (sum == product20, {n} cases incl. goldens)")


def _rows(words):
    return [decode_word(w) for w in words]


def _test_passthrough():
    # RTL-authored: the MAC word's product lands one step later than behavioral, so XFER sits
    # one word AFTER the MAC word. In-window residues: w0's three cmag-0 phases at cs_eff=0
    # (-3) plus the MAC's FULL product via the PP-bus capture: (8x-3+4)>>3 = x.
    rows = _rows([
        enc_io(sel=SRC_RDAD, wa=1, cmag=0, zero=1, csign=1),   # DAB=in; R1<-in; ZERO clears @step1
        enc_idle(ra=1, cmag=32, csign=0),                      # MAC: in x 1.0 (cs_eff=1)
        enc_idle(xfer=1),                                      # capture @step3 slot-3.06
        enc_io(sel=SRC_RDRREG, wrda=True, chans="A", reset=True),
    ])
    eng = RTL22()
    xs = [1000, -2000, 12345, -30000, 0, 7, 32767, -32768]
    ys = [dict(eng.run_sample(rows, x & 0xFFFF)).get("A", 0) for x in xs]
    assert ys == xs, f"passthrough mismatch: {ys} vs {xs}"
    print("  RTL passthrough               OK (out == in, same frame; XFER one word after MAC)")


def _comb_rows(D, g):
    return _rows([
        enc_io(sel=SRC_RDAD, wa=0, cmag=0, zero=1, csign=1),   # R0<-x; ZERO; residues -2 in-window
        enc_memr(D, wa=1, ra=0, cmag=32, csign=0),             # DAB=y[n-D]; R1<-y[n-D]; MAC x*1.0
        enc_idle(ra=1, cmag=g, csign=0),                       # MAC g/32 * y[n-D]
        enc_idle(xfer=1),                                      # capture x + g*y @step4
        enc_memw(0x0000),                                      # DM[CPC] <- RES = y[n]
        enc_io(sel=SRC_RDRREG, wrda=True, chans="A", reset=True),
    ])


def _test_feedback_comb(D=40, g=16, n=200):
    """Exact vs the closed-form recurrence under the traced alignment. The capture (gated by
    w3.XFER, landing at step 4) reads the PP bus = ACC + PR: w0's three cs0 residues (-3),
    w1's full product, and w2's FULL product — pairC included via the combinational adder
    path (§4.2: the result reg D pins sit on PP3..18). The feedback coefficient acts at
    full stored weight: y[n] = sat16((-3 + P20(x,32,1) + P20(y',g,1) + 4) >> 3)."""
    rows = _comb_rows(D, g)
    eng = RTL22()
    out, exp, ym = [], [], {}
    for i in range(n):
        x = 16000 if i == 0 else 0
        out.append(dict(eng.run_sample(rows, x & 0xFFFF)).get("A", 0))
        yd = ym.get(i - D, 0)
        e = sat16((-3 + product20(x, 32, 1) + product20(yd, g, 1) + 4) >> 3)
        ym[i] = e
        exp.append(e)
    assert out == exp, ("comb closed-form mismatch",
                        [(i, a, b) for i, (a, b) in enumerate(zip(out, exp)) if a != b][:5])
    peaks = [(i, v) for i, v in enumerate(out) if abs(v) > 50]
    ideal = [(k * D, int(16000 * (g / 32) ** k)) for k in range(5)]
    for (pi, pv), (ei, ev) in zip(peaks, ideal):
        assert pi == ei and abs(pv - ev) <= 6, f"comb peak {(pi, pv)} vs ideal {(ei, ev)}"
    print(f"  RTL feedback comb g={g}/32     OK (closed-form EXACT; FULL g={g}/32 via PP-bus capture; "
          f"peaks {peaks[:5]})")


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
    print("### aru_freerun22_rtl self-tests (traced alignment) ###")
    _test_booth3_identity()
    _test_passthrough()
    _test_feedback_comb(D=40, g=16)
    _test_feedback_comb(D=37, g=21)     # multi-pair cmag: pairs (1,0),(1,0),(1,0) span all 3 phases
    _test_concert_extraction()
    print("ALL PASS")
