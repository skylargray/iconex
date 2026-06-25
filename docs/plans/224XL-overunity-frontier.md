> **⚠️ SUPERSEDED (Session 8, 2026-06-24) — the over-unity λ was a RED HERRING.** The power-iteration
> eigenvalue is a recirculation mode **decoupled from the audio input** (and dominated by a frozen-DC / collapse
> artifact); driving λ≤1 did NOT produce a working reverb. Session 8 then **fully confirmed the microword
> decode** (incl. owner schematic traces: XFER=MI24=l3.b0, ZERO=MI25=l3.b1 AS0-gated, C0-C5=MI26-31, inv_l3=True),
> found the **multiply scale is /32 not /64** (`prod>>5`, per the ADD'L MULT diagnostic), confirmed the FPC I/O is
> 16-bit, and **localized the one remaining bug to ARU datapath TIMING** — the static-WCS reverb tank is dead
> (CONCERT impulse → silence) because the diffused/predelayed signal never gets written into the DMEM long-delay
> lines, even though every decoded field is correct. **▶ START HERE NOW: `docs/plans/224XL-signature-analysis-plan.md`**
> (the endgame: exact 3-state ARU model + signature-table validation) and memory `224xl-session8-inv-l3-and-dead-tank.md`.
> The Session-7 "decode error → over-unity" narrative below is HISTORICAL — the decode it produced is correct,
> but the over-unity it chased was never the real problem.

---

# 224XL over-unity — RESOLVED (Session 7): it was a MICROWORD DECODE error (owner schematic trace)

**Status: ROOT CAUSE FOUND.** The over-unity was a **microword-decode error** — the reverse-engineered field
map in `aru_datapath.load_microcode` had WA, the DMEM read/write select, XFER, ZERO, CSIGN, and the
coefficient in the WRONG bit positions. Rebuilt from the owner's schematic trace (the true map is in §5a),
the eigenvalue test flips completely: **every clean program is now lossless (λ=1.000000) or gently decaying —
ZERO programs hot, ZERO dead tanks** (vs 8/13 hot, up to λ=1.67, in the old decode). CONCERT → λ=1.000000.
This is the textbook reverb prototype (lossless core; RT60 from a separate damping coefficient). `acc_latch`
(the manual-confirmed pipeline timing) is a genuine secondary correction but the DECODE was the main bug.

**Confirmed corrected microword map (owner trace + test):** offset OFST0–15 = MI0–15 (l0,l1); l2 byte:
b0=DMEM read(1)/write(0), b1=DMEM-op-enable, b2,b3=WA0,WA1, b4,b5=RA0,RA1, b6=PROT(MI22, datapath-irrelevant),
b7=CSIGN; l3 byte: b0=XFER, b1=ZERO, b2–7=coeff C0–C5. DP(=MI4)/RESET D/(=MI3) are offset bits reused on
non-DMEM device steps (datapath-irrelevant). Tools: `tools/_hunt_rebuild.py` + `_hunt_rawcache.py`.

**Device-select decode (owner trace) — now complete.** `MEMAC = MI17` directly (DRAM accessed iff MI17=1;
NO offset-bit15 gating). Sub-decoder (MI17=0 & MI16=1), DAB read source by (MI13,MI12): 00=idle, **01=RDRREG/**
(result reg → DAB = the feedback path), 10=RD XREG/, **11=RD AD/** (A/D audio input). WR DA/ (D/A out) from the
first-half MI16/MI17 via U49. MI12,MI13 = microword bits 12,13 (l1). ⇒ the eigenvalue model must treat only the
**RDRREG/** (MI17=0,MI16=1,MI12=1,MI13=0) steps as "result reg drives DAB"; RD AD/ injects the audio input
(=0 in the closed loop), RD XREG/ and idle inject 0. (Earlier rebuild lumped all MI17=0 as result-reg — an
over-approximation; full device decode now in `_hunt_rebuild2.py`.)

**Byte-inversions — mostly pinned; one byte left.** PINNED (physically justified):
- **inv_l2 = False** (l2 used direct, NOT `~`): "MEMAC = MI17 *directly*" ⇒ MI17 = raw l2.b1; and under
  inv_l2=False the device decode identifies the RD AD/ (A/D-input) steps as **s75/s125** — exactly the A/D
  input-fingerprint steps — whereas inv_l2=True puts them at s77/s127 (wrong). Two independent reasons.
- **read_bit = 1** (MI16=1 ⇒ DMEM read, =0 ⇒ write), per the owner's U47 trace.
- l0,l1 inverted (offset = `~(l0|l1<<8)`, delays already verified; MI12,MI13 = `~l1` bits 4,5).
- **inv_l3 (the l3 coeff/XFER/ZERO byte) = the ONE remaining bit.** Both polarities give all-reverbs-≤1
  (no hot), so the eigenvalue can't separate them. Weak lean to **inv_l3=True** (gives 18 zero-coefficient
  move-steps, typical of real microcode; inv_l3=False makes all 110 steps nonzero-coeff). Definitive pin
  needs the diagnostic passthrough, which my simplified harness can't run: the D/A output path (WR DA/) and
  the 2-channel register routing aren't modeled (passthrough reads 0 in `_hunt_diagpin2.py`). **Best path to
  finish: pin inv_l3 in the C++ reconstruction** — build the full A/D→ARU→D/A datapath and run the ZERO-DELAY
  (unity passthrough) + MAX-DELAY (0.5 s) diagnostics end-to-end against their known behavior; that single
  bit is the only remaining ambiguity, and it does NOT affect the over-unity result.

Then: rebuild `aru_datapath.load_microcode` to the true map (inv_l2=F, read_bit=1, inv_l3 TBD), regen golden,
mirror to C++, verify CONCERT IR → RT60≈20 s. Tools: `_hunt_rebuild2.py` (full device decode + reverb test),
`_hunt_diagpin2.py` (diagnostic harness, has the WR DA/ output-routing gap noted above).

---
*(Historical Session-7 narrative below — the (b3,b4) decode and acc_latch-only "partial fix" were stepping
stones; the real answer is the full decode correction above.)*

**REFUTED this turn (owner schematic trace):** the **RA=(b3,b4)** decode that gave 13/13. Owner traced
RA1 = U19(74LS377) Q2 ← D2 ← (U18 74163 pipeline) ← net **MI21** ← DATA5. MI21 = third-byte bit 5 = the model's
**b5**. So **RA = (b5,b4) — the current/documented decode — is CONFIRMED, and (b3,b4) is dead** (it needed RA's
high bit to be the DMEM-select bit; U19 shows RA1 and the DMEM-select are different bits). The 13/13 was an
overfit on a wrong decode.

**THE remaining lead — the rest of the microinstruction decode is WRONG in my model.** Owner's U19 output map:
Q0=DP, Q1=RA0, Q2=RA1, Q3=**RESET D/**, Q4=XFER. My model has **no DP and no RESET D/** bits, and its XFER(b2)/
ZERO(b7)/DMEM-select(b3) positions do **not** line up with U19's layout. So my reverse-engineered byte decode
(RA aside) is misassigned — and a wrong XFER/ZERO/DMEM position, or the unmodeled per-cycle **RESET D/**, is the
likely cause of the residual over-unity. Next: reconstruct the TRUE microword→control map from the T&C
schematic (crops in `docs/reference/224/crops/tc2_uword_*.png`, `tc2_srcselect.png`, `tc1_xferck_gen.png`;
full sheets `…-060-01320_1/2.png`) and rebuild the decoder. See §5.

**Retraction/whiplash history (lesson):** mid-session I (a) found (b3,b4)+acc_latch=13/13, (b) wrongly
retracted `acc_latch` as "unphysical" from the static net topology, (c) the owner's timing diagrams reinstated
`acc_latch`, (d) the owner's RA trace then refuted the (b3,b4) decode. Net: `acc_latch` REAL+partial; (b3,b4)
DEAD; decode reconstruction is the path. Lesson: reconcile candidates with BOTH net topology AND timing AND the
actual microword wiring before believing an eigenvalue fit.

Session 7 (2026-06-24). Supersedes the Session-6 framing below. Full prior record:
`docs/plans/224XL-concert-decay-investigation.md`. C++ core state: memory `224xl-cpp-scaffold`.

---

## 1. The corrected problem statement (this is the big Session-7 reframe)

The over-unity is **NOT CONCERT-specific.** With a *robust* eigenvalue measurement (random-start power
iteration — the old single-seed-at-prog[0] measurement was giving a **false "dead-tank" λ=0.0045316
artifact** = the renorm floor `exp(log(1e-300)/128)` whenever prog[0] didn't couple to the tank),
**8 of the 13 cleanly-booting programs are over-unity under the base model**, while 5 are correctly lossless:

| program (pid) | base λ (b5,b4 decode), ppm from 1.0 |
|---|---|
| 0x01 CONCERT | +1126 |
| 0x04 RICH CHAMBER | +1056 |
| 0x05 ROOM | +34664 |
| 0x06 SMALL ROOM | +23970 |
| 0x0a CD PLATE B | +8198 |
| 0x0c CHORUS&ECHO | **+667788 (λ=1.67!)** |
| 0x10 PLATE/PLATE | +76109 |
| 0x12 PLATE/CHORUS | +83222 |
| 0x02,0x03,0x08,0x11,0x14 | lossless (±0 ppm) |

(pid→name is the NVS3 directory order, approximate. The 8 hot programs all boot clean — over-unity is real,
not a load artifact. Independently confirmed for CONCERT & 0x04 by the saturating-INTEGER impulse envelope:
+1.81 / +0.018 dB/s GROW — a method totally separate from power iteration.)

**The correct hardware model is program-independent, so it must make EVERY (reverb) program lossless
(λ≈1.0, the lossless prototype; RT60 then comes from a separate small damping coefficient).** "All programs
lossless" is a *vastly* stronger objective than the CONCERT-only test the earlier sessions used, and it is the
right gate for any candidate fix. It is what exposed the acc_latch+reg_wbr-alone result (below) as a CONCERT
overfit, and what the winning candidate passes.

## 2. The Session-7 candidate (manual-grounded timing + decode lead)

**TWO ingredients together collapse all 13 clean programs from λ up to 1.67 → near-lossless:**

**(a) TIMING — `acc_latch` (now MANUAL-CONFIRMED, not a guess).** XFER captures the accumulator BEFORE the
current microinstruction's own product is accumulated. Evidence: Service Manual §3.7 (line 400): *"the final
result of the multiply and accumulate does not become available until the very end of AS0 of the next system
cycle. If a transfer command is present the result register is loaded at this time by XFER CK; if the zero
command is given the accumulator is also cleared at this instant"* + Fig 3.4 (XFER CK & ZERO/ pulse at AS0
while the product only builds across AS0→AS1→AS2). So the result register (U43/U44, D=PP=AC+product) does
latch AC+product, but at the XFER-CK instant the product register hasn't formed this step's product → RES =
the accumulated group sum. At microinstruction granularity this is exactly the `acc_latch` flag (XFER reads
the pre-product accumulator; ZERO clears after). The current model (XFER reads post-product ACC) is WRONG.
*This was mid-session wrongly retracted as "unphysical" — the timing diagrams reinstated it.*

**(b) DECODE — RA=(b3,b4) (LEAD, needs the RA-wiring trace §5-B).** With the correct `acc_latch` timing,
RA=(b3,b4) makes ALL 13 clean programs near-lossless; RA=(b5,b4)+acc_latch reaches fewer. It is a revision
*within* the "RA-vs-XFER ambiguity in lane2[5:2]" that `aru_datapath` resolved on CONCERT alone, and it
contradicts the documented field map (b3 = DMEM-select), so it is the one thing still needing the schematic
(which microword bits drive RA0/RA1). `reg_wbr` (register-file write-before-read) was a third flag in the
flag-model; with the manual `acc_latch` it may be unnecessary — settle when the faithful model is finalized.

**Measurement caveat:** the random-start power iteration is start-sensitive near λ=1 (some genuinely-lossless
programs spuriously read the dead-tank floor). The robust signal is the gross collapse (λ=1.67→~1) and the
exact-lossless fixes; precise "N/13" counts need a hardened eigensolver (§6).

*Note: `_hunt_cyclefaithful.py` and `_hunt_pipeline.py` (the explicit cycle/defer models) had scaling/defer
BUGS (missing the ÷8 result shift; an over-aggressive 1-cycle defer that starves the loop). The
manual-consistent model is the `acc_latch` flag model in `_hunt_lossless.py` — at microinstruction
granularity the manual's "result next cycle" is captured by `acc_latch` alone; no separate defer.*

---
**Evidence — converged λ (nsamp=60000, 2-seed), all 13 clean programs, candidate = (b3,b4)+acc_latch+reg_wbr:**

| pid | base (b5,b4) | CANDIDATE (b3,b4)+acc_latch+reg_wbr |
|---|---|---|
| 0x01 | +1126 | **+0.0** |
| 0x04 | +1056 | **+0.0** |
| 0x05 | +34664 | **+0.0** |
| 0x06 | +23970 | +362  (residual) |
| 0x08 | 0 | +0.0 |
| 0x0a | +8198 | +37 |
| 0x0c | **λ=1.67** | **+0.0** |
| 0x10 | +76109 | +0.0 |
| 0x12 | +83222 | +0.0 |
| 0x02,03,11,14 | 0 | ~0 |

**One (decode, timing) choice collapses λ values spanning +0…+667788 ppm (7 orders of magnitude) to
near-lossless — 11/13 to machine-zero, 2 within a few hundred ppm.** A random overfit cannot take a λ=1.67
program to exactly λ=1.0 while holding 12 others at λ=1.0. Integer audio-path independently confirms CONCERT
& 0x04 go from GROW to flat/decay. **This is the leading hypothesis for the whole over-unity bug.**

**Confidence:** HIGH that *some* (decode+timing) correction of this shape is the fix (it's the only thing that
has ever passed the all-programs gate); MEDIUM on the *exact* form below until the schematic confirms it
(§5). The decode and the timing are both **structural** (program-independent), not hand-tuned per program.

## 3. Lead 1 (all-pass coefficient matching) — REFUTED at the premise

An exact, validated (max err 1.8e-15 vs the float datapath) **symbolic single-sample flow graph**
(`tools/_hunt_symflow.py`) proves the +124 closers are **NOT** the per-cell all-pass feedback. Each cell's
self-feedback (coeff of its own delayed word M[O] in its next write M'[O]) is at most **|−0.766|** (cells
s54, s105), mostly −0.03…−0.12 — every cell is sub-unity, and the +124 is a *feedforward* term where
self+input = 1.0 exactly. The cells are recursive **combs** coupled into an FDN (e.g. s54:
M'[O] = −0.766·M[O] − 0.984·M[cross] + 0.234·M[in]), not Schroeder all-passes. So "make feedforward
magnitude = the +0.969 feedback" was based on a wrong model. The coupling matrix C (66×66) is massively
non-paraunitary (σ_max up to 20.7; ρ(C)=1.75 *uniquely* for CONCERT & 0x04) yet realized λ barely exceeds 1
— i.e. the eigenvalue is highly non-normal and **delay/ordering/timing sensitive**, which is exactly why
single-coefficient fixes can't reach it and why the *timing* correction in §2 is so powerful.

## 4. Still ELIMINATED / DEAD ENDS (do not re-investigate)

- λ is real & converged (4 methods incl. independent integer envelope dB/s). Not a measurement artifact.
- Lead 1 literal recipe (per-cell all-pass feedforward/feedback matching): premise wrong (§3).
- **acc_latch+reg_wbr with the OLD (b5,b4) decode = CONCERT OVERFIT** (fixes only 3/8 hot programs, worsens
  0x06). Single-DOF fixes all fail the all-programs gate. The decode change in §2(a) is what unlocks it.
- `mac_pipe` (multiplier product-register 1-cycle pipeline, ARUCK): collapses the loop to the dead-tank
  λ=0.0045 → NOT the hardware (or it's bypassed). `D_wbDelay` (DMEM CAS write-back one step late): no effect.
  ⇒ ARUCK and CAS timing are NOT the over-unity lever; deprioritize tracing them.
- `res_latch` alone (74F374 latches one microstep behind for b3): halves CONCERT (+1126→+564) but is NOT in
  the winning combo and *breaks* the candidate if added on top (over-damps several to the dead tank).
- An explicit extra **1-cycle output `defer`** on top of `acc_latch` (tried in `_hunt_pipeline.py`) starves
  the loop → dead tank. The manual's "result next cycle" is already captured by `acc_latch` at microinstruction
  granularity; do NOT add a second deferral. (`acc_latch` itself is CONFIRMED physical — see §2a, not eliminated.)

## 4b. ARU datapath topology — RECONSTRUCTED from the 060-01318 pinouts (ground truth)

`regfile F=R[RA]` (LS670 U29–U32; write strobe **DAB WSTB**) → multiplier `F×coeff` (combinational) →
**product register PR** (U10/U11/U12, clock **ARUCK**) → adder `Σ = AC + (±PR)` (U19–U23, combinational;
sign via U5–U9 XOR) → sat-mux `PP = Σ` (U33–U37) → **accumulator AC ← PP** (U45–U49 LS163, clock
**ARUCKE/**, cleared by **ZERO/**, LOAD/ENP/ENT grounded ⇒ parallel-load every edge) ; **result register
RES ← PP3..PP18** (U43/U44 74F374, clock **XFER CK**, output-enabled to the DAB bus by **RDRREG/**).
So `RES = (AC + product)[3:18]` — but per the TIMING (§2a, Fig 3.4) the XFER-CK edge is at AS0 *before* the
current microinstruction's product is formed, so the captured value is the prior group sum (= `acc_latch`).
The clock phasing is now RESOLVED by the manual (Ch.3 + Fig 3.2/3.3/3.4); the only remaining unknown is the
**RA wiring** (§5).

## 5a. CONFIRMED microword bit→signal map (owner schematic trace) — DECODE IS MIS-MAPPED

Owner traced U19 (74LS377) + the 74163 pipeline regs (U17/U18/U4). Confirmed (by MI bit):
- **WA0 = MI18, WA1 = MI19** (from U17 S163 pins 12/11).
- **RA0 = MI20, RA1 = MI21** (from U18; matches the model's b4/b5).
- **XFER = MI24** (U19 Q5 ← D5 ← U4 pin14).
- **ZERO = MI25** (U19 Q6 ← D6 ← U4 pin13; ZERO/ = NAND(Q6, AS0) — gated to AS0, matching Fig 3.4).
- **DP ← MI4** (U19 Q0 ← D0 ← U34A; DP → LS27 → S1 = multiplier shift-reg control).
- **RESET D/ ← global RESET/** (U19 Q3 ← D3 ← RESET/, NOT a microword bit).
- **CSIGN/ = MI23** (U19 Q4 ← MI23 → U34D LS08 → U20 S112 → CSIGN/). So MI23 = coefficient sign (the
  model's "ZERO" bit b7 = MI23 is actually CSIGN). Q7 ← (not depicted) = TBD.
- **DMEM access decode = U47 (LS139), enable grounded, select A=MI16 B=MI17:** Y2=MEMW/ (write DMEM) when
  MI17=1 & MI16=0 ; Y3=MEMR/ (read DMEM) when MI17=1 & MI16=1. So **MI17 = "DMEM op this step", MI16 =
  read(1)/write(0)**. When MI17=0 → Y0/Y1 (pin4/5) = non-memory DAB sources (TBD). (U47 2nd half: A=MI12,
  B=MI13, enable=convoluted = the X-reg/AD/DA device selects.)
- **HUGE implication:** the model's b0,b1 (which it called WA0,WA1) are actually the **DMEM op-select
  (MI16,MI17)**; the real WA = b2,b3 (MI18,19). And the model READS/WRITES DMEM on every step — WRONG; the
  hardware only touches DMEM when MI17=1, else the DAB comes from the result register / A/D (Y0/Y1). So the
  model's recirculation graph is fundamentally mis-wired. Corrected control byte (l2=MI16–23): b0=DMEM r/w,
  b1=DMEM-op-enable, b2,b3=WA0,WA1, b4,b5=RA0,RA1, b6=TBD, b7=CSIGN; and l3: b0=XFER, b1=ZERO, b2..7=coeff?
- **DAB source/dest is a 2-level decode.** U47 Y0(pin4)=NC (MI17=0,MI16=0 → idle). U47 Y1(pin5) (MI17=0,
  MI16=1) → U33 inv → enables U47 2nd half (select MI12/MI13) + U49 → the non-memory selects WR DA/, WR XREG/,
  RD AD/, RD XREG/, RDRREG/, TEST. So: MI17/MI16 = {00 idle, 01 sub-decoder, 10 write-DMEM, 11 read-DMEM};
  sub-decoder (MI12/MI13) picks result-reg / A/D / X-reg / D/A. For the closed-loop recirc, model the DAB
  source on non-DMEM steps as the RESULT REGISTER (refine with the exact RDRREG/ MI12/MI13 code if needed).
- **Coefficient magnitude C0–C5 = MI26–MI31** (= l3 bits 2–7), sign **CSIGN = MI23**. So the real coeff =
  ±((l3>>2)&0x3F)/64 with sign from l2.b7 — NOT the model's (l3&0x7F with sign=l3.b7). Full l3 byte: b0=XFER,
  b1=ZERO, b2..7 = C0..C5.
- **Near-complete corrected microword map** (raw stored byte → bit; polarity/inversion TBD by test):
  l0,l1 = offset (TBD vs DP=MI4); l2: b0=DMEM-rw, b1=DMEM-op, b2=WA0, b3=WA1, b4=RA0, b5=RA1, b6=TBD(MI22),
  b7=CSIGN; l3: b0=XFER, b1=ZERO, b2..7=C0..C5. DAB src non-DMEM steps = result reg (assume).
- **Offset OFST0–15 = MI0–MI15 directly (confirmed)** = stored bytes l0,l1 (matches the old decode). **DP and
  RESET D/ are NOT separate microword bits** — they are MI4 and MI3 (offset bits) REUSED, gated by U47 pin5
  (the sub-decoder select = MI17=0 & MI16=1, a non-DMEM device op). On those steps the offset isn't a DMEM
  address, so MI3/MI4 double as RESET D/ (→U25 S74) and DP (→S1 multiplier shift). Irrelevant to the recirc
  eigenvalue. **DECODE NOW COMPLETE** except MI22 (l2.b6, old model's ignored "PROTECT"). Rebuilt in
  `tools/_hunt_rebuild.py` (+ `_hunt_rawcache.py`); inversions/polarities swept; test result pending.

**Implication — the model's `aru_datapath.load_microcode` decode is WRONG on almost every control field
except RA.** The model slices the microword as 4 bytes with the 3rd byte = MI16–23 (locked by RA1=MI21).
In that byte the model put WA at bits 0,1 (real WA = bits 2,3 = MI18,19), used bit 2 for XFER and bit 3 for
the DMEM-write-select — **but bits 2,3 are actually WA0,WA1.** And the REAL XFER (MI24) and ZERO (MI25) live in
the 4th byte, which the model treats as the COEFFICIENT. So the model's "comb closers" (steps it thinks write
the result to DMEM + XFER) are really just **WA=3 (scratch-register) steps** — a coincidental structure that
recirculates for CONCERT and goes haywire elsewhere. **This mis-decode — not a subtle timing effect — is the
likely root of the multi-program over-unity.** acc_latch is still a real (confirmed) timing fix, but the
decode must be rebuilt from scratch first. STILL NEEDED to rebuild (see §5):
DMEM read/write select bit; coefficient C0–C5 + CSIGN bits; offset OFST0–15 bits; U19 Q4(MI23)/Q7 functions.

## 5. WHAT TO TRACE / RECONSTRUCT — the full microinstruction→control decode

Clock phasing is ANSWERED by the manual (no trace needed): microinstruction = 9 MC (32.55 ns) = 3 ARU states;
MAC pipelined; XFER CK & ZERO/ at AS0 (⇒ `acc_latch`); DMEM write data = result reg via XFER CK; register file
written every cycle (WA=3 scratch). RA = (b5,b4) CONFIRMED by the owner's trace. **What's left is the REST of
the microword→control-signal map**, because the model's `_hunt_*`/`aru_datapath.load_microcode` decode (XFER=b2,
ZERO=b7, PROTECT=b6, DMEM=b3, WA=b1:0) is REVERSE-ENGINEERED and does NOT match the real hardware latch layout.

The hardware path: microcode RAM (MCM68B10) → AM8304 transceivers (U44/U115…, DATA↔MI bus) → 74163 pipeline
regs (U17,U18,…, loaded each cycle) → 74LS377 decode latches (U19,…) → control signals. Owner-confirmed for
U19: Q0=DP, Q1=RA0, Q2=RA1, Q3=**RESET D/**, Q4=XFER; RA1←D2←MI21←DATA5.

**Needed (each is a small lookup the owner can do, or I can trace from the crops/full sheets):**
1. U19 Q5,Q6,Q7 — what signals? And confirm XFER(Q4)←D4←MI23 (locks the bit order).
2. The latch(es) that generate **ZERO/**, the **DMEM read/write select** (MEMR//MEMW/ vs RDRREG/ — see
   `tc2_srcselect.png`), and **WA0/WA1** — and which MI/DATA bit feeds each.
3. What **DP** and **RESET D/** do (where they go / what they reset or enable) — these are per-microinstruction
   controls the model omits entirely; a wrong/omitted one is the prime suspect for the residual over-unity.
Then rebuild `load_microcode` to the true map and re-test all-programs-lossless (with `acc_latch`).
Schematic sources already in repo: `docs/reference/224/crops/tc2_uword_latches.png`, `tc2_uword_decode_feed.png`,
`tc2_srcselect.png`, `tc1_xferck_gen.png`; full T&C sheets `…-060-01320_1.png` / `_2.png`.

(NOT needed: ARUCK pipelining alone collapses the loop and CAS write-back delay has no effect — §4 — so
deprioritize those. The product register DOES exist (ARUCK) — that's why A1's phase matters.)

## 6. Open items

- **Measurement robustness.** The random-start power iteration is start-sensitive near λ=1 (a single seed
  spuriously reads the dead-tank floor for some lossless programs). **3-seed-max fixes it in practice** — the
  manual-consistent candidate (`_hunt_lossless.lam`, acc_latch+reg_wbr+(b3,b4), 3 seeds, nsamp=50000) gives a
  clean **13/13** (0x06 +371 ppm, 0x0a +37, rest machine-zero). For a definitive final check use an Arnoldi
  eigensolver on the matrix-free operator.
- **Get the RA wiring (§5-B)** from the schematic — the last unknown. Clock phasing is already resolved from
  the manual. Then finalize a clean faithful model (start from `_hunt_lossless.py`'s `acc_latch` model, which
  is the manual-consistent one — NOT `_hunt_cyclefaithful.py`/`_hunt_pipeline.py`, which have bugs §7) and
  re-confirm all-programs-lossless with a hardened eigensolver.
- Settle whether `reg_wbr` is actually needed: with the manual `acc_latch`, does RA=(b3,b4)+acc_latch ALONE
  reach all-lossless, or is reg_wbr (register-file write-through) also required? (Affects what to verify on
  the schematic — the LS670 same-address read-during-write behavior, DAB WSTB vs read.)
- Only after the schematic confirms a decode+phasing: mirror to C++, **regen golden** (it will change),
  re-run gates (`ctest`, `diff_harness`, `mult_vectors_test`), verify a real CONCERT IR → RT60≈20 s.

## 7. Tools (all Session-7, reuse these)

- `tools/_hunt_symflow.py` — exact validated symbolic single-sample flow graph (§3). `sym_sweep(prog)`.
- `tools/_hunt_coupling.py` — coupling matrix C + SVD/non-normality (σ_max, ρ).
- `tools/_hunt_progcache.py` — boots all 21 programs once → `_progcache.pkl` (decoded microcode +
  clean-boot status). 13 clean. **Use the cache; don't re-boot per experiment.**
- `tools/_hunt_lossless.py` — `lam(prog, pick, **timing)` random-start λ; decode-vs-all-programs sweep.
- `tools/_hunt_decodefix.py` — parametrized `lam(prog, pick, dsel, **timing)`; flag-model decode sweep.
- `tools/_hunt_lossless.py:lam(prog, pick, acc_latch=True, reg_wbr=True)` — **the manual-consistent model**
  (acc_latch = XFER reads pre-product accumulator). This is the one that gives the candidate's 13/13.
- ⚠️ `tools/_hunt_cyclefaithful.py` and `_hunt_pipeline.py` — attempts at explicit cycle/defer models; BOTH
  have bugs (cyclefaithful: RES=AC+product without the ÷8 result shift used a wrong XFER-vs-product order;
  pipeline: missing ÷8 fixed, but the explicit 1-cycle `defer` starves the loop). Do not trust their counts.
  The manual's pipeline is captured by `acc_latch` at microinstruction granularity (no separate defer).
- `tools/_hunt_timing.py` / `_hunt_timing2.py` / `_hunt_timing3.py` — timing-variant engines (single &
  random-start; the latter is the robust one).
- `tools/_hunt_intconfirm.py` — saturating-integer audio-path dB/s confirmation under the candidate.
- Base model: `tools/aru_datapath.py`; float λ: `tools/exp_lambda_clean.py:lambda_trajectory`.
- Numbers: CONCERT base λ=1.0011264 (+1126 ppm); candidate ≈+0.0; native 34130 Hz; closers coeff +124→0.969.

## 8. Mindset (hard-won — reinforced this session)

A decay/lossless result is only real if it is (a) a principled structural correction (not hand-tuned per
program), (b) survives the **all-programs** gate, (c) is consistent with an independent method, **and (d) is
realizable in the actual hardware — reconciled with both the chip-net TOPOLOGY (§4b) and the TIMING (Ch.3 +
Fig 3.2/3.3/3.4), not just an abstract flag model.** Cautionary tale this session: I read the static
topology (RES D = AC+product) and wrongly declared `acc_latch` impossible — but the *timing* (XFER CK fires
before the product forms) makes it real. Net topology alone is necessary but not sufficient; you need the
clock phasing too. The candidate now meets (a)–(d) for the TIMING; the DECODE (RA=(b3,b4)) still needs the
§5-B trace. Do NOT change the C++ core / golden until the RA trace confirms the decode (it rewrites golden).
