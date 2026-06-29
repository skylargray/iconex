# 224XL — M3: free-run the phase-accurate RTL model into a coherent reverb

> **READ-FIRST / START-HERE for M3.** This is the next milestone of the holistic plan
> (`docs/plans/013`). **M0a/M0 (netlist), M1 (clock/state engine), M2 (datapath, passes the
> whole POST un-suppressed) are DONE.** The phase-accurate RTL model
> (`tools/aru_rtl.py` = framework + `ClockEngine`; `tools/aru_rtl_dp.py` = `ARU_RTL` datapath)
> currently runs only in **single-step** mode (the SBC strobes one microinstruction at a time;
> the WCS program counter is held). **M3 makes it run FREE** — the T&C autonomously sequences
> the 100-step microprogram per audio sample, the DMEM recirculates across samples, and a
> **reverb emerges from the wiring.** Success = a coherent, decaying impulse response whose RT60
> tracks the size/decay parameter, **with no hand-tuned gain** (the loop closes because the
> netlist closes it). This is exactly the failure that nine early sessions chased on *sectional*
> (value-level) models; the holistic thesis (`013 §0`) is that those failures were artifacts of
> sectional composition — the loop will close when the structural model is wired + clocked right.

---

## ★ STATUS (2026-06-29) — engine DONE + verified; CONCERT recirculation localized

**Built: `tools/aru_freerun.py`** (the free-run engine; does NOT touch the POST-green M1/M2 files).
`FreeRunARU` sweeps the WCS PC 0→99 (RESET@99), fetches+decodes each step (reusing the M2 `decode`
+ the verified gate Booth), routes the DAB per the §2T device decode, models the fig-3.4 **deferred
MAC** as a 1-instruction pipeline (`pend`), accumulates a **clean signed MAC** (`sat16(ACC≫3)`),
advances **CPC +1/sample**, recirculates the DMEM (`addr = CPC + OFST_stored + 1 = CPC − OFST`), and
does the I/O (inject @ RD AD/, capture @ WR DA/ on channels A–D). Run: `python tools/aru_freerun.py`
(fast structural suite) / `… concert` (boots + characterizes CONCERT).

**Verified (success criteria 1–3 MET):**
1. **Runs clean (M3.0)** — executes the whole 100-step CONCERT program for thousands of samples
   (500k+ microinstructions) with **no decode/addressing fault**; sensible per-step DAB-driver
   histogram (MEMR/RDRREG/RD_AD/RD_XREG/HOLD).
2. **Zero-delay (M3.1) PASS** — a hand-loaded RD AD/→WR DA/ program passes the input straight to
   outputs A & D **unchanged** (proves engine + 100-step loop + DAB routing + I/O boundary).
3. **Max-delay (M3.2) PASS** — a hand-loaded DMEM delay reappears at the output **exactly `delay`
   samples later** (verified 64 & 150), proving the DMEM write→read delay across samples.

**Engine recirculation CAPABILITY (M3.3) PROVEN** — a hand-built feedback comb `y[n]=x[n]+½·y[n−D]`
produces a coherent decaying echo train with ratios **exactly 0.5** — the loop closes from the wiring,
decay set by the coeff, **no tuned constant**. So the structural engine *can* make a recirculating
reverb when the WCS closes the loop (the holistic thesis).

**CONCERT (criterion 4) — partial, root cause localized (NOT a dead engine):** running the captured
**static** CONCERT WCS free, the **DMEM delay memory retains the input-burst energy and decays over
~1.7 s (a reverb-like RT)** — writes store real values, the long read taps (0.9–1.4 s) read them back.
But the **OUTPUT (WR DA/) is sparse** — the direct signal + **discrete echoes (~1.4–1.6 s)**, not a
dense continuous tail. Diagnosis: storage/feedback works at a reverb timescale; the output isn't
densified. Most-likely causes (next session): the **per-frame LFO modulation** (M4 — the 4 modulated
taps 56/57/107/108 smear the delays into a dense field; the modulation is main-loop-paced, decoded in
`224XL_modulation_lfo.md`, and is NOT yet driven by `boot8080`) and/or a **feedback-timing refinement**
(the read-before-write / deferred-MAC conventions are the two un-POST-tested choices — probe them
against fig-3.3/3.4). **Per the discipline: no gain knob was added; the finding is a localized
output-density / modulation gap, not a tuned decay.**

**Decisions baked into the engine (see file docstring):** deferred MAC = 1-instruction pipeline
(fig-3.4); regfile/DMEM = **read-before-write** (ARUCK@MS6 operand load precedes the MS7 write —
CONCERT decouples its MEMR-write-register from a later read step, consistent with this); accumulator =
clean signed MAC (positive single-multiplies match the POST goldens exactly, negatives within ≤2 LSB
≈ −84 dB by design, since a clean accumulator is the right model for multi-tap sums); CPC +1/sample at
RESET@99 (resolves the §5.1 ⚪ RUN-mode count cadence). **POST regression still green** on `aru_rtl_dp.py`.

**Open → M4:** drive the per-frame WCS modulation (the main-loop LFO, co-simulated with the free-run)
so CONCERT's output densifies into a faithful decaying tail; then RT60-tracking + ≥3 programs + L7 IR.

---

## 0. Goal and success criteria

**Goal.** Extend the M2 RTL model from single-step to **free-run**: the T&C microsequencer fetches
and executes all 100 WCS microwords every audio sample (34.13 kHz), the CPC advances per sample,
the DAB is driven per-step by the device decode, the DMEM recirculates, and audio flows A/D → DSP
→ D/A. Run a program over many samples and capture the impulse response at the output node.

**Success (in order of strength):**
1. **Runs without faulting** — the free-run engine executes the full 100-step microprogram for
   thousands of samples, all elements clocked on their real edges, no decode/addressing error.
2. **Zero-delay program** (the simplest case, no DMEM): an impulse at the input appears at the
   output unchanged (input → outputs A & D), proving the free-run engine + I/O + the 100-step loop.
3. **Max-delay program** (0.5 s, uses DMEM): the impulse reappears ~0.5 s later, proving the
   DMEM write→read delay path (`addr = CPC − OFST` across samples).
4. **CONCERT (a real reverb): a coherent, *recirculating* impulse response** — energy circulates
   through the all-pass/comb structure and **decays** (does not die in <10 ms, does not blow up),
   with a sensible reverb tail. **No hand-tuned gain** — the loop gain is whatever the coeffs +
   wiring produce.
5. **RT60 tracks the size/decay parameter** across programs/settings, and the result is consistent
   across ≥3 programs (= plan 013 **M4**, the tail of this work).

**Definition of done for M3:** criteria 1–4 met (coherent recirculating CONCERT reverb from the
wiring). RT60-tracking + multi-program (5) carry into M4; L7 (real-unit IR match) is last.

---

## 1. What's in place vs what M3 adds

**In place (M1/M2, verified):**
- `ClockEngine` (M1): MS0–8 / AS0–2 / ARUCK / ARUCKE/ / DAB WSTB/ / DAB RSTB / XFER CK / ZERO/ —
  validated against fig-3.2/3.4 (`tools/aru_rtl.py`).
- The datapath elements as edge-clocked structural objects (M2): regfile (4×LS670), the 3-AS
  modified-Booth multiply (via the verified `aru_booth.comb_array`), accumulator, result register,
  CPC, DMEM (`addr = CPC − OFST`, read-before-write), device decode (`tools/aru_rtl_dp.py`).
- The microword field map (§G3R), the single-step read-back path, the SBC port map — all
  POST-verified.

**What M3 adds (the free-run half — L6.7–L6.13, never exercised by POST):**
1. **The WCS program counter (microsequencer).** A real PC sweeping **step 0→99** (100
   microinstructions = one sample), **RESET at count 99**, advancing per microinstruction (on
   DAB RSTB/). Fetch microword[PC] from the WCS image (`0x4000 + 4·PC`) and execute it. (In
   single-step the PC was *held*; here it runs.)
2. **CPC cadence for RUN.** CPC advances **+1 per sample** (at the RESET@99 boundary), NOT per
   microinstruction — so all 100 steps of a sample address DMEM relative to the same CPC, and a
   cell written at sample S is read OFST samples later (delay = `OFST_read − OFST_write` samples).
   (Single-step advanced CPC per strobe; that is the single-step cadence, not RUN — netlist §5.1
   flags the count-clock source as un-traced; resolve which edge clocks it in RUN.)
3. **Per-step DAB-source routing.** Each step the **device decode** (§2T) picks the *one* driver
   of the shared DAB: `MEMR/` → DRAM data; `RDRREG/` → result register; `RD AD/` → A/D input
   (FPC); sub-decoder selects; or **idle = hold** (no driver → the DAB keeps its last value, no
   pull resistors). The bus is consumed by: regfile write (`DAB WSTB`/¬MS7), DMEM write (`MEMW/`,
   DIN = result reg), and the D/A output (`WR DA/`). This per-step muxing is the heart of the
   signal-flow graph and is what POST never drives.
4. **The deferred MAC across instructions.** fig-3.4: a multiply's result is available at the
   *next* instruction's AS0, where `XFER CK` (if the microword's XFER bit is set) latches the
   accumulator into the result register, and `ZERO/` clears the accumulator. In single-step we
   flushed this per strobe; in free-run the **1-instruction pipeline latency is real** and must be
   modeled (the accumulator/result-reg carry state across steps).
5. **The audio I/O boundary.** Inject the input at the `RD AD/` step (A/D), capture the output at
   the `WR DA/` step(s) (D/A, outputs A–D). For a first IR, model the I/O as fixed-point (raw
   16-bit), deferring the FPC float↔fixed conversion (fig-3.5/3.6) — the reverb tail lives in the
   fixed-point DSP loop, not the FPC.
6. **The recirculation.** With (1)–(5) wired, the feedback loop closes structurally: a step writes
   an (attenuated) sample to a DMEM cell; a later step (later sample) reads it, multiplies by the
   feedback coeff, accumulates, and writes it back — the recirculating delay network of the reverb.

---

## 2. The free-run execution model (the precise shape to build)

**Per audio sample (one "frame" = 100 microinstructions):**
```
for step in 0..99:                      # WCS PC sweep (RESET@99); advances on DAB RSTB/
    mw = WCS[0x4000 + 4*step]           # fetch the 32-bit microword (l0..l3)
    d  = decode(mw)                     # §G3R field map (offset, MEMAC/MI16, WA, RA, CSIGN, XFER, ZERO, coeff)
    run one microinstruction (MS0..MS8 / AS0..AS2) on the ClockEngine, with:
      • addr   = (CPC + OFST_stored + 1) & 0xFFFF        # = CPC − OFST  (DMEM steps)
      • DAB driver = device_decode(d):                   # exactly ONE per step, else hold
          MEMR/      -> DAB <- DMEM[addr]
          RDRREG/    -> DAB <- result_reg
          RD AD/     -> DAB <- audio_in (impulse on sample 0, else 0)
          (idle)     -> DAB holds last value
      • regfile:  R[WA] <- DAB   @ DAB WSTB (¬MS7)        # if a regfile-write step
      • multiply: PP = booth(R[RA], coeff, CSIGN)         # 3-AS pipeline -> product reg @ ARUCK
      • accum:    ZERO/ clears @ AS0; += PP @ ARUCKE/     # 1-instr deferred
      • result:   result_reg <- sat16(ACC>>3) @ XFER CK   # when XFER set (deferred to next-AS0)
      • DMEM wr:  DMEM[addr] <- result_reg  @ MEMW/        # if a MEMW step
      • output:   capture DAB @ WR DA/  -> output sample(s)
CPC <- (CPC + 1) & 0xFFFF               # advance one sample position at RESET@99
```
This is the signal-flow graph the Service Manual describes (§3.1/§3.7): "the WCS is cycled by an
8-bit program counter (U1,U14); a 100-step control program … reset at count 99." The reverb is the
fixed point of this graph iterated over samples.

**Key timing facts to honor (netlist §6T, fig-3.4):** XFER CK = NAND(AS0, XFER, …) → result-reg
load is one instruction late; ZERO/ = NAND(MI25-gate, AS0) → accumulator clear at AS0; DAB WSTB/ =
¬MS7 → regfile write late in the cycle; DAB RSTB/ → advances the PC + reclocks the offset latch +
field registers. **The deferred overlap is the thing a sectional model cannot represent — model it.**

---

## 3. Build phases (smallest → strongest)

### Phase M3.0 — the free-run engine (no audio yet)
Add a `run_sample()` / `run_free(n_samples, input)` driver to the RTL model that sweeps the WCS PC
0→99, fetches+decodes+executes each step on the existing M2 elements, advances CPC per sample, and
carries the deferred-MAC + DMEM + DAB state across steps. Source the WCS image + offsets from
`boot8080` (CONCERT default at `0x4000` / `0x3F4D`). *Validate:* it runs 100 steps/sample for many
samples with no fault; instrument the per-step DAB driver, the active device, and the regfile/DMEM
writes; sanity-check against the microword decode of a few known steps.

### Phase M3.1 — zero-delay program (engine + I/O, NO recirculation)
The zero-delay diagnostic (SM §5.5; PGM 7) passes the input straight to outputs A & D with no DMEM.
Drive an impulse in at `RD AD/`, capture at `WR DA/`. *Validate:* the impulse comes out unchanged
(unity passthrough), one sample later — this proves the free-run engine, the 100-step loop, the DAB
routing, and the I/O boundary **without** the hard recirculation. (Reaching this program needs its
WCS image — load via the LARC program-select / diagnostic key, or hand-load the zero-delay WCS.)

### Phase M3.2 — max-delay program (the DMEM delay path)
The max-delay diagnostic (SM §5.4; PGM 8) is a ~0.5 s straight delay using DMEM. *Validate:* the
impulse reappears ~0.5 s (≈17000 samples) later — proving the DMEM write→read delay across samples
(`addr = CPC − OFST`, CPC per sample) and the DMEM recirc plumbing, still without a feedback tail.

### Phase M3.3 — CONCERT: a coherent recirculating reverb
Run CONCERT with an impulse. *Validate:* energy recirculates through the all-pass/comb structure and
**decays** (RT60 on the order of seconds; the old default-tail estimate ≈ 2.6 s) — not dead in
<10 ms (the historic "dead tank"), not growing (the historic "over-unity"). If it misbehaves,
**localize the specific net/edge** (§4) — do NOT introduce a gain knob.

### Phase M3.4 — RT60 / modulation / multi-program (→ M4)
- **Modulation:** the always-on LFO makes the offsets/coeffs time-varying (the firmware rebuilds the
  WCS lane-3 each frame; the static-WCS eigenvalue for CONCERT was measured ≈ +1100 ppm, i.e.
  slightly over-unity — modulation is part of what shapes the decay). Add the per-frame WCS update
  (re-read `boot8080`'s rebuilt WCS each sample, or model the LFO) once the static loop is coherent.
- **RT60 tracking** vs the size/decay parameter; **≥3 programs** consistent (M4); then **L7** IR
  compare to a real unit (last).

---

## 4. Validation discipline + the known failure modes (READ — this is why prior attempts failed)

**The discipline (holistic, non-negotiable):**
- **No hand-tuned gain.** The loop must close because the wires + coeffs close it. If you find
  yourself scaling a feedback path to "make it decay," stop — that hides a structural bug.
- **A failure is a specific net or edge.** When the IR is wrong, probe the model's internal nets
  against fig-3.3/3.4: which step drives the DAB, what the regfile/result-reg/DMEM hold each step,
  when XFER/ZERO fire. The bug is a mis-routed DAB driver, a mis-timed strobe, or a wrong offset —
  *localizable*, because the model is structural.
- **Verify bottom-up within M3:** engine (M3.0) → zero-delay (M3.1) → max-delay (M3.2) → CONCERT
  (M3.3). Don't debug the reverb tail before the delay path is proven.

**Known failure modes from the sectional era (now expected to be structural artifacts — watch them):**
- **"R3-clobber":** a recirc tap writes its delayed sample to register R3, and the next step (also
  WA=3) overwrites R3 before any nonzero-coeff step multiplies it → feedback lost. In the structural
  model this is a question of the *exact per-step WA/RA + DAB-WSTB timing* — model register survival
  across steps (L6.10), don't assume.
- **"Write-head trample":** write steps decode to clustered offsets that overwrite each other in the
  shared buffer. Check the actual `CPC − OFST` addresses per write step.
- **"Dead tank" / "over-unity":** the loop dies fast or grows. With modulation off, CONCERT's static
  eigenvalue is mildly over-unity (+1100 ppm) — so expect the *static* loop to sit near unity; the
  decay shape is shaped by modulation (M3.4). First get *recirculation* (energy persisting + cycling
  through the structure), then the exact decay.
- **The deferred MAC:** getting XFER/ZERO/accumulate one instruction late wrong will scramble the
  per-step values — this is precisely what single-step flushed and free-run does not.

---

## 5. Key facts, files, addresses, netlist sections

- **Build on:** `tools/aru_rtl.py` (M1 framework + `ClockEngine`), `tools/aru_rtl_dp.py` (`ARU_RTL`
  datapath; reuse the elements, add the free-run driver). `tools/aru_booth.py` (gate multiply).
  `tools/boot8080.py` (boots to CONCERT; `read_offsets(m)`; WCS at `0x4000:0x4200`, offsets at
  `0x3F4D` downward). Regression: `tools/aru_post.py` / `aru_rtl_dp.py` must still pass the whole POST.
- **WCS image:** `0x4000 + 4·step` (l0,l1,l2,l3) for step 0..127 (100 used). Default = CONCERT.
- **Netlist (`224XL_interconnect_netlist.md`):** §3.5 (PC tc_U14/U1, count@DAB RSTB/, ENT=HALT/,
  RESET@99), §6T (clock/state/strobe gen), §2T (device decode → DAB driver enables: MEMR//MEMW//
  RDRREG//RD AD//WR DA/), §4/§4F (ARU MAC + multiplier), §5 (DMEM addr=CPC−OFST + DRAM + XREG),
  §G3R (field map). **§2T device decode is the per-step DAB-routing spec** (the new free-run piece).
- **Timing (`224XL_timing_spec.md`):** fig-3.2 (MS/AS skeleton), **fig-3.4 (the deferred MAC — THE
  key for cross-instruction timing)**, fig-3.3 (DMEM read/write strobes), fig-3.5/3.6 (FPC A/D, D/A
  cycles — the I/O boundary, for when float↔fixed is added).
- **Service Manual:** §3.1/§3.7 (the 100-step signal-flow graph; the result register as pipeline
  buffer), §3.6 (DMEM, "critical path DIN = XFER CK → result reg"), §5.4/§5.5 (max-delay/zero-delay
  programs — the M3.1/M3.2 targets), §3.8 (FPC). `224XL_system_architecture.md` §6 (offset=delay,
  addr=CPC−offset, tail=loop-gain, modulation=time-varying offsets).
- **Prior records (the failure modes, now to be resolved structurally):** the memory session files
  (`224xl-session{7..11}-*`, `224xl-concert-decay-rootcause`) — for *what was ruled out*, not for
  their value-level conclusions (superseded by the netlist/holistic model).

---

## 6. Risks / honest unknowns
- **RUN-mode CPC cadence.** The CPC count-clock source is un-traced (netlist §5.1 ⚪). Single-step
  showed +1/strobe; RUN should be +1/sample (RESET@99). Confirm the actual edge before trusting the
  delay times; the zero/max-delay programs (M3.1/M3.2) will expose a wrong cadence immediately.
- **The deferred MAC + per-step DAB routing** are the genuinely new, un-POST-tested mechanisms —
  expect the first bugs here. Probe against fig-3.4 / §2T.
- **Modulation.** A static-WCS CONCERT may sit at/over unity (the +1100 ppm finding). The coherent
  *recirculation* is the M3.3 bar; faithful decay/RT60 likely needs the per-frame WCS modulation
  (M3.4). Don't fake the decay with a gain.
- **The FPC I/O.** Modeling float↔fixed (fig-3.5/3.6) is deferred; a fixed-point I/O is enough for
  the IR shape. Add the FPC when matching absolute levels / a real-unit IR.
- **Speed.** 100 steps × ~34k samples/s × seconds of IR is heavy in Python. Get correctness on a
  short run first, then vectorize the inner sample loop (or port to C) — correctness before speed.
- **No free-run hardware oracle.** POST can't reach any of this; the final word is a real-unit IR
  (or single-step port capture of a real ARU running a known microprogram) — the highest-value ask.

## 7. Ground rules (unchanged — why the project survived)
- The netlist + timing spec are ground truth for wiring/edges; don't re-derive from memory.
- The loop closes from the wiring, never from a tuned constant. "Sounds like a reverb" is not
  verification — the staged targets (zero-delay → max-delay → CONCERT) + (eventually) a measured IR are.
- Build on the verified 8080 (`boot8080`) + the M1/M2 RTL model; keep the whole POST green as the
  regression at every step.
- Flag any suspected schematic-trace gap (e.g. the RUN-mode CPC clock) for the owner rather than
  guessing — that discipline is how the SR-tap errors and the cmag=63 locus were resolved.
```
