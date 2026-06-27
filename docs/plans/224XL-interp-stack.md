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
| L4 field decode | ❌ FAITH | bit-map unverified; needs schematic trace and/or expanded POST coverage |
| L5 address arith | ❌ FAITH | offset→address wiring; bits 12/13 control-vs-address |
| L6 ARU datapath | ❌ FAITH | only a POST slice checked; MAC timing, DAB source, register survival open |
| L7 audio IR | ⬜ PENDING | real-unit IR, LAST step only |

**L4/L5/L6 are decomposed into their own bottom-up atoms** (each with status + ground-truth validator +
dependencies) in [`224XL-L4-L5-L6-decomposition.md`](224XL-L4-L5-L6-decomposition.md). Key structural fact
from that breakdown: POST single-step tests can pin the **datapath primitives** (L6.1–L6.6) and the L4 fields
they distinguishingly vary, but the **free-run execution** (L6.7–L6.13: T&C sequencer, per-step DAB routing,
cross-step timing) and L5's `CPC−offset` arithmetic are **not** POST-reachable — schematic control-path trace
or hardware only.

## Changelog
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
