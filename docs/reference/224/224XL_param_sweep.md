# 224XL parameter sweep — param → coefficient/delay transfer functions

Recovered empirically by booting the real firmware (`tools/boot_xl`), reaching the main loop, then
injecting LARC slider values per parameter and reading how the WCS microword image changes after the
de-zipper settles. Tool: `tools/param_sweep.py` (`sweep(power_up_id)` → JSON). CONCERT HALL example:
`docs/reference/224/224XL_param_sweep_01.json`. Slider grid = `0x20,40,60,80,A0,C0,E0,FF` (0x20 ≈ default).

## The always-on modulation engine (found while sweeping)

Independent of any knob, the firmware **continuously modulates 4 tank taps** — pairs **(56,57)** and
**(107,108)**. Each delay sweeps **~±47 samples** (range ~93) and the paired interpolation coefficient
tracks the fractional delay full-range (±127). The feedback gain (+0.976) and static allpasses do NOT
modulate. This is the Concert Hall's signature modulated tank = the LFO→tap injection (a 480L roadmap
open item, now answered for the 224). *Open:* the exact LFO rate/waveform (the 224XL analogue of the
PCM70 `sub_0ad2` phase accumulator) is not yet decoded — only the targets + depth.

## Parameter system

LARC slider positions live at **`0x3c00-0x3c05`** (6 sliders for CONCERT). The main-loop scan `0x8185`
diffs them vs last-seen `0x3c16+`, calling handler **`0x85f2`** on change; type-scaling (param type in
`0x3c33`) → apply path `0xADxx` walks the **`0x3CF4` group table** (built by the interpreter `0xAA9C`)
and writes param-derived values to the linked WCS coeff/delay bytes, ramped by the de-zipper. Param
labels are in NVS2 (CONCERT @0x9CDE = `LOW MID XOV HFD DEP PDL`); other programs use ATT/CHO/HFB/DIF/
BAND/NOTE/RTIM/SIZE variants.

## CONCERT HALL transfer tables (slider 0x20→0xFF)

| Slider | Label | Controls | Effect (value at 0x20 … 0xFF) |
|---|---|---|---|
| 0 | **LOW** | low-band decay | coeff steps 43,95: `-107 … -47` (+ the modulated tank taps) |
| 1 | **MID** | mid-band decay / diffusion | 16 allpass coeffs (62–68,113–119): e.g. step62 `-75 → -63`, step63 `-16 → -28` |
| 2 | **XOV** | crossover freq | clean **linear** pair (45,46,97,98): step45 `-15,-31,-47,-63,-79,-95,-111,-127` (Δ16); step46 `-108…-12` |
| 3 | **HFD** | HF damping | input-filter coeffs (40,41,92,93): step40 `-39 … -127`, step41 `-84 … -124` (high-end) |
| 4 | **DEP** | input diffusion depth | 8 diffuser coeffs (29–32,81–84): monotonic ramps |
| 5 | **PDL** | **predelay** | **DELAY** steps 42,94 (not a coeff): step42 `21839→147` samples, step94 `44767→23075` (predelay shortens as slider rises) |

Curves are monotonic / piecewise-linear (XOV is exactly linear in Δ16) — directly implementable as a
lookup or linear map from a 0..1 parameter. The 224's multiband decay architecture is explicit: LOW/MID
= per-band reverb time, XOV = the band split, HFD = HF damping, DEP = diffusion, PDL = predelay.

## Status / next

- ✅ Method proven on CONCERT; `param_sweep.py` runs any program (`python tools/param_sweep.py <id>`).
  A full pass over all 20 programs is a batch job (~10 min each) for the reconstruction phase.
- 🟡 Sweep the range below 0x20 for the full bidirectional curve; some params wrap at 0xFF (slider
  clamp) — useful range is below the wrap.
- 🟡 Decode the LFO rate/waveform driving the 4 modulated taps (the modulation engine internals).
