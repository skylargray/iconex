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

// Saturate to the result/accumulator rails (reference sat16). NOTE: the "16" in the
// name reflects the first-cut 16-bit rails; revisit the name if ArithProfile is
// retargeted to the 20-bit hardware accumulator.
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
    SGDSP_ASSERT(coeff >= -127 && coeff <= 127);   // 7-bit sign-magnitude coefficient
    const AruAccum prod = (static_cast<AruAccum>(x) * coeff) >> ArithProfile::kCoeffShift;
    return aruSat16(acc + prod);
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
    int      coeff;    // signed 7-bit magnitude (-127..127)
    uint8_t  zero;     // clear accumulator before MAC
    uint8_t  xfer;     // load result register / write tank
    uint8_t  wa;       // write-register address (3 = pass-through)
    uint8_t  ra;       // read-register address (b5<<1 | b4)
    uint8_t  b3;       // RW/SRC (OPEN; recorded for parity, unused in first cut)
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

    // Instrumented twin for the diff harness. Records up to maxProbes per-step
    // probes (caller sizes the buffer); returns the per-sample energy in esumOut.
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
        pos_ = (pos_ + 1) & kDmemMask;
        int np = 0;
        int64_t esum = 0;
        AruWord lastRes = res_;
        for (int i = 0; i < nActive_; ++i) {
            const AruStep& st = steps_[i];
            const uint32_t addr = (pos_ - st.offset) & kDmemMask;
            AruWord dab;
            if (st.xfer) { dmem_[addr] = res_; dab = res_; }
            else         { dab = dmem_[addr]; }
            if (i == firstActive_) dab += in;     // additive input == reference at sample 0
            R_[st.wa] = dab;
            const AruWord raccIn = R_[st.ra];
            if (st.zero) acc_ = 0;
            const AruAccum prod = (static_cast<AruAccum>(raccIn) * st.coeff)
                                  >> ArithProfile::kCoeffShift;
            acc_ = aruSat16(acc_ + prod);
            int64_t resVal = kProbeResSentinel;
            if (st.xfer) {
                res_ = static_cast<AruWord>(aruSat16(acc_));
                esum += (res_ < 0) ? -res_ : res_;
                lastRes = res_;
                resVal = res_;
            }
            if (Trace && probes) {
                probes[np++] = Probe{ (int64_t)sampleIndex_, (int64_t)st.s, (int64_t)addr,
                                      (int64_t)dab, (int64_t)raccIn, (int64_t)prod,
                                      (int64_t)acc_, resVal };
            }
        }
        if (Trace) { if (nProbes) *nProbes = np; if (esumOut) *esumOut = esum; }
        ++sampleIndex_;
        return lastRes;   // first-cut audio proxy = last RES of the sample
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
