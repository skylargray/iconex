# Lexicon 480L — Reverse-Engineering Roadmap

**Objective:** recover the 480L reverb algorithms (delay-line maps, allpass/comb
structure, coefficient tables, modulation, output-tap scheme) at a level
sufficient to reconstruct or re-implement them.

**Strategy in one line:** don't start on the 480L. Climb the family tree from the
simplest sibling that shares its datapath, build a working ARU microword decoder
there, then carry it up to the 480L — the hardest member of the family.

**Confidence legend:** ✅ verified (manual / our own disassembly) · 🟡 strong
community evidence (teardowns, developer posts) · ❓ open.

**Progress:** Phase 0 ✅ · Phase 1 ✅ (PCM60 microword + topology decoded, V1.0 set) ·
Phase 2 ✅ **complete** (PCM70 live-update + coefficient encoding decoded; **both carry-overs
now closed** — U67 = 7 control planes + banner, coefficient = WCS plane 6; LFO phase accumulator
= `sub_0ad2h`@0x0AD2/0x4335) · Phase 3 (224XL) **in progress** — Phase-0 integrity PASS; flat
memory/bank map + ARU port interface (0x00-0x07) decoded; **datapath variant CONFIRMED** (2 mult
bits via NVS4 0xB4F0 packer + dedicated shift-register port 0x05); **program-record bytecode VM +
microword build mechanism DECODED** (interpreter 0xAA9F, step-builder 0xB55B: offset = ptr−writeptr,
ring-buffer wrap, sign-magnitude+2-bit coeff); **build EMULATED on real firmware** (`tools/z80emu.py`)
→ **complete reverb algorithm recovered** for the first 3 program records: delay tap map (61 taps,
allpass pairs, 17-tap output line, ~100 steps) **+ coefficient gains** (sign-mag/127: allpass −½,
loop +0.976, diffusion gains). decode **cross-validated against the 224X Service
Manual** (WCS@0x4000–0x41FF, offset=position−microword=delay, 100 steps, 34.13 kHz, 16×6-bit sign-mag
mult + saturation + dual-rank shift register — all confirmed). **v8.2.1 = the operational 224XL
firmware** (the serial port is the **LARC** UI, not a diagnostic terminal; `DIAGNOSTICS` = power-up
self-test banner): emulator now boots it through the LARC `0xC8` handshake to the main loop and drives
the LARC display (captured `224XL V8.2 DIAGNOSTICS…`). record→name reachable — next: model the DSP
power-up self-test so it loads programs, then inject PROG keypresses to capture WCS+name per program.
**Microcode→firmware divergence:** original-224 **OTP = static mask-ROM microcode** (1 hall ×16 param
frames, 0.3–562 ms, Concert Hall ancestor); 224X/XL = **SBC-loaded WCS firmware**. See §5 RESULTS.

---

## 1. What we're actually after

The 480L "reverb algorithm" is **DSP microcode** — fixed-width microwords executed
by Lexicon's custom ARU datapath on the HSP cards. It is **not** in the host CPU
firmware and **not** on the register cartridge. Three distinct things have been
conflated before, so to keep them straight:

| Artifact | Contents | Relevance |
|---|---|---|
| **Host EPROMs** (U40–U43, our 4 dumps) | 68008 firmware: UI, program/param manager, slave-download driver, data tables | The *plumbing* that loads algorithms — not the algorithms ✅ |
| **Register cartridge** (NVRAM, J1, `$70000`) | Saved presets/registers (144-byte parameter records) | Settings only — no algorithm code ✅ |
| **Program cartridge** (ROM, e.g. "480L Program Cartridge V1.00") | Algorithm microcode + program definitions (Random Hall, Ambience, etc.) | **This is where cart-delivered algorithms live** ✅ |

Note: base Banks 1–17 ship in mainframe firmware; the Random Hall / Ambience /
Stereo Adjust family arrived on the 480L later (v4.x), ported over from the
300-series. 🟡 So the "target" algorithms are split between firmware-resident
and cartridge-resident microcode.

---

## 2. 480L processing architecture (recap)

| Item | Finding | Conf. |
|---|---|---|
| Host CPU | Motorola **68008** (8-bit bus, 20-bit / 1 MB address) | ✅ |
| Slaves | **Z80 @ 4 MHz**, two per HSP board, up to six in max config | ✅ |
| DSP datapath | custom **ARU, 18-bit** (P/N 330-04362, U60/U89) + custom **MMU** (330-03766, U69/U98) | ✅ |
| Microword | **48-bit**, fields documented in Service Manual Ch. 4.8.2 (offset → MMU, coefficient, control) | ✅ |
| Control store | **WCS** (2018 SRAM), dual-ported slave/DSP by phase-stealing; DSP PC counts 0–79 per sample | ✅ |
| Program length | 80 microcode steps, multiple ARU cores (commonly cited as **four processing cores**) | ✅ / 🟡 |
| Algorithm transport | host **DMA-writes slave Z80 RAM** via six 16 KB channels at `0x48000`; slave loads WCS, then live-updates offsets/coefficients | ✅ |
| Fixed HSP PROMs | 74S472 CONTROL (U62/U91), 74S472 COEF (U77/U112), 82S123 TIMING (U103) — sequencing/base data, not the algorithm | ✅ |

Implication: the ARU is a documented-enough microcoded engine to disassemble. The
remaining unknowns are the ARU's **arithmetic semantics** (rounding / saturation /
coefficient encoding), not the instruction structure.

---

## 3. The Lexicon datapath family — generational map

There is a clean split in the silicon. The 480L is on the **older, more legible**
side of it. 🟡 (per published teardowns; see §10)

| Generation | Members | Datapath | Microcode visibility |
|---|---|---|---|
| **ARU** (discrete) | 200, **224XL**, **PCM60**, **PCM70**, **480L** | custom ARU + MMU + TTL | sequencer in the open — directly disassemblable |
| **Lexichip** (VLSI) | 300 / 300L / **M300**, **PCM80/81**, PCM90/91 | single-chip ARU derivative | internal microcode bus not exposed — harder |

Cross-generation compatibility notes (🟡):

- **PCM60 / PCM70 / 480L ARUs are practically identical.** The 480 adds one T-state
  per instruction (one extra multiply); the PCM70 is an updated PCM60.
- **224XL ARU is a variant** — allows two multiplier bits at once, uses a dedicated
  shift register rather than rewired single registers. Same family, decoder needs
  adaptation.
- **Lexichip microcode is "very similar but not identical" to the 480L ARU** — a few
  control bits repurposed for ADC/DAC timing and memory-bank select. A 480-literate
  reader can mostly read it.
- **Program step counts differ:** 224 = 100, PCM60/70 = 128, 480 = 80 × 4 cores,
  300 = 96 (two Lexichips), PCM91 = 128. These set the microword slicing stride per box.

---

## 4. Asset inventory (dumps on hand)

| Dump | Gen | Datapath | Steps | Role in this project | Priority |
|---|---|---|---|---|---|
| **PCM60** | ARU | ARU, **no control processor**, ROM control store, no tap modulation | 128 | Cleanest ARU ISA reference — fully static · ✅ **ISA + topology decoded (Phase 1)** | **1 ✅** |
| **PCM70** | ARU | PCM60 + slave Z80 (reload-at-will) | 128 | Isolates the modulation / live-update mechanism · ✅ **architecture + modulation decoded (Phase 2)** | **2 ✅** |
| **224XL** | ARU | ARU variant (2 mult bits, shift register) | ~100 | Algorithmic ancestor of the Concert Hall figure-eight tank | 3 |
| **M300** | Lexichip | 2× Z80 + Lexichip VLSI | 96-ish | The 480-family algorithms (Random Hall, Ambience, Stereo Adjust) in near-480 dialect | 4 |
| **480L** (host ROMs) | ARU | 68008 + ≤6 Z80 + 4× ARU/MMU | 80×4 | **The target** | 5 (assemble) |
| **PCM80 / 81** | Lexichip | Lexichip + Motorola 56002 | — | Reverb is Lexichip-internal; heritage is PCM70 | last / skip |

---

## 5. The roadmap

### Phase 0 — Characterize every dump
For each EPROM image, classify the contents before disassembling anything:
- Which processor's code is it? **Master Z80 (UI)**, **slave Z80**, **ARU microcode**,
  or **Lexichip control-store image**.
- Z80 code reads as Z80 (RST vectors at `0x00/08/.../38`, recognizable opcode density).
- Microcode reads as **periodic fixed-stride records** — the microword stride pops out
  structurally (entropy + autocorrelation by candidate word width).
- Record ROM widths, socket/board origin, and which images pair into a wide microword
  (the 480L splits its 48-bit word across A/B banks — expect similar bank-splitting elsewhere).

**RESULTS ✅ (PCM60, 2026-06).** Two PCM60 dump sets were supplied. The **V2.0 set
(2764 / 8 KB) was corrupted** and is unusable as-is: all four `.hex` files were
byte-identical (each ≈ chip-1, not their own chip), three `.bin` tails were
overwritten with ASCII Intel-HEX *text* of foreign Z80 code, and U38/U43 (8 KB) were
mostly blank. The **V1.0 set (2732 / 4 KB at U32/U35/U38/U43) is clean** — four
distinct images, `bin == hex` on all four, no contamination — and became the Phase 1
basis. Lesson banked into §6: validate dump integrity (dedupe, double-read-diff,
ASCII-contamination scan) *before* any decode; a bad set yields confident nonsense.

### Phase 1 — PCM60: establish the ARU ISA  ⭐ critical path
The PCM60 is the floor of the family: ROM control store, **no control processor**, **no
tap modulation** → the entire algorithm is one static microcode image with zero runtime
confounds. Deliverables:
1. Determine the PCM60 microword **width and field layout** (offset / coefficient / control).
2. Write a **microword decoder** (not a CPU disassembler — this is microcode).
3. Decode the full 128-step program; confirm it resolves into a sane Schroeder/allpass-loop
   topology you already understand. That validation closes the loop on the field map.
4. Pin the **arithmetic semantics**: the ×0.5 double-precision-multiply scalar idiom, the
   MAC instruction, rounding-toward-zero behavior, coefficient shift encoding.

Output: a tested ARU microword decoder + a documented PCM60 algorithm. This is the
Rosetta Stone everything else is read against.

**RESULTS ✅ (V1.0 firmware set, 2026-06).**

*Geometry.* All four ROMs carry a hard **period-128** (U43 autocorr 0.98, U38 0.82 vs
~0 baseline) → 128-step program, each 4 KB ROM = 32 frames × 128 bytes. The four ROMs
are **parallel byte-lanes of one 32-bit microword**. ROM address decodes as:

> `A11 (program A/B) | A10–A7 (parameter 0–15) | A6–A0 (step 0–127)`

confirming the "no control processor" model: the panel knobs drive the upper address
lines, selecting a precomputed coefficient frame; the 128-step microprogram is static.
There are **2 programs** (U43 has exactly 2 unique frames) and **16 param frames**.

*Field map (microword = 32 bits).*

| Lane | Field | Meaning | Conf. |
|---|---|---|---|
| **U38 : U32** | 16-bit **signed offset** (2's comp), U38 = hi byte, U32 = lo byte | → MMU. Per the 480L Ch.4 MMU model the offset is subtracted from a once-per-sample position pointer. **negative = read a delay tap** (delay = −offset samples); **positive = write target** near the write pointer | ✅ |
| **U35** | **coefficient** (8-bit, /256) | ARU multiplier. `0x7F` = 0.496 = the **×0.5 scalar**. The decay knob scales these — smooth sweep, deepest taps drop fastest (the decay envelope) | ✅ |
| **U43** | **control** (8-bit) | **low nibble = opcode** (`n0` = memory WRITE; `n3/n7/nF` = READ/MAC — confirmed against the offset-sign read/write split). bit3 = section marker, bit2 = phase | role ✅, full opcode map 🟡 |

*Topology.* Decoding `U38:U32` yields a sane reverb tap set — **60 distinct delay taps,
68 … ~27,100 samples** (program A) — an incommensurate spread, as a dense reverb wants.
The algorithm reads as a **recirculating tapped-delay network**: a feedback core (long
delays, ~0.9 gain, interleaved reads/writes) feeding chains of decaying-gain taps
(0.5 → 0.4) that accumulate to the output — i.e. the Schroeder/allpass-loop family
shape, now with actual numbers. This closes the loop on the field map.

**Deliverables status:** (1) width + field layout ✅ · (2) microword decoder ✅
(`pcm60_decode.py`, parameterized by the field table) · (3) topology ✅ **at the
tap-map level** (per-step delay + coeff + read/write; resolves to the expected shape) ·
(4) arithmetic semantics — *partial*: the **×0.5 scalar idiom is identified** (`0x7F`),
but rounding/saturation + exact coeff sign/scaling remain.

**Gaps CLOSED by Phase 1:**
- ✅ PCM60 microword width, lane→field map, and address decode.
- ✅ Offset/MMU semantics (16-bit signed, pointer-relative) → absolute delay lengths.
- ✅ Coefficient lane + the decay-knob → gain-scaling mechanism; the ×0.5 scalar.
- ✅ Opcode field location (control low nibble) + read/write classification.
- ✅ A working, reusable decoder — the Rosetta Stone for Phases 2–5.

**Gaps STILL OPEN (PCM60):**
- ❓ **Full data-flow wiring** — the accumulator / register-file routing (which reads
  sum into which intermediate; where each write sources from). Lives in the *upper*
  control-word bits (the 480L byte-5 `ACC/`, `XCLK/`, `WA/RA` analogues). Tap map is
  done; the datapath plumbing is not.
- ✅ (resolved in Phase 2) Coefficient **sign/scaling convention** — **signed**: separate sign
  control bit (value bit 7 → microword ctrl bit 3) + complemented, ÷4-shifted magnitude in a
  3- or 4-bit field. **Rounding-toward-zero / saturation** behavior still wants hardware (§8).
- ❓ MMU **row/col** physical mapping (linear delay is known; not needed for topology).

**NEXT STEPS:** proceed to **Phase 2 (PCM70 diff)** to capture the modulation /
live-update mechanism (also answers a 480L open question, §9). Optional follow-ups:
decode the upper control bits against the 480L byte-5 control semantics to *infer*
the register routing, and run behavioral validation on hardware for the arithmetic.

### Phase 2 — PCM70: add the modulation axis
The PCM70 is "an updated PCM60" with a slave Z80 that reloads the control store at will.
**Diff PCM70 against PCM60**; the delta is essentially the modulation / live-coefficient
mechanism — the exact thing left open on the 480L (modulation injection points). Also
captures the Concert Hall / Plate lineage. Minor decoder tweak for the extra T-state.

**RESULTS ✅ core done (V2.0 set: U62/U67/U95, 2026-06).**

*Integrity (Phase-0 discipline) — PASS.* Three **distinct** images (distinct hashes, no
dedupe-collapse); **no Intel-HEX ASCII contamination** (the exact failure that poisoned the
V2.0 PCM60 tails); no address-line aliasing (half/quarter self-compare ≈0.01–0.02; U67's
0.77 is shared 0xFF fill, not a mirror). U62 fully programmed; **U67 active only in the low
1 KB** (0x000–0x3FF), rest 0xFF. **Version skew:** master U62 = ©1986 **V2.0**; slave U95 +
opcodes U67 = ©1985 **V1.20** — the V2.0 revision touched only the host firmware.

*Architecture* — exactly the "PCM60 + Z80(s)" the roadmap predicted:

| ROM | Banner / type | Role |
|---|---|---|
| **U62** | ©1986, 27256 | **Master host Z80** — RST table (`JP 0x1800`), program-name strings (CONCERT HALL, RICH PLATE/CHAMBER, INFINITE CHAMBER, CHORUS+ECHO, MULTIBAND DELAY…), category + BPM tables. **UI / program & parameter manager** (no DSP modulation here). |
| **U95** | "PCM70 SLAVE AND SPACEWARE V1.20", 27128 | **Slave Z80** — the SpaceWare algorithm + **live-coefficient engine**. *This is the modulation axis.* |
| **U67** | "PCM70 OPCODES V1.20", 2764 | **ARU microcode (control-store image)** — active 1 KB = **8 × 128-byte planes → 128-step program** (matches the family's 128). Repeated step motifs = chained allpass stages. |

*The live-update mechanism — the core Phase 2 result (all slave-side, U95):*
- **Machine:** Z80, IM 1, ISR @**0x02D3** = a ÷8 **BPM-timekeeping** divider only (*not* the
  coefficient modulation — that runs in the foreground). Foreground dispatcher @**0x80** polls
  port 0x50 + RAM command flags 0x4343–0x4348 the master pokes. RAM 0x4000–0x47FF. **Ports:**
  0x00 = WCS/data strobe · 0x30 = control/reset (init `0x69`) · 0x40 = address/latch · 0x50(in)
  = status/handshake.
- **The WCS is memory-mapped @≈0x8000–0x83FF** as 128-byte byte-planes — *not* port-streamed
  (ports are strobe/latch/handshake only). `sub_02b6h` `lddr`-loads three planes into
  0x8180/0x8280/0x8300 from ROM **0x2ACD–0x2C4C** (the descending-ramp region the earlier table
  scan flagged — so those curves are **coefficient/offset plane data**). Structural planes come
  from **U67**; the slave-managed coeff/offset planes are what get modulated. Read-back base =
  pointer in `RAM[0x42EE]`.
- **Per-coefficient write = RMW** (`sub_0ecch`/`sub_0e59h`): updates only the coeff/offset field,
  preserving opcode/control bits. **Encoding (from the code):** magnitude `>>2` (÷4) → `cpl` →
  **3-bit field** (single-byte) or **4-bit field** (two-byte, mode by control **bit 4**); **sign**
  = the value's bit 7 → microword control **bit 3**. Every write is mirrored to a **RAM shadow
  @0xBE00+offset** (the hardware store is write-only, so the shadow makes RMW possible).
- **Animation engine** (`sub_071dh`): walks a list of 3-byte **`{addr_lo, addr_hi, value}`**
  entries → `DE` = WCS target, **steps the value** (−4/pass if bit 7=0, −1/pass if bit 7=1 — a
  multi-rate ramp), writes it back via `sub_0ecch`; self-loops. The **de-zipper / coefficient-
  animation** engine. Rotates a 48-byte double-buffered param block (0x4000/0x4040/0x4080) and
  indexes per-algorithm data via a pointer at **0x3FFE** (top of ROM).
- **Change detection** (`sub_0527h`): diffs working params (0x4000–0x402F) vs the loaded copy
  (0x4040–0x406F); on change runs `di → sub_071dh → sub_02b6h →` 0x40/0x00 strobe + 16-cycle
  `djnz` settle.
- **End-to-end:** master writes params → slave RAM 0x4000+ → `sub_0527h` detects → `sub_071dh`
  ramps each `{WCS-addr, value}` toward target → `sub_0ecch` RMW-encodes it into the memory-mapped
  WCS plane (+0xBE00 shadow). **Modulation injection points = the WCS addresses in the animated
  list; "modulation" = time-varying values fed to them** — exactly the 480L's open mechanism, one
  generation simpler.

*ARU coefficient encoding — resolved:* the field is **signed** — separate sign control bit +
complemented, ÷4-shifted magnitude, with two field-packing modes (3- or 4-bit). (Settles the
§9 "unsigned /256 vs signed + SIGN bit" question; concrete input to the §8 ARU arithmetic too.)

*Same-ISA bet — holds* (both sessions agree the PCM70 reuses the family model). The **precise
U67 plane field-map** (which plane is opcode vs coefficient vs offset) is still open = **carry-
over 1**. Partial result from this side (the other session didn't load the PCM60 set): with the
PCM60 V1.0 images loaded, a *linear* read of U67's low region shows opcode nibbles matching
PCM60 U43 (n7 ≫ nF/n3 > n0…) and a Phase-1-decoder pass resolves a read/write/MAC structure —
consistent with the opcode/control plane sitting in the low bytes — but this must be re-run
**plane-resolved** to label all 8 planes (U67 is plane-organized, so a contiguous read mixes
fields). *(Supersedes this block's earlier port-streamed / {offset,ctrl} reading.)*

**Gaps CLOSED by Phase 2 (and for the 480L §9):**
- ✅ **Modulation / live-update mechanism** — slave maintains a `{WCS-addr, value}` list pushed
  through a memory-mapped control-store window + RAM shadow + RMW. The 480L's 0x48000-window
  streaming is the bigger-iron version of this.
- ✅ **Coefficient encoding / sign convention** — signed; sign control bit + complemented ÷4
  magnitude; two packing modes.
- ✅ **Live-coefficient streaming pattern** — `sub_071dh` + `sub_0ecch`, RMW touching only the
  coeff/offset field, opcode/control bits intact.
- 🟡 **Parameter smoothing** = multi-rate ramping (de-zipper), not instantaneous writes.

**Gaps STILL OPEN (PCM70):** — *both carry-overs now CLOSED (2026-06, byte-verified; see
`docs/reference/PCM70/PCM70_phase2_results.md`).*
- ✅ **LFO phase accumulator** — **`sub_0ad2h` @0x0AD2**; accumulator RAM word **0x4335**
  (init 0x0010, +1/tick, `AND 7` wrap → 8-page window), sample cached 0x4337, depth-scaled via
  `sub_10d3h`@0x10D3, staged to the 0x40B0 de-zipper queue, committed via `sub_0ecch`. Paced by
  the foreground loop (`CALL`@0x00EF), not the ISR. Triangle/ramp vibrato (waveform-base 🟡).
  Rate = cascaded reload dividers 0x4332/0x4333 from 0x418B/0x418C. **(Carry-over 2 ✅.)**
- ✅ **U67 microword plane field-map** — active 1 KB = 8 plane-major 128-byte pages = **7 static
  control/opcode/routing planes (0-6) + 1 ASCII banner plane (7)**. **No resident offset/coeff
  VALUE planes** — those are slave-assembled at runtime into the WCS. (Per-bit layout identical
  across planes 0-6 — bit5/4/3 fixed; cosine vs PCM60 U43 = 0.94-0.98; the "60-tap offset" was a
  control-byte-pairing artifact.) **(Carry-over 1 ✅.)**
- ✅ **WCS coefficient plane** — the live per-coefficient RMW de-zipper targets **WCS plane 6
  (0x8300-0x837F)** exclusively (`sub_0655h` stamps DE=0x8300+(idx&0x7F); read-back base confirms).
  Planes 3/4/5 get one-shot bulk preloads only. *(Most of the "exact WCS window decode" gap.)*
- 🟡 **Fine sub-role split of U67 planes 0-6** — all control-domain; per-plane→ARU-bit-field
  mapping (banks/sections/routing) not crisply resolved.
- ❓ **Literal PCM70-vs-PCM60 reverb-tap diff** — must run **U95-WCS-source vs PCM60** (U67 has no
  taps; PCM70 assembles its delay topology at runtime from per-algorithm record blocks).

**NEXT STEPS:** (1) re-load PCM60 V1.0, run the Phase-1 decoder on U67 **plane-resolved** + the
literal byte-diff (carry-over 1) — this also yields the byte-level PCM70-vs-PCM60 tap comparison;
(2) isolate the LFO phase routine in U95 (carry-over 2); then (3) **Phase 3 (224XL)** — the
Concert Hall figure-eight tank ancestor (validate integrity first; ARU variant: 2 multiplier
bits + dedicated shift register; adapt the decoder).

*Verified routines/addresses (for resume):* slave ISR `0x02D3` (÷8 BPM) · dispatcher `0x80`
(polls 0x50 + flags 0x4343–0x4348) · plane loader `sub_02b6h` (→ WCS 0x8180/0x8280/0x8300 from
ROM 0x2ACD–0x2C4C) · RMW coeff write `sub_0ecch`/`sub_0e59h` (÷4 + cpl + 3/4-bit field; sign →
ctrl bit 3; mode → ctrl bit 4) · animation/de-zipper `sub_071dh` (`{addr,value}` list, −4/−1
multi-rate ramp; self-loop `jp 0725h`) · change-detect `sub_0527h` (0x4000–0x402F vs 0x4040–
0x406F) · WCS memory-map `0x8000–0x83FF` · write-only-store shadow `0xBE00` · per-algorithm data
pointer `0x3FFE` · read-back base `RAM[0x42EE]` · param double-buffer `0x4000/0x4040/0x4080` ·
ports `0x00/0x30/0x40/0x50`. (Artifacts from that session: `PCM70_U95_slave_disasm_org0.asm`,
`PCM70_phase0_analysis.py`.)

### Phase 3 — 224XL: the Concert Hall ancestor
The figure-eight / Griesinger-Dattorro Concert Hall tank you mapped originates here. The
224XL ARU is a variant (two multiplier bits, dedicated shift register) — adapt the decoder
accordingly. This is the most direct source for the *structure* of the classic hall,
just in a slightly older dialect. (~100 steps.)

**RESULTS — Phase-0 integrity + ROM roles ✅ (set: `ROMs/Lexicon 224/224XL v8_21`, 2026-06).**
Tooling: `tools/phase0.py` (reusable integrity battery), `tools/nvs224_explore.py`, `tools/find_io.py`.

*Integrity (Phase-0 discipline) — PASS.* 11 images (3× SBC 2716 + 8× NVS 2732), **all distinct**
(no dedupe-collapse), **zero Intel-HEX ASCII contamination** anywhere, **no address-line aliasing**
(half/quarter self-compare ≈0.01-0.05; the 0.22-0.41 on NVS5-7 is shared 0xFF-fill / repeated
coefficient structure — like U67's 0.77 — not a mirror). Fill sane (NVS8 active to ~0x0900, FF after).

*ROM roles (Phase-0 classification):*

| ROM(s) | Size | Role | Evidence |
|---|---|---|---|
| **SBC1** | 2 KB ×1 | SBC Z80 **LARC serial comms + boot + power-up self-test** | per LARC doc, "all serial-comms code + checksum diagnostics are in SBC ROM 1"; banner `224XL V8.2 DIAGNOSTICS` = the power-up self-test display; the 0xEE/0xEF I/O = the **LARC serial link** (not a console) |
| **SBC2** | 2 KB ×1 | SBC Z80 **ARU/audio hardware driver** | dense `OUT` to contiguous low-port block **0x00-0x07** (0x03:22, 0x07:18, 0x06:13…) + `IN` 0x00-0x09 — the ARU/DSP interface |
| **SBC3** | 2 KB ×1 | SBC Z80 program directory/load + NVS-bank dispatch | z80-valid 0.999 |
| **NVS1-8** | 4 KB ×8 | **program / microcode / coefficient data** | NVS3@0x0000 = program-name table (`CONCERT HALL / BRIGHT HALL / DARK HALL / RICH CHAMBER / … / M BAND DELAY / SIZE / GATE`); NVS4-8 = coefficient-alphabet bytes (BC/BF/7C/80/01/02) with a rising FF-fill ladder |

*Key structural finding (changes the decode approach):* the 224XL ARU microcode is **NOT** stored
as static repeating byte-planes like the PCM60. No NVS ROM shows a clean ~100-step (or any) period
(autocorr ≤0.11 at every stride); NVS entropies (4.2-7.0) and FF-fill (0.1-42%) are too disparate
for parallel byte-lanes of one word; no ldir/lddr in the SBC. → the 224XL is a **control-computer-
programmed** design (the SBC formats/loads the ARU at runtime via the 0x00-0x07 port block — the
bigger, earlier analogue of the PCM70 slave→WCS path). The microword field map therefore needs the
**SBC disassembly** (find the ARU-load routine + microword bit packing) with the correct memory map,
not a static plane decode.

**RESULTS — ARU interface + memory map + microword field map (2026-06; 5-agent ARU-trace workflow,
byte-grounded at correct load bases).**

*Memory / bank map ✅ (HIGH — flat 64 KB, **NO bank switching**).* Proven by SBC1's reset
ROM-checksum (0x0708-0x0766): phase 2 reads **all eight NVS ROMs linearly across 0x8000-0xFFFF with
no intervening port write** — only possible if all are simultaneously mapped; Z80 also `CALL`s
directly into the window.

| Region | Window | Role |
|---|---|---|
| SBC1 | 0x0000-0x07FF | reset (`JP 0x003B`), RST-0x38 IV fill, ROM checksum, memcpy 0x0614 |
| SBC2 | 0x0800-0x0FFF | boot init (`LD SP,0x4000`), ARU/DSP I/O drivers + power-up self-test (POST) |
| SBC3 | 0x1000-0x17FF | program directory lookups, program load/run, dispatch into NVS banks |
| RAM | 0x4000+ | stack 0x4000; ARU microword RAM image staged at **0x41xx** (4-byte records, stride 4) |
| batt-RAM | 0x3C00-0x3FFF | battery-backed presets / live params |
| **NVS1** | 0x8000 | shared **ARU runtime engine** library (`CALL 0x8000`) |
| **NVS2** | 0x9000 | per-program ("algorithm") control code |
| **NVS3** | 0xA000 | program-name table + 5-byte directory @0xA446 + **loader/interpreter** (0xA791/0xAA9F) |
| **NVS4** | 0xB000 | **math/pack bank** (packers 0xB4F0/0xB4FF, extractors 0xB54D/0xB552); coeff record array @0xB800 |
| **NVS5-7** | 0xC000-0xEFFF | continuation of **21 × 0x2AA (682)-byte** ARU coeff/microcode records (array ends ~0xEFFE) |
| **NVS8** | 0xF000 | variable-length per-program parameter/range records |

> **Note:** the **SBC ROMs are the operational v8.2.1 firmware** (LARC serial UI + boot + power-up
> self-test + program management); the heavy **ARU build engine** lives in the **NVS code banks**
> (NVS1 engine + NVS3 loader/interpreter + NVS4 packer), called by the SBC. *(An earlier draft
> mislabeled the SBC as a "diagnostic image" — corrected; v8.2.1 is the final shipping firmware.)*

*ARU port protocol ✅ (HIGH — pinned by the SBC2 POST walking-bit test 0x0A20-0x0B64, the Rosetta).*
- **0x06** = data LOW byte (write + readback) · **0x07** = data HIGH byte → one **16-bit transfer
  latch**, written low-then-high.
- **0x03** = primary **write strobe** (latches 6/7 into the ARU); `IN 0x03 &1` = **busy/sync
  handshake** → 0x3C71.
- **0x02** = WCS step/sequencer reset + mode/diag latch (also POST error-code display).
- **0x00** = address-counter clear / halt-reset · **0x01** = load-enable (issued before RUN).
- **0x05** = address **auto-increment clock** = the **dedicated shift-register advance line**.
- `IN 0x08/0x09` = overload/peak status + panel switch matrix.
- *Refuted as ARU:* **0xE7** = system PIO/CTC + front-panel strobe (NOT a bank latch); 0xE4/0xE5 =
  panel display; 0xEE/0xEF = console UART; **0x3D00** = boot-test display scratch RAM (NOT a DMA window).
- *Canonical writer* (SBC2 `0x0D1E`): `OUT(0x02)` reset · `OUT(0x00)` clear · `OUT(0x03)` ·
  settle · then per word `LD A,(HL);OUT(0x06)` lo · `LD A,(HL);OUT(0x07)` hi · `OUT(0x03)` latch.
- *Canonical runtime load* (NVS3 `0xACEE-0xAD54`): `OUT(0x00)` halt · timing pads · `OUT(0x02)`
  control · `OUT(0x01)` load-enable · build 0x41xx image (stride 4) · `OUT(0x03)` RUN.

*ARU datapath variant ✅ CONFIRMED (the §3 "2 mult bits + dedicated shift register" prediction):*
- **Two multiplier bits at once** = NVS4 `0xB4F0` coefficient packer: `A=B; CPL; ADD A,A; ADD A,A`
  (= `~field << 2`) then `OR (2 LSBs from a companion table)` → each coeff byte carries a shifted
  main field **plus 2 extra LSBs**. Extractors 0xB54D (`>>2`), 0xB552 (`>>3`).
- **Dedicated shift register** = port **0x05** hardware auto-increment line + software serial
  shift-add multipliers (SBC3 `0x120B`, NVS4 `0xB6FA`).
- **Transport is PORT-based** (like PCM60), **not** a memory-mapped WCS (unlike PCM70).
- Bus is **active-low** (every store preceded by `CPL`); coeff is **sign-magnitude** (bit7=sign,
  NVS4 0xB4FF/0xB531 — the family's sign-in-MSB idiom); **opcode field only ~2 bits** (NVS4 0xB63C
  `AND 3`) vs PCM60's 4-bit nibble.

*Program record format = a packed-bytecode VM (✅ DECODED, byte-grounded; corrects the earlier
"raw 4-byte record" assumption).* A program record is **not** a flat microword array — it is a
**tagged bytecode** that the NVS3 interpreter expands into the microword image. Disassembled at the
correct base (`tools/disrange.py`, `tools/aru224_records.py`):
- Record header carries 13 ring-buffer/range bytes (recbase+0x33 → RAM 0x3CD8, via the interpreter
  @0xAA23). Bytecode stream starts at recbase+0x35 (or +0x44 if recbase+0x30==0xFE).
- **Interpreter loop @0xAA9F:** reads a **TAG** byte = `opcode(bits4-5)<<4 | count(bits0-3)`;
  terminator `0xFF`. Per group it records `{dest_lo, dest_hi, tag}` into a **group table @0x3CF4**
  (for later real-time knob updates), then dispatches:
  - op `0x00` (0xAB26): `count` × index-byte → resolver.
  - op `0x10` (0xAAE8): entries with a **bit-7 flag** selecting an extra literal.
  - op `0x20` (0xAACD): `count` × `{index, literal, literal}`.
- **Resolver @0xAB0C:** `index = byte & 0x7F`; computes `0x4003 + index*4` and writes that **pointer**
  into the image — i.e. the image is *linked* to 4-byte coefficient slots in the **0x4003-0x41FF RAM
  table** (the same region the ARU latch image lives in → a self-referential link table).

*Microword build mechanism (✅ DECODED — confirms the field map).*
- **Offset/delay** = 16-bit **`offset = pointer − write_ptr`** via `0xB714` (`HL=HL−BC`); **delay =
  −offset** — the exact PCM60 `U38:U32` semantics. Step-builder `0xB55B` walks the delay structure
  with **ring-buffer wrap** against bounds at **0x3CD8/0x3CDA/0x3CDC/0x3CDE** (the delay-RAM extent
  = the MMU equivalent), and scales addresses via the shift-register multiply `0xB6FA` (`<<4`).
- **Coefficient = sign-magnitude across 2 bytes** (packers 0xB4F0/0xB4FF, byte-confirmed):
  - HI byte (`0xB4FF`): `bit7 = SIGN`, `bits6:0 = 7-bit magnitude`.
  - LO byte (`0xB4F0`): `bits7:2 = (~coarse) << 2`, `bits1:0 = 2 LSBs` from a companion fetch — the
    **"two multiplier bits at once"** packed into the low byte. Extractors 0xB54D (`>>2`)/0xB552 (`>>3`).
  - Fetch `0xB510`: `A = (recbase + 0xC0AA + DE)` — the coefficient source is record-relative.
- **Step count** seed = 0x10 at 0xB55B (`SUB 0x10` → 0-based index); the build terminates on the
  bytecode `0xFF`, so step count is **data-driven per program** (≈100, to confirm by emulation).

*Program selection path ✅:* program# → 5-byte directory @0xA446 (`{flags, group, sub, page-hi,
page-lo/len}`; 22 entries + 0xFF terminator) → per-program NVS2/NVS3 code (page-hi 0x96-0xB0) +
the 21×682-byte record array @0xB800 → interpreter expands → image @0x41xx → ARU via the
0x00/0x02/0x01/0x03 strobes; knob moves rewrite only affected coeff bytes via the 0x3CF4 group table.

*Build emulation + reverb tap map ✅ (the validation — ran the ACTUAL firmware build code).*
A pure-Python Z80 emulator (`tools/z80emu.py`, self-tested: the ROM's `0x120B` shift-add multiply
and `0x0B714` subtract give correct results incl. carry) executes the real step-builder `0xB55B` and
the interpreter `0xAA9F` on a program record (`tools/aru224_emulate.py`). The step-builder writes a
128-word offset buffer (downward from 0x3F4D); decoded (delay = −offset) it yields a **sane reverb
tap map** for every record tried:

| Record | active steps | distinct taps | range (samp) | allpass pairs | recirc-loop tap | output multi-tap line |
|---|---|---|---|---|---|---|
| @0xB800 (rec 0) | ~104 | 63 | 128 … 12353 | 25 | 6008 ×4 | 5-tap run @step13 |
| @0xBAAA (rec 1) | ~99 | 61 | 128 … 12353 | 16 | 706 ×6 | — |
| @0xBD54 (rec 2) | ~107 | 59 | 16 … 12353 | 14 | 4097 ×11 | **17-tap line** 3327→8867 (Δ312–439, incommensurate) |

Structure recovered (the Concert Hall figure-eight signature): input/diffuser **allpass pairs**
(small paired taps 80/81, 208/209, 242/243, 616/617 …), a **recirculating loop** referenced by one
heavily-reused fixed tap (rec 2: 4097 ×11), a spread of long delays, and a terminal **monotonic
multi-tap output delay line** (rec 2: 3327, 3659, 3975, 4332, 4770, 5094, 5533, 5901, 6281, 6670,
6982, 7367, 7762, 8100, 8497, 8867 — incommensurate Δ312–439, the dense output taps of a reverb).
The **`−1` (0xFFFF) fill** after the program puts the **active length at 99–107 steps — empirically
confirming the ~100-step prediction**. This **validates the 224XL microword field map** (offset lane
→ delay) and the build mechanism end-to-end. (The directory-globals 0x3CCE/0x3CCF only set the
ring-buffer *base*, which cancels in offset = ptr − write_ptr, so the *relative* topology — pairs,
loop, output line, step count — is exact even with them seeded 0.) Tooling: `tools/z80emu.py`,
`tools/aru224_emulate.py` (`show_tap_map`).

*Coefficient gains ✅ DECODED (the other half of the algorithm).* Hooking the source-fetch `0x0B510`
during the interpreter run (`capture_coeffs`) recovers the per-tap coefficients, which decode cleanly
as **sign-magnitude / 127** — textbook reverb gains, applied in pairs to the allpass read/write taps:

| coeff byte | decode | role |
|---|---|---|
| `0x7C` | **+0.976** | recirculating-loop feedback (just under unity → long decay) |
| `0xBF` | **−0.496 ≈ −½** | the classic Schroeder/Griesinger **allpass coefficient** |
| `0xE7` | −0.811 | diffuser/comb gain |
| `0xDC` / `0xE4` | −0.724 / −0.787 | diffuser gains |
| `0x97` | −0.181 | low-gain tap |

So **delays + gains together = the recovered 224XL reverb algorithm** (input/diffuser allpasses at
±0.5, a ~0.976 recirculating loop, comb/diffusion gains, and the multi-tap output line) — for the
first three program records, with the method proven for the rest.

**Operational boot via the LARC — v8.2.1 IS the operational firmware ✅ (CORRECTED).** *An earlier
draft of this doc wrongly called v8_21/v8_1A "diagnostic-only ROMs." That was a mistake — see
`docs/reference/224/Lexicon-224-info.md` + `LARC_Theory_of_Operation.md`.* The 224XL replaced the
224/224X's **parallel** control head with the **LARC** (Lexicon Alphanumeric Remote Control), which
talks to the SBC over a **serial 8251 link** (ports 0xEE data / 0xEF status). So the serial port the
earlier draft mistook for an "RS-232 diagnostic terminal" is in fact **the primary user interface**;
the `224XL V8.2 DIAGNOSTICS` string is the **power-up self-test banner shown on the LARC**, after
which normal operation proceeds. v8.2.1 is the final shipping 224XL firmware.

**Proven by emulation (`tools/z80emu.py` now has IM1 interrupt support):** with a minimal LARC model
(8251 status + the LARC's `0xC8` "I'm here" handshake reply, + periodic UART interrupts driving the
IRQ-driven serial ISR at `0x03EE`), v8.2.1:
1. completes the LARC handshake (`0x0067 OUT 0xEE,0xE0` → LARC replies `0xC8` → `0x0084 CP 0xC8` →
   `JP 0x0703` main),
2. runs power-up diagnostics and **drives the LARC alphanumeric display** — captured serial TX decodes
   to ASCII: `224XL V8.2  DIAGNOSTICS ****…` then `DIAG ERROR  TYPE E32  C=55 B=FF BIT1 ADDR=3FFF`.

That `DIAG ERROR` is the firmware's **power-up self-test of the DSP hardware** (DMEM / ARU / WCS,
reached via the X-register I/O ports) — which this **SBC-only emulator doesn't model** (the ports
return stub values, so the test reads `C=55` vs expected `FF`). So the firmware stops at the self-test
*before* normal program-load — an **emulation-completeness** gap, **not** a missing-ROM gap.

**LARC↔SBC serial protocol decoded** (from the SBC ISR `0x03EE`/`0x0413`): bytes with bit6 clear =
slider/pot data; bit6 set = commands keyed by `B&0x38` (a plain keypress → `RAM 0x3c11`; multi-byte
messages via a `0x3c15` state machine); `0xC8` = the power-up handshake. The **program name is sent
SBC→LARC as ASCII to the DL-1414 displays** — so once past the self-test, capturing the serial TX
yields the displayed program name, giving **record→name directly**.

**Path to record→name (clear, machinery mostly built):** model the DSP power-up self-test responses
(the X-register / DMEM / WCS ports) enough to pass it → firmware reaches normal operation and loads the
power-up program (DIP-switch-selected) → then inject LARC PROG-button keypresses (`→0x3c11`) to cycle
all programs, capturing the WCS algorithm + the TX name for each. The decoded **delays + gains** above
stand regardless.

**BONUS — original-224 static ARU microcode recovered from the OTP mask ROMs ✅** (`tools/otp224_decode.py`).
The 4 `ROMs/Lexicon 224/OTP` ROMs (35004016–18, 2 KB each) are **parallel byte-lanes of one static
microword — the PCM60 format** (no SBC/build needed):

| OTP ROM | lane | evidence |
|---|---|---|
| `..._4` | control/opcode | low-nibble `7:1056 3:352 F:304 0:128 B:96` = the family opcode alphabet; **autocorr@128 = 1.0, exactly 1 unique frame** = 128-step program × 16 param frames |
| `..._3` | offset HIGH | FC/FB/FE sign-extended negatives |
| `..._1` | offset LOW | sparse |
| `..._2` | coefficient | smooth descending envelope ramps |

Structure = **1 reverb program × 16 parameter frames** (`ctrl` lane = **1 unique 128-byte frame** =
fixed topology; `offhi` = **16 unique** frames, `offlo`/`coeff` = 5 each → a parameter sweep, almost
certainly the **reverb-time/size** control). Decodes to a sane tap map every frame (82–92 taps,
**0.3 … 562 ms** at 34.13 kHz) with the **identical PCM60 field map** (16-bit signed offset → delay;
coeff /256 with the ×0.5 scalar; control low-nibble opcode n3/n7/nF/n0). The manual notes reverberant
measurements use the **Concert Hall** program → the OTP is very likely the original-224 Concert Hall.
**vs PCM60: ISA-identical siblings, distinct tuning** (control 45% exact / 60% within-8; coeff
envelope 81% within-8; ~11% shared taps). Confirms the family-tree ISA premise in concrete bytes.

**The microcode → firmware divergence (per the service manual + the dumps).** The 224-family ARU
runs a **100-step WCS** (4×128×8 SRAM = 32-bit microword) at **34.13 kHz**, loaded by the SBC; the
microword's low 16 bits = a data-memory **offset subtracted from a current-position counter** (delay
= position − offset), the upper 16 = 6-bit signed (CSIGN) coefficient + 4×16 register-file addresses +
control; the multiplier is **16×6-bit, two shift-adds at once via a dual-rank shift register, with
saturation** (the "2-mult-bit + shift-register" datapath — *standard* 224, not XL-specific). The
**original 224 (OTP) shipped the program as STATIC mask-ROM microcode**; the **224X/224XL moved to
SBC-LOADED firmware** that *builds* the WCS at 0x4000–0x41FF (the bytecode VM + step-builder decoded
above). Same ARU, two delivery eras.

**Manual cross-check ✅:** every 224XL field I recovered by emulation is confirmed by the 224X Service
Manual §3.5–3.7 — WCS @0x4000–0x41FF (4-byte step), offset=position−microword (delay), 100 steps,
34.13 kHz, sign-magnitude coefficient + saturation, dual-rank-shift multiplier. So the decoded
delays+gains are now corroborated by the authoritative source, and delays convert to ms at 34.13 kHz
(e.g. rec 2's output line 3327–8867 samp = **97–260 ms**).

*(Correction note: an earlier draft here claimed v8_21/v8_1A were "serial-terminal diagnostic service
ROMs, not operational firmware, record→name needs an operational ROM dump." That was WRONG — the
serial port is the **LARC** user interface, not a diagnostic terminal, and v8.2.1 is the operational
firmware. Superseded by the "Operational boot via the LARC" results above.)*

**OPEN / NEXT (Phase 3 cont.):**
- 🟡 **record→name labels — reachable, not blocked.** Next step: model the DSP power-up self-test
  ports (X-register/DMEM/WCS) so v8.2.1 passes self-test → loads the power-up program → then inject
  LARC PROG keypresses (`→0x3c11`) and capture WCS + the DL-1414 ASCII name per program. (22 names
  already decoded @0xA001: CONCERT/BRIGHT/DARK HALL, RICH CHAMBER, ROOM, SMALL ROOM, CHAMBER, PLATE,
  CD PLATE A/B, SMALL PLATE, CHORUS&ECHO, RES CHORDS, M BAND DELAY, HALL/HALL, PLATE/PLATE, PLATE/HALL,
  PLATE/CHORUS, SIZE GATE, SIZE 1/2 — pending only the record↔name link.)
- 🟡 **all 21 records** — records 0/1/2 fully decoded (delays + gains); the @0xB800 array's exact
  boundaries for 3–20 need the real scan routine (the inferred 0x2AA stride misaligns past rec 2).
- 🟡 sample→ms at the 224 sample rate (cosmetic; absolute-delay base cancels in the offsets).
- ✅ **tooling reusable for the family:** `tools/z80emu.py` + the hook pattern carry straight to
  **M300 / 480L** — run their real loaders the same way to recover delays + gains.
- ❓ Hardware behavioral validation (the §8 ARU-quirks caveat) remains the final confirmation.

### Phase 4 — M300: the 480-family algorithms in Lexichip form
Crossing into the Lexichip generation, but now fluent in ARU microcode. The M300 carries
the actual late 480-lineage algorithms (Random Hall, Ambience, Stereo Adjust, Rich Plate)
in a microcode dialect that's *very similar but not identical* to the 480L. Characterize
the delta (repurposed control bits, 96-step program, bank select). This is where the
specific cart-delivered 480L algorithms become readable.

### Phase 5 — 480L: assemble the target
With the ISA, the modulation mechanism, the hall structure, and the late-algorithm dialect
all in hand, return to the 480L and resolve its specific complications:
- 80-step × multi-core program layout and how the cores interleave.
- The program/algorithm microcode source (firmware-resident vs program-cartridge) and how it's
  DMA'd into the slaves (the live parameter/coefficient streaming routine — still ❓).
- Map decoded microcode onto the open topology uncertainties (§9).

### Optional — PCM80/81
Lowest value for this goal: the reverb path is Lexichip-internal and tangled with the
56002 effects engine; heritage traces to the PCM70 you'll already have decoded.

---

## 6. Method per dump (repeatable recipe)
1. **Split** Z80 code from microcode (Phase 0 heuristics).
2. **Z80 / 68k code** → standard disassembly. Use `z80dasm` for the Z80 parts (capstone has
   no Z80 support); capstone for any 68008 host code (480L).
3. **Microcode** → run the custom microword decoder; emit a per-step listing of
   {delay offset, coefficient, routing, control}.
4. **Reconstruct topology** from the listing (delays + allpasses + loop + taps).
5. **Validate** against a known-good reference (the PCM60's static hall; your existing
   480L topology synthesis).
6. **Characterize arithmetic** empirically where the dump is ambiguous (rounding, saturation).

---

## 7. Tooling
- `z80dasm` (Z80 host/slave code) · `capstone` (68008 host code, 480L).
- Custom **Python microword decoder**, parameterized by word width + field map (reused
  across boxes with per-device field tables).
- Entropy / autocorrelation scan to find microword stride (Phase 0).
- Bash for slicing/`base64`/byte-bucketing as before.

---

## 8. Known hazards
- **The chips have quirks.** Per a Lexicon algorithm developer: across this whole family
  there were operations dependent on DSP-fed wait-states + cycle counting, microcode words
  that were meaningless, and words that didn't do what the encoding implied. A clean
  disassembly still needs **behavioral validation on real hardware**. 🟡
- **ARU arithmetic ≠ naive fixed-point.** Hardwired shifts, rounding-toward-zero, and
  the 12/13-bit converter asymmetry mean a literal "multiply and quantize to 16 bits" will
  *not* match. Decode the actual shift/round idioms.
- **224XL and Lexichip are dialects**, not the same decoder — budget per-device field tables.
- **480L multi-core interleave** is the last and hardest structural puzzle; defer it to Phase 5.

---

## 9. Open 480L questions to resolve (carried from topology work)

*Phase 1 note: the PCM60 decode proved the method end-to-end and resolved the PCM60
analogues of the first two items below (delay lengths, decay-gain → coefficient scaling,
the ×0.5 scalar). These remain open for the **480L specifically** until Phase 5, but are
no longer methodologically blocked.*

- ❓ Exact delay-line lengths and allpass coefficients. *(decoder proven on PCM60; the
  `U38:U32`-style 2's-complement offset → delay readout transfers to the 480L's wider word.)*
- ❓ Decay-gain distribution (which gains sit inside which allpasses). *(PCM60: decay knob
  scales the coefficient lane, deepest taps fastest — same pattern expected on 480L.)*
- ❓ Damping-filter specifics.
- ✅/🔄 Modulation injection points (LFO → which delay taps) — **Phase 2 found the
  mechanism** (slave-side, U95): the slave keeps an animated list of `{WCS-addr, value}`
  entries (`sub_071dh`), ramps each value (multi-rate de-zipper), and RMW-encodes it
  (`sub_0ecch`) into a **memory-mapped WCS window (~0x8000) with a 0xBE00 RAM shadow**.
  Injection points = the WCS addresses in that list; "modulation" = the time-varying values.
  The *general model* is now answered; the **480L-specific tap targets** remain ❓ until
  Phase 5. (This is the one-generation-simpler analogue of "slave loads WCS, then live-updates"
  — the 480L's `0x48000`-window streaming is the bigger-iron version.)
- ❓ Output-tap map / inter-stage density taps.
- ❓ Live parameter/coefficient streaming routine in the host firmware (distinct from the
  boot-time HALT probe; uses the same `0x48000` windows).

---

## 10. References
- Lexicon 480L Service Manual — Ch. 4 (Circuit Description), Ch. 6 (Parts Lists). *(project)*
- 480L host ROM disassembly + memory-map notes. *(project / our work)*
- Griesinger, "Practical Processors and Programs for Digital Reverberation." *(project)*
- Gearspace "reverb subculture" thread — developer/reverse-engineer commentary. *(project)*
- ARU/Lexichip teardown notes, 10000cows.com (Lexicon ARU page) — generational map,
  microword similarity, per-device step counts. 🟡
- Product/architecture confirmations: Sound on Sound (PCM81/91), vintagedigital (M300),
  gearspace (300/300L). 🟡

---

*Roadmap is strategy + confidence-tagged facts; the ARU microword decoder built in Phase 1
is the linchpin deliverable that unlocks every subsequent phase.*
