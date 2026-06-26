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

## Open / unverified about the decode

- 🟠 **`inv_l3`** — coefficient byte polarity (raw vs complemented). Only a weak lean (=True). Resolve by
  pin-tracing C0/–C5/ on 060-02475 (Track A of the validation plan), not by what makes a reverb ring.
- ⚪ **Offset↔control alignment** — the offsets live in the `0x3F4D` buffer (one step order), the control
  lanes are built by the interpreter (possibly another). The per-step pairing is not established. This is
  why naive recombination still failed in Session 11.
- 🟡 **Which image to apply this map to** — the firmware-built WCS image (via `aru224_emulate`), not `0x4000`.

## Source of truth (corrected)

- ✅ **Real delays:** `tools/aru224_emulate.py::tap_map(recbase)` — runs the firmware's B55B builder and reads
  the `0x3F4D` offset table (read **downward**: step *s* at `0x3F4D − 2s`). Validated byte-identical to a
  real-boot snapshot for non-FE records. CONCERT (`0xB800`): short, sensible delays (128, 1756, 2242,
  **6008**×4 = a 176 ms recirculating loop), range 4–176 ms. All 20 programs in
  `docs/reference/224/224XL_record_name_map.md`. *Caveat (🟡):* "faithful read" — that these are the ARU's
  actual delays and that `delay=−offset` is the right interpretation are pending Track A.
- ❌ **Do not use** `mem[0x4000:0x4200]` (what `aru_datapath.py` reads). It is empty for non-FE programs and
  gives clustered ~30 000-sample garbage for CONCERT.

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
