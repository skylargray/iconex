# 224XL — L4 / L5 / L6 decomposition (the ARU, broken into bottom-up atoms)

> Companion to [`224XL-interp-stack.md`](224XL-interp-stack.md) (the L1–L7 stack) and
> [`224XL-bottom-up-continuation.md`](224XL-bottom-up-continuation.md) (handoff). L1–L3 (the 8080 side)
> are ✅ VERIFIED. This doc expands the three inference layers — **L4 microword field decode**,
> **L5 address arithmetic**, **L6 ARU datapath** — into the smallest independently-verifiable components,
> each with: what it is, status, **its ground-truth validator**, dependencies, and open risk. Same rule
> as the top stack: a component is ✅ only when proven by something independent of our own interpretation.

## Validators available for the ARU (what counts as ground truth here)
We can't run the ARU/T&C hardware, so every L4–L6 atom must be pinned by one of:
- **[POST-step]** — the firmware's own self-test, which **single-steps** the ARU via ports (latch 0x0A1D,
  register 0x0C48, multiplier 0x0942, DMEM 0x0B75). Certifies a primitive/field **only for the microword
  patterns the test distinguishingly varies** (a wrong-but-consistent decode can alias — see the POST
  coverage analysis, being adversarially verified in `wf_73bb6dc6`). Single-step ≠ free-run.
- **[schematic]** — owner net-trace of the relevant chips (ARU 060-01318, T&C 060-02475, DMEM 060-02512).
  The only validator for the **free-run control path** the SBC never exercises.
- **[hardware]** — measurement on a real unit (probe DMEM / result reg / a tap while running a known
  microprogram). The gold standard for free-run; currently unavailable.
- **[cross-pipeline]** — agreement between two independently-built decoders (weak: two guesses can agree).

> **★ The single biggest structural fact:** POST proves the ARU's **datapath primitives** (in single-step) —
> and it now DOES (the whole POST passes un-suppressed: latch/register/multiplier/DMEM). The **static wiring**
> is also done: the M0b netlist (`224XL_interconnect_netlist.md`) is the owner's full schematic trace of the
> control path. What remains is the **free-running execution** (T&C 100-step sequencing + per-step DAB routing
> + cross-step MAC timing + recirculation) — which produces the reverb and is where every failure lived. It is
> now assembled in a **phase-accurate RTL model** (plan 013 M1/M2, `tools/aru_rtl*.py`) and, as of 2026-06-29,
> **built as a running free-run engine** (plan 013 M3, `tools/aru_freerun.py`): the loop now CLOSES once the
> per-step delay offsets come from the firmware 0x3F4D buffer (`tap_map`) instead of the WCS 0x4000 lanes 0/1
> (that wrong source was **the dead-tank root cause**). A real-unit IR (or single-step port capture) is the
> final check.

Status legend: ✅ VERIFIED · 🔶 PARTIAL/IN-PROGRESS · ❌ FAITH (unproven) · ⬜ PENDING.

---

# L4 — Microword field decode (4 bytes → control fields)

**Input:** the 4 bytes of a step from the firmware-built WCS image (L3, ✅ — bytes are real).
**Output:** the per-step control fields the ARU acts on.
**Why hard:** the bit→meaning map is human-schematic-read; POST validates a field only where it
distinguishingly varies it. Decompose by *field*, foundation first.

| ID | Component | What it is | Status | Validator(s) | Depends on |
|---|---|---|---|---|---|
| **L4.0** | **Lane layout & polarity** | l2=MI16–23 **direct**, l3=MI24–31 read **complemented** (`~l3`); the "skip if l2==l3==0xFF" NOP rule | 🔶 LARGELY VERIFIED | [schematic] netlist §G3R; [POST-step] every test patches l2/l3 and POST passes un-suppressed → the byte layout is right | — |
| **L4.1** | **OFFSET field** | MI0–15 = 16-bit offset (l0,l1); the microword OFST is stored **COMPLEMENTED** (OFST/), adder carry-in high → addr = CPC + OFST_stored + 1 | 🔶 PARTIAL | **[PARTIAL]** the DMEM test E91 drives a **nonzero** offset (OFST/=0xDFFF → 0x2000) and passes; netlist §G3R/§5.2. Open: offset *variation* (one value tested) + dual-use bits 12/13 | L4.0 |
| **L4.2** | **MI16 / MI17 device bits** | MI16=device-select, MI17=MEMAC; `(MEMAC,MI16)` = (1,1) read / (1,0) write / (0,1) sub / (0,0) NC | 🔶 PARTIAL | [schematic] netlist §2T.1; [POST-step] passing POST exercises (1,0) MEMW (DMEM test) + (0,x) compute. (1,1) MEMR not distinctly varied | L4.0 |
| **L4.3** | **WA (write reg addr)** | b2 bits 2–3 → which of 4 registers is written | 🔶 PARTIAL | **[PARTIAL]** verified: POST pins WA∈{b2,b3} (transpose & same-bits aliasing DISPROVEN); intra-field order/polarity unpinned | L4.0 |
| **L4.4** | **RA (read reg addr)** | b2 bits 4–5 → which register feeds the multiplier | 🔶 PARTIAL | **[PARTIAL]** verified: POST pins RA∈{b4,b5}; order/polarity unpinned (joint symmetry with WA) | L4.0 |
| **L4.5** | **CSIGN** | b2 bit 7 → coefficient sign | 🔶 PARTIAL | **[PINNED-narrow]** verified: POST mult test pins "bit7 toggles product sign"; the polarity label is convention | L4.0 |
| **L4.6** | **XFER** | MI24 (`~l3` bit0) → XFER CK loads the result register from the accumulator | 🔶 NET-TRACED | [schematic] netlist §G3R + §6T.4 (XFER CK=tc_U36). Still **[UNCOVERED by POST]** (XFER=0 in every POST microword); but the XFER=0 single-step read-back path is now understood — it bypasses the XFER-gated load via the X-register (scout) | L4.0 |
| **L4.7** | **ZERO** | MI25 (`~l3` bit1) → ZERO/ clears the accumulator | 🔶 LARGELY VERIFIED | [schematic] netlist §G3R + §2T.3 (ZERO/=tc_U48); [POST-step] passing the multiplier + DMEM tests **requires** ZERO clearing the accumulator each step (ZERO=1 throughout) | L4.0 |
| **L4.8** | **Coeff magnitude** | MI26–31 (`~l3` bits2–7) → 6-bit coeff C0–C5, serialized M0=C4,C2,C0 / M1=C5,C3,C1 | 🔶 LARGELY VERIFIED | [schematic] netlist §4F + §3.9; [POST-step] the **gate-level Booth model** (`aru_booth`) reproduces all 20 multiplier goldens bit-exact across cmag 21/42/63 + unity → the coeff bit→weight wiring is pinned by the verified gates (no longer just 3 codes) | L4.0 |
| **L4.9** | **Sub-decoder select** | offset bits 12,13 = MI12,MI13 (dual-use as address + device-sub-select) | ❌ FAITH | [schematic] U47 sub-decoder; **dual-use is a key risk** (control bits inside the "offset") | L4.0, L4.1 |
| **L4.10** | **MI4 gate** | offset bit 4 gates the sub-decoder (U34A) | ❌ FAITH | [schematic] only | L4.1 |
| **L4.11** | **PROT / MI22 etc.** | b2 bit 6 and any leftover bits | ⬜ UNKNOWN | [schematic] | L4.0 |

**L4 exit criterion:** every field bit either (a) distinguishingly varied by a POST test our model passes,
or (b) net-traced on the schematic. Bits that no test varies and no trace covers stay ❌.

---

# L5 — Address arithmetic (offset → physical DRAM cell)

**Input:** the OFFSET field (L4.1) + the CPC.  **Output:** the 17-bit DMEM address (16-bit within-bank + bank).
**Why hard:** the reverb's whole delay structure *is* this arithmetic; and POST may not exercise it (POST
appears to supply the address via the CPC at offset≈0, never testing `CPC − offset` for nonzero offsets —
**being adversarially verified in `wf_73bb6dc6`**).

| ID | Component | What it is | Status | Validator(s) | Depends on |
|---|---|---|---|---|---|
| **L5.1** | **CPC** | Current-Position Counter (dmem_U51/U65, 16-bit); +1 per sample (free-run) / +1 per single-step strobe (POST); cleared by OUT 0x05 (CPC CLR) | 🔶 LARGELY VERIFIED | **[PINNED, single-step]** the DMEM test E91 certifies CPC auto-increment + unique addressing across the 64K sweep (passes). The +1/**sample** free-run cadence is [schematic] only (the count-clock source is un-traced) | — |
| **L5.2** | **The subtract** | `addr = CPC − OFST` (OFST stored complemented → CPC + OFST_stored + 1) | 🔶 PARTIAL | **CORRECTION (was "provably UNCOVERED, offset=0"):** the **dedicated** DMEM test (0x0B75) drives a **nonzero constant offset** (OFST/=0xDFFF → 0x2000) with the CPC walking, and a faithful `CPC−OFST` model **passes E91**. So the adder IS exercised — at one offset value. Open: offset *variation* + the dual-use bits 12/13 | L5.1, L4.1 |
| **L5.3** | **Active-low + carry-in impl.** | adder adds `OFST/` (complemented) with carry-in tied high (dmem_U49/U50/U63/U64) → two's-complement subtract | 🔶 LARGELY VERIFIED | [schematic] netlist §5.2 (carry-in dmem_U49.pin7=+5V); the model with this addressing passes E91 | L5.2 |
| **L5.4** | **OFFSET→adder wiring** | which offset bits feed which adder inputs (straight order); the dual-use bits 12/13 (L4.9) | 🔶 NET-TRACED | [schematic] netlist §5.2 net-by-net; **the dual-use bits 12/13 are the residual risk** (not POST-varied) | L5.3, L4.9 |
| **L5.5** | **Top carry-out** | the adder top carry-out `dmem_U64.pin9` — **n/c.** There is NO bank: single 64K×16, no bank-select | ✅ RESOLVED | [schematic] netlist §5.5/§G3D. **CORRECTION: the old "carry-out=17th bit=bank / flat 128K" is wrong** — `dmem_U1–U16` unpopulated, `CAS1/` hard-disabled | L5.3 |
| **L5.6** | **DRAM row/col mux** | dmem_U18/U36 multiplex row/col onto the 8 DRAM addr lines; physical cell = linear addr | 🔶 LARGELY VERIFIED | [schematic] netlist §5.3/§5.4; [POST-step] the DMEM test's all-64K write/read sweep (E91 passes) covers address integrity | L5.5 |
| **L5.7** | **Physical DMEM org** | ONE bank of 16×4164 (dmem_U20–U35), bit-sliced (column i → DABi), DIN/DOUT to the DAB | ✅ (owner-traced) | [schematic] netlist §5.5. (**Single bank** — `dmem_U1–U16` not populated; not 2 rows/banks) | — |
| **L5.8** | **delay = offset samples** | a delay tap reads `CPC − OFST`, i.e. OFST samples back; realized recirc delay set by the offset values | 🔶 PARTIAL (free-run) | **★ SOURCE CORRECTED (2026-06-29):** the per-step delay offsets do **NOT** come from the WCS 0x4000 lanes 0/1 (those give clustered ~0.9–1.7 s / ≈30000-sample GARBAGE → DMEM read/write address disjoint regions → DEAD TANK; this was the `tools/aru_freerun.py` root-cause bug). The REAL ms-scale per-step offsets live in the firmware **0x3F4D** offset buffer, extracted by `tools/aru224_emulate.py::tap_map(0xB800)` (B55B builder; byte-identical to the firmware load). The offset↔control per-step alignment is **CONFIRMED step-index-keyed**: `tap_map[s]` aligns with the 0x4000 COEFFICIENTS[s] (CONCERT step 0 = 362 ms predelay; steps 5–23 = varied 7–176 ms diffuser cluster; 176 ms recirc reused 4×). With the corrected offsets the loop CLOSES (output went dead 2–4 samples → dense field). 🟡 offset sign/encoding still being pinned (M3). CAVEAT: `tools/boot8080.py::read_offsets` reads a CONTAMINATED 0x3F4D (576 ms for step 2 vs 176) — use `tap_map` | L5.2 |

**L5 exit criterion:** the `CPC − OFST` adder (active-low offset + carry-in high; single 64K bank) is
net-traced AND exercised — **the DMEM test E91 now drives a nonzero constant offset (0x2000) and passes**, so
the adder + CPC walk are covered at one offset. Residual: offset **variation** (only one value tested) + the
dual-use bits 12/13, both confirmable only by free-run (M3) or hardware.

> **★ Free-run offset SOURCE (2026-06-29):** the per-step delay offsets fed to this adder in free-run come
> from the firmware **0x3F4D** offset buffer (`tools/aru224_emulate.py::tap_map`), **not** the WCS 0x4000
> lanes 0/1. Sourcing offsets from 0x4000 lanes 0/1 gave clustered ~0.9–1.7 s garbage delays so DMEM reads
> and writes addressed disjoint regions and the recirculation loop never closed (**the dead-tank root cause**,
> the `tools/aru_freerun.py` bug). The `tap_map[s]` ms-scale offsets are step-index-keyed and align with the
> 0x4000 COEFFICIENTS[s]; with them (`addr = CPC + offset[step]`) the feedback loops exist at ms-scale and a
> SHORT ~0.5 s tail emerges — dead tank → audible (L5.8). 🟡 The full ~2.6 s decay is still open (loop gain too
> low: quantization / coeff scaling / LFO modulation) — a further cause beyond the offset source (M3/M4).

---

# L6 — ARU datapath semantics (fields → per-step computation, then free-run execution)

Two distinct halves. **Primitives** (L6.1–L6.6) are single-step-testable by POST. **Free-run execution**
(L6.7–L6.13) is the autonomous WCS loop POST never runs — schematic/hardware only — and is where the reverb
actually breaks.

## 6a. Datapath primitives (POST-step testable)
| ID | Component | What it is | Status | Validator(s) | Depends on |
|---|---|---|---|---|---|
| **L6.1** | **Register file** | 4×16-bit (LS670 aru_U29–U32); write port WA (write-enable = DAB WSTB = ¬MS7, every step); read port RA (continuous) | 🔶 LARGELY VERIFIED | **[POST-VERIFIED]** the register/walking-pattern test E40 **passes** on a faithful 4-word regfile; WA/RA pinned to {b2,b3}/{b4,b5} (transpose & same-bits aliasing DISPROVEN). Gap: intra-field order/polarity; **cross-step survival (L6.10) is free-run only** | L4.3, L4.4, L6.2 |
| **L6.2** | **DAB (data bus)** | 16-bit bus; on the ARU board connects ONLY to regfile + result reg; bridges to DMEM via XREG (U38–U41). No DMEM→multiplier bypass. | ✅ (owner-traced) | [schematic] (owner confirmed: DAB↔U29-32,U43-44,XREG) | — |
| **L6.3** | **Multiplier** | 16×6 two's-complement modified-Booth, **/32** scale; gate-level (NAND array + 74F283 chain + fig-3.4 schedule) | ✅ POST-VERIFIED | **[SOLVED]** the gate-level model (`tools/aru_booth.py`, netlist §4F) reproduces **all 20 multiplier-test goldens bit-exact** (E83 passes): /32 scale, ±2¹⁵ rail, exact rounding, coeff weight-order all pinned. cmag=63 (all-ones) = a unique combinational **+3/dual-rail-phase** correction (plan 016; origin owner-confirmed outside the traced wiring) | L4.5, L4.8, L6.1 |
| **L6.4** | **Accumulator** | 20-bit; add product; **saturate at ±2¹⁸** (74F157 muxes aru_U33–U37); ZERO clears | 🔶 LARGELY VERIFIED | **[POST-step]** the multiplier test accumulates a single product/step and passes (E83); ±2¹⁵ output rail + rounding pinned. Multi-term MAC accumulation across a chain is free-run (M3) | L6.3, L4.7 |
| **L6.5** | **Result register** | LS374 (aru_U43/U44); loaded by XFER CK from accumulator (`RES = sat16(ACC≫3)`); drives DAB via RDRREG/ | 🔶 LARGELY VERIFIED | **[POST-step]** the read-back path is exercised (E40/E83/E91 read results back); **XFER=0 in POST → the single-step read-back bypasses the XFER-gated load, reading the X-register-captured DAB** (scout-confirmed). RES = round-half-up at ≫3 | L6.4, L4.6 |
| **L6.6** | **MAC pipeline timing** | product available ≈end of AS0 of the *next* cycle (deferred); XFER captures @AS0; ZERO clears @AS0 | 🔶 PARTIAL | [schematic] fig-3.4 + the M1 clock engine models the per-AS schedule; the cmag=63 cycle-accurate cosim (plan 016) explored the single-step pipeline. The **cross-instruction deferral in free-run** is M3 | L6.3, L6.4 |

## 6b. Free-run execution (NOT POST-testable — schematic/hardware only)

> **★ M3 ENGINE BUILT (2026-06-29):** `tools/aru_freerun.py` = class `FreeRunARU` (separate from the
> POST-green `tools/aru_rtl_dp.py`, which it does NOT touch). It sweeps the WCS program counter 0→99
> (RESET@99), does per-step §2T device-decode DAB routing, runs the fig-3.4 deferred MAC as a 1-instruction
> pipeline with a clean signed multiply-accumulate (`RES = sat16(ACC≫3)`), CPC +1/sample, DMEM recirculation,
> and fixed-point I/O (inject at RD AD/, capture at WR DA/). **Verified:** M3.0 = the full 100-step CONCERT
> runs 500k+ microinstructions with no fault; **M3.1** zero-delay passthrough PASS; **M3.2** max-delay
> DMEM-delay PASS (impulse reappears exactly `delay` samples later); **M3.3** a hand-built feedback comb decays
> exactly per coefficient (recirculation proven). POST regression stays green on `aru_rtl_dp.py`
> (E32/E40/E83/E91; mult 20/20). `tools/render_wav.py` renders the output to a 34.13 kHz WAV.

| ID | Component | What it is | Status | Validator(s) | Depends on |
|---|---|---|---|---|---|
| **L6.7** | **T&C microsequencer** | autonomously fetches & sequences the **100 WCS microwords/sample**; AS0/1/2, MS0–8, 293 ns cycle, 34.13 kHz | 🔶 BUILT (M3) | [schematic] netlist §6T (PC tc_U14/U1, MS-gen, AS-gen); the M1 `ClockEngine` reproduces the MS/AS skeleton. **The free-run 100-step PC sweep (RESET@99) is now built in `tools/aru_freerun.py` — M3.0 runs 500k+ microinstructions/no fault.** Closure to a real-unit IR is L7 | L4.0 |
| **L6.8** | **Per-step DAB-source routing (free-run)** | each step the **device decode** picks who drives the DAB (DMEM read / RES via RDRREG/ / audio-in / sub / **idle=hold**) — NOT the SBC | 🔶 BUILT (M3) | [schematic] netlist §2T (tc_U47/U48/U49) — fully traced; **now built in `tools/aru_freerun.py`** (per-step §2T device decode). ⚠ the output-channel decode (SDAA–D) in `aru_freerun.py` is a binary code, but netlist §2T.4 = 4 INDEPENDENT reversed strobes (OFST8/→SDAD … OFST11/→SDAA) — a channel-LABEL bug only, not an IR-value bug | L4.2, L4.9, L6.2 |
| **L6.9** | **idle = hold** | undriven DAB floats and holds its last value (no pull resistors) | 🔶 | [schematic] (no pull resistors); modeled by the RTL `Net` hold-last. Its *effect per step* is free-run = M3 | L6.8 |
| **L6.10** | **Register survival across steps** | does a value written to a register survive to be read later, or is it clobbered? (the old "R3-clobber") | 🔶 BUILT (M3) | [schematic] regfile + WA/DAB-WSTB timing traced; **runs clean in `tools/aru_freerun.py`** (M3.0, 500k+ steps no fault). The R3-clobber was a *sectional-model* artifact (plan 013 §0). **The two un-POST-tested timing choices — read-before-write of the regfile operand + the deferred-MAC retire ordering — were PROVEN INERT** (toggling each leaves the loop eigenvalue bit-identical), so neither was the dead-tank cause | L6.1, L6.7 |
| **L6.11** | **DMEM read latency / read-before-write** | DMEM DOUT valid late (≈MS7, Fig 3.3); every DMEM cycle is **read-before-write** | 🔶 LARGELY VERIFIED | [schematic] §5/§6D; the read-before-write semantics are POST-verified (E91 passes). Free-run load-delay timing = M3 | L5, L6.2 |
| **L6.12** | **DMEM write data + timing** | written value = RES (via XFER); the write-head sweep (old "trample") | 🔶 NET-TRACED | [schematic] §5.5/§6D; single-step DMEM write verified (E91). Free-run write-head behavior = M3 | L6.5, L5, L6.7 |
| **L6.13** | **Output node (WR DA/)** | the D/A output strobe = `WR DA/ = NAND(OFST7/, tcWR)` (tc_U49 g2); which step(s) drive the audio out | 🔶 NET-TRACED | [schematic] netlist §2T.2 | L4.2, L6.2 |

**L6 exit criterion:** 6a primitives **each pass their POST sub-test on a faithful model — DONE** (the whole
POST passes un-suppressed; mult is the gate-level Booth). 6b free-run components are now **net-traced** on the
T&C/ARU control schematic (the M0b netlist) and, **as of 2026-06-29, BUILT and running in `tools/aru_freerun.py`**
(M3.0 = full CONCERT runs 500k+ microinstructions/no fault; M3.1 passthrough + M3.2 DMEM-delay + M3.3
feedback-comb decay all PASS; sourcing offsets from `tap_map`/0x3F4D — not 0x4000 — makes the feedback loops
exist at ms-scale so a SHORT ~0.5 s tail emerges (dead → audible); the full ~2.6 s decay is still 🟡 open).
Remaining: pin the offset sign/encoding + run the per-frame LFO modulation inside the loop for a proper decaying
tail, then match a real-unit IR (L7). **6a passing ≠ L6 done** — it's now "primitives ✅, free-run engine built
(M3), IR match = L7."

---

# L7 — Parameter application (LARC params → WCS coefficients) — ★ FULLY TRACED (2026-06-29)

How a stored program's parameter values become the per-step WCS coefficients/delays the free-run engine reads.
Firmware-disassembly-verified this session.

**Flat param array (NOT just the 6 live sliders).** All FIVE LARC control pages' parameter values live in ONE
flat RAM array based at **0x3ca3** (6 bytes/page × 5 pages = 30 bytes; a record header/type byte at 0x3ca2).
The 6 LARC faders at **0x3c00–0x3c05** are ONLY the live fader-echo of the CURRENT page. Array slot =
`0x3ca3 + page*6 + slider`, computed at **0x862e** (A = (0x3c34)*6 + B).

**Page state / paging.** **0x3c32** = raw page counter (PAGE-key handler **0x8f50** does INC); **0x3c34** =
derived/clamped page index (read only at 0x862e; written at 0x1477). The PAGE key (0x8f50) advances 0x3c32,
recomputes 0x3c34, and reloads the 6 sliders 0x3c00–05 from the new page's array slice (**0x87c2**).

**Apply chain.** main-loop scan **0x8185** (DE=0x3c00 live, HL=0x3c16 last-seen, B=0..9; B≤5 → handler 0x85f2)
→ **0x85f2** type-scales by program type (0x3c33), QUEUES a de-zip job (pending-flag array 0x3c20+B), sets
dirty flag 0x3c51 → the DE-ZIPPER applier **0xB000** RAMPS the coeff/delay one step per main-loop pass and
PACKS the byte into the WCS 0x4000 image (**0xB4F0** = 6-bit coeff magnitude into the upper bits; **0xB4FF** =
sign into bit7 of the adjacent byte).

**Group table 0x3CF4** (built by the interpreter 0xAA9F; 32 entries × 3 bytes; opcode low-nibble = count, bits
0x30 = sub-type 0x00/0x10/0x20) LINKS each parameter's group to its target WCS step(s); the step→coeff-address
transform is **0xAB0C** (`addr = 0x4003 + step*4`).

**Recall at load.** program-load **0x13B6** → lookup **0x133e** finds the program record in the **0xB800** array
(21 records × 0x2AA bytes; record 0 = CONCERT) → **0x13d9** (`LD DE,0x3ca2; LD B,0x30; CALL 0x0614`) RECALLS
the 48-byte param/toggle block into 0x3ca2.. → the **0xa791** apply engine builds the FULL WCS image. ⇒ the
variation defaults ARE recalled and the full WCS IS built at load (boot: **110/128** steps already have built
coefficients).

**Toggles (3 PARAM-key toggles) — stored as BITS in one RAM byte 0x3ccd**, loaded from the program record at
load (0xA892). bit0 (0x01) = **Dynamic Decay** (gates LF/Mid Stop Decay; read at 0x83B4); bit6 (0x40) =
**Mode Enhancement** (gates the Chorus/LFO modulation engine 0xAD5C: `AND 0x40; JP z` skips the whole LFO
update when clear); bit7 (0x80) = **Decay Optimization** (read at 0x83D1). CONCERT boots **0x3ccd = 0xC0**
(Mode Enhancement + Decay Optimization ON, Dynamic Decay OFF). Toggle cycle index = 0x3c41; mask table @0xa758.

**CONCERT group→param→WCS-step map** (verified vs the param sweep + disassembly):
- **P0 LF Decay** → steps 43, 95
- **P1 Mid Decay** → anchors 64, 68, 115, 119 + interpolated allpass coeffs 62,63,66,67,113,114,117,118 (via
  the decay generator 0x86b2/0x8da5/0x8e03, NOT in the group table)
- **P2 Crossover** → 45, 46, 97, 98
- **P3 Treble Decay / HF-damp** → 40, 41, 92, 93
- **P4 Depth / input-diffusion** → 29–32, 81–84
- **P5 Predelay** → DELAY steps 42, 94
- **PAGE 2 Chorus** → group g0 steps 57, 108 (animated by the LFO over canonical taps 56/57/107/108; depth
  0x3cd4, rate 0x3cd3=0x20)
- **PAGE 2 Diffusion** → group g19 steps 52,60,72,104,111,123 (the recirculation ALLPASS, coeff ≈ −95/−0.74)
- **Tank feedback** → g20–29 steps 27,28,79,80 (coeff −127, near-unity)

> **★ PARAM HYPOTHESIS RULED OUT (the dead tank was NOT un-recalled parameters).** The page-1 slider coeffs
> AND the page-2 Diffusion(=25)/Chorus(=50) defaults are all recalled into 0x3ca3 and baked into the WCS at
> load (110/128 steps built; Diffusion/Chorus/feedback coeffs present at boot; Mode Enhancement ON). Applying
> CONCERT Variation 1's full preset was a NO-OP. The dead tank was the **offset-source bug** (L5.8 / the
> `tools/aru_freerun.py` 0x4000-offset bug), not parameters.

**WCS image clarification.** The 0x4000 SBC image holds the CORRECT COEFFICIENTS in **lanes 2/3** (the
param-derived decay/diffusion/feedback coeffs, byte-identical to the build, present at boot). Its **lanes 0/1
are NOT a reliable free-run delay-offset source** (see L5.8). `aru_freerun.py` reads coeffs from 0x4000
correctly; only its offset source was wrong.

**CONCERT = Concert Hall, Variation 1** (docs/reference/224/224X_chapter8_variation_presets.md; Owner's Manual
ch.4): 5 control pages, 7 variations, average decay 2.6 s. Var-1 preset: P1 LF Decay 3.0 s / Mid Decay 2.0 s /
Crossover 720 Hz / Treble Decay 6.30 kHz / Depth 33 / Predelay 24.0 ms; P2 LF Stop 3.0 s / Mid Stop 3.0 s /
Chorus 50 / HF Bandwidth 9.00 kHz / Diffusion 25 / Definition 00; P3 Preecho Levels 00; P4 Preecho Delays
5.00/9.75/17.5/25.0 ms + Fine Predelay 0.36/10.2 ms; P5 Size/Gate; toggles Dynamic Decay OFF, Mode Enhancement
ON, Decay Optimization OFF.

---

## POST coverage of the L4 field map and L5 address map (adversarially verified — `wf_73bb6dc6`)

Status legend: **[PINNED]** survived independent re-disassembly + a coverage attack that failed to find an
aliasing wrong-decode; **[PARTIAL]** pinned only up to a named aliasing symmetry; **[UNCOVERED]** a
wrong-but-consistent decode provably aliases through, or the bits are never varied.

POST drives the ARU **single-step** (DSP HALTed, WCS program counter U1/U14 stopped; one `OUT 0x03` clock =
one microstep) — structurally different from the **free-run** reverb (T&C runs 100 WCS words/sample, CPC
+1/sample). The whole coverage question hinges on this: single-step never enters the mechanisms the reverb
depends on.

**What POST certifies (TRANSPORT, not full SEMANTICS):**
- **[PINNED] WCS scratch RAM (0x089F):** all 512 bytes of 0x4000-0x41FF store/return every bit; assigns no
  field meaning.
- **[PINNED] SBC↔ARU port plumbing (0x0A1D latch):** ports 0x00/0x01/0x05/0x06/0x07 read back; `IN 0x02`
  echoes `OUT 0x07`; the 8 data LINES toggle independently — NOT that any line is routed to the correct field.
- **[PINNED, SATISFIED] Multiplier value/scale/rounding (0x0942):** the **/32** scale, **±2¹⁵** readback rail,
  and **exact 16-bit rounding** are pinned — no clean integer model fits, so a **gate-level serial Booth** is
  required (a 1-LSB-off model FAILS). **Now built and passing:** `tools/aru_booth.py` reproduces all 20 goldens
  bit-exact (E83 passes); cmag=63 = +3/dual-rail (plan 016). (Strongest single POST constraint; a datapath fact.)
- **[PINNED] Raw DMEM cell storage (0x0B75):** per-cell storage over the swept range, proven STORED-not-bus.

**L4 field map — NOT 100% verified:**
- **[PARTIAL] WA/RA (0x0C48):** enumeration of every ordered bit-pair × polarity → **exactly 4 decodes pass,
  all read WA∈{b2,b3}, RA∈{b4,b5}; zero same-bit-set decodes pass.** ⇒ the "WA/RA from the same wrong bits"
  aliasing is **DISPROVEN**, and a **WA↔RA transpose FAILS** (refuting the earlier "transpose still passes"
  guess). Residual: the 4 survivors are {identity, both-fields bit-reversed, both inverted, both reversed+
  inverted} — a joint relabeling, **so intra-field MSB/LSB order + polarity are NOT pinned** (matters only if
  free-run uses the index value for anything beyond slot selection).
- **[PINNED, narrowly] CSIGN = L2 bit7 toggles product sign** (mult 7E vs FE). Not proven "CSIGN" vs a generic
  sign gate; polarity label untested.
- **[PARTIAL] coeff (L3 bits 2-7):** only 3/64 codes exercised; **36 of 720 bit-permutations alias** → per-bit
  **weight order NOT pinned**.
- **[UNCOVERED] device MI16/MI17:** held (0,1) on every step; the 2-bit map (11/10/01/00) is **never
  enumerated**. A permuted device decode aliases through.
- **[PARTIAL — corrected] OFFSET + ZERO are now exercised:** the DMEM test (0x0B75) **does** set the 16-bit
  OFFSET nonzero (0x2000) and **requires ZERO** to clear the accumulator each step (both verified by E91
  passing). Still uncovered by POST: **XFER** (=0 in every microword — its load path isn't exercised) and
  bit6/PROT.
- **Resolved caveat:** the DMEM-test microword (step 127: CSIGN=1/WA=3/RA=3, unity, MEMW) is **self-consistent**
  under the netlist field map — a unity ×1 passes the DAB input through (WA=3 write, RA=3 read), the DMEM cycle
  is read-before-write, and the model passes E91. (The earlier "internally-inconsistent / 0x41F5 is an OFFSET
  byte" reading was an artifact of the wrong addressing assumption, now corrected.)

**L5 address map (`addr = CPC − OFST`) — ★ CORRECTED 2026-06-29: PARTIALLY covered (the earlier "provably
total gap" was WRONG):**
- **[PINNED]** per-cell storage across the swept range (DMEM sweep).
- **[PARTIAL — corrected] the offset→address ARITHMETIC IS exercised.** A live probe of the **dedicated DMEM
  test (0x0B75)** shows its active microword (step 127) carries a **nonzero** offset (OFST/=0xDFFF → 0x2000),
  and the CPC walks one position per strobe; a faithful `addr = CPC + OFST_stored + 1` model **passes E91**.
  So the dmem_U49/U50/U63/U64 subtractor + CPC ARE driven at a nonzero offset. (The earlier wf_73bb6dc6 claim
  that "every POST DMEM access pins OFFSET=0 / supplies the address via OUT 0x00/0x05" was incorrect — the
  address is `CPC − OFST`, not port-supplied.) **Still open:** offset *variation* (only 0x2000 tested) + the
  dual-use bits 12/13.
- **[RESOLVED] no bank:** the adder top carry-out (`dmem_U64.pin9`) is n/c; single 64K×16 bank (netlist §5.5).
- **L5 is now PARTIALLY POST-validated (one offset); full offset-range + free-run validation needs M3/hardware.**

**Free-run-only mechanisms POST never exercises (the L6.7–L6.13 gap):** the T&C 100-step sequencer; CPC
+1/sample; the adder with **varying nonzero per-step offsets**; per-step device-decode switching (read/write/
sub/hold, idle=hold); cross-step MAC pipeline timing (XFER CK, late DMEM-read load, acc_latch order);
XFER/ZERO accumulate sequencing; accumulator survival + ±2¹⁸ saturation across a MAC chain; recirculation/
feedback — **the entire reverb.** The known open bugs (R3 clobber, write-head offsets) live here and pass
POST untouched.

**Bottom line (updated 2026-06-29):** the **whole POST now passes un-suppressed** on a netlist-faithful model.
POST certifies the transport + pins WA→{b2,b3}, RA→{b4,b5} (up to inert joint symmetry), CSIGN=bit7-toggles-
sign, the **gate-level multiplier (20/20, weight-order fixed by the verified gates — no longer a 3-code/36-perm
gap)**, ZERO (required by the mult+DMEM tests), and the **`CPC − OFST` arithmetic at one nonzero offset (0x2000,
the DMEM test)**. Still NOT POST-covered: XFER's load path (XFER=0 in POST), OFFSET *variation*, the device
2-bit map's MEMR leg, and the dual-use bits 12/13 — these + all **free-run** timing/routing are net-traced on
the M0b schematic and validated structurally; full confirmation needs the free-run model (M3) or hardware.

## How to drive this (the work order)
1. **DONE — faithful ARU+DMEM model on `tools/boot8080.py` passes the whole POST un-suppressed.** Cleared the
   POST-step column: L6.1 (regfile/E40), L6.3 (gate-level multiplier/E83), L6.4 (accumulator), L5.1/L5.2/L5.6
   (DMEM/E91, incl. `CPC−OFST` at offset 0x2000 + read-before-write), and the L4 fields each test varies.
   Models: `tools/aru_post.py` (behavioral) and `tools/aru_rtl*.py` (phase-accurate).
2. **DONE — the schematic control-path trace exists:** the M0b interconnect netlist
   (`224XL_interconnect_netlist.md`) traces the T&C microsequencer (§6T), per-step DAB decode (§2T), MAC
   clocking (§6T.4), and the offset→adder wiring (§5.2) — the part POST cannot reach.
3. **DONE — the free-run datapath is BUILT (plan 013 M3, `tools/aru_freerun.py`):** real WCS PC 0–99 (RESET@99),
   per-step §2T DAB routing, deferred MAC, idle=hold, CPC +1/sample, DMEM recirculation; M3.0 runs 500k+
   microinstructions/no fault and M3.1/M3.2/M3.3 (passthrough / DMEM-delay / feedback-comb decay) PASS. The
   **dead-tank root cause was the offset source** — fixed by reading per-step offsets from the firmware 0x3F4D
   buffer (`aru224_emulate.tap_map`), not the WCS 0x4000 lanes 0/1 (L5.8). The L7 param-application chain is
   fully traced (params recalled + WCS built at load; param hypothesis ruled out).
4. **NEXT:** pin the offset sign/encoding, run the per-frame LFO modulation (Mode Enhancement engine 0xAD5C)
   inside the loop for a proper ~2.6 s decaying tail, then (L7) compare to a real-unit IR.

## Dependency summary (bottom-up)
`L4.0 → L4 fields → {L5 (needs L4.1/L4.9), L6.1–L6.5 (need L4 fields)} → L6.6 timing → L6.7 sequencer →
L6.8–L6.12 free-run → L7 audio`. Nothing in 6b is trustworthy until 6a + L5 are pinned, and 6b itself needs
the schematic/hardware validators, not POST. **L7 (param→WCS) is fully traced (2026-06-29) and feeds the
free-run engine** via the 0x4000 coefficient image (lanes 2/3) + the 0x3F4D offset buffer (tap_map).
