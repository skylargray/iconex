# 224XL — Phase 1 kickoff: build the gate-faithful ARU from the M0b netlist and pass the firmware's POST

> **READ FIRST.** This continues the bottom-up reconstruction of the Lexicon 224XL reverb. The method, the verified lower layers (L1–L3), the tools, and the mistakes-not-to-repeat are in **`docs/plans/010 - 224XL-bottom-up-continuation.md`** — read it. This prompt is the *next* step after that plan's frontier, because the situation has changed materially since it was written.

## 0. What changed: M0b is complete — the ARU/T&C/DMEM are now net-traced ground truth

The bottom-up plan's frontier was **L4–L6 (the ARU/T&C/DMEM), all ❌ FAITH**, to be verified by "a schematic net-trace by the owner, or the firmware's POST." **The schematic net-trace now exists and is done:** the entire signal path is transcribed, pin-by-pin, in **`docs/reference/224/224XL_interconnect_netlist.md`** (ARU 060-01318 + DMEM 060-02512 + T&C 060-02475, both sheets), **triple-verified** (deterministic pin-check + adversarial audit vs the owner's source + Service-Manual cross-check). Every chip is keyed to a datasheet-verified `parts/*.v`.

This means **L4 (microword field decode) and L6 (ARU datapath wiring) are no longer guesses** — they are the netlist. It also **corrects several FAITH beliefs** in the bottom-up plan §7.2 — fold these in:

- **★ CSIGN is NOT a stored microword bit.** It is the **`tc_U20` (74S112) JK-FF output** (ARUCKE/-clocked, AS0-gated, driven from MI23). The plan's "`b2 bit7 = CSIGN`" is the *stored* sign; the *datapath* sign is the JK output. **OPEN: does the JK *follow* or *toggle* the stored sign each step?** Work it out from the J/K logic (`tc_U34` g3/g4) — it could flip the multiply sign vs the naive bit-read. (netlist §3.10)
- **★ DMEM is ONE 64K×16 bank, NO bank-select.** `dmem_U20–U35` (4164, CAS0/); `dmem_U1–U16` are **NOT populated**; the offset-adder top carry-out (`dmem_U64.pin9`) is **n/c** and `CAS1/` is hard-disabled. The plan's "**flat 128K / carry-out = 17th address bit = bank** / 2 rows top=CAS0 bottom=CAS1" is **wrong for this rev** — it's a single linear 64K buffer. (netlist §5.5, §G3D)
- **Hardware microword field map (netlist §G3R, schematic-traced):** `MI0–15`=offset · `MI16`=device-select · `MI17`=**MEMAC** · `MI18/19`=WA0//WA1/ · `MI20/21`=RA0//RA1/ · `MI22`=PROT · `MI23`→CSIGN-JK · `MI24`=**XFER** · `MI25`=**ZERO-gate** · `MI26–31`=**coeff C0/–C5/**.
- **The multiplier is fully traced now** (it was "the only ARU gap"): regfile `aru_U29–32` (74670) → dual-rank shifter (74194) → **modified-Booth NAND array** (74LS00, §4F.5) gated by `M0//M1/` (serialized by `tc_U11`→M0/ even, `tc_U10`→M1/ odd, 74195) → PP adders → product reg. So the **gate-level modified-Booth multiply can be built** — this is what the value-level model got wrong by 1 LSB.
- **Decode timing:** the offset latch + microword field registers + RESET FF all clock on **`DAB RSTB/`** (the per-step strobe that also steps the PC). `addr = CPC − OFST` (2's-comp, carry-in tied high). `RES = sat16(ACC≫3)`, ±2¹⁸ saturation. `XFER CK = tc_U36`; `ZERO/ = tc_U48`; clock tree `ARUCK/ARUCKE/ARUCKE/` (three distinct nets, `tc_U40`); MS gen `tc_U56`(÷9)+`tc_U39`; AS gen `tc_U23`. Full timing in **`docs/reference/224/224XL_timing_spec.md`** (figs 3.2–3.6).
- **One open reconciliation:** the *firmware-storage* field map (the lane/bit tables in `224XL_microword_fieldmap.md` and `224XL_technical_reference.md` §3) **disagrees** with the hardware MI map on bit positions (e.g. the tech-ref puts XFER/ZERO in lane-2; hardware has them in lane-3 = MI24/25). The difference is absorbed by the stored byte order + active-low inversions. **Building the model from the netlist and passing POST will pin the true byte→MI mapping** — that is part of this task, not a blocker.

## 1. The next step (this session): build the gate-faithful ARU from the netlist → pass POST un-suppressed

This is simultaneously (a) the bottom-up plan's L4–L6 verification gate and (b) the foundation of the Phase-1 bit-exact model. Build the ARU/T&C/DMEM model **from the netlist** (no more guessing the field map or datapath), wire it into `tools/boot8080.py`'s I/O callbacks (ports `0x00–0x09`), let **POST run un-suppressed**, and make the ARU self-tests pass **on their own merits** — each pass is firmware-authored proof of a slice of L4+L6.

Suggested order (smallest → strongest, per bottom-up plan §7.1):
1. **Latch test `0x0A1D`** — `OUT 0x07,0x55` → `IN 0x02` echoes `0x55`, then `0xAA`. (Proves the port/latch path.)
2. **Register / walking-pattern test `0x0C48`** — the SBC single-steps the ARU (`OUT 0x06,lo`/`OUT 0x07,hi` load, `OUT 0x03` = single-step clock, `IN 0x06`/`IN 0x07` read back); golden tables at `0xCC3`/`0xCCF`. Requires a real 4-word register file + device decode — **build it from netlist §4F.1 + §2T/§2D**. (Track B got this passing on the old emulator; redo on the netlist-built model.)
3. **Multiplier test `0x0942`** (error E83) — the value-level `(x≪3)·cs≫5` model is off by exactly 1 LSB on negative coefficients. **Build the gate-level modified-Booth multiply from netlist §4F** and it should now pass **bit-exact** (golden e.g. `0x5555 × −21/32 = 0xC7FF`). This is the first thing M0b makes newly achievable.
4. **U42 "bus-test" (E34)** — an 8080 multibus self-loopback, **not** the ARU (netlist DMEM §5.6, the bus-test reg). Shim/model separately.

Each passing sub-test → update the status board (`docs/plans/012 - 224XL-interp-stack.md`) flipping that L4/L6 slice from ❌ FAITH to ✅ VERIFIED (now backed by **both** the schematic net-trace *and* POST).

## 2. Then — only after POST passes — revisit the headline reverb problem with a verified datapath

The bottom-up plan §7.3 says: do NOT chase the recirc/feedback failure (R3-clobber, write-head trample, over-unity vs dead-tank) on an unverified decode — that was the nine-session trap. Once the netlist-built ARU passes POST, you finally have a verified L4/L6, and the M0b corrections directly bear on those threads (the single-64K-bank addressing; CSIGN-as-JK possibly flipping a sign; the exact field map). Run the datapath over CONCERT (offsets from `0x3F4D` via `boot8080.read_offsets`; WCS from `0x4000`) and resolve loop closure **then**. L7 (IR comparison) is still last.

## 3. Ground rules (unchanged — they are why we survived)
- **A layer is ✅ only when verified by something independent of our interpretation.** The M0b netlist is the owner's schematic net-trace (a valid verifier for *wiring*); POST is the independent *functional* oracle. Use both. "Looks like a reverb" is not verification.
- **The netlist is ground truth for wiring** — don't re-derive ARU/T&C/DMEM pinouts or the field map from memory or from the older firmware-belief docs; read `224XL_interconnect_netlist.md` (and `parts/*.v` for pinouts).
- **Verify bottom-up; L7/IR is last.** Don't get nerd-sniped by the reverb before POST passes.
- Build on **`tools/boot8080.py`** + the **`kosarev/z80` `I8080Machine`** (L1, passes 8080exm). The retired `z80emu.py` has an 8080 parity bug — do not use it.

## 4. Key inputs
- **Netlist (the spec to build from):** `docs/reference/224/224XL_interconnect_netlist.md` — §4/§4F (ARU MAC + multiplier), §5 (DMEM addr/DRAM/XREG), §2T/§2D (device decode), §3 (WCS + field map), §6T/§6D (clock/strobe/state gen), **§G3R (the hardware MI field map)**, §G-* (the few remaining ⚪: the owner-omitted PLL — MC is the model's clock input; the SBC host interface).
- **Timing:** `docs/reference/224/224XL_timing_spec.md` (figs 3.2–3.6: MS/AS skeleton, the MAC pipeline, DMEM strobes).
- **Parts:** `docs/reference/224/parts/*.v` (datasheet-verified pinouts).
- **Boot/POST:** `tools/boot8080.py` (faithful boot, reaches mainloop), `tools/_trackB_post.py` (prior POST work — port to the netlist model), `tools/aru_datapath.py` (the L6 model to rebuild from the netlist).
- **Service Manual:** `docs/reference/224/Lexicon-224X-Service-Manual.md` (§3.5 T&C, §3.6 DMEM, §3.7 ARU, §5.x DIAG/POST).
- **Memory:** `224xl-holistic-m0-progress.md` (M0b complete — read this), `224xl-bottomup-2026-06-26.md`, `224xl-schematic-autoread-unreliable.md` (use owner hand-trace, never auto-tile-reading).

## 5. Start-here checklist
1. Read `docs/plans/010 - 224XL-bottom-up-continuation.md` + `012 - 224XL-interp-stack.md`, then skim the netlist §G3R + §4F + §2T.
2. Confirm L1–L3: `python tools/boot8080.py` → reaches mainloop, prints CONCERT offsets (`[-12353, 128, 19679, …]`).
3. **Build the ARU register file + device decode from the netlist, wire into boot8080's I/O callbacks, un-suppress POST, and pass `0x0A1D` then `0x0C48`.** Then the gate-level multiplier for `0x0942`. Update the status board per pass.
4. Note any place the netlist-built decode disagrees with the firmware-storage field map (`microword_fieldmap.md`) — POST is the arbiter; record the resolved byte→MI mapping.

**Net:** M0b removed the "we can only infer the ARU" blocker. The job now is to *instantiate* the verified wiring as a model and let the firmware's own self-test confirm it — turning L4/L5/L6 green with hard evidence, not plausibility.
