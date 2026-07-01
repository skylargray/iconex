# Plan 020 Milestone M3.X — go/no-go result (2026-06-30)

**Question:** does the CONCERT reverb tail EMERGE on the timing-faithful, free-running model?
**Answer: NO.** Per the plan's pre-registered decision table this is the "**nothing densifies**" branch →
**STOP Phase 4–6; re-open the cmag=0/PROT + output-capture semantics (plan 016).**

## What was built and verified (Phases 1–3, all green)
- **Phase 1** — edge-driven deferred MAC on `aru_rtl_dp.ARU_RTL` (`mac_step`, sequenced by the
  `aru_rtl.ClockEngine` AS0 edges; persistent ACC/RES; 74LS163 synchronous clear). POST E32/E40/E83/E91
  PASS; `_multiply` goldens 20/20; edge-MAC == `aru_freerun.product20` 4000/4000; **1.5 anti-"faithfully
  wrong" battery: reproduces `aru_freerun`'s deferred MAC on 200/200 random sequences.**
- **Phase 2** — `aru_freerun_rtl.FreeRunRTL` free-runs the WCS PC over the datapath on real edges. PC
  modulus RESOLVED (§3.5 + SM): 7-bit count-only counter, WCS-generated RESET ("normally reset at count
  99"), default modulus=100, **parameterized**. Oracle: FreeRunRTL == `aru_freerun` IDENTICAL on the comb
  AND on the real CONCERT program (all channels). POST inherited unchanged → still PASS.
- **Phase 3** — the audio-relevant DMEM timing (read-before-write: old→DAB before the new write; CPC
  +1/sample at RESET; addr=CPC−OFST) is already faithfully modeled in FreeRunRTL and PROVEN value-identical
  to the behavioral engine. Per the plan's performance rule, the **gate-level RAS/CAS/refresh sequencer is
  deliberately abstracted** (it does not change the audio VALUES, only refresh/timing margins) — recorded
  as an AC3 documented abstraction. E91 PASS.

**Key structural fact:** the full Phase-1..3 timing-faithful model is **numerically IDENTICAL to the
behavioral `aru_freerun`** on CONCERT. `aru_freerun`'s statement order already matched the edge order for
the recirculation-relevant timing, so the rebuild adds fidelity but **no divergence** — which by itself
shows timing is not the lever.

## The milestone 2×2 (reverb_metrics on the emitted D/A output; S2 burst; control battery TRUSTED)
| cell | config | verdict |
|---|---|---|
| A100 | timed, static, modulus=100 (== behavioral baseline) | **DRY** (chC = A/D input passthrough) |
| A128 | timed, static, modulus=128 (steps 100–127 execute — NEW) | **DRY** |
| C128 | timed, modulated, modulus=128 (LFO on taps 107–119 + ≤99) | **DRY** (chC) + peak-5 tonal chD = nothing |

`aru_freerun` hardcodes NSTEPS=100 and thus **could not** test modulus=128 / the 107–119 modulation;
FreeRunRTL can, and it still does not densify. So even the one genuinely new capability the rebuild
unlocked does not produce the tail.

## Decision (plan-faithful)
The plan states, verbatim: *"if 'nothing densifies,' STOP and re-open cmag=0/PROT (plan 016) — do not push
on to Phase 4–6."* Milestone = nothing densifies → **STOP.** Phases 4–6 (full gate FPC / gate ARU back-end
/ resolved DAB bus) are COMPLETENESS work that cannot change this outcome, because the model is already
value-identical to the behavioral one and the output death is upstream of them.

**The operative root cause (Phase 0.5 + confirmed here):** the RDRREG→WR DA output steps (4/99) read a
result register that the late microprogram steps (78–98, near-zero operands, repeated XFER=1) have
overwritten to ~0 before the output fires. The large mid-program RES values (±8000–18000) are never
captured at an output step. This is **microword/output-capture semantics** (XFER gating "untested" in the
decode; cmag=0/PROT unresolved, plan 016) — NOT MAC timing, NOT DMEM timing, NOT the offset convention,
NOT loop closure (all ruled out).

## Output-capture investigation (post-M3.X, owner-directed) — hypotheses systematically ruled out
After M3.X the owner directed chasing the output-capture death rather than building Phase 4–6. Findings
(all on `FreeRunRTL`, CONCERT, S2, reverb_metrics on the emitted output; tools: `xfer_gate_probe.py` +
the PROT probe; `FreeRunRTL` gained optional `xfer_gate` + `prot_mode` hooks):

- **XFER-CK gating (netlist §G3T):** XFER CK = NAND(AS0, XFER, **tc_U25.pin9**). The third term is an
  **"unused"-FF output** (§3.11 says tc_U25 FF-2 is unused) → provisionally a tied constant, i.e. XFER
  fires on every XFER bit (the faithful default). Tested 8 alternative gating rules (only-cmag>0, only
  MEMW, only compute, not-IO, only-MEMAC, not-idle, only-RDRREG-driver): **every one → DRY.** XFER gating
  is NOT the fix.
- **PROT (MI22, effect UNTRACED in the netlist):** tested PROT suppressing {ZERO clear, DMEM write,
  regfile write} on PROT=1 steps: **every one → DRY.** PROT (as these effects) is NOT the fix.

**Cumulative elimination — the wet output stays dead under ALL of:** wrong MAC timing (M3.X: timed ==
behavioral), offset/address convention (9 conventions), loop-not-closing (the loop DOES close, MEMR reads
≈9980 warmed), XFER-gating (8 rules), PROT effects (3 rules). The chC dry passthrough (peak = input) and
the dead wet channels are invariant to every tractable simulation-side hypothesis.

**Conclusion:** the missing tail is NOT reachable by any correction to the *dynamics* of the current
decode. What remains are provenance/structure questions the simulation cannot settle: (1) whether the
0x4000 snapshot is the actually-running program (vs a firmware-modified/`0x3F4D` build), (2) whether the
wet output is even routed through steps 4/99·RDRREG, (3) the cmag=0 semantics (plan 016). These are the
**L7 ceiling** — they need the physical unit or a provenance-verified WCS/IR dump, not more simulation.

## Next investigation (replaces Phase 4–6)
Resolve WHY the output steps read a dead RES / what the cmag=0 + PROT + XFER-gating semantics actually are.
Candidate: the real result-register hold / XFER-gating rule differs from the decode's assumption, OR the
output path emits a value the current §2T decode mis-routes. This likely needs the physical unit or a
provenance-verified WCS/IR dump to settle definitively (the L7 ceiling). Artifacts: `tools/milestone_m3x.py`,
`tools/aru_freerun_rtl.py`, `tools/aru_rtl_dp.py` (Phase-1 edge MAC), `tools/test_phase1_edgemac.py`.
