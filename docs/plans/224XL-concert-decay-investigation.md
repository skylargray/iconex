# 224XL CONCERT decay — complete investigation record

**Status:** OPEN (root cause understood; exact structural origin unresolved). Last updated 2026-06-23.
**Scope:** make the booted-default CONCERT reverb **decay** (RT60 ≈ 20 s) instead of sustaining/growing.
Everything else in the ARU reconstruction is resolved, committed, and diff-harness-green.

This is the consolidated record of a long systematic-debugging investigation. It supersedes the original
"final 3×10⁻⁴ continuation brief" whose central premise (a sub-LSB rounding fix) was **refuted** here.
Read the Executive Summary, then the Verified-Faithful and Refuted sections before touching anything —
many deep dead-ends are recorded so they are not repeated.

---

## 1. Executive summary

The booted-default CONCERT loop **grows** instead of decaying: clean converged power-iteration structural
eigenvalue **λ ≈ 1.0008** (small-signal, float-exact), vs the hardware target **λ = 0.9999899** (20 s tank
at 34130 Hz, from the P85 IR). The integer model grows to a saturation-bounded limit cycle and sustains.

The original brief blamed a **sub-LSB rounding/truncation** detail. That was **refuted by direct experiment**:
the instability is present in **exact float arithmetic with zero quantization**, so it is **structural**, not
arithmetic. We then verified, and found **faithful**, every reconstructable element — microcode, the full ARU
arithmetic datapath (confirmed against high-res schematic redraws), the sign convention, the accumulator MAC
structure, the crossover steps, and the execution timing. We also proved on first principles that arithmetic
rounding/truncation **cannot** change a loop's decay eigenvalue (it only adds a fixed DC bias).

The decisive reframe (credit: the project owner): a 20 s reverb cannot rely on coincidental tolerance — a
nested **all-pass** reverb is *lossless by construction* and the decay must ride on top as a *provable loss*.
Our measurements bear this out exactly:
- The loop is **all-pass-flat**: scaling every coefficient by 20 % barely moves λ. That is the signature of a
  lossless all-pass network sitting at ~unity.
- The **MID/LOW "decay" coefficients are nearly impotent** on λ — the decay-control mechanism is decoupled.
- **Removing the closer feedforward (MID→0) makes the model decay** (λ=0.9996). The all-pass network underneath
  is sound; the feedforward **over-recovers**, pushing the loop a hair over unity.
- The decay is supposed to be **frequency-dependent** (CONCERT params = LOW low-band decay, MID mid-band decay,
  XOV crossover; V7.2 IR shows HF decays faster than LF, 3.79 s vs 5.25 s). The **mid-band is under-damped** —
  its 3653 Hz resonance is the mode that grows. Adding a one-pole HF-damping lowpass to the recirculation pulls
  λ straight to target (a=0→1.0008, a=0.2→1.00003).

**Net:** the model faithfully implements the firmware, yet sits ~0.08 % over unity, uniformly across all decay
settings, because it lacks sufficient **mid-band / HF damping**. The exact hardware origin of that damping is
unresolved — the crossover steps are present and faithfully addressed, yet under-damp. This matches the
480L-roadmap hazard that "microcode words … didn't do what the encoding implied; a clean disassembly still
needs behavioral validation on real hardware."

**The fork (decision pending):**
1. **Behavioral hardware check** — watch a real ARU run the closer/crossover words to find what diverges from
   the literal decode. The only definitive path; needs a working 224XL + logic analyzer.
2. **V7.2-calibrated HF-damping element** — model the band-split damping as a one-pole lowpass calibrated to
   reproduce V7.2's measured LF/HF split and the 20 s default λ. A real, documented mechanism (not an arbitrary
   leak), flagged as the one element whose exact hardware origin is open.

---

## 2. The problem (precise statement)

- Per output sample the ARU runs a 128-step WCS microprogram over a 64K-word circular delay memory (DMEM),
  a 4×16-bit register file, a saturating MAC, and a 16-bit result register. The CONCERT reverb tank lives in
  DMEM + register feedback. 110 of the 128 steps are active.
- The booted default (power_up_id=0x01) should be a **20 s** reverb (λ=0.9999899). Our model gives λ≈1.0008
  (grows to a saturation limit cycle; flat envelope over a 20 s integer run, RT60≈46000 s).
- λ↔RT60: `λ = 10^(−3 / (RT60 · 34130))`. Sensitivity ~±1×10⁻⁶ per ±2 s of RT60 — this is a knife-edge system.

## 3. Ground-truth oracles (in repo)

- `IR/Lexicon 224XL/P85 - 20.0 Seconds A.wav` — **default CONCERT, RT60 ≈ 20 s** (24-bit/48 kHz stereo).
  λ_target = 0.9999899 @ 34130 Hz. Rich, diffuse, multi-modal hall (comb peaks ~400–5712 Hz).
- `IR/Lexicon 224XL/Concert Hall V7.2.L.wav` — same program, **shorter** state, RT60 ≈ 4.86 s (24-bit/96 kHz
  mono). **HF decays faster than LF (3.79 s / 5.25 s) — direct evidence of frequency-dependent tank damping.**
- Both IRs have strong energy at **3653 Hz** (P85 1.49×, V7.2 2.55× rms-normalized) — the model's growing-mode
  frequency is a *real* tank resonance, not a spurious artifact. The issue is the gain at that resonance.

---

## 4. Verified FAITHFUL (do not re-investigate)

Implemented in `tools/aru_datapath.py` (reference) and `libs/sgdsp/include/sgdsp/reverb/224xl.hpp` (C++ core),
integer-exact by the diff harness (`DIFF PASSED`). The per-step model (R[0..3], ACC, RES; pos+1/sample):

- **Coefficient:** 6-bit `C = (lane3 7-bit magnitude) >> 1`, applied as `C/64`. Magnitude stored direct; sign
  from CSIGN (lane3 bit7, active-low: 1⇒negative). Gains ≥1 arise from 4-step MAC accumulation gated by ZERO.
  Verified vs the firmware ADD'L MULT diagnostic (0x7D→×1, 0xBD→×−0.5, 0xDD→×−0.25 …).
- **Datapath:** `operand = x<<3`; `prod = (operand·Cs) >> 6` (floor); `ACC = sat20(ACC+prod)` (±524287); on
  XFER `RES = sat16(ACC>>3)` (floor). LS670 register file read-before-write. Comb closer writes POST-XFER RES.
- **b3 = RDRREG/ (A50):** result-register OE onto the DAB. `b3=1` → `DM[addr]=RES` (write-back) and `dab=RES`;
  `b3=0` → `dab=DM[addr]` (read). Independent stored bit.
- **DMEM:** one 64K×16 bank (sixteen 4164 DRAMs, #060-02512). `addr = (pos − offset) & 0xFFFF`, base 0
  (anchored by FPC input-read s76, offset 0xFFFF, low14 0x3FFF, WA=2). Outputs tie to DAB unbuffered.
- **Field map:** ZERO/=A49, XFER CK=A27, RDRREG/=A50, CSIGN/=A48, RA0/=A46, RA1/=A42, WA0/=A44, WA1/=A45.
  RA field = `(b5,b4)` (datapath-validated; alternatives collapse the tank or implausibly reuse b3/RDRREG).

**Session-2 schematic verification (high-res redraws of ARU sheet 060-01318, provided by the owner):**
- **Result register (U43/U44, 74F374):** `RDRREG/`/A50 → pin-1 OE *directly* (no extra gate); `XFER CK`/A27 →
  pin-11 clock; D-inputs are a **bare wired tap of `PP3..PP18`** = `ACC>>3` (floor, no rounding hardware).
- **Full 20-bit accumulator:** 5× S283 adders (U19-23), 5× LS157 sat-muxes (U33-37), 5× LS163 accumulator
  registers (U45-49), 5× LS86/S86 XOR, LS377/LS175 partial-product input registers (U10-12, ARUCK-clocked).
- **CSIGN stage:** `CSIGN/`→74S04→XOR controlled-invert (two's-complement negate, applied *after* the multiply).
- **Accumulator MAC structure:** 20 ZERO clears, mostly **4-step MAC blocks** (matches the diagnostic).

---

## 5. The investigation — every hypothesis tested and its verdict

All diagnostics are in `tools/` (catalog in §7). Verdicts are reproducible.

| # | Hypothesis | Test | Verdict |
|---|---|---|---|
| 1 | Sub-LSB rounding/truncation in the multiply or result transfer | float-exact (no quant) still grows; floor quant *reduces* growth | **REFUTED** — structural, not rounding |
| 2 | Rounding-mode at the two shift points | 16/16 combos {floor,nearest,toward-zero,round-even}² give identical growth | **REFUTED** (`exp_rounding`) |
| 3 | Bit-faithful serial multiplier truncation | same class as #1/#2; float-exact already unstable | **REFUTED** |
| 4 | Documented LFO modulation detunes the unstable mode | static ±50-sample detune of s56/57/107/108 leaves λ identical to 7 digits; live swept modulation reduces +1.31→+0.86 dB/s but never decays | **REFUTED** (`exp_lfo`, `exp_modlive`) |
| 5 | Closer pipeline ordering | base / read-after-write / pre-XFER / result-from-prod all λ>1 (base hottest) | **REFUTED** (`exp_order`) |
| 6 | Execution-timing semantics | defer DMEM writes = identical; register reset = identical; defer register writes = non-physical collapse (0.66) | **REFUTED** (`exp_structvar`) |
| 7 | Sign decode error | uniform rule matches firmware diagnostic *and* traced hardware; no single sign-flip yields λ<1 | **REFUTED** (`exp_sign`) |
| 8 | RA field assignment wrong | tested (b5,b4)/(b5,b3)/(b4,b3)/… — only (b5,b4) gives a coherent decaying-or-growing tank; alternatives collapse to silence or implausibly reuse b3 | **REFUTED** (decode correct) |
| 9 | Crossover taps mis-addressed (short-delay) | instrumented actual delays: sensible short loops (s45→s43 = 1-sample HF feedback), firmware-derived | **REFUTED** (`echo_delays`) — crossover faithful |
| 10 | ARU-arithmetic idiom (round-toward-zero / sign-magnitude) | produces a **dead-zone** (sub-LSB signals die) + saturation (large signals grow); never a clean 20 s decay | **REFUTED as the decay fix** (`exp_idiom`) — real for output fidelity, not for λ |

**Key general principle (proven):** arithmetic rounding/truncation/sign can only add a fixed per-pass DC bias;
a constant per-pass term gives a DC equilibrium while perturbations still grow at the structural λ. So no
rounding idiom can pull a structurally-unstable loop (λ>1 at normal amplitude) to stable. This exonerates the
entire arithmetic datapath as the *decay* culprit, independent of (and consistent with) the schematic.

### What the eliminations leave — the structural picture (the reframe)

- **All-pass-flat:** `d(λ)/d(eps) ≈ −0.005` (scaling all coeffs); needs eps≈0.20 to reach λ<1 (`exp_crux`).
  Signature of a lossless all-pass network at ~unity. The decay is NOT set by the swept coefficients.
- **Decay coefficients impotent:** scaling MID ×0.5 → λ=1.0004 (barely moves); closer feedback ×0.8 → 1.0008.
- **Feedforward over-recovers:** MID→0 → λ=0.9996 (decays); λ grows monotonically with feedforward magnitude
  (×1.5→1.0030); sign is correct (flip is worse). Localized to the **third feedforward tap** of each closer
  block (reads R[2]=a DMEM tap): zeroing them → λ=0.9998729. **But the decode is faithful** (third-FF reads
  R[2] per the microword), so this is *where* the sensitivity lives, not a fixable decode error.
- **Hand-derived closer block A (s62–s65):**
  `res_new = [ +62·res_in − 37·r3_in − 8·d_a − 37·d_b ] / 64`, with `d_b = DMEM[pos−50456]` (cross-block,
  1-pass-delayed). The `−37·d_b` cross-coupling is the over-recovery term.
- **Frequency-dependent decay:** params LOW/MID/XOV = a two-band (crossover) decay. V7.2 confirms HF<LF.
  Crossover steps (s45/46/97/98) ARE modeled and faithfully addressed (s45→s43 is a real 1-sample HF feedback
  loop), yet the **mid-band is under-damped**. A one-pole HF lowpass on the recirculation → λ to target.
- **Uniform across settings:** the model sustains for MID idx0–6, decays only at idx7 (`exp_slider`) — a
  systematic offset, not a per-setting tuning issue.
- **3653 Hz mode** is a real resonance (present in both IRs); the model's gain there is a hair too high.

### Refuted dead-ends from earlier (do not revisit)
- Position-base / DMEM bank aliasing (one 64K bank, base 0; the s52/s104 @4096 collision is negligible).
- Register-file "address-3 magic" gating (no such gating; WA=3 no-op collapses the tank).
- Complemented coefficient magnitude (`(127−mag)/64`) — magnitude is direct (firmware packer).
- Coarse coefficient/denominator/result-shift/feedback changes (scale-invariant; overshoot or collapse).
- Echo-pattern IR comparison as a topology discriminator — **confounded** by the instability (the model's IR
  is dominated by its growing mode; `run()` injects at s0 not the real input s76; stabilizing for comparison
  hits the saturation lock). Inconclusive; superseded by the band-split picture.

---

## 6. Root cause (current best understanding)

The CONCERT tank is a **nested all-pass network (lossless by construction) + a frequency-dependent band-split
decay (LOW/MID/XOV)**. Our reconstruction implements the all-pass network and the crossover faithfully, but
the **mid-band ends up under-damped by ~0.08 %**, so its 3653 Hz resonance grows instead of decaying. The
damping deficit is uniform across decay settings and is NOT attributable to any independently-verifiable
component (microcode, arithmetic, sign, accumulator, crossover addressing, execution timing all faithful).

By elimination, the deficit is one of:
1. **A microcode word that doesn't do what its encoding implies** (the 480L-roadmap hazard) — our bit-faithful
   decode is correct, but the hardware's *behavior* on the closer/crossover words diverges. Needs a behavioral
   hardware check to confirm.
2. **A distributed per-delay-line HF damping** (air-absorption-style) that the firmware microcode and the
   datapath schematic don't obviously encode — i.e. a real hardware element below what those sources show.

Either way, the missing piece is **mid-band / HF damping**, which is exactly the documented behavior (V7.2's
HF<LF). It is a real mechanism, not an arbitrary attenuation.

---

## 7. Tools created this investigation (`tools/`)

Reference model: `aru_datapath.py` (`run`, `run_trace`), `boot_xl.py`, `decode_microword.py`. Diagnostics:

| Tool | What it measures / showed |
|---|---|
| `measure_decay.py` | per-sample energy envelope → growth/decay rate; confirmed growth + s65/s88 localization |
| `exp_rounding.py` | rounding-mode sweep at both shift points + amplitude test → rounding inert; saturation-bounded limit cycle |
| `exp_structural.py` | float-exact (no sat/quant) run → structural λ>1; floor quant *reduces* growth |
| `exp_eig.py` | power-iteration structural λ + dominant-frequency probe |
| `exp_lfo.py` | static modulated-tap detune → λ unmoved (mode has no support on s56/57/107/108) |
| `exp_modlive.py` | live swept chorus modulation → reduces growth, never decays |
| `exp_topology.py` | tank tap/offset dump + short-range loop finder |
| `exp_order.py` | converged power-iteration λ; closer pipeline-ordering variants |
| `exp_structvar.py` | execution-timing variants (defer DMEM/register, register reset) |
| `exp_bootstate.py` | booted LARC sliders (=0) + modulation params + closer WCS bytes |
| `exp_slider.py` | MID/LOW slider sweep → RT60 (sustains idx0–6, decays idx7) |
| `exp_edc.py`, `exp_smallimp.py`, `exp_crux.py` | long-run EDC, small-impulse decay, linear-λ-vs-saturating-decay vs eps → all-pass-flat, saturation limit cycle |
| `exp_sign.py` | CSIGN decode verification + per-tap sign-flip sensitivity |
| `exp_idiom.py` | sign-magnitude / round-toward-zero multiply idioms → dead-zone, not a decay fix |
| `echo_extract.py`, `echo_autocorr.py`, `echo_stable.py` | model-vs-real IR feature/resonance comparison (artifacts in `tools/_ir/`) — confounded by instability |
| `echo_delays.py` | **instrumented actual recirculation delays** → crossover faithfully addressed (1-sample HF loop) |

Key λ measurements (clean converged power iteration, float-exact): baseline **1.0009967**; MID→0 **0.9996**;
third-FF zeroed **0.9998729**; HF-damping a=0.2 **1.00003**. Target **0.9999899**.

---

## 8. The fork (decision pending) + how to continue

**Option 1 — behavioral hardware check (definitive).** Probe a real ARU running CONCERT to see what the closer
feedforward / crossover words actually do vs the literal decode. Needs a working 224XL + logic analyzer.
Per the 480L roadmap §8 hazard, this is the class of bug a clean disassembly cannot settle on its own.

**Option 2 — V7.2-calibrated HF-damping element (principled stand-in).** Model the band-split mid-band damping
as a one-pole lowpass in the recirculation; calibrate it to reproduce V7.2's measured LF/HF split (5.25 s /
3.79 s) and verify it lands the 20 s default on λ=0.9999899. Document it in `ArithProfile` as the open
hardware-fidelity element. This is data-driven from real hardware and reproduces the documented
frequency-dependent decay — not an arbitrary leak. **Caveat:** apply it in the linear (sub-saturation) path —
a flat post-hoc leak fights the saturation limit cycle (small leak can't break it; large over-damps).

**Gates / discipline (unchanged):** any reference-arithmetic change MUST be mirrored in
`libs/sgdsp/include/sgdsp/reverb/224xl.hpp` and keep the diff harness green:
```
python tools/export_golden_224.py 0x01
cd tools/harness/224xl && cmake -S . -B build && cmake --build build --config Release
ctest --test-dir build -C Release            # 2/2
build/Release/diff_harness.exe golden 01     # DIFF PASSED
build/Release/mult_vectors_test.exe          # ALL PASS
```
Validate decay against the P85 EDC (clean single exponential, RT60 ≈ 20 s) — never accept a non-exponential
truncation-cliff or dead-zone "decay". Bonus cross-check: reducing LOW/MID per the param-sweep curves should
move the model toward V7.2's ~4.86 s.

**Reference docs:** `docs/reference/224/224XL_technical_reference.md` (§2–§4, §9, §10),
`docs/plans/224XL-authoring-progress.md`, `docs/plans/480L_reversing_roadmap.md` §8 (the "words that don't do
what the encoding implies" hazard). Schematics: `docs/reference/224/*.png` (ARU #060-01318 incl. the
redraw/zoom crops, T&C #060-02475, DMEM #060-02512). Param curves: `docs/reference/224/224XL_param_sweep_01.json`.

## 9. Definition of done

The booted-default CONCERT, run through `wav_ir_tool` (float boundary) or the integer reference, produces a
**clean single-exponential decay with RT60 ≈ 20 s** matching P85's EDC shape and HF<LF behavior — via a
hardware-faithful (or explicitly V7.2-calibrated + documented) mid-band/HF damping element — with the diff
harness still green and the multiplier unit tests passing.
