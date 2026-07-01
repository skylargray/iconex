# 0020 — Emulating the 224XL from MC, and discovering the loaded program is invalid

**Date:** 2026-06-30 → 2026-07-01
**Scope at start:** execute plan 020 (224XL complete whole-machine emulation) — build the free-running,
phase-accurate ARU+T&C+DMEM+FPC where the CONCERT reverb *emerges*.
**Scope at end:** we discovered that the CONCERT WCS program we have been feeding *every* model is
**invalid** (the hardware would reset it ~14×/sample instead of once per 100 steps), which is the real,
root reason no model ever reverberated. Along the way we replaced the asserted-timing model with a genuine
**MC-driven, gate-level T&C clock/strobe emulation** validated against the timing figures.

---

## TL;DR — the three headline outcomes

1. **★ ROOT CAUSE FOUND: the loaded CONCERT program is invalid.** The WCS RESET signal
   (`RESET = tcWR·OFST3/`, schematic-confirmed) fires at **14 steps** on our CONCERT WCS; a valid 100-step
   program (SM §3.5 + the exact 34.13 kHz sample-rate arithmetic) must reset at **exactly one** step (99).
   So every emulator we ever built — behavioral, timed, emergent — has been running a program the real
   hardware would reset 14 times per sample. **This is why the reverb never formed, in any attempt.** It is
   NOT the DSP, the timing, the MAC, the DAB, cmag=0, or the offset convention.

2. **We now emulate the T&C clock from the master clock MC.** The old model *hardcoded* the MS/AS/strobe
   waveforms and merely validated them against fig-3.2 — so any error in the assumed shapes was invisible.
   We built `tools/tc_clock.py` that ticks **MC** through the transcribed chips (tc_U56/U39/U25/U40/U38/U23/
   U20/U36/U48/U37) and the MS0–8 / AS0 / ARUCK / DAB-strobes / XFER-CK / ZERO all **emerge** and validate
   against figs 3.2/3.3/3.4. The datapath now consumes these emergent strobes; POST stays green.

3. **The reverb-processing question is BLOCKED until we have a valid program.** Owner gate: "until we get a
   program with RESET at step 99 and only step 99, we can't evaluate what's broken in the reverb further."
   The build defect is localized to the firmware WCS builder (`0xB55B` + interpreter), not the DSP model.

---

## The journey arc (chronological)

### Phase 0 — baseline + Phase 0.5 discriminating experiments (behavioral engine)
- Confirmed bedrock: `aru_post.py` POST E32/E40/E83/E91 **PASS**; `reverb_metrics` control battery 10/10.
- Built the Phase-0.3 scaffold `tools/aru_whole.py` (free-run + capture WR DA/ output only; P1/P2/P5
  enforced) and probes `tools/phase05_probes.py`.
- **First probe pass was BUGGED** (a no-op modulation probe from an empty tap filter + a railed `mono`-sum
  mis-read as over-unity). An **inertness guard** (assert probe output ≠ baseline) caught it. *Lesson:
  never trust a discriminating experiment whose knob isn't proven to move the measured node.*
- Corrected result: **all three levers (coefficients / modulation / loop-gain) were INERT** on the
  behavioral engine's D/A output. Localized: the internal DMEM field DOES build+decay, but the D/A output
  is dead — chC is dry passthrough, chA/chB (the RDRREG→WR DA "wet" path, steps 4/99) sit at ±2 LSB.
- **Under-warming trap + correction:** a snapshot ~6 ms in wrongly concluded "MEMR reads/writes address
  disjoint regions → loop never closes." A *fully-warmed* (~2 s) trace overturned it: the loop DOES close
  (MEMR reads ≈ 9980), RES holds large values mid-program, but the output steps read RES when it's tiny.
  *Lesson: warm a feedback loop to steady state before reading its state.*
- The offset-convention probe (`tools/offset_convention_probe.py`) tried 9 address conventions — all `DRY`.

### Phase 1–6 rebuild + Milestone M3.X (owner said "proceed with full phase 1 to 6")
- **Phase 1 — edge-driven deferred MAC** on `aru_rtl_dp.ARU_RTL` (`mac_step`, sequenced by the ClockEngine
  AS0 edges, persistent ACC/RES, 74LS163 sync clear). POST green; goldens 20/20; **anti-"faithfully-wrong"
  battery reproduces `aru_freerun`'s deferred MAC on 200/200 random sequences.**
- **Phase 2.0 — WCS PC modulus resolved** (netlist §3.5 + SM): a 7-bit count-only counter, WCS-generated
  RESET; default modulus 100, parameterized. **`tools/aru_freerun_rtl.FreeRunRTL`** free-runs the WCS PC
  over the datapath; oracle **identical** to `aru_freerun` on the comb AND the real CONCERT program.
- **Phase 3 — DMEM timing:** read-before-write / CPC / offset already faithful (value-identical); gate
  RAS/CAS deliberately abstracted per the performance rule (AC3). Memoized `_booth_product` (hot path).
- **Milestone M3.X (2×2 + the NEW modulus=128 + modulation-on-107–119):** **NO cell WET-PASS/DENSE.** The
  full timing-faithful model is numerically identical to the behavioral engine on CONCERT → **timing is
  definitively not the lever.** Plan says STOP Phase 4–6; owner honored the STOP.
- **Output-capture investigation:** XFER-gating (8 hypotheses) + PROT (3 hypotheses) — **all INERT.** The
  dead output survives every dynamics-level fix.

### The MC pivot (owner: "what is generating MC?" → "generate MC, run everything from it")
- Answer: **nothing was generating MC.** `aru_rtl.ClockEngine` hardcoded the MS/AS/strobe tuples; MC was
  never modeled. The "phase-accurate / pixel-validated" claim only ever checked the *asserted* shapes.
- Built **`tools/tc_clock.py`** — ticks MC through the real chips; MS0–8, ARUCK, AS0, DAB WSTB//RSTB,
  XFER CK, ZERO/ **emerge** and validate vs figs 3.2/3.3/3.4. Then rewired `ARU_RTL` to an `EmergentClock`
  (edges DERIVED from MC), and added a **sub-slot 74LS163+74F374 MAC** (`mac_step_subslot`) where
  capture-before-clear *emerges* from the synchronous-clear semantics. POST + oracle stayed green.

### The RESET-decode investigation (the payoff)
- Building the PC counter forced the question: *when does RESET fire?* Decoding it on CONCERT: **step 4**,
  not 99. Owner confirmed the schematic path (MI3 → U45 → OFST3/ → U34B → RESET) and that tc_U34 is a
  2-input LS08. So the decode is correct — and it fires at step 4.
- **The sample-rate proof:** 30.72 MHz ÷ (9 MS × 34130 Hz) = **exactly 100 microinstructions/sample** ⟹
  RESET must fire once per 100 steps = step 99. SM §3.5 confirms verbatim ("100-step program, reset at
  count 99, RESET generated by the WCS itself"). Contradiction with step 4 ⟹ the program is invalid.
- **Trace harness (verified kosarev core):** the live WCS resets at 14 steps; step 99 doesn't reset; the
  offsets are firmware-computed in a **0x3F00 working buffer (51k writes)** and pushed to the WCS.
- **Into-RUN trace (40M ticks past mainloop):** still invalid; step 99's offset byte *oscillates* (treated
  as a modulated tap, not a fixed reset).
- **Clean-boot test (owner: "are we bypassing diagnostics?!"):** yes — `boot8080` uses a STUB ARU that
  FAILS POST, then injects a PGM-2 "skip diagnostics" key. But the **faithful-ARU boot** (`aru_post.run_post
  (aru_factory=ARU_RTL)`) PASSES POST, **0 DIAG errors, no bypass** — and produces a **byte-identical
  invalid WCS.** So the bypass was NOT the cause; the invalid program is deterministic under a faithful boot.
- **Verified 0xB800 = CONCERT** (directory @0xA446 entry `01 01 01 96 01`, name @0xA002 "CONCERT HALL",
  record 0 of the 0xB800 array; ROMs complete). Source data ruled out.
- **Build trace:** step 4's lane0 (`0x89`, bit3 set) is copied verbatim from the `B55B`/0x3F4D buffer by a
  copy loop @`0xAA40`; the interpreter (@AB63/AB67) writes only lane2/lane3 for I/O steps — it never
  overwrites lane0/lane1. The reset bit is **on the wrong step** (step 4, not 99) ⟹ the offset/command
  values land on the wrong WCS steps. Defect localized to the `B55B` build.

---

## Key technical findings

### About the machine (durable facts)
- **MS4 is an ACTIVE-LOW net** — it *is* tc_U56's QD (high 8/9 slots), driving only the two active-low
  inputs tc_U56 /LD and tc_U23 /CLR. fig-3.2 draws the active-high state (= NOT the net). Any logic that
  treated MS4 as active-high one-hot was wrong.
- **ARUCK rises ~0.3 MS into the slot** (fig-3.2 rise-lag), so ARUCK-clocked outputs (AS0) settle mid-slot
  and gate in the *next* integer slot. Needed for AS0 to match fig-3.2.
- **XFER CK = NAND(AS0, XFER, ARUCKE/)** — the third term `tc_U25.pin9` is **2Q of the ARUCKE FF = ARUCKE/**,
  NOT the "unused-FF constant" an earlier probe assumed. That ARUCKE/ gate IS the ~20 ns "XFER CK lags
  ZERO/" mechanism. Capture-before-clear is *structural* (163 sync clear lands one ARUCKE/ edge after XFER
  captures), and it reproduces the deferred MAC 300/300.
- **CSIGN JK (tc_U20 FF2):** J = AS0·MI23, K = AS0·/MI23 → never both 1 → a registered pass-through of MI23
  during AS0, no cross-instruction deferral. Byte-identical to the direct `csign = MI23` bit. Faithful.
- **WCS PC:** 7-bit count-only counter (tc_U14/U1, /LD tied high), sync-cleared by a WCS-generated RESET;
  the program sets its own length via a reset microword.
- **RESET = tc_U34 g2 = AND(tcWR, OFST3/)**, tcWR = (MEMAC=0, MI16=1) via U17→U47, OFST3/ = MI3 = l0 bit 3;
  PC /CLR = inv(RESET). Schematic-confirmed by owner.
- **WCS load mapping is straight:** SM §3.5 — U46 decodes the low 2 SBC-address bits to select one of the
  four 128×8 RAMs, so `0x4000[4k+b]` → WCS PC step k, byte b (l0=MI0-7 … l3=MI24-31).
- **Sample rate:** 34.13 kHz = exactly 100 microinstructions × 292.97 ns; one RESET per sample.
- **Offsets are firmware-computed:** `B55B` step-builder → 0x3F4D buffer; a copy loop @0xAA40 transfers the
  offset field (lane0/lane1) into the WCS for all 128 steps; the interpreter @0xAA9F writes lane2/lane3.

### About our emulation (state of the model)
- The **MC-driven clock/strobe generation** (tc_clock.py) is emergent + figure-validated.
- The **MAC timing** (163 sync-clear + 374 load) is emergent (mac_step_subslot).
- The **datapath value computation** (adders, saturation, regfile, CPC, offset arithmetic, DMEM DRAM, DAB
  tri-state, device decode, FPC) remains **behavioral/abstracted** — see
  `docs/reference/224/224XL_asserted_vs_emergent.md` for the full subsystem audit.
- **POST still runs on the atomic `_multiply`, not the sub-slot MAC** — POST validates the multiply value +
  DMEM, not yet the emergent sub-slot timing.

---

## Resolved questions
- **Why did no model reverberate?** Because the loaded CONCERT program is invalid (resets 14×/sample). Not
  the DSP/timing/MAC/DAB/cmag=0.
- **What generates MC?** Previously nothing (hardcoded waveforms). Now: `tc_clock.py` ticks MC through the
  real chips; the whole clock skeleton emerges and validates vs the figures.
- **Is the asserted MS/AS/strobe timing correct?** Yes, at the edge level — the emergent edge schedule is
  logically identical to the old asserted one (which is why POST never broke). But it hid MS4-active-low,
  the ARUCK rise-lag, and the ARUCKE/-gated XFER CK.
- **Is timing the lever for the missing tail?** No (Milestone M3.X: timed == behavioral output).
- **Is the PGM-2 diagnostic bypass corrupting the program?** No — a clean faithful-ARU boot (POST passes,
  no bypass) gives a byte-identical invalid WCS.
- **Is 0xB800 the right CONCERT record?** Yes — verified via the firmware name table + directory + ROM.
- **Is the WCS load mapping straight (0x4000[k]→PC k)?** Yes — SM §3.5 + live content.
- **CSIGN JK, PC-modulus mechanism, RESET decode, MS4 polarity** — all resolved (above).

## Open items / blockers
- **★ THE BLOCKER: obtain a valid RESET-at-99 program.** Root defect: `B55B`'s per-step offset/command
  values land on the *wrong* WCS steps (reset bit on step 4, not 99). Unknowns:
  - Where exactly does the `B55B` buffer index / the 0xAA40 copy-loop direction diverge?
  - Is the interpreter *supposed* to overwrite lane0/lane1 for I/O steps (and doesn't in our emulation)?
  - Is this an emulation bug in the build, or a genuine misunderstanding of the record/build?
- The `224XL_asserted_vs_emergent.md` "behavioral/abstracted" cells (datapath value computation) remain to
  be gate-leveled *if* a future audio discrepancy demands it (Phase 5/6 — currently gated off).
- POST does not yet run on the emergent sub-slot MAC (retire the atomic `_multiply`).
- The de-facto CONCERT reference IR (`IR/Lexicon 224XL/Concert Hall V1.1.L.wav`, RT60 ≈ 2.5 s) remains the
  structural benchmark once a valid program runs.

## Suggested next steps (in priority order)
1. **★ Single-step `0xB55B` and map each buffer write to its intended WCS step.** Log every offset-buffer
   write with the step index it targets, and compare against the 0xAA40 copy loop's downward walk. Find
   where the index/direction diverges. Oracle: *valid ⇔ RESET at step 99 and only 99.* This is the
   prerequisite for ALL further reverb work.
2. **Check whether the interpreter should write I/O steps' lane0/lane1.** If the real firmware overwrites
   the offset field for I/O steps with the true I/O command, our emulation may be missing that branch.
3. **Cross-check against a different program.** Build a structurally simpler program (e.g. a plate) and see
   whether *it* comes out with RESET-at-99 — isolates whether the defect is CONCERT-specific or systemic.
4. **Physical-unit / provenance-verified WCS dump** — the ground-truth escape hatch if the build RE stalls.
5. Once a valid program exists: re-run the whole emergent-MC machine (tc_clock + sub-slot MAC + FreeRunRTL)
   and the Milestone metric on it — everything is built and waiting.

---

## Artifacts created / modified this session
**New tools:** `aru_whole.py` (scaffold), `phase05_probes.py`, `offset_convention_probe.py`,
`xfer_gate_probe.py`, `aru_freerun_rtl.py` (FreeRunRTL), `milestone_m3x.py`, **`tc_clock.py`** (MC-driven
clock/strobe emulation + `EmergentClock`).
**Modified:** `aru_rtl_dp.py` — Phase-1 edge MAC (`mac_step`), memoized `_booth_product_cached`, sub-slot
MAC (`mac_step_subslot`), wired to `EmergentClock`; `aru_freerun_rtl.py` uses the sub-slot MAC + xfer/prot
hooks.
**Docs:** `docs/reference/224/224XL_phase05_probe_results.md`, `224XL_milestone_m3x_results.md`,
`224XL_asserted_vs_emergent.md`.
**Memory:** `224xl-phase05-levers-inert`, `224xl-milestone-m3x-done`, `224xl-no-speculative-role-labels`,
`224xl-emulate-from-MC-whole-netlist`, `224xl-reset-decode-contradiction` (the crux).

## Verification state (all green except where noted)
- POST E32/E40/E83/E91 **PASS** (on both the behavioral `aru_post.ARU` and the RTL `ARU_RTL` with the
  emergent clock + sub-slot MAC).
- `reverb_metrics` control battery **10/10 TRUSTED**.
- Phase-1 edge-MAC faithfulness **200/200**; sub-slot MAC vs deferred MAC **300/300**.
- `tc_clock.py` emergent MS0–8 / ARUCK / AS0 / DAB WSTB//RSTB / (ZERO/ vs XFER CK) **all match** figs
  3.2/3.3/3.4.
- Working tree on `main`; nothing committed (owner chose to stay on main).

## Owner directives captured (standing guidance)
- **No speculative DSP-role labels** (diffuser/tank/delay/allpass/feedback-tap/wet-output) until a working
  reverb proves them — describe mechanically only.
- **Emulate the WHOLE netlist from MC** — nothing asserted. Validate emergent signals against the figures.
- **Boot exactly like normal hardware** — a faithful POST-passing boot with no diagnostic bypass; don't
  trust anything produced by a degraded boot.
- **Don't evaluate reverb processing until we have a valid program** (RESET at step 99 and only 99).

## Process lessons (banked)
- An **inertness guard** catches no-op experiments. **Warm feedback loops to steady state** before reading
  state. **The clock figures are the check, the netlist+MC is the source.** **A confident conclusion on an
  unvalidated foundation is worthless** — the RESET decode exposed that the entire reverb effort ran on an
  invalid program. The single most valuable move was following the owner's insistence on booting exactly
  like the hardware and emulating from MC — it is what surfaced the real blocker.
