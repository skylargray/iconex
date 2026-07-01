# Plan 020 — Phase 0.5 discriminating experiments: results + decision

**Date:** 2026-06-30. **Engine under test:** the *behavioral* free-run engine `tools/aru_freerun.FreeRunARU`
(the plan explicitly probes this cheap existing engine BEFORE the Phase 1–3 timing rebuild). **Metric:**
`tools/reverb_metrics.analyze` on the emitted `WR DA/` output only (P1), control battery TRUSTED in-process
(P5). **Scaffold:** `tools/aru_whole.py` (Phase 0.3). **Probe harness:** `tools/phase05_probes.py`.
**Stimulus:** S2 noise burst (0.30 s burst / 2.2 s total) + S1 impulse, from `tools/stimulus.py`.

> ⚠ **Everything here is a property of the BEHAVIORAL engine, not proven of the real machine.** The
> plan's premise is that this engine's MAC/XFER/operand timing is unfaithful; these results are evidence
> about *that engine* and about *where fidelity must improve*, not a verdict on the 224XL itself.
>
> ⚠ **No DSP-role labels.** Steps/blocks are described MECHANICALLY only (by what they verifiably do) —
> never "diffuser/tank/delay/allpass/feedback tap". We will not know what any block IS until a working
> reverb proves it (owner directive; provenance ledger).

## What the static CONCERT machine emits (per D/A channel; sample-and-hold = last WR DA/ per frame)
- **chC** = the sampled **A/D input, output unchanged** (step 63, RD_AD→WR DA). Verdict `DRY`. Peak = the
  input level.
- **chA, chB** = the **RDRREG→WR DA output steps (4/99)**. **DC-DEAD:** the result register `RES` at those
  steps is a flat **±2 LSB the entire run** (0/51195 samples nonzero). Those output steps carry no signal.
- **chD** = a HOLD-driver WR DA/ step (83) emitting the held DAB value — a couple of **sparse late output
  events** (~1.35–1.45 s), not a continuous dense tail.
- **Internal DMEM contents DO build and decay** over multiple seconds (RMS ≈ 2800–4200), i.e. the memory
  stores energy — but that stored energy is **disconnected from the D/A output** (see below).

## The three levers — ALL provably INERT on this engine (Δ = 0 vs baseline)
Measured on every real channel A/B/C/D separately (never a summed `mono` — an early pass mis-read a
railed mono sum as "over-unity"; the plan says measure channels separately, do not sum):

| lever (plan §) | edit | effect on D/A output | effect on internal DMEM contents |
|---|---|---|---|
| 0.5.1 coefficients | force `cmag∈{16,32}` into steps 5–23 + steps {0,1,2,3,51} | **Δ=0 (inert)** | **Δ=0** (RMS 2849.2 identical) |
| 0.5.2 modulation | per-frame LFO on the per-frame-rewritten steps [42,56,57,62–68,94] | **Δ=0 (inert)** | — |
| 0.5.3 loop-gain | scale `cmag` of steps {0,1,2,3,51} ×0.5 … ×2.0 | **Δ=0 (inert)** | **Δ=0** (RMS 2849.2 identical) |
| (control) XFER steps | `cmag=32` on the 6 XFER→RES steps {44,59,63,75,77,96} | **Δ=0 (inert)** | Δ=0 |
| (control) GLOBAL | ALL steps `cmag=0` | output changes | **contents collapse to RMS 1.0** |
| (control) GLOBAL | ALL steps `cmag=63` | output changes; every sample fires | **contents blow up to RMS 8975** |

**Reading:** the multiply/MAC path is *globally* live (all-off collapses the contents, all-max blows them
up), but **every targeted edit to the specific steps the topology hypotheses single out is individually
inert** — on both the memory contents and the output. So on this engine those specific steps contribute
≈ nothing (their operand registers are ≈ 0 when the multiply fires); the stored energy is formed by the
bulk of *other* steps and read out only as the direct input plus a few sparse late output events.

## 0.5.4 Decision (superseded in emphasis by the RES-death root cause below)
Not any of the four pre-registered branches cleanly. It is the plan's half-anticipated fifth outcome: the
behavioral engine is too unfaithful to discriminate the levers, because (1) its RDRREG→WR DA output steps
are dead (RES ≈ 0), and (2) the coefficient/modulation/gain levers are inert at the individual-step level
(live only in the blunt all-on/all-off aggregate). NOT "modulation is the lever" (inert); NOT "STOP,
nothing works" (contents form and respond globally). The follow-up probe below localizes it further.

## RES-death root cause — CORRECTED at steady state (2026-06-30) — the operative finding
> ⚠ An earlier version of this section concluded "MEMR reads and MEMW writes address DISJOINT regions →
> the loop only closes at long separations → reads return 0". **That was an UNDER-WARMING ARTIFACT** — it
> was measured ~6 ms in, but the taps are 0.3–1.6 s, so of course nothing had filled yet. The
> offset-convention probe (`tools/offset_convention_probe.py`) + a fully-warmed trace
> (`scratchpad/diag_res_death_warmed.py`, `diag_loop_closes_full.py`) corrected it. Kept visible as a
> lesson: warm the loop to steady state before reading its state.

**Corrected mechanism (fully warmed, ~2 s):**
- **The feedback loop DOES close** under the EXISTING `addr = CPC + ofst + 1 = CPC − OFST`. MEMR reads
  return large recirculated values (max |MEMR read| ≈ **9980**; step 3 reads 9805, steps 5–23 read 8007,
  step 51 reads 6353). The memory is full of recirculating signal.
- **The MAC produces large products and the result register RES holds large values MID-PROGRAM** (step 32
  → −18376, step 35/36 → +8886, step 58/62 → +8008, step 66 → −8379). The wet computation is happening.
- **But the two RDRREG→WR DA output steps read RES when it is TINY.** Step 4 (very early) reads the
  previous sample's decayed tail (RES = +2). Step 99 (very end) reads RES = +2 because **there are no MEMR
  reads after step 53** — so steps 78–98 multiply near-zero register operands, and their repeated `XFER=1`
  overwrites the large mid-program RES with tiny results before step 99 emits. The big wet RES is never
  captured at an output step.

**Offset-convention probe result (9 conventions):** the output is `DRY` under EVERY convention, and the
baseline already closes the loop internally (max |MEMR read| ≈ 9980). So **the offset convention is NOT
the lever**, and loop closure is NOT the problem.

**Operative decision:** the dead output is an **OUTPUT-CAPTURE / result-register (XFER) TIMING & GATING
problem** — *which* result the RDRREG output steps (4/99) emit — NOT the offset convention, NOT loop
closure, NOT simple loop-gain. Prime suspects:
1. **XFER gating / result-register (74F374) hold semantics.** The decode flags XFER as "bit verified;
   gating UNTESTED". Many late steps (78–98) carry `XFER=1` and overwrite RES with tiny results. If XFER
   is actually conditionally gated (so those late writes don't fire), a large mid-program RES could persist
   to step 99. This is exactly the edge-accurate XFER-CK-vs-374 timing of Phase 1, and the plan-018
   output-path work.
2. **The cmag=0 repeated-read block** (steps 5–23) and **PROT** semantics (plan 016) — still unresolved;
   they shape what the mid-program RES contains.

**Cheapest next probe (before any big rebuild):** on the existing engine, test XFER-gating hypotheses —
e.g. suppress the tiny late XFERs (or hold the result register from the last LARGE-ACC XFER) and see
whether the step-99 output emits the mid-program wet value and the tail densifies. If a specific XFER/
result-register rule revives the output, the lever is the output-capture semantics — a targeted fix, not
the full Phase-1..6 rebuild. Phase 1 edge-timing is the faithful way to settle it.

> Display caveat: the ACC column in `diag_res_death_warmed.py` prints `s16(ACC)` on a 20-bit accumulator,
> so it wraps and understates magnitude — the RES (16-bit) and MEMR-read values are exact; conclusions
> rest on those.

## Artifacts
- Scaffold: `tools/aru_whole.py` · Probes: `tools/phase05_probes.py` · WAVs: `renders/` (timestamped, P2).
- Bedrock still green: POST E32/E40/E83/E91 PASS; `reverb_metrics` control battery 10/10 TRUSTED.
