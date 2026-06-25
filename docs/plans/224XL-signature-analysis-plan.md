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

---

## 7. SESSION 9 LOG (2026-06-24) — oracle infra BUILT; the "timing-only" premise is CHALLENGED

### 7.1 Verified deliverables (reusable; trust these)
- **`tools/sig224.py` — HP-5004A signature oracle, CALIBRATED & verified PASS.** Convention (confirmed against
  ALL FIVE §5.7 +5V references at integer N): poly `X^16+X^12+X^9+X^7+1`, Fibonacci left-shift, data-bit IN the
  feedback XOR, taps at value-bits {15,11,8,6}, MSB-nibble-first display via `"0123456789ACFHPU"` (F=0xC, H=0xD,
  P=0xE, U=0xF). **Window lengths N (ARUCK edges):** ARU no-fb=62, **ARU fb=90 (=30 steps×3 ARUCK/step ✓)**,
  T&C=30, DMEM=4096(=2¹²), FPC=98. GROUND(all-0)→0000 ∀N. `display_to_value("29F3")=0x29C3`.
- **`tools/diag3.py` — Diag-3 ARU SIGNAT WCS capture (cached `_diag3_wcs.bin`).** Dispatch cracked: jump table
  @`0x0330` is indexed by program number → **Diag-3 handler = `0x0CF0`** (verified: idx8=0x0EF4 Max-Delay,
  idx7=0x0EFD Zero-Delay). The handler tail-calls a frame-sync wait @`0x0627` (spins on `mem[0x3C14]==0x80`);
  patch it to RET to let the build run. It only writes WCS steps 96-127; isolate handler-written bytes by the
  0xFF/0x00 prefill-agreement method. **Result: 30 active steps (98-127), all MI17=1, RA cycling 3→0, coeffs
  ±47/±31/±2/±12/±8/±16/±32, 8 XFER / 25 ZERO.**
- **`tools/aru_cycle.py` — cycle-accurate model** (decode + /32 reused from aru_datapath). ADD'L MULT (EA0-EB3)
  arithmetic **PASS**: RES=x·cs/32 for cs=32(×1),16(×½),−32(×−1),8(×¼),40(×5/4). Has `timing='faithful'|'legacy'`.
- **Timing ground truth extracted** (`docs/reference/224/images/fig-3.2/3.3/3.4*.png` + `…ARU pinouts…01318.txt`):
  Fig 3.2: cycle=MS0-8; AS0=MS0-2, AS1=MS3-5, AS2=MS6-8; ARUCK once/AS-state. Fig 3.4: XFER CK fires at the
  cycle k→k+1 boundary, capturing ACC **before** k's own product; ZERO clears for k's fresh accumulation; product
  available end of AS0 of next cycle. Fig 3.3: DMEM CAS in AS2; **"DIN critical path = XFER CK→result reg."**
  **Full ARU netlist** (pinout file): RES=U43/U44 D-inputs=**PP[3..18]** (Q/DAB outputs are tri-stated/unmeasured,
  shown "-" in §5.7); accumulator AC[0..19]=U45-49 Q; the §5.7 ARU **feedback oracle measures the PP bus (adder/
  sat-mux output, U43/U44/U45-49 D-pins) and AC bus (U45-49 Q-pins)** — so reproducing it REQUIRES the sub-cycle
  serial-multiply (PP0/PP1/PP2 accumulation), not just microinstruction-level RES.

### 7.2 THE CHALLENGE TO "decode settled / timing-only" (hard evidence, multiple independent fixes failed)
Tracing the **audio path** under the confirmed frontier decode, the CONCERT impulse never even ENTERS the tank:
- CONCERT input = RD-AD step **s76** (sub3) → `R[3]=20000`. The very next step **s77 reads R[3]=20000 but has
  coeff cs=0** (product 0) and, being a DMEM op, overwrites `R[3]=RES=0`. **The impulse is multiplied by zero and
  discarded at the first hop.** No XFER step ever sees nonzero ACC ⇒ peak=0, 0 live DMEM cells (immediate MAC),
  matching `run_trace`'s dead 2/4000.
- **Tried and REFUTED as the revival** (none make CONCERT sustain or even enter the tank): faithful 1-cycle-late
  RES load (Figs 3.3/3.4); immediate vs deferred(`pend`) MAC; DMEM read-modify-write (read-old-onto-DAB + write
  RES); all 2⁵ DMEM read/write assignments of Max-Delay; 14-bit(16K) / 15-bit / 16-bit DMEM buffer.
- **Max-Delay is a DEGENERATE oracle:** its 5 DMEM steps are ALL MI16=0 (no MI16=1 reads at all), so under the
  frontier "MI16=read/MI17=MEMAC" decode it has **no DMEM-read path** and cannot echo under ANY timing — and the
  legacy `_hunt_diagunity` decode ALSO fails it now (its RA=0 output reads a never-written register). **The
  "+0.969 unity echo" in prior memory is NOT reproducible with current tools/decodes.** (CONCERT, unlike Max-Delay,
  *does* have 8 MI16=1 reads + 10 writes, so its read path exists — but the impulse still dies at the coeff-0 hop.)
- ⇒ The dead tank is **not explained by ARU pipeline timing alone**. The first failure is upstream — the input
  coupling / coefficient at the input-use step (s77 coeff=0) and/or the DMEM read/write & register-file routing.
  This points back into the **l2-byte / coeff / injection decode**, which §1 declares settled. **Genuine conflict.**

### 7.3 ORACLE BUILT (`tools/aru_sig.py`) — DECODE IS CORRECT; my bug was a missing register-file PRELOAD
**Correction (the decode is settled and right — WA0=MI18, WA1=MI19, RA0=MI20, RA1=MI21, owner-verified).** My
earlier "WA decode is wrong" reading was an ERROR. The Diag-3 program's all-WA=3 is the *intended* pass-through
(§3.7 "address 3 is the pass-through location"): with WA=3 every step, R[0],R[1],R[2] are **preserved**, and the
signature test PRELOADS the register file with the four XREG constants the handler loads via OUT 0x06/0x07
(`0xAAAA, 0x9999, 0xC787, 0x607F`); RA rotates 0,3,2,1 to read them. My model started R=[0,0,0,0] — *that* is why
the accumulator sat at 0000. **Preloading R with those four constants (decode UNCHANGED) brings the accumulator
ALIVE: 41/90 nonzero over the feedback window.** (CONCERT decodes with healthy varying WA under the same map,
which already proved the decode — the all-WA=3 was specific to this test and is legitimate.)

The serial multiply (PP0/PP1/PP2 = `(x<<3)*cmag>>5` to ±1 LSB truncation), 20-bit sat accumulator, /32 scale, FPC,
XFER/ZERO-from-l3, and the signature algorithm are all validated. `AC_TARGET`/`PP_TARGET` hold the §5.7 feedback
targets; `compare()` scores any model against them.

### 7.4 CALIBRATION STATUS — model alive but §5.7 node signatures stick at 0–1/40 (the WALL)
Swept the principled knobs (decode FIXED): preload values (raw + active-low complement × all 24 register
orderings), accumulator pipeline phase (operand read→multiply delay 0/1; XFER/ZERO state 0/1/2; PP-bus assignment
straight-binary vs Fig-3.4-literal), sampling alignment 0–89. The model RUNS and is periodic (steady-state ACC
range ≈ −160k..+210k, real RES values), but reproduces only **0–1 of the 40** §5.7 AC/PP node signatures
(`AC16==AC17` sign-anchor never matches). A pipeline-phase tweak is NOT enough.

**Why (the diagnosis):** because WA=3 every step, R[0],R[1],R[2] are never overwritten — they hold their PRELOADED
values for the entire run, so those values DIRECTLY set the whole steady-state sequence. The four XREG constants
(`AAAA/9999/C787/607F`) in any order/polarity do NOT reproduce §5.7, so the diagnostic's **real initial ARU state**
(register file + RES + accumulator) is established by the SBC's `OUT 0x00..0x07` ARU-control sequence during the
build — a path NOT modeled (boot_xl's ARU stub ignores ports 0x00-0x03). Greening §5.7 needs that **SBC-driven ARU
preload/single-step phase** modeled (the ARU diagnostic-control interface: how OUT 0x00-0x07 load/clock the
register file, X-reg, result reg), or gate-perfect sub-cycle datapath fidelity — a deeper sub-project than a phase
calibration. `tools/aru_sig.py:compare()` remains the acceptance test once that init is modeled.

**Oracle's delivered value:** confirmed the decode is correct, and showed the dead state is a MODEL-INITIALIZATION
problem (register/ARU state), not the decode or a simple timing bug.

### 7.5 SBC PRELOAD DETERMINED (firmware trace) + the signature-calibration LIMITATION
**Preload protocol decoded from the handler** (`tools/aru_sig` trace of OUT 0x00-0x07 + WCS patches): the handler
patches step-126's l2 (`0x41FA`) to WA=0,1,2,3 and single-steps (OUT 0x03) with XREG = `AAAA, 9999, C787, 607F`
respectively, so the diagnostic loads **R[0]=AAAA, R[1]=9999, R[2]=C787, R[3]=607F** (the SBC drives the DAB from
the X-reg and clocks R[WA]). Order is now KNOWN, not guessed. (The single-step also runs step-126's microinstruction
— cs=-32,ZERO=1 — so RES/ACC also get a small initial state.)

**But §5.7 still 0/40** with that exact preload (+ active-low complement + bus-inversion variants). **Why this is a
wall:** the HP signature is a black-box 16-bit hash with NO partial feedback — it flags *any* single-bit error over
the 90-edge window, so to green even one node the serial multiply, accumulator pipeline, the **negative-logic adder**
(74F283 + the NAND/XOR inversions), CSIGN 2's-complement carry, the saturation muxes (74F157), the per-pin
**active-low polarity**, and the **ARUCK-vs-ARUCKE/ sample phase** must ALL be bit-perfect at once. That is a full
gate-level ARU emulation, and with no gradient there's no way to *calibrate* into it — it must be built right from
the netlist. This is a substantial sub-project, and the signature's all-or-nothing nature makes it a poor calibration
target (great for fault detection, bad for model fitting).

**Recommendation (engineering judgment):** the oracle already delivered its decisive value (decode confirmed +
preload determined). For the GOAL (a live RT60≈20s reverb), bit-exact signature fidelity is overkill — the high-level
datapath is validated (ADD'L MULT, /32, serial multiply ±1 LSB) and the decode + preload are pinned. Pivot to direct
CONCERT validation (which gives a continuous RT60 error signal, unlike the black-box signature), seeding the register
file / DMEM with the real power-up state, and use the §5.7 signatures only as a final gate once a gate-level ARU
model is built. C++ golden UNTOUCHED (RT60 gate red).

### 7.6 CONCERT RT60 pivot — bug PRECISELY localized, but no high-level timing revives the tank
Reproduced the documented dead-tank EXACTLY (deferred MAC, inject impulse at ALL 19 sub=3 RD-AD steps at n=0 — the
A/D holds the impulse so every RD-AD reads it): the impulse enters **1 DMEM cell** (predelay 0xCFC1 = −3750), held,
read back at sample 18230 (~0.53 s) — and the **diffusion processes it (RES=−7032 at s25) but it never reaches a
tank-write**: the DMEM-write at s24 fires with RES=0 (stale, one step before the XFER), and between s25's XFER and
the next write RES is overwritten by intervening XFER steps, so the diffused value is lost. Tank stays at 1 cell ⇒
no recirculation ⇒ silence.

**Tried & REFUTED (none fill the tank past 1 cell):** deferred / immediate / faithful-next-cycle MAC; DMEM-write
DIN deferred 1 step (Fig 3.3 "DIN=XFER CK→result reg"); operand read→multiply 1-cycle pipeline (Fig 3.4); DMEM read
latency; all combinations. The recirculation (DMEM-read → multiply → XFER → RES → DMEM-write → delay → DMEM-read)
never closes because the XFER↔write↔result-feedback alignment is wrong, and NO microinstruction-granular value-level
timing model I can construct fixes it.

### 7.7 GATE-LEVEL ARU BUILT (`tools/aru_gate.py`) → reveals the signature test is SBC-SINGLE-STEPPED
Built the gate-level datapath from the 060-01318 netlist: serial multiply (shift-add, ADD'L MULT **PASS**),
negative-logic accumulate (CSIGN XOR → 74F283 adder → 74F157 sat-muxes → accumulator U45-49 @ARUCKE/), result reg
@XFER-CK = PP[3..18], per-ARUCK PP/AC sampling, firmware preload R[0..3]=AAAA/9999/C787/607F fixed, only sub-cycle
phases swept. **Result: still 1/40 vs §5.7 — IDENTICAL to every prior model.** ⇒ the gap is NOT datapath fidelity
(now gate-level); it is UPSTREAM.

**Root cause of the 0–1/40 wall (decisive):** the signature-test runtime `0x02AD`→`0x119B` is a **dispatcher that
SINGLE-STEPS the ARU under SBC control** (reads flag `0x3C06`, RRA-indexes a jump table of per-op handlers at
`0x02F1..`). **The signature test does NOT free-run the 30-step WCS — the SBC orchestrates each ARU cycle and feeds
data.** Every model this session ran the WRONG mechanism (free-running the WCS), which is why none matched.
Reproducing §5.7 requires emulating the **full SBC-driven ARU single-step sequence** (firmware + a faithful ARU that
responds to the single-step control ports) — a major co-emulation, NOT more datapath modeling.

**This DECOUPLES the signature from CONCERT.** CONCERT runs the WCS FREE (normal op); the signature test
single-steps (a diagnostic mode). So greening §5.7 would NOT directly validate CONCERT's free-run timing, and the
gate-level datapath (same value-level result as the high-level model, ±1 LSB) does NOT change CONCERT's dead tank.
⇒ Two SEPARATE problems:
- **§5.7 green:** needs SBC+ARU single-step co-emulation (large; low value for the audio goal).
- **CONCERT live tank (the real goal):** a FREE-RUN recirculation-timing bug, precisely localized (§7.6) but
  unresolved — no value-level timing variant (high-level or gate-level) revives it. Likely needs the exact DMEM
  write/read/XFER cycle timing from the DMEM schematic (060-02512, Fig 3.3 delay-line U59), OR an approximate model
  tuned directly for RT60. C++ golden UNTOUCHED (RT60 gate red).

> NOTE: §7.2 (the "decode-settled challenge") is SUPERSEDED by §7.3+ — the decode is CORRECT; the issues were model
> initialization (§7.3-7.5) and free-run recirculation timing (§7.6-7.7), never the decode. Kept for the audit trail.

### 7.8 OWNER SCHEMATIC READS → 2 corrections; the dead tank is now pinned to ADDRESSING
The owner read Figs 3.3/3.4 and traced nets (decisive):
- **Memory-access decode CONFIRMED:** MEMW/ = U47 (74LS139) pin 6 from MI16+MI17; MI17 drives MEMAC. ⇒ write iff
  MI17=1 & MI16=0, read iff MI17=1 & MI16=1 (= the frontier decode; not the bug).
- **Datapath TIMING CONFIRMED, ruling it out:** XFER loads the result reg EARLY (≈MS3); CAS/write is MS4-8 AFTER it;
  DMEM read data is valid only MS8→next cycle. This matches the model ⇒ the dead tank is NOT a timing bug.
- **CORRECTION 1 — the MAC is IMMEDIATE, not deferred.** Microinstruction M's own XFER bit captures M's own product
  (the 1-cycle latency is internal to M, not a shift to the next program step). `run_trace`'s deferred `pend` was
  WRONG. Immediate MAC (`if ZERO:ACC=0; ACC+=prod; if XFER:RES=ACC>>3`) gets the impulse into **3 DMEM cells** (vs 1).
- **CORRECTION 2 — THE REMAINING BUG IS THE ADDRESS MATH.** Even immediate-MAC collapses: the 3 input-written cells
  are almost never re-read (only the predelay, 5×/40k; the 2 comb cells never), so write/read addresses don't form
  recirculating loops. Fix the OFFSET→ADDRESS arithmetic (`addr=(pos-offset)&0xFFFF`, `offset=~(l1<<8|l0)`) — suspect
  the high offset bits b15/b14 are control not address (→14-bit/16K buffer), the position-counter step, or the offset
  sign — so a written comb cell is RE-READ at its delay → recirculation → RT60. Tested & not it: 64K/16K/16K-wrap,
  read-latency. **DECODE + TIMING + memory-access are CONFIRMED — do NOT reopen. The open item is purely addressing.**
  (Owner schematic q for next session: how the OFST/ offset becomes the DRAM row/col address — are all 16 bits used,
  or do b15/b14 do something else?)
