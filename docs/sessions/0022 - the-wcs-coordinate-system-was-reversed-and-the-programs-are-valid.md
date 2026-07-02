# 0022 — The WCS coordinate system was reversed; all 13 buildable programs are VALID

**Date:** 2026-07-01
**Scope at start:** whole-corpus review ("where is the project going wrong?") — five parallel readers over the
service manual, netlist/pinouts, plans 010–020 + provenance ledger, sessions 1–0021, and tools/ROMs.
**Scope at end:** ★★★ **the blocker is resolved.** The WCS **execution order is the REVERSE of the CPU image**
(pin-proven), the microword data lanes are read through the **Multibus complement** (all four lanes, uniformly),
and under that single corrected coordinate system **13/13 buildable factory programs contain exactly one RESET
microword, at the last executed step** — with a fully sane I/O census. The "invalid program" era is over.

---

## 1. The keystone (pin-verified in the owner's own trace, `224XL TC pinouts from 060-02475-D.txt`)

1. **`ADRn/` lines are active-low** (Multibus convention). Proof: the 0x4000 window decoder `tc_U50`
   (74LS133) takes ADR9/,A/–D/,F/ direct + ADRE/ inverted — it decodes 0x4000–0x7FFF **only if the lines
   carry complemented address bits** (true-level lines would decode ~0xBE00). The firmware provably writes
   the WCS at 0x4000, so the polarity is settled.
2. **The word address is NOT compensated:** mux `tc_U42/U28` (74F157, non-inverting) feeds **ADR2/–ADR8/
   straight** to WCS A0–A6 (A-side) vs **true PC0–PC6** (B-side). ⇒ **CPU word k = physical row 127−k; the
   DSP executes CPU words 127, 126, … descending.**
3. **The byte lanes ARE compensated:** `tc_U46` (74LS155) selects on ADR0//ADR1/ but its outputs are wired
   in reversed order (/Y3→lane0 … /Y0→lane3) ⇒ byte→lane = identity (consistent with E20–E23 + POST).
   Lexicon compensated the lanes in copper and the word order in firmware (the program-load copy loop
   walks the WCS descending).

Why 21 sessions missed it: **POST, E91, and every self-consistency loop are invariant under a global
bijective remap** (firmware writes and emulator executes through the same assumed map). Session 0021's
exhaustive reset search (2,560 combos) swept decodes *inside* the wrong coordinate system — it scored
"reset at CPU word 99" when the criterion is "reset at CPU word 128−L, scored over words 127…128−L."

## 2. E1 — the validity scan (this session; `scratchpad/e1_sweep.py`, WCS images cached)

Booted all 21 program ids on the verified core (session-0021 `0x8160` selector patch); 13 build (ids
1,2,3,4,5,6,8,10,12,16,17,18,20 — the rest produce empty WCS images, presumably non-program slots).
Scored every (t = stored `l2&3` value meaning tcWR) × (b = stored-bit level asserting an OFST command
line) × (window model):

| t | b | identity-100 | identity-var | **reversed-var** |
|---|---|---|---|---|
| any except (2,0) | any | 0/13 | 0/13 | 0/13 |
| **2** | **0** | 0/13 | 0/13 | **13/13** |

**The unique winner is the full Multibus data complement** — tcWR ⟺ stored `l2&3==2`, command bits
asserted on stored-bit==0 — i.e. the same convention already known empirically for lane 3 (`~l3` coeffs),
now shown to govern **all four lanes uniformly**, plus the reversed window.

Per-program: **exactly one reset in the executed window, always at its bottom edge**; the few extra
firing words (0,3,4 on ids 2/3/10) live in the never-executed staging region below the program.

| id | L (steps) | reset word | id | L | reset word |
|---|---|---|---|---|---|
| 1 CONCERT | 104 | 24 | 10 | 103 | 25 |
| 2 | 99 | 29 | 12 | 99 | 29 |
| 3 | 99 | 29 | 16 | 101 | 27 |
| 4 | 104 | 24 | 17 | 108 | 20 |
| 5 | 106 | 22 | 18 | 103 | 25 |
| 6 | 101 | 27 | 20 | 99 | 29 |
| 8 | 99 | 29 | | | |

**Programs are variable-length, anchored at word 127, ending where the reset lands** — dale116dot7's
"not all of them actually use all 128" exactly. (Whether the effective frame is L or L+1 counts — the
fetch-pipeline ±1 — is an E3 cycle-accuracy question; L=99 + 1 = the SM's canonical 100.)

## 3. E2 — the I/O census (`scratchpad/e2_census.py`)

Under (t=2, b=0), for all 13 programs:
- **1 RESET, at the last executed step (13/13)** — and it rides an output write (see below).
- **Exactly 2 RD-AD reads: execution position 0 and ~half-frame (50±4)** — fig-3.5's two-channel
  alternate-half schedule. Execution position 0 = **word 127 = the cross-program invariant step**: every
  program's shared first instruction is "read the A/D" (which is why it is invariant).
- **All four output channels A–D covered in every program**; every WR-DA sources **RDRREG** (the result
  register — the wet path, netlist §2T.3 sel==01). Programs write either 4 spread singles or stereo pairs
  (`AD`+`BC`) at opposite half-frames; adjacent-step pairs are absorbed by the FPC's double-buffer+BUSY.
- Census (CONCERT): **55 MEMR + 36 MEMW + 10 IO + 3 idle = 104 executed steps.** The idle steps
  (words 103/53/51) are the SBC's on-the-fly WCS-access NOP slots (SM §3.5 "pairs of SBC accesses").

**CONCERT reads as a reverb program at last** (execution order): A/D read + WR-XREG (input level to the
CPU — Decay Optimization's meter) → ladders of read-modify-write pairs at matched offsets (in-place
recursive delay nodes) → `MEMW 0x0000` (write at the current pointer = input injection) → outputs
B(exec 31), A(50) → second A/D read (52) → the long-delay ladder (the second loop) → outputs D(83) →
**C at exec 103 with the RESET bit** — *"the program counter is cleared by writing an address with bit 3
set to the I/O space"* (dale), verbatim: the frame's final output write clears the PC. Stereo phasing:
inputs at 0°/180°, outputs interleaved — zmix's "inputs 180° apart, outputs 90° rotated."

## 4. What this dissolves (the complete list)

- **"0/20 programs invalid"** → an artifact of scoring the wrong type value, wrong bit polarity, and wrong
  window. The ten old "spurious resets" are **MEMW steps** (delay-write offsets; e.g. 0x045D ≈ a 1117-sample
  write position) whose bit 3 was incidental.
- **The cmag=0 "diffuser block" (words 5–23) + "recirc taps {0,1,2,3}"** → **idle staging below the
  program, never executed** (plus in-program idle = CPU NOP slots). The plan-016 crux evaporates.
- **The word-127 `l1=0xCF` invariant** → the shared first executed step (the A/D read).
- **"CONCERT genuinely uses steps 100–127"** → those are the first 28 executed steps.
- **Modulation targets 107–119** → executed steps 8–20 (the early read/write ladder — the modulated taps).
- **Step-99 l0 runtime oscillation** → word 99 = physical row 28, a swept mid-program delay tap. Benign.
- **B55B "delay-transforming IO command words"** → it exempts stored-2 = **the real IO class**; it never
  touches command words. The build was always right; the read was wrong.
- **fig-3.3 "RESET/" vs tc_U25** (owner re-read this session) → the figure's row is the DMEM-local
  **dmemRESET** = inv(backplane RESET/); its ~MS5–7 fall clocks the CPC, matching the CPC-valid window.

## 5. Owner hardware corrections integrated this session (docs updated)

dmemRESET rename + the missing **dmem_U58A** (RESET/ → dmemRESET) — the frame-event tree now closes
end-to-end (reset microword → PC clear ∥ RESET/ → backplane → FPC sync + CPC count + halt sync), closing
the CPC RUN-cadence question; **tc_U19 /E = AS0/** (re-verified); **FPC CK = MS5** (tc_U39.Q1) — pins the
D/A capture edge inside the WR-DA step; **ADR SEL/ = tc_U22.pin7** (handshake JK) — no more off-sheet stub;
**backplane convention** (all same-named nets cross; ARUCKE/ crosses, ARU re-buffers via aru_U42); SM E8x
coefficients are **±** (POST anchors CSIGN both ways); the tcWR·OFST3/ region re-verified ~10× by owner +
adversarial crop review. Netlist, timing JSON (re-rendered), and SM updated accordingly.

## 6. The corrected decode spec (stored CPU-byte domain, 0x4000 image)

- **Execution:** words 127 down to (128−L); L = 128 − (the unique reset word); words below = staging.
- **Type** = `l2 & 3`: **0 = MEMR, 1 = MEMW, 2 = IO (tcWR), 3 = idle.**
- **IO command bits** (asserted when stored bit == **0**): bit3=RESET, bit4=DP, bit5=TEST,
  bit6=WR XREG (MS7-gated), bit7=WR DA; bits8–11 = SDA **D,C,B,A** (independent enables);
  source select = `(~bits13..12)&3`: 1=RDRREG, 2=XREG, 3=RD-AD, 0=none.
- **Offset/delay:** delay = stored `l0|l1<<8` **directly** (adder: CPC + line + 1 with line = ~stored ⇒
  addr = CPC − stored). B55B's window [1447, 6004] = 42–176 ms taps — sensible at last.
- **Coefficients:** cmag = `(~l3>>2)&0x3F`, XFER/ZERO = `~l3` bits 0/1 — **unchanged** (lane 3 was already
  read through the same complement; it was the other three lanes that weren't).

## 7. Next steps (E3/E4)

1. **E3 — rework the engines**: execute words 127→(128−L) in order; type table + command polarity per §6;
   CPC advances on the RESET event (traced), not the loop boundary; FPC output capture at MS5; tc_U19 AS0/
   staging in the RTL path; settle the ±1 frame-length pipeline question in the emergent-clock model.
   Then re-run the M3.X battery + `reverb_metrics` and LISTEN. Every pre-0022 free-run audio result is void
   (wrong execution order, wrong types).
2. **E4 — known-answer oracles**: firmware diag programs 7 (ZERO DELAY) and 8 (MAX DELAY) end-to-end;
   SM §5.7 V8.2.1 signature tables for the free-running T&C.
3. Housekeeping: supersession banners on plans 013/016/017/018 (cmag=0 crux, offset-source claims);
   re-derive `decode_concert_program.py` outputs; the 8 non-building ids (7,9,11,13,14,15,19,21) —
   identify what those record slots are.

## Verification state
- No tool/source files modified (docs + timing JSON + scratchpad only). POST untouched (still green by
  construction — none of its inputs changed).
- E1/E2 artifacts: `scratchpad/e1_sweep.py`, `e2_census.py`, `wcs_cache.json` (13 program WCS images).
- Memory updated: `224xl-reset-decode-contradiction` (RESOLVED + confirmed), MEMORY.md headline.

## Process lessons
- **Self-consistency tests cannot see coordinate transforms.** POST/E91/goldens all pass under any global
  bijective remap of the store. Only absolute anchors (the halt bench addresses, the invariant word, the
  modulation targets, dale's sentence) could break the frame — and they had each been explained away
  individually instead of being read as four votes against the coordinate system.
- **The winning convention was the physically-motivated one** (Multibus active-low bus, uniform across
  address AND data), already proven for lane 3 — generalizing an established local fact beat inventing
  new mechanism.
- **Exhaustive searches are only as good as their scoring frame.** 2,560 decode combos returned zero hits
  because the window/order was held fixed; 24 combos in the right frame returned exactly one perfect hit.

---

# PART 2 — E3 execution (same session): the machine is ALIVE; the MAC alignment is the last open layer

**Engine built:** `tools/aru_freerun22.py` — the 0022 decode + reversed execution on the verified Booth/MAC
arithmetic. Self-tests: decode roundtrip, zero-delay passthrough (exact), feedback comb (exact 0.5-decay
echoes), CONCERT extraction (L=104, reset word 24, census 55/36/10/3, final step = RESET+WRDA·C). ALL PASS.

**First light (CONCERT static, impulse + burst, metric-gated):** after 21 sessions of DRY — **wetness ≈ 1.0
on all four channels, seconds of persistence.** The loop closes and recirculates. Verdicts FAIL/TONAL:
a stable, input-independent limit cycle (identical peaks for impulse/burst/silence) — marginal modes, not
a decaying tail.

**Eliminations (each a sweep, all metric- or trajectory-scored):**
1. *Global CSIGN flip:* csinv=1 (the Multibus level of MI23 through the follow-JK) turns the machine
   STABLE — a real decaying ~0.3 s response (peak = 0.19·input = the traced input gain) — but the tank
   drains instantly (DM RMS 513→20 in 0.05 s). csinv=0 is over-unity (grows from silence — self-excited).
   **The dead↔rail bimodality under a global flip ⇒ two near-equal feedback paths whose RELATIVE per-step
   sign is wrong ⇒ no global convention fixes it.**
2. *cmag=0 DC baseline:* exonerated (clamping to exact 0 changes peaks by 2 LSB).
3. *Regfile/operand timing (24 variants):* write-through, delayed write, RA/WA/XFER/ZERO from the previous
   word (the tc_U19 second-stage question) — no decaying cell; space swings dead↔rail.
4. *CSIGN follow-vs-TOGGLE (the unresolved JK) × 4 timing bases:* no decaying cell.
5. *Split pipeline depths* (fig-3.4 owner-read: product retires at +2, XFER/ZERO at +1): vd2/xd1 is the
   closest cell yet — near-unity, low-level slow growth (peak ~1500) — still not a decaying tail.
6. *RUN-state WCS:* captured live (40M ticks past mainloop): only 22/512 bytes change — the swept tap
   offsets (words 42,56,57,94,107,108 l0) **and lane-3 COEFFICIENTS of 16 ladder words** (56,57,62-64,
   66-68,107,108,113-115,117-119) — live coefficient modulation (corrects the M4-era "modulation never
   touches coefficients"). Structurally identical program (same census/L/reset/input-cmag) ⇒ the static
   snapshot is not the blocker per se.

**Dataflow microscope (frame-level probe):** the input enters at gain 6/32 via the second A/D read (the
first is cmag=0 in this build), lands in the tank (`DM[22930]←−3080`), returns one frame later on the
offset-42607 read — and then wet values repeatedly die in the register file 1–2 steps before their
consumers (R3 clobbered by WA=3 dumps; RES overwritten one step before the next MEMW). The program's
register lifetimes presuppose an operand/pipeline alignment the behavioral engine doesn't have yet.

**Open (the one remaining layer):** the exact MAC/register alignment — POST provably cannot constrain it
(three semantics all pass), and knob-sweeps are exhausted. Next arbiters, in order:
(a) **live-modulation co-sim** (8080 interleaved at ~62 ticks/frame — the real machine never runs
statically) — **RUN, ELIMINATED:** modulation does not stabilize any cell (baseline sign still rails
to ~17k plateau; near-unity vd2/xd1 cells still creep to ~1.4-2k over 2.5 s; stable-sign cell stays
dead). The alignment fault is upstream of modulation;
(b) **the edge-driven RTL model** (`aru_freerun_rtl` + ClockEngine, gate-equation timing, no knobs)
ported onto the 0022 decode;
(c) **hand-analysis of one 4-step ladder cell** (exact CONCERT bytes, closed form — derive the alignment
that makes it an allpass);
(d) the **E4 known-answer oracles** (firmware diag ZERO-DELAY / MAX-DELAY, §5.7 signature tables).
