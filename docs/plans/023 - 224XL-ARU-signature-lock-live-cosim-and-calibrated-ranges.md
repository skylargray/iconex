# 023 — 224XL: the ARU datapath signature lock, the live co-sim, and calibrated ranges

**Status:** READY TO EXECUTE (written 2026-07-02 at the close of sessions 0024/0025/0026 — all
three the same day; read their docs in order before starting).
**Read first:** `docs/sessions/0024 - the-known-answer-oracles-and-the-pp-bus-capture-correction.md`,
`0025 - the-csign-lag-falsification-and-the-shelf-injection-law.md`,
`0026 - the-full-parameter-surface-all-five-larc-pages.md`. The engine of record is
**`tools/aru_freerun22_rtl.py`** at: the 0022 frame (L+1 steps, reversed words), the PP-bus capture
(RES ← ACC + ppC combinationally, netlist §4.2), **cs_eff = STORED l2 bit7, 1 = positive (the E83
golden anchor)**, own-sign at every pp (falsification-tested), stereo `(in_h1, in_h2)` input.
Trust 0026 > 0025 > 0024 > 0022 > everything older.

**Mission.** The model now reproduces the documented defaults (mod-replay: LF 3.2 / mid 2.2 /
broadband 2.6 vs documented 3.0 / 2.0 / 2.6), the D1 diag oracles, the T&C signature table
(374/376), the measured fs (32,508 Hz from the real IR), and the full 5-page parameter surface.
Two locks remain before the model can be called DONE at the semantics level, plus the calibration
that turns "levers work" into "ranges exact":
- **E1** — the ARU §5.7 signature tables: per-pin verification of the ENTIRE MAC datapath
  (Booth array, PR, accumulator pipeline, PP bus/sat-mux, result reg, XFER/ZERO edges, the E83
  sign path) against the manufacturer's own measurements. The last untested semantics live here.
- **E2** — the TRUE live co-sim (8080 interleaved per frame): retires the frozen-LFO
  approximation (±0.2–0.3 s RT60 spread), formally closes the last ~10% of D2b, and unlocks the
  runtime dynamics (stop decays) + audible chorus.
- **E3** — the LARC display calibration (registry #28): byte ↔ displayed-value maps from the
  firmware's own display strings, then the formal D2d range-endpoint verification.
- **E4** — the variation oracle: per-variation recalled presets + the w43/95 sign law
  (LF-vs-Mid relation → boost/cut) across Concert Hall V1–V7.

---

## 1. Ground truth (established; do not re-derive)

### 1.1 Engine + oracle state (0024/0025/0026)
- Capture: RES = sat16((ACC_reg + ppC(w_{n−2}) + 4)>>3) at 3.06 — the PP bus (§4.2). ZERO clears
  the register only. Effective coefficients = FULL stored cmag (no pairC loss).
- Signs: cs_eff = stored bit7 (1=pos). The complement was the crossover band-inversion
  (registry #25); the CSIGN-lag variants are dead (#23, `RTL22(csign_lag=True)` +
  `_test_csign_split` pin them). The factory opposite-sign idiom is residue-load-bearing
  (P20(x,32,1) = 8x+3; test programs must cancel residues deliberately).
- Frame: L+1 steps; fs = 30.72e6/9/(L+1); CONCERT = 32,508 Hz MEASURED from the benchmark IR
  (warp s=1.000; autocorr lags to ~0.2%; registry #22). 34.125 kHz = the L=99 bank's rate; the
  manual's coarse-delay milliseconds are NOMINAL at that rate (preechoes measure ×1.048 on
  CONCERT — the fingerprint).
- The idle floor under E83 is DC-dominated (−62…−68 dBFS per channel): **floor-subtract every
  headline metric** (raw-burst verdicts read TONAL; registry #16 is mandatory).
- D1 CLOSED 16/16 (half-1 = LEFT); D3 T&C 374/376 (2 single-glyph table errata; FP54=+5V@N=30
  hardware-confirms the L+1 frame); POST green throughout.
- Documented-defaults: settled LF 3.3–3.75 / mid 2.3 / bb 2.7–2.9; live-replay (d4lite)
  LF 3.20 / mid 2.2 / bb 2.6 — on the documented numbers. LFO-phase spread ±0.2–0.3 s.
- D2c bank coherent under E83: PLATE 1.74 (doc 1.8), CHAMBER alive 2.18 (was silent), 10/13
  WET-PASS; id 3 = invalid selector (no 0x03 record), id 4 = the unlisted record (name it, E3c).

### 1.2 Parameter system (0026 — the complete map)
- All-page values: flat array **`0x3CA3 + page*6 + slider`** (header 0x3CA2, toggles 0x3CCD);
  **direct-call `0xA791`** rebuilds the full image (validated byte-identical) — EXCEPT the decay
  family (LF/Mid/Stops/PDL/Chorus → the decay generator `0x86B2`/`0x8DA5`/`0x8E03`, registry
  #26): drive those via sliders `0x3C00-05` with **page select = write `0x3C34`**.
- Byte scales: % params = byte/2.56; PE delay = byte × 34 frames (nominal ms); FinePD = byte ×
  4 frames; PDL byte 0 = the 24.0 ms documented minimum. Recalled defaults == ch.8 V1 presets.
- Preecho taps = words **80/28/79/27** (L→A, R→C, R→A, L→C — ch.4's routing column; the June
  "tank feedback" label is dead). Depth = words 29-32/81-84, A/C-only (exact). Crossover pole
  words 45/97 (fc = fs·ln(32/cmag)/2π; documented 170 Hz–19 kHz = cmag 31…1). HFBW = 74/75/125/127.
  Diffusion = 33-39/85-91 observed (§7.5's "g19 = 52/60/72/104/111/123" does NOT match — June-era).
- Quirks: Definition-excursion ladder hysteresis (#27 — re-derive baselines); raw slider bytes
  beyond the LARC physical scale overdrive documented ranges (#28).

### 1.3 E1 anchors (the ARU signature tables)
- Tables digitized: `docs/reference/224/224-signature-value-tables.md` — ARU **no-feedback**
  (reference +5V = `29F3` ⇒ window **N = 62 ARUCK edges**) and **feedback** (`3696` ⇒ **N = 90 =
  30 steps × 3** — the diag-3 frame again) configs, ~54 chips each. Setups (SM §5.7): ARU
  no-feedback START=RESET/ (ext-16), STOP=**XFERCK** (U43.11), CLOCK=ARUCK (U10.11); feedback
  START=STOP=RESET/. **N=62 is itself a timing oracle**: the XFERCK-terminated window measures
  where the (first?) XFER capture lands relative to RESET/ — derive the predicted N from the
  diag-3 WCS + the 0023 alignment BEFORE running (a known answer).
- Stimulus: diag-3 (`wcs_diag.json["sig3"]`, verified-core capture, = `_diag3_wcs.bin`).
  **The XREG question:** diag-3 is XREG-heavy; the post-build handler loop at **`0x0D10`**
  (the "signature-pulse loop") is what the bench runs during measurement — trace it FIRST
  (disassemble 0x0CF0–0x0D40 region; instrument OUT 0x06/0x07 on the verified core): what 16-bit
  XREG values does it write, and are they constant/frame-periodic? (They must be, or the pin
  signatures would not be stable on the bench.) The frame-sync wait 0x0627 spins on `0x3C14` —
  in-emulator, either patch to RET (free-run, d1a-style) or set the flag per frame (E2's
  machinery); confirm the XREG sequence is the same either way.
- Pin map source: netlist §4.1 (AC bus → aru_U45-49 Q pins + adder A pins), §4.2 (PP bus →
  sat-mux Y + accumulator D + result-reg D PP3-18), §4.3 (adder Σ + carry chain), §4.4/4.5
  (sat-mux/SAT/B-IN), §4.6 (sub-XOR row), §4.7 (PR aru_U10/U11/U12), §4.8 (result reg U43/U44 —
  the PP→bit table), §4.9 (ACC control), §4F.1-4F.8 (regfile, F-net, shifter, SR-net, Booth
  NANDs, front-end adders, CSIGN/sub-ctrl). The D3c scorer (`d3_signatures.py`) is the template:
  parse → per-pin streams → ONE global window phase scan → match/mismatch/not-modeled.
- The engine's per-step events map to per-ARUCK streams: each step has 3 ARUCK edges (AS0/1/2);
  the modeled quantities at each edge are derivable from RTL22's state (opnd/pps/ACC sequence/
  RES/regfile). Build the probe layer as a parallel "slot emitter" that replays a frame and
  yields (step, AS) → net values; do NOT restructure the engine.

### 1.4 E2 anchors (live co-sim)
- Budget: ~62 CPU ticks per frame (0022-measured). `probe_run.run_ticks` serves the RST-7
  (HLT starvation trap — 0025). The frame-sync ISR flag is **`0x3C14`** (set to 0x80 per frame
  by the real ISR; the mainloop's per-frame work spins on it at 0x0627-style waits).
- d4lite (`d4lite_mod_replay.py` + `d4lite_snapshots.json`) already validates the WCS-trajectory
  replay path; the co-sim differs by having the 8080 LIVE (dynamics, de-zipper, display, key
  handling all real). Snapshot-replay is the fallback if interleaving stalls.
- Stop decays: gate 0x83B4 (DynDecay bit 0x3CCD.0); the input-level detector's source is
  UNTRACED — find what it reads (ARU readback ports? XREG? disasm around 0x83B4/0x83D1) before
  promising dynamics.
- Chorus: depth `0x3CD4` (default 4 ≈ ±40-sample sweep), rate `0x3CD3` = 0x20; Mode Enhancement
  (0x3CCD bit6) gates the whole LFO at `0xAD5C`.

### 1.5 E3/E4 anchors
- Display buffer: `0x3F4F..0x3F80` (message) + `0x3F8E..` (DL-1414 image the LARC draws);
  boot8080 captures TX bytes; boot_xl's display milestone = 0x82CF. The D2c name-readback came
  back EMPTY under the id patch — wire the display refresh (call 0x82CF? capture TX after
  injection) and parse the value strings the firmware itself renders.
- Documented endpoints to score (ch.4 Table 4.2): LF/Mid/Stops 0.6–70 s; XOV/Treble/HFBW
  170 Hz–19.0 kHz; PDL 24.0–216 ms; Depth/Dif/PE-levels 0–99; Chorus 0–97; Definition 0–75;
  PE delays 0–188 ms; FinePD 0–31.3 ms; Size 08–87 (errata: Concert/Bright max 40 m); Gate
  0–5.08 s.
- Variations: the recall at **`0x13D9`** copies 0x30 bytes into 0x3CA2 — trace its SOURCE pointer
  per variation (where do V2–V7 preset blocks live?); the LARC variation keys are in the same
  serial key space as PGM-2 (0x30/0x10 press/release codes — enumerate via the key dispatch).
  ch.8 documents every variation's presets; ch.4 documents decays (V1 2.6 avg; V2 1.7/1.7;
  V3 3.8/2.4; V4 3.0/3.0; V5 avg 6.5 s; V6/V7 DynDecay mirror pairs 5.7/1.7).
- The w43/95 sign law (0025): LF>Mid ⇒ boost sign (stored bit7=1 under E83 at cmag 5 for V1);
  Mid≫LF ⇒ cut. Predict per variation BEFORE reading the bytes.

## 2. Dead-end / discipline registry (carried; additions 0024–0026)
Everything from plan 022 §2 stands, plus:
| # | Item | Verdict |
|---|---|---|
| 17 | Result-reg capture = registered ACC | DEAD — PP bus (§4.2); capture includes pairC combinationally |
| 18 | effective coeff = cmag−(cmag&3) | DISSOLVED by #17 |
| 19 | Band RT60 by block-RMS without noise truncation | CONFOUNDED — Schroeder T30 on Lundeby-truncated tails |
| 20/21 | Mainloop-snapshot images / boot-image verdicts | PRE-APPLY — settle ≥2M ticks; movers = 8 bytes (56/57/107/108) |
| 22 | Fixed 34.125 kHz for all programs | DEAD — fs_real(CONCERT) = 32,508 measured (`d2f_fs_from_ir.py`) |
| 23 | CSIGN one-edge lag on pairC (either consumer) | DEAD — 0.8 s TONAL collapse; control defers one AS like data |
| 24 | One-slider-one-wordset param independence | DEAD — joint compilation (w43/95 = f(LOW, MID) incl. SIGN) |
| 25 | cs_eff = ~stored bit7 | DEAD — E83 anchor; the complement WAS the band inversion |
| 26 | Bare 0xA791 as the full apply | INCOMPLETE — decay family needs the slider/decay-generator route |
| 27 | Param-apply hysteresis (Definition/ladder) | Re-derive baselines after excursions |
| 28 | Raw slider bytes = LARC scale | FALSE — overdrive beyond documented ranges; calibrate via the display (E3) |

## 3. Phase E1 — the ARU §5.7 signature co-sim ★ the datapath lock
E1a. **Trace the 0x0D10 pulse loop.** Disassemble the diag-3 handler tail; instrument OUT
     0x06/0x07 (+ any 0x00-0x05 control OUTs) on the verified core through ≥3 frames of loop
     execution under BOTH pacings (0x0627→RET free-run; 0x3C14-flag per-frame). Deliverable: the
     exact per-frame XREG write sequence + proof of periodicity (byte-identical across frames and
     boots). If the loop is NOT periodic → STOP and re-read the SM setup (maybe the analyzer
     window makes it irrelevant); do not guess.
E1b. **Predict the no-feedback window length.** From the diag-3 rows + the 0023/0024 alignment,
     derive N(START=RESET/, STOP=XFERCK, CLOCK=ARUCK) — the count of ARUCK edges between the
     RESET/ edge and the first XFER CK rise. **It must come out 62** (the manual's `29F3`
     calibration). A mismatch here falsifies the XFER-edge placement — investigate before E1c.
E1c. **Slot emitter + pin map + score.** Parallel probe layer replaying one steady-state frame
     of diag-3 with the XREG stream from E1a, emitting per-(step, ARUCK-edge) values for every
     §4.x net; map pins from the netlist tables; ONE global window-phase scan per config;
     score match/mismatch/not-modeled for BOTH ARU tables (~54 chips each). Every mismatch names
     its net. Success = the MAC datapath (incl. E83 signs, PP-bus capture, ACC pipeline,
     serializer, Booth array) is pinned at hardware pins. Budget: this is the biggest single
     item — timebox the pin map to the high-confidence §4.1/4.2/4.7/4.8/4.9/4F.3/4F.4 sets
     first (≈60% of listed pins), then widen.
E1d. Stretch: the DMEM table (CLOCK=RESET/, window=CPC-MSB half-cycle = 32768 frames — cheap at
     ~4,700 fps) and the FPC table (needs diag-6 + the FPC codec path — capture diag-6's WCS via
     the d1a route first: menu item 6, find its handler in the 0x0330 table).

## 4. Phase E2 — the live co-sim (D4 proper)
E2a. **Interleave.** One process: boot8080 to mainloop+settle; per audio frame set
     `m.memory[0x3C14] = 0x80`, `run_ticks(m, 62)`, harvest WCS writes (either diff the 4-word
     mover set + de-zipper targets, or attach `trace8080` for exactness), patch the decoded rows,
     `RTL22.run_sample`. Validate against d4lite: the mover trajectory must advance at the same
     per-frame rate as the tick-based replay (and the LFO period must match
     `224XL_modulation_lfo.md`'s ~345k-instruction triangle).
E2b. **Render + verdicts.** CONCERT 6.5 s co-sim: per-band RT60 vs documented/benchmark (expect
     ≈ d4lite: LF 3.2 / mid 2.2 / bb 2.6, tighter); LISTEN via `process_wav_rtl.py` (snare +
     a sustained source for the chorus). The frozen-phase approximation retires here.
E2c. **Chorus.** Render Chorus byte 0x02 vs 0xF0 under the co-sim; measure tap-sweep depth
     (should track 0x3CD4: 4 → 60) and audible modulation; cross-check the documented pitch-
     wobble note (ch.4 Dark Hall Chorus>50 caveat) qualitatively.
E2d. **Stop decays (only if E2a is solid).** Find the input-level detector's data source
     (disasm 0x83B4/0x83D1 back-refs); if it reads an ARU/XREG level the co-sim can supply,
     drive burst-then-silence and verify the running→stopped coefficient switch (V1: stops
     3.0/3.0 vs running 3.0/2.0 — the LF-stop equality makes the mid band the observable).
     If the source is un-modelable, record why and bank for the variation phase (V6/V7 are the
     dramatic test cases).

## 5. Phase E3 — the LARC display calibration + formal D2d
E3a. **Byte ↔ displayed value.** After each slider injection, drive the display refresh (the
     0x82CF path or harvest the serial TX stream) and parse the firmware's own value string
     ("2.0 SEC", "720 HZ", "24.0 MS"…). Map byte↔display for every CONCERT parameter (both
     pages' scales); the LARC's physical full-scale byte is whatever displays the documented
     maximum.
E3b. **D2d formal.** At the calibrated endpoint bytes: Mid Decay 0.6 s and 70 s (render 12–15 s,
     fit T15 for the long end), XOV/Treble/HFBW 170 Hz and 19 kHz corners, PDL 216 ms, PE delay
     188 ms, FinePD 31.3 ms. PASS = measured ≈ displayed ≈ documented. This retires the last
     June-era transfer-function claims (`224XL_param_sweep.md` final supersession note).
E3c. **Names.** Fix the display-name readback (empty under the id patch in 0026); name id 4's
     record and confirm id 3 displays garbage/no-program.

## 6. Phase E4 — the variation oracle
E4a. Trace the recall source per variation (0x13D9's pointer; where V2–V7 blocks live) OR find
     the variation-select key/RAM path; capture recalled param blocks for Concert Hall V1–V7.
E4b. **Predict then read:** the w43/95 sign+cmag per variation from the documented LF-vs-Mid
     relation (V2 1.7/1.7 ⇒ ~0; V3 3.8/2.4 ⇒ boost; V4 3.0/3.0 ⇒ ~0; V5 ⇒ large boost; V6/V7 ⇒
     DynDecay pairs) — a decode-independent apply-law oracle. Then verify the % param bytes vs
     ch.8 (Diffusion 25/15/01/01…, Depth, Chorus, preecho levels per variation).
E4c. Render V2/V3/V5 at defaults → documented decay verdicts (V5's 6.5 s average is the big
     dynamic-range test; V2's 1.7/1.7 equal-band case tests the shelf-zero prediction).
E4d. Stretch: other-bank variations with crisp ch.4 numbers (Room V1 1.4 s; Plate V2 0.6/1.8 at
     XOV 170 Hz; CD plates 1.8) — extend the D2c table from anomaly-hunting to spec-scoring.

## 7. Phase E5 — consolidation (as time allows)
- Banner the pre-E83 sign statements (timing-spec §CSIGN lines, tech-ref remnants, 0023 doc is
  already bannered via 0024/0025 pointers; check `224XL_timing_spec.md`).
- `reverb_metrics`: first-class floor-subtraction mode (the DC floor makes raw verdicts TONAL).
- Diffusion early-window observable; FinePD-L observable; Size/Gate behavior notes.
- `aru_whole.py` / C++ scaffold re-sync to the locked semantics (only after E1 passes).

## 8. Verification rules (unchanged + additions)
- Defaults are the oracle; sliders only verify documented ranges (owner directive). Never tune.
- **Floor-subtract EVERYTHING** (the E83 DC floor; registry #16). Band comparisons per-band at
  the documented crossover; Schroeder T30 on truncated tails (#19).
- No audio claim without the WAV on disk; reverb verdicts via `reverb_metrics` battery.
- POST green at every phase; engine self-tests before every render batch.
- Routing claims need both stereo polarities (D1 discipline).
- Signature mismatches are findings that NAME their net; clock/window definitions first.
- Predictions BEFORE reads (E1b's N=62; E4b's sign law) — a prediction table in the session doc.
- Every probe's final message states which registry entry it would re-open, if any.

## 9. Facts that will save time
- Boot ≈ 40 s; settle +6M ticks; `probe_run.run_ticks` for ALL post-boot running (HLT trap).
- Direct-call pattern: push 0xFFFF sentinel, set PC, breakpoint at the stop PC (0x0F17-style
  loops never return; 0xA791 RETs). Two-prefill agreement for WCS captures.
- Engine ≈ 4,700 frames/s (6.5 s render ≈ 45 s); the D2h cache (`d2h_param_wcs.json`) holds
  lo/hi images for every 0xA791-reachable parameter; `d4lite_snapshots.json` holds a 15M-tick
  WCS trajectory at 50k-tick resolution.
- The LFO-phase spread is ±0.2–0.3 s on RT60 — quote spreads for static images.
- Byte laws: % = byte/2.56; PE delay = byte×34 fr; FinePD = byte×4 fr; PDL byte 0 = 24.0 ms.
- The diag-3 frame is 30 steps (FP54@N=30); its reset word is 99; active words 98–127.
- sig224 self-test in-process before any scoring pass; the two known T&C table errata are
  U3.10 (`00U0`→0000) and U11.6 (`2PU6`→29U6) — do not "rediscover" them.
- The 0x8160 id patch does NOT reach diag programs or variations (different namespaces).
- `renders/` under session0022_probes is gitignored (WAVs regenerate); caches are committed.

## 10. Artifacts
- New: `tools/session0022_probes/{e1_xreg_trace, e1_aru_signatures, e2_live_cosim,
  e3_display_calibration, e4_variations}.py` + caches (`xreg_pulse.json`, `wcs_diag6.json`,
  `display_map.json`, `variation_params.json`).
- Updates: `224XL_param_sweep.md` (final supersession after E3b), `224XL_timing_spec.md`
  (E83 banner), the D2c table extended to spec-scoring (E4d).
- Records: session doc 0027+; memory index update; this plan gets its execution banner.
