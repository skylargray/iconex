# 224XL CONCERT microword verification — RESULTS (plan 019 executed)

**Date:** 2026-06-30. **Plan:** `docs/plans/019 - 224XL-WCS-microword-verification.md`.
**Question:** are the 100 CONCERT WCS microwords (`224XL_CONCERT_program_decode.md`, read from
`m.memory[0x4000:0x4200]`) the EXACT microwords the real 224XL executes for CONCERT?

## Verdict

**All three provenance gaps CLOSED. The 100 CONCERT microwords are correct _modulo the ROM dumps_** —
the strongest certainty achievable without the physical unit. Every acceptance criterion passed; the
`cmag=0`/`PROT=1` block at steps 5–22 is a **real firmware output**, not a stubbing/emulation artifact.

| Gap | What it doubted | Result | AC |
|---|---|---|---|
| **G1** build hardware-dependence | the WCS could read a stubbed ARU/T&C/DMEM port | **CLOSED** — 0x4000 byte-invariant under hardware-stub variation | AC1 ✅ |
| **G2** POST-bypass | a POST-pass might build the WCS differently than the PGM-2 bypass | **CLOSED** — identical with POST fully passing vs bypassed; build reads no POST-sourced cell | AC3 ✅ |
| **G3** lane-3 single-source | lane 3 (cmag/XFER/ZERO) came from the kosarev core ONLY | **CLOSED** — byte-identical lane 3 on a second, independently-certified 8080 | AC2 ✅ |

**Residual (the ceiling, stated plainly):** TRUE 100% = compare against the **physical unit** — dump the
WCS SRAM (MCM68B10) from a real CONCERT-loaded 224XL, or match its measured impulse response. No unit is
available, so this verification reaches **"certain modulo the ROM dumps"** (themselves checkable against
additional dumps). We do **not** claim more.

---

## Phase 1 — the build is a deterministic pure function of (ROM + program record). [G1, + static G2]

### 1.1 / 1.2 — build-window I/O census (`tools/trace_concert.py` aggregate)
Build window = `[prog_load @ write-order 66573 … last 0x4000 write @ 78574]` (mainloop @ 79497).
Every `IN` inside the window is the serial 8251 **status port 0xEF** (LARC display handshake, returns
`0x01`). **Zero hardware-port reads** in the window — no `0x06/0x07` ARU latch, no `0x02`, nothing. The
lone `IN 0x02→0x00` occurs at order 6678, during POST, far before the build.

### 1.3 — ★ STUB-VARIATION TEST (the proof) — `tools/verify_build_hwindep.py`
Re-booted CONCERT four times, each returning a different byte (`0x00, 0xFF, 0x55, 0xAA`) for **every
non-serial input port** (ARU latch `0x06/0x07` + the else-branch incl. `0x02`).

```
hw_stub=0x00 / 0xFF / 0x55 / 0xAA  ->  0x4000 IDENTICAL (0/512 bytes differ), lane-3 included
cross-check: fresh default boot == cached prior-session WCS (byte-identical)
VERDICT: G1 CLOSED — build is hardware-independent.   AC1: PASS
```
The stubs provably cannot have corrupted the microwords; the `cmag=0`/`PROT=1` block is real firmware output.

### 1.4 — static POST-state independence — `tools/verify_post_independence.py`
Captured every RAM read the build performs and each read's last-writer phase:
```
build-window RAM reads = 13013;  last-writer phase: prog_load 12986, init 14, normal_op 13
POST/DIAG-sourced reads: NONE
VERDICT: build is POST-INDEPENDENT (reads no cell last written by the POST self-test).
```

## Phase 2 — lane 3 cross-validated on a SECOND independent, exerciser-grade 8080. [G3 — the key]

Rather than depend on external test ROMs, a **clean-room 8080 core** (`tools/i8080_ref.py`) was written
from the documented Intel 8080 instruction/flag definitions and certified two independent ways
(`tools/i8080_ref_validate.py`):

- **Spec-formula ALU oracle (independent of kosarev):** **659,456** exhaustive checks — every ALU op over
  all operands/carry-in — against flag formulas computed directly from the 8080 spec (parity = even
  popcount; add/sub carry & half-carry; DAA; rotates). **PASS.** This is the decisive catcher for the G3
  risk: the old `z80emu` set P to *overflow* like a Z80; an exhaustive ADD/SUB/CMP sweep catches that on
  the first operand pair where overflow ≠ parity. The oracle is pure arithmetic, **not** another emulator.
- **Differential fuzz vs the exerciser-verified kosarev core:** **768,000** instructions across **all 256
  opcodes** over random register/flag/memory states — identical registers/flags/PC/SP/memory. **PASS.**

### 2c — boot CONCERT on both cores, diff 0x4000 — `tools/verify_lane3_crosscore.py`
Both cores boot the real firmware through POST + PGM-2 bypass to mainloop independently
(`tools/boot8080_ref.py` ports the boot driver to the ref core):
```
kosarev 0x4000[:8] = 8951bb8b8984bb8b
ref     0x4000[:8] = 8951bb8b8984bb8b
WHOLE 0x4000..0x41FF: 0 / 512 bytes differ  (lane 0/1/2/3 all 0)
VERDICT: G3 CLOSED — WCS byte-identical on two independent verified cores (lane 3 included). AC2: PASS
```

## Phase 3 — POST-pass vs POST-bypass. [G2, empirical] — `tools/verify_post_pass_vs_bypass.py`

The netlist-faithful ARU (`tools/aru_post.py`) is wired onto the ARU I/O ports so the firmware's POST
self-test **passes on its own merits** — no PGM-2 inject. Compared against the standard PGM-2-bypass boot:
```
POST sub-tests: E32 PASS · E40 PASS · E83 PASS · E91 PASS   (0 DIAG errors)
reached_normal_op=True  reached_mainloop=True (no bypass needed)
0x4000..0x41FF: 0 / 512 bytes differ (POST-pass vs POST-bypass)
VERDICT: G2 CLOSED — WCS identical with POST-pass vs POST-bypass.   AC3: PASS
```

---

## Acceptance criteria
- **AC1 (G1):** 0x4000 byte-invariant under hardware-stub variation. **PASS.**
- **AC2 (G3):** lane 3 byte-identical on two independent exerciser-grade 8080 cores. **PASS.**
- **AC3 (G2):** 0x4000 identical POST-pass vs POST-bypass (and statically POST-independent). **PASS.**
- **All three ⇒** the 100 CONCERT microwords are correct **modulo the ROM dumps**. TRUE 100% still
  requires the physical unit (WCS SRAM dump or measured IR) — the residual, out of scope without hardware.

## Decode-table status
No phase revealed a discrepancy, so `224XL_CONCERT_program_decode.md` was **not** regenerated — its source
(`verified_wcs_0x4000.json`) is byte-identical to every boot performed here (`8951bb8b8984bb8b…`). The
decode itself remains gate-traced + POST-verified (`224XL_provenance_ledger.md`); what this plan
established is that the **WCS bytes being decoded are the genuine firmware output**, on two cores, under
hardware-stub variation, and with POST passing. (Open downstream items — PROT's downstream effect, the
purpose of the `cmag=0` bus-move steps, delay-magnitude convention — are unchanged; they are about what the
verified microwords MEAN, not whether they are real.)

## Artifacts (all under `tools/`, results JSON in the session scratchpad)
| file | role |
|---|---|
| `verify_build_hwindep.py` | Phase 1.3 stub-variation (G1) |
| `verify_post_independence.py` | Phase 1.4 static POST-independence |
| `i8080_ref.py` | clean-room independent 8080 core |
| `i8080_ref_validate.py` | Phase 2b — spec-oracle + differential certification |
| `boot8080_ref.py` | boot driver for the ref core |
| `verify_lane3_crosscore.py` | Phase 2c lane-3 cross-core diff (G3) |
| `verify_post_pass_vs_bypass.py` | Phase 3 POST-pass vs bypass (G2) |
| `boot8080.py` | +`hw_stub` parameter (additive; default = unchanged behavior) |
