#pragma once
// =============================================================================
// sgdsp - Core Type Definitions
// =============================================================================

#include <cstdint>
#include <cstddef>
#include "platform.hpp"

namespace sgdsp::core {

// =============================================================================
// Primary Sample Type (configurable at compile time)
// =============================================================================
#if defined(SGDSP_USE_FLOAT64)
    using Sample = double;
#elif defined(SGDSP_USE_Q31) && SGDSP_HAS_CMSIS
    using Sample = q31_t;
#elif defined(SGDSP_USE_Q15) && SGDSP_HAS_CMSIS
    using Sample = q15_t;
#else
    using Sample = float;  // Default: float32
#endif

// =============================================================================
// Fixed-Point Types
// =============================================================================
#if SGDSP_HAS_CMSIS
    using Q15 = q15_t;   // 1.15 fixed-point
    using Q31 = q31_t;   // 1.31 fixed-point
#else
    using Q15 = int16_t;
    using Q31 = int32_t;
#endif

// =============================================================================
// Size and Rate Types
// =============================================================================
using BlockSize = uint16_t;
using SampleRate = uint32_t;
using Phase = uint32_t;  // 32-bit phase accumulator for oscillators

// =============================================================================
// Sample Rate Tags (for compile-time calculations)
// =============================================================================
template<SampleRate Fs>
struct SampleRateTag {
    static constexpr SampleRate value = Fs;
    static constexpr float period = 1.0f / static_cast<float>(Fs);
    static constexpr float nyquist = static_cast<float>(Fs) / 2.0f;
};

// Common sample rates
using SR_44100  = SampleRateTag<44100>;
using SR_48000  = SampleRateTag<48000>;
using SR_96000  = SampleRateTag<96000>;
using SR_192000 = SampleRateTag<192000>;

// Daisy Seed 2 DFM default
using SR_DAISY_DEFAULT = SR_48000;

// =============================================================================
// Common Constants
// =============================================================================
constexpr float kPi = 3.14159265358979323846f;
constexpr float kTwoPi = 6.28318530717958647692f;
constexpr float kHalfPi = 1.57079632679489661923f;
constexpr float kSqrt2 = 1.41421356237309504880f;
constexpr float kInvSqrt2 = 0.70710678118654752440f;

// dB conversion constants
constexpr float kLog10_20 = 0.1151292546497023f;    // ln(10) / 20
constexpr float k20_Log10e = 8.685889638065035f;    // 20 / ln(10)

}  // namespace sgdsp::core
