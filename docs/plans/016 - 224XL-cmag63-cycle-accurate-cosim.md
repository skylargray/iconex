# 224XL — nail down the cmag=63 multiplier residual via a cycle-accurate POST single-step co-simulation

> **READ-FIRST / START-HERE for this task.** This is a focused continuation of Phase-1 (plan
> `015`). Phase-1 is essentially done: the netlist-faithful ARU passes the firmware's POST
> **latch (E32, 0x0A1D)**, **register (E40, 0x0C48)**, and **multiplier (E83, 0x0942)** self-tests
> un-suppressed on the verified 8080. The multiplier is bit-exact for **16/20** firmware goldens
> *purely from the verified gate wiring*; the remaining **4 cmag=63 (all-ones coefficient)** cases
> are off by **+1..+2 LSB** and currently pass only via a flagged **calibrated fudge** (`+3·dual`
> in `tools/aru_booth.py::multiply`). **This task: explain those 4 cases FAITHFULLY (no fudge),
> or definitively rule out the leading hypothesis and localize the cause.** The method (owner's
> directive): a **cycle-accurate co-simulation of the POST single-step sequence** — the SBC (the
> verified 8080) stepping the ARU through the *real* ARUCK/ARUCKE/XFER/ZERO/MS/AS pipeline with
> register state carried across consecutive `OUT 0x03` strobes — **not** isolated per-value
> multiplies (which is all the current model does).

---

## ✅ EXECUTED 2026-06-29 — RESULT: pipeline hypothesis REFUTED; cmag=63 = unique combinational +3/dual-rail phase

Deliverable: **`tools/aru_cycaccurate.py`** (self-contained; `python tools/aru_cycaccurate.py`). Three results:

- **PART A — the leading hypothesis (§2) is REFUTED.** A stateful AS-phase engine (74194 / partial-product reg /
  accumulator / result reg, persisting ACROSS strobes), driven by the *exact* firmware strobe sequence (disassembled:
  5 blocks, **one** OUT-0x03 strobe per case, ZERO clears the accumulator every step, **no reset between cases**),
  swept over **every** physically-motivated schedule (PP-register delay 0/1, accumulator-clear position, drain depth,
  cross-step PP leakage), **never exceeds 16/20**. No sequential schedule reproduces cmag=63. The residual is **not**
  a deferred-MAC / single-step-readback / register-state effect. (Also: since the faithful per-step model already
  matches 16/20 *same-step* and the firmware compares each case to its own golden, a whole-product "read N−1"
  deferral is independently impossible — it would break the 16 that pass.)
- **PART B — the correction is a UNIQUE flat +9.** The accumulator (−ACC) must be larger by K for each cmag=63 golden:
  K ∈ [7,14] (0x3333), [4,11] (0xCCCC), [2,9] (0x3FFF), [9,16] (0xC000); **intersection = exactly {9}** = 3 phases ×
  +3. It is **not operand-dependent** — the apparent +1/+1/+1/+2 at the output is just the `≫3` round. (The plan's §0
  table below showed faith=25804 for 0x3333; the live model gives 25805 — the §0 numbers were stale, corrected here.)
- **PART C — it's COMBINATIONAL, gated by both Booth rails.** `comb_array` is exactly additive (`dual==m0+m1−none`);
  **+3 per dual-rail phase is the unique exact correction** (+1/+2/+4 all fail → 20/20 only at +3). cmag=21 (M0-only)
  and cmag=42 (M1-only) need +0, so it fires only when **M0 AND M1 both assert**, adding +3 into PR0/PR1.

**Service-Manual chapter 5 corroborates the localization** (read per owner request): the all-ones coefficient is
notated **"+63/64"** (max fraction 1−2⁻⁶, a designed special case), and *"E89-E8B [the +63/64 test] … test the
intermediate address … check U13, U24 to U25, and U38 and U39"* — the **front-end intermediate adders**
`aru_U13/U39/U25/U38/U24`, exactly where the +3 lands. (Module map from EA0-EB3: 74LS00 = Booth NAND array;
U13/U24/U25/U38/U39 = intermediate adder; 74S86 U5-U9 = sign; U19-U23 = second adders.)

**Disposition vs success criteria:** criterion **#2 fully met** (definitively NOT pipeline; re-localized + documented),
and **#1 closed as far as is tractable** — the `+3·dual` in `aru_booth.py::multiply()` is the **unique, firmware-
validated** correction, and its gate-level origin is now **EXHAUSTIVELY EXCLUDED from the digital wiring**: the owner
re-verified (2026-06-29) against **060-01318** the intermediate adders `aru_U13/U24/U25/U38/U39`, the **entire** NAND
Booth array (`aru_U14/U26/U27/U28/U40/U41/U50/U51/U52/U53`), the M0/M1 fanout (`aru_U54`), and the spare gates
(`aru_U42` 74S86 g3/g4, `aru_U2` 74S04 g1/g2 — schematic-labeled spare/unused) — **all correct as traced; no `M0·M1`
gate; all ten F283 carry-ins accounted for.** So the +3 is an **accepted empirical correction** whose origin lies
*outside* the traced gate netlist (candidates, not pursued: a device/family-level 74LS00→74F283 behavior in the
both-rails-driven case, or a board ECO per SM §8). **Regression (criterion #3):** POST E32 + E40 + E83 still PASS
un-suppressed on the verified 8080 (`tools/aru_post.py`); cmag=21/42 + unity stay exact. Full write-up: netlist
**§4F.9**; reproducer **`tools/aru_cycaccurate.py`**. **STATUS: CLOSED. Next frontier = DMEM test E91 (0x0B75).**

---

## 0. The exact problem (precisely characterized — do not re-derive)

The firmware multiplier test (`0x0942`) single-steps the ARU with 20 (operand `F`, coeff magnitude
`cmag`, coeff sign `csign`) tuples and compares the read-back result to a ROM golden table. The
**20 goldens** (`F` signed 16-bit; `csign`: 1=positive, 0=negate; `exp` signed 16-bit):

```
F        cmag csign exp        F        cmag csign exp
0x5555   21   0    -14337      0x5555   42   0    -28673
0xAAAA   21   0     14335      0xAAAA   42   0     28671
0x6666   21   0    -17204      0x6666   42   0    -32768  (sat)
0x9999   21   0     17202      0x9999   42   0     32767  (sat)
0x5555   21   1     14336      0x5555   42   1     28672
0xAAAA   21   1    -14336      0xAAAA   42   1    -28672
0x6666   21   1     17203      0x6666   42   1     32767  (sat)
0x9999   21   1    -17203      0x9999   42   1    -32768  (sat)
                                ── the 4 cmag=63 (all-ones) cases, all csign=1 ──
0x3333   63   1     25806   (faithful model gives 25804, off +2)
0xCCCC   63   1    -25805   (faithful gives -25806, off +1)
0x3FFF   63   1     32255   (faithful gives 32254, off +1)
0xC000   63   1    -32254   (faithful gives -32256, off +2)
```

`multiply_faithful()` in `tools/aru_booth.py` reproduces the first 16 **bit-exact** from the gate
wiring; the cmag=63 four are short by +1..+2 LSB (in the *positive* direction for both operand
signs).

## 1. What is RIGOROUSLY ruled out (re-confirm with `tools/aru_booth.py` if you doubt it)

- **NOT the front-end.** `comb_array()` (literal NAND array §4F.4/4F.5 + 5×74F283 carry chain
  §4F.7 + Σ→PR §4.7) reproduces the per-rail products (M0 rail = operand×4, M1 rail = operand×8)
  **and** the combined dual-rail product (`M0pp+M1pp = F×12` per phase for cmag=63) **exactly**.
  The 3 SR→NAND tap errors (`aru_U40.pin1` SR3→SR5, `aru_U26.pin12` SR8→SR10, `aru_U51.pin4`
  SR12→SR14) were **owner-verified against schematic 060-01318 and corrected**; the §4.7/§4.6
  within-nibble reversal **cancels** (use the straight net Σ→PR). All SR taps, carry-in pins, and
  `aru_U24` Cout (n/c) are owner-verified.
- **NOT a back-end carry.** A gate-literal back-end (subtract-XOR `aru_U5–9` + adder chain
  `aru_U19–23` with **carry-in = CSIGN/** [confirmed by the owner `aru_U2` pin5↔pin10 tie] +
  sat-mux `aru_U33–37` + accumulator `aru_U45–49`) reproduces `Σmag` exactly.
- **NOT truncation/rounding.** ★ DECISIVE TEST ★ — even **infinite-precision `round(F·cmag/32)`**
  is +1..+2 LSB BELOW every cmag=63 golden, while cmag=21,42 are exact. So the hardware genuinely
  computes ~1.6 LSB *more* than `F·63/32` for the all-ones coefficient (effective coeff ≈ 63.004).
- **REFUTED guesses (do not revisit):** (a) "missing M1 two's-complement hot-one" — separate-rail
  accumulation == combined-array, **bit-identical**. (b) "Booth/carry-save sign-extension
  correction" — named the *mechanism class* without ever finding a gate; no net located. (c) The
  CSIGN/ and ARUCKE/ **bias circuits** (220R/330R dividers; ARUCKE/→`aru_U42.5` is just the
  ARUCK-generator XOR) are **analog level / clock-edge** details with **no arithmetic effect** and
  are **coefficient-independent**, so they cannot cause a cmag-63-only residual.
- **CONFIRMED-faithful facts the gate-literal back-end pinned (preserve these):** the **result
  register ROUNDS (round-half-up) at the ≫3**, NOT truncates (the gate-literal accumulator for
  `0x5555×21` = 114686; firmware result 14336 = `round(114686/8)`, floor would be 14335). The
  **sign is applied as two's-complement (`−M−1`) at the OUTPUT**, NOT by accumulating `−Σmag`.

## 2. The leading hypothesis (what to test)

The residual is **operand-dependent**, **only on cmag=63 (both Booth rails fire every phase)**, and
**not in any combinational stage**. That signature points to a **timing / register-state effect
across the consecutive single-steps of the test** — i.e. the **deferred MAC pipeline** (Service-
Manual fig 3.4: a multiply spans ~3 microinstructions; the result is available "one AS behind"),
where the product/accumulator/result registers carry state between `OUT 0x03` strobes.

★ **Critical clue — XFER is 0 for the multiplier-test microwords.** Decode: l3=0x01 → `~l3`=0xFE →
`XFER = ~l3 bit0 = 0`; l3=0x55 → `~`=0xAA → XFER=0; l3=0xA9 → `~`=0x56 → XFER=0. So during the
*entire* multiplier test the microword's XFER bit is **0**, meaning the result register is **not**
loaded by the normal `XFER CK` path. Yet the firmware reads a meaningful product back. **So the
single-step read-back path is non-obvious** — it must either (a) the diagnostic single-step strobe
asserts `XFER CK`/`RDRREG/` itself, or (b) the read-back reads the accumulator/sat-mux output
directly, or (c) it reads a register holding a *previous* step's value (pipeline latency). The
current `tools/aru_post.py` sidesteps this by computing `RES` fresh and returning it on IN 0x06/07
(works for 16/20); the cycle-accurate model must get the *real* path right — that is most likely
where the cmag=63 +2 hides (e.g. pipeline cross-talk between consecutive operands on the value-
dense all-ones case).

**Possible outcomes (all acceptable as "done"):** (1) the cycle-accurate model reproduces all 20
faithfully → cmag=63 explained, drop the fudge. (2) it still gives 25804 for cmag=63 → the residual
is NOT pipeline/state; re-localize (single-step readback wiring on 060-02475/01318, or a genuine
sub-LSB hardware quirk) and document. Either way, **report the exact mechanism, with evidence.**

## 3. The method — cycle-accurate co-simulation

Build on `tools/aru_post.py` (the POST harness already wiring a stateful ARU into the verified 8080
via `tools/boot8080.py`). Replace the ARU's `single_step()` (currently a one-shot per-value
multiply) with a **cycle-accurate microinstruction engine** that, on each `OUT 0x03` strobe, runs
the full MS0–MS8 / AS0–AS2 sequence with **stateful** registers that **persist across strobes**:

- **Clock/state gen (from fig 3.2 + §6T):** MS = 9-state one-hot ring, 1 step per MC tick; ARUCKE
  = registered `OR(MS2,MS5,MS8)` (`tc_U25` FF2); **ARUCK rises at MS0/MS3/MS6** (3 pulses/micro-
  instruction, one per AS phase); AS-gen `tc_U23` (clk ARUCK, async-clr MS4) → AS0, AS1/, AS-seq;
  S0/S1 (74194 mode) from `tc_U24` (clk = `tc_U23.Q1`) + `tc_U38` — but **fig 3.4 already gives the
  resulting schedule**: LOAD@AS2(prev), SHIFT-RIGHT@AS0 & AS1.
- **Stateful ARU datapath (the point of this exercise):**
  - **74194 shifter** (clk ARUCK): LOAD `F<<3` then shift-right-by-2 each ARUCK → operand `F·2⁰`,
    `F·2⁻²`, `F·2⁻⁴` (use `aru_booth.load_SR` / `shift_right2`).
  - **74195 serializer** (clk ARUCKE, SH/LD=AS1/): M0 = C4,C2,C0; M1 = C5,C3,C1 across the 3 phases.
  - **Front-end** `comb_array(SR,M0,M1)` each ARUCK → **product register** (`aru_U10/11/12`, clk
    ARUCK) — STATEFUL (holds last value between strobes).
  - **Back-end:** subtract-XOR(`CSIGN/`) → adder(`carry-in=CSIGN/`) → sat-mux → **accumulator**
    (`aru_U45–49`, clk ARUCKE/, **async/sync clear by ZERO/**) — STATEFUL.
  - **Result register** (`aru_U43/44`, clk `XFER CK`, OE `RDRREG/`) — STATEFUL; capture PP3..18.
  - `XFER CK = tc_U36 = NAND(AS0, XFER, …)`; `ZERO/ = tc_U48 = NAND(MI25-gate, AS0)`. **Resolve how
    the single-step read-back actually obtains the product given XFER=0 in the microword** (§2 clue).
- **Drive it with the REAL firmware test.** Do NOT feed isolated values — run the actual POST
  `0x0942` routine on the 8080 (it patches l2@`0x41FA`/l3@`0x41FB`, loads via OUT 0x06/0x07,
  strobes OUT 0x03, reads IN 0x06/0x07, compares to the ROM golden at `0x09E5`). The consecutive
  operands + the carried register state are exactly what a per-value model omits.

## 4. Tools, files, and firmware addresses

- `tools/aru_post.py` — POST harness: `ARU` class + `run_post()` (boots `boot8080`, POST
  un-suppressed, reports per-subtest PASS/FAIL). **Extend `ARU.single_step` into the cycle-accurate
  engine here.** Ports: OUT 0x07=hi / 0x06=lo (input latch), OUT 0x03=single-step strobe, IN 0x07/
  0x06=result read-back, IN 0x02=latch echo; scratch l2=`0x41FA`, l3=`0x41FB`, offset/static
  `0x41FC–0x41FF`.
- `tools/aru_booth.py` — `comb_array`, `load_SR`, `shift_right2`, `multiply_faithful` (16/20, gate-
  literal, NO fudge — the reference), `multiply` (20/20 with the flagged `+3·dual` fudge to retire),
  `GOLDENS` (the 20 tuples), `selftest()`.
- `tools/boot8080.py` — the verified-8080 faithful boot (`I8080Machine`, passes 8080exm). USE THIS.
  RETIRED: `tools/z80emu.py` (8080 parity bug).
- `tools/dis224.py` — disassembler (`python tools/dis224.py <start_hex> <end_hex>`). The test
  routine: entry `0x0942`; single-step driver subroutine `0x099A`; ROM golden table `0x09E5`; input
  tables `0x09D5`/`0x09DD`; per-test WCS scratch image table `0x0A0D` (written to `0x41F0–0x41FF`,
  giving phase-1 leftover l2=0x7E/l3=0xA9). POST master sequence `0x08F0–0x0930`; ARU re-init
  `0x02AD` runs before each sub-test.
- `docs/reference/224/224XL_interconnect_netlist.md` — **§4** (back-end PP/accumulator), **§4F**
  (multiplier front-end), **§4F.9** (the multiply operation + the cmag=63 finding), **§3** (WCS /
  field decode / **§3.9 serializer** / **§3.10 CSIGN JK**), **§2T** (device decode incl. XFER/ZERO/
  RDRREG gen), **§6T** (clock/state/strobe gen — MS/AS/ARUCK/ARUCKE/XFER CK/ZERO/), **§G3R** (MI
  field map).
- `docs/reference/224/224XL_timing_spec.md` — **fig 3.2** (clock skeleton: MS/AS/ARUCK grid) and
  **★ fig 3.4 (ARU MAC deferred pipeline — THE key)**; single source `tools/timing/timing_spec.json`.
- Raw owner pinouts (ground truth for wiring; do NOT re-derive from memory): `224XL ARU pinouts
  from 060-01318.txt`, `224XL TC pinouts from 060-02475-D.txt`, `224X_DMEM_pinouts_from_060-02512.txt`.
- Memory: `224xl-holistic-m0-progress.md` (full Phase-1 record), `224xl-pinout-audit.md` /
  `224xl-schematic-autoread-unreliable.md` (never use memory pinouts; never auto-tile-read).

## 5. Success criteria

1. The cycle-accurate co-sim reproduces **all 20 firmware multiplier goldens bit-exact with NO
   calibrated fudge** (retire `+3·dual`), with the mechanism for the cmag=63 +1..+2 LSB explained
   and tied to specific register/timing behavior (e.g. pipeline latency, the XFER=0 read-back path,
   cross-step state) — **or** —
2. it definitively shows the cmag=63 residual is **not** a pipeline/state effect (cycle-accurate
   still yields 25804), in which case re-localize (the single-step read-back wiring, or a genuine
   sub-LSB quirk) and document precisely.
3. **Regression:** cmag=21/42 and unity must stay exact; the full POST (latch E32 + register E40 +
   multiplier E83) must still pass un-suppressed on the verified 8080.

## 6. Ground rules (why the project survived)

- **The firmware goldens are the only oracle.** "Looks right / passes with a fudge" is not solved.
  No new calibrated constants — the whole point is to *derive* cmag=63, not fit it.
- **Verify bottom-up; the netlist is ground truth for wiring.** Don't re-derive ARU/T&C pinouts
  from memory; read the netlist / the owner raw txts. Owner-confirmed: the 3 SR taps, the carry-in
  topology, `aru_U24` Cout n/c, the bias circuits.
- **Build on the verified 8080** (`boot8080`/`I8080Machine`), not `z80emu`.
- If you suspect a *new* schematic transcription error, flag the exact pin(s) for the owner to
  triple-check (this is how the 3 SR-tap errors were caught — it works).
- Keep `multiply_faithful()` as the no-fudge reference throughout; compare against it.

**One-line orientation:** the gate-level *combinational* multiplier is solved (16/20 from verified
wiring; cmag=21/42 + unity exact, result-reg rounds, sign at output). The cmag=63 +1..+2 LSB is a
proven, operand-dependent, all-ones-only residual that lives in the *sequential* behavior (the
deferred MAC pipeline / single-step read-back register state, XFER=0 clue) — build the cycle-
accurate POST single-step co-sim to nail it.
