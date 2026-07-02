# 022 — 224XL: known-answer oracles (D1/D3) and parameter state (D2)

**Status:** READY TO EXECUTE (written 2026-07-02 at the close of session 0023).
**Read first:** `docs/sessions/0023 - the-rtl-arbiter-answered-the-accumulator-pipeline-and-the-first-tail.md`
(the answered alignment + the engine), then plan 021's banner. The engine of record is
**`tools/aru_freerun22_rtl.py`** — every render in this plan goes through it. Trust 0023 > 0022 > everything
older; the technical_reference's *interpretation* layers (offset/ctl/coeff column decodes, "FPC bit15"
readings) are pre-0022 and VOID — its **firmware addresses, ROM block locations, and dispatch chains are
disassembly facts and remain good**.

**Mission.** The tail exists (WET-PASS/DENSE ×4ch, RT60 1.9 s boot / 1.4 s run vs the 2.5 s benchmark).
Now LOCK the model with absolute, frame-independent oracles and close the parameter loop:
- **D1** — the firmware's own diagnostic delay programs (7 = ZERO DELAY, 8 = MAX/0.5-s DELAY), built by
  ROM and fully specified by the SM: *Left in → outputs A and D; Right in → outputs B and C*; program 8
  interposes ~0.5 s of DMEM delay, program 7 none. End-to-end: firmware builds the WCS, the engine runs
  it, the audio does exactly that. Tests build+decode+I/O+output with none of CONCERT's complexity.
- **D2** — drive the real parameter system (LARC sliders → firmware apply chain → WCS bytes) and
  re-measure: the param→RT60 transfer on the RTL engine, the setting that reproduces the 2.5-s benchmark
  IR, and the D0 anomalies (ids 3/8/12/20). Replaces the void June-era transfer-function readings.
- **D3** — SM §5.7 signature analysis: compute HP-5004A signatures from the engine's free-running pin
  streams and compare against the digitized per-pin tables. Hardware-grade verification at named pins.

---

## 1. Ground truth (established; do not re-derive)

### 1.1 The engine and its alignment (session 0023 — the full table is in the 0023 doc §1)
Frame = L+1 steps (fs = 30.72e6/9/(L+1); CONCERT 32,508 Hz; L=99 → 34,133 Hz). Write-through operand
(SR loads post-MS7-write at slot-0.58 of the next step). Accumulator one ARUCKE/ edge behind the PR
(pps of W land 7.43(W+1)/1.43(W+2)/4.43(W+2)). XFER capture at 3.06(n) iff w_{n−1}.XFER = MAC through
ppB(w_{n−2}); ZERO clear at 4.43(n) iff w_{n−1}.ZERO deletes exactly the missed pairC (effective
coefficient into a capture = cmag − (cmag&3)). CSIGN JK carries each word's own sign; cs_eff = ~stored
bit7; both polarities stable. ACC wraps mod 2²⁰. Deterministic Booth-residue floor ±2.5 LSB RMS
(−82 dBFS) — impulse metrics read it as TONAL; use bursts or subtract the zero-input render (c3 method).
POST stays green via the untouched single-step path.

### 1.2 D1 anchors (all already in the repo)
- **SM ch.5** (`docs/reference/224/Lexicon-224X-Service-Manual-chapter-5.md`): the diag menu table —
  1 RESTART, 3 ARU SIGNAT, 4 ARU test, 5 NVS strobe, 6 FPC SIGNAT, **7 ZERO DELAY, 8 MAX DELAY** —
  and the known answers verbatim: both "Left input passes to outputs A and D, and Right input passes
  to outputs B and C"; 8 = 0.5-second delay-line through DMEM, 7 = 0 seconds, no DMEM.
- **Firmware dispatch (disassembly facts, tech-ref §12):** SBC1 `0x032D` `JP 0x11BE` over the table at
  `0x0330`; item 7 → handler **`0x0EFD`**, item 8 → **`0x0EF4`**; both call the WCS builder **`0x0F2C`**
  (fill 0x4000-0x41FF with 0xFF-NOPs; reverse-copy ROM 4-step blocks `0x0F5F` → CPU steps 124-127 (LEFT)
  and `0x0F6F` → steps 74-77 (RIGHT); patch step 29 = the reset word ⇒ L=99, 100-step frame; then
  OUT 0x01 + OUT 0x03 = RUN). ZERO DELAY additionally patches the offset low bytes of the two output
  steps (0x4130/0x4131 → step 76; 0x41F8/0x41F9 → step 126).
- **LARC key injection** is a solved harness problem: keys are serial bytes on the 8251 (ports
  0xEE/0xEF); PGM-2 = 0x30 press / 0x10 release (`boot8080.py`); `param_sweep.py`/`boot_xl.py` already
  inject slider values into the running firmware.
- `tools/_diag3_wcs.bin` (2026-06-24) = a captured **diag WCS image** — decoded structure (25 IO words,
  XREG traffic) identifies it as the **diag-3 ARU-SIGNATURE stimulus program**, proving diag WCS capture
  worked before; the same capture route serves D1 (and D3).

### 1.3 D2 anchors
- **The parameter system is disassembled** (`224XL_param_sweep.md`): sliders at `0x3C00-0x3C05`; main-loop
  scan `0x8185` diffs vs `0x3C16+`; handler `0x85F2`; type scaling via `0x3C33`; apply path `0xADxx`
  walks the `0x3CF4` group table (built by interpreter `0xAA9C`); de-zipper ramps the WCS bytes. CONCERT
  slider labels (NVS2 @0x9CDE): `LOW MID XOV HFD DEP PDL`.
- **Sweep harness + data exist**: `tools/param_sweep.py` (inject grid 0x20..0xFF per slider, wait for
  de-zipper, read WCS) + per-program JSONs `docs/reference/224/224XL_param_sweep_*.json`. The June-era
  *interpretation* of those sweeps (coeff/delay transfer functions) is void; the raw byte captures and
  the modulation-target findings (pairs (56,57),(107,108) sweep ~±47 samples; ladder lane-3 pairs
  modulated sum-preserving) are data and stand.
- The RUN-state CONCERT image (`wcs_run_concert.json`) renders RT60 1.4 s vs boot 1.9 s — parameter
  state moves the tail, as required.
- **Benchmark:** `IR/Lexicon 224XL/Concert Hall V1.1.L.wav`, RT60 ≈ 2.5 s (structural target).

### 1.4 D3 anchors
- **Digitized tables:** `docs/reference/224/224-signature-value-tables.md` — per-pin 4-char signatures
  for T&C / ARU / DMEM / FPC, firmware V8.2.1 (same version as our ROMs).
- **Setups (SM ch.5 §5.7):** T&C: START=STOP=RESET (U19 pin 9 = RESETD/), CLOCK=DAB RSTB/ (U20.6).
  ARU: START=RESET/ (ext-16), STOP=XFERCK (U43.11), CLOCK=ARUCK (U10.11); second setup START=STOP=RESET/.
  DMEM: START=STOP=CPC MSB (U65.8), CLOCK=RESET/ (U58A.1). Stimulus = the signature diag programs
  (3 = ARU/T&C-side, 6 = FPC) — diag 3's WCS is already captured (`_diag3_wcs.bin`).
- **The analyzer:** HP 5004A — 16-bit LFSR with the standard HP polynomial (feedback taps at stages
  7, 9, 12, 16), data XORed in at CLOCK edges between START and STOP, displayed 4 hex-ish chars from
  the alphabet `0123456789ACFHPU`. Implement + self-test against a published known vector first.

## 2. Dead-end / discipline registry (additions from 0023)
Everything in plan 021's registry stands EXCEPT #1/#2 (CSIGN bimodality — dissolved; both polarities
stable on the RTL alignment). New entries:
| # | Item | Verdict |
|---|---|---|
| 13 | Clear-owner = w_n ("no-lag" Q6 sample) | DEAD — renders identically zero (c2) |
| 14 | Clear landing at the 1.43 edge | DEAD — captures would always read a just-cleared ACC |
| 15 | Same-edge ACC (PR latch + accumulate in one edge-group) | DEAD — this was the 22-session DRY bug; fig-3.4's "one AS behind" is load-bearing |
| 16 | Impulse-stimulus metric verdicts on this machine | CONFOUNDED by the residue floor — use bursts or floor-subtraction |
Also: pre-0022 interpretation layers in `224XL_technical_reference.md` §12 (FPC bit15 tables, offset/ctl
column decodes) are VOID as *readings* — the raw bytes and ROM addresses in them are good.

## 3. Phase D1 — the diagnostic delay oracles ★ first
D1a. **Capture the diag WCS images.** Boot the verified core to the mainloop (e1_sweep pattern), then
     reach the builders. Two routes, in preference order:
     (1) *direct-call patch*: after mainloop, redirect execution to handler `0x0EFD` / `0x0EF4` (the
     0x8160-selector-patch idiom — patch a jump or drive PC directly on the emulated core) and let the
     ROM builder write 0x4000-0x41FF; capture both images (they must differ ONLY in the four patched
     offset low bytes — a built-in checksum of the route);
     (2) *LARC menu route* (fallback + more faithful): inject the diag-menu key serial codes (find the
     codes next to PGM-2's 0x30/0x10 in the key-scan disasm; the menu is documented in SM ch.5).
     Cache both images in `tools/session0022_probes/wcs_diag.json`.
D1b. **Stereo input support in the engine.** The diag programs read L and R in opposite half-frames
     (fig-3.5). Extend `RTL22.run_sample`/`run_free` to accept per-frame `(inL, inR)`: RD-AD steps in
     execution order alternate halves (first read → half-1 channel, second → half-2). CONCERT behavior
     with mono input must be unchanged (regression: re-run c1 checksums).
D1c. **Run the known answers** (through `program_rows22` + the engine, no byte interpretation):
     - ZERO DELAY: L-only stimulus → outputs A,D ≈ stimulus (scaled), B,C ≈ 0; R-only → B,C live, A,D ≈ 0.
       Measure channel separation (>40 dB) and through-gain; document the observed L/R↔half mapping.
     - MAX DELAY: same routing with a single dominant echo at ~0.5 s (the SM's number; measure the exact
       frame delay and reconcile with the patched offsets and fs = 34,133 Hz — expect ≈ 17k frames).
     - Both: POST stays green; the diag frame must extract as L=99/100 steps.
     **Pass = the plan-021 D1 oracle is closed.** Fail = the failing stage (build vs decode vs engine
     vs FPC routing) is isolated by construction — fix before touching D2/D3.

## 4. Phase D2 — parameter state (the RT60 gap + the D0 anomalies)
D2a. **Re-sweep on the live firmware** (param_sweep harness): for CONCERT, sweep `LOW` and `MID`
     (the decay sliders) over the grid, capture settled WCS images (de-zipper wait as before), and
     **render each through the RTL engine** → the real param→RT60 transfer curves (c5 method,
     floor-subtracted, burst). Locate the slider settings whose render matches the benchmark IR's
     2.5 s; render that setting and compare early pattern + decay shape against the benchmark
     (structural comparison — NED, block-RMS envelope — not bit-exact).
D2b. **XOV/HFD sanity**: one sweep each; verify monotone spectral effects (HF decay ratio) — this is
     the first time the transfer functions are measured through the true machine.
D2c. **The D0 anomalies**: for ids 3 (FAIL), 8 (near-silent), 12/20 (indeterminate): capture their
     RUN-state images (the e3j RUN-capture pattern: run N ticks past mainloop, snapshot 0x4000) and/or
     sweep their first sliders; re-render. Classify each as (a) boot-state artifact (parked taps /
     muted input — CONCERT's own boot image had parked taps), (b) needs-modulation (see D4), or
     (c) genuine engine discrepancy (→ STOP and investigate before proceeding).
D2d. Update `224XL_param_sweep.md` with the RTL-frame re-reading (band the old interpretation with a
     supersession note; keep the raw JSONs).

## 5. Phase D3 — §5.7 signature analysis (hardware-grade lock)
D3a. **Implement the analyzer**: 16-bit HP-5004A LFSR (taps 7/9/12/16), gate on START/STOP, sample the
     probed net at each CLOCK edge, display map `0123456789ACFHPU`. Self-test on a known vector
     (construct one by hand or use a documented HP example) before use.
D3b. **Emit pin streams from the engine.** Add a probe layer that exposes, per step (and per slot where
     needed), the modeled nets: PC0-6, MI0-31, OFST0-15/, stage-1/stage-2 outputs, CSIGN/, M0//M1/,
     DAB0-15, MS/AS/strobes, CPC bits, RESET//RESETD/. The T&C setup (CLOCK = DAB RSTB/ = once per
     step, window = RESETD/-to-RESETD/ = one frame) needs only per-step values at the slot-0 edge —
     already modeled. The ARU setup (CLOCK = ARUCK = 3×/step) needs the per-AS values — also modeled.
D3c. **Run diag 3's WCS** (`_diag3_wcs.bin`, re-captured fresh via the D1a route for provenance) on the
     engine free-run; compute signatures for every table pin the model exposes; compare to
     `224-signature-value-tables.md` (T&C table first — the most completely modeled module). Score:
     match / mismatch / not-modeled per pin. **Every mismatch names its net — this is the per-pin
     falsifier for anything still wrong in the model.**
D3d. Stretch: the DMEM table (CLOCK = RESET/ = per-frame, window = CPC-MSB half-cycle = 32768 frames —
     long but cheap at ~5k frames/s) and the FPC table (needs diag 6 + the FPC codec path).

## 6. Phase D4 (stretch) — the modulation co-sim (plan-021 C4, carried)
Only after D1-D3: interleave the verified 8080 (~62 CPU ticks per 105-step frame — the 0022 measured
budget) with the RTL engine so the live LFO writes land mid-stream; render CONCERT and listen for the
chorus; compare tap-sweep depth against `224XL_modulation_lfo.md` + the param-sweep modulation findings.
This also retires the run-state-snapshot approximation (one frozen LFO phase) used since 0022.

## 7. Verification rules (unchanged + additions)
- No audio claim except as a `reverb_metrics` verdict (battery in-process) on an emitted stream with the
  WAV on disk. Burst stimulus or floor-subtraction for anything near the residue floor (registry #16).
- POST green at every phase (untouched single-step path).
- Tank statements use ENERGY (RMS²·N).
- Every probe's final message states which registry entry it would re-open, if any.
- D1's channel-routing claim requires BOTH polarity runs (L-only AND R-only).
- D3 signature mismatches are findings, not failures — each names a net; investigate top-down
  (clock/window definition first, then the net's model).

## 8. Facts that will save time
- The diag builder writes DOWNWARD from 0x41FF (reverse copy) — lane order lands [l3,l2,l1,l0]; do not
  hand-decode the ROM blocks — capture the BUILT image and extract with `program_rows22` like any program.
- Diag frame: reset at CPU word 29 ⇒ L=99 ⇒ 100 steps ⇒ fs = 34,133 Hz (dale's rate).
- The two diag images differ in exactly 4 bytes (0x4130/31, 0x41F8/F9) — use as a capture checksum.
- Program-id patch (0x8160) does NOT reach the diag programs (ids 7/8 in the record array are empty
  slots — different namespace from the diag menu).
- The engine does ~4,700 frames/s; a full 8-point × 2-slider D2 sweep with 4.5-s renders ≈ 25 min —
  budget accordingly, run in background, cache aggressively (wcs images keyed by slider state).
- `process_wav_rtl.py` (session 0023) processes arbitrary WAVs through any cached image — use it for
  listening checks (it resamples, drives at −6 dBFS, floor-subtracts, normalizes; stereo A/C out).
- The residue floor is a predicted physical signature (−82 dBFS deterministic idle pattern per program)
  — if a real unit is ever on the bench, it is a one-measurement model check.

## 9. Artifacts
- Engine: `tools/aru_freerun22_rtl.py` (+ the D1b stereo-input extension, kept regression-clean).
- New: `tools/session0022_probes/wcs_diag.json`, `d1_diag_oracles.py`, `d2_param_rt60.py`,
  `d3_signatures.py` (+ the LFSR module), updates to `224XL_param_sweep.md`.
- Records: session doc 002x per session; plan-021 banner already points here for the remaining items.
- Superseded-but-useful: `224XL_technical_reference.md` §12 (addresses good, readings void);
  June param-sweep JSONs (raw data good).
