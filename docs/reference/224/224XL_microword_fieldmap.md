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
| 2 | 1:0 | **WA** | `(~lane2) & 3` — register-file write addr (1 of 4; addr 3 = pass-through) | HIGH |
| 2 | 5:4 | **RA** | `((~lane2)>>4) & 3` — register-file **read** addr (RA1,RA0) | **HIGH** — datapath-validated |
| 2 | 3 | **RW / SRC** | `((~lane2)>>3) & 1` — DMEM read/write (or DAB-source) select | MED |
| 2 | 2 | **XFER** | `((~lane2)>>2) & 1` — load result register / write the tank | **HIGH** |
| 2 | 6 | **PROTECT / MAC-enable** | `((~lane2)>>6) & 1` — set on ~99% of active steps | MED |
| 2 | 7 | **ZERO** | `((~lane2)>>7) & 1` — clear accumulator at MAC-block start | HIGH |

**RA vs XFER resolved (`tools/aru_datapath.py`).** lane2[5:2] split: `b5,b4`=RA, `b3`=RW/SRC, `b2`=XFER.
Three independent lines of evidence: (1) **XFER=b2** is set on exactly the result-transfer steps (every
`+0.976` loop-close and DMEM-write step); (2) data-flow **liveness** favors RA including `b5` (0.727 vs
≤0.57); (3) the manual's RA-independent-of-WA constraint rejects `(b5,b3)` (it makes RA≡WA every step);
(4) **decisive** — running the decoded CONCERT microcode through the ARU datapath, `RA=(b5,b4)` is the
*only* assignment that forms a coherent recirculating reverb tank (sustained energy); `(b5,b3)` and
`(b4,b3)` collapse to silence. Lane→SRAM map confirmed by manual diag E20–E23: lane0=U49, lane1=U33,
lane2=U18, lane3=U3.

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

**Pinned:** OFST (lanes 0–1, active-low), COEFF magnitude + CSIGN (lane3 raw), lane2 = control byte,
WA (bits1:0), **RA (bits5:4)**, **XFER (bit2)**, ZERO (bit7), the lane→SRAM map (manual E20–E23).

**Open (the only remaining items for bit-exact, resolved when building the C++ core vs the emulator):**
- `b3` (RW/SRC): DMEM read/write vs DAB-source select — its exact role (which steps read vs write the
  delay memory, and the input/output FPC steps).
- The exact **arithmetic**: the 20→16-bit accumulator shift, the coeff denominator (≈/128) and the
  "2 extra multiplier LSBs", rounding-toward-zero, and saturation — these set the decay/gain precisely.
  The ARU datapath model (`tools/aru_datapath.py`) already runs the routing correctly (RA/XFER pinned);
  these arithmetic details are tuned by diffing its output against the firmware emulator.
- Whether `b6` is the specific WCS PROTECT bit or a generic MAC-enable (doesn't affect audio).
