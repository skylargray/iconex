# 0027 — The complement domain and the ARU pin lock (plan 023 executed)

**Date:** 2026-07-02 (follows 0026)
**Scope:** execution of `docs/plans/023 - 224XL-ARU-signature-lock-live-cosim-and-calibrated-ranges.md`
(E1 complete; E2a-c complete; E3a/E3c complete + E3b partial; E4 complete; E5 partial — the
engine re-sync is specified and banked).
**Result:** ★★★★ the ARU §5.7 signature tables verify the ENTIRE MAC datapath at hardware pins —
**1467/1469 listed pins match; the feedback table is 710/710 PERFECT** — and getting there
uncovered the project's deepest simplification yet: **the DAB physically carries ACTIVE-LOW
(complemented) values, and in that domain the exactly-traced wiring computes the E83 goldens by
PURE TRUNCATION — the engine's '+4 round', the '+3 dual-rail correction', and the POST '-M-1
negative law' all dissolve as CPU-domain bookkeeping of the same physical bits.**

---

## 1. E1a — the signature-pulse loop is silent; the XREG pump initializes the regfile

Runtime trace on the verified core (`e1_xreg_trace.py`, 3 boots, both pacings):
- The `0x0D10` loop (`CALL 0x02AD; JP 0x0D10`) performs **ZERO DSP-port writes** — it is a
  key-poll idle. The bench state is the ARU free-running with **XREG = 0x607F, static**.
- The setup pump (`0x0D1E`, called twice) writes XREG values **AAAA / 9999 / C787 / 607F**,
  each followed by a single-step strobe, with WCS pokes `0x41FA <- F6/FA/FE` between — decode:
  the pokes cycle the parked word's **WA through 1, 2, 3**. The pump is **regfile
  initialization**: R1=0x9999, R2=0xC787, R3=0x607F (idempotent via the double call), R0 takes
  0xAAAA through the POST-leftover parked word. R0-R2 are never written by the free-run program
  (every diag-3 row has WA=3) = constant E83-pattern operands. 0xAAAA x 47/32 x 8 = 256.7k sits
  2% under the ±2^18 SAT rail — near-max stimulus, deliberately not saturating in the
  no-feedback window.
- Setup byte-identical across boots; the executed WCS (words 99-127) byte-identical to
  `_diag3_wcs.bin`.

## 2. E1b — the analyzer convention derived BEFORE scoring (the N=62 falsifier)

Enumerating clock polarity × START polarity × window side against BOTH manual +5V references
jointly: **exactly one convention survives — CLOCK = ARUCK FALLING edges, START = RESET/ rise —
giving no-feedback N=62 (29F3) and feedback N=90 (3696) simultaneously** (`e1b_window_predict.py`).
The N=62 window independently confirms the XFER-edge placement (first XFERCK after RESET/ =
step 20 of the NEXT frame at slot 3.06; a misplacement would give ~59/65). Independent
confirmations in the tables: ARUCK pins read `0000` (own-fall sampling), Vcc pins read the
+5V reference of each window length.

## 3. ★★ E1c — the complement domain + the per-pin lock (1467/1469)

`e1c_backend_resolve.py`: no CPU-domain bit convention of the traced wiring reproduces the E83
goldens by truncation (best 10/20, misses = exactly the mod-8 rounding boundaries). Adding the
domain axis: **two arithmetic-identical variants hit 20/20 — both in the COMPLEMENT domain,
with the traced wiring exactly** (rail = inv(CSIGN/), cin = inv(rail) via the aru_U2 inverters,
PR = comb_array output, '163 clear-to-0, no dual-3, no capture bias). Physical origin: the XREG
write bridge (dmem_U39/U41) carries the SBC's complemented `DATA0-7/` levels onto the DAB with
no inversion (§5.6) — the whole ARU computes on active-low values, and every boundary
(XREG readback, FPC) complements back.

`e1_aru_signatures.py` (the slot emitter + 794-pin map + scorer, both tables, one global
window phase): **champion = the traced complement-domain convention at rot 89 = the E1b
anchor: 1467/1469 MATCH; feedback table 710/710 PERFECT.** The two exceptions are single-glyph
digitization errata contradicted by same-net sister pins (**U51.12** `33FC`→`35FC`, sister
U52.12; **U39.14** `F1CU`→`F1C0`, sister U41.3) — noted in the tables doc.

Measured along the way (each a named physical fact the table adjudicated):
- **Sampling physics:** the analyzer samples LATE in the ARUCK cycle — both ripple chains have
  settled to the CURRENT computation at the sample (front-end live; PP/AC/carries one sample
  past my initial 'about-to-register' emission) while the registers still capture the OLD sums
  at their earlier edges — **fig-3.4's one-AS-behind pipeline is intact and now pinned from
  both sides.** DAB WSTB/ reads all-ones (the MS7 write pulse precedes the sample instants).
- **Field timing:** the stage-1/offset field family (RA/WA lines, regfile addressing) changes
  between S0 and S1 (~slot 2-3), one sample after the JK/serializer family — retro-explains
  the operand write-through without the LS670-propagation story.
- **Netlist corrections (electrically inert relabelings, now bannered in §4.1/§4.2):** the
  '163 Q pin roles are within-nibble REVERSED (pin14 = bit3 … pin11 = bit0, with the adder-A
  pin roles reversing identically); the result-register chips **U43↔U44 are swapped** (U43 =
  high byte).
- **Saturation:** diag-3 deliberately saturates at the frame tail (cmag-47 rows on the 0x607F
  operand); the feedback table SHOWS it (U42.3 = `000P`) while the no-feedback window's STOP
  placement excludes those samples (U42.3 = `0000`) — and the traced sat-mux clamp FEEDS THE
  ACCUMULATOR (converging to the ±rail; the engine's wrap-only ACC is an erratum candidate
  whenever SAT fires transiently mid-group).

**What is now pinned at manufacturer-measured hardware pins:** the Booth NAND array + front-end
adder chain + product register, the sub-XOR row + CSIGN JK timing (own-sign窗口), the back-end
adder + carry chain, sat-mux/clamp/SAT detect, the accumulator, the result register (PP3..18
pure bit tap), the regfile + write-through, the shifter/serializer schedule (S0/S1 mode lines
included), the XREG/DAB routing, the L+1 frame, and the complement bus domain.

## 4. ★ E5 finding — the engine diverges from the physical law at sub-LSB

`e5_engine_vs_physical.py`: RTL22's value model (product20 + `(v+4)>>3` uniform) vs the
pin-locked physical law differ by **±1-2 LSB on most captures** (lone negative unity:
consistently −2; odd cmags ±1; ~70% of random-program frames) — invisible to every RT60/POST/
D1 oracle, but real. **The physical law is the anchor (1467/1469 pins). The engine MAC core
should be re-expressed in the complement domain** (CPU value = ~physical at the boundaries);
that re-sync requires re-running the full oracle battery and is the top next-session item —
the probe is its spec and regression.

## 5. E2 — the TRUE live co-sim (D4 proper; D2b formally closed)

`e2_live_cosim.py`: one process, the frame-sync flag `0x3C14 <- 0x80` per frame +
`run_ticks(m, 62)`, mover bytes harvested at frame granularity (audio does not feed back into
the 8080 — the trajectory is capture-equivalent). **Non-mover WCS drift: NONE across 211k
frames** (full-image spot checks).

| CONCERT (6.5 s) | LF(<720) | mid(>720) | broadband |
|---|---|---|---|
| live co-sim chA / chC | **3.27 / 3.25** | **2.28 / 2.23** | **2.68 / 2.64** |
| documented | 3.00 | 2.00 | **2.60 (avg)** |
| benchmark IR | 2.85 | 1.92 | 1.99 |
| d4lite (0025) | 3.20 | 2.22 | 2.67 |

Broadband within 3% of the documented average, zero parameters tuned — the frozen-LFO
approximation is retired and the plan-022 D2 mission is formally closed. **The LFO period
measured under true pacing: ~325k instructions (~23.6k frames) vs the documented ~345k** —
the modulation clock validates. **E2c chorus:** the tap sweep tracks the depth byte 0x3CD4
(span 14 / 34 / 126 frames at depth 0x02 / 0x04(default) / 0xF0); deep chorus mildly shortens
measured RT60 (3.00/2.15/2.56) via modulation decorrelation. WAVs in `renders/e2_cosim_*`.
E2d (stop-decay dynamics) banked: the level-detector source remains untraced; V6/V7's
DynDecay structure is confirmed at the toggle level (§7).

## 6. E3 — the display calibration (registry #28 closed for page 1) + the key map

**The display is the calibration instrument:** slider injection triggers the firmware's own
value render into the message buffer **0x3F4F** (the 0026 readback at 0x3F8E was the wrong
buffer). Two new mechanisms measured (`e3_display_calibration.py`, `display_map.json`):
- **Soft takeover (slider pickup):** a slider is IGNORED until it crosses the recalled preset,
  then tracks. (Reframes 0025's "slider 0x02 = the recall value" — 0x02 simply hadn't picked
  up; the true low ends sit below the presets.) Calibration = ascend to pick up, then descend.
- **Byte↔value maps (page 1, CONCERT):** LF/Mid decay **0.6 s (≤0x08) → 3.0 (0x80) → 70 s
  (0xF8) — the documented 0.6-70 s endpoints EXACT**; XOV/Treble corners **170 Hz (≤0x08) →
  720 (0x20) → 19.0 kHz (0xF8) — the documented 170 Hz-19.0 kHz EXACT**; Depth/% = byte/2.56
  (0-97 at 0xF8 ✓ the 0026 law); FinePD-R 1.00→31.7 ms (doc 31.3); **Predelay 26→862 ms
  (clamps ≥0xC0) — the formatter tracks far past the documented 216 max** (the true preset
  displays 024 MSEC ✓ via the param-select key). Pages 2-5 rendered with page-1 formatters —
  the display page follows the LARC PAGE key, not the apply-page 0x3C34 (see the key map).
- **The LARC key map** (`e4_key_enum.py`, `key_map.json`): modal UI — **0x21 = PROGRAM-select,
  0x22 = BANK-select, 0x26 = VARIATION-select; number keys 1-8 = 0x2C/0x30/0x34/0x38/0x3C/
  0x2D/0x31/0x35; 0x3E = PAGE (sets the display page AND 0x3C34); param-select keys
  0x23/0x27/0x2B/0x2F/0x33/0x37 display the current value WITHOUT touching it; 0x2E = DynDecay
  toggle prompt; 0x3A = second function; 0x25 = register recall.**
- **E3c — the program name map** (`e3c_names.py`, `program_names.json`): B1 HALLS (CONCERT
  0x01, BRIGHT HALL 0x20, DARK HALL 0x05), B2 ROOMS (ROOM 0x04, SMALL ROOM 0x40, CHAMBER 0x08,
  RICH CHAMBER 0x80, DARK CHAMBER 0x41, INVERSE ROOM 0x81), B3 PLATES (PLATE 0x02, **SMALL
  PLATE 0x03**, CD PLATE A 0x21, CD PLATE B 0x10, RICH PLATE 0x11), B4 EFFECTS (CHORUS&ECHO
  0x0C, RES CHORDS 0x14, M BAND DELAY 0x24). **The D2c anomalies dissolve: 'id 4 unlisted' =
  ROOM; 'id 3 invalid' = SMALL PLATE (a real program — the power-up-id patch garbage was a
  harness artifact).** The ids are bit-coded, not sequential.
- **E3b formal (partial):** the calibrated endpoints replicate on a fresh boot (0.6/70 SEC,
  230 MSEC displayed). Renders: mid-lo measured 1.31 s vs 0.6 displayed (confound: LF-band
  bleed through the 720 Hz split once the short mid tail drops below the long LF); mid-hi
  10.4 s (−12 dB fit) vs 70 (confound: near-unity loops are exquisitely sensitive to the
  frozen LFO phase — the co-sim is the fair test); PDL arrival detection was too crude (25%
  threshold catches the depth early component). All three carried as named follow-ups, not
  verdicts.

## 7. E4 — the variation oracle (predictions confirmed)

Recall through the REAL variation keys (`e4_variations.py`, predictions declared first):

| var | documented LF/Mid | prediction (w43/95) | measured w43/95 | verdict |
|---|---|---|---|---|
| V1 | 3.0 / 2.0 | small boost (cmag 5) | cmag 5 cs1 | ✓ |
| V2 | 1.7 / 1.7 | **~ZERO injection** | **cmag 0** | ✓✓ the shelf-zero test |
| V3 | 3.8 / 2.4 | boost (ratio 1.58≈V1's 1.5) | cmag 5 cs1 | ✓ (ratio-law: same ratio → same cmag) |
| V4 | 3.0 / 3.0 | **~ZERO injection** | **cmag 0** | ✓✓ |
| V5 | avg 6.5 s | long everything | cmag 2, w44 cmag 22 (long mid) | ✓ |
| V6/V7 | DynDecay pair | — | **toggles 0xC1 (DynDecay ON)**, w44 = 9 vs 22 mirror | ✓✓ documented dynamics structure |

V1 restores exactly after the cycle. **E4c renders vs ch.4** (static settled images, ±0.2-0.3 s
frozen-phase spread): **V2 = 1.78/1.59 vs documented 1.7/1.7 (within 5%/-8%)**; V3 = 4.39/2.99
vs 3.8/2.4 (+13/+23% — the known static-image bias direction, cf. V1 static +12/+15%);
**V5 broadband 7.04/7.18 vs the documented 6.5 s average (+8%)**. WAVs in `renders/e4c_*`.

## 8. Registry additions

| # | Item | Verdict |
|---|---|---|
| 29 | CPU-domain bit-level back-end (any polarity/cin/clear variant) | **DEAD** — max 10/20 E83 goldens by truncation; the physical datapath computes in the COMPLEMENT (active-low DAB) domain where the traced wiring is 20/20 exact (`e1c_backend_resolve.py`) |
| 30 | '+4 round', '+3 dual-rail', '-M-1 law' as physical mechanisms | **DISSOLVED** — CPU-domain bookkeeping of the complement-domain truncation (all three; the aru_booth/aru_cycaccurate empirical corrections stand as VALUE-level identities only) |
| 31 | RTL22 value model == physical at sub-LSB | **FALSE** — ±1-2 LSB on most captures (`e5_engine_vs_physical.py` = the spec + regression for the re-sync); every headline oracle blind to it |
| 32 | Slider byte applies directly from any position | **FALSE** — soft takeover: ignored until the slider crosses the recalled preset (pickup), then tracks; calibrate ascend-then-descend |
| 33 | 0x3C34 as THE page state | PARTIAL — it is the APPLY page; the DISPLAY page follows the LARC PAGE key (0x3E sets both) |
| 34 | d2c id namespace sequential/invalid ids | DEAD — ids are bit-coded record tags; 0x03 = SMALL PLATE, 0x04 = ROOM (`program_names.json`) |
| 35 | Engine ACC wrap-only (no clamp into ACC) | ERRATUM CANDIDATE — the traced sat-mux clamp feeds the ACC D inputs; matters only when SAT fires transiently (diag-3 tail proves the path); fold into the re-sync |

## 9. Verification state

- POST/self-test battery untouched this session (no engine edits); all probes ran on the
  verified core + RTL22 as-committed. E1c results reproducible via
  `python tools/session0022_probes/e1_aru_signatures.py` (steady in 33 frames; ~2 min).
- New probes: `e1_xreg_trace.py`, `e1b_window_predict.py`, `e1c_backend_resolve.py`,
  `e1_aru_signatures.py` (+ `e1c_results.txt`, `e1c_scores.json`, `xreg_pulse.json`),
  `e2_live_cosim.py` (+ `e2_cosim_*.json`), `e3_display_probe.py`,
  `e3_display_calibration.py` (+ `display_map.json`), `e3b_endpoints.py` (+ `e3b_states.json`),
  `e3c_names.py` (+ `program_names.json`), `e4_key_enum.py` (+ `key_map.json`),
  `e4_variations.py` (+ `variation_params.json`), `e4c_variation_renders.py`,
  `e5_engine_vs_physical.py`. WAVs in `renders/` (gitignored, regenerate).
- Docs: signature-tables 0027 note (+2 ARU errata); netlist §4.1/§4.2 pin-role corrections.
- `224XL_timing_spec.md` checked for pre-E83 sign claims: none (its CSIGN rows are
  decode-pointers; generated file) — no banner needed.

## 10. Open (next session)

1. **THE ENGINE RE-SYNC** — re-express the RTL22 MAC core in the complement domain
   (`e5_engine_vs_physical.py` = spec + regression): fold in the sub-LSB law, the SAT-clamp-
   into-ACC path, then re-run the FULL battery (POST, D1 16/16, D3 374/376, E1c 1467/1469,
   D2b co-sim) and re-render the headline verdicts. Then `aru_whole.py` / C++ re-sync.
2. E3b clean-up: mid-lo with both bands short; mid-hi under the co-sim; PDL arrival via
   main-peak detection. Page-2..5 display calibration via the PAGE key (0x3E).
3. E2d stop decays: trace the level-detector source (0x83B4/0x83D1 back-refs); V6/V7 are the
   test cases (toggle + presets already confirmed).
4. E1d: the DMEM signature table (CPC-MSB window) + FPC table (diag-6 capture via the menu).
5. `reverb_metrics`: first-class floor-subtraction mode (probes do it manually today).
6. D2c re-score with the true names/ids (`program_names.json`) incl. ROOM vs its documented
   1.4 s.
