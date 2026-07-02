#pragma once
// =============================================================================
// sgdsp - Lexicon224XL - bit-exact 224XL ARU/T&C/DMEM core (integer, phys domain)
// =============================================================================
// C++ port of the pin-locked RTL engine tools/aru_freerun22_rtl.py (class RTL22,
// plan 021 Phase A / plan 024 F1 re-sync; sessions 0027/0028): the free-running
// ARU under the session-0022 coordinate system, the traced control-pipeline
// alignment (netlist 3.5-3.11, 2T, 4.7-4.9, 4F, 6D + fig-3.3/3.4), and the
// COMPLEMENT-DOMAIN physical MAC law locked per-pin by the 5.7 ARU signature
// tables (1467/1469 pins; feedback table 710/710).
//
// INTERNAL STATE IS PHYS (active-low DAB domain): the regfile R, delay memory
// DMEM, result register RES, DAB, and 20-bit accumulator ACC all carry the
// complemented patterns the hardware carries (CPU value = s16(~pattern) for the
// 16-bit buses; ACC has no CPU-domain value reading). CPU-domain boundaries:
//   RD-AD injects ~x;  WR-DA emits s16(~DAB);  WR XREG readback = ~DAB;  the
//   host->DSP latch XREG_host (CPU value) drives ~XREG_host onto the DAB;
//   unwritten DMEM reads phys 0xFFFF (= CPU 0).
//
// One frame = rows 0..L inclusive (L+1 steps; row r = CPU word 127-r; L = 128 -
// reset word); CPC += 1 per frame (16-bit wrap). Per step, in traced slot order:
//   slot-0 edge   operand SR loads regfile[RA(w_{n-1})] POST-write (write-
//                 through); the three RAW comb-array partial products of
//                 w_{n-1} are determined here (raw3, pairs A/B/C).
//   slot-1.43     ACC <- BE(ACC + ppB(w_{n-2}))       (sat-mux output loads, #35)
//   slot-3.06     XFER CK rise (owner w_{n-1}): RES <- (BE(. + ppC(w_{n-2})) >> 3)
//                 & 0xFFFF - the PP-bus tap, pairC included combinationally,
//                 PURE bit tap (no rounding hardware).
//   slot-4.43     ZERO/ (owner w_{n-1}) sync-clears ACC to phys 0, else the '163
//                 loads the SAME sat-mux output the capture read (own-sign
//                 schedule; the live-sign register variant is FALSIFIED, #23).
//   device phase  addr = CPC - stored offset; MEMR DOUT -> DAB; MEMW drives RES
//                 and latches DIN; IO drives per sel (RDRREG/XREG/RD-AD) else
//                 bus hold; WR-DA emits s16(~DAB) on the selected channels.
//   slot-7.43     ACC <- BE(. + ppA(w_{n-1})); regfile write R[WA(w_n)] <- DAB
//                 (every step); WR XREG readback captures ~DAB.
//   carry         pipe <- (rawB, rawC, cs) of w_{n-1} (pairs B/C retire next
//                 step under their OWN word's sign).
// BE = backend20: rail = cs_eff (= stored l2 bit7, 1 = positive), B = raw ^
// railmask, cin = 1-rail, 20-bit sum, SAT = s19^s18, clamp = topB ? 0xC0000 :
// 0x3FFFF; the clamp feeds BOTH the result path and the accumulator (#35).
//
// The decode is the session-0022 stored-word decode (tools/aru_freerun22.py
// decode22): 4 lanes through the Multibus data complement (lane 3 = ~l3 for
// XFER/ZERO/cmag), IO command bits assert when the STORED bit == 0, channels
// A..D = stored offset bits 11..8, sel = (~bits13..12) & 3, delay offset =
// stored value directly.
//
// This header is comment-mechanical by design: MEMR/MEMW taps and address
// regions are described as wired, with no speculative role labels. The law
// source is tools/aru_freerun22_rtl.py + docs/sessions/0027 (and the plan-024
// F1 re-sync); bit-exact parity vs that engine is proven by
// tools/harness/224xl (diff_harness + booth_vectors_test on RTL22-exported
// goldens). Everything below the process call is integer.

#include "../core/types.hpp"       // SampleRate
#include "../core/platform.hpp"    // SGDSP_INLINE, SGDSP_NOINLINE
#include "224xl_booth.hpp"         // gate-level comb array: raw3/loadSR/shiftRight2
#include <cstdint>

namespace sgdsp::reverb
{
using namespace core;

// 16-bit PHYS (active-low DAB-domain) pattern. DMEM is the hardware-fixed 64K
// ring of these; unwritten cells read phys 0xFFFF (= CPU 0).
using AruWord = uint16_t;

namespace aru224 {

inline constexpr uint32_t kMask20 = 0xFFFFFu;

// One traced back-end adder + sat-mux evaluation (phys domain; port of
// aru_freerun22_rtl.backend20, e1c champion convention):
//   rail = cs, B = raw ^ rail-mask (the sub-XOR row), cin = inv(rail),
//   20-bit sum (no wrap-out), SAT = sum19 ^ sum18,
//   clamp = topB ? 0xC0000 : 0x3FFFF (aru_U33-37 + U2; topB = B bit19).
// The RETURN VALUE feeds both the result path and the '163 accumulator D
// inputs (registry #35 - the clamp loads into ACC).
SGDSP_INLINE uint32_t backend20(uint32_t acc, uint32_t raw, uint32_t cs) noexcept
{
    const uint32_t xorb = raw ^ (cs ? kMask20 : 0u);
    const uint32_t ssum = (acc + xorb + (1u - cs)) & kMask20;
    if (((ssum >> 19) ^ (ssum >> 18)) & 1u)
        return ((xorb >> 19) & 1u) ? 0xC0000u : 0x3FFFFu;
    return ssum;
}

} // namespace aru224

// One decoded stored WCS word (session-0022 decode, tools/aru_freerun22.py
// decode22 + the precomputed effective sign of aru_freerun22_rtl.decode_word).
struct AruRow
{
    uint8_t  typ;       // stored l2 & 3: 0=MEMR 1=MEMW 2=IO 3=idle
    uint8_t  WA;        // (l2 >> 2) & 3, stored-direct
    uint8_t  RA;        // (l2 >> 4) & 3, stored-direct
    uint8_t  cs;        // effective coefficient sign = stored l2 bit 7 (1 = positive; E83 anchor)
    uint8_t  XFER;      // ~l3 bit 0
    uint8_t  ZERO;      // ~l3 bit 1
    uint8_t  cmag;      // (~l3 >> 2) & 0x3F
    uint16_t ofst;      // stored offset value DIRECTLY; addr = CPC - ofst
    // IO command fields (typ == 2 only; each asserts when the STORED bit == 0)
    uint8_t  RESET;     // stored ofst bit 3
    uint8_t  DP;        // bit 4
    uint8_t  TEST;      // bit 5
    uint8_t  WRX;       // bit 6 (WR XREG)
    uint8_t  WRDA;      // bit 7 (WR DA)
    uint8_t  chanMask;  // D/A channels, bit0=A..bit3=D = stored ofst bits 11..8
    uint8_t  sel;       // DAB source = (~bits13..12) & 3: 0=none 1=RDRREG 2=XREG 3=RD-AD
};

// Per-step probe for the traced twin: the phys state AFTER the step completes.
struct StepProbe
{
    int32_t  step;      // row index 0..L within the frame
    uint32_t acc;       // 20-bit phys accumulator pattern
    uint16_t res;       // phys result-register pattern
    uint16_t dab;       // phys DAB pattern
    uint16_t r[4];      // phys regfile patterns R0..R3
};

class Lexicon224XLCore
{
public:
    static constexpr uint32_t kDmemWords = 65536;   // hardware 64K ring
    static constexpr uint32_t kDmemMask  = 0xFFFFu;
    static constexpr int      kMaxRows   = 129;     // L <= 128 -> at most 129 rows
    // DAB source selects (decoded sel values)
    static constexpr uint8_t  kSrcNone = 0, kSrcRdRReg = 1, kSrcXreg = 2, kSrcRdAd = 3;

    // ---- lifecycle ----
    // dmem must point at kDmemWords AruWords; prepare() fills it with the phys
    // default 0xFFFF (CPU 0). sampleRate is informational (the hardware frame
    // rate is program-defined; see sampleRateHz()).
    SGDSP_NOINLINE void prepare(SampleRate sampleRate, AruWord* dmem) noexcept
    {
        sampleRate_ = sampleRate;
        dmem_ = dmem;
        reset();
    }

    // Decode a 128-word WCS image (4 stored bytes/word, CPU word order) and
    // extract the executed program (aru_freerun22_rtl.program_rows22): the
    // reset word = IO-typed with stored l0 bit3 == 0, w_reset = MAX such CPU
    // index; L = 128 - w_reset; physical row r = CPU word 127-r; the frame is
    // rows 0..L INCLUSIVE (L+1 steps - the pipeline's extra word executes).
    // Returns false (and disables the engine) if no reset word exists.
    // Ends in reset(): a program load is a fresh engine, like constructing a
    // fresh RTL22 in the Python reference.
    SGDSP_NOINLINE bool loadProgram(const uint8_t wcs[512]) noexcept
    {
        int wReset = -1;
        for (int k = 0; k < 128; ++k) {
            const uint8_t l0 = wcs[4 * k + 0];
            const uint8_t l2 = wcs[4 * k + 2];
            if ((l2 & 3) == 2 && ((l0 >> 3) & 1) == 0) wReset = k;   // keep the max
        }
        if (wReset < 0) { nRows_ = 0; wReset_ = -1; reset(); return false; }
        wReset_ = wReset;
        const int L = 128 - wReset;
        nRows_ = L + 1;
        for (int r = 0; r <= L; ++r) {
            const int k = (127 - r) & 0x7F;   // row r = CPU word 127-r (r=128 wraps to
                                              // word 127, mirroring Python wcs[-1])
            rows_[r] = decodeWord(&wcs[4 * k]);
        }
        reset();
        return true;
    }

    // Full engine reset to the RTL22 power-on state. Does NOT clear the
    // host->DSP latch XREG_host (it lives on the SBC side of the bridge; the
    // Python reference only zeroes it at construction - set it explicitly via
    // setXregHost() when needed).
    SGDSP_NOINLINE void reset() noexcept
    {
        for (auto& r : R_) r = 0xFFFF;              // phys ~0 (CPU 0 each)
        acc_ = 0;                                   // phys pattern (value -1 = cleared state)
        res_ = 0xFFFF;                              // phys ~0 (CPU 0)
        dab_ = 0xFFFF;                              // phys ~0 (CPU 0)
        cpc_ = 0;
        xregWr_ = 0;
        rdadN_ = 0;
        wp_ = nullptr;                              // no previous word yet
        pipeB_ = pipeC_ = aru224::kRawIdle;         // zero-rail baseline phases
        pipeCs_ = 1;
        stepCount_ = 0;
        frameCount_ = 0;
        if (dmem_)
            for (uint32_t i = 0; i < kDmemWords; ++i) dmem_[i] = 0xFFFF;
    }

    // ---- program facts ----
    int frameSteps() const noexcept { return nRows_; }              // = L + 1
    int resetWord() const noexcept { return wReset_; }
    double sampleRateHz() const noexcept                            // 30.72e6/9/(L+1)
    {
        return nRows_ > 0 ? 30.72e6 / 9.0 / static_cast<double>(nRows_) : 0.0;
    }
    const AruRow& row(int r) const noexcept { return rows_[r]; }

    // ---- host bridge ----
    // Host->DSP latch, CPU-domain value; drives ~XREG_host onto the DAB on
    // SRC_XREG reads (static 0 in free-run; the diag bench parks 0x607F).
    void setXregHost(uint16_t cpuValue) noexcept { xregHost_ = cpuValue; }
    uint16_t xregHost() const noexcept { return xregHost_; }
    // DSP->host latch readback, CPU-domain value (WR XREG complements back).
    uint16_t xregReadback() const noexcept { return xregWr_; }

    // ---- one frame = rows 0..L, then CPC += 1 ----
    // Stereo input (in_h1, in_h2): the FPC A/D mux alternates channel per
    // half-frame, so RD-AD steps in EXECUTION ORDER alternate halves - first
    // read -> half-1, second -> half-2; the counter resets each frame. Mono =
    // pass the same value for both halves. Only the low 16 bits are used.
    // out[0..3] = CPU-domain outputs for channels A..D this frame: last WR-DA
    // write wins; 0 if the channel was unwritten this frame (not held).
    SGDSP_INLINE void processFrame(int32_t in_h1, int32_t in_h2, int32_t out[4]) noexcept
    {
        frameImpl(in_h1, in_h2, out, nullptr);
    }

    // Traced twin: identical walk; additionally records probes[r] (r = 0..
    // frameSteps()-1) with the phys state after each step completes. `probes`
    // must have room for frameSteps() records.
    SGDSP_NOINLINE void processFrameTraced(int32_t in_h1, int32_t in_h2, int32_t out[4],
                                           StepProbe* probes) noexcept
    {
        frameImpl(in_h1, in_h2, out, probes);
    }

    // ---- decode (exposed for tests) ----
    static AruRow decodeWord(const uint8_t l[4]) noexcept
    {
        AruRow d{};
        const uint16_t ofst = static_cast<uint16_t>((l[1] << 8) | l[0]);
        const uint8_t  inv3 = static_cast<uint8_t>(~l[3]);
        d.typ  = l[2] & 3;
        d.WA   = (l[2] >> 2) & 3;
        d.RA   = (l[2] >> 4) & 3;
        d.cs   = (l[2] >> 7) & 1;                   // cs_eff = stored l2 bit 7 (1 = positive)
        d.XFER = inv3 & 1;
        d.ZERO = (inv3 >> 1) & 1;
        d.cmag = (inv3 >> 2) & 0x3F;
        d.ofst = ofst;
        if (d.typ == 2) {                           // IO command bits assert on stored == 0
            const auto bit = [ofst](int n) -> uint8_t {
                return static_cast<uint8_t>(((ofst >> n) & 1) == 0);
            };
            d.RESET = bit(3);
            d.DP    = bit(4);
            d.TEST  = bit(5);
            d.WRX   = bit(6);
            d.WRDA  = bit(7);
            d.chanMask = static_cast<uint8_t>((bit(11) << 0) |   // A = stored bit 11
                                              (bit(10) << 1) |   // B = bit 10
                                              (bit(9)  << 2) |   // C = bit 9
                                              (bit(8)  << 3));   // D = bit 8
            d.sel = static_cast<uint8_t>(((((~ofst) >> 13) & 1) << 1) | (((~ofst) >> 12) & 1));
        }
        return d;
    }

private:
    static SGDSP_INLINE int32_t s16(uint32_t v) noexcept    // signed 16-bit read of a pattern
    {
        return static_cast<int32_t>(static_cast<int16_t>(static_cast<uint16_t>(v)));
    }

    SGDSP_INLINE void frameImpl(int32_t in_h1, int32_t in_h2, int32_t out[4],
                                StepProbe* probes) noexcept
    {
        out[0] = out[1] = out[2] = out[3] = 0;      // unwritten channel -> 0 this frame
        if (nRows_ <= 0 || dmem_ == nullptr) return;
        const uint32_t h1 = static_cast<uint32_t>(in_h1) & 0xFFFFu;
        const uint32_t h2 = static_cast<uint32_t>(in_h2) & 0xFFFFu;
        rdadN_ = 0;                                 // new frame: A/D mux back to half-1
        for (int r = 0; r < nRows_; ++r) {
            stepRow(rows_[r], h1, h2, out);
            if (probes)
                probes[r] = StepProbe{ r, acc_, res_, dab_,
                                       { R_[0], R_[1], R_[2], R_[3] } };
        }
        cpc_ = (cpc_ + 1u) & 0xFFFFu;               // RESET/ event -> CPC +1 per frame
        ++frameCount_;
    }

    // One microinstruction (one WCS row), events in traced slot order - the
    // line-for-line port of RTL22.step (own-sign schedule; the falsified
    // csign_lag variant, dead-end #23, is intentionally not ported).
    SGDSP_INLINE void stepRow(const AruRow& d, uint32_t h1, uint32_t h2,
                              int32_t out[4]) noexcept
    {
        // slot-0 edge: operand SR loads regfile[RA(wp)] POST-write (write-
        // through); the three raw partial products of w_{n-1} are determined
        // here (pairs live AS0/1/2 this step).
        uint32_t rawA, rawB, rawC, csw;
        if (wp_ != nullptr) {
            aru224::raw3(R_[wp_->RA], wp_->cmag, rawA, rawB, rawC);
            csw = wp_->cs;
        } else {
            rawA = rawB = rawC = aru224::kRawIdle;  // power-on: zero-rail comb baseline
            csw = 1;
        }
        const uint32_t rawB2 = pipeB_, rawC2 = pipeC_;  // w_{n-2}'s pairs B/C retire
        const uint32_t cs2 = pipeCs_;                   // this step, OWN sign

        // slot-1.43 edge: ACC <- BE(ACC + ppB(w_{n-2})) - the sat-mux output loads (#35)
        const uint32_t sum0 = aru224::backend20(acc_, rawB2, cs2);

        // slot-3.06: XFER CK rise - result reg D = PP bus = BE(sum0 + ppC(w_{n-2})),
        // own sign; RES = PP3..18 pure bit tap (no rounding hardware; the rails
        // keep the tap wrap-free)
        const uint32_t sum1 = aru224::backend20(sum0, rawC2, cs2);
        if (wp_ != nullptr && wp_->XFER)
            res_ = static_cast<uint16_t>((sum1 >> 3) & 0xFFFFu);

        // slot-4.43 edge: sync clear (owner = wp) replaces the ppC(w_{n-2})
        // register load - the value already reached RES via the PP bus; else
        // the '163 loads the SAME sat-mux output the capture read.
        const uint32_t acc4 = (wp_ != nullptr && wp_->ZERO) ? 0u : sum1;

        // device phase for word w_n (stage-1 fields live all step); the DAB carries phys
        const uint16_t addr = static_cast<uint16_t>((cpc_ - d.ofst) & 0xFFFFu);
        switch (d.typ) {
        case 0:                                     // MEMR: DOUT -> DAB (~slot 7)
            dab_ = dmem_[addr];
            break;
        case 1:                                     // MEMW: RDRREG drives; DIN latches @slot4
            dab_ = res_;                            // (post-capture RES: capture was slot 3)
            dmem_[addr] = dab_;
            break;
        case 2: {                                   // IO: one driver per sel, else hold
            if (d.sel == kSrcRdRReg) {
                dab_ = res_;
            } else if (d.sel == kSrcRdAd) {
                const uint32_t ain = (rdadN_ & 1u) ? h2 : h1;   // A/D mux alternates halves
                ++rdadN_;
                dab_ = static_cast<uint16_t>(~ain & 0xFFFFu);   // the A/D drives the complement
            } else if (d.sel == kSrcXreg) {
                dab_ = static_cast<uint16_t>(~static_cast<uint32_t>(xregHost_) & 0xFFFFu);
            }
            if (d.WRDA) {                           // FPC captures the DAB at slot 5,
                const int32_t ov = s16(~static_cast<uint32_t>(dab_));  // complementing back
                for (int c = 0; c < 4; ++c)
                    if ((d.chanMask >> c) & 1) out[c] = ov;     // last write wins
            }
            break;
        }
        default:                                    // idle: bus hold
            break;
        }

        // slot-7.43 edge: ACC <- BE(acc4 + ppA(w_{n-1})); regfile write @MS7
        // (unconditional); WR XREG captures the DAB (readback complements back)
        acc_ = aru224::backend20(acc4, rawA, csw);
        R_[d.WA] = dab_;
        if (d.typ == 2 && d.WRX)
            xregWr_ = static_cast<uint16_t>(~static_cast<uint32_t>(dab_) & 0xFFFFu);

        // carry the pipeline: w_{n-1}'s pairs B/C retire next step under its own sign
        pipeB_ = rawB;
        pipeC_ = rawC;
        pipeCs_ = csw;
        wp_ = &d;                                   // d lives in rows_, stable across frames
        ++stepCount_;
    }

    // ---- state (phys patterns unless noted) ----
    uint16_t R_[4] = {0xFFFF, 0xFFFF, 0xFFFF, 0xFFFF};
    uint32_t acc_ = 0;                  // 20-bit phys accumulator pattern
    uint16_t res_ = 0xFFFF;
    uint16_t dab_ = 0xFFFF;
    uint32_t cpc_ = 0;                  // 16-bit frame counter
    uint16_t xregHost_ = 0;             // host->DSP latch (CPU-domain value)
    uint16_t xregWr_ = 0;               // DSP->host readback (CPU-domain value)
    uint32_t rdadN_ = 0;                // per-frame RD-AD occurrence counter
    const AruRow* wp_ = nullptr;        // w_{n-1}: gates this step's capture/clear
    uint32_t pipeB_ = aru224::kRawIdle; // (rawB, rawC, cs) of w_{n-2}
    uint32_t pipeC_ = aru224::kRawIdle;
    uint32_t pipeCs_ = 1;
    uint64_t stepCount_ = 0;
    uint64_t frameCount_ = 0;
    // program
    AruRow rows_[kMaxRows] = {};
    int    nRows_ = 0;                  // = L + 1 after a successful loadProgram
    int    wReset_ = -1;
    // external DMEM + rate
    AruWord*   dmem_ = nullptr;
    SampleRate sampleRate_ = 0;
};

using Lexicon224XL = Lexicon224XLCore;

} // namespace sgdsp::reverb
