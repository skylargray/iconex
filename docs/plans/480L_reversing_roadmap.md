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
Phase 2 ✅ core done (PCM70 architecture + modulation mechanism; same-ISA confirmed) ·
Phase 3 (224XL) → next. See the per-phase RESULTS blocks in §5.

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
- ❓ Exact coefficient **sign/scaling convention** (unsigned /256 vs signed + control
  SIGN bit) and **rounding-toward-zero / saturation** — same class as §8; wants hardware.
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

**RESULTS ✅ core done (V2.0 set: U62/U67/U95, 2026-06).** Dumps clean (no corruption).

*Architecture* — exactly the "PCM60 + Z80(s)" the roadmap predicted:

| ROM | Size | Role |
|---|---|---|
| **U62** | 32 KB | **Master Z80 firmware** (©1986). Boots `JP 0x1800`; runs UI + DSP control + modulation. Holds reverb program names (CONCERT HALL, RICH PLATE/CHAMBER, INFINITE CHAMBER…) |
| **U95** | 16 KB | **"SLAVE AND SPACEWARE V1.20"** — slave Z80 code (~0x60–0x18FB) **+** SpaceWare program data (120-byte records @0x1957+: CHORUS, ECHO FLANGE, PAN/CIRCULAR DLYS…) |
| **U67** | 8 KB | **"PCM70 OPCODES V1.20"** — ARU control-word microcode (~1 KB), the analogue of PCM60 U43 |

*The delta = a writable, Z80-streamed control store + modulation* (the PCM60 had a static
parallel ROM addressed by knobs). The **slave Z80** loads each program's base
microcode/coeffs into the DSP (OUT to ports 0x30/0x40 with strobe handshaking on 0x00).
The **master Z80** then continuously modulates it via a **timer ISR** (RST38 → 0x1855):
a free-running counter + a **0–15 LFO phase in bit-reversed order** (table @0x191C =
`00 08 01 09…`, spreading 16 updates evenly), which each tick **selects one of 16
control-store slots** (walking-bit strobe on ports 0x10/0x20) and **writes that slot's
data** (ports 0x30/0x40) from RAM tables (0x9C03/0x9BF3) holding the current modulated
values. That timed slot-refresh is the live-update substrate for chorus/flange/pan motion.

*Same ARU ISA — confirmed.* U67 opcodes use the **identical opcode vocabulary** as PCM60
U43 (same low nibbles in the same rank order: n7 ≫ nF/n3 > n0=WRITE > nB/n8; matching
high nibbles), and a U67 block run through the **Phase 1 decoder** resolves into the same
READ/WRITE/MAC structure (setup section → long sustained-MAC tank). The microword
encoding (16-bit signed offset → MMU, 8-bit coeff, control/opcode) and the decoder carry
over directly. ✅ This validates the roadmap's central bet that the family shares one ISA.

**Gaps CLOSED by Phase 2:**
- ✅ PCM70 architecture (master Z80 / slave Z80 + SpaceWare / opcode ROM) and its diff vs PCM60.
- ✅ The **modulation / live-update mechanism**: timed ISR rewriting control-store slots with
  LFO-modulated offset/coeff values — directly models the 480L's "slave live-updates WCS".
- ✅ Same-ISA confirmation: the PCM60 decoder transfers behaviorally to the PCM70.

**Gaps STILL OPEN (PCM70):**
- ❓ **Per-program tap field-map.** *Progress:* programs are stored as **120-byte packed
  blocks** (U95 @0x1957+: name@+0x00 (13B) + zero-pad + data region from ~+0x2C). The
  parameter-entry format is confirmed from the `0x071D` code: **`{16-bit LE offset, ctrl
  byte}`**, offset 2's-complement (delay = −offset), ctrl carrying the same opcode nibbles
  as U67/PCM60 — e.g. `0E 9A 0F` → −26098-sample tap, ctrl `nF`=R/MAC. So the **offset
  encoding matches the PCM60**; the *layout* (packed block) does not. **Remaining:** the
  data region interleaves offsets, coeff runs (`C2 C8 5A CE…`) and symmetric mod patterns
  (`99 CE 32 D8 32 99 CE`) — to label which bytes are taps vs coeffs vs mod-depth, trace the
  **unpacking routine** that fills `0x41xx` working RAM from the block at program-select
  (the list `0x071D` walks via pointer `(0x41FA)`). Then a byte-level PCM70-reverb-vs-PCM60
  tap comparison is possible. Also confirm where the **reverb** blocks (CONCERT HALL etc.)
  live — names are in U62; data blocks may be in either ROM.
- ❓ Exact **port→lane mapping** (0x10/0x20 = select strobe; 0x30/0x40 = data — which lanes:
  offset-hi/lo vs coeff/control) — same flavor of task as the PCM60 MMU mapping.
- ❓ The modulation-compute code that fills 0x9C03/0x9BF3 (the actual LFO depth/waveform → tap math).

**NEXT STEPS:** (1) **[in progress]** trace the block-unpack routine (ROM 120-byte block →
`0x41xx` RAM, the list `(0x41FA)`/`0x071D` walks) to label the tap/coeff/mod fields, then lay
a specific PCM70 reverb's tap map beside the PCM60 baseline; (2) trace the 0x9C03/0x9BF3 fill
code for the exact LFO→tap math; then (3) proceed to **Phase 3 (224XL)** — the Concert Hall
ancestor — adapting the decoder for the 2-multiplier-bit variant.

*Key addresses for resume:* entry walker `0x071D` (reads `E=(HL),D=(HL+1),A=(HL+2)`; ramp =
SUB 4 / SUB 1 on bit-7 of ctrl; writes DSP via `CALL 0x0ECC`); working-list pointer `(0x41FA)`
in slave RAM; program blocks @0x1957+ (U95), 120-byte stride, data region ~+0x2C; DSP data
ports 0x30/0x40, strobe 0x00, slot-select 0x10/0x20; modulation RAM tables 0x9C03/0x9BF3;
LFO phase table @0x191C (master U62).

### Phase 3 — 224XL: the Concert Hall ancestor
The figure-eight / Griesinger-Dattorro Concert Hall tank you mapped originates here. The
224XL ARU is a variant (two multiplier bits, dedicated shift register) — adapt the decoder
accordingly. This is the most direct source for the *structure* of the classic hall,
just in a slightly older dialect. (~100 steps.)

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
  mechanism**: the control processor live-rewrites control-store *slots* on a timed ISR
  refresh (16 slots, bit-reversed LFO phase, modulated offset/coeff data streamed to the
  DSP). The *general model* is now answered; the **480L-specific tap targets** remain ❓
  until Phase 5. (This is the live-update analogue of "slave loads WCS, then live-updates".)
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
