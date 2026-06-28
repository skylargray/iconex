# sgdsp Processor Authoring Guide

How to write a new DSP processor using the sgdsp library patterns. The primary
reference is the production `Glay` modulated delay (`sgdsp::delay::GlayCore`,
[`delay/glay.hpp`](../../libs/sgdsp/include/sgdsp/delay/glay.hpp)) — the most
actively developed processor and the one shipping in the `glay` firmware app.
Simpler processors (`PitchDelay`, the CRTP filters) are used where a smaller
example is clearer.

This guide covers authoring the **processor** (the header-only sgdsp class). For
how an app *hosts* a processor on the Celeste platform runner — the
`app_init`/`app_audio`/`app_tick` hooks, memory placement, and knob wiring — see
the companion [Firmware App Integration Guide](firmware-app-integration-guide.md).

---

## File Anatomy

Every processor lives in a single header file under `libs/sgdsp/include/sgdsp/<module>/`. The file follows this structure:

```
#pragma once
// =============================================================================
// sgdsp - <Name> - <short description>
// =============================================================================
// Multi-line block comment explaining the algorithm, its math, and any
// non-obvious design decisions. This is the primary documentation.

#include "../core/types.hpp"      // Sample, SampleRate, etc.
#include "../core/platform.hpp"   // SGDSP_INLINE, SGDSP_DTCM, etc.
// ... other includes from sgdsp or <cmath>

namespace sgdsp::<module>
{
    using namespace core;   // brings in Sample, SampleRate, kPi, etc.

    class MyProcessor { ... };

} // namespace sgdsp::<module>
```

No `.cpp` files. Everything is header-only for inlining on the target.

---

## Two Processor Styles

### Style 1: CRTP (simple processors)

For processors with a straightforward `Sample in -> Sample out` interface, inherit from `Processor<Derived>`. This gives you free block processing, reset dispatch, and a uniform API.

```cpp
#include "../core/processor.hpp"

class MyFilter : public Processor<MyFilter>
{
public:
    void prepareImpl(SampleRate sampleRate) noexcept { ... }

    SGDSP_INLINE Sample processSampleImpl(Sample in) noexcept
    {
        // your per-sample DSP here
        return out;
    }

    void resetImpl() noexcept { state_ = 0.0f; }

private:
    float state_ = 0.0f;
};
```

The base class provides these public methods that dispatch to your `*Impl` versions:

| Base class method | You implement | Required? |
|---|---|---|
| `processSample(in)` | `processSampleImpl(in)` | **Yes** |
| `process(block)` | `processImpl(block)` | No (default loops over `processSampleImpl`) |
| `reset()` | `resetImpl()` | No (default is no-op) |
| `prepare(sr)` | `prepareImpl(sr)` | No (default is no-op) |

### Style 2: Standalone (complex processors)

For processors that need a non-standard interface (external buffers, a unified
mono/stereo entry point, multiple overloads, a write-only path), skip the CRTP
base and define the API directly. `Glay` uses this style — its public surface is
representative of a full effect:

```cpp
template <uint32_t MaxSamples, uint32_t Channels = 1>
class GlayCore
{
public:
    // prepare() takes one external delay buffer AND one pitch-shifter
    // workspace per channel — buffer SIZE is the MaxSamples template param,
    // not a runtime argument.
    void prepare(SampleRate sampleRate, Sample *channelBuffers[Channels],
                 float *pitchWorkspaces[Channels]) noexcept;
    void reset() noexcept;
    void clearDelay() noexcept;

    // Setters validate + precompute (see Parameters section)
    void setTime(float ms) noexcept;
    void setDepth(float depth) noexcept;
    void setType(float type) noexcept;
    // ... setSpeed, setFeedback, setTone, setMix, setPhaseOffset

    // Mono entry point (only enabled when Channels == 1)
    SGDSP_INLINE Sample processSample(Sample in) noexcept;
    // Stereo entry point — in-place (only enabled when Channels == 2)
    SGDSP_INLINE void process(Sample &inL, Sample &inR) noexcept;

private:
    // ...
};
```

Use standalone when:
- `prepare()` needs more than just `SampleRate` (e.g., external buffer pointers)
- The processor handles both mono and stereo from one template (see
  [Unified Mono/Stereo](#unified-monostereo-via-a-channels-parameter))
- You need multiple `process` overloads or a `write()`-only path — `PitchDelay`
  is a smaller standalone example with `process(in)`, `process(in, ratio)`, and
  a `write()`-only mode
- The class is a template with compile-time configuration

---

## Lifecycle Methods

Every processor follows the same lifecycle. Name and signature must match this pattern:

### `prepare(SampleRate sr, ...)` — called once before processing

- Store sample rate, compute derived coefficients, allocate/connect buffers
- Call `reset()` at the end to zero all state
- CRTP style: `void prepareImpl(SampleRate sampleRate) noexcept`
- Standalone style: `void prepare(SampleRate sr, ...) noexcept`

```cpp
// Size comes from the MaxSamples template param; the caller passes only a
// pointer to memory it owns (see External Buffers).
void prepare(SampleRate sr, Sample *buffer) noexcept
{
    sampleRate_ = static_cast<float>(sr);
    delayLine_.init(buffer, MaxSamples);
    updateAntiAliasFilter();
    reset();
}
```

### `reset()` — clear all internal state to zero

- Zero filter states, delay lines, phase accumulators
- Do NOT recalculate coefficients (that's `prepare`'s job)

```cpp
void reset() noexcept
{
    delayLine_.clear();
    antiAliasLpf_.reset();
    initHeadPhases();
}
```

### The per-sample hot path — name depends on style

There are three accepted forms; pick the one matching your style:

| Form | Signature | Used by |
|---|---|---|
| CRTP | `Sample processSampleImpl(Sample in) noexcept` (base exposes `processSample`) | CRTP filters, `Gain` |
| Standalone mono | `Sample processSample(Sample in) noexcept` | `Glay` (mono), `Gain` |
| Standalone stereo | `void process(Sample &inL, Sample &inR) noexcept` (in-place) | `Glay` (stereo) |

`PitchDelay` is the exception that names its mono path `process(Sample in)` and
adds overloads — fine for a standalone class, but **prefer `processSample` for a
single-sample mono entry point** so it reads the same as the CRTP base. Reserve
the bare `process(...)` name for block or in-place stereo processing.

All forms share these rules:

- Marked `SGDSP_INLINE` (force-inlined on all platforms)
- Mono returns `Sample`; in-place stereo returns `void` and writes through its references
- All math is `float`, no `double` promotion
- No branches in inner loops when possible (use branchless math or `if constexpr`)

---

## Parameters: Setters and Getters

Parameters follow a simple convention:

```cpp
// Setter: void set<Name>(<type>) noexcept
void setTime(float ms) noexcept { /* clamp + precompute, see below */ }
void setMix(float mix) noexcept { mix_ = math::clamp(mix, 0.0f, 1.0f); }

// Getter: <type> <name>() const noexcept
float time() const noexcept { return time_; }
```

Rules:
- Setters are `void`, `noexcept`, prefixed with `set`
- Getters are `const noexcept`, named after the parameter (no `get` prefix)
- Clamp/validate in the setter, not in `process()`
- Precompute derived values in the setter (a control-rate cost, not per-sample)

`Glay::setTime` clamps, converts ms → samples once, and leaves `process()` to
just read the result:

```cpp
void setTime(float ms) noexcept
{
    time_ = math::clamp(ms, 5.0f, 2000.0f);
    baseDelaySamples_ = time_ * 0.001f * sampleRate_;  // precompute samples
}
```

When a parameter feeds several derived coefficients, do the work in a private
`update*()` helper the setter calls — `Glay::setDepth` clamps `depth_`, derives a
noise-blend amount, then calls `updateDepthCoeffs()` to fold sample rate and the
depth curve into one cached multiplier:

```cpp
void setDepth(float depth) noexcept
{
    depth_ = math::clamp(depth, 0.0f, 1.0f);
    float noiseNormalized = std::max(0.0f, depth_ * 2.0f - 1.0f);
    noiseBlendAmt_ = (noiseNormalized > 0.0f)
                         ? (kBaselineNoiseBlend + noiseNormalized * (1.0f - kBaselineNoiseBlend))
                         : 0.0f;
    updateDepthCoeffs();  // precompute the rest at control rate
}
```

---

## Template Parameters

Use templates for compile-time configuration that affects the hot path. `Glay`
is parameterized on its buffer size and channel count:

```cpp
template <uint32_t MaxSamples, uint32_t Channels = 1>
class GlayCore { ... };
```

- Integer template params for buffer sizes, loop bounds, and channel count (the compiler unrolls them)
- Enum template params for algorithm selection (resolved with `if constexpr`)
- Prefer power-of-2 buffer sizes so a ring buffer's modulo becomes a bitwise AND
- Always provide sensible defaults (`Channels = 1`)

`if constexpr` eliminates dead code at compile time — no function pointers, no vtables:

```cpp
if constexpr (Interp == InterpMethod::None)
    val = delayLine_.read(static_cast<uint32_t>(offset));
else
    val = delayLine_.readLinear(offset);
```

### Unified Mono/Stereo via a Channels Parameter

A single class can serve both mono and stereo without runtime branching or code
duplication. `Glay` does this with a `Channels` template param and three
mechanisms:

**1. SFINAE selects the right process entry point.** Only one of these compiles
for a given `Channels`, so a `Glay<…, 1>` has *no* stereo method and vice-versa:

```cpp
// Mono — enabled only when Channels == 1
template <uint32_t C = Channels, std::enable_if_t<C == 1, int> = 0>
Sample processSample(Sample in) noexcept;

// Stereo — enabled only when Channels == 2, in-place
template <uint32_t C = Channels, std::enable_if_t<C == 2, int> = 0>
void process(Sample &inL, Sample &inR) noexcept;
```

**2. Per-channel state lives in `std::array<_, Channels>`.** One declaration
covers both configurations; loops over `Channels` collapse to straight-line code
when `Channels == 1`:

```cpp
std::array<float, Channels> ouState_{};
std::array<filter::OnePoleLowpass, Channels> ouLowpass_;
std::array<GlayChannel<MaxSamples>, Channels> channels_;
```

**3. `if constexpr` guards channel-specific setters.** Stereo-only parameters
still compile (and no-op) in a mono build, so callers don't need `#ifdef`s:

```cpp
void setPhaseOffset(float offset) noexcept
{
    if constexpr (Channels == 2)
        lfo_.setPhaseOffset(math::clamp(offset, 0.0f, 1.0f));
    // mono: compiles to nothing
}
```

Expose the common configurations as aliases so apps name the size, not the
template soup:

```cpp
template <uint32_t MaxSamples> using Glay       = GlayCore<MaxSamples, 1>;
template <uint32_t MaxSamples> using StereoGlay = GlayCore<MaxSamples, 2>;
using StereoGlay2s = StereoGlay<131072>;  // 2730 ms @ 48 kHz — used by the glay app
```

---

## Member Variable Layout

Group members by access frequency for cache performance. Comment the groups:

```cpp
private:
    // Group 1: Hot per-sample variables (touched every sample)
    float baseDelaySamples_ = 12000.0f;
    float smoothedBaseDelay_ = 12000.0f;
    float depthAmplitudeCoeff_ = 0.0f;

    // Group 2: Parameters (touched only in setters)
    float time_ = 250.0f;
    float depth_ = 0.5f;
    float mix_ = 0.5f;

    // Group 3: Sample-rate-derived values
    float sampleRate_ = 48000.0f;
    float invSampleRate_ = 1.0f / 48000.0f;

    // Group 4: Per-channel state — one array, sized by the template param
    std::array<float, Channels> ouState_{};
    std::array<noise::WhiteNoiseFast, Channels> noise_;

    // Group 5: Sub-components and channels
    std::array<GlayChannel<MaxSamples>, Channels> channels_;
    oscillator::StereoLFO lfo_;
    dynamics::L2Limiter<128> limiter_;
```

Rules:
- All members have default initializers (no uninitialized state)
- Use `float` for everything in the hot path (avoid `double`)
- Hold per-channel state in `std::array<_, Channels>`, never duplicated scalars
- Compile-time constants use `static constexpr`:

```cpp
static constexpr float kMaxDepthCents = 85.0f;
```

---

## Decomposing Complex Processors

When a processor has substantial DSP that is *duplicated per channel*, factor
that work into a per-channel struct and keep an orchestrator class on top. `Glay`
splits cleanly in two:

- **`GlayChannel<MaxSamples>`** — a `struct` (all members public) holding one
  channel's delay line, saturators, tone filter, pitch shifter, and feedback
  state, plus a `process(...)` that runs one sample through that channel.
- **`GlayCore<MaxSamples, Channels>`** — owns `std::array<GlayChannel, Channels>`
  plus the shared pieces (LFO, output limiter, modulation/crossfade state), holds
  all the parameter setters, and drives each channel from `processSample` /
  `process`.

```cpp
template <uint32_t MaxSamples>
struct GlayChannel               // per-channel DSP — public members, no setters
{
    DelayLineExternal delayLine;
    clip::GruTape tape;
    pitch::SpectralPitchShifter<11> pitchShifter;
    // ...
    void prepare(SampleRate sr, Sample *delayBuffer, float *pitchWorkspace, ...) noexcept;
    SGDSP_INLINE Sample process(Sample in, float feedbackAmt, float delaySamples, ...) noexcept;
};

template <uint32_t MaxSamples, uint32_t Channels = 1>
class GlayCore                   // orchestrator — owns channels + shared state + the API
{
    std::array<GlayChannel<MaxSamples>, Channels> channels_;
    oscillator::StereoLFO lfo_;
    dynamics::L2Limiter<128> limiter_;
    // setters / getters / processSample / process ...
};
```

Guidelines:
- The per-channel type is a plain `struct` — it is an implementation detail of
  the core, so skip getters/setters and let the orchestrator poke its fields.
- Parameters that are global to the effect (mix, feedback, LFO rate) live on the
  core; the core fans them out to each channel inside its setters (e.g.
  `setType` loops `for (auto &ch : channels_) ch.setType(type_)`).
- Keep the channel object self-contained per `prepare`/`reset` so the core just
  loops over `channels_` to forward lifecycle calls.
- The orchestrator still follows every rule above — this just nests one processor
  shape inside another.

---

## Composing with Existing Components

Reuse library primitives rather than reimplementing:

| Need | Use |
|---|---|
| Delay buffer (external memory) | `delay::DelayLineExternal` |
| Delay buffer (internal, fixed size) | `delay::DelayLine<MaxSamples>` |
| Fractional delay reads | `DelayLineExternal::readLinear()`, `readSinc16()` |
| Latency-match a dry path to a buffer's read latency | `delay::AlignmentDelay<MaxSamples>` |
| One-pole lowpass/highpass smoothing | `filter::OnePoleLowpass` / `OnePoleHighpass` |
| Biquad (designed LP/HP/BP/shelf, with Q) | `filter::Biquad` + `filter::BiquadDesign::lowpass(...)` etc. |
| Single LFO | `oscillator::LFO` |
| Dual-phase LFO (mono + stereo, phase offset) | `oscillator::StereoLFO` |
| White noise / RNG | `noise::WhiteNoiseFast` |
| Oversample a nonlinearity (anti-alias) | `resample::Oversampler8x` (+ `OversamplerDelayMatch` for the dry/bypass path) |
| BBD / bucket-brigade saturation | `clip::BBD…` (e.g. `BBDWDFLiteT8x`) |
| Tape-style hysteresis saturation | `clip::GruTape` |
| Per-sample / lookahead limiting | `dynamics::BrickwallLimiter`, `dynamics::L2Limiter<N>` |
| Spectral / phase-vocoder pitch shift | `pitch::SpectralPitchShifter<N>` (needs an external workspace — see below) |
| Math utilities | `math::clamp()`, `math::lerp()`, `math::fastTanh()`, `math::fastPow()` |
| Interpolation | `math::interpLinear()`, `math::interpCubic()` |

Sub-components follow the same lifecycle — call their `prepare`/`reset` from
yours. A few (the FFT-based `SpectralPitchShifter`) also need their own external
workspace passed through your `prepare()`; see the next section.

---

## External Buffers

For large memory (delay lines, FFT workspaces, reverb buffers), use pointer-based
external buffers so the caller controls memory placement. This keeps the processor
*object* small enough to live in DTCM while its large buffers sit in SDRAM or AXI
SRAM. Three rules make this work cleanly:

**1. Size is a template parameter, not a runtime argument.** Encode capacity in
the type so the compiler can turn ring-buffer modulo into a bitwise AND and so the
caller can size matching storage at compile time. `prepare()` then takes only a
*pointer*:

```cpp
template <uint32_t MaxSamples>
struct GlayChannel
{
    void prepare(SampleRate sr, Sample *delayBuffer, float *pitchWorkspace, ...) noexcept
    {
        delayLine.init(delayBuffer, MaxSamples);     // size from the template param
        pitchShifter.prepare(sr, pitchWorkspace);    // a second external buffer
    }
    DelayLineExternal delayLine;                      // small object — just a pointer + indices
    pitch::SpectralPitchShifter<11> pitchShifter;
};
```

**2. A processor may need more than one external buffer, of different classes.**
`Glay` needs both a delay line **and** an FFT workspace per channel, and they
belong in different memory regions (the delay line is big and latency-tolerant →
SDRAM; the FFT scratch is hot → AXI SRAM). Take one pointer per category, one
array slot per channel:

```cpp
template <uint32_t MaxSamples, uint32_t Channels = 1>
class GlayCore
{
public:
    void prepare(SampleRate sampleRate,
                 Sample *channelBuffers[Channels],     // delay line per channel
                 float  *pitchWorkspaces[Channels]) noexcept;
};
```

**3. Publish a static size helper for workspaces the caller can't size by hand.**
When the required size depends on internal compile-time config (FFT order, hop),
expose a `static constexpr` so the caller allocates exactly enough:

```cpp
using PitchShifter = sgdsp::pitch::SpectralPitchShifter<11>;
constexpr uint32_t kWorkspace = PitchShifter::workspaceSize();   // processor tells the caller
```

Usage by the caller (the `glay` app — see the
[Firmware App Integration Guide](firmware-app-integration-guide.md) for the
placement macros):

```cpp
SDRAM_BSS float delayBufferL[131072];                 // big + slow → SDRAM
SDRAM_BSS float delayBufferR[131072];
alignas(16) float pitchWorkspaceL[kWorkspace];        // hot scratch → AXI SRAM, 16-byte aligned
alignas(16) float pitchWorkspaceR[kWorkspace];

float *buffers[2] = {delayBufferL, delayBufferR};
float *pitchWs[2] = {pitchWorkspaceL, pitchWorkspaceR};
glay->prepare(48000, buffers, pitchWs);
```

The processor itself stays placement-agnostic — it never declares *where* its
buffers live, only that they exist. That decision belongs to the app.

---

## Inline, Performance, and Memory Placement

### Inline / exception annotations

| Macro | Meaning | When to use |
|---|---|---|
| `SGDSP_INLINE` | `__forceinline` / `__attribute__((always_inline))` | `process()` and any helper it calls |
| `SGDSP_NOINLINE` | Prevent inlining | `prepare()`, `reset()`, error paths |
| `noexcept` | Every method. No exceptions in embedded. | Always |

Mark `process()` and everything it calls as `SGDSP_INLINE`. Mark `prepare()` and `reset()` as regular (non-inline) — they run once, and inlining them wastes ITCM.

### Memory-placement macros

`core/platform.hpp` defines section macros for placing *storage* and *code* in
specific memory regions. They expand to nothing by default and are overridden by
the platform config (e.g. `config/sgdsp_daisy_seed2.hpp`), which must be included
**before** `sgdsp.hpp`.

| Macro | Region | Use for |
|---|---|---|
| `SGDSP_DTCM` | Tightly-coupled data RAM, 0-wait | Hot data touched every sample: filter state, coefficients, the processor object itself |
| `SGDSP_ITCM` | Tightly-coupled instruction RAM, 0-wait | Functions on the audio IRQ path (the app's audio callback, hot free functions) |
| `SGDSP_SDRAM` | External RAM, large but slow | Large delay lines / reverb buffers (>10 KB) |
| `SGDSP_AXI_RAM` | Internal RAM, moderate speed | General-purpose / FFT scratch |
| `SGDSP_HOT_DATA` | Alias of `SGDSP_DTCM` | Convenience for hot data |

**Who annotates what.** A processor normally stays placement-agnostic: it does
*not* tag its own members with these macros — it exposes external buffers
(above) and is small enough that the *app* drops the whole object into DTCM via a
placement-`new` over an `SGDSP_DTCM` byte array. The app owns placement; the
processor owns behavior. The one thing an author commonly tags directly is a free
function that runs on the audio path (`SGDSP_ITCM`). Note the `glay` app also uses
its own `SDRAM_BSS` attribute for the delay buffers — that's an *app-level* macro,
not the library's `SGDSP_SDRAM`. See the
[Firmware App Integration Guide](firmware-app-integration-guide.md) for the full
placement story.

---

## Type Aliases from `core/types.hpp`

| Type | Definition | Use for |
|---|---|---|
| `Sample` | `float` (default) | Audio sample values |
| `SampleRate` | `uint32_t` | Sample rate in Hz |
| `BlockSize` | `uint16_t` | Block/buffer sizes |
| `kPi`, `kTwoPi` | `constexpr float` | Math constants |

Always `using namespace core;` inside your namespace to access these without prefix.

---

## Checklist for a New Processor

1. **Header file** in the right module directory (`delay/`, `filter/`, `clip/`, etc.)
2. **`#pragma once`** and banner comment with algorithm description
3. **Includes**: `types.hpp`, `platform.hpp`, plus whatever you compose with
4. **Namespace**: `sgdsp::<module>`
5. **Class**: CRTP or standalone depending on interface complexity
6. **Template params**: buffer size + `Channels` if mono/stereo unified; power-of-2 sizes
7. **`prepare()`**: store sample rate, connect external buffers, init sub-components, call `reset()`
8. **`reset()`**: zero all state, clear sub-components
9. **Hot path**: `SGDSP_INLINE`, pure `float` math — `processSample(in)` (mono) and/or in-place `process(inL, inR)` (stereo)
10. **Setters**: validate + precompute, `noexcept`
11. **Getters**: `const noexcept`, no `get` prefix
12. **Members**: grouped by access frequency, all default-initialized; per-channel state in `std::array<_, Channels>`
13. **Decompose** per-channel DSP into a sub-struct when serving multiple channels
14. **Constants**: `static constexpr` for compile-time values
15. **External buffers**: pointer-in via `prepare()`, sized by template param; publish a `workspaceSize()` helper if the caller can't size it
16. **Integrate**: wire the processor into an app — see the [Firmware App Integration Guide](firmware-app-integration-guide.md)

---

## Complete Minimal Example

A simple gain processor using the CRTP pattern:

```cpp
#pragma once
// =============================================================================
// sgdsp - Gain
// =============================================================================
// Simple gain stage with smoothing.

#include "../core/types.hpp"
#include "../core/platform.hpp"
#include "../core/processor.hpp"
#include "../filter/onepole.hpp"

namespace sgdsp::dynamics
{

using namespace core;

class Gain : public Processor<Gain>
{
public:
    void prepareImpl(SampleRate sampleRate) noexcept
    {
        smoother_.setTimeConstant(5.0f, static_cast<float>(sampleRate));
    }

    void setGain(float linear) noexcept { targetGain_ = linear; }
    float gain() const noexcept { return targetGain_; }

    SGDSP_INLINE Sample processSampleImpl(Sample in) noexcept
    {
        float g = smoother_.processSample(targetGain_);
        return in * g;
    }

    void resetImpl() noexcept
    {
        smoother_.resetTo(targetGain_);
    }

private:
    float targetGain_ = 1.0f;
    filter::OnePoleLowpass smoother_;
};

} // namespace sgdsp::dynamics
```
