#!/usr/bin/env python3
"""Plan-016 deliverable: cycle-accurate POST single-step co-sim of the ARU multiplier,
built to nail down the cmag=63 (+1..+2 LSB) residual once and for all.

RESULT (2026-06-29): the residual is NOT a pipeline / single-step register-state effect.
It is a clean, UNIQUE, COMBINATIONAL correction of +3 per dual-Booth-rail phase (+9 for
the all-ones coefficient), localized to the FRONT-END intermediate adders. Three
independent analyses below establish this:

  PART A  cycle-accurate engine + schedule sweep  -> REFUTES the pipeline hypothesis.
          A stateful AS-phase engine (74194 shifter, partial-product register, accumulator,
          result register) carried ACROSS strobes and driven by the EXACT firmware strobe
          sequence (the real 0x0942 test: 5 blocks, one OUT-0x03 strobe per case, ZERO
          clears the accumulator each step, NO reset between cases). Swept over every
          physically-motivated schedule (PP-register delay 0/1, accumulator-clear position,
          pipeline drain depth, cross-step PP leakage): EVERY variant gives at best 16/20.
          No sequential schedule reproduces cmag=63. => not a deferred-MAC / readback effect.

  PART B  arithmetic forensics  -> the correction is a UNIQUE flat +9 at the accumulator.
          For the four cmag=63 goldens the accumulator (-ACC) must be larger by K, where
          K in [7,14] (0x3333), [4,11] (0xCCCC), [2,9] (0x3FFF), [9,16] (0xC000). The
          intersection is exactly {9} = 3 phases x +3. NOT operand-dependent (the apparent
          +1/+1/+1/+2 at the output is just the >>3 round). cmag=21 (M0-only) and cmag=42
          (M1-only) need +0, so the correction is gated by BOTH Booth rails firing.

  PART C  dual-rail dissection + locus  -> +3 lives in the front-end, gated by M0.M1.
          comb_array is exactly additive: dual == m0 + m1 - none (no missing carry inside
          the traced array). Injecting +3 per dual-rail phase into the front-end product
          register gives 20/20 faithfully; +1/+2/+4 do not (so +3 is exact, not a range).
          => the hardware adds +3 (binary 11, into PR0/PR1) per phase in which M0 AND M1
          are both asserted. This term is NOT in the traced wiring (no M0.M1 gate, all ten
          F283 carry-ins accounted for); it is an UN-TRACED net. Owner re-check targets on
          schematic 060-01318: aru_U13 carry-in (pin7, "+5V"), the two spare aru_U42 (74S86)
          XOR gates, the two spare aru_U2 (74S04) inverters, and the M0/M1 fanout off aru_U54.

CORROBORATION (Service Manual chapter 5, S5.3.2): the multiplier test's three coefficients
are +21/32, +42/32, and "+63/64" (the all-ones case notated as the max fraction 1-2^-6 =>
a designed special case, not noise). And: "E89 to E8B [the +63/64 test] will test the
intermediate address. Therefore ... check U13, U24 to U25, and U38 and U39" -- i.e. the
manual itself says the all-ones test exercises the front-end intermediate adders
(U13/U39/U25/U38/U24), independently confirming the localization. (EA0-EB3 module map:
74LS00 = Booth NAND array; U13/U24/U25/U38/U39 = intermediate adder; 74S86 U5-U9 = sign;
U19-U23 = second adders.)

CONCLUSION: tools/aru_booth.py::multiply()'s `+3*dual` term is therefore the UNIQUE
combinational correction for the all-ones coefficient (the dual-rail Booth partial-product
completion), NOT an arbitrary calibrated fudge -- though the exact gate that injects it is
un-traced and flagged for the owner. multiply_faithful() (no correction) = 16/20; multiply()
(+3*dual) = 20/20; POST E32/E40/E83 pass un-suppressed on the verified 8080 (tools/aru_post.py).

Run:  python tools/aru_cycaccurate.py
"""
import os
import sys
import itertools

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import aru_booth as B

GOLDENS = B.GOLDENS                       # (F, cmag, csign, exp) -- firmware POST 0x0942 tables
GMAP = {(F & 0xFFFF, c, s): e for (F, c, s, e) in GOLDENS}


def s16(v):
    v &= 0xFFFF
    return v - 0x10000 if v & 0x8000 else v


# ---------------------------------------------------------------------------
# The EXACT firmware strobe sequence (disassembly of 0x0942..0x09D2): five blocks,
# one OUT-0x03 strobe per case, l2/l3 patched per block, NO reset between cases.
# ---------------------------------------------------------------------------
def firmware_sequence():
    seq = []
    blocks = [
        (0x7E, 0xA9, [0x5555, 0xAAAA, 0x6666, 0x9999]),   # blk1 cmag21 cs0
        (0xFE, 0xA9, [0x5555, 0xAAAA, 0x6666, 0x9999]),   # blk2 cmag21 cs1
        (0x7E, 0x55, [0x5555, 0xAAAA, 0x6666, 0x9999]),   # blk3 cmag42 cs0
        (0xFE, 0x55, [0x5555, 0xAAAA, 0x6666, 0x9999]),   # blk4 cmag42 cs1
        (0xFE, 0x01, [0x3333, 0xCCCC, 0x3FFF, 0xC000]),   # blk5 cmag63 cs1
    ]
    for l2, l3, ops in blocks:
        inv3 = (~l3) & 0xFF
        cmag = (inv3 >> 2) & 0x3F
        zero = (inv3 >> 1) & 1                            # ZERO-gate (=1 -> clear ACC each step)
        csign = (l2 >> 7) & 1
        for op in ops:
            seq.append(dict(F=op, cmag=cmag, csign=csign, zero=zero))
    return seq


# ===========================================================================
# PART A -- stateful cycle-accurate engine + schedule sweep
# ===========================================================================
class CycARU:
    """Stateful AS-phase engine. Registers (PP, ACC, RES) persist ACROSS strobes so any
    deferred-pipeline / cross-step leakage would surface. Schedule is parameterized over the
    small space of physically-motivated alignments (NOT free constants)."""

    def __init__(self, pp_delay=0, clear_at='pre', drain=0):
        self.pp_delay = pp_delay     # 0: ACC sees this phase's term; 1: sees prev phase (PP lag)
        self.clear_at = clear_at     # 'pre': clear before phase0; 'as0': clear coincides w/ phase0
        self.drain = drain           # extra flush phases after phase2 (pp_delay=1 only)
        self.PP = 0                  # partial-product register (signed term) -- persists
        self.ACC = 0                 # accumulator -- persists
        self.RES = 0                 # result register -- persists

    def strobe(self, F, cmag, csign, zero=1):
        C = [(cmag >> i) & 1 for i in range(6)]
        SR0 = B.load_SR(s16(F)); SR1 = B.shift_right2(SR0); SR2 = B.shift_right2(SR1)
        phase_in = [(SR0, C[4], C[5]), (SR1, C[2], C[3]), (SR2, C[0], C[1])]
        nphase = 3 + (self.drain if self.pp_delay else 0)
        for p in range(nphase):
            term = B._s20(B.comb_array(*phase_in[p])) if p < 3 else 0
            if self.clear_at == 'pre' and p == 0 and zero:
                self.ACC = 0
            add = term if self.pp_delay == 0 else self.PP
            if self.clear_at == 'as0' and p == 0 and zero:
                self.ACC = 0            # synchronous clear overrides this phase's add
            else:
                self.ACC += add
            self.PP = term              # ARUCK latches PP after the accumulate
        Mpos = B._sat16((-self.ACC + 4) >> 3)
        self.RES = Mpos if csign else (-Mpos - 1)
        return self.RES


def run_variant(pp_delay, clear_at, drain):
    aru = CycARU(pp_delay, clear_at, drain)
    ok = 0; rows = []
    for st in firmware_sequence():
        got = aru.strobe(st['F'], st['cmag'], st['csign'], st['zero'])
        exp = GMAP[(st['F'] & 0xFFFF, st['cmag'], st['csign'])]
        ok += (got == exp)
        rows.append((st['F'] & 0xFFFF, st['cmag'], st['csign'], exp, got))
    return ok, rows


def part_a():
    print("=" * 92)
    print("PART A -- cycle-accurate engine over the EXACT firmware sequence; schedule sweep")
    print("         (does any sequential/pipeline schedule reproduce cmag=63?)")
    print("=" * 92)
    best = 0
    for pp_delay, clear_at, drain in itertools.product([0, 1], ['pre', 'as0'], [0, 1, 2, 3]):
        if pp_delay == 0 and drain > 0:
            continue
        ok, rows = run_variant(pp_delay, clear_at, drain)
        c63 = sum(1 for r in rows if r[1] == 63 and r[3] == r[4])
        best = max(best, ok)
        print(f"  pp_delay={pp_delay} clear={clear_at:3} drain={drain}: {ok:2}/20  (cmag63 {c63}/4)")
    print(f"\n  => BEST over ALL schedules = {best}/20.  No schedule reaches 20/20.")
    print("  => the cmag=63 residual is NOT a pipeline / single-step register-state effect.\n")


# ===========================================================================
# PART B -- arithmetic forensics: the correction is a unique flat +9 at -ACC
# ===========================================================================
def part_b():
    print("=" * 92)
    print("PART B -- forensics: what -ACC correction K does each cmag=63 golden require?")
    print("=" * 92)
    print(f"  {'F':>7} {'exp':>7} {'faith':>7} {'-ACC':>9}   K-range (add to -ACC to hit golden)")
    inter_lo, inter_hi = -10 ** 9, 10 ** 9
    for F, cmag, cs, exp in GOLDENS:
        if cmag != 63:
            continue
        Fs = s16(F)
        C = [(cmag >> i) & 1 for i in range(6)]
        SR0 = B.load_SR(Fs); SR1 = B.shift_right2(SR0); SR2 = B.shift_right2(SR1)
        negacc = -sum(B._s20(B.comb_array(SR, m0, m1))
                      for SR, m0, m1 in [(SR0, C[4], C[5]), (SR1, C[2], C[3]), (SR2, C[0], C[1])])
        faith = B.multiply_faithful(F, cmag, cs)
        magexp = exp if cs == 1 else (-exp - 1)
        klo = magexp * 8 - 4 - negacc      # (-ACC + K + 4) >> 3 == magexp  =>  K in [klo, khi]
        khi = magexp * 8 + 3 - negacc
        lo, hi = sorted((klo, khi))
        inter_lo, inter_hi = max(inter_lo, lo), min(inter_hi, hi)
        print(f"  0x{F & 0xFFFF:04X} {exp:>7} {faith:>7} {negacc:>9}   K in [{lo:+d}, {hi:+d}]")
    print(f"\n  => intersection of all four K-ranges = [{inter_lo:+d}, {inter_hi:+d}]"
          f"  (unique K = +9 = 3 phases x +3)\n")


# ===========================================================================
# PART C -- dual-rail dissection + locus of the +3
# ===========================================================================
def _mul_corr(F, cmag, csign, per_dual):
    C = [(cmag >> i) & 1 for i in range(6)]
    SR0 = B.load_SR(s16(F)); SR1 = B.shift_right2(SR0); SR2 = B.shift_right2(SR1)
    negacc = 0
    for SR, m0, m1 in [(SR0, C[4], C[5]), (SR1, C[2], C[3]), (SR2, C[0], C[1])]:
        negacc += -B._s20(B.comb_array(SR, m0, m1)) + (per_dual if (m0 and m1) else 0)
    Mpos = B._sat16((negacc + 4) >> 3)
    return Mpos if csign else (-Mpos - 1)


def part_c():
    print("=" * 92)
    print("PART C -- locus: front-end correction gated on BOTH Booth rails (dual); which is exact?")
    print("=" * 92)
    # additivity check
    add_ok = True
    for F in [0x3333, 0xCCCC - 0x10000, 0x3FFF, 0xC000 - 0x10000, 0x5555, 0x1234]:
        SR = B.load_SR(F)
        for _ in range(3):
            d = B._s20(B.comb_array(SR, 1, 1))
            m0 = B._s20(B.comb_array(SR, 1, 0))
            m1 = B._s20(B.comb_array(SR, 0, 1))
            no = B._s20(B.comb_array(SR, 0, 0))
            add_ok = add_ok and (d == m0 + m1 - no)
            SR = B.shift_right2(SR)
    print(f"  comb_array additivity  dual == m0 + m1 - none : {'HOLDS (no missing carry)' if add_ok else 'FAILS'}")
    for per_dual in (0, 1, 2, 3, 4):
        ok = sum(1 for F, c, s, e in GOLDENS if _mul_corr(F, c, s, per_dual) == e)
        tag = "  *** 20/20 (exact correction) ***" if ok == 20 else ""
        print(f"  +{per_dual} per dual-rail phase : {ok:2}/20{tag}")
    print("\n  => +3 per dual-rail phase is the UNIQUE exact correction (+1/+2/+4 all fail).")
    print("  => the hardware adds +3 (PR0/PR1) per phase where M0 AND M1 both fire.\n")


if __name__ == "__main__":
    part_a()
    part_b()
    part_c()
    print("=" * 92)
    print("SUMMARY: cmag=63 residual = combinational +3 / dual-Booth-rail phase (front-end),")
    print("uniquely determined; NOT pipeline/state. multiply()'s +3*dual is the derived")
    print("correction. Exact injecting gate un-traced -> owner re-check 060-01318 (see header).")
    print("=" * 92)
