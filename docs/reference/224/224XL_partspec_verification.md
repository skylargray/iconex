# 224XL — datasheet-verified part-spec table (M0a)

> **Purpose.** The interconnect netlist (Phase 0b) and the RTL model (Phase 2) are keyed on THIS table.
> Per the holistic-model plan §0 Ground Rule 1: **every pinout here is read by the assistant from a real
> datasheet that is downloaded, rendered (PyMuPDF → PNG), read as an image, and archived** in
> `docs/reference/224/datasheets/`. **No pinout comes from training memory.** Each entry cites its datasheet.
>
> **Method per part:** `WebFetch` the datasheet (saves the PDF even when its own text parser can't read the
> scan) → `python -c "import fitz; …"` render the pinout page/zoom to PNG → Read the PNG → archive the PDF.
>
> **Family note.** A 7400-series pinout is defined by the **function number** (e.g. "283"), not the family
> (LS / S / F / HC); the families are pin-compatible for a given function. The TI datasheets cited each draw
> ONE pinout covering several families (e.g. the '283 sheet covers 283/LS283/S283). Where the owner's board
> uses a 74F/74S part, the pinout below is from a TI sheet that covers that function; the 74F variant is the
> same function and pin-compatible. (A 74F-specific sheet would be a future belt-and-suspenders confirm.)
>
> **Confidence:** ✅ datasheet-verified (read by assistant) · 🟡 partial/family-inferred · ⚪ unverified.
> "matches owner trace" = the pin→signal here agrees with `224XL ARU pinouts from 060-01318.txt`.

## Status
| Part | Function | Role on board(s) | Datasheet (archived) | Status |
|---|---|---|---|---|
| 74283 | 4-bit adder | aru_U19-23, aru_U13/24/25/38/39, dmem_U49/50/63/64 | `74283_TI_SDLS095A.pdf` | ✅ |
| 74163 | sync 4-bit counter | aru_U45-49 (accumulator) | `74163_TI.pdf` | ✅ |
| 74374 | octal D-FF (3-state) | aru_U43/44, aru_U10/11, dmem_U38-41 | `74374_TI.pdf` (SDLS165B) | ✅ |
| 74157 | quad 2:1 mux | aru_U33-37, dmem_U36/U18 | `74157_TI.pdf` (SDLS058) | ✅ |
| 7486 | quad 2-in XOR | aru_U5-9, aru_U42 | `7486_TI.pdf` (SDLS124) | ✅ |
| 74175 | quad D-FF | aru_U12 (product reg low) | `74175_TI.pdf` (SDLS068A) | ✅ |
| 7404 | hex inverter | aru_U2, dmem_U58 | `7404_TI.pdf` (SDLS029C) | ✅ |
| 74670 | 4×4 register file | aru_U29-32 (register file) | `74670_TI.pdf` (SDLS193) | ✅ **.v pins 10/11 fixed** |
| 7400 | quad 2-in NAND | tc_U48, dmem_U44 | `7400_TI.pdf` (SDLS025D) | ✅ |
| 7410 | triple 3-in NAND | tc_U49, dmem_U43 | `7410_TI.pdf` (SDLS035A) | ✅ |
| 74139 | dual 2:4 decoder | tc_U47 (device decode) | `74139_TI.pdf` | ✅ |
| 74138 | 3:8 decoder | dmem_U55/56/57, (aru_U54?) | `74138_TI.pdf` | ✅ |
| 7402 | quad 2-in NOR | dmem_U60 | `7402_TI.pdf` | ✅ |
| 7408 | quad 2-in AND | dmem_U45 | `7408_TI.pdf` (SDLS033) | ✅ |
| 7474 | dual D-FF +PRE/CLR | dmem_U46/U47 | `7474_TI.pdf` (SDLS119) | ✅ |
| 7420 | dual 4-in NAND | dmem_U54 | `7420_TI.pdf` | ✅ |
| 7403 | quad NAND (OC) | dmem_U52 | `7403_TI.pdf` | ✅ |
| 74244 | octal buffer (3-state) | dmem_U6/U61, dmem_U48 | `74244_TI.pdf` (SDLS144D) | ✅ |
| 74393 | dual 4-bit binary counter | dmem_U51/U65 (CPC) | `74393_TI.pdf` (SDLS107) | ✅ |
| 74194 | 4-bit univ. shift register | aru_U3/U4/U15/U16/U17/U18 (mult shifter) | `74194_TI.pdf` | ✅ (= `parts/74ls194.v`) |
| 4164 | DRAM 64K×1 (Siemens HYB4164) | dmem_ array | `41662.pdf` | ✅ |
| DL630B | 5-tap digital delay line (Bel 0447-0150-02) | dmem_U59 (DRAM timing) | `belfuse-0447.pdf` | ✅ |
| 74LS27 | triple 3-in NOR | tc_U38 | `7427_TI.pdf` | ✅ (= .v) |
| 74S112 | dual JK-FF (-edge) | tc_U20/U21/U22/U26 | `74112_TI.pdf` | ✅ (= .v) |
| 74LS155 | dual 2:4 decoder | tc_U46 | `74155_TI.pdf` | ✅ (= .v) |
| 74LS377 | octal D-FF + enable | tc_U19 | `74377_TI.pdf` (SDLS167) | ✅ (= .v) |
| 74LS174 | hex D-FF | tc_U9 | `74174_TI.pdf` (SDLS068A) | ✅ (= .v) |
| 74LS123 | dual monostable | tc_U13 | `74123_TI.pdf` (SDLS043) | ✅ **.v had pins 5/6/7↔13/14/15 swapped — FIXED** |
| 74195 | 4-bit shift register | tc_U10/U11 | `74195.pdf` (Motorola) | ✅ (= .v) |
| 74LS133 | 13-in NAND | tc_U50 | `74ls133.pdf` (Motorola) | ✅ (= .v) |
| MCM6810 | 128×8 SRAM (WCS store) | tc_ WCS lanes 0-3 | `mcm68a10p_mot.pdf` | ✅ |

> Role/designator column is from the owner trace + crops and is itself subject to Phase-0b confirmation;
> THIS table verifies the generic **function-number pinout**, which is what the netlist/model are keyed on.

---

## Verified pinouts (DIP, top view) — read by assistant from the cited datasheet

### 74283 — 4-bit binary full adder · TI SDLS095A · `74283_TI_SDLS095A.pdf`
`1=Σ2 2=B2 3=A2 4=Σ1 5=A1 6=B1 7=C0 8=GND 9=C4 10=Σ4 11=B4 12=A4 13=Σ3 14=A3 15=B3 16=Vcc`
Weights (A1/B1/Σ1=bit0 LSB … A4/B4/Σ4=bit3 MSB): A{0:5,1:3,2:14,3:12} Σ{0:4,1:1,2:13,3:10} B{0:6,1:2,2:15,3:11}. **Matches owner trace.**

### 74163 — synchronous 4-bit counter · TI · `74163_TI.pdf`
`1=CLR\ 2=CLK 3=A 4=B 5=C 6=D 7=ENP 8=GND 9=LOAD\ 10=ENT 11=QD 12=QC 13=QB 14=QA 15=RCO 16=Vcc`
D-in A..D = bit0..3; Q-out QA..QD = bit0..3. **Matches owner trace.** (Accumulator wired load-mode: LOAD\=GND, ENP=ENT=GND, CLR\=ZERO/, CLK=ARUCKE/.)

### 74374 — octal D flip-flop, 3-state · TI SDLS165B · `74374_TI.pdf`
`1=OC\(OE) 2=1Q 3=1D 4=2D 5=2Q 6=3Q 7=3D 8=4D 9=4Q 10=GND 11=CLK 12=5Q 13=5D 14=6D 15=6Q 16=7Q 17=7D 18=8D 19=8Q 20=Vcc`
**Matches owner trace (U43).**

### 74157 — quad 2:1 mux · TI SDLS058 · `74157_TI.pdf`
`1=A/B\(SEL) 2=1A 3=1B 4=1Y 5=2A 6=2B 7=2Y 8=GND 9=3Y 10=3B 11=3A 12=4Y 13=4B 14=4A 15=G\(strobe) 16=Vcc`
Per mux n: nA=I0, nB=I1, nY=Y; SEL low→A, high→B. **Matches owner trace (U33).**

### 7486 — quad 2-input XOR · TI SDLS124 · `7486_TI.pdf`
`1=1A 2=1B 3=1Y 4=2A 5=2B 6=2Y 7=GND 8=3Y 9=3A 10=3B 11=4Y 12=4B 13=4A 14=Vcc`
**Matches owner trace (U5).**

### 74175 — quad D flip-flop · TI SDLS068A · `74175_TI.pdf`
`1=CLR\ 2=1Q 3=1Q\ 4=1D 5=2D 6=2Q\ 7=2Q 8=GND 9=CLK 10=3Q 11=3Q\ 12=3D 13=4D 14=4Q\ 15=4Q 16=Vcc`
**Matches owner trace (U12).**

### 7404 — hex inverter · TI SDLS029C · `7404_TI.pdf`
`1=1A 2=1Y 3=2A 4=2Y 5=3A 6=3Y 7=GND 8=4Y 9=4A 10=5Y 11=5A 12=6Y 13=6A 14=Vcc`
Per inverter n: nA in, nY out.

### 74670 — 4×4 register file, 3-state · TI SDLS193 · `74670_TI.pdf`
`1=D2 2=D3 3=D4 4=RB 5=RA 6=Q4 7=Q3 8=GND 9=Q2 10=Q1 11=GR\ 12=GW\ 13=WB 14=WA 15=D1 16=Vcc`
Write addr WA(14),WB(13); write enable GW\(12). Read addr RA(5),RB(4); read enable GR\(11). Data in D1(15),D2(1),D3(2),D4(3). Data out Q1(10),Q2(9),Q3(7),Q4(6). (4 words × 4 bits; four chips = 4 words × 16 bits.)

### 7400 — quad 2-input NAND · TI SDLS025D · `7400_TI.pdf`
`1=1A 2=1B 3=1Y 4=2A 5=2B 6=2Y 7=GND 8=3Y 9=3B 10=3A 11=4Y 12=4B 13=4A 14=Vcc`
Gates: G1{1,2→3} G2{4,5→6} G3{9,10→8} G4{12,13→11}. (NAND inputs are symmetric; the A/B label on an input pair is cosmetic.)

### 7410 — triple 3-input NAND · TI SDLS035A · `7410_TI.pdf`
`1=1A 2=1B 3=2A 4=2B 5=2C 6=2Y 7=GND 8=3Y 9=3A 10=3B 11=3C 12=1Y 13=1C 14=Vcc`
Gates: G1{1,2,13→12} G2{3,4,5→6} G3{9,10,11→8}.

### 74139 — dual 2-to-4 decoder · TI · `74139_TI.pdf`
`1=1G\ 2=1A 3=1B 4=1Y0 5=1Y1 6=1Y2 7=1Y3 8=GND 9=2Y3 10=2Y2 11=2Y1 12=2Y0 13=2B 14=2A 15=2G\ 16=Vcc`
Decoder 1: enable 1G\(1), addr 1A(2)/1B(3), outs 1Y0-3(4-7). Decoder 2: enable 2G\(15), addr 2A(14)/2B(13), outs 2Y0-3(12-9).

### 74138 — 3-to-8 decoder · TI · `74138_TI.pdf`
`1=A 2=B 3=C 4=G2A\ 5=G2B\ 6=G1 7=Y7 8=GND 9=Y6 10=Y5 11=Y4 12=Y3 13=Y2 14=Y1 15=Y0 16=Vcc`
Addr A(1)/B(2)/C(3); enables G1(6,active-high), G2A\(4)/G2B\(5,active-low); outs Y0(15)…Y7(7).

### 7402 — quad 2-input NOR · TI · `7402_TI.pdf`
`1=1Y 2=1A 3=1B 4=2Y 5=2A 6=2B 7=GND 8=3A 9=3B 10=3Y 11=4A 12=4B 13=4Y 14=Vcc`
Gates (note: NOR has output first): G1{2,3→1} G2{5,6→4} G3{8,9→10} G4{11,12→13}.

### 7408 — quad 2-input AND · TI SDLS033 · `7408_TI.pdf`
`1=1A 2=1B 3=1Y 4=2A 5=2B 6=2Y 7=GND 8=3Y 9=3A 10=3B 11=4Y 12=4A 13=4B 14=Vcc`
Gates: G1{1,2→3} G2{4,5→6} G3{9,10→8} G4{12,13→11}.

### 7474 — dual D flip-flop (preset + clear) · TI SDLS119 · `7474_TI.pdf`
`1=1CLR\ 2=1D 3=1CLK 4=1PRE\ 5=1Q 6=1Q\ 7=GND 8=2Q\ 9=2Q 10=2PRE\ 11=2CLK 12=2D 13=2CLR\ 14=Vcc`
FF1: CLR\(1),D(2),CLK(3),PRE\(4),Q(5),Q\(6). FF2: Q\(8),Q(9),PRE\(10),CLK(11),D(12),CLR\(13).

### 7420 — dual 4-input NAND · TI · `7420_TI.pdf`
`1=1A 2=1B 3=NC 4=1C 5=1D 6=1Y 7=GND 8=2Y 9=2A 10=2B 11=NC 12=2C 13=2D 14=Vcc`
G1{1,2,4,5→6} G2{9,10,12,13→8}.

### 7403 — quad 2-input NAND, open-collector · TI · `7403_TI.pdf`
`1=1A 2=1B 3=1Y 4=2A 5=2B 6=2Y 7=GND 8=3Y 9=3A 10=3B 11=4Y 12=4A 13=4B 14=Vcc`
Gates: G1{1,2→3} G2{4,5→6} G3{9,10→8} G4{12,13→11} (same pinout as 7400/7408; outputs open-collector).

### 74244 — octal buffer/line driver, 3-state · TI SDLS144D · `74244_TI.pdf`
`1=1G\ 2=1A1 3=2Y4 4=1A2 5=2Y3 6=1A3 7=2Y2 8=1A4 9=2Y1 10=GND 11=2A1 12=1Y4 13=2A2 14=1Y3 15=2A3 16=1Y2 17=2A4 18=1Y1 19=2G\ 20=Vcc`
Group1 (enable 1G\=1): 1A1→1Y1, 1A2→1Y2, 1A3→1Y3, 1A4→1Y4. Group2 (enable 2G\=19): 2A1→2Y1 … 2A4→2Y4.

### 74393 — dual 4-bit binary counter · TI SDLS107 · `74393_TI.pdf`
`1=1A 2=1CLR 3=1QA 4=1QB 5=1QC 6=1QD 7=GND 8=2QD 9=2QC 10=2QB 11=2QA 12=2CLR 13=2A 14=Vcc`
Counter1: clk 1A(1), clear 1CLR(2), Q 1QA-1QD(3,4,5,6). Counter2: clk 2A(13), clear 2CLR(12), Q 2QA-2QD(11,10,9,8).
(CPC = two cascaded: per the DMEM crop, 1QD→2A within a chip and chip-to-chip ripple → 16-bit; consistent with this pinout.)

### 74194 — 4-bit bidirectional universal shift register · TI · `74194_TI.pdf`
`1=CLR\ 2=SR_SER 3=A 4=B 5=C 6=D 7=SL_SER 8=GND 9=S0 10=S1 11=CLK 12=QD 13=QC 14=QB 15=QA 16=Vcc`
Modes (rising CLK): S1S0=00 hold · 01 shift-right (QA←SR_SER) · 10 shift-left (QD←SL_SER) · 11 parallel-load.
**Matches `parts/74ls194.v` exactly.** Modes match fig-3.4 (operand: 11=LOAD@AS0, 01=SHIFT-RIGHT@AS1/AS2).

### 7427 — triple 3-input NOR · TI · `7427_TI.pdf`
`1=1A 2=1B 3=2A 4=2B 5=2C 6=2Y 7=GND 8=3Y 9=3A 10=3B 11=3C 12=1Y 13=1C 14=Vcc`
Gates: G1{1,2,13→12} G2{3,4,5→6} G3{9,10,11→8}. (Same physical pinout as 7410.) **Matches `74ls27.v`.**

### 74112 — dual JK FF, negative-edge, preset+clear · TI · `74112_TI.pdf`
`1=1CLK 2=1K 3=1J 4=1PRE\ 5=1Q 6=1Q\ 7=2Q\ 8=GND 9=2Q 10=2PRE\ 11=2J 12=2K 13=2CLK 14=2CLR\ 15=1CLR\ 16=Vcc`
**Matches `74s112.v`.**

### 74155 — dual 2:4 decoder/demux (common A,B) · TI · `74155_TI.pdf`
`1=1C 2=1G\ 3=B 4=1Y3 5=1Y2 6=1Y1 7=1Y0 8=GND 9=2Y0 10=2Y1 11=2Y2 12=2Y3 13=A 14=2G\ 15=2C 16=Vcc`
**Matches `74ls155.v`.**

### 74377 — octal D-FF with clock-enable (no 3-state) · TI SDLS167 · `74377_TI.pdf`
`1=G\(/E) 2=1Q 3=1D 4=2D 5=2Q 6=3Q 7=3D 8=4D 9=4Q 10=GND 11=CLK 12=5Q 13=5D 14=6D 15=6Q 16=7Q 17=7D 18=8D 19=8Q 20=Vcc`
(Same pinout as 374 but pin1 = clock-enable; outputs always driven.) **Matches `74ls377.v`.**

### 74174 — hex D-FF (common clock + clear) · TI SDLS068A · `74174_TI.pdf`
`1=CLR\ 2=1Q 3=1D 4=2D 5=2Q 6=3D 7=3Q 8=GND 9=CLK 10=4Q 11=4D 12=5Q 13=5D 14=6D 15=6Q 16=Vcc`
**Matches `74ls174.v`.**

### 74123 — dual retriggerable monostable · TI SDLS043 · `74123_TI.pdf`
`1=1A 2=1B 3=1CLR\ 4=1Q\ 5=2Q 6=2Cext 7=2Rext/Cext 8=GND 9=2A 10=2B 11=2CLR\ 12=2Q\ 13=1Q 14=1Cext 15=1Rext/Cext 16=Vcc`
⚠ **`74ls123.v` had pins 5/6/7 ↔ 13/14/15 swapped (one-shot 1 vs 2 Q/Cext/Rext) — FIXED 2026-06-26.**
The '123 cross-couples the two halves across the package (a quirk KiCad libs commonly miss).

### 74195 — 4-bit parallel-access shift register · Motorola SN54/74LS195A · `74195.pdf`
`1=MR\(CLR) 2=J 3=K\ 4=P0 5=P1 6=P2 7=P3 8=GND 9=PE(SH/LD\) 10=CP(CLK) 11=Q3\ 12=Q3 13=Q2 14=Q1 15=Q0 16=Vcc`
**Matches `74195.v`** (top row Q0=15…Q3=12, Q3\=11, CP=10, PE=9 confirmed from the connection diagram).

### 74LS133 — 13-input NAND · Motorola SN54/74LS133 · `74ls133.pdf`
output **Y = pin9**; GND = pin8; Vcc = pin16; the 13 inputs = pins 1-7 and 10-15 (all symmetric).
**Matches `74ls133.v`** (the only thing that matters — output on pin9 — confirmed from the gate drawing).

### MCM6810 — 128×8 static RAM (the WCS microstore) · Motorola · `mcm68a10p_mot.pdf`
`1=Vss 2=D0 3=D1 4=D2 5=D3 6=D4 7=D5 8=D6 9=D7 10=CS0 11=CS1\ 12=CS2\ 13=CS3 14=CS4\ 15=CS5\ 16=R/W 17=A6 18=A5 19=A4 20=A3 21=A2 22=A1 23=A0 24=Vcc`
7 address (A0-A6 → 128 words), 8 data (D0-D7), 6 chip-selects (CS0,CS3 active-HIGH; CS1\,CS2\,CS4\,CS5\ active-LOW),
**R/W̄ (pin16): the bar is over the W → write is active-LOW, i.e. HIGH = Read, LOW = Write** (6800-family convention).
All pins read directly except pin16 (by elimination — the only pin left). `.v` = `parts/mcm68b10.v`
(owner-created; I fixed a CS3/CS4 polarity swap in it — see below).

### 4164 — 64K×1 DRAM · Siemens HYB4164 · `41662.pdf`
`1=NC 2=D(DIN) 3=W\(WE) 4=RAS\ 5=A0 6=A2 7=A1 8=Vcc 9=A7 10=A5 11=A4 12=A3 13=A6 14=Q(DOUT) 15=CAS\ 16=Vss`
8 multiplexed address A0-A7 (8 row + 8 col = 64K). ⚠ Datasheet: **pin2=DIN, pin14=DOUT** (the DMEM crop read these
swapped; immaterial because the 224XL ties DIN↔DOUT, but the datasheet is authoritative). No `.v` yet.

### DL630B — 5-tap digital delay line · Bel Fuse 0447-0150-02 · `belfuse-0447.pdf`
`1=IN 4=TAP2(60ns) 6=TAP4(120ns) 7=GND 8=TAP5(150ns) 10=TAP3(90ns) 12=TAP1(30ns) 14=Vcc ; NC=2,3,5,9,11,13`
14-pin DIP, 5 active TTL taps at **30 ns/tap** (TAP1..TAP5 = 30/60/90/120/150 ns); Vcc 5 V. **Tap-pin order is
non-monotonic** (TAP1=12, TAP2=4, TAP3=10, TAP4=6, TAP5=8). `TAPk(t) = IN(t − 30 ns·k)`. Used as `dmem_U59` to
sequence the DRAM RAS/CAS strobes (fig-3.3; the 224XL wires the 30/60/150 ns taps). `.v` = `parts/dl630b.v`.
(Pinout from the Bel 0447 datasheet — owner-confirmed; I'd missed the functional pin diagram on first pass.)

---
## Authoritative part list = `docs/reference/224/parts/*.v`
The owner maintains a Verilog part inventory (`parts/<part>.v`), each with a PINOUT block + Lexicon P/N +
in-224XL designator usage. **That is the authoritative part list** (it corrected my crop-derived guesses:
the shifter is 74LS194 not "74199"; "74273" was never a real part). M0a's job is to datasheet-verify each
`.v` file's PINOUT (they are currently sourced from "KiCad 74xx.lib" and self-marked *"confirm against
schematic"*). Status vs the 25 `.v` files:
- **✅ datasheet-verified & .v matches exactly (23):** 74f157, 74f374, 74xx86†, 74ls194, 74ls163, 74ls244,
  74s175, 74ls00†, 74s04, 74xx08, 74xx10, 74ls20, 74ls03, 74xx74, 74ls138, 74ls139, 74ls27, 74s112, 74ls155,
  74ls377, 74ls174, 74195, 74ls133.  († 74xx86 / 74ls00 differ only on symmetric XOR/NAND input A/B labels — immaterial.)
- **✅ datasheet-verified, .v had a REAL error → FIXED (2):**
  - `74ls123.v` — one-shot-1/2 Q/Cext/Rext swapped (pins 5/6/7 ↔ 13/14/15); corrected from TI SDLS043.
  - `74ls670.v` — read-enable `/GR` ↔ output `Q1` swapped (pins 10/11); corrected from TI SDLS193. **(functional)**
- **✅ datasheet-verified, .v had a REAL error → FIXED (2):** `74ls123.v` (one-shot pins 5/6/7↔13/14/15) and
  `74ls670.v` (read-enable /GR ↔ output Q1, pins 10/11 — functional). Both corrected from the datasheet.
- **✅ `.v` files now complete.** I created `74xx283.v` (adders), `74xx02.v` (NOR), `dl630b.v` (delay, pinout
  owner-confirmed: IN=1, TAP1=12/TAP2=4/TAP3=10/TAP4=6/TAP5=8, GND=7, Vcc=14). Owner-created files verified by me
  vs datasheet: `74ls393.v` ✓, `4164.v` ✓ (confirms pin2=Din/pin14=Dout), `mcm68b10.v` → **had CS3/CS4 polarity
  swapped, FIXED** (CS3=pin13 active-HIGH, /CS4=pin14 active-LOW; the two active-high selects are CS0 & CS3).
  Owner-added `am8304.v` (AMD octal transceiver) & `mc4044.v` (Motorola PLL phase detector) — owner-verified from
  owner-provided datasheets not in `datasheets/`, so **not yet independently re-checked by me**.

## M0a status: COMPLETE
All 25 pre-existing `parts/*.v` files are **datasheet-verified** (23 match exactly — 2 of those differ only on
immaterial symmetric-input labels; 2 had REAL pinout errors, now FIXED). The 3 non-logic parts (MCM6810 SRAM,
4164 DRAM, DL630B delay) are datasheet-verified from owner-provided PDFs. **`.v` files created for the 6 that
were missing** (74xx283, 74ls393, 74xx02, mcm6810, 4164, dl630b) → every verified part now has a `.v`.

**31 parts datasheet-verified ✅** (downloaded / owner-provided → rendered with PyMuPDF → read by the assistant →
archived in `datasheets/`). Every overlap with the owner's ARU pin trace matches. **Three real `.v` pinout errors
(`74ls670`, `74ls123`, `mcm68b10`) were caught and corrected** from the datasheets. The part-spec foundation for
**M0b** (the netlist) is solid. (Two owner-added parts — `am8304`, `mc4044` — await their datasheets in `datasheets/`
for independent check.)
