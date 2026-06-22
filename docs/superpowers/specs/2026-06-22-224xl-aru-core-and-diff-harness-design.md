# Lexicon 224XL — Bit-exact ARU Core + Diff Harness (Scaffold) — Design

**Date:** 2026-06-22
**Status:** Approved (design); spec under review
**Scope:** Scaffold the header-only C++17 224XL ARU reverb core (`224xl.hpp`) and the
desktop diff/validation harness, per `docs/plans/480L_rom_to_plugin_guide.md`, adapted to the
224XL's actual datapath. This is a **first-cut working scaffold**, not the finished bit-exact-vs-hardware
core.

Source material: `docs/reference/224/224XL_technical_reference.md` (master), the per-topic 224XL docs,
`docs/plans/sgdsp-processor-authoring-guide.md`, the Python tools in `tools/`, and the sgdsp library at
`libs/sgdsp/include/sgdsp/`.

---

## 1. Goal & the reality that shapes it

The 480L guide assumes the golden reference is hardware (or a ROM emulator that emits audio). **The 224XL
has no audio-producing emulator** — its Z80 SBC only *builds and modulates* the WCS microcode; the real
ARU/DMEM hardware computed the audio. Therefore:

- The bit-exact reference for arithmetic is the **Python `aru_datapath.py` model**, independently anchored
  by the **Service-Manual multiplier test vectors** (and, later, a real-hardware recording).
- The bit-exact reference for *program correctness* is the firmware-produced WCS image
  (`mem[0x4000:0x4200]`) decoded with the §3 field map.

### Validation gate for this scaffold

> **The C++ core reproduces the Python `aru_datapath` reference integer-exact on CONCERT (0x01) static
> microcode, AND the Service-Manual multiplier test vectors pass, AND the C++ microword decode matches
> `decode_microword.decode(0x01)` field-for-field.**

Hardware-anchored bit-exactness is explicitly **out of scope for the scaffold** and deferred to later
milestones (§7). Several arithmetic details are genuinely OPEN (tech-ref §4/§10) and are resolved *in* the
diff loop, not before it.

---

## 2. Decisions (locked)

| # | Decision | Choice |
|---|---|---|
| 1 | Scaffold depth | **Working first-cut** — compiles, reproduces the Python reference for CONCERT static, passes multiplier vectors, OPEN arithmetic behind named knobs; float boundary + param/modulation interfaces present but lightly stubbed. |
| 2 | Program scope | **CONCERT (0x01) first**, table generator structured so the other 19 programs drop in. |
| 3 | Python tooling | **Additive** — new exporter + a non-breaking `run_trace()` in `aru_datapath.py`. Existing tool behavior unchanged. |
| 4 | Harness build | **CMake.** |
| 5 | Harness location | **`tools/harness/224xl/`** (goldens at `tools/harness/224xl/golden/`). |
| 6 | Core filename / class | File `224xl.hpp`; class `Lexicon224XLCore` (identifier can't start with a digit). |
| 7 | WCS table source | **Generated** from firmware into a C++ header (guide §F.3 — never hand-transcribe). |

---

## 3. The 224XL ARU datapath (what the core executes)

Authoritative values from `224XL_technical_reference.md` §1–§3:

- **128 WCS steps per output sample, fixed** for all programs. Loop `S = 0..127`; RESET is implicit at the
  loop boundary (hardwired counter terminal-wrap, no microword bit).
- **Register file**: 4 registers × 16-bit, independent read address `RA` (2-bit) and write address `WA`
  (2-bit). `R[WA] = DAB` every cycle; `WA == 3` is a pass-through/scratch write.
- **Multiplier**: 16×(6+sign)-bit, 2's-complement, saturating.
- **Accumulator**: 20-bit (hardware). `ZERO` clears it.
- **Result register**: 16-bit, loaded from the accumulator on `XFER`.
- **DMEM**: circular 64K words → `DMEM_MASK = 0xFFFF`. `addr = (position − offset) & 0xFFFF`;
  `position += 1` per sample.
- **FPC analog I/O**: address-decoded into the offset field — `offset & 0x8000` = FPC select,
  `offset & 0x4000` = channel (0 → right→B,C / 1 → left→A,D); input read = `WA=2, low14=0x3FFF`; output
  write = pass-through `WA=3` step. Live-image use requires the per-program position base (OPEN).

### Microword field map (active-low storage; §3)

For step `S`, 4 bytes at `0x4000 + S*4 + lane` (lane0=U49 … lane3=U3):

| Field | Decode |
|---|---|
| OFST (lane0–1) | `offset = (~(lane1<<8 \| lane0)) & 0xFFFF`; `addr = (position − offset) & 0xFFFF` |
| COEFF mag (lane3 6:0) | `lane3 & 0x7F` (raw) |
| CSIGN (lane3 7) | active-low, `1 ⇒ negative` |
| RA (lane2 5:4) | `((~lane2)>>4) & 3` |
| RW/SRC (lane2 3) | `((~lane2)>>3) & 1` (b3 — OPEN read/write semantics) |
| XFER (lane2 2) | `((~lane2)>>2) & 1` |
| WA (lane2 1:0) | `(~lane2) & 3` |
| ZERO (lane2 7) | `((~lane2)>>7) & 1` |
| PROTECT (lane2 6) | `((~lane2)>>6) & 1` |

NOP/pure-delay step ⇔ `lane2 == lane3 == 0xFF`.

---

## 4. Component A — the core (`libs/sgdsp/include/sgdsp/reverb/224xl.hpp`)

Standalone style (authoring guide §"Two Processor Styles"), namespace `sgdsp::reverb`, `using namespace
core;`, header-only, `#pragma once`, banner comment, includes `../core/types.hpp` + `../core/platform.hpp`.

```cpp
namespace sgdsp::reverb {
using namespace core;

template <uint32_t DmemWords = 65536, uint32_t Channels = 2>
class Lexicon224XLCore { ... };

template <uint32_t N = 65536> using Lexicon224XL     = Lexicon224XLCore<N, 2>;
template <uint32_t N = 65536> using Lexicon224XLMono = Lexicon224XLCore<N, 1>;
}
```

### 4.1 Fixed-point types

- `using AruWord = int32_t;` — carries the 16-bit signed register/sample value (±32767); int32 for headroom.
- `using AruAccum = int64_t;` — accumulator carrier; effective width is a knob (§4.3).
- DMEM is a hardware-fixed 64K ring; the ring mask is the constant `kDmemMask = 0xFFFF`. The `DmemWords`
  template param exists for guide-conformance / app placement and is `static_assert`ed ≥ 65536.
- External buffer: `AruWord* dmem` passed into `prepare()` (External-Buffers pattern), app owns placement.

### 4.2 Lifecycle & surface (authoring-guide conformant)

- `void prepare(SampleRate sr, AruWord* dmem[Channels]) noexcept` — store rate, connect buffer(s), init
  sub-components, call `reset()` last. `SGDSP_NOINLINE`.
- `void reset() noexcept` — zero state only; never recompute coefficients.
- `SGDSP_INLINE void process(Sample in, Sample& outL, Sample& outR) noexcept` — float boundary wrapper.
- `SGDSP_INLINE void processFixed(AruWord in, AruWord& outL, AruWord& outR) noexcept` — integer entry the
  harness calls (bit-exact).
- Setters `void set<Name>(...) noexcept` (clamp + precompute); getters `<type> <name>() const noexcept`
  (no `get` prefix).
- The object tags none of its own members with `SGDSP_*` (placement-agnostic).

### 4.3 Datapath + OPEN-arithmetic knobs

A single `executeSample()` runs all 128 steps per tech-ref §2. Per step: decode (or read pre-decoded
table), DMEM/FPC access, register write, multiply-accumulate, conditional `XFER`. RA hardcoded to the
validated `(ctl>>4)&3`.

The not-yet-resolved arithmetic lives in one `struct ArithProfile` of `static constexpr` values so tuning
is a one-line change:

| Knob | First-cut value (matches Python ref) | Hardware target |
|---|---|---|
| `kCoeffShift` (the `/128` denominator) | `7` | resolve (≈/128 + 2-LSB weighting) |
| `kAccSatBits` (accumulator saturation width) | `16` (reference uses `sat16`) | `20` |
| `kResultShift` (20→16 result-register shift) | `0` | resolve |
| `kRoundMode` | truncate-toward-zero | confirm via diff |
| `b3` read/write semantics | per reference | resolve |

**The first cut sets these knobs to exactly reproduce the current `aru_datapath.py` arithmetic**
(`ACC = sat16(ACC + R[RA]*coeff/128)`, `RES = sat16(ACC)`), so layers 1 and 2 go green immediately. Moving
toward hardware later flips knobs, not datapath code.

> Note: the hardware's 20-bit multiplicand alignment (`operand20 = sign_extend(x,17)<<3`, tech-ref §2) and
> the 2-LSB coefficient packing are **documented but not applied in the first cut**, because the current
> reference does plain `R[RA]*coeff//128`. This divergence is called out in a comment so it is not a silent
> bug; it is enabled when the reference advances toward hardware.

### 4.4 Float boundary

The only float in the signal path:
`floatToAru(x) = clamp(lround(x * 32768.0f), -32768, 32767)`; `aruToFloat(v) = v * (1.0f/32768.0f)`.
`[CONFIRM]` round-vs-truncate against the codec path later. Until the per-program position base pins true
FPC routing, stereo out duplicates the mono datapath result to L and R (documented, not silently wrong);
true L→A,D / R→B,C split is a deferred milestone.

### 4.5 Parameters & modulation (scaffolded, lightly stubbed)

Interfaces present: a `setParameter(index, value01)` surface mapping through the per-program sweep curves
(`224XL_param_sweep_<id>.json`) and a triangle-LFO walker per §6/§7. The bring-up target is CONCERT
**static** (no modulation), matching the static reference. Established findings (§F.5) are pinned with
`SGDSP_ASSERT` / comments so they cannot drift.

---

## 5. Component B — generated program tables (`libs/sgdsp/include/sgdsp/reverb/224xl_programs.hpp`)

Guide §F.3: never hand-transcribe. `tools/gen_224xl_programs.py` boots the firmware
(`boot_xl.boot(power_up_id=...)`), reads `mem[0x4000:0x4200]`, and emits a generated C++ header containing,
per program: the 512-byte raw WCS image and the decoded per-step fields. First cut emits **CONCERT (0x01)**;
the generator loops the 20-program table (tech-ref §5) so the rest are one command away. The header is the
single source of truth shared with the Python reference (same bytes → the whole transcription error class
disappears).

---

## 6. Component C — golden export (Python, additive) → `tools/harness/224xl/golden/`

1. **`tools/aru_datapath.py`**: add a **non-breaking** `run_trace(prog, ra_pick, nsamp, imp)` alongside the
   existing `run()`. It emits a deterministic stream: per step — offset, addr, decoded coeff, RA index,
   `R[RA]` pre-MAC, product, ACC post, RES (on XFER), DMEM read/written value; per sample — the output
   value (energy proxy now; true output once FPC is pinned). Pinned to the validated
   `ra_pick = lambda st: (st['b5']<<1)|st['b4']`. Existing `run()`/`load_microcode()` behavior unchanged.
2. **`tools/export_golden_224.py`**: runs the reference and writes, per program id, to
   `tools/harness/224xl/golden/<id>_wcs.bin`, `<id>_fields.json`, `<id>_trace.bin`. The C++ harness reads
   these files at run time — **no Python invoked during the harness build/run** (CI-friendly).

---

## 7. Component D — the diff harness (`tools/harness/224xl/`, CMake)

`CMakeLists.txt` plus three executables that all `#include` the one core header:

1. **`diff_harness`** — loads the goldens, runs `processFixed()` over the same input, and asserts
   integer-exact equality at every probe point. On mismatch, prints the **first divergent sample index +
   step + field name + expected/actual**. Covers layer 1 (microcode-decode parity) and layer 2 (arithmetic
   parity).
2. **`mult_vectors_test`** — the Service-Manual multiplier vectors as standalone asserts: coefficients
   ±21/32, ±42/32, ±63/64 and ×1, ×½, ×−1, ×¼, ×5/4 (four multiplications each; the last two must trip
   saturation). Independent anchor for the arithmetic, per tech-ref §4.
3. **`wav_ir_tool`** — WAV in → `process()` (float) → WAV out, plus an impulse/IR dump mode for
   ears/spectrogram/EDC checks (guide §C.3).

Desktop build pulls only the sgdsp portable headers (`libs/sgdsp/include`); no platform config, no
CMSIS/STM headers. `SGDSP_INLINE → inline`, placement macros → no-ops (verified: `platform.hpp` has no
`#error` and defaults to no-ops, so no desktop shim is needed).

---

## 8. Validated now vs deferred

| Green at end of scaffold | Deferred (knobs/interfaces in place) |
|---|---|
| C++ microword decode == `decode_microword.decode(0x01)` field-for-field | Per-program position base → live FPC I/O |
| C++ ARU == Python `aru_datapath` integer-exact (CONCERT static) | True stereo L→A,D / R→B,C split |
| Multiplier test vectors pass (incl. saturation) | Hardware-anchored arithmetic (20-bit acc, 2-LSB coeff, result shift, rounding) (governs loop gain/decay — first-cut tank sustains) |
| Builds via CMake; header compiles as plain C++17 | Param/modulation dynamic parity (§9 layer 3); all 20 programs; DPF + Seed2 wrappers |

---

## 9. Bring-up sequence

1. `tools/gen_224xl_programs.py 0x01` → generated CONCERT table header.
2. `tools/export_golden_224.py 0x01` → goldens on disk.
3. CMake configure + build the three harness tools.
4. `mult_vectors_test` green (anchors arithmetic independently).
5. `diff_harness` layer-1 (decode) green.
6. Tune `ArithProfile` knobs until `diff_harness` layer-2 (arithmetic) green.
7. `wav_ir_tool` produces a non-silent, bounded impulse response (clean decay follows the deferred ArithProfile tuning, §8 — the first-cut tank sustains, matching the reference).

---

## 10. Deliverables (files)

- `libs/sgdsp/include/sgdsp/reverb/224xl.hpp` — the core.
- `libs/sgdsp/include/sgdsp/reverb/224xl_programs.hpp` — generated CONCERT table (extensible to 20).
- `tools/gen_224xl_programs.py` — table-header generator.
- `tools/export_golden_224.py` — golden exporter.
- `tools/aru_datapath.py` — additive `run_trace()` (existing API untouched).
- `tools/harness/224xl/CMakeLists.txt`
- `tools/harness/224xl/diff_harness.cpp`
- `tools/harness/224xl/mult_vectors_test.cpp`
- `tools/harness/224xl/wav_ir_tool.cpp`
- `tools/harness/224xl/golden/` — exported goldens (generated; git-ignore or commit per preference).

---

## 11. Non-goals (explicit)

- Not matching real 224 hardware audio sample-for-sample (no hardware reference yet).
- Not the DPF plugin or the Seed2 firmware app (the core is built to host them later; not wrapped here).
- Not all 20 programs validated (CONCERT only; generator covers the rest).
- Not dynamic param/modulation parity (interfaces only; static CONCERT is the gate).
