# Lexicon 224XL — Complete Technical Reference for Reconstruction

**Purpose.** Everything reverse-engineered about the 224XL reverb, organized to drive the two next
steps: (1) the **emulator-diff harness** and (2) the **bit-exact header-only C++17 core** (see
`docs/plans/480L_rom_to_plugin_guide.md`). Every claim here was recovered from the real v8.2.1 firmware
running in a Z80 emulator and/or the 224X Service Manual; confidence is flagged where relevant. Source
docs: `224XL_microword_fieldmap.md`, `224XL_record_name_map.md`, `224XL_param_sweep.md`,
`224XL_modulation_lfo.md`; source tools in `tools/`. ROM set: `ROMs/Lexicon 224/224XL v8_21`.

---

## 1. System architecture

The 224XL is two computers:

- **SBC** — a Z80 control computer. Runs the LARC serial UI, manages programs/parameters, **builds and
  loads the WCS microcode**, and **continuously modulates** it. Does NOT compute audio.
- **DSP** — three modules (T&C, ARU, DMEM) forming a microcoded reverb engine. **Executes the WCS
  microprogram at 34.13 kHz**, one pass per output sample, reading/writing a large delay memory (DMEM)
  and the analog I/O (FPC). THIS is what the C++ core reimplements.

Data flow: `program record → SBC build engine → WCS image (microcode) → ARU executes → audio`.
Parameters and modulation are the SBC rewriting WCS coefficient/offset bytes over time.

Key clocks/sizes: system cycle **292.97 ns** (3.41 MHz), 9 time-slots/cycle grouped AS0/AS1/AS2;
**100 microcode steps** per sample → **34.13 kHz** (the WCS counter resets at 99). Note the WCS *image*
is 128 slots (0x4000–0x41FF = 512 B); the hardware executes ~100 of them (the program ends at a RESET
the WCS generates). Decoded programs show live content out to ~step 108–127 plus 0xFFFF fill —
**exactly how many steps execute per sample, and where the program-end RESET sits, is an OPEN item**
(§10) that the diff harness must pin (it sets both the true step count and the sample rate). Until then,
treat 100 as nominal and use the firmware's own image extent per program.

### SBC memory map (for driving the emulator)

| Region | Window | Role |
|---|---|---|
| SBC1 | 0x0000–0x07FF | reset, LARC serial, boot, power-up self-test |
| SBC2 | 0x0800–0x0FFF | ARU/DSP I/O drivers, POST |
| SBC3 | 0x1000–0x17FF | program directory/load, NVS dispatch |
| battery RAM | 0x2000–0x27FF | user registers (saved program variations); 0xFFFF = DIP switch |
| SBC RAM / stack | 0x3C00–0x3FFF | working state, stack; **WCS image staged + modulated here** |
| **WCS** | **0x4000–0x41FF** | the 100-step microprogram (4 SRAMs, see §3); memory-mapped to SBC |
| NVS1 | 0x8000 | ARU runtime engine (`CALL 0x8000`) |
| NVS2 | 0x9000 | per-program code + param **labels** (CONCERT @0x9CDE = "LOW MID XOV HFD DEP PDL") |
| NVS3 | 0xA000 | name table @0xA002, directory @0xA446, loader/interpreter 0xA791/0xAA9F |
| NVS4 | 0xB000 | math/pack bank (packers 0xB4F0/0xB4FF), coeff record array @0xB800 |
| NVS5–7 | 0xC000–0xEFFF | continuation of the 21×682-byte record array |
| NVS8 | 0xF000 | per-program parameter/range records |

---

## 2. The ARU datapath (the C++ core's execution engine)

From Service Manual §3.7 + the ARU schematic #060-01318 (verified: register file = four **LS670** chips,
4-word×4-bit each with **independent read/write addressing**).

Components:
- **Register file** — 4 registers × 16-bit. Independent **write address WA (2-bit)** and **read address
  RA (2-bit)**. `DAB WSTB/` writes the DAB into R[WA] **every cycle** (data not always meaningful).
  **Address 3 = pass-through** (dummy/scratch write location).
- **Multiplier** — 16×6-bit 2's-complement, **saturating**. Serial shift-and-add done **two bits at a
  time** via a dual-rank shift register (one cycle per 6-bit multiply). Coefficient = 6 bits `C0–C5` +
  sign `CSIGN/`.
- **Accumulator** — 20-bit. `ZERO/` clears it.
- **Result register** — 16-bit. `XFER/` (clock XFER CK) loads it from the accumulator.
- **DMEM** — **circular delay memory of 65536 words → `DMEM_MASK = 0xFFFF`** (manual: one bank of 64K
  DRAM, or two 16K banks; 16-bit offset + 16-bit position ⇒ 64K). Addressed by a 16-bit **current-
  position counter** (incremented once per sample) **minus** the microword offset. The DAB carries DMEM
  data, FPC audio, the result register, or the SBC XREG.

  **Address/delay convention (authoritative — use this in C++):** the stored offset bytes are `OFST/`
  (active-low). True offset = `~(lane1<<8 | lane0) & 0xFFFF`. The hardware does a 2's-complement subtract
  (`address = position + OFST/ + 1`), i.e. **`address = (position − offset) & 0xFFFF`**. The "delay in
  samples" a tap represents = `(position − address) mod 65536 = offset`. Absolute offsets in a live
  firmware image are large (relative to an arbitrary position base that cancels across read/write pairs);
  the human-readable per-tap lengths in `224XL_record_name_map.md` come from the standalone build with
  base 0 and use the signed `delay = −offset` convention. For the C++ core only the address formula above
  matters — the circular buffer makes the base irrelevant; the reverb topology is in the read/write
  *relative* positions.

### The 20-bit multiplicand alignment (critical for bit-exact)

Per §3.7: forming the 20-bit operand from the 16-bit register value `x`:
- the **MSB of x (x[15]) becomes the two MSBs** of the 20-bit word (bits 19,18 = sign extension),
- **x[15:0] occupies bits 18..3**,
- the **low 3 bits (2,1,0) are tied to 0**.

So `operand20 = sign_extend(x, 17) << 3`. Overflow detect = XOR of the top two bits (must match unless
overflow). On overflow, saturate to most-positive / most-negative.

### Per-step execution (one WCS step)

```
addr   = (position - offset) & DMEM_MASK            # offset from microword (lanes 0-1)
dab    = (write op) ? RES->DMEM[addr]               # XFER/write step deposits result reg
                    : DMEM[addr]                     # read op puts delay tap on the bus
                    (FPC audio in/out on the I/O steps)
R[WA]  = dab                                         # register write every cycle (WA=3 = pass-through)
prod   = multiply20(R[RA], coeff, CSIGN)            # 16x6 saturating, with the 20-bit alignment above
if ZERO: ACC = 0
ACC    = saturate20(ACC + prod)
if XFER: RES = saturate16(ACC >> SHIFT)             # SHIFT/rounding = an OPEN arithmetic detail (§6)
```

100 steps = one output sample; `position += 1` per sample. The reverb's recirculating tank lives in
the DMEM + register feedback; the `+0.976`-class coefficients on XFER steps close the loops.

---

## 3. The WCS microword (the instruction format)

WCS = 4 × (128×8) SRAM. For step `S`, the 4 bytes are at `0x4000 + S*4 + lane` (SBC addr bits[1:0]=lane,
[8:2]=step). **Lane→SRAM** (manual diag E20–E23): lane0=U49, lane1=U33, lane2=U18, lane3=U3.

**Storage is active-low** with a mixed-polarity quirk: the OFFSET and the LANE2 CONTROL byte are stored
complemented; the LANE3 coefficient **magnitude** is stored direct. A `NOP`/pure-delay step ⇔
`lane2==lane3==0xFF` (the control+coefficient half is all-zero in true logic; lanes 0–1 may still hold a
don't-care offset, so the full 32-bit word is not necessarily all-zero).

| Lane | Bits | Field | Decode | Conf |
|---|---|---|---|---|
| 0–1 | 16 | **OFST** | `offset = (~(lane1<<8 \| lane0)) & 0xFFFF`; **DMEM addr = (position − offset) & 0xFFFF** (see §2) | HIGH |
| 3 | 6:0 | **COEFF mag** | `lane3 & 0x7F` (**raw**); gain ≈ mag/127 (exact denom ≈ /128, see §6) | HIGH |
| 3 | 7 | **CSIGN** | raw bit7, active-low: `1 ⇒ negative` | HIGH |
| 2 | 5:4 | **RA** | `((~lane2)>>4)&3` — read-register address (RA1,RA0) | HIGH (datapath-validated) |
| 2 | 3 | **RW/SRC** | `((~lane2)>>3)&1` — DMEM read/write (or DAB-source) select | MED |
| 2 | 2 | **XFER** | `((~lane2)>>2)&1` — load result register / write the tank | HIGH |
| 2 | 1:0 | **WA** | `(~lane2)&3` — write-register address (3 = pass-through) | HIGH |
| 2 | 7 | **ZERO** | `((~lane2)>>7)&1` — clear accumulator (opens a MAC block) | HIGH |
| 2 | 6 | **PROTECT** | `((~lane2)>>6)&1` — WCS-access protect / MAC-enable (≈always 1 on active steps) | MED |

**RA/XFER resolution** (the hard part, now settled): running the decoded CONCERT microcode through the
ARU datapath, `RA=(b5,b4)` is the **only** assignment that forms a coherent recirculating reverb tank;
`(b5,b3)`/`(b4,b3)` collapse to silence. Corroborated by data-flow liveness, the manual's
RA-independent-of-WA constraint (the LS670 schematic confirms separate RA/WA address nets), and XFER=b2
firing on exactly the result-transfer steps. The exact split of lane2[5:2] = `b5,b4`=RA · `b3`=RW/SRC ·
`b2`=XFER. (100%-authoritative bit positions would come from T&C schematic #060-02475, not yet in hand.)

Decoder: `tools/decode_microword.py` (`decode(power_up_id)` → per-step dicts with delay, coeff, CSIGN,
WA, RA, RW, XFER, ZERO, PROT).

---

## 4. Arithmetic & validation vectors (for bit-exact)

The reverb character lives in the integer ARU arithmetic. Pin these via the firmware-emulator diff
(§9) and the manual's exact test vectors:

- **Coefficient encoding.** 6-bit `C0–C5` magnitude + `CSIGN`. The "two multiplier bits at once" packs
  2 extra LSBs (NVS4 packer 0xB4F0 lo byte `(~coarse<<2)|2LSB`; 0xB4FF hi byte `sign|7-bit`). Coeffs can
  be **>1** (e.g. the manual's +5/4, +42/32). Stored lane3 7-bit value decodes to the gains we measured
  (e.g. lane3=0x7C → +0.976). Exact denominator (≈/128) + the 2-LSB contribution = an OPEN detail.
- **Service-Manual multiplier test vectors** (Diagnostic Program "ARU TESTS" / "ADD'L MULT", exact and
  reproducible — use as C++ unit tests): coefficients **+21/32, +42/32, +63/64**, and **×1, ×1/2, ×−1,
  ×1/4, ×5/4**. Four multiplications each; the last two coefficients must trip the saturation logic.
- **Saturation** — on positive/negative overflow force most-positive/most-negative (the 20-bit two-MSB
  XOR detector).
- **Rounding** — toward zero (truncation) per the family's §8 caveat; confirm by diff.
- **OPEN (resolve in the diff harness):** the 20→16-bit result-register shift amount; the coeff
  denominator + 2-LSB weighting; `b3` (which steps read vs write DMEM); the FPC input/output steps
  (where audio enters/leaves). The ARU datapath model `tools/aru_datapath.py` already runs the ROUTING
  correctly (RA/XFER pinned) — these remaining details set the exact gain/decay.

---

## 5. Programs & microcode extraction

20 reverb/effect programs. Selector ID = a record's first byte; the firmware finds the record by ID in
the @0xB800 array (page-wrap walk: `HL=0xB800; +0x2AA; if (L==0xFE) HL+=2`). Names are
firmware-authoritative, cross-checked 20/20 vs the NVS3 directory (`{flags=ID, group=bank, sub=prog}`).

**To extract a program's WCS microcode** (the per-sample microprogram):
```python
import sys; sys.path.insert(0,'tools'); import boot_xl as B
cpu,mem,larc,aru,ms,*_ = B.boot(power_up_id=0x01, verbose=False)   # 0x01 = CONCERT HALL
wcs = bytes(mem[0x4000:0x4200])     # 128 steps x 4 bytes (active-low)
```
Or `tools/decode_microword.decode(0x01)` for the decoded per-step list.

Program table (id · name · bank/prog · #modulated taps; full delays/gains in `224XL_record_name_map.md`
and per-program `224XL_param_sweep_<id>.json`):

| id | program | B/P | mod | id | program | B/P | mod |
|---|---|---|---|---|---|---|---|
| 0x01 | CONCERT HALL | 1/1 | 4 | 0x21 | CD PLATE A | 3/3 | 18 |
| 0x20 | BRIGHT HALL | 1/2 | 4 | 0x06 | HALL/HALL | 5/1 | 4 |
| 0x05 | DARK HALL | 1/3 | 8 | 0x0A | PLATE/PLATE | 5/2 | 4 |
| 0x40 | SMALL ROOM | 2/2 | 8 | 0x12 | PLATE/HALL | 5/3 | 4 |
| 0x08 | CHAMBER | 2/3 | 4 | 0x22 | PLATE/CHORUS | 5/4 | 10 |
| 0x80 | RICH CHAMBER | 2/4 | 2 | 0x42 | RICH SPLIT | 5/5 | 0 |
| 0x41 | DARK CHAMBER | 2/5 | 2 | 0x0C | CHORUS&ECHO | 4/1 | 12 |
| 0x81 | INVERSE ROOM | 2/6 | 0 | 0x14 | RES CHORDS | 4/2 | 0 |
| 0x02 | PLATE | 3/1 | 2 | 0x24 | M BAND DELAY | 4/3 | 0 |
| 0x10 | CD PLATE B | 3/4 | 16 | 0x11 | RICH PLATE | 3/5 | 0 |

Decoded structure (CONCERT, the canonical example): pre-delay line → symmetric allpass diffusers
(`-c,-small,-c`) → recirculating tank (4-step MAC blocks `[-c,-small,-c,+0.976]`, ZERO opens / XFER
closes, reads R3 feedback) → multi-tap output line. ~100–108 active steps per program.

---

## 6. Parameters (per-program transfer functions)

Each reverb exposes ~6 parameters (CONCERT = LOW MID XOV HFD DEP PDL; other programs use ATT/CHO/HFB/
DIF/BAND/NOTE/RTIM/SIZE variants — labels in NVS2). The C++ core needs, per program, **which WCS
steps each parameter rewrites and the value→coeff/delay curve**. These are recovered empirically.

**Param path:** LARC slider positions `0x3c00–0x3c05` → main-loop scan `0x8185` diffs vs last-seen
`0x3c16+` → handler `0x85f2` (type-scaling, param type in `0x3c33`) → apply walks the **`0x3CF4` group
table** (built by the interpreter `0xAA9C`) → rewrites the linked WCS coeff/delay bytes, **ramped by
the de-zipper** (so transitions smooth, not instantaneous).

**Transfer data:** `tools/param_sweep.py` / `batch_sweep.py` → `224XL_param_sweep_<id>.json` for all 20
programs. Each file lists, per parameter, the affected coeff steps and delay steps, with the value at 8
slider points (0x20…0xFF; 0x20 ≈ default). Curves are monotonic / piecewise-linear (e.g. CONCERT XOV is
exactly linear, Δ16/step). CONCERT example:

| Slider | Label | Controls |
|---|---|---|
| 0 | LOW | low-band decay (2 coeffs + the modulated taps) |
| 1 | MID | mid-band decay (16 allpass coeffs) |
| 2 | XOV | crossover (linear coeff pair) |
| 3 | HFD | HF damping (input-filter coeffs) |
| 4 | DEP | input diffusion (8 coeffs) |
| 5 | PDL | **predelay → DELAY steps** (42/94: 21839→147 samples), not a coeff |

For the C++ core: expose params as 0..1, map through the per-program JSON curve to the target
coeff/delay at the linked steps, and de-zipper (ramp) toward target (multi-rate, ≈ −4/−1 per control
tick) for click-free changes.

---

## 7. Modulation / LFO engine

The firmware continuously modulates selected tank taps (the chorus that de-metallizes the reverb).
Engine `0xAD5C–0xAE9B`, doc `224XL_modulation_lfo.md`.

- **Waveform: triangle.** A phase value steps ±1/±2 toward bounds at `0x3cd4` and reverses.
- **Paced by the main loop** (`0x816F → 0x8281 → 0xAD5C`), once per foreground pass.
- **Rate:** cascaded divider `0x3e45` (reload 8) × `0x3e46` (reload from **`0x3cd3`**); phase advances
  every `8 × 0x3cd3` passes (CONCERT `0x3cd3=32`). Full period ≈ 345k SBC instructions (~sub-2 Hz).
- **Depth:** bound **`0x3cd4`**. CONCERT `0x3cd4=4` → measured peak-to-peak delay swing **≈93 samples
  (±≈47)** on each modulated tap (measured over multiple LFO periods; an earlier "×10/→41" figure was a
  single-window undersampling artifact — use ±47). Swing scales ~linearly with `0x3cd4`. Optionally
  param-driven via `(param−15)×4` (`0xB3D4`).
- **Enable:** `0x3ccd` bit6.
- **Targets:** per-program modulated WCS steps (table §5, 0–18 taps), modulated in **anti-phase pairs**.
  Each modulated tap = a **fractional delay** whose interpolation coefficient (the allpass coefficient,
  computed at `0xAE72`: `SUB 4 / AND 3 / OR 3`) tracks the delay's fractional part. So in C++: a
  fractional delay line per modulated tap with allpass interpolation, LFO-swept.

For bit-exact-over-time, the C++ core must replicate this WCS modulation (it changes the offset + interp
coeff of the listed steps each control tick). The static (un-modulated) microcode is the same image with
those taps at their center value.

---

## 8. Tools & the emulator (how to get reference data)

In `tools/` (Python; `python` on Windows). The Z80 emulator is the ground-truth source of microcode,
modulation frames, and param mappings.

| Tool | Use |
|---|---|
| `z80emu.py` | pure-Python Z80 with IM1 interrupts. API: `Z80(mem)`, `.PC`, regs, `.step()`, `.in_hook/.out_hook`, `.interrupt()`, `.call(addr,max_ins)`, `.m`/`.rb/.wb/.rw/.ww` |
| `boot_xl.py` | boots v8.2.1 → main loop. `boot(power_up_id=ID)` → `(cpu,mem,larc,aru,milestones,cap,snap)`; `mem[0x4000:0x4200]` = WCS. Models LARC serial + active-low ARU latch + POST-pass |
| `decode_microword.py` | WCS image → per-step signal graph |
| `harvest_xl.py` | all-program names + delays + gains |
| `param_sweep.py` / `batch_sweep.py` | param→coeff/delay transfer tables (per-program JSON) |
| `aru_datapath.py` | **the ARU execution reference** (routing correct; arithmetic to tune) |
| `aru224_emulate.py` | build-engine decode (delays via tap_map, gains via capture_coeffs) |

Driving the live firmware (to capture modulation frames / param effects): boot to the main loop, then
step the CPU while firing the serial interrupt (`if cpu.IFF1 and (icount-last)>=64 and (larc.tx_en or
larc.rx_ready(cpu)): cpu.interrupt()`); the WCS at `0x4000` updates live. Inject a parameter by writing
the slider byte `mem[0x3c00+p]=v` with `mem[0x3c16+p]` differing + `mem[0x3c14]|=0x80`, then run. POST
self-test ports are stubbed (active-low ARU latch); the self-tests are modeled as "pass".

---

## 9. The emulator-diff harness (validation plan)

The Z80 emulator builds/modulates the WCS but does **not** compute audio (the real ARU hardware did).
So the bit-exact reference is the **Python ARU datapath model** (`aru_datapath.py`), and the harness has
two layers:

1. **Microcode parity (already achievable).** For each program, the C++ core must load the **identical
   WCS image** the firmware produces (`mem[0x4000:0x4200]`) and decode it with the §3 field map. Assert
   the C++ decode == `decode_microword.decode(id)` field-for-field. This guarantees the *program* is
   right.
2. **Arithmetic parity (the bit-exact tuning loop).** Run the Python ARU reference and the C++ core on
   the same WCS with the same input, compare output **sample-by-sample (integer == integer)**. Tune the
   OPEN arithmetic (§4: result-register shift, coeff denominator + 2 LSBs, b3 read/write, rounding) until
   they match AND the reference is independently anchored by: (a) the Service-Manual multiplier test
   vectors (§4) as unit tests, (b) a stable, decaying reverb impulse response with the measured delays/
   gains/RT, and (c) — if available — a real-hardware 224 recording for final ground truth.
3. **Dynamic parity.** Drive the firmware emulator and the C++ core with the same parameter and time
   base; assert the C++ core's modulation + param de-zipper reproduce the firmware's live WCS frames
   (capture WCS frames from the emulator at control ticks; compare to the C++ core's WCS state).

Recommended core shape (per `480L_rom_to_plugin_guide.md`): one header-only C++17 class with an
**integer** datapath (`processSampleFixed(int32)->int32`, exact) consumed by the harness, plus a float
boundary (`processSample(float)->float`) for the DPF/STM32 wrappers.

---

## 10. Open items (resolve during the build)

**Must find FIRST — these block even a functional (not-yet-bit-exact) core:**
- **FPC audio I/O steps** — *where the input sample is injected onto the DAB, and which steps read the
  4 output channels (A,B,C,D).* Without this the ARU has no defined input/output and no audio can run.
  Findable: Manual §3.8 (FPC) + the Zero-Delay / Max-Delay diagnostic programs describe the routing
  (left→A,D; right→B,C); the input/output steps are specific microword steps doing FPC reads/writes.
- **Executed step count + program-end RESET** (§1/§5 contradiction) — does the ARU run exactly 100
  steps, or a per-program count up to 128? Where is the RESET microword? This sets the sample rate and
  which steps are live.

**Bit-exact arithmetic (tune via §9 layer 2, the diff loop):**
- result-register shift (20→16), coeff denominator (≈/128) + the 2 extra LSBs, rounding (toward-zero?)
  and the exact saturation, and **`b3`** (which steps read vs write DMEM). The datapath model already
  runs the *routing* correctly; these set the exact gain/decay. Anchor with the Manual multiplier test
  vectors (§4).

**Lower priority / corroboration:**
- **RA→bit 100%-authoritative** — the ARU schematic **#060-01318 is in hand** (confirms the LS670
  4×4-register-file array with independent RA/WA nets — the structure RA=(b5,b4) requires). The exact
  microword-bit→signal wiring would come from **T&C schematic #060-02475** / the backplane pinout (not
  yet obtained); current RA resolution is datapath-validated + schematic-corroborated.
- **Full bidirectional param curves** — sweep slider range below 0x20 (current grid is 0x20–0xFF).
- **Per-program modulation rate/depth** — read `0x3cd3`/`0x3cd4`/`0x3ccd` per program at boot (CONCERT
  given); a small batch pass captures all 20.

---

## 11. Quick reference — key addresses

- WCS image: `0x4000–0x41FF` (4-byte steps; lane0=U49…lane3=U3, active-low).
- Program record array: `0xB800` (page-wrap walk; ID = record[0]); lookup `0x13B6→0x133E`.
- Name table `0xA002`; directory `0xA446` (`{flags=ID,group,sub,page-hi,len}`).
- Build engine: interpreter `0xAA9F`, step-builder `0xB55B` (FE path) / `0xB65A` (non-FE pre-built
  table @recbase+0xA7..0x2A7), coeff packers `0xB4F0`/`0xB4FF`, coeff source `0xB510`.
- Params: sliders `0x3c00–0x3c05`, last-seen `0x3c16+`, handler `0x85f2`, group table `0x3CF4`,
  param type `0x3c33`, page `0x3c3c`.
- Modulation: engine `0xAD5C`, rate `0x3cd3`, depth `0x3cd4`, enable `0x3ccd` bit6, phase counters
  `0x3e45/0x3e46`, value writes `0xAE6C` (delay) / `0xAE8E` (interp coeff).
- Boot/normal-op: reset `0x0000→0x003B`, LARC handshake `0x0067`/`0xC8`, POST → `0x00CC` → `0x813B`
  (normal op), main loop `0x8169`, program load `0x13B6`, display `0x82CF`.

---

*This document is the single source of truth for the 224XL reconstruction. Keep it in sync with the
per-topic docs (`224XL_microword_fieldmap.md`, `224XL_param_sweep.md`, `224XL_modulation_lfo.md`,
`224XL_record_name_map.md`) and the `tools/` reference implementations.*
