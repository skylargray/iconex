# 0024 — The known-answer oracles: D1 closed, the T&C signature lock, and the PP-bus capture correction

> **➜ The §7 LF finding (crossover band-inversion) is RESOLVED in session 0025** (same day): the
> inversion was the engine's global cs_eff convention (0023's complement), adjudicated by the E83
> golden anchor — see `0025 - the-csign-lag-falsification-and-the-shelf-injection-law.md`.

**Date:** 2026-07-02 (same day as 0023)
**Scope:** execution of `docs/plans/022 - 224XL-known-answer-oracles-and-parameter-state.md`
(D1 complete, D2a/D2b/D2c + diagnosis, D3 T&C complete, D4-lite probe; D2d gated, D3d/D4 banked).
**Result:** ★★★ three independent oracle families now lock the model — and the D2b documented-defaults
oracle caught a real engine bug the other two could not see: **the result register reads the PP bus
(sat-mux/adder output), not the accumulator register** (netlist §4.2 had it traced all along). With the
fix, every stored coefficient acts at FULL weight; the "effective coeff = cmag−(cmag&3)" consequence of
0023 is dissolved, and the mirrored cmag 13/10/6 pre-capture words in the factory programs are live
values, not dead LSBs.

---

## 1. D1 — the firmware's own delay diagnostics: CLOSED (16/16 PASS)

**D1a capture** (`d1a_capture_diag.py`, verified kosarev core, e1 boot pattern): direct-called the
diag-menu handlers after mainloop — item 8 MAX = `0x0EF4`, item 7 ZERO = `0x0EFD`, both `CALL 0x0F2C`
(builder) then land in the display loop `0x0F17` (= run-to-done PC; ZERO's four offset patches happen
before it). Frame-sync wait `0x0627` → RET (the diag3 patch). Two-prefill (0xFF/0x00) agreement =
**512/512 bytes** (the builder's own full fill, now recorded). Built-in route checksum **PASS**: the two
images differ in EXACTLY the four ZERO-patch bytes (word 76 ofst `0x7FFF→0x4001`, word 126
`0x3FFF→0x0001`). Both images extract as **reset word 29 ⇒ L=99 ⇒ 100-step frame, fs = 34,133 Hz**.
Cache: `tools/session0022_probes/wcs_diag.json` (+ a verified-core re-capture of diag-3, byte-identical
to `_diag3_wcs.bin` — the D3c provenance item).

**D1b stereo** — `RTL22` accepts `(in_h1, in_h2)`: the FPC A/D mux alternates halves per fig-3.5, so
RD-AD steps in execution order alternate (first read → half-1). Mono path bit-identical (channel
digests unchanged pre/post edit; `tuple(x,x) == mono` exact) — `d1b_regression.py`.

**D1c known answers** (`d1_diag_oracles.py`, POST green first, both polarities per plan §7):

| | routing | lag | gain | separation |
|---|---|---|---|---|
| ZERO h1-only | **A,D live / B,C dead** | exactly **1 frame** (29 µs = "0 s") | **+1.000** | 253 dB (dead = literal zeros) |
| ZERO h2-only | **B,C live / A,D dead** | 1 frame | +1.000 | 253 dB |
| MAX h1-only | A,D | exactly **16383 frames = 0.4800 s** ("0.5 s") | +1.000 | 253 dB |
| MAX h2-only | B,C | 16383 frames | +1.000 | 253 dB |

The SM's "Left → A,D / Right → B,C" answer **pins the binding: half-1 (first RD-AD read) = LEFT**.
16383 = the read−write offset difference `0x3FFF` exactly, both halves. End-to-end: the firmware built
the WCS, `program_rows22` + `RTL22` ran it with no byte interpretation in between, and the audio does
exactly what the service manual says. **The plan-021 D1 oracle is closed** — and it survived the §4
capture correction unchanged (its words are all cmag=32, pairC = ±1 residue: by design blind to the
capture-source question).

## 2. D2a — the capture point, pinned

`d2a_capture_settled.py` (verified core, no keys, no audio; WCS snapshot per 1M ticks, 80M ticks past
mainloop):
- **Power-up apply/de-zipper transient:** 14 bytes change within the first ~1M ticks then freeze —
  CPU words **42, 62–64, 66–68, 94, 113–115, 117–119** (lanes 0+3) = exactly the MID-allpass + predelay
  words of the sweep map. **The mainloop "boot" image is pre-apply — not the default state.**
- **Persistent movers:** exactly **8 bytes = words {56,57,107,108} lanes 0+3** (the modulated tap pairs),
  forever. A "settled" image = everything else stable, movers at a frozen LFO phase.
- **run40M-vs-settled: 0 bytes differ outside the movers** — `wcs_run_concert.json` was already the
  settled default (different phase). Fresh capture: `wcs_settled_concert.json`.
- `d2a2_low_state.py` (corrected reading after the run): **the power-up 0x3C00-05 slider bytes are all
  0x00 — a "no position" sentinel** (the LARC never sent physical positions in our harness). The
  variation-1 preset state is applied by the **NVS recall path at program load** (netlist §7.3) — that
  IS the D2a transient — so the settled image is the documented variation-1 state by the recall route,
  not by slider apply. Slider writes are one-way (writing 0 back is ignored); injected positions apply
  through the documented word sets, live-confirming the June map on the verified core: **XOV →
  exactly [45,46,97,98]; DEP → exactly [29–32,81–84]**. LOW/HFD at probe value 0x80 moved no bytes
  (mid-scale plausibly maps onto the recalled preset's own values — LF 3.0 s / Treble 6.30 kHz);
  the d2b2 lo/hi extremes discriminate.

## 3. D2b — the documented-defaults oracle: the FAIL that found the bug

**Method first (plan §7):** per-band RT60 = Schroeder T30 on the Lundeby-truncated tail
(reverb_metrics primitives), octave + two-band split at the documented 720 Hz crossover, floor-subtracted
burst renders. **Validated on the benchmark IR** (`Concert Hall V1.1.L.wav` — a real 224XL at these same
documented presets): measures **LF 2.85 / mid 1.92 / broadband 1.99** vs documented **LF 3.0 / mid 2.0**
(−5%/−4%). (A naive block-RMS band fit without noise truncation had read LF 3.9/mid 2.6 — method error,
fixed before any model conclusion was drawn.)

**Pre-fix model at the settled default:** LF **1.39–1.42 s** (vs 2.85) — half; mid 1.62–1.66 (within
20%); predelay **chC main arrival 23.99 ms ≈ the documented 24.0 ms**, chA early (0.12/6.0 ms —
documented fine predelays are 0.36/10.2 ms; structure noted, not interpreted). Per the plan rule the
FAIL was diagnosed, not tuned:
- **band method** — eliminated (benchmark reproduces documented values);
- **capture point** — eliminated (D2a/D2a2; boot/run/settled all fail LF the same way);
- **static-image approximation** — eliminated as the primary cause by the **D4-lite modulation replay**
  (`d4lite_mod_replay.py`: snapshot the firmware's own LFO trajectory every 50k ticks, hot-swap the 4
  modulated words per frame at 62 ticks/frame): LF stayed ~1.5 s. (By-product: RT60 is measurably
  LFO-phase-dependent — frozen phases spanned 1.40–1.66 s broadband — the D4 co-sim remains real physics.)
- **remaining suspect** — the capture-window arithmetic for cmag&3≠0 words. The settled image has
  **14 pre-capture ("victim") words with cmag ∈ {13, 10, 6}, mirrored across the half-frames** — under
  0023's "effective coeff = cmag−(cmag&3)" those LSBs were don't-cares, yet they are systematic. No
  prior oracle covered cmag&3≠0 captures (D1 = cmag 32; POST never exercises capture timing; the comb
  self-tests compared the engine to its own closed form).

## 4. ★ The correction: the result register captures the PP bus

Re-reading netlist **§4.2** (owner-traced, 2026-06-28, sitting there all along): *"PP bus — sat-mux
output... loads = accumulator reg D input, **and (PP3..PP18 only) result reg D input**"* — the 74F374
result register's D pins are on the **combinational adder/sat-mux output**, not the accumulator
register's Q. At the XFER CK rise (slot-3.06 of step n) the adder holds
`ACC_registered (…+ppB(w_{n−2}), added @1.43) + PR (= ppC(w_{n−2}), latched @0.58)` — so

> **RES ← sat16((ACC + ppC(w_{n−2}) + 4) >> 3) — the FULL group MAC, pairC included combinationally.**

The ZERO clear at 4.43 replaces only the ppC *register* add — the value already reached RES through the
PP bus; the clear resets the accumulator for the next group (fig-3.4's reading unchanged). The 0023
engine read `res_from_acc(self.ACC)` — the register — an assumption every prior oracle was blind to.
One-line fix in `aru_freerun22_rtl.py`; consequences:
- **"effective coefficient = cmag−(cmag&3)" is DISSOLVED** — all stored cmags act at full weight; the
  mirrored 13/10/6 victim values are meaningful; B4's cell pole is −6/32 (not −4/32).
- Self-tests re-derived and green (passthrough unchanged `(8x−3+4)>>3 = x`; combs now EXACT vs the
  full-g closed form — g=21 decays at 21/32).
- POST untouched (single-step path) — green. D1 oracle unchanged — 16/16. D3 signatures unchanged
  (control nets) — 374/376.
- D2b re-run on the fixed engine: **[filled in §7]**

## 5. D3 — SM §5.7 signature analysis: the T&C module is signature-exact (374/376)

`d3_signatures.py` (analyzer `sig224.py` re-self-tested in-process; stimulus = the verified-core diag-3
capture):
- **The manual's own reference signature confirms the L+1 frame:** diag-3 = reset word 99 ⇒ L=29 ⇒
  **30 hardware steps**, and the T&C +5V reference `FP54` = the all-ones signature at **exactly N=30**
  (sig224's independent calibration). The ARU feedback reference `3696` = N=90 = 30×3 ARUCK. Dale's
  100-step/34.13 kHz claim, the row-L idle, and the fetch pipeline are now **hardware-manual-confirmed**.
- **Per-pin scoring:** the netlist pin map + the 0023 pipeline alignment generate every listed pin's
  30-bit stream at the DAB RSTB/ sample edge (PC = (n+1) mod F; MI = fetched row n+1; stage-1/OFST/ =
  w_n; stage-2 = w_n; CSIGN/ = w_{n−1}.MI23; M0//M1/ = ~pairC lines of w_{n−1} via the 74195 P3=Q2
  load; RESET/ = const-1 at the sample; RESETD/ = single-0 at the post-reset boundary; tcWR/MEMW//
  MEMR//WR DA//DP/RESET combs). ONE global window phase scanned (0..29) — the winner is the modeled
  RESETD/ boundary — everything else is structure:
  **374/376 listed pins MATCH (69/71 distinct signature values; 0 unmapped).**
- The 2 exceptions are presumed single-glyph digitization errata of the table transcription, each
  contradicted by same-net sister pins: U3.10 `00U0` (GND; sisters `0000`) and U11.6 `2PU6` (C4/ net;
  U5.12/U11.7/U11.13 = `29U6`). Noted in `224-signature-value-tables.md`.
- One benign netlist correction adjudicated by the table: §2T.5 g3's input pins 9/10 are swapped
  (tc_U34.pin10 = inv-Q4 net, pin9 = AS0) — electrically identical AND-gate inputs; noted in the netlist.
- The pipeline is VISIBLE in the table: stage-1 D vs Q pins carry different signatures exactly one step
  apart; U19's D/Q pairs share signatures; the serializer's Q2 shift-state matches at 3 pins.

**What D3 locks:** the WCS store/addressing, the reversed coordinate system, the fetch pipeline, the
L+1 frame, both stage latches, the offset complement, CSIGN's one-more-stage delay, the serializer
timing, the reset chain, and the device decode — at named hardware pins, against the manufacturer's
own measurements of a working unit. **The ARU datapath tables (feedback config) are the remaining
§5.7 lock** — they would oracle-pin the PP-bus capture arithmetic; needs the diag-3 `0x0D10` loop's
XREG pump sequence (banked as next session's D3d/A-priority).

## 6. D2c — cross-program documented-decay check (settled images, fixed engine)

Selector decode: the D0 ids are record first-byte values — 1=CONCERT, 2=PLATE, 5=DARK HALL,
6=HALL/HALL, 8=CHAMBER, 10=PLATE/PLATE, 12=CHORUS&ECHO(effect), 16=CD PLATE B, 17=RICH PLATE,
18=PLATE/HALL, 20=RES CHORDS(effect); **id 3 has no record with that first byte** in the 0xB800 array.
Settled renders (chA, burst, floor-subtracted Schroeder T30; note ±0.2–0.3 s LFO-phase spread applies):

| id | program | doc | verdict | RT60 | classification |
|---|---|---|---|---|---|
| 1 | CONCERT | 2.6 avg | WET-PASS/DENSE | 1.54 (this phase; 1.90 in D2b's capture) | LF gap open (§3/§7) |
| 2 | PLATE | 1.8 | WET-PASS/DENSE | **3.52** | NEW finding — decays ~2× LONG; needs the CONCERT-style per-band/state treatment before verdicting |
| 3 | *(invalid selector)* | — | FAIL, peak=rails | 4.28 | **(b/harness)** garbage load — retire from the oracle set |
| 4 | *(unlisted record — SMALL PLATE?)* | — | WET-PASS/DENSE | 2.43 | a real program; name it next session |
| 5 | DARK HALL | hall | WET-PASS/DENSE | 1.40 | plausible (a) |
| 6 | HALL/HALL | split | WET-PASS/DENSE | 1.61 | plausible (a) |
| 8 | CHAMBER | reverb | **INDETERMINATE, peak=5** | — | **(d) GENUINE** — near-silent even settled; top ARU-table-session candidate |
| 10 | PLATE/PLATE | split | WET-PASS/DENSE | 1.68 | plausible (a) |
| 12 | CHORUS&ECHO | effect | INDETERMINATE | 0.38 | **(c) needs-modulation** (chorus/echo with frozen LFO) |
| 16 | CD PLATE B | 1.8 | WET-PASS/DENSE | 1.49 | −17%, watch |
| 17 | RICH PLATE | plate | metric FAIL (tail 1.83 present) | 1.83 | check the metric's dry-gate vs this program's output structure |
| 18 | PLATE/HALL | split | WET-PASS/DENSE | 1.41 | plausible (a) |
| 20 | RES CHORDS | effect | WET-PASS/DENSE | 2.97 | (a) resonators ring long — correct-for-program |

D0's anomaly set is resolved: **3 = harness artifact, 12/20 = effect programs behaving as such,
8 = the one genuine engine/program discrepancy** (survives the settled capture AND the PP-bus fix).
(The display-name readback at 0x3F8E came back empty under the id patch — names above are from the
record map; wire the display milestone next time.)

## 7. Run-log verdicts (filled at session close)

- **D2b (fixed engine, settled default, documented presets, chA/chC):**
  **mid(>720) = 1.90/1.85 s — PASS (benchmark 1.92, documented 2.0; was 1.62/1.66 pre-fix)**;
  broadband 1.90/1.85 (benchmark 1.99); predelay chC 23.99 ms ≈ documented 24.0 ms;
  **LF(<720) = 1.48/1.51 s — still FAIL (benchmark 2.85, documented 3.0)**, and the octave detail
  shows the 8 kHz band running LONG (1.86 vs benchmark 1.51) — i.e. the remaining gap is isolated to
  the BAND-SHAPING corrective words (LF extension via LOW words 43/95 cmag 5 + crossover 45/46
  (cmag 28 ⇒ exact one-pole fc = fs·ln(32/28)/2π = 691 Hz @32,508 — within fc-definition fuzz of the
  documented 720 Hz; see §6b); HF damping via HFD words 40/41 cmag 22/10). The mid-band core, routing, frame, predelay, and now the capture arithmetic all reproduce
  documented/benchmark values. Diagnosis continues via the band-lever sensitivity probe
  (`d2b2_band_levers.py`) and next session's ARU signature co-sim.
- **d2a2 idempotence:** see run log (§2).
- **D2c table:** see run log (§6).
- **D4-lite (fixed engine):** LF 1.56/1.64, mid 1.43/1.44 chA/chC — live modulation time-averages
  the phase-dependent decay; it is NOT the LF mechanism.
- **⚠ LFO-phase spread (post-fix, broadband chA):** "settled" captures at different frozen phases
  render 1.54 (D2c's capture) / 1.59 (run40M) / 1.90 (D2b's capture); live replay 1.34–1.44. Any
  single-image RT60 quote carries ±0.2–0.3 s of frozen-phase uncertainty — quote the spread, or
  replay the modulation (d4lite), until the D4 co-sim retires the approximation.
- **d2b2 band levers (chained captures — each lo/hi pair clean for its own lever):**
  LOW lo→hi moves words [43,95] but the LF(<720) band does NOT respond (1.54→1.47) — while those
  same [43,95] bytes DOUBLE the measured MID band (base ~1.9 → **3.96 s**); MID works in its own
  band (3.96→1.24 across its range, words 44/62-68/96/113-119); HFD moves [40,41,92,93] with weak
  8 kHz response on its (contaminated) baseline (0.48→0.52).
  **⇒ THE NAMED HYPOTHESIS — the crossover band-routing is INVERTED in the engine:** the LF-extension
  correction (through the 45/46/97/98 shelf; one-pole 691 Hz ≈ the documented 720) lands on the
  wrong side of the crossover. One sign/group-boundary flip predicts, simultaneously: LF 1.5→~2.9,
  8 kHz 1.86→~1.5, LOW-lever→LF response, and the model's inverted LF<mid ordering. Falsify next
  session via the ARU §5.7 datapath signatures (the hardware arbiter for capture-group arithmetic)
  and/or a controlled shelf transfer-function measurement — NOT by flipping signs to fit (owner rule).

## 6b. The sample-rate challenge — fs measured from the real unit (owner question)

Owner challenge: a per-program frame rate (fs = 30.72e6/9/(L+1)) seems implausible for hardware with
clocked converters, and the crossover computing low (my crude `(1−a)fs/2π` gave 647 Hz vs the
documented 720) smells like a clock error. Resolution (`d2f_fs_from_ir.py`) — the model knows CONCERT's
structure in FRAMES and the benchmark IR is a real unit on a 96 kHz timebase, so fs_real is measurable:
- **Warped-envelope correlation** (model IR time-scaled by s vs the real IR, early 0.7 s): single clean
  peak at **s = 1.000 → fs_real = 32,508 Hz** (corr 0.816; the 34,133 Hz hypothesis scores 0.663, a
  local minimum). Fine scan at 0.001 resolution confirms s = 1.000.
- **Autocorrelation periodicities** match pairwise to 0.1–0.4 ms (~0.2%): model 125.1/129.5/137.2/141.5
  ms ↔ real 124.9/129.5/136.8/141.5 ms. At 34,133 Hz every real lag would sit 4.8% short. This is the
  strongest absolute-timebase validation of the model to date.
- Mechanism: the FPC is frame-SLAVED (RESET/ → FPC U4.pin2 input-cycle-counter sync; FPC CK = MS5;
  SAR conversion is triggered per event) — converters follow the frame; the fixed analog anti-alias/
  reconstruction filters tolerate the 31.3–34.1 kHz bank spread. **FP54@N=30 (D3) already proved frames
  are unpadded on Lexicon's own bench**, and a 105-step frame physically cannot beat 32,508 Hz at the
  traced MC/9 step clock. Predelay agrees: model 23.99 ms @32,508 ≈ documented 24.0 (at 34,133 it
  would be 22.85).
- **Where "34.125 kHz" comes from:** it is EXACTLY the 100-step frame (30.72e6/9/100 = 34,133 ≈
  dale/seancostello's 34.125) — the rate of the L=99 bank (PLATE, the diag delay programs, etc.) and of
  Dattorro's published algorithm spec (seancostello's identification came from the publication, and the
  subculture research file itself carries a "verify against hardware" flag on this exact number). It is
  the flagship rate, not CONCERT's: **the 224XL is a variable-frame-rate machine, 31.3–34.1 kHz across
  the bank, and the real CONCERT measures 32,508 Hz.**
- The crossover: with the exact one-pole corner, cmag 28/32 gives 691 Hz @32,508 (my 647 was the crude
  approximation). The remaining −4% vs the documented "720 Hz" is a filter-topology/fc-definition
  question (the XOV structure is two words per side; the single-word read is a simplification), now
  DECOUPLED from the clock — it rides with the D2d range verification.

## 8. Dead-end / discipline registry (additions)

| # | Item | Verdict |
|---|---|---|
| 17 | Result-reg capture = the registered ACC | **DEAD** — §4.2: RES D-pins are on the PP bus; capture = ACC + PR combinationally (the pairC IS captured) |
| 18 | "effective coeff = cmag−(cmag&3)" (0023 §1 consequence) | **DISSOLVED** by #17 — full stored weight; the 13/10/6 victim cmags are live values |
| 19 | Band RT60 by block-RMS slope without noise truncation | CONFOUNDED on real IRs — use Schroeder T30 on the Lundeby-truncated tail (validated on the benchmark) |
| 20 | Mainloop-snapshot WCS as "the program" | DEAD as a default-state capture — pre-apply; settle ≥2M ticks and confirm quiescence outside the 8 movers |
| 21 | Boot-image cross-program verdicts (D0) | CONFOUNDED by #20 — re-render from settled captures |
| 22 | Fixed 34.125 kHz sample rate for all programs | **DEAD** — fs_real(CONCERT) measured = 32,508 Hz from the benchmark IR (envelope-warp corr peak at s=1.000; autocorr lags match ~0.2%); 34.125k = the 100-step-frame rate of the L=99 bank only (`d2f_fs_from_ir.py`) |

Registry #16 (impulse metrics) unchanged; #13/14/15 (clear-owner/1.43-clear/same-edge ACC) unchanged —
the PP-bus correction touches the CAPTURE SOURCE, not the clear timing those falsified.

## 9. Verification state

- Engine `tools/aru_freerun22_rtl.py` @ PP-bus capture: self-tests ALL PASS (golden-anchored booth3,
  passthrough, full-g combs ×2, CONCERT extraction).
- POST E32/E40/E83/E91 green (un-suppressed, single-step path) — re-run post-fix.
- D1 16/16 PASS post-fix (WAVs in `renders/d1_*`); D3 374/376 post-fix.
- All audio claims via `reverb_metrics` (battery in-process per run) or Schroeder T30 on
  floor-subtracted tails, WAVs on disk (`renders/d2_*`, `d2c_*`, `d4lite_*`).
- New probes: `d1a_capture_diag.py`, `d1b_regression.py`, `d1_diag_oracles.py`,
  `d2a_capture_settled.py`, `d2a2_low_state.py`, `d2_param_rt60.py`, `d2c_settled_all.py`,
  `d3_signatures.py`, `d4lite_mod_replay.py` (+ caches `wcs_diag.json`, `wcs_settled_concert.json`,
  `wcs_settled_all.json`, `d4lite_snapshots.json`).

## 10. Open (next session)

1. **ARU §5.7 signature co-sim** — the datapath oracle that pins the PP-bus capture at hardware pins:
   trace the diag-3 handler's signature-pulse loop (`0x0D10`) for its XREG write sequence + frame
   phase, emit per-ARUCK accumulator/PR/adder pin streams, score the ARU no-feedback + feedback tables.
2. **D2 close-out** per the D2b re-run verdict (below): if LF still short → the LF mechanism hunt
   continues with the pairC question settled; if PASS → D2d documented-range verification.
3. D3d stretch: DMEM table (CLOCK=RESET/, window=CPC-MSB) and FPC table (diag 6).
4. D4 true co-sim (interleaved 8080) — the phase-dependence measured here makes it material.
5. `aru_whole.py` / C++ scaffold re-sync to the corrected capture.
