# 224XL Faithful Reconstruction Plan — eliminate every approximation

**Status:** OPEN. Created 2026-06-23 (end of Session 4). **This is the START-HERE document for the next
session.** Read it fully before touching code.

**Mandate (from the project owner, verbatim intent):** the 224XL reconstruction must be a **bit-exact,
fully-faithful** recreation. Every place the current model approximates or omits real hardware/firmware
behavior is a defect to be fixed — *not* a corner to be cut. Do not conclude "needs hardware" while any
known real element is still a stand-in.

**Why this plan exists:** the long-running CONCERT-decay investigation
(`docs/plans/224XL-concert-decay-investigation.md`) established that the booted-default CONCERT reverb (and
every long hall) **grows** at a uniform **≈ +1100 ppm/pass** in our model instead of decaying to RT60 ≈ 20 s.
Session 4 proved — by the owner tracing the actual ARU schematic nets — that the **arithmetic datapath is
faithful** (see §1), so the deficit is **not** a decode/datapath bug. It is instead masked/explained by the
fact that the analysis model **omits or approximates several real, always-on mechanisms** — above all the
**chorus modulation**. This plan fixes all of them, in order, with verification gates, so the next session
can either reproduce the hardware's decay faithfully or isolate a genuinely-irreducible gap.

---

## 0. How to use this plan

1. Read §1 (what is already CONFIRMED faithful — do **not** re-investigate these).
2. Read §2 (the approximation register — the master checklist of what's wrong).
3. Execute §3 item-by-item in the §4 order. Every arithmetic/behavioral change is mirrored in **both**
   `tools/aru_datapath.py` (Python reference) **and** `libs/sgdsp/include/sgdsp/reverb/224xl.hpp` (C++ core)
   and must keep the diff harness green (§5).
4. After each item, re-measure the CONCERT decay (`tools/exp_lambda_clean.py` for structural λ on the
   *static* image, and the new live-modulated EDC harness from Item 1) and record the result here.

---

## 1. CONFIRMED FAITHFUL — do NOT re-investigate (Session 4, schematic-traced)

The owner read the literal nets off ARU schematic 060-01318 (recorded in
`docs/reference/224/224XL ARU pinouts from 060-01318.txt`). The arithmetic datapath is now **wiring-verified**,
not inferred:

- **Accumulator = 5× 74LS163** (U45–U49), 20 bits `AC0..AC19`. Pin1 `CLR\` = **ZERO/**; pin2 `CP` =
  **ARUCKE/** (per-step clock); pin9 `L\` = GND (always parallel-LOAD); pins7/10 ENP/ENT = GND (no count).
  So each ARUCKE/ edge: `AC ← PP` (the data inputs `PP0..PP19`), **or 0 if ZERO/ asserted** (synchronous
  clear overrides load).
- **Adders = 5× 74F283** (U19–U23), ripple-carried U19→U23. **A-inputs = `AC` feedback** (bit-aligned),
  **B-inputs = `U5..U9` (74S86 XOR) outputs** (the sign-controlled product), **Σ-outputs → the sat-muxes**.
  LSB carry-in (U19 pin7) = `U2` (74S04) = **CSIGN** (two's-complement subtract). So the adder computes
  `AC + (product ⊕ CSIGN) + CSIGN = AC ± product`.
- **Saturation muxes = 5× 74F157** (U33–U37). `SEL` = **SAT** (from the `U42` 74S86 two-MSB overflow XOR);
  I0 = adder Σ (the sum); I1 = **B-IN** (the saturation constant, = `U2` 74S04 pin8 broadcast); Y outputs =
  **`PP0..PP19`**. So `PP = SAT ? B-IN : (AC ± product)`.
- **Result register = 2× 74F374** (U43/U44). D-inputs = **`PP3..PP18`**, Q-outputs = `DAB0..DAB15`,
  clock = **XFER CK**, OE = **RDRREG/**. So on an XFER step, **`RES = PP[3..18]` = exactly `PP >> 3`,
  16-bit-from-20**. (The result register reads the *combinational* `PP` bus, not the latched `AC`.)
- **Net datapath (faithful):** `PP = saturate(AC ± product)`; `accumulator ← PP` (or 0 on ZERO/);
  `RES ← PP[3..18]` on XFER; the b3/RDRREG write-back drives the **post-XFER** RES onto the DAB → DMEM.
  Register file (LS670) read-enable `GR` = GND ⇒ **read-before-write is literal**.
- **ZERO/clear timing — RESOLVED by logic, not schematic-squinting:** the multiply is **serial** (2
  coefficient bits/state × 3 states). It only produces the correct product (validated by Lexicon's own
  ADD'L MULT test vectors, which our code reproduces) if the accumulator is **not** cleared between the 3
  sub-states. Therefore ZERO/ can only assert on the **first** sub-state — i.e. "clear, *then* accumulate
  this step's product." **That is exactly the committed model** (`if ZERO: ACC=0; ACC += product`). The
  scary "sync-clear discards the product → +6755 ppm" reading is **ruled out** (it would correspond to
  clearing at the end, which would break the validated multiply).
- **Field map** (lane2: ZERO=b7, PROT=b6, RA=b5b4, b3/RDRREG=b3, XFER=b2, WA=b1b0; lane3 = 7-bit
  sign-magnitude coeff, effective `C = (mag>>1)/64`): schematic + 20-program statistics + verbatim-builder.
- **Topology:** the CONCERT band-split "halves" (s37–46 / s89–98) are **serial stages of ONE shared tank**
  (cross-half DMEM edges, 6240 shared addresses, Fig 4.1), NOT stereo mirrors. The authored ZERO asymmetry
  is legitimate. **"Variant J" is REFUTED** (overfit) — do not adopt it.
- **Parameter identity:** firmware "HFD" = **"HF Decay" = the manual's "Treble Decay"** (in-loop air-
  absorption damping, steps 40/41/92/93), NOT HF Bandwidth (= firmware "HFB", a page-2 *input* filter).

**Consequence:** the ≈ +1100 ppm structural excess is uniform across all long halls and present in the
*exact float linear map* (no rounding/saturation), so it is **not** a datapath, field-map, coefficient, or
ZERO-timing error. It is what the **static** WCS image does. The hardware never runs static — which is the
entire point of §2/§3.

---

## 2. The approximation register (master checklist)

Every item below is a place the current **analysis model** (`tools/aru_datapath.py` + the `exp_*.py`
harnesses) departs from bit-exact faithfulness. Fix ALL of them.

| # | Approximation | Affects decay? | Fix in §3 |
|---|---|---|---|
| **1** | **Modulation omitted from the audio/λ model** — runs a single *frozen* WCS snapshot; the SBC continuously rewrites the WCS (chorus + param ramps) every control tick | **YES — primary suspect** | §3.1 |
| **2** | Modulated taps read with **linear interpolation**, but firmware uses **all-pass interpolation** (engine `0xAE72`) | **YES** | §3.1 |
| **3** | LFO is an **assumed triangle at a guessed rate/depth**, not the firmware's actual waveform/rate/depth (`0x3cd3`/`0x3cd4`/`0x3ccd`, phase counters `0x3e45/46`) | **YES** | §3.1 |
| **4** | **Serial multiply collapsed** to one net op; the 3 sub-state partial products and any **intermediate saturation** are not modeled | maybe (large-signal) | §3.2 |
| **5** | **Saturation substitute value** modeled as a hard clamp; the exact sat-mux constant (`B-IN` = U2 pin8) not verified/modeled | limit-cycle only | §3.3 |
| **6** | **Native sample rate = 34130 Hz** assumed; it is an **analog LC-tank oscillator** (drifts, not crystal-derived) | shifts λ↔RT60 target | §3.4 |
| **7** | **FPC analog I/O / converters** not modeled (input = 0); the **12/13-bit converter asymmetry** (480L hazard) ignored | I/O fidelity only | §3.5 |
| **8** | Model runs a **frozen WCS**, not the live **param de-zipper / group-table** ramped image | maybe (param ramps) | §3.1 (subsumed) |

---

## 3. Detailed work items

### 3.1 Faithful live modulation + live WCS (items 1, 2, 3, 8) — **DO THIS FIRST**

**What the firmware actually does** (tech ref §7 + `docs/reference/224/224XL_modulation_lfo.md`; engine
`0xAD5C`–`0xAE9B`):
- The SBC, on a periodic control tick, rewrites selected WCS taps to **chorus-modulate** the tank.
- **Modulated taps** are per-program (tech ref §5 table, 0–18 taps). **CONCERT = s56/s57 (pair A) and
  s107/s108 (pair B), modulated in ANTI-PHASE.**
- Each modulated tap is a **fractional delay**: the LFO sets the integer offset **and** a fractional part;
  the **all-pass interpolation coefficient** is computed at `0xAE72` (`SUB 4 / AND 3 / OR 3`) and tracks the
  fractional part. The "2 extra LSBs" (packer `0xB4F0`) are this interp coeff (NOT the main multiply).
- LFO **rate** `0x3cd3`, **depth** `0x3cd4` (≈ ±47 samples), **enable** `0x3ccd` bit6; phase counters
  `0x3e45/0x3e46`. Value writes: delay at `0xAE6C`, interp coeff at `0xAE8E`.

**Faithful implementation (two valid routes — do Route A first for the decay test, then Route B for the
standalone core):**

- **Route A — frame replay (bit-exact by construction, fastest to test the decay):**
  1. Instrument the boot emulator (`tools/boot_xl.py` / `tools/aru224_emulate.py`) to **dump the full WCS
     image every modulation control tick** over a long run: per step, the offset (integer + fractional /
     interp-coeff) and coeff. This is the firmware's *actual* live modulated WCS-frame stream — ground truth.
  2. Determine the **control-tick rate** (how many output samples per WCS update) from the firmware timer /
     modulation interrupt. Record it here.
  3. Build a new audio harness `tools/exp_live.py` that runs the ARU per output sample against the
     **current** WCS frame (advancing frames at the control-tick rate), with **all-pass fractional-delay
     interpolation** on the modulated taps (see below). Re-measure the EDC/decay.
- **Route B — re-implement the modulation engine (for the standalone bit-exact C++ core):** port the
  `0xAD5C`/`0xAE72` math (LFO phase → offset + interp coeff → WCS bytes) into the core so it modulates the
  WCS itself, then verify its per-tick frames match Route A's captured frames **byte-for-byte**.

**All-pass fractional-delay read (replaces the linear interp in `exp_modlive.py`):** for a modulated tap
with integer delay `D` and interpolation coefficient `c` (from `0xAE72`), the fractional delay is a
first-order all-pass interpolator with per-tap state:
`y[n] = c · x[n] + x[n−1] − c · y[n−1]`  (x = the DMEM tap at integer delay `D`; verify the exact form and
the `c`↔fraction mapping against the firmware's `0xAE72` output — get the actual byte values, don't assume).

**Verify:**
- Route-A frames == firmware live frames (they are the same thing) — sanity-check the dump.
- The all-pass `c` values used == the firmware's `0xAE8E` writes for the same ticks (capture and compare).
- Re-measure CONCERT decay on the live-modulated model. **Record:** does it cross to decay? By how much?
  (Prior *approximate* test: growth +1.31→+0.86 dB/s — never trusted; redo faithfully.)
- Cross-check: the live-modulated model's transfer function vs the P85 / V7.2 IRs (`tools/modal_output.py`)
  should improve toward the 0.92 real-vs-real ceiling **without** any artificial filter.

**Note:** the structural-λ tools (`exp_lambda_clean.py`) measure an LTI eigenvalue and **cannot** represent a
time-varying (parametric) modulated tank. The decay verdict under modulation must come from the **EDC of the
live integer model**, not from λ. Keep λ only as the static-image diagnostic.

### 3.2 Faithful serial multiplier (item 4)

**What's missing:** the multiply is `operand × 6-bit coefficient`, done **serially** (2 coeff bits/state ×
3 states; coefficient serialized via the T&C LS195 shift registers). The accumulator is load-only (no shift),
so the **per-state shift must be applied to the operand/partial-product** on its way into the U5–U9 XORs. Our
model collapses this to one net `prod = ((operand<<3)·Cs)>>6`. The net result is test-vector-validated, but
any **intermediate saturation/overflow within the 3 sub-states** is not modeled.

**To implement faithfully, first TRACE the multiplier datapath** (still un-traced — the only ARU gap left):
the chips between the register file (LS670 outputs = the operand) and the adder B-inputs (U5–U9), i.e. the
operand register + the coefficient-gated/shifted partial-product generator. Ask the owner for the pinouts of
those U-numbers (the ones whose outputs feed U5–U9 `A`-inputs, and the operand register fed by the LS670 Q).
Then model the 3-state accumulation explicitly, including saturation **after each state** if the hardware
saturates per state. **Verify** against the ADD'L MULT test vectors (must still pass) AND construct new
large-signal vectors that would expose per-state saturation.

### 3.3 Exact saturation value (item 5)

**Trace** `B-IN` (= `U2` 74S04 pin8) to its source and the `SAT` generation (the `U42` 74S86 two-MSB XOR
on AC18/AC19 or PP18/PP19 — confirm which). Model the **exact** value the sat-mux substitutes on overflow
(it may be a sign-extended max, not a generic clamp). **Verify** the saturating limit-cycle amplitude/shape
matches the hardware's (and that the multiply test vectors that trip saturation still pass).

### 3.4 Native sample rate (item 6)

The clock is an **LC-tank oscillator** (owner-confirmed), so Fs is analog and drifts around the nominal
≈ 34130 Hz. Determine the nominal: (a) read the LC component values + the divider chain from the schematic,
and/or (b) recover the sample-timer/ARU-clock divider from the firmware (the boot sets up the timing), and/or
(c) fit it from the measured comb spacing of the P85/V7.2 IRs. This affects the **λ↔RT60 target mapping**
(`λ = 10^(−3/(RT60·Fs))`) and time-accurate output, **not** λ itself. Document the value + its uncertainty;
do not treat 34130 as exact.

### 3.5 FPC analog I/O + converters (item 7)

Model the actual input ADC and output DAC, including the **12/13-bit converter asymmetry** (480L roadmap §8
hazard). The recirculating tank is digital, so this does **not** affect the decay λ — but it is required for
a faithful end-to-end (audio-in → audio-out) recreation. Lowest priority for the decay question; required
for the final core. Refs: tech ref §12 (FPC I/O), the FPC strobes `RD AD/`, `WR DA/`, channel selects.

---

## 4. Execution order & dependencies

1. **§3.1 Faithful modulation (Route A)** — highest value; it is the un-modeled always-on element most
   likely to explain/close the decay deficit. Self-contained (needs only the boot emulator + a new audio
   harness). **Start here.**
2. **§3.2 Serial multiplier trace + model** — needs new schematic pinouts (owner) for the multiplier; model
   the 3-state multiply + per-state saturation.
3. **§3.3 Exact saturation value** — small; needs the B-IN/SAT trace (owner).
4. **§3.4 Sample rate** — independent; do anytime.
5. **§3.5 FPC I/O** — for the final end-to-end core; after the decay question is settled.
6. **§3.1 Route B** — re-implement the modulation engine in the standalone C++ core once Route A confirms
   the behavior.

After §3.1, re-assess: if the faithfully-modulated model decays at ≈ 20 s and matches P85, the central
question is **answered** and remaining items are fidelity polish. If it still grows, the residual is now a
*genuinely* isolated, fully-faithful-model excess — at which point the 480L "behavioral hardware capture"
path is justified (and only then).

---

## 5. Gates & verification discipline (unchanged, mandatory)

Every reference-model change is mirrored in the C++ core and must keep the harness green:
```
python tools/export_golden_224.py 0x01
cd tools/harness/224xl && cmake -S . -B build && cmake --build build --config Release
ctest --test-dir build -C Release            # 2/2
build/Release/diff_harness.exe golden 01     # DIFF PASSED
build/Release/mult_vectors_test.exe          # ALL PASS  (must still pass after §3.2/§3.3)
```
Validate decay against the **P85 EDC** (clean single exponential, RT60 ≈ 20 s) — never accept a
non-exponential truncation-cliff or dead-zone "decay". Modulation correctness is validated by **frame-exact
match** to the live firmware (§3.1), not by ear.

---

## 6. Definition of done

The booted-default CONCERT, run through the **fully faithful** model — live firmware-driven modulation
(all-pass fractional delay, real LFO), faithful serial multiply + exact saturation, correct sample rate, and
FPC I/O — produces a **clean single-exponential decay with RT60 ≈ 20 s** matching P85's EDC shape and HF<LF
behavior, with the diff harness green and all multiply unit tests passing, and **zero remaining
stand-ins/approximations** in the register of §2. Any element that genuinely cannot be settled without
hardware is explicitly flagged (not silently approximated).

---

## 7. Key references

- **This session's full record:** `docs/plans/224XL-concert-decay-investigation.md` (§0.10 — read §0.10.8–
  0.10.10 for the schematic-confirmation + the approximation pivot).
- **Schematic ground-truth (owner-traced nets):** `docs/reference/224/224XL ARU pinouts from 060-01318.txt`.
- **Master technical reference:** `docs/reference/224/224XL_technical_reference.md` (§2 datapath, §4
  arithmetic, §7 modulation, §12 FPC I/O).
- **Modulation engine detail:** `docs/reference/224/224XL_modulation_lfo.md`.
- **Manual (parameter functions + topology):** `docs/reference/224/224X_chapter3_operation.md`,
  `224X_chapter4_programs.md` (Fig 4.1 = Concert/Bright/Room reverb block).
- **Models:** `tools/aru_datapath.py` (Python reference), `libs/sgdsp/include/sgdsp/reverb/224xl.hpp` (C++).
- **Harnesses:** `tools/exp_lambda_clean.py` (static λ), `tools/exp_modlive.py` (the *approximate*
  modulation test to be replaced by the faithful §3.1 harness), `tools/modal_output.py` (P85 TF oracle),
  `tools/boot_xl.py` / `tools/aru224_emulate.py` (live firmware / WCS modulation source).
