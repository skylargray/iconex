# 224XL Vocabulary Provenance Ledger

> **⚠ RE-BASE REQUIRED (2026-07-01, session 0022):** this audit (2026-06-29) was performed inside the
> pre-0022 coordinate system. The GATE-LEVEL entries (bit positions, strobe equations, Booth/cmag,
> `addr = CPC + OFST/ + 1`) still stand — but every entry's *interpretation layer* (which stored value
> means MEMR/MEMW/IO, step indices, "wet output steps 4/99", SDAA-D channel readings, the reset oracle)
> is superseded by the corrected frame: type `l2&3` 0=MEMR/1=MEMW/2=IO/3=idle, IO bits assert on
> stored-0, execution reversed (words 127→128−L). Notably: the old "sel==01→RDRREG wet-output WATCH item"
> is now confirmed-in-frame (every WR-DA sources RDRREG, 13/13 programs), and the old E40-based
> "transpose disproven" verdict was frame-poisoned (re-tested in 0022 — still not the answer, but the
> POST anchor argument was invalid). Authority: `docs/sessions/0022 …` + `docs/plans/021`.

**Purpose.** Every reverse-engineering error in this project traced back to *interpreting* firmware bytes or
hardware nets and then presenting the interpretation as fact. This ledger classifies every term and field we use
so we build only on grounded ones. Produced by an adversarial provenance audit (2026-06-29) against the gate trace
(`224XL_interconnect_netlist.md`), the firmware POST self-tests (`tools/aru_post.py`, `aru_booth.py`), the Service
Manual, and the ROM. **Re-run / extend the audit when adding vocabulary.**

**Classes:**
- **hardware-verified** — gate-traced AND reproduces a firmware POST golden (E32/E40/E83/E91) or a Booth golden.
- **empirically-grounded** — supported by an observed param-sweep / firmware disassembly, but not gate-proven.
- **invented-or-assumed** — our label, no cited support.
- **contradicted-by-source** — the source disagrees with how we use it.

**Tally (46 terms): 18 hardware-verified · 17 empirically-grounded · 4 invented · 2 contradicted.**

---

## ⛔ DO NOT TRUST (was treated as fact; actually invented or contradicted)

1. **`SDAA-D` D/A channel select as a 4-bit binary nibble** — **CONTRADICTED** (§2T.4 L1099-1101). The hardware
   is **four independent one-hot AND-buffer enables, in REVERSED order**: `OFST8/→SDAD (D)`, `OFST9/→SDAC (C)`,
   `OFST10/→SDAB (B)`, `OFST11/→SDAA (A)`. A `WR DA/` step writes the DAB to *every* enabled channel. The old
   binary nibble was wrong on both encoding and bit order. **FIXED 2026-06-29** in `tools/aru_freerun.py`
   `device_decode` (cross-confirmed: real CONCERT `WR DA` steps set several `OFST8-11` bits at once — a binary
   index cannot be "3 channels"; strict one-hot would be illegal). POST + M3 suite stay green.
2. **§7.5 step→function map's "✅ verified" badge** — **CONTRADICTED by our own docs.** The param names and the
   firmware group-table/decay-generator mechanism are real, but there is **no reproduced golden, no itemized
   sweep log, no topology trace.** `224XL_microword_fieldmap.md` itself says a working reverb from this map "has
   never been demonstrated end-to-end (UNKNOWN)." → downgrade to *"step assignments disassembly-grounded;
   end-to-end UNVERIFIED."*
3. **"diffuser block = steps 5-23"** — **INVENTED** (this session; lived only in a trace tool). §7.5 maps params
   to steps 27-119 and never to 5-23 (input-diffusion P4 = 29-32/81-84). The 19 identical `0x1AB3`/`cmag=0`
   microwords at steps 5-23 are **real microwords of unknown function** — do not call them a diffuser.
4. **"allpass" / "all-pass" internal topology** — **INVENTED.** The Service Manual has zero "allpass" hits for
   the digital section (it uses elliptical/Cauer only for the *analog* anti-alias filters). Imported by analogy
   from Schroeder/Dattorro theory; no traced read→MAC→write all-pass step triple exists.
5. **"tank feedback" / "recirculating tank" with correct loop gain** — **INVENTED / over-asserted.** DMEM-as-
   shared-buffer is grounded and a hand-built comb decays (M3.3), but CONCERT is currently over-unity and does
   **not** decay (M4 open). A correctly-decaying tank is asserted, not shown.
6. **⚠ WATCH — `sel==01 → RDRREG` "wet output" (added 2026-06-29).** The gate Boolean is hardware-verified
   (§2T.3 `RDRREG/ = NAND(NAND(MEMW/,2Y1), DAB RSTB)` genuinely ORs the MEMW and sel==01 cases), but the
   **functional role** ("this is the intended wet output to `WR DA/`") is **inferred** — not stated by §2T/SM and
   not POST-exercised. A correct equation must not launder an unproven role. Treat as a hypothesis.

## ✅ SAFE TO RELY ON (genuinely hardware-verified)

- **Coefficient datapath:** `cmag = (~l3>>2)&0x3F` (6-bit magnitude C0..C5, gate-traced MI26-31, Booth 20/20 +
  E83); `coeff = cmag/32` (cmag=32 = ×1.0, golden-proven; "/32" is a derived label, not an SM phrase); `CSIGN`
  (l2 b7) and its `−M−1` negate; `>>3` **round-half-up** result (golden-proven it rounds, not truncates).
- **Microword field decode (bit positions):** `WA` (l2 b2-3 = MI18/19), `RA` (l2 b4-5 = MI20/21), `MEMAC`
  (l2 b1 = MI17), `MI16` (l2 b0), `ZERO` (~l3 b1 = MI25), `XFER`'s **bit position** (~l3 b0 = MI24). (E40/E83/E91.)
- **DMEM addressing:** `offset = l0|l1<<8` (MI0-15); complemented-OFST polarity; **`addr = CPC − OFST =
  CPC + OFST_stored + 1`** (the most-corroborated term: gate + *verbatim* SM §3.6 + E91); `MEMR`/`MEMW` select;
  `RDRREG` (RES→DAB, general MEMW case); `CPC` counter+role; dec-2 `{OFST12/,OFST13/}` **bit order**.
- **Caveat riding even on these:** several are "bit-map verified, *gating/timing/cadence* not golden-exercised" —
  `XFER=1` transfer gating, `ZERO`'s AS0-edge timing, `XFER` load gating, and `CPC`'s **+1/sample RUN cadence**
  are gate-traced but not exercised by any POST golden.

## 🟡 EMPIRICALLY-GROUNDED (use, but flag as not gate-proven)

- The whole §7.5 param→step map (Predelay→42,94; Chorus→57,108; Diffusion-group→52,60,72,104,111,123; tank-fb→
  27,28,79,80; LF/Mid/Treble decay rows) — disassembly-derived bindings, *labels* interpretive, no sweep log shown.
- `RD AD/`, `RD XREG/`, `WR DA/`, `WR XREG/` (gate + SM, but the FPC A/D & D/A path is outside every POST).
- `cmag=0` semantics (no cmag=0 golden; the "+57 DC trickle over 19 steps" is self-admittedly untested).
- `cmag=63` "+9" correction (reproduces firmware uniquely, but **no gate produces it** — owner-admitted; origin open).
- deferred-MAC 1-instruction pipeline (SM prose verbatim, timing not golden-verified; NOT the cmag=63 cause).
- perceptual labels "predelay" / "chorus" / "delay tap" (mechanism solid; the musical name is nomenclature).

## Answers to the two grounding questions that prompted this audit

- **"How do we know which steps are diffuser vs delay taps?"** We don't, for DSP *role*. Hardware-verified is only
  the *mechanism*: any `MEMR`-at-offset reads a delayed sample (`addr = CPC−OFST`), so **"delay tap" is safe
  nomenclature**. **"Diffuser / allpass / tank" are interpretation with no traced topology.** §7.5 binds
  front-panel *parameters* to steps via the disassembled group table — that gives "Predelay touches 42/94," never
  "step N is an all-pass."
- **"Where does `cmag` come from — is it invented?"** The **field is hardware-verified** (gate-traced to the
  Booth coefficient input, reproduces E83 20/20). The **name** is ours. Only the `cmag=63` "+9" correction is
  open (reproduces the firmware; its gate origin is unknown by the owner's own admission).

## Method (keep using it)

Never interpret a firmware-built byte layout or a single net in isolation. Trace the firmware on the **verified
kosarev core** under `tools/trace8080.Trace8080` (full write + I/O capture) and OBSERVE; cross-check every claimed
field against a POST golden; classify, don't assert. The `z80emu` core has a known 8080 parity bug — do not trust
structure claims derived from it (`aru224_emulate`); cross-check against the kosarev trace.
