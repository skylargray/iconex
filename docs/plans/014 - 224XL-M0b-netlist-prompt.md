# 224XL — M0b kickoff prompt: faithfully transcribe the interconnect netlist

> **Paste this as the opening task for a fresh session.** It is self-contained. Read the linked files
> before acting. Your job is **M0b** of `docs/plans/013 - 224XL-holistic-model-plan.md`: produce the holistic
> **interconnect netlist** of the ARU + T&C + DMEM — the net-by-net wiring that the phase-accurate RTL model
> (Phase 1+) will be built from. **This is a faithful-transcription job, gated on owner review before any code.**

---

## 0. The one rule that overrides everything (we learned it the hard way)

Earlier in this project an "audit" invented two false anomalies in the owner's correct ARU pin trace because it
used **datasheet pinouts from training memory**. Both were wrong; the owner caught them. So:

1. **NEVER state a part spec or pinout from memory.** Every chip pinout is already datasheet-verified and lives in
   `docs/reference/224/parts/*.v` (PINOUT blocks) and is summarized in
   `docs/reference/224/224XL_partspec_verification.md`. **Use those. Do not re-derive a pinout.** If you hit a
   chip with no `.v` file, stop and run the verify pipeline (§4) before using it.
2. **The schematic + the owner's traces are GROUND TRUTH for what is wired.** Transcribe them *faithfully*.
   Do **not** "correct" the owner, and do **not** label anything an "anomaly / reversal / swap / bug." If the
   wiring looks wrong to you, you are misreading it — re-read. (Bit-significance comes from how a *whole nibble*
   is wired together, never from one pin's index label.)
3. **Flag gaps; never guess.** Anything you can't read on a sheet/crop goes in a GAPS list with the exact
   location, not a plausible-looking invention.
4. **Provenance + confidence on every net** (✅ read on sheet/owner-trace · 🟡 inferred/partial · ⚪ unknown).
5. **Adversarial verification targets OUR OWN reads** (hallucinated nets, misread pins) — not the owner's board.
6. **Board-prefix every chip:** `aru_` (060-01318), `tc_` (060-02475), `dmem_` (060-02512). U-numbers restart
   per sheet, so `aru_U49` ≠ `tc_U49` ≠ `dmem_U49`, and `dmem_U6` is even two chips on one sheet. Endpoint
   format: `aru_U43.pin11`.

Full rationale: plan §0. Memory: `224xl-pinout-audit.md`, `224xl-board-namespace.md`, `224xl-holistic-m0-progress.md`.

---

## 1. What is already DONE (do not redo)

- **L1–L3 verified** (8080 core, firmware boot, the WCS image it builds). `tools/boot8080.py` → CONCERT offsets.
- **M0a COMPLETE** — every chip's pinout datasheet-verified (render → read → archived in
  `docs/reference/224/datasheets/`), cross-checked against `parts/*.v`. Table:
  `docs/reference/224/224XL_partspec_verification.md`. Three real `.v` pinout errors were found and fixed
  (`74ls670`, `74ls123`, `mcm68b10`). **`parts/*.v` is the authoritative part inventory** (each has the verified
  pinout + Lexicon P/N + in-224XL designators). Parts present include: 74xx00/02/08/10/20/27/74/86, 74s04/175,
  74f157/374, 74ls123/133/138/139/155/163/174/194/195/244/377/393/670, 74xx283 (adders), 4164 (DRAM),
  mcm68b10 (128×8 WCS SRAM), am8304 (octal transceiver), mc4044 (PLL phase detector), dl630b (5-tap delay).
- The **ARU accumulator/PP back-end is already net-traced by the owner**, pin-by-pin, in
  `docs/reference/224/224XL ARU pinouts from 060-01318.txt` (U5–U12, U19–U23, U33–U37, U43–U49). **Transcribe
  this directly** (it is the highest-confidence source); just re-key it to the verified pinouts and the namespace.

What is NOT done: the cross-board interconnect (DAB bus + who drives it each cycle), the T&C device-decode and
clock/strobe generation, the DMEM address path + DRAM/XREG, and the ARU register-file/multiplier front-end
wiring. **That is M0b.**

---

## 2. The deliverable

`docs/reference/224/224XL_interconnect_netlist.md` — a net-by-net wiring table + a one-page block diagram,
organized by the six net-groups below (plan §3 Phase 0b). For every net: `net → [board_Uxx.pinN, …]`, the
single **driver** vs the **loads**, **confidence**, and **provenance** (which sheet/crop/owner-source). Anything
unreadable → the **GAPS / QUESTIONS FOR OWNER** section. Keyed entirely on `parts/*.v` pinouts.

**The six net-groups:**
1. **DAB bus** (16-bit shared): every driver + receiver + the per-cycle **tri-state enable** for each (regfile
   D-in, result-reg Q-out via RDRREG/, XREG bridge, FPC RD AD/, DMEM read data). Who drives each step?
2. **Device decode / DAB-driver select**: `tc_U47` (LS139) + `tc_U48` (LS00) + `tc_U49` (LS10, incl U49C=WR DA/)
   + `tc_U34A` — the logic turning (MI16,MI17,MI12,MI13,MI4,MI7) into bus-driver enables / DMEM r-w / sub-selects.
3. **WCS-output → control-input wiring**: every microword latch bit → its destination pin (regfile WA/RA, the
   coefficient serializer M0/M1 via the 74195/74194 shifters, CSIGN, XFER CK, ZERO/, the offset bits → the
   address adder). This *replaces* the abstract "field map."
4. **PP / accumulator bus** (ARU): mostly **transcribe the owner pin trace** — adders `aru_U19-23`, sat-mux
   `aru_U33-37`, accumulator `aru_U45-49`, product reg `aru_U10-12`, subtract XOR `aru_U5-9`, result reg
   `aru_U43-44`. Add the multiplier front-end (regfile `aru_U29-32` 74670, operand shifters 74194, Booth/M0-M1).
5. **Address path** (DMEM): CPC `dmem_U51/U65` (393) → adder `dmem_U49/U50/U63/U64` (283, A=CPC / B=OFST/,
   carry-in high) → carry-out=bank → row/col mux `dmem_U36/U18` (157) → DRAM array (4164, 2 banks, bit-sliced);
   XREG `dmem_U38-41` (374) bridging DAB↔DATA; CAS gating; the DL630B (dmem_U59) strobe sequencer.
6. **Clock distribution**: MC, MS0-8, AS0/1/2, ARU CK, DAB WSTB(≈MS7), XFER CK, ZERO/, DAB RSTB, ARUCKE/ — which
   element each edge clocks. Cross-check against fig-3.2 / 3.3 / 3.4. T&C clock-gen uses mc4044 (PLL) + counters.

---

## 3. Sources (exact paths)

**Schematic sheets (PRIMARY — full pages, very high-res):**
- ARU: `docs/reference/224/Lexicon-224X-Service-Manual-060-01318.png` (6366×5000)
- T&C: `docs/reference/224/Lexicon-224X-Service-Manual-060-02475-D_1.png` and `…-D_2.png` (~9500×6300, 2 sheets)
- DMEM: `docs/reference/224/Lexicon-224X-Service-Manual-060-02512_1.png` and `…_2.png` (~9300×6200, 2 sheets)
- (also `…-01318-U29-U32.png`, `…-01318-U43-U44.png` = ARU detail crops.)
- Supplementary crops: `docs/reference/224/crops/` (236 files; named by region, e.g. `q_ADDER`, `q_MUX`,
  `s1f_CPC`, `tc2_srcselect`, `v_XREG`, `aru_regfile`, `aru_resultreg`).

**Verified part pinouts:** `docs/reference/224/parts/*.v` + `224XL_partspec_verification.md` + `datasheets/`.

**Owner ARU pin trace (authoritative back-end):** `docs/reference/224/224XL ARU pinouts from 060-01318.txt`.

**Timing figures:** `docs/reference/224/images/fig-3.2-…png` (T&C), `fig-3.3-…png` (DMEM), `fig-3.4-…png` (ARU MAC).

**Prose / prior decode beliefs (use as leads, re-verify against the sheet):**
`224XL_system_architecture.md` (§2 DAB, §5-6 address), `224XL_microword_fieldmap.md` (device decode),
`224XL-interp-stack.md`. **Treat all prior crop-derived netlist claims as 🟡 until re-confirmed on the full
sheets — an earlier crop-extraction pass hallucinated nets; the verifiers caught it.**

---

## 4. Tooling reality (don't fight it)

- **The Read tool cannot render PDFs here** (`pdftoppm` missing). For datasheet PDFs: `import fitz` (PyMuPDF) →
  `page.get_pixmap(matrix=fitz.Matrix(z,z), clip=fitz.Rect(...))` → save PNG → Read it.
- **The schematic SHEETS are PNG, not PDF, and are 6000–9500 px** — a whole-page Read gets downscaled to
  illegibility. **Tile-and-trace:** crop regions with **PIL** (`Image.open(...).crop((l,t,r,b)).save(...)`) and
  Read each tile. Trace nets across tile boundaries (overlap your tiles ~10%). Use the crops/ files for known
  sub-blocks.
- **Image size limit:** keep each rendered/cropped image **under ~1900 px per side**, especially when reading
  several in one message (larger multi-image reads get rejected). Render at a zoom/crop that respects this.
- Watch for **non-monotonic pinouts** (the 74283, 74123, and the DL630B taps are all "crossed" — that's real;
  trust the verified `.v`).

---

## 5. Recommended execution (ultracode: orchestrate it)

Do M0b as a **workflow**, net-group by net-group / sheet-region by sheet-region, with adversarial verification —
the same pattern that worked for M0a's verification:

- **Fan out one tracer per net-group** (or per sheet quadrant). Each agent: tiles its sheet region with PIL,
  reads the tiles, and emits a structured net list (`net → driver + loads`, board-prefixed, keyed to the `.v`
  pinouts, confidence + provenance, gaps). **Hard instruction to each: flag-don't-guess; pinouts come from
  `parts/*.v`, never memory; cite the tile you read each net from.**
- **Adversarially re-read** each fragment with a second agent (re-tile, independently confirm the high-stakes
  nets — bus connections, control destinations, the adder A-vs-B, clock edges). Default to DISPUTED if not
  positively visible. The verifier hunts OUR hallucinations.
- **You (main loop) synthesize** the verified fragments into the netlist doc + block diagram + gaps. Keep the
  ARU back-end as a direct transcription of the owner pin trace (don't re-trace it from the sheet unless verifying).

Suggested order: (4) ARU back-end transcription [fast, owner-trace] → (2)+(3) T&C decode+control on 060-02475 →
(5) DMEM address/DRAM/XREG on 060-02512 → (6) clock dist on 060-02475 + figures → (1) DAB summary [depends on 2].

First concrete steps: read this prompt's linked files; open `224XL_partspec_verification.md` and skim every
`parts/*.v`; render a low-zoom overview of each sheet (PIL, downscaled, just to map where blocks are); then start
the workflow with the ARU back-end + T&C decode groups.

---

## 6. The gate

M0b ends at **M0: present the netlist to the owner for correction BEFORE any Phase-1 code.** The owner reads the
schematics; your netlist is a draft for them to correct. Surface the GAPS prominently (they offered to point you
to sources). Do not start the RTL framework until the owner signs off on the netlist.

## 7. Mistakes already made — do not repeat
- Memory-derived pinouts (the false audit). · Trusting crop-extractor output without adversarial re-read.
- Missing a pin diagram by only rendering part of a datasheet (the DL630B). · Reading "DL**6**30B" as "DL**G**30B"
  and "74L**S194**" as "74199" — read labels carefully, owner-confirm part identities.
- Building anything from literal pin numbers without the verified `.v` (it bit-scrambled a nibble once).
