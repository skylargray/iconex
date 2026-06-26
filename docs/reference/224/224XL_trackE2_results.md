# Track E.2 / E.4 — Adversarial Gate on the Live-Image Datapath Reconstruction (`aru_datapath3.py`)

**Date:** 2026-06-26 · **Scope:** Track F skepticism applied to the Track E.2-BUILD result (`tools/aru_datapath3.py`, `docs/reference/224/224XL_trackE2build_results.md`). Reproduce the headline numbers, audit genuineness, test RT60-tracking across >=3 programs + a SIZE sweep, deliver a verdict on the ⚪ headline.

**Cardinal rule recap:** success is NOT "it makes sound." Success is a recirculating loop that closes at a *stable sub-unity gain*, an RT60 that tracks SIZE for the *right reason*, a smooth decay, and consistency across programs. Never fit-to-taste.

## Verdict on the ⚪ headline ("any decode produces a coherent 224XL reverb end-to-end"): **STILL OPEN**

A coherent decaying reverb was **NOT demonstrated**. But the Track E.2-BUILD negative is **GENUINE and now precisely located one level deeper than Track E.4**: with the *complete per-microword routing read straight from the authoritative live `mem[0x4000]` image* (no WA=0/RA=0 surrogate, no tuned gain, both CSIGN polarities), the loop does not close — it produces a few sparse echoes then **decays to total silence (DEAD tank)** in *every* program tested. This is a *different* failure from Track E.4's surrogate over-unity rail-pin: correct routing distributes the energy, but the gains land on the wrong read taps relative to the recirc write-head, so the recirc loop has **zero gain** and starves. The build correctly refused to hand-tune a feedback gain.

## 1. Genuineness — is the (non-)closure real, or a convenient WA/RA/gain choice? **REAL.**

The routing is not reconstructed and not a surrogate — it is read **directly** from the live `0x4000` lanes 2,3, which `aru_datapath.decode_image` (the task's stated authoritative decoder) assembles. Independent checks:

| check | result |
|---|---|
| `cs == +/-cmag` for all microwords (no /127, no damping, no feedback const) | **0 violations / 110** |
| datapath3 lane2/3 (WA/RA/XFER/ZERO/device/CSIGN) vs `decode_image` | **0 mismatches / 110 steps** |
| offset RAW `l0\|l1<<8` vs `A.tap_map(0xB800,0xFF)` | **RAW 88/110, inverted 0/110**, 5 head steps `0x89` |
| engine multiply | `prod=(racc<<3)*cs>>5` (validated /32), unchanged |

**Independent recirc loop round-trip gain re-derivation.** The dominant recirc tap is offset **6835** (steps s23, s53), both `cmag=0`, `csign=1`, `WA=3`, `RA=3` -> **tap_gain 0.000**. So the recirculation loop's round-trip gain is **literally 0.0** — a single starved echo. The strong coefficients sit on *other*, unpaired read taps:

```
read tap |gains|: 1.94(s3) 1.81(s2) 0.94(s51) 0.94(s103) 0.91(s0) 0.91(s1) 0.00(s23) 0.00(s53)
```

Several individual taps are over-unity, but they are not on the recirc loop. **No gain was tuned; the negative is a genuine consequence of the decoded routing + coeffs.**

## 2. RT60-tracking — right reason or coincidence? **No RT60 exists -> cannot track.**

Real (live-image) routing, 3 programs, 200k samples, impulse=20000:

| program | mw | peak | nonzero-energy samps | last burst | late(50k+) | verdict |
|---|---:|---:|---:|---:|---:|---|
| CONCERT 0xB800 | 110 | 762630 | 5 | samp 39050 (1.14 s) | 0 | **dead** |
| PLATE 0xBAAA | 105 | 518914 | 2 | samp 1 | 0 | **dead** |
| 0xD000 | 105 | 612203 | 3 | samp 4096 | 0 | **dead** |

Every program: a few bursts then total silence. **No decade of decay to fit -> RT60 is not measurable.** (The closure heuristic prints `stable_subunity` only because `late=0` is silence; the honest label is **dead**.)

What *does* track SIZE monotonically is the **structural recirc-tap delay** (the validated part). From `A.tap_map(0xB800)` the recirc tap (6835 at cce=0xFF) scales strictly:

```
cce  0x20  0x40  0x60  0x80  0xA0  0xC0  0xE0  0xFF
ms   16.7  45.9  70.9 100.1 125.1 150.2 179.4 200.3   (monotonic: True)
```

This is the delay RT60 *would* track if the loop closed — the recirc loop length grows with SIZE for the right reason (BASE scales the wrap arithmetic). **Honest caveat:** monotonicity holds only for the *specific recirc tap / referenced-slot filter*; over the unfiltered tap range the deepest tap is non-monotonic (623->873->534->634 ms) and the `most_common` heuristic reports `monotonic:False`. The surrogate (`aru_datapath2`) SIZE sweep is also flat (decay_ratio 0.67-0.85, T_eff inf 0/9) — over-unity, also no RT60.

## 3. Reproduction — all headline numbers reproduced

- Histogram (both CSIGN): `DMEM_READ=8, DMEM_WRITE=10, RD_AD=11, RDRREG=3, RD_XREG=4, HOLD=74, XFER=45, ZERO=43`.
- Impulse (300k): 5 bursts — **762630@0, 32767@1, 28160@10932 (=320.3 ms recirc echo), 268926@38026, 287294@39050** — then 0; total 1,379,777; late=0.
- CSIGN A/B: NEG peak 762630, POS peak 771747, identical echo1@320 ms, **both dead** (non-discriminating: recirc tap cmag=0).
- Secondary cluster = 268926+287294 = 556220 = **19.8x** re-amplification of echo1 — a non-physical artifact of the unpaired over-unity taps, then death.

## 4. Remaining INFERRED / GUESS gaps (honest)

1. **Section grouping / gain-pairing (root blocker, UNKNOWN).** WHICH DMEM_WRITE captures WHICH read-tap-derived RES, and at WHICH XFER boundary the accumulator is committed before the write — i.e. which consecutive microwords form one allpass/comb. The live image gives every per-microword *field* correctly but NOT the *grouping*. This is why the recirc tap carries no gain while strong gains sit on unpaired taps, and why each round trip writes stale/zero back and starves.
2. **CSIGN polarity (Track B pos vs aru_datapath neg) UNRESOLVED.** Non-discriminating at audio because the dominant recirc tap has cmag=0; cannot be settled until the comb gain is correctly placed on the recirc loop.
3. **Sentinel/input taps INFERRED.** The −1/−12353 tap roles and the input binding are inferred; the captured spine has no native INPUT tap, so audio is injected at the 11 firmware RD-AD steps.
4. **Recirc-tap identification heuristic not fully ROM-grounded** (SIZE-monotonicity is filter-dependent).

**CONFIRMED (non-circular, not gaps):** RAW offset decode (88/110 tap_map), per-microword lane2/3 fields (0 mismatches vs `decode_image`), engine arithmetic (/32, +/-2^18 sat, 1-step deferred MAC), recirc-delay SIZE scaling (16.7->200.3 ms monotonic).

## Bottom line

Track E.2-BUILD is an **honest, well-instrumented negative**, advanced one level past Track E.4. The offsets are now right (RAW), the per-microword routing is the *real* hardware control (byte-identical to the authoritative decode), and no gain was fitted — yet the loop is **dead** across CONCERT/PLATE/0xD000 because the firmware-correct coefficients land on the wrong read taps relative to the recirc write-head (recirc loop gain = 0). The ⚪ Definition-of-Done item ("any decode produces a coherent 224XL reverb end-to-end") is **STILL OPEN**; the precise, firmware-underdetermined blocker is the **per-section (read taps -> accumulate -> XFER -> DMEM write-back) grouping** within the 110-step macro-expansion — no longer offsets, no longer per-microword fields, but the section topology.

**Files (absolute):**
- `d:/OneDrive/Gray Instruments/iconex/tools/aru_datapath3.py` (live-image build + loop-gain analysis)
- `d:/OneDrive/Gray Instruments/iconex/docs/reference/224/224XL_trackE2build_results.md` (build results — verified accurate)
- `d:/OneDrive/Gray Instruments/iconex/tools/aru_datapath.py` (reused engine `run_trace`; `decode_image` authoritative lane2/3 reference — note its `offset=~(l0|l1<<8)` should be RAW; datapath3 corrects this locally)
- `d:/OneDrive/Gray Instruments/iconex/tools/aru_datapath2.py` + `aru_e3_sweep.py` (surrogate path, over-unity — Track E.4 baseline)