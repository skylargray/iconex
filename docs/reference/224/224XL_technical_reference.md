# Lexicon 224XL — Complete Technical Reference for Reconstruction

> **★★★ THE CURRENT MODEL (sessions 0022–0027, 2026-07-02) — read THIS, then treat the body below as
> the historical record it is.** The verified, oracle-locked model (engine of record:
> `tools/aru_freerun22_rtl.py`; per-pin lock: `tools/session0022_probes/e1_aru_signatures.py`,
> 1467/1469 ARU signature pins, feedback table 710/710):
>
> - **Coordinate system (0022):** CPU word k = physical row 127−k; execution runs CPU words
>   **127 down to the reset word**; all four lanes read through the Multibus complement.
>   Decode (in code: `aru_freerun22.decode22`): **type = stored `l2 & 3`** (0=MEMR, 1=MEMW, 2=IO,
>   3=idle); IO command bits assert on stored-0 (bit3 RESET, bit6 WR-XREG, bit7 WR-DA, bits 8-11 =
>   channels D/C/B/A, bits 12-13 → DAB source 0=none/1=RDRREG/2=XREG/3=RD-AD); **WA = `(l2>>2)&3`,
>   RA = `(l2>>4)&3`, CSIGN = `l2` bit 7 (1 = positive, E83-golden-anchored 0025)**;
>   **XFER/ZERO/cmag = `~l3`** (bit0/bit1/bits2-7); **offset/delay = stored `l1:l0` DIRECTLY**,
>   `addr = (CPC − stored) & 0xFFFF`. 13/13 factory programs validate.
> - **Frame (0023):** the hardware frame is **L+1 steps** (the row after the reset word executes;
>   an idle in all 13 programs). **fs = 30.72 MHz / 9 / (L+1)** per program — 31.3–34.1 kHz across
>   the bank; L=99 → the canonical 100 steps / 34.13 kHz; **CONCERT (L=104) = 32,508 Hz, measured
>   from a real unit's IR (0024)**. The old "128 steps fixed" was the WCS *storage* size (words
>   below the reset word are unexecuted staging).
> - **MAC pipeline (0023):** write-through operand (the shifter loads R[RA(w)] after w's own MS7
>   regfile write, at the next step's first ARUCK edge); the accumulator runs **one ARUCKE/ edge
>   behind the product register** (fig-3.4); own-sign at every partial product
>   (falsification-tested 0025); the ZERO clear is owned by w_{n−1} and lands after the capture.
> - **Capture (0024):** the result register's D inputs are on the **PP bus** (sat-mux/adder
>   output), so the XFER capture includes the in-flight pairC term combinationally — the full
>   group MAC. Chip attribution U43 = high byte / U44 = low byte (0027).
> - **★ The arithmetic law (0027):** the DAB is an **ACTIVE-LOW (complement-domain) bus** — the
>   whole datapath computes on complemented values, every boundary (XREG, FPC) complements back.
>   In that domain the traced wiring is EXACT with **no rounding hardware**: accumulate =
>   `ACC + (PR ⊕ rail) + cin`, `rail = inv(CSIGN/)`, `cin = inv(rail)`; result = a pure bit tap
>   of **PP3..18 (truncation)**; saturation = `Σ19⊕Σ18` selecting the ±2¹⁸ clamp, which also
>   feeds the accumulator. The E83 goldens reproduce 20/20 with zero corrections — the doc-era
>   "+4 round-half-up", "+3 dual-rail", and "−M−1 negative law" were CPU-domain bookkeeping of
>   this one truncation. (The value-level engine still carries ±1-2 LSB of that bookkeeping —
>   the plan-024 re-sync.)
> - **Modulation (0024–0027, measured):** the SBC triangle LFO rewrites ONLY the modulated tap
>   words per frame (CONCERT: words 56/57/107/108); period ≈ 325k instructions under true
>   62-ticks-per-frame pacing; depth byte `0x3CD4`. The true live co-sim renders CONCERT at
>   factory defaults to **LF 3.27 / mid 2.28 / broadband 2.68 s vs the documented 3.0/2.0/2.6-avg**.
> - **Parameters (0026–0027):** all five LARC pages mapped; byte↔display calibration from the
>   firmware's own formatter hits the documented endpoints exactly (decay 0.6–70 s, corners
>   170 Hz–19 kHz, % = byte/2.56); sliders have **soft takeover** (ignored until they cross the
>   recalled preset). Variations V1-V7 recalled via the real LARC keys; the w43/95 shelf sign
>   law verified predictively.
>
> Authorities: `docs/sessions/0022 … 0027`, `224XL_interconnect_netlist.md`,
> `224-signature-value-tables.md`, `224XL_timing_spec.md`, and the engine + probes in
> `tools/`/`tools/session0022_probes/`. **Claims below that contradict the above are historical.**

**Purpose.** Everything reverse-engineered about the 224XL reverb, organized to drive the two next
steps: (1) the **emulator-diff harness** and (2) the **bit-exact header-only C++17 core** (see
`docs/plans/480L_rom_to_plugin_guide.md`). Every claim here was recovered from the real v8.2.1 firmware
running in a Z80 emulator and/or the 224X Service Manual; confidence is flagged where relevant. Source
docs: `224XL_microword_fieldmap.md`, `224XL_record_name_map.md`, `224XL_param_sweep.md`,
`224XL_modulation_lfo.md`; source tools in `tools/`. ROM set: `ROMs/Lexicon 224/224XL v8_21`.

---

> ## ★ M0b NETLIST CORRECTIONS (2026-06-28) — schematic ground truth, read first ★
>
> The full board has since been **net-traced from the schematics** (`docs/reference/224/224XL_interconnect_netlist.md`,
> ARU 060-01318 + DMEM 060-02512 + T&C 060-02475, every signal-path net, triple-verified). That netlist is now the
> **authoritative source for all STRUCTURAL / wiring / part / field-map facts** and supersedes the items below in
> *this* doc. (It does **not** touch the reverb-behavior content — `0x4000`-vs-`0x3F4D`, dead-tank, decay — which
> remains the separate open problem in the Session-11 banner.)
>
> **Hardware microword field map (netlist §G3R — schematic-traced, supersedes the firmware-storage table in §3):**
> `MI0–15`=OFFSET → OFST0–15/ · `MI16`=device-select · **`MI17`=MEMAC** · `MI18/19`=WA0//WA1/ · `MI20/21`=RA0//RA1/ ·
> `MI22`=PROT · `MI23`→CSIGN logic · **`MI24`=XFER** · **`MI25`=ZERO-gate** · **`MI26–31`=coeff C0/–C5/**. The doc's §3
> "lane N / bit M" positions are the *firmware-storage* view (behaviorally fit, possibly with byte inversions) — where
> they disagree with this hardware map (e.g. XFER/ZERO are lane-3 = MI24/25, not lane-2), the hardware map governs;
> reconcile via the byte inversions, do not assume the literal bit slots match.
>
> **Key corrections (structural):**
> - **★ CSIGN is NOT a stored/decoded microword bit.** It is the **`tc_U20` (74S112) JK-FF output** — ARUCKE/-clocked,
>   AS0-gated, a function of MI23 (MI23→tc_U18.QD→tc_U19.Q4→tc_U34→JK). A faithful model must replicate the JK toggle,
>   not read CSIGN from "lane bit 7." (netlist §3.10) — *this overrides the §3 "field-bit map is ✅" line below for CSIGN.*
> - **Coefficient serializer = `74195` (not "LS195"):** M0/ ← `tc_U11` (even C0/C2/C4), M1/ ← `tc_U10` (odd C1/C3/C5). (§3.9)
> - **Multiplier = modified-Booth (radix-4)** — the even/odd M0//M1/ streams are the two Booth selects. Service Manual
>   §3.7 calls the same mechanism "modified shift and add." (§4F.5)
> - **WCS = four MCM68B10 = `tc_U43/U29/U15/U2`** (MI0-7/8-15/16-23/24-31). The Service Manual §5 diagnostic names them
>   U3/U18/U33/U48 — a **manual-internal designator inconsistency**; the schematic/trace designators govern. (§3.1)
> - **DMEM delay memory = ONE 64K×16 bank** (`dmem_U20–U35`, 4164, CAS0/). `dmem_U1–U16` are **NOT populated** this rev;
>   no bank-select (top carry-out `dmem_U64.pin9` = n/c, `CAS1/` hard-disabled). The "128K / 2-bank / carry=bank-bit"
>   framing is **superseded** (older revs used 16K-class parts in two banks). (§5.5, §G3D)
> - **Delay-line part = `DL6308`** (the earlier "DL630B/DLG30B" was an OCR misread), `dmem_U59`. (§6D)
> - **Clock origins traced:** MC = PLL (`tc_U27` mc4044 + `tc_U41` ÷15, ×15 from `02/`) → tapped at `tc_U40.pin11`;
>   MS0-8 = `tc_U56` (÷9) + `tc_U39` (shift-reg); AS = `tc_U23`; the offset latch + field registers + RESET FF all clock
>   on **`DAB RSTB/`** (the per-step strobe — what some notes called "tcCLKA"). (§6T)

---

> ## ⚠️ CONFIDENCE STATUS BANNER (Session 11, 2026-06-25) — read first
>
> Taxonomy: ✅ CONFIRMED · 🟡 PARTIAL (faithful but interpretation unverified) · 🔵 INFERRED · 🟠 GUESS ·
> ⚪ UNKNOWN. Full state + validation plan: **`docs/plans/224XL-validation-plan.md`**.
>
> **The single biggest correction:** a *second* decode pipeline (`tools/aru_datapath.py`) read the microword
> from **`mem[0x4000:0x4200]`** and was iterated for ~9 sessions chasing a "dead tank." **`0x4000` is the
> wrong source** — proven in Session 11 (CHAMBER/non-FE → `0x4000` is all zeros; the firmware's real offset
> table at **`0x3F4D`** matches the firmware load byte-for-byte). The delays in *this* doc come from the
> **firmware-driven** pipeline (`harvest_xl.py`/`aru224_emulate.py`, the `0x3F4D` source) and are the **correct**
> ones — short, sensible (CONCERT 4–176 ms, 176 ms recirc loop). Where this doc and `aru_datapath`/`0x4000`
> disagree, **this doc is right.**
>
> **What is ✅ CONFIRMED:** the DSP architecture; the DAB one-driver/cycle + float-hold behavior; the device
> decode (U47/U48/U49 — MEMR/MEMW/RDRREG/RD-AD/RD-XREG/WR-DA, MI4 gate); the address adder + straight OFST
> wiring + standard DRAM mux (`addr=CPC−offset`); the register file (LS670, WA=MI18/19, RA=MI20/21, addr-3
> pass-through); `/32` coeff scale + ±2¹⁸ rail; program names (20/20 vs directory); the program-load mechanism
> (B55B + interpreter, FE/non-FE). The **field-bit map** (which bits mean what) is ✅ — with two M0b refinements
(see top banner): **CSIGN is the `tc_U20` JK-FF, not a directly-applied stored bit**, and the §3 "lane/bit"
table is the *firmware-storage* view (reconcile vs the hardware MI map, netlist §G3R).
>
> **What is 🟡 PARTIAL:** that `aru224`'s `0x3F4D` delays are the ARU's *actual* addresses and that
> `delay=−offset` is the right interpretation (the read is faithful/byte-identical, but that is near-circular —
> it reads the firmware's *own* output; needs the firmware-routine teardown, Track A). ~~DMEM 128K/bank-select~~ → ✅ RESOLVED (M0b netlist): ONE 64K×16 bank (`dmem_U20–U35`), no bank-select; see top banner.
> The modulation engine. The 16-bit fixed-point / FPC scaling numbers.
>
> **What is 🔵 INFERRED / 🟠 GUESS:** `inv_l3` coeff polarity (🟠); the FE writeptr-base/SIZE scaling (🟠);
> MAC ordering; the offset↔control per-step alignment (⚪).
>
> **What is ⚪ UNKNOWN (the headline gap):** **no decode, in either pipeline, has ever been run end-to-end
> through a faithful datapath to produce a correct 224XL reverb.** "Looks like a reverb tap map" / "decodes to a
> coherent graph" was plausibility, never proof — the same false-confidence that made the `0x4000` error
> persist for days. Treat every "RESOLVED/complete/verified" claim *below* against this bar: if its only support
> is plausible structure, it is at most 🟡. The firmware's own ARU POST self-test is currently **suppressed**,
> not passed (Track B exists to fix that).
>
> One internal inconsistency to flag: this doc says **128 steps/sample** (from the firmware build loop), while
> `224XL_system_architecture.md` says **100** (from the manual). Both are cited; treat the step count as 🟡
> until reconciled (likely 128 hardware slots with ~100 non-NOP).

---

## 1. System architecture

The 224XL is two computers:

- **SBC** — a Z80 control computer. Runs the LARC serial UI, manages programs/parameters, **builds and
  loads the WCS microcode**, and **continuously modulates** it. Does NOT compute audio.
- **DSP** — three modules (T&C, ARU, DMEM) forming a microcoded reverb engine. **Executes the WCS
  microprogram at 34.13 kHz**, one pass per output sample, reading/writing a large delay memory (DMEM)
  and the analog I/O (FPC). THIS is what the C++ core reimplements.

Data flow: `program record → SBC build engine → WCS image (microcode) → ARU executes → audio`.
Parameters and modulation are the SBC rewriting WCS coefficient/offset bytes over time.

**Step count — CORRECTED (0022/0023; supersedes the "128 fixed" claim).** The WCS *stores* 128 words,
but execution runs **CPU words 127 down to the program's reset word** (reversed — the SBC address
lines are active-low Multibus and the word-address mux is uncompensated), and the hardware frame is
**L+1 steps** where `L = 128 − reset_word` (the row after the reset word executes too — an idle in
all 13 factory programs; hardware-confirmed by the T&C signature reference FP54 = +5V @ N=30 for the
30-step diag-3 frame). Words below the reset word are **unexecuted staging** — the 128-entry build
loop (`0xB65A`) fills storage, not the frame. RESET is a WCS-decoded IO command (stored bit3 == 0 on
an IO-typed word), one per program, riding the final WR-DA (session 0022, 13/13). The SM's
"count 99 / 100 steps" and the 128-entry build are both right — they describe different things.

**Sample rate — MEASURED (0024).** **fs = 30.72 MHz / 9 / (L+1)**, per program: the 224XL is a
variable-frame-rate machine (31.3–34.1 kHz across the bank). L=99 programs run the canonical
100 steps → 34.13 kHz; **CONCERT (L=104, 105 steps) runs 32,508 Hz — measured from the benchmark
IR of a real unit** (envelope-warp s=1.000; autocorrelation lags match to ~0.2%). The converters
are frame-slaved (FPC syncs to RESET/), so they follow the loaded program's rate.

### SBC memory map (for driving the emulator)

| Region | Window | Role |
|---|---|---|
| SBC1 | 0x0000–0x07FF | reset, LARC serial, boot, power-up self-test |
| SBC2 | 0x0800–0x0FFF | ARU/DSP I/O drivers, POST |
| SBC3 | 0x1000–0x17FF | program directory/load, NVS dispatch |
| battery RAM | 0x2000–0x27FF | user registers (saved program variations); 0xFFFF = DIP switch |
| SBC RAM / stack | 0x3C00–0x3FFF | working state, stack; **WCS image staged + modulated here** |
| **WCS** | **0x4000–0x41FF** | the **128-step** microprogram (4 SRAMs, see §3); memory-mapped to SBC |
| NVS1 | 0x8000 | ARU runtime engine (`CALL 0x8000`) |
| NVS2 | 0x9000 | per-program code + param **labels** (CONCERT @0x9CDE = "LOW MID XOV HFD DEP PDL") |
| NVS3 | 0xA000 | name table @0xA002, directory @0xA446, loader/interpreter 0xA791/0xAA9F |
| NVS4 | 0xB000 | math/pack bank (packers 0xB4F0/0xB4FF), coeff record array @0xB800 |
| NVS5–7 | 0xC000–0xEFFF | continuation of the 21×682-byte record array |
| NVS8 | 0xF000 | per-program parameter/range records |

---

## 2. The ARU datapath (the C++ core's execution engine)

From Service Manual §3.7 + the ARU schematic #060-01318 (verified: register file = four **LS670** chips,
4-word×4-bit each with **independent read/write addressing**).

Components:
- **Register file** — 4 registers × 16-bit. Independent **write address WA (2-bit)** and **read address
  RA (2-bit)**. `DAB WSTB/` writes the DAB into R[WA] **every cycle** (data not always meaningful).
  **Address 3 = pass-through** (dummy/scratch write location).
- **Multiplier** — 16×6-bit 2's-complement, **saturating**; a **modified-Booth (radix-4)** shift-and-add done
  **two bits at a time** via a dual-rank shift register (one cycle per 6-bit multiply; the even/odd coefficient
  streams M0//M1/ are the Booth selects — SM §3.7 calls it "modified shift and add"). Coefficient *magnitude* =
  6 bits `C0–C5`. The add/subtract sign **`CSIGN/` is *not* part of the stored coefficient — it is the `tc_U20`
  (74S112) JK flip-flop output** (ARUCKE/-clocked, AS0-gated from MI23; netlist §3.10): the model must replicate
  the JK toggle, not just read a sign bit.
- **Accumulator** — 20-bit. `ZERO/` clears it.
- **Result register** — 16-bit. `XFER/` (clock XFER CK) loads it from the accumulator.
- **DMEM** — **circular delay memory of 65536 words → `DMEM_MASK = 0xFFFF`** (schematic #060-02512:
  **one 64K×16 bank** of sixteen 4164 DRAMs; no bank-select; position base = 0). Addressed by a 16-bit
  **current-position counter** (incremented once per sample) **minus** the microword offset. The DAB
  carries DMEM data, FPC audio, the result register, or the SBC XREG.

  **Address/delay convention — CORRECTED (0022; supersedes the `~stored` reading):** the delay/offset
  is the **stored `lane1:lane0` value DIRECTLY** — `addr = (CPC − stored) & 0xFFFF`. (The OFST/ bus
  *lines* carry the complement and the adder's carry-in supplies the +1; reading the STORED bytes,
  no inversion is applied. The old `offset = ~stored` rule was half of the coordinate-system error.)
  The "delay in samples" a tap represents = the stored offset; the circular buffer makes the position
  base irrelevant; the reverb topology is in the read/write relative offsets. In code:
  `aru_freerun22.decode22` / `aru_freerun22_rtl.program_rows22`.

### The 20-bit multiplicand alignment (critical for bit-exact)

Per §3.7: forming the 20-bit operand from the 16-bit register value `x`:
- the **MSB of x (x[15]) becomes the two MSBs** of the 20-bit word (bits 19,18 = sign extension),
- **x[15:0] occupies bits 18..3**,
- the **low 3 bits (2,1,0) are tied to 0**.

So `operand20 = sign_extend(x, 17) << 3`. Overflow detect = XOR of the top two bits (must match unless
overflow). On overflow, saturate to most-positive / most-negative.

### Per-step execution — SUPERSEDED (0022–0027): see `tools/aru_freerun22_rtl.py`

The pseudocode that used to sit here (128 fixed steps; FPC selected by offset bit15; a `b3` write-back
bit; same-step MAC retire; `RES = sat16(ACC>>3)` with floor) is the pre-0022 model and is WRONG on
every one of those points. The current per-step semantics, verified end-to-end, are (per executed row
w_n, in traced edge order — `RTL22.step` is the code of record):

- device phase by **type = stored `l2&3`**: MEMR (DMEM DOUT → DAB), MEMW (RDRREG drives the DAB and
  the DAB is written to `DMEM[CPC − stored]`), IO (source per the sel field: RDRREG / XREG / RD-AD;
  WR-DA emits the DAB to the selected channels; RESET fires here), idle (bus hold);
- the regfile is written **every step** at MS7 (`R[WA(w_n)] ← DAB`);
- the multiply of w_n executes physically during step n+1 (write-through operand), its partial
  products retiring at the following ARUCKE/ edges (**the accumulator runs one edge behind the
  product register**, fig-3.4);
- an XFER on w_{n−1} captures at step n's slot-3 edge from the **PP bus** (ACC + the in-flight pairC
  — the full group MAC); a ZERO on w_{n−1} clears the accumulator one edge after the capture;
- **all values on the DAB / in the regfile / in DMEM are complement-domain** (session 0027); the
  physical result register is a pure PP3..18 bit tap (truncation — no rounding hardware).

`position` (CPC) increments once per frame on the RESET event; the frame is L+1 steps (§1).

---

## 3. The WCS microword (the instruction format)

WCS = 4 × (128×8) SRAM. For step `S`, the 4 bytes are at `0x4000 + S*4 + lane` (SBC addr bits[1:0]=lane,
[8:2]=step). **Lane→SRAM** (manual diag E20–E23): lane0=U49, lane1=U33, lane2=U18, lane3=U3. *(M0b: those are
the Service-Manual §5-diagnostic designators — a manual-internal inconsistency; the **schematic** WCS SRAMs are
**MCM68B10 `tc_U43/U29/U15/U2`** = MI0-7 / MI8-15 / MI16-23 / MI24-31 respectively, netlist §3.1.)*

**Storage is active-low** with a mixed-polarity quirk: the OFFSET and the LANE2 CONTROL byte are stored
complemented; the LANE3 coefficient **magnitude** is stored direct. A `NOP`/pure-delay step ⇔
`lane2==lane3==0xFF` (the control+coefficient half is all-zero in true logic; lanes 0–1 may still hold a
don't-care offset, so the full 32-bit word is not necessarily all-zero).

| Lane | Bits | Field | Decode | Conf |
|---|---|---|---|---|
| 0–1 | 16 | **OFST** | `offset = (~(lane1<<8 \| lane0)) & 0xFFFF`; **DMEM addr = (position − offset) & 0xFFFF** (see §2) | HIGH |
| 3 | 6:0 | **COEFF mag** | `lane3 & 0x7F` (**raw, direct/linear** — packer 0xB4FF is magnitude-direct); **effective C = mag >> 1 (6 bits), applied as C/64 = mag/128** (§4, §6) | HIGH |
| 3 | 7 | **CSIGN** (stored sign) | raw bit7, active-low: `1 ⇒ negative`. **M0b: the *datapath* `CSIGN/` is the `tc_U20` JK-FF output, not a direct read of this bit — see the reconciliation note below.** | 🟡 |
| 2 | 5:4 | **RA** | `((~lane2)>>4)&3` — read-register address (RA1,RA0) | HIGH (datapath-validated) |
| 2 | 3 | **RW/SRC (b3)** | `((~lane2)>>3)&1` — `RDRREG/`=A50: result-register tristate OE onto DAB. `b3=1` ⇒ RES drives DAB and is written back to `DMEM[addr]` (comb/allpass feedback write-back); `b3=0` ⇒ `DMEM[addr]` (or FPC) drives DAB (a read). Independent stored bit — firmware-confirmed (copied verbatim from the program record). **DMEM write-back is gated by b3, not XFER; XFER (clock) independently loads the result register.** | HIGH (schematic + firmware) |
| 2 | 2 | **XFER** | `((~lane2)>>2)&1` — load result register / write the tank | HIGH |
| 2 | 1:0 | **WA** | `(~lane2)&3` — write-register address (3 = pass-through) | HIGH |
| 2 | 7 | **ZERO** | `((~lane2)>>7)&1` — clear accumulator (opens a MAC block) | HIGH |
| 2 | 6 | **PROTECT** | `((~lane2)>>6)&1` — WCS-access protect / MAC-enable (≈always 1 on active steps) | MED |

> **★ M0b — firmware-storage table vs hardware MI map (reconcile; do not assume they match).** The table above
> is the **firmware-storage** decode (the byte/bit layout the SBC writes — behaviorally validated, it reproduces
> the correct coefficients/control). The **hardware** microword map traced from the schematic (netlist §G3R) is:
> lane-2 byte (MI16-23) = {MI16 device-select, MI17 MEMAC, MI18/19 WA0//WA1/, MI20/21 RA0//RA1/, MI22 PROT,
> MI23 → CSIGN logic}; lane-3 byte (MI24-31) = {**MI24 XFER, MI25 ZERO-gate, MI26-31 = 6-bit coeff C0/-C5/**}.
> So in *hardware*: XFER/ZERO live in **lane-3** (not lane-2), the coeff is **6 bits (MI26-31)**, and lane-3 bit 7
> = MI31 = **C5/** (not CSIGN); **CSIGN is the `tc_U20` JK-FF** (driven from MI23). The firmware-storage table and
> the hardware MI map therefore **disagree on literal bit positions** — the difference is absorbed by the storage
> byte order + active-low inversions. **This is an open reconciliation** (a known "encoding ≠ literal wiring"
> hazard): keep the validated table for *decoding the firmware image*, but treat the hardware MI map as the wiring
> ground truth, and verify the CSIGN-JK behavior (does it *follow* or *toggle* the stored sign?) against the J/K logic.

**RA/XFER resolution** (the hard part, now settled + schematic-confirmed): running the decoded CONCERT
microcode through the ARU datapath, `RA=(b5,b4)` is the **only** assignment that forms a coherent
recirculating reverb tank; `(b5,b3)`/`(b4,b3)` collapse to silence. Corroborated by data-flow liveness,
the RA-independent-of-WA constraint, and XFER=b2 firing on exactly the result-transfer steps. The exact
split of lane2[5:2] = `b5,b4`=RA · `b3`=RW/SRC · `b2`=XFER.

**T&C schematic #060-02475 (now in hand) authoritatively confirms the field architecture.** Reading the
microinstruction → ARU connector signal map off the sheet: `OFST0–OFST15` = pins A9–A24 (16-bit offset);
**`WA0/`=A44, `WA1/`=A45, `RA0/`=A46, `RA1/`=A42** (separate 2-bit read + write addresses);
**`ZERO/`=A49, `XFER CK`=A27** (XFER is delivered as a gated clock, not a static level),
**`CSIGN/`=A48, `PROT/`** each a distinct line; **`RDRREG/`=A50** (the b3 / RW-SRC line — the result
register's tristate output-enable onto the DAB, driven by ARU U43/U44 = 74F374 pin-1 OC/);
coefficient `C0/–C5/` serialized (U10/U11 74195 shift registers, clocked by ARUCKE/AS1, serialized
into M0//M1/ as 2 bits/state × 3 states); FPC strobes `RD AD/`, `WR DA/`, channel selects `SDAA–SDAD`
(U32). **Every control signal is active-low** (the `/` suffix) — confirming the complemented-storage
decode — and **every field is a separate signal** — confirming RA≠WA independence. `RESET/` is generated
by flip-flop **U25 (74S74)**, a decoded/registered signal, **not** a microword data bit (confirming §1's
hardwired counter-wrap RESET). The schematic thus confirms the field structure, active-low storage, and
RESET mechanism; the literal microword-bit→pin *index* wiring (the U19/U45 register taps) is at the
scan's legibility limit, but the bit assignment is already datapath-validated (above).

**Pin correction (from prior note):** an earlier draft stated `XFER/`=A49; the correct reading from
ARU schematic #060-01318 + T&C #060-02475 is **`ZERO/`=A49** and **`XFER CK`=A27**.

Decoder: `tools/decode_microword.py` (`decode(power_up_id)` → per-step dicts with delay, coeff, CSIGN,
WA, RA, RW, XFER, ZERO, PROT).

### FPC audio I/O (address-decoded into the offset field) — full details in §12

Analog I/O is selected by the **offset high bits** (no dedicated FPC bit): **`offset & 0x8000` = FPC
select** (vs delay RAM); **`offset & 0x4000` = channel** (0 = right→B,C / 1 = left→A,D). **Input read** =
read step `WA=2`, bit15 set, `low14 = 0x3FFF` (`RD AD/`); **output write** = pass-through `WA=3` step,
bit15 set (`WR DA/`, channel from bit14). Verified via the Zero/Max-Delay diagnostic programs — full
derivation, the decoded diagnostic table, and the live-image position-base caveat are in **§12**.

---

## 4. Arithmetic & validation vectors (for bit-exact)

The reverb character lives in the integer ARU arithmetic. All core details are now RESOLVED (firmware +
schematic + hardware IR confirmed). Use the diff harness (§9) and the manual's exact test vectors to
verify the C++ implementation.

- **Coefficient encoding — CORRECTED (0022–0025; supersedes the "C/64" reading).** The coefficient is
  **6 bits at a /32 scale**: `cmag = ((~l3)>>2) & 0x3F`, value 32 = ×1.0, range ≈ ±2 (the E83
  self-test's +42/32 = 1.3125 is only representable at /32). **Sign = stored `l2` bit 7, 1 = positive**
  (E83-golden-anchored, 0025; delivered to the datapath through the tc_U20 JK with the traced one-step
  window). XFER/ZERO are `~l3` bits 0/1. The old "7-bit magnitude >>1, applied /64" table was the
  pre-0022 lane misread.
- **`cmag=0` baseline (plan-016 active-low NAND array) — reconciled.** `cmag=0` is the plan-016
  active-low NAND-array baseline (the "+3 ACC units per `cmag=0` multiply" = the all-ones product
  register). For a **single** multiply it correctly rounds to 0 at the `>>3` round-half-up (matches every
  golden). In the free-run MAC, 19 consecutive `cmag=0` bus-move steps accumulate ~+57 → a ≈−73 dB DC
  trickle — **faithful to the gate model, NOT the dead-tank cause** (§6.4). Cross-multiply accumulation
  of the baseline is untested by plan 016 (which only exercised single-step); flag as a sub-LSB open
  item, like the `cmag=63` +3.
- **Gains ≥ 1 arise from MAC accumulation, not a single multiply (RESOLVED).** The Service Manual's
  ×1, ×5/4, ×42/32 gains arise from **4-step MAC accumulation gated by the ZERO bit**, firmware-
  confirmed via the ADD'L MULT diagnostic (handler 0x0D99): stored lane3 bytes → gains:
  `0x7D` (mag125, ZERO=0) → **×1.0**, `0xBD` (mag61) → **×−0.5**, `0x7D` (ZERO=1) → **×−1.0**,
  `0xDD` (mag93) → **×−0.25**, `0x5D` (mag93) → **×−1.25**.
- **20-bit accumulator (RESOLVED).** LS163 counters; LS157 saturation muxes; LS86 two-MSB overflow XOR.
  Saturates to ±524287. `ACC` is 20-bit; the multiplicand alignment is `sign_extend(x,17)<<3` (§2).
- **Result register transfer — REFINED (0024/0027).** The 74F374 D inputs are on the **PP bus**
  (sat-mux/adder output), so the capture = the accumulator PLUS the in-flight pairC term. Physically
  the transfer is a **pure PP3..18 bit tap — truncation of the complement-domain value; there is no
  rounding hardware** (0027; the CPU-domain "sat16((ACC+4)>>3) round-half-up" was bookkeeping of the
  same bits). Chip attribution: U43 = high byte, U44 = low byte.
- **b3 read/write (RESOLVED — §3).** `b3=1` ⇒ RES drives the DAB and is written to `DMEM[addr]`
  (comb/allpass feedback write-back); `b3=0` ⇒ `DMEM[addr]` reads. Gated by `RDRREG/`=A50 — an
  independent stored bit (not derived from any field combo). DMEM write-back is gated by b3, not XFER.
- **Register file — read-before-write (RESOLVED).** 4× LS670 with independent read/write addressing.
  Read port returns the value **before** this cycle's `R[WA]=dab` write. When WA==RA the multiplicand
  is the old (pre-write) value. `DAB WSTB/` writes every cycle; WA=3 = pass-through scratch.
- **Comb-closer ordering — SUPERSEDED by the traced pipeline (0023/0024).** There is no "b3
  write-back bit"; MEMW-typed words write the DAB (driven by RDRREG) into DMEM, and the capture/
  clear/retire ordering follows the fig-3.4 pipeline (capture at slot-3 from the PP bus; the ZERO
  clear one edge later; each word's products retire one step behind). See §2 and
  `aru_freerun22_rtl.py`'s header for the full edge schedule.
- **Rounding.** Arithmetic floor (right-shift `>>3`) — toward −∞, not toward zero.
- **Service-Manual multiplier test vectors** (Diagnostic "ARU TESTS" / "ADD'L MULT", use as C++ unit
  tests): coefficients **+21/32, +42/32, +63/64**, and **×1, ×1/2, ×−1, ×1/4, ×5/4**. Four multiplications
  each; the last two must trip saturation. Implemented in `mult_vectors_test.cpp` — all pass.
- **Saturation** — on positive/negative overflow force most-positive/most-negative (20-bit two-MSB XOR
  detector; sat16 at result register output).

**SCHEMATIC-NET CONFIRMATION (Session 4d, owner-traced — `docs/reference/224/224XL ARU pinouts from
060-01318.txt`).** The datapath above is now **wiring-verified**, not inferred:
- Accumulator = 5× **74LS163** (U45–U49): `AC0..AC19`; pin1 CLR\=**ZERO/**, pin2 CP=**ARUCKE/** (per-step),
  L\=GND (always parallel-load), ENP/ENT=GND (no count). Each ARUCKE/ edge: `AC ← PP` (data inputs PP0..19)
  or **0 if ZERO/** (synchronous clear overrides load).
- Adders = 5× **74F283** (U19–U23), ripple-carried: A=`AC` feedback, B=`U5..U9` (74S86 XOR = product⊕CSIGN),
  Σ→sat-muxes; LSB Cin=`U2` 74S04=CSIGN ⇒ `AC ± product`.
- Sat-muxes = 5× **74F157** (U33–U37): SEL=`SAT` (U42 74S86 two-MSB XOR), I0=Σ, I1=`B-IN` (sat constant),
  Y=`PP` ⇒ `PP = saturate(AC ± product)`.
- Result reg = 2× **74F374** (U43/U44): D=`PP3..PP18`, Q=`DAB0..DAB15`, clk=XFER CK, OE=RDRREG/ ⇒
  **`RES = PP[3..18]` = exactly `>>3`** (reads the *combinational* PP bus, not latched AC).
- **ZERO clears on the FIRST multiply sub-state** (the serial multiply = 2 coeff-bits/state × 3 states only
  yields the test-vector-correct product if not cleared mid-multiply) ⇒ "clear then accumulate" = the
  committed model. Net: the whole accumulate→saturate→transfer path + clear timing is **faithful**.
- **Still un-traced (the only ARU gap):** the *multiplier* itself — the chips between the LS670 operand and
  the U5–U9 XOR A-inputs (operand register + coefficient-gated/shifted partial-product). Needed for §3.2 of
  the faithful-reconstruction plan (per-state saturation). The sat constant `B-IN`/`SAT` source also untraced.

**✅ APPROXIMATION REGISTER — CLOSED (0023–0027).** Every item on the Session-4d list is now either
modeled or measured: (1)+(3)+(8) live modulation runs in the true interleaved co-sim
(`e2_live_cosim.py`, real LFO at real pacing); (2) the modulated taps are replayed from the
firmware's own byte writes (no interpolation model needed); (4)+(5) the serial multiply and the
saturation path are bit-level and per-pin verified (1467/1469, incl. the clamp value and its feed
into the accumulator); (6) fs is measured per program (CONCERT 32,508 Hz); (7) the FPC boundary is
modeled at the fixed-point level (the codec table run — plan 024 F2b — will pin its pins too).
Remaining known gap: the engine's ±1-2 LSB CPU-domain bookkeeping vs the physical law (plan 024 F1).

---

## 5. Programs & microcode extraction

20 reverb/effect programs. Selector ID = a record's first byte; the firmware finds the record by ID in
the @0xB800 array (page-wrap walk: `HL=0xB800; +0x2AA; if (L==0xFE) HL+=2`). Names are
firmware-authoritative, cross-checked 20/20 vs the NVS3 directory (`{flags=ID, group=bank, sub=prog}`).

**To extract a program's WCS microcode** (the per-sample microprogram):
```python
import sys; sys.path.insert(0,'tools'); import boot_xl as B
cpu,mem,larc,aru,ms,*_ = B.boot(power_up_id=0x01, verbose=False)   # 0x01 = CONCERT HALL
wcs = bytes(mem[0x4000:0x4200])     # 128 steps x 4 bytes (active-low)
```
Or `tools/decode_microword.decode(0x01)` for the decoded per-step list.

Program table (id · name · bank/prog · #modulated taps; full delays/gains in `224XL_record_name_map.md`
and per-program `224XL_param_sweep_<id>.json`):

| id | program | B/P | mod | id | program | B/P | mod |
|---|---|---|---|---|---|---|---|
| 0x01 | CONCERT HALL | 1/1 | 4 | 0x21 | CD PLATE A | 3/3 | 18 |
| 0x20 | BRIGHT HALL | 1/2 | 4 | 0x06 | HALL/HALL | 5/1 | 4 |
| 0x05 | DARK HALL | 1/3 | 8 | 0x0A | PLATE/PLATE | 5/2 | 4 |
| 0x40 | SMALL ROOM | 2/2 | 8 | 0x12 | PLATE/HALL | 5/3 | 4 |
| 0x08 | CHAMBER | 2/3 | 4 | 0x22 | PLATE/CHORUS | 5/4 | 10 |
| 0x80 | RICH CHAMBER | 2/4 | 2 | 0x42 | RICH SPLIT | 5/5 | 0 |
| 0x41 | DARK CHAMBER | 2/5 | 2 | 0x0C | CHORUS&ECHO | 4/1 | 12 |
| 0x81 | INVERSE ROOM | 2/6 | 0 | 0x14 | RES CHORDS | 4/2 | 0 |
| 0x02 | PLATE | 3/1 | 2 | 0x24 | M BAND DELAY | 4/3 | 0 |
| 0x10 | CD PLATE B | 3/4 | 16 | 0x11 | RICH PLATE | 3/5 | 0 |

Decoded structure (CONCERT, the canonical example): pre-delay line → symmetric allpass diffusers
(`-c,-small,-c`) → recirculating tank (4-step MAC blocks `[-c,-small,-c,+0.976]`, ZERO opens / XFER
closes, reads R3 feedback) → multi-tap output line. ~100–108 active steps per program.

---

## 6. Parameters (per-program transfer functions)

Each reverb exposes ~6 parameters (CONCERT = LOW MID XOV HFD DEP PDL; other programs use ATT/CHO/HFB/
DIF/BAND/NOTE/RTIM/SIZE variants — labels in NVS2). The C++ core needs, per program, **which WCS
steps each parameter rewrites and the value→coeff/delay curve**. These are recovered empirically.

**Param path:** LARC slider positions `0x3c00–0x3c05` → main-loop scan `0x8185` diffs vs last-seen
`0x3c16+` → handler `0x85f2` (type-scaling, param type in `0x3c33`) → apply walks the **`0x3CF4` group
table** (built by the interpreter `0xAA9F`) → rewrites the linked WCS coeff/delay bytes, **ramped by
the de-zipper** (so transitions smooth, not instantaneous). **Full disassembly-verified architecture in
§6.1; toggles §6.2; CONCERT group map §6.3; the free-run engine + dead-tank offset-source bug §6.4.**

### 6.1 Parameter-application architecture (FULLY TRACED — firmware-disassembly-verified, 2026-06-29)

The full apply path is now disassembled end-to-end. The headline correction: **all five LARC control
pages' parameter values live in ONE flat RAM array based at `0x3ca3`** (6 bytes per page × 5 pages =
30 bytes; a record header/type byte sits at `0x3ca2`). The 6 LARC faders at `0x3c00–0x3c05` are **only
the live fader-echo of the *current* page** — paging does **not** just swap the 6 sliders; the whole
30-byte block persists.

- **Array slot** = `0x3ca3 + page*6 + slider`, computed at **`0x862e`** (`A = (0x3c34)*6 + B`).
- **Page state:** `0x3c32` = raw page counter (the PAGE-key handler `0x8f50` does INC); `0x3c34` =
  derived/clamped page index (read only at `0x862e`; written at `0x1477`). *(This supersedes the
  earlier "page `0x3c3c`" pointer in the quick-reference.)*
- **Paging:** the PAGE key (`0x8f50`) advances `0x3c32`, recomputes `0x3c34`, and reloads the 6 sliders
  `0x3c00–05` from the new page's array slice (`0x87c2`).
- **Apply chain:** main-loop scan `0x8185` (DE=`0x3c00` live, HL=`0x3c16` last-seen, B=0..9; **B≤5 →
  handler `0x85f2`**) → `0x85f2` type-scales by program type (`0x3c33`), **queues a de-zip job**
  (pending-flag array `0x3c20+B`), sets dirty flag `0x3c51` → the **de-zipper applier `0xB000`** ramps
  the coeff/delay one step per main-loop pass and **packs the byte into the WCS `0x4000` image**
  (`0xB4F0` = 6-bit coeff magnitude into the upper bits; `0xB4FF` = sign into bit7 of the adjacent byte).
- **Group table `0x3CF4`** (built by the interpreter `0xAA9F`; 32 entries × 3 bytes; opcode low-nibble =
  count, bits `0x30` = sub-type `0x00`/`0x10`/`0x20`) links each parameter's group to its target WCS
  step(s); the step→coeff-address transform is **`0xAB0C`: `addr = 0x4003 + step*4`**.
- **Recall at load:** program-load `0x13B6` → lookup `0x133e` finds the program record in the `0xB800`
  array (21 records × `0x2AA` bytes; record 0 = CONCERT) → **`0x13d9`** (`LD DE,0x3ca2; LD B,0x30;
  CALL 0x0614`) recalls the **48-byte param/toggle block** into `0x3ca2..` → `0xa791` apply engine
  builds the **full** WCS image. ⇒ the variation defaults **are** recalled and the full WCS **is** built
  at load (boot: 110/128 steps already have built coefficients).

### 6.2 Toggles (the 3 PARAM-key switches)

Stored as **bits in one RAM byte `0x3ccd`**, loaded from the program record at load (`0xA892`):
- **bit0 (`0x01`) = Dynamic Decay** — gates LF/Mid Stop Decay; read at `0x83B4`.
- **bit6 (`0x40`) = Mode Enhancement** — gates the Chorus/LFO modulation engine `0xAD5C`
  (`AND 0x40; JP z` skips the whole LFO update when clear). *(This is the modulation enable referenced
  in §7 as "`0x3ccd` bit6.")*
- **bit7 (`0x80`) = Decay Optimization** — read at `0x83D1`.

**CONCERT boots `0x3ccd = 0xC0`** (Mode Enhancement + Decay Optimization ON, Dynamic Decay OFF). Toggle
cycle index = `0x3c41`; mask table @`0xa758`.

### 6.3 CONCERT group → param → WCS-step map (verified vs the param sweep + disassembly)

Page 1 (the 6 sliders, §6 table): **P0 LF Decay** → steps 43,95 · **P1 Mid Decay** → anchors
64,68,115,119 + interpolated allpass coeffs 62,63,66,67,113,114,117,118 (via the decay generator
`0x86b2`/`0x8da5`/`0x8e03`, **NOT** in the group table) · **P2 Crossover** → 45,46,97,98 · **P3 Treble
Decay/HF-damp** → 40,41,92,93 · **P4 Depth/input-diffusion** → 29–32,81–84 · **P5 Predelay** → DELAY
steps 42,94.

Page 2: **Chorus** → group g0 steps 57,108 (animated by the LFO modulation over the canonical taps
56/57/107/108, depth `0x3cd4`, rate `0x3cd3=0x20`) · **Diffusion** → group g19 steps 52,60,72,104,111,123
(the recirculation **allpass**, coeff ≈ −95/−0.74) · **tank feedback** → g20–29 steps 27,28,79,80
(coeff −127, near-unity).

### 6.5 CONCERT = Concert Hall, Variation 1 — boot preset

CONCERT (id `0x01`, record 0 in the `0xB800` array) = **Concert Hall, Variation 1**
(`docs/reference/224/224X_chapter8_variation_presets.md`; Owner's Manual ch.4). 5 control pages, 7
variations, average decay **2.6 s**; the manual notes Halls "have a relatively low initial echo density,
which gradually builds as time progresses" to a dense tail. The Var-1 preset recalled at load:

- **Page 1:** LF Decay 3.0 s · Mid Decay 2.0 s · Crossover 720 Hz · Treble Decay 6.30 kHz · Depth 33 ·
  Predelay 24.0 ms.
- **Page 2:** LF Stop 3.0 s · Mid Stop 3.0 s · Chorus 50 · HF Bandwidth 9.00 kHz · Diffusion 25 ·
  Definition 00.
- **Page 3:** Preecho Levels 00. **Page 4:** Preecho Delays 5.00/9.75/17.5/25.0 ms + Fine Predelay
  0.36/10.2 ms. **Page 5:** Size/Gate.
- **Toggles (`0x3ccd` = `0xC0`):** Dynamic Decay OFF · Mode Enhancement ON · Decay Optimization OFF.

**Transfer data:** `tools/param_sweep.py` / `batch_sweep.py` → `224XL_param_sweep_<id>.json` for all 20
programs. Each file lists, per parameter, the affected coeff steps and delay steps, with the value at 8
slider points (0x20…0xFF; 0x20 ≈ default). Curves are monotonic / piecewise-linear (e.g. CONCERT XOV is
exactly linear, Δ16/step). CONCERT example:

| Slider | Label | Controls |
|---|---|---|
| 0 | LOW | low-band decay (2 coeffs + the modulated taps) |
| 1 | MID | mid-band decay (16 allpass coeffs) |
| 2 | XOV | crossover (linear coeff pair) |
| 3 | HFD | **HF Decay = the manual's "Treble Decay"** — an *in-loop* air-absorption HF damping (band-split steps 40/41/92/93; Fig 4.1 puts it inside the Reverb block). **NOT** HF Bandwidth (= `HFB`, a page-2 *input* low-pass). Decode currently renders it inert — see investigation §0.10. |
| 4 | DEP | input diffusion (8 coeffs) |
| 5 | PDL | **predelay → DELAY steps** (42/94: 21839→147 samples), not a coeff |

For the C++ core: expose params as 0..1, map through the per-program JSON curve to the target
coeff/delay at the linked steps, and de-zipper (ramp) toward target (multi-rate, ≈ −4/−1 per control
tick) for click-free changes.

### 6.4 Free-run engine + the offset-source bug recurrence (M3, 2026-06-29)

A **free-run execution engine** now exists: `tools/aru_freerun.py` = class `FreeRunARU` (does **not**
touch the POST-green `tools/aru_rtl_dp.py`). It sweeps the WCS program counter 0→99 (RESET@99), does
per-step §2T device-decode DAB routing, the fig-3.4 deferred MAC as a 1-instruction pipeline, a signed
multiply-accumulate (`RES = sat16(ACC>>3)`), DMEM recirculation, and fixed-point I/O (inject at `RD AD/`,
capture at `WR DA/`). Verified: runs the whole 100-step CONCERT for 500k+ microinstructions with no fault;
zero-delay passthrough PASS; max-delay DMEM-delay PASS (impulse reappears exactly `delay` samples later);
a hand-built feedback comb decays exactly per coefficient. POST regression stays green on `aru_rtl_dp.py`
(E32/E40/E83/E91, multiply 20/20). `tools/render_wav.py` renders the free-run output to a 34.13 kHz WAV.

**★ Dead-tank root cause (the big one) — the `0x4000` offset-source bug recurred.** `aru_freerun.py`
initially sourced the per-step DMEM delay **offset** from WCS lanes 0/1 of the `0x4000` image
(`ofst=(l1<<8)|l0; addr=CPC+ofst+1`) — the **wrong source** (the same Session-11 error). For CONCERT
those `0x4000` lanes 0/1 give clustered ~0.9–1.7 s (≈30000-sample) **garbage** delays, so DMEM reads and
writes address **disjoint** regions and the recirculation loop never closes → **dead tank**. The real
per-step delays live in the firmware **`0x3F4D` offset buffer**, extracted by
`tools/aru224_emulate.py::tap_map(0xB800)` (runs the B55B builder; validated byte-identical to the
firmware load). *This reinforces the §2/banner authority of `0x3F4D` over `0x4000` for delays — the
`0x4000` image is the correct source for the COEFFICIENTS (lanes 2/3), not the free-run delay offsets.*

- ✅ **Offset↔control per-step alignment CONFIRMED** step-index-keyed and correct: `tap_map[s]` aligns
  perfectly with the boot8080 `0x4000` COEFFICIENTS[s] — step 0 = 362 ms predelay (the first MEMR),
  steps 5–23 = a **varied** 7–176 ms diffuser cluster (NOT the 19 identical 1.7 s taps the wrong source
  produced), a 176 ms recirc loop reused 4×. *(This advances the formerly-⚪ "offset↔control per-step
  alignment" item in the Session-11 banner to ✅ alignment-confirmed.)*
- ✅ **Offset SOURCE fixed → a SHORT decaying tail emerges.** With the corrected ms-scale offsets
  (`addr = CPC + offset[step]`, wired into `aru_freerun.concert_offsets()`) the feedback loops EXIST (≈72
  short write→read loops at 1–200 ms; write/read addresses overlap) and CONCERT goes from a *fully dead*
  tank (impulse → 2–4 live samples) to a **short ~0.5 s decaying tail** (noise burst → ~0.3 s tail; the
  DMEM buffer decays ~1.7 s). *(Earlier "loop closes / dense continuous field" was a flawed-test artifact —
  that matrix overwrote lanes 0/1 and corrupted the I/O routing; the clean `run_free(offsets=…)` result is
  the short tail above.)*
- 🟡 **The full ~2.6 s hall decay is STILL OPEN.** The tail decays too FAST (~0.5 s) — the loop gain is too
  low, so a further cause remains beyond the offset source: quantization-to-zero / coeff scaling / the
  per-frame LFO modulation. The offset SIGN is settled (of `{CPC−off, CPC+off, CPC−|off|}` only
  `addr=CPC+offset`/`delay=−offset` survives). A prior note that `0x4000`-raw matches
  `tap_map` for ~120/128 steps with ~5 head steps (lane0=`0x89`, i.e. CONCERT steps 0–4) repacked, and
  `delay=+offset`, is part of this still-being-reconciled picture. *(Do not overwrite the §2 `delay=−offset`
  convention — it remains 🟡; this is an added data point.)* A proper ~2.6 s decay also needs the
  per-frame LFO modulation (§7) run inside the free-run.
- ✅ **CAVEAT — contaminated `read_offsets`.** `tools/boot8080.py::read_offsets` reads a **contaminated**
  `0x3F4D` from the *booted* firmware (modified post-build: gives 576 ms for step 2 vs `tap_map`'s correct
  176 ms). Use `aru224_emulate.tap_map`, not the booted `read_offsets`, for free-run delays.

**Parameter hypothesis RULED OUT.** The dead tank was **not** caused by un-recalled parameters: the
page-1 slider coeffs **and** the page-2 Diffusion(=25)/Chorus(=50) defaults are all recalled into
`0x3ca3` and baked into the WCS at load (110/128 steps built; Diffusion/Chorus/feedback coeffs present at
boot; Mode Enhancement ON). Applying CONCERT Variation 1's full preset was a **no-op**. The dead tank was
the offset-source bug above.

**Engine timing (M4 diagnosis).** The two un-POST-tested timing choices — read-before-write of the
regfile operand, and the deferred-MAC retire ordering — were **proven inert** (toggling each leaves the
loop eigenvalue bit-identical), so neither is the dead-tank cause. The free-run output channel decode
(SDAA–D) in `aru_freerun.py` is a binary code but netlist §2T.4 says **4 independent reversed strobes**
(OFST8/→SDAD … OFST11/→SDAA) — a channel-**label** bug only, not an IR-value bug.

---

## 7. Modulation / LFO engine

The firmware continuously modulates selected tank taps (the chorus that de-metallizes the reverb).
Engine `0xAD5C–0xAE9B`, doc `224XL_modulation_lfo.md`.

- **Waveform: triangle.** A phase value steps ±1/±2 toward bounds at `0x3cd4` and reverses.
- **Paced by the main loop** (`0x816F → 0x8281 → 0xAD5C`), once per foreground pass.
- **Rate:** cascaded divider `0x3e45` (reload 8) × `0x3e46` (reload from **`0x3cd3`**); phase advances
  every `8 × 0x3cd3` passes (CONCERT `0x3cd3=32`). Full period ≈ 345k SBC instructions (~sub-2 Hz).
- **Depth:** bound **`0x3cd4`**. CONCERT `0x3cd4=4` → measured peak-to-peak delay swing **≈93 samples
  (±≈47)** on each modulated tap (measured over multiple LFO periods; an earlier "×10/→41" figure was a
  single-window undersampling artifact — use ±47). Swing scales ~linearly with `0x3cd4`. Optionally
  param-driven via `(param−15)×4` (`0xB3D4`).
- **Enable:** `0x3ccd` bit6.
- **Targets:** per-program modulated WCS steps (table §5, 0–18 taps), modulated in **anti-phase pairs**.
  Each modulated tap = a **fractional delay** whose interpolation coefficient (the allpass coefficient,
  computed at `0xAE72`: `SUB 4 / AND 3 / OR 3`) tracks the delay's fractional part. So in C++: a
  fractional delay line per modulated tap with allpass interpolation, LFO-swept.

For bit-exact-over-time, the C++ core must replicate this WCS modulation (it changes the offset + interp
coeff of the listed steps each control tick). The static (un-modulated) microcode is the same image with
those taps at their center value.

---

## 8. Tools & the emulator (how to get reference data)

In `tools/` (Python; `python` on Windows). The Z80 emulator is the ground-truth source of microcode,
modulation frames, and param mappings.

| Tool | Use |
|---|---|
| `z80emu.py` | pure-Python Z80 with IM1 interrupts. API: `Z80(mem)`, `.PC`, regs, `.step()`, `.in_hook/.out_hook`, `.interrupt()`, `.call(addr,max_ins)`, `.m`/`.rb/.wb/.rw/.ww` |
| `boot_xl.py` | boots v8.2.1 → main loop. `boot(power_up_id=ID)` → `(cpu,mem,larc,aru,milestones,cap,snap)`; `mem[0x4000:0x4200]` = WCS. Models LARC serial + active-low ARU latch + POST-pass |
| `decode_microword.py` | WCS image → per-step signal graph |
| `harvest_xl.py` | all-program names + delays + gains |
| `param_sweep.py` / `batch_sweep.py` | param→coeff/delay transfer tables (per-program JSON) |
| `aru_datapath.py` | **the ARU execution reference** (routing correct; arithmetic to tune) |
| `aru224_emulate.py` | build-engine decode (delays via `tap_map(0xB800)` from `0x3F4D`, gains via capture_coeffs) |
| `aru_rtl.py` / `aru_rtl_dp.py` | phase-accurate RTL clock engine + datapath (**POST-green**: E32/E40/E83/E91, mult 20/20) |
| `aru_freerun.py` | **free-run engine** (`FreeRunARU`): runs the whole 100-step program continuously (§6.4) |
| `render_wav.py` | renders the free-run output to a 34.13 kHz WAV |

Driving the live firmware (to capture modulation frames / param effects): boot to the main loop, then
step the CPU while firing the serial interrupt (`if cpu.IFF1 and (icount-last)>=64 and (larc.tx_en or
larc.rx_ready(cpu)): cpu.interrupt()`); the WCS at `0x4000` updates live. Inject a parameter by writing
the slider byte `mem[0x3c00+p]=v` with `mem[0x3c16+p]` differing + `mem[0x3c14]|=0x80`, then run. POST
self-test ports are stubbed (active-low ARU latch); the self-tests are modeled as "pass".

---

## 9. The emulator-diff harness (validation plan)

The Z80 emulator builds/modulates the WCS but does **not** compute audio (the real ARU hardware did).
So the bit-exact reference is the **Python ARU datapath model** (`aru_datapath.py`), and the harness has
two layers:

1. **Microcode parity (already achievable).** For each program, the C++ core must load the **identical
   WCS image** the firmware produces (`mem[0x4000:0x4200]`) and decode it with the §3 field map. Assert
   the C++ decode == `decode_microword.decode(id)` field-for-field. This guarantees the *program* is
   right.
2. **Arithmetic parity (RESOLVED).** Run the Python ARU reference and the C++ core on the same WCS
   with the same input, compare output **sample-by-sample (integer == integer)**. All arithmetic details
   in §4 are now resolved (coefficient encoding, b3/RDRREG/, result shift >>3, read-before-write, closer
   ordering). The reference and core are anchored by: (a) the Service-Manual multiplier test vectors (§4)
   as unit tests (all passing), (b) the current eigenvalue λ≈1.0008 (grows; the structural gap to the
   hardware P85 target λ=0.9999899 — missing band-split damping, NOT rounding — is the final item, see §10),
   and (c) the real-hardware
   IRs `P85 - 20.0 Seconds A.wav` (primary oracle, RT60≈20 s) and `Concert Hall V7.2.L.wav` (secondary)
   for decay-shape / HF / LFO ground truth. `diff_harness golden 01` → DIFF PASSED.
3. **Dynamic parity.** Drive the firmware emulator and the C++ core with the same parameter and time
   base; assert the C++ core's modulation + param de-zipper reproduce the firmware's live WCS frames
   (capture WCS frames from the emulator at control ticks; compare to the C++ core's WCS state).

Recommended core shape (per `480L_rom_to_plugin_guide.md`): one header-only C++17 class with an
**integer** datapath (`processSampleFixed(int32)->int32`, exact) consumed by the harness, plus a float
boundary (`processSample(float)->float`) for the DPF/STM32 wrappers.

### Hardware IR ground truth (now available)

Two real CONCERT HALL impulse responses are in the repo:

**Primary oracle (default param state, 20 s):** `IR/Lexicon 224XL/P85 - 20.0 Seconds A.wav`
- **RT60 ≈ 20 s** (clean single exponential, default CONCERT program).
- **Target λ = 0.9999899** at the 34.13 kHz native rate. Use for absolute eigenvalue calibration.

**Secondary (shorter param state):** `IR/Lexicon 224XL/Concert Hall V7.2.L.wav` (24-bit/96 kHz, mono/Left)
- **RT60 ≈ 4.86 s** (LF ~5.25 s, HF ~3.79 s — HF damping present). Target **λ ≈ 0.9999580**.
- **LFO/chorus** visible in the tail: ~2–3 Hz, mod depth ~0.76 samples. **Pre-delay ≈ 147 ms**.
- Use for decay-shape / HF roll-off / LFO validation and as a second eigenvalue crosscheck.

The RESOLVED arithmetic brings λ from the broken ~1.48 (sustaining) → **~1.0008** (grows, near-critical).
DMEM addressing (base=0, schematic #060-02512) and register file (#060-01318) are confirmed correct.
The remaining gap to the P85 target is **structural — missing frequency-dependent band-split damping, NOT
sub-LSB rounding** (refuted; see §10 and `docs/plans/224XL-concert-decay-investigation.md`).

Additional schematics now in hand (cross-reference): ARU #060-01318, FPC #060-01320, DMEM #060-02512,
DMEM #060-02273, Block-Diagram-Memory + zoom crops.

---

## 10. Open items (resolve during the build)

**RESOLVED (these were the two gating items):**
- **FPC audio I/O — RESOLVED (§12).** Address-decoded into the offset field: bit15 = FPC select, bit14 =
  channel (0=right→B,C / 1=left→A,D); input = read step `WA=2, low14=0x3FFF` (`RD AD/`); output =
  pass-through `WA=3` step (`WR DA/`). Verified by building the Zero/Max-Delay diagnostic programs
  (`0x0EFD`/`0x0EF4` → builder `0x0F2C`).
- **Executed step count + RESET — RESOLVED (§1).** **128 steps/sample, fixed** for all programs
  (verified: build loop `0xB65A`/WCS copy `0xAB55` both 128; last content step = 127 in every program).
  **RESET = a WCS-decoded condition, no *dedicated* microword bit** (verified: no bit unique to step 127) —
  **M0b: *not* a hardwired counter terminal-wrap**: SM §3.5 + netlist §3.11 = `tcWR·OFST3/` (tc_U34) → PC clear,
  "reset … generated by the WCS." SM puts it at count 99 (= 100 steps), in tension with the 128-entry build — see §1.
  Loop `S=0..127` and reset at the boundary (working model pending the 100-vs-128 reconciliation).

**Bit-exact arithmetic — RESOLVED (firmware + schematic + hardware IR):**
- **Coefficient encoding:** 6-bit magnitude C = mag>>1, applied as C/64 (= mag/128); sign = CSIGN
  (active-low; **M0b: `CSIGN/` is the `tc_U20` JK-FF, not a directly-applied bit — §3**); magnitude direct/linear. Gains ≥ 1 arise from 4-step MAC accumulation, not a single
  multiply. The "2 extra LSBs" (0xB4F0) belong to the modulation interpolation coefficient only.
- **Result-register shift:** `RES = sat16(ACC >> 3)` from a 20-bit accumulator. Arithmetic floor (>>3).
- **b3 / RDRREG/ (A50):** result register tristate OE onto DAB. `b3=1` ⇒ RES drives DAB + written to
  DMEM (write-back); `b3=0` ⇒ DMEM/FPC drives DAB (read). Independent stored bit.
- **Register file:** read-before-write (LS670); WA=3 = pass-through scratch; DAB WSTB/ writes every cycle.
- **Comb-closer ordering:** XFER loads RES before b3 drives the DAB — post-XFER value written to DMEM.
- **Loop eigenvalue:** RESOLVED arithmetic brings CONCERT λ from ~1.48 (broken) → **~1.0008** (grows;
  near-critical). DMEM addressing (base=0, schematic #060-02512) and register file (#060-01318) are
  confirmed correct. Remaining gap to hardware target (λ=0.9999899, P85 20 s IR) is **structural — missing
  frequency-dependent band-split damping, NOT sub-LSB rounding** (refuted; see §10 and
  `docs/plans/224XL-concert-decay-investigation.md`).
- Implemented in `tools/aru_datapath.py` and `libs/sgdsp/include/sgdsp/reverb/224xl.hpp`; verified
  integer-exact by the diff harness (DIFF PASSED) with multiplier unit tests passing.

**Confirmed correct (previously open):**
- **DMEM addressing** — one 64K×16 bank (sixteen 4164 DRAMs, schematic **#060-02512**). Formula:
  `addr = (pos − offset) & 0xFFFF`, position base = **0** (anchored by the input-read step s76,
  offset=0xFFFF, WA=2 ⇒ addr=pos+1). No bank-select; #060-02273 is the SBC program-memory board, not
  the delay RAM. **CONFIRMED CORRECT.**
- **Register file** — 4×LS670 (U29–U32, schematic **#060-01318** register-file zoom): WA/RA feed all
  chips, `DAB WSTB/` (A41) writes every cycle, no special address-3 gating — R[3] stores normally.
  **CONFIRMED CORRECT.**

**✅ The "final remaining item" — RESOLVED by the 0022 coordinate-system correction.** The λ≈1.0008
instability, the "missing band-split damping," and the whole eigenvalue hunt were artifacts of
decoding the WCS in the wrong coordinates (both pre-0022 pipelines). Under the corrected decode +
traced pipeline + E83 sign convention + live modulation, **CONCERT at factory defaults renders the
documented decays with zero tuning** (co-sim LF 3.27 / mid 2.28 / bb 2.68 vs documented 3.0/2.0/
2.6-avg), the octave ladder is monotone like the real unit, and the parameter levers track ch.4/ch.8.
The band-split damping exists and is exactly where the manual says (the crossover/shelf words —
w45/46/97/98 pole, w43/95 ± injection, HFD words 40/41/92/93).
**Fs — RESOLVED (0024):** fs = 30.72e6/9/(L+1) per program; CONCERT measured 32,508 Hz; there is no
4.37 MHz step clock (the step clock is MC/9 ≈ 3.41 MHz always; the frame LENGTH varies instead).

**Lower priority / corroboration:**
- **RA→bit + field map — schematic-confirmed.** Both schematics in hand: ARU **#060-01318** (LS670
  register file, independent RA/WA nets) and T&C **#060-02475** (signal map: OFST0-15=A9-A24,
  WA0/=A44, WA1/=A45, RA0/=A46, RA1/=A42, **ZERO/=A49, XFER CK=A27** (clock), CSIGN/=A48, RDRREG/=A50,
  PROT/; all active-low; RESET/ from flip-flop U25). Confirm: ZERO/=A49 (corrects prior draft's
  "XFER/=A49"). Field structure, active-low storage, RESET mechanism all schematic-confirmed. (Closed.)
- **Full bidirectional param curves** — sweep slider range below 0x20 (current grid is 0x20–0xFF).
- **Per-program modulation rate/depth** — read `0x3cd3`/`0x3cd4`/`0x3ccd` per program at boot (CONCERT
  given); a small batch pass captures all 20.

---

## 11. Quick reference — key addresses

- WCS image: `0x4000–0x41FF` (4-byte steps; SRAMs = MCM68B10 `tc_U43/U29/U15/U2` per the schematic — the
  "lane0=U49…lane3=U3" in older notes are the manual §5-diagnostic designators; active-low).
- Program record array: `0xB800` (page-wrap walk; ID = record[0]); lookup `0x13B6→0x133E`.
- Name table `0xA002`; directory `0xA446` (`{flags=ID,group,sub,page-hi,len}`).
- Build engine: interpreter `0xAA9F`, step-builder `0xB55B` (FE path) / `0xB65A` (non-FE pre-built
  table @recbase+0xA7..0x2A7), coeff packers `0xB4F0`/`0xB4FF`, coeff source `0xB510`.
- Params: live sliders `0x3c00–0x3c05` (current-page fader echo only), **flat param array `0x3ca3`**
  (6 bytes × 5 pages; slot = `0x3ca3 + page*6 + slider`, computed at `0x862e`; header byte `0x3ca2`),
  last-seen `0x3c16+`, scan `0x8185`, handler `0x85f2`, group table `0x3CF4` (built `0xAA9F`;
  step→addr `0xAB0C` = `0x4003 + step*4`), de-zipper applier `0xB000`, pending-flags `0x3c20+`,
  dirty `0x3c51`, param type `0x3c33`, **page state `0x3c32` (raw) / `0x3c34` (clamped)**, PAGE key
  `0x8f50`, page-reload `0x87c2`.
- Param recall at load: `0x13B6 → 0x133e` (find record) → `0x13d9` (`LD DE,0x3ca2; LD B,0x30;
  CALL 0x0614`, recalls 48-byte param/toggle block) → `0xa791` (build full WCS image).
- Toggles: `0x3ccd` (bit0 Dynamic Decay @`0x83B4`, bit6 Mode Enhancement @`0xAD5C`, bit7 Decay
  Optimization @`0x83D1`; loaded `0xA892`; CONCERT = `0xC0`); cycle index `0x3c41`, mask table `0xa758`.
- Modulation: engine `0xAD5C`, rate `0x3cd3`, depth `0x3cd4`, enable `0x3ccd` bit6, phase counters
  `0x3e45/0x3e46`, value writes `0xAE6C` (delay) / `0xAE8E` (interp coeff).
- Boot/normal-op: reset `0x0000→0x003B`, LARC handshake `0x0067`/`0xC8`, POST → `0x00CC` → `0x813B`
  (normal op), main loop `0x8169`, program load `0x13B6`, display `0x82CF`.

---

## 12. FPC audio I/O — the input read & 4 output writes (RESOLVED)

**How recovered.** The two minimal diagnostic programs whose behavior is fully specified by the manual
(§5: "7 ZERO DELAY" = input straight to output, no DMEM; "8 .5 S DELAY" = input → 0.5 s delay → output;
both route left→A,D, right→B,C) are *built in ROM*, not stored as records. The diag-menu dispatch
(SBC1 `0x032D` `JP 0x11BE` over the table at `0x0330`) sends item 7 → handler **`0x0EFD`** (ZERO DELAY)
and item 8 → **`0x0EF4`** (MAX/.5 s DELAY). Both call the WCS builder **`0x0F2C`**, which:
1. fills `0x4000–0x41FF` with `0xFF` (all-NOP);
2. reverse-copies (routine `0x0933`/`0x0938`, writes *downward* from `0x41FF`) a 4-step block from ROM
   `0x0F5F` into steps **124–127** (LEFT) and a 4-step block from ROM `0x0F6F` into steps **74–77**
   (RIGHT) — so source bytes land in lane order `[l3,l2,l1,l0]`;
3. patches step 29 (`0x4074=0xF7`, `0x4076=0xFE`);
4. issues `OUT(0x01)` then `OUT(0x03)` (= RUN).
ZERO DELAY's handler additionally patches the two `WA=3` output steps' offset low bytes
(`0x4130/0x4131` → step 76, `0x41F8/0x41F9` → step 126) to shorten the delay to ~0.

**Decoded diagnostic blocks** (offset = `~(l1<<8|l0)`; `ctl=~l2`; coeff = raw `l3`):

| pgm | step | l0 l1 l2 l3 | offset | b15 | b14 | low14 | WA | coeff | role |
|---|---|---|---|---|---|---|---|---|---|---|
| MAX | 74  | 7f e9 fe ff | 0x1680 | 0 | 0 | —     | 1 | −1.000 | DMEM delay-line (right) |
| MAX | 75  | 00 40 fd fe | 0xBFFF | 1 | 0 | 0x3FFF| 2 | −0.992 | **FPC INPUT read (right), RD AD/** |
| MAX | 76  | ff 7f fc 7c | 0x8000 | 1 | 0 | 0x0000| 3 | +0.976 | **FPC OUTPUT write (B,C), WR DA/** |
| MAX | 77  | ff cf fe 7d | 0x3000 | 0 | 0 | —     | 1 | +0.984 | DMEM delay-line (right) |
| MAX | 124 | 7f e6 fe ff | 0x1980 | 0 | 0 | —     | 1 | −1.000 | DMEM delay-line (left) |
| MAX | 125 | 00 00 fd fe | 0xFFFF | 1 | 1 | 0x3FFF| 2 | −0.992 | **FPC INPUT read (left), RD AD/** |
| MAX | 126 | ff 3f fc 7c | 0xC000 | 1 | 1 | 0x0000| 3 | +0.976 | **FPC OUTPUT write (A,D), WR DA/** |
| MAX | 127 | ff cf fe 7d | 0x3000 | 0 | 0 | —     | 1 | +0.984 | DMEM delay-line (left) |

(bit14 carries the channel only on FPC steps, where bit15=1: the left FPC steps 125/126 have bit14=1;
the plain DMEM delay steps 124/127 have bit14=0 — bit14 is just part of an ordinary delay address there.)

(ZERO DELAY = identical except step 76 offset → `0xBFFE` and step 126 offset → `0xFFFE`; i.e. the *only*
bytes that differ between zero-delay and half-second-delay are the `low14` of the two `WA=3` output
steps — proving those steps are the output writes and that the output offset's low bits set the tap.)

**The FPC encoding (authoritative for the C++ core):**
- **`offset & 0x8000` (bit15) = FPC select.** When set, the access targets the FPC "device on the DAB"
  (§3.8: "the analog I/O looks simply like another device that can be read from / written into via the
  DAB") instead of delay RAM. Delay-line steps have bit15 = 0.
- **`offset & 0x4000` (bit14) = channel group.** 0 → right channel (input R; outputs **B,C**); 1 → left
  channel (input L; outputs **A,D**). Matches the manual's program routing left→A,D, right→B,C.
- **Input step** = a *read* step (non-XFER, `WA≠3`) with bit15 set and `low14 = 0x3FFF`. Asserts RD AD/;
  the A/D sample for that channel is driven onto the DAB and latched into the read register. (Diag uses
  `WA=2`.)
- **Output step** = the *pass-through* step (`WA=3`) with bit15 set; asserts WR DA/ with the channel
  select. The result register is driven to the FPC double-buffer for that output pair. `low14` is the
  output/strobe code (and, on the diag, doubles as the delay-tap selector).
- Every active diag I/O step has **ZERO=0, PROTECT=0, XFER=0, RW=0** (`ctl` ∈ {0x01,0x02,0x03}); the
  device is chosen purely by the **offset high bits**, *not* by a dedicated FPC microword bit. This is
  why the 32-bit microword has "no spare bit" — FPC I/O is address-decoded, identical to a DMEM
  read/write but at addresses with bit15 set. (Confirms the earlier scouting note: RESET/strobes are not
  dedicated microword bits; they are decoded from address/counter state in the T&C+FPC.)

**Note on live reverb images — position base (CONFIRMED = 0).** In the diagnostic programs the WCS is
built with a position base such that the FPC steps decode cleanly (input `low14 = 0x3FFF`, channel in
bit14). In a live program image (e.g. CONCERT from `boot_xl`) the stored offsets are **absolute and
position-relative** (§2: "absolute offsets are large relative to an arbitrary position base that cancels
across read/write pairs"). The position base is **confirmed = 0** (anchored by the input-read step:
CONCERT step 76, `offset = 0xFFFF`, WA=2 ⇒ addr = pos+1; schematic #060-02512). So bit15/bit14 of a
*live absolute* offset is still a valid FPC marker at base 0. The reliable, base-invariant fingerprint
that always survives regardless of base is the **input read** at `low14 = 0x3FFF` with `WA=2`. For the
C++ core's per-step execution: branch on `offset & 0x8000` (with base=0 this is simply the raw offset
bit15) to route reads from the FPC input latch (channel = `& 0x4000`) and `WA=3` writes to the FPC
output channel (channel = `& 0x4000`, strobe = `low14`), instead of reading/writing DMEM.

---

*This document is the single source of truth for the 224XL reconstruction. Keep it in sync with the
per-topic docs (`224XL_microword_fieldmap.md`, `224XL_param_sweep.md`, `224XL_modulation_lfo.md`,
`224XL_record_name_map.md`) and the `tools/` reference implementations.*
