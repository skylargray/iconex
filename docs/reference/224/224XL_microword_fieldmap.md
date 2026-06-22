# 224XL ARU microword — bit-field map (the signal-graph decoder)

The linchpin decode: the full 32-bit ARU microword, recovered from four independent angles
(firmware coefficient-packer path, empirical WCS-image correlation, cross-generation OTP/PCM60
Rosetta, and the Service Manual §3.5–3.7), reconciled adversarially and validated by reconstructing
CONCERT HALL's signal graph. Decoder: `tools/decode_microword.py` (`decode(power_up_id)` → per-step
dicts). This turns the verified delay+gain tap list into an actual **signal graph** (per step: which
register is read/written, the multiply coefficient + sign, accumulate vs transfer, delay tap).

## Layout

WCS = 4 × (128×8) SRAM. Per step `S`, the 4 stored bytes are at `0x4000 + S*4 + lane` (lane 0–3;
SBC address bits[1:0]=lane, [8:2]=step). 100 active steps, 34.13 kHz. **Storage is active-low**
(the offset and control bytes are complemented; the coefficient *magnitude* is stored direct — a
genuine mixed-polarity quirk, confirmed empirically). A step with `lane2==lane3==0xFF` = NOP/pure-delay.

| Lane | Bits | Field | Decode | Confidence |
|---|---|---|---|---|
| 0–1 | 16 | **OFST** | `offset = ~(lane1<<8 \| lane0) & 0xFFFF`; **delay = offset** (DMEM addr = position − offset, 2's-comp) | **HIGH** — all angles + clean taps |
| 3 | 6:0 | **COEFF magnitude** | `lane3 & 0x7F` (**raw, not complemented**), gain = mag/127 | **HIGH** — image test 77 matches vs ≤50 for alternatives |
| 3 | 7 | **CSIGN** | raw bit7, active-low: `1 ⇒ negative` | **HIGH** |
| 2 | 1:0 | **WA** | `(~lane2) & 3` — register-file write addr (1 of 4; addr 3 = pass-through) | MED |
| 2 | 5:2 | **RA / XFER** phase | `((~lane2)>>2) & 0xF` — read-addr + transfer strobe; **not cleanly split** (value `0xF` ⇒ XFER/result-reg load) | LOW |
| 2 | 6 | **PROTECT / MAC-enable** | `((~lane2)>>6) & 1` — set on ~99% of active steps | MED |
| 2 | 7 | **ZERO** | `((~lane2)>>7) & 1` — clear accumulator at MAC-block start | MED |

Lane→SRAM/MI map (Service Manual): lane0=U49/MI0-7, lane1=U33/MI8-15, lane2=U18/MI16-23, lane3=U3/MI24-31.

## Execution model (ARU, Service Manual §3.7)

4×16-bit **register file** (write addr WA, read addr RA; addr 3 = pass-through) → 16×6-bit 2's-complement
**multiplier** (coeff C0–C5 + CSIGN, **saturating**) → 20-bit **accumulator** → 16-bit **result register**.
Per step: read register[RA] × coeff (signed) → accumulate; write DAB→register[WA]; **ZERO** clears the
accumulator (open a MAC block), **XFER** loads the result register from the accumulator (close a block).
DMEM read/write at `position − offset`. The 224XL variant does "two multiplier bits at once" (dual-rank
shift register) — but those extra LSBs are **not separately visible in the WCS image**.

## Validation — CONCERT HALL decodes to a coherent reverb graph

The control bits assemble into the documented topology, not noise:
- **Pre-delay line** — steps 5–22: 18 fill steps at constant offset = input pre-delay.
- **Recirculating tank** — the `+0.976` feedback coeff (`lane3=0x7C`) appears **16×**, 12 in clean 4-step
  MAC blocks `[-c, -small, -c, +0.976]` with `WA=3, RA=3` on the feedback step, `ZERO` opening and the
  RA/XFER phase reaching `0xF` (XFER) on the closing feedback write.
- **Symmetric allpass diffusers** — e.g. steps 62–65 = `-0.591, -0.126, -0.591, +0.976` (matched outer
  coefficients about a center tap = the canonical allpass signature); also `-0.748, -0.031, -0.748`.
- **Terminal output line** — steps 125–127 read specific taps (`-0.811, -1.0, -0.157`) to the output.

## Pinned vs. genuinely open

**Pinned:** OFST (lanes 0–1, active-low), COEFF magnitude + CSIGN (lane3 raw), lane2 = control byte
(not coefficient), WA (lane2 bits1:0), the lane→MI map.

**Partially pinned (behavior-supported, no manual bit index):** ZERO (lane2 b7), PROTECT/enable (b6),
XFER (phase = 0xF) — they behave exactly as named but the manual prints no bit index.

**Open (needs the ARU schematic or live silicon):** the exact split of lane2 bits5:2 into RA0/RA1 vs the
XFER strobe (they co-vary at MAC-phase boundaries); whether bit6 is the specific WCS PROTECT bit or a
generic MAC-enable; the "2 extra multiplier LSBs" (collapsed into the 7-bit lane3 value in the image).
Per the §8 caveat, some bits5:2 transitions may be timing-derived strobes — labelled provisionally.
