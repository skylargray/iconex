# 0028 — The engine re-sync, the table sweep, and the graduated stop-decay (plan 024 executed)

**Date:** 2026-07-02 (follows 0027, same day)
**Scope:** execution of `docs/plans/024 - 224XL-complement-domain-engine-resync.md`
(F1 complete incl. the C++ port; F2a complete; F2b foundations banked; F3 mechanism
closed with named leftovers; F4a/c/d done (F4b carried); F5 complete).
**Result:** ★★★★ the engine of record now COMPUTES IN the pin-locked complement domain —
the full oracle battery is green with **e5 at ZERO differing frames** and the corrected
signature tables at **1469/1469 (ARU) / 376/376 (T&C) / 167/167 (DMEM, new)** — and the
stop-decay dynamic is a live, traced mechanism: the DSP posts the raw input sample to the
X-register every frame, the firmware level-tracks it, and a graduated scheduler walks a
twelve-word coefficient family down (11→10→9) starting ~151 ms after the input stops.

---

## 1. F1 — the complement-domain engine re-sync (the gate; everything passed)

**F1a/F1b.** `tools/aru_freerun22_rtl.py` rewritten: internal state (regfile/DMEM/RES/DAB/
ACC) carries the PHYS (active-low) patterns; per accumulate `backend20` = the traced
adder/sat-mux (rail = cs, B = raw^railmask, cin = inv(rail), 20-bit sum, SAT = s19^s18,
clamp 0xC0000/0x3FFFF by topB) whose output loads BOTH the result path and the '163
accumulator (registry #35 folded in); `raw3` = the raw comb-array partial products of the
phys operand (PRLOAD=raw); capture = the pure PP3..18 bit tap; boundaries complement
(RD-AD `~x`, WR-DA `s16(~DAB)`, XREG both ways; new `XREG_host` attribute for bench
states). `booth3`/`product20`/`res_from_acc`/`wrap20` remain as VALUE-LEVEL identities
(registry #30) for tests and historical probes — not in the datapath.

The self-tests were RE-DERIVED from the law (the value view: π(phase) = s20(raw)+1 on the
phys operand; ±π by cs; ZERO clear → value −1; capture = arithmetic >>3, wrap-free by the
rails; word sum Σπ(F,c) = 3·dual(c)+3−product20(−F−1,c,1)):
- passthrough y == x EXACT for all x incl. ±full-scale (V₁ = 8x+7);
- **negative unity y = −x−2** (the physical −2 LSB the e5 census measured; +FS clamps to
  −32768 through the sat-mux) — a new pin the old engine could not pass;
- comb closed forms EXACT (V₁ = 8x+10+3·dual−P20(−y'−1,g,1)), incl. multi-pair cmag 21
  and the FLAG-SIGN INERTNESS pin (zero-cmag phases have π = 0 exactly — the old '±3
  residue' idioms dissolve, registry #30);
- the own/lag CSIGN split REDESIGNED for the phys law (zero-cmag flag words are inert, so
  the discriminator is a cmag-5 pairC retiring during an opposite-sign word; own-sign:
  the register loads the captured PP value exactly);
- a SAT-clamp-into-ACC walk (transient mid-group SAT converges to the rail: y = −1 where
  a wrap-only ACC would ghost +32767) — the #35 regression;
- the XREG host-latch boundary (0x607F reads back exactly).

**F1c — the battery, in the mandated order, all green:**
1. POST E32/E40/E83/E91 un-suppressed (hard-asserted in the D1 run).
2. D1 diag oracles **16/16**, unity EXACT ±0 (impulse peaks +16000, lags 1/0x3FFF).
3. D3 T&C **376/376** against the owner-corrected table (was 374/376; the U3.10 `00U0`
   and U11.6 `2PU6` glyphs owner-confirmed as source errata, corrected in the block with
   originals recorded — the tables doc carries the note).
4. e1c ARU signatures **1469/1469** (no-feedback 759/759 + feedback 710/710) at the
   unchanged champion (raw/cs/0/0 @rot 89) against the owner-corrected tables
   (U51.12 → 35FC, U39.14 → F1C0). NEW `f1_e1c_engine_xcheck.py`: the engine locks
   BIT-IDENTICAL to the scoring Emitter across 240 steady steps (ACC/RES/regfile/DAB
   per step) on the diag-3 bench.
5. `e5_engine_vs_physical.py` (untouched): **ZERO differing frames** across the whole
   battery — registry #31 closed.
6. Audio: live co-sim LF 3.22/3.24, mid 2.30/2.24, **bb 2.68/2.65** (0027: 3.27/3.25,
   2.28/2.23, 2.68/2.64 — max move 0.05 s, far inside the 0.15 s stop-gate); D2b settled
   battery PASS (all four ±20% checks; method validated on the benchmark IR first); the
   idle floor re-measured as predicted-different: **chA DC +12.4 LSB / chC −5.4 LSB,
   AC-RMS 2.0/3.4 LSB, near-DC drift** — same DC-dominated character as 0025's law
   (floor-subtract everything stands).

**F1c side finding — the diag-3 stale cells.** The steady frame is NOT
write-before-read closed: MEMR rows 1/4/5 read cells last written 54426/5555/65536
frames earlier (through the CPC wrap; the steady written value V* = phys 0x8000, the
saturated tail capture). The read value never reaches a MAC operand (WA=3 every row;
every RA=3 load samples R3 one step after an IO overwrote it) and differs from the
unwritten default only in DAB bit 15 — and BOTH DAB15-carrying pins (U29.15, U43.6) are
UNLISTED, so H0 (stale reads decay to phys 0) and H1 (DRAM retains across the wrap →
0x8000) both score 1469/1469 (`f1_dmem_stale_reads.py`): the convention is
measured-inert to the lock and stays an open bench question.

**F1d — downstream re-syncs.**
- `aru_whole.py`: default engine = the pin-locked RTL22 (adapter with per-image row
  cache; program-defined fs stamped into captures); behavioral engine reachable for
  archaeology only; self-check green end-to-end (DRY verdict at fs 34133.3).
- The C++ scaffold REWRITTEN to the physical law (`libs/sgdsp/.../224xl.hpp` +
  `224xl_booth.hpp` gate-array transcription): new exporter + diff harness prove
  **bit-exact parity on FOUR cases — d1zero, d1max, CONCERT-settled across 66,000
  frames INCLUDING the 65536-frame CPC wrap, and sig6 (the diag-6 program with
  XREG_host = 0xFAAA, covering the host→DSP latch complement bridge)**; booth vectors
  4000/4000 + backend20 200/200 (151 clamp-rail cases); negative controls trip on
  single-bit flips (the sig6 control fails at frame 0 step 51 with the phys complement
  0x0555 visible on the bus). The DSP→host WR-XREG readback remains the single
  golden-unexercised C++ boundary (README notes it). Built with MSVC (the
  DaisyToolchain g++ is an ARM cross-compiler — noted in the harness README).

## 2. F2a — the DMEM signature table: 167/167 at a fully pre-derived convention

The SM lift-jumper ("U65.13 → U65.1") DERIVED before scoring: it re-clocks U65's high
nibble from cpc11 (falls per 4096 frames) to the cpc7 NET on pin 1 (falls per 256), so
**modified cpc12-15 mirror cpc8-11 and the "CPC MSB" (U65.8) period = 16×256 = 4096
frames = the manual's own +5V reference `826P`** — that is WHY the SM rewires the
counter: every sampled stream must be window-periodic. The table then confirmed the
wiring internally: U65.13 = U65.1 = U51.8 = `C25F`; mirror pairs `5H21`/`HP66`/`U81P`;
mux SEL pins `0000` (ROW SEL low at the sample → column side A8-15 on AD0-7); the adder
B-constants = row 29's IO command word (OFST6/+OFST12/ high = WRX + sel=1 — the live
word at the RESET/ rise, not the reset word); the carry chain crossings and the
U49-Σ→U36-B net identities all agree. `f2_dmem_signatures.py`: **167/167** listed pins
(incl. the U1-16/U20-35 DRAM-common address pattern and the U17 33Ω pack pairs) at
live-row=29 / post-bump / rot 0 — the exact predicted anchor. One source erratum found
and OWNER-CONFIRMED in-session: **U65.4 (1QB = cpc9) read `0000` while its same-net
sister U63.3 AND its lift-jumper mirror U65.10 both read `19H6`** (a counting bit cannot
be constant while its bus twin counts) — corrected in the tables doc (original recorded
in its note); the netlist §5 needed no change (the model used it as-is).

## 3. F2b — the FPC table foundations (the per-pin emitter is staged, not built)

`f2_fpc_foundations.py` banks, each verified:
- diag-6 captured on the verified core via the **0x0330 menu table** (item 6 → handler
  0x0E84; anchors item3/7/8 = the known handlers; d1a route, 512/512 agreement) →
  `wcs_diag.json["sig6"]`;
- the window RECONCILED: diag-6 extracts as w_reset=31, **L=97 → a 98-step frame**;
  CLOCK = FPCCLK at 1/step with START=STOP=RESET → N=98 = sig224's `96F6`;
- the bench state decoded from the 0x0EEC pump block (same 0x0D1E routine as diag-3's,
  F6/FA/FE parked-word WA cycle): **R0=0x5555, R1=0xCCCC, R2=0x1999, XREG=0xFAAA**;
- the steady frame streams EXACTLY those four constants to the D/A (A/B at steps 2/3
  from the R0/R1 unity captures; C/D at steps 52/53 from R2/XREG, half a frame apart) —
  hand-derived from the value law, engine-confirmed. No RD-AD step: the SAR lift
  (U26.11→+5V) leaves the AIN idle pattern to the FPC pins — the e1c AD_CONST question
  lands there. The emitter build (766-line owner FPC trace at fpcCLKA granularity,
  fig-3.5/3.6) is the next session's e1c-scale piece.

## 4. F3 — the stop-decay dynamic: mechanism CLOSED, two named leftovers

**F3a (disassembly, `dis224.py` on the NVS window).** The input-level detector's source
is the **DSP→host X-register readback**: 0x829D..0x82CD does IN A,(0x07)/IN A,(0x06)
with a one's-complement abs and peak-holds into 0x3E38 — and the WCS supplies it:
**CONCERT's row 0 (CPU w127), the RD-AD input word itself, carries WR XREG** — the raw
A/D input sample is posted to the latch every frame. Chain: peak-hold → log-compress
(MSB normalize + 0x0FB7) → the RUNNING level 0x3E10 (instant attack; release via the
10-deep history ring 0x3E15-1F, shifted per tick at 0x83F8) → the DynDecay gates
(0x3CCD bit 0 = the arm toggle — V6/V7 recall 0xC1, V1 0xC0; 0x3C51 = the state byte;
jump/drop thresholds 0x27/0x16/0x18 on the ring deltas).

**F3b (`f3_stop_decay.py` + `f3b_switch_hunt.py`).** The co-sim gained the ONE
documented feedback edge: the engine's `XREG_wr` (the re-synced core maintains the
CPU-domain readback natively) served to the 8080 at IN 0x06/0x07, fully inline
(no trajectory replay — the trajectory now depends on the audio). Measured on V6
(armed), with a forced-loud control and a V1 (unarmed) control:
- the level state TRACKS the burst and releases after it (P1 PASS; both controls clean);
- **~151 ms after the input stops** (matching the manual's "time delay in switching
  from running decay to stopped" parameter) the stop event stages (0x3E11←1,
  0x3E14←0x0F) and a de-zipper walk (~24 frames/word) steps the **cmag of the
  twelve-word family w62/63/64/66/67/68 + their +51 mirrors w113-119 DOWN one unit at
  a time (11→10→9)** as the level falls through the ring thresholds — and back up when
  it returns. A GRADUATED decay-coefficient scheduler, not a binary flip.
- The plan's "w44-family 9↔22" target was the V6-vs-V7 VARIATION difference, not the
  runtime dynamic (registry #38).
- Named leftovers: (a) the 0x80/0xBC loudness gates sit ABOVE the XREG-log ceiling
  (~0x37 at −1.4 dBFS) — those branches ride another term (0x3C62 OR-in; overload-flag
  candidate) (#39); (b) late-tail 0x3E10 hops 0x07↔0x17 at ~the LFO period under zero
  input — source untraced (#40); (c) the audible stop-vs-running tail contrast needs
  the page-2 Stop sliders set apart from the running decays (next session, now that the
  page-2 display calibration exists).

## 5. F4 — E3 clean-ups

- **F4c (the PDL range).** Owner-manual Table 4.2 (Concert Hall) documents Predelay
  **24.0 → 216 msec** (Bright Hall 4.3 identical) — 216 IS the documented hall maximum.
  The 0027-calibrated formatter tracking to 862 ms at the 0xC0 clamp means the firmware
  accepts bytes ~4× past the documented factory range (216×4 = 864 ≈ 862): the
  documented range occupies the low quarter of the physical byte scale.
- **F4a (pages 2-5 display calibration, `f4_display_pages25.py`).** All pages
  calibrated with the PAGE key pressed + verified per page; `display_map.json` gains
  `p{2-5}s{1-6}` records (page-1 preserved byte-for-byte). Highlights: **p2 LF/MID STOP
  DCY presets render 3.0/3.0 SEC — the documented V1 stops EXACT** (the stop targets the
  F3 scheduler switches toward); the stop sliders ride the same 0.6-70 s ladder as the
  running decays; Chorus/Diffusion % = byte/2.56; HFBW = the corner ladder (preset
  9.00 kHz); DEFINITION % clamps at 75; p3 = routed levels (`L)A R)C R)A L)C`, presets
  4/4 exact); p4 DELAY 1-4 = **1.125 ms/byte** (soft top 180-188 ms), FIN PDLY =
  **0.140625 ms/byte → 31.3 ms** (documented 31.3 ✓); p5 SIZE 10→40 METERS; REV STOP
  DLY displays 0.00 across the byte range on CONCERT. NEW refinements (recorded in the
  JSON notes): the PAGE key SKIPS apply page 4 (display 5 pairs with 0x3C34 = 5 —
  refines registry #33); page-4 ascend writes land 25 slider-bytes low vs descend
  (descend = the calibration); pages 4/5 preset STORAGE is finer than the slider scale
  (the flat array 0x3CA3+page·6+slider is preset-exact for pages 1-3 only).
- **F4d (the d2c re-score, `f4_d2c_rescore.py`)** — settled cache through the re-synced
  engine, floor-subtracted, true names (`program_names.json`), spec rows: CONCERT
  **PASS** (+10/+17%, the known static-image bias; co-sim is the fair test); ROOM 1.4 s
  **PASS** (+19.3%); CD PLATE B **PASS**; CD PLATE A **PASS** (new settled capture,
  id 0x21); SMALL PLATE renders as a normal ~1.9 s plate — the old 'invalid selector'
  row fully dissolved (registry #34). PLATE vs the 'V2 0.6/1.8 @170' row FAILs on the
  <170 Hz band only (1.69 vs 0.6; the >170 band −3%) — reported with its two printed
  caveats (the 0027-named crossover-bleed confound + the boot image recalls V1, not V2);
  a V2-recalled re-test is the named follow-up, not an engine discrepancy.
- **F4b** (e3b redo: both-bands-short mid-lo, co-sim mid-hi, PDL main-peak arrival)
  remains CARRIED (now unblocked by F4a's calibrated curves; a follow-up, not a verdict).

## 6. F5 — consolidation

- `reverb_metrics.analyze_pair` — first-class burst-minus-silence floor subtraction:
  verdicts on the DIFFERENCE, the silence twin's floor signature (dc/ac_rms/peak)
  reported in the result; control battery extended with a floored-reverb recovery case:
  **11/11 TRUSTED** (the pair case recovers RT60 2.6 s at 0.2% with the floor named).
- The signature-tables doc carries the 0028 verification notes (T&C 376/376 corrected,
  ARU 1469/1469 corrected, DMEM 167/167 with the owner-confirmed U65.4 correction);
  this session doc; the memory index; plan 024's banner.

## 7. Registry additions

| # | Item | Verdict |
|---|---|---|
| 36 | diag-3 stale-cell reads (MEMR rows 1/4/5 through the CPC wrap) | OPEN but measured-INERT — never reach a MAC operand; both DAB15 carriers unlisted; H0 (decay to phys 0) vs H1 (retention → 0x8000) tie at 1469/1469 (`f1_dmem_stale_reads.py`) |
| 37 | DMEM table U65.4 `0000` | ERRATUM, owner-CONFIRMED in-session (model 19H6; same-net sister U63.3 + lift-jumper mirror U65.10 both 19H6) — corrected; DMEM = 167/167 |
| 38 | "w44-family 9↔22" as the runtime stop switch | DEAD — that is the V6-vs-V7 variation delta; the runtime dynamic is the graduated w62/63/64/66/67/68 (+51) scheduler (`f3b_switch_hunt.py`) |
| 39 | the 0x80/0xBC loudness-gate branches (0x8331/0x8303) | OPEN — unreachable from the XREG-log scale (ceiling ~0x37 near FS); another source ORs in at 0x3C62 (overload-flag candidate) |
| 40 | late-tail 0x3E10 hops (0x07↔0x17, ~LFO period, zero input) | OPEN — firmware-side interaction, source untraced |

Registry #29/#30 stand as written in 0027; **#31 and #35 are CLOSED at the engine level**
(e5 zero + the lockstep + the clamp self-test).

## 8. Verification state

- Engine self-tests: ALL PASS (expectations derived, never fitted). Battery: POST green,
  D1 16/16, D3 376/376, e1c 1469/1469 + 240-step lockstep, e5 ZERO, co-sim within
  0.05 s of 0027, D2b settled PASS, metric battery 11/11.
- New probes: `f1_e1c_engine_xcheck.py`, `f1_dmem_stale_reads.py`,
  `f2_dmem_signatures.py`, `f2_fpc_foundations.py`, `f3_stop_decay.py`,
  `f3b_switch_hunt.py` (+ the F4 worker's `f4_*` probes). Caches: `wcs_diag.json`
  gains `sig6`; `e1c_scores.json`/`e2_cosim_factory.json` refreshed.
- C++: booth vectors + 3/3 diff cases bit-exact (MSVC build; `golden_rtl/` committed,
  regenerable via `tools/export_golden_224xl_rtl.py`).
- The pre-0028 state-reading probes (b45/c2/c4/e3d/e3e) see the PHYS domain if re-run —
  session records, not maintained tools (c2's engine-internal imports are pre-resync).

## 9. Open (next session)

1. **The FPC per-pin emitter** (everything staged: stimulus locked, N=98 reconciled,
   the 766-line owner trace + fig-3.5/3.6; adjudicates the AIN idle pattern = the e1c
   AD_CONST question).
2. The stop-decay audible contrast (page-2 Stop sliders apart from running; the
   graduated scheduler's per-step thresholds/timing map); leftovers #39/#40.
3. F4b (e3b redo with the calibrated curves) + whatever the F4 worker carried.
4. The stale-cell H0/H1 (a bench question; only if a listed-pin path to DAB15 emerges).
