# Lexicon 480L ARU (330-04362) — Pin / Field / Operation Reference

Custom 18-bit CMOS arithmetic unit, 40-pin PDIP, made by Harris for Lexicon.
Manual descriptor: *"IC, DIGITAL, ARU, 18 BIT, CMOS, 15M"* (15M ≈ 15 MHz speed grade 🟡).
Two instances per HSP board: **U60** = "HSP Arithmetic Unit 1", **U89** = "HSP Arithmetic Unit 2"
(schematic 060-04391, sheets 6 & 7). Identical part; board nets differ only by a `1`/`2` suffix.

**Source:** transcribed directly from the uploaded schematic sheets.
**Confidence:** ✅ read from schematic · 🟡 inferred from naming/topology · ❓ unknown without bench characterization.

---

## 1. Complete pinout (40-pin DIP)

Pin numbers, names, and direction are ✅ (read from the drawing). The "Function" column is 🟡 unless noted.

| Pin | Signal (chip) | Dir | Board net (AU1 / AU2) | Function (inferred) | Conf. |
|----:|---|:--:|---|---|:--:|
| 1 | VSS | PWR | GND | Ground | ✅ |
| 2 | DAB10 | I/O | DAB1/2 bus b12 | Data bus bit 10 | ✅ name / 🟡 bidir |
| 3 | DAB11 | I/O | bus b13 | Data bus bit 11 | ✅/🟡 |
| 4 | DAB12 | I/O | bus b14 | Data bus bit 12 | ✅/🟡 |
| 5 | DAB13 | I/O | bus b15 | Data bus bit 13 | ✅/🟡 |
| 6 | DAB14 | I/O | bus b16 | Data bus bit 14 | ✅/🟡 |
| 7 | DAB15 | I/O | bus b17 | Data bus bit 15 | ✅/🟡 |
| 8 | DAB16 | I/O | bus b18 | Data bus bit 16 | ✅/🟡 |
| 9 | DAB17 | I/O | bus b19 | Data bus bit 17 (**MSB**) | ✅/🟡 |
| 10 | VCC | PWR | +5V | Supply | ✅ |
| 11 | WA1 | IN | WA1 | Write-address bit 1 | ✅ name / 🟡 fn |
| 12 | **AS2/** | IN | **C/** | Arithmetic-select 2 (active-low); board net is `C/`, sourced from the timing chain (U104), **not** the function PROM | ✅ name / 🟡 fn |
| 13 | WAO | IN | WAO | Write-address bit 0 | ✅/🟡 |
| 14 | RA1 | IN | RA1 | Read-address bit 1 | ✅/🟡 |
| 15 | RAO | IN | RAO | Read-address bit 0 | ✅/🟡 |
| 16 | DAB0 | I/O | bus b2 | Data bus bit 0 (**LSB**) | ✅/🟡 |
| 17 | DAB1 | I/O | bus b3 | Data bus bit 1 | ✅/🟡 |
| 18 | F0 | IN | F0 | Function-select bit 0 | ✅ name / 🟡 fn |
| 19 | F1 | IN | F1 | Function-select bit 1 | ✅/🟡 |
| 20 | F2 | IN | F2 | Function-select bit 2 | ✅/🟡 |
| 21 | VCC | PWR | +5V | Supply | ✅ |
| 22 | **OVLD/** | OUT | OVLD1/ → OVLD2/ | Overload / saturation flag (active-low) | ✅ name / 🟡 fn |
| 23 | BCON0/ | IN | BCON0/ | B-operand control 0 (active-low) | ✅/🟡 |
| 24 | SC/ | IN | SC/ | Shift control (active-low) | ✅/🟡 |
| 25 | CIO/ | IN | CIO/ | Carry in/out control (active-low) | ✅/🟡 |
| 26 | **MC** | CLK | MCB1 / MCB2 | **Master clock** (clock-edge symbol on pin) | ✅ |
| 27 | BCON3 | IN | BCON3 | B-operand control 3 | ✅/🟡 |
| 28 | AREG/ | IN | AREG/ | A-register load/enable (active-low) | ✅/🟡 |
| 29 | XCLK/ | IN | XCLK1/ / XCLK2/ | **Transfer ARU accumulator → transfer register** (microword byte 5 bit 4). *Not* a free-running clock — corrects my earlier guess | ✅ (Ch.4 §4.2.4) |
| 30 | MWR | IN | MWR | Memory/transfer-register write control; behavior set jointly with MCEN/ (see §7, Table 4.5) | ✅ (Ch.4) |
| 31 | RST/ | IN | tied to +5V1 | Async reset (active-low); **strapped high = held inactive** | ✅ |
| 32 | VSS | PWR | GND | Ground | ✅ |
| 33 | DAB2 | I/O | bus b4 | Data bus bit 2 | ✅/🟡 |
| 34 | DAB3 | I/O | bus b5 | Data bus bit 3 | ✅/🟡 |
| 35 | DAB4 | I/O | bus b6 | Data bus bit 4 | ✅/🟡 |
| 36 | DAB5 | I/O | bus b7 | Data bus bit 5 | ✅/🟡 |
| 37 | DAB6 | I/O | bus b8 | Data bus bit 6 | ✅/🟡 |
| 38 | DAB7 | I/O | bus b9 | Data bus bit 7 | ✅/🟡 |
| 39 | DAB8 | I/O | bus b10 | Data bus bit 8 | ✅/🟡 |
| 40 | DAB9 | I/O | bus b11 | Data bus bit 9 | ✅/🟡 |

**Power/ground:** VCC = pins 10, 21; VSS = pins 1, 32. (Note 21 = "+5V", 10 = "VCC" on the symbol — same rail.)

---

## 2. Pin groups (functional view)

**Data bus — DAB0..DAB17 (18 bits).** ✅ width matches the "18 BIT" descriptor.
Board mapping: chip DAB*n* → board bus bit *n+2*, i.e. `DAB1<0:19>` bits 2–19 carry DAB0–DAB17;
bus bits 0–1 are driven elsewhere. 🟡 **Likely bidirectional** — the ARU has no separate operand-input
bus, and the DAB net is straddled by `74HCT244` input buffers (U72/U95) *and* `74HCT374` output latches
(U73/U86), the classic time-multiplexed read-operand / write-result arrangement. Confirm direction with the
bench harness before trusting it.

**Function select — F2:F0 (3 bits).** ✅ pins / 🟡 role. 8 possible operations.
Sourced from the **function PROM U77/U112 → latch U76/U111**. Encoding ❓ (see §4).

**Arithmetic modifiers.** AS2/ (pin 12), CIO/ (25), SC/ (24) — extend/condition the operation:
- **AS2/** (board net `C/`) comes from the **timing/sequencer chain (U104)**, not the function PROM →
  it's a phase/arith-mode line, plausibly the extra control that distinguishes single vs double-precision
  multiply steps. 🟡
- **CIO/** = carry in/out control (chained add/subtract, multi-word). 🟡
- **SC/** = shift control — candidate for the ÷4 / ×0.5 coefficient scaling idiom. 🟡

**B-operand control — BCON3, BCON0/.** Select the B source / constant. Only bits 0 and 3 reach the ARU
(bits 1,2 may be internal or unused). 🟡

**A-register — AREG/.** Loads/enables the A operand register. 🟡

**Register-file addressing — RA0,RA1 (read) / WA0,WA1 (write) + MWR (write strobe).**
2-bit read and 2-bit write addresses ⇒ an internal **4-location register/accumulator file**, written when
MWR is asserted. 🟡 (This is the most important structural inference to confirm — it implies 4 accumulators.)

**Clocks — MC (pin 26, master) and XCLK/ (pin 29, aux).** Two-phase clocking; XCLK/ is the strongest
candidate for the 480's extra-multiply T-state vs the PCM60/70. 🟡

**Flags — OVLD/ (pin 22, out).** Saturation/overflow indicator. Critical for matching arithmetic semantics
(tells you exactly *when* the unit clamps). Combined downstream (U42/U52) into the system `OVLD/`. ✅ pin.

**Reset — RST/ (pin 31).** Strapped to +5V → not used dynamically. ✅

---

## 3. Where each control bit comes from (microword → ARU chain)

Traced from sheets 6/7. This tells you which microcode field drives which ARU input.

```
slave-written coefficient/state bits
        │
   C1<0:4> (coef addr) + ST<0:2> (state) + DPOX1/ ──► U77 (74S472 PROM) ──► U76 (374 latch) ──► F0,F1,F2,CIO/,SC/  ──► ARU
   ST<0:2> + DP1/,DPD1/,ACC1,SHORT1/,B/          ──► U62 (74S472 PROM) ──► U61 (374 latch) ──► BCON3,BCON0/,AREG/  ──► ARU
                                                                          (U61 also regenerates ST<0:2> = sequencer state)
   timing/phase chain (U102/U103/U104) ───────────────────────────────────────────────────► C/ (=AS2/), ZCLK, PCCLR ──► ARU/system
   master clock distribution ─────────────────────────────────────────────────────────────► MC, XCLK/
   address generation (slave/sequencer) ──────────────────────────────────────────────────► RA0/1, WA0/1, MWR
```

Key consequence for reversing: the ARU's **function and operand-control fields are PROM-decoded** from the
raw microword (the `74S472` PROMs U62/U77 are the decode tables). So two things must be recovered to define
an "instruction": (a) the raw microword bits the slave writes, and (b) the **U62/U77 PROM contents** that map
them to F/BCON/AREG/CIO/SC. **U62 and U77 are dumpable `74S472` bipolar PROMs (512×8)** — pull and read them on
the T48; that gives you the decode half directly, no guessing. ✅ high-value, low-effort.

---

> **Superseded by §7.** Chapter 4 shows the ARU is a multiply-accumulate engine, not a generic
> 8-opcode ALU. The "function" is parameterized by the coefficient + precision/accumulate/sign
> control bits, with F2:F0 being per-step sequencer ROM outputs. Read §7 first.

## 4. Operation table — structure known, encoding TBD

The schematic fixes the *operand* of an operation but not its *meaning*. Do **not** assume an encoding;
fill this by characterization. Template to populate:

| F2 | F1 | F0 | AS2/ | CIO/ | SC/ | Operation | Notes |
|:--:|:--:|:--:|:--:|:--:|:--:|---|---|
| 0 | 0 | 0 | ? | ? | ? | ❓ | |
| 0 | 0 | 1 | ? | ? | ? | ❓ | |
| … | | | | | | | |
| 1 | 1 | 1 | ? | ? | ? | ❓ | |

Expected op set (from family priors, 🟡): pass/load, add, subtract, multiply, multiply-accumulate,
and the double-precision-multiply-×½ idiom. Map them to codes empirically.

---

## 5. Characterization plan (bench harness)

Using the FPGA-socket approach, with pin directions now known:

1. **Power/clock first.** VCC 10/21, VSS 1/32, hold RST/ (31) high. Drive MC (26); add XCLK/ (29) once
   you see whether ops need it.
2. **Pin-direction check.** Tri-state your drivers on DAB; confirm whether the ARU ever *drives* DAB
   (settles the bidirectional question) and in which clock phase.
3. **Register-file probe.** Write known values via DAB + WA0/1 + MWR, read back via RA0/1 → confirms the
   4-location file and its timing.
4. **Function sweep.** For each F2:F0 (× AS2//CIO//SC/ combinations), feed fixed operand pairs and capture
   DAB + OVLD/. Build the real §4 table.
5. **Arithmetic semantics.** With the multiply/MAC codes identified, sweep operands across sign and
   magnitude extremes to pin rounding (truncate vs round-to-zero), the shift/scale behavior on SC/, and the
   exact OVLD/ saturation threshold.
6. **Shortcut:** dump PROMs **U62 + U77** (74S472) to get the microword→control decode for free, and
   cross-check against an ARU observed running in-system in a PCM60 (simpler, single-core).

---

## 6. Open questions
- ❓ Exact F/AS2/CIO/SC operation encodings (§4).
- ❓ DAB bidirectional? Which phase reads vs writes? (§5 step 2)
- ❓ Internal register-file depth — is RA/WA really 4×, and are read/write files separate or shared? (§5 step 3)
- ❓ Role of XCLK/ vs MC — does multiply consume an XCLK edge? (the 480-vs-PCM60 "extra T-state")
- ❓ BCON full width — only bits 0,3 are pinned out; what do they select?
- ❓ Rounding/saturation rule and OVLD/ threshold (the bits that make a bit-exact model).

---

*Pin map and net tracing are schematic-verified (✅). Functional roles are inferred from naming + topology (🟡).
Operation encodings and arithmetic semantics require the bench harness or an in-system capture (❓). The cheapest
next step that removes guesswork is dumping the U62/U77 decode PROMs.*

---

## 7. Chapter 4 reconciliation (manual-verified)

Service Manual Ch. 4 (§4.2.4 microcode, §4.2.8 arithmetic section) fills in most of the §6 blanks. ✅ = stated in the manual.

### 7.1 The ARU is a coefficient-driven MAC engine — not an 8-opcode ALU ✅
> "The ARU performs an eighteen-by-four-bit multiply and accumulate every instruction cycle. Data is read into
> or gated out of the ARU buffers onto the DAB once an instruction cycle." (§4.2.8)

So one 18×4 MAC happens per cycle. A full multiply by the 8-bit coefficient is built from **4-bit slices**
across multiple cycles ("double-precision" = the normal 2-cycle case; "n-precision" = more slices). The
operation isn't carried as an opcode in the microword — it's a **multiply-accumulate sequence** driven by the
state machine (ST<0:2>) through the U77/U62 ROMs, parameterized by the control bits below. F2:F0 are the
per-step ROM outputs that walk that sequence — which is why they're PROM-decoded, not microword-resident.

### 7.2 Coefficient path ✅ (was ❓)
Microword **byte 2 = C7..C0**, an 8-bit value (0–255) — the multiply coefficient, loadable in one WCS read
("facilitating rapid ramp up/down of coefficients"). The coefficient (as C<0:4> + state) **addresses the
control ROM**, which emits the per-slice ARU control. *Open detail:* byte 2 is 8 bits but only C<0:4> (5 bits)
reaches the ROM address per §4.2.8 — resolve the width split when you dump U77. **SIGN** (byte 3) sets the
coefficient sign on the last cycle.

### 7.3 Register file + accumulator ✅ (confirms the 4-location inference)
- **Register file**, addressed 2 bits → 4 locations. Normal/non-last cycles use read address **{RA00,RA10}**;
  the last cycle of an n-precision multiply uses **{RA01,RA11}**. **CLKEN/** selects which (U79 vs U80).
  Write address = **{WA0,WA1}** (byte 5). These mux down to the ARU's RA0/RA1 (pins 15/14) and WA0/WA1 (13/11).
- Separate **accumulator**. **ACC/** picks the MAC source: `ACC/=0` → register file, `ACC/=1` → accumulator.
- **ENACC/** (last cycle) decides whether to accumulate. **SHORT/** chains this multiply's result as the source
  of the next one (tells the timing ROM). **DP/** marks the last cycle (`DP/=1`).

### 7.4 DAB is bidirectional, and direction is explicit ✅ (was 🟡)
Direction is set by MWR + MCEN/ (microword byte 5). From **Table 4.5**:

| MWR | MCEN/ | Operation |
|:--:|:--:|---|
| 0 | 0 | Audio-memory **read**; ARU transfer-register output **disabled** |
| 0 | 1 | used on I/O reads |
| 1 | 0 | Audio-memory **write**; ARU transfer register **drives DAB** |
| 1 | 1 | I/O writes, and pass the ARU transfer register into the ARU register files |

### 7.5 XCLK/ corrected ✅
**XCLK/ (pin 29) = "transfer the accumulated result in the ARU accumulator to the transfer register."** It's a
microword-controlled strobe, not the "extra multiply T-state" I'd guessed. The transfer register is what then
drives DAB (per Table 4.5). **MC (pin 26)** is the actual master clock — control latches every MC edge.

### 7.6 Overflow ✅
A **pulse on OVLD/** = an overflow occurred inside the ARU; it clocks flop U8 → OVLDB (latching), readable on
DUART. Whether the result **saturates or wraps** on overflow is still ❓.

### 7.7 Microword control bits that drive the ARU (byte 3 & byte 5) ✅
| Bit | Byte | Meaning |
|---|:--:|---|
| RA00, RA10 | 3 | Reg-file read addr — single precision + non-last n-precision cycles |
| RA01, RA11 | 3 | Reg-file read addr — last cycle of n-precision |
| CLKEN/ | 3 | Enables U79/U80 clocking; selects normal (U79) vs last-cycle (U80) read-addr set |
| SHORT/ | 3 | This multiply's result feeds the next n-precision multiply |
| ENACC/ | 3 | Accumulate-or-not on the last cycle |
| SIGN | 3 | Coefficient sign on the last cycle |
| WA0, WA1 | 5 | Reg-file write address |
| ACC/ | 5 | MAC source: 0 = register file, 1 = accumulator |
| DP/ | 5 | 0 = first/non-last cycle; 1 = last cycle |
| XCLK/ | 5 | Accumulator → transfer register |
| OP/ | 5 | I/O instruction (enables WET address/control bus) |
| MCEN/ | 5 | Memory-control enable (with MWR, Table 4.5) |
| MWR | 5 | Memory/transfer-register write (with MCEN/) |

### 7.8 Updated open questions
- ❓ Per-step F2:F0 / SC/ / CIO/ / AS2/ encodings inside one MAC — *resolved by dumping U77 + U62*.
- ❓ Accumulator width and the **rounding/truncation** when it's reduced to the 18-bit transfer register.
- ❓ **Saturate vs wrap** on OVLD/ (the manual flags overflow but doesn't state the result behavior).
- ❓ The byte-2 (8-bit) vs C<0:4> (5-bit) coefficient-width split into the control ROM.
- ❓ AS2/ (net C/) exact role; full BCON semantics.

**Bottom line:** the architecture and control semantics are now manual-verified; what remains is purely the
*numeric* behavior — coefficient→slice encoding (U77/U62 dump) and rounding/saturation (bench or in-system
capture). The generic-ALU framing in §4 is retired.
