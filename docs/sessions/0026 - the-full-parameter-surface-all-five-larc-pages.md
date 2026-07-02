# 0026 — The full parameter surface: all five LARC pages verified

**Date:** 2026-07-02 (follows 0025)
**Scope:** owner question — "do we have all 4 pages of parameters working as expected?" (ch.4/ch.8).
**Result:** all FIVE pages (ch.4 Table 4.2 — page 5 = Size/Gate) are now mapped and the crisp
documented oracles pass: **Depth's A/C-only rule exact (B/D bit-identical), all four preechoes
appear on their documented channels at the documented delays, and the delay-byte laws are pinned
integer-exactly (PE delay = byte × 34 frames; Fine Predelay = byte × 4 frames).** The preecho
millisecond stretch (×1.048 = 34,133/32,508) is an independent fingerprint of the variable-fs
model: the manual's coarse-delay numbers are nominal at the flagship rate, CONCERT's real clock
stretches them.

## 1. The routes

- **Flat param array** `0x3CA3 + page*6 + slider` (netlist §7.1) + **direct-call `0xA791`**
  (full-image apply; d1a sentinel pattern). Built-in validation: an untouched rebuild is
  **byte-identical to the boot image** (mod the 8 movers). Covers XOV/Treble/Depth/HFBW/
  Diffusion/Definition/preechoes/fine-predelays/Size/Gate.
- **The decay family does NOT recompile through bare `0xA791`** (LF/Mid/Stops/PDL/Chorus → the
  decay generator `0x86B2`/`0x8DA5`/`0x8E03` runs from the slider handler, not the group-table
  walker) → drive via the SLIDER route (`0x3C00-05`), with **page-2 access by writing the derived
  page index `0x3C34`** — no LARC page-key emulation needed (registry #26).
- **Apply hysteresis found:** a Definition excursion leaves the MID ladder words shifted after
  restore (the generator reran during the excursion but not on restore) — post-excursion
  baselines must be re-derived (registry #27; lo-vs-hi pairs remain clean).

## 2. The recalled defaults ARE the ch.8 variation-1 presets (byte scales decoded)

`0x3CA2` header 0x01; toggles `0x3CCD = 0xC0` (ModeEnh+DecayOpt ON, DynDecay OFF ✓ ch.8).
Percentage params = byte/2.56: **Depth 0x55→33 ✓, Diffusion 0x40→25 ✓, Chorus 0x80→50 ✓,
Definition 0x02→~0 ✓**. Preecho delay bytes = nominal ms: **0x05/0x09/0x11/0x19 = 5/9/17/25 ≈
the documented 5.00/9.75/17.5/25.0 ✓**. FinePD-R 0x52 = 82×4 fr = 10.09 ms ≈ documented 10.2 ✓;
FinePD-L 0x02 ≈ 0.25 ms ≈ documented 0.36 ✓. PDL byte 0x00 = the documented 24.0 ms minimum ✓.
PE levels 0x02 ≈ 00 ✓. (LF/Mid/Treble/XOV bytes are on the nonlinear decay/corner scales.)

## 3. The complete param → WCS map (CONCERT; observed via d2h lo/hi diffs)

| page.slider | parameter | WCS words | verified oracle |
|---|---|---|---|
| 1.1/1.2 | LF/Mid Decay | 43,95 / ladder 62-68,113-119 (+44,96) | ✅ 0025 (levers + documented defaults) |
| 1.3 | Crossover | 45,46,97,98 | ✅ byte law: w45 cmag 32→2 over the range ⇒ corner 0→14.3 kHz (fc = fs·ln(32/c)/2π; cmag 31 ⇒ 164 Hz ≈ doc min "170 Hz", cmag 1 ⇒ 17.9 kHz ≈ doc max "19.0 kHz" — endpoint quantization exact) |
| 1.4 | Treble Decay | 40,41,92,93 | ✅ 8k RT60: hi 1.75 s (mid 2.28); lo = unfittable-fast (max damping) — spans the documented range direction |
| 1.5 | Depth | 29-32,81-84 | ✅✅ **ch.4 verbatim: A −17.4 dB, C −17.1 dB; B and D bit-identical (+0.0 dB)** |
| 1.6 | Predelay | 42,94 (delay lanes) | ✅ slider route: both taps move together (+2.09 ms @lo); restore clean; byte↔ms scale nonlinear, raw 0xF0 overdrives past the LARC scale (+700 ms vs doc max 216) — display-calibration = next tool |
| 2.1/2.2 | LF/Mid Stop Decay | (gated) | ✅ **DynDecay gate confirmed as documented**: OFF ⇒ array accepts, WCS untouched; ON ⇒ still static-idle (stop decays are runtime dynamics — input-level detector; D4 territory) |
| 2.3 | Chorus | LFO depth `0x3CD4` (words 56/57/107/108 animated) | ✅ depth byte 0x04→0x3C over the range, rate `0x3CD3` untouched; default 0x80 ⇒ depth 4 ⇒ the measured ±40-sample mover sweep — self-consistent |
| 2.4 | HF Bandwidth | 74,75,125,127 | ✅ tail upper edge: lo ⇒ <2 kHz (max lowpass), hi ⇒ ~9.9 kHz measured edge |
| 2.5 | Diffusion | 33-35,37-39,85-87,89-91 | 🟡 words move; NED@250 ms too blunt (tail already dense) — early-window observable needed. (§7.5's "g19 = 52/60/72/104/111/123" attribution does not match the observed set — June-era reading, flag it) |
| 2.6 | Definition | 50-52,58-60,62-68,70-72,102-104,109-111,113-119,121-123 | 🟡 empirical: hi shortens broadband 2.78→2.33 s (more articulation, less tail — plausible; no documented number to score) |
| 3.1-3.4 | Preecho Levels 1-4 | **80 / 28 / 79 / 27** | ✅✅ stereo impulse: **taps appear on the documented channels with the documented input routing (L→A, R→C, R→A, L→C) at 5.29/10.27/18.36/26.21 ms = the documented 5.00/9.75/17.5/25.0 ms × exactly 34,133/32,508** (nominal-rate ms, real-rate clock — an independent variable-fs fingerprint). The June "tank feedback (words 27/28/79/80)" label is dead. |
| 4.1-4.4 | Preecho Delays 1-4 | 80/28/79/27 delay lanes | ✅✅ **integer law: Δofst = byte × 34 frames, exact at all eight test points** (byte = nominal ms at 34.13 kHz) |
| 4.5/4.6 | Fine Predelay L/R | 83 / 31 delay lanes | ✅ **integer law: Δofst = byte × 4 frames, exact** — and the documented 31.3 ms max = 254×4 fr at the REAL 32,508 Hz ✓. (L's render observable masked by the Depth early component — byte oracle used) |
| 5.1/5.3 | Size / Gate | 80-ish/79-ish singles at hi | 🟡 mapped only; Size interacts with the tap words — errata (Concert max 40 m) + var-6/7 dynamics = future |

## 4. Registry additions

| # | Item | Verdict |
|---|---|---|
| 26 | Bare `0xA791` as the full apply | INCOMPLETE — it walks the group table only; the decay family (LF/Mid/Stops/PDL/Chorus) requires the slider handler's decay-generator path (page-switch by writing `0x3C34`) |
| 27 | Param-apply hysteresis | The MID ladder does not restore after a Definition excursion under repeated `0xA791`; re-derive baselines after any excursion (lo-vs-hi pairs unaffected) |
| 28 | Raw slider-byte overdrive | Injected bytes beyond the LARC's physical scale produce out-of-documented-range values (PDL 0xF0 ⇒ +700 ms vs max 216); range scoring needs the byte↔displayed-value calibration (read the LARC display buffer during injection) — the named next tool |

## 5. Files

`d2h_param_surface.py` (+ cache `d2h_param_wcs.json`), `d2i_render_oracles.py`,
`d2j_slider_params.py`. All comparisons floor-subtracted (registry #16); movers masked.

## 6. Status vs the owner's question

Every parameter on all five pages is now **mechanically mapped and lever-verified**; the ones
with crisp documented numbers **pass** (Depth routing, preecho routing+delays+laws, fine-predelay
law, crossover endpoints, DynDecay gate, defaults = presets). Remaining refinements: byte↔display
calibration for exact range scoring (registry #28), a sharper Diffusion early-window observable,
FinePD-L's render observable, stop-decay dynamics + Size/Gate behavior (D4/variation territory).
