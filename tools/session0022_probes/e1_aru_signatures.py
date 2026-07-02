#!/usr/bin/env python3
"""E1c (plan 023) — the ARU §5.7 signature co-sim: per-pin verification of the whole MAC
datapath against the manufacturer's own signature tables.

★★★ RESULT (2026-07-02, session 0027): 1467/1469 listed pins MATCH at the E1b-predicted
window anchor (rot 89 = the sample after the RESET/ rise), champion variant = the
EXACTLY-TRACED wiring in the COMPLEMENT DOMAIN (PRLOAD=raw, RAIL=cs, DUAL3=0, CAPB=0).
The FEEDBACK table is 710/710 PERFECT; the 2 no-feedback exceptions are single-glyph
digitization errata, each contradicted by a same-net sister pin that matches:
  U51.12 '33FC' -> 35FC (net SR16; sister U52.12 matches 35FC's stream)
  U39.14 'F1CU' -> F1C0 (net = NAND U41 gate-1 Y; sister U41.3 matches)
What this locks at hardware pins: the Booth NAND array + front-end adder chain, the
product register, the sub-XOR row + CSIGN JK timing, the back-end adder + carry chain,
the sat-mux/clamp/SAT detect (incl. the deliberate tail saturation of diag-3 — the
no-feedback window EXCLUDES it by STOP placement), the accumulator, the result register,
the regfile + write-through, the shifter/serializer schedule, the XREG/DAB routing, the
L+1 frame, ARUCK fall-edge sampling, and THE COMPLEMENT (active-low) DAB DOMAIN in which
the traced arithmetic reproduces the E83 goldens by pure truncation (the '+4 round',
'+3 dual-rail', and '-M-1' laws all dissolve as CPU-domain bookkeeping).
Netlist corrections measured by the table (both electrically inert relabelings):
  §4.1: the '163 Q pin roles are within-nibble REVERSED (pin14=bit3..pin11=bit0);
  §4.2/§4.8: result-reg chips U43<->U44 swapped (U43 = high byte).

Setup (SM §5.7 + E1b): diag-3 free-running, XREG = 0x607F (E1a: the 0x0D10 loop writes
NOTHING; the pump is setup-only and ends at 0x607F). Analyzer CLOCK = ARUCK **falling**
edges (E1b: the unique convention hitting BOTH +5V refs — no-feedback N=62, feedback
N=90), START = RESET/ rise. Data samples = settled levels just before each ARUCK fall:
3 per step, 90 per frame. The two tables share the same underlying streams; only the
window length differs (62 vs 90) with a COMMON start anchor (global phase scanned).

Sampling semantics per step n (samples S0/S1/S2, one per AS phase):
  registers clocked at the ARUCK rise ~1 slot before the sample (PR, SR, serializer):
    POST-edge values; ACC (ARUCKE/ ~ the sample edge itself): PRE-edge values.
  fast combinational (NAND array, XOR row, U54/U2 inverters, M rails): live levels.
  slow combinational (both 74F283 ripple chains + sat-mux/PP): the value ABOUT TO BE
    registered at the enclosing edge (fig-3.4's own one-AS-behind lag guarantees the bus
    is stably-old at the edges; the sample sits inside that window).
  DAB per sub-step driver timeline (RES pre/post the 3.06 capture; MEMR DOUT lands
    late; XREG/AD constants; bus-hold on idle).

Bit-level datapath: the traced back-end (B = PR XOR rail, cin = inv(rail), 20-bit chain,
sat-mux, always-load '163) with the SUB-LSB conventions the wiring does not pin scanned
as named variants, adjudicated BY THE TABLE (e1c_backend_resolve showed no pure variant
reproduces the E83 goldens by truncation — the '+4 round' and the '-M-1' negative law
are real but untraced, siblings of the +3-dual term):
  PRLOAD in {raw, inv}   (front-end Sigma complement convention)
  RAIL   in {cs, inv_cs} (sub-ctrl level vs cs_eff)
  DUAL3  in {0, 3}       (the +3/dual-rail phase, injected in the accumulate sum)
  CAPB   in {0, 4}       (capture-side rounding bias on the result VALUE — recirculates)

Scoring: parse both ARU tables; ONE global window phase (rotation) shared by every pin
and BOTH tables; per-pin match/mismatch; per-variant totals. Success = the champion
variant names the physical sub-LSB convention and pins the datapath at hardware pins.
"""
import sys, os, json, re
from itertools import product as iproduct

TOOLS = r"d:\OneDrive\Gray Instruments\iconex\tools"
sys.path.insert(0, TOOLS)
HERE = os.path.dirname(os.path.abspath(__file__))
DOCS = os.path.join(os.path.dirname(TOOLS), "docs", "reference", "224")

import sig224
import aru_booth as B
from aru_freerun22_rtl import program_rows22, RTL22
from aru_freerun22 import SRC_NONE, SRC_RDRREG, SRC_XREG, SRC_RDAD

MASK20 = 0xFFFFF
XREG_CONST = 0x607F          # E1a: the bench XREG value (setup pump ends here; loop silent)
AD_CONST = 0x0000            # bench A/D idle (diag-3 has no WR-DA -> no conversions)

# ★ THE COMPLEMENT DOMAIN (this session, e1c_backend_resolve): the DAB physically carries
# ACTIVE-LOW values (the XREG bridge U39/U41: DATA0-7/ -> DAB with no inversion, §5.6 —
# and the SBC data bus is the complemented Multibus domain, session 0022). In this domain
# the EXACTLY-TRACED wiring (rail = inv(CSIGN/), cin = inv(rail), PR = comb_array raw,
# '163 clear to 0) reproduces ALL 20 E83 goldens by PURE TRUNCATION at the PP3..18 tap:
# the engine's '+4 round', the '+3 dual-rail correction', and the POST '-M-1 negative law'
# all dissolve as CPU-domain bookkeeping of the same physical bits.
XREG_PHYS = (~XREG_CONST) & 0xFFFF          # 0x9F80 on the DAB
AD_PHYS = (~AD_CONST) & 0xFFFF              # 0xFFFF on the DAB

# ---------------------------------------------------------------- self-tests + stimulus
print("### sig224 self-test ###")
assert sig224._selftest(), "sig224 self-test FAILED"

cache = json.load(open(os.path.join(HERE, "wcs_diag.json")))
img = bytes.fromhex(cache["sig3"]["wcs"])
assert img == open(os.path.join(TOOLS, "_diag3_wcs.bin"), "rb").read()
wcs = [(img[4*k], img[4*k+1], img[4*k+2], img[4*k+3]) for k in range(128)]
rows, L, w_reset = program_rows22(wcs)
F = L + 1
assert (w_reset, L, F) == (99, 29, 30)
print(f"\ndiag-3: L={L}, F={F} steps, XREG=0x{XREG_CONST:04X}")

_xp_path = os.path.join(HERE, "xreg_pulse.json")
if os.path.exists(_xp_path):
    xp = json.load(open(_xp_path))
    assert xp["verdicts"]["final_xreg_setup"] == hex(XREG_CONST)
    assert xp["verdicts"]["loop_writes_xreg"] is False
else:
    print("WARNING: xreg_pulse.json not yet captured — using XREG=0x607F from the "
          "static disassembly read (E1a run pending)")


def s16(v):
    v &= 0xFFFF
    return v - 0x10000 if v & 0x8000 else v


# ---------------------------------------------------------------- gate-level per-phase
def phase_detail(opnd, cmag):
    """Per AS phase of one word: (SR20 list, m0, m1, raw, dual) x3 from the verified
    gate front-end."""
    C = [(cmag >> i) & 1 for i in range(6)]
    SR = B.load_SR(s16(opnd))
    out = []
    for p, (m0, m1) in enumerate([(C[4], C[5]), (C[2], C[3]), (C[0], C[1])]):
        if p > 0:
            SR = B.shift_right2(SR)
        raw = B.comb_array(SR, m0, m1)
        out.append(dict(SR=list(SR), m0=m0, m1=m1, raw=raw, dual=(m0 and m1)))
    return out


def fe_adder_detail(SR, m0, m1):
    """Front-end NAND outputs + adder A/B nibbles + carries for one phase (traced maps)."""
    mrail = {**{c: m0 for c in B.M0_CHIPS}, **{c: m1 for c in B.M1_CHIPS}}
    Y = {(chip, gate): (0 if (SR[sr] & mrail[chip]) else 1)
         for (chip, gate), sr in B.NAND_A.items()}
    det = {"nand": Y, "A": {}, "B": {}, "cin": {}, "cout": {}}
    carry = {}
    for ad in B.CARRY_ORDER:
        a0, a1, a2, a3, b0, b1, b2, b3, cin_src = B.ADDERS[ad]
        A = Y[a0] | (Y[a1] << 1) | (Y[a2] << 2) | (Y[a3] << 3)
        Bv = Y[b0] | (Y[b1] << 1) | (Y[b2] << 2) | (Y[b3] << 3)
        cin = 1 if cin_src == '+5V' else carry[cin_src]
        s = A + Bv + cin
        carry[ad] = (s >> 4) & 1
        det["A"][ad] = A
        det["B"][ad] = Bv
        det["cin"][ad] = cin
        det["cout"][ad] = carry[ad]
    return det


# ---------------------------------------------------------------- bit-level frame walk
class Emitter:
    """Self-contained bit-level replay of the diag-3 frame at one sub-LSB convention.
    Mirrors RTL22 semantics (structure asserted against it separately) but carries the
    PHYSICAL 20-bit accumulator/PP/PR bits and the per-sample streams."""

    def __init__(self, variant):
        self.prload, self.rail_pol, self.dual3, self.capb = variant
        # Bench regfile init = the setup pump (E1a): the 0x0D1E warm-up single-steps
        # XREG values through parked words whose lane-2 pokes cycle WA 1,2,3 (F6/FA/FE),
        # twice (idempotent for R1-R3); R0 takes the FIRST strobe's value 0xAAAA via the
        # POST-leftover parked word (WA=0). R3 is overwritten every free-run step (all
        # diag-3 rows have WA=3); R0/R1/R2 are never written by the program = constant
        # operands — the E83 test patterns, stored as their PHYSICAL (complemented DAB)
        # levels: ~AAAA/~9999/~C787/~607F. 0x5555 x 47/32 x 8 = 256.7k sits 2% under the
        # +-2^18 SAT rail: designed to exercise near-max without saturating mid-window.
        self.R = [(~v) & 0xFFFF for v in (0xAAAA, 0x9999, 0xC787, 0x607F)]
        self.ACC = 0                  # physical 20-bit register bits
        self.RES = 0                  # physical 16-bit result register bits
        self.dab = 0
        self.dout_reg = 0             # DMEM DOUT register (old data until ~slot 7)
        self.DM = {}
        self.CPC = 0
        self.wp = None
        self.pipe = None              # dict for w_{n-2}: rawB, rawC, cs, dual flags
        self.pipe_prev = None
        self.ph_wp = None             # phase details of w_{n-1} (computed at step top)

    def pr_bits(self, raw):
        return (~raw) & MASK20 if self.prload else raw & MASK20

    def rail(self, cs):
        return cs if self.rail_pol == 0 else 1 - cs

    def backend(self, acc, raw, cs, dual):
        """One traced adder/sat-mux evaluation -> (PP, SAT, xorB, cin, rail, raw sum)."""
        r = self.rail(cs)
        cin = 1 - r                                       # traced: cin = inv(rail)
        xorb = self.pr_bits(raw) ^ (MASK20 if r else 0)
        ssum = acc + xorb + cin + (3 if (self.dual3 and dual) else 0)
        ssum &= MASK20
        sat = ((ssum >> 19) ^ (ssum >> 18)) & 1
        if sat:
            topb = (xorb >> 19) & 1
            pp = (topb << 19) | (topb << 18) | (0x3FFFF if not topb else 0)
        else:
            pp = ssum
        return pp, sat, xorb, cin, r, ssum

    def step(self, d, emit=None):
        """One WCS row; emit(sample_dict) called 3x if given."""
        wp = self.wp
        # operand + phases of w_{n-1} (write-through: post previous step's MS7 write)
        if wp is not None:
            opnd = self.R[wp["RA"]]
            ph = phase_detail(opnd, wp["cmag"])
        else:
            opnd, ph = 0, phase_detail(0, 0)
        p2 = self.pipe or dict(rawB=phase_detail(0, 0)[1], rawC=phase_detail(0, 0)[2],
                               cs=1)
        cs2 = p2["cs"]

        acc_endprev = self.ACC
        res_pre = self.RES

        # --- edge 1.x: ACC <- sum0 = acc + ppB(w_{n-2}) [own sign]
        sum0, sat0, xb0, cin0, r0, ss0 = self.backend(acc_endprev, p2["rawB"]["raw"],
                                                      cs2, p2["rawB"]["dual"])
        acc_after1 = sum0

        # --- capture 3.06: PP bus = acc_after1 + ppC(w_{n-2}) [own sign]
        sum1, sat1, xb1, cin1, r1, ss1 = self.backend(acc_after1, p2["rawC"]["raw"],
                                                      cs2, p2["rawC"]["dual"])
        if wp is not None and wp["XFER"]:
            v = ((sum1 + self.capb) & MASK20) if not sat1 else sum1
            self.RES = (v >> 3) & 0xFFFF
        res_post = self.RES

        # --- edge 4.x: ZERO clear (owner wp) or register sum1
        if wp is not None and wp["ZERO"]:
            acc_after4 = 0
        else:
            acc_after4 = sum1

        # --- edge 7.x preview: sum2 = acc_after4 + ppA(w_{n-1}) [own sign]
        csn = wp["cs"] if wp is not None else 1
        sum2, sat2, xb2, cin2, r2, ss2 = self.backend(acc_after4, ph[0]["raw"],
                                                      csn, ph[0]["dual"])

        # --- DAB timeline (per-sample) + engine-consistent single value
        typ = d["typ"]
        addr = (self.CPC - d["ofst"]) & 0xFFFF
        dab_hold = self.dab
        if typ == 0:                                     # MEMR
            new_dout = self.DM.get(addr, 0) & 0xFFFF
            dab_t = [self.dout_reg, self.dout_reg, new_dout]
            self.dout_reg = new_dout
            dab_end = new_dout
        elif typ == 1:                                   # MEMW: RES drives (RDRREG)
            dab_t = [res_pre, res_post, res_post]
            dab_end = res_post
            self.DM[addr] = dab_end
        elif typ == 2:
            sel = d["sel"]
            if sel == SRC_RDRREG:
                dab_t = [res_pre, res_post, res_post]
                dab_end = res_post
            elif sel == SRC_XREG:
                dab_t = [XREG_PHYS] * 3
                dab_end = XREG_PHYS
            elif sel == SRC_RDAD:
                dab_t = [AD_PHYS] * 3
                dab_end = AD_PHYS
            else:
                dab_t = [dab_hold] * 3
                dab_end = dab_hold
        else:                                            # idle: bus hold
            dab_t = [dab_hold] * 3
            dab_end = dab_hold
        self.dab = dab_end

        # --- emit the three samples ---
        if emit is not None:
            # JK level: [3.0(n),3.0(n+1)) holds MI23(w_{n-1}); before slot3 of step n:
            # MI23(w_{n-2}).  Physical line CSIGN/ = MI23 = 1 - stored_b7 = 1 - cs.
            jk = [1 - cs2, 1 - csn, 1 - csn]
            # Field family (stage-1/offset-latch outputs: RA/WA lines + regfile read
            # address): changes BETWEEN S0 and S1 (~slot 2-3) — pin-scan measured
            # (U54 address lines match at rot-1 vs the JK/serializer streams).
            fld = [wp if wp is not None else d, d, d]
            # F-net (regfile Q at the LIVE read address, PRE-MS7-write — the write
            # lands after the S2 sample): S0 = R[RA(w_{n-1})] = opnd(wp) just loaded.
            f_t = [opnd & 0xFFFF, self.R[d["RA"]] & 0xFFFF, self.R[d["RA"]] & 0xFFFF]
            # PR contents + the phase args of the JUST-LATCHED computation per sample
            pr_t = [(p2["rawC"], cs2), (ph[0], csn), (ph[1], csn)]
            sr_t = [ph[0]["SR"], ph[1]["SR"], ph[2]["SR"]]
            pair_t = [(ph[0]["m0"], ph[0]["m1"]), (ph[1]["m0"], ph[1]["m1"]),
                      (ph[2]["m0"], ph[2]["m1"])]
            slow = [(sum0, sat0, xb0, cin0, r0, ss0), (sum1, sat1, xb1, cin1, r1, ss1),
                    (sum2, sat2, xb2, cin2, r2, ss2)]
            acc_t = [acc_endprev, acc_after1, acc_after4]
            for k in range(3):
                ppv, satv, xbv, cinv, railv, sumv = slow[k]
                ph_lat, cs_lat = pr_t[k]
                # The analyzer samples LATE in the ARUCK cycle: both ripple chains have
                # SETTLED to the CURRENT computation by the sample (the registers still
                # captured the OLD sums at their earlier edges — fig-3.4 unchanged).
                # Front-end: NAND / adder A/B / Σ / couts all show the LIVE phase.
                fed = fe_adder_detail(ph[k]["SR"], ph[k]["m0"], ph[k]["m1"])
                # PR register (Q pins + XOR-row A pins) = the LATCHED phase; the D pins
                # (= FE Σ nets) show the live computation (emitted as PRD).
                rail_live = self.rail(cs_lat)
                xbl = self.pr_bits(ph_lat["raw"]) ^ (MASK20 if rail_live else 0)
                emit(dict(
                    k=k, d=d, wp=wp,
                    PR=self.pr_bits(ph_lat["raw"]),          # PRQ class (latched)
                    PRD=self.pr_bits(ph[k]["raw"]),          # live FE Σ / D nets
                    FE=fed,                                  # live front-end detail
                    SR=sr_t[k], M0=pair_t[k][0], M1=pair_t[k][1],
                    ACC=acc_t[k], PP=ppv, SUM=sumv, SAT=satv, XORB=xbv, CIN=cinv,
                    RAIL=railv, XBL=xbl,
                    CSIGNn=jk[k],
                    DAB=dab_t[k],
                    Fnet=f_t[k],
                    ZEROn=(0 if (k == 0 and wp is not None and wp["ZERO"]) else 1),
                    XFERCK=(0 if (k == 0 and wp is not None and wp["XFER"]) else 1),
                    WSTBn=1,   # write pulse (slot 7) precedes the late S2 sample
                    S0=1, S1=(1 if k == 2 else 0),
                    RDRREGn=(0 if (typ == 1 or (typ == 2 and d.get("sel") == SRC_RDRREG))
                             else 1),
                    RA=fld[k]["RA"], WA=fld[k]["WA"], w=d,
                ))

        # --- edge 7.x + MS7: register sum2; regfile write ---
        self.ACC = sum2
        self.R[d["WA"]] = dab_end & 0xFFFF
        # pipeline: w_{n-1}'s pairB/pairC retire next step
        if wp is not None:
            self.pipe = dict(rawB=ph[1], rawC=ph[2], cs=wp["cs"])
        self.wp = d

    def run_frame(self, emit=None):
        for d in rows:
            self.step(d, emit=emit)
        self.CPC = (self.CPC + 1) & 0xFFFF


def steady_frame(variant, max_iters=400):
    """Iterate frames to the frame-periodic fixed point; return the emitted samples of
    one steady frame (list of 90 dicts) + convergence info."""
    em = Emitter(variant)
    sig_prev = None
    for it in range(max_iters):
        em.run_frame()
        key = (em.ACC, em.RES, tuple(em.R), em.dab, em.dout_reg,
               tuple(sorted(em.DM.items())[-8:]))
        # cheap state hash: DM grows per frame (fresh addresses), so compare the
        # VALUES the frame produced instead: harvest via a probe frame every 16
        if it % 16 == 15:
            probe = []
            em2 = _clone(em)
            em2.run_frame(emit=probe.append)
            sig = tuple((p["ACC"], p["PP"], p["DAB"], p["PR"]) for p in probe)
            if sig == sig_prev:
                samples = []
                em.run_frame(emit=samples.append)
                return samples, it + 2
            sig_prev = sig
    raise RuntimeError(f"no frame-periodic fixed point in {max_iters} frames "
                       f"(variant {variant})")


def _clone(em):
    import copy
    c = Emitter((em.prload, em.rail_pol, em.dual3, em.capb))
    c.R = list(em.R)
    c.ACC = em.ACC
    c.RES = em.RES
    c.dab = em.dab
    c.dout_reg = em.dout_reg
    c.DM = dict(em.DM)
    c.CPC = em.CPC
    c.wp = em.wp
    c.pipe = dict(em.pipe) if em.pipe else None
    return c


# ---------------------------------------------------------------- stream extraction
def bit(v, b):
    return (v >> b) & 1


def build_streams(samples):
    """dict stream-name -> list of 90 bits. Weight-indexed buses.

    Sample-timing classes (pin-scan measured, this session): registers show their
    POST-edge (current) contents; combinational chains show the SETTLED CURRENT
    computation. The slow-sum quantities (PP/AC-register/BE carries/SAT) as emitted
    are 'about to register at the enclosing edge' = one sample EARLIER than the
    settled state the analyzer sees -> shift those streams left by one sample
    (frame-periodic steady state makes this exact)."""
    S = {}
    n = len(samples)
    def put(name, fn):
        S[name] = [fn(p) & 1 for p in samples]
    def put_shift(name, fn):
        S[name] = [fn(samples[(i + 1) % n]) & 1 for i in range(n)]
    for b_ in range(20):
        put(f"PRQ{b_}", lambda p, b=b_: bit(p["PR"], b))       # latched register (Q, XOR-A)
        put(f"PRD{b_}", lambda p, b=b_: bit(p["PRD"], b))      # live FE Σ (D pins)
        put_shift(f"AC{b_}", lambda p, b=b_: bit(p["ACC"], b))
        put_shift(f"PP{b_}", lambda p, b=b_: bit(p["PP"], b))
        put_shift(f"SUM{b_}", lambda p, b=b_: bit(p["SUM"], b))   # pre-mux adder sum
        put(f"XB{b_}", lambda p, b=b_: bit(p["XBL"], b))       # LIVE xor-row net level
        put(f"SR{b_}", lambda p, b=b_: p["SR"][b])
    for b_ in range(16):
        put(f"DAB{b_}", lambda p, b=b_: bit(p["DAB"], b))
        put(f"F{b_}", lambda p, b=b_: bit(p["Fnet"], b))
    # front-end nets
    for (chip, gate) in B.NAND_A:
        put(f"NAND_{chip}_{gate}", lambda p, cg=(chip, gate): p["FE"]["nand"][cg])
    for ad in B.CARRY_ORDER:
        for i in range(4):
            put(f"FEA_{ad}_A{i}", lambda p, a=ad, j=i: bit(p["FE"]["A"][a], j))
            put(f"FEA_{ad}_B{i}", lambda p, a=ad, j=i: bit(p["FE"]["B"][a], j))
        put(f"FEC_{ad}_cin", lambda p, a=ad: p["FE"]["cin"][a])
        put(f"FEC_{ad}_cout", lambda p, a=ad: p["FE"]["cout"][a])
    # back-end carries: nibble-wise from the slow sum components, shifted like PP
    def be_carry(p, k):
        s = (p["ACC"] & ((1 << (4 * k)) - 1)) + (p["XORB"] & ((1 << (4 * k)) - 1)) + p["CIN"]
        return (s >> (4 * k)) & 1
    for k_ in range(1, 5):
        put_shift(f"BEC{k_}", lambda p, k=k_: be_carry(p, k))
    put("CINBE", lambda p: p["CSIGNn"])                  # live: cin = inv(rail) = CSIGN/
    put("RAILA", lambda p: 1 - p["CSIGNn"])              # live: rail = inv(CSIGN/)
    put("RAILB", lambda p: 1 - p["CSIGNn"])
    put("CSIGNn", lambda p: p["CSIGNn"])
    put_shift("SAT", lambda p: p["SAT"])
    put("TOPB", lambda p: bit(p["XBL"], 19))             # live xor bit 19
    put("BINV", lambda p: 1 - bit(p["XBL"], 19))
    put("M0", lambda p: p["M0"])
    put("M1", lambda p: p["M1"])
    put("M0n", lambda p: 1 - p["M0"])
    put("M1n", lambda p: 1 - p["M1"])
    put("ZEROn", lambda p: p["ZEROn"])
    put("XFERCK", lambda p: p["XFERCK"])
    put("WSTBn", lambda p: p["WSTBn"])
    put("S0", lambda p: p["S0"])
    put("S1", lambda p: p["S1"])
    put("RDRREGn", lambda p: p["RDRREGn"])
    # T&C-sourced address lines (MI level = 1 - stored bit; U54 outputs = stored)
    put("RA0_MI", lambda p: 1 - (p["RA"] & 1))
    put("RA1_MI", lambda p: 1 - ((p["RA"] >> 1) & 1))
    put("WA0_MI", lambda p: 1 - (p["WA"] & 1))
    put("WA1_MI", lambda p: 1 - ((p["WA"] >> 1) & 1))
    put("RA0_ST", lambda p: p["RA"] & 1)
    put("RA1_ST", lambda p: (p["RA"] >> 1) & 1)
    put("WA0_ST", lambda p: p["WA"] & 1)
    put("WA1_ST", lambda p: (p["WA"] >> 1) & 1)
    S["C0"] = [0] * len(samples)
    S["C1"] = [1] * len(samples)
    return S


# ---------------------------------------------------------------- the pin map
def build_pinmap():
    """(chip, pin) -> stream name. Netlist §4.1-4.9 + §4F.1-4F.8, weight-resolved."""
    PM = {}
    def put(u, p, s):
        PM[(u, p)] = s

    # --- U2 74S04 (sub-ctrl / cin / clamp inverters, §4.5/§4F.8)
    for p, s in ((5, "RAILA"), (6, "CINBE"), (8, "BINV"), (9, "TOPB"),
                 (10, "RAILA"), (11, "CSIGNn"), (12, "RAILB"), (13, "CSIGNn"),
                 (7, "C0"), (14, "C1")):
        put("U2", p, s)

    # --- shifters U3,U4,U15-U18 (74LS194, §4F.3)
    shift = {
        "U3": dict(A="C0", B="C0", C=None, D=None, SER="SR4", QA="SR2", QB="SR0", QC=None, QD=None),
        "U4": dict(A="F0", B="C0", C=None, D=None, SER="SR5", QA="SR3", QB="SR1", QC=None, QD=None),
        "U15": dict(A="F15", B="F14", C="F12", D="F10", SER="SR19", QA="SR19", QB="SR17", QC="SR15", QD="SR13"),
        "U16": dict(A="F15", B="F13", C="F11", D="F9", SER="SR18", QA="SR18", QB="SR16", QC="SR14", QD="SR12"),
        "U17": dict(A="F7", B="F5", C="F3", D="F1", SER="SR12", QA="SR10", QB="SR8", QC="SR6", QD="SR4"),
        "U18": dict(A="F8", B="F6", C="F4", D="F2", SER="SR13", QA="SR11", QB="SR9", QC="SR7", QD="SR5"),
    }
    pinof = dict(A=3, B=4, C=5, D=6, SER=2, QA=15, QB=14, QC=13, QD=12)
    for u, m in shift.items():
        for role, s in m.items():
            if s is not None:
                put(u, pinof[role], s)
        put(u, 1, "C1")            # CLR\ = +5
        put(u, 9, "S0")
        put(u, 10, "S1")
        put(u, 11, "C0")           # ARUCK sampled at own fall
        put(u, 16, "C1")
        put(u, 8, "C0")

    # --- XOR row U5-U9 (§4.6; weights resolved from the PR-source pins)
    # per chip: (pin12,pin11)=w(base+3)? NO: rows give (A,Y) pin pairs with weights:
    xor_rows = {  # chip: [(Apin, Ypin, weight), ...]
        "U5": [(12, 11, 3), (9, 8, 2), (4, 6, 1), (1, 3, 0)],
        "U6": [(12, 11, 7), (9, 8, 6), (4, 6, 5), (1, 3, 4)],
        "U7": [(12, 11, 11), (9, 8, 10), (4, 6, 9), (1, 3, 8)],
        "U8": [(12, 11, 15), (9, 8, 14), (4, 6, 13), (1, 3, 12)],
        "U9": [(12, 11, 19), (9, 8, 18), (4, 6, 17), (1, 3, 16)],
    }
    for u, rws in xor_rows.items():
        rail = "RAILA" if u in ("U5", "U6") else "RAILB"
        for apin, ypin, w in rws:
            put(u, apin, f"PRQ{w}")
            put(u, ypin, f"XB{w}")
        for bp in (2, 5, 10, 13):
            put(u, bp, rail)
        put(u, 7, "C0")
        put(u, 14, "C1")

    # --- product register U10/U11 (74F374) + U12 (74S175), §4.7 weight-resolved
    # D/Q pin pairs for F374: (D,Q) = (3,2),(4,5),(7,6),(8,9),(13,12),(14,15),(17,16),(18,19)
    pr374 = {"U10": [19, 18, 17, 16, 15, 14, 13, 12],   # D0..D7 weights
             "U11": [11, 10, 9, 8, 7, 6, 5, 4]}
    dq = [(3, 2), (4, 5), (7, 6), (8, 9), (13, 12), (14, 15), (17, 16), (18, 19)]
    for u, ws in pr374.items():
        for (dp, qp), w in zip(dq, ws):
            put(u, dp, f"PRD{w}")  # D = front-end Sigma net = LIVE computation
            put(u, qp, f"PRQ{w}")  # Q = the latched register
        put(u, 11, "C0")           # ARUCK
        put(u, 1, "C0")            # OE\ = GND
        put(u, 10, "C0")
        put(u, 20, "C1")
    # U12 74S175: D0..D3 = w3,w2,w1,w0; pins D:(4,5,12,13) Q:(2,7,10,15)
    for (dp, qp), w in zip([(4, 2), (5, 7), (12, 10), (13, 15)], [3, 2, 1, 0]):
        put("U12", dp, f"PRD{w}")
        put("U12", qp, f"PRQ{w}")
    put("U12", 9, "C0")            # CP = ARUCK
    put("U12", 1, "C1")            # CLR\ = +5
    put("U12", 8, "C0")
    put("U12", 16, "C1")

    # --- front-end adders U13,U24,U25,U38,U39 (§4F.7; A/B from NANDs, Sigma -> PR)
    fe_pins = dict(A=(5, 3, 14, 12), B=(6, 2, 15, 11), CIN=7, COUT=9, S=(4, 1, 13, 10))
    for ad in B.CARRY_ORDER:
        base = B._NIB[ad]
        for i in range(4):
            put(ad, fe_pins["A"][i], f"FEA_{ad}_A{i}")
            put(ad, fe_pins["B"][i], f"FEA_{ad}_B{i}")
            put(ad, fe_pins["S"][i], f"PRD{base + i}")
        put(ad, fe_pins["CIN"], "C1" if ad == "U13" else f"FEC_{B.CARRY_ORDER[B.CARRY_ORDER.index(ad)-1]}_cout")
        put(ad, fe_pins["COUT"], f"FEC_{ad}_cout")
        put(ad, 8, "C0")
        put(ad, 16, "C1")

    # --- Booth NAND array U14,U26-28,U40,41,50-53 (§4F.4/§4F.5)
    gate_pins = {1: (1, 2, 3), 2: (4, 5, 6), 3: (9, 10, 8), 4: (12, 13, 11)}
    for (chip, gate), srv in B.NAND_A.items():
        ap, bp, yp = gate_pins[gate]
        put(chip, ap, f"SR{srv}")
        put(chip, bp, "M0" if chip in B.M0_CHIPS else "M1")
        put(chip, yp, f"NAND_{chip}_{gate}")
    for chip in list(B.M0_CHIPS | B.M1_CHIPS):
        put(chip, 7, "C0")
        put(chip, 14, "C1")

    # --- back-end adders U19-U23 (§4.1/§4.3/§4.6): A=AC, B=XB, Sigma=PP-pre-mux (= PP
    #     when SAT=0; diag-3 never saturates — asserted), carries
    be_pins = dict(A=(5, 3, 14, 12), B=(6, 2, 15, 11), S=(4, 1, 13, 10), CIN=7, COUT=9)
    for k, u in enumerate(("U19", "U20", "U21", "U22", "U23")):
        for i in range(4):
            w = 4 * k + i
            put(u, be_pins["A"][i], f"AC{w}")
            put(u, be_pins["B"][i], f"XB{w}")
            put(u, be_pins["S"][i], f"SUM{w}")
        put(u, be_pins["CIN"], "CINBE" if k == 0 else f"BEC{k}")
        put(u, be_pins["COUT"], f"BEC{k+1}" if k < 4 else None)
        if k == 4:
            PM.pop(("U23", 9), None)                     # top carry n/c
        put(u, 8, "C0")
        put(u, 16, "C1")

    # --- sat-muxes U33-U37 (§4.4): I0=Sigma(=PP), I1=B-IN/topB, Y=PP, SEL=SAT
    for k, u in enumerate(("U33", "U34", "U35", "U36", "U37")):
        # I0 pins tap the PRE-mux sum nets (§4.3: p2=s0, p5=s1, p11=s2, p14=s3)
        put(u, 2, f"SUM{4*k+0}")
        put(u, 5, f"SUM{4*k+1}")
        put(u, 11, f"SUM{4*k+2}")
        put(u, 14, f"SUM{4*k+3}")
        put(u, 4, f"PP{4*k+0}")    # Y1
        put(u, 7, f"PP{4*k+1}")    # Y2
        put(u, 9, f"PP{4*k+2}")    # Y4
        put(u, 12, f"PP{4*k+3}")   # Y3
        for i1p in (3, 6, 10, 13):
            put(u, i1p, "BINV")
        put(u, 1, "SAT")
        put(u, 15, "C0")           # G\ = GND
        put(u, 8, "C0")
        put(u, 16, "C1")
    put("U37", 10, "TOPB")         # clamp exception (§4.4)
    put("U37", 13, "TOPB")

    # --- U42 74S86 saturation detect (§4.5) + spares
    put("U42", 1, "SUM19")         # _aru_sum19 (pre-mux)
    put("U42", 2, "SUM18")
    put("U42", 3, "SAT")
    put("U42", 9, "C1")            # spare inputs tied high (table: 29F3)
    put("U42", 10, "C1")
    put("U42", 7, "C0")
    put("U42", 14, "C1")
    put("U42", 8, "C0")            # spare gate output (table 0000)

    # --- result register U43/U44 (§4.2/§4.8): D = PP3..18, Q = DAB
    # chips SWAPPED vs the §4.2 transcription (table-measured: U43 = high byte)
    res_d = {("U44", 14): 3, ("U44", 13): 4, ("U44", 18): 5, ("U44", 17): 6,
             ("U44", 4): 7, ("U44", 3): 8, ("U44", 8): 9, ("U44", 7): 10,
             ("U43", 14): 11, ("U43", 13): 12, ("U43", 18): 13, ("U43", 17): 14,
             ("U43", 4): 15, ("U43", 3): 16, ("U43", 8): 17, ("U43", 7): 18}
    for (u, p), w in res_d.items():
        put(u, p, f"PP{w}")
    res_q = {("U44", 15): 0, ("U44", 12): 1, ("U44", 19): 2, ("U44", 16): 3,
             ("U44", 5): 4, ("U44", 2): 5, ("U44", 9): 6, ("U44", 6): 7,
             ("U43", 15): 8, ("U43", 12): 9, ("U43", 19): 10, ("U43", 16): 11,
             ("U43", 5): 12, ("U43", 2): 13, ("U43", 9): 14, ("U43", 6): 15}
    for (u, p), db in res_q.items():
        put(u, p, f"DAB{db}")
    for u in ("U43", "U44"):
        put(u, 1, "RDRREGn")
        put(u, 11, "XFERCK")
        put(u, 10, "C0")
        put(u, 20, "C1")

    # --- accumulator U45-U49 (§4.2/§4.1/§4.9)
    for k, u in enumerate(("U45", "U46", "U47", "U48", "U49")):
        put(u, 6, f"PP{4*k+0}")    # D
        put(u, 5, f"PP{4*k+1}")    # C
        put(u, 4, f"PP{4*k+2}")    # B
        put(u, 3, f"PP{4*k+3}")    # A
        # Q pin roles within-nibble REVERSED vs the §4.1 transcription (table-
        # measured: pin14 = bit3 .. pin11 = bit0; the adder-A pin roles reverse
        # identically, so §4.1's net PAIRING & the arithmetic stand — only the
        # pin<->bit map flips)
        put(u, 14, f"AC{4*k+3}")
        put(u, 13, f"AC{4*k+2}")
        put(u, 12, f"AC{4*k+1}")
        put(u, 11, f"AC{4*k+0}")
        put(u, 1, "ZEROn")
        put(u, 2, "C0")            # ARUCKE/ sampled 0 (pre-rise at the fall sample)
        put(u, 7, "C0")
        put(u, 9, "C0")
        put(u, 10, "C0")
        put(u, 8, "C0")
        put(u, 16, "C1")

    # --- register file U29-U32 (§4F.1)
    rf = {"U29": (15, 14, 13, 12), "U30": (11, 10, 9, 8),
          "U31": (7, 6, 5, 4), "U32": (3, 2, 1, 0)}      # D1..D4 = DAB hi..lo per chip
    for u, (b1, b2, b3, b4) in rf.items():
        put(u, 15, f"DAB{b1}")     # D1
        put(u, 1, f"DAB{b2}")      # D2
        put(u, 2, f"DAB{b3}")      # D3
        put(u, 3, f"DAB{b4}")      # D4
        put(u, 10, f"F{b1}")       # Q1
        put(u, 9, f"F{b2}")        # Q2
        put(u, 7, f"F{b3}")        # Q3
        put(u, 6, f"F{b4}")        # Q4
        put(u, 5, "RA1_ST")        # RA = RA1_inv (U54 out = stored level)
        put(u, 4, "RA0_ST")        # RB = RA0_inv
        put(u, 14, "WA1_ST")       # WA = WA1_inv
        put(u, 13, "WA0_ST")       # WB = WA0_inv
        put(u, 12, "WSTBn")        # GW\ = DAB WSTB/
        put(u, 11, "C0")           # GR\ = GND
        put(u, 8, "C0")
        put(u, 16, "C1")

    # --- U54 74S04 (address buffers + Booth-select inverters, §4F.6)
    for p, s in ((1, "RA0_MI"), (2, "RA0_ST"), (3, "WA0_MI"), (4, "WA0_ST"),
                 (5, "RA1_MI"), (6, "RA1_ST"), (9, "WA1_MI"), (8, "WA1_ST"),
                 (11, "M1n"), (10, "M1"), (13, "M0n"), (12, "M0"),
                 (7, "C0"), (14, "C1")):
        put("U54", p, s)

    return PM


# ---------------------------------------------------------------- table parsing
def parse_table(txt, header):
    m = re.search(re.escape(header) + r".*?```(.*?)```", txt, re.S)
    assert m, f"table {header!r} not found"
    table = {}
    sides = [None, None]
    for line in m.group(1).splitlines():
        for side, seg in enumerate((line[:31], line[31:])):
            toks = seg.split()
            i = 0
            while i < len(toks):
                t = toks[i]
                if re.fullmatch(r"U\d+", t):
                    sides[side] = t
                    i += 1
                else:
                    pin, sg = toks[i], toks[i + 1]
                    if sg != "-" and sides[side]:
                        table[(sides[side], int(pin))] = sg
                    i += 2
    return table


# ---------------------------------------------------------------- scoring
def score_variant(variant, tables, PM, verbose=False):
    samples, iters = steady_frame(variant)
    # diag-3 DOES saturate at the frame tail (cmag-47 rows; the feedback table's
    # U42.3 = 000P shows SAT firing inside the 90-window, while the no-feedback
    # 62-window ends at step 20 and excludes those samples — by design).
    S = build_streams(samples)
    n = len(samples)

    def sig_of(strm, rot, wlen):
        seq = strm[rot:] + strm[:rot]
        return sig224.value_to_display(sig224.sig_value(seq[:wlen]))

    best = None
    for rot in range(n):
        tot = 0
        for tname, (table, wlen) in tables.items():
            for key, want in table.items():
                s = PM.get(key)
                if s is None or S.get(s) is None:
                    continue
                if sig_of(S[s], rot, wlen) == want:
                    tot += 1
        if best is None or tot > best[1]:
            best = (rot, tot)
    rot, tot = best
    detail = {}
    for tname, (table, wlen) in tables.items():
        match, mismatch, notmod = [], [], []
        for key in sorted(table, key=lambda x: (int(x[0][1:]), x[1])):
            want = table[key]
            s = PM.get(key)
            if s is None or S.get(s) is None:
                notmod.append(key)
                continue
            got = sig_of(S[s], rot, wlen)
            (match if got == want else mismatch).append((key, want, got, s))
        detail[tname] = dict(match=match, mismatch=mismatch, notmod=notmod)
    return rot, tot, detail, iters


def main():
    txt = open(os.path.join(DOCS, "224-signature-value-tables.md"), encoding="utf-8").read()
    t_nfb = parse_table(txt, "#### ARU Module — Version 8.2.1 — no feedback")
    t_fb = parse_table(txt, "#### ARU Module — Version 8.2.1 (feedback configuration)")
    print(f"parsed: no-feedback {len(t_nfb)} pins, feedback {len(t_fb)} pins")
    tables = {"no-feedback(62)": (t_nfb, 62), "feedback(90)": (t_fb, 90)}

    PM = build_pinmap()
    listed = set(t_nfb) | set(t_fb)
    mapped = sum(1 for k in listed if k in PM)
    print(f"pin map: {len(PM)} pins built; {mapped}/{len(listed)} listed pins mapped")

    variants = list(iproduct((0, 1), (0, 1), (0, 3), (0, 4)))
    results = []
    for v in variants:
        try:
            rot, tot, detail, iters = score_variant(v, tables, PM)
        except RuntimeError as e:
            print(f"  variant {v}: {e}")
            continue
        nlisted = sum(len(d["match"]) + len(d["mismatch"]) for d in detail.values())
        results.append((tot, v, rot, detail))
        print(f"  variant PRLOAD={'inv' if v[0] else 'raw'} RAIL={'inv_cs' if v[1] else 'cs'} "
              f"DUAL3={v[2]} CAPB={v[3]}: {tot}/{nlisted} @rot={rot} (steady in {iters} frames)")

    results.sort(key=lambda r: -r[0])
    tot, v, rot, detail = results[0]
    print(f"\n### CHAMPION: PRLOAD={'inv' if v[0] else 'raw'} RAIL={'inv_cs' if v[1] else 'cs'} "
          f"DUAL3={v[2]} CAPB={v[3]} @rot {rot} ###")
    for tname, d in detail.items():
        nm = len(d["match"]); nx = len(d["mismatch"]); nn = len(d["notmod"])
        print(f"\n[{tname}] MATCH {nm}  MISMATCH {nx}  not-modeled {nn}")
        if d["mismatch"]:
            print("  mismatches (pin: table vs model [stream]):")
            for (u, p), want, got, s in d["mismatch"]:
                print(f"    {u}.{p}: {want} vs {got}  [{s}]")
        if d["notmod"]:
            print(f"  not modeled: {['%s.%d' % k for k in d['notmod']]}")

    json.dump(dict(champion=dict(variant=v, rot=rot, total=tot),
                   results=[(t, list(vv), r) for t, vv, r, _ in results]),
              open(os.path.join(HERE, "e1c_scores.json"), "w"), indent=1)
    print("\nscores -> e1c_scores.json")


if __name__ == "__main__":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass
    main()
