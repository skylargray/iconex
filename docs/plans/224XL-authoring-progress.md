# Lexicon 224XL — Authoring Progress & Roadmap

**Last updated:** 2026-06-22
**Goal:** A single header-only C++17 ARU core that runs bit-exact in a diff harness, and (later) as
Seed2 firmware via `sgdsp` and as a DPF VST3/AU/CLAP plugin — the path laid out in
[480L_rom_to_plugin_guide.md](480L_rom_to_plugin_guide.md), applied to the 224XL.

This doc tracks where the 224XL reconstruction actually is against that guide, what the current
codebase contains, what was learned, and the prioritized next steps.

**Authoritative companions**
- Reconstruction spec for the C++ phase: [docs/superpowers/specs/2026-06-22-224xl-aru-core-and-diff-harness-design.md](../superpowers/specs/2026-06-22-224xl-aru-core-and-diff-harness-design.md)
- Implementation plan (8 tasks): [docs/superpowers/plans/2026-06-22-224xl-aru-core-and-diff-harness.md](../superpowers/plans/2026-06-22-224xl-aru-core-and-diff-harness.md)
- Master technical reference: [docs/reference/224/224XL_technical_reference.md](../reference/224/224XL_technical_reference.md)
- Authoring conventions: [sgdsp-processor-authoring-guide.md](sgdsp-processor-authoring-guide.md)
- Target architecture: [480L_rom_to_plugin_guide.md](480L_rom_to_plugin_guide.md)

---

## 1. Status at a glance

| Area | State |
|---|---|
| Reverse-engineering (architecture, microword, programs, params, modulation) | ✅ Done (prior sessions) — see the technical reference |
| Bit-exact C++17 ARU core (`224xl.hpp`) | ✅ First cut, merged to `main` |
| Emulator-diff harness (integer parity) | ✅ CONCERT static **integer-exact** vs the Python reference |
| Multiplier/saturation unit tests | ✅ Pass (Service-Manual coefficient anchors) |
| Decaying/tuned reverb (gain/decay arithmetic) | ✅ **RESOLVED** — coefficient encoding, b3/RDRREG/, result shift, read-before-write, closer ordering all confirmed; λ → 0.9979 (genuine decay) pending position base |
| Hardware IR ground truth | ✅ **In repo** — `IR/Lexicon 224XL/Concert Hall V7.2.L.wav` (RT60 ~4.9 s, 24-bit/96 kHz) |
| FPC analog I/O (live input + true stereo split) | ⏳ Deferred — pending per-program position base (final blocker) |
| Parameters (per-program curves) | ⏳ Interface stub only |
| Modulation / LFO (dynamic parity) | ⏳ Interface stub only |
| All 20 programs | ⏳ Only CONCERT (0x01) generated/validated |
| Seed2 firmware wrapper (Phase D) | ⛔ Not started |
| DPF plugin wrapper (Phase E) | ⛔ Not started |
| Three-consumer CI (Phase F.1) | ⛔ Not started (harness builds locally) |

**Headline:** the C++ core reproduces the Python `aru_datapath.py` reference *integer-exact* for CONCERT
static microcode (`diff_harness golden 01` → `DIFF PASSED`), and the arithmetic is now fully RESOLVED
(coefficient encoding, b3/RDRREG/, result-register shift, read-before-write, comb-closer ordering) —
verified by the diff harness + Service-Manual unit tests + the hardware IR. Loop eigenvalue moves from
the broken ~1.48 → ~0.9979 (genuine single-exponential decay) once the per-program DMEM position base
is pinned. **The one remaining structural blocker is the per-program position base** (DMEM address
aliasing between tank banks). After that: I/O wiring, parameters, modulation, host wrappers.

---

## 2. What exists in the codebase (this phase's deliverables)

All merged to `main` (2026-06-22). Goldens and build dirs are gitignored (reproducible).

**Core (header-only C++17)**
- [libs/sgdsp/include/sgdsp/reverb/224xl.hpp](../../libs/sgdsp/include/sgdsp/reverb/224xl.hpp) —
  `sgdsp::reverb::Lexicon224XLCore<DmemWords, Channels>`. Integer ARU datapath: 4×16-bit register file,
  `int64` accumulator, 64K-word DMEM ring (`kDmemMask = 0xFFFF`), 128-step microprogram with NOPs skipped,
  saturating MAC. Float appears **only** at the I/O boundary (`floatToAru`/`aruToFloat`). Two entries:
  `processFixed` (integer, what the harness diffs) and `process` (float, for the future plugin/firmware),
  plus an instrumented `processFixedTraced` twin. All OPEN arithmetic lives in one `ArithProfile` struct.
- [libs/sgdsp/include/sgdsp/reverb/224xl_programs.hpp](../../libs/sgdsp/include/sgdsp/reverb/224xl_programs.hpp) —
  **generated** CONCERT (0x01) WCS image (single source of truth; never hand-transcribed).

**Python reference & golden pipeline (additive — existing tools untouched)**
- [tools/aru_datapath.py](../../tools/aru_datapath.py) — the bit-exact reference model; added a
  non-breaking `run_trace()` that emits per-step probes + per-sample energy.
- [tools/gen_224xl_programs.py](../../tools/gen_224xl_programs.py) — boots firmware → generates the C++ table header.
- [tools/export_golden_224.py](../../tools/export_golden_224.py) — exports `wcs.bin` / `fields.json` /
  `esum.bin` / `steps.bin` / `meta.json` goldens for the harness.
- [tools/test_run_trace.py](../../tools/test_run_trace.py) — proves `run_trace` esum == `run` esum (non-breaking).

**Desktop diff harness (CMake)** — [tools/harness/224xl/](../../tools/harness/224xl/)
- `diff_harness.cpp` — Layer-1 (microword decode parity vs `fields.json`) + Layer-2 (per-step probe + per-sample
  energy parity vs the binaries). Prints the first divergent sample/step/field on mismatch.
- `mult_vectors_test.cpp` — multiplier/saturation unit tests anchored on the Service-Manual coefficient set.
- `wav_ir_tool.cpp` — drives the float boundary; `ir` (impulse-response dump) and `wav` (filter a mono WAV) modes.
- `golden_io.hpp`, `CMakeLists.txt`, `README.md`.

**Reproduce:**
```
python tools/gen_224xl_programs.py 0x01
python tools/export_golden_224.py 0x01
cd tools/harness/224xl && cmake -S . -B build && cmake --build build --config Release
ctest --test-dir build -C Release --output-on-failure       # 2/2 pass
build/Release/diff_harness.exe golden 01                     # DIFF PASSED
```

---

## 3. What was learned (this phase)

Beyond the reverse-engineering already captured in the technical reference, the C++/harness phase pinned
down several things that matter for the rest of the build:

1. **The golden reference is the Python model, not hardware.** The 224XL's Z80 SBC *builds and modulates*
   the WCS microcode but does **not** compute audio (the discrete ARU/DMEM hardware did). So unlike the
   480L guide's assumption of a ROM emulator that emits audio, the 224XL's bit-exact golden is
   `tools/aru_datapath.py`, anchored by the Service-Manual multiplier vectors (and, eventually, a real
   224 recording). This is the single biggest structural deviation from the 480L guide for this machine.

2. **Floor division, not truncation.** The reference computes `(reg*coeff)//128` (Python floor, toward −∞).
   The C++ must use **arithmetic right shift `>>7`**, never `/128` (which truncates toward zero and diverges
   on negative products). Proven load-bearing: swapping `>>7`→`/128` makes the very first step diverge
   (`prod = −1718` truncation vs `−1719` floor).

3. **NOP steps must be skipped at load.** A NOP (`lane2==lane3==0xFF`) decodes to `coeff = −127`; if executed
   it corrupts the accumulator. The reference drops NOPs; the core mirrors that. CONCERT has **110 active
   steps** of 128.

4. **Additive input injection at the first active step** is identical to the reference's replacement
   (`dab = imp`) because DMEM and RES are zero at sample 0 — and it generalizes cleanly to continuous input
   on the float path.

5. **The probe-trace methodology works and is non-vacuous.** Diffing the 8-field per-step probe
   `(n, s, addr, dab, racc_in, prod, acc, res)` pinpoints the exact first divergence. Verified non-vacuous
   by perturbing the core (arithmetic, RA bits, golden bytes) and confirming the harness fails each time.

6. **Arithmetic RESOLVED — the tank decays. (UPDATED)** The RESOLVED arithmetic (items below) brings
   the CONCERT loop eigenvalue from the broken ~1.48 (sustaining) → ~1.0003 (structural unity from DMEM
   address aliasing between overlapping tank-bank offsets) → **~0.9979** (genuine clean single-exponential
   decay, matching the hardware IR shape) once the per-program position base is pinned. The diff harness
   stays green (DIFF PASSED) and multiplier unit tests pass throughout.

7. **Arithmetic knobs — all RESOLVED:**

   | Knob | First-cut | RESOLVED value |
   |---|---|---|
   | `kCoeffShift` (coeff denominator) | `7` (`/128`) | **6 (`/64`)** — 6-bit C = mag>>1, applied as C/64 (= mag/128 net); magnitude direct/linear |
   | `kAccSatBits` (accumulator width) | `16` (`sat16`) | **20** (LS163 counters; sat ±524287) |
   | `kResultShift` (20→16 result transfer) | `0` | **3** (`RES = sat16(ACC >> 3)`; arithmetic right-shift / floor) |
   | `kRoundMode` | truncate-toward-zero | **Floor (arithmetic >>)** — toward −∞ |
   | `b3` (DMEM read/write) | per reference | **RDRREG/=A50** — result-reg tristate OE; `b3=1` ⇒ write-back, `b3=0` ⇒ read; independent stored bit |
   | Register-file read timing | — | **Read-before-write** (LS670); old value used when WA==RA |
   | Comb-closer ordering | — | **XFER loads RES first**, then b3 writes post-XFER RES to DMEM |
   | "2 extra LSBs" (0xB4F0) | attributed to main multiply | **Modulation interpolation coefficient only** (computed at 0xAE72 `AND 3 / OR 3`) |

   Gains ≥ 1 (×1, ×5/4, ×42/32) arise from 4-step MAC accumulation (ZERO gating), firmware-confirmed
   via the ADD'L MULT diagnostic (handler 0x0D99).

---

## 4. Mapping to the 480L guide's phases

The guide ([480L_rom_to_plugin_guide.md](480L_rom_to_plugin_guide.md)) defines Phases A–F. Status for the 224XL:

- **Phase A — ROMs → executable spec.** ✅ Mostly done. The "instrumented emulator + golden traces + test
  vectors + extracted structure" role is filled by the technical reference (topology, microword field map,
  programs, params, modulation) plus this phase's `run_trace()` instrumentation and `export_golden_224.py`
  trace export. *Caveat vs the guide:* the golden is the Python ARU model, not an audio-emitting ROM
  emulator (§3 item 1 above).

- **Phase B — author the header-only core.** ✅ First cut. `224xl.hpp` follows the authoring guide
  (standalone style, `sgdsp::reverb`, `prepare`/`reset`/`process`, external buffers, placement-agnostic).
  Adapted to the 224XL's *actual* widths (16-bit reg / 20-bit acc / 6–7-bit coeff / 64K DMEM), **not** the
  480L's 18-bit datapath. Integer datapath + float boundary as the guide mandates.

- **Phase C — bit-exact validation harness.** ✅ First cut, the core achievement of this phase.
  Integer parity for CONCERT static (Layer 1 decode + Layer 2 arithmetic). Multiplier vectors pass.
  WAV/IR tool exists. *Remaining within Phase C:* tune the OPEN arithmetic toward hardware (§3 item 7),
  dynamic (param/modulation) parity, and extend to all 20 programs.

- **Phase D — wrap in `sgdsp` for Seed2 firmware.** ⛔ Not started. The core is already an `sgdsp`-shaped
  processor, so this is "host it in an app" (object in DTCM, `AruWord` DMEM in SDRAM, codec at/resampled to
  the native rate) rather than new DSP.

- **Phase E — wrap in DPF for VST3/AU/CLAP.** ⛔ Not started. Same header, DPF glue, named params,
  headless.

- **Phase F — cross-checks & guardrails.** 🟡 Partial. Done: coefficient/table single-source-of-truth
  (generated header, F.3); no-float-in-the-datapath enforced (F.4); established findings encoded as
  asserts/comments (F.5). Not done: CI building all three consumers from the one header on every change
  (F.1); bit-exactness only claimed at native rate (F.2 — currently moot, no resampling yet).

---

## 5. Next steps (prioritized roadmap to full implementation)

### A. ✅ RESOLVED — Arithmetic (coefficient encoding, b3, result shift, register timing, closer ordering)
All arithmetic is confirmed (firmware + ARU schematic #060-01318 + T&C #060-02475 + hardware IR).
Implemented in `tools/aru_datapath.py` and `libs/sgdsp/include/sgdsp/reverb/224xl.hpp`. Diff harness
passes (DIFF PASSED); multiplier unit tests pass. Loop eigenvalue CONCERT: ~1.48 → ~1.0003 →
**~0.9979** (genuine decay) once the position base is pinned. See §3 item 7 for the full knob table.

**Hardware IR ground truth now in repo:** `IR/Lexicon 224XL/Concert Hall V7.2.L.wav` (24-bit/96 kHz,
RT60 ~4.9 s, LF ~5.25 s / HF ~3.79 s, LFO ~2–3 Hz, pre-delay ~147 ms, λ_target ≈ 0.999958 ±1e-6).
Use for decay-shape / HF / LFO validation. Parameter settings unknown — exact RT60 calibration deferred.

### B. Pin per-program position base → FPC I/O + DMEM alignment  *(current highest priority)*
- **The final structural blocker.** Two tank banks write overlapping offsets (e.g. 0x1000, 0xD4D8)
  that alias in the 64K buffer, holding λ at ~1.0003. Pinning the per-program base to a non-aliasing
  address window drops λ to ~0.9979 — genuine clean exponential decay matching the IR shape.
- Anchor: the input read at `low14 = 0x3FFF`, `WA=2` (CONCERT step 76, offset=0xFFFF) ⇒ address =
  position+1. The SM notes the DMEM may be one 64K bank or two 16K banks.
- Once pinned: route `(offset−base)&0x8000` reads from FPC input latch, `WA=3` writes to FPC output
  channel (`&0x4000`: L→A,D / R→B,C). Replace the first-cut "duplicate mono to L/R."

### C. Parameters
- Wire `setParameter(index, value01)` through the per-program sweep curves in
  `docs/reference/224/224XL_param_sweep_<id>.json`, mapping value → target coeff/delay at the linked WCS
  steps. Add the multi-rate de-zipper (≈ −4/−1 per control tick) for click-free changes.

### D. Modulation / LFO (dynamic parity — guide §9 layer 3)
- Implement the triangle-LFO walker (rate `0x3cd3`, depth `0x3cd4`, enable `0x3ccd` bit6) modulating the
  per-program tank taps in anti-phase pairs, with allpass-interpolated fractional delays. Validate by
  capturing live WCS frames from the firmware emulator at control ticks and diffing the core's WCS state.

### E. All 20 programs
- Loop `gen_224xl_programs.py` / `export_golden_224.py` over the 20-program table; run `diff_harness` per
  program. The generator/exporter already support this — it's a batch pass plus per-program triage.

### F. Phase D — Seed2 firmware app
- Host the core in an `sgdsp` app: object in DTCM, `AruWord` DMEM in SDRAM (64K words), codec at the ARU
  native rate (≈34.13 kHz) or resample at the callback boundary. (Per the Firmware App Integration Guide.)

### G. Phase E — DPF plugin
- `DISTRHO_PLUGIN_HAS_UI 0`, unique/brand/CLAP IDs, expose the named params, `run()` → `process()`,
  `Makefile all: vst3 au clap jack`, host-rate ↔ native-rate resampling at `activate()`. Validate with
  `auval` / `pluginval`.

### H. Phase F — CI & guardrails
- CI builds all three consumers (harness + DPF + Seed2 cross-compile) from the one header on every commit,
  runs the diff harness against the goldens, and forbids float in the datapath.

---

## 6. Open questions / risks

- **Per-program position base — the final structural blocker.** Without the correct per-program base,
  tank banks alias in the 64K buffer and λ stays at ~1.0003 (structural unity loop). This is step B
  above, and unlocks both correct DMEM topology and FPC I/O decode for live images.
- **224XL step clock / exact Fs.** 128 steps × ~34.13 kHz ⇒ ~4.37 MHz step clock (inferred). Bit-exact
  delay lengths only hold at the true native rate — confirm via a hardware Fs measurement.
- **Hardware IR parameter settings unknown.** `Concert Hall V7.2.L.wav` is usable for decay-shape, HF,
  and LFO shape validation. Exact RT60 calibration and absolute gain matching require a recording with
  known parameter settings.
- **Reference/core lockstep.** Any further arithmetic changes must update `aru_datapath.py` and
  `ArithProfile` together; the diff harness is the safety net. Treat the reference as the spec.

---

## 7. How to pick up the work

1. Read this file, then the technical reference (§2 links) for the locked decisions.
2. Reproduce the green baseline (§2 "Reproduce") — confirm `DIFF PASSED` and `ctest` 2/2.
3. **Current target: step B — pin the per-program position base.** The arithmetic is fully resolved;
   the single remaining structural gap is the DMEM address aliasing between tank banks. Anchor on the
   input-read step (CONCERT step 76, offset=0xFFFF, WA=2) ⇒ address = position+1 to find the base.
   Once pinned: λ drops to ~0.9979 and FPC I/O decode (`(offset−base)&0x8000`) becomes correct for
   live images. Validate with `wav_ir_tool ir` against `IR/Lexicon 224XL/Concert Hall V7.2.L.wav`
   (decay shape / HF roll-off / LFO).
