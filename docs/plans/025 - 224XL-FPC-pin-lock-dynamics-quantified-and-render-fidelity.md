# 025 — 224XL: the FPC pin lock, the dynamics quantified, and the render-fidelity follow-through

**Status:** READY TO EXECUTE (written 2026-07-02 at the close of session 0028).
**Read first:** `docs/sessions/0028 - the-engine-resync-the-table-sweep-and-the-graduated-stop-decay.md`
(the whole thing — the engine now IS the physical law and three of four §5.7 tables are closed),
then 0027 as needed. The engine of record is **`tools/aru_freerun22_rtl.py`** — pin-locked,
battery-green, e5 at ZERO; do not touch it this session unless a gate fails (any engine edit
re-runs the FULL F1c battery of plan 024 before anything else is quotable). Trust
0028 > 0027 > 0026 > 0025 > 0024 > 0022 > everything older.

**Mission.** 0028 left exactly one §5.7 table un-modeled (FPC), one dynamics mechanism
qualitatively-but-not-quantitatively closed (the graduated stop-decay scheduler), and the
FPC codec functions grounded-but-not-pin-verified in the render path. This session: build
the FPC per-pin emitter and score its table (G1 — the last board lock), verify/correct the
FPC float↔fixed codec against it and measure render fidelity with the codec ON (G2),
quantify the stop-decay scheduler and produce the documented audible observable (G3),
clear the E3 leftovers F4a unblocked (G4), consolidate (G5). G1 gates G2; G3/G4 are
independent of both.

---

## 1. Ground truth (established 0028; do not re-derive)

### 1.1 The engine + battery state
- RTL22 computes in the complement domain (raw3/backend20/PP3..18 tap; SAT clamp feeds the
  '163; CPU boundaries complement; `XREG_host` bench attribute; `XREG_wr` = the DSP→host
  readback the level detector consumes). Battery green: POST, D1 16/16 ±0, D3 376/376,
  e1c 1469/1469 + 240-step lockstep, e5 ZERO, co-sim bb 2.68/2.65, D2b settled PASS.
- Tables closed at pins: ARU 1469/1469, T&C 376/376, DMEM 167/167 (all errata
  owner-confirmed and corrected in the blocks, originals in the notes).
- C++ bit-exact 4/4 (d1zero/d1max/concert-with-CPC-wrap/sig6-XREG); the DSP→host WR-XREG
  readback is the ONE golden-unexercised C++ boundary.
- Floor signature (phys law): chA DC +12.4 / chC −5.4 LSB, AC-RMS 2-3.4 LSB, near-DC
  drift; `reverb_metrics.analyze_pair` = the first-class burst-minus-silence mode
  (battery 11/11) — USE IT for every decay verdict this session.

### 1.2 The FPC bench (F2b foundations — `f2_fpc_foundations.py` reproduces all of it)
- diag-6 WCS cached (`wcs_diag.json["sig6"]`, 512/512 agreement; menu table 0x0330 item 6
  → handler 0x0E84; idle loop 0x0EC6). Extracts w_reset=31, **L=97 → 98-step frame**;
  SM CLOCK = FPCCLK (FPC U4 pin 5) with START=STOP=RESET (U4 pin 2) → **N=98 = sig224's
  96F6** — the window is RECONCILED; do not re-derive, do assert it in the probe.
- Bench state: the 0x0D1E pump (block 0x0EEC; F6/FA/FE parked-word WA cycle) parks
  **R0=0x5555, R1=0xCCCC, R2=0x1999, XREG=0xFAAA**; the steady frame delivers exactly
  those four constants to WR-DA: **A/B at steps 2/3 (R0/R1 unity captures), C/D at steps
  52/53 (R2/XREG)** — half a frame apart (the output demux's two-phase cadence). The
  program has NO RD-AD step; the SM lifts the AIN SAR completion (U26.11 → +5V) so the
  A/D side runs its deterministic idle pattern.
- Source for the pin model: `docs/reference/224/224XL FPC pinouts from 060-01320.txt`
  (766-line OWNER hand-trace — the trusted class of source) + SM fig-3.5/3.6 + the
  §G3D/§2T cross-board nets (SDAA-D from tc_U32 = OFST8-11/, WR DA/, RD AD/, RESET/).

### 1.3 The stop-decay mechanism (F3 — qualitative closure)
- Source: the DSP posts the RAW INPUT SAMPLE to XREG every frame (CONCERT row 0 carries
  WRX); firmware (NVS 0x829D..0x84xx): |sample| peak-hold 0x3E38 → log-compress (0x0FB7)
  → running level **0x3E10** (instant attack; release via the 10-deep ring 0x3E15-1F);
  DynDecay arm = 0x3CCD bit 0 (V6/V7 recall 0xC1; V1 0xC0); state byte 0x3C51; stage
  bytes 0x3E11/0x3E12/0x3E14.
- The switch: **~151 ms after input stops** (the documented switch-delay parameter), a
  de-zipper walk (~24 frames/word) steps the cmag of **w62/63/64/66/67/68 (+51 mirrors
  w113-119)** down 11→10→9 as the level falls, back up when it returns. GRADUATED, not
  binary (registry #38: 'w44 9↔22' was the V6-vs-V7 variation delta).
- The co-sim feedback edge exists: `f3_stop_decay.cosim()` (engine `XREG_wr` → 8080
  IN 0x06/0x07, fully inline — trajectory depends on audio, no replay shortcut).
- Page-2 calibration (F4a): **LF/MID STOP DCY presets = 3.0/3.0 SEC (the documented V1
  stops, exact)**, same 0.6-70 s ladder as the running decays; the calibrated curves
  live in `display_map.json` p2s1/p2s2.

### 1.4 Known-open (registry #36-#40)
#36 diag-3 stale cells (inert; bench question only). #39 the 0x80/0xBC loudness-gate
branches are unreachable from the XREG-log scale (~0x37 ceiling near FS) — another term
ORs in at 0x3C62 (overload-flag candidate). #40 late-tail 0x3E10 hops 0x07↔0x17 at ~the
LFO period under zero input — source untraced.

## 2. Dead-end / discipline registry
Plan 023 §2 (#13-28) and 0027 §8 (#29-35, with **#31/#35 CLOSED by 0028**) stand;
0028 adds #36-40 (§1.4; #37 resolved). Do not re-open closed entries without new
pin-level evidence.

---

## 3. Phase G1 — THE FPC PER-PIN EMITTER ★ (the last §5.7 board)

G1a. **Conventions FIRST (E1b discipline — predictions before reads).** From the owner
     trace + fig-3.5/3.6, derive on paper before scoring: the fpcCLKA↔FPCCLK relation
     (U4 pin 5 is the analyzer clock — find U4's part + what divides what; the strobe
     counters U1/U2 and input-cycle counter U7/U8 run on fpcCLKA); how many fpcCLKA per
     step/frame; which edges the '163s count; what the SAR lift (AIN U26.11 = +5V)
     freezes (completion never fires → derive the SAR's stuck sequence and the AIN
     hand-off codes). Write the predicted per-counter periods and the +5V/GND reference
     check INTO the probe before the first score (the 826P-style falsifier).
G1b. **The emitter + score** (`g1_fpc_signatures.py`): streams at FPCCLK sampling over
     N=98; stimulus = the §1.2 frame (the four constants at steps 2/3/52/53 through the
     OGA/output section; the AIN idle pattern on the input section); pin map from the
     trace; ONE global window rotation; score the FPC table (~17 chips). Every mismatch
     names its net; single-glyph errata need a same-net sister pin (the U65.4 pattern)
     and OWNER confirmation before any table correction.
G1c. **The AD idle pattern** falls out of the input-section model → close the e1c
     AD_CONST question: if the true idle code ≠ 0x0000 (CPU), re-run `e1_aru_signatures`
     with the corrected constant and confirm 1469/1469 is unmoved (diag-3's RD-AD row
     feeds R3-only, but confirm at pins, don't argue it).
G1d. **F2c follow-through:** netlist FPC section / pinout-txt updates per findings
     (owner-verify protocol); tables-doc verification note in the 0028 style.

## 4. Phase G2 — the FPC codec verified → render fidelity (gated on G1)

G2a. Verify `aru_freerun.fpc_input_float_to_fixed` / `fpc_output_fixed_to_float` against
     the pin-locked emitter semantics (gain-ranger IGA thresholds and cap, SAR truncation
     direction, the OGA shift-until-MSBs-differ cap-3 law, DAC mantissa/discard bits,
     sign handling). Fix what disagrees — these were grounded from figures (2026-06-30),
     never pin-verified. Unit vectors from the emitter become the codec's self-test.
G2b. Render with the codec ON: e2 co-sim (factory) with `fpc_enabled=True` end-to-end.
     Expected: headline RT60s unchanged within LFO-phase noise (the boundary is
     unity-gain by design); NEW = the 12-bit float quantization grain — measure the
     floor/grain delta vs the fixed-point render with `analyze_pair` and document the
     codec-on floor signature. **If any headline verdict moves >0.15 s, STOP and
     diagnose** (that would mean the codec is not the unity-gain boundary the magnitude
     verdict claimed).
G2c. C++: add the WR-XREG readback golden (the diag-3 program has WRX words rows 20-27;
     a 5th case asserting `xregReadback()` per frame vs the Python `XREG_wr` trace
     closes the last unexercised boundary), and port the verified codec if G2a changed
     it (float boundary only; the integer diff gate must stay 5/5 bit-exact).

## 5. Phase G3 — the dynamics quantified (independent of G1/G2)

G3a. **Map the scheduler** (`g3_scheduler_map.py`, the f3b harness + finer watches):
     the level-task tick cadence (frames per ring shift); the exact level thresholds at
     which each 11→10→9 step fires (correlate step frames with 0x3E10/ring values); the
     up-switch law; whether the walk continues below 9 with longer silence (the idle
     floor keeps the level alive — see #40); the 0x3E12 stage counter's role. Deliver
     the scheduler as a stated law (thresholds + delays + step sizes), the way E1b
     stated the window law.
G3b. **The documented audible observable:** V1 with DynDecay ARMED (the 0x2E key opens
     the DynDecay prompt — e4-explore the confirm flow first; V1's own page-2 stops are
     the documented 3.0/3.0 vs running 3.0/2.0), burst→silence through the feedback
     co-sim, `analyze_pair` per-band: the MID tail after the stop event must move from
     ~2.0 s toward the 3.0 s stop target (LF stays ~3.0 — the null control). Also run
     V6/V7 for the record. **This is the ch.4 dynamics row made audible — the phase
     gate for G3.**
G3c. Registry #39/#40 traces (bounded — timebox these): who writes 0x3C62 (scan
     writers; overload-flag hypothesis — an ISR or the meter path?); what makes 0x3E10
     hop 0x07↔0x17 at ~LFO period under zero input (candidate: the LFO task's WCS mover
     writes land near the level task's reads, or a shared scratch). If un-closed in the
     timebox, document the evidence and park.

## 6. Phase G4 — E3 leftovers (all unblocked by F4a's calibration)

G4a. **F4b proper:** mid-lo with BOTH LF and Mid at 0.6 s (kills the crossover bleed);
     mid-hi 70 s under the co-sim (near-unity loops need live modulation — expect a
     LONG render; size it first); PDL arrival via main-peak detection on chC vs the
     displayed value (the p1 curve + the p4 FinPD 0.140625 ms/byte law are in
     `display_map.json`).
G4b. **PLATE V2 re-test:** recall PLATE then VARIATION 2 through the keys, settle,
     settled render, score vs the documented 0.6/1.8 @ XOV 170 — closes the one F4d
     FAIL's caveat pair.
G4c. **The p4/p5 preset-storage question:** the select-key presets render finer than the
     slider scale and off the flat array (F4a finding) — find where page-4/5 presets
     live (trace the param-recall path for a p4 slider from the 0xA791/recall route;
     0026's param-route map is the starting point). Mechanical answer only (an address
     + scale), no role speculation.

## 7. Phase G5 — consolidation

- Session doc 0029; memory index; this plan's banner; tables-doc note (G1);
  netlist/pinout updates (G1d); the C++ README scope line (G2c).
- If G2a changed the codec: re-run the plan-024 F1c battery with fpc OFF (must be
  untouched-green) and record the fpc-ON deltas as a separate table.

## 8. Verification rules (unchanged + additions)

- Defaults are the oracle; `analyze_pair` for every decay verdict; per-band at the
  documented crossover; WAVs on disk; POST green at every phase.
- **G1a's predicted counter periods + +5V refs must be written before the first table
  read** (the 826P discipline); the FPC score uses ONE global rotation.
- Errata protocol: same-net sister pin + owner confirmation before correcting any table
  glyph (originals recorded in the note — the U65.4 pattern).
- Engine edits (none expected): full plan-024 F1c battery re-run before anything else.
- Every probe's final message states which registry entry it would re-open.

## 9. Facts that will save time

- Boot ≈ 40 s; settle 6M ticks; `probe_run.run_ticks` for ALL post-boot running.
- The feedback co-sim harness is `f3_stop_decay.cosim()` (input hook pattern, per-frame
  WCS re-decode, watch arrays) — extend, don't rewrite. ~700 frames/s inline.
- Keys: 0x26+number = variation; 0x3E = PAGE (skips apply page 4 — display 5 pairs with
  0x3C34=5); 0x2E = the DynDecay prompt (confirm flow unexplored); p4 calibration reads
  come from the DESCEND pass (ascend lands 25 bytes low).
- e1c full scan ≈ 2 min; single variant ≈ 15 s; the DMEM scorer ≈ 1 min.
- The level-task RAM map: 0x3E38 peak / 0x3E10 running / 0x3E15-1F ring / 0x3E3D gated
  instant (floor 0x10) / 0x3C51 state / 0x3CCD toggles / 0x3C54 tracked max.
- `dis224.py <start> <end>` covers SBC+NVS at true addresses; `scan` mode finds IN/OUT.
- `renders/` is gitignored (top level too, since 0028); caches are committed.

## 10. Artifacts

- New: `g1_fpc_signatures.py` (+ FPC netlist/pinout updates), `g2_fpc_codec_verify.py`
  (+ codec fixes in `aru_freerun.py` if needed), fpc-on co-sim record,
  `g3_scheduler_map.py`, `g3b_stop_audible.py`, `g4a_e3b_redo.py`, `g4b_plate_v2.py`,
  `g4c_preset_storage.py`, C++ case 5 (WRX readback).
- Records: session doc 0029; memory update; this plan's execution banner.
