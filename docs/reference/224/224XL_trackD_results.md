# 224XL Track D — Internal-Consistency Validation Across All 20 Programs

**Plan:** `docs/plans/224XL-validation-plan.md` Track D (cross-program consistency)
**Pipeline under test:** `tools/aru224_emulate.py` `A.tap_map(recbase, cce=…)` (128 signed-16 offset words) + `A.capture_coeffs(recbase)` (DE,byte gain pairs); bases from `tools/harvest_xl.py` `H.record_bases()[:20]`.
**Foundation (taken as CONFIRMED, not re-derived):** physical delay = +offset in the sensible band (addr = CPC − offset); negatives are special/sentinel tap-types; coeff byte bit7=CSIGN, bits0–6 = magnitude/127; SIZE enters as cce byte at 0x3CCE; DMEM = 64K-word, wrap = 65536 samples = 1.9202 s @ 34.13 kHz.
**Cardinal rule:** plausible ≠ verified — every headline below was independently re-extracted and the numbers shown.

---

## Overall verdict

**The validated decode PASSES internal consistency at the structural and physical-bounds level across all 20 programs, and STRAINS on three overstated quantitative sub-claims plus one metric-definition fragility.** All four sub-tasks were independently re-run; the **data layer reproduces 100%** (D1 table, D2 table, D3 table, D4 CONCERT/PLATE series all matched byte-for-byte on re-extraction). The strains are wording/precision overstatements layered on sound data, not decode failures.

| Task | Headline | Reproduces? | Verdict |
|------|----------|-------------|---------|
| D1 monotonic structural scaling | Family predicts tap-density + coeff profile; plate=short+dense-early CONFIRMED; room<hall REFUTED at face value; no global monotonic size axis | 100% | **holds, 2 claims downgraded** |
| D2 physical bounds | 0 hard violations (no delay ≥ wrap; no coeff > rail) across all 20 | 100% | **holds** |
| D3 FE vs non-FE structure | Both paths exhibit predelay→recirc→multitap, 10/10 each; neither anomalous | 100% | **holds, 1 claim downgraded** |
| D4 SIZE param sweep | FE offsets scale monotone with SIZE; non-FE invariant; gains/ccf untouched | core 100% | **holds qualitatively, precision claim refuted** |

---

## D1 — Monotonic structural scaling (HOLDS; two CONFIRMED claims downgraded)

The per-program structural metrics (recirc = most-reused positive in-band tap, tap counts, max delay, early-tap density, mean/max |c|) reproduce exactly, and the core ordering conclusions stand:

- **Plate signature CONFIRMED:** classic single plates have the shortest recirc loops AND densest early field (PLATE 20.7 ms / 25 early; CD PLATE A 29.6 ms / 17; PLATE/CHORUS 45.0 ms / 33) vs halls/chambers 138–300 ms. Plates are genuinely distinct.
- **room < hall REFUTED at face value:** SMALL ROOM 194.9 ms and INVERSE ROOM 259.8 ms exceed DARK HALL 138.3 ms — but these are algorithmically different (gated/inverse, pre-baked), so not a contradiction. INFERRED.
- **No single global monotonic size axis:** 5 dual-engine SPLIT/RICH/CD variants make the single-tap recirc metric an unreliable size proxy; family predicts tap-density + coeff profile well, recirc length only within the single-engine subset.
- **Negative-sentinel contamination CONFIRMED:** the old name-map "recirc loop" column counted shared negative sentinels (−12289 in 20/20, −1 in 20/20, −4097 in 19/20, −12353 in 15/20) — these are write-tap/sentinel markers, not per-program loops.

**Downgrades (independently verified):**
- **Claim 1 "byte-identical structure" → INFERRED/corrected.** CONCERT(0xB800) and BRIGHT(0xC554) full 128-word arrays differ at **10 of 128 positions** (e.g. pos32 258↔261, pos33 6008↔258, pos85 −29765↔256). What IS identical is the **in-band positive-tap multiset** (verified equal → recirc 6008, #taps, maxd, early all match). Correct wording: "identical in-band positive-tap multiset," not "byte-identical."
- **Claim 6 "19/20 reach unity, M BAND DELAY lone outlier" → corrected to 18/20.** Independently, **two** programs are sub-unity: **CHAMBER (max |c| = 0.976 = 124/127)** and **M BAND DELAY (0.843 = 107/127)**. The finding's own table lists CHAMBER 0.976, contradicting its "19/20" prose. M BAND DELAY remains the extreme **mean** |c| outlier (0.490).

**Methodological fragility (caveat, not refutation):** the recirc tie-break ("first occurrence in step order among most-reused in-band taps") is load-bearing and only this undocumented rule reproduces all 20 values. DARK HALL (2745 and 4722 both at count 4) and CHAMBER (10217 vs 14809) rest on a coin-flip tie-break — the "DARK HALL shorter loop" narrative is metric-fragile.

---

## D2 — Physical-sanity bounds (HOLDS, clean)

Strongest sub-task. Reproduced column-for-column across all 20 records.

- **(a) Wrap bound:** every active (positive) delay < 65536 samples; **0 over-wrap violations**; global max active offset = 32687 (RICH SPLIT) = 957.7 ms, well under the 1.9202 s wrap. **Stronger than the finding:** sweeping cce 0..0xFF (max SIZE), worst-case active offset only reaches 32735 — still far under wrap. The cce=0-only scope does NOT break the bound.
- **(b) Coefficient rail:** global max magnitude byte = 127 → |gain| = 1.0; **0 over-127**. Honestly framed: over-rail is **structurally impossible** by 7-bit field width (byte&0x7f ≤ 127), a property of the field, not a hard-won empirical pass — correct per the cardinal rule.
- **(c) +1.000 cross-check:** records with a +1.000 tap = [11,12,15,16,17,18,19], matching `224XL_record_name_map.md` exactly; rec3 CHAMBER (no −1.000, max +0.976) and rec14 M BAND DELAY (no −1.000, max −0.843) also match.
- **(d) Write-region minority:** taps >16383 are a small minority (CONCERT 2/92, PLATE/CHORUS 17/82, RICH SPLIT 16/70) = recirculating-tank write region (the "large write-offset" cluster). PARTIAL: counts verified independently, semantic label rests on the doc note.
- **(e) Special-tap distribution:** −1 sentinels 18–33/record (outliers RES CHORDS 70, M BAND DELAY 48, both sparse); recurring shared negspec set (−12353,−12289,−6273/−6529,−4097…) in nearly every record; paired large-negatives (~−28k..−32.7k) in FE-path records.

**TOTAL hard violations (active ≥ wrap OR mag > 127) = 0**, reproduced independently. Presentation nit: the "active" column counts all positive offsets including the >16383 write region — rename to "positive-offset count" for clarity; both definitions yield 0 violations.

---

## D3 — FE vs non-FE structural agreement (HOLDS; reconciliation claim refuted-as-stated)

- **Split CONFIRMED:** 10 FE (marker 0xFE: B800,BAAA,BD54,C554,CAAA,E000,E2AA,E554,E800,EAAA) / 10 non-FE (0xFF: C000,C2AA,C800,CD54,D000,D2AA,D554,D800,DAAA,DD54).
- **Structural KIND CONFIRMED:** all 20 programs in BOTH classes exhibit predelay (20/20), recurring recirc loop n≥2 (20/20; FE min n=4, nonFE min n=3), and output multi-tap increasing-run ≥4 (20/20; FE min run=4, nonFE min run=5). Every per-program cell (pre, loopmag, n, run) reproduced exactly, including the odd ones (PLATE pre=128, CHAMBER pre=2047, SMALL ROOM pre=90 are genuine smallest in-band taps). **Neither build path yields a structurally anomalous decode.**
- **Negated-write-side loop CONFIRMED:** INVERSE ROOM has +4097 count=0, −4097 count=11 → the doc "4097×11" is the |magnitude| of the write-side offset.

**Downgrade — Claim 5 (reconciliation with record_name_map recirc column) → PARTIAL/REFUTED-as-stated.** The finding's loop metric (most-reused |magnitude| over the FULL 128-word buffer) disagrees with the doc's active-in-band metric for **5 of 20**:

| program | doc (active in-band) | finding (full buffer) |
|---------|---------------------|------------------------|
| DARK HALL | 2745×4 | 30407×6 (the finding's own table even prints this, contradicting the validated doc) |
| HALL/HALL | 2665×2 | 27444×6 |
| PLATE/PLATE | 4097×3 | 26682×3 |
| PLATE/HALL | 61×2 | 26410×4 |
| RES CHORDS | 6529×5 | 6529×6 (count off) |

The >16383 write-region/−1-tail offsets dominate the full-buffer metric. Restricting to the doc's active-in-band region reproduces the doc value for all 5. The KIND conclusion is unaffected; only the "reconciles with the doc" assertion is cherry-picked (claim 5's evidence omits exactly the 4 hard mismatches).

---

## D4 — SIZE parameter sweep (HOLDS qualitatively; sub-sample precision claim REFUTED)

**Core mechanism solidly verified (independently reproduced):**
- stepscale (0x3CE9) advances monotonically with cce; CONCERT recirc tap = 6008,7147,9140,12843,16261,19679 (176→577 ms), origin-LSQ k=284.805.
- **non-FE CHAMBER (0xC000) completely SIZE-invariant** — confirms FE(computed)/non-FE(pre-baked) split; all 11 non-FE records have stepscale flat at 16.
- multiplicative model (base·ss/16) REFUTED (predicts 24032 vs measured 19679 at cce=0xFF).
- genuine 16-bit wrap of the longest taps at high SIZE (CONCERT 31535→−30583).
- gains SIZE-independent (capture_coeffs reads neither cce nor 0x3CCE); ccf (0x3CCF) inert (0 offsets changed).

**Two claims REFUTED (independently verified):**

1. **The "[16..64] SIZE band" is NOT universal.** Sweeping all 20 records, FE stepscale falls into **5 distinct families**:
   - `[16,20,27,40,52,64]` → CONCERT, PLATE, BRIGHT HALL
   - `[16,28,44,73,102,128]` → DARK HALL
   - `[16,30,46,78,110,140]` → PLATE/CHORUS, RICH SPLIT
   - `[16,34,54,92,130,166]` → RICH PLATE
   - `[16,36,56,96,136,174]` → INVERSE ROOM, RICH CHAMBER, DARK CHAMBER
   - `[16,16,…]` (flat) → all 10 non-FE
   **INVERSE ROOM (0xBD54), explicitly listed as one of the four tested programs, uses [16..174], not [16..64].**

2. **The "affine to ≤0.86 samp across ALL in-range taps of EVERY FE program" claim is FALSE.** Fitting INVERSE ROOM monotone non-wrapped taps against its OWN band [16..174] gives **worst residual 131.1 samples** (tap55 series [330,722,1115,1900,2685,3156], increments [392,393,785,785,471] — a doubling-then-drop the single-slope model can't capture); against the wrongly-assumed [16..64] band it balloons to **1101.7 samples**. Re-running the census per-program: B800/BAAA/C554/CAAA/E000/E800 are clean (≤0.86), but **BD54=131, E2AA=42, E554=131, EAAA=131** — 4 of 10 FE programs deviate by tens-to->100 samples.

**Corrected D4 conclusion:** *monotone SIZE scaling confirmed for FE / invariance for non-FE / gains untouched / multiplicative wrong / genuine wrap* — all solid. But *affine-to-sub-sample* holds **only for the low-slope [16..64] family**; high-slope programs carry an unmodeled second-order/piecewise term (residuals 42–1101 samp).

---

## Where the decode strains (summary)

1. **Wording overstatements** (D1): "byte-identical" → in-band multiset; "19/20 unity" → 18/20 (CHAMBER + M BAND DELAY sub-unity).
2. **Metric-definition divergence** (D1/D3): the single-most-reused-tap "recirc" metric is tie-break-fragile and, over the full buffer, contradicts the validated record_name_map for 5/20 programs. Restricting to the active in-band region resolves it.
3. **Unmodeled second-order SIZE term** (D4): the affine SIZE law is exact only for the low-slope program family; 4/10 FE programs need a piecewise/second-order model. This is the one finding with forward implications for the C++ rebuild — a SIZE-accurate implementation cannot use a single global slope.

## Where it is robust

- **Zero physical-bounds violations** across all 20 programs at all SIZE settings (delays < wrap, coeffs ≤ rail) — D2 is clean and the rail bound is structural.
- **Both build paths encode one delay grammar** (predelay→recirc→multitap), 10/10 each — D3 KIND result is solid and reproduces exactly.
- **Same-engine family coherence** (CONCERT≡BRIGHT in-band multiset; DARK HALL = same engine shorter loop) and uniformly sane coefficient magnitudes (mean |c| 0.49–0.77).

**Bottom line:** the reverse-engineered offset+coefficient decode is internally consistent and physically sane across the whole program set; the residual strains are precision/wording corrections and one genuine modeling gap (SIZE second-order term), none of which undermine the validated foundation.
