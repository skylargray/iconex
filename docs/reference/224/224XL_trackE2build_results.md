# Track E.2-BUILD — complete per-microword CONCERT program from the live 0x4000 image

**Date:** 2026-06-26 · **Tool:** `tools/aru_datapath3.py` (extends aru_datapath2.py; reuses
`aru_datapath.run_trace` engine unchanged). · **Owner:** Skylar Gray.

## What this did

Built the COMPLETE per-microword CONCERT program directly from the **live `mem[0x4000:0x4200]`
image** (the authoritative ROM-assembled hardware microword), every field firmware-derived:

| field | source |
|---|---|
| WA, RA, device (MI16/MI17), CSIGN | lane2 (owner field map, used DIRECT) — agrees 128/128 with baked recbase+0x2A9 (Track E2b) |
| XFER, ZERO, 6-bit coeff mag | lane3 (used COMPLEMENTED) |
| sub-decoder MI12,MI13 | lane1 bits 4,5 (used COMPLEMENTED) |
| **delay offset** | **RAW `l0\|l1<<8`** (NOT inverted — the E2a/E2b correction; raw matches tap_map 88/110, inverted 0/110) |
| MI4 (sub-decoder gate) | `(~l0)` bit4 — the convention under which the device histogram reproduces the validated split |

This REPLACES the aru_datapath2.py WA=0/RA=0 surrogate that produced the over-unity rail-pin.

## Cross-check vs the live image: PASS

Device role histogram exactly reproduces the Track E2b split:
`DMEM_READ=8, DMEM_WRITE=10, RD_AD=11, RDRREG=3, RD_XREG=4, HOLD=74 (71+3 idle); XFER=45, ZERO=43`.
The recirc tap (offset 6835) appears at s23 and s53, both CSIGN=1, both WA=3/RA=3 DMEM-read — matches.

## Result: the loop does NOT close — it is a DEAD (decay-to-silence) tank, not runaway, not a tail

Run through `run_trace` (200k–300k samples, impulse=20000 injected at the firmware RD-AD steps):

- **5 energy bursts in 300k samples, then total silence:** impulse@0 (762630) → echo1@10932 samp
  (320.3 ms, 3.7 % of impulse) → a secondary cluster @~38000 samp → **0 from sample ~39050 onward.**
- `total energy ≈ 1.38e6`, `late (samp 50000+) = 0`. Not over-unity, not sustained.
- The closure heuristic prints `stable_subunity` only because late=0 (silence); the HONEST verdict
  is **dead** — sparse echoes decaying to silence, no continuous decaying tail, no measurable RT60
  (no decade of decay to fit).

### The comb-loop structure IS physically correct

The write steps are write-HEAD pointers (signed delay −4097..−12353 = ahead of CPC); read steps tap
behind. Loop length = read_delay − write_delay. For the recirc tap (6835) paired with the dominant
write head (headdelay −4097, four writes s40/s52/s92/s104) the loop = **10932 samp = 320.3 ms** —
exactly the observed echo1 delay. Other read taps form loops at 360, 656, 724, 731 ms — the right
range for a CONCERT HALL (cf. the 176 ms loop family at smaller SIZE). **The delays are right.**

### CSIGN polarity (Track B A/B test): NON-DISCRIMINATING here

Both conventions run:

| convention | peak | echo1 | total E | verdict |
|---|---|---|---|---|
| CSIGN=1→NEG (aru_datapath) | 762630 | 28160 @320 ms | 1.38e6 | dead |
| CSIGN=1→POS (Track B/POST) | 771747 | 28159 @320 ms | 1.43e6 | dead |

Essentially identical, because **the dominant 320 ms recirc tap (s23/s53) has cmag=0** (tap_gain
0.000) — its sign is irrelevant. The CSIGN polarity cannot be discriminated until the comb gain is
correctly placed ON the recirc loop (see blocker). The Track B vs aru_datapath conflict remains
unresolved at the audio level, deferred for the same reason as E2a/E2b.

## The precise remaining firmware-underdetermined field (the blocker)

**The read-tap → comb-loop GAIN pairing in the macro-expansion is unresolved.** The coefficients
are firmware-correct, but they land on the WRONG read taps relative to the recirc loops:

- the 320 ms recirc tap (s23/s53) has **cmag=0** — it carries the delayed signal into a register
  but applies NO loop gain;
- meanwhile other read taps carry strong gains (s2 tap_gain **+1.81**, s85 −0.94, s33 −0.94) that
  are NOT paired with the recirc write-head, so a single comb sees no sub-unity feedback;
- consequently the recirculated signal reaches RES at an XFER step (e.g. s63 RES=−22528 at n=10932)
  but the DMEM_WRITE that should re-store that section output back to the SAME write-head address
  (to close the comb) has already fired or been ZERO'd earlier in the step order — so each round
  trip writes the WRONG (stale/zero) value back and the loop starves to silence.

In short: **WHICH DMEM_WRITE captures WHICH read-tap-derived RES, and at WHICH XFER boundary the
accumulator is committed before the write — i.e. the per-section ordering of (read taps → accumulate
→ XFER → DMEM write-back) within the 110-step expansion — is the open field.** The live 0x4000 image
gives every individual microword's fields correctly, but the SECTION GROUPING (which consecutive
microwords form one allpass/comb, and therefore which XFER/write-back closes which read tap's loop)
is not yet recovered. This is the same "offset→microword binding / section topology" frontier that
E2b flagged, now confirmed at the datapath level: the bug is no longer offsets (those are right) but
the accumulate/XFER/write-back grouping.

Iterating only on firmware-derived fields (RAW offset, owner lane2/3 decode, both CSIGN polarities)
did not close the loop; no gain was tuned. A genuine, precisely-located negative.

## Files (absolute)
- `d:/OneDrive/Gray Instruments/iconex/tools/aru_datapath3.py` (this build; `build_live_program`,
  `role_of`, `recirc_loop_gain`, `analyze`)
- `d:/OneDrive/Gray Instruments/iconex/tools/aru_datapath.py` (reused engine: `run_trace`,
  `decode_image` — note its `offset = ~(l0|l1<<8)` should be RAW; aru_datapath3 corrects this locally)
