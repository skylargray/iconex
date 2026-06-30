# 020 — 224XL complete whole-machine emulation (free-running, phase-accurate)

**Goal.** Build the plan-013 holistic vision *for real*: ONE free-running, phase-accurate, clocked model of the
whole 224XL DSP machine — **ARU + T&C + DMEM + FPC**, tied together by the real **DAB / strobes / clock** as the
netlist traces them — where the CONCERT reverb tail **EMERGES** from the wiring + the timing, not from hand-coded
behavioral logic. **Judged by a self-validating measurement harness that cannot silently lie (§ Metric).**

**Why now (the fork in the road).** The 100 CONCERT microwords are **PROVEN correct** (plan 019). The reverb still
doesn't form (single echo, not a dense tail). The **fidelity audit (2026-06-30)** established that NEITHER existing
emulator faithfully models the machine: **only the ARU Booth front-end is gate-level**; the T&C sequencer free-run,
the MS/AS sub-cycle phasing, the DMEM DRAM timing, the FPC, and the DAB bus are **behavioral / abstracted / omitted
in both**. A dense decaying tail *may* be an **emergent timing property** — 100 microinstructions feeding back through
a *properly-clocked* accumulator and a *properly-timed* delay memory every sample. **But that is a HYPOTHESIS, not a
fact** (see the two confounds below), so this plan is structured to *test* it cheaply before committing to the build,
and to *measure* the result with a harness proven against ground truth.

> **⚠ Two confounds this plan must control for (they sank earlier attempts):**
> 1. **Coefficient liveness.** The static CONCERT WCS is coefficient-sparse: steps **5–22 are `cmag=0` (multiply
>    OFF)** and the only recirculating taps with `cmag>0` are `{0,1,2,3,51}` (reads) + `{44,75,77,96}` (live writes)
>    (`tools/decode_concert_program.py`). `aru_freerun`'s own findings say densification "**likely needs the
>    per-frame LFO modulation AND/OR a feedback-timing refinement**." So "single echo" may be caused by *missing
>    coefficients/modulation*, **not** wrong timing. Timing fidelity alone may never produce a tail. The milestone
>    MUST vary this, not hold it fixed at "static/zero" (§ Milestone M3.X is a 2×2).
> 2. **Measurement integrity.** Past sessions reported "RT60 = N s / dense tail" that, on listening, were **100% dry**
>    — because they measured the **internal delay-memory energy (`buf_RMS`)**, not the **emitted D/A output**, with no
>    dry/wet control and no rendered WAV. **This is now the #1 risk and the reason the Metric section comes first.**

---

## Architecture decision
**EXTEND `tools/aru_rtl_dp.py` (+ `tools/aru_rtl.py`) to free-run. Do NOT promote `tools/aru_freerun.py`.**
The decisive reason: **`aru_rtl_dp` passes POST (E32/E40/E83/E91)**, so it carries the bedrock regression green
through every phase; `aru_freerun` does not pass POST at all. It also already holds the validated **M1 ClockEngine**
(`aru_rtl.py`: MS0-8/AS0-2/ARUCK/ARUCKE/DAB-RSTB waveforms, pixel-validated vs fig-3.2) and the **gate-level Booth
front-end** (`aru_booth.py`).
**Honesty about the graft:** `aru_freerun` is the one that already *free-runs* (100-step PC, §2T routing, recirc), so
the free-run **orchestration is a substantial NEW build on top of `aru_rtl_dp`'s single-step datapath**, not "mostly a
harvest." Budget Phase 2 accordingly. Keep `aru_freerun` as a behavioral oracle (do not delete) until the new model
supersedes it on POST + M3 + CONCERT.

## Already done — DO NOT rebuild
- `aru_rtl.py` — the M1 ClockEngine + validated MS/AS/ARUCK/ARUCKE/DAB-RSTB waveforms (vs fig-3.2).
- `aru_rtl_dp.py` — the M2 datapath: gate-level Booth front-end + behavioral back-end + single-bank DMEM, **POST-
  passing single-step**.
- `aru_booth.py` — the gate-level Booth array; 20/20 goldens.
- `aru_post.py` — the POST harness (E32/E40/E83/E91) + firmware driver; the BEDROCK regression.
- `boot8080.py` — the verified-core firmware boot → the 0x4000 WCS image + the SBC driver.

## HARVEST from `aru_freerun.py` — port, don't reinvent
- The **§2T device decode** (MEMR/MEMW/RD AD/WR DA/RDRREG/RD XREG/WR XREG + the SDAA-D one-hot-reversed channels).
- The **offset convention** (`addr = CPC + lanes + 1 = CPC − OFST`) — POST-grounded, settled.
- The **deferred-MAC + synchronous-clear (74LS163) understanding** — but now **ENFORCED BY EDGES** (the ClockEngine),
  not by Python statement order. This is the whole point of Phase 1.
- The **FPC float↔fixed math** (`fpc_input_float_to_fixed`/`fpc_output_fixed_to_float`).
- The PROVEN-WRONG things to NOT carry: the `for k in range(100)` PC, the atomic-dict DMEM, the value-passing DAB,
  **and any habit of reporting `buf_RMS` / internal energy as if it were the output.**

---

## ★★★ TEST STIMULUS — the defined input battery (what we inject; pinned + deterministic)

> "The input" must be ONE defined, reproducible battery used identically by Phase 0.5, the Milestone, and the metric's
> dry-gate — not "an impulse" in one place and "a noise burst" in another. The 224XL is fixed-point (saturation +
> quantization) and, with modulation on, time-varying — so the input **shape, LEVEL, channel, and injection point** all
> change the answer and must be fixed. Define a tiny deterministic generator `tools/stimulus.py`:

- **S1 — Calibrated unit impulse, LEVEL-SWEPT (primary; for the IR-based metrics).** One sample = `L`, then silence,
  for `L ∈ {−20, −12, −6, −1} dBFS` (sweep — do **not** pick one level). Injected at the **A/D input (`RD_AD`)** through
  PM-2's gain-ranging, never poked into an internal node. Yields the impulse response → RT60 (Schroeder), NED, EDC.
  The **level sweep is mandatory**: RT60/density that move with level localize **saturation/quantization (gain)**, not
  topology. Report per level.
- **S2 — Interrupted pseudo-random noise burst (cross-check; ISO-3382-style decay).** Seeded PRNG (the
  `aru_freerun.src`: ±8000 for `t < 0.30 s`, else 0; `fs=34130`); measure the post-burst decay. Independent,
  higher-SNR RT60. **S1 and S2 RT60 must agree within ±20 % or the verdict is `INDETERMINATE`.**
- **S3 — Modulation-phase ensemble (for any modulated-WCS run).** The modulated machine is time-varying → the IR
  depends on WHEN in the LFO cycle the impulse fires. Fire S1 at `N ≥ 8` evenly-spaced LFO phases; report the ensemble
  (median RT60/NED + spread). A single-phase modulated IR is not trusted.
- **Channels & provenance.** Specify the input channel and **measure each D/A output channel (A/B/C/D) separately** —
  the decode shows DRY-clobber on overlapping channels, so do not sum them blindly. Every stimulus is
  `(shape, level_dBFS, seed, fs, channel, lfo_phase)` — fully reproducible — and the **exact excitation array is what
  the metric's dry-gate subtracts and logs with the WAV** (P1/P3), so "what was injected" is never ambiguous.

## ★★★ THE METRIC — an error-proof reverb measurement harness (BUILD AND PROVE THIS FIRST)

> Every prior "RT60 = N s / dense tail" claim that turned out to be dry came from measuring the wrong signal with no
> ground-truth control. The fix is not a better formula — it is a harness that **physically cannot report reverb on a
> dry signal** and that **continuously re-proves itself against signals whose answer is known.** No CONCERT number is
> trusted until this harness passes its own calibration on the same run.

### Module: `tools/reverb_metrics.py` (+ self-test `tools/reverb_metrics_selftest.py`)

**Six non-negotiable principles (each kills a specific past failure):**

- **P1 — Measure ONLY the emitted output.** The harness's sole signal input is the exact int16 stream the machine
  sends to the **D/A (`WR DA/` captures)** — the *same array* written to the WAV. It is structurally forbidden from
  reading `buf_RMS`, the DMEM contents, an accumulator, or any internal node. *(Kills the `buf_RMS`-sustains-but-
  output-dry false positive.)*
- **P2 — Always emit the WAV + provenance, atomically with the number.** Every `analyze()` call writes a 16-bit WAV
  of the exact analyzed samples and records `sha256`, length, peak, RMS, fs. A reported metric is the triple
  **(number, WAV path, sha256)** — never a bare number. *(Makes every claim listenable and traceable.)*
  **WAV-naming rule (mandatory): every output WAV filename MUST start with a `YYYYMMDD-HHMMSS` timestamp**
  (date+time of the run), e.g. `20260630-184205_concertC_static_-6dBFS_chA.wav`. This makes renders sort chronologically,
  prevents silently overwriting a prior render, and ties each WAV to when it was produced. No WAV is written without
  the leading timestamp.
- **P3 — DRY-GATE FIRST; refuse to report reverb on a dry signal.** Before ANY RT60/density math, run the wetness
  gate (below). If it fails, the verdict is **`DRY`** and RT60/density return `N/A (dry)`. *(Kills "dry pulse reported
  as 2.6 s reverb" outright.)*
- **P4 — RT60 only when the decay is a clean exponential, else `INDETERMINATE`.** RT60 = the two ISO-3382 Schroeder
  measures **T20 and T30** on a **noise-floor-truncated** energy-decay curve (the reliable pair on real measured IRs),
  with a block-RMS envelope kept as a diagnostic cross-check. If the log-linear R² is poor, the clean decay range is
  insufficient, or T20/T30 disagree without a clean fallback, the verdict is **`INDETERMINATE`** with the reason —
  never a confident wrong number.
- **P5 — Self-calibrate against known controls on every run.** `analyze()` refuses to judge CONCERT unless the control
  battery (below) classifies correctly in the same process. A metric that can't tell dry from wet from a known-RT60
  reverb is broken and is not trusted for *anything*. *(This is what makes it error-proof.)*
- **P6 — Three-state, pre-registered verdicts** (`WET-PASS` / `FAIL` / `INDETERMINATE` / `DRY`) with thresholds fixed
  in the code, decided before looking at CONCERT.

**`analyze(output_int16, excitation_int16, fs, name) -> verdict`** — `excitation_int16` is always one of the
§ Test-stimulus arrays (S1/S2), never improvised. The pipeline, in order:

0. **Render + provenance (P2).** Write `name.wav` from `output_int16`; record sha/len/peak/RMS.
1. **Wetness / dry-gate (P3) — the most important guard.**
   - Estimate the dry/direct component: cross-correlate `output` with `excitation`, find lag `d` and best-fit gain
     `a`; `dry_hat[n] = a·excitation[n−d]`. `wet = output − dry_hat`.
   - `wetness = energy(wet) / energy(output)`.
   - `late_ratio = energy(output after excitation ends + 5 ms guard) / energy(output during excitation)`.
   - **If `wetness < 0.02` AND `late_ratio < −40 dB` → verdict `DRY`. STOP. Report "no reverb / passthrough."**
2. **Tail isolation.** Tail = output strictly after the excitation ends (S1 impulse: after the click; S2 burst: after
   the 0.30 s `burst_end`). All decay/density metrics use the TAIL only, never the direct sound.
3. **RT60 — ISO-3382 T20/T30 on a noise-floor-truncated EDC + quality gates (P4).**
   - Truncate the IR ~10 dB above its noise floor (Lundeby-lite) so the backward-integrated Schroeder curve doesn't
     bend up into the noise/fade tail (this is what lets a 20 s reverb in a 20 s file measure correctly).
   - **T30** = slope fit over **−5…−35 dB**; **T20** = over **−5…−25 dB**. Block-RMS envelope slope = diagnostic only
     (too noisy on real IRs to gate on).
   - **Quality gates:** R² ≥ 0.9 (log-linear = exponential = reverb-like); clean range ≥ 35 dB for T30 / ≥ 25 dB for
     T20; T20/T30 agree within ±20% (→ median) — else use T20 when its fit is clean (deep tail truncated), else
     `INDETERMINATE` with the reason. Validated on real IRs: 224XL Concert Hall → 2.5 s, the "20.0 Seconds" preset →
     19.8 s, halls/plates 0.7–2.3 s (see AC0-M).
4. **Echo density.**
   - **Abel–Huang Normalized Echo Density (NED)** profile: sliding-window fraction of samples beyond the window σ,
     normalized so fully-diffuse (Gaussian) → 1.0 and a lone echo → ~0. Report the NED(t) curve and the **mixing time**
     (time to reach NED ≥ 0.9). A dense tail reaches ~1 quickly; a single echo never does.
   - **Peak count/sec** in the tail above a threshold (single echo → ~1–2; dense → ≥ hundreds/sec).
   - **Density verdict:** `SPARSE` (single-echo) vs `DENSE` (diffuse), with the numbers.
5. **Smoothness / no-over-unity.** The smoothed EDC must be **monotonically non-increasing** within tolerance:
   measure its max positive slope; **energy GROWTH → `FAIL` (over-unity rail)**, never a positive RT60. Tail spectral
   flatness (a diffuse tail is broadband, not a ringing tone).
6. **Verdict (P6).** Combine into `DRY` / `INDETERMINATE` / `FAIL(over-unity)` / **`WET-PASS`** (wet + log-linear
   decay with measurable RT60 + `DENSE`), with every sub-number and the WAV triple attached.

### Self-calibration battery — `reverb_metrics_selftest.py` (P5; the trust anchor)
`analyze()` is run on synthetic signals with KNOWN answers; the harness is trusted **only if every control classifies
correctly**, and the CONCERT run *imports and asserts* this selftest first:

| control signal | required verdict | proves |
|---|---|---|
| dry impulse (click, no reverb) | `DRY` | dry-gate fires on a pure click |
| dry passthrough of a noise burst | `DRY` | dry-gate fires on sustained dry audio |
| single delay `x[n]+0.5·x[n−D]` | `WET` but **`SPARSE`**, RT60 `INDETERMINATE`/single-echo | won't call one echo a reverb tail |
| synthetic exp-decay noise reverb, **RT60 ∈ {0.8, 2.6, 5.0}s** | `WET-PASS`, **RT60 within ±15 %**, `DENSE` | the RT60 estimator is actually correct |
| growing feedback (gain > 1) | `FAIL (over-unity)` | never reports a positive RT60 on a runaway |
| silence | `INDETERMINATE` (empty) | never invents a number from noise |

**If any control is mis-classified, the metric is broken — fix it before measuring CONCERT. No exceptions.**
This battery is itself part of AC0-M (below) and runs at the top of every CONCERT measurement.

**Beyond the synthetic controls, the harness is validated on (a) a REAL reverb ALGORITHM** — a Freeverb /
Schroeder–Moorer network with analytic RT60 (`tools/reverb_metrics_realtest.py`; this is what caught and fixed an
early spectral-flatness tonality bug that misread comb-colored reverbs) — **and (b) REAL measured impulse responses
from `IR/`** including the actual target, the **Lexicon 224XL Concert Hall** (`tools/reverb_metrics_irtest.py`). The
224XL Concert Hall measures `WET-PASS / DENSE`, **RT60 ≈ 2.5 s** (corroborating the ch.8 ~2.6 s spec), the "20.0
Seconds" preset → 19.8 s, and halls/plates 0.7–2.3 s — so the metric is proven to report the right answer on genuine
reverbs with real-world features (comb coloration, early reflections, frequency-dependent decay, measurement noise
floor), not just ideal synthetic decays.

### Listening cross-check (the human ground truth)
The harness always renders the WAV (P2, with the mandatory `YYYYMMDD-HHMMSS` timestamp prefix). At the milestone and
final, **the WAV is the artifact of record** — the number is reported next to the file the owner can listen to. The
render path (`tools/render_wav.py`) consumes the SAME `output_int16` array `analyze()` does (assert identical sha) and
follows the same timestamped naming, so what is measured == what is heard == what is written. No claim of "tail" is
made without the listenable file behind it.

---

## Phase 0 — Baseline, metric harness, and free-run scaffold
0.1. Confirm `python tools/aru_post.py` → E32/E40/E83/E91 all PASS today (the bedrock). Record it.
0.2. **Build `tools/stimulus.py` (the § Test-stimulus S1/S2/S3 battery) + `tools/reverb_metrics.py` +
   `reverb_metrics_selftest.py`, and pass the full control battery (§ Metric). This is a gate: do it before any audio
   claim.** (AC0-M.)
0.3. Stand up `tools/aru_whole.py` (new) to host the free-running machine (ClockEngine + datapath + Booth) with a
   free-run scaffold: load a WCS image, run N samples, **capture the A/D→D/A output stream** (the `WR DA/` samples)
   for the metric. Keep `aru_freerun.py` as the behavioral reference (do not delete).

## Phase 0.5 — ★ Cheap discriminating experiments (localize the cause BEFORE the expensive rebuild)
> The three real unknowns — **what `cmag=0` does**, **whether modulation is required for density**, **DAB
> arbitration** — are NOT "timing fidelity" and can be probed in hours on the *existing* free-running `aru_freerun`,
> measured by the now-proven harness. This can de-risk or even re-scope the whole rebuild.
> **All renders below use the § Test-stimulus battery (S1 level-swept + S2), measured by `reverb_metrics`.**
0.5.1. **Coefficient probe:** on `aru_freerun`, force non-zero `cmag` into the steps 5–22 block (and/or the `{0,1,2,3,
   51}` taps) and render. Does density appear? → tells you whether the static zeros are the blocker.
0.5.2. **Modulation probe:** apply the per-frame modulation stream (the LFO rewrites to taps `[42,56,57,62–68,94,
   107–119]`) over a render. Does density appear *without* any timing change? → tells you whether modulation is the
   lever, independent of Phases 1–3.
0.5.3. **Loop-gain probe:** sweep an overall feedback gain; find the decay↔over-unity boundary. → tells you whether
   the issue is gain/scaling (an FPC concern) vs topology.
0.5.4. **Decision gate:** record which lever (timing / coefficients / modulation / gain) moves density on the existing
   engine. If density needs **coefficients or modulation**, treat the timing rebuild as *necessary-but-not-sufficient*
   and carry a modulated WCS into every later test. If **nothing** densifies even with non-zero coeffs + modulation,
   STOP and re-open the `cmag=0`/PROT semantics (plan 016) before building anything.

## Phase 1 — Edge-drive the datapath [makes XFER/ZERO/accumulate EDGES, not statements]
1.1. Run the datapath on `aru_rtl.ClockEngine` edges. fig-3.4 3-phase MAC: partial products at i2.AS0-2; accumulate
   i2.AS1→i3.AS0; **ZERO/ at i2.AS0 = the 74LS163 SYNCHRONOUS clear (fires on next ARUCKE/ edge), XFER CK at i2.AS0
   (~20–40 ns after ZERO/, captures BEFORE the clear lands)** — wired to the real strobes (§6T.4: XFER CK =
   NAND(AS0,XFER,…); ZERO/ = NAND(MI25,AS0)), not to statement order.
1.2. Accumulator (`aru_U45-49`, 163) clocks on ARUCKE/, SR̄/CLR = ZERO/ (sync). Result reg (`aru_U43/44`, 374) clocks
   on XFER CK. Both driven from the ClockEngine.
1.3. **VERIFY: `aru_post.py` E32/E40/E83/E91 still PASS** with the edge-driven datapath (single-step).
1.4. **VERIFY: cmag=63 +3 goldens still reproduce** (`aru_cycaccurate.py` / the 20 Booth goldens).
1.5. **★ Edge-wiring faithfulness battery (anti-"faithfully wrong"):** the edge-driven deferred-MAC must reproduce
   `aru_freerun`'s statement-order RES across a randomized sweep of `(x, cmag, csign, XFER, ZERO)` — POST (steps
   126/127) + 20 goldens are too narrow to certify the edge wiring alone. Hand-traces had confirmed errors (§4F.4);
   pixel-validating waveforms proves shapes, not that strobes hit the right elements.

## Phase 2 — T&C microsequencer free-run [all steps fetch real microwords on real edges]
2.0. **RESOLVE THE PROGRAM LENGTH FIRST.** The 0x4000–0x41FF image is **128 steps** (512 B/4), `decode_concert_program`
   decodes only `range(100)`, and the modulation finding touches taps **107–119 (>99)**. Phase 2.1 assumes "RESET@99 /
   0→99". These conflict: if the PC resets at 99, steps 100–127 never run and modulation to 107–119 is meaningless; if
   those steps are real, the modulus ≠ 99. **Pin the true WCS PC modulus (from §3.5 + observing the firmware) before
   wiring the counter** — it defines the entire program.
2.1. Instantiate the WCS PC (§3.5: `tc_U14/U1` 163×2, counts on **DAB RSTB/**, RESET at the value fixed in 2.0,
   ENT=HALT/). Replace the single-step 126/127 selection with the PC sweeping the full program, fetching each 32-bit
   microword from the 0x4000 image.
2.2. Wire the offset latch (§3.6), control-field regs (§3.7), coeff serializers (§3.9, U10/U11), CSIGN JK (§3.10) so
   each fetched microword drives the datapath through the traced T&C path (harvest §2T device-decode for strobes).
2.3. **VERIFY: keep a bypassable single-step mode so `aru_post.py` STILL PASSES** (POST drives one microword via the
   SBC; specify the PC-source mux, HALT//ENT, preserving the 126/127 path exactly). Then **VERIFY free-run executes
   the full program** with correct per-step phasing (CPC advances once/sample at RESET).
2.4. **VERIFY M3 capability tests** (port `test_zero_delay`/`test_max_delay`/`test_feedback_comb` from `aru_freerun`):
   the free-run datapath must reproduce a clean comb `y[n]=x[n]+0.5·y[n−D]` — **measured by `reverb_metrics`, which
   must classify it `WET / SPARSE`** (a known single-tap loop, not a dense tail).
2.5. **★ Free-run regression oracle (POST is blind here):** POST only exercises steps 126/127 — it can stay green
   while free-run phasing is wrong. Add a per-sample, per-step **DAB/RES trace cross-checked vs `aru_freerun` on the
   SETTLED quantities** (device decode, offset, single-tap recirc) and pre-declare the **expected divergence** (the
   multi-step timed accumulation — the whole point). Add a **passivity bound** (no energy growth on a decaying input).

## Phase 3 — DMEM DRAM timing [recirculation becomes a TIMED cycle, not a dict index]
3.1. CPC counter (§5.1: `dmem_U51/U65` 393, +1/sample at RESET), offset adders (§5.2: `283`, `addr=CPC+OFST/+1`),
   row/col mux (§5.4: `157`).
3.2. DL6308 RAS/CAS/ROW-SEL sequencer (§6D / fig-3.3: RAS@MS2, CAS@MS4 only when MEMAC, DOUT ~MS7 strobed by DAB WSTB/,
   DIN from result reg) over the 4164 array (§5.5). Read-before-write is a **timed DRAM cycle** (old → DAB before the
   new value writes). *(Note: fig-3.3 trust level — mark whether it is owner-hand-traced or auto-read, §Hygiene.)*
3.3. **VERIFY: `aru_post.py` E91 (DMEM test) still PASSES** with the timed DRAM model.
3.4. **VERIFY timed recirculation** via the M3 max-delay/feedback-comb tests through the timed DMEM (metric: `WET /
   SPARSE`, correct delay).

### ★ Pre-milestone prerequisites (pull the confounds in FRONT of the go/no-go)
The milestone must not run on models the plan itself distrusts, or it will mis-attribute a failure:
- **PM-1 DAB arbitration (don't leave it for Phase 6):** the plan calls value-passing DAB *proven wrong* and names DAB
  arbitration a prime fail-suspect — so a **correct single-driver-per-phase DAB** (not necessarily gate-level yet:
  exactly one of RDRREG//MEMR//RD AD//RD XREG//FPC enabled per phase, receivers latched by WSTB//RSTB) must be in
  place **before M3.X**. Else the feedback path the tail rides on is built on a known-wrong bus.
- **PM-2 Minimal FPC scaling (gain-ranging) before M3.X:** tail density/decay is loop-gain dependent (saturation,
  quantization). A bare impulse bypassing the FPC float↔fixed gain-ranging can give the wrong loop gain. Insert a
  **minimal (even behavioral) FPC input/output scaling** so the excitation enters and the output leaves at realistic
  levels; the full gate FPC is Phase 4. Document any remaining bypass as a known confound on the milestone.

### ★ Benchmark reference IR — the de-facto CONCERT target (NEW, 2026-06-30)
For the first time the project has a concrete reference to compare the emulator's CONCERT output against **without a
physical unit**: **`IR/Lexicon 224XL/Concert Hall V1.1.L.wav`** — identified by the owner as the default 224XL
**CONCERT (Concert Hall)** program. Two things converged to make this usable: plan 019 PROVED the loaded CONCERT
microwords are genuine, and this harness now measures that IR as `WET-PASS / DENSE`, **RT60 ≈ 2.5 s**, corroborating
the ch.8 CONCERT spec (~2.6 s). The long-standing blocker ("which IR is the default Concert Hall?") is resolved, so
this is the strongest available proxy for the target sound.

- **USE (when appropriate): a STRUCTURAL benchmark.** Compare the emulator's CONCERT impulse response to this reference
  on the metric's own quantities — **RT60, NED echo-density / mixing time, the Schroeder EDC shape, the spectral
  decay** — for a quantitative similarity check, not merely "is there a plausible tail." This upgrades AC4 from
  "plausible RT" to "**matches the reference IR's RT60 + density within tolerance.**"
- **HONESTY / what it is NOT.** It is a third-party capture (not the owner's own unit; the exact variation/parameter
  settings and capture chain are unverified), so it is a **structural reference, not bit-exact L7 ground truth.** A
  true L7 (sample-exact IR match) still needs the physical unit or a provenance-verified WCS/IR dump. Do not claim L7
  from this file — use it for shape/RT60/density similarity, with the WAV always rendered alongside for listening.

### ★★ MILESTONE M3.X — DOES THE CONCERT TAIL EMERGE? (a 2×2, not a single render)
After Phases 1–3 + PM-1/PM-2, **free-run the § Test-stimulus battery (S1 level-swept + S2; S3 phase-ensemble for the
modulated cells) through the four conditions** and measure every D/A output channel with `reverb_metrics` (proven on
its control battery first, P5), keeping the rendered WAVs:

| | behavioral `aru_freerun` | new timed model |
|---|---|---|
| **static WCS** | baseline (expected single echo) | **cell A** |
| **modulation-applied WCS** | **cell B** | **cell C** |

**Pre-registered decision (thresholds from § Metric — fixed before running):**
- **Cell C is `WET-PASS / DENSE` with a plausible RT60** — and ideally **structurally comparable to the benchmark
  reference IR** (RT60 ≈ 2.5 s, NED/EDC shape in the same ballpark) → the timing-faithful model + live coefficients
  produce the tail. Thesis confirmed; proceed to Phase 4–6 to complete fidelity and validate RT60 against the reference.
- **Timed model densifies where `aru_freerun` does not (A or C beats its behavioral counterpart)** → timing is *a*
  lever; keep going, note how much it contributed.
- **Only the modulated column (B/C) densifies, on EITHER engine** → the lever is **coefficients/modulation, not
  timing**; re-scope — modulation co-sim becomes primary and the gate-level Phases 5–6 are deferred/optional.
- **Nothing densifies in any cell** → **STOP.** Do not build Phase 4–6. Re-open `cmag=0`/PROT semantics (plan 016)
  and DAB arbitration with the now-timed model + proven metric as the sharper probe.
> Note: every cell reports the metric's three-state verdict + the WAV. A "DENSE" claim that the owner plays and hears
> as dry is, by construction (P1–P3, P5), impossible to emit here — if it ever happens, the harness is the bug.

## Phase 4 — FPC as components + AIN/AOUT boundary  *(full gate version; minimal scaling already in PM-2)*
4.1. Instantiate the FPC datapath from the pinout (`224XL FPC pinouts from 060-01320.txt`) + fig-3.5/3.6: input cycle
   counter + seq ROM, SAR/IGA float→fixed (U16/U27/U28/U38/U39), OGA/GSA fixed→float (U23/24/34/35/U43), the
   **double-buffer (U36/U37 value + U40/U41 select)** and the **BUSY-gated strobe counter (U1/U2, 0x2A→0x40) + mux U42
   + U3 OUT strobe**.
4.2. This replaces the cadence-guessed BUSY model with the **gate-grounded** output double-buffer (resolves the
   output-clobber on real timing, not a tuned `busy_dur`). **Also test the distinct hypothesis** that the DRY-clobber
   (decode steps `{58,62,63,70}`) is a **channel-routing/microword-semantics** issue, not just BUSY timing.
4.3. **VERIFY** audio I/O: impulse in → correct gain-ranged fixed value to the DSP; DSP result → correct BUSY-gated D/A
   per channel (metric on the emitted output).

## Phase 5 — Gate-level ARU back-end  *(CONDITIONAL — see performance rule)*
5.1. Instantiate the behavioral ARU back-end as gates: accumulator adder chain (§4.3, 283×5), sat-mux (§4.4, 157×5),
   saturation (§4.5, `aru_U42` XOR + `aru_U2` clamp), subtract-XOR row (§4.6, 86×5), result reg (§4.8, 374×2),
   accumulator reg (§4.9, 163×5 + ZERO/ sync clear).
5.2. **VERIFY: POST still PASSES**; the datapath is fully gate-level.
> **Only do Phase 5 where the audit/Milestone shows the behavioral back-end changes the AUDIO** (per the performance
> rule). If Cell C already produces the correct tail, gate-leveling a back-end that already matches POST + the metric
> is completeness, not necessity — schedule it as such.

## Phase 6 — Cross-module interconnect + integration  *(DAB resolution already done in PM-1)*
6.1. Promote PM-1's DAB to the **full resolved tri-state bus** if not already, and wire the cross-module
   interconnections as the netlist traces them: the MI0-31 microword bus, OFST0-15/, the strobe set (§6T),
   CPC/RESET/CPC-CLR, the FPC↔T&C timing (FPC CK/RESET//RD AD//WR DA//SDAA-D), the SBC↔DAB X-register bridge.
6.2. **Full integration:** the whole machine free-runs; the SBC firmware can still drive single-step (POST) AND the
   T&C runs free for audio.
6.3. **FINAL VERIFY:** POST green; M3 capability tests green; **CONCERT produces a dense decaying tail** —
   `reverb_metrics` `WET-PASS / DENSE` with plausible RT60, **and the rendered WAV audibly reverberant** (owner
   listen).

---

## Performance budget & "minimum fidelity" rule  *(new — the build must be runnable)*
The ClockEngine walks **~9 MS phases / microinstruction** → ~`steps × 9` engine-steps per sample. At 34130 Hz a
~4 s impulse (needed to *see* an RT60≈2.6 s tail) is ~150k samples → **~10⁸ engine-steps**; a full gate back-end
multiplies each by hundreds of gate evals → **10¹⁰–10¹¹ Python ops → hours-to-days per render.** The milestone must
run in **minutes**. Therefore:
- **Budget:** M3.X render ≤ a few minutes wall-clock; final renders ≤ ~1 hour. State and check it.
- **Strategy:** memoize combinational blocks keyed on their inputs; vectorize where the structure allows; keep
  **gate-level ONLY where the fidelity audit shows the abstraction changes the audio** (everything else stays
  edge-disciplined but behavioral); optional Cython/C hot path if needed.
- **Rule:** **Phases 5–6 gate-leveling is CONDITIONAL on an observed audio discrepancy**, not mandatory completeness.
  "Minimum fidelity to reproduce the phenomenon" governs; AC3 documents anything left deliberately abstracted.

## Acceptance criteria
- **AC0 (regression, every phase):** `aru_post.py` E32/E40/E83/E91 PASS throughout. Non-negotiable.
- **AC0-M (metric integrity, before any audio claim):** `reverb_metrics_selftest.py` passes the full control battery
  (dry→`DRY`, single-echo→`SPARSE`, known-RT60→within ±15 %, over-unity→`FAIL`, silence→`INDETERMINATE`, tone→`TONAL`);
  AND the metric is validated on a real reverb algorithm (`reverb_metrics_realtest.py`) and real IRs incl. the 224XL
  Concert Hall (`reverb_metrics_irtest.py`). Re-run the control battery at the top of every CONCERT measurement.
  **No audio metric is reported unless this passed in the same process.** [DONE — all three suites green 2026-06-30.]
- **AC1 (M3 capability):** ported `test_zero_delay`/`test_max_delay`/`test_feedback_comb` classify `WET / SPARSE` with
  the correct delay on the free-run model.
- **AC2 (the hypothesis, 2×2):** Milestone M3.X — at least the modulated timed cell (C) yields `WET-PASS / DENSE`, and
  the result localizes the lever (timing vs coefficients vs modulation) per the decision table.
- **AC3 (completeness, scoped by performance rule):** the audio-relevant ARU+T&C+DMEM+FPC is gate/phase-accurate where
  it matters; the DAB is a resolved bus; every fidelity-audit "behavioral/abstracted/omitted" cell is upgraded **or
  documented as deliberately abstracted with justification.**
- **AC4 (structural reverb):** under the § Test-stimulus battery (S1 level-swept + S2 agreeing within ±20 %), CONCERT's
  tail is `WET-PASS / DENSE`, no over-unity rail, **and the WAV is audibly reverberant**, with an RT60 in the right
  ballpark for CONCERT — the **measured 224XL Concert Hall IR (`IR/Lexicon 224XL/Concert Hall V1.1`) reads RT60 ≈ 2.5 s**
  via this very harness (and the ch.8 spec says ~2.6 s), so that is the concrete structural target. STRUCTURAL
  acceptance only (see ceiling): a plausible measured-style RT60 + dense diffuse tail, NOT a bit-exact IR match.

## The ceiling (state it plainly)
**A bit-exact L7 IR match still needs the physical unit** (or a provenance-verified dump), which is unavailable — so
AC4 is a **STRUCTURAL** acceptance (a dense, smoothly-decaying, audibly-reverberant tail with a plausible RT60 and no
over-unity rail), **not** a sample-exact IR match. What HAS changed (2026-06-30): we now have a **de-facto CONCERT
reference IR** (`IR/Lexicon 224XL/Concert Hall V1.1.L.wav`, RT60 ≈ 2.5 s) to benchmark the *structure* against
(RT60 / echo-density / EDC shape / spectral decay) — a real, quantitative target the project lacked before, even
though it is a third-party capture rather than the owner's own unit. Do not claim L7 from it. Once the model produces
the tail it also becomes the oracle for the per-frame LFO/offset modulation and multi-program coverage.

## Recommended order & ground rules
- **Order:** Phase 0 (incl. the metric harness) → **Phase 0.5 discriminating experiments** → 1 → 2 → 3 → PM-1/PM-2 →
  **Milestone M3.X (2×2)** → then 4 → 5 → 6 (5–6 conditional per the performance rule).
- **Metric first, always.** No "tail/RT60/density" statement is made except as a `reverb_metrics` three-state verdict
  on the **emitted D/A output**, driven by the **§ Test-stimulus battery** (S1 level-swept + S2; S3 when modulated),
  with the WAV attached and the control battery passed in the same run. Never report `buf_RMS` / internal energy as
  output, and never improvise a one-off input.
- **POST green at EVERY phase**; POST is necessary but **blind to free-run timing** — also keep the Phase-2.5 free-run
  oracle + passivity bound green.
- **Harvest, don't reinvent** (device decode, FPC math, offset convention) — but budget Phase 2's free-run
  orchestration as a real new build.
- **Keep `aru_freerun.py`** as the behavioral reference until the new model supersedes it on POST + M3 + CONCERT.
- **If Milestone M3.X says "coefficients/modulation, not timing,"** re-scope to modulation co-sim and defer the gate
  back-end; **if "nothing densifies," STOP** and re-open `cmag=0`/PROT (plan 016) — do not push on to Phase 4–6.

## Hygiene / provenance to fix while editing
- The fidelity audit is currently only a **scratchpad task id (`w4zhz093x`)** — ephemeral. Capture its conclusions in
  a durable doc; this plan's whole premise rests on it.
- Mark each timing figure used (fig-3.3 DRAM, fig-3.5/3.6 FPC) as **owner-hand-traced vs auto-read** — auto-reads are
  flagged unreliable and Phases 3–4 depend on exactly these.
- Define AC4's decay target precisely (source + RT60-vs-"avg decay").

## Key tools / netlist sections (quick reference)
- Build base: `tools/aru_rtl.py` (ClockEngine), `tools/aru_rtl_dp.py` (datapath), `tools/aru_booth.py` (Booth),
  `tools/aru_post.py` (POST + driver), `tools/boot8080.py` (WCS image). New: `tools/aru_whole.py`,
  **`tools/reverb_metrics.py` + `tools/reverb_metrics_selftest.py`** (the measurement gate) + `reverb_metrics_realtest.py`
  (Freeverb validation) + `reverb_metrics_irtest.py` (real-IR validation incl. 224XL Concert Hall), **`tools/stimulus.py`**
  (the defined S1/S2/S3 input battery), `tools/render_wav.py`. Real IRs live under `IR/` (read via `soundfile`).
- Harvest: `tools/aru_freerun.py` (§2T decode, FPC codec, conventions, behavioral oracle).
- Netlist: `docs/reference/224/224XL_interconnect_netlist.md` — ARU §4/§4F, T&C §2T/§3/§6T, DMEM §5/§6D.
- Timing: `docs/reference/224/224XL_timing_spec.md` (figs 3.2–3.6). FPC: `224XL FPC pinouts from 060-01320.txt`.
- Decode/coeffs: `tools/decode_concert_program.py` (static WCS coeff map: `cmag=0` steps 5–22; recirc taps).
- Vision/context: `docs/plans/013` (holistic), `019` (microwords proven), `016` (cmag=0/PROT crux),
  `224XL_microword_verification_results.md`, [[224xl-m4-output-path-and-static-wcs]] (modulation taps; the audit).
