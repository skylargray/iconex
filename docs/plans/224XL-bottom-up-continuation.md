# 224XL reconstruction — bottom-up continuation plan & session handoff

> **READ THIS FIRST if you are a new session.** This is the start-here doc. It captures the method,
> the verified state, every tool/address/fact you need, the next steps, and the mistakes that wasted
> entire prior sessions so you don't repeat them. The **living status board** is
> [`224XL-interp-stack.md`](224XL-interp-stack.md) — keep it updated as you verify each layer.

---

## 0. One-paragraph orientation

We are reconstructing the **Lexicon 224XL** digital reverb (1980s, an 8080-managed microcoded DSP) as a
bit-exact software model, from ROM dumps + schematics + the service manual. Nine prior sessions kept
declaring things "CONFIRMED" that were wrong, because they validated by *plausibility* ("looks like a
reverb") instead of *ground truth*. We have switched to a **strict bottom-up, layer-by-layer verification**
method. As of 2026-06-26, layers **L1–L3 are VERIFIED** (the 8080 CPU, the firmware boot, and the program
the firmware builds). The frontier is **L4–L6** — the **ARU/T&C** (the actual DSP), which we can only
*infer* and which is where every catastrophic flaw has lived. Do **not** jump to the audio output (L7);
it's a pass/fail oracle with zero diagnostic power and is the *last* thing we do.

---

## 1. The method (do not deviate)

1. **Two processors, one hard boundary.** The **8080 (SBC)** runs the firmware that *builds* the DSP
   microcode. The **ARU + T&C** is a separate processor that *executes* it. We have a **bit-exact emulator
   for the 8080** (so L1–L3 are verifiable ground truth). We have **no ground-truth emulator for the ARU**
   — everything about how it interprets the microcode (L4–L6) is inference.
2. **A layer is ✅ only when verified by something independent of our own interpretation** — a standard test
   suite, the firmware's own self-test (POST), a schematic net-trace by the owner, or real-hardware
   measurement. "It looks right / it makes a plausible reverb" is **not** verification.
3. **Verify bottom-up.** L1 → L2 → … Never trust a higher layer while a lower one is unproven.
4. **The IR comparison (L7) is LAST.** Comparing our impulse response to a real 224XL only tells you
   *that* it's wrong, never *why/where*. Useless as a debugging tool. Only meaningful once L1–L6 are each ✅.
5. **Quote the evidence.** For any firmware claim, quote the disassembly (addr: bytes mnemonic). For any
   hardware claim, cite the schematic net or the POST result. Mark confidence honestly
   (✅ VERIFIED / 🔶 IN PROGRESS / ❌ FAITH / ⬜ PENDING).

---

## 2. The interpretation stack (status board summary)

| Layer | What it is | Status | Verified by |
|---|---|---|---|
| **L1** 8080 CPU core | execute SBC ROM | ✅ VERIFIED | `z80.I8080Machine` passes cputest/8080pre/**8080exm** |
| **L2** firmware exec | boot → POST → program-load | ✅ VERIFIED | `tools/boot8080.py`; faithful POST + real PGM-2 bypass; WCS cross-checked |
| **L3** program build | firmware writes 0x3F4D offsets + 0x4000 WCS | ✅ VERIFIED (CONCERT) | bytes built on verified 8080; byte-identical to old pipeline (modulo LFO) |
| — | **GROUND-TRUTH BOUNDARY** (below = ARU inference) | | |
| **L4** microword field decode | 4 bytes → offset/WA/RA/CSIGN/XFER/ZERO/coeff/device | ❌ FAITH | bit-map only human-schematic-read; **most errors live here** |
| **L5** address arithmetic | offset → DRAM cell (addr = CPC − offset) | ❌ FAITH | adder/mux wiring; bits 12/13 dual-use |
| **L6** ARU datapath | regfile × /32 mult + accumulate + DMEM r/w + timing | ❌ FAITH | only a POST slice checked |
| **L7** audio result | run L6 over samples → reverb IR | ⬜ LAST | real-unit IR, only after L1–L6 ✅ |

Full annotated stack with per-layer detail: [`224XL-interp-stack.md`](224XL-interp-stack.md).

---

## 3. Environment & key files

- **Repo root:** `d:/OneDrive/Gray Instruments/iconex` · Windows · Python 3.14 · use the Bash tool.
- **ROM dumps:** `ROMs/Lexicon 224/224XL v8_21/` — `SBC{1,2,3} 2716.BIN`, `NVS{1..8} 2732.BIN`.

### Tools (current)
| File | Purpose | Notes |
|---|---|---|
| `tools/boot8080.py` | **★ THE faithful boot** on the verified 8080 | USE THIS. Reaches program-load via real PGM-2 bypass. |
| `tools/dis224.py` | disassemble SBC(0x0000-0x17FF) or NVS(0x8000+) | `python tools/dis224.py <start_hex> <end_hex>` ; `... scan 02 06 07` for I/O sites |
| `tools/disrange.py` | disassemble NVS at true addresses | `python tools/disrange.py <start> <end>` |
| `tools/aru224_emulate.py` | offset/coeff decoder (`tap_map`, `capture_coeffs`) | ⚠ still runs the OLD `z80emu` — offsets verified to match, but port to `boot8080` for rigor |
| `tools/aru_datapath.py` | ARU datapath model (L6) — field decode + run | ❌ unverified L4/L6; the place to fix once ARU is validated |
| `tools/_trackB_post.py` | Track-B faithful ARU port model (old emulator) | reference for the ARU POST work |
| `tools/boot_xl.py`, `tools/z80emu.py` | **RETIRED** old boot + emulator | `z80emu.py` has the 8080 parity bug — do not use for new work |

### Docs (read these)
- `docs/plans/224XL-interp-stack.md` — **live status board** (update as you go).
- `docs/plans/224XL-validation-plan.md` — the earlier adversarial validation plan (Tracks A–F) + §5 results.
- `docs/reference/224/224XL_system_architecture.md` — **§5–6 = the address arithmetic** (offset→addr, banks).
- `docs/reference/224/224XL_microword_fieldmap.md` — the L4 bit-map (the thing to verify).
- `docs/reference/224/224XL_track{AC,B,D,E,E2}_results.md` — prior multi-agent investigation results.
- `docs/reference/224/Lexicon-224X-Service-Manual.md` — §3.6–3.7 ARU/timing; §5.x DIAG/POST.
- `docs/reference/224/LARC_Theory_of_Operation.md` — the LARC remote (button scanning, serial).
- `docs/reference/224/"224XL ARU pinouts from 060-01318.txt"` — owner's ARU chip pinouts.
- Memory: `.../memory/224xl-validation-2026-06-26.md` (prior frontier) and `MEMORY.md` index.

---

## 4. L1 — the verified 8080 core (how to reproduce)

**Package:** `kosarev/z80` (https://github.com/kosarev/z80) — a C++ Z80/**i8080** emulator with a Python API.
It is **not on PyPI as a wheel**; it builds from source and needs a **C++ compiler** (MSVC; already installed
on this machine — VS Build Tools at `C:/Program Files (x86)/Microsoft Visual Studio/...`).

```bash
git clone https://github.com/kosarev/z80   # e.g. into a scratch dir
pip install ./z80                          # setuptools auto-finds MSVC; builds a native wheel
python -c "import z80; print(z80.I8080Machine())"   # confirm
```
Currently installed: `z80-1.0b3`. **Validate it yourself** (don't trust the README): the exhaustive
exercisers ship in the repo at `examples/supplements/{cputest,8080pre,8080exm}.com`; run them through an
`I8080Machine` with a CP/M BDOS shim (see `examples/exercisers.py`). `8080exm` CRC-checks every opcode+flag
combo (≈37 s) — passing it = bit-exact 8080. **All pass.**

### I8080Machine API (record — saves you the rediscovery)
```python
import z80
m = z80.I8080Machine()
m.set_memory_block(addr, b)        # load bytes;  m.memory is a writable 64K view (m.memory[a]=v works)
m.pc, m.sp, m.a..m.l, m.af/bc/de/hl   # registers as properties (read+write)
m.ticks_to_stop = N; ev = m.run()  # run ≤N ticks; ev & 2 = BREAKPOINT_HIT, ev & 1 = END_OF_FRAME
                                   # elapsed ticks this run = N - m.ticks_to_stop
m.set_breakpoint(a); m.clear_breakpoint(a)
m.set_input_callback(fn)           # fn(port)->value     (IN)
m.set_output_callback(fn)          # fn(port, value)     (OUT)
m.set_read_callback / set_write_callback   # optional memory hooks (slow; usually unneeded)
snap = bytes(m.get_state_view()); m.get_state_view()[:] = snap   # full snapshot/restore (regs+64K mem)
```
**Interrupts:** the i8080 binding has **no** interrupt-assert method (it's `#if Z80_MACHINE` only). Assert the
RST-7 serial interrupt **by hand** — this is exactly what the 8080 does on interrupt acknowledge:
```python
if m._I8080State__iff[0]:                 # INTE flip-flop (interrupt-enable); exposed as this slice
    sp=(m.sp-2)&0xFFFF
    m.memory[sp]=m.pc&0xFF; m.memory[(sp+1)&0xFFFF]=(m.pc>>8)&0xFF
    m.sp=sp; m.pc=0x0038; m._I8080State__iff[0]=0   # push PC, jump RST7 vector, clear INTE
```

---

## 5. L2 — the faithful boot (how it works)

`tools/boot8080.py` boots **without suppressing POST** and reaches program-load the way a real unit does
when a user skips diagnostics. Run it: `python tools/boot8080.py` → reaches mainloop, builds the WCS.

**Boot milestones (PC):** reset `0x0000` → handshake `0x0089` → POST → `DIAG_E 0x021D` (the stub ARU fails the
latch test → "DIAG ERROR TYPE E32" on the LARC) → **inject PGM-2** → normal_op `0x813B` → prog_load `0x13B6`
→ mainloop `0x8169`.

**LARC serial model (8251):** port `0xEE`=data, `0xEF`=status (bit0 TxRDY, bit1 RxRDY). Handshake: firmware
`OUT 0xEE,0xE0`, then **drains** stale RX, then waits for a fresh `0xC8` reply — so the reply must be delayed
to arrive *after* the drain (we delay it ~5000 ticks). After the handshake the serial is interrupt-driven
(RST-7 ISR @`0x03EE`, vector `0xFF` → `0x0038`).

**The PGM-2 "skip diagnostics" key (found empirically, faithful):** a LARC button event is **one serial byte**
`0x20 | (bit<<2) | column`, bit5 = press. We brute-forced all 32 codes; **`0x30`** (col0, bit4, press) is the
*only* one that bypasses to normal-op. Inject `0x30` (press) then `0x10` (release). (The button bitmap lives
at `0x3C06–0x3C09`; the TX-complete flag the firmware waits on is `0x3C14==0x80`.)

**Why not just force a program with a ROM patch?** Patching `0x8160` (the power-up program selector) changes
NVS1, which **breaks the ROM-checksum diagnostic that POST now actually runs**. So we don't patch; the firmware
loads its **default** power-up program = `mem[0xB800]` = `0x01` = **CONCERT HALL**.

**L2/L3 verification (the cross-check that made it ✅):** the WCS the faithful boot builds was diffed against the
old (z80emu, POST-suppressed) pipeline for CONCERT: the **0x3F4D offset table and 0x4000 lanes 0–2 are
byte-identical**; only the **lane-3 (coeff) bytes** differ, and those churn frame-to-frame from the always-on
LFO modulation even when the old harness is compared to itself (steps 42/94/…). ⇒ the verified 8080 builds the
same program; the parity bug did not corrupt the build.

---

## 6. L3 — the firmware-built data (what the ARU consumes)

After boot, read straight from `m.memory`:
- **`0x3F4D` offset buffer** — 128 × 16-bit signed offsets, written **downward**: step *s* at `0x3F4D − 2s`,
  **hi@a, lo@a-1**. `tools/boot8080.read_offsets(m)` does this. (Also exposed by `aru224_emulate.tap_map`.)
- **`0x4000:0x4200`** — the **128 × 4-byte WCS microword image** — the actual artifact the ARU/T&C executes
  (the hardware reads this memory-mapped window directly; a ROM-wide scan found no OUT-stream upload).

**Default program = CONCERT (id 0x01).** Loading the other 19 faithfully needs the **LARC program-select
serial messages** (decode them when you need all programs — same button/message protocol as §5; do NOT
ROM-patch). This is an open task but not blocking L4–L6.

---

## 7. THE FRONTIER — L4/L5/L6 (the ARU), and how to verify it

Everything below the boundary is inference. **The right ground-truth validator is the firmware's own POST**
— the ARU self-tests. This is the "come back and implement POST properly" step. Do it on the **verified
8080 / boot8080 foundation**, not the old emulator.

### 7.1 The plan: make a faithful ARU PASS POST (non-circular validation)
Build an ARU port model and wire it into `boot8080`'s I/O callbacks (ports `0x00–0x09`), then let POST run
**un-suppressed** and make the ARU sub-tests pass on their own merits. Each passing sub-test is a
firmware-authored proof of a slice of L4 (the bit-map) and L6 (the datapath):

- **ARU latch test `0x0A1D`** (called from `0x0911`): `OUT 0x07,0x55` then `IN 0x02` must echo `0x55`; then
  `0xAA`. (Proves the input-latch / port path.)
- **Register / walking-pattern test `0x0C48`** (the real "signature" test — there is **no** HP-LFSR
  signature; the §5.7 `29F3/3696` values are external-analyzer probe readings, **absent from ROM**). The SBC
  **single-steps** the ARU via ports: per step `OUT 0x06,lo` + `OUT 0x07,hi` load the 16-bit value, `OUT 0x03`
  is the **single-step clock**, then `IN 0x06`/`IN 0x07` read back the result. Golden tables at `0xCC3`/`0xCCF`
  (`C2 CE 55 | C6 DE 66 | …`). It preloads R[0..3] and checks the readbacks. **Passing it requires a real
  4-word register file + device decode** (Track B confirmed a faithful regfile passes it — it stores 4 distinct
  16-bit words and reads them back). This is the strongest L4/L6 check available.
- **Multiplier test `0x0942` (error E83):** the value-level `(x<<3)*cs>>5` model is **off by exactly 1 LSB**
  on negative coefficients vs the real **gate-level modified-Booth serial multiply** (golden e.g. `0x5555 ×
  −21/32 = 0xC7FF`, model gives `0xC800`). Bit-exactness needs the netlist multiplier. (Matters for the C++
  golden; may not matter for audio.)
- **The U42 "bus-test" (error E34):** an 8080 **multibus self-loopback** register (the SBC reading its own
  DATA/ bus) — **not** the ARU. Shim or model separately.

Prior art: `tools/_trackB_post.py` did much of this on the *old* emulator and got latch + register passing,
multiplier failing by 1 LSB. **Redo on `boot8080`** and treat each pass as a layer-verification.

### 7.2 What the ARU model is (current FAITH-level beliefs, to be confirmed by POST/schematic)
- **L4 field map** (per 4-byte step `0x4000+4s`): `b0,b1` = 16-bit **offset** (read **RAW**: `l0|l1<<8` — *not*
  inverted; the old `aru_datapath` `~`-inversion was a bug); `b2`: bit0=MI16, bit1=MI17, bits2-3=**WA**,
  bits4-5=**RA**, bit7=**CSIGN**; `b3` (complemented): bit0=**XFER**, bit1=**ZERO**, bits2-7=**coeff**.
  Device `(MI17,MI16)`: 11=DMEM read, 10=DMEM write, 01=sub-decoder (gated by MI4 = offset bit4), 00=NC.
  *(This whole bit-map is the single biggest unverified thing — POST is how you prove it.)*
- **L5 address** (`224XL_system_architecture.md` §6, owner-traced): `addr = CPC − offset`; the adder adds the
  **active-low** offset `~offset` with **carry-in tied high** (U49/U50/U63/U64); **carry-out = 17th address
  bit = the bank** (no separate bank-select — that resolves the long memory-bank confusion). Flat 128K. A delay
  line = (**small** write-offset W, **larger** read-offset R); realized **delay = R − W** samples; offset =
  "how many samples back". DMEM = 2 rows × 16× 4164 (top=CAS0, bottom=CAS1), bit-sliced (column *i* → DAB*i*),
  DIN tied to DOUT.
- **L6 datapath** (ARU pinouts `060-01318`): register file = 4× **74LS670** (U29–U32), **write-enable =
  DAB WSTB = MS7** (fires **every** step), read port continuous; multiplier **/32** (operand≪3, product≫5);
  20-bit accumulator saturating at **±2¹⁸**; result register = **74F374** (U43/U44). The **DAB bus**
  (DAB0–15) connects **only** to the register file + result register (on the ARU board) + the **XREG latch
  bridge** (U38–U41) to the DMEM data bus — i.e. a DMEM read reaches the multiplier **only via the register
  file** (no bypass). **DMEM read data is valid late** (≈end of MS7 through MS8/MS0 per Fig 3.3), which may
  impose a 1-step load-delay — unconfirmed.

### 7.3 The headline open problem (don't get nerd-sniped before L4 is verified)
No decode has **ever** produced a coherent reverb end-to-end. The datapath either runs away (over-unity) or
dies (the feedback never recirculates). Two concrete unresolved threads, both **L4/L6** issues:
(a) the recirc read tap writes its delayed sample to register **R3 (WA=3)**, and the next step (also WA=3)
**overwrites R3** before any nonzero-coeff step multiplies it → feedback lost; (b) the "write heads" decode to
**clustered** offsets that trample each other in the shared buffer. **Resolve these only after L4/L6 are
verified by POST** — chasing them on an unverified decode is exactly the trap of the last nine sessions.

---

## 8. Mistakes that wasted prior sessions (do not repeat)

- **Confusing plausible with verified.** Nine sessions of "CONFIRMED" claims that were wrong. Only the
  bottom-up method survives.
- **`tools/z80emu.py` had a real 8080 bug** — it set P/V to *overflow* on ADD/SUB (Z80 semantics); the 8080
  sets **parity**, and the firmware branches on parity. Retired; use `I8080Machine`.
- **"0x4000 is the wrong source" was itself wrong.** Its OFST lanes are just packed differently; read **RAW**
  they match `tap_map` 120/128. `aru_datapath`'s `~`-inversion was the bug.
- **`delay = −offset` is wrong** → physical **delay = +offset** (addr = CPC − offset).
- **The "memory bank select" rabbit hole** — there is no separate bank-select; the bank is just the adder's
  **carry-out**. Asked about ≥4 times; it's settled.
- **Patching `0x8160`** to force a program **breaks the POST ROM-checksum** — don't (use the LARC program-select
  protocol instead).
- **IR comparison as a debugging tool** — it has no diagnostic power. Last step only.
- **Trusting "owner-traced" claims I can't re-check** — the schematic is read by a human; treat schematic-only
  facts as 🔶 until POST or measurement confirms them. (And: the human owner reads the schematics; the assistant
  must NOT keep re-deriving schematic facts from memory — look them up in `224XL_system_architecture.md` §6.)

---

## 9. New-session start-here checklist

1. Read this doc + `224XL-interp-stack.md` (the live status board).
2. Confirm L1: `python -c "import z80; z80.I8080Machine()"`; if missing, rebuild (`pip install ./z80`, needs
   MSVC) and re-run the exercisers from `examples/supplements/`.
3. Confirm L2/L3: `python tools/boot8080.py` → should reach mainloop and print sane offsets
   (`[-12353, 128, 19679, …]` for CONCERT).
4. **Work the frontier (L4–L6):** build a faithful ARU port model on `boot8080`, un-suppress POST, and make
   the **latch test (0x0A1D)** then the **register/walking-pattern test (0x0C48)** pass on their own merits.
   Each pass verifies a slice of the L4 bit-map + L6 datapath. Update the status board.
5. Only after L4–L6 are ✅: source offsets (0x3F4D) + verified controls, run the datapath, and *finally*
   compare the IR to a real unit (L7) — and if a real-unit IR capture becomes available, that is the single
   most valuable artifact for the whole project.

---

## 10. Confidence ledger (snapshot 2026-06-26)
- ✅ L1 8080 core (exercisers) · ✅ L2 faithful boot (`boot8080.py`) · ✅ L3 program build for CONCERT.
- ❌ L4 microword bit-map · ❌ L5 offset→address · ❌ L6 ARU datapath — all FAITH; **verify via POST next**.
- ⬜ L7 audio IR — last, needs real-unit reference.
- Open: load all 20 programs (LARC program-select); the recirc/feedback failure (R3 clobber, write-head
  trample); the multiplier's last LSB (gate-level serial multiply); a real-hardware IR capture.
