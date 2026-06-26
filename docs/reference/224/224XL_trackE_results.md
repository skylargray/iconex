# Track E.4 — Adversarial Gate on the Track E Reverb Reconstruction

**Date:** 2026-06-26 · **Owner:** Skylar Gray · **Scope:** Apply Track F skepticism to the Track E result (`tools/aru_datapath2.py`, `tools/build_concert_program.py`, `tools/aru_e3_sweep.py`).

**Cardinal rule recap:** success is NOT "it makes sound." Success is a recirculating loop that closes at a *stable sub-unity gain*, an RT60 that tracks SIZE/decay monotonically for the *right reason*, a smooth exponential-ish decay, and consistency across programs. We never fit-to-taste.

## Verdict

**PARTIAL — a coherent decaying reverb was NOT demonstrated, but the negative result is GENUINE, not an artifact of a bad gain.** The validated OFFSET/coeff/SIZE *spine* is real and SIZE-monotonic; the per-microword loop-closure *wiring* (WA/RA/XFER/ZERO/device) is unresolved, and with the derived wiring the loop is **over-unity, clamped by hardware saturation** — a rising-then-rail-pinned envelope, not a decay. The Track E author correctly refused to hand-tune a feedback gain to manufacture an RT60.

## 1. Genuineness — was closure hand-tuned?

**No hand-tuned gain exists.** The only signal-path scaling in `aru_datapath2.py` is the principled coefficient bridge:

```python
def cmag_to_cs(cmag, csign):      # line 47-50
    mag = round(cmag / 127.0 * 32)    # 7-bit /127 record gain -> engine /32 rep
    return -mag if csign else mag     # cmag=127 -> cs=32 = unity
```

The engine multiply is the owner-validated `prod = (racc_in<<3) * cs >> 5` (`aru_datapath.py:169`), i.e. exactly the `/32` hardware scale, untouched. The smoothing window (`W=64`) and `-60 dB` threshold (`speak/1000`) are on the **measurement** side of `rt60()`, never the signal path. There is no damping factor, no feedback-gain knob, no fudge constant.

**The loop is over-unity — re-derived independently from the decoded coefficients.** The recirculation feeds delay-line address **6835**. SIX microwords read that same address, with decoded gains:

| idx | slot | cmag | gain |
|----:|-----:|-----:|------:|
| 0 | 108 | 124 | +0.976 |
| 2 | 119 | 63 | −0.496 |
| 3 | 115 | 63 | −0.496 |
| 31 | 74 | 63 | −0.496 |
| 37 | 111 | 95 | −0.748 |
| 38 | 104 | 95 | −0.748 |

Signed sum = **−2.008**; Σ|gain| = **3.96**. A round-trip loop gain of |2.0| cannot close sub-unity. Confirmed by the impulse response: energy **rises** from ~11k to ~785k and **pins** there. That plateau is **89% of the full saturation ceiling** (32767 × 32 XFER steps = 1,048,544); the ±2¹⁸ (`sat20`) accumulator clamp is the *only* thing preventing runaway. That is the textbook signature of an over-unity loop, not a sub-unity reverb tail.

> **Conclusion:** closure was not fitted; it genuinely does *not* close. The over-unity is a real consequence of the unreconciled wiring lumping 6 coeff taps onto one recirc address.

## 2. RT60-tracking — right reason or coincidence?

**RT60 does not track because no RT60 exists.** Reproduced SIZE sweep (CONCERT HALL, cce 0x00..0xFF):

| cce | recirc(ms)* | peak | decay_ratio | T_eff |
|-----|------------:|-----:|------------:|------:|
| 0x00 | 32.7 | 377854 | 0.673 | inf |
| 0x40 | 45.9 | 261100 | 0.755 | inf |
| 0x80 | 100.1 | 261116 | 0.688 | inf |
| 0xC0 | 150.2 | 259582 | 0.761 | inf |
| 0xFF | 200.3 | 261114 | 0.698 | inf |

`decay_ratio` is **flat in the 0.67–0.87 marginal band** at every SIZE; `T_eff` is **infinite at 0/9 sizes**. There is no decade of decay to fit, so RT60 cannot track anything.

What *does* track is **delay-line DEPTH**: filtered to the spine's 46 referenced slots, the deepest read delay is perfectly monotonic **233.5 → 266.9 → 325.3 → 375.4 → 433.8 → 483.9 → 533.9 → 592.3 → 634.1 ms** across cce 0x00..0xFF. (Caveat: this monotonicity *requires* the referenced-slot filter; over all 128 tap_map entries the deepest delay is non-monotonic, 623→715→823→924→634 ms. The `most_common` "recirc tap" heuristic is also erratic — even the sweep tool reports `monotonic: False` for it.) So SIZE genuinely scales the FE-computed offsets, but that is a *structural* property decoupled from a (nonexistent) decay.

## 3. Reproduction

Every headline number reproduced exactly on my own runs:

- `aru_datapath2.py 0xFE`: paired peak=931237@93436, late/early=1.01, marginal; percomb dead (peak 19375@0); writeonly marginal (251245); allpass ≡ paired.
- `aru_e3_sweep.py`: 5-program survey all marginal except PLATE weakly-lossy (0.030); SIZE sweep flat, T_eff=inf 0/9.
- Independent recirc-gain script: 6 taps @6835, signed sum −2.008.
- Independent rail check: plateau = 89% of 1,048,544 ceiling.
- Independent long-horizon (400k): energy 11k → 785k → held.

## 4. Remaining INFERRED / GUESS gaps (honest)

1. **WA/RA provenance (root blocker).** `build_engine_prog` hard-codes WA=0, RA=0 for all microwords with a hand-reasoned pipeline story — not from firmware. The 110-step baked control image (recbase+0x2A8) and the 52-tap offset spine do not reconcile bit-for-bit. This is what produces the 6-taps-on-one-address over-unity.
2. **−1 / large-negative sentinels (INFERRED).** Roles keyed on values (−1=WRITE_HEAD, −12353=INPUT, others=WRITE_NEG), reasoned from wrap-pointer arithmetic + SIZE-invariance, not ROM-traced. The captured spine contains *no* INPUT tap — `inject_input()` had to designate step 0 as audio-in.
3. **0x4000 OFST repack (garbage CONFIRMED, mechanism INFERRED).** lane0 overwritten to constant 0x89; only 18 DMEM steps decode (vs 52 needed). Correctly rejected as offset source; the repack mechanism vs the live OFFTAB interleave (0x41FD−4k) is not fully traced.
4. **Coeff bit-width mismatch.** Spine uses 7-bit /127 captured coeffs; the 0x4000 control lane carries 6-bit /32. The bridge round-trips them but the sources disagree — part of the same macro-expansion gap.

**Solidly CONFIRMED (non-circular):** OFFSET = tap_map[k] matches live hardware OFFTAB 128/128 at live SIZE; SIZE scales referenced-delay depth monotonically; engine arithmetic (/32, ±2¹⁸ sat, 1-step deferred MAC) is owner-validated and untouched.

## Bottom line

Track E is an **honest, well-instrumented negative result**. It did exactly the right thing: it proved the offset/coeff/SIZE spine end-to-end, found the loop does not close at sub-unity (over-unity, rail-clamped), and declined to fabricate a feedback gain. The Definition-of-Done item "Track E produces a coherent, parameter-tracking reverb" is **not met**; the blocker is the WA/RA/XFER/ZERO/device macro-expansion (the 110-step control image vs 52-tap spine reconciliation), which remains the open frontier.

**Relevant files (absolute):**
- `d:/OneDrive/Gray Instruments/iconex/tools/aru_datapath2.py`
- `d:/OneDrive/Gray Instruments/iconex/tools/build_concert_program.py`
- `d:/OneDrive/Gray Instruments/iconex/tools/aru_e3_sweep.py`
- `d:/OneDrive/Gray Instruments/iconex/tools/aru_datapath.py` (reused engine: `run_trace` L129, `/32` multiply L169)
- `d:/OneDrive/Gray Instruments/iconex/tools/concert_program_cceFE.json` (the validated 52-microword spine)