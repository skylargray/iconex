# 224XL modulation / LFO engine

The 224XL continuously modulates selected tank delay taps (the chorus that gives the halls/plates
their evolving, non-metallic sound). Decoded from the firmware + validated by poking; engine at
SBC `0xAD5C`–`0xAE9B`.

## Pacing & control

- **Paced by the main loop:** `0x816F` (main loop) → `0x8281` → `0xAD5C`, once per foreground pass.
- **Enable:** `0x3ccd` bit6 (CONCERT = `0xC0`).
- **Rate:** cascaded divider — `0x3e45` (reload **8**) × `0x3e46` (reload from **`0x3cd3`**); the
  modulation phase advances once every `8 × 0x3cd3` main-loop passes. CONCERT `0x3cd3 = 0x20` (32).
- **Depth:** bound **`0x3cd4`**; the delay swing ≈ `bound × ~10` samples (validated: bound 2/4/8 →
  swing 19/41/81 samples). CONCERT `0x3cd4 = 4` → ~±20 samples. Depth can be param-driven via
  `(param − 15) × 4` at `0xB3D4` (some programs), or fixed (`=4` at `0xB3CC`).
- **Waveform: triangle** — the phase value steps by ±1/±2 toward the bounds and reverses (engine
  `0xADD4`–`0xAE4E`); confirmed by the captured delay trajectory (clean linear ramp up/down).
- **Period:** CONCERT full triangle ≈ 345k SBC instructions (~sub-2 Hz chorus).

## Targets (per program)

Each modulated tap is a fractional delay: the engine writes the **delay** (`0xAE6C`, slow ramp, 7-byte
offset) and the **allpass interpolation coefficient** (`0xAE8E`, computed at `0xAE72`: `SUB 4 / AND 3 /
OR 3` — the fractional-delay coefficient that tracks the delay). Taps are modulated in **pairs, in
anti-phase** (one pair's coeff rises while the other's falls).

Modulated WCS steps per program (from the batch sweep `modulated_steps`):

| Program | Modulated taps | Pairs |
|---|---|---|
| CONCERT HALL, BRIGHT HALL | 56,57,107,108 | 2 |
| DARK HALL | 55,56,69,70,107,108,121,122 | 4 |
| PLATE | 100,101 | 1 |
| CHAMBER | 64,65,91,92 | 2 |
| SMALL ROOM | 58,59,73,74,109,110,124,125 | 4 |
| RICH CHAMBER | 116,117 | 1 |
| HALL/HALL | 65,66,108,109 | 2 |
| PLATE/HALL | 80,81,104,105 | 2 |
| PLATE/CHORUS | 48,49,…,61 (10) | 5 |
| CD PLATE A | 56–76 (18) | 9 |
| CHORUS&ECHO | 91–107 (12) | 6 |
| INVERSE ROOM, RES CHORDS, RICH PLATE, RICH SPLIT | — | 0 (no modulation) |

So modulation depth/breadth scales with the program character: halls = a gentle 1–2 pairs, rooms/dark
halls = 4 pairs, CD plates and chorus programs are densely modulated (9–18 taps), and the "inverse"/
resonant/rich-dense programs have none.

## Reconstruction notes

- LFO = triangle, frequency = `f_mainloop / (8 × rate_divisor × triangle_steps)`; depth in samples ≈
  `0x3cd4 × ~10`; per-program targets as above. Anti-phase pairs.
- The interpolation coefficient is the standard fractional-delay/allpass coefficient (`0xAE72` math) —
  reproduce with a fractional delay line + allpass interpolation on the listed taps.
