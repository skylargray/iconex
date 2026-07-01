# 0021 — The invalid CONCERT program is SYSTEMIC and reset-decode-robust (reframing the blocker)

**Date:** 2026-07-01
**Scope at start:** resolve the WCS build defect from session 0020 — trace `0xB55B` + the `0xAA40` copy
loop to find where the reset bit lands on the wrong step, per the leading hypothesis (buffer-order vs
WCS-step mismatch). Oracle: valid ⇔ RESET at step 99 and only 99.
**Scope at end:** the leading hypothesis (H1, buffer-order mismatch) is **refuted**; the defect is
**not CONCERT-specific** (every factory program builds invalid) and **not a reset-decode misread**
(exhaustively refuted, gate-level confirmed). The blocker is reframed: the firmware, booting faithfully,
places the reset bit on multiple early IO steps and never at step 99, for reasons that survive every
decode/ordering/timing/param fix we can test. Root cause narrowed to a foundational offset-field/microword
encoding question OR a missing control-head-driven load input — pending the owner's schematic knowledge or a
physical-unit dump. **No fix fabricated** (per debugging discipline + owner gate).

---

## TL;DR — the headline outcomes

1. **★ The prior leading hypothesis (H1: buffer-order/direction mismatch) is REFUTED.** The `0xAA40` copy
   loop is a **straight, order-preserving blit**: WCS step *k*'s offset field (l0/l1) = `buffer[0x3E4E+2k]`.
   Source walks `0x3F4D`→`0x3E4E` (2 bytes/step), dest walks WCS step 127→0 (4 bytes/step). No index/
   direction divergence. CONCERT step-4's reset bit is in buffer slot 4 because **B55B computed it there**,
   not because the copy mis-mapped it.

2. **★★ The defect is SYSTEMIC, not CONCERT-specific.** Building **all 20** factory programs (CONCERT,
   PLATE, CHAMBER, …) on the verified core yields **0/20 valid** — every one resets at 6-16 scattered steps,
   never uniquely at step 99. It is not credible that Lexicon shipped a unit whose entire factory set is
   invalid ⇒ the error is in our reconstruction/environment, not the firmware/ROMs.

3. **★★ No reset-decode reinterpretation rescues it — gate-level confirmed.** Exhaustive search
   (32 microword bits × 8 tcWR-definitions × 2 polarities × 5 latch-timing shifts, across 20 programs) finds
   **ZERO** combinations giving reset-at-99 (or even ≥17/20 single-reset). The netlist (§2T.1/§2T.5/§3.11)
   confirms `RESET = tcWR·OFST3/ = (MEMAC=0 & MI16=1) & (l0 bit3)`, combinational into the PC sync-clear. The
   decode is correct; the data simply never satisfies it.

4. **The reverb-processing question remains BLOCKED** (owner gate: no valid RESET-at-99 program). But the
   blocker is now understood to be **deeper and systemic**, not a CONCERT-specific `B55B` index bug.

---

## The journey arc (chronological)

### Reproduced the baseline oracle
- Faithful POST-passing boot (`aru_post.run_post(aru_factory=aru_rtl_dp.ARU_RTL)`, **POST E32/E40/E83/E91
  all PASS, no bypass**) → CONCERT WCS resets at **[4, 33, 34, 37, 47, 55, 59, 62, 66, 71]** (want [99]).
- Confirmed the two boots (faithful vs stub+PGM-2) are **byte-identical** for CONCERT ⇒ the traced stub
  build is a faithful witness for CONCERT.

### Refuted H1 (buffer-order mismatch) — the prior leading hypothesis
- Disassembled `0xAA38-0xAA4B` (copy loop 1): straight blit, `WCS[k].l0/l1 ← buffer[0x3E4E+2k]`.
- Provenance trace (`Trace8080 watch_range=0x3E00-0x41FF`): every reset-step l0 last-written by the copy
  loop (`0xAA46`); the value came from B55B's buffer, not a scrambled index.

### Refuted H4 (reset-decode misread) — exhaustively
- CONCERT-only search: no (tcWR-def × offset-bit × polarity) gives reset-at-99.
- All-20-program search (32 microword bits × 8 tcWR-defs × 2 polarities): **0 universal reset-at-99**, 0
  near-misses.
- Latch-timing shift H7 (`OFST3/` is a *latched* `MI3`, tc_U45 374 on DAB RSTB/): tested ±2-step shifts of
  tcWR and OFST3 independently → still 0 universal.
- Netlist §2T.5 line 1107: `tc_U34 g2: RESET = tcWR·OFST3/` feeds the PC sync-clear **combinationally**
  (the tc_U25 74S74 FF makes only the *delayed* `RESETD/` for DMEM, not the PC clear). §2T.1: `tcWR` =
  dec-1 1Y1 = (MEMAC=0, MI16=1) from the latched microword. **Decode confirmed at the gate level.**

### Cross-checked all 20 programs (task direction #3) → SYSTEMIC
- Ported the `boot_xl` program selector (patch `0x8160 LD A,(0xB800)` → `LD A,id`) to the verified
  `boot8080` core. Built all 20 (correct names: CONCERT HALL, PLATE, CHAMBER, …) → **0/20 valid**.
- The ROM microword table (source B55B reads, at `[0x3E01]+0x2A8`=`0xBAA8`, entry `(l0,l1,l2,l3)` base
  `0xB8AA`) itself does **not** encode reset-at-99: CONCERT ROM step 99 = `76 0B BD FF` → l0 bit3 = **0**;
  the reset bit (IO+bit3) is scattered across early IO steps in the ROM data.
- No clean single "program-end" marker bit exists in the ROM tables either (searched all 32 bits).

### Ruled out runtime & params
- Ran CONCERT **250M ticks past mainloop** into RUN: reset-count pinned at **10** the whole time (no
  convergence). Running longer is **not** the fix.
- Captured B55B's inputs right after `CALL 0xB55B`: modulation window `[0x3CD8]=1447, [0x3CDA]=6004`,
  threshold `[0x3CDC]=1447` — **sensible real delays, not garbage**. Not a "params uninitialized" issue.

### Mapped the build mechanism
- WCS = **B55B offset field (l0/l1)** + **ROM control lanes (l2/l3)** (copy loop 2 `0xAB55`, source
  `[0x3E01]+0x2A9`) + **interpreter patches** (`0xAA9F` builds an index table; patches ~36 steps' l2/l3) +
  **per-frame modulation** (`0xB310` patches a few taps' l0/l1).
- **B55B** (`0xB627` loop): reads the ROM microword table; for non-MEMW steps calls `0xB683`, which is
  range-gated (`RET nc` on `[0x3CDC]`) — it **keeps** l0/l1 for offsets below ~1447 and **recomputes**
  larger ones. This treats IO-step command words as delays. The reset-bit problem appears in **both** kept
  (ROM steps 33/34/37) **and** recomputed (steps 4/47/55/59/62/66/71) IO steps.

### Tooling limitation found (+ a retraction)
- The `power_up_id` code-patch (`0x8160`) **and** the data-patch (`mem[0xB800]`) both break the **faithful**
  `aru_post` boot (→ all-idle WCS / "DIAG ERROR"): they bypass record validation the faithful boot honors
  (the stub bypasses it via PGM-2). ⇒ non-CONCERT programs are currently only verified on the **stub** boot.
- **RETRACTED:** the mid-session "faithful ≠ stub for PLATE/CHAMBER, environment-sensitive build" claim was
  a **patch artifact** (the broken code-patch produced an unbuilt all-idle WCS), not a real difference.

---

## What is now SOLID vs SUPPORTED

**SOLID (faithful POST-passing boot, no bypass):**
- CONCERT builds **invalid** — reset at [4,33,34,37,47,55,59,62,66,71], not step 99.
- POST E32/E40/E83/E91 **PASS**; `reverb_metrics` control battery **10/10**.
- Reset decode = `tcWR·OFST3/` (gate-confirmed) and no reinterpretation yields reset-at-99.

**STRONGLY SUPPORTED (stub boot, which faithfully reproduces CONCERT byte-for-byte):**
- All 20 factory programs build invalid; no universal reset decode; the ROM microword table doesn't encode
  reset-at-99. (Only CONCERT is cross-verified on the faithful boot — see the tooling limitation.)

## Refuted / ruled out (with evidence)
- **H1 buffer-order/direction mismatch** — the 0xAA40 copy is a straight order-preserving blit.
- **H4 reset-decode misread** — exhaustive 32-bit × tcWR × polarity × latch-shift search, all 20 programs.
- **Runtime finalization** — 250M ticks, no convergence.
- **Params uninitialized** — B55B window is sensible real delays.

## Reframe of the blocker
The reset bit is systematically **not at step 99** in the built WCS for **any** program; **no** reset-decode
reinterpretation fixes it; the gate decode is **confirmed**. So the root cause is one of:
- **(a) a foundational misunderstanding of the offset-field / microword→OFST encoding** that consistently
  mis-locates the reset bit (e.g., a transform between the stored microword and the effective `OFST` we're
  not applying; or program termination is not actually via `OFST3/` on a normal WCS step), OR
- **(b) a missing program-load input/finalization** the real hardware performs during a **proper
  control-head-driven load** (not the power-up shortcut our boot uses).

This **supersedes** the session-0020 framing that localized a *CONCERT-specific* `B55B` index/ordering bug.

## ★★ LATE-SESSION LEAD (owner's idea) — the 224XL may be a 128-step program (RESET reframed)

> **⚠ REFINED LATER THIS SESSION — see Part 2.** seancostello's measured **224XL = 34.125 kHz =
> 30.72MHz/(9×100)** and dale116dot7's firmware disassembly both confirm the executed program is **100
> steps** (`reset at count 99`). The PC is 128-*capable* (7-bit), but steps 100-127 are the unused /
> 8080-NOP-staging region. So the natural-wrap "model B" below is **not** the mechanism; the reset **is** the
> WCS microword's `tcWR·OFST3/`, confirmed gate-exact from the pinouts in Part 2. Keep this section for the
> periodicity evidence (still valid), but read Part 2 for the corrected conclusion.

Owner proposed: the original 224 had 100 steps, but the **224XL revision was increased to 128**. A
decode-independent periodicity scan of the raw program storage (`period1/2/3.py`, `step127.py`, `step128.py`)
strongly supports it:
- **4-byte-per-step** and **682-byte-per-record** are the only real periods (autocorrelation); **no ~100-step
  (400-byte) period** exists. Records are adjacent 682-byte slots (0xB800, 0xBAAA, 0xBD54, …).
- The **only** non-0xFF byte constant across all 20 programs is **step 127's l1 = 0xCF** (record offset 679)
  — a shared **MEMW** final step. **Nothing at step 99 is shared.** The program-invariant marker is at the
  **128-step boundary**, not 99.
- **CONCERT genuinely uses steps 100-127** (only 14 idle of 28; real IO/MEMR/MEMW) — not shadow padding.
- The WCS PC is a **7-bit count-only counter → wraps 127→0 naturally**; a 128-step program needs no reset
  microword — the counter overflow *is* the sample boundary. Rate = 30.72MHz/(9×128) = **26.67 kHz** (the
  docs' 34.13 kHz is *derived from assuming 100 steps* — likely an original-224X figure).

**Self-consistent model (B):** the XL runs 128 steps, PC wraps naturally at 127, and `RESET = tcWR·OFST3/`
is **not** the sample boundary ⇒ `OFST3` (l0 bit3) on IO steps is a **normal offset/command bit**, and the
14 "scattered resets" are **false positives** from applying the original-224 100-step reset model. Under
this model the programs are **valid** and the blocker dissolves. (Plan-020's M3.X already ran modulus=128
end-to-end; the missing piece there was reverb *density* / output-capture, not the reset.)

**Decisive fork (needs the owner's schematic):** the netlist traces the PC clear as a single source
`tc_U14 pin1 (/CLR) ← tc_U33.pin12 = inv(tcWR·OFST3/)`. If that path is truly operative, `OFST3=1` at step 4
would still truncate the program (model A → a real 128-step encoding/build bug). If on the XL board the PC
wraps freely with that path cut/repurposed (model B), the programs are valid. **The one check:** is
`tc_U14 pin1`/`tc_U33 pin12` really driven by `tcWR·OFST3/` on the 224XL T&C sheet, or does the counter wrap
freely? That trace decides 100-vs-128 *and* whether the blocker exists. **Testable now without hardware:**
re-run the emergent-MC machine at 128-step natural-wrap (RESET ≠ WCS microword) and measure vs the reference
IR — if the tail emerges, model B is confirmed.

## Suggested next steps (priority order)
0. **★ Resolve the 100-vs-128 fork (above)** — the highest-leverage item; may dissolve the blocker entirely.
1. **Faithful multi-program boot via a proper LARC "load program N" injection** (not the `0x8160` shortcut,
   which bypasses record validation) — to rigorously confirm the systemic finding on the faithful boot.
2. **Re-examine the offset-field / microword→`OFST3/` encoding with the owner's schematic.** The gate decode
   is confirmed yet the data never satisfies reset-at-99 — is there a stored↔effective `OFST` transform, or a
   different program-termination mechanism, we're missing? (This is the highest-leverage unknown.)
3. **Investigate a control-head-driven load** (parameters/commit sequence) vs the power-up shortcut — does a
   full load change the built WCS?
4. **Physical-unit / provenance-verified WCS dump** — the ground-truth escape hatch.

## Artifacts (all analysis in the session scratchpad; NO tool/source files modified)
- `baseline_wcs.py` (oracle: faithful vs stub, byte-identity), `build_trace.py` (provenance),
  `full_program.py` (structure), `h4_search.py` / `universal_decode.py` / `latch_shift.py` (decode search),
  `program_sweep.py` / `faithful_sweep.py` (20-program sweeps), `rom_table2.py` / `rom_endmarker.py` (ROM
  table), `into_run.py` (runtime), `b55b_params.py` (B55B inputs).

## Verification state
- POST E32/E40/E83/E91 **PASS** (faithful `aru_post` boot, ARU_RTL).
- `reverb_metrics` control battery **10/10 TRUSTED**.
- Working tree **clean** on `main` — all investigation lived in the scratchpad; no source changed.

## Owner directives honored
- Booted exactly like hardware (faithful POST-passing boot; retracted a stub-boot artifact when caught).
- No speculative DSP-role labels (described steps mechanically: MEMR/MEMW/IO/idle).
- Did **not** evaluate reverb processing (no valid program exists).
- Did **not** fabricate a fix (debugging Iron Law: no fix without a confirmed root cause).

## Process lessons (banked)
- **A refuted leading hypothesis is progress.** H1 (buffer-order) was the session-0020 favorite; killing it
  cleanly redirected the search.
- **Widen before deepening.** Checking all 20 programs (cheap) converted a "CONCERT bug hunt" into a
  "systemic reconstruction error" — a far more accurate frame — before any deep B55B RE.
- **Exhaust the decode space before blaming the build.** 32 bits × tcWR × polarity × latch-shift × 20
  programs made "the decode is wrong" a settled non-issue, and gate-level docs sealed it.
- **Verify the selection mechanism on the boot you trust.** The `power_up_id` patch works on the stub but
  silently breaks the faithful boot — caught only by cross-checking, and it produced a false "environment
  sensitivity" claim that had to be retracted.

---
---

# ═══════════ PART 2 — continuation (SAME session, after the 128-step lead) ═══════════

The session ran well past everything above. Second-half arc: external ground truth (a forum archive from
people who disassembled the real firmware), a cross-ROM-**version** comparison, a **D/A output-structure**
trace, a full **gate-level trace of `tcWR` from the pinouts**, and a definitive trace of **how the IO steps'
l0/l1 is built**. Net result: the reset decode is now confirmed **exact to the gate**, the 128-step lead is
**refined to 100 steps**, the "invalid program" is reframed as **decode-noise over-counting**, and the live
question is narrowed to the **device-type / offset-field interpretation of the "IO" steps specifically**.

## ★ External ground truth — the reverb-subculture research (`docs/reference/reverb subculture/`)
Owner pointed to a distilled two-thread forum archive. Authoritative because **dale116dot7 disassembled the
actual 224 firmware** and read the 224XL service manual. Recorded as memory `224xl-reverb-subculture-research`.
- **dale (bestiary line 67, verbatim):** *"The 224XL service manual indicates the program is **100 steps**.
  However, the microcode actually could do 128 steps — **the program counter is cleared by writing an address
  with bit 3 set to the I/O space**. … not all of them actually use all 128."* → confirms BOTH our reset
  mechanism (bit-3 write to I/O space) AND the 100-step length. Larry the O (eyewitness, 1979): "100 lines of
  microcode."
- **seancostello:** 224/224X = 29.761 kHz, **224XL = 34.125 kHz** = 30.72MHz/(9×100) → arithmetic-confirms
  **100 steps**. This **refines the Part-1 128-step lead**: the PC is 128-*capable* but the program is 100;
  steps 100-127 are the 8080-NOP / staging region (the shared step-127 marker lives there, unexecuted).
- **modulation (Casey #300/#1028):** the 8080 **rewrites the WCS every sample** for modulation and "randomly
  missed some delay updates" — the 224's famed "random" Concert Hall chorus is **CPU timing jitter on a simple
  LFO**, not a hardware random LFO. 6-bit coeff = 1/32 steps.
- **topology (acreil; Dattorro/Griesinger, published + IR-confirmed):** 3 recursive allpass filters +
  cross-coupled feedback loops + modulated taps; stereo = inputs 180° apart, outputs 90° rotated. A validated
  reference to aim the reconstruction at.

## ★★ Version comparison (owner's idea) — version-CONSISTENT, and the reset count is at the NOISE FLOOR
Owner asked whether other ROM revisions "all do this." Decoded the CONCERT-array records across **224XL v8.2.1,
224XL v8.1A, 224X v8.1** (`version_compare.py`; raw-data decode):
- **Shared program ids produce BYTE-IDENTICAL reset patterns** across all three (id 0x06→16, id 0x0A→13,
  id 0x08→13, …). ⇒ the multi-reset is **not corruption and not a version regression** — it's a stable
  property of the shared microcode. (v8_1A/v8_1 order the array differently and drop a few programs.)
- **★★ The reset count sits at the random-noise floor.** A step reads "IO" when `l2&3==1` (¼) and `l0 bit3`
  set (½) → **P(IO∧bit3)=1/8 → ~12.5 expected per 100 steps from *arbitrary* data.** Observed across every
  program: 5-16, mean ~10. Confirmed empirically: scanning the **original 224 v4.3 boot code** as microcode
  produced "6-10 resets" at *every* 2-byte offset. So **"every IO-typed microword's l0 bit3 = a PC clear" is
  detecting NOISE, not a deliberate marker.** A program that truly marked one reset step would show ~1 — far
  below the ~12.5 floor. This is the pivot that reframed "invalid program" → "we over-count resets."

## D/A output-structure trace — the output is coherent; the "resets" split into signal + noise
Ran the built CONCERT WCS through the ARU engine (`da_trace.py`), capturing which steps drive the D/A:
- **Step 99 is the LAST WR_DA** (final output to channels A,B; C's last @63, D's @83) — exactly where dale's
  per-sample "final I/O-space write that clears the PC" belongs. **And step 99 has bit 3 = 0.**
- Of the 10 IO+bit3 "resets": **7 have large delay-range offsets** (0x3xxx-0x5xxx) that decode as nonsense —
  e.g. **7 separate A/D-input reads per sample** (you read A/D once). Only **3 (33,34,37)** are small,
  deliberate command words (0x045D/0x045C/0x038F) carrying bit 3; those 3 come straight from the ROM (B55B
  keeps them; it *adds* bit 3 to the 7 by clamping large offsets).

## ★★ tcWR gate-level trace from the pinouts (owner: "trace tcWR carefully per the pinouts")
Proposed hypothesis: `tcWR` is a strobe (fires once, on the real output write). Traced the full path on
**060-02475-D** — **hypothesis REFUTED:**
- **U17** (74S163, pin9 `/LD`=GND) is in parallel-load — it **latches** MI16/MEMAC on every **DAB RSTB/** edge
  and holds them the whole step. A latch, not a pulse.
- **U47** (LS139) dec-1 pin1 **`1E/`=GND — always enabled.** `1Y1`→U33→`tcWR` is a pure combinational decode of
  latched (MEMAC=0, MI16=1), **held the entire step. `tcWR` is a LEVEL.**
- **U34 g2** `RESET = tcWR·OFST3/` is a **bare 2-input AND with no timing input.** The tell: `WR XREG/` (U49)
  *is* gated by **MS7**, and the RD-AD/RD-XREG decoder (U48→U47 `2E/`) by **DAB RSTB** — but RESET has neither.
  No per-sample strobe on the reset.
- **PC clear** (U14/U1 pin1 `/CLR` ← U33 pin12 = `inv(RESET)`) is **combinational**; the registered
  `RESET/`/`RESETD/` (U25→U19) feed only the DMEM/PROT paths, not the PC.
- **New finding — the reset is pipelined one step:** U45 (`OFST3/`) and U17 (`tcWR`) both clock on **DAB RSTB/**,
  the *same* edge as the PC — so RESET from microword *k* is sampled by the PC's sync-clear at *k+1*. Shifts
  *which* step clears by one; does **not** change the count.
- **Byte→lane + field decode re-confirmed from the pinouts:** U46 (155) + ADR0//ADR1/ ⇒ `0x4000+4k+b` → step k
  lane b (l0,l1,l2,l3); `OFST3/` = U45.Q1 ← MI3 = U43 D3 = **l0 bit 3**; `MEMAC` = U17.QB ← MI17 = **l2 bit1**,
  `MI16` = **l2 bit0**. All exactly as decoded.

**⇒ the reset decode is confirmed EXACT, to the gate.** The interpretation error is therefore **not** in the
reset logic or timing — it is one level down, in the **offset-field content** of the IO steps.

## ★★ How the IO steps' l0/l1 field is built (definitive)
Traced every build pass that writes l0/l1 (`b55b_transform.py`, `l2_source.py`, `da_trace.py`, + disassembly of
B55B, both copy loops, the interpreter, `0xB510`, `0xB310`, and the post-interpreter `0xAC00-0xAD60` block):
- **There is NO separate I/O-command-word construction anywhere.** The IO steps' l0/l1 is built **identically
  to delay steps**: **B55B** reads the record's microword-table l0/l1 and runs it through a **delay-window
  transform** — keep if MEMW or below the floor (~1447); **clamp** if above the ceiling (6004); **sweep** if
  inside — then copy-loop-1 blits it to the WCS. B55B's **only** device exemption is `(l2&3)==2` (MEMW); it
  treats IO steps as delays.
- The interpreter builds a pointer/index table (reusing the 0x3E4E buffer) and patches l2/l3 + steps 78/29;
  per-frame modulation (`0xB310` +4/frame, `0xAC01` −4/frame) sweeps only the designated tap steps. **Neither
  writes IO-command words.**
- Concretely: CONCERT step 4's record l0/l1 = **`0x1F21`** (7969, above the ceiling) → B55B **clamp** →
  **`0x5489`**; bit 3 falls out of the clamp. **All 10 reset bits are a byproduct of B55B's delay clamp/sweep**,
  not deliberate markers — which is exactly why the count is version-consistent and at the noise floor.

## The live open hypothesis (owner: "that's a fair hypothesis")
The decode is gate-exact and the IO steps' l0/l1 is provably a **delay-processed value**. So the remaining
question is narrow: **for a step whose l2 says IO but whose l0/l1 is a delay-magnitude value that B55B
modulates as a delay — is that a genuine IO/output step, or is our device-type read of those specific steps
what's off?** Two branches:
- **(a)** those steps' l0/l1 genuinely *is* a delay and bit 3 there is **not** the reset it decodes as (i.e.
  they are not really `tcWR` steps), or
- **(b)** the record value at those slots / the device-type of those steps is being mis-read by us.
This is where the session paused — **next action: find out how the IO steps' l0/l1 gets built was answered
(B55B delay-transform); the follow-on is to test whether those steps are genuinely IO/output steps.**

## Reframed bottom line (supersedes the Part-1 framing)
- The **reset decode is correct to the gate** (`tcWR·OFST3/` = IO·l0bit3, combinational PC clear, one-step
  pipeline). Not the bug.
- The program is **100 steps** (dale + seancostello); the 128-step natural-wrap model is **not** the mechanism.
- The "invalid program" signal is at the **random-noise floor** and **version-consistent** — so it's an
  **over-count**: we flag ~10 IO-typed microwords whose l0 bit 3 is incidental delay data.
- The IO steps' l0/l1 is built as a **delay** (B55B), with **no I/O-command construction** in the build.
- ⇒ the real error is in **what the "IO" steps actually are / how their l0/l1 should be read** — the live
  hypothesis above.

## Updated verification state (end of session)
- POST E32/E40/E83/E91 **PASS**; `reverb_metrics` control battery **10/10 TRUSTED**.
- **No tool/source files modified** — all analysis in the session scratchpad. Tree changes on `main`: this
  session doc + memory files only.
- Memory: added `224xl-reverb-subculture-research`; crux `224xl-reset-decode-contradiction` updated with the
  systemic / decode-robust / version-consistent / noise-floor findings + the dale ground truth.

## Additional scratchpad artifacts (Part 2)
`period1/2/3.py`, `step127.py`, `step128.py` (periodicity), `version_compare.py` + inline version sweeps,
`da_trace.py` (D/A structure), `b55b_trace.py` / `b55b_transform.py` / `l2_source.py` (B55B transform + l2
source), `enum_programs.py`, `faithful_verify.py` / `sel2.py` / `patchtest.py` (boot-selection probes).

## Process lessons (Part 2)
- **The noise floor is a diagnostic.** When the "signal" (reset count) equals what random data yields, the
  interpretation is finding noise. That single measurement reframed the whole problem.
- **Own a refuted hypothesis immediately.** The `tcWR`-strobe idea was wrong; the pinout trace refuted it
  cleanly, and saying so (not forcing it) is what narrowed the search to the offset-field content.
- **Cross-version comparison rules out corruption/regression faster than any single-program deep-dive.**
- **Trace, don't interpret.** Every advance in Part 2 came from tracing the verified core / the pinouts, not
  from reasoning about what the bytes "should" mean.
