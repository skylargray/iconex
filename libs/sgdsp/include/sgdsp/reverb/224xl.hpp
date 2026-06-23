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
// authored to match that reference integer-exact; the firmware/schematic-resolved
// arithmetic constants are isolated in ArithProfile so tuning is one line.
//
// Float appears ONLY at the I/O boundary. Everything between floatToAru and
// aruToFloat is integer. See docs/reference/224/224XL_technical_reference.md and
// docs/superpowers/specs/2026-06-22-224xl-aru-core-and-diff-harness-design.md.

#include "../core/types.hpp"       // Sample, SampleRate
#include "../core/platform.hpp"    // SGDSP_INLINE, SGDSP_NOINLINE, SGDSP_ASSERT
#include <cstdint>

namespace sgdsp::reverb
{
using namespace core;

// 16-bit signed ARU word carried in int32 for headroom; accumulator carried in
// int64. DMEM is a hardware-fixed 64K ring (mask 0xFFFF).
using AruWord  = int32_t;
using AruAccum = int64_t;

// ---- ARU arithmetic profile (firmware/schematic-resolved; authority is
// tools/aru_datapath.py run()/run_trace()). The hardware datapath is:
//   * 6-bit coefficient C = (abs(coeff7) >> 1), sign applied via CSIGN (so the
//     effective signed coefficient Cs = +/-(mag>>1)).
//   * operand = x << 3 (the 17->20 bit operand alignment into the multiplier).
//   * product = (operand * Cs) >> 6   (arithmetic right shift; floors toward -inf).
//   * 20-bit saturating accumulator, rails +/-524287.
//   * result register RES = sat16(ACC >> 3), rails [-32768, +32767].
// These supersede the old (x*coeff)>>7 / 16-bit-acc first cut. Move toward any
// further hardware nuance by editing the constants here. ----
struct ArithProfile
{
    static constexpr int      kOperandShift = 3;        // operand = x << 3 (multiplier input align)
    static constexpr int      kCoeffShift   = 1;        // 6-bit coeff = (abs(coeff7) >> 1)
    static constexpr int      kProdShift    = 6;        // product = (operand * Cs) >> 6
    static constexpr int      kResultShift  = 3;        // RES = sat16(ACC >> 3)
    static constexpr AruAccum kAccMax       = 524287;   // 20-bit accumulator high rail (+2^19-1)
    static constexpr AruAccum kAccMin       = -524287;  // 20-bit accumulator low rail (reference sat20)
    static constexpr AruAccum kResMax       = 32767;    // 16-bit result register high rail
    static constexpr AruAccum kResMin       = -32768;   // 16-bit result register low rail
};

// Saturate to the 20-bit signed accumulator rails (reference sat20, +/-524287).
SGDSP_INLINE AruAccum aruSat20(AruAccum x) noexcept
{
    if (x > ArithProfile::kAccMax) return ArithProfile::kAccMax;
    if (x < ArithProfile::kAccMin) return ArithProfile::kAccMin;
    return x;
}

// Saturate to the 16-bit result-register rails (reference sat16, [-32768, +32767]).
SGDSP_INLINE AruAccum aruSat16(AruAccum x) noexcept
{
    if (x > ArithProfile::kResMax) return ArithProfile::kResMax;
    if (x < ArithProfile::kResMin) return ArithProfile::kResMin;
    return x;
}

// The 6-bit signed coefficient Cs = +/-(abs(coeff7) >> 1) carried by CSIGN.
// coeff7 is the decoded signed 7-bit-magnitude microword field (-127..127).
SGDSP_INLINE int aruCoeff6(int coeff7) noexcept
{
    SGDSP_ASSERT(coeff7 >= -127 && coeff7 <= 127);
    const int mag = coeff7 < 0 ? -coeff7 : coeff7;
    const int c   = mag >> ArithProfile::kCoeffShift;   // (mag >> 1), 6-bit magnitude
    return coeff7 < 0 ? -c : c;
}

// The ARU product term: operand = x<<3, prod = (operand * Cs) >> 6. Arithmetic
// right shift floors toward -inf to match Python `(operand*Cs) >> 6`. Cs is the
// already-resolved 6-bit signed coefficient (see aruCoeff6). NOTE: C++20 guarantees
// arithmetic shift on signed; on MSVC/GCC/Clang it already holds in C++17. Do NOT
// use `/ 64` (truncates toward zero on negatives). This is the SINGLE source of the
// product term, shared by aruMac and the datapath so the unit test (via aruMac) and
// executeSample cannot drift.
SGDSP_INLINE AruAccum aruProd(AruWord x, int cs6) noexcept
{
    SGDSP_ASSERT(cs6 >= -63 && cs6 <= 63);             // 6-bit signed coefficient
    const AruAccum operand = static_cast<AruAccum>(x) << ArithProfile::kOperandShift;
    return (operand * cs6) >> ArithProfile::kProdShift;
}

// One multiply-accumulate step: acc + product, 20-bit-saturated. `cs6` is the
// resolved 6-bit signed coefficient (apply aruCoeff6 to the raw 7-bit field first).
SGDSP_INLINE AruAccum aruMac(AruAccum acc, AruWord x, int cs6) noexcept
{
    return aruSat20(acc + aruProd(x, cs6));
}

// Per-step probe record (mirrors aru_datapath.run_trace tuple field order).
struct Probe
{
    int64_t n, s, addr, dab, racc_in, prod, acc, res;
};
static constexpr int64_t kProbeResSentinel = (int64_t)0x8000000000000000ULL; // INT64_MIN

// A decoded active microword step (NOP steps are dropped at load time).
struct AruStep
{
    int      s;        // original step index 0..127
    uint32_t offset;   // DMEM offset; addr = (pos - offset) & 0xFFFF
    int      coeff;    // signed 7-bit magnitude (-127..127); kept for L1 decode parity
    int      cs6;      // resolved 6-bit signed coefficient Cs = +/-(abs(coeff)>>1)
    uint8_t  zero;     // clear accumulator before MAC
    uint8_t  xfer;     // XFER: load result register (RES = sat16(ACC>>3)) / write tank
    uint8_t  wa;       // write-register address (3 = pass-through)
    uint8_t  ra;       // read-register address (b5<<1 | b4)
    uint8_t  b3;       // DAB source / DMEM read-write select: b3 -> dab=RES & post-XFER DM write
};

template <uint32_t DmemWords = 65536, uint32_t Channels = 2>
class Lexicon224XLCore
{
    static_assert(DmemWords >= 65536, "224XL DMEM is a 64K ring; size must be >= 65536");
    static_assert(Channels == 1 || Channels == 2, "Channels must be 1 or 2");

public:
    static constexpr uint32_t kDmemMask = 0xFFFFu;  // hardware 64K ring mask

    // ---- Lifecycle ----
    SGDSP_NOINLINE void prepare(SampleRate sampleRate, AruWord* dmem) noexcept
    {
        sampleRate_ = sampleRate;
        dmem_ = dmem;
        reset();
    }

    // Decode a 128-step WCS image (4 active-low bytes/step) into the active-step
    // list, skipping NOPs (lane2==lane3==0xFF). Matches aru_datapath.load_microcode.
    SGDSP_NOINLINE void loadProgram(const uint8_t wcs[512]) noexcept
    {
        nActive_ = 0;
        for (int s = 0; s < 128; ++s) {
            const uint8_t l0 = wcs[s*4+0], l1 = wcs[s*4+1];
            const uint8_t l2 = wcs[s*4+2], l3 = wcs[s*4+3];
            if (l2 == 0xFF && l3 == 0xFF) continue;          // NOP / pure-delay fill
            const uint8_t ctl = static_cast<uint8_t>(~l2);
            AruStep st;
            st.s      = s;
            st.offset = static_cast<uint32_t>(~(l0 | (l1 << 8))) & 0xFFFFu;
            st.coeff  = (l3 & 0x80) ? -static_cast<int>(l3 & 0x7F) : static_cast<int>(l3 & 0x7F);
            st.cs6    = aruCoeff6(st.coeff);   // 6-bit signed coeff Cs = +/-(abs(coeff)>>1)
            st.zero   = (ctl >> 7) & 1;
            st.xfer   = (ctl >> 2) & 1;
            st.wa     = ctl & 3;
            st.ra     = (ctl >> 4) & 3;     // datapath-validated RA = b5<<1 | b4
            st.b3     = (ctl >> 3) & 1;
            steps_[nActive_++] = st;
        }
        firstActive_ = (nActive_ > 0) ? 0 : -1;
    }

    SGDSP_NOINLINE void reset() noexcept
    {
        for (auto& r : R_) r = 0;
        acc_ = 0;
        res_ = 0;
        if (dmem_) for (uint32_t i = 0; i <= kDmemMask; ++i) dmem_[i] = 0;
        pos_ = 0;
        sampleIndex_ = 0;
    }

    int activeStepCount() const noexcept { return nActive_; }
    const AruStep& step(int i) const noexcept { return steps_[i]; }

    // ---- Integer surface (harness) ----
    SGDSP_INLINE void processFixed(AruWord in, AruWord& outL, AruWord& outR) noexcept
    {
        const AruWord o = executeSample<false>(in, nullptr, nullptr);
        outL = o; outR = o;   // first cut: mono datapath duplicated; FPC L/R split deferred
    }

    // Instrumented twin for the diff harness. Records one probe per active step into
    // `probes` (caller MUST size it >= activeStepCount()); writes the probe count to
    // *nProbesOut and the per-sample energy to *esumOut.
    SGDSP_NOINLINE AruWord processFixedTraced(AruWord in, Probe* probes, int* nProbesOut,
                                              int64_t* esumOut) noexcept
    {
        int n = 0;
        int64_t esum = 0;
        const AruWord o = executeSample<true>(in, probes, &n, &esum);
        if (nProbesOut) *nProbesOut = n;
        if (esumOut) *esumOut = esum;
        return o;
    }

    // ---- Float boundary (DPF/sgdsp); only float in the signal path ----
    SGDSP_INLINE void process(Sample in, Sample& outL, Sample& outR) noexcept
    {
        AruWord l, r;
        processFixed(floatToAru(in), l, r);
        outL = aruToFloat(l);
        outR = aruToFloat(r);
    }

    // ---- Parameters (scaffolded; static CONCERT is the bring-up target) ----
    void setParameter(int index, float value01) noexcept { (void)index; (void)value01; }

private:
    static constexpr float kAruScale = 32768.0f;
    SGDSP_INLINE static AruWord floatToAru(Sample x) noexcept
    {
        float s = x * kAruScale;
        if (s >  32767.0f) s =  32767.0f;
        if (s < -32768.0f) s = -32768.0f;
        return static_cast<AruWord>(s >= 0.0f ? s + 0.5f : s - 0.5f);
    }
    SGDSP_INLINE static Sample aruToFloat(AruWord v) noexcept
    {
        return static_cast<Sample>(v) * (1.0f / kAruScale);
    }

    // The 128-step microprogram for one output sample. Trace==true records probes
    // and the energy sum, exactly mirroring aru_datapath.run_trace. The two
    // instantiations share ONE datapath (DRY); tracing compiles out of the hot path.
    template <bool Trace>
    SGDSP_INLINE AruWord executeSample(AruWord in, Probe* probes, int* nProbes,
                                       int64_t* esumOut = nullptr) noexcept
    {
        SGDSP_ASSERT(dmem_ != nullptr);   // prepare() must connect external DMEM before processing
        pos_ = (pos_ + 1) & kDmemMask;
        int np = 0;
        int64_t esum = 0;
        AruWord lastRes = res_;
        for (int i = 0; i < nActive_; ++i) {
            const AruStep& st = steps_[i];
            // 1. delay address
            const uint32_t addr = (pos_ - st.offset) & kDmemMask;
            // 2. DAB source: b3 -> the CURRENT (pre-XFER) result register drives DAB;
            //    else read DMEM. Additive impulse at the first active step of sample 0.
            AruWord dab = st.b3 ? res_ : dmem_[addr];
            if (i == firstActive_) dab += in;     // additive injection: equals the reference's
                                                  // dab=imp at sample 0 (DM/RES are 0 there) and
                                                  // generalizes to continuous input on the float path
            // 3. (coefficient Cs is precomputed as st.cs6 = +/-(abs(coeff)>>1))
            // 4. LS670 read-before-write: read the multiplicand FIRST, then write the bus.
            const AruWord raccIn = R_[st.ra];
            R_[st.wa] = dab;
            // 5. ZERO clears the accumulator before this step's product.
            if (st.zero) acc_ = 0;
            // 6. MAC: operand = raccIn<<3, prod = (operand*Cs)>>6, 20-bit saturating acc.
            const AruAccum prod = aruProd(raccIn, st.cs6);
            acc_ = aruSat20(acc_ + prod);
            // 7. XFER then b3 write-back: RES loads from sat16(ACC>>3) FIRST, then the
            //    b3 write-back stores the POST-XFER RES into DMEM (ordering is load-bearing:
            //    a b3+XFER comb closer writes the just-computed RES while step-3's R[WA]
            //    captured the OLD RES via dab earlier this sample).
            int64_t resVal = kProbeResSentinel;
            if (st.xfer) {
                res_ = static_cast<AruWord>(aruSat16(acc_ >> ArithProfile::kResultShift));
                resVal = res_;
            }
            if (st.b3) dmem_[addr] = res_;
            // 8. energy probe (sum |RES| over XFER steps)
            if (st.xfer) {
                esum += (res_ < 0) ? -res_ : res_;
                lastRes = res_;
            }
            if (Trace && probes) {
                probes[np++] = Probe{ (int64_t)sampleIndex_, (int64_t)st.s, (int64_t)addr,
                                      (int64_t)dab, (int64_t)raccIn, (int64_t)prod,
                                      (int64_t)acc_, resVal };
            }
        }
        if (Trace) { if (nProbes) *nProbes = np; if (esumOut) *esumOut = esum; }
        ++sampleIndex_;
        return lastRes;   // audio proxy = last RES of the sample
    }

    // Group 1: hot per-sample state
    AruWord  R_[4] = {0, 0, 0, 0};
    AruAccum acc_ = 0;
    AruWord  res_ = 0;
    uint32_t pos_ = 0;
    int64_t  sampleIndex_ = 0;
    // Group 2: program
    AruStep  steps_[128];
    int      nActive_ = 0;
    int      firstActive_ = -1;
    // Group 3: external DMEM + rate
    AruWord*   dmem_ = nullptr;
    SampleRate sampleRate_ = 0;
};

template <uint32_t N = 65536> using Lexicon224XL     = Lexicon224XLCore<N, 2>;
template <uint32_t N = 65536> using Lexicon224XLMono = Lexicon224XLCore<N, 1>;

} // namespace sgdsp::reverb
