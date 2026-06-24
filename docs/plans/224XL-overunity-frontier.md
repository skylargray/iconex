# 224XL CONCERT over-unity — START HERE (decay frontier, after the 6-angle hunt)

**Status:** OPEN. The +1126 ppm over-unity is now fully characterized; **two digital structural leads remain,
both untested.** This doc is self-contained — read it, then go straight to §3 (the two tests).

Created end of Session 6 (2026-06-24). Full record: `docs/plans/224XL-concert-decay-investigation.md`
§0.10.10–§0.10.12. C++ core state: memory `224xl-cpp-scaffold`.

---

## 1. The problem in one paragraph

The booted-default CONCERT reverb, decoded from the v8.2.1 firmware into a 128-step WCS microprogram and run
through the bit-exact ARU datapath model (`tools/aru_datapath.py`), **GROWS** at a float linear eigenvalue
**λ ≈ 1.0011266 (+1126 ppm/sample, ~+333 dB/s)** instead of decaying to the hardware's RT60 ≈ 20 s
(target **λ = 0.9999899**, −10.1 ppm, from `IR/Lexicon 224XL/P85 - 20.0 Seconds A.wav`). Same firmware
coefficients, schematic-confirmed arithmetic — yet the model runs away and the hardware decays. The decay is
**digital by design** (a reverb's RT60 is set by its coefficients; it is NOT an analog-loss accident — the
project owner is firm on this and is correct).

## 2. THE finding (Session 6, 6-angle parallel hunt — all high-confidence)

**There is NO single bug. The over-unity is an EMERGENT COLLECTIVE eigenmode of the coupled all-pass bank.**
The loop-decomposition built the DMEM write→read graph: **24 nested Schroeder comb/all-pass cells**, and
**every individual cell is SUB-UNITY (max round-trip |g| = 0.83)** — each decays on its own. The +1126 ppm
appears only as the spectral radius of the *whole coupled system*: ~28 near-lossless all-pass cells (all
clustered at the **+124 → +0.969 all-pass feedback coefficient**) coupled through the **shared 4-word
register file** + overlapping DMEM. A correctly-coupled all-pass bank is stable; ours is collectively hot by
~1100 ppm. So the error is in the **coupling of individually-correct cells**, which is exactly why
element-by-element inspection found nothing.

**ELIMINATED — do NOT re-investigate (all high-confidence, Session 5–6):**
- λ is REAL & converged (4 independent methods: power-iter, matrix-free random-start PM ×2 seeds, long
  float64 impulse log-slope, L∞ peak-amplitude). The OUTPUT itself grows. Not a measurement artifact.
- NOT the field/bit decode (committed `RA=(b5,b4)` is uniquely the most reverb-like of ~50 re-decodes;
  every λ<1 re-decode is a degenerate dead-tank, λ≈0.0045).
- NOT a global gain bug — the ZERO/.5s-DELAY diagnostic passthrough is **exactly 1.00000000** (bit-exact).
- NOT the coefficient convention (floor/round/ceil/127-norm/no-shift/two's-comp/sign-flip all run *hotter*).
- NOT saturation value (±2^18, implemented), sample rate (per-sample λ), rounding/truncation, modulation
  (mode decoupled from the modulated taps, λ rate-invariant), de-zipper (settled image grows MORE).
- NOT FPC/DMEM addressing — SM §3.5: low 16 bits = full DMEM address, **no reserved bit15**; FPC + DMEM are
  separate strobe domains. Real FPC steps are λ-neutral dead-sinks.
- NOT register-file write gating — owner net-trace: **DAB WSTB/ → LS670 GW (pin 12) directly, ungated,
  writes every cycle**; R[3] stores normally; WA=3 is scratch but stored. The comb closers legitimately use
  WA=3/RA=3 as their feedback register.
- NO single principled change reaches decay: best off-by-one removes 16 ppm, best sign flip 185 ppm; only a
  uniform **~24% coefficient attenuation** (g*≈0.76) reaches λ=1 — too large for any off-by-one, and
  overfitting. (The earlier "11%" was an unsettled-impulse artifact; settled value is ~24%.)
- **Overfit trap (do NOT fall in):** several changes *do* flip to decay — WA=3-passthrough (−336 ppm),
  RA-reassignments, FPC-suppress, dropping step 94 — but EVERY one works by deleting *real, designed*
  feedback/taps (R[3] is the intended feedback register; step 94 is a genuine recirculation read; the bit15
  steps are real tank taps). These are "variant J"-style overfits, NOT fixes.

## 3. THE TWO REMAINING LEADS (both digital, both invisible to the diff harness because Python≡C++ share the assumption)

### LEAD 1 — All-pass coefficient MATCHING (software-testable NOW; prime suspect)

**Hypothesis:** the closer cells are meant to be **true lossless Schroeder all-passes** (|H(z)|=1). A Schroeder
all-pass `H(z) = (−g + z^−D)/(1 − g·z^−D)` is all-pass ONLY if the **feedforward magnitude == the feedback
magnitude == g**. If the model's feedforward coefficient `−c` does NOT equal the feedback `+0.969` for each
cell, each cell is slightly *active*, and ~28 coupled push the collective over unity. The field map shows the
closer blocks as `[−c, −small, −c, +0.976]` — the `+0.976`(≈+0.969) is the feedback `g`; the `−c` are the
feedforward. **If `c ≠ 0.969`, they're mismatched.** (Spot-check: block s58–61 has feedback `+124` (g=0.969)
but feedforward steps `−95` (0.734) — mismatched, if that −95 is the matching feedforward.)

**Exact test recipe:**
1. Identify the 24 cells from the write→read offset-match graph. **Reuse `tools/_hunt_loopgraph.py`** (it
   already found them). Closers (XFER+b3, coeff +124): s = 36,46,54,61,65,69,73,88,98,105,112,116,120,124;
   forward-writes: s = 39,60,64,68,72,91,111,115,119,123.
2. For each cell, pin its **feedback** coefficient (the +124 closer) and its **feedforward** coefficient(s)
   (the −c step(s) in the same ZERO-opened accumulation block feeding that closer). Work out the block
   structure from the step order + ZERO/XFER boundaries (`aru_datapath.load_microcode(0x01)` fields).
3. Check `|feedforward|` vs `|feedback|` per cell. True all-pass ⇒ matched.
4. **Decisive test:** modify the float model so each cell is an EXACT all-pass (feedforward = −(feedback
   magnitude)), and measure the collective λ (`exp_lambda_clean.lambda_trajectory`, converged tail median).
   **Does λ collapse to ≈1.000000 (lossless)?** If yes ⇒ the cells are designed-lossless and the
   feedforward/feedback mismatch is the over-unity source.
5. If λ→1.0: find WHY the decode mismatches — is the feedforward or feedback coeff mis-decoded (wrong
   value/sign/which-step), checkable against the raw firmware lane3 bytes? The designed 20 s decay is then a
   tiny additional in-loop loss (HFD / decay-time coefficient) on the now-lossless bank.

**Success criterion:** a *principled* structural correction (firmware/schematic-justified, not a hand-tuned
subset) that yields λ ≈ 0.99999 (or λ≈1.0 lossless + the decay param → 0.99999), that **survives the
diagnostic passthrough AND a second hall** (e.g. BRIGHT, DARK). Treat ANY decay result skeptically: re-run
the overfit check (does it delete real feedback? does it break another hall?).

### LEAD 2 — ARU pipeline / latch timing (needs a schematic/T&C trace)

**Hypothesis:** the collective eigenvalue is exquisitely sensitive to *when* RES and the registers latch
relative to the reads. The model assumes RES updates at XFER and is immediately available to the next
microstep (and read-before-write on the register file). If the hardware pipelines (e.g., RES/DMEM result
available one microstep *later* than the model assumes), the coupling — hence the collective eigenvalue —
changes. The diff harness can't catch this (Python and C++ use the same timing assumption).

**Exact test recipe:**
1. From the schematic + T&C (owner has full schematics; this is a *timing* trace, harder than the datapath
   chips): determine, within ONE microstep, the relative timing of: register-file read, the MAC, the
   accumulator clock **ARUCKE/**, the multiplier product-register clock **ARUCK**, the result-register latch
   **XFER CK** (74F374 U43/U44), the register-file write strobe **DAB WSTB/**, and the DMEM read/write
   (CAS on MEMAC). Key question: **is RES (and the DMEM write-back) available to the immediately-next
   microstep, or is there a pipeline stage/delay?**
2. In the model, test timing variants (RES read delayed 1 step; b3 write-back delayed; register write
   visible next-step-only; etc.) and measure λ. If a *physically-justified* pipeline timing yields λ≈1, that
   coupling correction is the fix.

**Success criterion:** same as Lead 1 — principled (matches the schematic timing), survives diagnostic +
second hall.

## 4. Files, tools, key numbers

- **Model:** `tools/aru_datapath.py` — `load_microcode(0x01)` → CONCERT prog (step dicts: s, offset, coeff,
  ZERO, b3, XFER, WA, b5, b4). `run()/run_trace()` = integer; the float linear map is in
  `tools/exp_lambda_clean.py:lambda_trajectory(prog, PICK, nsamp, K)` (PICK=`lambda st:(st['b5']<<1)|st['b4']`).
- **Float datapath (the eigenvalue's map):** `addr=(pos-offset)&0xFFFF; dab=RES if b3 else DM[addr];
  x=R[PICK]; R[WA]=dab; if ZERO:ACC=0; ACC+=x*8*Cs/64 (Cs=±(|coeff|>>1)); if XFER:RES=ACC/8; if b3:DM[addr]=RES`.
- **Session-6 hunt scratch (reuse these):** `tools/_hunt_loopgraph.py` (the 24-cell write→read graph),
  `_hunt_loopdecomp.py`, `_hunt_rtgain.py` (per-cell round-trip gain), `_hunt_minfix2.py` (single-change
  search), `_hunt_ctldecode.py` (field-decode sweep), `_hunt_coeffscale*.py` (4-method λ verification),
  `_hunt_diagunity*.py` (diagnostic passthrough = unity), `_hunt_fpcselect*.py`, `_hunt_assumptions.py`
  (the full single-assumption elimination sweep).
- **Numbers:** baseline λ=1.0011266 (+1126.7 ppm); target λ=0.9999899 (−10.1 ppm, RT60 20 s @ 34130 Hz);
  per-cell max round-trip |g|=0.83; closers cluster at +124 → Cs+62 → g=0.969; unity needs ~24% uniform
  coeff cut.
- **Gates (after any reference-model change, mirror to C++ + regen golden first — the golden dir reverts on
  env refresh):** `python tools/export_golden_224.py 0x01` → build `tools/harness/224xl` →
  `ctest` (2/2) + `diff_harness.exe golden 01` (DIFF PASSED) + `mult_vectors_test.exe` (ALL PASS).

## 5. The mindset (hard-won)

Two over-claims happened this session by getting ahead of the evidence. Rule: **a decay result is only real
if it (a) is a principled, firmware/schematic-justified structural correction, (b) survives the diagnostic
passthrough, and (c) survives a second hall** — otherwise it's an overfit that deleted real feedback. The
single-assumption space is fully eliminated; the answer is in the *coupling* (Lead 1 or Lead 2).
