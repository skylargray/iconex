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

**Step count = 128, fixed (RESOLVED, verified).** The 224XL executes **all 128 WCS steps (0–127) every
sample** — verified three ways: the build loop `0xB65A` (`LD C,0x80`) and the WCS hardware-copy `0xAB55`
(`LD B,0x80`) both process 128 steps, and the last program-content step = **127** in every program
booted (CONCERT/PLATE/BRIGHT/DARK/SMALL ROOM/CHAMBER). The earlier "~100/~110" was an undercount of
non-NOP steps; NOPs are interspersed but still execute (as pure-delay/no-op cycles). **RESET = a
hardwired 8-bit-counter terminal-count wrap (no microword bit)** — verified: AND-ing step-127's 32-bit
word across all programs and removing bits present in any other step yields `0x00000000` (no
end-of-program marker). So the C++ core loops `S = 0..127` and resets at the loop boundary.

**Sample rate.** 224X = 3.41 MHz ÷ 100 = 34.13 kHz (manual). The 224XL runs 128 steps; its published Fs
is still ≈34.13 kHz, implying a proportionally faster T&C step clock ≈ **4.37 MHz** (≈229 ns/cycle).
*Firmware-certain: 128 steps/sample.* The exact clock/Fs is an inference (the T&C clock is hardware,
not firmware-visible) — confirm with a hardware Fs measurement or T&C schematic #060-02475.

### SBC memory map (for driving the emulator)

| Region | Window | Role |
|---|---|---|
| SBC1 | 0x0000–0x07FF | reset, LARC serial, boot, power-up self-test |
| SBC2 | 0x0800–0x0FFF | ARU/DSP I/O drivers, POST |
| SBC3 | 0x1000–0x17FF | program directory/load, NVS dispatch |
| battery RAM | 0x2000–0x27FF | user registers (saved program variations); 0xFFFF = DIP switch |
| SBC RAM / stack | 0x3C00–0x3FFF | working state, stack; **WCS image staged + modulated here** |
| **WCS** | **0x4000–0x41FF** | the **128-step** microprogram (4 SRAMs, see §3); memory-mapped to SBC |
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
for S in 0..127:                                    # ALWAYS 128 steps/sample (verified, §1); no early stop
  off14 = offset & 0x3FFF
  if offset & 0x8000:                               # FPC select (bit15) -> analog I/O, not DMEM (§3 FPC)
     ch = (offset & 0x4000) ? LEFT(A,D) : RIGHT(B,C)
     if WA == 2:        dab = FPC_in[ch]            # RD AD/  : input read  (off14 == 0x3FFF)
     elif WA == 3:      FPC_out[ch] = RES; dab = RES# WR DA/  : output write (off14 = strobe/tap)
  else:
     addr = (position - offset) & 0xFFFF            # ordinary DMEM tap
     dab  = (write op) ? (DMEM[addr] = RES, RES) : DMEM[addr]
  R[WA]  = dab                                       # register write every cycle (WA=3 = pass-through)
  prod   = multiply20(R[RA], coeff, CSIGN)          # 16x6 saturating, 20-bit alignment above
  if ZERO: ACC = 0
  ACC    = saturate20(ACC + prod)
  if XFER: RES = saturate16(ACC >> SHIFT)           # SHIFT/rounding = OPEN arithmetic detail (§4)
position += 1                                        # RESET is implicit at the loop boundary (no microword bit)
```

**128 steps = one output sample** (fixed for all programs — see §1); `position += 1` per sample. The
reverb's recirculating tank lives in the DMEM + register feedback; the `+0.976`-class coefficients on
XFER steps close the loops. (`write op` = whether a non-FPC step writes vs reads DMEM — tied to the
`b3` RW/SRC bit / XFER; an OPEN arithmetic detail, §4.)

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

**RA/XFER resolution** (the hard part, now settled + schematic-confirmed): running the decoded CONCERT
microcode through the ARU datapath, `RA=(b5,b4)` is the **only** assignment that forms a coherent
recirculating reverb tank; `(b5,b3)`/`(b4,b3)` collapse to silence. Corroborated by data-flow liveness,
the RA-independent-of-WA constraint, and XFER=b2 firing on exactly the result-transfer steps. The exact
split of lane2[5:2] = `b5,b4`=RA · `b3`=RW/SRC · `b2`=XFER.

**T&C schematic #060-02475 (now in hand) authoritatively confirms the field architecture.** Reading the
microinstruction → ARU connector signal map off the sheet: `OFST0–OFST15` = pins A9–A24 (16-bit offset);
**`WA0/`=A44, `WA1/`=A45, `RA0/`=A46, `RA1/`=A42** (separate 2-bit read + write addresses); **`XFER/`=A49,
`CSIGN/`=A48, `ZERO`, `PROT/`** each a distinct line; coefficient `C0/–C5/` serialized (U10/U11);
FPC strobes `RD AD/`, `WR DA/`, channel selects `SDAA–SDAD` (U32). **Every control signal is active-low**
(the `/` suffix) — confirming the complemented-storage decode — and **every field is a separate signal**
— confirming RA≠WA independence. `RESET/` is generated by flip-flop **U25 (74S74)**, a decoded/registered
signal, **not** a microword data bit (confirming §1's hardwired counter-wrap RESET). The schematic thus
confirms the field structure, active-low storage, and RESET mechanism; the literal microword-bit→pin
*index* wiring (the U19/U45 register taps) is at the scan's legibility limit, but the bit assignment is
already datapath-validated (above).

Decoder: `tools/decode_microword.py` (`decode(power_up_id)` → per-step dicts with delay, coeff, CSIGN,
WA, RA, RW, XFER, ZERO, PROT).

### FPC audio I/O (address-decoded into the offset field) — full details in §12

Analog I/O is selected by the **offset high bits** (no dedicated FPC bit): **`offset & 0x8000` = FPC
select** (vs delay RAM); **`offset & 0x4000` = channel** (0 = right→B,C / 1 = left→A,D). **Input read** =
read step `WA=2`, bit15 set, `low14 = 0x3FFF` (`RD AD/`); **output write** = pass-through `WA=3` step,
bit15 set (`WR DA/`, channel from bit14). Verified via the Zero/Max-Delay diagnostic programs — full
derivation, the decoded diagnostic table, and the live-image position-base caveat are in **§12**.

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

**RESOLVED (these were the two gating items):**
- **FPC audio I/O — RESOLVED (§12).** Address-decoded into the offset field: bit15 = FPC select, bit14 =
  channel (0=right→B,C / 1=left→A,D); input = read step `WA=2, low14=0x3FFF` (`RD AD/`); output =
  pass-through `WA=3` step (`WR DA/`). Verified by building the Zero/Max-Delay diagnostic programs
  (`0x0EFD`/`0x0EF4` → builder `0x0F2C`).
- **Executed step count + RESET — RESOLVED (§1).** **128 steps/sample, fixed** for all programs
  (verified: build loop `0xB65A`/WCS copy `0xAB55` both 128; last content step = 127 in every program).
  **RESET = hardwired counter terminal-wrap, no microword bit** (verified: no bit unique to step 127).
  Loop `S=0..127` and reset at the boundary.

**Open (resolve during the build):**
- **Per-program position base** — needed to apply the FPC bit15/bit14 decode and align DMEM read/write
  tap pairs in *live* images (diagnostic images decode cleanly; live offsets are base-relative). Anchor:
  the input read at offset `0xFFFF` (`WA=2, low14=0x3FFF`) ⇒ address = position+1. The main remaining I/O
  sub-task. Live reverbs are **mono-in / stereo-out** (one input read; outputs split L→A,D / R→B,C).
- **224XL step clock / exact Fs** — 128 steps × ~34.13 kHz ⇒ ~4.37 MHz step clock (inferred; confirm via
  a hardware Fs measurement or T&C schematic #060-02475).

**Bit-exact arithmetic (tune via §9 layer 2, the diff loop):**
- result-register shift (20→16), coeff denominator (≈/128) + the 2 extra LSBs, rounding (toward-zero?)
  and the exact saturation, and **`b3`** (which steps read vs write DMEM). The datapath model already
  runs the *routing* correctly; these set the exact gain/decay. Anchor with the Manual multiplier test
  vectors (§4).

**Lower priority / corroboration:**
- **RA→bit — schematic-confirmed.** Both schematics are now in hand: ARU **#060-01318** (LS670 register
  file, independent RA/WA nets) and T&C **#060-02475** (the full signal map: OFST0-15=A9-A24, WA0/=A44,
  WA1/=A45, RA0/=A46, RA1/=A42, XFER/=A49, CSIGN/=A48, ZERO, PROT/, all active-low; RESET/ from flip-flop
  U25, not a microword bit). These confirm the field structure, active-low storage, and RESET mechanism.
  Only the literal microword-bit→pin *index* wiring is at the scan's legibility limit; the bit
  assignment itself is datapath-validated. (Effectively closed.)
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

## 12. FPC audio I/O — the input read & 4 output writes (RESOLVED)

**How recovered.** The two minimal diagnostic programs whose behavior is fully specified by the manual
(§5: "7 ZERO DELAY" = input straight to output, no DMEM; "8 .5 S DELAY" = input → 0.5 s delay → output;
both route left→A,D, right→B,C) are *built in ROM*, not stored as records. The diag-menu dispatch
(SBC1 `0x032D` `JP 0x11BE` over the table at `0x0330`) sends item 7 → handler **`0x0EFD`** (ZERO DELAY)
and item 8 → **`0x0EF4`** (MAX/.5 s DELAY). Both call the WCS builder **`0x0F2C`**, which:
1. fills `0x4000–0x41FF` with `0xFF` (all-NOP);
2. reverse-copies (routine `0x0933`/`0x0938`, writes *downward* from `0x41FF`) a 4-step block from ROM
   `0x0F5F` into steps **124–127** (LEFT) and a 4-step block from ROM `0x0F6F` into steps **74–77**
   (RIGHT) — so source bytes land in lane order `[l3,l2,l1,l0]`;
3. patches step 29 (`0x4074=0xF7`, `0x4076=0xFE`);
4. issues `OUT(0x01)` then `OUT(0x03)` (= RUN).
ZERO DELAY's handler additionally patches the two `WA=3` output steps' offset low bytes
(`0x4130/0x4131` → step 76, `0x41F8/0x41F9` → step 126) to shorten the delay to ~0.

**Decoded diagnostic blocks** (offset = `~(l1<<8|l0)`; `ctl=~l2`; coeff = raw `l3`):

| pgm | step | l0 l1 l2 l3 | offset | b15 | b14 | low14 | WA | coeff | role |
|---|---|---|---|---|---|---|---|---|---|---|
| MAX | 74  | 7f e9 fe ff | 0x1680 | 0 | 0 | —     | 1 | −1.000 | DMEM delay-line (right) |
| MAX | 75  | 00 40 fd fe | 0xBFFF | 1 | 0 | 0x3FFF| 2 | −0.992 | **FPC INPUT read (right), RD AD/** |
| MAX | 76  | ff 7f fc 7c | 0x8000 | 1 | 0 | 0x0000| 3 | +0.976 | **FPC OUTPUT write (B,C), WR DA/** |
| MAX | 77  | ff cf fe 7d | 0x3000 | 0 | 0 | —     | 1 | +0.984 | DMEM delay-line (right) |
| MAX | 124 | 7f e6 fe ff | 0x1980 | 0 | 0 | —     | 1 | −1.000 | DMEM delay-line (left) |
| MAX | 125 | 00 00 fd fe | 0xFFFF | 1 | 1 | 0x3FFF| 2 | −0.992 | **FPC INPUT read (left), RD AD/** |
| MAX | 126 | ff 3f fc 7c | 0xC000 | 1 | 1 | 0x0000| 3 | +0.976 | **FPC OUTPUT write (A,D), WR DA/** |
| MAX | 127 | ff cf fe 7d | 0x3000 | 0 | 0 | —     | 1 | +0.984 | DMEM delay-line (left) |

(bit14 carries the channel only on FPC steps, where bit15=1: the left FPC steps 125/126 have bit14=1;
the plain DMEM delay steps 124/127 have bit14=0 — bit14 is just part of an ordinary delay address there.)

(ZERO DELAY = identical except step 76 offset → `0xBFFE` and step 126 offset → `0xFFFE`; i.e. the *only*
bytes that differ between zero-delay and half-second-delay are the `low14` of the two `WA=3` output
steps — proving those steps are the output writes and that the output offset's low bits set the tap.)

**The FPC encoding (authoritative for the C++ core):**
- **`offset & 0x8000` (bit15) = FPC select.** When set, the access targets the FPC "device on the DAB"
  (§3.8: "the analog I/O looks simply like another device that can be read from / written into via the
  DAB") instead of delay RAM. Delay-line steps have bit15 = 0.
- **`offset & 0x4000` (bit14) = channel group.** 0 → right channel (input R; outputs **B,C**); 1 → left
  channel (input L; outputs **A,D**). Matches the manual's program routing left→A,D, right→B,C.
- **Input step** = a *read* step (non-XFER, `WA≠3`) with bit15 set and `low14 = 0x3FFF`. Asserts RD AD/;
  the A/D sample for that channel is driven onto the DAB and latched into the read register. (Diag uses
  `WA=2`.)
- **Output step** = the *pass-through* step (`WA=3`) with bit15 set; asserts WR DA/ with the channel
  select. The result register is driven to the FPC double-buffer for that output pair. `low14` is the
  output/strobe code (and, on the diag, doubles as the delay-tap selector).
- Every active diag I/O step has **ZERO=0, PROTECT=0, XFER=0, RW=0** (`ctl` ∈ {0x01,0x02,0x03}); the
  device is chosen purely by the **offset high bits**, *not* by a dedicated FPC microword bit. This is
  why the 32-bit microword has "no spare bit" — FPC I/O is address-decoded, identical to a DMEM
  read/write but at addresses with bit15 set. (Confirms the earlier scouting note: RESET/strobes are not
  dedicated microword bits; they are decoded from address/counter state in the T&C+FPC.)

**Caveat for *live* reverb images — the position base.** In the diagnostic programs the WCS is built
with a position base such that the FPC steps decode cleanly (input `low14 = 0x3FFF`, channel in bit14).
In a live program image (e.g. CONCERT from `boot_xl`) the stored offsets are **absolute and
position-relative** (§2: "absolute offsets are large relative to an arbitrary position base that cancels
across read/write pairs"). So bit15/bit14 of a *live absolute* offset is **not** by itself a clean FPC
marker — many ordinary delay taps have bit15 set merely because of the base. The reliable, base-invariant
fingerprint that *does* survive is the **input read** at `low14 = 0x3FFF` with `WA=2`: it appears in
CONCERT at **step 76** (`offset = 0xFFFF`, WA=2, coeff −1.0) — the input-injection step — exactly as in
the diagnostic. The diff harness (§9) must pin the per-program position base so the FPC address decode
lines up; once the base is subtracted, the bit15 = FPC / bit14 = channel rule holds for the live image
too. For the C++ core's per-step execution: branch on `(offset − base) & 0x8000` to route reads from the
FPC input latch (channel = `& 0x4000`) and `WA=3` writes to the FPC output channel (channel = `& 0x4000`,
strobe = `low14`), instead of reading/writing DMEM. Pinning `base` per program is the remaining sub-task
(it is the same base that makes the read/write tap pairs align in DMEM).

---

*This document is the single source of truth for the 224XL reconstruction. Keep it in sync with the
per-topic docs (`224XL_microword_fieldmap.md`, `224XL_param_sweep.md`, `224XL_modulation_lfo.md`,
`224XL_record_name_map.md`) and the `tools/` reference implementations.*
