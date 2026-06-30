# 019 — 224XL CONCERT microword verification: are these the REAL microwords?

**Goal.** Establish, to the highest certainty achievable *without a physical unit*, that the 100 CONCERT WCS
microwords (`docs/reference/224/224XL_CONCERT_program_decode.md`, read from `m.memory[0x4000:0x4200]` after a
verified-core boot) are the EXACT microwords the real 224XL executes for CONCERT — or find precisely where and
why they differ.

**Why this matters.** The entire reverb reconstruction is built on these 100 microwords. The open M4 problems
(the inert `cmag=0`+`PROT=1` block at steps 5–22, the over-unity feedback) hinge on **lane 3** (`cmag`/`XFER`/
`ZERO`). If lane 3 is even slightly wrong we are chasing a phantom. This plan closes the provenance gaps.

---

## Already established — DO NOT redo (load-bearing, verified)
- ROM dumps are real (`ROMs/Lexicon 224/224XL v8_21/`); the **kosarev `import z80` I8080 core** passes the
  canonical 8080 exercisers (cputest / 8080pre / 8080exm). `tools/boot8080.py` boots it.
- **0x4000–0x41FF IS the WCS** — *write-trace confirmed* (the expander, writer PCs `0xAA42–0xAB63`, writes it
  during `prog_load`; it is NOT streamed via I/O). Tool: `tools/trace_concert.py` (+ `tools/trace8080.py`).
- The **decode** (bit→field map) is POST-verified (`docs/reference/224/224XL_provenance_ledger.md`).
- **Lanes 0–2** (offset MI0-15, MEMAC, MI16, WA, RA, CSIGN, PROT) are **CROSS-VALIDATED**: byte-identical between
  the kosarev-core boot and the old `tools/z80emu.py` (`tools/aru224_emulate.py`) pipeline.
- The static snapshot (`scratchpad/concert_wcs.json` / `verified_wcs_0x4000.json`) = the verified-core boot,
  byte-identical.

## The gaps this plan closes
- **G1 — build hardware-dependence.** The WCS build runs with **stubbed** ARU/T&C/DMEM I/O ports
  (`boot8080.on_input` returns `0xFF` for ARU ports `0x06/0x07`, etc.). If the build reads any stubbed port and
  uses it, the WCS could differ from the real unit. The "build is pure 8080, no ARU" claim is **unproven**.
- **G2 — POST-bypass.** We inject PGM-2 (`0x30/0x10`) to skip POST (the stubbed ARU fails it). If the firmware
  builds the WCS differently after a POST *pass* vs a *bypass*, ours could be wrong.
- **G3 — lane-3 single-source (the sharpest).** `cmag`/`XFER`/`ZERO` come from the kosarev core ONLY — the
  z80emu pipeline **disagrees on lane 3** (z80emu has an 8080 parity bug, and the coeff build uses parity
  branches). The most reverb-critical bytes are the **least cross-validated** AND the **most emulation-sensitive**.

## The ceiling (state it plainly)
TRUE 100% = compare against the **physical unit**: dump the WCS SRAM (MCM68B10) from a real CONCERT-loaded 224XL,
or match its **measured impulse response**. No physical unit is available, so this plan reaches **"certain modulo
the ROM dumps"** — the strongest achievable without hardware. Do not claim more.

---

## Phase 1 — Prove the build is a deterministic pure function of (ROM + program record). [closes G1, helps G2]

**The decisive test is STUB VARIATION: if varying the stubbed hardware-port values leaves 0x4000 byte-identical,
the build provably does not use those ports.**

1.1. **Enumerate the build's I/O.** Run `tools/trace_concert.py` (boots to CONCERT under `Trace8080`, which logs
   every `IN`/`OUT` with order markers incl. `prog_load`@0x13B6 and `mainloop`@0x8169). From the saved
   `scratchpad/trace_concert_aggregate.json`, list every `IN` whose order falls in the **build window**
   (`prog_load` → the last 0x4000 write). Record `(writer-PC, port, returned-stub-value)` for each.

1.2. **Classify each `IN` port:** serial/LARC (`0xEE` data, `0xEF` status — display handshake, not build data)
   vs hardware (`0x06/0x07` ARU latch, or any other). Flag every hardware-port read in the build window.

1.3. **★ STUB-VARIATION TEST (the proof).** Re-boot to CONCERT several times, each with a *different* stub value
   for the hardware ports (edit `boot8080.on_input`: return `0x00`, then `0xFF`, then `0x55`, then `0xAA` for
   `0x06/0x07` and any other flagged port). Read `m.memory[0x4000:0x4200]` each time and diff.
   - **Build a small harness** (e.g. `tools/verify_build_hwindep.py`) that parameterizes the stub value and
     returns the 0x4000 image, so the diff is one script.
   - **DECISION:** if 0x4000 is **byte-identical across all stub values → G1 CLOSED** (the build is hardware-
     independent; the stubs cannot have corrupted the microwords, and the `cmag=0` block is a real firmware
     output, not a stubbing artifact). If it **changes → the build IS hardware-dependent**: identify which port
     + value it needs, and obtain the REAL value (from the faithful ARU model in Phase 3 / from the POST path).

1.4. **POST-state independence (static).** From the same trace, confirm the build code (`B55B`@0xB55B, expander
   @0xAA9F→0xAB39, coeff fetch @0xB510) does not read any memory location that the POST writes (the DIAG
   status). If the build is reached and runs identically regardless of POST outcome and reads no POST-set flag,
   G2 is *likely* independent — confirm empirically in Phase 3.

**Phase 1 deliverable:** a yes/no on "the WCS build touches no hardware that affects the microwords," with the
stub-variation diff as evidence. This is the cheapest, highest-leverage step — do it FIRST.

---

## Phase 2 — Cross-validate lane 3 (the coefficients) on a SECOND independent verified 8080. [closes G3 — the key]

2.1. **Obtain a genuinely independent, exerciser-verified 8080 core.** NOT `tools/z80emu.py` (known parity bug).
   Options, in order of preference:
   - (a) A different mature 8080 emulator library (Python or via `ctypes`/subprocess) — **first run it through
     `8080exm`/`8080pre`/`cputest` and require a clean pass**, especially the parity (P/V) behaviour.
   - (b) Write a fresh minimal 8080 core and validate it the same way.
   The point is **independence** from the kosarev core's implementation.

2.2. **Run the SAME CONCERT build on the second core.** Port the `boot8080` driver logic (memory map, the serial
   8251 stubs on `0xEE/0xEF`, the RST-7 interrupt injection, the PGM-2 bypass) to the second core's interface.
   Reach `mainloop`, read `0x4000–0x41FF`.

2.3. **Require BYTE-IDENTICAL**, with explicit focus on **lane 3** (every `4k+3` byte) and the decoded `cmag`/
   `XFER`/`ZERO`. Diff against the kosarev WCS.
   - **DECISION:** identical → **G3 CLOSED** (lane 3 cross-validated on two independent correct cores). Differ →
     the lane-3 build is sensitive to an instruction both cores must get right: dump the firmware instructions
     the expander/coeff-fetch execute (esp. parity-flag ops `ADD/SUB/CMP` + conditional `JP P/M/PE/PO`), run
     BOTH cores on those against `8080exm`, and determine which is correct. Fix the wrong core; re-diff.

2.4. **Sanity:** confirm both cores agree with the kosarev core on lanes 0–2 too (should already match z80emu on
   those) — a regression check that the port is faithful.

**Phase 2 deliverable:** byte-identical lane-3 on two independent verified cores, OR a localized parity/instruction
discrepancy resolved in favour of the exerciser-correct core. This is the most reverb-critical gap.

---

## Phase 3 — Differential boot: POST-pass vs POST-bypass. [closes G2 empirically]

3.1. **Build a POST-PASSING boot.** The current boot BYPASSES POST because the stubbed ARU fails. Wire a faithful
   ARU onto the boot's ARU I/O ports so POST PASSES: the POST-verified datapath already exists
   (`tools/aru_rtl_dp.py` / `tools/aru_post.py` reproduce E32/E40/E83/E91). Route the ARU port reads
   (`0x06/0x07` latch + the strobe ports) through that model in `boot8080.on_input/on_output` so the firmware's
   POST self-test passes instead of erroring (no PGM-2 inject needed).

3.2. **Boot with POST PASSING → load CONCERT → read 0x4000.**

3.3. **Compare to the PGM-2-bypass WCS.**
   - **DECISION:** identical → **G2 CLOSED** (the build is POST-independent; the bypass we use is harmless).
     Differ → the boot path matters; the **POST-passing** WCS is authoritative — regenerate the decode table from
     it and re-assess the M4 work on the corrected microwords.

   *(If Phase 1.3 shows hardware-independence AND 1.4 shows no POST-state branch, G2 is largely settled and Phase 3
   becomes a confirmation rather than a discovery.)*

**Phase 3 deliverable:** the WCS is invariant to POST pass vs bypass (or the POST-passing WCS replaces the snapshot).

---

## Acceptance criteria (what "verified" means here)
- **AC1 (G1):** `0x4000` byte-invariant under hardware-stub variation (Phase 1.3).
- **AC2 (G3):** lane 3 byte-identical on two independent exerciser-verified 8080 cores (Phase 2.3).
- **AC3 (G2):** `0x4000` identical with POST-pass vs POST-bypass (Phase 3.3), or statically proven POST-independent.
- **All three ⇒** the 100 CONCERT microwords are correct **modulo the ROM dumps** (themselves checkable against
  additional dumps). **TRUE 100%** still requires the physical unit (WCS SRAM dump or measured IR) — out of scope
  without hardware; note it as the residual.

## Recommended order
**Phase 1 first** (cheapest; decisive on G1; collapses much of G2; and directly tests whether the `cmag=0` block
is real firmware output vs a stubbing artifact). Then **Phase 2** (the sharpest gap — lane-3 coeffs). Then
**Phase 3** (empirical G2).

## Ground rules
- Never trust a single emulator for lane 3 — that is the whole point of Phase 2.
- The stub-variation test (1.3) is a real experiment, not a code-read; run it.
- Keep POST (`tools/aru_post.py`) + the M3 suite (`tools/aru_freerun.py`) green throughout.
- Report which gaps CLOSED vs which remain; do not round "high confidence" up to "verified."
- If any phase reveals the snapshot is wrong, regenerate `224XL_CONCERT_program_decode.md` from the corrected
  build and re-open the M4 analysis on the corrected microwords before doing anything else.

## Key addresses / tools (quick reference)
- ROMs: `ROMs/Lexicon 224/224XL v8_21/` (SBC1-3 2716, NVS1-8 2732).
- Boot (verified core): `tools/boot8080.py` (`boot(trace=…, snapshot_cb=…, extra_ticks_after_mainloop=…)`).
- Trace harness: `tools/trace8080.py`; CONCERT driver: `tools/trace_concert.py`.
- Other (buggy) pipeline for the lanes-0-2 cross-check: `tools/aru224_emulate.py` (`build_record`, `tap_map`).
- Decode table generator: `tools/decode_concert_program.py` → `docs/reference/224/224XL_CONCERT_program_decode.md`.
- Milestones: `prog_load`=0x13B6, `mainloop`=0x8169. Program record array @0xB800 (CONCERT=entry 0). WCS image
  @0x4000–0x41FF. Build routines: record builder @0xB55B, expander @0xAA9F (stops 0xAB39), coeff fetch @0xB510.
- POST-passing ARU model (Phase 3): `tools/aru_rtl_dp.py` / `tools/aru_post.py` (E32/E40/E83/E91).
