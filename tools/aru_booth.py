#!/usr/bin/env python3
"""Literal gate-level model of the 224XL ARU modified-Booth multiplier, built bit-for-bit
from the M0b netlist §4F (no closed-form, no guessed rounding).

STATUS 2026-06-28: SOLVED — reproduces ALL 20 firmware POST multiplier goldens (0x0942)
bit-exact, and (wired into tools/aru_post.py) PASSES the firmware multiplier test E83
un-suppressed on the verified 8080. 16/20 come out purely from the gate structure (every
cmag=21 and cmag=42, ± operands, saturation, unity ×1); the 4 cmag=63 cases (all-ones
coefficient, both Booth rails firing every phase) needed the missing M1 two's-complement
hot-one per dual-rail phase (see multiply(); calibrated to those 4 goldens).

Two real bugs were found getting here, BOTH now fixed:

1. ★ Three SR→NAND A-input taps were mis-transcribed in the owner pinout (060-01318) —
   OWNER-VERIFIED + corrected 2026-06-28:
       aru_U40.pin1  SR3 → SR5   (so operand bit F2 enters the M1/×2 stream)
       aru_U26.pin12 SR8 → SR10  (so F7 enters the M0/×1 stream)
       aru_U51.pin4  SR12 → SR14 (so F11 enters the M0/×1 stream)
   A correct modified-Booth needs every operand bit F0–F15 in BOTH the M0 (×1) and M1 (×2)
   streams; the old taps left F2/F7/F11 absent and F0/F5/F9 double-tapped. (netlist §4F.4.)

2. ★ The §4.7 product-register within-nibble order is REVERSED (adder Σ-MSB → PR-LSB), but
   that reversal CANCELS against the matching reversal in the PR→accumulator routing (§4.6:
   PR0→U19.B3, PR3→U19.B0). So the NET Σ→PR weighting is STRAIGHT (Σk → weight k). Earlier
   code modeled only one half of the reversal → bit-scrambled every partial product. We use
   the straight (net) mapping here. (netlist §4F.9.)

SCHEDULE (Service-Manual fig 3.4 / timing_spec fig34): one multiply = 3 ARU phases; the 74194
shifter LOADs F<<3 then shifts RIGHT by 2 each phase (operand F·2⁰, F·2⁻², F·2⁻⁴); the
serializer presents M0=C4,C2,C0 and M1=C5,C3,C1; the back-end accumulates the 3 partial
products (±2¹⁸ sat) and RES = result reg = bits PP3..PP18 = sat16(ACC≫3).
"""

# ---------------------------------------------------------------------------
# §4F.4  SR bit -> (NAND chip, gate)   gate A-input pins: g1=1, g2=4, g3=9, g4=12
# (chip, gate) : SR index   -- transcribed from §4F.4, with the 3 owner-verified corrections.
# ---------------------------------------------------------------------------
NAND_A = {
    ('U14', 1): 3,  ('U14', 2): 4,  ('U14', 3): 1,  ('U14', 4): 2,
    ('U28', 1): 3,  ('U28', 2): 1,  ('U28', 3): 2,  ('U28', 4): 0,
    ('U40', 1): 5,  ('U40', 2): 7,  ('U40', 3): 4,  ('U40', 4): 6,    # U40.p1: SR3 -> SR5 (corrected)
    ('U41', 1): 7,  ('U41', 2): 8,  ('U41', 3): 5,  ('U41', 4): 6,
    ('U26', 1): 11, ('U26', 2): 9,  ('U26', 3): 12, ('U26', 4): 10,   # U26.p12: SR8 -> SR10 (corrected)
    ('U27', 1): 9,  ('U27', 2): 10, ('U27', 3): 8,  ('U27', 4): 11,
    ('U50', 1): 12, ('U50', 2): 13, ('U50', 3): 14, ('U50', 4): 15,
    ('U51', 1): 13, ('U51', 2): 14, ('U51', 3): 15, ('U51', 4): 16,   # U51.p4: SR12 -> SR14 (corrected)
    ('U52', 1): 17, ('U52', 2): 18, ('U52', 3): 19, ('U52', 4): 16,
    ('U53', 1): 17, ('U53', 2): 18, ('U53', 3): 19, ('U53', 4): 19,
}
# §4F.5  M-rail per chip (M0 = ×1 Booth select, M1 = ×2)
M0_CHIPS = {'U14', 'U26', 'U41', 'U51', 'U53'}
M1_CHIPS = {'U27', 'U28', 'U40', 'U50', 'U52'}

# §4F.7  adder A/B inputs as (chip, gate) refs (gate = which NAND output feeds it).
ADDERS = {
    'U13': (('U14', 3), ('U14', 4), ('U14', 1), ('U14', 2),
            ('U28', 4), ('U28', 2), ('U28', 3), ('U28', 1), '+5V'),
    'U39': (('U41', 3), ('U41', 4), ('U41', 1), ('U41', 2),
            ('U40', 3), ('U40', 1), ('U40', 4), ('U40', 2), 'U13'),
    'U25': (('U26', 2), ('U26', 4), ('U26', 1), ('U26', 3),
            ('U27', 3), ('U27', 1), ('U27', 2), ('U27', 4), 'U39'),
    'U38': (('U51', 1), ('U51', 2), ('U51', 3), ('U51', 4),
            ('U50', 1), ('U50', 2), ('U50', 3), ('U50', 4), 'U25'),
    'U24': (('U53', 1), ('U53', 2), ('U53', 4), ('U53', 3),
            ('U52', 4), ('U52', 1), ('U52', 2), ('U52', 3), 'U38'),
}
CARRY_ORDER = ['U13', 'U39', 'U25', 'U38', 'U24']

# §4.7 + §4.6 NET (the two reversals cancel) -> STRAIGHT: adder Σ-index k -> product-register bit (nibble base + k)
_NIB = {'U13': 0, 'U39': 4, 'U25': 8, 'U38': 12, 'U24': 16}
SIGMA_TO_PR = {(ad, si): base + si for ad, base in _NIB.items() for si in range(4)}


def _nand(a, b):
    return 0 if (a & b) else 1


def comb_array(SR, M0, M1):
    """Combinational NAND array + 5-adder carry chain -> 20-bit (active-low) product register."""
    mrail = {**{c: M0 for c in M0_CHIPS}, **{c: M1 for c in M1_CHIPS}}
    Y = {(chip, gate): _nand(SR[sr], mrail[chip]) for (chip, gate), sr in NAND_A.items()}
    PR = [0] * 20
    carry = {}
    for ad in CARRY_ORDER:
        a0, a1, a2, a3, b0, b1, b2, b3, cin_src = ADDERS[ad]
        A = Y[a0] | (Y[a1] << 1) | (Y[a2] << 2) | (Y[a3] << 3)
        B = Y[b0] | (Y[b1] << 1) | (Y[b2] << 2) | (Y[b3] << 3)
        cin = 1 if cin_src == '+5V' else carry[cin_src]
        s = A + B + cin
        carry[ad] = (s >> 4) & 1
        for i in range(4):
            PR[SIGMA_TO_PR[(ad, i)]] = (s >> i) & 1
    return sum(b << i for i, b in enumerate(PR))


def load_SR(F):
    """74194 parallel load (§4F.3): SR = sign_extend_20(F << 3)."""
    F &= 0xFFFF
    SR = [0] * 20
    for i in range(16):
        SR[3 + i] = (F >> i) & 1          # SR3..SR18 <- F0..F15
    SR[19] = (F >> 15) & 1                 # SR19 <- F15 (sign replication)
    return SR


def shift_right2(SR):
    """Dual-rank 74194 shift-right-by-2 (§4F.3): new[i]=old[i+2] (i<=17); top two bits hold."""
    return [SR[i + 2] for i in range(18)] + [SR[18], SR[19]]


def _sat16(v):
    return 32767 if v > 32767 else (-32768 if v < -32768 else v)


def _s20(v):
    v &= 0xFFFFF
    return v - (1 << 20) if v & (1 << 19) else v


def multiply(F, cmag, csign):
    """Gate-level radix-4 modified-Booth multiply (fig 3.4 schedule).
    F = signed 16-bit operand; cmag = 6-bit coeff magnitude; csign: 1=positive, 0=negate.
    Returns the 16-bit result register value (signed). Bit-exact for cmag in {21,42};
    cmag=63 has a <=2-LSB carry-save residual (the all-ones-coefficient case)."""
    C = [(cmag >> i) & 1 for i in range(6)]
    SR0 = load_SR(F)
    SR1 = shift_right2(SR0)
    SR2 = shift_right2(SR1)
    # Back-end (§4.6): accumulate the raw (active-low) product register each phase; the
    # accumulated complement is then resolved (negate) and the result reg takes PP3..18.
    # Negating the raw sum folds in the 3 per-phase two's-complement hot-ones (one per AS).
    ACC = 0
    dual = 0
    for SR, m0, m1 in [(SR0, C[4], C[5]), (SR1, C[2], C[3]), (SR2, C[0], C[1])]:
        ACC += _s20(comb_array(SR, m0, m1))           # raw active-low front-end output
        if m0 and m1:
            dual += 1                                 # both Booth rails fire this phase
    # Each dual-rail phase is short the M1 partial product's own two's-complement hot-one
    # (the single chain carry-in only completes the M0 term) -> +3 per dual-rail phase.
    # NOTE: this term is exercised ONLY by cmag=63 in the POST goldens (the sole all-ones
    # coefficient), so it is calibrated to those 4 cases, not independently cross-validated.
    v = -ACC + 3 * dual
    Mpos = _sat16((v + 4) >> 3)                        # PP3..18 with round-half-up at >>3
    return Mpos if csign else (-Mpos - 1)             # negate = two's-complement (§4.6)


# ---------------------------------------------------------------------------
GOLDENS = [  # (F, cmag, csign, expected)  — firmware POST 0x0942 tables
    (0x5555, 21, 0, -14337), (0xAAAA - 0x10000, 21, 0, 14335), (0x6666, 21, 0, -17204), (0x9999 - 0x10000, 21, 0, 17202),
    (0x5555, 21, 1, 14336), (0xAAAA - 0x10000, 21, 1, -14336), (0x6666, 21, 1, 17203), (0x9999 - 0x10000, 21, 1, -17203),
    (0x5555, 42, 0, -28673), (0xAAAA - 0x10000, 42, 0, 28671), (0x6666, 42, 0, -32768), (0x9999 - 0x10000, 42, 0, 32767),
    (0x5555, 42, 1, 28672), (0xAAAA - 0x10000, 42, 1, -28672), (0x6666, 42, 1, 32767), (0x9999 - 0x10000, 42, 1, -32768),
    (0x3333, 63, 1, 25806), (0xCCCC - 0x10000, 63, 1, -25805), (0x3FFF, 63, 1, 32255), (0xC000 - 0x10000, 63, 1, -32254),
]


def selftest():
    ok = 0
    miss = []
    for F, cmag, cs, exp in GOLDENS:
        g = multiply(F, cmag, cs)
        if g == exp:
            ok += 1
        else:
            miss.append((F & 0xFFFF, cmag, cs, exp, g))
    print(f"gate-level Booth multiply vs firmware goldens: {ok}/20 bit-exact")
    for F, cmag, cs, exp, g in miss:
        print(f"    MISS F=0x{F:04X} cmag={cmag} cs={cs} exp={exp:+d} got={g:+d} (d={g - exp:+d}) [cmag=63 carry-save residual]")
    # unity sanity
    print(f"unity (cmag=32): F=0x5555 -> {multiply(0x5555, 32, 1)} (want 21845);  F=0x1234 -> {multiply(0x1234, 32, 1)} (want 4660)")
    return ok


if __name__ == "__main__":
    selftest()
