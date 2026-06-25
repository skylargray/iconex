# 224XL — Signature Analysis Validation Plan (the datapath-timing endgame)

> **START HERE for the 224XL reconstruction (supersedes the over-unity framing).** Session 8 (2026-06-24)
> proved the over-unity λ was a **red herring**, fully **confirmed the microword decode** (incl. owner
> schematic traces), fixed the multiply scale, and **localized the one remaining bug to ARU datapath
> TIMING** — the static-WCS reverb tank is dead (CONCERT impulse → silence) even though every decoded
> field is correct. This plan uses the manual's **§5.7 Signature Analysis** as an exact per-node hardware
> oracle to pinpoint *where* the datapath model diverges from the real ARU, then fix it.

---

## 0. TL;DR

The audio enters CONCERT correctly (input → predelay buffer), is processed through the all-pass diffusion
(result-register/RDRREG feedback), **but the diffused signal never gets written into the DMEM long-delay
lines**, so the recirculating tank never fills and the impulse dies. Decode is confirmed correct, so this is a
**datapath/pipeline-timing** problem. The principled fix: build the exact 3-state (AS0/AS1/AS2) ARU model and
**validate it node-by-node against the manual's signature tables** — the first divergent node is the bug.

## 1. CONFIRMED — do NOT re-investigate (Session 8 + owner schematic traces)

Authoritative decode (all schematic-confirmed). 32-bit microword = 4 stored bytes `l0,l1,l2,l3` = MI0-7,
MI8-15, MI16-23, MI24-31. WCS byte for step S, lane L is at `0x4000 + S*4 + L`; lane L bit b = MI(8L+b)
(DATA0↔MI24 etc., AM8304 non-inverting).

| field | bits | polarity / notes |
|---|---|---|
| offset OFST0-15 | MI0-15 (l0,l1) | `offset = ~(l1<<8 | l0) & 0xFFFF` (l0,l1 inverted) |
| DMEM read/write | **MI16** = l2.b0 | read iff MI16=1 (`read_bit=1`); **inv_l2=False** (l2 used raw) |
| MEMAC (DMEM-op) | **MI17** = l2.b1 | DRAM/CAS only when MI17=1 (manual §3.6). MI17=0&MI16=0 ⇒ idle (Y0=NC) |
| WA0,WA1 | MI18,19 = l2.b2,b3 | write reg addr (3 = scratch/pass-through) |
| RA0,RA1 | MI20,21 = l2.b4,b5 | read reg addr |
| PROT | MI22 = l2.b6 | datapath-irrelevant |
| CSIGN | MI23 = l2.b7 | coefficient sign |
| **XFER** | **MI24 = l3.b0** | **inv_l3=True**: XFER=`~l3.b0`. (U4 S163 QA→U19 LS577 D14→Q15→XFER, active-high) |
| **ZERO** | **MI25 = l3.b1** | `~l3.b1`, **gated by AS0** (U4 QB→U19→U48D ¼S00 NAND(·,AS0)→ZERO/) |
| **C0-C5 coeff** | **MI26-31 = l3.b2-7** | `cmag = (~l3>>2)&0x3F` (active-low C0/-C5/; U4 QC/QD→C0/C1, U5→C2-5) |

- **inv_l3=True is required & consistent** (NOP/unused step stored 0xFF ⇒ all controls off ⇒ XFER=~l3.b0).
- **Device decode:** MI17=1 → DMEM (MI16=1 read / MI16=0 write, data=RES). MI17=0&MI16=1 → sub-decoder by
  (MI13,MI12) from `~l1` bits 4,5: 01=RDRREG/ (result reg→DAB feedback), 11=RD AD/ (audio in), 10=RD XREG/,
  00=idle. MI17=0&MI16=0 → idle (DAB undriven). **sub3 really is RD-AD (input)** — CONCERT input = ONLY step
  76 (the base-invariant fingerprint offset bit15 & low14=0x3FFF). (sub3=RDRREG was tested and REFUTED.)
- **Multiply scale = /32, NOT /64:** `prod = (x<<3)*cs >> 5` (net per-step gain = cs/32). Confirmed by the
  ADD'L MULT diagnostic (§5.3.2 tests ×1 and ×5/4 ⇒ coeff 32 = ×1.0, 40 = ×1.25 — only at /32). The closer
  `l3=0x7C` → cs=32 → gain 1.0. **APPLIED to `tools/aru_datapath.py`** (`prod>>5` + exact MAC pipeline `pend`).
  ⚠️ Still TODO in C++: `224xl.hpp` `kProdShift` 6→5 and update `mult_vectors_test.cpp` (it encoded /64).
- **MAC pipeline (acc_latch):** the MAC result is available only at AS0 of the NEXT cycle; XFER loads RES and
  ZERO clears at that instant (§3.7). Implemented as a 1-step deferred product.
- **FPC I/O is 16-bit** (not 12-bit): instantaneous floating-point conv (§3.8/§3.9) — analog gain ×1..8 ×
  digital shift 4..1 always nets ×16 ⇒ full-scale input = ±32768 on the DAB. ⚠️ Fix `224xl.hpp` `floatToAru`.
- **Topology (manual ch.4 Fig 4.1):** Input → HF Bandwidth → Predelay → **Diffusion (all-pass)** → **Reverb
  tank** (LF/Mid/Treble Decay + Chorus) → Depth → Fine Predelay → Outputs; preechoes bypass to outputs.
  **Chorus modulation CAN be off** — the static-WCS tank MUST work without modulation (owner-confirmed).
- **Ground-truth diagnostic bytes** verified by running the firmware builder (`boot_xl.boot`; push 0xFFFF,
  PC=0x0F2C, step to RET; ZERO patches `[0x41F8]=01,[0x41F9]=00,[0x4130]=01,[0x4131]=40`). They match the
  reverse-engineered table; the Max-Delay program reproduces a **unity +0.969 echo** (delay-line recirc works).

## 2. THE BUG (precise, Session-8 trace)

CONCERT impulse → input lands in **1 DMEM cell** (predelay buffer, value ≈−3750, held ~1.5s, read back at the
comb delays) → processed through the all-pass diffusion (XFER→RES, sub1 RDRREG RES→register, re-MAC) → **but
the diffused result never reaches a DMEM long-delay write.** Step-trace at the echo (n=18230): s4 mult →
ACC=−56250; **s24 (DMEM-WRITE) writes RES=0 (stale)** because the XFER that captures the result fires at **s25**
(one step later, RES=−7032) and there are **45 XFER steps but only 10 DMEM-writes**, so RES is overwritten ~4×
between writes; at sample end all 4 registers are 0. Result: tank empty after 20s (0 of 16256 cells).

**RULED OUT** (none revive it): coefficient bits/inversion, /32-vs-/64 scale, MAC-pipeline phase (deferred vs
immediate vs acc_latch), XFER-gating the DMEM-write, idle/sub DAB source (=0/=hold/=DMEM/=RES), injection
point/count, sub3=RDRREG, the live modulation. Power iteration is unreliable here (frozen-cell λ=1.0 +
random-start collapse, scale-invariant) — use the time-domain impulse.

**New timing facts that point at sub-microinstruction detail:** ZERO gated to AS0; XFER delivered as a gated
CLOCK (XFER CK), not a static level; the multiply is serial over AS0/AS1/AS2 with a partial-product register
(U10/U11/U12, clk ARUCK) and a separate accumulator (U45-49, clk ARUCKE/). The current model is
microinstruction-granular and may mis-time the XFER/DMEM-write interaction.

## 3. THE PLAN

### Phase A — exact 3-state (AS0/AS1/AS2) ARU model
Build a cycle-accurate ARU per Manual §3.7 (serial multiply), so node values exist at every ARUCK/ARUCKE/XFER-CK
edge (required for Phase B, and possibly the fix itself):
1. Per microinstruction = 3 ARU states. **AS0**: load register file `R[RA]` into the dual-rank shift register
   (U3/U4/U15-18); ZERO/ and XFER CK act here. **AS0/AS1/AS2**: each state does a double shift-add (2 coeff
   bits/state via M0//M1 NAND layer U14/U26-28/U40/U41/U50-53), accumulating partial products into the
   **partial-product register U10/U11/U12** (clk ARUCK, no saturation).
2. The complete product is added to the **accumulator** (U45-49, clk ARUCKE/, the only saturating stage, rails
   ±2^18) — the result is available at AS0 of the NEXT microinstruction.
3. **Result register** RES (U43/U44, clk XFER CK) ← `PP[3..18]` = ACC>>3; OE = RDRREG/. DMEM `DIN` = RES, timed
   by XFER CK (Fig 3.3 note). CSIGN two's-complement subtract; sat-mux substitutes ±2^18.
4. Validate against the ADD'L MULT vectors (must still pass) and the Max-Delay unity echo.
5. **Test the dead tank:** run the CONCERT impulse on the 3-state model. The finer timing may itself fix the
   XFER↔DMEM-write alignment. If it sustains → measure RT60, skip to Phase C.

### Phase B — signature-analysis validation (the oracle)
1. **Implement the HP-5004A signature algorithm** (16-bit LFSR):
   - Polynomial **X^16 + X^12 + X^9 + X^7 + 1** (feedback taps at bits 16,12,9,7, 1-indexed). Per CLOCK edge:
     `fb = data XOR bit16 XOR bit12 XOR bit9 XOR bit7`; shift the register up one; insert `fb` at bit 1.
   - Display: 16-bit value → 4 nibbles (MSB first) → character set **`0123456789ACFHPU`** (nibble 0..15).
   - **VERIFY the exact polynomial / bit-order / char-map** — conventions vary; the calibration in step 3 is
     the proof.
2. **Boot Diagnostic Program 3 (ARU SIGNAT)** in the emulator. Find its handler from the diag-menu dispatch
   (SBC1 `0x032D` → `JP 0x11BE` over the table at `0x0330`; item 3 → handler) the same way Session 8 found
   Max-Delay (item 8 → `0x0EF4` → builder `0x0F2C`). Run it (push return / set PC / step to RET) and capture
   the WCS + run state it sets up. (Diag 3 is implemented in v8.2.1; "not in V8.0" per Table 5.1.)
3. **CALIBRATE the algorithm + clock count** using the manual's reference signatures, which encode N (the
   number of CLOCK edges between START and STOP): clocking all-1s for N edges must yield the **+5V** signature;
   all-0s must yield **0000** (GROUND). Solve for N from the +5V signature for each setup, and confirm it
   matches the Diag-3 run length × (ARUCK edges per microinstruction = 3 for ARU).
4. **Compute node signatures** from the model at ARU-state granularity, gated START→STOP, clocked on the
   setup's CLOCK, and compare to the §5.7 tables. **The first node whose signature mismatches = the exact
   place the datapath model diverges from the hardware.** Prioritize the ARU **feedback** config (it exercises
   the result-register recirculation = our broken link) and the result register (U43/U44 = DAB0-15),
   accumulator (U45-49), partial-product register (U10/U11/U12).

### Phase C — fix + verify
- Fix the divergence the signatures expose; re-validate all signatures green.
- Re-run the CONCERT impulse → confirm a clean single-exponential EDC, **RT60 ≈ 20 s** (P85 reference IR
  `IR/Lexicon 224XL/P85 - 20.0 Seconds A.wav`), HF<LF, decay from the program's in-loop damping coeffs.
- Mirror the corrected datapath to `libs/sgdsp/include/sgdsp/reverb/224xl.hpp` (incl. **/32 scale**: kProdShift
  6→5; **16-bit FPC** floatToAru; the 3-state timing / acc_latch), regen the golden
  (`python tools/export_golden_224.py 0x01`), and re-green the gates (ctest 2/2; diff_harness DIFF PASSED;
  mult_vectors_test ALL PASS after updating its /32 vectors).

## 4. Signature-analysis SETUP conditions (Manual §5.7, V8.2.1)

| module | schematic | START | STOP | CLOCK | +5V sig | GROUND |
|---|---|---|---|---|---|---|
| T&C | 060-02475 | RESET, U19 pin 9 | RESET, U19 pin 9 | DAB RSTB/, U20 pin 6 | FP54 | 0000 |
| ARU (no feedback) | 060-01318 | RESET/, ext. card pin 16 | XFERCK, U43 pin 11 | ARUCK, U10 pin 11 | 29F3 | 0000 |
| ARU (feedback) | 060-01318 | RESET/, ext. card pin 16 | RESET/, ext. card pin 16 | ARUCK, U10 pin 11 | 3696 | 0000 |
| DMEM | 060-02512 | MSB of CPC, U65 pin 8 | MSB of CPC, U65 pin 8 | RESET/, U58A pin 1 | 826P | 0000 |

(Control head displays **E0A** during Diag 3. DMEM setup lifts U65 pin 13, jumpers to U65 pin 1.) The per-pin
signature value tables follow §5.7 in `docs/reference/224/Lexicon-224X-Service-Manual.md`.

## 5. Tools & references
- Emulator/boot: `tools/boot_xl.py` (`boot()` → cpu/mem; run a ROM routine: `cpu.push(0xFFFF); cpu.PC=addr;
  step until PC==0xFFFF`). Z80 API: `PC,SP,push,step,rb,wb`.
- Decode/datapath: `tools/aru_datapath.py` (frontier decode + /32 + exact pipeline; legacy behind `legacy=True`).
- Session-8 tools (reuse): `_hunt_arbiter.py` (both-gates), `_hunt_symflow2.py` (validated symbolic flow graph,
  err=0), `_hunt_l3stats.py`, `_hunt_longir.py`, `_hunt_diagunity.py`, `_hunt_rawcache.py` (`_rawcache.pkl`).
- Manual: `docs/reference/224/Lexicon-224X-Service-Manual.md` (§3.6 DMEM, §3.7 ARU, §3.8 FPC, §5.3.2 ADD'L
  MULT, §5.4-5.5 diag programs, **§5.7 signature tables**). Block diagram: `images/fig-4-1-reverb-*.png`.
- Schematics: ARU 060-01318, T&C 060-02475 (sheet-2 crops `crops/tc2_*`, coeff `…02475-D_2-U10-U11.png`),
  DMEM 060-02512.
- Full Session-8 record: memory `224xl-session8-inv-l3-and-dead-tank.md`. **Note: `224XL_technical_reference.md`
  is STALE — trust this plan + the frontier doc + the manual, not the tech ref.**

## 6. Discipline
A result is real only if it (a) is a principled structural correction, (b) survives the **all-programs** check,
(c) matches an independent oracle (here: the §5.7 signatures and the firmware-built diagnostics), and (d) is
realizable in the schematic + timing. Do NOT touch the C++ core / golden until the audio path produces a real
RT60≈20s decay. The decode is settled — resist re-litigating it; the bug is in the timing.
