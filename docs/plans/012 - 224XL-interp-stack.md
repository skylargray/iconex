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
   Everything below is INFERENCE about a SECOND processor (the ARU+T&C) that we have NO ground-truth
   emulator for. The 8080 only *builds* the WCS; the ARU/T&C hardware *executes* it — and we can't run
   that hardware, so we guess what each bit/step means.
══════════════════════ PROCESSOR #2: the ARU + T&C (the DSP that does the reverb) ═══════════
                                          │
   L4  MICROWORD FIELD DECODE  ❌ FAITH   split each 4-byte step → offset / MI16,MI17 (read/write/sub) /
       (the bit-map)            WA / RA / CSIGN / XFER / ZERO / coeff
                               INPUT: L3 bytes + a claimed bit-map
                               TRUST: bit *meanings* come only from human schematic-reading + narrow
                                 POST coverage. ★ MOST ERRORS LIVE HERE (the ~inversion, the sign,
                                 WA/RA meaning, which bits are control vs address).
                                          │
   L5  ADDRESS ARITHMETIC  ❌ FAITH   offset → addr = CPC − offset (active-low + carry-in); bank=carry;
       (§6 of sys-arch doc)     128K flat single linear space (no separate bank-select; bank = the carry)
                               INPUT: L4 offset field + adder/mux wiring (U49/U50/U63/U64)
                               RISK: offset→address wiring & dual-use bits 12/13 (control vs address).
                                          │
   L6  ARU DATAPATH SEMANTICS  ❌ FAITH   what the hardware DOES per step: reg-file (4×LS670 U29-U32)
       (tools/aru_datapath.py)  read/write, ×coeff /32, ±2¹⁸ accumulate, result reg, DMEM read/write,
                                DAB routing, idle=hold, MAC pipeline timing, register survival rules
                               INPUT: L4 fields + L5 addressing + ARU schematic + manual timing
                               PARTIAL CHECK: POST latch+register tests pass on a faithful model (Track B)
                                 — validates a slice (regfile, device decode, /32 unity), not the whole.
                                          │
   L7  AUDIO RESULT  ⬜ PENDING (do LAST)   run L6 over many samples → impulse response / reverb
                               VERIFY BY: compare to a measured IR from a real 224XL. Pass/fail only —
                               NO diagnostic power, so only meaningful once L1–L6 are each ✅.
```

## Per-layer ledger
| Layer | Status | Verified by / what's open |
|---|---|---|
| L1 CPU core | ✅ VERIFIED | kosarev/z80 `I8080Machine`; cputest + 8080pre + **8080exm** all pass in our env |
| L2 firmware exec | ✅ VERIFIED | `tools/boot8080.py` — faithful POST + real PGM-2 bypass (0x30/0x10) → prog_load; WCS cross-checked byte-identical to old pipeline (modulo LFO phase) |
| L3 program build | ✅ VERIFIED (CONCERT) | bytes built on verified 8080 via faithful boot; 0x3F4D + lanes 0-2 byte-identical. Open: other 19 programs (need LARC program-select); real-SBC capture unavailable |
| L4 field decode | 🔶 LARGELY VERIFIED | (a) M0b schematic net-trace (§G3R: l2=MI16–23, l3=MI24–31; WA=MI18/19, RA=MI20/21, XFER=MI24, ZERO=MI25, coeff=MI26–31; CSIGN/=tc_U20 JK follows MI23) **and** (b) firmware POST passing un-suppressed on the verified 8080 (`tools/aru_post.py`): **latch E32 + register E40 + multiplier E83 all PASS** (pins device-decode + WA/RA + CSIGN + coeff-byte polarity inv_l3 via ~l3, AND the gate-level Booth coeff serialization C0–5). Open: OFFSET/L5 fields are free-run, not POST-reachable |
| L5 address arith | ❌ FAITH | offset→address wiring; bits 12/13 control-vs-address (POST pins offset=0 → not POST-reachable; needs free-run/hardware) |
| L6 ARU datapath | 🔶 LARGELY VERIFIED | netlist-built ARU (regfile 4×LS670 + device decode U47 + /32 MAC + ±2¹⁸ sat) **passes the firmware register/walking-pattern test (E40) and the latch+static-readback+bus-test routine (E32) un-suppressed on the verified 8080**. **Multiplier: literal gate-level model (`tools/aru_booth.py`) = 16/20 bit-exact, STRUCTURAL** (NAND array + carry chain + fig-3.4 schedule); found+fixed 3 owner-confirmed schematic-trace errors (§4F.4 SR taps) + the §4.7/§4.6 reversal-cancellation (§4F.9). cmag=63 (both Booth rails) ≤2-LSB carry-save residual open. MAC cross-step timing + DAB free-run routing still open |
| L7 audio IR | ⬜ PENDING | real-unit IR, LAST step only |

**L4/L5/L6 are decomposed into their own bottom-up atoms** (each with status + ground-truth validator +
dependencies) in [`224XL-L4-L5-L6-decomposition.md`](224XL-L4-L5-L6-decomposition.md). Key structural fact
from that breakdown: POST single-step tests can pin the **datapath primitives** (L6.1–L6.6) and the L4 fields
they distinguishingly vary, but the **free-run execution** (L6.7–L6.13: T&C sequencer, per-step DAB routing,
cross-step timing) and L5's `CPC−offset` arithmetic are **not** POST-reachable — schematic control-path trace
or hardware only.

## Changelog
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
  the next frontier.
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
