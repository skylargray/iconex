# 0023 — The RTL arbiter answered: the accumulator pipeline lag, and the FIRST TAIL

**Date:** 2026-07-02
**Scope:** execution of `docs/plans/021 - 224XL-RTL-arbiter-and-first-tail.md` (all of Phase A/B/C,
Phase D partially — see §8).
**Result:** ★★★ **CONCERT renders a real reverb tail.** The metric harness returns **WET-PASS / DENSE on
all four channels** (burst stimulus, boot AND run-state WCS images), floor-subtracted **RT60 = 1.83–1.91 s
(boot) / 1.37–1.42 s (RUN-state)** vs the 2.5 s benchmark IR — the first wet, dense, *decaying* output in
23 sessions. The one open question (the MAC/register/XFER alignment) is **answered from the traced gates**,
with one correction to the plan's own A3 sketch: **the accumulator lags the product register by one full
ARUCKE/ edge** (fig-3.4's "the accumulate runs one AS behind the partial products" — the 74F283 back-end
adder chain cannot settle inside 0.85 MC slots). Engine: `tools/aru_freerun22_rtl.py`.

---

## 1. The emergent alignment (the answer to plan-021 §3)

All from the traced netlist (§3.5–3.11, §2T, §4.7–4.9, §4F, §6D) + the emergent clock (tc_clock,
fig-3.2/3.3-validated) + fig-3.4, using the calibrated discrete slot convention. "Step n" = the step
during which word w_n's stage-1 fields + offset latch are live. Slot edges are MC edges; x.43 = the
ARUCKE/ rising edge inside slot x.

| event | edge | owner / content |
|---|---|---|
| PC advance + stage-1/OFST latch | slot-0.0 (DAB RSTB/ rise) | stage-1 ← the word fetched during step n−1 ⇒ **fetch → fields-live pipeline; the frame is L+1 steps** (§2) |
| operand SR load (74194) | slot-0.58 (ARUCK; mode=LOAD asserted during AS2, lands at the edge ending it) | SR ← regfile[RA(w_{n−1})] **AFTER step n−1's MS7 write — write-through** |
| stage-2 load (tc_U19) | slot-3.0 (ARUCKE in AS0) | {RA, XFER, ZERO, MI23} ← w_n |
| CSIGN JK (tc_U20) | slot-3.0+ (ARUCKE/ fall; races the LS377 and samples PRE-load Q4) | CSIGN/ ← w_{n−1}'s MI23 — one more stage behind, exactly matching the MAC defer: **all three pps of a word carry that word's own sign** |
| serializer load (74195, SH//LD=AS1/) | slot-6.0 | ← w_n's C-bits; pairs (C4,C5),(C2,C3),(C0,C1) live during AS0/AS1/AS2 **of step n+1** (third pair via the P3=Q2 feedback at the next load) |
| product register (ARUCK) | 3.58(n+1), 6.58(n+1), 0.58(n+2) | ppA(w_n), ppB(w_n), ppC(w_n) |
| **accumulator (ARUCKE/, one edge behind the PR — fig-3.4)** | **7.43(n+1), 1.43(n+2), 4.43(n+2)** | **+= ppA(w_n), ppB(w_n), ppC(w_n)** — the adder chain (~1.4 slots) forces the extra edge |
| XFER capture (74F374 on XFER CK rise) | slot-3.06(n) | iff **w_{n−1}.XFER**: RES ← sat16((ACC+4)>>3) of the MAC **through ppB(w_{n−2})** — i.e. the group MAC minus the pre-XFER word's pairC partial |
| ZERO clear (163 sync /CLR) | slot-4.43(n) | iff **w_{n−1}.ZERO** (same owner as the capture, one edge later): replaces the ppC(w_{n−2}) add — **deletes exactly the pairC chunk the capture just missed**; nothing else is lost, nothing leaks |
| DMEM DIN latch (CAS fall, early write) | slot-4.0 | MEMW writes the **just-captured** RES |
| FPC D/A capture (FPC CK = MS5) | slot-5.0 | WR-DA channels get post-capture RES |
| regfile write (DAB WSTB/=¬MS7, unconditional) | slot-7 | R[WA(w_n)] ← DAB (DOUT lands ~here on MEMR) |
| ACC width | — | the 163/283 chain **wraps mod 2²⁰** (signed); saturation only in the sat-mux result path |
| CPC | once per frame (RESET/ event) | all addresses of the frame pre-bump |

**Consequences for the factory idiom** (the XFER∧ZERO word X, 473/486 of all flagged words):
X captures the accumulation group complete through w_{X−1} *minus pairC(w_{X−1})*, and the clear deletes
that same pairC. Everything else survives whole — including the cmag=32 ×1.0 data-moves and the full
g≥16 ladder coefficients. Effective coefficient of a word feeding an XFER capture = cmag − (cmag&3)·(pairC
weight) — which is why the ladder h-words are compiled pairA-free (<16) and lose only their two low bits.

## 2. The frame is L+1 steps (fetch-pipeline consequence, confirmed from the bytes)

The PC points at w_{n+1} during step n; RESET (comb, from stage-1 fields) fires during the reset word's
own fields-live step; the PC sync-clear lands one boundary later — so **the row after the reset word
executes every frame**. Confirmed three independent ways:
- **all 13 factory programs park an idle word at row L** (typ=3, cmag=0, no flags, WA=3 — scanned);
- L=99 programs ⇒ 100 hardware steps ⇒ fs = 30.72e6/9/100 = 34,133 Hz ≈ dale's canonical **34.125 kHz**;
- CONCERT (L=104) ⇒ 105 steps ⇒ **fs = 32,508 Hz** (not 32,821 as plan-021 §1.2 had).
The row-L idle's WA=3 also explains the taint tracer's old "WA=3 dump": R3 ← held DAB at every frame
boundary (it holds the reset step's RDRREG value = the last C-channel output).

## 3. How the alignment was pinned (chronology of the arbiter)

1. **Ported the engine** to the 0022 frame with the two-stage control pipeline at traced edges. First
   derivation had the accumulator adding at the same edge-group as the PR latch (as `mac_step_subslot`
   effectively did). B1 passed (single-pair cmags can't see the difference).
2. **B2 POST green; B3 handoffs CONNECT** — multi-stage register chains MAC'd, row-40 RES→MEMW one step
   later, first-ever OUT events (f3/f4). Already massively different from the behavioral engine's
   one-MAC dead-end.
3. **First render: earlies −40 dB + a perpetual ±2.3-RMS tonal floor.** Diagnosis via the program dump:
   under the same-edge back-end, the ZERO clear at 4.43 killed ppA of its own word — deleting every
   cmag=32 ×1.0 data-move and the 16/32 chunk of every g-word. The factory bytes (h-words all pairA-free,
   run-state modulation writing cmag onto XF∧ZR words) said the machine cannot work that way.
4. **fig-3.4 (owner-read, digitized) settled it**: "PARTIAL PRODUCT REG i2.AS0-AS2", "ACCUMULATOR
   accumulate i2.AS1→i3.AS0 … one AS behind the partial products = the pipeline register", "ZERO/ clears
   at i2.AS0 so it reads 0 at i2.AS1". The accumulate is one ARUCKE/ edge behind the PR latch — physics
   (F283 chain settle ≈ 1.4 slots > 0.85) forces the same reading. With that lag, the clear kills only
   the pairC the capture missed, and the ×1.0 moves + full g survive.
5. **Race falsifications** (both dead, empirically):
   - clear-owner = w_n ("no-lag" Q6 sample): output identically ZERO (every capture wiped one step early);
   - clear landing at the 1.43 edge: captures always see a just-cleared ACC — dead by inspection.
   The surviving semantics (owner = w_{n−1}, landing 4.43) is also the LS-typ-delay reading.
6. **CSIGN polarity re-derived on this engine** (E3b's verdict was behavioral-frame-relative): BOTH
   polarities are now stable — the old dead↔rail bimodality was an alignment artifact. The traced chain's
   native polarity (cs_eff = Multibus level = ~stored bit7) is kept. PROT is asserted on ~all words
   (inactive level; consumer untraced; no effect modeled).

## 4. Phase B results (all PASS)

- **B1**: booth3 per-phase identity (Σpps == product20, 4020 cases incl. 20 goldens); RTL-authored
  passthrough EXACT (out==in same frame; XFER sits one word after the MAC word on this machine);
  feedback comb EXACT vs the closed-form recurrence for g=16 AND multi-pair g=21 (g_eff = g − pairC).
- **B2**: POST E32/E40/E83/E91 all PASS un-suppressed (untouched single-step path), mainloop reached.
- **B3**: taint CONNECT — input → ×(gain, ppA-intact ~26/32) → two write heads → ladder cells
  (260/277/516/911/1116 region) → in-place recirculation → OUT. Both named handoffs connect.
- **B4**: in-place RMW cells are bounded recursive nodes (measured pole −0.125 = −(6−2)/32 — the
  pairC-deleted h, exactly as predicted by §1).
- **B5**: tank ENERGY (RMS²·N) decays smoothly ~26 dB/s through the 0.7-s bulldozer cliff (the parked
  write-once trail was never part of the loop; output energy shows no cliff). Crude tank RT60 ≈ 1.8 s.

## 5. Phase C results — THE FIRST TAIL

`reverb_metrics` (calibration battery in-process), burst stimulus (±8000, 0.30 s), 4.5 s renders:

| image | chA | chB | chC | chD |
|---|---|---|---|---|
| boot | **WET-PASS/DENSE** | WET-PASS/DENSE | WET-PASS/DENSE | WET-PASS/DENSE |
| run-state | **WET-PASS/DENSE** | WET-PASS/DENSE | WET-PASS/DENSE | WET-PASS/DENSE |

Floor-subtracted RT60 (50-ms block slope, −5…−40 dBr): **boot 1.91/1.83/1.86/1.88 s (A/B/C/D);
run-state 1.40/1.42/1.37/1.41 s.** Benchmark IR ≈ 2.5 s — same structure, parameter-state-dependent
(the run-state image carries mid-LFO Decay-Optimization coefficients; the exact parameter → cmag chase
is plan-021 D2, still open). Early peaks ≈ −14 dB re input. WAVs: `tools/session0022_probes/renders/`
(`c1_rtl_*`, `c3_*_diff_*` = floor-subtracted, ×64 gain).

**The impulse renders still read INDETERMINATE/TONAL** — that is the deterministic Booth-residue floor
(each (0,0) serializer phase contributes ±1 to the ACC; the program's sign mix leaves a ±2.5-LSB RMS
limit cycle ≈ −82 dBFS re full scale). It is real, calibrated hardware behavior (the +4 result rounding
is its single-product compensation); on a physical unit it sits below the analog noise floor. The burst
stimulus (and floor subtraction) sees straight through it.

## 6. What this settles / dissolves

- **The one open question of plan 021 (operand/register/XFER alignment): ANSWERED** — §1's table, no
  knobs, every edge traced or figure-pinned, the two wiring-allowed races falsified empirically.
- **Dead-end registry #1/#2 (CSIGN bimodality)**: dissolved — an artifact of the behavioral alignment.
- **"Levers inert" / "nothing densifies" (plans 018/020 era)**: fully void — with the right alignment the
  machine densifies and decays with no levers at all.
- **The "input muted (cmag=0)" reading of word 127**: under the RTL alignment the A/D read's OWN cmag
  (26) multiplies the input via write-through; the following cmag=0 word is a plain data-move. Input
  enters at ~0.8 (ppA intact), twice per frame.
- **fs for CONCERT = 32,508 Hz** (L+1), not 32,821.
- **`mac_step` / `mac_step_subslot` (aru_rtl_dp Phase-1 models)**: superseded for free-run — they
  collapse the accumulator's extra pipeline edge (POST can't see it; the free-run machine lives on it).
  POST path itself untouched and green.

## 7. Cross-program oracle (D0)

All 13 buildable factory programs through the same engine + metric harness (burst, chA, boot images):

| id | L | fs | verdict | RT60 (floor-sub) | | id | L | fs | verdict | RT60 |
|---|---|---|---|---|---|---|---|---|---|---|
| 1 CONCERT | 104 | 32508 | **WET-PASS** | 1.91 | | 10 | 103 | 32821 | WET-PASS | 1.62 |
| 2 | 99 | 34133 | WET-PASS | 2.45 | | 12 | 99 | 34133 | INDETERMINATE | — |
| 3 | 99 | 34133 | FAIL | — | | 16 | 101 | 33464 | WET-PASS | 1.40 |
| 4 | 104 | 32508 | WET-PASS | **5.56** | | 17 | 108 | 31315 | WET-PASS | **5.93** |
| 5 | 106 | 31900 | WET-PASS | 1.53 | | 18 | 103 | 32821 | WET-PASS | 1.57 |
| 6 | 101 | 33464 | WET-PASS | 1.71 | | 20 | 99 | 34133 | INDETERMINATE | 0.43 |
| 8 | 99 | 34133 | INDETERMINATE (output peak = 4 — near-silent) | | | | | | | |

**9/13 WET-PASS with program-specific RT60 diversity (1.4–5.9 s)** — a coherent program bank, strong
independent support for the alignment. Anomalies (8 near-silent; 3 FAIL; 12/20 indeterminate) are
boot-parameter-state material for D2 (CONCERT's own boot image has its modulated taps parked at
offset 1/254 with degenerate coefficients — other programs plausibly boot more/less muted).

## 8. Remaining open (next session)

1. **D1 known-answer diag oracles** (firmware diag 7 = ZERO DELAY, 8 = MAX DELAY): needs LARC keypress
   injection into the boot harness (the diag menu; the program-id patch at 0x8160 does NOT reach these —
   ids 7/8 in the record array are empty slots). `_diag3_wcs.bin` in tools/ suggests a prior partial path.
2. **D2 parameter state**: the RT60 gap (1.9 vs 2.5 s benchmark) is parameter-state; trace the LARC
   parameter → coefficient application (netlist §7 apply chain) or drive DECAY explicitly, rebuild,
   re-measure. The run-state image (mid-LFO) is already captured and renders.
3. **D3 §5.7 signature tables**: hardware-grade free-run verification at named pins (START=RESET/); the
   T&C DPORT readback latches (§6T.6) are the observation points.
4. **C4 live-modulation co-sim** (62 ticks/frame) for the chorus on the RTL engine.
5. The residue floor: confirm against real-unit behavior (it predicts a specific −82 dBFS idle tone per
   program — a testable hardware signature!).
6. `aru_whole.py` / the C++ scaffold re-sync to the RTL alignment.

## 9. Verification state

- New engine `tools/aru_freerun22_rtl.py` (self-tests ALL PASS, incl. golden-anchored per-phase identity).
- POST green (E32/E40/E83/E91) on the untouched single-step path — re-run this session.
- All audio claims above are `reverb_metrics` verdicts on emitted D/A streams, battery passed in-process,
  WAVs rendered. Tank statements are ENERGY (RMS²·N).
- Probes: `tools/session0022_probes/{b3_rtl_taint, b45_cell_and_tank, c1_concert_render_rtl,
  c2_race_falsification, c3_floor_subtracted_ir, c4_csign_and_prot, c5_rt60, d0_all_programs}.py`.
- Engine speed: ~4700 frames/s (2.5-s render ≈ 17 s) — well inside plan A5's budget.

## 10. Process lessons

- **A timing figure's pipeline annotations are load-bearing.** The whole outcome hinged on fig-3.4's
  "one AS behind" — present in the digitized spec all along, collapsed by every behavioral model since.
  When a traced schedule and a drawn schedule disagree by one edge, believe the drawing and check
  settle-time physics: the adder chain's propagation time IS the pipeline register.
- **Compiled programs encode the hardware's own rules.** The h<16 (pairA-free) segregation, the sum-40
  modulated pairs, the row-L idles — each was a decode-independent vote about the machine's semantics,
  readable straight off the bytes once asked the right question.
- **Verdicts inherited from a wrong frame must be re-derived in the new frame** (E3b's CSIGN "stable"
  polarity was behavioral-frame-relative; both polarities are stable here). Same lesson as 0022's, one
  level down.
- **Deterministic residue floors can mask a working machine from a metric.** The INDETERMINATE/TONAL
  impulse verdicts were the floor, not the tail; subtracting the zero-input render (legal because the
  datapath is linear mod rounding) revealed the truth. Never let a verdict on a confounded stimulus
  overrule a clean one.
