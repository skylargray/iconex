# 224XL reconstruction — bottom-up continuation plan & session handoff

> **READ THIS FIRST if you are a new session.** This is the start-here doc. It captures the method,
> the verified state, every tool/address/fact you need, the next steps, and the mistakes that wasted
> entire prior sessions so you don't repeat them. The **living status board** is
> [`224XL-interp-stack.md`](224XL-interp-stack.md) — keep it updated as you verify each layer.

---

## 0. One-paragraph orientation

We are reconstructing the **Lexicon 224XL** digital reverb (1980s, an 8080-managed microcoded DSP) as a
bit-exact software model, from ROM dumps + schematics + the service manual. Nine early sessions kept
declaring things "CONFIRMED" that were wrong, because they validated by *plausibility* ("looks like a
reverb") instead of *ground truth*. We switched to a **strict bottom-up, layer-by-layer verification**
method. **L1–L3 are VERIFIED** (the 8080 CPU, the firmware boot, the program the firmware builds). The
ARU/T&C/DSP layers **L4–L6**, once pure inference, are now **net-traced (the M0b interconnect netlist) and
POST-verified**: a netlist-faithful ARU+DMEM model **passes the firmware's entire power-up self-test
un-suppressed** (latch E32, register E40, multiplier E83, DMEM E91) — on both the behavioral model
(`tools/aru_post.py`) and the phase-accurate RTL model (`tools/aru_rtl.py`/`aru_rtl_dp.py`, plan 013 M1/M2).
The frontier is now **the free-run reverb (plan 013 M3)** — the autonomous WCS loop POST never exercises.
Do **not** jump to the audio output (L7); it's a pass/fail oracle with zero diagnostic power and is the
*last* thing we do. **For the current method + structural model, see `docs/plans/013` (the holistic plan,
which supersedes the sectional method here); this doc remains the L1–L3 reproduction + lessons reference.**

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
| **L4** microword field decode | 4 bytes → offset/WA/RA/CSIGN/XFER/ZERO/coeff/device | 🔶 LARGELY VERIFIED | M0b netlist (§G3R) + POST passing un-suppressed (latch/register/multiplier). Fields POST can't distinguish are net-traced only |
| **L5** address arithmetic | offset → DRAM cell (addr = CPC − offset) | 🔶 LARGELY VERIFIED | DMEM test E91 passes on `addr=CPC−OFST` (CPC walks, one constant offset 0x2000). Open: offset *variation* + dual-use bits 12/13 |
| **L6** ARU datapath | regfile × /32 mult + accumulate + DMEM r/w + timing | 🔶 LARGELY VERIFIED | primitives (regfile/mult/accumulator/result-reg/DMEM r/w) POST-verified; free-run execution (the reverb) = plan 013 M3, open |
| **L7** audio result | run L6 over samples → reverb IR | ⬜ LAST | real-unit IR, only after the free-run model (M3) is coherent |

Full annotated stack with per-layer detail: [`224XL-interp-stack.md`](224XL-interp-stack.md).

---

## 3. Environment & key files

- **Repo root:** `d:/OneDrive/Gray Instruments/iconex` · Windows · Python 3.14 · use the Bash tool.
- **ROM dumps:** `ROMs/Lexicon 224/224XL v8_21/` — `SBC{1,2,3} 2716.BIN`, `NVS{1..8} 2732.BIN`.

### Tools (current)
| File | Purpose | Notes |
|---|---|---|
| `tools/boot8080.py` | **★ THE faithful boot** on the verified 8080 | USE THIS. Reaches program-load via real PGM-2 bypass. |
| `tools/aru_post.py` | **★ behavioral ARU+DMEM model + POST harness** | passes the WHOLE POST un-suppressed (E32/E40/E83/E91); `run_post(aru_factory=…)` injectable |
| `tools/aru_rtl.py` | **★ phase-accurate RTL micro-framework + clock engine (M1)** | `Net`/`Reg`/`Counter`/`Latch` + `ClockEngine`; `selftest()` validates fig-3.2/3.4 vs `timing_spec.json` |
| `tools/aru_rtl_dp.py` | **★ phase-accurate RTL datapath (M2)** `ARU_RTL` | structural regfile/mult/accum/result/CPC/DMEM; passes the whole POST via `aru_post.run_post(aru_factory=ARU_RTL)` |
| `tools/aru_booth.py` | gate-level modified-Booth multiplier | bit-exact 20/20 POST goldens (NAND array + 74F283 chain + fig-3.4 schedule); cmag=63 = +3/dual-rail |
| `tools/aru_cycaccurate.py` | cmag=63 cycle-accurate proof (plan 016) | refutes the pipeline hypothesis; pins the unique +3/dual-rail correction |
| `tools/dis224.py` | disassemble SBC(0x0000-0x17FF) or NVS(0x8000+) | `python tools/dis224.py <start_hex> <end_hex>` ; `... scan 02 06 07` for I/O sites |
| `tools/disrange.py` | disassemble NVS at true addresses | `python tools/disrange.py <start> <end>` |
| `tools/aru224_emulate.py` | offset/coeff decoder (`tap_map`, `capture_coeffs`) | ⚠ still runs the OLD `z80emu`; offsets verified to match. Pre-netlist; use the netlist + aru_post/aru_rtl for the datapath |
| `tools/aru_datapath.py`, `tools/_trackB_post.py` | **SUPERSEDED** pre-netlist datapath / old-emulator POST | replaced by `aru_post.py` (+ `aru_rtl*.py`); kept for history only |
| `tools/boot_xl.py`, `tools/z80emu.py` | **RETIRED** old boot + emulator | `z80emu.py` has the 8080 parity bug — do not use for new work |

### Docs (read these)
- `docs/plans/013 - 224XL-holistic-model-plan.md` — **★ the current method** (phase-accurate structural model; supersedes the sectional method here).
- `docs/plans/012 - 224XL-interp-stack.md` — **live status board** (update as you go).
- `docs/reference/224/224XL_interconnect_netlist.md` — **★ the M0b netlist: ground truth for all ARU/T&C/DMEM wiring** (§G3R field map, §4F multiplier, §5 DMEM, §2T/§2D decode, §6T clock/strobe).
- `docs/reference/224/224XL_timing_spec.md` — figs 3.2–3.6 (MS/AS skeleton, MAC pipeline, DMEM strobes); single source `tools/timing/timing_spec.json`.
- `docs/reference/224/224XL_system_architecture.md` — §5–6 = the address arithmetic (offset→addr; **ONE 64K bank, no bank-select** — see netlist §5.5).
- `docs/reference/224/224XL_microword_fieldmap.md` — early firmware-storage bit-map; superseded by netlist §G3R + POST.
- `docs/reference/224/Lexicon-224X-Service-Manual.md` (+ `-chapter-5.md`) — §3.5 T&C, §3.6 DMEM, §3.7 ARU, §5.x DIAG/POST.
- `docs/reference/224/"224XL ARU pinouts from 060-01318.txt"` (+ T&C 060-02475-D, DMEM 060-02512 txts) — owner's chip pinouts.
- Memory: `MEMORY.md` index → `224xl-holistic-m0-progress.md` (the full current record).

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

## 7. L4/L5/L6 (the ARU) — VERIFIED via POST; the frontier is now free-run (M3)

The "come back and implement POST properly" step is **DONE.** A netlist-faithful ARU+DMEM model wired into
`boot8080`'s I/O callbacks passes the firmware's entire POST **un-suppressed** (no plausibility, no hardcoded
goldens). This holds on both the behavioral model (`tools/aru_post.py`) and the phase-accurate RTL model
(`tools/aru_rtl.py` + `tools/aru_rtl_dp.py`). Each passing sub-test is firmware-authored proof of a slice of
L4 (the field map) and L6 (the datapath).

### 7.1 Done: the ARU PASSES POST (non-circular validation)
The four ARU/DMEM sub-tests, all **PASS un-suppressed**:

- **ARU latch test `0x0A1D`** (called from `0x0911`): `OUT 0x07,0x55` then `IN 0x02` echoes `0x55`, then
  `0xAA`. (Port/input-latch path.) → **E32 PASS.**
- **Register / walking-pattern test `0x0C48`** (the real "signature" test — there is **no** HP-LFSR
  signature; the §5.7 `29F3/3696` values are external-analyzer probe readings, **absent from ROM**). The SBC
  **single-steps** the ARU via ports: per step `OUT 0x06,lo` + `OUT 0x07,hi` load the value, `OUT 0x03` is the
  single-step clock, then `IN 0x06`/`IN 0x07` read back. Needs a real 4-word register file + device decode
  (netlist §4F.1 + §2T). → **E40 PASS.**
- **Multiplier test `0x0942` (error E83):** the value-level `(x<<3)*cs>>5` model was off by ≤2 LSB; the real
  **gate-level modified-Booth serial multiply** (`tools/aru_booth.py`, built from netlist §4F: NAND array +
  74F283 carry chain + fig-3.4 schedule) is bit-exact. Getting there fixed 3 owner-confirmed SR-tap errors +
  the §4.7/§4.6 reversal cancellation; the all-ones (cmag=63) case = a unique combinational +3/dual-rail-phase
  correction (plan 016). → **E83 PASS (20/20 goldens).**
- **DMEM test `0x0B75` (error E91):** `addr = CPC − OFST` with the CPC advancing per single-step strobe (the
  offset held constant; the full-64K sweep wraps so write/read passes realign) and every DMEM cycle a
  **read-before-write** (the firmware's two complementary passes verify storage one strobe per cell). → **E91 PASS.**
- **The U42 "bus-test" (error E34/inside the bus window):** an 8080 **multibus self-loopback** register (the
  SBC reading its own DATA/ bus) — **not** the ARU; shimmed at IN 0x03@0x0AC5 / IN 0x04@0x0AE9.

Prior art `tools/_trackB_post.py` (old emulator) got latch+register passing, multiplier off — now superseded
by the boot8080-based models above.

### 7.2 What the ARU model is (now netlist-traced §G3R + POST-verified; corrections folded in)
- **L4 field map** (netlist §G3R, schematic-traced + POST-confirmed): `MI0–15`=offset (l0,l1); `MI16`=device-
  select; `MI17`=**MEMAC**; `MI18/19`=WA; `MI20/21`=RA; `MI22`=PROT; `MI23`→CSIGN; `MI24`=**XFER**; `MI25`=
  **ZERO-gate**; `MI26–31`=**coeff C0–5**. Stored byte→MI: **l2 = MI16–23 direct, l3 = MI24–31 read via `~l3`**
  (the coeff/XFER/ZERO byte is active-low). Device `(MEMAC,MI16)`: (1,1)=DMEM read, (1,0)=DMEM write,
  (0,1)=sub-decoder, (0,0)=NC. **CORRECTION vs the old belief:** `CSIGN` is **not a stored datapath bit** — it
  is the `tc_U20` (74S112) **JK-FF output** that *follows* MI23 (AS0-gated, no toggle); l2 bit7 (=MI23) selects
  the sign.
- **L5 address** (netlist §5, POST-verified by E91): `addr = CPC − OFST`. The microword **OFST field is stored
  COMPLEMENTED** (OFST/), and the adder (dmem_U49/U50/U63/U64) adds it with **carry-in tied high** →
  `addr = (CPC + OFST_stored + 1) mod 2¹⁶`. **CORRECTION vs the old belief: this is ONE 64K×16 bank, NOT flat
  128K.** `dmem_U1–U16` are **NOT populated**, `CAS1/` is hard-disabled, and the adder top carry-out
  (`dmem_U64.pin9`) is **n/c** — there is no bank-select. The CPC advances +1 per sample in free-run (per
  single-step strobe in POST). A delay = offset samples back; modulation = time-varying offset.
- **L6 datapath** (netlist §4/§4F, POST-verified): register file = 4× **74LS670** (aru_U29–32), write-enable =
  **DAB WSTB = ¬MS7** (every step), read port continuous; modified-Booth multiply **/32** (gate-level, 20/20
  goldens); 20-bit accumulator saturating at **±2¹⁸**; result register = **74F374** (aru_U43/U44). The **DAB**
  (DAB0–15) connects on the ARU board **only** to the register file + result register, bridged to the DMEM data
  path by the **XREG latch** (dmem_U38–U41) — a DMEM read reaches the multiplier **only via the register file**.
  **Read-back path (POST-confirmed):** with XFER=0 in the POST microwords, IN 0x06/0x07 reads the X-register-
  captured DAB (the result-reg/sat-mux output for compute, or DRAM old-contents for a DMEM read-before-write) —
  it bypasses the XFER-gated result-register load. DMEM DOUT is valid late (≈MS7) per Fig 3.3.

### 7.3 The headline open problem — now the M3 free-run frontier (L4/L6 ARE verified)
No decode has yet produced a coherent reverb end-to-end: in free-run the datapath either runs away
(over-unity) or dies (the feedback never recirculates). The two old threads — (a) the recirc tap writing to
R3 then being overwritten, (b) "write heads" decoding to clustered offsets that trample — were chased on an
*unverified* decode and on a *sectional* (value-level) model; the holistic plan (`013 §0`) argues those were
**artifacts of sectional composition, not properties of the circuit.** Now that L4/L6 are POST-verified and a
phase-accurate RTL model exists, the disciplined path is **plan 013 M3**: extend the RTL model with the real
WCS program counter (0–99 sweep, RESET@99), per-step DAB-source routing, the deferred MAC across instructions,
and idle=hold — and let the loop close *because the wiring closes it*. A failure there is a specific mis-wired
net or mis-timed edge, localizable against fig-3.3/3.4 — not a guess.

---

## 8. Mistakes that wasted prior sessions (do not repeat)

- **Confusing plausible with verified.** Nine sessions of "CONFIRMED" claims that were wrong. Only the
  bottom-up method survives.
- **`tools/z80emu.py` had a real 8080 bug** — it set P/V to *overflow* on ADD/SUB (Z80 semantics); the 8080
  sets **parity**, and the firmware branches on parity. Retired; use `I8080Machine`.
- **"0x4000 is the wrong source" was itself wrong.** Its OFST lanes are just packed differently; read **RAW**
  they match `tap_map` 120/128. `aru_datapath`'s `~`-inversion was the bug.
- **`delay = −offset` is wrong** → physical **delay = +offset** (addr = CPC − offset).
- **The "memory bank select" rabbit hole** — SETTLED by the M0b netlist: there is **no bank at all.** DMEM is
  ONE 64K×16 bank (`dmem_U20–U35`); `dmem_U1–U16` are unpopulated, `CAS1/` hard-disabled, and the adder's top
  carry-out (`dmem_U64.pin9`) is **n/c**. (The earlier "bank = the carry-out / flat 128K" guess was wrong for
  this rev.)
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
4. **L4–L6 are POST-verified (done).** The ARU+DMEM model passes the whole POST un-suppressed on `boot8080`
   (`python tools/aru_post.py`, and `python tools/aru_rtl_dp.py` for the RTL model). If extending, keep each
   POST gate green as the regression.
5. **Work the current frontier = free-run (plan 013 M3):** extend the phase-accurate RTL model (`tools/aru_rtl.py`
   + `aru_rtl_dp.py`) with the real WCS PC + per-step DAB routing + deferred MAC, source offsets (0x3F4D) +
   verified controls, and demonstrate a coherent decaying reverb (loop closes from the wiring). *Then* (L7)
   compare the IR to a real unit — if a real-unit IR (or single-step port access to a real ARU) becomes
   available, that is the single most valuable artifact for the project.

---

## 10. Confidence ledger (snapshot 2026-06-29)
- ✅ L1 8080 core (exercisers) · ✅ L2 faithful boot (`boot8080.py`) · ✅ L3 program build for CONCERT.
- 🔶 L4 microword field map (netlist §G3R + POST) · 🔶 L5 offset→address (E91 passes; one offset, variation
  open) · 🔶 L6 ARU datapath (primitives POST-verified; free-run = M3). The whole POST passes un-suppressed.
- ⬜ L7 audio IR — last, needs real-unit reference.
- Solved since the snapshot: the multiplier's last LSB (gate-level Booth, 20/20; cmag=63 = +3/dual-rail, plan
  016); DMEM addressing (E91). Open: **free-run reverb (plan 013 M3)** — the recirc/feedback closure (the old
  R3-clobber/trample threads, to be resolved structurally in the RTL model); load all 20 programs (LARC
  program-select); the C++ bit-exact core re-sync; a real-hardware IR capture.
