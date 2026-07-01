# 224XL emulator — asserted vs emergent accounting (2026-06-30)

Full audit of every subsystem in the model against the owner directive *"emulate the whole netlist from MC;
nothing asserted."* Status legend:

- **EMERGENT-GATE** — modeled at gate/register level from the transcribed netlist; behavior emerges from the
  wiring. Validated against goldens/figures.
- **EMERGENT-TIMING** — the element's CLOCK/STROBE timing now emerges from MC (via `tc_clock`), even if its
  data VALUE is still computed behaviorally.
- **BEHAVIORAL** — value computed by a Python abstraction that is netlist-grounded but NOT gate-level (e.g.
  `addr = CPC+ofst+1`, `res = sat16(ACC>>3)`). Structurally faithful, not structurally emergent.
- **ASSERTED** — a value/convention chosen or read from a figure/spec, not derived from the wiring.
- **OMITTED** — not modeled.

> The point of this doc: be honest about where the model still *asserts*. The clock/state/strobe generation
> and the MAC capture-vs-clear timing are now EMERGENT from MC (the big change this session). Most of the
> DATAPATH VALUE computation (adders, saturation, DMEM DRAM, FPC, DAB resolution) is still BEHAVIORAL — the
> Phase-5/6 gate-level build was gated off by the milestone and never done.

## 1. T&C clock / state / strobe generation (§6T) — NOW EMERGENT (`tools/tc_clock.py`)
| element | chips | status | validated vs | notes |
|---|---|---|---|---|
| MC (master clock) | tc_U40.pin11 | **ASSERTED (as input)** | — | MC is TICKED as the root clock. The PLL that makes it (tc_U26 VCO + tc_U41 ÷15 + tc_U27 phase det) is **OMITTED** — owner-omitted, MC is the model's input. Fine per §6T.1. |
| MS0–8 | tc_U56 (÷9) + tc_U39 (shift) | **EMERGENT-GATE** | fig-3.2 (all 9 ✔) | **MS4 is an ACTIVE-LOW net** (=tc_U56 QD) — finding. |
| ARUCK / ARUCKE / ARUCKE/ | tc_U25 FF2, tc_U40, tc_U38 | **EMERGENT-GATE** | fig-3.2 ARU CK ✔ | ARUCK rises ~0.3 MS into slot (rise-lag modeled). |
| AS0 / AS0/ / AS1/ | tc_U23 (74LS175) | **EMERGENT-GATE** | fig-3.2 AS0 ✔ | |
| AS1 / AS2 (full sequencing) | tc_U24, tc_U38 (S0/S1 seq) | **PARTIAL / OMITTED** | — | AS1/ comes from U23; the full AS1/AS2 sequencing via tc_U24/U38 is **§G3T off-sheet — not modeled**. Only AS0 is used by the strobes. |
| DAB WSTB/ | tc_U37 (=inv MS7) | **EMERGENT-GATE** | fig-3.3 ✔ | |
| DAB RSTB / RSTB/ | tc_U20 FF1 (JK) | **EMERGENT-GATE** | fig-3.3 ✔ | J=MS1,K=MS8. |
| XFER CK | tc_U36 = NAND(AS0,XFER,ARUCKE/) | **EMERGENT-GATE** | fig-3.4 (⊆ ZERO/, narrower) ✔ | **tc_U25.pin9 = ARUCKE/, NOT a constant** — corrects the earlier XFER-gate probe. |
| ZERO/ | tc_U48 = NAND(ZEROgate,AS0) | **EMERGENT-GATE** | fig-3.4 ✔ | |
| tcCLKB | tc_U37 (=inv MC) | **EMERGENT-GATE** | — | strobe-FF clock. |
| GSTB//WSTB//CS (WCS access) | tc_U21/U22 | **OMITTED** | — | SBC↔WCS access strobes; not in the audio free-run path. |

## 2. WCS microsequencer + microword field regs (§3)
| element | chips | status | notes |
|---|---|---|---|
| WCS PC | tc_U14/U1 (74LS163 ×2, 7-bit) | **BEHAVIORAL** | modeled as a Python modulus counter clocked at RESET; clock source (DAB RSTB/) is emergent. Counter itself not gate-level. |
| **PC modulus (program length)** | RESET = tc_U34 AND(tcWR,OFST3/) | **ASSERTED = 100 — netlist CONTRADICTS** | ⚠ Investigated 2026-06-30: RESET = AND(tcWR, OFST3/=MI3) fires FIRST at **step 4** under BOTH polarities (same-step and ±1 skew) on the CONCERT image — implying a 5-step program, which is absurd. So the RESET decode as transcribed does NOT reproduce "reset at 99"; the PC modulus **cannot be derived from the current netlist trace**. Remains asserted at 100 (SM). This is a concrete GAP to resolve (RESET-path trace error, or the offset/MI3 mapping, or the physical unit). See §PC-modulus below. |
| offset latch → OFST0-15/ | tc_U45/U31 (74F374) | **BEHAVIORAL** | `ofst = lanes 0/1`; the 374 scramble/complement is folded into `addr = CPC−OFST`, not modeled per-pin. |
| control-field regs (MEMAC/WA/RA/PROT/XFER/ZERO/cmag) | tc_U17/U18/U4/U5 (163 as load-regs), tc_U19 (377) | **BEHAVIORAL** | `decode(l2,l3)`; fields extracted by mask, not by the load-register chain. |
| coeff serializers M0//M1/ | tc_U11/U10 (74195) | **BEHAVIORAL (folded into Booth)** | the even/odd Booth streams are consumed by the gate Booth array directly, not serialized by modeled 74195s. |
| **CSIGN generator** | tc_U20 FF2 (74S112 JK) | **RESOLVED → FAITHFUL** | Traced 2026-06-30: J = AS0·MI23, K = AS0·/MI23 (via tc_U18.QD→tc_U19.Q4→tc_U34 g3/g4). J,K are NEVER both 1 → NOT a toggle; it's a SET/RESET = **registered pass-through of MI23 during AS0** with no cross-instruction deferral vs the multiply. Modeled explicitly and confirmed **byte-identical** to the direct `csign = MI23` bit on CONCERT (which POST already validates). The current model is faithful. |
| PROT (MI22) | tc_U18.QC | **OMITTED (effect)** | bit decoded; downstream effect untraced in the netlist → not modeled. |

### §PC-modulus — the RESET-decode contradiction (unresolved gap)
The WCS PC (tc_U14/U1) is a 7-bit count-only counter sync-cleared by RESET; the program length = where RESET
fires. RESET = `tc_U34` g2 = **AND(tcWR, OFST3/)** (sheet-2 pinout), where tcWR = the I/O-step decode
(MEMAC=0,MI16=1) and OFST3/ = `tc_U45.Q1` = the latched MI3 (=l0 bit 3). Evaluated on the CONCERT 0x4000
image, RESET fires FIRST at **step 4** — under the direct polarity (tcWR·MI3), the inverted polarity
(tcWR·/MI3 → first at step 26), AND a ±1 latch skew (still step 4). None gives "reset at count 99" (step 99
is an I/O step with MI3=0). A 4–5-step program is absurd for a reverb. So one of these is wrong: (a) the
transcribed RESET path (a gate/polarity in tc_U33/U34/U19 or the RESET→RESET/→RESETD/ pipeline), (b) the
OFST/MI3 mapping, or (c) the assumption that the 0x4000 image runs from step 0. **Until resolved, the PC
modulus is ASSERTED = 100 (SM statement), parameterized.** This is a real, specific gap — likely needs a
re-trace of the RESET path or the physical unit. (It also bears on the Phase-2.0 100-vs-128 question and the
per-frame-modulated taps 107–119.)

## 3. ARU datapath (§4/§4F)
| element | chips | status | validated | notes |
|---|---|---|---|---|
| Booth front-end (shifter/NAND array/carry chain) | aru_U3/4/14/26/27/28/40/41/50-53 + 283s | **EMERGENT-GATE** | 20/20 goldens | `aru_booth.comb_array` — the literal gates. |
| MAC **timing** (accumulate / XFER capture / ZERO clear) | 74LS163 acc + 74F374 res | **EMERGENT-TIMING** | reproduces deferred MAC 300/300 | `mac_step_subslot`: sync-clear + edge-load on the EMERGENT ZERO//XFER-CK/ARUCKE/ strobes. Capture-before-clear EMERGES. |
| accumulator adder chain | aru_U19/24/25/38/39 (283×5) | **BEHAVIORAL** | — | value = `sat20(ACC+product)`; the 5-adder ripple not modeled. |
| sat-mux + saturation + subtract-XOR | aru_U…157×5, U42 XOR, U2 clamp, 86×5 | **BEHAVIORAL** | — | value = `res_from_acc = sat16((ACC+4)>>3)`. Gate back-end (Phase 5) **not built** (milestone-gated). |
| result register value tap (PP3..18) | aru_U43/U44 (374) | **BEHAVIORAL** | — | 16-bit `>>3` tap folded into res_from_acc. |
| regfile (4×16) | aru_U…LS670 | **BEHAVIORAL** | — | Python `R[WA] <- DAB @ DAB WSTB`. |

## 4. DMEM (§5/§6D)
| element | chips | status | notes |
|---|---|---|---|
| CPC counter | dmem_U51/U65 (74LS393) | **BEHAVIORAL** | Python counter, +1/sample at RESET. |
| offset adders / row-col mux | dmem_283 / 157 | **BEHAVIORAL** | `addr = CPC + ofst + 1`. |
| DRAM array (4164) + DL6308 RAS/CAS seq | dmem_U59 DL6308 + 4164s | **BEHAVIORAL (dict) / RAS-CAS OMITTED** | delay memory = Python dict; read-before-write = dict old-then-write. Gate RAS/CAS/refresh **deliberately abstracted** (AC3 — doesn't change audio VALUES, only refresh margins). |

## 5. DAB bus / device decode / FPC / I-O
| element | status | notes |
|---|---|---|
| DAB shared bus | **BEHAVIORAL** | Python value, hold-last, one driver per §2T decode. NOT a resolved tri-state bus (PM-1 gate resolution not built — milestone-gated). |
| §2T device decode (MEMR/MEMW/RD AD/WR DA/RDRREG/RD XREG/SDAA-D) | **BEHAVIORAL** | `device_decode()`, netlist-grounded gate booleans but coded as Python. |
| FPC float↔fixed codec | **BEHAVIORAL / default OFF** | `fpc_input/output_*`; full gate FPC (Phase 4: SAR/IGA/OGA/GSA/double-buffer/BUSY) **not built**. |
| A/D-D/A boundary (RD AD/ inject, WR DA/ capture) | **BEHAVIORAL** | fixed-point I/O at the decoded strobes. |

## 6. Verification / boot
| element | status | notes |
|---|---|---|
| 8080 core (boot/POST driver) | **EMERGENT (verified core)** | kosarev I8080, plan-019 verified. |
| POST single-step path | **BEHAVIORAL MAC (atomic `_multiply`)** | ⚠ POST runs on `single_step`/`_multiply` (atomic, clears ACC each call), NOT the sub-slot MAC. So POST validates the multiply VALUE + DMEM, but does NOT yet exercise the emergent sub-slot MAC timing. Making single_step run the 9-slot emergent MC clock is a further step. |
| reverb metric harness | **N/A (measurement)** | `reverb_metrics` — measures emitted output only; validated on controls + real IRs. |

## Bottom line
**Emergent now:** the entire T&C clock/state/strobe generation (MS/AS/ARUCK/ARUCKE/DAB-RSTB/DAB-WSTB//XFER-CK/
ZERO/) from MC, validated vs fig-3.2/3.3/3.4; and the MAC capture-vs-clear timing (163 sync-clear + 374 load).
**Still asserted/behavioral:** the WHOLE datapath VALUE computation (adder chain, saturation, regfile, CPC,
offset arithmetic, DMEM DRAM, DAB tri-state resolution, device decode, FPC), the PC modulus, the CSIGN JK,
and PROT's effect. **The milestone's "timing is not the lever" conclusion is now on firmer ground** — the
clock/strobe timing AND the MAC capture timing emerge correctly from MC and still produce the same output —
so the missing tail is confirmed to live in the datapath-value / microword-semantics domain, not the clock.
Next faithful steps (in priority for the reverb question): (a) resolve the PC modulus + CSIGN JK from the
wiring; (b) run POST on the emergent sub-slot MAC (retire `_multiply`); (c) gate-level DAB resolution +
device decode; (d) gate ARU back-end (Phase 5) only if an audio discrepancy appears.
