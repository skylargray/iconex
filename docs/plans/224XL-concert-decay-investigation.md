# 224XL CONCERT decay — complete investigation record

**Status:** OPEN (root cause characterized precisely; exact missing-loss mechanism unresolved). Last updated 2026-06-23 (Session 3).
**Scope:** make the booted-default CONCERT reverb **decay** (RT60 ≈ 20 s) instead of sustaining/growing.
Everything else in the ARU reconstruction is resolved, committed, and diff-harness-green.

This is the consolidated record of a long systematic-debugging investigation. It supersedes the original
"final 3×10⁻⁴ continuation brief" whose central premise (a sub-LSB rounding fix) was **refuted** here.
Read the Executive Summary, then the Verified-Faithful and Refuted sections before touching anything —
many deep dead-ends are recorded so they are not repeated.

> **⚠️ READ §0 FIRST (Session 3, 2026-06-23).** An exhaustive ROM-vs-implementation audit (4 parallel
> reverse-engineering agents + direct experiments) **corrected several earlier numbers and conclusions**:
> the λ tool the earlier sessions used was **non-converged** (so its absolute GROW/DECAY verdicts and every
> "fix" λ in §5/§7 are unreliable), the true converged λ is **1.00112 (+1124 ppm)** — about **2× hotter**
> than the ~590 ppm recorded below — and the excess is **systematic across all long halls** (not
> CONCERT-specific). The "missing HF damping" framing is also revised (the HFD *parameter* is inert on λ).
> Trust §0 over any conflicting number elsewhere in this doc.
>
> **CURRENT PLAN / START HERE: §0.9.** §0.8 validated the topology and showed the missing loss is
> frequency-dependent and *crossover-shaped*, but the fix is **NOT** to add a calibrated filter — it is to
> find the **mis-modeled crossover/band-split** (LOW/MID/XOV) that is decoupled in our reconstruction. §0.9
> has the reasoning and the concrete trace plan (steps s43–46 / s95–98, the 1-sample feedback). Do that, not
> a fudge.

---

## 0. SESSION 3 (2026-06-23) — exhaustive ROM audit + corrected measurements

Driven by the directive "no hardware; exhaustively analyse the firmware ROMs for EVERY discrepancy in the
Python and C++." Four parallel reverse-engineering agents audited each reconstruction layer against the ROM
ground truth, plus direct converged-λ experiments. **Net: the reconstruction is faithful across every
reconstructable layer; the prior "structural" conclusion stands but is now far better characterized, and
several earlier numbers/levers were measurement artifacts.**

### 0.1 The measurement was broken — corrected numbers
- **`exp_eig.power_iter` / `exp_crux.lin_lambda` are NON-CONVERGED.** They use a cumulative-average growth
  with a malformed norm (mixes instantaneous state with a 200-sample proxy history), so λ is **nsamp-dependent**:
  the *same* program gives λ=0.9998 @ nsamp=8000 but 1.0006 @ 20000, still rising. The transient takes
  **~23 000 samples** to settle (long predelay + dense near-unity modes).
- **Correct method:** float-exact linear map, renormalize on the true L2 state norm (R, ACC, RES, all nonzero
  DMEM) every 128 samples, read the converged tail past ~25 000 samples. Tool: **`tools/exp_lambda_clean.py`**.
- **Corrected baseline λ = 1.00112 (+1124 ppm)** (two independent agents + this tool agree). The gap to the
  P85 target (λ=0.9999899, −10 ppm) is **~1134 ppm ≈ 0.11 %**, roughly **double** the ~590 ppm in §1–§2 below.
- **Every λ in §5/§7 measured with the old tool is unreliable** — specifically the "fixes" MID→0=0.9996,
  third-FF=0.9998729, HF-damp a=0.2→1.00003, and "eps≈0.20 to reach λ<1." Re-measure converged before trusting.

### 0.2 The gain landscape (converged) — only MID moves λ; HFD is inert
Converged λ vs parameter (`tools/exp_paramspace_conv.py`): **baseline idx0 = +1126 ppm**; **MID idx7 = −87 ppm**
(the only individual param that crosses unity, and only at max); **XOV idx6 = +1888 ppm** (destabilizes);
**HFD, DEP, LOW = inert (+1122…+1134 ppm, unchanged).** Implications:
- The signature is a **uniform ~+1130 ppm offset** sitting on top of an otherwise-correct MID sweep (range
  ~1213 ppm). The MID coefficients are faithful and sweep λ correctly; a constant excess rides underneath.
- **The "missing HF damping" thesis cannot be the HFD parameter.** HFD is an *input* filter (ref §6), so it
  *cannot* move the loop eigenvalue — confirmed inert. Whatever linear loss is missing acts in the **MID-band
  recirculation**, not via the HFD control.

### 0.3 Exhaustive ROM audit — ALL reconstructable layers FAITHFUL
| Layer | Method | Verdict |
|---|---|---|
| **Microword field map** (lane0–3) | Reconstructed the ROM WCS-copy loop `0xAB55` exactly: lane2/lane3 are **copied verbatim** from the program record (0 byte mismatches). Exhaustive lane2 bit-permutation sweep. | **FAITHFUL** — no field reassignment yields λ<1 while keeping a coherent tank. |
| **Coefficient / multiplier** | ARU schematic #060-01318 + packer `0xB4FF` (`AND 0x7F`, magnitude direct) + ADD'L MULT diag. | **FAITHFUL** — `Cs=±(mag>>1)`, `x<<3`, `>>6`, `RES=ACC>>3`, sat20 all confirmed. **The loop closers all store mag=124 (EVEN)**, so `(mag>>1)/64 ≡ mag/128` exactly → the denominator/odd-LSB question is **moot**; the "+0.976" label is really 0.96875. (Doc nit: the ADD'L MULT gains ×1/×−0.5/… in §4 are a misread; the diag is a near-unity structure.) Any move toward 7-bit makes it **hotter** (wrong way). |
| **Z80 emulator** (build path) | Instrumented boot; the build path executes **zero** prefixed ops (no CB/DD/FD/ED). add8/sub8 exhaustive 256², add16 exhaustive all-65536-HL. | **FAITHFUL** — offsets are computed correctly. (CCF H-flag, DAA H-flag, DD/FD-half fallback bugs exist but **never execute** on any boot path.) |
| **Datapath feedback timing** | vs schematic redraw: position-increment once/sample, LS670 read-before-write, post-XFER closer write-back, b3/RDRREG source. Converged-λ tested every plausible variant. | **FAITHFUL** — **no hardware-plausible timing variant yields λ<1**; the only "decaying" variants are non-physical collapses to silence. The committed model already picks the lowest-λ option everywhere. |
| **Python ↔ C++ parity** | Rebuilt harness; `ctest` 2/2, `DIFF PASSED`, `mult_vectors ALL PASS`. | **Integer-exact** within the harness (impulse, 4000 samples). Only divergences are *intended* streaming-I/O generalizations (C++ injects every sample / returns `lastRes`; Python injects sample-0 / returns `esum`) — no λ effect. |
| **Default parameter state** | Booted WCS coeffs == param-sweep **idx0** for every controlled step. | **FAITHFUL** — boot is at the correct default. |
| **FPC analog I/O** | Input-read steps (bit15, low14=0x3FFF, WA=2) sourced as 0 (hardware-faithful). | **Not the cause** — λ unchanged (1.0011262). (The broad bit15&WA=3 "output" filter is invalid in a live image; it sweeps in the closers.) |

### 0.4 The excess is SYSTEMATIC, not CONCERT-specific
Converged λ by program (`tools/exp_programs.py`): **CONCERT +1124 ppm, BRIGHT HALL +1198 ppm** (both long
halls **GROW**); DARK HALL / PLATE / SMALL ROOM / INVERSE ROOM collapse (decay fast); CHAMBER λ=0.781 (decays).
**Both long halls grow by ~the same amount.** A uniform missing per-pass loss flips only the near-unity (long)
reverbs; short programs still decay. This is a **systematic** deficit, strong evidence *against* a
CONCERT-specific topology/decode bug and *for* a real, roughly-uniform per-pass loss the model lacks.

### 0.5 Precise root-cause characterization (supersedes §6's wording)
- The model's **only** loss is **amplitude-dependent quantization** (floor at the two shifts): small signals
  die (dead-zone), large signals grow at the structural rate → a **saturation LIMIT CYCLE** (sustains forever).
- The hardware produces a **clean 20 s exponential decay**, which requires a roughly **amplitude-independent
  (linear) per-pass loss** of **~0.11 %** that the model does not have.
- So the missing element is a **linear per-pass loss**, distributed across the recirculating closers
  (all-pass-flat; localization is diffuse — s88/s65 most sensitive but no single block dominates), common to
  the hall topology. It is **not** in the WCS microcode, the datapath, the offsets, the field map, the
  coefficients, or the Z80 emulation — all verified faithful.
- **The original "sub-LSB rounding" brief is DEFINITIVELY refuted:** float and integer both grow at the
  structural rate; quantization produces a limit cycle, never the needed *linear* loss. (Rounding can only
  add a bounded DC bias — re-confirmed.)

### 0.6 Revised fork — what to verify next (no hardware required)
1. **Is P85 truly the booted default?** The model cannot produce a clean 20 s decay at *any* MID setting
   (idx0 grows; idx7 → RT60≈2.3 s). Verify by matching the model's swept-decay **modal frequencies** to P85:
   if the modes line up and only the decay *rate* differs uniformly, the topology is right and a single
   linear loss is the entire gap (strongly supporting a calibrated damping element as faithful-enough).
2. **Implement the documented fractional-delay all-pass interpolation** on the modulated taps (s56/57/107/108)
   — a real firmware element (ref §7, engine `0xAE72`) the integer-offset model omits entirely. Low prior
   (the growing mode has little support there) but it is the one un-modeled firmware mechanism left.
3. **A single calibrated *linear* loss is now the leading firmware-faithful stand-in** — but as a uniform
   recirculation leak / one-pole, NOT via the HFD parameter (inert). Calibrate to V7.2's HF<LF split and the
   20 s default; flag in `ArithProfile` as the open hardware-fidelity item (480L-roadmap §8 hazard: "a word
   that doesn't do what its encoding implies," or a per-delay HF damping below schematic resolution).
4. **Closed (do not redo):** field map, multiplier/coeff, Z80/offsets, datapath timing, Python↔C++ parity,
   default params, FPC input handling, sub-LSB rounding, all field/timing permutations.

New tools this session: `exp_lambda_clean.py` (converged λ — **use this, not exp_eig**), `exp_paramspace_conv.py`,
`exp_paramspace.py`, `exp_localize.py`, `exp_programs.py`, `exp_fpc.py`, `exp_symmetry.py`.

### 0.7 SESSION 3b — Z80 emu fixes + P85 modal/transfer-function match

**Z80 emulator fixes (committed to `tools/z80emu.py`, verified by `tools/test_z80_fixes.py`):**
- **CCF** now sets H = old carry (was always clearing H).
- **DAA** now sets the H output flag (subtract: H = oldH ∧ (low<6); add: H = (low>9)); the `corr`
  computation was already ZEXALL-correct (validated by an independent 100×100 BCD-decimal ground-truth test).
- **DD/FD fallback** now does IXH/IXL half-register substitution (the undocumented index-half ops), instead
  of silently running the un-prefixed opcode.
- All three never execute on any 224XL boot path (agent-verified) so they don't affect the WCS; fixed for
  general correctness. Boot regression clean (110 active steps). `test_z80_fixes.py` = ALL PASS.

**P85 modal match — CONFOUNDED BY THE INSTABILITY (inconclusive about topology).** Tools:
`modal_match.py`, `modal_verify.py`, `modal_tf.py`, `param_match_search.py`, `hf_match.py`.
- The method WORKS: a second real CONCERT IR (V7.2) vs P85 → full-spectrum correlation **0.916**; a
  delay-scrambled control → 0.30. So the test discriminates real-CONCERT from random.
- But the MODEL's transfer function (white-noise-excited, **stabilized by a uniform leak because it grows**)
  correlates with P85 at only **~0.03 — worse than the random scramble** — and **NO reachable parameter state
  reproduces P85** (swept LOW/MID/XOV/HFD/DEP/PDL incl. every max-RT60 variant: all 0.03–0.05).
- The peak-alignment "match" reported in §0.6-era notes (median ratio 0.997) was the **dense-comb
  nearest-neighbour bias**: a rigorous null test (random peak-sets, same count/band) gives the model
  **p≈0.4 (chance)**, and even V7.2-vs-P85 scores chance on peaks — the peak test has no power; only the
  full-spectrum correlation does.
- **Why 0.03 (worse than scramble):** the model is over-unity, so any single stabilizing leak leaves one
  near-marginal mode (~1896 Hz) dominating the TF, swamping the broad comb P85 has. Spectral comparison
  therefore **cannot isolate topology** while the model is unstable — a chicken-and-egg with the missing loss.
- **The proposed "one-pole HF lowpass on the recirculation" fix does NOT stabilize the model** (per-closer
  LP, pole up to 0.95 → still grows to 1e12+). It only ever looked viable under the non-converged λ tool.
  A uniform per-sample state leak (≈ delay-line "air absorption") DOES stabilize but doesn't reproduce P85.
- **User insight tested:** P85 is likely "default + max RT60." Confirmed it can't be a param-state artifact —
  coefficient params (LOW/MID/XOV/HFD/DEP) don't move modal *frequencies* (only PDL changes a delay), and no
  setting matches P85. So if the topology were right, *some* stabilized state should resemble P85; none does.

**Net (Session 3b, intermediate — partly SUPERSEDED by §0.8):** the modal match was confounded by an
**output-tap artifact** (the probe read one internal node, not the reverb output). Once corrected (§0.8) the
topology validates and the HF-damping mechanism is confirmed. (Disregard the "topology suspect / HF-lowpass
eliminated" wording above — those conclusions used the bad single-tap output.)

---

## 0.8 SESSION 3c — BREAKTHROUGH: topology validated + missing element identified

Tools: `tools/modal_output.py`, `tools/damp_probe.py`, `tools/damp_grid.py`, `tools/damp_verify.py`,
`tools/modal_decisive.py`. The Session-3b "model TF ≠ P85 (corr ~0.03)" was a **bad-output-tap artifact** —
the probe read `last RES` (one arbitrary internal node) instead of the reverb output. Reading the **FPC
output taps** (the WA=3, bit15 DAC writes; right channel) changes everything.

**Powered metric:** full-spectrum correlation of the white-noise transfer function vs the P85 hardware IR.
Benchmarks: **V7.2 (a second real CONCERT IR) vs P85 = 0.92** (the achievable ceiling); a **delay-scramble
control = 0.30**; self-consistency 0.985 (reproducible).

**Result 1 — the topology is SUBSTANTIALLY CORRECT.** With the FPC output and only a flat stabilizing leak,
the model correlates **0.53** with P85 — far above the scramble's 0.30. The reconstructed tank delays/topology
are sound; the earlier "topology differs" is retracted.

**Result 2 — the missing element is a FREQUENCY-DEPENDENT (HF) recirculation loss.** A grid over
(flat-leak depth × per-b3 one-pole-LP pole `a`) shows the P85 correlation is **insensitive to overall RT but
strongly driven by `a`**, peaking at **0.84 at `a`≈0.6–0.7** (corner ~1.6–2.7 kHz) — approaching the 0.92
real-vs-real ceiling. So adding HF damping to the recirculation takes the match 0.53 → 0.84.

**Result 3 — it produces a clean, stable, frequency-dependent decay.** The HF-damped model **decays** (no
growth, no limit cycle) and gives **HF ≪ LF** (HF ~4.5 kHz RT60 ≪ MID/LF), reproducing V7.2's documented
HF<LF (3.79 s/5.25 s). (`a`=0.7 over-damps HF ~11:1 vs V7.2's ~1.4:1 — the spectral metric rewards HF
flatness — so the physically-faithful value is gentler, `a`≈0.5, corr ~0.83; finalize during C++ calibration.)

**Reconciliation with §0.2/§0.6 (HFD inert; "HF lowpass refuted"):** both still hold and don't conflict —
the HF damping here is a **structural recirculation element**, NOT the HFD *parameter* (an input filter,
correctly inert on λ); and a per-closer LP **alone** can't stabilize (a lowpass passes the low-frequency
growth at gain 1) — it must ride on a small **flat** loss that handles stability, with the LP supplying the
HF *shape*. That pairing is exactly what matches P85.

**Conclusion / resolution.** The decay deficit = a missing **frequency-dependent recirculation damping**
(air-absorption-class HF loss) on top of a small flat loss that removes the ~1124 ppm structural excess. This
is **"Option 2" of the original fork, now strongly validated** (topology confirmed; HF<LF reproduced; 0.84
match vs the 0.92 ceiling). Its exact hardware origin remains the open item (480L-§8 hazard / an analog or
below-schematic element), but it is a **real, IR-validated mechanism, not an arbitrary leak**.

**Next:** (a) calibrate the loss — a one-pole (or high-shelf) HF damping `a`≈0.5 + a flat leak set to the 20 s
default λ — to jointly hit P85's spectrum and V7.2's HF/LF decay ratio; (b) implement in `ArithProfile`
(`libs/.../224xl.hpp`) as the documented frequency-dependent recirculation loss, keep the diff harness green;
(c) investigate the **~1.10 frequency scale** at best correlation (V7.2 best-scale 1.057; model 1.10) — a
possible native-Fs refinement (≈34130→~37500?) or a P85-config size difference — as a separate item.

---

## 0.9 SESSION 3c REFRAME — do NOT fudge a filter; find the mis-modeled crossover/band-split

The project owner pushed back on §0.8's "implement a one-pole" recommendation, correctly: if the Z80
emulation, the ARU datapath, and the firmware-built WCS are all faithful, the system is **fully
deterministic** — there is nothing to "add." The output is exactly what the firmware + ARU produce. **If our
model grows and the hardware decays, then one of those three is NOT actually faithful.** The one-pole that
matched P85 at 0.84 (§0.8) is a **diagnostic of the missing behavior's shape, not a real component.** This
section is the corrected framing and the concrete next-session plan.

**1. There is no analog hiding place — the missing loss MUST be in the firmware/ARU.** The recirculating tank
is entirely digital (DMEM → register → MAC → DMEM). It never touches the analog I/O (only the FPC input read
and the output writes do). So the decay cannot live in an analog element outside the WCS. → the deficit is a
**reconstruction error**, not a missing physical part. (This also kills the "calibrated leak / 480L-§8 analog
element" line as the primary answer.)

**2. What the decay IS, in the firmware.** A nested all-pass tank is lossless by construction; the CONCERT
decay is a **deliberate frequency-dependent damping filter inside the loop** — the **LOW / MID band decay
split by the XOV crossover** (params §6). That band-split *is* the decay mechanism. It is a one-pole/shelf
filter realized by specific WCS steps — the crossover region **s43–46 and s95–98**, including the documented
**"s45→s43 1-sample feedback"** (a 1-sample-delay feedback IS a one-pole filter).

**3. Smoking gun that it's MIS-MODELED, not missing.** In the firmware LOW/MID/XOV are *the* decay controls.
In our model they are nearly **impotent** (converged sweep, `exp_paramspace_conv.py`): only MID at its extreme
idx7 barely crosses unity (−87 ppm); **XOV makes it WORSE** (idx6 → +1888 ppm); LOW/HFD/DEP do essentially
nothing to λ. A correctly-realized band-split would sweep RT60 across a wide range with the default at 20 s.
Ours doesn't — **the decay filter is decoupled.** That is not a tiny arithmetic offset (which would leave the
params working, just shifted); it is the filter not filtering. The §0.8 one-pole (corner ~1.6 kHz) is almost
certainly the **same crossover filter the firmware already implements** and we are failing to reproduce.

**4. Answers to the three framing questions (owner, 2026-06-23):**
- *Why isn't it traceable?* It IS — we audited the **generic** datapath (MAC/sat/field-map/Z80 arithmetic) and
  it's faithful, but the band-split is a **short-delay feedback filter**, a knife-edge whose behavior depends
  on the exact coefficient, sign, **delay (±1 sample)**, and **intra-sample read/write ordering** of a few
  steps — none of which the multiplier diagnostic exercises (it tests only isolated MACs), and exactly where
  the schematic bit→pin wiring is at the scan's legibility limit. That one corner rests on inference.
- *Is it a parameter thing?* The parameter **values** are faithful (booted WCS = default, matches the sweep).
  What's broken is the parameter→damping **coupling** — the filter steps those params drive don't form a
  filter. Realization/topology error on the crossover steps, not wrong values.
- *Why add a one-pole?* We shouldn't. It would paper over the bug. The firmware already has that filter.

**5. THE NEXT STEP (deterministic root cause — do this instead of implementing any filter).** Trace the
crossover/band-split steps and find why sweeping their coefficients barely moves the loop decay:
  - Instrument **s43–46** and **s95–98** (and the closer blocks they feed): dump their exact decoded fields
    (offset/delay, coeff, CSIGN, RA, WA, b3, XFER, ZERO), the **actual DMEM addresses** they read/write each
    sample, and the **per-sample value flow** through them. Confirm whether they are *supposed* to form a
    damping one-pole / shelf (feedforward + short-delay feedback with matched-ish coefficients).
  - Identify the divergence — the likely culprits, in order:
    1. **The short delay is off by ±1 sample** (turns a one-pole into a different/zero-damping filter). Check
       the exact read vs write addresses of the s45↔s43 feedback against the position-increment timing.
    2. **A field-decode error specific to a 1-sample-feedback step** (e.g. RA or b3 on s45/s46) that routes
       the feedback to the wrong register/tap so the pole never forms. The field map is verbatim-from-ROM but
       the bit→FIELD assignment on these steps is the inferred part.
    3. **Intra-sample ordering** of the feedback read relative to its write (the filter needs y[n−1]; if it
       reads y[n] or y[n−2] the pole is wrong). Untestable by the MAC diagnostic.
  - Success criterion: a change that makes the **LOW/MID/XOV parameters actually control the loop decay**
    (sweep RT60 smoothly, default → ~20 s) — at which point the model decays with **no added filter** and the
    P85/V7.2 transfer-function match should reach the ~0.92 ceiling on its own.
  - Tools to build on: `tools/decode_microword.py`, `tools/echo_delays.py` (instruments actual recirculation
    delays), `tools/aru_datapath.run_trace`, and the §0.8 probes (`damp_probe.py`/`damp_grid.py`) as the
    validation oracle (the correct fix should reproduce the 0.84→0.92 match *without* the artificial LP).

**Status of §0.8's recommendation:** SUPERSEDED. Do **not** implement a calibrated one-pole in `ArithProfile`.
The §0.8 results stand as evidence (topology validated; the missing loss is frequency-dependent and
crossover-shaped), but the fix is to **repair the crossover/band-split realization**, not to add a filter.

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
