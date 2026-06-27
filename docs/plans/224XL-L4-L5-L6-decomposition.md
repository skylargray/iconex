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

> **★ The single biggest structural fact:** POST proves the ARU's **datapath primitives** (in single-step),
> the schematic can prove the **static wiring**, but the **free-running execution** (T&C sequencing +
> per-step routing + cross-step timing) — which is what actually produces the reverb and is where every
> failure has lived — is verifiable **only by schematic control-path trace or hardware.** Keep that boundary
> visible in every layer below.

Status legend: ✅ VERIFIED · 🔶 PARTIAL/IN-PROGRESS · ❌ FAITH (unproven) · ⬜ PENDING.

---

# L4 — Microword field decode (4 bytes → control fields)

**Input:** the 4 bytes of a step from the firmware-built WCS image (L3, ✅ — bytes are real).
**Output:** the per-step control fields the ARU acts on.
**Why hard:** the bit→meaning map is human-schematic-read; POST validates a field only where it
distinguishingly varies it. Decompose by *field*, foundation first.

| ID | Component | What it is | Status | Validator(s) | Depends on |
|---|---|---|---|---|---|
| **L4.0** | **Lane layout & polarity** | which byte is offset/control; b3 read **complemented**, b2 **direct**; the "skip if l2==l3==0xFF" NOP rule | ❌ FAITH | [schematic] T&C decode 060-02475; [POST-step] (every test patches a microword — its byte layout must match) | — |
| **L4.1** | **OFFSET field** | b0,b1 = 16-bit offset, read **RAW** (`l0|l1<<8`), *not* inverted | ❌ FAITH | **[UNCOVERED by POST]** verified: pinned 0x0000 every POST step → bits/polarity/dual-use 0% covered. [cross-pipeline] matches 0x3F4D 120/128 only | L4.0 |
| **L4.2** | **MI16 / MI17 device bits** | b2.0=MI16, b2.1=MI17; `(MI17,MI16)` = 11 read / 10 write / 01 sub / 00 NC | ❌ FAITH | **[UNCOVERED]** verified: held (0,1) every POST step; the 2-bit map never enumerated → aliases. [schematic] only | L4.0 |
| **L4.3** | **WA (write reg addr)** | b2 bits 2–3 → which of 4 registers is written | 🔶 PARTIAL | **[PARTIAL]** verified: POST pins WA∈{b2,b3} (transpose & same-bits aliasing DISPROVEN); intra-field order/polarity unpinned | L4.0 |
| **L4.4** | **RA (read reg addr)** | b2 bits 4–5 → which register feeds the multiplier | 🔶 PARTIAL | **[PARTIAL]** verified: POST pins RA∈{b4,b5}; order/polarity unpinned (joint symmetry with WA) | L4.0 |
| **L4.5** | **CSIGN** | b2 bit 7 → coefficient sign | 🔶 PARTIAL | **[PINNED-narrow]** verified: POST mult test pins "bit7 toggles product sign"; the polarity label is convention | L4.0 |
| **L4.6** | **XFER** | b3 bit 0 → load result register from accumulator | ❌ FAITH | **[UNCOVERED]** verified: XFER=0 in every POST pattern → unpinned. [schematic] XFER CK net only | L4.0 |
| **L4.7** | **ZERO** | b3 bit 1 → clear accumulator | ❌ FAITH | **[UNCOVERED]** verified: XFER↔ZERO swap passes (position not pinned). [schematic] only | L4.0 |
| **L4.8** | **Coeff magnitude** | b3 bits 2–7 → 6-bit multiplier coefficient | 🔶 PARTIAL | **[PARTIAL]** verified: POST pins /32 at 3 codes; **36/720 bit-permutations alias** → weight order unpinned | L4.0 |
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
| **L5.1** | **CPC** | Current Position Counter, 16-bit, **+1 per sample**, free-running; "current write position" | 🔶 PARTIAL | **[PINNED, single-step]** verified: DMEM test certifies CPC auto-increment + unique addressing across the sweep; the **+1/sample free-run** behavior is [schematic] only | — |
| **L5.2** | **The subtract** | `addr = CPC − offset` | ❌ FAITH | **[UNCOVERED — provably]** verified: POST pins offset=0 → adder invariant under every wiring; **zero POST coverage**. [schematic]/[hardware] ONLY | L5.1, L4.1 |
| **L5.3** | **Active-low + carry-in impl.** | adder adds `~offset` with carry-in tied high (U49/U50/U63/U64) → two's-complement subtract | ❌ FAITH | [schematic] 060-01318 adder nets | L5.2 |
| **L5.4** | **OFFSET→adder wiring** | which offset bits feed which adder inputs; straight order? what about the dual-use bits 12/13 (L4.9)? | ❌ FAITH | [schematic] net-by-net — **the dual-use bits are the risk** | L5.3, L4.9 |
| **L5.5** | **Carry-out → bank** | the 17th address bit = the adder carry-out; selects bank (no separate bank-select) → flat 128K | ❌ FAITH | [schematic] carry → CAS0/CAS1 gating | L5.3 |
| **L5.6** | **DRAM row/col mux** | U36/U18 multiplex A0–7 (row) / A8–15 (col); no bit scramble; physical cell = linear addr | ❌ FAITH | [schematic]; [POST-step] DMEM test all-64K write/read covers address integrity | L5.5 |
| **L5.7** | **Physical DMEM org** | 2 rows × 16×4164, bit-sliced (column i → DABi), DIN=DOUT, top=CAS0/bottom=CAS1 | ✅ (owner-traced) | [schematic] (owner confirmed this session) | — |
| **L5.8** | **delay = R − W** | a delay line = small write-offset W + larger read-offset R; realized delay = R−W samples | ❌ FAITH | derived from L5.2; needs free-run to confirm | L5.2 |

**L5 exit criterion:** the `CPC − offset` adder (incl. active-low/carry/bank) is net-traced, AND the
offset→adder wiring is confirmed bit-by-bit (especially the dual-use 12/13). POST's DMEM test alone does
**not** suffice (it doesn't drive nonzero offsets).

---

# L6 — ARU datapath semantics (fields → per-step computation, then free-run execution)

Two distinct halves. **Primitives** (L6.1–L6.6) are single-step-testable by POST. **Free-run execution**
(L6.7–L6.13) is the autonomous WCS loop POST never runs — schematic/hardware only — and is where the reverb
actually breaks.

## 6a. Datapath primitives (POST-step testable)
| ID | Component | What it is | Status | Validator(s) | Depends on |
|---|---|---|---|---|---|
| **L6.1** | **Register file** | 4×16-bit (LS670 U29–U32); write port WA (write-enable = DAB WSTB = MS7, every step); read port RA (continuous) | 🔶 PARTIAL | **[PINNED, single-step]** verified: stores 4 distinct 16-bit words; WA/RA pinned to {b2,b3}/{b4,b5} (transpose & same-bits aliasing DISPROVEN). Gap: intra-field order/polarity; **cross-step survival (L6.10) is free-run only** | L4.3, L4.4, L6.2 |
| **L6.2** | **DAB (data bus)** | 16-bit bus; on the ARU board connects ONLY to regfile + result reg; bridges to DMEM via XREG (U38–U41). No DMEM→multiplier bypass. | ✅ (owner-traced) | [schematic] (owner confirmed: DAB↔U29-32,U43-44,XREG) | — |
| **L6.3** | **Multiplier** | 16×6 two's-complement serial multiply, **/32** scale (operand≪3, product≫5); modified-Booth, gate-level | 🔶 PARTIAL | **[PINNED, strongest]** verified: POST pins **/32 scale, ±2¹⁵ rail, exact 16-bit rounding**; no clean integer model fits → **gate-level serial Booth required** (1-LSB-off FAILS). Gap: coeff weight-order (L4.8) | L4.5, L4.8, L6.1 |
| **L6.4** | **Accumulator** | 20-bit; add product; **saturate at ±2¹⁸** (74F157 muxes U33–U37); ZERO clears | ❌ FAITH | [POST-step] (mult test accumulates); [schematic] sat muxes | L6.3, L4.7 |
| **L6.5** | **Result register** | LS374 (U43/U44); loaded by XFER CK from accumulator (`RES = sat16(ACC≫3)`); drives DAB via RDRREG/ | ❌ FAITH | [schematic] (pinout known); [POST-step] readback path | L6.4, L4.6 |
| **L6.6** | **MAC pipeline timing** | when the product is available (≈end of AS0 of the *next* cycle), when XFER captures, when ZERO clears — the 1-step-deferred-product question | ❌ FAITH | [schematic] T&C/ARU clocking (Fig 3.4); [hardware] | L6.3, L6.4 |

## 6b. Free-run execution (NOT POST-testable — schematic/hardware only)
| ID | Component | What it is | Status | Validator(s) | Depends on |
|---|---|---|---|---|---|
| **L6.7** | **T&C microsequencer** | autonomously fetches & sequences the **100 WCS microwords/sample**; the AS0/AS1/AS2 states, MS0–8, 293 ns cycle, 34.13 kHz | ❌ FAITH | [schematic] T&C 060-02475; [hardware] | L4.0 |
| **L6.8** | **Per-step DAB-source routing (free-run)** | each step the **device decode** picks who drives the DAB (DMEM-read data / RES via RDRREG / audio-in / sub / **idle=hold**) — NOT the SBC | ❌ FAITH | [schematic] U47/U48/U49C device decode (owner partly traced); [hardware] | L4.2, L4.9, L6.2 |
| **L6.9** | **idle = hold** | undriven DAB floats and holds its last value (no pull resistors) | 🔶 | [schematic] (owner: no pull resistors) — but its *effect per step* is free-run-only | L6.8 |
| **L6.10** | **Register survival across steps** | does a value written to a register survive to be read by a later step, or is it clobbered? (the R3-clobber problem) | ❌ FAITH | [schematic] write-enable timing + WA per step; [hardware] | L6.1, L6.7 |
| **L6.11** | **DMEM read latency / load-delay** | DMEM DOUT valid late (≈end MS7→MS8/MS0, Fig 3.3) → possible 1-step delay before read data is usable | ❌ FAITH | [schematic] DMEM timing 060-02512; [hardware] | L5, L6.2 |
| **L6.12** | **DMEM write data + timing** | what value is written (RES) and when, as the write heads sweep (the trample problem) | ❌ FAITH | [schematic]; [hardware] | L6.5, L5, L6.7 |
| **L6.13** | **Output node (WR DA/)** | the D/A output strobe = U49C `(MI17,MI16)=(0,1) & MI7=1`; which step(s) drive the audio out | 🔶 | [schematic] (owner traced U49C) | L4.2, L6.2 |

**L6 exit criterion:** 6a primitives each pass their POST sub-test on a faithful model (mult needs gate-level
multiply); 6b free-run components each net-traced on the T&C/ARU control schematic **and/or** matched against
a hardware capture of the ARU running a known microprogram. **6a passing ≠ L6 done** — it's "primitives ✅,
free-run ❌."

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
- **[PINNED] Multiplier value/scale/rounding (0x0942):** the **/32** scale, **±2¹⁵** readback rail, and the
  **exact 16-bit rounding** are pinned — no clean integer model fits; residual is a consistent ±1 LSB
  (gate-level serial Booth). A multiplier off by 1 LSB on negatives **FAILS**. (Strongest single POST
  constraint, but a *datapath* fact, not a field-map fact.)
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
- **[UNCOVERED] bit6; XFER (=0 always); ZERO (XFER↔ZERO swap passes); the 16-bit OFFSET field** — never set
  nonzero by any ARU sub-test.
- **Caveat:** under the current map the DMEM-test's loaded words decode to an internally-inconsistent
  CSIGN=1/WA=3/RA=3, and 0x41F5 is actually an OFFSET-high byte under 4-byte alignment — POST does **not**
  self-consistently pin the byte semantics it relies on.

**L5 address map (`addr = CPC − offset`) — NOT verified; gap PROVABLY TOTAL:**
- **[PINNED]** raw port-supplied address → cell (DMEM sweep).
- **[UNCOVERED — provably] the offset→address ARITHMETIC.** Every POST DMEM access pins the microword OFFSET
  to **0x0000** (verified by emulating preload 0x0933) and supplies the address via `OUT 0x00`/`OUT 0x05`.
  With offset=0, `addr = CPC − 0 = CPC` for **any** offset-decode wiring → invariant under every transform
  (permutation, polarity, subtract-vs-add, carry, field width, dual-use 12/13). The U49/U50/U63/U64
  subtractor is **never driven with a nonzero offset**. (`0x0EFD` sets offset=1 but is dead/uncalled.)
- **[UNCOVERED] carry-out → bank:** the sweep needs only 65536 distinct cells (true 17-bit and 16-bit wrap
  satisfy it identically).
- **L5 is a purely free-run mechanism, 100% unvalidated by power-up POST.**

**Free-run-only mechanisms POST never exercises (the L6.7–L6.13 gap):** the T&C 100-step sequencer; CPC
+1/sample; the adder with **varying nonzero per-step offsets**; per-step device-decode switching (read/write/
sub/hold, idle=hold); cross-step MAC pipeline timing (XFER CK, late DMEM-read load, acc_latch order);
XFER/ZERO accumulate sequencing; accumulator survival + ±2¹⁸ saturation across a MAC chain; recirculation/
feedback — **the entire reverb.** The known open bugs (R3 clobber, write-head offsets) live here and pass
POST untouched.

**Bottom line:** POST certifies the **transport** + pins **WA→{b2,b3}, RA→{b4,b5}** (up to inert joint
symmetry), **CSIGN=bit7-toggles-sign**, and **coeff/32 at 3 codes** (up to a 36-permutation weight aliasing).
It certifies essentially **nothing** about device-field placement, OFFSET, XFER/ZERO, or the **L5 CPC−offset
arithmetic** (provably zero coverage). L5 and all free-run timing/routing must be validated by
**schematic control-path trace or hardware**, never POST.

## How to drive this (the work order)
1. **Build the faithful ARU port model on `tools/boot8080.py`** and pass POST un-suppressed — clears the
   POST-step column: L6.1 (regfile), L6.3 (multiplier, needs gate-level), L6.4 (accumulator), L5.1/L5.6
   (DMEM via the DMEM test), and the L4 fields each test distinguishingly varies. Update this table as each
   sub-test passes; **note every aliasing caveat** the coverage analysis (`wf_73bb6dc6`) surfaces.
2. **Get the schematic control-path trace** for the free-run half (L6.7–L6.12, L5.2–L5.5): the T&C
   microsequencer, the per-step DAB mux, the MAC clocking, the offset→adder wiring. This is the part POST
   physically cannot reach.
3. **Only then** assemble the full free-run datapath and (L7) compare to a real-unit IR.

## Dependency summary (bottom-up)
`L4.0 → L4 fields → {L5 (needs L4.1/L4.9), L6.1–L6.5 (need L4 fields)} → L6.6 timing → L6.7 sequencer →
L6.8–L6.12 free-run → L7 audio`. Nothing in 6b is trustworthy until 6a + L5 are pinned, and 6b itself needs
the schematic/hardware validators, not POST.
