# Lexicon 480L — Host Memory Map, HSP Interface & Parameter Path

Reverse-engineering notes for the 480L **host-processor card** firmware, from static analysis of the
four ROM dumps (`ROM1`–`ROM4`) + 68008 disassembly (capstone), **cross-checked against the 480L
Service Manual, Chapter 4 (Circuit Description)** — the authoritative hardware reference.

**Confidence legend:** ✅ verified (manual and/or disassembly) · 🟡 inferred (strong evidence) ·
❓ open / unconfirmed.

> **Status of this revision:** all four ROMs are now placed in the address space (ROM4 located at
> `0xA0000` — §3), and the host→HSP transport is established as **memory-mapped DMA to slave RAM**
> via six 16 KB channels at **`0x48000`** (channel base confirmed from the driver — §6). An earlier
> revision's "shared-RAM / no window" conclusion is **retracted** (root cause in §6.3).

---

## 1. System overview

| Item | Finding | Conf. |
|---|---|---|
| Host CPU | **Motorola 68008** (8-bit bus, **20-bit address = 1 MB**); 68000-compatible ISA → clean 68000 disassembly | ✅ (manual §4.3/4.4) |
| RTOS | **VRTX/68000 Rev. 3.20**, Hunter & Ready 1986 (+ TRACER/68K debugger) | ✅ |
| Firmware build marker | `cap870826` | 🟡 |
| HSP boards | each = dual subsystem: two **Z80 "slave" CPUs @ 4 MHz**, each with Writable Control Store (WCS), micro-pipeline, custom DSP | ✅ (manual §4.2) |
| Slaves total | up to **six** (two per HSP board), reset/interrupt in pairs | ✅ |
| Host→slave transport | **memory-mapped DMA** to slave RAM via six 16 KB channels (`0x48000–0x5FFFF`) + slave control via `$C0015/16/17` | ✅ |
| Audio engine code | DSP microcode runs on the HSP Z80 slaves; **not** 68k code in these host ROMs | ✅ |

Clock: 16 MHz osc → 8 MHz CPU; also MIDICLK (500 kHz), ERRCLK (62.5 kHz). Reset PC `0x00066EAE`;
boot SSP `0x0000BFFC` (ROM2 is aliased low at reset for vector fetch, then runs at `0x60000`).

> **Address-map caveat.** The manual's *reference* config places DUARTs at `$60000`/`$64000` and the
> RAM cartridge at `$70000`; **this dump's** map (read from the code) places DUARTs at
> `0x40000`/`0x44000`, the cartridge at `0x10000`, and ROM4 at `0xA0000`. The map is set by PALs
> **U23/U24**, reprogrammed per ROM/RAM size — so base addresses are configuration-dependent. The
> `$C0000` strobe block is identical in both. Addresses below are **this dump's** map.

---

## 2. Address-space memory map (this dump) — complete

| Range | Size | Contents | Conf. |
|---|---|---|---|
| `0x000000–0x00FFFF` | 64 KiB | **System RAM** = battery-backed NVRAM (U38 8/32K + U39 32K). Boot stack (top `0xBFFC`); VRTX task stacks; **active-program image @ `0x00BB80`** (per-machine, `0x33E` stride — §5.4); internal **register/preset store @ `0xC584`** (`0x90` stride); cartridge-format flags @ `0xE1A6`. | ✅ |
| `0x010000–0x01FFFF` | 64 KiB | **Cartridge NVRAM** (manual: `$70000`). Register records @ `0x010004 + n×0x90`; warm-boot signature `0x5BA0` @ `0x010000`. | ✅ |
| `0x020000–0x02FFFF` | 64 KiB | **ROM1** — program directory: BE pointer table @ `0x020000` (program#×4); 144-byte records from file `0x2000`; bank names. | ✅ |
| `0x030000–0x03FFFF` | 64 KiB | unused | ✅ |
| `0x040000–0x043FFF` | 16 KiB | **DUART1** (68681) — MIDI (Ch A) + LARC1 (Ch B). Manual: `$60000`. §5.1. | ✅ |
| `0x044000–0x047FFF` | 16 KiB | **DUART2** (68681) — Computer-Automation (Ch A) + LARC2 (Ch B). Manual: `$64000`. | ✅ |
| `0x048000–0x05FFFF` | 96 KiB | **Slave DMA channels** — six 16 KB windows, slave *N* @ `0x48000 + N×0x4000`. Writing here bus-grants slave *N* and DMA-writes its Z80 RAM. Base confirmed (driver loads `0x48000` from ROM4 `0xA8834`). §6. | ✅ |
| `0x060000–0x07FFFF` | 128 KiB | **ROM2** — main firmware: vectors @ `0x060000`, VRTX, boot, serial, program/parameter manager (`0x79000–0x7D000`). | ✅ |
| `0x080000–0x09FFFF` | 128 KiB | **ROM3** — VRTX wrappers, MIDI/SysEx, parameter math, **and the slave-download/sync driver (`~0x88F00–0x89D00`)**. | ✅ |
| `0x0A0000–0x0BFFFF` | 128 KiB | **ROM4** (located this revision) — data/table ROM: parameter **page tables**, UI/controller **string tables** (e.g. ptr table @ `0xA9630`), and the slave-driver **data tables** (§6.2). *Not* RAM. | ✅ |
| `0x0C0000–0x0C001F` | — | **`$C0000` strobe block** — transfer registers, peak detectors, slave control, soft reset (discrete decode **U92**, not a PI/T). §5.3. | ✅ |
| `0x0C0020–0x0FFFFF` | — | unused | ✅ |

All four ROMs are now placed: **ROM1 `0x20000`, ROM2 `0x60000`, ROM3 `0x80000`, ROM4 `0xA0000`**
(27256/27512 sockets U40–U43; PAL U24 = chip selects). The **only RAM** is the low 64 KiB NVRAM
(U38/U39) plus the cartridge — there is no separate "working RAM" region (the `0xA0000` block earlier
assumed to be RAM is ROM4). Values ≥ `0x100000` in code are data constants (2²⁰ scale, masks, timing);
the 68008's 20-bit bus cannot address there.

---

## 3. ROM inventory — all placed

| ROM | Size | Maps at | Role | How located |
|---|---|---|---|---|
| ROM1 | 64 KiB | `0x020000` | Program directory (pointer table + records + names) | program-pointer table + resolver |
| ROM2 | 128 KiB | `0x060000` | Main firmware + vectors + VRTX + program/parameter manager | reset-vector table, self-linked calls |
| ROM3 | 128 KiB | `0x080000` | VRTX wrappers, MIDI/SysEx, parameter math, **slave-download driver** | ROM2↔ROM3 cross-calls |
| ROM4 | 128 KiB | **`0x0A0000`** | Data ROM: parameter page tables, UI string tables, slave-driver data tables | 70-entry self-pointer string table resolves only at `0xA0000`; no writes to region; 1272 ptrs into ROM2 |

---

## 4. RAM data structures (all in low 64 KiB)

| Address | Contents | Conf. |
|---|---|---|
| `…–0x00BFFC` | Supervisor boot stack (down from `0xBFFC`) | ✅ |
| `0x00BB80` | **Active-program parameter image** — per-machine, `0x33E` (830 B) stride; raw + derived runtime values (§5.4) | ✅ |
| `0x00C206` | program-manager system variable | 🟡 |
| `0x00C584` | **Internal register/preset store** — 144-byte records | ✅ |
| `0x00E1A4 / 0x00E1A6` | register-count / cartridge-format flags (`0x2B67`,`0x1E61`) | ✅ |
| `0x010004 + n×0x90` | **Cartridge register** records (battery-backed) | ✅ |

Note: `0xAC44` (previously listed as a RAM "alternate buffer") is actually **inside ROM4** —
a stored reference/default parameter set used by the display/compare path, not RAM scratch.

The boot RAM test writes/verifies `0xA55AA55A` at `0xB828`/`0xBFFC`, confirming the `0xBB80` image is
in genuine read/write memory. ✅

---

## 5. Peripherals & key structures

### 5.1 Dual DUART (68681) — `0x040000` / `0x044000`

| | Channel A | Channel B |
|---|---|---|
| **DUART1** (`0x40000`; mfr `$60000`) | **MIDI** in/out | **LARC 1** (RS-422) |
| **DUART2** (`0x44000`; mfr `$64000`) | **Computer Automation** (RS-422) | **LARC 2** (RS-422) |

Register file (A3–A0 select; manual Table 4.8): `+0`/`+B` Rx/Tx buffer A/B · `+1` status · `+2` mode/cmd ·
`+4` IPCR/Aux · `+5` ISR/IMR · `+6/7` counter · `+C` interrupt vector · `+D` **input port / OPCR** ·
`+E` **set OP bits** · `+F` **reset OP bits**. **`BLOCK/` = DUART1 OP4** (slave-DMA block-mode hold).
Inputs: IP5 `PLOCK`, IP1 `WCPRES`, IP0 `OVLDB`. The serial handler (XON/XOFF + RX/TX polling) is the
LARC/MIDI link; it never touches the `0xBB80` image or the slave channels.

### 5.2 Interrupts (68008, 3 levels)

L7 `PF/` Power-Fail (→ NVRAM-protect housekeeping) · L5 DUART1+DUART2 (shared, **round-robin**;
NVRAM user vectors) · L2 `SLAVEINT/` (a slave raising an interrupt; HSP `4002H` strobe).

### 5.3 `$C0000` strobe block (discrete, U92) — full map

| Addr | Strobe | Function |
|---|---|---|
| `$C0000/01/02` | `XFERINLO/MID/HI` (R) | Read 24-bit **transfer-in** register |
| `$C0003` / `$C0004` | `RDPEAKL/` / `RDPEAKR/` (R) | Read + clear L / R digital peak (8-bit) |
| `$C0007` | `SOFTR/` (R) | Soft reset → `SR/`, **resets all slaves** |
| `$C0010/11/12` | `XFOUTLO/MID/HI` (W) | Write 24-bit **transfer-out** register |
| `$C0015/16/17` | `SP0WR//SP1WR//SP2WR/` (W) | **Slave-pair control** (slaves 0,1 / 2,3 / 4,5) |

**Transfer registers** = a 24-bit host↔HSP side channel (host writes `$C0010-12`, HSP reads via wet-bus
`$3F`; HSP writes wet `$3E`, host reads `$C0000-02`) for **wave-table download, diagnostics, sample
upload** — not the main parameter path. (Boot writes `0xFF/0xFF/0x7F` here = transfer-out test pattern.)
**Slave control reg** = U30 (74HCT175 quad-FF, hardware-verified): active-low D0 `INT1/`, D1 `RESET1/`,
D2 `INT2/`, D3 `RESET2/`; writing `$0D` to `$C0015` resets only slave 0; `SR/` clears all (boot does
`clr.b $C0015/16/17` → all slaves held reset). ✅

### 5.4 Active-program parameter image @ `0x00BB80`

Per machine, `0x33E` (830 B) stride. Host's working copy: `+0x08` descriptor ptr; `+0x1E2` parameter
block (resolved-record copy target); `+0x22x` working/derived words; `+0x2A` fixed-point derived value
(×2²⁰); `+0x2EE` machine-ready gate (`==4`); `+0x2F0` status; `+0x37/38/3D` coefficient bytes. The
ROM3 slave driver reads this image and DMA-writes the relevant data into the slave channels (§6).

---

## 6. Host→HSP parameter path — traced

### 6.1 Host-side preparation (verified)

Resolver `0x07CCBA` maps a number → 144-byte record (ROM1 program / `0xC584` register / `0x010004`
cartridge). Live-load (callers `0x07A75C`/`0x07AA8E`; finalize `0x07AABC`) validates the machine
(`cmpi.w #$4, $2EE(struct)`) and copies+transforms the record's parameters into the `0x00BB80` image
(transforms `0x9071C`/`0x9074A`/`0x90778`; coefficient derivation `0x8591C`), bracketed by VRTX
`trap #0` `0x20`/`0x21` (scheduler **lock/unlock**). `TRAP #0`=`TRAP #1` → VRTX dispatcher `0x060118`.
(`0x0912F6` separately re-encodes records as MIDI/SysEx; `0x096DD6` reads the image for display/compare.)

### 6.2 Slave download — the transport (manual §4.2.2/§4.3 + located driver)

Host → slave is **bus-grant DMA**: the host writes a **slave-channel** address (`0x48000 + N×0x4000`);
PAL U23 asserts `SLAVEAS/`, presents host A19–A0 to slave *N*; U33 issues `DMAREQ N/`; the Z80 returns
bus-grant (`DMAACK/`); the host's stalled access completes (`DMADTACK/`) and writes the slave's RAM.
**Block mode** (`BLOCK/` = DUART1 OP4) holds the slave for bulk transfer. Run control via `$C0015/16/17`
(reset/release/INT) and `$C0007` (global). Once running, the slave folds the new bytes into its WCS
microcode at the next sample period — so a parameter change is a tiny DMA write, no audio-rate bandwidth.

**The driver (disassembled).** The slave-bring-up code is **ROM3 `0x89BF6`** (orchestrator) +
**`0x89C90`** (per-slave worker), reading two ROM4 tables:

- **Channel-base table @ `0xA8834`** — six entries, one per slave, verified:
  `0x48000, 0x4C000, 0x50000, 0x54000, 0x58000, 0x5C000` (16 KB apart, slave *N* @ `0x48000+N×0x4000`).
- **Slave-control pointer table @ `0xA8818`** — `[0xC0015, 0xC0016, 0xC0017]` (the three slave pairs).

The worker `0x89C90` executes the manual's bring-up sequence literally, per slave *i*:

```
movea.l #$A8834,a0 ; movea.l (a0,i*4),a2   ; a2 = slave i channel base (0x48000 for i=0)
movea.l #$A8818,a0 ; movea.l (a0,pair*4),a3 ; a3 = pair control reg (0xC0015/16/17)
move.b  d0,(a3)                             ; RELEASE slave (compose reset/INT byte -> $C0015)
move.b  (a2),d2                             ; read-back old byte from slave RAM
move.b  #$76,(a2)                           ; *** DMA WRITE into slave RAM[0] via the 0x48000 window ***
clr.b   (a3)                                ; RESET slave again ($C0015 = 0)
```

`0x76` is the **Z80 `HALT` opcode** — this is the manual's "download a minimal program to slave
location zero," i.e. a power-up probe that parks each slave at HALT and read-back-tests its RAM. It
**hardware-confirms**: the `0x48000` window writes straight into slave Z80 RAM, run-control is
`$C0015/16/17`, and the slaves are Z80s. The companion routine `0x890E0` is the **slave-control
writer** — it composes each pair's reset/INT byte from ROM4 masks OR'd with per-pair RAM state
(`0xE450/51/52`) and writes `0xC0015/16/17`. (These probe writes are single bytes = byte mode; no
`BLOCK/` immediate exists in the firmware — per the manual, byte mode auto-handles multi-byte
transfers, holding the slave bus until the host next touches non-slave space.) So: driver *code* =
ROM3, driver *data* = ROM4, transport = byte-mode DMA into the `0x48000` slave windows. ✅

### 6.3 Why "shared RAM / no window" was wrong

The parameters genuinely don't leave via the DUART data ports or the `$C0000` strobes — that held up.
The error was concluding "therefore the HSP reads host RAM." The real path is **memory-mapped DMA into
slave RAM at `0x48000`**, driven by ROM3 code via ROM4 tables. The earlier scans missed it because the
driver's table base lives in **ROM4 (then unplaced)**, the channel base is a **ROM4 data constant** (not
an instruction immediate, so invisible to an immediate-only base scan), and a 40-result cap in the
gap-pointer scan exited on ROM1's coincidental matches before reaching ROM4. The `lock/unlock` (not
`lock/notify`) around the `0xBB80` update fits a host slave-service task that reads the image and pushes
it, rather than an autonomous HSP reader.

---

## 7. Boot sequence (annotated, from `0x066EAE`)

```
066EAE  move.w  #$2700,sr        ; supervisor, ints masked
066EB2  movea.l #$BFFC,a7        ; boot stack
066EB8  cmpi.w  #$5BA0,$10000    ; warm-boot signature?
066EC4  jmp     $10002           ;   -> warm-boot entry (if matched)
066ECA  reset                    ; RESET to peripherals
066ECE  move.b  $C0007,d0        ; SOFTR/ -> SR/ : reset all slaves
066ED4  clr.b   $C0015/16/17     ; slave-pair regs = 0 : hold all slaves reset
066EE4  clr.b   $4000D / $4400D  ; DUART output-port config = 0
066EF0  ...set/reset DUART OP bits...
066F20  bsr     $67A4A           ; config download + RAM test
```

---

## 8. Key routines

| Address | Routine | Conf. |
|---|---|---|
| `0x066EAE` | Reset / cold boot | ✅ |
| `0x066ECE–0x066EE0` | Slave global reset + hold (`$C0007`, `$C0015/16/17`) | ✅ |
| `0x067210–0x067330` | Serial handshake (DUART; XON/XOFF, `trap #1`) | ✅ |
| `0x067A4A` | Config download + RAM test | ✅ |
| `0x060118` | **VRTX kernel dispatcher** (`TRAP #0`=`TRAP #1`) | ✅ |
| `0x07CCBA` | Program/register resolver | ✅ |
| `0x07AABC` | Load finalize — params → `0xBB80` image | ✅ |
| `0x09071C`/`0x09074A`/`0x090778`, `0x08591C` | Parameter transforms / coefficient derivation | ✅ |
| `0x0912F6` | MIDI/SysEx record encoder | ✅ |
| `0x089BF6` | **Slave bring-up orchestrator** (loops all 6 slaves; spawns the worker, waits, resets) | ✅ |
| `0x089C90` | **Per-slave worker** — release (`$C0015`), `move.b #$76,(0x48000+N×0x4000)` HALT-probe DMA into slave RAM, reset | ✅ |
| `0x0890E0` | **Slave-control writer** — composes & writes `$C0015/16/17` reset/INT bytes | ✅ |

---

## 9. HSP (slave) board internals — manual §4.2 (reference)

Each HSP board = two subsystems; each = **Slave Z80 (4 MHz)** + Writable Control Store + micro-pipeline
+ DSP (arithmetic + MMU + audio memory) + audio I/O onto the shared "wet" bus. The WCS is dual-ported
slave/DSP by phase-stealing (slave gets 1 of 4 clock phases); DSP PC counts 0–79 per sample. The slave
loads DSP microcode into the WCS, then continuously updates offsets/coefficients.

**Slave Z80 memory map (Table 4.1):** `0000–1FFF` 8K SRAM · `2000–3FFF` read DAB · `4000–47FF` WCS
Bank A (`4000` page-select, `4001` I/O enable, `4002` slave→host int, `4003` wait-enable) · `6000–67FF`
WCS Bank B. This SRAM is what the host DMA-writes through the host-side slave channels at `0x48000`.

---

## 10. Open / unconfirmed items

- 🟡 **Parameter-download routine** — the bring-up *probe* (HALT to slave RAM[0]) is fully disassembled;
  the routine that streams **live parameter/coefficient bytes** from the `0xBB80` image into the slave
  channels during play uses the same `0x48000` windows but hasn't been isolated yet.
- 🟡 **VRTX call-number map** for this build (`0x20`/`0x21` inferred as lock/unlock).
- ℹ️ **Manual vs. dump base addresses** differ (PAL U23/U24 config); `$C0000` block identical.
- ✅ *(resolved)* ROM4 at `0xA0000`; six slave channels `0x48000–0x5FFFF` (table @ `0xA8834`);
  slave control `0xC0015/16/17` (table @ `0xA8818`); literal slave-RAM DMA write shown; "working RAM"
  reclassified as ROM4.

---

## Appendix — host→HSP transport, hypotheses resolved

| Hypothesis | Verdict | Basis |
|---|---|---|
| Params out a DUART data port | ❌ | No param-path writes to `0x4x002/3`; serial code never touches `0xBB80` |
| Params via `$C0000` strobes | ❌ (for params) | `$C0000` = transfer-reg/peak/slave-control; transfer regs carry wave tables/diagnostics |
| Shared RAM — HSP reads host image | ❌ retracted | Manual: host *writes* slave RAM; no autonomous HSP read of host memory |
| **Memory-mapped DMA to slave RAM (`0x48000` channels)** | ✅ **confirmed (line-by-line)** | Manual §4.2.2/§4.3; ROM3 worker `0x89C90` does `move.b #$76,(0x48000)` into slave RAM, framed by `$C0015` release/reset; channel table @ ROM4 `0xA8834` = six 16K windows; byte-mode (no `BLOCK/`) |

---

*Static-analysis + service-manual notes; addresses are byte offsets in the 68008's 1 MB space. DSP
microcode runs on the HSP Z80 slaves and is not present in these host ROMs.*
