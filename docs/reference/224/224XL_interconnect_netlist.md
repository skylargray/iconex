# 224XL — interconnect netlist (M0b)

> **What this is.** The net-by-net wiring of the ARU + T&C + DMEM as one machine, the artifact the
> phase-accurate RTL model (Phase 1+) is built from. Per `docs/plans/224XL-holistic-model-plan.md` §3 Phase 0b
> and the kickoff `docs/plans/224XL-M0b-netlist-prompt.md`. **This is a faithful transcription, gated on owner
> review before any Phase-1 code.**
>
> **Ground rules in force (plan §0):** (1) no pinout from memory — every pin here is keyed to a
> datasheet-verified `parts/*.v` via `224XL_partspec_verification.md`; (2) the schematic + owner traces are
> ground truth — transcribe faithfully, do **not** "correct" or label anything reversed/anomalous;
> (3) flag gaps, never guess; (4) provenance + confidence on every net; (5) adversarial verification targets
> OUR reads, not the board; (6) board-prefix every chip (`aru_` = 060-01318, `tc_` = 060-02475,
> `dmem_` = 060-02512); endpoints are `aru_U43.pin11`.

## Legend
- **Confidence:** ✅ read on sheet / owner pin-trace · 🟡 inferred or partial · 🟠 single-source/uncertain · ⚪ unknown (gap).
- **Driver** = the pin that sources the net; **loads** = pins that receive it. Tie-offs note GND/Vcc.
- **Net name:** owner-trace signal names are transcribed verbatim (`PPn`, `ACn`, `DABn`, `B-IN`, `SAT`, …).
  Numeric suffixes are **labels, not asserted bit-weights** (see §4.10). Internal nets I had to name myself are
  prefixed `_` and flagged as my naming.

## Build status (by net-group, plan §2 of the kickoff)
| # | Net-group | Status |
|---|---|---|
| 4 | **ARU PP/accumulator back-end** | ✅ **transcribed** (§4 — from the owner pin trace) |
| 4F | **ARU multiplier front-end** (regfile, shifters, Booth, M0/M1, PP adders) | ✅ **transcribed + owner-confirmed** (§4F; consistency-clean — §Q) |
| 5 | **DMEM address path / DRAM / XREG** | ✅ **transcribed** (§5 — owner hand-trace 060-02512) |
| 2 | Device decode / DAB-driver select | 🟡 **DMEM-resident I/O decode done** (§2D, 060-02512); T&C DAB-driver select (`tc_U47/48/49`, 060-02475) still ⚪ |
| 6 | Clock / strobe distribution | 🟡 **DMEM RAS/CAS/ROW-SEL strobe-gen done** (§6D, 060-02512; fig-3.3); T&C clock-gen (MC/MS/AS, 060-02475) still ⚪ — timing in `224XL_timing_spec.md` |
| 3 | WCS-output → control-input wiring | ⚪ not started (060-02475 + 02512) |
| 1 | DAB bus (full driver/receiver/enable summary) | 🟡 partial — ARU result-reg §4.8, regfile D-in §4F.1, DMEM DRAM + XREG §5.5/§5.6; full per-cycle enable summary pends group 3 |

---

# Net-group 4 — ARU PP / accumulator back-end  ✅

**Source:** `docs/reference/224/224XL ARU pinouts from 060-01318.txt` (owner pin trace, board 060-01318),
re-keyed to the verified pinouts in `224XL_partspec_verification.md`. Every net in this group is **✅** =
present in the owner trace. Board prefix `aru_` throughout.

**Chips in this group** (function ← `224XL_partspec_verification.md`):
`aru_U43/U44` 74F374 result reg · `aru_U45-U49` 74LS163 accumulator · `aru_U33-U37` 74F157 sat-mux ·
`aru_U19-U23` 74F283 adder · `aru_U5-U9` 74S86 subtract-XOR · `aru_U42` 74S86 overflow-XOR ·
`aru_U2` 74S04 inverter · `aru_U10/U11` 74F374 + `aru_U12` 74S175 product register.

## 4.0 Dataflow (what the wiring computes — for orientation, not a claim about bit-weights)
```
            (front-end: regfile→shifters→Booth→PP adders  ── GAP §G1)
                                   │  D
                          ┌────────▼────────┐  ARUCK
   product register  PR   │ aru_U10/U11/U12 │◄────────── ARUCK   (Q = PR0..PR19)
                          └────────┬────────┘
                                   │ Q
                          ┌────────▼────────┐  sub-ctrl rail (CSIGN), per bit
        subtract XOR      │  aru_U5..U9     │  Bk = PRk XOR sub-ctrl
                          └────────┬────────┘
                                   │ B
        accumulator AC ──A──►┌─────▼─────┐  C0(carry-in)=aru_U2.pin6 (CSIGN)
        (feedback)           │ aru_U19..U23 (adder chain, U19=low→U23=high) │
                             └─────┬─────┘  Σ
                                   │  (Σ also taps aru_U42 → SAT overflow; B3-top → aru_U2 → B-IN)
                          ┌────────▼────────┐  SEL = SAT
        sat-mux           │ aru_U33..U37    │  I0 = Σ (normal), I1 = B-IN (clamp)
                          └────────┬────────┘  Y = PP0..PP19
                                   │ PP
                 ┌─────────────────┼───────────────────┐
                 │ PP (all 20)     │ PP3..PP18 (16)     │
        ┌────────▼────────┐  ZERO/ │            ┌───────▼────────┐  XFER CK
        │ aru_U45..U49    │◄ARUCKE/│            │ aru_U43/U44    │◄──────── XFER CK
        │ accumulator reg │        │            │ result register│
        └────────┬────────┘        │            └───────┬────────┘  OE = RDRREG/
                 │ Q = AC0..AC19    │                    │ Q
                 └──────────────────┘                    ▼ DAB0..DAB15  (shared DAB bus)
              (AC feeds adder A — the accumulate loop)
```
Net summary: the **accumulate loop** is AC (accumulator Q) → adder A; the **add term** is PR (product reg Q)
→ XOR(sub-ctrl) → adder B; the sum Σ → sat-mux → PP → back into the accumulator on `ARUCKE/` (cleared by
`ZERO/`). `XFER CK` snapshots PP3..PP18 into the result register, which drives the DAB when `RDRREG/` enables it.

---

## 4.1 AC bus — accumulator output (AC0..AC19)
Driver = accumulator reg Q output; load = adder A input (the feedback). 20 nets, all ✅ (owner trace).

| Net | Driver | Load |
|---|---|---|
| AC0 | aru_U45.pin14 (QA) | aru_U19.pin5 (A0) |
| AC1 | aru_U45.pin13 (QB) | aru_U19.pin3 (A1) |
| AC2 | aru_U45.pin12 (QC) | aru_U19.pin14 (A2) |
| AC3 | aru_U45.pin11 (QD) | aru_U19.pin12 (A3) |
| AC4 | aru_U46.pin14 (QA) | aru_U20.pin5 (A0) |
| AC5 | aru_U46.pin13 (QB) | aru_U20.pin3 (A1) |
| AC6 | aru_U46.pin12 (QC) | aru_U20.pin14 (A2) |
| AC7 | aru_U46.pin11 (QD) | aru_U20.pin12 (A3) |
| AC8 | aru_U47.pin14 (QA) | aru_U21.pin5 (A0) |
| AC9 | aru_U47.pin13 (QB) | aru_U21.pin3 (A1) |
| AC10 | aru_U47.pin12 (QC) | aru_U21.pin14 (A2) |
| AC11 | aru_U47.pin11 (QD) | aru_U21.pin12 (A3) |
| AC12 | aru_U48.pin14 (QA) | aru_U22.pin5 (A0) |
| AC13 | aru_U48.pin13 (QB) | aru_U22.pin3 (A1) |
| AC14 | aru_U48.pin12 (QC) | aru_U22.pin14 (A2) |
| AC15 | aru_U48.pin11 (QD) | aru_U22.pin12 (A3) |
| AC16 | aru_U49.pin14 (QA) | aru_U23.pin5 (A0) |
| AC17 | aru_U49.pin13 (QB) | aru_U23.pin3 (A1) |
| AC18 | aru_U49.pin12 (QC) | aru_U23.pin14 (A2) |
| AC19 | aru_U49.pin11 (QD) | aru_U23.pin12 (A3) |

## 4.2 PP bus — sat-mux output (PP0..PP19)
Driver = sat-mux Y output; loads = accumulator reg D input, **and** (PP3..PP18 only) result reg D input.
20 nets, all ✅. (PP0,PP1,PP2,PP19 do **not** reach the result register — see §4.8.)

| Net | Driver | Load (accumulator) | Load (result reg) |
|---|---|---|---|
| PP0 | aru_U33.pin4 (Y1) | aru_U45.pin6 (D) | — |
| PP1 | aru_U33.pin7 (Y2) | aru_U45.pin5 (C) | — |
| PP2 | aru_U33.pin9 (Y4) | aru_U45.pin4 (B) | — |
| PP3 | aru_U33.pin12 (Y3) | aru_U45.pin3 (A) | aru_U43.pin14 (D5) |
| PP4 | aru_U34.pin4 (Y1) | aru_U46.pin6 (D) | aru_U43.pin13 (D4) |
| PP5 | aru_U34.pin7 (Y2) | aru_U46.pin5 (C) | aru_U43.pin18 (D7) |
| PP6 | aru_U34.pin9 (Y4) | aru_U46.pin4 (B) | aru_U43.pin17 (D6) |
| PP7 | aru_U34.pin12 (Y3) | aru_U46.pin3 (A) | aru_U43.pin4 (D1) |
| PP8 | aru_U35.pin4 (Y1) | aru_U47.pin6 (D) | aru_U43.pin3 (D0) |
| PP9 | aru_U35.pin7 (Y2) | aru_U47.pin5 (C) | aru_U43.pin8 (D3) |
| PP10 | aru_U35.pin9 (Y4) | aru_U47.pin4 (B) | aru_U43.pin7 (D2) |
| PP11 | aru_U35.pin12 (Y3) | aru_U47.pin3 (A) | aru_U44.pin14 (D5) |
| PP12 | aru_U36.pin4 (Y1) | aru_U48.pin6 (D) | aru_U44.pin13 (D4) |
| PP13 | aru_U36.pin7 (Y2) | aru_U48.pin5 (C) | aru_U44.pin18 (D7) |
| PP14 | aru_U36.pin9 (Y4) | aru_U48.pin4 (B) | aru_U44.pin17 (D6) |
| PP15 | aru_U36.pin12 (Y3) | aru_U48.pin3 (A) | aru_U44.pin4 (D1) |
| PP16 | aru_U37.pin4 (Y1) | aru_U49.pin6 (D) | aru_U44.pin3 (D0) |
| PP17 | aru_U37.pin7 (Y2) | aru_U49.pin5 (C) | aru_U44.pin8 (D3) |
| PP18 | aru_U37.pin9 (Y4) | aru_U49.pin4 (B) | aru_U44.pin7 (D2) |
| PP19 | aru_U37.pin12 (Y3) | aru_U49.pin3 (A) | — |

> Note PP18 → aru_U44.pin7: the owner trace lists U44.pin7 as `D2`. (74F374 pin7 = D2 per the verified pinout.)
> Result reg captures exactly **PP3..PP18 = 16 bits** → consistent with `result = sat16(ACC ≫ 3)` (low 3 and
> top 1 of the 20-bit saturated value dropped). The PP→result-reg bit assignment is tabulated in §4.8.

## 4.3 Adders — aru_U19..U23 (74F283), one nibble each
A-input = AC (feedback, §4.1). B-input = subtract-XOR output (§4.6). Σ-output → sat-mux I0 (§4.4) — these Σ→mux
nets are 1-driver/1-load internal; named `_aru_sumN` (my naming). Carry-in of the chain = CSIGN path (§4.5).

**Carry chain (ripple, low→high):** ✅
| Net | Driver | Load |
|---|---|---|
| _aru_cin (chain carry-in) | aru_U2.pin6 (74S04 inv-3 Y) | aru_U19.pin7 (C0) |
| _aru_c4_19 | aru_U19.pin9 (C4) | aru_U20.pin7 (C0) |
| _aru_c4_20 | aru_U20.pin9 (C4) | aru_U21.pin7 (C0) |
| _aru_c4_21 | aru_U21.pin9 (C4) | aru_U22.pin7 (C0) |
| _aru_c4_22 | aru_U22.pin9 (C4) | aru_U23.pin7 (C0) |
| (aru_U23.pin9 C4) | — | Not depicted in trace (top carry-out unused / ⚪) |

**Σ → sat-mux I0** (driver = adder Σ, load = mux A-input): ✅
| Net | Driver (adder Σ) | Load (mux I0) |
|---|---|---|
| _aru_sum0 | aru_U19.pin4 (Σ0) | aru_U33.pin2 (A1/I0a) |
| _aru_sum1 | aru_U19.pin1 (Σ1) | aru_U33.pin5 (A2/I0b) |
| _aru_sum2 | aru_U19.pin13 (Σ2) | aru_U33.pin11 (A4/I0d) |
| _aru_sum3 | aru_U19.pin10 (Σ3) | aru_U33.pin14 (A3/I0c) |
| _aru_sum4 | aru_U20.pin4 (Σ0) | aru_U34.pin2 |
| _aru_sum5 | aru_U20.pin1 (Σ1) | aru_U34.pin5 |
| _aru_sum6 | aru_U20.pin13 (Σ2) | aru_U34.pin11 |
| _aru_sum7 | aru_U20.pin10 (Σ3) | aru_U34.pin14 |
| _aru_sum8 | aru_U21.pin4 | aru_U35.pin2 |
| _aru_sum9 | aru_U21.pin1 | aru_U35.pin5 |
| _aru_sum10 | aru_U21.pin13 | aru_U35.pin11 |
| _aru_sum11 | aru_U21.pin10 | aru_U35.pin14 |
| _aru_sum12 | aru_U22.pin4 | aru_U36.pin2 |
| _aru_sum13 | aru_U22.pin1 | aru_U36.pin5 |
| _aru_sum14 | aru_U22.pin13 | aru_U36.pin11 |
| _aru_sum15 | aru_U22.pin10 | aru_U36.pin14 |
| _aru_sum16 | aru_U23.pin4 | aru_U37.pin2 |
| _aru_sum17 | aru_U23.pin1 | aru_U37.pin5 |
| _aru_sum18 | aru_U23.pin13 (Σ2) | aru_U37.pin11 (A4/I0d) *(also taps aru_U42.pin2 — §4.5)* |
| _aru_sum19 | aru_U23.pin10 (Σ3) | aru_U37.pin14 (A3/I0c) *(also taps aru_U42.pin1 — §4.5)* |

> A-inputs are AC0..AC19 (§4.1); B-inputs are `_aru_xorB0..19` (§4.6). The Σ index ↔ PP index mapping is
> monotonic through the mux (Σk → PPk), per §4.2/§4.4.

## 4.4 Sat-muxes — aru_U33..U37 (74F157)
Per-channel: I0 = adder Σ (normal path), I1 = `B-IN` (saturation clamp), Y = PP. SEL = `SAT`. Strobe G\ = GND.
✅ (owner trace).

| Pin role (each of U33-U37) | Net |
|---|---|
| pin1 SEL (A/B select) | **SAT** (driver aru_U42.pin3 — §4.5) |
| pin2 I0a, pin5 I0b, pin11 I0d, pin14 I0c | `_aru_sumN` (§4.3) |
| pin3 I1a, pin6 I1b, pin10 I1d, pin13 I1c | **B-IN** (driver aru_U2.pin8 — §4.5) — **U33-U36 all four; see exception for U37 below** |
| pin4 Y1, pin7 Y2, pin9 Y4, pin12 Y3 | **PPn** (§4.2) |
| pin15 G\ (output strobe) | GND (tie-off → always enabled) |

> **⚠ U37 clamp exception (✅ owner trace — faithfully transcribed):** on aru_U37 only, the two channels
> carrying the **top** PP bits use the **un-inverted** clamp node, not `B-IN`:
> - aru_U37.pin3 (I1a), aru_U37.pin6 (I1b) = **B-IN** (aru_U2.pin8), same as U33-U36.
> - aru_U37.pin10 (I1d), aru_U37.pin13 (I1c) = **`_aru_topB`** = aru_U2.pin9 & aru_U23.pin11 (the
>   *pre-inverter* top adder-B node, §4.5) — **not** B-IN.
>
> SEL semantics from the verified 74157 pinout: SEL low → I0 (the adder sum, normal); SEL high → I1 (the clamp).
> So `SAT=1` forces every PP bit to its clamp input. 🟡 The split (top bits get `_aru_topB`, all others get the
> inverted `B-IN`) is what makes the clamp resolve to a proper ±full-scale pattern — interpretation deferred
> (Ground Rule 3), wiring transcribed faithfully.

## 4.5 Saturation logic — overflow detect (aru_U42 74S86) + clamp value (aru_U2 74S04)
✅ (owner trace).

| Net | Driver | Load(s) | Meaning (🟡 inferred) |
|---|---|---|---|
| **SAT** | aru_U42.pin3 (74S86 1Y) | aru_U33-U37.pin1 (all five SEL) | overflow flag |
| `_aru_sum19` (same net as §4.3) | aru_U23.pin10 (Σ3 top) | aru_U37.pin14 (I0c) **+ aru_U42.pin1 (1A)** | top sum bit, also into overflow XOR |
| `_aru_sum18` (same net as §4.3) | aru_U23.pin13 (Σ2 top) | aru_U37.pin11 (I0d) **+ aru_U42.pin2 (1B)** | next sum bit, also into overflow XOR |
| **B-IN** | aru_U2.pin8 (74S04 inv-4 Y) | aru_U33-U36 all four I1 pins (3,6,10,13) **+ aru_U37.pin3, aru_U37.pin6** | inverted clamp value (most bits) |
| **`_aru_topB`** | aru_U9.pin11 (74S86 4Y, = bit-19 subtract-XOR out) | aru_U23.pin11 (B3, top adder B-in) · aru_U2.pin9 (inv-4 A, → makes B-IN) · **aru_U37.pin10 (I1d)** · **aru_U37.pin13 (I1c)** | un-inverted top adder-B node; also the clamp value for U37's top channels |

> 🟡 Reading: `SAT = Σ19 XOR Σ18` (two-MSB-disagree overflow detect). The clamp uses two polarities of the
> sign bit: `B-IN = NOT(_aru_topB)` on most bits, but the **top** PP bits (U37 I1c/I1d) get `_aru_topB`
> un-inverted — together producing a proper ±full-scale saturated word. Transcribed faithfully; the
> overflow/clamp *interpretation* is not asserted as fact (Ground Rule 3) — it follows from the model.
> `aru_U2.pin6` (inv-3 Y) drives the adder chain carry-in (`_aru_cin`, §4.3); inv-3's input (aru_U2.pin5)
> is the **CSIGN/subtract carry path** and is **not in the owner trace → ⚪ GAP §G2.**

## 4.6 Subtract-XOR row — aru_U5..U9 (74S86): PR XOR sub-ctrl → adder B
Each gate: A = product-register Q bit (`PRn`), B = **sub-ctrl rail** (commoned), Y = adder B input
(`_aru_xorBn`). The owner notes pins 2,5,10,13 of all five are commoned to the subtract-control rail
("CS33N/ via aru_U2"). ✅

**Sub-control rail:** origin now traced — see **§4F.8** (driven by aru_U2 from `CSIGN/`; `CSIGN/` itself = WCS/T&C, §G3).
| Net | Driver | Loads |
|---|---|---|
| **sub-ctrl rail** (U5/U6 group) | aru_U2.pin10 (5Y, =inv CSIGN/) | aru_U5.pin2,5,10,13 · aru_U6.pin2,5,10,13 |
| **sub-ctrl rail** (U7/U8/U9 group) | aru_U2.pin12 (6Y, =inv CSIGN/) | aru_U7.pin2,5,10,13 · aru_U8.pin2,5,10,13 · aru_U9.pin2,5,10,13 |

**PR → XOR A, XOR Y → adder B** (✅; product-register bit names `PRn` are my naming — owner trace gives the pins):
| Bit | PR source (driver) | XOR gate (A in) | XOR Y (driver) | adder B load |
|---|---|---|---|---|
| 0 | aru_U12.pin2 (Q0) | aru_U5.pin12 (4B) | aru_U5.pin11 (4Y) | aru_U19.pin11 (B3) |
| 1 | aru_U12.pin7 (Q1) | aru_U5.pin9 (3A) | aru_U5.pin8 (3Y) | aru_U19.pin15 (B2) |
| 2 | aru_U12.pin10 (Q2) | aru_U5.pin4 (2A) | aru_U5.pin6 (2Y) | aru_U19.pin2 (B1) |
| 3 | aru_U12.pin15 (Q3) | aru_U5.pin1 (1A) | aru_U5.pin3 (1Y) | aru_U19.pin6 (B0) |
| 4 | aru_U11.pin12 (Q4) | aru_U6.pin12 (4B) | aru_U6.pin11 (4Y) | aru_U20.pin11 (B3) |
| 5 | aru_U11.pin15 (Q5) | aru_U6.pin9 (3A) | aru_U6.pin8 (3Y) | aru_U20.pin15 (B2) |
| 6 | aru_U11.pin16 (Q6) | aru_U6.pin4 (2A) | aru_U6.pin6 (2Y) | aru_U20.pin2 (B1) |
| 7 | aru_U11.pin19 (Q7) | aru_U6.pin1 (1A) | aru_U6.pin3 (1Y) | aru_U20.pin6 (B0) |
| 8 | aru_U11.pin2 (Q0) | aru_U7.pin12 (4B) | aru_U7.pin11 (4Y) | aru_U21.pin11 (B3) |
| 9 | aru_U11.pin5 (Q1) | aru_U7.pin9 (3A) | aru_U7.pin8 (3Y) | aru_U21.pin15 (B2) |
| 10 | aru_U11.pin6 (Q2) | aru_U7.pin4 (2A) | aru_U7.pin6 (2Y) | aru_U21.pin2 (B1) |
| 11 | aru_U11.pin9 (Q3) | aru_U7.pin1 (1A) | aru_U7.pin3 (1Y) | aru_U21.pin6 (B0) |
| 12 | aru_U10.pin12 (Q4) | aru_U8.pin12 (4B) | aru_U8.pin11 (4Y) | aru_U22.pin11 (B3) |
| 13 | aru_U10.pin15 (Q5) | aru_U8.pin9 (3A) | aru_U8.pin8 (3Y) | aru_U22.pin15 (B2) |
| 14 | aru_U10.pin16 (Q6) | aru_U8.pin4 (2A) | aru_U8.pin6 (2Y) | aru_U22.pin2 (B1) |
| 15 | aru_U10.pin19 (Q7) | aru_U8.pin1 (1A) | aru_U8.pin3 (1Y) | aru_U22.pin6 (B0) |
| 16 | aru_U10.pin2 (Q0) | aru_U9.pin12 (4B) | aru_U9.pin11 (4Y) | aru_U23.pin11 (B3) |
| 17 | aru_U10.pin5 (Q1) | aru_U9.pin9 (3A) | aru_U9.pin8 (3Y) | aru_U23.pin15 (B2) |
| 18 | aru_U10.pin6 (Q2) | aru_U9.pin4 (2A) | aru_U9.pin6 (2Y) | aru_U23.pin2 (B1) |
| 19 | aru_U10.pin9 (Q3) | aru_U9.pin1 (1A) | aru_U9.pin3 (1Y) | aru_U23.pin6 (B0) |

> aru_U9.pin11 (4Y, bit-16 XOR out / adder U23 B3) **also** feeds aru_U2.pin9 (B-IN source, §4.5) — i.e. the
> top B bit is tapped for the sign-extension clamp. ✅ (owner trace explicitly notes this dual connection).
> For aru_U6/U7/U8 the owner gave the A-inputs and stated pins 3,6,8,11 → adder B0..B3 "per pattern"; the B
> loads above follow that stated pattern (🟡 where only the pattern, not each pin, was written out — U6/U7/U8).
> U5 and U9 are spelled out pin-by-pin in the trace (✅).

## 4.7 Product register — aru_U10/U11 (74F374) + aru_U12 (74S175)
Holds the multiplier partial-product sum (`PR0..PR19`). D-inputs come from the **front-end PP adders**
(aru_U13/U24/U25/U38/U39 74F283 — ⚪ their full pinouts are GAP §G1; the owner trace gives only the Σ pins that
land on the product-register D inputs). Q-outputs → subtract-XOR (§4.6). Clock = **ARUCK**. ✅ for the pins
listed; the upstream adders are a gap.

**Clock / control:**
| Net | Pin | Note |
|---|---|---|
| **ARUCK** | aru_U10.pin11 (CP), aru_U11.pin11 (CP), aru_U12.pin9 (CP) | product-reg clock; origin = T&C (⚪ §G3) |
| (OE\) | aru_U10.pin1 = GND, aru_U11.pin1 = GND | always output-enabled (tie-off) |
| (CLR\) | aru_U12.pin1 = +5 | 74S175 clear tied high (tie-off) |

**D-inputs (from front-end PP adders — driver side is GAP §G1):**
| PR D-pin | Net (front-end adder Σ) |
|---|---|
| aru_U10.pin3 (D0) | aru_U24.pin10 (Σ3) |
| aru_U10.pin4 (D1) | aru_U24.pin13 (Σ2) |
| aru_U10.pin7 (D2) | aru_U24.pin1 (Σ1) |
| aru_U10.pin8 (D3) | aru_U24.pin4 (Σ0) |
| aru_U10.pin13 (D4) | aru_U38.pin10 (Σ3) |
| aru_U10.pin14 (D5) | aru_U38.pin13 (Σ2) |
| aru_U10.pin17 (D6) | aru_U38.pin1 (Σ1) |
| aru_U10.pin18 (D7) | aru_U38.pin4 (Σ0) |
| aru_U11.pin3 (D0) | aru_U25.pin10 (Σ3) |
| aru_U11.pin4 (D1) | aru_U25.pin13 (Σ2) |
| aru_U11.pin7 (D2) | aru_U25.pin1 (Σ1) |
| aru_U11.pin8 (D3) | aru_U25.pin4 (Σ0) |
| aru_U11.pin13 (D4) | aru_U39.pin10 (Σ3) |
| aru_U11.pin14 (D5) | aru_U39.pin13 (Σ2) |
| aru_U11.pin17 (D6) | aru_U39.pin1 (Σ1) |
| aru_U11.pin18 (D7) | aru_U39.pin4 (Σ0) |
| aru_U12.pin4 (D0) | aru_U13.pin10 (Σ3) |
| aru_U12.pin5 (D1) | aru_U13.pin13 (Σ2) |
| aru_U12.pin12 (D2) | aru_U13.pin1 (Σ1) |
| aru_U12.pin13 (D3) | aru_U13.pin4 (Σ0) |

**Q-outputs → §4.6 (PR source column).** ✅

## 4.8 Result register — aru_U43/U44 (74F374)
D = PP3..PP18 (§4.2); Q → **DAB0..DAB15**; OE\ = **RDRREG/**; CP = **XFER CK**. ✅ (owner trace).

**Control:**
| Net | Pins | Origin |
|---|---|---|
| **RDRREG/** | aru_U43.pin1 (OE\), aru_U44.pin1 (OE\) | DAB-driver enable for the result reg; from T&C device decode (⚪ §G3) |
| **XFER CK** | aru_U43.pin11 (CP), aru_U44.pin11 (CP) | result-reg load; from T&C (⚪ §G3) |

**Q → DAB (this is the ARU's drive of the shared DAB bus; the DAB also has other drivers/receivers on T&C/DMEM
— full bus summary in net-group 1, pending):**
| DAB net | Driver |
|---|---|
| DAB0 | aru_U43.pin15 (Q5) |
| DAB1 | aru_U43.pin12 (Q4) |
| DAB2 | aru_U43.pin19 (Q7) |
| DAB3 | aru_U43.pin16 (Q6) |
| DAB4 | aru_U43.pin5 (Q1) |
| DAB5 | aru_U43.pin2 (Q0) |
| DAB6 | aru_U43.pin9 (Q3) |
| DAB7 | aru_U43.pin6 (Q2) |
| DAB8 | aru_U44.pin15 (Q5) |
| DAB9 | aru_U44.pin12 (Q4) |
| DAB10 | aru_U44.pin19 (Q7) |
| DAB11 | aru_U44.pin16 (Q6) |
| DAB12 | aru_U44.pin5 (Q1) |
| DAB13 | aru_U44.pin2 (Q0) |
| DAB14 | aru_U44.pin9 (Q3) |
| DAB15 | aru_U44.pin6 (Q2) |

**PP → result-reg → DAB assignment** (faithful map; bit-weights NOT asserted, §4.10):
| DAB | ← Q | ← D | ← PP |
|---|---|---|---|
| DAB5 | Q0 p2 | D0 p3 | PP8 |
| DAB4 | Q1 p5 | D1 p4 | PP7 |
| DAB7 | Q2 p6 | D2 p7 | PP10 |
| DAB6 | Q3 p9 | D3 p8 | PP9 |
| DAB1 | Q4 p12 | D4 p13 | PP4 |
| DAB0 | Q5 p15 | D5 p14 | PP3 |
| DAB3 | Q6 p16 | D6 p17 | PP6 |
| DAB2 | Q7 p19 | D7 p18 | PP5 |
| DAB13 | Q0 p2 | D0 p3 | PP16 |
| DAB12 | Q1 p5 | D1 p4 | PP15 |
| DAB15 | Q2 p6 | D2 p7 | PP18 |
| DAB14 | Q3 p9 | D3 p8 | PP17 |
| DAB9 | Q4 p12 | D4 p13 | PP12 |
| DAB8 | Q5 p15 | D5 p14 | PP11 |
| DAB11 | Q6 p16 | D6 p17 | PP14 |
| DAB10 | Q7 p19 | D7 p18 | PP13 |

## 4.9 Accumulator register control — aru_U45..U49 (74LS163), common pins
✅ (owner trace; tie-offs put the '163 in permanent parallel-load mode = a clocked register with sync clear).
| Net | Pins (all of U45-U49) | Role |
|---|---|---|
| **ZERO/** | pin1 (CLR\) | synchronous clear of accumulator |
| **ARUCKE/** | pin2 (CP) | accumulator clock |
| GND | pin7 (ENP), pin9 (LOAD\), pin10 (ENT) | tie-offs → always-load mode |
| (RCO pin15) | — | not depicted / unused (⚪) |

> `ZERO/` and `ARUCKE/` origins = T&C / WCS (⚪ §G3). `ARUCKE/` vs `ARUCK` (product reg, §4.7) are distinct
> clocks in the owner trace — transcribed as two separate nets; their phase relationship is a T&C/clock-group item.

## 4.10 Bit-weight is intentionally NOT asserted here (Ground Rule 2/3)
The owner's `PPn`/`ACn`/`DABn` suffixes are transcribed **verbatim as net names**. Whether a given net is the
LSB or MSB of its word is **set by the whole-nibble wiring + the carry chain + the multiplier weighting acting
together**, and is validated by the model passing POST — it is **not** inferred from a pin's numeric label, and
nothing here is called "reversed/swapped." (This is the exact failure mode the plan §0 warns about: a prior
"audit" invented a "reversed accumulator" from single pin labels and was wrong.) The within-nibble D→Q vs
A-input ordering looks non-trivial; that is expected and is left for the model to resolve, not declared an anomaly.

---

# Net-group 4F — ARU multiplier FRONT-END  ✅ (owner trace, expanded 2026-06-27)

**Source:** same owner pin trace (`224XL ARU pinouts from 060-01318.txt`), front-end section, re-keyed to verified
pinouts + cross-checked by internal consistency (regfile→shifter F-nets, shifter→NAND SR-nets, carry chain,
adder→product-register feed all confirmed single-driver/symmetric). Two items 🟡 **pending owner confirm** (4F.5, 4F.7).

## 4F.0 Dataflow
```
DAB0..15 ─► regfile aru_U29-U32 (LS670, addr RA/WA) ─F0..F15─► dual-rank shifter aru_U3,U4,U15-U18 (LS194,
   CLK=ARUCK, mode S0/S1) ─SR0..SR19─► Booth NAND array aru_U14,U26,U27,U28,U40,U41,U50-U53 (LS00, 2nd input =
   M0/M1 rail from aru_U54) ─► front-end adders aru_U13,U24,U25,U38,U39 (F283, carry chain U13→U39→U25→U38→U24)
   ─Σ─► product register aru_U10/U11/U12 (§4.7) ─► [back-end MAC, group 4]
```
This is the multiplier: operand `F=reg[RA]` is loaded/shifted in the LS194 rank; the LS00 array forms the
modified-Booth partial products selected by M0/M1; the F283 chain sums them into the product register each ARUCK.

## 4F.1 Register file — aru_U29..U32 (74LS670, 4 words × 4 bits each; 4 chips = 4 words × 16 bits)
D ← DAB; Q → F-net; read-addr = {RA1_inv,RA0_inv}; write-addr = {WA1_inv,WA0_inv}; GW\=DAB WSTB/; GR\=GND. ✅
| Chip | D1(15)/D2(1)/D3(2)/D4(3) ← DAB | Q1(10)/Q2(9)/Q3(7)/Q4(6) → F |
|---|---|---|
| aru_U29 | DAB15 / DAB14 / DAB13 / DAB12 | F15 / F14 / F13 / F12 |
| aru_U30 | DAB11 / DAB10 / DAB9 / DAB8 | F11 / F10 / F9 / F8 |
| aru_U31 | DAB7 / DAB6 / DAB5 / DAB4 | F7 / F6 / F5 / F4 |
| aru_U32 | DAB3 / DAB2 / DAB1 / DAB0 | F3 / F2 / F1 / F0 |

Common to all four (✅): pin5(RA)=**RA1_inv**, pin4(RB)=**RA0_inv**, pin14(WA)=**WA1_inv**, pin13(WB)=**WA0_inv**,
pin12(GW\)=**DAB WSTB/**, pin11(GR\)=**GND**. (RA*/WA* inverted sources = aru_U54, §4F.6; their pre-inversion
origins RA0/RA1/WA0/WA1 + DAB WSTB/ come from T&C — §G3.)

## 4F.2 F-net bus (F0..F15): regfile Q (driver) → shifter parallel input (load) ✅
| Net | Driver | Load | Net | Driver | Load |
|---|---|---|---|---|---|
| F0 | aru_U32.pin6 | aru_U4.pin3 (A) | F8 | aru_U30.pin6 | aru_U18.pin3 (A) |
| F1 | aru_U32.pin7 | aru_U17.pin6 (D) | F9 | aru_U30.pin7 | aru_U16.pin6 (D) |
| F2 | aru_U32.pin9 | aru_U18.pin6 (D) | F10 | aru_U30.pin9 | aru_U15.pin6 (D) |
| F3 | aru_U32.pin10 | aru_U17.pin5 (C) | F11 | aru_U30.pin10 | aru_U16.pin5 (C) |
| F4 | aru_U31.pin6 | aru_U18.pin5 (C) | F12 | aru_U29.pin6 | aru_U15.pin5 (C) |
| F5 | aru_U31.pin7 | aru_U17.pin4 (B) | F13 | aru_U29.pin7 | aru_U16.pin4 (B) |
| F6 | aru_U31.pin9 | aru_U18.pin4 (B) | F14 | aru_U29.pin9 | aru_U15.pin4 (B) |
| F7 | aru_U31.pin10 | aru_U17.pin3 (A) | F15 | aru_U29.pin10 | aru_U15.pin3 (A) + aru_U16.pin3 (A) |

## 4F.3 Dual-rank shift register — aru_U3,U4,U15,U16,U17,U18 (74LS194) ✅
Common: pin1(CLR\)=+5V; pin9(S0)=**S0**; pin10(S1)=**S1**; pin11(CLK)=**ARUCK** (owner: *not* ARUCKE/).
(S0/S1/ARUCK origins = T&C — §G3.)
| Chip | parallel in A(3)/B(4)/C(5)/D(6) ← F | SR_SER(2) | Q QA(15)/QB(14)/QC(13)/QD(12) → SR |
|---|---|---|---|
| aru_U3 | GND / GND / nd / nd | SR4 | SR2 / SR0 / nd / nd |
| aru_U4 | F0 / GND / nd / nd | SR5 | SR3 / SR1 / nd / nd |
| aru_U15 | F15 / F14 / F12 / F10 | SR19 | SR19 / SR17 / SR15 / SR13 |
| aru_U16 | F15 / F13 / F11 / F9 | SR18 | SR18 / SR16 / SR14 / SR12 |
| aru_U17 | F7 / F5 / F3 / F1 | SR12 | SR10 / SR8 / SR6 / SR4 |
| aru_U18 | F8 / F6 / F4 / F2 | SR13 | SR11 / SR9 / SR7 / SR5 |

> Note the recirculation: aru_U15 QA=SR19 feeds its own SR_SER=SR19; aru_U16 QA=SR18 feeds its own SR_SER=SR18
> (dual-rank shift feedback). ✅ (owner trace; SR digest confirms single-driver).

## 4F.4 SR-net bus (SR0..SR19): shifter Q (driver) → NAND A-input(s) [+ SR_SER feedback] ✅
| Net | Driver (shifter Q) | NAND A-loads |
|---|---|---|
| SR0 | aru_U3.pin14 | aru_U28.pin12 |
| SR1 | aru_U4.pin14 | aru_U14.pin9, aru_U28.pin4 |
| SR2 | aru_U3.pin15 | aru_U14.pin12, aru_U28.pin9 |
| SR3 | aru_U4.pin15 | aru_U14.pin1, aru_U28.pin1, aru_U40.pin1 |
| SR4 | aru_U17.pin12 | aru_U14.pin4, aru_U40.pin9 (+ aru_U3.pin2 SR_SER) |
| SR5 | aru_U18.pin12 | aru_U41.pin9 (+ aru_U4.pin2 SR_SER) |
| SR6 | aru_U17.pin13 | aru_U40.pin12, aru_U41.pin12 |
| SR7 | aru_U18.pin13 | aru_U40.pin4, aru_U41.pin1 |
| SR8 | aru_U17.pin14 | aru_U26.pin12, aru_U27.pin9, aru_U41.pin4 |
| SR9 | aru_U18.pin14 | aru_U26.pin4, aru_U27.pin1 |
| SR10 | aru_U17.pin15 | aru_U27.pin4 |
| SR11 | aru_U18.pin15 | aru_U26.pin1, aru_U27.pin12 |
| SR12 | aru_U16.pin12 | aru_U26.pin9, aru_U50.pin1, aru_U51.pin4 (+ aru_U17.pin2 SR_SER) |
| SR13 | aru_U15.pin12 | aru_U50.pin4, aru_U51.pin1 (+ aru_U18.pin2 SR_SER) |
| SR14 | aru_U16.pin13 | aru_U50.pin9 |
| SR15 | aru_U15.pin13 | aru_U50.pin12, aru_U51.pin9 |
| SR16 | aru_U16.pin14 | aru_U51.pin12, aru_U52.pin12 |
| SR17 | aru_U15.pin14 | aru_U52.pin1, aru_U53.pin1 |
| SR18 | aru_U16.pin15 | aru_U52.pin4, aru_U53.pin4 (+ aru_U16.pin2 SR_SER) |
| SR19 | aru_U15.pin15 | aru_U52.pin9, aru_U53.pin9, aru_U53.pin12 (+ aru_U15.pin2 SR_SER) |

> ✅ **SR19 → aru_U53.pin9 AND aru_U53.pin12** (both tied to SR19 — **owner-confirmed** 2026-06-27, not a typo;
> top-bit replication in the Booth array). aru_U52.pin12=SR16 by contrast.

## 4F.5 Booth NAND array — aru_U14/U26/U27/U28/U40/U41/U50/U51/U52/U53 (74LS00)
Each 2-input NAND gate: **A** = an SR bit (§4F.4), **B** = the **M-rail** (Booth select), **Y** → a front-end
adder A or B input (§4F.7). The NAND→adder output mapping is given on the adder side (§4F.7). ✅ (owner-confirmed
2026-06-27). The M-rail is **split into M0 and M1** (the two modified-Booth selects), each driving five NANDs:
| M-rail | Driver | NANDs gated (each chip's pins 2,5,10,13 = 1B/2B/3B/4B) |
|---|---|---|
| **M1** | aru_U54.pin10 (5Y) | aru_U27, aru_U28, aru_U40, aru_U50, aru_U52 |
| **M0** | aru_U54.pin12 (6Y) | aru_U14, aru_U26, aru_U41, aru_U51, aru_U53 |

> ✅ M0//M1/ (the Booth-select sources at aru_U54.pin13/pin11) originate on T&C/WCS — §G3.

## 4F.6 aru_U54 (74S04) — address buffers + Booth-select inverters ✅
| Inverter | In | Out → |
|---|---|---|
| 1 | pin1 = **RA0** | pin2 = **RA0_inv** → regfile RB (all U29-32 pin4) |
| 2 | pin3 = **WA0** | pin4 = **WA0_inv** → regfile WB (all U29-32 pin13) |
| 3 | pin5 = **RA1** | pin6 = **RA1_inv** → regfile RA (all U29-32 pin5) |
| 4 | pin9 = **WA1** | pin8 = **WA1_inv** → regfile WA (all U29-32 pin14) |
| 5 | pin11 = **M1/** | pin10 = **M1** → M-rail of aru_U27,U28,U40,U50,U52 (§4F.5) ✅ |
| 6 | pin13 = **M0/** | pin12 = **M0** → M-rail of aru_U14,U26,U41,U51,U53 (§4F.5) ✅ |

> ✅ owner-confirmed 2026-06-27. RA0/RA1/WA0/WA1 (register-file addresses) and M0//M1/ (Booth selects) all
> originate on T&C/WCS — §G3.

## 4F.7 Front-end adders — aru_U13,U24,U25,U38,U39 (74F283): Booth partial-product summation ✅
A/B inputs ← Booth NAND outputs; Σ → product register (§4.7). **Carry chain:** aru_U13 (C0=+5V) → aru_U39 →
aru_U25 → aru_U38 → aru_U24 (C4 = n/c). ✅ (symmetric in trace).
| Adder | A0(5)/A1(3)/A2(14)/A3(12) ← NAND | B0(6)/B1(2)/B2(15)/B3(11) ← NAND | Cin(7) | Cout(9) | Σ0(4)/Σ1(1)/Σ2(13)/Σ3(10) → |
|---|---|---|---|---|---|
| aru_U13 | U14.8 / U14.11 / U14.3 / U14.6 | U28.11 / U28.6 / U28.8 / U28.3 | +5V | →U39.7 | aru_U12 (PR0-3) |
| aru_U39 | U41.8 / U41.11 / U41.3 / U41.6 | U40.8 / U40.3 / U40.11 / U40.6 | U13.9 | →U25.7 | aru_U11 (PR4-7 hi nibble) |
| aru_U25 | U26.6 / U26.11 / U26.3 / U26.8 | U27.8 / U27.3 / U27.6 / U27.11 | U39.9 | →U38.7 | aru_U11 (PR4-7 lo nibble) |
| aru_U38 | U51.3 / U51.6 / U51.8 / U51.11 | U50.3 / U50.6 / U50.8 / U50.11 | U25.9 | →U24.7 | aru_U10 (PR12-19 …) |
| aru_U24 | U53.3 / U53.6 / U53.11 / U53.8 | U52.11 / U52.3 / U52.6 / U52.8 | U38.9 | n/c | aru_U10 (PR12-19 …) |

> ✅ **aru_U25 A-inputs = U26** (owner-confirmed 2026-06-27; the earlier "U28" was a transcription slip caught by
> the internal-consistency cross-check). (Σ→product-register mapping per §4.7; the exact PR-bit ↔ adder-Σ weighting
> is left to the model, per §4.10.)

## 4F.8 Sub-control / CSIGN origin (resolves old §G2) ✅
The subtract path is now fully traced to the ARU boundary:
| Net | Driver | Loads |
|---|---|---|
| **CSIGN/** | (from T&C/WCS — §G3) | aru_U2.pin11 (5A), aru_U2.pin13 (6A) |
| **sub-ctrl rail (U5/U6)** | aru_U2.pin10 (5Y = inv of CSIGN/) | aru_U5 & aru_U6 pins 2,5,10,13; also sensed at aru_U2.pin5 (3A) |
| **sub-ctrl rail (U7/U8/U9)** | aru_U2.pin12 (6Y = inv of CSIGN/) | aru_U7 & aru_U8 & aru_U9 pins 2,5,10,13 |
| **_aru_cin** (adder carry-in) | aru_U2.pin6 (3Y = inv of the U5/U6 rail) | aru_U19.pin7 (C0) |

> So `sub-ctrl = NOT(CSIGN/)` XOR-ed into every adder B bit (§4.6), and the chain carry-in = NOT(sub-ctrl) =
> CSIGN/ — the standard two's-complement subtract enable. Source `CSIGN/` itself is a WCS/T&C signal (§G3).

---

# Net-group 5 — DMEM address path / DRAM / X-register  ✅

**Source:** owner hand-trace `docs/reference/224/224X_DMEM_pinouts_from_060-02512.txt` (board 060-02512),
re-keyed to verified `parts/*.v`; architecture cross-checked vs Service-Manual ch.3 + timing fig-3.3. Board
prefix `dmem_` throughout. Every net = **✅ owner trace** unless marked. Cross-board signal *origins*
(`OFST0–15/`, `RESET`, `CPC CLR`, `ADR0–7/`, `IORC//IOWC/`, `MEMAC`, `MEMW/`, `DAB RSTB`, the `XREG`/`DPORT`
strobes) are generated on T&C/SBC → **§G3D**.

**Chips:** `dmem_U51/U65` 74LS393 CPC · `dmem_U49/U50` 74F283 + `dmem_U63/U64` 74LS283 offset adders (same pinout)
· `dmem_U18/U36` 74LS157 row/col mux · `dmem_U20–U35` 4164 DRAM (populated) · **`dmem_U1–U16` 4164 — NOT POPULATED**
(this rev; older revs used a half-capacity part — owner-confirmed) · `dmem_U38–U41` 74LS374 X-register ·
`dmem_U42` 74LS374 bus-test reg · `dmem_U48/U62` 74LS244 offset read-back.

## 5.0 Dataflow (orientation)
```
 CPC counter dmem_U51/U65 (+1 per RESET edge) ──A──►┐
 OFST0..15/ (microword offset, complemented)  ──B──►│ adders dmem_U49→U50→U63→U64  (Cin=+5V)
                                                     │  Σ = address A0..A15  ( = CPC − OFST )
                       row/col mux dmem_U18/U36 (SEL=ROW SEL) ──AD0..7──► DRAM A0..7
 DAB0..15 ◄── DIN/DOUT ──► DRAM array dmem_U20..U35 (64K×16; RAS//CAS0//WR/)
 DAB0..15 ◄────────────► X-register dmem_U38..U41 ◄── DATA0..7/ ──► (SBC 8-bit I/O bus)
 OFST0..15/ ──► read-back buffers dmem_U48/U62 ── DATA0..7/ ──► (SBC reads the offset)
```
**Address = CPC − OFST** (two's-complement: A=CPC, B=complemented `OFST/`, chain carry-in tied HIGH). ✅ matches
fig-3.3 grid-note and SM ch.3. Net names: `A0..A15` = the adder **Σ outputs** (= the DRAM address bus); the
adders' own `(A0)..(A3)` **pins** are the CPC operand inputs — different signal (see the txt legend). CPC
operand nets named `_cpc0.._cpc15` (my naming; the trace gives them pin-to-pin, no net label).

> **✅ Independent confirmation — Service Manual §3.6 (Theory of Operation), verbatim, cross-checked 2026-06-27:**
> - *Addressing (§5.2):* "The absolute address of a memory reference is computed by subtracting the offset from
>   the current position. A 2's complement subtraction is performed by adding the complemented 16-bit word,
>   OFST/, to the output of the current position counter and **tying the carry input of the adder (U49, U50, U63,
>   and U64) high**." → names the adders by designator, matches §5.2 exactly.
> - *CPC (§5.1):* "held by a **16-bit current position counter (U51 and U65)** and is normally incremented once
>   every sampling interval." → matches §5.1.
> - *Address mux (§5.4):* "A **multiplexer (U18 and U36)** is used to multiplex the resulting address onto the
>   eight address lines of the 64k dynamic RAMs." → matches §5.4.
> - *X-register (§5.6):* "**U38, U39, U40, and U41 form the X register**, which enables the SBC module to read
>   from and write to the DAB. U38 and U40 … DAB → SBC; U39 and U41 … SBC → DAB." + "**decoders (U55, U56, U57)**
>   … generate the strobes used in the I/O access of the ports." → matches §5.6 + §2D.1.
> - *Strobe delay-line (§6D):* "timing and control signals … generated by a **delay-line circuit (U59)** based on
>   … **MEMAC, DABSTB, and MEMR**." → matches §6D.
> - *Bank footprint:* Ch.5 §5.3.2 (E91/E92 = bank 1 = U20–U35; E95/E96 = bank 2 = U1–U16) corroborates the
>   two-bank footprint — this rev populates **bank 1 only** (bank 2 = U1–U16 unpopulated; §5.5/§G3D).
> - **Gap:** §3.6 names only MEMAC/DABSTB/MEMR as the T&C → DMEM timing inputs; `MEMW/` → `WR/` (via dmem_U61H,
>   §6D.3) is **owner-trace-only** — its T&C origin is unconfirmed (§G3D).

## 5.1 CPC — current-position counter `dmem_U51`, `dmem_U65` (74LS393) ✅
16-bit ripple counter: `dmem_U51` = bits 0–7, `dmem_U65` = bits 8–15. Clocked by the **RESET** net on 1CP
(a '393 counts on the **falling** edge of CP — datasheet); async clear = **CPC CLR** on MR. ⚠ "RESET" is the
*count clock* here, not the clear — and is distinct from `RESET/` (slashed). Its source/role beyond the pin is
**not traced** (§G3D).

| Net | Pins | Role |
|---|---|---|
| **RESET** | dmem_U51.pin1 (1CP) | CPC count clock (falling edge); ⚪ source = §G3D |
| (ripple 7→8) | dmem_U51.pin8 (2QD) → dmem_U65.pin1 (1CP) | low-byte carry clocks high byte |
| **CPC CLR** | dmem_U51.pin2 (1MR), dmem_U51.pin12 (2MR), dmem_U65.pin2 (1MR), dmem_U65.pin12 (2MR) | async clear; ⚪ source = §G3D (driven by dmem_U58F.pin12) |
| _cascade U51 | dmem_U51.pin13 (2CP) = dmem_U51.pin6 (1QD) | nibble ripple |
| _cascade U65 | dmem_U65.pin13 (2CP) = dmem_U65.pin6 (1QD) | nibble ripple |

**CPC Q → adder A-input** (driver = '393 Q, load = '283 A pin):
| _cpc | Driver | Load | _cpc | Driver | Load |
|---|---|---|---|---|---|
| _cpc0 | dmem_U51.pin3 (1QA) | dmem_U49.pin5 (A0) | _cpc8 | dmem_U65.pin3 (1QA) | dmem_U63.pin5 (A0) |
| _cpc1 | dmem_U51.pin4 (1QB) | dmem_U49.pin3 (A1) | _cpc9 | dmem_U65.pin4 (1QB) | dmem_U63.pin3 (A1) |
| _cpc2 | dmem_U51.pin5 (1QC) | dmem_U49.pin14 (A2) | _cpc10 | dmem_U65.pin5 (1QC) | dmem_U63.pin14 (A2) |
| _cpc3 | dmem_U51.pin6 (1QD) | dmem_U49.pin12 (A3) | _cpc11 | dmem_U65.pin6 (1QD) | dmem_U63.pin12 (A3) |
| _cpc4 | dmem_U51.pin11 (2QA) | dmem_U50.pin5 (A0) | _cpc12 | dmem_U65.pin11 (2QA) | dmem_U64.pin5 (A0) |
| _cpc5 | dmem_U51.pin10 (2QB) | dmem_U50.pin3 (A1) | _cpc13 | dmem_U65.pin10 (2QB) | dmem_U64.pin3 (A1) |
| _cpc6 | dmem_U51.pin9 (2QC) | dmem_U50.pin14 (A2) | _cpc14 | dmem_U65.pin9 (2QC) | dmem_U64.pin14 (A2) |
| _cpc7 | dmem_U51.pin8 (2QD) | dmem_U50.pin12 (A3) | _cpc15 | dmem_U65.pin8 (2QD) | dmem_U64.pin12 (A3) |

## 5.2 Offset adders `dmem_U49/U50` (74F283) + `dmem_U63/U64` (74LS283) — address = CPC − OFST ✅
A = CPC (§5.1), B = `OFST/` (complemented offset), Σ = address `A0..A15`. **Carry chain:** U49 (C0=+5V) → U50 →
U63 → U64 (C4 = n/c). Carry-in tied HIGH = the +1 of the two's-complement subtract.

**Carry chain:** dmem_U49.pin7(C0)=+5V; dmem_U49.pin9(C4)→dmem_U50.pin7(C0); dmem_U50.pin9→dmem_U63.pin7;
dmem_U63.pin9→dmem_U64.pin7; dmem_U64.pin9(C4)=n/c.

**B-inputs (OFST/) and Σ-outputs (address A):**
| Adder | B0(6)/B1(2)/B2(15)/B3(11) ← OFST/ | Σ0(4)/Σ1(1)/Σ2(13)/Σ3(10) → addr net |
|---|---|---|
| dmem_U49 | OFST0/ / OFST1/ / OFST2/ / OFST3/ | A0 / A1 / A2 / A3 |
| dmem_U50 | OFST4/ / OFST5/ / OFST6/ / OFST7/ | A4 / A5 / A6 / A7 |
| dmem_U63 | OFST8/ / OFST9/ / OFST10/ / OFST11/ | A8 / A9 / A10 / A11 |
| dmem_U64 | OFST12/ / OFST13/ / OFST14/ / OFST15/ | A12 / A13 / A14 / A15 |

> A-inputs are `_cpc0.._cpc15` (§5.1). `OFST0–15/` come from the microword offset (T&C/WCS, §G3D). The A↔Σ
> within-nibble ordering follows the verified 74283 pinout (non-monotonic upper nibble) — bit-weight not
> asserted here (Ground Rule 2/3, cf §4.10).

## 5.3 Address bus `A0..A15` (adder Σ) → row/col mux ✅
| Net | Driver (adder Σ) | Load (mux) | Net | Driver | Load |
|---|---|---|---|---|---|
| A0 | dmem_U49.pin4 | dmem_U36.pin3 (B1) | A8 | dmem_U63.pin4 | dmem_U36.pin2 (A1) |
| A1 | dmem_U49.pin1 | dmem_U36.pin6 (B2) | A9 | dmem_U63.pin1 | dmem_U36.pin5 (A2) |
| A2 | dmem_U49.pin13 | dmem_U36.pin10 (B3) | A10 | dmem_U63.pin13 | dmem_U36.pin11 (A3) |
| A3 | dmem_U49.pin10 | dmem_U36.pin13 (B4) | A11 | dmem_U63.pin10 | dmem_U36.pin14 (A4) |
| A4 | dmem_U50.pin4 | dmem_U18.pin3 (B1) | A12 | dmem_U64.pin4 | dmem_U18.pin2 (A1) |
| A5 | dmem_U50.pin1 | dmem_U18.pin6 (B2) | A13 | dmem_U64.pin1 | dmem_U18.pin5 (A2) |
| A6 | dmem_U50.pin13 | dmem_U18.pin10 (B3) | A14 | dmem_U64.pin13 | dmem_U18.pin11 (A3) |
| A7 | dmem_U50.pin10 | dmem_U18.pin13 (B4) | A15 | dmem_U64.pin10 | dmem_U18.pin14 (A4) |

## 5.4 Row/col multiplexers `dmem_U18`, `dmem_U36` (74LS157) → DRAM address `AD0..7` ✅
Common: pin1 (SEL) = **ROW SEL**; pin15 (G\) = GND (always enabled). Per 74157: SEL **low → A** side, SEL
**high → B** side. The **B** side carries `A0..A7` (low addr), the **A** side `A8..A15` (high addr).
| Mux out | Pin (Y) | A-input (8–15) | B-input (0–7) |
|---|---|---|---|
| **AD0** | dmem_U36.pin4 (Y1) →33R | A8 (pin2) | A0 (pin3) |
| **AD1** | dmem_U36.pin7 (Y2) →33R | A9 (pin5) | A1 (pin6) |
| **AD2** | dmem_U36.pin9 (Y3) →33R | A10 (pin11) | A2 (pin10) |
| **AD3** | dmem_U36.pin12 (Y4) →33R | A11 (pin14) | A3 (pin13) |
| **AD4** | dmem_U18.pin4 (Y1) →33R | A12 (pin2) | A4 (pin3) |
| **AD5** | dmem_U18.pin7 (Y2) →33R | A13 (pin5) | A5 (pin6) |
| **AD6** | dmem_U18.pin9 (Y3) →33R | A14 (pin11) | A6 (pin10) |
| **AD7** | dmem_U18.pin12 (Y4) →33R | A15 (pin14) | A7 (pin13) |

> Per fig-3.3 `ROW SEL` (owner-confirmed): HIGH (row) MS0–2, LOW (col) MS3–7, HIGH MS8. SEL high → B → DRAM
> latches **row = A0..A7** (on RAS/); SEL low → A → **col = A8..A15** (on CAS/). Standard 64K-DRAM row/col split.
> `AD0..7` feed the DRAM address pins through 33Ω series resistors.

## 5.5 DRAM array `dmem_U20..U35` (4164) — 64K×16 delay memory ✅
16 devices, one per DAB bit. **`dmem_U1..U16` are NOT POPULATED** (older-rev footprints; their CAS1/ is
hard-disabled — §6D). Populated bank uses **CAS0/**.

**Common to all `dmem_U20..U35`:** pin1 NC · pin3 (WR/) = **WR/** · pin4 (RAS/) = **RAS/** · pin5 (A0)=AD0 ·
pin6 (A2)=AD2 · pin7 (A1)=AD1 · pin8 VCC · pin9 (A7)=AD7 · pin10 (A5)=AD5 · pin11 (A4)=AD4 · pin12 (A3)=AD3 ·
pin13 (A6)=AD6 · pin15 (CAS/) = **CAS0/** · pin16 VSS. (Strobe sources: WR/←§6D, RAS//CAS0/←§6D.)

**Per-device DIN (pin2) & DOUT (pin14) — both tied to the same DAB line** (bidirectional; DOUT 3-state except on read):
| Device | DAB | Device | DAB | Device | DAB | Device | DAB |
|---|---|---|---|---|---|---|---|
| dmem_U20 | DAB0 | dmem_U24 | DAB4 | dmem_U28 | DAB8 | dmem_U32 | DAB12 |
| dmem_U21 | DAB1 | dmem_U25 | DAB5 | dmem_U29 | DAB9 | dmem_U33 | DAB13 |
| dmem_U22 | DAB2 | dmem_U26 | DAB6 | dmem_U30 | DAB10 | dmem_U34 | DAB14 |
| dmem_U23 | DAB3 | dmem_U27 | DAB7 | dmem_U31 | DAB11 | dmem_U35 | DAB15 |

## 5.6 X-register `dmem_U38–U41` (74LS374) + bus-test reg `dmem_U42` — DAB ↔ DATA bridge ✅
Bridges the 16-bit DAB to the SBC 8-bit data bus `DATA0–7/`. Read path: DAB→DATA via U38 (low byte)/U40 (high
byte). Write path: DATA→DAB via U39 (→DAB0–7)/U41 (→DAB8–15). All XREG strobes ← §G3D.

| Chip | Function | D ← | Q → | OE\ (pin1) | CP (pin11) |
|---|---|---|---|---|---|
| dmem_U38 | DAB→DATA, low | D0-7(3,4,7,8,13,14,17,18) = **DAB0..DAB7** | Q0-7(2,5,6,9,12,15,16,19) = **DATA0/..DATA7/** | **RDL XREG/** | **WR XREG/** (=dmem_U61.pin12) [& dmem_U40.pin11] |
| dmem_U40 | DAB→DATA, high | D0-7 = **DAB8..DAB15** | Q0-7 = **DATA0/..DATA7/** | **RDH XREG/** | dmem_U61.pin12 (WR XREG/) [& dmem_U38.pin11] |
| dmem_U39 | DATA→DAB, low | D0-7 = **DATA0/..DATA7/** | Q0-7 = **DAB0..DAB7** | **RD XREG/** (=dmem_U61.pin14) [& dmem_U41.pin1] | **WRL XREG/** |
| dmem_U41 | DATA→DAB, high | D0-7 = **DATA0/..DATA7/** | Q0-7 = **DAB8..DAB15** | dmem_U61.pin14 (RD XREG/) [& dmem_U39.pin1] | **WRH XREG/** [& dmem_U42.pin11] |
| dmem_U42 | bus-test loopback | D0-7 = **DATA7/..DATA0/** (bit-reversed) | Q0-7 = **DATA7/..DATA0/** (each Qn tied to same net as Dn) | **DPORT2/** | **WRH XREG/** [& dmem_U41.pin11] |

> ⚠ **dmem_U42** (bus-test): each `Dn` and `Qn` are the **same** DATA net, and the byte is **bit-reversed**
> (D0/Q0=DATA7/ … D7/Q7=DATA0/) — owner-confirmed correct (a loopback bus-test register), not a transcription
> flip. Bit mapping (DAB→DATA / DATA→DAB) within each '374 follows the verified pinout; bit-weight not asserted.

## 5.7 Offset read-back buffers `dmem_U48/U62` (74LS244) — OFST/ → DATA/ ✅
Let the SBC read the current offset. **`dmem_U48`** buffers `OFST0–7/`→`DATA0–7/` (enable **DPORT0/**);
**`dmem_U62`** buffers `OFST8–15/`→`DATA0–7/` (enable **DPORT1/**). Net effect: each `OFSTn/`→its `DATAn/`
(U48) / `OFST(8+n)/`→`DATAn/` (U62). Both enables (pins 1 & 19) tie to the one DPORT each.
| Buffer | inputs (A) ← OFST/ → outputs (Y) = DATA/ | enable |
|---|---|---|
| dmem_U48 | OFST6/→DATA6/, OFST1/→DATA1/, OFST2/→DATA2/, OFST3/→DATA3/, OFST4/→DATA4/, OFST5/→DATA5/, OFST0/→DATA0/, OFST7/→DATA7/ | **DPORT0/** |
| dmem_U62 | OFST11/→DATA3/, OFST10/→DATA2/, OFST9/→DATA1/, OFST14/→DATA6/, OFST15/→DATA7/, OFST8/→DATA0/, OFST13/→DATA5/, OFST12/→DATA4/ | **DPORT1/** |

---

# Net-group 2 (DMEM-resident) — I/O device decode `dmem_U52–U58`  ✅

**Source:** same DMEM hand-trace, sheet 2. Turns the SBC I/O cycle (`ADR0–7/`, `IORC//IOWC/`) into the XREG/DPORT
strobes + bus handshake. (The *other* device decode — the T&C `tc_U47/48/49` DAB-driver select named in plan §2 —
is on 060-02475, **not opened** → remains ⚪ for net-group 2 proper.) Inputs `ADR0–7/`, `IORC//IOWC/`, `RESET` ← SBC (§G3D).

## 2D.1 Address decoders `dmem_U55/U56/U57` (74LS138) ✅
Shared address: pin1(A)=**ADR0/**, pin2(B)=**ADR1/**, pin3(C)=**ADR2/** (all three '138s).
| Decoder | G2A\(4) | G2B\(5) | G1(6) | Outputs Y0(15)…Y7(7) |
|---|---|---|---|---|
| dmem_U55 (write) | dmem_U54.pin8 | **IOWC/** (=dmem_U52.pin10) | **ADR3/** | Y0=WRH XREG/, Y1=WRL XREG/, Y2=dmem_U58.pin13, Y3=nc, Y4=dmem_U53.pin10, Y5=dmem_U54.pin2, Y6=dmem_U53.pin5, Y7=dmem_U53.pin1 |
| dmem_U56 (read) | dmem_U54.pin8 | **IORC/** (=dmem_U52.pin9) | **ADR3/** | Y0=RDH XREG/, Y1=RDL XREG/, Y2=DPORT5/, Y3=DPORT4/, Y4=DPORT3/, Y5=DPORT2/, Y6=DPORT1/, Y7=DPORT0/ |
| dmem_U57 (host port) | dmem_U54.pin8 | **IORC/** (=dmem_U52.pin9) | dmem_U58.pin6 (=/ADR3) | Y6=HR/, Y7=HR1/; Y0–Y5 = nc |

> `DPORT0/`→U48 enable (§5.7); `DPORT1/`→U62 enable (§5.7); `DPORT2/`→U42 OE (§5.6); `DPORT3–5/`,`HR//HR1/`
> consumed off-board (⚪). `WRH/WRL/RDH/RDL XREG/` → X-register (§5.6). Decoder enable `dmem_U54.pin8` = §2D.2.

## 2D.2 Decode enable & handshake glue ✅
| Chip | Gate | Connections |
|---|---|---|
| dmem_U54 (74LS20) | U54A | pin1(1A)=+5V, pin2(1B)=dmem_U55.pin10(Y5), pin4(1C)=dmem_U53.pin11, pin5(1D)=dmem_U53.pin8(**HALT/**), pin6(1Y)=dmem_U53.pin9 |
| | U54B | pin9(2A)=ADR4/, pin10(2B)=ADR5/, pin12(2C)=ADR7/, pin13(2D)=ADR6/, pin8(2Y)=**decoder G2A\ enable** → dmem_U55.pin4, dmem_U56.pin4, dmem_U57.pin4, dmem_U58.pin11 |
| dmem_U52 (74LS03, OC) | g3 | pin9(3A)=**IORC/** [→U56.5/U57.5], pin10(3B)=**IOWC/** [→U55.5], pin8(3Y)=+5V(1K pull-up) & pin13 |
| | g4 | pin12(4A)=dmem_U58.pin10, pin13(4B)=pin8, pin11(4Y)=**XACK/** |
| dmem_U53 (74LS00) | U53A | pin1=dmem_U55.pin7(Y7), pin2=dmem_U53.pin6, pin3=dmem_U53.pin12 & pin4 |
| | U53B | pin4=dmem_U53.pin3 & pin12, pin5=dmem_U55.pin9(Y6), pin6=dmem_U53.pin2 |
| | U53C | pin8(3Y)=dmem_U54.pin5 & **HALT/**, pin9(3A)=dmem_U54.pin6, pin10(3B)=dmem_U55.pin11(Y4) |
| | U53D | pin11(4Y)=dmem_U54.pin4, pin12(4A)=dmem_U53.pin3 & pin4, pin13(4B)=**RESET** (not RESET/) |
| dmem_U58 (74S04) | U58C | pin5(3A)=**ADR3/** [&U55.6/U56.6], pin6(3Y)=dmem_U57.pin6 (=/ADR3) |
| | U58D | pin8(4Y)=dmem_U43.pin3, pin9(4A)=GND [& dmem_U43.pin9] (CAS-enable inverter; §6D) |
| | U58E | pin10(5Y)=dmem_U52.pin12, pin11(5A)=dmem_U54.pin8 [& U55/56/57.pin4] |
| | U58F | pin12(6Y)=**CPC CLR**, pin13(6A)=dmem_U55.pin13(Y2) |
| | U58B | **DEAD** (pin3=dmem_U61.pin16, pin4=dmem_U60.pin11 unpopulated) — §6D |

> Generates `WRH/WRL/RDH/RDL XREG/`, `DPORT0–5/`, `HR//HR1/`, `XACK/`, `HALT/`, `CPC CLR`. This is the SBC↔DMEM
> I/O decode; SM ch.3/ch.5 (host interface). `dmem_U52` is open-collector (XACK/ wired-AND).

---

# Net-group 6 (DMEM-resident) — RAS/CAS/ROW-SEL strobe generator  ✅

**Source:** same DMEM hand-trace, sheet 2. The DL6308 delay line sequences the DRAM strobes. **LIVE path =
`dmem_U59` (DL6308), `dmem_U46A` (74S74), `dmem_U44` (74S00), `dmem_U45` (74S08), `dmem_U43` (74S10), `dmem_U58D`,
`dmem_U61` buffers.** An **unpopulated alternate generator (`dmem_U47` 74S74, `dmem_U60` 74S02, and `dmem_U46B`)**
shares these net names — **ignore for modeling**; its endpoints are tagged `[dead]` in the source txt and below.
Strobe waveforms are owner-confirmed in **fig-3.3**.

## 6D.1 Delay sequencer `dmem_U59` (DL6308, 5-tap, 30 ns/tap) ✅
| Pin (tap) | Net |
|---|---|
| pin1 (IN) | dmem_U46A.pin5 (1Q) & dmem_U45.pin10 |
| pin12 (TAP1 30ns) | dmem_U45.pin13 & dmem_U45.pin9 |
| pin4 (TAP2 60ns) | dmem_U45.pin12 & dmem_U44.pin12 |
| pin6 (TAP4 120ns) | dmem_U46A.pin4 (1PRE\) |
| pin8 (TAP5 150ns) | dmem_U44.pin4 & dmem_U44.pin5 |
| pin10 (TAP3 90ns) | n/c |

## 6D.2 Strobe-forming logic ✅
| Chip | Gate | Net |
|---|---|---|
| dmem_U46A (74S74) | — | pin1(1CLR\)=+5V, pin2(1D)=GND, pin3(1CLK)=dmem_U61.pin7 (**DAB RSTB**, buffered) & dmem_U44.pin10 [& dead U60.8], pin4(1PRE\)=dmem_U59.pin6 (TAP4), pin5(1Q)=dmem_U59.pin1 & dmem_U45.pin10, pin6(1Q\)=nc |
| dmem_U44 (74S00) | U44A | pin4(2A)=pin5 & dmem_U59.pin8 (TAP5), pin5(2B)=pin4 & dmem_U59.pin8, pin6(2Y)=dmem_U44.pin9 (= inv TAP5) |
| | U44B | pin9(3A)=dmem_U44.pin6, pin10(3B)=dmem_U46A.pin3 & dmem_U61.pin7 [& dead U60.8], pin8(3Y)=dmem_U44.pin13 |
| | U44C | pin12(4A)=dmem_U45.pin12 & dmem_U59.pin4 (TAP2), pin13(4B)=dmem_U44.pin8, pin11(4Y)=dmem_U43.pin11 & dmem_U43.pin4 [& dead U60.1] |
| dmem_U45 (74S08) | U45A | pin9(3A)=pin13 & dmem_U59.pin12 (TAP1), pin10(3B)=dmem_U59.pin1 & dmem_U46A.pin5, pin8(3Y)=**RAS/** (→33R) [& dead U47.2/U47.9/U60.9] |
| | U45B | pin12(4A)=dmem_U44.pin12 & dmem_U59.pin4 (TAP2), pin13(4B)=pin9 & dmem_U59.pin12 (TAP1), pin11(4Y)=**ROW SEL** [& dead U60.12/U47.5] |
| dmem_U43 (74S10) | U43A | pin3(2A)=dmem_U58.pin8, pin4(2B)=pin11 & dmem_U44.pin11 [& dead U60.1], pin5(2C)=pin10 & dmem_U61.pin16 & dmem_U58.pin3, pin6(2Y)=**CAS0/** (→33R) |
| | U43B | pin9(3A)=GND & dmem_U58.pin9, pin10(3B)=pin5 & dmem_U61.pin16 & dmem_U58.pin3, pin11(3C)=pin4 & dmem_U44.pin11 [& dead U60.1], pin8(3Y)=**CAS1/** (→33R) — **permanently inactive** (3A grounded → unpopulated bank) |

## 6D.3 `dmem_U61` (74LS244) strobe/clock buffers ✅
DMEM-resident sections (sheet 2) + the three sheet-1 sections:
| Section | In | Out |
|---|---|---|
| U61B (drawn "U61G") | pin4 = **MEMAC** | pin16 → dmem_U58.pin3 & dmem_U43.pin5 & dmem_U43.pin10 (CAS-gate: "CAS falls only when MEMAC high") |
| U61F | pin13 = **DAB RSTB** | pin7 → dmem_U46A.pin3 & dmem_U44.pin10 [& dead U60.8]; (pin1/pin19 G\ = GND) |
| U61E (sheet 1) | pin6 = **RD XREG/** | pin14 → dmem_U39.pin1 & dmem_U41.pin1 (XREG read OE) |
| U61G-sec (sheet 1) | pin8 = **WR XREG/** | pin12 → dmem_U38.pin11 & dmem_U40.pin11 (XREG write CP) |
| U61H (sheet 1) | pin11 = **MEMW/** | pin9 → **WR/** (→33R → all DRAM pin3) |
| **U61C** | pin17 = MC | pin3 → **DEAD** (drives only unpopulated U47/U46B) |
| **U61D** | pin15 = MS1 | pin5 → **DEAD** (drives only unpopulated U60) |

> **Strobe timing (fig-3.3, owner-confirmed):** RAS/ low MS2–6; ROW SEL row(H) MS0–2 / col(L) MS3–7 / H MS8;
> CAS0/ low MS4–8 (**falls only when MEMAC high** — gated through dmem_U61B→dmem_U43A); WR/ = buffered MEMW/.
> Per SM ch.3 the DMEM strobes are sequenced by the DL6308 from T&C `MEMAC`/`DABSTB`/`MEMR`. CAS1/ (the
> unpopulated bank) is hard-disabled. `MC`, `MS1`, `MEMAC`, `DAB RSTB`, `MEMW/` origins = T&C (§G3D).

---

# GAPS / QUESTIONS FOR OWNER

> Per Ground Rule 3 these are flagged, not guessed. The ARU-internal gaps are now closed by the owner's expanded
> trace; what remains is (a) two items for owner confirmation and (b) the genuinely cross-board signal origins.

### §G1 — ARU multiplier front-end — ✅ RESOLVED (owner expanded the trace 2026-06-27)
Now transcribed in net-group **4F** (regfile, dual-rank shifter, Booth NAND array, M0/M1 selects, front-end
adders, carry chain, Σ→product-register feed). Internal-consistency verified.

### §G2 — CSIGN / subtract-control origin — ✅ RESOLVED to the ARU boundary
Traced in **§4F.8**: `CSIGN/` enters at aru_U2.pin11/pin13; aru_U2 generates both sub-ctrl rails and the adder
carry-in. `CSIGN/` itself is a WCS/T&C signal (see §G3).

### §G3 — Cross-board signal origins (T&C / WCS) — ⚪ OPEN (next net-groups)
These are wired/consumed on the ARU but **generated on T&C**: `RDRREG/`, `XFER CK`, `ARUCK`, `ARUCKE/`, `ZERO/`,
`DAB WSTB/`, `S0`, `S1`, the regfile addresses `RA0/RA1/WA0/WA1`, the Booth selects `M0//M1/`, and `CSIGN/`.
Resolved by net-groups 2/3/6 (060-02475 + figs 3.2/3.4). `SAT` is generated **on the ARU** (aru_U42, §4.5) ✅.

### §G3D — DMEM cross-board origins + unpopulated structure
**Consumed on DMEM, generated off-board (⚪ origins, next net-groups on 060-02475 / SBC):**
- *From the SBC I/O bus:* `ADR0–7/`, `IORC/`, `IOWC/`, `RESET` (the unslashed CPC count-clock / handshake net —
  its source/role beyond the pin is **not traced**, §5.1), `RD XREG/`, `WR XREG/` (host read/write of the XREG,
  buffered by dmem_U61E/G).
- *From T&C:* `MEMAC`, `MEMW/`, `DAB RSTB`, `MC`, `MS1`, and the microword offset `OFST0–15/`.
- *Generated **on** the DMEM* (not gaps): the `WRH/WRL/RDH/RDL XREG/` + `DPORT0–5/` strobes (§2D decoders),
  `CPC CLR` (dmem_U58F), `XACK/`/`HALT/`/`HR//HR1/` (handshake), and `RAS//CAS0//ROW SEL/WR/` (§6D).

**Unpopulated structure (this product rev — owner-confirmed; faithfully carried from the source txt):**
1. **`dmem_U1–U16` (lower DRAM bank, CAS1/) NOT populated** → the delay memory is **one bank, 64K×16**
   (`dmem_U20–U35`, CAS0/). `CAS1/` is hard-disabled (dmem_U43B pin9 grounded). Consistent with `4164.v`
   (lists only U20–U35). Bears on memory depth = **64K words** (cf. older "128K/2-bank" notes — superseded).
2. **Unpopulated alternate RAS/CAS generator: `dmem_U47` (74S74), `dmem_U60` (74S02), and `dmem_U46B`.** These
   share net names with the live generator but drive/are-driven-by nothing populated. **Ignore for modeling;**
   the live path is dmem_U43/U44/U45/**U46A**/U59 (§6D). Every dead endpoint is tagged `[dead]` in §6D and in
   the source txt. (`dmem_U58B`, `dmem_U61C`, `dmem_U61D` are likewise dead — they feed only U47/U60.)

### §G4 — Not-depicted power/unused pins — owner directive: assume correctly connected
Owner: Vcc/GND and a few outputs (e.g. aru_U23.pin9 top carry-out, aru_U45-49 RCO) are left off the drawing for
tidiness; **assume they are wired correctly** (the unit functions). Not treated as gaps.

### §Q — Owner-confirmed (was: two open items) ✅ RESOLVED 2026-06-27
1. **aru_U25 A-inputs = U26** (not U28) — owner fixed in the pinout txt; netlist §4F.7 updated. ✅
2. **SR19 → aru_U53.pin9 AND pin12** (both tied) — owner confirmed (top-bit replication, not a typo); §4F.4 updated. ✅
3. **aru_U54 M-rail split** confirmed: pin10(5Y)=M1→{U27,U28,U40,U50,U52}; pin12(6Y)=M0→{U14,U26,U41,U51,U53}; §4F.5/4F.6 updated. ✅

> Final internal-consistency pass (after owner edits): **no remaining errors** — impossible-pins/missing-pins/bus
> single-driver all clean; symmetry clean except benign net-name-style (U5 sub-ctrl rail) and one non-exhaustive
> multi-point enumeration (U23.pin11 on the `_aru_topB` net). Automated schematic re-read was unreliable and was
> NOT used for corrections (see memory `224xl-schematic-autoread-unreliable`).

---

# Conventions
- **Net names:** owner-trace names verbatim (`PPn`,`ACn`,`DABn`,`SAT`,`B-IN`, sub-ctrl rail). My own names for
  un-named internal nets carry a leading `_` (`_aru_sumN`, `_aru_c4_NN`, `_aru_cin`, `_aru_u42_inA`).
- **Pin refs:** `board_Uxx.pinN` with the role in parens, role taken from the verified pinout in
  `224XL_partspec_verification.md`.
- **Provenance:** every net in net-group 4 = owner pin trace `224XL ARU pinouts from 060-01318.txt`, re-keyed to
  the verified pinouts. Confidence ✅ unless marked.
