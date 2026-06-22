#pragma once
// =============================================================================
// sgdsp - Lexicon224XL - bit-exact 224XL ARU reverb reconstruction (integer)
// =============================================================================
// Reproduces the discrete-ARU datapath of the Lexicon 224XL: a 128-step WCS
// microprogram executed once per output sample over a 64K-word circular delay
// memory (DMEM), a 4x16-bit register file, a saturating multiply-accumulate, and
// a 16-bit result register. The reverb tank lives in DMEM + register feedback.
//
// The bit-exact reference is the Python model tools/aru_datapath.py (the 224XL's
// Z80 SBC builds/modulates microcode but does not compute audio). This core is
// authored to match that reference integer-exact; arithmetic details still being
// resolved (tech-ref 4/10) are isolated in ArithProfile so tuning is one line.
//
// Float appears ONLY at the I/O boundary. Everything between floatToAru and
// aruToFloat is integer. See docs/reference/224/224XL_technical_reference.md and
// docs/superpowers/specs/2026-06-22-224xl-aru-core-and-diff-harness-design.md.

#include "../core/types.hpp"       // Sample, SampleRate
#include "../core/platform.hpp"    // SGDSP_INLINE, SGDSP_NOINLINE, SGDSP_ASSERT
#include <cstdint>
#include <array>

namespace sgdsp::reverb
{
using namespace core;

// 16-bit signed ARU word carried in int32 for headroom; accumulator carried in
// int64. DMEM is a hardware-fixed 64K ring (mask 0xFFFF).
using AruWord  = int32_t;
using AruAccum = int64_t;

// ---- OPEN-arithmetic profile (tech-ref 4/10). First-cut values reproduce the
// current aru_datapath.py reference exactly. Move toward hardware by editing here. ----
struct ArithProfile
{
    static constexpr int      kCoeffShift = 7;        // the "/128" denominator (arithmetic >>)
    static constexpr AruAccum kSatMax     = 32767;    // sat16 high rail (reference uses 16-bit sat)
    static constexpr AruAccum kSatMin     = -32768;   // sat16 low rail
    // Hardware targets, NOT yet applied (enabled when matching hardware, not the
    // current reference): 20-bit accumulator, 2-LSB coeff packing, 20->16 result
    // shift, the operand20 = sign_extend(x,17)<<3 alignment.
};

// Saturate to the 16-bit result/accumulator rails (reference sat16).
SGDSP_INLINE AruAccum aruSat16(AruAccum x) noexcept
{
    if (x > ArithProfile::kSatMax) return ArithProfile::kSatMax;
    if (x < ArithProfile::kSatMin) return ArithProfile::kSatMin;
    return x;
}

// One multiply-accumulate step: acc + ((x * coeff) >> 7), saturated.
// Uses arithmetic right shift (floor toward -inf) to match Python `(x*coeff)//128`.
// NOTE: C++20 guarantees arithmetic shift on signed; on MSVC/GCC/Clang it already
// holds in C++17. Do NOT replace with `/ 128` (truncates toward zero on negatives).
SGDSP_INLINE AruAccum aruMac(AruAccum acc, AruWord x, int coeff) noexcept
{
    const AruAccum prod = (static_cast<AruAccum>(x) * coeff) >> ArithProfile::kCoeffShift;
    return aruSat16(acc + prod);
}

} // namespace sgdsp::reverb
