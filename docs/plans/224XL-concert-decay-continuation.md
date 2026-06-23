# 224XL CONCERT decay — final 3×10⁻⁴ continuation brief

**For a fresh session.** This is a self-contained brief to finish ONE thing: make the booted-default
CONCERT reverb **decay** instead of sustaining. Everything else in the ARU reconstruction is resolved
and committed. Read this top to bottom before touching anything.

---

## The single remaining goal

The booted-default CONCERT loop is **near-critical and ~3×10⁻⁴ too hot**: float linear eigenvalue
**λ ≈ 1.000346**, so the integer model grows to a plateau (~360k energy) instead of decaying. The
hardware default CONCERT is a **20-second** tank: target **λ = 0.9999899** at the 34.13 kHz native rate
(from the IR below). Close that ~3.6×10⁻⁴ gap so CONCERT decays cleanly (genuine λ ≤ ~0.99999, a single
exponential), without a truncation-cliff hack.

**The gap is SUB-LSB.** One coefficient unit is 1/64 ≈ 1.5%; the needed nudge is ~0.03%. So the fix is a
rounding/truncation detail in the saturating multiply or result transfer — NOT an integer
coefficient/shift/denominator change (those are resolved and any coarse change overshoots wildly).

---

## Hardware ground truth (in repo — your oracles)

- `IR/Lexicon 224XL/P85 - 20.0 Seconds A.wav` — **default CONCERT, RT60 ≈ 20.2 s** (24-bit/48 kHz stereo,
  captures the full decay to −60 dB). **λ_target = 0.9999899 @ 34130 Hz.** THE calibration target for the
  booted-default model. (Sensitivity ~±1×10⁻⁶ per ±2 s of RT60.)
- `IR/Lexicon 224XL/Concert Hall V7.2.L.wav` — same program, a **shorter** param state, RT60 ≈ 4.86 s,
  λ = 0.9999580 (24-bit/96 kHz). Use as a second point: the decay param scales the feedback coefficients,
  so a correct model should reach ~4.86 s when the LOW/MID params are reduced from the 20 s default.
- λ from RT60: `λ = 10^(-3 / (RT60 * 34130))`. Measure model decay via the Schroeder EDC of the per-sample
  energy envelope (sum |RES| over XFER steps) or the output proxy.

Caveat: P85's params are the stated "default"; confirm the booted WCS (power_up_id=0x01) actually
corresponds to that 20 s default (see next-step 4). The recordings' exact param values are otherwise
unknown, so match decay SHAPE + RT60, not bit-exact audio.

---

## RESOLVED — do NOT re-investigate (firmware + schematic + hardware confirmed)

Implemented in `tools/aru_datapath.py` (reference) and `libs/sgdsp/include/sgdsp/reverb/224xl.hpp`
(C++ core), verified integer-exact by the diff harness (`DIFF PASSED`). Committed (d89bb57 +
subsequent). The cycle-accurate model per active step (R[0..3], ACC, RES; pos+1/sample):

- **Coefficient:** 6-bit `C = (lane3 magnitude) >> 1`, applied as `C/64` (= mag/128). Magnitude stored
  **linear/direct**; sign from CSIGN (bit7, active-low: 1⇒negative). Gains ≥ 1 (Manual ×1, ×5/4) come from
  **4-step MAC accumulation gated by ZERO**, NOT a single multiply. (Firmware ADD'L MULT diagnostic
  0x0D99 Rosetta map: lane3 0x7D/ZERO=0→×1, 0xBD→×−0.5, 0x7D/ZERO=1→×−1, 0xDD→×−0.25, 0x5D→×−1.25.)
  The "2 extra LSBs" (packer 0xB4F0) are for the **modulation interpolation** coeff (0xAE72), NOT the main multiply.
- **b3 = RW/SRC = RDRREG/** (result-register output-enable onto the DAB; ARU U43/U44 = 74F374, pin A50) =
  DMEM read/write + DAB-source select: `b3=1` → `DM[addr]=RES` (comb write-back, dab=RES); `b3=0` →
  `dab=DM[addr]` (read). It is an independent stored bit. (NOT XFER.)
- **Datapath:** `operand = x<<3`; `prod = (operand * Cs) >> 6` (arithmetic floor); `ACC = sat20(ACC+prod)`
  (±524287); on XFER `RES = sat16(ACC>>3)`. **LS670 register file read-before-write** (read R[RA] before
  `R[WA]=dab`). **Comb closer writes the POST-XFER RES** (XFER updates RES before the b3 write-back).
- **DMEM = ONE 64K×16 bank** (sixteen 4164 DRAMs; DMEM schematic #060-02512). `addr=(pos-offset)&0xFFFF`,
  **position base = 0** (anchored by the input-read step s76, offset 0xFFFF, WA=2 ⇒ addr=pos+1). NOT two
  16K banks; no bank-select. #060-02273 is the SBC program-memory board (irrelevant to DMEM).
- **Register file = 4×LS670 (U29-U32)** (ARU #060-01318 register-file zoom): `WA/RA` feed all chips; `DAB
  WSTB/` (A41) writes **every cycle**; **NO special address-3 gating** — `R[3]` stores normally;
  "pass-through" is just the firmware's dump-the-don't-care convention.
- **Field map:** `ZERO/ = A49`, `XFER CK = A27`, `RDRREG/ = A50`, `CSIGN/ = A48`, `RA0/=A46, RA1/=A42,
  WA0/=A44, WA1/=A45`.

## REFUTED dead-ends — do NOT revisit (each cost a deep investigation)

- **Position base / DMEM bank aliasing.** DMEM is one 64K bank, base 0. The earlier "λ=0.9979 with the
  tank in its own address window" was a **Schroeder-integration artifact** over a non-decaying signal — not
  a real decay. The s52/s104 offset-0x1000 collision is real but **negligible** (fixing it doesn't move λ).
- **Register-file address-3 "magic" gating.** No such gating exists (zoom-confirmed). `WA=3` no-op is
  non-physical (collapses the tank to silence).
- **Complemented coefficient magnitude** (`gain=(127-mag)/64`). Refuted by the firmware packer (magnitude
  is direct) and the diagnostic gains.
- **Coarse coefficient denominator / result-shift / feedback-path changes.** All scale-invariant vs the
  structural mode; they overshoot, collapse, or don't move λ.

## Where the excess lives (localization)

The growing mode is in the two `+0.976` comb closers **s65 and s88** (zeroing s88 → λ=1.000000, s65 →
1.000006). They read `RA=3`; their feedback steps write `WA=3`. The mode is a narrow self-oscillation
(~3653 Hz / ~9.3-sample loop) and is **gain-invariant** (uniform coeff cuts barely move λ). So the lever is
the exact per-pass rounding/truncation of the closer's accumulate→result path, not its nominal gain.

---

## Next-step investigations (in priority order)

1. **Bit-faithful saturating multiplier (most likely home of the sub-LSB).** The model collapses the
   multiply to the net `prod=(operand*Cs)>>6`. The real ARU is a 2's-complement shift-and-add doing **2
   bits/state × 3 states** via the dual-rank shift register (LS194/LS195) and a partial-product register
   (SM §3.7; ARU #060-01318). Model the actual partial-product formation + its low-bit truncation
   bit-faithfully and re-measure the closer loop. The per-pass truncation bias of the real multiplier is
   the prime suspect for the ~0.03% the net model misses.
2. **Rounding/truncation mode sweep.** At (a) `prod=(operand*Cs)>>6` and (b) `RES=sat16(ACC>>3)`, sweep
   floor / toward-zero / round-to-nearest (and any add-half round bit). Measure the booted-default CONCERT
   energy-EDC vs P85's RT60. Look for a *principled* mode that yields genuine λ ≤ 0.99999 (a clean
   exponential, not a low-amplitude cliff). NOTE earlier coarse floor-vs-trunc tests read as "negligible"
   on λ — but at 3×10⁻⁴ the bias may matter; measure carefully (the float-eigenvalue fit is noisy at this
   scale, so prefer the integer EDC/RT60 over 20–40 s).
3. **Comb-closer pipeline ordering.** Re-derive the exact intra-cycle order for s65/s88 against the ARU
   timing (SM Fig 3.4): when XFER CK loads RES vs when RDRREG/ drives the DAB vs the DMEM write vs the
   register read-before-write. A one-cycle pipeline subtlety in the closer could shave the residual.
4. **Confirm the booted param state == P85's 20 s default.** Read the slider bytes 0x3c00–0x3c05 and the
   modulation params 0x3cd3/0x3cd4/0x3ccd at boot (power_up_id=0x01) and compare against
   `docs/reference/224/224XL_param_sweep_01.json`. If the booted default isn't the 20 s state, recompute
   λ_target from the actual booted params. (Then also verify: reducing LOW/MID per the sweep curves should
   move the model toward V7.2's 4.86 s — a strong cross-check of the whole arithmetic.)
5. **Always-on LFO modulation (§7).** The triangle LFO continuously modulates the tank tap offsets
   (anti-phase pairs). It decorrelates the comb modes and may change the *apparent* RT/shape; model it and
   compare. (It should not turn a true λ>1 into <1, but it affects the measured envelope and the
   3653 Hz self-oscillation that currently dominates.)
6. **Hardware internal capture (only if obtainable).** The output IR pins the decay but not internal
   per-step state. A real-ARU capture of an internal node, or a known test vector run through the hardware
   multiplier, would settle the sub-LSB definitively. Likely unavailable; treat the IR EDC as the oracle.

---

## How to work (tools, gates, discipline)

- **Reference:** `tools/aru_datapath.py` — `run()` / `run_trace()` (the bit-exact model; the C++ core must
  mirror it). `decode_microword.py` (per-step decode). `boot_xl.boot(power_up_id=0x01)` → WCS at
  `mem[0x4000:0x4200]`.
- **Harness (the gate):** `tools/harness/224xl/` (CMake). Any change to the reference arithmetic MUST be
  mirrored in `libs/sgdsp/include/sgdsp/reverb/224xl.hpp` and keep the diff harness green:
  ```
  python tools/export_golden_224.py 0x01
  cd tools/harness/224xl && cmake -S . -B build && cmake --build build --config Release
  ctest --test-dir build -C Release            # 2/2
  build/Release/diff_harness.exe golden 01     # DIFF PASSED (integer-exact reference<->core)
  build/Release/mult_vectors_test.exe          # ALL PASS
  ```
- **IR validation:** load P85 (and V7.2), Schroeder EDC, RT60, λ. Match the model's CONCERT energy-EDC
  shape + RT60 to P85 (~20 s). Do NOT accept a non-exponential truncation-cliff "decay."
- **Discipline:** root-cause before changing anything (the dead-ends above were each a deep dig — don't
  repeat them). Keep reference↔core lockstep (diff green) on every change. Prefer a *principled*
  hardware-faithful detail over an arbitrary attenuation knob; if you must use a knob, put it in
  `ArithProfile`, document it as IR-calibrated, and note it's the open sub-LSB.
- **Master docs:** `docs/reference/224/224XL_technical_reference.md` (§2–§4, §9, §10),
  `docs/plans/224XL-authoring-progress.md`. Schematics: `docs/reference/224/*.png`
  (ARU #060-01318, T&C #060-02475, FPC #060-01320, DMEM #060-02512, plus the U29-U32 / U43-U44 / U10-U11
  zoom crops; full-res crops were generated under docs/reference/224/crops/, gitignored).

## Definition of done

The booted-default CONCERT, run through `wav_ir_tool` (float boundary) or the integer reference, produces a
**clean single-exponential decay with RT60 ≈ 20 s** matching P85's EDC shape, via a hardware-faithful
(or explicitly IR-calibrated + documented) sub-LSB rounding/truncation — with the diff harness still green
and the multiplier unit tests passing. Bonus: reducing LOW/MID per the param-sweep curves reproduces
V7.2's ~4.86 s.
