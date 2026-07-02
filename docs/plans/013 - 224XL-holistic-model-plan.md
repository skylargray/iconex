# 224XL — holistic structural-model plan (the ARU+T&C+DMEM as ONE clocked machine)

> **⛔ SUPERSEDED IN PART (2026-07-01, session 0022):** the WCS **coordinate system used throughout this
> plan is wrong** — execution order is the REVERSE of the CPU image and the lanes read through the Multibus
> complement (pin-proven; 13/13 programs valid under the corrected frame). Every step-indexed claim here
> (offsets, "steps 0–99", tap lists, M3/M4 audio results) is stale. The holistic *vision* stands; the
> current execution plan is **`docs/plans/021`** (read `docs/sessions/0022 …` first).

> **Why this plan exists.** The bottom-up L1–L7 stack was right for the **8080 side** (L1–L3: CPU → boot →
> program build — cleanly layered, now ✅ VERIFIED). It was **wrong for the ARU.** The ARU + T&C + DMEM are
> not three composable blocks — they are **one machine where the interconnection and the timing ARE the
> behavior** (one shared DAB bus, time-multiplexed; a multiply/accumulate pipeline that overlaps across
> microinstructions; a feedback loop that spans the whole system over thousands of samples). Modeling them
> in sections and hand-composing the timing produced every failure we chased (the "R3 clobber," the
> "write-head trample," the loop that won't close) — those were **artifacts of sectional composition, not
> properties of the circuit.** This plan builds the ARU+T&C+DMEM as **one integrated, clock-driven structural
> model**, wired as the schematic draws it, where the reverb **emerges** instead of being assembled.
>
> **The key reframe:** in the real hardware **there is no "field map" to guess.** Each WCS output bit is a
> *wire* to a specific pin (a register's write-address input, a mux select, the adder's carry-in, the XFER
> clock gate). The owner has traced those wires. Our job is to **encode the netlist + the clock**, not to
> abstract bits into "fields" and reinvent a datapath function. The whole "is the field map 100%?" question
> dissolves: you wire the bits as drawn and the meaning is automatic.

This supersedes the **method** of `224XL-L4-L5-L6-decomposition.md` (which captured useful *facts* — pinouts,
timing, POST coverage — but the wrong *sectional method*). L1–L3 (`224XL-interp-stack.md`) stand: the verified
8080 builds the WCS bytes; this model consumes those bytes and produces audio; L7 (real-unit IR) is still the
final check.

---

## 0. Ground rules — verification discipline (NON-NEGOTIABLE; learned the hard way)

> **Why these exist.** On 2026-06-26 an "adversarial pinout audit" reported **two anomalies in the owner's
> ARU pin trace. Both were false.** The audit's 74F283 pinout came from the assistant's **training memory**
> (it had the upper bit-2/bit-3 pins transposed), and that one wrong pinout was fed into *all three* checks
> (two agents + a script) — so the "triple confirmation" was **circular**. It then **invented a "reversed
> accumulator" conclusion** from a single correctly-read pin label. The owner disproved it against the real
> datasheet (Jameco 1000766 / TI SDLS095A) and the schematic. The trace was correct all along. The rules
> below make that class of failure impossible; treat them as binding on every phase.

1. **No part spec or pinout from memory — EVER.** Every chip pinout must come from a datasheet that is
   **downloaded, rendered, read, and archived**. Pipeline that works in this environment:
   `WebFetch` the datasheet (it saves the PDF locally even when its own parser fails) → render with
   **PyMuPDF** (`import fitz`; the Read tool *cannot* render PDFs here — `pdftoppm` is missing) to PNG at
   high zoom → **Read the PNG image** → copy the datasheet into `docs/reference/224/datasheets/`. Every
   part-spec line cites its datasheet (part #, rev, page). If a part can't be verified, it is ⚪, not assumed.
2. **The schematic + the owner's traces are GROUND TRUTH for what is wired.** Document them *faithfully*.
   The assistant's job is to (a) verify the generic *part pinouts* against datasheets and (b) transcribe the
   *nets* as drawn. The assistant does **not** "correct" the owner's trace, and does not re-derive wiring
   from memory. When the model disagrees with the schematic, **the schematic wins** and the bug is in our
   model/reasoning.
3. **Do not invent conclusions.** Document what the wires say. Never label something an
   "anomaly / reversal / swap / bug" unless it is **demonstrated end-to-end by an independent check** (a POST
   pass/fail on the real protocol, a measured IR, a runnable test that fails). "It looks reversed to me" is
   not a finding — it is a signal to re-read the schematic more carefully. Bit-significance is set by the
   *consistent* wiring of a whole nibble (D-inputs **and** Q-outputs **and** the adder/mux taps together),
   never by which index label lands on one pin.
4. **Provenance + confidence on every claim** (✅ datasheet/schematic-cited · 🟡 documented, unconfirmed ·
   🟠 single-source/inferred · ⚪ unknown), so the owner can check each without trusting recall.
5. **Adversarial verification targets OUR OWN output** — hallucinated nets from crop reads, transcription
   slips, a checker's own assumptions — **not** the owner's traced schematic. (When agents read crops, expect
   hallucination; the verifier's job is to catch *us*, not to second-guess the board.)
6. **Namespace every chip by board** (`aru_`/`tc_`/`dmem_`): designators restart per sheet, so the same
   U-number is a different chip on each board (and `dmem_U6` is even two chips on one sheet).

---

## 1. Modeling level — phase-accurate RTL (not value-level, not full gate-delay)

Three choices; we take the middle one deliberately:
- ❌ **value-level / functional** (what failed): compute each block's output independently, chain them. Loses
  the bus sharing and the timing — the very things that define behavior.
- ✅ **phase-accurate RTL** (this plan): model the actual storage elements (registers, counters, latches) and
  the combinational logic between them, **clocked by the real MS/AS state machine.** Each element acts on its
  real edge (DAB WSTB at MS7, ARU CK once per AS-state, XFER CK at the next instruction's AS0…); combinational
  nets are evaluated in between. Captures the deferred/overlapping pipeline and the shared bus exactly, without
  modeling propagation delays.
- ❌ **full gate-level with delays**: every gate + ns delays + continuous-time sim. Overkill and slow.

**Behavior emerges.** We never code "the loop should close" or "the feedback is +g·delay." We wire the result
register to the DMEM data path, the DMEM read to the bus, the bus to the register file, the register to the
multiplier — as drawn — clock it, and the recirculation is a consequence of the wiring. When something is
wrong, it's a *specific wire or edge*, and it's localizable.

---

## 2. The clock skeleton (ground truth: fig-3.2, fig-3.4, fig-3.3)

This is the heartbeat the whole model runs on. **Do not abstract it away.**
- **Microinstruction cycle = 292.97 ns = MS0…MS8** (32.55 ns each), grouped **AS0=MS0-2, AS1=MS3-5,
  AS2=MS6-8** (AS1 is slightly short so MS4 doesn't clear AS0 early). (fig-3.2)
- **MC** = master clock (one pulse per MS edge). **ARU CK** fires **once per AS-state** (3×/cycle), lagging MC
  by <19 ns. (fig-3.2)
- **One microinstruction = one WCS step. 100 steps = one audio sample** → 34.13 kHz. The CPC advances **+1 per
  sample** (once per 100 cycles).
- **The MAC pipeline (fig-3.4), exactly:** within instruction *N*, the operand `F = reg[RA]` loads into the
  multiplier shift register at AS0 (`S1S0=11=LOAD`), then shifts right 2 bits per AS (`01` at AS1, AS2);
  the coefficient is consumed **2 bits per AS-state** (`C5C4` @AS0, `C3C2` @AS1, `C1C0` @AS2 → modified-Booth,
  6 bits over the 3 AS-states), producing partial products PP0/PP1/PP2. The **accumulate, ZERO, and XFER CK of
  instruction *N* happen at instruction *N+1*'s AS0** — i.e. the result is one microinstruction late, and the
  accumulator sums `0 → ±PP1 → ±(PP1+PP2)` across *N+1*'s AS-states. **This deferred overlap is the thing a
  sectional model cannot represent.**
- **Register file write = DAB WSTB at MS7** (every step). (DMEM/ARU pinouts.)
- **DMEM read latency (fig-3.3):** DOUT valid ≈ end of MS7 → through MS8 → next cycle's MS0 (a ~1-step load
  delay); "critical path for DIN is XFER CK → result register." Write strobed by WR/+CAS.

---

## 3. Build phases

### Phase 0a ✅ DONE — Verified part-spec table (`224XL_partspec_verification.md`)
Before any net is interpreted, build `docs/reference/224/224XL_partspec_verification.md`: every distinct chip
type used on the three boards (e.g. 74F283, 74LS163, 74F157, 74F374, 74S86/175, 74LS670, 74LS199, 74LS393,
74LS374, 74LS139/138, 74LS00/10/20, 74S00/02/04/08/10/74, 74LS244, 4164/4116 DRAM, the DLG30B delay module),
each with its **datasheet-verified pinout** (pin → signal), the **archived datasheet** it came from
(`docs/reference/224/datasheets/<part>.pdf`, page), and a confidence tag. **No pinout from memory.** The
netlist (0b) and the model (Phase 2) are keyed on THIS table — never on recalled pinouts. (DLG30B and any
Lexicon-custom module that has no public datasheet are marked ⚪ and characterized from the schematic + fig-3.3
timing only.)

### Phase 0b ✅ DONE — Transcribe the INTERCONNECT NETLIST (`224XL_interconnect_netlist.md`, owner-reviewed)
The piece I never built. **Faithfully transcribe** (Ground Rule 2 — document, don't editorialize) a single
**wiring table / netlist** connecting the three boards, from the owner's pin traces + the hi-res crops in
`docs/reference/224/crops/`, with every chip pin resolved against the Phase-0a part table:
- **The DAB bus** (`_dab_*`, `_rc_dab_bus`, `_p1_dab_r7`): the 16 shared data lines — every driver and every
  receiver (regfile D-in, result-reg Q-out, XREG bridge, …), and the **tri-state enable** for each (who drives
  each cycle).
- **The device decode / DAB-driver select** (`_q_u47*`, `_q_u48*`, `_q_u34A*`, `_q_NE_u49`): U47 (LS139) +
  U48 + U49C + U34A — the logic that turns `(MI16,MI17,MI12,MI13,MI4)` into bus-driver enables / DMEM
  read-write / sub-decoder selects. **This becomes the "device field" — as wiring, not a guess.**
- **The WCS-output → control-input wiring** — every microword bit's destination pin (regfile WA0/WA1/RA0/RA1,
  coefficient M1/M0 load, CSIGN, XFER CK gate, ZERO/, the offset bits → address adder inputs). **This replaces
  the L4 "field map" entirely.**
- **The PP / accumulator bus** (`_pp_*`): PP0–19, the adders (U19-23), sat-muxes (U33-37), accumulator
  registers (U45-49), product register (U10-12), the CSIGN/subtract control (U5-9 XOR).
- **The address path** (`_rc_*`, `_dab_*`, `_dmem_ov*`): CPC counter → address adder (LS283) → carry-out=bank →
  row/col mux (LS157 U36/U18) → DRAM array; the XREG latches (U38-41) bridging DAB↔DMEM DATA.
- **The clock distribution**: MC, MS0-8, AS0/1/2, ARU CK, DAB WSTB, XFER CK, ZERO/, ARUCK, DAB RSTB — which
  element each edge clocks.

**Deliverable:** a net-by-net list (`net → [(board_chip,pin), …]`, board-prefixed per Ground Rule 6) keyed on
the Phase-0a part table, **with provenance + confidence on every net** (Ground Rule 4), + a one-page block
interconnect diagram, saved as `docs/reference/224/224XL_interconnect_netlist.md`, **presented to the owner for
correction before coding.** Anything not legible on a crop or owner trace is **flagged as a gap, never guessed**
(Ground Rule 3). This is where the "look at it holistically" happens. (Owner has confirmed the ARU/T&C/DMEM
sheets show all inter-module connections; T&C and DMEM are 2 pages each.)

### Phase 1 ✅ DONE (M1) — The clock/state engine (T&C) = `tools/aru_rtl.py`
The micro-framework core (`Net` value+hold / `Reg`/`Counter`/`Latch` edge-clocked) + `ClockEngine`: per
microinstruction cycle it walks MS0→MS8 / AS0→AS2, raises ARU CK 3× (MS0/3/6), and emits the strobes
(DAB WSTB/=¬MS7, XFER CK/ZERO/ @AS0, DAB RSTB J=MS1/K=MS8) on the exact edges from §2. **Validated:**
`selftest()` reproduces fig-3.2 (ARUCK/AS0/AS1/AS2/MS) and the fig-3.4 MAC schedule bit-for-bit vs
`tools/timing/timing_spec.json`. The **microsequencer** (full WCS program counter sweeping 0–99, RESET@99) is
deferred to free-run (M3); in single-step the PC is held (ENT=HALT/ low), so the parked step re-executes.

### Phase 2 ✅ DONE (M2) — Encode each part as a structural element (as drawn) = `tools/aru_rtl_dp.py`
Each clocked chip as a small object with its real inputs/outputs and **its clock edge**, not a behavioral
shortcut:
- **Register file** 4×LS670 (U29-32): D from DAB; write addr WA, write-enable=DAB WSTB(MS7); read addr RA,
  continuous Q→multiplier operand.
- **Multiplier**: the shift register (load@AS0, shift-right-2/AS) + Booth recode (M1,M0 = 2 coeff bits/AS) +
  partial-product register (U10-12) → PP bus. The /32 scale falls out of the shift weights (F×2⁰/2⁻²/2⁻⁴…).
- **Accumulator**: adders (U19-23) + sat-muxes (U33-37, ±2¹⁸ rail) + accumulator regs (U45-49); ZERO/ clears;
  CSIGN→subtract via the XOR row (U5-9).
- **Result register** LS374 (U43/44): loaded by XFER CK from the accumulator (`sat16(ACC≫3)`); drives DAB via
  RDRREG/.
- **CPC + address adder** (LS283) + carry→bank + row/col mux (LS157) + **DRAM array** (the real 2-bank,
  bit-sliced 4164 store); **XREG** (LS374 U38-41) bridging DAB↔DATA with its clock timing.
- **Device decode** (U47/U48/U49C/U34A): produces the per-cycle DAB driver enable + DMEM r/w + sub-selects.

### Phase 3 — Wire it together & run (single-step DONE; free-run = M3)
The elements are wired via the Phase-0 nets, with the WCS bits driving control inputs directly (no field map),
and the model is driven through the firmware's single-step port protocol — passing the whole POST (Phase 4.1).
The **DAB** is one shared 16-bit net with hold-last-value when undriven (no pull resistors). **Free-run BUILT
(M3, `tools/aru_freerun.py`):** the clock runs free for N samples with the real WCS PC sweeping 0–99 +
per-cycle device-decode-selected DAB driver, capturing the **output node** (WR DA/). With the per-step DMEM
offset sourced correctly (firmware 0x3F4D buffer via `aru224_emulate.tap_map`, **not** the 0x4000 lanes 0/1 —
see Phase 4.2) the recirculating loops EXIST at ms-scale and a SHORT (~0.5 s) decaying tail emerges (dead →
audible); getting the full faithful ~2.6 s decay (the loop gain is still too low) + LFO modulation is M4.

### Phase 4 — Validate by emergence (not by hand-checking)
1. **POST as an emergent property ✅ DONE (strongest available check).** The model, driven through the
   firmware's own single-step protocol (the `boot8080` ARU ports), **passes the whole POST un-suppressed —
   latch E32 + register E40 + multiplier E83 + DMEM E91 — with nothing hand-coded** (run: `python
   tools/aru_rtl_dp.py`, and `tools/aru_post.py` for the behavioral model). Because POST is the firmware's own
   validation, this is strong evidence the wiring + datapath primitives are right. (The multiplier test forces
   the gate-level Booth, which this model has by construction.) *Correction to the earlier POST-coverage note:
   the DMEM test E91 DOES exercise the `CPC−OFST` adder at one nonzero offset (0x2000) with the CPC walking; the
   rest of L5 (offset variation, dual-use 12/13) + the free-run routing are validated structurally + by item 2.*
2. **Free-run coherence — IN PROGRESS (M3, `tools/aru_freerun.py`).** Run a program (CONCERT) for thousands of
   samples; the recirculating loop should close at a stable sub-unity decay **because the wires close it**, not
   because we tuned a gain. RT60 should track the decay/size parameter across programs. **Dead-tank root cause
   FOUND + fixed (2026-06-29):** the engine was sourcing the per-step DMEM delay OFFSET from the WRONG place —
   WCS lanes 0/1 of the 0x4000 image — which for CONCERT give clustered ~0.9–1.7 s (≈30000-sample) garbage
   delays, so DMEM reads/writes address DISJOINT regions and the loop never closes (the classic dead tank,
   already flagged in Session 11 / system-architecture doc). The REAL per-step delays live in the firmware
   **0x3F4D offset buffer**, extracted by `tools/aru224_emulate.py::tap_map(0xB800)` (the B55B builder; validated
   byte-identical to the firmware load) — step-index-keyed and aligned with the 0x4000 COEFFICIENTS[s]: step 0 =
   362 ms predelay, steps 5–23 = a VARIED 7–176 ms diffuser cluster (not 19 identical 1.7 s taps), a 176 ms
   recirc loop reused 4×. With the ms-scale offsets the feedback loops now EXIST (≈72 short write→read loops at
   1–200 ms; write/read addresses overlap) and a **SHORT (~0.5 s) decaying tail emerges** — CONCERT went from a
   *fully dead* tank (impulse → 2–4 live samples) to an audible short tail (noise burst → ~0.3 s tail; the DMEM
   buffer decays ~1.7 s). The offset SOURCE is the confirmed fix (`addr = CPC + offset[step]`, settled by the
   offset matrix: of {CPC−off, CPC+off, CPC−|off|} only CPC+off survives), wired into `tools/aru_freerun.py`
   (`concert_offsets()`). **🟡 STILL OPEN — the full ~2.6 s hall decay:** the loop gain is too low (the tail
   decays too fast), so a further cause remains beyond the offset source — quantization-to-zero / coeff scaling
   / the per-frame LFO modulation. (CAVEAT: `tools/boot8080.py::read_offsets` reads a CONTAMINATED 0x3F4D from
   the booted firmware — 576 ms vs the correct 176 ms for step 2 — so use `aru224_emulate.tap_map`.) The offset
   failure was a *specific* mis-sourced value, localized exactly as the discipline predicts.
3. **L7 — real-unit IR (last).** If/when a hardware capture exists, compare. Pass/fail only; meaningful now
   because everything beneath is structural.

---

## 4. Tooling — BUILT
The phase-accurate RTL micro-framework exists: **`tools/aru_rtl.py`** = `Net` (value + hold-last),
`Reg`/`Counter`/`Latch` (clocked on a named edge), and the `ClockEngine` that steps the MS/AS state machine
(M1); **`tools/aru_rtl_dp.py`** = the datapath elements wired on those edges (M2), reusing the verified gate
Booth (`tools/aru_booth.py`). No external dependency; the L3 WCS image + the `boot8080` port harness feed it
(`aru_post.run_post(aru_factory=ARU_RTL)`). For M3 free-run over long IRs, vectorize the inner sample loop
after correctness is proven — correctness first.

## 5. Resource map
- **Part datasheets (Ground Rule 1):** `docs/reference/224/datasheets/` — the archived, verified pinout source
  for every chip type; rendered for reading with PyMuPDF (`import fitz`, the Read tool can't render PDFs here).
  The verified table lives in `224XL_partspec_verification.md`. **This is the only source for pinouts.**
- **Master/ARU/DMEM timing:** `images/fig-3.2` (T&C), `fig-3.4` (ARU MAC pipeline), `fig-3.3` (DMEM read/write),
  `fig-3.5`/`fig-3.6` (FPC AD/DA cycles, for the I/O boundary).
- **Schematic crops (`docs/reference/224/crops/`, 236 files):** `_dab_*`/`_dmem_ov*`/`_rc_*` = DMEM+DAB+XREG+
  result-reg; `_q_*`/`_re_*` = device decode (U47/U48/U34/U49); `_pp_*` = PP/accumulator bus. Full sheets:
  060-01318 (ARU), 060-02475 (T&C, 2pp), 060-02512 (DMEM, 2pp).
- **Prose:** Service Manual §3.6–3.7 (`Lexicon-224X-Service-Manual.md`); owner-traced pinouts
  `"224XL ARU pinouts from 060-01318.txt"`.

## 6. Milestones / definition of done
0. **M0a ✅ DONE** — verified part-spec table (`224XL_partspec_verification.md`): every chip type's pinout
   datasheet-verified + archived in `datasheets/`, no memory.
1. **M0 ✅ DONE** — interconnect netlist faithfully transcribed, keyed on M0a, with provenance/confidence + gap
   list, and **owner-reviewed** (`224XL_interconnect_netlist.md`; ARU+DMEM+T&C all sheets, triple-verified).
2. **M1 ✅ DONE (2026-06-29)** — clock/state engine reproduces fig-3.2 & fig-3.4 waveforms. Built as
   `tools/aru_rtl.py` (micro-framework core `Net`/`Reg`/`Counter`/`Latch` + `ClockEngine`); `selftest()` validates
   the generated MS/AS/ARUCK/strobe waveforms against `tools/timing/timing_spec.json` (fig-3.2) and the fig-3.4 MAC
   schedule (bit-match).
3. **M2 ✅ DONE (2026-06-29)** — datapath elements wired as structural elements clocked on real edges
   (`tools/aru_rtl_dp.py` `ARU_RTL`: regfile / 3-AS multiply pipeline via `aru_booth.comb_array` / accumulator /
   result reg / CPC / DMEM addr=CPC−OFST + read-before-write / device decode). **The model PASSES the firmware POST
   single-step tests un-suppressed — E32 latch + E40 register + E83 multiplier + E91 DMEM — driven via
   `aru_post.run_post(aru_factory=ARU_RTL)`.** Single-step semantics scout-confirmed (WCS PC held; OUT 0x05=CPC CLR;
   XFER=0 read-back via the X-register). Primitives + wiring corroborated by the firmware itself.
4. **M3 — engine DONE + verified; dead-tank OFFSET-SOURCE bug found + fixed → short tail emerges; full ~2.6 s
   decay still open (2026-06-29). Plan + full status: `docs/plans/017`.** Built `tools/aru_freerun.py`
   (free-run engine; does NOT touch the POST-green
   M1/M2 files): WCS PC 0→99 (RESET@99), per-step §2T device-decode DAB routing, the **fig-3.4 deferred MAC** as
   a 1-instruction pipeline, clean signed multiply-accumulate (`sat16(ACC≫3)`), CPC **+1/sample** at RESET@99,
   DMEM recirc, I/O (inject @RD AD/, capture @WR DA/). **Verified:** M3.0 runs the whole 100-step CONCERT for
   500k+ microinstructions with no fault; **M3.1 zero-delay** (impulse→outputs A&D unchanged) and **M3.2
   max-delay** (impulse reappears exactly `delay` samples later) PASS; **M3.3 engine recirculation capability
   PROVEN** (hand-built feedback comb decays exactly per coeff, no tuned gain). `tools/render_wav.py` renders the
   free-run output to a 34.13 kHz WAV. **★ DEAD-TANK ROOT CAUSE (the big one):** the engine sourced the per-step
   DMEM delay OFFSET from the WRONG place — WCS lanes 0/1 of the 0x4000 image (`ofst=(l1<<8)|l0`) — which for
   CONCERT give clustered ~0.9–1.7 s (≈30000-sample) garbage delays, so reads/writes hit DISJOINT regions and
   the loop never closes. The REAL per-step delays live in the firmware **0x3F4D offset buffer**, extracted by
   `tools/aru224_emulate.py::tap_map(0xB800)` (B55B builder; byte-identical to the firmware load), step-index-keyed
   and aligned with the 0x4000 COEFFICIENTS[s] (step 0 = 362 ms predelay, steps 5–23 = a VARIED 7–176 ms diffuser
   cluster, 176 ms recirc reused 4×). With the corrected ms-scale offsets (`addr = CPC + offset[step]`, wired into
   `concert_offsets()`) the feedback loops EXIST (≈72 short write→read loops; addresses overlap) and a **SHORT
   (~0.5 s) decaying tail emerges** — dead tank → audible short tail (the DMEM buffer decays ~1.7 s). (CAVEAT:
   `boot8080.read_offsets` reads a CONTAMINATED 0x3F4D — use
   `aru224_emulate.tap_map`.) **Parameter hypothesis RULED OUT:** the dead tank was NOT un-recalled params — the
   full param/variation defaults ARE recalled into 0x3ca3 and baked into the WCS at load (110/128 steps built;
   Diffusion/Chorus/feedback coeffs present at boot; Mode Enhancement ON), and applying CONCERT Variation 1's
   full preset was a NO-OP; it was the offset-source bug. The param-application architecture is now FULLY TRACED
   (flat RAM array @0x3ca3, 6×5 pages; de-zipper applier 0xB000 packs ramped coeffs into 0x4000; recall at load
   0x13B6→0x13d9; see `docs/plans/017`). 🟡 STILL OPEN — the full ~2.6 s decay: with the correct offsets +
   `addr=CPC+offset` the tail decays too FAST (~0.5 s, loop gain too low), so a further cause remains beyond the
   offset source — quantization-to-zero / coeff scaling / the **per-frame LFO modulation** run inside the free-run.
   (The offset sign is settled: of {CPC−off, CPC+off, CPC−|off|} only `addr=CPC+offset` survives.) No gain knob added
   (discipline held). POST stays green. Read-before-write + deferred-MAC PROVEN INERT (toggling each leaves the
   loop eigenvalue bit-identical) — NOT the dead-tank cause.
5. **M4 (open)** — (a) pin the exact DMEM offset sign/encoding so the closed loop yields a proper decaying tail
   (not the current weak flat ~unity sustain); (b) co-simulate the per-frame WCS LFO modulation (gated by Mode
   Enhancement bit6 of 0x3ccd; engine 0xAD5C) with the free-run so CONCERT densifies into a faithful ~2.6 s decay;
   then RT60-tracking + consistent across ≥3 programs; then (if available) L7 IR match. The param-application
   chain that feeds the WCS (flat array @0x3ca3, de-zipper 0xB000, group table 0x3CF4, recall at load 0x13d9) is
   already traced — see `docs/plans/017`.

## 7. Risks / honest unknowns
- **★ Memory-derived part data (the failure that already bit us).** Stating a pinout/spec from training memory
  is the highest-severity failure: it is plausible, confident, and wrong, and it poisons everything keyed on it.
  *Mitigation:* Ground Rule 1 (datasheet → render → read → archive); never let an unverified pinout into a check,
  and never reuse one assumption across "independent" checks (that makes confirmation circular).
- **★ Inventing conclusions from a faithful read.** Even correctly-transcribed pins can spawn a false "anomaly"
  if we editorialize ("this looks reversed/broken"). *Mitigation:* Ground Rule 3 — only an independent
  pass/fail check (POST, IR, runnable test) may call something a bug; otherwise document and move on.
- **Netlist completeness:** ✅ M0 is done + owner-reviewed (ARU+DMEM+T&C, all sheets, triple-verified), and the
  whole POST passing on the netlist-faithful model is strong end-to-end evidence the interconnect is right.
  Remaining ⚪: the owner-omitted PLL (MC = the model's clock input) + the SBC-side I/O-port decode (the port
  map was scout-inferred + confirmed by POST); neither affects the datapath.
- **Sub-MS ordering within a phase** (rare race-style dependencies, e.g. read-before-write on the LS670 within
  MS7) may need care; resolve from the figures, not assumption.
- **Speed:** phase-accurate over 100 steps × 34 k samples/s is heavy in Python; correctness first, optimize
  second (vectorize, or port the inner loop to C if needed).
- **Still no free-run hardware oracle:** POST + structural fidelity + figure-matching are strong, but the final
  word is a real-unit measurement. Single-step port access to a working ARU (a lower bar than an acoustic IR)
  would let us *directly* confirm the netlist — the highest-leverage hardware ask.
