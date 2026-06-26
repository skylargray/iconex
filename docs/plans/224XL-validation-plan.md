# 224XL Adversarial Validation Plan — proving the decode before trusting it

> **Why this plan exists.** Two reverse-engineering pipelines were built in parallel and never
> reconciled. `aru_datapath.py` decoded the microword from `mem[0x4000:0x4200]` and was iterated for
> ~9 sessions (Sessions 3–11) chasing a "dead tank." `aru224_emulate.py` (built earlier, 2026-06-21)
> decoded the *real* firmware-computed offset table from the `0x3F4D` buffer. In Session 11 a one-line
> cross-check exposed the truth: **`0x4000` is the wrong source** — for a non-FE program (CHAMBER) it is
> *all zeros*, while the `0x3F4D` buffer matches the firmware's own load byte-for-byte. Every dead-tank
> symptom (delays 32× too long, write-head trample, over-unity) was an artifact of the wrong source.
>
> The deeper lesson: **both pipelines were declared "validated/complete" on the basis of plausible-looking
> output ("a sane reverb tap map"), never an end-to-end test against ground truth or even against each
> other.** This plan exists so we never again confuse *plausible* with *verified*. **No claim graduates to
> CONFIRMED without a non-circular check.**

---

## 0. Confidence taxonomy (used in this plan and all reference docs)

| Tag | Meaning | Bar to earn it |
|---|---|---|
| ✅ **CONFIRMED** | True beyond reasonable doubt | Owner schematic trace (net-by-net) **and/or** direct measurement/proof; cross-checked by ≥2 independent angles |
| 🟡 **PARTIAL** | Strong evidence, specific gap | Solid but with a named caveat (e.g. read is faithful but interpretation unverified) |
| 🔵 **INFERRED** | Logically derived, not directly checked | Follows from CONFIRMED facts but the derivation itself is untested |
| 🟠 **GUESS** | Plausible, weak/no support | A working hypothesis; could be wrong |
| ⚪ **UNKNOWN** | Open | Not determined |

**Rule:** "the firmware computes value X" and "X looks like a reverb" are **at most 🟡** — never ✅ — until X is shown to be what the ARU *hardware* uses **and** to produce correct behavior.

---

## 1. Current confidence state (the thing this plan must raise)

### ✅ CONFIRMED (owner schematic trace and/or direct proof)
- **DSP architecture:** microcoded engine T&C (sequencer/WCS/decode) + DMEM (delay store/addressing) + ARU
  (4×16 regfile, serial 16×6 multiplier, 20-bit sat accumulator, 16-bit result reg). 100 microsteps/sample,
  293 ns cycle, MS0–MS8 → AS0/AS1/AS2, 34.13 kHz. (Manual §3.6–3.7.)
- **DAB:** shared 16-bit bus, exactly one driver per cycle; register file written every cycle from the DAB;
  undriven DAB **floats and holds** its last value (no pull resistors on DAB0–15; DAB RSTB is a *clock*,
  not a bus reset — manual line ~939). (Schematic 060-02512 + hardfacts workflow.)
- **Device decode (U47 LS139 + U48 S00 + U49C, owner net-traced 060-02475):**
  `(MI17,MI16)=(1,1)`→**MEMR/** (DMEM read); `(1,0)`→**MEMW/** (DMEM write, data = bus, RES via RDRREG);
  `(0,1)`→**Y1** enables the sub-decoder; `(0,0)`→**Y0 = NOT CONNECTED**. Sub-decoder (decoder-2,
  select `(MI13,MI12)`) **gated by MI4** via U34A: 1=RDRREG, 2=RD XREG, 3=RD AD, 0=idle. **RDRREG/** =
  U48A∧U48C gated by **DAB RSTB** (= f(MS1,MS8) via U20 S112). **WR DA/** (D/A output) = **U49C** (74LS10):
  `(MI17,MI16)=(0,1)` **AND MI7=1**.
- **Address path:** adder U49/U50/U63/U64 (4×LS283), **OFST straight order** (OFST0–3→U49 … OFST12–15→U64),
  `addr = CPC − offset` (active-low offset + carry-in high). DRAM mux U36/U18 (LS157) = standard
  row(A0–7)/col(A8–15), **no bit permutation**; physical cell = linear address.
- **Register file:** 4×LS670 (U29–U32), WA=MI18/19, RA=MI20/21, DAB WSTB every cycle, **address 3 =
  pass-through** (junk write target for "don't care" steps — manual line 392).
- **ARU arithmetic:** `/32` coefficient scale (result reg U43/U44 LS374 take PP3..PP18 = product≫3; operand
  ≪3); **±2¹⁸ saturation** (74F157 muxes U33–U37, overflow = U42 XOR of top two sum bits). (060-01318.)
- **Program storage & names:** 21-record array @0xB800 in NVS ROM; **program names 20/20 cross-checked**
  against the NVS3 directory @0xA446 — names are firmware-authoritative.
- **Program-load mechanism:** firmware routine `0x13B6` → **B55B step-builder** (computes/copies the 128
  delay offsets into the **0x3F4D buffer**, written downward) + **bytecode interpreter 0xAA9F** (expands
  coefficients). Two paths: **FE** (`recbase+0x30==0xFE`, offsets computed `ptr−writeptr`) vs **non-FE**
  (copies a pre-baked 128-entry table from `recbase+0xA7..0x2A7`).
- **`0x4000` is the wrong offset source (Session 11 proof):** CHAMBER (non-FE) → `0x4000` decodes to **all
  zeros**; the `0x3F4D` buffer matches the firmware's own load exactly. `aru_datapath.py`'s entire
  `mem[0x4000:0x4200]` premise is retired.

### 🟡 PARTIAL (faithful but interpretation/location unverified)
- **The microword field-bit MAP** (OFST=lane0,1; COEFF mag+CSIGN=lane3; WA/RA/XFER/ZERO/MEMAC=lane2): the
  *bit meanings* are consistent with the owner's device-decode trace, **but** the map was historically
  applied to the wrong image (`0x4000`). The map-as-hardware-description is likely right; **which memory
  image to apply it to, and whether lane0,1 there are the real delays, is not re-confirmed.**
- **`aru224_emulate` delay extraction:** *byte-identical to a real-boot `0x3F4D` snapshot* (non-FE) ⇒ it
  **reads the firmware's output faithfully**. Caveat (near-circular): this proves the read, **not** that the
  `0x3F4D` values are the ARU's actual addressing data, **nor** that `delay = −offset` is the right
  interpretation, **nor** that they yield a correct reverb.
- **DMEM = 128K (2 banks 64K×1 4164):** parts list + board photo confirm the *chips*; schematic 060-02512 is
  a hybrid (16K/4116 footprint as drawn). Bank select traced to **A14** as drawn; **A16=carry inferred** for
  the jumpered 4164 board.
- **Chorus modulation:** decoded from firmware (engine 0xAD5C–0xAE9B) + validated by poking; per-program
  modulated-tap table from a batch sweep. Mechanism (per-frame rewrite of selected delay offsets + allpass
  interpolation coeff, triangle LFO) is solid; exact depth/rate scaling partly inferred.

### 🔵 INFERRED
- The `0x3F4D` buffer values are the delays the **ARU hardware** uses (firmware computes them ⇒ assumed used).
- MAC ordering `add → XFER → ZERO` (manual §3.7 derivation, not bench-verified).
- bank = A16 carry on the 64K board (not drawn).

### 🟠 GUESS
- `inv_l3` (coefficient byte polarity) = True (weak lean only).
- The FE writeptr-base scaling that makes the recirc loop 176 ms vs 577 ms.
- The exact loop-closure routing of a *working* datapath.

### ⚪ UNKNOWN
- **Whether any decode, fed through a faithful datapath, produces a correct 224XL reverb. This has NEVER
  been demonstrated end-to-end for either pipeline.** ← the headline gap.
- The per-step alignment between the `0x3F4D` offset table and the control fields.
- Whether the field-bit MAP applies to the real (firmware-built) WCS image.

---

## 2. The validation workflow (all parts)

Six tracks. Tracks A–C are the **non-circular validators**; D–E build on them; F is adversarial gating.
Run A, B, D, E as parallel investigations where possible; each finding is independently re-checked (F).

### Track A — Pull the firmware's offset-computation routine apart **by hand**
**Goal:** confirm the *interpretation* (units, sign, what the offset means), not just that we read the buffer.
This is the single most important track — it is the only thing that turns 🟡 "faithful read" into ✅.

1. **Disassemble `0x13B6` → B55B (`0xB55B`)** completely. Document the control flow and the
   `recbase+0x30==0xFE` branch.
2. **FE path (computed offsets):** trace the `ptr − writeptr` arithmetic step by step. Determine exactly:
   - what `ptr` and `writeptr` (`0x3cf1`) point at, in samples vs bytes;
   - whether the stored 16-bit value is the **delay** or its **two's-complement/active-low** form, and the
     sign convention (`delay = −offset` must be *derived from the code*, not assumed);
   - whether/how the **SIZE / decay parameters scale** the offsets (this is the 176 ms-vs-577 ms-loop
     question — resolve which base is physical by reading the scaling math).
3. **Non-FE path (`0xB65A`):** confirm the pre-baked table at `recbase+0xA7..0x2A7` is copied verbatim and
   that its entries are in the *same units/sign* as the FE output.
4. **Interpreter `0xAA9F` + coeff capture (`0xB510` hook):** trace how the 6-bit coefficients and CSIGN are
   emitted, and **how offset and coefficient are paired per step** (this is the missing offset↔control
   alignment). Establish the canonical step ordering.
5. **Cross-check the WCS hand-off:** find where the assembled microcode is shipped to the **hardware WCS**
   (OUT stream / memory-mapped window), and confirm which buffer (the `0x3F4D` offsets, the control lanes)
   actually reaches the T&C WCS RAM. This closes the "is `0x3F4D` what the ARU uses" inference (🔵→✅ or
   refutes it).

**Exit criteria:** a written derivation of `delay = f(stored bytes, params)` from the ROM code, and a
per-step `(offset, WA, RA, coeff, CSIGN, device)` table whose construction is traced to firmware — not
pattern-matched.

### Track B — Make a faithful ARU model **pass the firmware's own self-test** (instead of suppressing it)
**Goal:** let the machine validate our datapath. Currently `boot_xl` patches the DIAG handlers (`0x0217/
0x021D → RET`) and stubs the ARU latch — i.e. POST is **bypassed**, so the firmware never actually checks
the ARU. This track removes that crutch.

1. Re-enable the POST handlers. Identify the two ARU checks: the **latch test** (`write 0x55→port 0x07`,
   `read port 0x02` expect `0x55`) and the **signature test loop `0x0A1D–0x0B64`**.
2. Replace the ARU port stub with a **faithful ARU datapath** (regfile + /32 multiplier + ±2¹⁸ accumulator +
   result register + the confirmed device decode) wired to ports 0x02/0x06/0x07.
3. Iterate the datapath until **POST passes on its own merits**. A passing signature test is a non-circular,
   firmware-authored proof that the ARU arithmetic + I/O model is correct.

**Exit criteria:** the real firmware boots to normal operation with **no suppressed POST errors**. (If full
signature-pass proves intractable, document exactly which sub-test fails and what it implies — that itself
is high-value evidence.)

### Track C — Reconcile and retire the two pipelines (formal)
1. For **all 20 programs**, diff `aru_datapath` (`0x4000`) offsets vs `aru224_emulate` (`0x3F4D`). Expect:
   `0x4000` empty/garbage for non-FE, divergent for FE. Document per-program.
2. Decide what `0x4000` actually is (FE-path scratch? a stale intermediate? an unrelated buffer) by tracing
   what writes it during a full boot.
3. **Decommission `mem[0x4000:0x4200]` as a source.** Make `aru224_emulate` (firmware-driven) the single
   canonical decoder; route `aru_datapath`'s control-field map onto the firmware-built image, not `0x4000`.

### Track D — Internal-consistency stress test across all 20 programs
Cheap, powerful sanity that "plausible" alone never provided:
- **Monotonic scaling:** decay/RT-related coefficients and tank-loop lengths should order sensibly
  (SMALL ROOM < ROOM < CHAMBER < CONCERT; plates vs halls distinct).
- **FE vs non-FE agreement** on shared structural features (predelay tap, recirc loop, output multi-tap).
- **Physical sanity bounds:** every delay < wrap period; no impossible offsets; coefficient magnitudes ≤ rail.
- **Parameter sweep:** vary a program's decay/size param at load and confirm the offsets/coeffs move the way
  the named parameter implies (uses Track A's scaling math).

### Track E — Rebuild the datapath on the validated decode and demonstrate a coherent reverb
**Only after A–C.** Build `tools/aru_datapath2.py` (or refit `aru_datapath`) sourcing **Track A's per-step
table** (real short delays + aligned controls). Success is **not** "it makes sound" — it is:
- the recirculating loop **closes at a stable sub-unity gain** (no runaway, no instant death);
- **RT60 tracks the decay parameter monotonically** across a sweep;
- the impulse envelope is a **smooth exponential-ish decay**, not a finite echo burst or a railed blip;
- consistent behavior across several programs (CONCERT, a plate, a room, RES CHORDS).

### Track F — Adversarial verification (gates every claim)
For each result from A–E, a second independent pass that tries to **refute** it: re-derive from the ROM
independently, re-run with a perturbed assumption, check against a second program. A claim only graduates
✅ if it survives. Specifically interrogate: the `delay=−offset` sign, the `/32` scale (vs `/64`), the
offset↔control step alignment, and any "it looks right" reasoning.

---

## 3. Execution notes / ordering

- **A first, then B in parallel.** A gives the interpretation; B gives the independent firmware-authored
  check. C is quick and can run alongside. D needs A's scaling math. E needs A+C. F gates throughout.
- **Token budget is not the constraint; certainty is.** Prefer the boring cross-check (Track D, Track C
  diff) over another clever datapath tweak.
- **Update the confidence table (§1) as tracks complete** — every item should move toward ✅ or be explicitly
  refuted. The reference docs (`224XL_microword_fieldmap.md`, `_system_architecture.md`, `_modulation_lfo.md`,
  `_technical_reference.md`) carry the same taxonomy and must be kept in sync.

## 4. Definition of done

The 224XL decode is "validated" when: (1) Track A has a written, ROM-derived offset/coeff/alignment
derivation; (2) Track B's faithful ARU passes POST unsuppressed (or the failure is fully characterized);
(3) Track E produces a coherent, parameter-tracking reverb for ≥3 programs; and (4) every ✅ in §1 has at
least one **non-circular** support. Anything not meeting that bar stays labeled 🟡/🔵/🟠/⚪ — honestly.
