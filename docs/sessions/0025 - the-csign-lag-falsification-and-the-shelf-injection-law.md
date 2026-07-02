# 0025 — The CSIGN-lag falsification and the E83 polarity anchor

**Date:** 2026-07-02 (same day as 0023/0024)
**Scope:** the crossover band-inversion hypothesis from session 0024 §7 (owner-directed).
**Result:** two mechanism candidates tested. (1) The wiring-motivated CSIGN one-edge lag on pairC:
derived, implemented, **FALSIFIED by the documented-defaults oracle** (registry #23) — own-sign at
every pp is now falsification-tested. (2) The byte-level lever anatomy + a localization A/B then
exposed the real suspect: **the free-run engine's GLOBAL cs_eff convention (~stored bit7, chosen
by fiat in 0023 when "both polarities looked stable") contradicts the E83-anchored POST model
(`aru_post`: CSIGN = stored bit7 direct, 1=positive, 20/20 firmware goldens bit-exact).** A global
flip is invisible to every double-negation oracle and to |loop-gain| (broadband RT60) — but it
inverts every state recursion's per-frame sign alternation (z=+0.875 lowpass ↔ z=−0.875
HF-alternator), i.e. WHICH BAND each cell shapes: the complemented convention IS the crossover
band-inversion. Engine flipped to the E83-anchored convention; verdicts in §6.

---

## 1. The pairC sign-window derivation (and why it was worth testing)

The sub-XOR row (§4.6) + negation carry-in (§4.3/§4.5) apply CSIGN/ combinationally between the
product register and the adder — the sign at each accumulate edge is whatever the JK holds THEN.
The JK reloads at slot-3.0 (AS0-gated, samples pre-load Q4 = w_{n−1}'s MI23), so its window
[3.0(n), 3.0(n+1)) covers **ppC(w_{n−2})@4.43(n)** + ppA(w_{n−1})@7.43(n) + ppB(w_{n−1})@1.43(n+1):
taken literally, pairC of every word is signed by its SUCCESSOR. 0023's "all three pps carry that
word's own sign" contradicted its own edge numbers for pairC — and no oracle covered it (D1 words
are cmag=32 → pairC = ±1 residue; POST is single-step; the combs used same-sign words; the D3
CSIGN pin stream is sampled inside the window). A sign-context census of the settled CONCERT image
made it live: **25 of 47 pairC-carrying words sit in opposite-sign contexts**, concentrated on the
MID ladder + shelf words.

Settle physics splits the two pairC consumers (the same ~1.4-slot adder propagation that defers
the ACC): the 3.06 capture (0.06 slots after the flip) must still see the own-sign sum; the 4.43
register add (1.43 slots) is marginal. Implemented as `RTL22(csign_lag=True)`: capture = own sign,
register = live (next word's) sign — with a term-exact self-test pinning both variants.

## 2. The falsification

All control-path oracles are blind to it, as predicted: POST green, **D1 16/16 unchanged**,
**D3 374/376 unchanged** under the lag. The arbiter was the documented-defaults render:

| settled CONCERT (chA) | LF(<720) | mid(>720) | broadband | verdict |
|---|---|---|---|---|
| own-sign (0024) | 1.48 | 1.90 | 1.90 | WET-PASS/DENSE |
| live-sign register (lag) | **1.03** | **0.82** | **0.82** | **INDETERMINATE/TONAL** |
| benchmark (real unit) | 2.85 | 1.92 | 1.99 | — |

The live-sign register add drains the loop across every band — the factory program is exquisitely
pairC-sign-sensitive, so own-sign producing the coherent 1.5–1.9 s bank is itself affirmative
evidence. **Resolution:** the control path defers one AS exactly like the data path (fig-3.4
again) — a control flip at 3.0 has not propagated through the settle-limited adder by 4.43 either;
the effective sign at every consumer is the one loaded an AS earlier = **own-sign at every pp**.
The JK-window puzzle and the settle constant are now one consistent story, falsification-tested.
Engine restored (`csign_lag=False` default), **bit-identical to the 0024 reference digests**;
the falsified variant + its term-exact split test stay in the file as the registry-#23 regression.

## 3. The lever byte anatomy — the apply law is JOINT and SIGN-BEARING

Byte-level decode of the d2b2 lever captures (each vs its predecessor state; movers 56/57/107/108
change every capture = LFO phase, ignore):

- **LOW** rewrites lane 3 of **w43/w95 only**: cmag 5→19 at 0xF0; slider 0x02 = the recall value
  (cmag 5) — the documented preset sits at the low end of the LOW slider's range. Offsets never
  move: LOW is a pure injection-GAIN lever. The engine shows **no LF response 5→19** — the
  inertness is at the byte level, not the apply chain.
- **MID rewrites w43/w95 TOO — lanes 2+3, including stored bit7 (the CSIGN source!)** — plus
  w44/w96 (the B/D output words, cmag 11→30) and the ladder (62-68/113-119). At MID-lo
  (mid decay driven long): w43/95 → cmag 10, **cs flips 0→1**.
- **HFD** at 0x02 recomputed the whole ladder as well (16→1 / 24→32) and zeroed w43 — the WCS
  coefficients are compiled from SEVERAL sliders jointly (per-stage damping = f(MID, HFD); the
  shelf = f(LOW, MID)). The June one-slider-one-wordset map was the marginal view from the
  default state; the raw JSONs stand, the independence assumption dies.

**The apply law for the shelf injection (w43/w95):**
| parameter state | w43/95 |
|---|---|
| recall preset (LF 3.0 s > Mid 2.0 s) | cmag 5, **cs=0** |
| LOW→0xF0 (LF driven longer) | cmag 19, cs=0 |
| MID-lo (Mid ≫ LF) | cmag 10, **cs=1** |

The stored sign encodes WHICH side of the crossover outlives the other — a ± shelf correction
around the mid-band recirculation, exactly the structure the documented "LF Decay vs Mid Decay"
pair requires. The engine's rendering of the recall bytes (cs=0 → negative MAC of the
0x100/0x102-cell state) measures as an LF CUT (model LF < mid; real unit LF > mid).

## 4. The injection chain, mechanically (no role labels)

Execution order (left half; right half mirrors at 95-98/0x102-0x103):
w46 (row 81, MEMR @CPC−0x2B27, cmag 4, XZ) → w45 (row 82, MEMR @CPC−0x0101, cmag 28 — reads the
cell written one frame earlier) → w44 (row 83, IO RDRREG WR-DA ch D, cmag 11, XZ) → w43 (row 84,
MEMW @CPC−0x0100, cmag 5 — writes the row-84 capture back to the cell) → … → w41 (row 86, MEMR
@CPC−0x0107, cmag 10, XZ). The 0x100-0x107 offsets are a chain of one-frame-recirculating DMEM
cells — the band-shaping filter bank. The w45 pole word (cmag 28 ⇒ one-pole 691 Hz ≈ the
documented 720 Hz crossover) has pairC = residue (28&3=0): the POLE is sign-window-insensitive;
the injection gain/sign (w43/95) is the parameter-bearing term.

## 5. The injection-sign A/B → the global polarity suspect → the E83 anchor

`d2g_injection_sign.py` (settled + LOW-hi images vs the same with ONLY stored bit7 flipped on
words 43+95, complemented-convention engine):

| image (chA) | LF(<720) | mid(>720) |
|---|---|---|
| settled (cmag 5) | 1.48 | 1.90 |
| settled + flip 43/95 | 1.52 | **2.69** |
| LOW-hi (cmag 19) | 1.48 | 1.69 |
| LOW-hi + flip | (unfittable) | 1.12 |

**The injection works entirely in the MID band under either sign** — the 0x100/0x102 state cell
holds a spectrally wrong component. Hand-tracing why: under the complemented convention the
state recursion w45 renders as `state[n] = −0.875·state[n−1] + …` — a pole at **z = −0.875**, an
HF-alternator — instead of `+0.875` = the one-pole lowpass whose corner (fs·ln(32/28)/2π = 691 Hz)
is the documented 720 Hz crossover. One GLOBAL sign flip fixes the pole and re-sorts every cell's
band — and it turned out the anchor already existed: **`aru_post.ARU.decode` uses
`CSIGN = (l2>>7)&1` (stored-direct, 1=positive) and passes the firmware's own E83 golden product
table 20/20 bit-exact** — the strongest hardware oracle in the project (the goldens are ROM-stored
signed products the real unit checks against its own ARU at every boot). Session 0022 recorded
stored-direct; the complement crept in during the 0023 port ("the Multibus line level") and
survived because every output oracle is blind to a global flip: D1's unity gain (double
negation), POST, the combs, broadband RT60 (|g| unchanged), D3 (line-level pin streams). The
engine now uses `cs_eff = stored bit7` with the E83 rationale in the docstring; the encoder
`csign` argument is WYSIWYG (1 = positive). The self-test programs were re-signed to preserve
intent — exposing, along the way, that the factory's opposite-sign idiom is residue-load-bearing
(P20(x,32,1) = 8x+3; the input word's −3 residues cancel it exactly).

## 6. Results and verdict (E83-anchored convention)

All prior oracles green post-flip, as the blindness analysis predicts: self-tests ALL PASS
(test programs re-signed; the passthrough/comb exactness turned out to REQUIRE the factory's
opposite-sign residue cancellation — P20(x,32,1) = 8x+3, the input word's −3 cancels it),
POST green, **D1 16/16**, **D3 374/376**. The band-resolved documented-defaults oracle — the only
one that could see the convention — transforms:

| chA (settled) | 250 Hz | 500 | 1k | 2k | 4k | 8k | LF(<720) | mid(>720) | broadband |
|---|---|---|---|---|---|---|---|---|---|
| complemented (0023/0024) | 1.46 | 1.36 | 2.02 | 1.73 | 1.63 | **1.86** | **1.48** | 1.90 | 1.90 |
| **E83-anchored** | 3.18 | 3.30 | 2.76 | 2.47 | 2.01 | **1.57** | **3.75** | 2.31 | 2.94 |
| benchmark (real unit) | 3.29 | 2.95 | 2.48 | 2.15 | 1.83 | 1.51 | 2.85 | 1.92 | 1.99 |
| documented | — | — | — | — | — | — | 3.00 | 2.00 | 2.60 (avg) |

**The octave ladder now descends monotonically like the real unit's; LF > mid > 8 kHz exactly as
documented; the 8 kHz damping lands within 4% of the benchmark; broadband sits at the documented
2.6 average (+5-12%).** Cross-checks: run40M independently agrees (LF 3.29/3.18, mid 2.29/2.25,
8k 1.50); the D2b formal gate scores 3/4 PASS (settled-chA LF 3.75 = +25%, the one miss — the
frozen-LFO phase spread on the LF band is ±0.4 s across captures). The residual is a fairly
uniform +10-20%, in the direction the static-image approximation predicts (d4lite re-run pending).

**The levers (d2g under E83):** settled LF 3.75 → **1.79 with the 43/95 sign flipped** (boost↔cut,
the apply law's semantics working); **LOW at cmag 19 → LF 7.50/5.66 s** — the LOW lever is alive
and heads toward its documented 70 s range end. The 0024 §7 finding ("LOW moves words 43/95 but
LF doesn't respond") is RESOLVED.

**The modulation replay closes most of the residual** (`d4lite_mod_replay.py` under E83 — the
firmware's own LFO trajectory hot-swapped per frame):

| | LF(<720) | mid(>720) | broadband |
|---|---|---|---|
| static settled | 3.75/3.30 | 2.31/2.28 | 2.94/2.72 |
| **live-modulation replay** | **3.20/3.21** | **2.22/2.17** | **2.67/2.59** |
| documented | 3.00 | 2.00 | **2.60 (avg)** |
| benchmark IR | 2.85 | 1.92 | 1.99 |

**LF within 7% of documented, mid within 11%, broadband average within 3% — with zero parameters
tuned.** The plan-022 D2 documented-defaults mission is, in substance, closed; the formal close-out
(true interleaved co-sim, LFO-phase statistics) is D4.

**New floor signature:** the deterministic idle limit cycle under E83 is **DC-dominated**
(A/B/C/D ≈ +27/+13/−14/+18 LSB DC ≈ the RMS; −62…−68 dBFS) vs the old zero-mean ±2.5 LSB. This
is why raw-burst `reverb_metrics` verdicts read INDETERMINATE/TONAL post-flip — the floor, not
the tail (floor-subtracted band fits unaffected; registry #16 discipline now mandatory for
headline verdicts). On hardware the D/A DC would vanish in the output coupling; as a bench
prediction it is another convention discriminator.

## 7. Registry additions

| # | Item | Verdict |
|---|---|---|
| 23 | CSIGN one-edge lag on pairC (live-sign at the 4.43 register add / 3.06 capture) | **DEAD** — collapses CONCERT to a 0.8 s TONAL husk under the documented-defaults oracle; own-sign at every pp is falsification-tested; the control path defers one AS like the data path (`RTL22(csign_lag=True)` + `_test_csign_split` = the pinned variant) |
| 24 | One-slider-one-wordset parameter map (June) | DEAD as an independence assumption — the apply chain compiles WCS coefficients from several sliders jointly (w43/95 = f(LOW, MID) incl. the SIGN lane; ladder = f(MID, HFD)); raw sweep JSONs remain data |
| 25 | cs_eff = ~stored bit7 (0023's "Multibus line level" complement) | **DEAD** — contradicts the E83-anchored POST convention (`aru_post` stored-direct, 20/20 firmware goldens); the complemented convention WAS the crossover band-inversion (z-pole sign of every state recursion). A global flip is invisible to D1/POST/combs/broadband-RT60/D3 — only band-resolved decay against the documented presets could see it |

## 8. Verification state

- Engine restored to own-sign default; self-tests ALL PASS (incl. the new `_test_csign_split`
  pinning both schedules term-exactly); `d1b_regression` digests **bit-identical to 0024**.
- Under the falsified variant, for the record: POST green, D1 16/16, D3 374/376 (all blind, as
  the derivation predicted) — the documented-defaults render was the only oracle with teeth.
- New probes: `d2g_injection_sign.py`; scratch: shelf structure + census + lever byte anatomy
  (session transcript).

## 9. Verification state and next

**Verification:** engine `aru_freerun22_rtl.py` @ E83-anchored cs_eff (stored bit7 = 1 = positive);
self-tests ALL PASS (incl. `_test_csign_split` pinning both pairC schedules and the registry-#23
variant); POST green; D1 16/16; D3 374/376; fs re-measured under the new convention:
**s = 1.000 → 32,508 Hz unchanged**, autocorr first peak now EXACT (124.9 ms both). d2f/d2g/d2b
WAVs in `renders/`.

**Next:**
1. **D4 modulation co-sim** — the remaining uniform +10–20% decay excess is the static-image
   approximation's direction (d4lite re-run pending in this session's log); the co-sim is now the
   quantitative close-out for D2b's last gap (and the chorus).
2. **ARU §5.7 datapath signature co-sim** (diag-3's 0x0D10 XREG pump) — the per-pin lock on the
   whole MAC arithmetic including the E83 convention and the PP-bus capture, at hardware pins.
3. **The variation oracle** (cheap): the ± apply law predicts w43/95 sign+cmag per documented
   variation preset (V2 1.7/1.7 and V4 3.0/3.0 equal → minimal injection; V3 3.8/2.4 → boost);
   needs variation-select key injection in the boot harness.
4. **D2d documented ranges** — unblocked in substance (the levers work: LOW cmag 19 → LF 7.5 s
   toward the 70 s end); formalize once D4 tightens the absolute calibration.
5. ~~D2c cross-program re-run under E83~~ **DONE at close — the anomalies resolve wholesale**
   (settled images, chA, floor-subtracted): **PLATE 1.74 s vs documented 1.8 (was 3.52 — gone)**;
   **CHAMBER WET-PASS/DENSE 2.18 s, peak 9072 (was near-silent peak 5 — its recirculation was
   destroying itself under the inverted convention)**; RICH PLATE now WET-PASS 2.60; CD PLATE B
   1.51 (doc 1.8); CONCERT 2.77; halls/splits 1.7–3.7; effects behave as effects (CHORUS&ECHO
   0.37). Remaining INDETERMINATE/TONAL flags (ids 4/12/18) = the DC-floor confound on raw-burst
   metrics — floor-subtracted tails healthy. Of the original D0 anomaly set {3, 8, 12, 20},
   only id 3 (the invalid selector) remains excluded, correctly.
6. The DC-dominated idle floor: add floor-subtraction to the headline metric path (registry #16
   now mandatory); bench prediction if a unit ever shows up.
