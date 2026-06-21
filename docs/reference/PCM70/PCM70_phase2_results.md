# Phase 2 — PCM70: the modulation / live-update axis

**Input set:** `Lexicon_PCM-70-V2_0-U62.BIN` (32K), `…U67.BIN` (8K), `…U95.BIN` (16K).
**Legend:** ✅ verified by our disassembly · 🟡 strong structural evidence · ❓ open.

---

## Phase 0 — integrity verdict: **PASS** ✅

Unlike the corrupted V2.0 PCM60 set, this one is clean and usable:

- Three **distinct** images (distinct MD5/SHA1) — no dedupe-collapse.
- **No Intel-HEX ASCII contamination** (zero `:NNNNNN…`-style records anywhere — the exact failure that poisoned the V2.0 PCM60 tails).
- **No address-line aliasing/mirroring** (half/quarter self-compare ≈ 0.01–0.02; U67's elevated 0.77 is just shared 0xFF fill, not a true mirror).
- Sensible fill: U62 fully programmed; **U67 active only in the lower 1 KB** (0x000–0x3FF), rest 0xFF; U95 lower half full + partial upper.

**Version skew (worth banking):** master **U62 = ©1986, V2.0**; slave **U95 + opcodes U67 = ©1985, V1.20**. The V2.0 revision touched only the host firmware; the slave/microcode are the unrevised V1.20 parts.

---

## ROM roles (from embedded banners + structure) ✅

| ROM | Size / type | Banner | Role |
|---|---|---|---|
| **U62** | 32K / 27256 | `(C) Copyright LEXICON, Inc. 1986` | **Master host Z80** — RST-vector table at 0x00 (`JP 1800h` on the 8-byte grid), program-name strings (CONCERT HALL, RICH PLATE/CHAMBER, INFINITE CHAMBER, CHORUS+ECHO, MULTIBAND DELAY, RES/RHYTHMIC CHORDS…), category + BPM tables. UI / program & parameter manager. |
| **U95** | 16K / 27128 | `PCM70 SLAVE AND SPACEWARE V1.20 1985` | **Slave Z80** — the SpaceWare algorithm + live-coefficient engine. **This is the modulation axis.** |
| **U67** | 8K / 2764 | `PCM70 OPCODES V1.20 1985` | **ARU microcode (control-store image).** Active 1 KB = 8 × 128-byte pages, plane-organized → **128-step program** (matches roadmap PCM60/70 = 128). Repeated step motifs = chained allpass stages. |

This is the roadmap's PCM70 model confirmed: PCM60's static microcode (**U67**) + a slave Z80 (**U95**) that reloads/modulates it, with a new master UI layer (**U62**).

---

## Slave (U95) machine model ✅

- Z80, **IM 1** → interrupt vector `0x38` → ISR at **0x02D3**. **RAM 0x4000–0x47FF** (stack 0x47FF).
- **I/O port map:**

  | Port | Direction | Function |
  |---|---|---|
  | `0x00` | out | WCS/data strobe (write 0 → settle → strobe) |
  | `0x30` | out | control / reset (init value `0x69`) |
  | `0x40` | out | address / latch |
  | `0x50` | in | status & master handshake (bit 0) |

- **Foreground (0x80):** command dispatcher. Polls port 0x50 + RAM command flags (0x4343–0x4348) the master pokes, dispatches handlers.
- **ISR (0x2D3):** lightweight **÷8 timekeeping divider** (alt-bank counter via `ex af,af'`/`exx`, reload = 8), maintains tick counters. This is the **tempo/BPM clock**, *not* the DSP coefficient modulation — modulation runs in the foreground, paced by these ticks.

---

## The live-update / modulation mechanism — core Phase 2 result ✅

**Where the control store lives.** The ARU **WCS is memory-mapped at ≈0x8000–0x83FF** in the slave's space, organized as multiple **128-byte byte-planes**. Evidence:
- `sub_02b6h` loads three 128-byte planes via `lddr` into **0x8180 / 0x8280 / 0x8300**, sourced contiguously from ROM **0x2ACD–0x2C4C** — a region that *contains the smooth descending ramps* found by the table scan (0x2B4D, 0x2B8E). So those curves are **coefficient/offset plane data**.
- Read-back base is a pointer in **RAM[0x42EE]** (`sub_0e51h`: `HL = (42EE) + DE`).
- Structural planes come from **U67 (OPCODES)**; the slave-managed coefficient/offset planes are what get modulated.

**Per-coefficient write primitive — `sub_0ecch` / `sub_0e59h`.** A read-modify-write into one microword byte (preserving opcode/control bits, updating only the coefficient/offset field). Encoding, straight from the code:

- magnitude `>> 2` (÷4) → `cpl` (1's-complement) → mask to **3 bits** (single-byte mode) or **4 bits** (two-byte mode), then `OR` into the preserved upper bits;
- **two packing modes selected by control bit 4** of the existing word (`bit 4,a → jp z`): 3-bit field in one byte, or a wider field spanning two bytes;
- **sign:** `sub_0e59h` does `bit 7,b → set 3,a` — the value's bit 7 (sign) maps to **microword control bit 3**;
- every write is mirrored to a **RAM shadow at 0xBE00 + offset** (the hardware store is write-only; the shadow makes RMW possible).

> **Resolves §9 "unsigned /256 vs signed + SIGN bit":** the ARU coefficient field is **signed — separate sign control bit + complemented, ÷4-shifted magnitude**. (Also concrete input to §8 ARU arithmetic: the shift/complement idiom is explicit here.)

**Update / animation engine — `sub_071dh`.** Walks a list of **3-byte entries `{addr_lo, addr_hi, value}`**: forms `DE = WCS target`, **steps the value** (`−4`/pass if bit 7 = 0, `−1`/pass if bit 7 = 1 — a multi-rate ramp), writes it back, and pushes it via `sub_0ecch`; self-loops (`jp 0725h`). This is the **de-zipper / envelope / coefficient-animation engine** — it smooths parameter changes and is the substrate slow modulation rides on. It also rotates a **48-byte (0x30) double-buffered parameter block** (0x4000 / 0x4040 / 0x4080) and indexes per-algorithm data via a pointer at **top-of-ROM (0x3FFE)**.

**Change detection — `sub_0527h`.** Diffs working params (0x4000–0x402F) against the loaded copy (0x4040–0x406F); on change runs the reload: `di → sub_071dh → sub_02b6h →` port-0x40/0x00 strobe + 16-cycle `djnz` settle → clear 0x00/0x30/0x40.

**End-to-end:** master writes params → slave RAM 0x4000+ → `sub_0527h` detects change → `sub_071dh` ramps each `{WCS-addr, value}` entry toward target → `sub_0ecch` RMW-encodes it into the memory-mapped WCS plane (+0xBE00 shadow). **Modulation injection points = the WCS addresses in the animated list; "modulation" = time-varying values fed to them.** This is exactly the 480L's open "modulation injection" mechanism, one generation simpler.

---

## What Phase 2 closes for the 480L (§9)

- ✅ **Modulation/live-update mechanism** — slave maintains a list of `(WCS-address, value)` entries pushed through a memory-mapped control-store window with a RAM shadow + RMW. The 480L's `0x48000`-window streaming is the bigger-iron version of this.
- ✅ **Coefficient encoding / sign convention** — signed, separate sign control bit, complemented + ÷4-shifted magnitude; two field-packing modes.
- ✅ **Live-coefficient streaming pattern** (§9 last bullet analogue) — `sub_071dh` + `sub_0ecch`; RMW updates only the coefficient/offset field, leaving opcode/control bits intact.
- 🟡 **Parameter smoothing** is multi-rate ramping in the update list, not instantaneous writes (de-zippering by design).

---

## Open after Phase 2

- ❓ **LFO phase accumulator.** Waveform/curve tables are located (the 0x2B00 and 0x3800–0x3BC0 ramps) and the animation engine that consumes targets is mapped — but the specific routine that advances an LFO phase and writes *oscillating* targets into the update list is not yet isolated.
- ❓ **U67 microword field map** (which of the ~8 planes is opcode vs coefficient vs offset). Wants the PCM60 Rosetta decoder cross-referenced; it was not loaded this session. Methodologically a Phase-1-style static decode — not blocked.
- ❓ **Exact WCS window decode** — 0x8000 region is evidenced; precise plane count and the U67-vs-slave-plane interleave aren't fully pinned.
- ❓ **Literal PCM70-vs-PCM60 microcode byte-diff** — needs the clean PCM60 V1.0 images loaded alongside U67 in the same session.

**Next:** (1) re-load the PCM60 V1.0 set; run the Phase-1 decoder on U67 and do the literal diff; (2) isolate the LFO phase routine in U95; then **Phase 3 — 224XL** (the Concert Hall figure-eight tank ancestor).

---

### Artifacts
- `PCM70_U95_slave_disasm_org0.asm` — full z80dasm of the slave (origin 0, addresses = file offsets).
- `PCM70_phase0_analysis.py` — integrity / entropy / autocorrelation / string / table-scan scripts.
