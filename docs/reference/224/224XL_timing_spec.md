# 224XL — timing spec (figs 3.2–3.6), MS/AS/step-grid form

> **GENERATED from `tools/timing/timing_spec.json` by `tools/timing/render_timing.py` — do not hand-edit.**
> Edit the JSON and re-run the renderer (it also emits round-trip waveform PNGs to lay beside the
> original Service-Manual figures). Everything is quantized to each figure's discrete grid
> (MS-state / AS-state / sample-step); nanosecond values are annotations only.

**Cell tokens:** `0`/`1` level · `⎍` clock pulse · `·` invalid/unspecified · `Z` hi-Z · a label = start of a valid/data box, `→` = box continues. **Conf:** signal name suffix `~`=medium, `??`=low (else high).

**value_source** distinguishes *fixed-cadence* signals (pure timing — fully specified here) from *microword-decoded* signals (timing here, but their VALUE each step comes from the decode map — NOT derivable from a timing diagram).


## fig32 — T&C module timing (clock skeleton)
*Source figure:* `fig-3.2-t-and-c-module-timing.png` · *round-trip render:* `fig32.png`

> One microinstruction = 292.97 ns = MS0..MS8 (32.55 ns each). IMPORTANT: the top *bracket* AS0=MS0-2/AS1=MS3-5/AS2=MS6-8 labels the conceptual ARU-state THIRDS (= fig-3.4 'ARU STATE'); the AS0/AS1/AS2 *signal* rows below are the actual flip-flop strobes, which are CLOCKED BY MS EDGES and therefore sit ~1 MS LATER than their thirds (AS1 is also deliberately narrowed). The true state boundaries are delimited by ARU CK (rises ~MS0.3/3.3/6.3). Per §3.5: MC=30.72 MHz, PLL ×15 from the 2.048 MHz 02/ SBC clock (MC4044 U27 + ÷2 JK U26; tank 61.44 MHz); state gen = ÷9 counter U56 + 8-bit shift register U39 (MS0-MS8); AS grouping by U38/U25/U23. Edge positions below verified by pixel-measuring fig-3.2 against an MC-calibrated MS grid (90 px/MS). Sub-MS rise/fall = clk-to-Q lag (the <17/<19/<30 ns annotations); the HIGH cells are integer-MS.

| signal | MS0 | MS1 | MS2 | MS3 | MS4 | MS5 | MS6 | MS7 | MS8 |
|---|---|---|---|---|---|---|---|---|---|
| MC | ⎍ | ⎍ | ⎍ | ⎍ | ⎍ | ⎍ | ⎍ | ⎍ | ⎍ |
| O2 ?? | 0 | 0 | 0 | 0 | 1 | 1 | 1 | 1 | 1 |
| MS0 | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MS1 | 0 | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MS2 | 0 | 0 | 1 | 0 | 0 | 0 | 0 | 0 | 0 |
| MS3 | 0 | 0 | 0 | 1 | 0 | 0 | 0 | 0 | 0 |
| MS4 | 0 | 0 | 0 | 0 | 1 | 0 | 0 | 0 | 0 |
| MS5 | 0 | 0 | 0 | 0 | 0 | 1 | 0 | 0 | 0 |
| MS6 | 0 | 0 | 0 | 0 | 0 | 0 | 1 | 0 | 0 |
| MS7 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 1 | 0 |
| MS8 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 1 |
| ARU CK | 1 | 0 | 0 | 1 | 0 | 0 | 1 | 0 | 0 |
| AS0 | 0 | 1 | 1 | 1 | 0 | 0 | 0 | 0 | 0 |
| AS1 | 0 | 0 | 0 | 0 | 0 | 1 | 1 | 0 | 0 |
| AS2 | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 1 | 1 |

**Signal catalog:**

| signal | module | kind | value_source | conf | note |
|---|---|---|---|---|---|
| MC | T&C | clock | PLL master clock 30.72 MHz | high | MC=30.72 MHz, period 32.55 ns = exactly one MS, so 1 pulse per MS (§3.5) |
| O2 | SBC (ref into T&C PLL) | clock | 02/ = SBC system clock 2.048 MHz (488 ns); PLL phase reference, NOT from the MS counter | low | CORRECTED per §3.5/§3.8 (was mislabeled 'phase-2 of MC'). 02/ is ASYNC to the MS grid: 488 ns = 15 MS vs the 9-MS micro cycle, so its phase vs MS0 advances each cycle (realigns every 5 micros). The wave is ONE snapshot from fig-3.2: 02/ is LOW across MS0-MS3 and rises to HIGH at ~MS4 (held MS4-MS8). Because 02/ is async, that edge position drifts cycle-to-cycle; this is just the depicted phase, not a fixed MS relationship. |
| MS0 | T&C | state | MS counter (one-hot) | high | rises <17 ns into the cycle |
| MS1 | T&C | state | MS counter (one-hot) | high |  |
| MS2 | T&C | state | MS counter (one-hot) | high |  |
| MS3 | T&C | state | MS counter (one-hot) | high |  |
| MS4 | T&C | state | MS counter (one-hot) | high | clears AS0 (see AS1 note) |
| MS5 | T&C | state | MS counter (one-hot) | high |  |
| MS6 | T&C | state | MS counter (one-hot) | high |  |
| MS7 | T&C | state | MS counter (one-hot) | high | DAB WSTB (regfile write) is at MS7 |
| MS8 | T&C | state | MS counter (one-hot) | high |  |
| ARU CK | T&C | clock | 1 per AS-state | high | pulse at each AS start; measured HIGH MS0.3-1.3 / MS3.3-4.3 / MS6.3-7.3 (rise lag ~0.3 MS, <19 ns; pulse spans into the next MS). The rising edges delimit the true ARU-state boundaries. |
| AS0 | T&C | state | flip-flop set@MS1, clear@MS4 | high | MEASURED signal (not the 'AS0=MS0-2' third): HIGH MS1-MS3. = the AS0 third shifted ~1 MS later by the clocked logic. Cleared by MS4 (rise lag <30 ns). |
| AS1 | T&C | state | flip-flop set@MS5, clear@MS7 | high | MEASURED signal: a NARROW pulse HIGH MS5-MS6 only (note: 'AS1 shorter than AS0/AS2 to avoid MS4 clearing AS0 prematurely'). Held off until MS5 so AS0's MS4-clear completes first. |
| AS2 | T&C | state | flip-flop set@MS7, clear@MS1(next) | high | MEASURED signal: HIGH MS7-MS8 and WRAPS the cycle boundary (cleared at MS1 of the next cycle), so MS0 shows the tail of the previous AS2. = the AS2 third shifted ~1 MS later. >46 ns after AS1. |

## fig34 — ARU module timing (MAC pipeline, deferred overlap)
*Source figure:* `fig-3.4-ARU-module-timing.png` · *round-trip render:* `fig34.png`

> ARU MAC pipeline across THREE microinstructions (i1,i2,i3); each AS = 3 MS = 97.66 ns. Owner-corrected placement 2026-06-27: operand read RA1/RA0 spans i1.AS1->i2.AS0; LOAD@i1.AS2 then SHIFT-right @i2.AS0 & i2.AS1; the operand weights (SHIFT REG), Booth coeff (M1,M0) and partial products all sit in i2.AS0-AS2; CSIGN valid i2.AS1->i3.AS0; the accumulate (0->±PP1->±(PP1+PP2)) runs i2.AS1->i3.AS0 (one AS behind the partial products = the pipeline register); ZERO/ and XFER CK pulse low at i2.AS0 (ZERO/ clears the accumulator so it reads 0 at i2.AS1; XFER CK lags ZERO/ ~20 ns). Shows the actions of one microinstruction's bits (pipelined/overlapped with neighbours).

| signal | i1.AS0 | i1.AS1 | i1.AS2 | i2.AS0 | i2.AS1 | i2.AS2 | i3.AS0 | i3.AS1 |
|---|---|---|---|---|---|---|---|---|
| ARU CK | ⎍ | ⎍ | ⎍ | ⎍ | ⎍ | ⎍ | ⎍ | ⎍ |
| RA1,RA0 | · | RA1,RA0 VALID | → | → | · | · | · | · |
| S1,S0 | · | · | 11 LOAD | 01 SHIFT-R | 01 SHIFT-R | · | · | · |
| SHIFT REGISTER | · | · | · | F·2⁰ | F·2⁻² | F·2⁻⁴ | · | · |
| M1 | · | · | · | C5 | C3 | C1 | · | · |
| M0 | · | · | · | C4 | C2 | C0 | · | · |
| PARTIAL PRODUCT REG ~ | · | · | · | · | PP0/ | PP1/ | PP2/ | · |
| CSIGN | · | · | · | · | VALID (sign) | → | → | · |
| ACCUMULATOR | · | · | · | · | 0 | ±PP1 | ±(PP1+PP2) | · |
| ZERO/ | 1 | 1 | 1 | 0 | 1 | 1 | 1 | 1 |
| XFER CK | 1 | 1 | 1 | 0 | 1 | 1 | 1 | 1 |

**Signal catalog:**

| signal | module | kind | value_source | conf | note |
|---|---|---|---|---|---|
| ARU CK | T&C | clock | 1 per AS | high | one pulse per AS state |
| RA1,RA0 | WCS->regfile | control | microword read-addr bits | high | regfile read address valid i1.AS1 -> i2.AS0 (owner-read) |
| S1,S0 | T&C (fixed schedule) | control | fixed per-AS schedule | high | 74194 mode: LOAD@i1.AS2, SHIFT-right@i2.AS0 & i2.AS1 (owner-read) |
| SHIFT REGISTER | ARU | data | operand F shifted | high | operand weight per AS, i2.AS0-AS2 (owner-corrected: shifted right to start at i2.AS0) |
| M1 | T&C U10 -> ARU Booth | control | coeff C0/-C5/ serialized (odd) by U10 | high | odd Booth stream, i2.AS0-AS2. Chip = U10 (per T&C trace 060-02475 sh.2: U10 P0/P1/P2=C1//C3//C5/, /Q3=M1/). |
| M0 | T&C U11 -> ARU Booth | control | coeff C0/-C5/ serialized (even) by U11 | high | even Booth stream, i2.AS0-AS2. Chip = U11 (per T&C trace 060-02475 sh.2: U11 P0/P1/P2=C0//C2//C4/, /Q3=M0/). |
| PARTIAL PRODUCT REG | ARU | data | Booth partial products | med | i2.AS0-AS2 (NOT explicitly owner-stated; kept one AS ahead of the accumulate = the pipeline register. CONFIRM) |
| CSIGN | WCS | control | microword sign bit | high | valid i2.AS1 -> i3.AS0 (owner-read) |
| ACCUMULATOR | ARU | data | running sum | high | accumulate i2.AS1 -> i3.AS0 (owner-corrected: shifted right one cell). ZERO/ clears it at i2.AS0 so it reads 0 at i2.AS1 |
| ZERO/ | WCS->ARU | strobe | microword ZERO bit | high | active-LOW: low pulse at i2.AS0 (clears accumulator), high again at i2.AS1 (owner-read) |
| XFER CK | WCS->ARU | strobe | microword XFER bit | high | active-LOW: same low pulse at i2.AS0 as ZERO/ but ~20 ns lag behind it (owner-read). Latches ACC -> result register |

## fig33 — DMEM timing (DRAM access strobes)
*Source figure:* `fig-3.3-DMEM-timing.png` · *round-trip render:* `fig33.png`

> DMEM DRAM access within one microinstruction (MS grid). GRID PIXEL-CALIBRATED 2026-06-27: MS0 starts x=430, 81.1 px/MS, anchored to the printed MS-digit centers (MSO center=468). ALL signals owner-confirmed on this grid 2026-06-27 - the strobes (RAS//CAS//DAB WSTB//MEMW//DAB RSTB/RESET/), ROW SEL, and the OFST//ADDRESS/DOUT/DIN/CPC valid-windows (auto-extraction had been unreliable - annotation arrows cross the thin strobe traces - so they were read off by the owner). Per §3.6: DMEM strobes generated by delay-line U59 (DL630B) from T&C signals MEMAC, DABSTB, MEMR. Address = CPC - OFST (2's-complement: CPC + complemented OFST/ + carry-in tied HIGH; adder U49/U50/U63/U64), row/col-muxed onto the 8 DRAM address lines by U18/U36. CPC = 16-bit counter U51/U65, +1 per sample. RAM outputs drive the DAB directly (no buffer). Notes: 'CAS/ falls only when MEMAC is high.' 'Critical path for DIN is XFER CK -> ARU result register.'

| signal | MS0 | MS1 | MS2 | MS3 | MS4 | MS5 | MS6 | MS7 | MS8 |
|---|---|---|---|---|---|---|---|---|---|
| OFST/ VALID | · | OFST VALID | → | → | → | → | → | → | → |
| ADDRESS VALID | · | · | ADDR VALID | → | → | → | → | → | → |
| RAS/ | 1 | 1 | 0 | 0 | 0 | 0 | 0 | 1 | 1 |
| ROW SEL | 1 | 1 | 1 | 0 | 0 | 0 | 0 | 0 | 1 |
| CAS/ | 1 | 1 | 1 | 1 | 0 | 0 | 0 | 0 | 0 |
| DOUT VALID | · | · | · | · | · | · | · | DOUT | → |
| DAB WSTB/ | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 0 | 1 |
| MEMW/ | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| DAB RSTB | 0 | 0 | 1 | 1 | 1 | 1 | 1 | 1 | 1 |
| DIN VALID | · | · | · | · | DIN | → | → | → | → |
| RESET/ | 1 | 1 | 1 | 1 | 1 | 0 | 0 | 0 | 0 |
| CPC VALID (0-7) | CPC VALID | → | · | · | · | · | CPC VALID | → | → |

**Signal catalog:**

| signal | module | kind | value_source | conf | note |
|---|---|---|---|---|---|
| OFST/ VALID | WCS->DMEM | bus-valid | 16-bit OFST0/-15/ bus (microword offset, complemented) | high | BUS valid-window (multi-bit, NO logic level). Held microinstruction-register value -> valid the whole cycle; only changes (reloads) at the MS0 boundary (<29ns settle). SAME shape every cycle; values differ. Used (latched by RAS/CAS) only when MEMAC. Lines feed adder B-inputs U49/U50/U63/U64 + read-back U48/U62. |
| ADDRESS VALID | DMEM | bus-valid | computed address bus = CPC - OFST | high | BUS valid-window (multi-bit). = CPC-OFST, recomputed each cycle; valid ~MS2-MS8 after the <67ns settle at the boundary. SAME shape every cycle. Latched into the DRAMs by RAS/CAS only when MEMAC. = adder sums U49/U50/U63/U64 -> row/col mux U18/U36 -> 8 DRAM addr lines. |
| RAS/ | DMEM (DL630B seq) | strobe | timing | high | active-LOW; row-address strobe; <44 ns |
| ROW SEL | DMEM | control | timing (U59) | high | OWNER-CONFIRMED on calibrated grid: HIGH (row addr) MS0-2, LOW (column addr) MS3-7, HIGH MS8 -> mux U18/U36 selects row then column for the DRAMs |
| CAS/ | DMEM (DL630B seq) | strobe | timing AND MEMAC | high | OWNER-CONFIRMED: active-LOW col-address strobe; HIGH MS0-3, falls@MS4, LOW MS4-8, rises@MS0 of next cycle (wraps). FALLS ONLY WHEN MEMAC HIGH |
| DOUT VALID | DMEM (DRAM read) | bus-valid | DRAM read data on the DAB | high | BUS valid-window (multi-bit). Occurs ONLY on a READ cycle; DRAM read data is valid LATE (~MS7+, <85ns) after the access. = 4164 DOUT pins tied directly to the DAB. Model: valid at the DAB read strobe. |
| DAB WSTB/ | DMEM | strobe | timing | high | READ: active-LOW; strobes read data onto DAB; <22 ns |
| MEMW/ | DMEM | strobe | timing AND write | high | WRITE: memory write enable; <83 ns. (Net is MEMW/ per the DMEM netlist 060-02512 U61 pin 11 -> DRAM WR/; the fig-3.3 'MFMW/' label was a transcription typo, owner-corrected.) |
| DAB RSTB | DMEM | strobe | timing | high | WRITE: latches DIN from DAB; <12 ns |
| DIN VALID | ARU result reg -> DAB | bus-valid | DRAM write data on the DAB (from ARU result reg) | high | BUS valid-window (multi-bit). Occurs ONLY on a WRITE cycle. = 4164 DIN pins <- DAB, from the ARU result register (critical path = XFER CK -> result reg). Valid MS4-MS8 (owner-read); model only needs it valid at the write strobe. |
| RESET/ | T&C | strobe | timing | high | active-LOW; <21 ns, <35.5 ns |
| CPC VALID (0-7) | DMEM (CPC counter) | bus-valid | CPC counter | high | BUS valid-window (multi-bit; 16-bit counter U51/U65, row shows bits 0-7). Owner-read: VALID MS6 -> MS1 of the NEXT cycle (wraps), INVALID MS2-MS5. That 5-MS window = the <160.5 ns annotation. So MS0,MS1 = tail of the previous window; MS6,MS7,MS8 = new window. |

## fig35 — FPC float->fixed (A/D input) cycle
*Source figure:* `fig-3.5-floating-to-fixed-ad-cycle-timing.png` · *round-trip render:* `fig35.png`

> X-axis = INPUT CYCLE COUNTER 0-99 (one audio sample = 100 microinstructions × 293 ns; sample time 29.3 us). Per §3.8: ROM-generated by the 8-bit input-cycle counter U7/U8 -> 256x4 ROM U6 (only the first 100 locations used); some ROM outputs deglitched by register U18. Columns are decades; TRANSITIONS APPROXIMATE (snapped to ~10). Two channels convert on alternate halves (CONVERT CH2 ~0-38, CONVERT CH1 ~52-88). SELF-TEST (FPC DBUG floats high when T&C/ARU/DMEM pulled): muxes U4/U42 swap FPC CK->02/ and substitute RESET//RDAD//WRDA//SDAA-D from counter-decode NANDs U5. Notes: absent a RESET pulse all signals repeat beyond count 99; CH1L is generated on the AIN module, not FPC.

| signal | 0 | 10 | 20 | 30 | 40 | 50 | 60 | 70 | 80 | 90 |
|---|---|---|---|---|---|---|---|---|---|---|
| FPCCK | ⎍ | ⎍ | ⎍ | ⎍ | ⎍ | ⎍ | ⎍ | ⎍ | ⎍ | ⎍ |
| RESET/ ~ | 0 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 |
| STBGN ?? | 1 | 1 | 1 | 1 | 0 | 0 | 1 | 1 | 1 | 1 |
| STCONV/ ?? | 1 | 1 | 1 | 1 | 0 | 0 | 1 | 1 | 1 | 0 |
| CNV CK ?? | ⎍ | ⎍ | ⎍ | ⎍ | 0 | 0 | ⎍ | ⎍ | ⎍ | ⎍ |
| LOAD ?? | 0 | 0 | 0 | 0 | ⎍ | 0 | 0 | 0 | ⎍ | 0 |
| CH 1 ?? | 1 | 1 | 1 | 1 | 1 | 0 | 0 | 0 | 0 | 0 |
| CH1L ?? | 0 | 0 | 0 | 0 | 1 | 1 | 1 | 1 | 1 | 0 |
| DATA VALID ?? | · | CH1 | → | → | · | · | CH2 | → | → | · |
| RDAD/ & WR DA/ ?? | 0 | 0 | 0 | ⎍ | 0 | 0 | ⎍ | 0 | 0 | 0 |
| BIT5 of counter ~ | 0 | 0 | 0 | 1 | 1 | 1 | 1 | 0 | 0 | 0 |

**Signal catalog:**

| signal | module | kind | value_source | conf | note |
|---|---|---|---|---|---|
| FPCCK | T&C->FPC | clock | FPC CK, once per 293 ns system clock | high | basic FPC clock from T&C |
| RESET/ | T&C->FPC | strobe | once per sample (29.3 us) | med | active-LOW; syncs the timing cycle at counter 0 (WCS RESET at count 99) |
| STBGN | FPC ROM U6 | control | ROM (counter) | low | strobe-begin; APPROX edges (~38, ~52, ~88) |
| STCONV/ | FPC ROM U6 -> AIN SAR | strobe | ROM (counter) | low | §3.8: brought HIGH at counter state 0 to START the AIN SAR conversion, held through the convert window, then back low (13th CNVCK resets SAR). [was inverted] APPROX edges |
| CNV CK | FPC ROM U6 -> AIN SAR | clock | ROM (gated burst) | low | §3.8: 13 convert-clock pulses per conversion (SAR data valid after the 12th; 13th resets SAR). Bursts during convert windows |
| LOAD | FPC ROM U6 | strobe | ROM (counter) | low | §3.8: asserted for TWO clock pulses — 1st loads input-gain counter U16 (IGA1/IGA0), 2nd loads the 12-bit SAR data into shift regs U27/U28/U38/U39; then shift-left per gain (00->4 shifts,01->3,10->2,11->1) |
| CH 1 | FPC ROM U6 | control | ROM (counter) | low | input channel select; CH1 ~0-52 then CH2 |
| CH1L | AIN module | control | derived from CH1 on AIN | low | §3.8/fig note: CH1 latched, generated on AIN (not FPC); its edge switches the input channel; APPROX |
| DATA VALID | FPC | data | conversion; gated to DAB by RD AD/ | low | §3.8: tri-state drivers U25/U26 gate converted data onto the DAB when the DSP asserts RD AD/. CH1 valid ~0-38, CH2 ~52-88 (gain-settling gaps) |
| RDAD/ & WR DA/ | FPC (self-test) | strobe | FPC DBUG high; counter-decode (U5) | low | SELF-TEST MODE only (FPC DBUG high): pulses ~count 38 and ~63 |
| BIT5 of counter | FPC counter U7/U8 | state | counter bit 5 (=32) | med | counter bit5 high for counts 32-63 |

## fig36 — FPC fixed->float (D/A output) cycle
*Source figure:* `fig-3.6-fixed-to-floating-da-cycle-timing.png` · *round-trip render:* `fig36.png`

> FPC D/A output sequencer (§3.8). Double buffer = 4-bit reg U40 (output-select SDAA-D) + 16-bit reg U36/U37 (output value); loaded on WR DA/, which sets NEW DAT/ (U3 pin6 = buffer full). When BUSY (from strobe counter U1/U2) is low, the value is loaded into shift reg U23/U24/U34/U35, the select into U41, and NEW DAT/ is cleared. Loading the shift reg also loads the strobe counter U1/U2 (initial 0x2A) and output-gain counter U43, starting an output cycle: gain counter counts up and the shift reg shifts LEFT until STOP/ (the two MSBs disagree = sign about to shift out) OR the counter has incremented 3 times. OGA1/OGA0 = 2 LSBs of the gain counter. flip-flop U3 then pulses mux-enable U42.15 to strobe OUT A-D. Coarse grid; TRANSITIONS APPROXIMATE.

| signal | G0 | G1 | G2 | G3(SCNT 2D..3F) | SCNT40 | next G0 | G1 | G2 |
|---|---|---|---|---|---|---|---|---|
| WR DA/ ?? | 0 | 1 | 1 | 1 | 1 | 1 | 1 | 0 |
| NEW DAT/ ?? | 0 | 1 | 0 | 0 | 0 | 0 | 0 | 0 |
| BUSY ?? | 0 | 1 | 1 | 1 | 1 | 1 | 1 | 0 |
| GCNT (U43) ~ | 0 | 1 | 2 | 3 | → | 0 | → | → |
| SCNT (U1/U2) ?? | · | · | · | 2A->40 | → | → | · | · |
| SHFT REG MODE (U23/24/34/35) ?? | LD | SHIFT | · | · | · | · | NOP | LD |
| OUT (A/B/C/D) ?? | · | · | settle 1.76us | → | → | → | valid ~4.08us | · |
| DAO-11,OGA0,OGA1 VALID ?? | · | · | VALID | → | → | → | → | · |

**Signal catalog:**

| signal | module | kind | value_source | conf | note |
|---|---|---|---|---|---|
| WR DA/ | DSP->FPC | strobe | DSP writes a D/A word | low | active-LOW; DSP asserts to load the double buffer (a new output value) |
| NEW DAT/ | FPC | strobe | double-buffer full (U3 pin6) | low | asserted when buffer loaded; deasserted when value moves to the shift reg (gated by NOR U14.1 so a reload doesn't clear it early) |
| BUSY | FPC (strobe counter U1/U2) | control | conversion in progress | low | high while a D/A conversion is running; inspected before loading the shift reg |
| GCNT (U43) | FPC | state | output GAIN counter U43 | med | output-gain counter 0-3; =3 holds while SCNT runs; 2 LSBs -> OGA1/OGA0 |
| SCNT (U1/U2) | FPC | state | strobe counter U1/U2 | low | strobe counter loaded at 0x2A, counts up during the conversion (293 ns/step) |
| SHFT REG MODE (U23/24/34/35) | FPC | control | sequencer | low | shift-register mode for the float mantissa: LOAD, SHIFT-left (fixed->float), then NOP |
| OUT (A/B/C/D) | FPC->AOUT | data | mux-enable strobe (U42.15 via U3) | low | §3.8/§3.10: OUT goes high ~1.76 us after DAC+gain valid (settling), then valid ~4.08 us (fig labels 4.10) |
| DAO-11,OGA0,OGA1 VALID | FPC->AOUT | data | D/A word + output gain | low | 12-bit D/A data DA0-11 + output-gain bits OGA0/OGA1 valid window |

---
## Global signal catalog — fixed-cadence vs microword-decoded

The model generates **fixed-cadence** signals straight from the MS/AS counters; **microword-decoded** signals need the decode map (their timing is here, their value is not).

| signal | figure | fixed-cadence? | value_source |
|---|---|---|---|
| MC | fig32 | yes | PLL master clock 30.72 MHz |
| O2 | fig32 | yes | 02/ = SBC system clock 2.048 MHz (488 ns); PLL phase reference, NOT from the MS counter |
| MS0 | fig32 | yes | MS counter (one-hot) |
| MS1 | fig32 | yes | MS counter (one-hot) |
| MS2 | fig32 | yes | MS counter (one-hot) |
| MS3 | fig32 | yes | MS counter (one-hot) |
| MS4 | fig32 | yes | MS counter (one-hot) |
| MS5 | fig32 | yes | MS counter (one-hot) |
| MS6 | fig32 | yes | MS counter (one-hot) |
| MS7 | fig32 | yes | MS counter (one-hot) |
| MS8 | fig32 | yes | MS counter (one-hot) |
| ARU CK | fig32 | yes | 1 per AS-state |
| AS0 | fig32 | yes | flip-flop set@MS1, clear@MS4 |
| AS1 | fig32 | yes | flip-flop set@MS5, clear@MS7 |
| AS2 | fig32 | yes | flip-flop set@MS7, clear@MS1(next) |
| ARU CK | fig34 | yes | 1 per AS |
| RA1,RA0 | fig34 | **NO (decode)** | microword read-addr bits |
| S1,S0 | fig34 | yes | fixed per-AS schedule |
| SHIFT REGISTER | fig34 | **NO (decode)** | operand F shifted |
| M1 | fig34 | **NO (decode)** | coeff C0/-C5/ serialized (odd) by U10 |
| M0 | fig34 | **NO (decode)** | coeff C0/-C5/ serialized (even) by U11 |
| PARTIAL PRODUCT REG | fig34 | **NO (decode)** | Booth partial products |
| CSIGN | fig34 | **NO (decode)** | microword sign bit |
| ACCUMULATOR | fig34 | **NO (decode)** | running sum |
| ZERO/ | fig34 | **NO (decode)** | microword ZERO bit |
| XFER CK | fig34 | **NO (decode)** | microword XFER bit |
| OFST/ VALID | fig33 | **NO (decode)** | 16-bit OFST0/-15/ bus (microword offset, complemented) |
| ADDRESS VALID | fig33 | **NO (decode)** | computed address bus = CPC - OFST |
| RAS/ | fig33 | yes | timing |
| ROW SEL | fig33 | yes | timing (U59) |
| CAS/ | fig33 | yes | timing AND MEMAC |
| DOUT VALID | fig33 | **NO (decode)** | DRAM read data on the DAB |
| DAB WSTB/ | fig33 | yes | timing |
| MEMW/ | fig33 | yes | timing AND write |
| DAB RSTB | fig33 | yes | timing |
| DIN VALID | fig33 | **NO (decode)** | DRAM write data on the DAB (from ARU result reg) |
| RESET/ | fig33 | yes | timing |
| CPC VALID (0-7) | fig33 | yes | CPC counter |
| FPCCK | fig35 | yes | FPC CK, once per 293 ns system clock |
| RESET/ | fig35 | yes | once per sample (29.3 us) |
| STBGN | fig35 | yes | ROM (counter) |
| STCONV/ | fig35 | yes | ROM (counter) |
| CNV CK | fig35 | yes | ROM (gated burst) |
| LOAD | fig35 | yes | ROM (counter) |
| CH 1 | fig35 | yes | ROM (counter) |
| CH1L | fig35 | **NO (decode)** | derived from CH1 on AIN |
| DATA VALID | fig35 | **NO (decode)** | conversion; gated to DAB by RD AD/ |
| RDAD/ & WR DA/ | fig35 | yes | FPC DBUG high; counter-decode (U5) |
| BIT5 of counter | fig35 | yes | counter bit 5 (=32) |
| WR DA/ | fig36 | **NO (decode)** | DSP writes a D/A word |
| NEW DAT/ | fig36 | **NO (decode)** | double-buffer full (U3 pin6) |
| BUSY | fig36 | **NO (decode)** | conversion in progress |
| GCNT (U43) | fig36 | yes | output GAIN counter U43 |
| SCNT (U1/U2) | fig36 | yes | strobe counter U1/U2 |
| SHFT REG MODE (U23/24/34/35) | fig36 | **NO (decode)** | sequencer |
| OUT (A/B/C/D) | fig36 | **NO (decode)** | mux-enable strobe (U42.15 via U3) |
| DAO-11,OGA0,OGA1 VALID | fig36 | **NO (decode)** | D/A word + output gain |
