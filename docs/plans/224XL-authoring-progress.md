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
| Decaying/tuned reverb (gain/decay arithmetic) | ✅ **RESOLVED** — coefficient encoding, b3/RDRREG/, result shift, read-before-write, closer ordering all confirmed; λ 1.48→~1.000346 (near-critical loop); DMEM addressing + register file CONFIRMED CORRECT |
| DMEM addressing (64K bank, base 0) | ✅ **CONFIRMED CORRECT** — one 64K×16 bank (#060-02512), `addr=(pos−offset)&0xFFFF`, base=0 (anchored by s76); no bank-select |
| Register file (WA/RA, no address-3 gating) | ✅ **CONFIRMED CORRECT** — 4×LS670 (U29-U32, #060-01318), DAB WSTB/ writes every cycle, R[3] stores normally |
| Hardware IR ground truth | ✅ **In repo** — P85 `IR/Lexicon 224XL/P85 - 20.0 Seconds A.wav` (RT60≈20 s, λ=0.9999899); Concert Hall V7.2.L (RT60≈4.86 s, λ=0.9999580) |
| Decaying CONCERT (sub-LSB fine-arithmetic) | ⏳ **Final remaining item** — model is ~3×10⁻⁴ too hot (λ≈1.000346 vs target 0.9999899); sub-LSB rounding/truncation in saturating multiplier/result transfer |
| FPC analog I/O (live input + true stereo split) | ⏳ Deferred — FPC encoding confirmed; position base confirmed 0 |
| Parameters (per-program curves) | ⏳ Interface stub only |
| Modulation / LFO (dynamic parity) | ⏳ Interface stub only |
| All 20 programs | ⏳ Only CONCERT (0x01) generated/validated |
| Seed2 firmware wrapper (Phase D) | ⛔ Not started |
| DPF plugin wrapper (Phase E) | ⛔ Not started |
| Three-consumer CI (Phase F.1) | ⛔ Not started (harness builds locally) |

**Headline:** the C++ core reproduces the Python `aru_datapath.py` reference *integer-exact* for CONCERT
static microcode (`diff_harness golden 01` → `DIFF PASSED`). Arithmetic is fully RESOLVED (coefficient
encoding, b3/RDRREG/, result-register shift, read-before-write, comb-closer ordering); loop eigenvalue
moves from the broken ~1.48 → ~1.000346. DMEM addressing (one 64K×16 bank, base=0, confirmed by
schematic #060-02512 and anchored by s76 input-read step) and the register file (4×LS670, no
address-3 gating, confirmed by #060-01318) are **confirmed correct** — these are no longer open items.
**The one remaining item to a fully decaying CONCERT is a sub-LSB fine-arithmetic detail** (~3×10⁻⁴):
the model currently runs λ≈1.000346 vs the hardware P85 target λ=0.9999899 (RT60≈20 s). After that:
I/O wiring, parameters, modulation, host wrappers.

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

6. **Arithmetic RESOLVED — the tank is near-critical. (UPDATED)** The RESOLVED arithmetic (items below)
   brings the CONCERT loop eigenvalue from the broken ~1.48 (sustaining) → **~1.000346** (near-critical,
   very slow growth). DMEM addressing is confirmed correct (one 64K×16 bank, base=0, schematic #060-02512;
   the earlier λ=0.9979 with the tank in its own address window was a Schroeder-integration artifact over a
   non-decaying signal, not a real decay; the s52/s104 offset-0x1000 collision is real but negligible).
   The register file is confirmed correct (4×LS670, U29-U32, #060-01318; DAB WSTB/ writes every cycle; no
   address-3 gating; R[3] stores normally). The diff harness stays green (DIFF PASSED) and multiplier unit
   tests pass throughout. The single remaining gap is sub-LSB rounding/truncation (~3×10⁻⁴) — see §5B.

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
   via the ADD'L MULT diagnostic (handler 0x0D99). Together these bring λ: 1.48 → ~1.000346.

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
passes (DIFF PASSED); multiplier unit tests pass. Loop eigenvalue CONCERT: ~1.48 → **~1.000346**.
See §3 item 7 for the full knob table.

**✅ CONFIRMED CORRECT — DMEM addressing.** The DMEM is one 64K×16 bank (sixteen 4164 DRAMs, schematic
#060-02512). Formula: `addr = (pos − offset) & 0xFFFF`, position base = 0 (anchored by the input-read
step s76, offset 0xFFFF, WA=2 ⇒ addr=pos+1). There is no bank-select; #060-02273 is the SBC
program-memory board, not the delay RAM. The earlier "λ=0.9979 with the tank in its own address window"
was a Schroeder-integration artifact over a non-decaying signal, not a real decay; the s52/s104
offset-0x1000 collision is real but negligible.

**✅ CONFIRMED CORRECT — Register file.** 4×LS670 (U29–U32, schematic #060-01318 register-file zoom):
WA/RA feed all chips, `DAB WSTB/` (A41) writes every cycle, no special address-3 gating — R[3] stores
normally; the "pass-through" is the firmware's dump-the-don't-care convention. (The "WA=3 magic lever"
idea is refuted.)

**Hardware IR targets now in repo:**
- **P85 (default CONCERT):** `IR/Lexicon 224XL/P85 - 20.0 Seconds A.wav` — RT60≈20 s, λ=0.9999899 @ 34130 Hz (primary oracle)
- **Concert Hall V7.2.L:** `IR/Lexicon 224XL/Concert Hall V7.2.L.wav` — RT60≈4.86 s, λ=0.9999580 (24-bit/96 kHz, LFO ~2–3 Hz, pre-delay ~147 ms)

### B. Close the final sub-LSB (decaying CONCERT)  *(current highest priority)*

The default CONCERT is a near-critical **20-second** tank: target **λ = 0.9999899 @ 34130 Hz** (from
the hardware IR `P85 - 20.0 Seconds A.wav`, RT60≈20 s). The model is currently λ≈1.000346 — ~3×10⁻⁴
too hot (grows to a plateau instead of decaying). The gap is sub-LSB (one coeff unit = 1/64 ≈ 1.5%;
needed nudge ≈ 0.03%) — a **rounding/truncation detail** in the 2's-complement saturating multiplier /
result transfer, localized to the two +0.976 comb closers (s65, s88). Below firmware/schematic
resolution; the hardware P85 IR is the only oracle.

Prioritized investigations (see **[224XL-concert-decay-continuation.md](224XL-concert-decay-continuation.md)** for the full brief):
1. Bit-faithful saturating multiplier — confirm floor-divide vs truncate in partial products, and
   saturation clamp behavior matches the LS163 counter terminal-count / LS157 sat-mux exactly.
2. Rounding/truncation-mode sweep vs P85 EDC — try the four rounding combinations (coeff×floor/round,
   result>>3 floor/round) and pick the one that minimizes λ error against the hardware IR decay curve.
3. Comb-closer pipeline ordering — verify XFER-then-b3 sequencing is bit-exact (no off-by-one in the
   result-register feedback for steps s65/s88).
4. Confirm booted param state == 20 s default — re-boot with `power_up_id=0x01` and check slider state
   matches P85 param settings, not the shorter V7.2 IR.
5. LFO — confirm the modulation walker is at center (depth=0 or phase=0) for the static impulse test,
   so the static eigenvalue comparison is valid.

DMEM-position-base and register-file items are **RESOLVED/confirmed** — no longer open.

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

- **Sub-LSB fine-arithmetic — the final remaining item.** The model runs λ≈1.000346 vs the hardware P85
  target λ=0.9999899 (RT60≈20 s). The gap (~3×10⁻⁴) is localized to the saturating multiplier /
  result-transfer rounding for the +0.976 comb closers (s65, s88). The hardware P85 IR is the only oracle.
  See step B above and `224XL-concert-decay-continuation.md` for the full investigation plan.
- **DMEM addressing and register file — CONFIRMED CORRECT.** No longer open: one 64K×16 bank, base=0
  (schematic #060-02512, anchored by s76); 4×LS670, no address-3 gating (schematic #060-01318).
- **224XL step clock / exact Fs.** 128 steps × ~34.13 kHz ⇒ ~4.37 MHz step clock (inferred). Bit-exact
  delay lengths only hold at the true native rate — confirm via a hardware Fs measurement.
- **Hardware IR P85 (20 s default) is the decay oracle.** `Concert Hall V7.2.L.wav` (RT60≈4.86 s) is
  also available for a shorter param state. Use P85 for absolute eigenvalue calibration.
- **Reference/core lockstep.** Any further arithmetic changes must update `aru_datapath.py` and
  `ArithProfile` together; the diff harness is the safety net. Treat the reference as the spec.

---

## 7. How to pick up the work

1. Read this file, then the technical reference (§2 links) for the locked decisions.
2. Reproduce the green baseline (§2 "Reproduce") — confirm `DIFF PASSED` and `ctest` 2/2.
3. **Current target: step B — close the sub-LSB fine-arithmetic.** The arithmetic, DMEM addressing, and
   register file are all confirmed correct. The single remaining gap is the rounding/truncation detail
   in the saturating multiplier / result transfer for the +0.976 comb closers (s65, s88). Target:
   λ=0.9999899 @ 34130 Hz (P85 hardware IR, RT60≈20 s). See `224XL-concert-decay-continuation.md`
   for the prioritized investigation plan. Validate with `wav_ir_tool ir` against
   `IR/Lexicon 224XL/P85 - 20.0 Seconds A.wav` (primary) and `Concert Hall V7.2.L.wav` (secondary).
