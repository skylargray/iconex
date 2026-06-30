# 224XL — M4: from a recirculating (over-unity) tank to a faithful decaying CONCERT reverb

> **READ-FIRST / START-HERE.** This continues the holistic reconstruction (`docs/plans/013`) and the M3
> free-run plan (`docs/plans/017`). **The recirculation loop now CLOSES** — two source-class bugs were found
> and fixed (the DMEM *offset* source, then the MEMW *writeback*), so CONCERT went from a dead tank → a single
> delayed echo → a **dense recirculating field.** What remains is the **decay**: the field currently *sustains*
> (over-unity, saturating), it does not decay into an RT≈2.6 s hall. This plan is the path from "recirculates"
> to "reverberates." **No hand-tuned gain** — the loop must decay because the data + scale are right.

---

## 0. The M4 arc so far (what is DONE — do not re-litigate)

**dead tank → (offset-source fix) single delay → (memw_live fix) dense recirculating field → [decay = this plan]**

The phase-accurate free-run engine is **`tools/aru_freerun.py`** (`class FreeRunARU`; does NOT touch the
POST-green `tools/aru_rtl_dp.py`). M3.0 runs the whole 100-step CONCERT for 500k+ microinstructions/no fault;
**M3.1 zero-delay, M3.2 max-delay, M3.3 feedback-comb all PASS; POST stays green.** Two bugs were fixed this
session, BOTH "the value comes from the wrong source / wrong register," and both are wired in + regression-clean:

1. **★ Offset-source bug (FIXED).** The per-step DMEM delay offset was read from the `0x4000` WCS-image lanes 0/1
   — **garbage for CONCERT** (constant `6835`/200 ms for the whole diffuser block → reads/writes hit disjoint
   cells → dead tank). The real ms-scale offsets live in the firmware **`0x3F4D`** buffer. Fixed:
   `aru_freerun.concert_offsets(0xB800)` = `aru224_emulate.tap_map(0xB800)`, passed as
   `run_free(wcs, src, N, offsets=concert_offsets(0xB800))`; **`addr = CPC + offset[step]`** (settled by a full
   source×formula matrix: of `{CPC−off, CPC+off, CPC−|off|}` only `CPC+off` survives; `0x4000`-raw is garbage
   under every formula). ⚠ Do NOT use `boot8080.read_offsets` (reads a CONTAMINATED post-build `0x3F4D`).
2. **★ memw_live bug (FIXED).** The MEMW writeback used the **stale, 1-instruction-deferred RES register**
   instead of the live MAC result; most MEMW steps have no XFER positioned to refresh RES, so the fed-back
   accumulated value was thrown away (read→writeback gain ≈ 0) → one forward delay at ~0.014, no recirculation.
   Fixed in `FreeRunARU.step` (the MEMW branch): **`self.DM[addr] = res_from_acc(self.ACC) & 0xFFFF`** (the live
   accumulator), grounded in the POST-verified `aru_rtl_dp.py` which loads RES live every step (fig-3.3: "DIN
   critical path = XFER CK → result register"). Result: impulse 4 → 83k nonzero output samples; CONCERT now
   recirculates densely.

**Measured INERT — do NOT re-try (proven dead ends):** `cmag=0`=unity (byte-identical output); read-before-write
vs write-before-read; deferred-MAC retire-order toggles. The dead-tank was never these.

**Parameter application is fully traced** (`docs/plans/011` "L7", `224XL_technical_reference.md` §6,
`224XL_interconnect_netlist.md` Net-group 7): flat param array `@0x3ca3` (5 pages × 6), apply chain
`0x8185→0x85f2→`de-zipper `0xB000→`pack into `0x4000`, recall at load `0x13B6/0x13d9/0xa791`, toggles `0x3ccd`
(Mode Enhancement = bit6, gates the LFO). The defaults ARE recalled + the WCS IS built at load — **params were
NOT the dead-tank cause** (applying CONCERT Var-1's full preset is a NO-OP).

---

## 1. The exact symptom to fix (READ — this is the whole problem now)

With both fixes, run CONCERT (`offsets=concert_offsets(0xB800)`): the recirculation closes but the field
**SUSTAINS FLAT and over-unity, it does not decay.** Evidence (all reproducible):
- Noise-burst env builds to ~0.92 of peak then holds **flat ~0.74 through 5 s** (a real RT≈2.6 s hall would
  decay 60 dB in ~2.6 s).
- Impulses of **30000 / 3000 / 300 all converge to the SAME `32768` 16-bit clip rail** by ~0.7 s — an
  **input-independent steady state = loop gain strictly > 1 (a saturating oscillator), not a linear reverb.**
- The sustain plateau is **independent of the injected feedback coefficient** (cmag=16/22/32 give the same
  level) → the level is **saturation-pinned**, not coeff-scaled.

So: **the loop gain is ≥ 1 and pinned by saturation; the target is ~0.9 with the tail decaying over ~2.6 s.**

---

## 2. The two converging causes (the FIX-workflow's high-confidence diagnosis)

**Cause A — DATA: the static WCS lane-3 (cmag/XFER/ZERO) is frozen garbage for the diffuser block.**
`boot8080.py` (L16-18) establishes that `0x4000` WCS **lanes 0–2 are byte-identical to the build but LANE 3 is
LFO-modulated frame-to-frame.** Our static `concert_wcs.json` (one boot snapshot, captured at mainloop with the
audio-frame DSP NOT running) froze the **diffuser block (steps 5–22) to `0xB31AFFFF` → cmag=0, XFER=0, ZERO=0,
WA=3/RA=3** — 18 identical fill words. So those 18 recirculating taps read delayed values but multiply by 0,
never accumulate, never latch, and clobber R3. The **firmware-built `0x3e4e` image** (`aru224_emulate.build_record(0xB800)`)
has **rich, DISTINCT diffuser coeffs there** (step5=`41 B0 7F 41`, step6=`00 AF 40 00`, step7=`83 41 00 B3`, …
cmag=47/63/19/47/6/18/47 with real XFER/ZERO/MEMAC variety) — but it is **NOT a clean 4-byte copy of `0x4000`**,
and `build_record` leaves `0x4000` all-zero, so a naive re-align is only an approximation. Critically, the lane-3
also carries the **ZERO/XFER bits that scope each comb/allpass MAC group** — frozen to ZERO=0/XFER=0, the engine
over-accumulates into one saturating ACC (the +57 baseline), which is *why* memw_live writes the clip rail.

**Cause B — SCALE: each feedback writeback returns ≥ unity instead of its coeff-scaled (<1) sum.**
`memw_live` writes `res_from_acc(self.ACC)` = `sat16((ACC+4)>>3)`, but ACC is the *globally* accumulated
(saturating) value, not the per-comb scoped sum. With correct ZERO/XFER per group the writeback would capture
one comb's scaled sum (sub-unity). There may *also* be a **cmag↔coeff decode/scale mismatch**: `decode()` takes
`cmag = (inv3>>2)&0x3F` (6-bit, 0–63), while the param-sweep coeff bytes are signed −127..+127 (lane3 = sign
bit7 + 7-bit magnitude) — verify the feedback coefficients land at the intended ~0.9, not ≥1.

These are coupled: **fixing A (real lane-3 with proper ZERO/XFER scoping) is the most likely single change to
also fix B** (correct group scoping → sub-unity writeback). Cause B is the fallback if A alone still over-units.

---

## 3. Next steps (numbered — execute in order; stop + measure at each)

1. **Reproduce + instrument the current over-unity state.** Boot CONCERT (or load `scratchpad/concert_wcs.json`
   for coeffs) + `concert_offsets(0xB800)`; `run_free(..., offsets=...)`; confirm: impulse 30000/3000/300 → same
   `32768` plateau; noise-burst env flat ~0.74. Add a probe that logs, per MEMW step, `res_from_acc(ACC)` vs the
   ACC magnitude and whether ACC is saturated (±2^18). This is the baseline the fix must beat (a *decaying* tail).

2. **★ Cause A — get the REAL per-frame lane-3 (the load-bearing step).** The diffuser block's cmag/XFER/ZERO
   are frozen garbage; source them live. Three options, cheapest first:
   - **(2a) Hook the firmware's coefficient fetch.** `aru224_emulate.capture_coeffs(0xB800)` already hooks
     **`0xB510`** (the firmware's coeff-source fetch, base `0x3e05`) during the interpreter expander — the exact
     parallel to `tap_map` for offsets. Extract a **per-step coeff table** (cmag/csign/XFER/ZERO/WA/RA) the same
     way `concert_offsets` extracts offsets, and feed it per step (add a `coeffs=` path to `step`/`run_sample`
     mirroring `offsets=`). Verify steps 5–22 then have distinct nonzero cmag **and** the right ZERO/XFER.
   - **(2b) Re-align the `0x3e4e` build image to the `0x4000` step order** (it is NOT a clean 4-byte copy —
     work out the mapping, e.g. via the group table `0x3CF4` / step→addr `0xAB0C = 0x4003+step*4`), and take
     lanes 2/3 from there for the steps `0x4000` froze.
   - **(2c) Co-simulate the per-frame DSP / LFO.** The modulation engine is `0xAD5C–0xAE9B` (main-loop-paced,
     triangle, depth `0x3cd4`, rate `0x3cd3=0x20`, enable `0x3ccd` bit6 = Mode Enhancement; the prior decode
     `224XL_modulation_lfo.md` says it targets steps 56/57/107/108 — but the whole lane-3 changing frame-to-frame
     implies a broader per-sample rebuild; resolve which). Drive the firmware's per-frame lane-3 build and read
     it out each frame (this is also what M3.4/M4 ultimately needs for the modulation).
   **Re-run after 2:** does CONCERT now DECAY (env falls 60 dB over ~2.6 s; impulse 30000 vs 300 now scale
   linearly, not both clipping)? The capability test injecting real coeffs *closed the loop* (83945 nonzero) but
   still plateaued over-unity — so confirm whether the **real ZERO/XFER bits** (not just nonzero cmag) bring it
   sub-unity. If yes → go to step 4. If still over-unity → step 3.

3. **Cause B — make each feedback writeback sub-unity.** If real lane-3 still over-units:
   - Verify ACC is **cleared (ZERO/) at the start of each comb/allpass MAC group** so `res_from_acc(ACC)` at the
     MEMW is *that comb's* scaled sum, not the running saturating total. Trace one comb: read tap V → ×cmag →
     ACC (cleared first) → writeback. The realized per-pass loop gain should be ~cmag/32 ≈ 0.9, not ≥1.
   - If the gain is still ≥1, check the **cmag↔coeff decode/scale** (§2 Cause B): is the feedback coeff that
     should be ~0.9 landing as ≥1 because of the 6-bit-vs-7-bit field or a `>>` mismatch? Cross-check the
     realized loop coefficient against the netlist §4F (multiply) + the param-sweep tables.
   - Reconcile the deferred-MAC with the POST-verified `aru_rtl_dp.py`: memw_live made the *writeback* live;
     check whether RES/ACC should be live for the **DAB/output path** too (currently a MEMW's DAB still uses the
     deferred RES — possibly inconsistent). Keep `product20`'s cmag=0 `+3` baseline (it is correct per plan 016).

4. **Validate the DECAY (the M4 done-bar).** With a stable sub-unity loop: impulse → a tail that **builds then
   decays** over ~2.6 s (the manual: Halls "have a relatively low initial echo density which gradually builds");
   linearity (output scales with input, no clip); RT60 ≈ 2.6 s for CONCERT Var-1. Render a timestamped 5 s WAV
   (`renders/YYYYMMDD_HHMMSS_*.wav` — owner directive) and have the owner listen. **This is the M3.3/criterion-4
   bar finally met.**

5. **Modulation + RT60 tracking (M4 proper).** Add the per-frame LFO (step 2c if not already) so the tail
   evolves/de-correlates; verify **RT60 tracks the LF/Mid Decay parameters** (the param array `@0x3ca3`, the
   group→step map in §6 of the technical reference). Confirm Mode Enhancement (`0x3ccd` bit6) gating works.

6. **Multi-program + L7 (the final checks).** Reproduce a coherent decaying reverb on **≥3 programs** (BRIGHT
   HALL `0x20`, PLATE `0x02`, ROOM …) by sourcing their offsets+coeffs the same way (`tap_map(recbase)` /
   coeff-hook per record in the `0xB800` array). Then **L7**: compare to a real-unit IR if/when a capture exists
   (pass/fail only; meaningful because everything beneath is structural).

---

## 4. Key files, tools, firmware addresses

- **Engine:** `tools/aru_freerun.py` — `FreeRunARU`; `concert_offsets(recbase)` (the `0x3F4D` offset source);
  the `offsets=` path in `run_sample`/`run_free`; the `memw_live` writeback. Run `python tools/aru_freerun.py`
  for the fast structural suite (zero-delay/max-delay/feedback-comb). `tools/render_wav.py` → timestamped WAVs.
- **Coeff/offset source (firmware):** `tools/aru224_emulate.py` — `tap_map(recbase)` (the `0x3F4D` offsets, via
  the B55B builder; **validated byte-identical to the firmware load**); `build_record(recbase)` (the `0x3e4e`
  image with real coeffs); **`capture_coeffs(recbase)` (hooks `0xB510`, the firmware coeff fetch — the parallel
  to `tap_map` for the per-step coefficients).** Uses the retired `z80emu` for the *build only* (pure compute,
  validated). The CONCERT record is `0xB800`; all 21 records stride `0x2AA`.
- **Boot:** `tools/boot8080.py` (verified 8080 → `0x4000` coeffs at mainloop; ⚠ `read_offsets` is contaminated).
  Cached CONCERT `0x4000` WCS:
  `C:/Users/Skylar/AppData/Local/Temp/claude/d--OneDrive-Gray-Instruments-iconex/f950f5a4-d96d-4fdd-899a-08b03ca853c7/scratchpad/concert_wcs.json`
  (coeffs only — offsets MUST come from `tap_map`).
- **Multiply / decode ground truth:** `tools/aru_booth.py` (gate Booth, 20/20 goldens); `decode()` /
  `product20()` / `res_from_acc()` in `aru_freerun.py`; netlist `§4F` (multiply), `§5/§3.6` (DMEM addr=CPC−OFST),
  `§G3R` (field map); `224XL_technical_reference.md` §2 (address convention) + §6 (params).
- **Firmware addresses:** WCS image `0x4000`; offsets `0x3F4D` (downward, hi@a/lo@a-1); param array `0x3ca3`
  (page state `0x3c32/0x3c34`); apply `0x85f2`→de-zip `0xB000` (pack `0xB4F0`/`0xB4FF`); group table `0x3CF4`
  (built `0xAA9F`; step→addr `0xAB0C`=`0x4003+step*4`); recall `0x13B6/0x133e/0x13d9/0xa791`; coeff fetch
  `0xB510` (base `0x3e05`); **modulation engine `0xAD5C–0xAE9B`** (depth `0x3cd4`, rate `0x3cd3`=0x20, enable
  `0x3ccd` bit6 = Mode Enhancement). CONCERT Var-1 preset: `docs/reference/224/224X_chapter8_variation_presets.md`.

---

## 5. Ground rules (unchanged — why the project survived)

- **No hand-tuned gain, ever.** The loop must decay because the data (lane-3) + scale (coeff/ZERO/XFER) are
  right, never because a constant was multiplied in. If you find yourself scaling a feedback path "to make it
  decay," stop — it hides the real bug (this is the discipline that caught the offset + memw_live bugs).
- **The netlist + timing spec are ground truth for wiring/edges; the firmware (boot8080/aru224_emulate) is
  ground truth for the values.** When the model disagrees, the schematic/firmware wins; the bug is ours.
- **A failure is a specific net / register / source.** Localize it (which step, which value, sat or not),
  exactly as the offset-source and memw_live bugs were localized — don't theorize, trace + measure.
- **Keep the regressions green at every step:** the fast structural suite + the whole POST (`aru_rtl_dp.py`).
- Flag any suspected schematic/firmware-trace gap (e.g. the `0x3e4e`→`0x4000` alignment, the per-frame lane-3
  build) for the owner rather than guessing.

---

## 6. Risks / honest unknowns

- **The per-frame lane-3 source (step 2) is the crux + the biggest unknown.** Whether the diffuser coeffs come
  from the static build (just frozen wrong in our snapshot) or from a per-sample DSP rebuild is not yet pinned;
  `capture_coeffs`/`0xB510` and the `0x3e4e` image are the leads, but the `0x3e4e`→`0x4000` mapping is not a
  clean copy. Resolve this empirically before trusting any decay result.
- **Over-unity may be partly intrinsic.** Prior work measured the *static* CONCERT eigenvalue ≈ **+1100 ppm
  (slightly over unity)** — so the *modulation* (step 5) may be part of what makes it decay/bounded in the real
  unit. Expect the static loop to sit near unity; get *recirculation + correct coeffs* first, then the modulation.
- **Saturation vs linear.** The current `32768`-rail plateau is a saturating oscillator; the fix must restore a
  *linear* decaying loop (verify by input-amplitude scaling), not just a bounded one.
- **No free-run hardware oracle.** POST + structural fidelity + figure-matching are strong, but the final word is
  a real-unit IR (L7) or a single-step port capture of a real ARU — the highest-leverage hardware ask.

---

## 7. One-line orientation

The recirculation **closes** (offset-source + memw_live fixed; CONCERT is a dense recirculating field). It does
not yet **decay** — it sustains over-unity because the diffuser block's **lane-3 (cmag/XFER/ZERO) is frozen
garbage** in the static WCS and the writeback returns the **saturating ACC** instead of a coeff-scaled sub-unity
sum. Source the **real per-frame lane-3** (firmware `0xB510`/`0x3e4e`/the LFO) so the ZERO/XFER scope each comb,
verify the loop gain lands ~0.9, and CONCERT will finally reverberate.
