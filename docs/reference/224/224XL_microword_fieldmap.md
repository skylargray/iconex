# 224XL ARU microword — bit-field map (the signal-graph decoder)

> **Confidence taxonomy** (see `docs/plans/224XL-validation-plan.md` §0): ✅ CONFIRMED (schematic-traced
> and/or proven) · 🟡 PARTIAL (faithful read but interpretation/location unverified) · 🔵 INFERRED ·
> 🟠 GUESS · ⚪ UNKNOWN.
>
> **⚠️ Session-11 correction.** The earlier version of this doc said the microword is read from
> `mem[0x4000 + S*4 + lane]`. **That is wrong.** `0x4000` was never the real WCS source: for a non-FE
> program (CHAMBER) it decodes to **all zeros**, while the firmware's actual offset table (the `0x3F4D`
> buffer) matches the firmware load byte-for-byte. The **field-bit *meanings* below are still valid**
> (owner schematic-traced), but **where they are read from, and the offset/coefficient *values*, must come
> from the firmware-built image (`aru224_emulate.py`), not `0x4000`.** The decoder `tools/aru_datapath.py`
> still reads `0x4000` and is therefore **producing wrong offsets** — see §"Source of truth".

> **✅ 2026-06-26 validation update** (plan §5; `224XL_trackAC_results.md`, `_trackE2_results.md`). Three
> load-bearing corrections beyond the Session-11 banner: **(1) the offset↔control alignment is SLOT-INDEX-KEYED**
> (each bytecode slot `k` keys *both* `offset=offbuf[k]` and `coeff=mem[recbase+0xAD+4k]`) — this was the root
> cause of the dead tank, not a value bug. **(2) The 0x4000 image's OFST decodes RAW** (`l0|l1<<8`, 120/128 vs
> `tap_map`); `aru_datapath`'s `~` **inversion was the bug** — only ~5 structural head steps (lane0→`0x89`) are
> genuinely repacked. **(3) Physical `delay = +offset`** (addr = CPC − offset); `delay = −offset` is refuted.
> The control lanes 2,3 of the live 0x4000 image are byte-identical to `decode_image` (authoritative). The lone
> open item for a working datapath is the **section grouping** (which microwords form one allpass/comb section).

## The 32-bit microword — field map (bit MEANINGS) ✅/🟡

The ARU microword is 32 bits = 4 stored bytes (lanes 0–3 = MI0–7 / MI8–15 / MI16–23 / MI24–31).
The *meaning of each field* is owner schematic-traced (060-02475/01318):

| Lane | Bits | Field | Meaning | Confidence |
|---|---|---|---|---|
| 0–1 | 16 | **OFST** | the 16-bit delay offset; `addr = CPC − offset` | ✅ map / 🟡 value (must come from `0x3F4D`, not `0x4000`) |
| 2 | 0 | **MI16** | with MI17: device select (read/write/sub) | ✅ (owner U47 trace) |
| 2 | 1 | **MI17 (MEMAC)** | `(MI17,MI16)`: `11`=MEMR/ read, `10`=MEMW/ write, `01`=sub-decoder, `00`=NC | ✅ |
| 2 | 3:2 | **WA** | register-file **write** address (MI18,MI19); **addr 3 = pass-through/junk** | ✅ (= MI18/19; manual L392) |
| 2 | 5:4 | **RA** | register-file **read** address (MI20,MI21) | ✅ |
| 2 | 6 | **PROT / MAC-enable** | (MI22) datapath-irrelevant to audio | 🟡 |
| 2 | 7 | **CSIGN** | coefficient sign | ✅ |
| 3 | — | **COEFF + XFER/ZERO** | 6-bit coefficient magnitude C0–C5 + XFER (load result reg) + ZERO (clear accumulator) | ✅ fields / 🟠 byte polarity (`inv_l3`) |
| (lane1 b4,5) | — | **MI12, MI13** | the sub-decoder select `(MI13,MI12)`; **dual-use**: also offset bits 12,13 | ✅ |
| (offset b4) | — | **MI4 (DP)** | gates the sub-decoder (U34A pin2); also offset bit 4 | ✅ |

**Device decode (✅ owner net-traced).** `(MI17,MI16)`: `11`→**MEMR/** (DMEM read → DAB=DM[addr]);
`10`→**MEMW/** (DMEM write, data = bus, RES driven via RDRREG); `01`→U47 **Y1** enables the sub-decoder
**only when MI4=1**: `(MI13,MI12)` 1=**RDRREG** (RES→DAB feedback), 2=**RD XREG** (host), 3=**RD AD** (audio
in), 0=idle; `00`→U47 **Y0 = NOT CONNECTED** (idle, DAB floats/holds). **WR DA/** (D/A output) = **U49C**
(74LS10): `(MI17,MI16)=(0,1)` AND **MI7=1**. **RDRREG/** is additionally gated by **DAB RSTB** = f(MS1,MS8).

**Coefficient scale ✅ `/32`** (result reg PP3..PP18 = product≫3; operand≪3). **Accumulator rails at ±2¹⁸ ✅.**

**✅ `cmag=0` = the plan-016 active-low NAND-array baseline** (the "+3 ACC units per `cmag=0` multiply" = the
all-ones product register). For a SINGLE multiply it correctly rounds to 0 at the `≫3` round-half-up (matches
every golden). In the free-run MAC, 19 consecutive `cmag=0` bus-move steps accumulate ~+57 → a ≈−73 dB DC
trickle — faithful to the gate model, NOT the dead-tank cause. *(Cross-multiply accumulation of the baseline
is untested by plan 016, which only exercised single-step; sub-LSB open item, like the `cmag=63` +3.)*

## Open / unverified about the decode

- 🟠 **`inv_l3`** — coefficient byte polarity (raw vs complemented). Only a weak lean (=True). Resolve by
  pin-tracing C0/–C5/ on 060-02475 (Track A of the validation plan), not by what makes a reverb ring.
- ✅ **Offset↔control alignment — CONFIRMED step-index-keyed (2026-06-29).** The free-run engine
  (`tools/aru_freerun.py`) verified that `tap_map[s]` aligns perfectly with the `0x4000` `COEFFICIENTS[s]`
  at the same step index `s`: CONCERT step 0 = 362 ms predelay (the first MEMR), steps 5–23 = a VARIED
  7–176 ms diffuser cluster (NOT the 19 identical ~1.7 s taps the wrong `0x4000` lane-0/1 source produced),
  with a 176 ms recirc loop reused 4×. The naive Session-11 recombination failed because of the offset
  *source* (`0x4000` lanes 0/1 = garbage), not the per-step pairing — which is correct.
- 🟡 **Which image to apply this map to** — the firmware-built WCS image (via `aru224_emulate`), not `0x4000`.

> **✅ Where the coefficient values come from (param-application chain, 2026-06-29).** The 6-bit COEFF
> magnitude + CSIGN packed into this microword are produced by the de-zipper applier `0xB000`: it ramps each
> coeff/delay one step per main-loop pass and PACKS the byte into the `0x4000` image (`0xB4F0` = 6-bit coeff
> magnitude into the upper bits; `0xB4FF` = sign into bit7 of the adjacent byte). The source param values for
> all five LARC pages live in ONE FLAT RAM array based at `0x3ca3` (6 bytes/page × 5 pages; recalled from the
> `0xB800` program record at load via `0x13d9`/`0xa791`, so the full WCS image — 110/128 steps for CONCERT —
> is already built at boot). The group table `0x3CF4` links each parameter's group to its target WCS step(s)
> (step→coeff-address transform `0xAB0C`: `addr = 0x4003 + step*4`). Full chain (faders `0x3c00-05`, page state
> `0x3c32`/`0x3c34`, apply scan `0x8185`→`0x85f2`, toggles `0x3ccd`) is in the **technical reference / system
> architecture** doc — this doc only documents the resulting microword bits.

## Source of truth (corrected)

- ✅ **Real delays:** `tools/aru224_emulate.py::tap_map(recbase)` — runs the firmware's B55B builder and reads
  the `0x3F4D` offset table (read **downward**: step *s* at `0x3F4D − 2s`). Validated byte-identical to a
  real-boot snapshot for non-FE records. CONCERT (`0xB800`): short, sensible delays (128, 1756, 2242,
  **6008**×4 = a 176 ms recirculating loop), range 4–176 ms. All 20 programs in
  `docs/reference/224/224XL_record_name_map.md`. *Caveat (🟡):* "faithful read" — that these are the ARU's
  actual delays and that `delay=−offset` is the right interpretation are pending Track A.
- ❌ **Do not use** `mem[0x4000:0x4200]` (what `aru_datapath.py` reads). It is empty for non-FE programs and
  gives clustered ~30 000-sample garbage for CONCERT.
- ⚠️ **Do not use** `tools/boot8080.py::read_offsets` either. It reads a **contaminated** `0x3F4D` from the
  *booted* firmware (modified post-build): it gives 576 ms for CONCERT step 2 vs `tap_map`'s correct 176 ms.
  Always use `aru224_emulate.tap_map`, which runs the B55B builder from the program record.

> **✅ Free-run engine (M3, 2026-06-29).** `tools/aru_freerun.py` (`class FreeRunARU`; does NOT touch the
> POST-green `tools/aru_rtl_dp.py`) sweeps the WCS program counter 0→99 (RESET@99), per-step §2T device-decode
> DAB routing, the fig-3.4 deferred MAC as a 1-instruction pipeline, signed multiply-accumulate
> (`RES = sat16(ACC≫3)`), DMEM recirculation, and fixed-point I/O (inject at RD AD/, capture at WR DA/). It
> initially **re-introduced the documented `0x4000` offset bug** (sourced `ofst=(l1<<8)|l0` from `0x4000` lanes
> 0/1 → dead tank); **fixed** by sourcing the per-step delays from the `0x3F4D` offset buffer via `tap_map`.
> With the corrected ms-scale offsets (`addr = CPC + offset[step]`; of `{CPC−off, CPC+off, CPC−|off|}` only
> `CPC+off` survives — settled by the offset matrix) the feedback loops EXIST at ms-scale and a **SHORT (~0.5 s)
> decaying tail emerges** — CONCERT goes from a *fully dead* tank to an audible short tail (the DMEM buffer
> decays ~1.7 s). *(An earlier "loop closes / dense continuous field" claim was a flawed-test artifact — that
> test overwrote lanes 0/1 and corrupted the I/O routing; the clean result is the short tail.)* 🟡 The full
> ~2.6 s hall decay is STILL OPEN — the tail decays too fast (loop gain too low: quantization / coeff scaling /
> the per-frame LFO modulation). POST regression stays green on `aru_rtl_dp.py` (E32/E40/E83/E91, multiply 20/20).

## Execution model (ARU, Service Manual §3.7) ✅

4×16-bit **register file** (LS670 U29–U32; write addr WA, read addr RA; **addr 3 = pass-through**) → 16×6-bit
two's-complement **multiplier** (saturating, `/32`) → 20-bit **accumulator** (±2¹⁸ rail) → 16-bit **result
register** (LS374 U43/U44). Per step: read register[RA] × coeff (signed) → accumulate; the DAB is written to
register[WA] every cycle; **ZERO** clears the accumulator (open a MAC block); **XFER** loads the result
register (close a block). DMEM read/write at `CPC − offset`. The multiply pipeline completes at the end of
AS0 of the *next* cycle (1-step deferred product). The dual-rank shift register does two multiplier bits per
ARU state; those extra LSBs are not separately visible.

> **Validation status:** the field MAP is ✅; a *working reverb* built from this map has **never been
> demonstrated end-to-end** (⚪). The old "CONCERT HALL decodes to a coherent reverb graph" claim was based on
> the wrong (`0x4000`) offsets and is **retracted**. See `docs/plans/224XL-validation-plan.md`.
