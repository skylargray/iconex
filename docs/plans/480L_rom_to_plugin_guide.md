# Lexicon 480L → Portable Reverb Processor

**From ROM dumps to a single header-only core that runs as STM32 firmware (via `sgdsp`) and as a DPF VST3/AU plugin.**

This guide assumes you have reached — or are reaching — a full algorithmic understanding of the 480L reverb (delay-line topology, allpass/comb structure, coefficient tables, and the modulation/animation engine) from your ROM-reversing work. It covers the path from that understanding to runnable, parameter-adjustable code on two very different targets without maintaining two codebases.

It refers throughout to your **`sgdsp` Processor Authoring Guide** (the conventions doc) and its companion **Firmware App Integration Guide**. Where a claim depends on an `sgdsp` detail this guide can't see (your exact `Sample` typedef, the `SGDSP_*` macro expansions, the ARU's interpolation behavior, the native sample rate), it is flagged `[CONFIRM]`.

---

## 0. The one architectural decision everything else follows from

Author **one header-only C++17 class** with an **integer (fixed-point) datapath** and a **float boundary**. That single header is consumed, unchanged, by three things:

| Consumer | Entry used | Numeric boundary | Purpose |
|---|---|---|---|
| Emulator-diff **harness** | `processSampleFixed()` (integer) | integer → integer, **exact** | Bit-exact validation against the ROM emulator |
| **DPF** plugin (`run()`) | `processSample()` / `process()` (float) | float → fixed → float | Desktop tweaking, listening, VST3/AU/CLAP delivery |
| **`sgdsp`** on Seed2 (audio callback) | `processSample()` / `process()` (float) | float → fixed → float | On-device firmware |

Two consequences make this work:

1. **Integer datapath, not float.** The 480L's character lives in the 18-bit ARU arithmetic — the coefficient quantization (magnitude `>>2` → ones-complement → field; sign on a separate microword bit), the accumulator width, and the multi-rate coefficient ramping. Reproduce that datapath in integers and you can assert **exact equality** against an instrumented emulator. Use float anywhere in the datapath and you forfeit that — float would merely approximate the integer machine and you'd lose the single most powerful validation tool you have. The Seed2's FPU does not change this: the M7 runs integer MACs fine (it has the DSP-extension instructions), so there is no performance reason to go float.
2. **The float boundary is identical for DPF and `sgdsp`.** Both hosts hand you float `±1.0`. Both wrappers do the same thing: convert float → 18-bit fixed on input, run the integer network, convert fixed → float on output. So the DPF wrapper and the `sgdsp` wrapper are structurally the same; only the harness is pure-integer (it skips even the boundary conversion and feeds the integer entry point directly).

```
            ┌────────────────────────────────────────────┐
            │     l480_core.hpp   (header-only, C++17)     │
            │  ── integer ARU datapath ──                  │
            │  processSampleFixed(int32 in) → int32        │  ← harness calls this (exact)
            │  processSample(Sample in)     → Sample       │  ← float wrapper (DPF + sgdsp)
            │  process(Sample in, &outL, &outR)            │
            └────────────────────────────────────────────┘
                 ▲                  ▲                  ▲
        emulator-diff harness   DPF Plugin::run()   sgdsp audio callback
        (int → int, exact)      (float boundary)    (float boundary, Seed2)
```

---

## Phase A — Turn the ROMs into an executable specification

Your golden reference is **not** a hardware unit and **not** a from-memory numpy model — it's the **dumped ROMs running in your emulator**. That is strictly better than a hardware reference, because an emulator exposes *internal* state, not just output audio. Exploit that.

### A.1 Establish the emulator as the reference

The reverb algorithm *is* the microcode plus the ARU datapath behavior. Your reimplementation goal is: given the same input samples and the same coefficient/microword stream, produce the same internal values and the same output, sample for sample. The emulator defines "the same."

### A.2 Instrument the emulator with probe points

Add logging hooks at the points where your C++ core will also have well-defined values, so you can diff at each stage rather than only at the output. Minimum useful probe set:

- **Post-coefficient-decode** — the integer coefficient actually applied this sample (after `>>2`/ones-complement/sign reconstruction). Catches encode/decode bugs at the source.
- **Post-MAC / accumulator** — the accumulator value before truncation/rounding back to sample width. Catches accumulator-width and rounding-mode bugs.
- **Delay-line read and write** — address and value for each tap read and each write. Catches ring-buffer indexing and (if any) interpolation bugs.
- **Modulation/animation step** — each `{WCS-addr, value}` update and the current ramp rate. Catches de-zippering/rate bugs.
- **Output** — the final per-channel integer sample.

Emit these as a deterministic per-sample trace (one record per sample, fixed field order). This trace file is your **golden trace**.

### A.3 Define test vectors

Drive the emulator (and later your core) with a small, fixed battery:

- **Unit impulse** → the integer impulse response; the most diagnostic single test.
- **Log sweep** → reveals frequency-dependent structure and modulation sidebands.
- **Parameter sweeps** → for each named parameter, step across its range and capture a trace per setting. This both validates and documents the parameter→coefficient mapping.
- **Silence with non-zero initial state** (if reachable) → checks `reset()` correctness.

Keep these vectors and their golden traces under version control; they are the regression suite for the entire project.

### A.4 Extract the structure (reference your established findings)

From the traces and your disassembly, write down — as a short, confidence-tagged spec — the things the core must reproduce:

- **Delay topology**: tap list, delay lengths (in samples at the native rate), routing into allpass/comb stages.
- **Allpass / comb structure**: which stages, their coefficients, nesting.
- **Coefficient tables**: the parameter→coefficient maps, sourced *from the ROM/emulator*, never hand-transcribed (see §F.3).
- **Coefficient encode/decode**: magnitude `>>2` → ones-complement → 3/4-bit field; sign routed to a separate microword control bit (your PCM70 Phase 2 finding — treat as authoritative).
- **Modulation/animation**: the `{WCS-addr, value}` walker stepping at two rates (−4 / −1 per pass) — multi-rate ramping/de-zippering by design.
- **Sample word format**: bit width (18), fractional convention, accumulator width, rounding/truncation rule. `[CONFIRM]` the exact fractional convention against the service manual / emulator.

Output of Phase A: a written datapath spec + golden traces. You are now ready to write code with an exact target.

---

## Phase B — Author the header-only core (`l480_core.hpp`)

Follow your authoring guide's conventions exactly so the same file is a first-class `sgdsp` processor. The only departure from a typical `sgdsp` processor is that the *internal* arithmetic is integer; the public surface stays float as the guide expects.

### B.1 File anatomy (per the authoring guide)

`#pragma once`, banner comment describing the algorithm, include `core/types.hpp` and `core/platform.hpp`, namespace `sgdsp::reverb`, `using namespace core;`. No `.cpp`. (Authoring guide → *File Anatomy*.)

### B.2 Use Standalone style, not CRTP

A reverb's natural entry is **mono-in / stereo-out** (and optionally stereo-in/stereo-out), which is neither the CRTP `Sample → Sample` nor the in-place `process(inL,inR)`. Your guide explicitly permits custom `process` overloads for standalone classes (the `PitchDelay` precedent), so a `void process(Sample in, Sample& outL, Sample& outR)` entry is in-contract. (Authoring guide → *Two Processor Styles* / *The per-sample hot path*.)

### B.3 Fixed-point types

Define the ARU word and accumulator explicitly. `[CONFIRM]` widths and the fractional point against your Phase-A spec.

```cpp
// 18-bit signed sample, carried in int32 (sign-extended). Accumulator is int64.
using AruSample = int32_t;   // valid range roughly ±2^17
using AruAccum  = int64_t;

static constexpr int  kAruBits  = 18;
static constexpr int  kAruFrac  = 17;                 // [CONFIRM] fractional bits
static constexpr AruSample kAruMax =  (1 << (kAruBits - 1)) - 1;
static constexpr AruSample kAruMin = -(1 << (kAruBits - 1));

// Boundary conversions (the ONLY float<->fixed in the signal path).
SGDSP_INLINE AruSample floatToAru(Sample x) noexcept {
    float s = x * float(1 << kAruFrac);
    if (s >  float(kAruMax)) s = float(kAruMax);
    if (s <  float(kAruMin)) s = float(kAruMin);
    return AruSample(s);                              // [CONFIRM] round vs truncate to match codec path
}
SGDSP_INLINE Sample aruToFloat(AruSample v) noexcept {
    return Sample(v) * (1.0f / float(1 << kAruFrac));
}
```

Any 18-bit integer is exactly representable in `float32` (24-bit mantissa), so the *storage* round-trip is lossless; only the host's own float processing outside your plugin introduces float error, which is irrelevant to internal fidelity.

### B.4 Integer datapath primitives — roll your own; do **not** reuse `sgdsp`'s float ones

This is the one hard rule that protects bit-exactness. `sgdsp::delay::DelayLineExternal::readLinear()` and the other library primitives are **float** — using them in the bit-exact network would make your output a float approximation of the emulator, breaking exact-equality testing. Write integer equivalents:

- **Integer ring buffer** over an external `AruSample*`, size a power-of-two template param so modulo becomes a bitwise AND (the guide's *External Buffers* rule, just typed `AruSample*` instead of `Sample*`).
- **Integer allpass / comb** stages using `AruAccum` MACs and the ARU's exact truncation/rounding.
- **Integer interpolation** *only if the ARU does it*, matching its exact method `[CONFIRM]`. If the ARU reads integer taps with modulation applied some other way, replicate that instead.
- **Coefficient decode** exactly as Phase A specifies (`>>2`/ones-complement/sign bit).
- **Animation engine**: the `{WCS-addr, value}` walker with the −4/−1 multi-rate ramp.

You keep the `sgdsp` external-buffer *pattern* (size = template param, pointer passed into `prepare()`, app owns placement); you just don't borrow its float DSP. You *may* still compose with `sgdsp` for anything outside the bit-exact path, but in practice the 480L applies its own de-zippering, so apply parameters through the ARU animation engine rather than an `sgdsp` smoother — otherwise the smoothing itself diverges from the emulator.

### B.5 Lifecycle, parameters, dual entry points

Match the guide's lifecycle and naming. Add the integer entry the harness needs, with the float entries as thin wrappers.

```cpp
#pragma once
// =============================================================================
// sgdsp - Lexicon480 - bit-exact 480L ARU reverb reconstruction (integer datapath)
// =============================================================================
// Reproduces the discrete-ARU 18-bit datapath: delay network + allpass/comb
// stages, ROM-sourced coefficient tables, and the {WCS-addr, value} multi-rate
// animation engine. Float only at the I/O boundary.

#include "../core/types.hpp"       // Sample, SampleRate
#include "../core/platform.hpp"    // SGDSP_INLINE, placement macros (no-op off-target)

namespace sgdsp::reverb
{
using namespace core;

template <uint32_t MaxSamples, uint32_t Channels = 2>
class Lexicon480Core
{
public:
    // sgdsp External-Buffers pattern, but typed AruSample* (ARU words), not Sample*.
    // Size is the MaxSamples template param; caller passes app-placed pointers.
    void prepare(SampleRate sampleRate, AruSample* delayBuffers[Channels]) noexcept;
    void reset() noexcept;

    // Named parameters (from lexicon_480L_named_parameters.md). Setters clamp +
    // precompute at control rate, per the guide's Parameters section.
    void  setDecay(float seconds) noexcept;
    float decay() const noexcept { return decay_; }
    void  setPreDelay(float ms) noexcept;
    void  setSize(float size) noexcept;
    // ... one setter/getter per named parameter

    // ---- Float surface: used by DPF run() and the sgdsp audio callback ----
    SGDSP_INLINE void process(Sample in, Sample& outL, Sample& outR) noexcept
    {
        AruSample l, r;
        processFixed(floatToAru(in), l, r);
        outL = aruToFloat(l);
        outR = aruToFloat(r);
    }

    // ---- Integer surface: used by the emulator-diff harness (bit-exact) ----
    SGDSP_INLINE void processFixed(AruSample in, AruSample& outL, AruSample& outR) noexcept;

private:
    // Group 1: hot per-sample state   (DTCM when the app places the object there)
    // Group 2: parameters             (touched only in setters)
    // Group 3: sample-rate-derived
    // Group 4: per-channel state in std::array<_, Channels>
    // Group 5: integer sub-components (ring buffers, allpass, comb, animation walker)
    float decay_ = 2.0f;
    float sampleRate_ = 0.0f;   // [CONFIRM] must equal the ARU native rate
    // ...
};

// Aliases so apps name the size, not the template soup (guide's pattern).
template <uint32_t N> using Lexicon480     = Lexicon480Core<N, 2>;
template <uint32_t N> using Lexicon480Mono = Lexicon480Core<N, 1>;
} // namespace sgdsp::reverb
```

Key conformance points, each tied to your guide:

- **`prepare(SampleRate, …)`** stores the rate, connects external buffers, inits sub-components, calls `reset()` at the end. (*Lifecycle Methods*.)
- **`reset()`** zeroes state only; never recomputes coefficients. (*Lifecycle Methods*.)
- **Setters** are `void … set<Name>(<type>) noexcept`, clamp + precompute; **getters** are `<type> <name>() const noexcept`, no `get` prefix. (*Parameters*.)
- **Hot path** marked `SGDSP_INLINE`, `noexcept`, no exceptions. (*Inline / exception annotations*.) Note the inner math is integer, not float — this is the one place you diverge from the guide's "all `float`" rule, by design, and it's confined to the datapath.
- **External buffers** sized by `MaxSamples`, pointer-in, app owns placement; publish a size helper if a sub-component's workspace can't be sized by hand. (*External Buffers*.)
- **Placement-agnostic**: the object tags none of its own members with `SGDSP_*`; the app drops the object into DTCM and the buffers into SDRAM. (*Inline, Performance, and Memory Placement*.)
- **Native sample rate**: delay lengths are integers of samples, so bit-exactness only holds when the core runs at the ARU native rate. Any rate conversion is a wrapper concern (§D.3, §E.6). `[CONFIRM]` the native rate.

---

## Phase C — The bit-exact validation harness (do this before any plugin)

This is where "rapid development" actually comes from. The harness is a tiny desktop program that includes the same header and proves it against the golden traces.

### C.1 Desktop compile of the core

The header rides on `core/types.hpp` and `core/platform.hpp`. Per your guide, the placement/inline macros "expand to nothing by default" and are only overridden by a platform config (`config/sgdsp_daisy_seed2.hpp`). So on desktop:

- Put `sgdsp`'s **portable** include dir on the path.
- **Do not** include the Daisy platform config or anything that pulls in CMSIS / STM32 HAL.
- `SGDSP_INLINE` → `inline` (or `[[gnu::always_inline]]`), `SGDSP_DTCM`/`SGDSP_SDRAM` → nothing. `[CONFIRM]` that your default `platform.hpp` already yields these no-ops off-target; if it `#error`s without a platform, add a trivial `sgdsp_desktop.hpp` that defines the macros as no-ops and `Sample`/`SampleRate` as on-target.

### C.2 Diff loop

```cpp
// harness.cpp  (desktop)
#include "sgdsp/reverb/l480_core.hpp"
// 1. load golden trace + input vector produced by the instrumented emulator
// 2. construct Lexicon480Core, prepare() at the NATIVE rate, set params to the
//    trace's parameter settings
// 3. for each input sample: call processFixed(); compare against the trace at
//    every probe point (post-decode, post-MAC, delay r/w, output)
// 4. assert exact integer equality; on mismatch, print sample index + stage
```

Because both sides are integer, equality is exact — the first mismatch points at the exact sample and stage that diverged. Iterate the core until every vector passes.

### C.3 Listening / IR harness

Add a second tiny tool: WAV in → `process()` (float) → WAV out, plus an impulse mode that dumps the IR. This is for ears and for spectrogram/EDC comparison; the integer harness is for correctness. Both include the same header.

---

## Phase D — Wrap the core in `sgdsp` for the Seed2 firmware

The core already *is* an `sgdsp` processor, so there is no adapter to write — only an app to host it. Follow the **Firmware App Integration Guide** for the `app_init` / `app_audio` / `app_tick` hooks and knob wiring; the essentials:

### D.1 Memory placement (app's job, not the core's)

- The **object** is small (pointers + indices + state) → place it in **DTCM** via placement-`new` over an `SGDSP_DTCM` byte array, per the guide.
- The **delay buffers** are large → place in **SDRAM** with your app-level `SDRAM_BSS` attribute (the guide notes the `glay` app does exactly this), typed `AruSample`:

```cpp
SDRAM_BSS AruSample delayL[kMaxSamples];
SDRAM_BSS AruSample delayR[kMaxSamples];
AruSample* buffers[2] = { delayL, delayR };
core->prepare(kAruNativeRate, buffers);
```

SDRAM is external (FMC) and higher-latency than DTCM/AXI-SRAM, so keep the hot per-sample state and the small coefficient tables internal (they already live in the DTCM-placed object) and let only the bulk delay memory sit in SDRAM. Enable the M7 D-cache for the SDRAM region. With 64 MB of SDRAM, capacity is a non-issue — size the buffers to the longest delay you need and stop worrying about the budget.

### D.2 Audio callback

In `app_audio`, convert the codec's float frames and call the float entry:

```cpp
for (size_t i = 0; i < n; ++i)
    core->process(in[i], outL[i], outR[i]);   // float in -> Q18 -> integer net -> float out
```

### D.3 Sample rate

For bit-exactness the core must run at the ARU native rate `[CONFIRM]`. Either configure the PCM3060 to that rate, or resample at the callback boundary (codec rate ↔ native rate) — a wrapper concern that never touches the datapath. If you run the codec at the native rate directly, there's no resampling at all.

Same header, zero divergence from the desktop build.

---

## Phase E — Wrap the core in DPF for VST3 and AU

All DPF facts below are verified against DPF's current `Makefile.plugins.mk` and macro docs.

### E.1 Project layout

```
l480-plugin/
├── dpf/                      (git submodule: https://github.com/DISTRHO/DPF)
├── sgdsp/                    (your library — submodule or include path)
└── plugins/
    └── Lexicon480/
        ├── DistrhoPluginInfo.h
        ├── Lexicon480Plugin.cpp
        └── Makefile
```

Add DPF as a submodule: `git submodule add https://github.com/DISTRHO/DPF dpf`.

### E.2 Bring the core in — and keep STM headers out

The plugin includes the **same** `l480_core.hpp`. On the DPF build you must:

- Add `sgdsp`'s portable include dir to the compiler include path (§E.5).
- **Never** include `config/sgdsp_daisy_seed2.hpp` or any CMSIS/STM header. The macros default to no-ops, so the integer core compiles as plain C++17 on desktop.

No code is duplicated — the single header is the only DSP source you author; the rest is DPF glue.

### E.3 `DistrhoPluginInfo.h`

Headless (no GUI) means **`DISTRHO_PLUGIN_HAS_UI 0`** and providing no UI sources — DPF then sets `HAVE_DGL = false` automatically and the host shows its generic parameter panel. AU and CLAP need unique identifiers; these are the macros that matter:

```cpp
#pragma once

#define DISTRHO_PLUGIN_NAME        "Lexicon480"
#define DISTRHO_PLUGIN_URI         "https://your.domain/l480"

#define DISTRHO_PLUGIN_NUM_INPUTS  1     // mono in (reverb); use 2 for stereo-in
#define DISTRHO_PLUGIN_NUM_OUTPUTS 2     // stereo out
#define DISTRHO_PLUGIN_HAS_UI      0     // headless — host provides generic knobs
#define DISTRHO_PLUGIN_IS_RT_SAFE  1

// Identifiers — REQUIRED for AUv2 and CLAP:
#define DISTRHO_PLUGIN_UNIQUE_ID   'L480'   // 4-char, unique within your brand (AUv2 subtype)
#define DISTRHO_PLUGIN_BRAND_ID    'Skyl'   // 4-char manufacturer, >=1 non-lowercase
#define DISTRHO_PLUGIN_CLAP_ID     "skylar.lexicon480"
// DISTRHO_PLUGIN_AU_TYPE is auto-set by DPF (an effect resolves to 'aufx').

enum Parameters {
    kParamDecay = 0,
    kParamPreDelay,
    kParamSize,
    // ... one per named 480L parameter
    kParameterCount
};
```

Expose the **named** 480L parameters here (from `lexicon_480L_named_parameters.md`) as host-automatable parameters. Keep raw per-coefficient / WCS-address poking out of the host parameter list — route that through a loadable preset/state blob or a debug build, or the generic editor becomes unusable with hundreds of entries.

### E.4 The `Plugin` subclass (headless)

Subclass `DISTRHO::Plugin`, hold one `Lexicon480Core`, and map DPF's calls onto the core. Outline:

```cpp
#include "DistrhoPlugin.hpp"
#include "sgdsp/reverb/l480_core.hpp"
START_NAMESPACE_DISTRHO

class Lexicon480Plugin : public Plugin {
public:
    Lexicon480Plugin() : Plugin(kParameterCount, 0, 0) {}   // params, programs, states

protected:
    const char* getLabel()     const override { return "Lexicon480"; }
    const char* getMaker()     const override { return "Skylar"; }
    const char* getLicense()   const override { return "ISC"; }
    uint32_t    getVersion()   const override { return d_version(1,0,0); }
    int64_t     getUniqueId()  const override { return d_cconst('L','4','8','0'); }

    void initParameter(uint32_t index, Parameter& p) override {
        p.hints = kParameterIsAutomatable;
        switch (index) {
            case kParamDecay:
                p.name = "Decay"; p.symbol = "decay";
                p.ranges.min = 0.1f; p.ranges.max = 30.0f; p.ranges.def = 2.0f;
                break;
            // ... ranges/names/defaults per named parameter
        }
    }

    float getParameterValue(uint32_t index) const override {
        switch (index) { case kParamDecay: return core_.decay(); /* ... */ }
        return 0.0f;
    }
    void setParameterValue(uint32_t index, float v) override {
        switch (index) { case kParamDecay: core_.setDecay(v); break; /* ... */ }
    }

    void activate() override {
        // host rate may differ from the ARU native rate — see E.6
        core_.prepare(getSampleRate() /* or native rate + resampler */, buffers_);
    }

    void run(const float** inputs, float** outputs, uint32_t frames) override {
        const float* in = inputs[0];
        float* outL = outputs[0];
        float* outR = outputs[1];
        for (uint32_t i = 0; i < frames; ++i)
            core_.process(in[i], outL[i], outR[i]);   // same float entry as sgdsp
    }

private:
    static constexpr uint32_t kMax = 131072;          // power-of-two
    sgdsp::reverb::Lexicon480Core<kMax, 2> core_;
    AruSample bufL_[kMax], bufR_[kMax];                // desktop: just static/heap; macros no-op
    AruSample* buffers_[2] = { bufL_, bufR_ };
};

Plugin* createPlugin() { return new Lexicon480Plugin(); }
END_NAMESPACE_DISTRHO
```

On desktop the placement macros are no-ops, so the buffers are ordinary memory — no DTCM/SDRAM concerns. The `process()` call is byte-identical to the Seed2 callback.

### E.5 The `Makefile`

DPF builds whatever formats you list by **overriding the `all:` target** after including `Makefile.plugins.mk`. Empty `FILES_UI` ⇒ headless. Add the `sgdsp` include path so the core resolves.

```makefile
#!/usr/bin/make -f
NAME = Lexicon480
FILES_DSP = Lexicon480Plugin.cpp
# (no FILES_UI -> DPF sets HAVE_DGL=false, builds DSP-only/headless)

include ../../dpf/Makefile.plugins.mk

# make the header-only core + sgdsp portable headers visible
BUILD_CXX_FLAGS += -I../../sgdsp/include -std=gnu++17

# choose formats: VST3 + AU + CLAP, plus a JACK standalone for quick testing
all: vst3 au clap jack
```

Notes:
- The format target names (`vst3`, `au`, `clap`, `jack`, `lv2`/`lv2_sep`, `vst2`, `ladspa`, `dssi`) come straight from DPF's makefile. The header comment in `Makefile.plugins.mk` documents this exact override pattern.
- `au` is **macOS-only** in DPF (guarded by `ifeq ($(MACOS),true)`); on Linux/Windows it's silently unavailable, so a portable `all:` can be `vst3 clap jack` off-mac and add `au` on mac.

### E.6 Sample-rate handling in the plugin

The host runs at 44.1/48/96 kHz; the core must run at the ARU native rate `[CONFIRM]` for bit-exactness. Two options:
- **Resample at the boundary**: host rate → native rate before `process()`, native → host after. The reverb stays bit-exact; only the resampler is approximate, and it's outside the validated datapath.
- **Run the whole plugin at the native rate** if you don't care about matching the host's rate internally (simpler, but the host still resamples around you).
Either way, `activate()` is where you decide and wire it; the core itself is always told its true operating rate.

### E.7 Build, install, validate

```bash
make                      # outputs land in ./bin/
```

Produces (on macOS): `bin/Lexicon480.vst3`, `bin/Lexicon480.component` (AU), `bin/Lexicon480.clap`. DPF auto-generates the AU's `Contents/Info.plist` via its export tool and links the AU against `AudioToolbox`/`AudioUnit`/`CoreFoundation` for you — nothing to hand-write.

Install (macOS, per-user):
```bash
cp -r bin/Lexicon480.vst3      ~/Library/Audio/Plug-Ins/VST3/
cp -r bin/Lexicon480.component ~/Library/Audio/Plug-Ins/Components/
```

Validate:
```bash
auval -v aufx L480 Skyl                 # AU: substitute your UNIQUE_ID / BRAND_ID
pluginval --validate bin/Lexicon480.vst3   # VST3 (and CLAP via clap-validator)
```

`auval` passing is the gate for Logic/GarageBand; `pluginval` for Reaper/Bitwig/Cubase etc.

---

## Phase F — Cross-checks and guardrails

### F.1 The three-consumer invariant

Wire CI to build all three from the one header on every change: (1) the integer harness (and run it against the golden traces), (2) the DPF plugin, (3) the Seed2 firmware (cross-compiled). If any fails to compile or the harness diverges, you've broken the shared core. This is what keeps "one header, three targets" honest.

### F.2 Bit-exactness lives at the native rate only

Never claim bit-exactness for output captured at a resampled rate. Validate at the native rate in the harness; treat the plugin/firmware boundary resampling as a separately-acceptable approximation.

### F.3 Coefficient tables: single source of truth

Generate the coefficient/delay-tap tables **programmatically from the ROM/emulator** into a header the core includes — never hand-transcribe them. Hand-copied tables are where silent divergence hides, and OCR/transcription errors are exactly the failure mode flagged in your prior work. If the emulator and the core read from the same generated table, that whole error class disappears.

### F.4 Don't let float into the datapath

Code review rule: the only `float`/`Sample` in `l480_core.hpp` are the boundary conversions and the control-rate parameter math in setters. Everything between `floatToAru` and `aruToFloat` is integer. A stray float multiply in a tap is a fidelity bug that the harness will catch but a reviewer should catch first.

### F.5 Established findings are authoritative

Where this guide's reconstruction details touch your prior-session conclusions (coefficient encode/decode, the multi-rate animation, WCS behavior, ROM placement), those conclusions win over any in-the-moment re-derivation. Encode them as asserts/comments in the core so they can't quietly drift.

---

## Condensed checklist

1. **Instrument the emulator** with probe points; capture golden traces for impulse, sweep, and per-parameter sweeps.
2. **Write the Phase-A datapath spec** (topology, coefficients, encode/decode, animation, word format) — confidence-tagged.
3. **Generate coefficient tables** from the ROM/emulator into an included header (§F.3).
4. **Author `l480_core.hpp`** — header-only, `sgdsp`-conformant, Standalone style, integer datapath, float boundary, `processFixed` + `process`. `[CONFIRM]` word format and native rate.
5. **Build the integer harness**; iterate the core to exact equality against the traces.
6. **Add the WAV/IR harness** for ears and spectrogram/EDC checks.
7. **Host in `sgdsp`** on the Seed2: object in DTCM, `AruSample` delay buffers in SDRAM, codec at native rate or resample. (Firmware App Integration Guide.)
8. **Wrap in DPF**: `DISTRHO_PLUGIN_HAS_UI 0`, `UNIQUE_ID`/`BRAND_ID`/`CLAP_ID`, named params, `run()` → `process()`, Makefile `all: vst3 au clap jack`, add `sgdsp` include path.
9. **Build/install/validate**: `make` → `bin/*.vst3`/`*.component`/`*.clap`; `auval` + `pluginval`.
10. **CI builds all three** from the one header; harness runs on every commit.

---

## Items to confirm against your sources

- `[CONFIRM]` ARU sample word: bit width (18), fractional convention, accumulator width, rounding/truncation rule.
- `[CONFIRM]` ARU native sample rate (sets delay-length integers and the resampling boundary).
- `[CONFIRM]` whether/how the ARU interpolates fractional delay taps (drives the integer interpolation primitive).
- `[CONFIRM]` your `sgdsp` `core/platform.hpp` yields no-op macros and a valid `Sample`/`SampleRate` when no platform config is included (else add a 10-line `sgdsp_desktop.hpp`).
- Point me at one concrete `sgdsp` primitive header (`core/types.hpp` and `delay/glay.hpp`) and I'll match your exact `Sample` typedef, macro names, and `DelayLineExternal` conventions so the core is drop-in rather than approximate.
