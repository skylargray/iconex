# 021 — 224XL: the RTL arbiter and the first tail

> ## ✅ EXECUTED 2026-07-02 — MISSION ACCOMPLISHED (session 0023)
> **The alignment is ANSWERED and the first tail EXISTS.** Engine: `tools/aru_freerun22_rtl.py`.
> CONCERT = **WET-PASS/DENSE on all 4 channels** (boot + run-state images), floor-subtracted
> **RT60 1.83–1.91 s (boot) / 1.37–1.42 s (run)** vs the 2.5 s benchmark. Phases A/B/C complete;
> D0 cross-program sweep run; D1 (diag LARC injection), D2 (parameter→cmag), D3 (§5.7 signatures),
> C4 (modulation co-sim) remain. TWO corrections to this plan's own sketch, both proven in-session:
> (1) §A3's "operand load ≈ MS6.3 BEFORE the MS7 write" is wrong — fig-3.4's LOAD mode lands at the
> edge ENDING AS2 = slot-0.58 of the NEXT step, i.e. **write-through** (pre-write mispairs the Booth
> serializer against the goldens); (2) the accumulator lags the product register by one full ARUCKE/
> edge (fig-3.4 "one AS behind"), which moves the pps of word W to slots 7.43(W+1)/1.43(W+2)/4.43(W+2)
> and makes the ZERO clear delete exactly the pre-XFER word's pairC. Also: **the hardware frame is
> L+1 steps** (row-L idles in all 13 programs; L=99 ⇒ dale's 34.13 kHz; CONCERT fs = 32,508 Hz), and
> E3b's CSIGN verdict + dead-ends #1/#2 were behavioral-frame artifacts (both polarities stable now).
> Full record: `docs/sessions/0023 - the-rtl-arbiter-answered-the-accumulator-pipeline-and-the-first-tail.md`.

**Status:** ~~READY TO EXECUTE~~ EXECUTED (written 2026-07-01 at the close of session 0022).
**Read first:** `docs/sessions/0022 - the-wcs-coordinate-system-was-reversed-and-the-programs-are-valid.md`
(the coordinate-system proof + the full E3 record). Then this plan. Trust these two documents over
EVERYTHING older — most pre-0022 docs carry now-refuted framings (they are bannered, but don't rely on
banners alone).

**Mission.** One question remains between the project and a working CONCERT tail: the exact
**MAC / register-file / XFER alignment** of the free-running datapath. Behavioral guessing is exhausted
(seven sweep families — see the dead-end registry). The arbiter is the **edge-driven RTL model**: port
`aru_freerun_rtl.FreeRunRTL` + the ClockEngine onto the session-0022 frame so the alignment falls out of
the traced gate equations instead of interpretation. Verify with the named acceptance probes, then render
CONCERT, then lock it with the E4 known-answer oracles.

---

## 1. Ground truth (established, do not re-derive)

### 1.1 The coordinate system (pin-proven + 13/13 data-confirmed, session 0022)
- `ADRn/` are active-low (Multibus). The 0x4000 window decode (tc_U50) proves it; the word-address mux
  (tc_U42/U28) is uncompensated; the lane decoder (tc_U46) IS compensated (outputs wired reversed).
- ⇒ **CPU word k = physical row 127−k. Execution = CPU words 127, 126, … down to the reset word.**
  Program length L = 128 − (reset word); words below the reset word are never-executed staging.
- All four lanes read through the Multibus data complement (lane 3 = the familiar `~l3`).

### 1.2 The decode (stored CPU-byte domain, 0x4000 image)
- **Type** = `l2 & 3`: **0 = MEMR, 1 = MEMW, 2 = IO (tcWR), 3 = idle.**
- **IO command bits assert when the stored bit == 0:** bit3=RESET, bit4=DP, bit5=TEST,
  bit6=WR XREG (MS7-gated), bit7=WR DA; bits 8–11 = SDA channels **D,C,B,A** (independent enables);
  DAB source select = `(~bits13..12)&3`: 0=none, 1=RDRREG (result reg), 2=XREG, 3=RD-AD.
- **Delay = stored `l0|l1<<8` DIRECTLY** (`addr = CPC − stored`; the OFST/ lines carry the complement and
  the adder adds +1). B55B's window [1447, 6004] = 42–176 ms taps.
- **Coefficients:** cmag = `(~l3>>2)&0x3F` (/32 scale, E83-anchored), XFER = `~l3&1`, ZERO = `(~l3>>1)&1`.
- **WA/RA = l2 bits {2,3}/{4,5}** (any consistent polarity is behaviorally inert), **CSIGN** from l2 bit 7
  — with the effective sign = **the Multibus level (`~bit7`)**: the stored-direct sense self-oscillates,
  the inverted sense is stable (E3b). Per-step sign PATTERN beyond that is part of the open question (§3).
- Per-program: exactly one reset, at the last executed step, riding the frame's final WR-DA.
  L values: 99 (ids 2,3,8,12,20), 101 (6,16), 103 (10,18), **104 (1=CONCERT, 4)**, 106 (5), 108 (17).
  CONCERT: reset word 24, census 55 MEMR + 36 MEMW + 10 IO + 3 idle, fs = 30.72e6/9/104 ≈ **32 821 Hz**.
- CONCERT I/O map (execution order): A/D reads at exec 0 (word 127 — the cross-program invariant step;
  its following MAC is **cmag=0** = ch-1 input muted in this build) and exec 52 (input gain **6/32**);
  WR-DA B@31, A@50, D@83, C@103(+RESET); idle CPU slots at words 103/53/51.

### 1.3 The machine's frame-event tree (owner-traced 2026-07-01)
Reset microword → comb `RESET` (PC sync-clear via tc_U33/tc_U14·U1) → `RESET/` (tc_U25 FF1, registered,
cleared at MS6) → backplane → FPC frame sync ∥ DMEM `dmem_U58A` → `dmemRESET` → **CPC +1 per frame** +
halt-latch sync. `FPC CK = MS5` (tc_U39.Q1) ⇒ the D/A double buffer captures the DAB at MS5 of the WR-DA
step. fig-3.3's "RESET/" row is the DMEM-local `dmemRESET` (inverse of backplane RESET/).

### 1.4 Live modulation (RUN-state capture, session 0022)
Only 22/512 bytes change during RUN: swept tap offsets (words 42,56,57,94,107,108 lane 0) **and lane-3
COEFFICIENTS of 16 ladder words** (56,57,62–64,66–68,107,108,113–115,117–119). Structurally identical
program. The 8080 gets ~62 ticks (2.048 MHz) per ~30.5 µs frame — a handful of instructions — Casey's
"randomly missed updates" mechanism, confirmed live.

## 2. THE DEAD-END REGISTRY — eliminated in session 0022; do NOT re-try
| # | Hypothesis | Verdict / evidence |
|---|---|---|
| 1 | Global CSIGN stored-direct | Self-oscillates from silence (zero-input grows to the same limit cycle) |
| 2 | Global CSIGN inverted alone gives the tail | Stable + tank sustains at ~unity, but output tail ~0.3–0.4 s sparse; not the fix by itself |
| 3 | cmag=0 gate-model DC residue as the pump | Clamping cmag=0→exact-0 changes peaks by 2 LSB |
| 4 | Regfile/operand timing knobs (write-through, delayed write, RA/WA/XFER/ZERO from previous word) — 24 variants | No decaying cell; space swings dead↔rail |
| 5 | CSIGN JK **toggle** modes (4 modes × 4 timing bases) | No decaying cell |
| 6 | Split pipeline depths (product@+2/XFER@+1 per fig-3.4 row-reading; also +3) | vd2/xd1 = nearest-unity (slow creep), still no decay |
| 7 | Static snapshot ≠ running program | RUN-state capture: 22/512 bytes (modulation only); structurally identical |
| 8 | Live modulation as the stabilizer (true 62-ticks/frame co-sim) | Rails/creep unchanged; not the stabilizer |
| 9 | WA/RA transpose ({4,5}/{2,3}) | Reconnects one handoff, rails (cs-direct) or over-damps (cs-inv) |
| 10 | WA/RA field complement | Behaviorally inert (bijection on slots) |
| 11 | "Tank drains in 50 ms" | FALSE — RMS-dilution artifact. Tank ENERGY holds ~9.9e6 for 0.65 s. Use energy (RMS²·N), never RMS-over-touched-cells |
| 12 | Modulation-required-for-loop-closure (M3.X-era) | Void — rendered under the wrong decode. All pre-0022 audio verdicts are void |
Also long-settled (older sessions, still true): reset-decode reinterpretations (0021's 2 560-combo sweep —
the decode was right, the FRAME was wrong); 128-step natural wrap (dead: 100-ish steps, variable L);
z80emu core (parity bug — use kosarev/`i8080_ref`); memory-derived pinouts; auto schematic reads.

## 3. The one open question (precisely)
The free-run **operand/register/XFER alignment**. Symptoms, mapped by the taint tracer
(`tools/session0022_probes/e3l_flow.py`):
- The engine's entire amplitude path is: input → ×6/32 → DM[42606-trail] → (frame 1) 42607 reads →
  one ×10/32 MAC → RES → **dead end**. Nothing at frames 2+.
- **Severed handoff #1:** word 74's register load (the tank read) is clobbered (WA=3 dump at word 71)
  before any RA=3 step reads it.
- **Severed handoff #2:** word 40's RES (=961·seed) lives one step; no MEMW falls inside its lifetime.
- Cell algebra (baseline semantics): each 4-step ladder cell computes C ← a′ − h·a″ and
  A ← g·b′ + g′·b_this — a **forward FIR lattice**, no in-cell feedback: the loop closes only around the
  whole memory cycle, so every register handoff is load-bearing and the tail is exquisitely sensitive to
  the alignment. POST **cannot** constrain it (three different MAC semantics all pass POST).
Whatever the RTL model produces must (acceptance probes, §4-B): make handoffs #1/#2 reach consumers,
keep the comb/passthrough tests exact, and keep POST green.

## 4. The build

### Phase A — port the edge-driven RTL model to the 0022 frame  ★ the arbiter
Base: `tools/aru_rtl.py` (ClockEngine, fig-3.2-validated), `tools/tc_clock.py` (EmergentClock from MC),
`tools/aru_rtl_dp.py` (edge datapath, `mac_step_subslot`, POST-passing), `tools/aru_freerun_rtl.py`
(free-run scaffold). Work items:
A1. Program sequencing: execute CPU words 127 → (128−L) (use `aru_freerun22.program_from_wcs`); PC clocked
    by DAB RSTB/; reset = the decoded microword event (already the frame boundary by construction).
A2. Device decode = `aru_freerun22.decode22` (types/commands/offsets per §1.2). Delete every old-§2T path.
A3. **The control pipeline exactly as traced — this is the whole point:**
    - Stage 1 (tc_U17/U18/U4/U5, 74S163-as-register, CLK = **DAB RSTB/**): type (MEMAC/MI16), **WA**,
      PROT, coefficient bits C0–5/ — valid for the word's own step.
    - Stage 2 (tc_U19, 74LS377, CP = **ARUCKE**, /E = **AS0/** — owner re-verified): **RA**, XFER,
      ZERO-gate, DP, RESETD — loads during the step's AS0 phase from stage-1 outputs.
    - Coefficient serializers (tc_U11/U10, 74195, CLK = ARUCKE, SH//LD = **AS1/**): load at AS1, shift —
      the Booth M0/M1 stream plays during the NEXT step's AS0–AS2 (fig-3.4) ⇒ the multiply of word W
      executes physically during step W+1.
    - CSIGN JK (tc_U20, CLK = ARUCKE/, J/K = AS0-gated MI23 via tc_U34 g3/g4 + tc_U33 inv4).
    - Strobes from the traced gates: XFER CK = NAND(AS0, XFER, tc_U25.pin9); ZERO/ = NAND(Q6, AS0) with
      the 74LS163 SYNCHRONOUS accumulator clear; DAB WSTB/ = ¬MS7 (regfile write, unconditional);
      operand load = 74194 LOAD at AS2 (ARUCK edge ≈ MS6.3, BEFORE the MS7 regfile write).
    - DMEM DOUT lands on the DAB late (~MS7): the regfile write at MS7 captures it; the operand load at
      MS6.3 does NOT — model these two capture points at their real edges. **The whole open question
      lives in the relative order of: DOUT valid, regfile write (MS7), operand load (AS2 start), stage-2
      RA validity, XFER CK, and the serializer phase. Wire them to edges; do not re-order by hand.**
A4. Keep the verified arithmetic: `aru_booth` gate array (+3-dual), `res_from_acc = sat16((ACC+4)>>3)`,
    sat20 accumulator, RDRREG drives the DAB on MEMW and IO-sel==1.
A5. Performance: profile before optimizing; memoize `product20` (already lru-cached); a 2.5 s render at
    ~9 MS-slots × 104 steps × 82 k frames must stay in minutes (the behavioral engine did 45 s — budget
    ≤ 10 min for the RTL model, else memoize sub-blocks).

### Phase B — acceptance probes (in this order; each must pass before the next)
B1. `aru_freerun22` self-tests reproduced on the RTL model: same-frame passthrough EXACT; feedback comb
    EXACT (0.5-decay peaks at D-spacing).
B2. POST still green (`aru_post.py` E32/E40/E83/E91) — via the single-step path, untouched.
B3. **Handoff probes:** frame-level taint trace (port `e3l_flow.py`) — handoff #1 (word-74 load must be
    MAC'd before clobber) and #2 (word-40 RES must reach a MEMW/OUT) must both CONNECT.
B4. Ladder-cell check: with a seeded DM cell, the 4-step cell must produce a bounded recursive response
    (in-cell or cross-cell feedback visible in the taint graph), not a pure forward FIR ending in silence.
B5. Tank energy (RMS²·N — see dead-end #11) sustained-and-decaying over ≥ 1.5 s without input.

### Phase C — CONCERT first tail
C1. Impulse (−6 dBFS) + noise burst through the metric harness (`reverb_metrics`, calibration battery
    in-process — unchanged discipline). All four channels, fs = 32 821.
C2. Target: `WET-PASS / DENSE`, RT60 in the ballpark of the benchmark IR
    (`IR/Lexicon 224XL/Concert Hall V1.1.L.wav` ≈ 2.5 s — structural target, not bit-exact).
C3. If stable but SHORT (~0.4 s): the loop works and the lever is coefficient/parameter state — go to D2.
C4. Then the live-modulation co-sim (62 ticks/frame — harness pattern in `e3j_cosim.py`) for the chorus.

### Phase D — E4 known-answer oracles (absolute, frame-independent)
D1. Firmware diagnostic programs **7 = ZERO DELAY** (analog in → out, through the ARU) and
    **8 = MAX DELAY** (~0.5 s echo, L→A,D / R→B,C): select via the LARC (keypress injection — the diag
    menu; boot harness pattern in `boot8080.py`), build, run end-to-end. These test build+decode+I/O+
    output with documented audible behavior and none of CONCERT's complexity.
D2. Parameter state: the boot's power-up parameters may not be the ch.8 CONCERT defaults (input ch-1 is
    muted, cmag=0!). Trace the parameter→coefficient application (the interpreter) or drive the LARC to
    set DECAY/levels explicitly; rebuild; compare cmag values on the ladder words.
D3. SM §5.7 V8.2.1 **signature-analysis tables** — expected bit streams at named pins (START=RESET/) —
    hardware-grade free-run verification once the RTL model runs.

## 5. Facts that will save time
- Input trail geometry: the 42606-write trail is bulldozed by the 19678-write head after exactly
  22 928 frames (0.699 s) — long-delay readers of that trail with cmag>0 don't exist; amplitude reaches
  the long structure only through register handoffs. (This is why the alignment is everything.)
- cmag=0 MEMR steps are DATA MOVES (DAB→regfile for a later MAC), not silence — and the famous words 5–23
  block is unexecuted staging; in-program idles (words 103/53/51) are the CPU's WCS-access slots.
- Two A/D reads per frame at exec 0 / ~52 (fig-3.5 halves); adjacent-step WR-DA pairs are legal (FPC
  double buffer); each program covers channels A–D.
- The 8 non-building ids {7,9,11,13,14,15,19,21} return empty WCS images — unresolved record slots; don't
  burn time there unless needed.
- `python tools/aru_freerun22.py` (set `E1_CACHE_DIR=tools/session0022_probes`) = the engine self-tests.
- Regenerating WCS images: `tools/session0022_probes/e1_sweep.py` (boots all ids; ~15 s each). The cached
  images are already in `tools/session0022_probes/wcs_cache.json` (13 programs) + `wcs_run_concert.json`
  (RUN-state, LFO mid-phase).
- Timing: MC 30.72 MHz (PLL ×15 from 2.048 MHz), 9 MS/step, AS thirds with ~1-MS clocked lag,
  DAB RSTB high ≈ MS2–MS8, CPC valid MS6→next-MS1.

## 6. Verification rules (unchanged discipline + one new one)
- No audio claim except as a `reverb_metrics` verdict on the emitted D/A stream, calibration battery
  passed in-process, WAV rendered (timestamped).
- POST green at every phase.
- **Tank measurements use ENERGY (RMS²·N), never RMS over touched cells** (dead-end #11).
- The final message of any probe: state which registry entry it would re-open, if any, before running it.

## 7. Artifacts
- Engine: `tools/aru_freerun22.py` (0022 decode + encoders + self-tests; probe flags csign_invert /
  immediate_backend are E3 leftovers — the RTL model supersedes them).
- Probes + caches: `tools/session0022_probes/` (e1 sweep, e2 census, e3 first-light, dataflow microscope,
  taint tracer, tank probe, WCS caches).
- RTL base to port: `tools/aru_rtl.py`, `tools/tc_clock.py`, `tools/aru_rtl_dp.py`, `tools/aru_freerun_rtl.py`.
- Record: `docs/sessions/0022 …` (proof chain, E1/E2 tables, full E3 eliminations).
- Superseded-but-bannered: plans 013/016/017/018/020, `224XL_system_architecture.md`,
  `224XL_technical_reference.md`, `224XL_provenance_ledger.md` (pre-0022 coordinate system).
