#pragma once
// =============================================================================
// sgdsp - Lexicon224XL - gate-level ARU Booth comb array (private detail header)
// =============================================================================
// Bit-for-bit C++ port of tools/aru_booth.py (the literal gate-level model of
// the 224XL ARU modified-Booth multiplier front end, netlist section 4F) plus
// the raw3() front-end walk of tools/aru_freerun22_rtl.py (sessions 0027/0028).
//
// The tables below transcribe the Python tables EXACTLY. They encode
// owner-verified schematic corrections read against 060-01318 (netlist 4F.4):
//   aru_U40.pin1  SR3  -> SR5    (operand bit F2 enters the M1/x2 stream)
//   aru_U26.pin12 SR8  -> SR10   (F7 enters the M0/x1 stream)
//   aru_U51.pin4  SR12 -> SR14   (F11 enters the M0/x1 stream)
// and the NET straight Sigma->PR weighting (the 4.7 within-nibble reversal
// cancels against the matching reversal in the PR->accumulator routing, 4F.9).
// Do NOT "simplify" or re-derive these tables.
//
// Conventions:
//   * SR is the 20-bit operand shifter pattern carried in a uint32_t
//     (bit i of the word = SR[i] of the Python list).
//   * combArray() returns the RAW comb-array output: the ACTIVE-LOW 20-bit
//     product-register pattern (PR), loaded raw by the product register
//     (aru_U10/U11/U12) - no complement anywhere in this header.
//   * All values are phys (complement-domain) patterns; the CPU/value view
//     lives at the engine boundaries only (see 224xl.hpp).

#include <cstdint>

namespace sgdsp::reverb::aru224 {

// ---------------------------------------------------------------------------
// 4F.4  SR bit tapped by each NAND A input, indexed [chip][gate-1].
// Gate A-input pins: g1=pin1, g2=pin4, g3=pin9, g4=pin12.
// Chip index order below is fixed by kChipId; the three owner-verified
// corrections are marked as in tools/aru_booth.py.
// ---------------------------------------------------------------------------
enum ChipId : uint8_t { cU14 = 0, cU28, cU40, cU41, cU26, cU27, cU50, cU51, cU52, cU53, kNumChips };

inline constexpr uint8_t kNandASr[kNumChips][4] = {
    /* U14 */ { 3,  4,  1,  2},
    /* U28 */ { 3,  1,  2,  0},
    /* U40 */ { 5,  7,  4,  6},   // U40.p1: SR3 -> SR5 (owner-corrected)
    /* U41 */ { 7,  8,  5,  6},
    /* U26 */ {11,  9, 12, 10},   // U26.p12: SR8 -> SR10 (owner-corrected)
    /* U27 */ { 9, 10,  8, 11},
    /* U50 */ {12, 13, 14, 15},
    /* U51 */ {13, 14, 15, 16},   // U51.p4: SR12 -> SR14 (owner-corrected)
    /* U52 */ {17, 18, 19, 16},
    /* U53 */ {17, 18, 19, 19},
};

// 4F.5  M-rail per chip: 0 = M0 (x1 Booth select), 1 = M1 (x2).
// M0_CHIPS = {U14, U26, U41, U51, U53}; M1_CHIPS = {U27, U28, U40, U50, U52}.
inline constexpr uint8_t kChipRail[kNumChips] = {
    /* U14 */ 0, /* U28 */ 1, /* U40 */ 1, /* U41 */ 0, /* U26 */ 0,
    /* U27 */ 1, /* U50 */ 1, /* U51 */ 0, /* U52 */ 1, /* U53 */ 0,
};

// 4F.7  adder A/B inputs as (chip, gate) refs (gate = which NAND output feeds
// it, 1..4); cin = -1 for the +5V tie, else the index of the upstream adder in
// kAdders (= Python CARRY_ORDER: U13, U39, U25, U38, U24). prBase = the NET
// straight Sigma->PR nibble base (4.7 + 4.6 reversals cancel; Sigma k -> PR
// bit prBase+k), Python _NIB/SIGMA_TO_PR.
struct GateRef  { uint8_t chip, gate; };
struct AdderSpec { GateRef in[8]; int8_t cin; uint8_t prBase; };

inline constexpr AdderSpec kAdders[5] = {
    /* U13 */ {{{cU14,3},{cU14,4},{cU14,1},{cU14,2},
                {cU28,4},{cU28,2},{cU28,3},{cU28,1}}, -1,  0},
    /* U39 */ {{{cU41,3},{cU41,4},{cU41,1},{cU41,2},
                {cU40,3},{cU40,1},{cU40,4},{cU40,2}},  0,  4},
    /* U25 */ {{{cU26,2},{cU26,4},{cU26,1},{cU26,3},
                {cU27,3},{cU27,1},{cU27,2},{cU27,4}},  1,  8},
    /* U38 */ {{{cU51,1},{cU51,2},{cU51,3},{cU51,4},
                {cU50,1},{cU50,2},{cU50,3},{cU50,4}},  2, 12},
    /* U24 */ {{{cU53,1},{cU53,2},{cU53,4},{cU53,3},
                {cU52,4},{cU52,1},{cU52,2},{cU52,3}},  3, 16},
};

// ---------------------------------------------------------------------------
// Combinational NAND array + 5-adder carry chain -> 20-bit (active-low)
// product-register pattern.  Port of aru_booth.comb_array.
// ---------------------------------------------------------------------------
inline uint32_t combArray(uint32_t SR, uint32_t M0, uint32_t M1) noexcept
{
    // Y per gate: NAND(SR[tap], Mrail(chip));  _nand(a,b) = 0 if (a & b) else 1
    uint8_t Y[kNumChips][4];
    for (int c = 0; c < kNumChips; ++c) {
        const uint32_t m = kChipRail[c] ? M1 : M0;
        for (int g = 0; g < 4; ++g)
            Y[c][g] = static_cast<uint8_t>((((SR >> kNandASr[c][g]) & 1u) & m) ? 0u : 1u);
    }
    uint32_t PR = 0;
    uint32_t carry[5] = {0, 0, 0, 0, 0};
    for (int a = 0; a < 5; ++a) {
        const AdderSpec& ad = kAdders[a];
        uint32_t A = 0, B = 0;
        for (int i = 0; i < 4; ++i) {
            A |= static_cast<uint32_t>(Y[ad.in[i].chip][ad.in[i].gate - 1]) << i;
            B |= static_cast<uint32_t>(Y[ad.in[4 + i].chip][ad.in[4 + i].gate - 1]) << i;
        }
        const uint32_t cin = (ad.cin < 0) ? 1u : carry[ad.cin];
        const uint32_t s = A + B + cin;
        carry[a] = (s >> 4) & 1u;
        PR |= (s & 0xFu) << ad.prBase;                 // straight Sigma k -> PR prBase+k
    }
    return PR;
}

// 74194 parallel load (4F.3): SR = sign_extend_20(F << 3).  The Python engine
// reads the phys operand SIGNED (s16) before load_SR, which masks back to 16
// bits - net effect: bits 3..18 = F0..F15, bit 19 = replicated F15, bits 0..2 = 0.
inline uint32_t loadSR(uint16_t F) noexcept
{
    return (static_cast<uint32_t>(F) << 3) | ((static_cast<uint32_t>(F >> 15) & 1u) << 19);
}

// Dual-rank 74194 shift-right-by-2 (4F.3): new[i] = old[i+2] for i <= 17;
// the top two bits HOLD (new[18] = old[18], new[19] = old[19]).
inline uint32_t shiftRight2(uint32_t SR) noexcept
{
    return ((SR >> 2) & 0x3FFFFu) | (SR & 0xC0000u);
}

// ---------------------------------------------------------------------------
// raw3 (port of aru_freerun22_rtl.raw3): the three RAW comb-array outputs
// (phys active-low 20-bit patterns) of one multiply of the PHYS operand - the
// actual product-register loads, pairs A/B/C in fig-3.4 order:
// (C4,C5), (C2,C3), (C0,C1), with a shift-right-2 between phases.
// ---------------------------------------------------------------------------
inline void raw3(uint16_t opndPhys, uint8_t cmag,
                 uint32_t& rawA, uint32_t& rawB, uint32_t& rawC) noexcept
{
    uint32_t SR = loadSR(opndPhys);
    rawA = combArray(SR, (cmag >> 4) & 1u, (cmag >> 5) & 1u);
    SR = shiftRight2(SR);
    rawB = combArray(SR, (cmag >> 2) & 1u, (cmag >> 3) & 1u);
    SR = shiftRight2(SR);
    rawC = combArray(SR, (cmag >> 0) & 1u, (cmag >> 1) & 1u);
}

// The zero-rail comb baseline (M0=M1=0 -> every NAND high -> PR = 0xFFFFF,
// operand-independent): the value-inert phase. Power-on pipeline fill.
inline constexpr uint32_t kRawIdle = 0xFFFFFu;

} // namespace sgdsp::reverb::aru224
