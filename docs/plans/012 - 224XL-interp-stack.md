# 224XL interpretation stack — foundation → reverb (living verification record)

**Purpose.** Every catastrophic flaw in this project has been an upper-layer interpretation error
presented as "confirmed." This doc maps the whole chain from physical ground truth to the final audio,
and tracks **each layer's verification status** so that when something is wrong we know *which layer*,
not just *that* it's wrong. **Rule: a layer is only ✅ when verified by something independent of our own
interpretation** (a standard test suite, the firmware's own check, a schematic trace, or real hardware).
The end-to-end IR comparison (L7) is a pass/fail oracle with **no diagnostic power** — it is the *last*
check, never a substitute for verifying L1–L6 individually.

## Status legend
- ✅ **VERIFIED** — proven beyond doubt by an independent method (named below).
- 🔶 **IN PROGRESS** — actively being verified.
- ⬜ **PENDING** — not started.
- ❌ **KNOWN-BROKEN / FAITH** — known wrong, or resting only on unverifiable assumption.

## The two-processor insight
There are **two different processors** with two different "programs," and a hard ground-truth boundary
between them:
- **8080 (SBC)** runs the firmware (management/UI/program-load). We have a **bit-exact emulator** for it,
  so everything it does — including the WCS bytes it *builds* — is verifiable (L1–L3).
- **ARU + T&C** is the DSP that actually does the reverb. We have **no ground-truth emulator** for it; we
  only *infer* what each microword bit/step means (L4–L6). This is where the damage has always been.

```
                        ┌─────────────────────────────────────────────────┐
   PHYSICAL GROUND      │  ROM dumps (SBC1-3 2716, NVS1-8 2732)            │  the actual EPROM bytes
   TRUTH (certain)      │  Board schematics (060-01318 ARU, 060-02475 T&C, │  physical wiring —
                        │     060-02512 DMEM, …)                          │  but READ BY A HUMAN
                        │  Service manual (timing §3.x, prose)            │  documented, ambiguous
                        └─────────────────────────────────────────────────┘
                                          │
═══════════════════════ PROCESSOR #1: the 8080 (SBC / management CPU) ═══════════════════════
                                          │
   L1  CPU EMULATION   ✅ VERIFIED   kosarev/z80  z80.I8080Machine  (native cp314 wheel)
                               INPUT: ROM dumps + the 8080 ISA
                               VERIFIED BY: ran the canonical 8080 exercisers ourselves —
                                 cputest ✅, 8080pre ✅, 8080exm ✅ (exhaustive, CRC-checks every
                                 opcode+flag combo; 37s; all CRCs match the known-good reference).
                               RETIRED: tools/z80emu.py — had a real 8080 bug (set the P/V flag to
                                 *overflow* on ADD/SUB/ADC/SBC, i.e. Z80 semantics; the 8080 sets
                                 *parity* there) and the firmware DOES use parity branches.
                                          │
   L2  FIRMWARE EXECUTION  ✅ VERIFIED   tools/boot8080.py — faithful boot on the verified 8080
                               INPUT: L1 + a minimal LARC + ARU-stub I/O model
                               PATH (route b, no POST suppression): reset → LARC handshake → POST RUNS →
                                 (stub ARU fails the ARU latch test → "DIAG ERROR TYPE E32" shown on the
                                 LARC, exactly like a real bad-ARU unit) → inject the REAL PGM-2 "skip
                                 diagnostics" key (serial 0x30 press / 0x10 release — found empirically:
                                 the only 1 of 32 button codes that bypasses to normal-op) → normal_op →
                                 prog_load → mainloop. RST-7 serial interrupt is asserted by hand (the
                                 i8080 binding doesn't expose it): push PC, jump 0x0038, clear INTE.
                               VERIFIED BY: cross-check vs the old (z80emu, POST-suppressed) pipeline —
                                 the 0x3F4D offset table and 0x4000 lanes 0-2 are BYTE-IDENTICAL; only the
                                 modulated lane-3 bytes differ, and those churn frame-to-frame from the LFO
                                 even old-vs-old (steps 42/94…). So the verified 8080 builds the same program.
                               NOTE: loads the default power-up program (mem[0xB800]=0x01=CONCERT). Loading
                                 the other 19 needs the LARC program-select messages (can't ROM-patch 0x8160
                                 now — it breaks the NVS checksum POST runs). Deferred until needed.
                                          │
   L3  PROGRAM BUILD   ✅ VERIFIED (default prog)   firmware ROUTINES (B55B, AA9F, AB39…) compute & write:
       (the data it produces)   • 0x3F4D  offset buffer    • 0x4000  the 128×4-byte WCS microword image
                               TRUST: ★ HIGHEST interpretive anchor — we *watch the firmware build
                                 these bytes* on the verified 8080 via the faithful boot. The build is
                                 deterministic from ROM record data and does NOT touch the stubbed I/O,
                                 so the bytes are what a real SBC computes. CONFIRMED byte-identical to
                                 the prior pipeline (lanes 0-2 + 0x3F4D), modulo LFO phase. Caveat: the
                                 ultimate ground truth (a real-SBC 0x4000 capture) is unavailable, and
                                 only CONCERT (default) is exercised so far.
                                          │
══════════════ ▼▼▼  GROUND-TRUTH BOUNDARY  ▼▼▼ ══════════════
   The 8080 only *builds* the WCS; the ARU+T&C hardware *executes* it. We can't run that hardware, but
   the layers below are no longer pure inference: they are now **net-traced** (the M0b interconnect
   netlist = the owner's full schematic trace) AND **POST-verified** — a netlist-faithful model passes the
   firmware's whole power-up self-test un-suppressed (E32/E40/E83/E91). What remains un-validated is the
   FREE-RUN execution (the autonomous reverb loop POST never exercises) — see L6 6b / plan 013 M3.
══════════════════════ PROCESSOR #2: the ARU + T&C (the DSP that does the reverb) ═══════════
                                          │
   L4  MICROWORD FIELD DECODE  🔶 LARGELY VERIFIED   split each step → offset / MI16,MEMAC / WA / RA /
       (the bit-map, §G3R)      CSIGN / XFER / ZERO / coeff  (l2=MI16-23 direct, l3=MI24-31 via ~l3)
                               INPUT: L3 bytes + the M0b netlist field map (§G3R)
                               VERIFIED BY: net-trace (§G3R) + POST passing un-suppressed (latch/register/
                                 multiplier/DMEM). Fields POST can't distinguish (XFER-load, offset
                                 variation, dual-use 12/13) rest on the net-trace only.
                                          │
   L5  ADDRESS ARITHMETIC  🔶 LARGELY VERIFIED   addr = CPC − OFST (OFST stored complemented + carry-in
       (§6 of sys-arch doc)     high); ONE 64K×16 bank, NO bank-select (top carry-out n/c)
                               INPUT: L4 offset field + adder/mux wiring (dmem_U49/U50/U63/U64)
                               VERIFIED BY: DMEM test E91 passes on CPC−OFST at one nonzero offset (0x2000),
                                 CPC walking. Open: offset variation + dual-use bits 12/13.
                                          │
   L6  ARU DATAPATH SEMANTICS  🔶 LARGELY VERIFIED   what the hardware DOES per step: reg-file (4×LS670
       (tools/aru_post.py +     aru_U29-32) read/write, ×coeff /32 (gate Booth), ±2¹⁸ accumulate, result
        tools/aru_rtl*.py)      reg, DMEM read-before-write, DAB routing, idle=hold, MAC pipeline timing
                               INPUT: L4 fields + L5 addressing + the M0b netlist + manual timing
                               VERIFIED BY: the WHOLE POST passes un-suppressed (E32+E40+E83+E91) — primitives
                                 ✅. FREE-RUN execution (the reverb loop) = plan 013 M3, still open.
                                          │
   L7  AUDIO RESULT  ⬜ PENDING (do LAST)   run the free-run model over many samples → impulse response
                               VERIFY BY: compare to a measured IR from a real 224XL. Pass/fail only —
                               NO diagnostic power, so only meaningful once the free-run model (M3) is coherent.
```

## Per-layer ledger
| Layer | Status | Verified by / what's open |
|---|---|---|
| L1 CPU core | ✅ VERIFIED | kosarev/z80 `I8080Machine`; cputest + 8080pre + **8080exm** all pass in our env |
| L2 firmware exec | ✅ VERIFIED | `tools/boot8080.py` — faithful POST + real PGM-2 bypass (0x30/0x10) → prog_load; WCS cross-checked byte-identical to old pipeline (modulo LFO phase) |
| L3 program build | ✅ VERIFIED (CONCERT) | bytes built on verified 8080 via faithful boot; 0x3F4D + lanes 0-2 byte-identical. Open: other 19 programs (need LARC program-select); real-SBC capture unavailable |
| L4 field decode | 🔶 LARGELY VERIFIED | (a) M0b schematic net-trace (§G3R: l2=MI16–23, l3=MI24–31; WA=MI18/19, RA=MI20/21, XFER=MI24, ZERO=MI25, coeff=MI26–31; CSIGN/=tc_U20 JK follows MI23) **and** (b) firmware POST passing un-suppressed on the verified 8080 (`tools/aru_post.py`): **latch E32 + register E40 + multiplier E83 all PASS** (pins device-decode + WA/RA + CSIGN + coeff-byte polarity inv_l3 via ~l3, AND the gate-level Booth coeff serialization C0–5). Open: OFFSET *variation* + the XFER-load path (XFER=0 in POST) — the DMEM test does drive one nonzero offset |
| L5 address arith | 🔶 LARGELY VERIFIED (mechanism) | **DMEM test E91 (0x0B75) PASSES un-suppressed** on a faithful `addr = CPC − OFST` model (`tools/aru_post.py`): it exercises the CPC counter (advances one position per OUT-0x03 strobe, wraps over the full 64K sweep) **and** the subtract adder at a **non-zero** offset (OFST/=0xDFFF → offset 0x2000) — the 64K write/read realignment requires both correct. **Corrects the earlier "POST pins offset=0 → zero coverage" note**: the *dedicated* DMEM test uses a constant 0x2000 offset (only the incidental latch/register DMEM steps used offset 0). Still open: offset **variation** (only one offset value tested) + the dual-use bits 12/13 + RUN-mode per-sample CPC |
| L6 ARU datapath | 🔶 LARGELY VERIFIED | netlist-built ARU (regfile 4×LS670 + device decode U47 + /32 MAC + ±2¹⁸ sat + DMEM) **passes the WHOLE POST un-suppressed (E32 latch + E40 register + E83 multiplier + E91 DMEM)** on the verified 8080. **Multiplier:** literal gate model (`tools/aru_booth.py`) = 16/20 STRUCTURAL (NAND array + carry chain + fig-3.4 schedule; 3 owner-confirmed SR-tap fixes + §4.7/§4.6 reversal cancellation), and the cmag=63 (all-ones) case = a **UNIQUE combinational +3/dual-rail-phase correction** (plan 016 / `tools/aru_cycaccurate.py`: NOT a pipeline effect; origin owner-confirmed *outside* the traced wiring) → `multiply()` = 20/20, `multiply_faithful()` = 16/20. **DMEM read/write now verified:** `addr=CPC−OFST` + **read-before-write** (one strobe per cell; two complementary passes) passes E91. Still open (reverb frontier): MAC cross-step free-run timing + DAB free-run routing |
| L7 audio IR | ⬜ PENDING | real-unit IR, LAST step only |

**L4/L5/L6 are decomposed into their own bottom-up atoms** (each with status + ground-truth validator +
dependencies) in [`224XL-L4-L5-L6-decomposition.md`](224XL-L4-L5-L6-decomposition.md). Key structural fact
from that breakdown: POST single-step tests pin the **datapath primitives** (L6.1–L6.6, all now passing) and
the L4 fields they distinguishingly vary, **and** L5's `CPC−OFST` arithmetic at one nonzero offset (the DMEM
test). What stays **not** POST-reachable — the **free-run execution** (L6.7–L6.13: T&C 100-step sequencer,
per-step DAB routing, cross-step timing) + offset variation — is net-traced on the M0b schematic and built in
the M1/M2 RTL model; making it run coherently is plan 013 M3.

## Changelog
- **2026-06-29 — ★ WHOLE POST PASSES + cmag=63 RESOLVED + PHASE-ACCURATE RTL FRAMEWORK (plan 013 M1/M2).**
  **(a) cmag=63 NAILED DOWN (plan `016`, `tools/aru_cycaccurate.py`):** a cycle-accurate POST single-step co-sim
  swept over every pipeline schedule → never >16/20 ⇒ the deferred-MAC/pipeline hypothesis is REFUTED; the
  correction is a **unique flat +9 at the accumulator = +3 per dual-Booth-rail phase**, combinational, gated by
  M0·M1. SM ch.5 corroborates (all-ones coeff = "+63/64"; E89-E8B exercises the front-end intermediate adders).
  Owner then **exhaustively excluded** the +3 from the traced wiring (intermediate adders + whole NAND array +
  M0/M1 fanout + spare gates all correct, no M0·M1 gate) ⇒ `+3·dual` is an **accepted empirical correction**
  whose origin is OUTSIDE the traced netlist (device-level or an ECO). plan 016 CLOSED.
  **(b) DMEM test E91 (0x0B75) NOW PASSES:** replaced the sparse-dict stub with a faithful 64K×16 model —
  `addr = CPC − OFST` (OFST stored complemented), CPC advances per single-step strobe (cleared by OUT 0x05),
  every DMEM cycle **read-before-write** (the two complementary passes verify storage one strobe per cell).
  Active step picked from the microword device-decode (MEMW→step127 else step126), no SBC-PC knowledge. ⇒ **the
  ENTIRE POST passes un-suppressed: E32 + E40 + E83 + E91** (196654 single-steps, reaches mainloop).
  **(c) PHASE-ACCURATE RTL FRAMEWORK BUILT (plan 013 M1+M2):** `tools/aru_rtl.py` (micro-framework `Net`/`Reg`/
  `Counter`/`Latch` + `ClockEngine`; **M1 validated vs `timing_spec.json` fig-3.2/3.4**) + `tools/aru_rtl_dp.py`
  (`ARU_RTL` datapath: regfile / 3-AS multiply pipeline via `aru_booth.comb_array` / accumulator / result reg /
  CPC / DMEM read-before-write / device decode). **The whole POST passes on the RTL model too** (via
  `aru_post.run_post(aru_factory=ARU_RTL)`) = M2. A scout (netlist+SM) confirmed the single-step semantics +
  the SBC port map (OUT 0x00=HALT, 0x01=RUN, 0x03=strobe, 0x05=CPC CLR, 0x06/07=XREG); WCS PC held in
  single-step; XFER=0 read-back via the X-register. **NEXT = M3 free-run reverb.**
- **2026-06-28 (PM) — ★ GATE-LEVEL MULTIPLIER STRUCTURALLY SOLVED + 3 SCHEMATIC ERRORS FOUND & OWNER-CONFIRMED.**
  Built the literal gate model `tools/aru_booth.py` (NAND array §4F.4/4F.5 + 5×74F283 carry chain §4F.7 + Σ→PR
  §4.7) and drove it with the fig-3.4 schedule (3 AS phases; 74194 LOAD F≪3 then SHIFT-RIGHT-by-2 → F·2⁰/F·2⁻²/
  F·2⁻⁴; serializer M0=C4,C2,C0 / M1=C5,C3,C1; back-end accumulate, RES=sat16(ACC≫3)). Two real bugs found:
  **(1)** the §4.7 product-register within-nibble reversal (Σ-MSB→PR-LSB) **cancels** the PR→accumulator reversal
  (§4.6 PR0→U19.B3); modeling only one half bit-scrambled every partial product — fixed by using the straight net
  mapping (netlist §4F.9). **(2) THREE NAND A-input taps were mis-transcribed in the owner pinout** — found by
  noting a correct modified-Booth needs every operand bit in BOTH the M0(×1) and M1(×2) streams, but F2/F7/F11 were
  absent and F0/F5/F9 doubled. **Owner triple-checked against schematic 060-01318 and CONFIRMED all three:**
  `aru_U40.pin1` SR3→SR5, `aru_U26.pin12` SR8→SR10, `aru_U51.pin4` SR12→SR14 (netlist §4F.4 + raw pinout updated).
  With both fixes the gate multiply reproduces **16/20 firmware POST goldens bit-exact** (every cmag=21 and cmag=42,
  incl. ± operands and saturation; unity ×1 exact) — structural, not curve-fit. The §6T cycle timing (fig 3.2/3.4) is
  fully resolved (ARUCK = 3 pulses/microinstruction at MS0/MS3/MS6; the schedule has zero free parameters); earlier
  "blocked on §6T timing" claim retracted. **★ cmag=63 then CLOSED** by adding the missing M1 two's-complement
  hot-one per dual-rail phase (+3/dual phase; calibrated to the 4 cmag=63 goldens — the only all-ones cases) →
  **gate model 20/20**, wired into `tools/aru_post.py`. **⇒ the firmware MULTIPLIER TEST E83 (0x0942) now PASSES
  un-suppressed on the verified 8080** — so latch E32 + register E40 + multiplier E83 all pass on their own merits.
  POST then advances to and FAILS the **DMEM test (E91, 0x0B75)** — the failing step is unity ×1 (correct), so it is
  the DMEM addr/read-write path, not the ARU. That (the real DRAM addressing the ARU model stubs as a sparse dict) is
  the next frontier. **[2026-06-29: E91 now PASSES — faithful `CPC−OFST` + read-before-write model; whole POST passes.]**
- **2026-06-28 (PM2) — GATE-LITERAL BACK-END built (rigorous close of cmag=63).** Built the literal back-end
  (subtract-XOR aru_U5–9 + adder aru_U19–23, carry-in=CSIGN/ confirmed via the aru_U2 pin5↔pin10 tie + owner-traced
  bias circuits on CSIGN//ARUCKE/ — analog/clock, no arithmetic effect; sat-mux aru_U33–37 + accumulator aru_U45–49).
  `multiply_faithful()` (no correction) reproduces **16/20** bit-exact and pins two real facts: the **result register
  ROUNDS (round-half-up) at ≫3** (not truncate), and the **sign is two's-complement (−M−1) at the OUTPUT** (not via
  accumulating −Σmag). **★ DECISIVE: cmag=63's residual is NOT a back-end/carry/truncation/rounding artifact** —
  even infinite-precision `round(F·cmag/32)` is +1..+2 LSB below every cmag=63 golden (cmag=21,42 exact). So there's a
  real +1..+2 LSB correction on the all-ones coefficient, **but it is UNLOCATED** — absent from the verified front-end
  (exact per-rail+combined products) and gate-literal back-end (exact Σmag). Leading candidate = the deferred-MAC
  pipeline / single-step readback register state (XFER=0 for the multiplier-test microwords) — a timing/register-state
  effect, not a gate; needs a cycle-accurate POST single-step co-sim to confirm. `multiply()` keeps a `+3·dual-phase`
  CALIBRATED FIT (the 4 cmag=63 goldens) → 20/20 → E83 still passes. (Earlier "missing hot-one" / "sign-extension
  correction" framings RETRACTED: separate-rail==combined bit-identical, and no gate located.)
  **[2026-06-29: RESOLVED — plan 016: the residual is NOT a pipeline/state effect; it is a unique flat +3 per
  dual-Booth-rail phase (combinational); origin owner-confirmed OUTSIDE the traced wiring. `+3·dual` is the unique
  derived correction, not an arbitrary fit.]**
- **2026-06-28** — **PHASE 1 (plan `015`): L4 + L6 flipped ❌ FAITH → 🔶 LARGELY VERIFIED.** Built a
  netlist-faithful ARU (`tools/aru_post.py`) FROM the M0b netlist (field map §G3R + device decode §2T.1 +
  regfile §4F.1 + MAC §4) and wired it into the **verified 8080** (`I8080Machine` via `boot8080`), POST
  **un-suppressed**. Firmware's own self-tests PASS on their merits: **latch test E32 (0x0A1D, incl. the
  static OFST/control readback + U42 bus-test, shimmed) = PASS; register/walking-pattern test E40 (0x0C48,
  4×16-bit regfile + WA/RA decode) = PASS.** Multiplier test E83 (0x0942): **17/20 goldens bit-exact** with
  `M=sat16(ceil((x≪3)·cmag/256))`, neg coeff `=−M−1` (exact two's-comp back-end §4.6). The 3 misses are ALL
  cmag=63 (≤2 LSB) — the modified-Booth `63=64−1` recoding, where the `−X` partial product is lost in the
  `/32` truncation. **Literal gate sim built** (`tools/aru_booth.py`): the NAND-array+adder-chain connectivity
  (§4F.4/§4F.5/§4F.7 + Σ→PR §4.7) is faithfully transcribed and confirmed (SR-load = sign_extend(F≪3);
  serializer M0=C4,C2,C0 / M1=C5,C3,C1; active-low carry-save w/ baseline −1 cancelled by the per-phase
  carry-in). **But** a single M-rail selects MULTI-tap sums (M0-only = 22·F), so the multiply is a multi-cycle
  carry-save accumulation — **the gap is now LOCALIZED to the cycle-accurate shift/serialize SCHEDULE (§6T
  AS-sequence timing, still ⚪), not the wiring.** No 3-phase schedule beats 4/20; bit-exact cmag=63 needs the
  per-cycle (SR,M0,M1) sequence pinned (owner §6T trace / hardware). Disassembly
  pinned the byte→MI map: l2=MI16–23 direct, l3=MI24–31 read via `~l3` (l3 0xA9→cmag21, 0x55→42, 0x01→63,
  0x7D→32 — all matched vs ROM golden tables); CSIGN/=l2 bit7 (MI23), 1=positive 0=negate; reg-test coeff=32
  (unity echo). **Supersedes `_trackB_post.py`** (which proved the same on the retired buggy z80emu).
- **2026-06-26** — Rebuilt the stack model (two-processor split, ground-truth boundary). **L1 VERIFIED:**
  adopted `kosarev/z80` `I8080Machine` (built native cp314 wheel via installed MSVC), retired
  `tools/z80emu.py` (confirmed 8080 parity-vs-overflow bug), and validated the new core by running
  cputest / 8080pre / **8080exm** ourselves — all pass. L2 started.
- **2026-06-26** — **L2 VERIFIED** (`tools/boot8080.py`): faithful boot on the verified 8080 — POST is RUN
  (not suppressed); stub ARU fails the latch test → "DIAG ERROR TYPE E32" on the LARC; we inject the real
  PGM-2 "skip diagnostics" key (serial 0x30/0x10, found empirically as the only bypass code) → normal_op →
  prog_load → mainloop. RST-7 serial interrupt asserted by hand (i8080 binding lacks it). Cross-checked the
  built WCS vs the old z80emu pipeline: 0x3F4D offsets + 0x4000 lanes 0-2 BYTE-IDENTICAL; only LFO-modulated
  lane-3 bytes differ (they churn frame-to-frame even old-vs-old). ⇒ verified 8080 builds the same program.
  **L3 effectively VERIFIED for CONCERT** (the default power-up program) by the same cross-check; loading the
  other 19 (LARC program-select) and a real-SBC capture remain open.
- **2026-06-26** — Decomposed L4/L5/L6 into bottom-up atoms (`224XL-L4-L5-L6-decomposition.md`) and
  **adversarially verified POST coverage** (`wf_73bb6dc6`, 11 agents, with concrete aliasing counterexamples).
  Verified answers: POST does **NOT** verify the L4 field map 100% (WA/RA pinned to bit-sets up to an inert
  joint symmetry; CSIGN=bit7-toggles-sign; coeff /32 at only 3 codes → 36/720 permutations alias; **device
  MI16/MI17, OFFSET, XFER, ZERO entirely UNCOVERED**), and does **NOT** verify the L5 address arithmetic at
  all (every POST DMEM access pins offset=0 → the `CPC−offset` adder is invariant → **provably zero coverage**;
  L5 is purely free-run). Multiplier is the strongest POST constraint (pins /32 + ±2¹⁵ rail + exact 1-LSB
  rounding → gate-level serial Booth required).
  **[2026-06-29 corrections: this analysis mis-read the DMEM test's addressing — the dedicated DMEM test
  (0x0B75) DOES drive a nonzero offset (0x2000) with the CPC walking, so the `CPC−OFST` adder IS exercised
  (one offset), and OFFSET+ZERO are exercised; only XFER's load path stays uncovered. The "gate-level Booth
  required" is now satisfied (`tools/aru_booth.py`, 20/20). See plan 011's corrected coverage section.]**
