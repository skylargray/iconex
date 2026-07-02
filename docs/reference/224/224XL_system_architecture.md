# 224X / 224XL — System Architecture (reverb signal path)

> **⚠ COORDINATE-SYSTEM CORRECTION (2026-07-01, session 0022) — read before trusting step-indexed
> content:** the WCS executes CPU words **127 down to (128−L)** (reversed; L per program, CONCERT=104,
> reset word 24) and all four lanes read through the **Multibus complement** (type `l2&3`: 0=MEMR 1=MEMW
> 2=IO 3=idle; IO command bits assert on stored-0; **delay = stored l0/l1 directly**, addr=CPC−stored).
> The hardware mechanism sections here (addr adder, MAC, clocks) remain sound; every step number, tap
> list, offset table, and program-structure claim predating 0022 is stale. Authority:
> `docs/sessions/0022 …` + `docs/plans/021`.

> Purpose: a complete, aligned systems model of how the 224X/224XL produces reverb, so that the
> reconstruction work targets the right subsystem. Scope is the **real-time audio signal path** and the
> hardware that defines it. Grounded in the Service Manual §3.1–3.9 and the traced schematics (T&C
> 060-02475, DMEM 060-02512, ARU 060-01318).
>
> **Confidence taxonomy** (see `docs/plans/224XL-validation-plan.md`): ✅ CONFIRMED · 🟡 PARTIAL · 🔵 INFERRED
> · 🟠 GUESS · ⚪ UNKNOWN. The structural model in §1–§5, §7 is ✅ (schematic-traced). The *offset-table layout*
> reasoning in §6 is partly 🔵/🟠 and was distorted by a now-fixed bug — see the Session-11 note in §5–§6.
>
> ## ★ M0b NETLIST CORRECTIONS (2026-06-28) — schematic ground truth ★
> The board is now fully net-traced (`docs/reference/224/224XL_interconnect_netlist.md`, triple-verified) — the
> authoritative source for STRUCTURAL/wiring/part/field-map facts. Corrections to *this* doc (reverb-behavior
> content in §6 unaffected):
> - **DMEM = ONE 64K×16 bank** (`dmem_U20–U35`, 4164, CAS0/). `dmem_U1–U16` **NOT populated**; **no bank-select**
>   (top carry-out `dmem_U64.pin9` = n/c, `CAS1/` hard-disabled). The **"128K / two banks / carry = 17th address
>   bit"** framing is **superseded (corrected inline throughout this doc)** — it's a single linear 64K buffer.
>   (netlist §5.5, §G3D)
> - **CSIGN is NOT a decoded microword control** like XFER/ZERO/WA/RA/MEMAC — it is the **`tc_U20` (74S112) JK-FF
>   output** (ARUCKE/-clocked, AS0-gated fn of MI23). Model must replicate the JK toggle. (netlist §3.10)
> - **Device decode = `tc_U47/U49/U48` (+ tc_U32/U34)** (not just "U47/U48"). (netlist §2T)
> - Confirmed by the trace (✅): `MEMAC=MI17`, `WA=MI18/19`, `RA=MI20/21`, `PROT=MI22`, offset=MI0–15, coeff=MI26–31;
>   WCS = 4× MCM68B10 `tc_U43/U29/U15/U2`; PC = `tc_U1/U14`; multiplier = modified-Booth (SM §3.7 "modified shift and add").
>
> **⚠️ Session-11 correction (read before §6).** Reconstruction work spent ~9 sessions decoding delay offsets
> from `mem[0x4000:0x4200]` and got clustered ~30 000-sample garbage → a "dead tank." **That memory was the
> wrong source.** The real delays are short and sensible (4–176 ms) and live in the firmware's `0x3F4D`
> offset buffer (extracted by `tools/aru224_emulate.py`, validated byte-identical to the firmware load). The
> "delay-memory-map / write-head trample" framing in §6.4/§6.7 was an artifact of the wrong offsets — keep
> the *mechanism* described there (it's how a circular-buffer reverb works) but note the trample problem as
> stated **did not reflect the real program.**

---

## 1. The core model: a microcoded DSP

The reverb is **not** software running on the host CPU. It is a **dedicated hardware DSP** formed by three
modules — **T&C + DMEM + ARU** — that executes a **100-step microprogram once per sample at 34.13 kHz**
(100 micro-steps × 293 ns = 29.3 µs per sample). The 8080 host is orders of magnitude too slow to touch
audio in real time; it only *authors and updates* the microprogram.

The reverb *topology* — which delays feed which gains feed which sums — is **defined entirely by the
microcode in the Writable Control Store (WCS)**. There is no dedicated "reverb filter" hardware. Combs,
all-passes, the recirculating tank, predelay, and early reflections are all **emergent** from the sequence
of micro-ops the WCS issues: *read a delayed sample, multiply-accumulate it by a coefficient, write a
result back.* In other words the machine is a **microprogram-defined signal-flow graph executed over a
delay memory by a multiply-accumulate engine.**

```
            ┌───────────── SBC (8080) ────────────────┐   authors/updates — NOT real-time audio
            │ scans pots/switches; for the loaded     │
            │ program+params computes the WCS micro-  │
            │ code, the DMEM offsets (delay lengths), │
            │ the 6-bit ARU coefficients, and the     │
            │ per-frame chorus-modulation deltas      │
            └───────────────────┬─────────────────────┘
                                │ writes WCS / drives I-O ports
        ┌──── T&C ─────┐   ┌───────── DMEM ─────────┐   ┌───────── ARU ────────────┐
        │ clock+state  │   │ delay memory (DRAM) +  │   │ 4×16 register file +     │
        │ generator +  │──>│ address generation +   │<─>│ serial 6-bit multiplier  │
        │ WCS + micro- │   │ DRAM control/refresh + │   │ + 20-bit sat accumulator │
        │ instr decode │   │ SBC I-O decode + XREG  │   │ + 16-bit result register │
        └──────────────┘   └───────────┬────────────┘   └───────────┬──────────────┘
            sequences                  │                            │
            everything        ═════════╪══════════ DAB (16-bit) ════╪═════════
                                       │                            │
                              ┌────────── FPC ───────────┐
            analog in ──> AIN │ float↔fixed conversion + │ AOUT ──> analog out
                              │ A/D and D/A timing       │
                              └──────────────────────────┘
```

---

## 2. The Digitized Audio Bus (DAB) — the central highway

Everything in the DSP communicates over the **DAB, a shared 16-bit bus.** Each 293 ns micro-cycle, **exactly
one device drives the DAB and the others read it.** This single fact governs the entire reverb: all audio
movement — between the delay memory, the math engine, and the analog I/O — is DAB traffic.

Devices on the DAB and when each one **drives** it:

| Driver | When it drives the DAB | Carries |
|---|---|---|
| DMEM (DRAM read) | a delay-tap **read** micro-op | a delayed audio sample out of the buffer |
| ARU result register (RES) | result-register read / feedback, and as the **write data** for a DMEM write | the latest multiply-accumulate result |
| FPC (RD AD/) | the **audio-input** micro-op | the current input sample (fixed-point) |
| FPC (WR DA/) accepts | the **audio-output** micro-op | the DSP drives RES → FPC for output conversion |
| SBC XREG | when the host reads/writes the bus (config/diagnostics) | host data into/out of the audio path |
| *(none)* | a NOP / unselected micro-op | bus **floats and holds its last driven value** — *schematic-proven*: no pull resistors on DAB0–15 (060-02512), and on a NOP the device-select decode `tc_U47/U49/U48` (060-02475) drives nothing |

The register file (ARU) is **written every cycle** from whatever is on the DAB (to the micro-op's write
address), so the DAB driver each step decides what enters the math. Understanding *who drives the DAB on
each of the 100 steps* is equivalent to reading the reverb's signal-flow graph.

---

## 3. SBC (Single-Board Computer) — the configurator

An 8080-based controller. Its ROMs (8 KB on-board + expansion on the NVS module) hold the **definitions** of
the programs (CONCERT, PLATE, …): for each program and parameter setting, the corresponding microcode, the
DMEM **offsets** (delay lengths), and the 6-bit **coefficients**. Its real-time responsibilities:

- Scan the control head (switches, slide pots) and drive the displays.
- On program load or parameter change, **compute and write the WCS** plus the associated offsets and
  coefficients. The WCS can be rewritten **while the DSP is running** (gated by the microword's PROT bit and
  a same-sample access arbiter), so parameter changes take effect on the fly.
- **Chorus modulation (🟡 firmware-decoded).** The reverb applies always-on chorus modulation: the SBC runs a
  triangle LFO (engine `0xAD5C`–`0xAE9B`, paced by the main loop) that **per frame rewrites the modulated taps'
  delay + allpass-interpolation coefficient**, in anti-phase pairs (see `224XL_modulation_lfo.md` for per-program
  targets, rate, depth). Session 11 corroborated this empirically: the firmware's per-frame patch list rewrites
  the **coefficient (lane3) bytes** of specific steps (CONCERT: 56,57,107,108). 🟡 because the engine is decoded
  and poke-validated but exact depth/rate scaling is partly inferred and it has not been run end-to-end.
- Housekeeping: power-up diagnostics, NVS load/save of user setups.

It **never processes an audio sample.** Treat it as the agent that *authors the signal-flow graph and
animates the modulation*, not as part of the per-sample datapath.

---

## 4. T&C (Timing & Control) — the sequencer + control unit

The DSP's instruction-fetch/decode/control. Three jobs:

1. **Clock generation.** A PLL locks to the host's 2.048 MHz clock and multiplies it to a 30.72 MHz master
   clock (MC). MC is divided to the **293 ns system cycle (3.41 MHz)**, which is split into **nine time slots
   MS0–MS8**, grouped into **three ARU states AS0 / AS1 / AS2**.
2. **State generation.** An 8-bit program counter walks the WCS; it is **reset at step 99**, giving a
   **100-step program per sample → 34.13 kHz** sample rate.
3. **WCS + microinstruction decode.** Four 128×8 static RAMs (**MCM68B10**, `tc_U43/U29/U15/U2`) hold the
   **32-bit microinstruction (MI0–MI31)** per step (loaded by the SBC). The T&C **decodes the microword into the
   control signals** that drive the ARU and DMEM each cycle — XFER (load result register, =MI24), ZERO (clear
   accumulator, gated from MI25), register addresses WA (=MI18/19) / RA (=MI20/21), MEMAC (memory op, =MI17),
   the read/write select (=MI16), etc. — and **serializes the 6-bit coefficient C0–C5 (=MI26–31) into the
   M0//M1/ bit-streams** (74195 shift registers: `tc_U11`→M0/ even, `tc_U10`→M1/ odd) consumed by the ARU's
   serial multiplier. **CSIGN is the exception:** the multiply add/subtract sign **CSIGN/ is NOT a decoded
   microword bit** — it is the `tc_U20` (74S112) JK flip-flop output (ARUCKE/-clocked, AS0-gated from MI23); a
   faithful model must replicate the JK toggle, not read CSIGN from a microword field. (netlist §3.10 / §G3R)

---

## 5. DMEM (Data Memory) — delay store + addressing + DRAM control + host gateway

The DMEM module bundles several distinct functions. They are easy to conflate, so they are separated here.

### 5.1 Data memory = the audio **delay-line storage**
A large DRAM array (on the 4164-populated XL board: **64 K words × 16 bits**, a single populated bank —
`dmem_U20–U35` on CAS0/; the second-bank footprint `dmem_U1–U16` is **NOT populated** this rev, CAS1/
hard-disabled) used as a **single shared circular buffer**. It holds **every delay in the reverb**: the predelay, early reflections,
and the comb / all-pass / recirculating-tank delay lines. It is the *only* place audio persists between
samples. Each cycle the DSP reads delayed audio out of, and/or writes new audio into, this buffer.

### 5.2 Address generation = turning "delayed by D" into a DRAM address
A 16-bit **Current Position Counter (CPC)** advances **+1 per sample**; a 16-bit adder (U49/U50/U63/U64,
✅ owner-traced, **OFST straight order**) computes **addr = CPC − offset** (active-low offset + carry-in high),
where the `offset` *is the delay length of that tap*. The DRAM mux (U36/U18, ✅) is standard row(A0–7)/col(A8–15)
— no bit scramble; physical cell = linear address. This arithmetic ✅ is what selects each delay tap — see §6.
**🟡 Where the offset values come from:** NOT `mem[0x4000]` (the long-used wrong source) — the firmware
*computes* the per-step offsets at program-load (B55B builder → the **`0x3F4D` buffer**) and they are short
(4–176 ms). Use `tools/aru224_emulate.py`. *(Faithful read confirmed; that `delay=−offset` and that these are
the ARU's actual addresses remain 🟡 pending the firmware-routine teardown — Track A of the validation plan.)*

### 5.3 Control signal generation — two unrelated things
- **DRAM control/timing:** the RAS/CAS/refresh strobes that run the dynamic RAM (a delay-line generator,
  **U59 = DL6308**, derived from MEMAC / DABSTB / MEMR).
- **SBC↔DSP I/O interface:** the LS138 **port decoders (U55/U56/U57)** that decode which OUT/IN port the host
  is accessing across all DSP modules; the **XREG** (U38–U41) — the register the SBC uses to read/write the
  DAB, i.e. its window into the audio path; the XACK handshake; and the **run / halt / single-cycle** control
  of the entire DSP (U53/U54). DMEM is, in effect, also the "bus interface card."

### 5.4 Diagnostic hardware
Tristate drivers let the host read the static OFST/ lines and a bus-test register; the XREG path lets the
host inject/observe DAB data. Used by the §5.x diagnostic programs and signature analysis.

---

## 6. The address arithmetic that defines the delays (expanded)

This is the conceptual core of the reverb and deserves its own treatment: **the delay structure of the entire
reverb is nothing more than the set of `offset` values the microprogram uses, interpreted through one piece of
arithmetic.** There is no filter hardware and no per-delay memory allocator — only a circular buffer and an
adder.

### 6.1 One circular buffer, one moving position
The DMEM is a single circular buffer of N = 65 536 words (the one populated 64 K bank). The **CPC is the current
position**, advancing one cell per sample and wrapping every N samples (≈ 1.92 s). Audio
"ages" relative to the CPC: a value written when the CPC was at position *p* sits at cell *p* and becomes
progressively older as the CPC moves away from it.

### 6.2 offset = delay in samples
A micro-op with offset *D* accesses the cell the CPC pointed at *D* samples ago:

```
    addr = (CPC − D) mod N
```

So:
- a **WRITE** at offset *W* stores the current value into cell `(CPC − W)`;
- a **READ** at offset *R* retrieves whatever is in cell `(CPC − R)`.

The **delay realized by a write/read pair on the same physical cell is `R − W` samples**: starting from a
write at `(CPC − W)`, the CPC must advance by `R − W` for the read address `(CPC − R)` to land on that same
cell. Hence:
- `offset` is literally **"how many samples back"**; the *delay length of a tap is its offset*.
- A delay **line** is a (small-offset **write head**, larger-offset **read tail**) pair; new audio is written
  at the head, read out `tail − head` samples later at the tail.
- Multi-tap delays are just **several reads at different offsets** off one write stream.

### 6.3 The hardware subtract: active-low offset + carry-in
The adder does **not** subtract directly. It adds the **active-low** offset `OFST/ = ~offset` to the CPC with
**carry-in tied high**:

```
    addr = CPC + (~offset) + 1  ≡  CPC − offset   (two's complement)
```

(Adder chain U49/U50/U63/U64, carry-in pulled high.) The 16-bit sum is the **full DRAM address** — a single
linear **64 K** buffer (`addr = (CPC − offset) & 0xFFFF`), **not a per-delay-line partition.** (M0b correction:
only one bank is populated this rev, so there is **no 17th address bit / bank-select** — the offset-adder top
carry-out `dmem_U64.pin9` is **not connected** and the unpopulated bank's `CAS1/` is hard-disabled. On a
two-bank rev the carry would have been the bank bit, but that path is unpopulated here.)

### 6.4 The delay memory map is a layout problem solved at program-load
Because every tap is just an offset into one shared buffer, the offsets are **not arbitrary** — the SBC, when
it builds a program, must lay them out so that:
- each line's `(write offset, read offset)` pair yields the **intended delay** (`R − W = D`);
- a line's stored audio **survives from its write until its read** — i.e. no *other* write head sweeps through
  that line's cells during the `R − W` interval. Equivalently, the `[W, R]` offset intervals of coexisting
  lines must be arranged (typically disjoint, or ordered so write heads never enter a live region) so the
  lines do not trample one another in the shared buffer.

This **"delay memory map"** — the assignment of offset ranges to the predelay, the diffusers, and each tank
line — is a real design artifact baked into the program. Reconstructing the reverb means recovering *this map*
(the offset table) and the coefficient table, **not** modeling abstract "comb filters." The offsets **are** the
topology; the coefficients are the gains.

> **🔵→correction (Session 11):** the *real* offset table (from `0x3F4D`) is short and sensibly laid out (the
> recovered CONCERT map: ~362 ms predelay tap, 4–176 ms diffuser/tank delays, a 176 ms recirc loop reused 4×).
> The "write heads cluster and **trample** each other" problem that dominated Sessions 3–11 was an **artifact of
> decoding offsets from the wrong memory (`0x4000`)** — it does **not** describe the real program. The
> survival/disjointness reasoning above is still the correct *mechanism*, but the real layout already satisfies
> it; recovering the map is now a matter of reading `0x3F4D` correctly, not solving a trample puzzle.

### 6.5 Wrap period bounds single delays; the tail comes from feedback
The buffer wraps every 65 536 samples (~1.92 s). Any single delay line must be shorter than the
wrap period. A long reverb tail (seconds) is therefore **not** one long delay — it is produced by **feedback**:
a line's read is scaled by a near-unity coefficient and **written back into the same line**, so energy
recirculates with loop time `R − W` and per-loop gain set by the coefficient. **The reverb decay time is set by
the loop gain, not by the raw delay length.**

### 6.6 Modulation = time-varying offsets (inferred)
The reverb applies always-on chorus modulation. The most likely mechanism is the SBC rewriting selected offsets
by small ± deltas per frame, so those delay-line lengths wobble (a delay-modulation / chorus effect), making the
address arithmetic time-varying — some offsets LFO-driven, animating the memory map over time. **This mechanism
is inferred from reverse engineering; it is not stated in the manual or schematics.**

### 6.7 The recirculating loop (and the resolved "dead-tank")
A recirculating loop is exactly: **read at offset `R` → multiply-accumulate by the feedback coefficient →
write at offset `W` of the same line**, closing every `R − W` samples. If the value read at `R` does not get
written back onto the line it tapped, the loop is **open** and the tank cannot ring.

> **Resolution (Session 11):** the "dead tank" chased for ~9 sessions was **not** a real loop-closure failure
> — it was the consequence of feeding the datapath the wrong (`0x4000`) offsets, which clustered the write
> heads so feedback was trampled. With the **real short delays** (`0x3F4D`, 176 ms recirc loop), the structure
> is sound: a 176 ms loop at the recovered feedback gain (~0.6) gives RT60 ≈ 2.6 s. ⚪ **What remains unproven**
> is the end-to-end demonstration: rebuild the datapath on the real offsets + correctly-aligned control fields
> and show a coherent, parameter-tracking decay. That is Track E of `docs/plans/224XL-validation-plan.md`.

---

## 7. ARU (Arithmetic Unit) — the ALU

The datapath that executes the math. Contents and the constraints that shape the algorithm:

- **4 × 16-bit register file** — the *entire* working set (only four registers), holding operands taken from
  the DAB (a DMEM read, the FPC input, the SBC XREG, or the result-register feedback).
- **Serial 16 × 6-bit two's-complement multiplier** with saturation logic — a **modified-Booth (radix-4)**
  shift-and-add multiply spread across AS0/AS1/AS2 (two partial products per state; the even/odd coefficient
  streams M0//M1/ are the Booth selects). (Service Manual §3.7 calls the same mechanism "modified shift and add.") The coefficient is **6 bits at a /32 scale** (value 32 = ×1.0,
  range ≈ ±2.0). **Schematic-proven** (060-01318): the result register (74F374 U43/U44) latches partial-product
  bits **PP3..PP18** (= product ≫3), while the operand enters the multiplier with its low 3 bits tied to 0 (=
  operand ≪3, manual §3.7) → net ×C/32. Corroborated by the firmware multiplier self-test (a +42/32 = 1.3125
  coefficient is only representable by a 6-bit field at /32, not /64). Every gain, filter coefficient, and
  feedback gain is quantized to these 6 bits.
- **20-bit saturating accumulator** — on overflow the **74F157 saturation muxes (U33–U37)** force the top two
  bits equal to the sign and the low 18 bits to its complement, giving **+0x3FFFF (+2¹⁸−1) / −0x40000 (−2¹⁸)** —
  a **schematic-proven** rail of **±2¹⁸** (060-01318; overflow detected by the U42 XOR of the top two sum bits).
  A >1 coefficient on a large operand rails it — real hardware behavior, part of the sound and a real hazard.
- **16-bit result register (RES)** — buffers the MAC output onto the DAB so the multiplier can start the next
  product without waiting for the previous result to be consumed. RES is the **feedback node**: RES → DAB →
  register file re-enters the math; RES → DAB → DMEM stores into a delay line.

The ARU does multiply-accumulate (gains and sums) and saturation — nothing else. It has **no filters in it**;
the filters are emergent from the WCS micro-op sequence operating over the DMEM delays (§1, §6).

---

## 8. Peripheral modules — what does and does not affect the reverb

| Module | In the real-time signal path? | Effect on reconstruction |
|---|---|---|
| **FPC** (Float↔Fixed Converter) | **Yes — keep it.** | Input enters the DAB *only* via its **RD AD/** op (float→16-bit fixed); output leaves *only* via **WR DA/** (fixed→float). It also generates A/D and D/A timing. Its **16-bit fixed-point scaling** sets levels/headroom. Abstractable to "sample→16-bit on DAB; 16-bit→sample," but the RD-AD/WR-DA micro-ops must be modeled — that is how audio gets in and out. |
| **AIN** (Audio Input) | At the analog boundary only. | Anti-alias filter + sample/hold + gain-ranger + ADC; sets the **34.13 kHz rate** and **input bandwidth (~15 kHz)**. Model as an ideal band-limited sampler; note the program's *HF Bandwidth* parameter interacts with it and shapes tone. |
| **AOUT** (Audio Output) | At the analog boundary only. | DAC + reconstruction filter + output gain switch. No effect on the delay/feedback structure. |
| **NVS** (Nonvolatile Storage) | No (setup only). | Holds user register setups (param values) + ROM expansion. Determines *which* program/params load (e.g. CONCERT's 2.6 s defaults), i.e. which offsets/coefficients exist — not the per-sample math. |
| **Control Head / Transition** | No. | UI (switches/pots/display); source of parameter values the SBC reads. |
| **Power Supplies** | No algorithmic effect. | One caveat: this rev is populated with **4164 (64 K)** parts as a **single 64 K bank** (`dmem_U20–U35`); the second-bank footprint (`dmem_U1–U16`) is unpopulated (bank jumpers E91/E92 = bank 1, E95/E96 = bank 2). Older revs used a half-capacity (16 K-class) part in two banks. |

---

## 9. The one-line model, and where the reverb lives

> A **microcoded DSP (T&C sequences, ARU computes, DMEM stores delays)** executes a **100-step-per-sample
> signal-flow graph** — defined by the WCS microcode, with delays = DMEM offsets and gains = 6-bit ARU
> coefficients — moving audio across the **DAB**, while the **SBC** authors and animates that microcode
> (program + params + chorus modulation) and the **FPC** bridges fixed↔float to the **AIN/AOUT** analog ends.

The reverb behavior — and the open dead-tank question — lives in one corner of this model: the **per-sample
DAB traffic that closes the comb/all-pass loops** (read a delay → MAC by a feedback coefficient → write it
back), with the 4-register file and RES as the only scratch. The productive way to read that corner is to
enumerate, for the loaded program's 100 steps, **the DAB driver, register read/write addresses, offset, and
coefficient of every step**. That table *is* the signal-flow graph, and it shows exactly where each loop is
meant to close.
