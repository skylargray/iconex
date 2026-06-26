# 224XL Track A + Track C Results — Offset/Delay Derivation, Per-Step Alignment, and the mem[0x4000] Verdict

Status: synthesized from the adversarially-verified Track A.2–A.5 and Track C.1 findings. Confidence tags reflect whether the **verifier independently reproduced** the claim by a non-circular check (re-disassembly, perturbation, or measurement). Where finder and verifier disagree, the better-evidenced side is taken and the disagreement is stated.

> **Cardinal rule of this project:** never confuse *plausible* with *verified*. A claim is CONFIRMED only with a non-circular check. "It looks like a reverb / the value looks sane" is at most PARTIAL.

---

## 1. Delay derivation: delay = f(stored bytes, SIZE)

### 1.1 The two build paths (CONFIRMED)
`B55B` (NVS4) is the per-program step-builder. It selects a path on the byte at **recbase+0x30**:

```
B563  2A 03 3E   LD HL,(0x3e03)     ; (0x3e03)=recbase+4
B566  11 2C 00   LD DE,0x2c
B569  19         ADD HL,DE          ; -> recbase+0x30
B56A  7E         LD A,(HL)
B56B  FE FE      CP 0xfe
B56D  C2 5A B6   JP nz,0xb65a       ; non-FE path if != 0xFE
```
CONCERT @0xB800 = 0xFE → **FE path**. CHAMBER @0xC000 = 0xFF → **non-FE path**.

Both paths write a 16-bit signed-offset table **DOWNWARD from 0x3F4D** (hi@a, lo@a-1, a = 0x3F4D − 2·step), 2 bytes/step. This is exactly the buffer `aru224_emulate.tap_map` reads. **(CONFIRMED — re-disassembled; independent run reproduces tap_map(0xB800) 128/128.)**

### 1.2 FE path arithmetic (CONFIRMED)
The FE offsets are **not** a live `ptr − writeptr` subtraction. They are read from a **pre-baked 4-byte/step table at recbase+0x2A8, downward**, each entry tag-routed:

```
w   = (hi<<8)|lo
tag = topbyte & 3
if tag == 2:   offset = signextend16(w)            # passthrough of a pre-signed word
elif w > DA:   offset = (w - DA) + BASE             # WRAP (loop-length wrap)
else:          offset = w                           # passthrough
```
- `DA = var_DA = (0x3CDA) = 6004` for CONCERT (delay-line length; seeded from record +0x38, word 0x1774).
- `BASE = (0x3CE5)`. At SIZE=0, `BASE = var_DA + 1 = 6005` (proven exact).
- Verified: baked 6007 → (6007−6004)+6005 = **6008** (the recirc-loop tap).

Helpers (CONFIRMED, unit-tested): `B714` = HL−BC; `B6FA` = base+scaled-index address-gen; `0x1137` = logical DE>>1; `0x11FB/0x120B` = 8×16 shift-add multiplies.

> Verifier note: the finder's prose said var_DA is seeded from recbase+0x3A; the correct byte is **recbase+0x38** (value/word right). Minor addressing slip, no conclusion affected.

### 1.3 Non-FE path arithmetic (CONFIRMED)
`B65A` is a hand-rolled strided **2-of-4** copy (no LDIR): for each 4-byte baked record at recbase+0x2A7 downward, only bytes 0–1 (offset hi:lo) are copied to 0x3F4D; bytes 2–3 (per-step control data) are skipped.
```
B666 7E LD A,(HL) / B667 12 LD (DE),A / B668 2B DEC HL / B669 1B DEC DE
B66A 7E LD A,(HL) / B66B 12 LD (DE),A / B66C-B66E 2B 2B 2B (skip bytes 2,3)
B66F 1B DEC DE / B670 0D DEC C / B671 C2 66 B6 JP nz / B674 LD HL,0xFFFF / B677 LD (0x3cdc),HL
```
HL−=4/iter, DE−=2/iter, C=0x80=128 steps. Output format is **identical** to the FE path. Verified byte-for-byte against a live CHAMBER boot snapshotted at PC=0xB67A (256/256 match), and generalized to 4 non-FE programs.

> Caveat: byte-identity to the live load holds only **at build completion (PC=0xB67A)**. In firmware steady state the bottom ~50 entries (steps 78–127) are overwritten by runtime activity.

### 1.4 Units (PARTIAL)
SAMPLES. Evidence: 128/128 match to `tap_map` (a samples-documented oracle) with **no `>>1`/`<<1` on the offset value** anywhere in B55B. The only shifts are `*16`/`*4` address scalings on the internal byte-base and a `/2` on intermediate wrap sums. **Gap:** samples-vs-bytes at the DMEM CPC-offset *address* level was not exercised by any verifier → PARTIAL at the hardware-address layer.

### 1.5 Sign convention (delay = −offset is **REFUTED**)
The stored value is the raw signed-16 offset; B55B applies no NEG/CPL. The downstream gloss `delay = −offset` is **overturned** for the physical taps:
- CONCERT: 35/128 offsets negative, **92 positive** (independently re-measured: n_neg=35, n_pos=92).
- The validated recirc loop (6008×4) and short delays (128, 1756, 2242) are **positive** offsets. Under `delay=−offset` those physical taps would be negative (nonsensical).

**Best-evidenced reading:** for the sensible band, physical **delay = +offset**. The negative entries (e.g. tag2 → −12353; the −1 entries) are special tap types (write-tap / sentinel), not ordinary delays. The sign→physical-delay mapping must be re-litigated against the DMEM write logic (Track B/E).

### 1.6 SIZE scaling — resolves "19679 vs 6008" (CONFIRMED)
SIZE enters as the byte at **0x3CCE** and scales BASE via the step-scale 0x3CE9:
```
BASE = (var_DA + 1) + k*(stepscale - 16),  k ≈ 284.8,  stepscale ∈ [16 (SIZE=0) .. 64 (SIZE=max)]
```
- SIZE=0: BASE=6005, recirc tap 6007 → **6008**.
- SIZE=max: BASE=19676, recirc tap 6007 → **19679** (the documented full-boot snapshot).

The "19679 vs 6008" discrepancy is the **same tap at two SIZE settings** — both physical. The live-vs-isolated delta is exactly:
```
19679 − 6008 = 13671 = BASE_live(19676) − BASE_iso(6005)
```
i.e. **the SIZE knob, not a writeptr bug**. This resolves the previously-open "FE writeptr-base scaling (176ms vs 577ms loop)". (The k≈284.8 constant is empirically fit, traced to B60C's `*16` (four `ADD HL,HL`) + a `*DE` multiply; only the SIZE=0 endpoint is algebraically exact → PARTIAL on the closed form.)

### 1.7 Which base is physical (CONFIRMED)
`BASE = (0x3CE5)` is used by every **active** tap. `0x3CE7 = 35770` is an **artifact base**: it finalizes only inactive FILL entries (baked 35770/35771/65535) producing −29765/−1 garbage that 0xFFFF fill overwrites. (Confirmed only after correcting a PC-visit-census measurement trap with precise **terminal-branch** tracking — re-verifiers must use terminal-branch tracking, not PC-visit counting.)

---

## 2. Per-step alignment: SLOT-INDEX-KEYED (CONFIRMED)

This is the load-bearing correction to Session 11. The naive same-index-by-step pairing was wrong; offsets are gathered through the bytecode's **named slot indices**.

### 2.1 Pipeline order (CONFIRMED, by live icount during CONCERT load)
```
0x13B6 dispatcher (1780500)
  → B55B step-builder (1786990)   : write OFFSET table downward from 0x3F4D (ptr 0x3CF1)
  → 0xAA38 bulk interleave        : copy 0x3F4D buffer into OFFTAB @0x41FD downward (HL-=2, DE-=4, B=0x80)
  → 0xAA9F interpreter (1804731)  : expand record bytecode; 3-byte step descriptor → 0x3CF4; CONCERT=32 steps
  → 0xAB39 terminator (1807514)   : lane assembly / strobes (ports 0-3)
  → B4F0/B4FF coeff pass (1810111): fill lane3 (coeff/XFER/ZERO), active-low (CPL), AFTER the interpreter
```
> Mechanism correction (CONFIRMED): the **dominant OFST writer is the AA38 bulk-copy loop**, not the AA9F interpreter body. `LD DE,0x4003` @AB16 is a *per-step coeff* subroutine. The final constant lane0=0x89 in the 0x4000 image arises because **later passes overwrite/repack** lane0 — the OFST packing is non-trivial.

### 2.2 The binding (AB0C → B510) (CONFIRMED)
Each slot reference is a bytecode byte = `(bit7=CSIGN) | (bits0-6 = slot index k)`. `AB0C` masks `AND 0x7f` → k, embeds the coeff pointer `0x4003+4*k` into the control image, then fetches the coeff via `0xB510`:
```
B510: 2A 05 3E LD HL,(0x3e05) / 19 ADD HL,DE / 7E LD A,(HL)   ; 0x3e05 = recbase+0xC0AA
```
A single index **k** keys BOTH:
```
OFFSET = OFFTAB[k] = offbuf[k]                        (lanes 0-1)   [OFFTAB[k] @ 0x41FD-4k == offbuf[k], CONFIRMED]
COEFF  = mem[recbase+0xAD+4*k]  (bit7=CSIGN)          (lane3 bits2-7)
```
0xB510 fetch confirmed end-to-end: 0x3e05 = (0xB800+0xC0AA)&0xFFFF = 0x78AA; all 30 fetches addr == recbase+0xAD+4·slot.

### 2.3 Header decode + canonical ordering (CONFIRMED)
Header low nibble N (`AND 0x0F`) = #slot refs (N=0 → control-only/structural step, AAC9 skip). Bits 4–5 (`AND 0x30`) select emit format: 0x00→AB26, 0x10→AAE8 (CSIGN-conditional), 0x20→AACD. CONCERT: N∈{0:6,1:10,2:12,4:3,6:1}; subop∈{0x00:17,0x10:7,0x20:8}.

**Canonical step ordering:** steps emitted in bytecode order (DE walks the bytecode); within a step, slot refs left-to-right; each ref's offset/coeff gathered through the named index k — **never by advancing an offset pointer**. Proof: CONCERT step0 references slots **0x6c and 0x39** (not 0,1). This directly explains the Session-11 dead tank.

### 2.4 Device / WA / RA / XFER / ZERO (INFERRED for the per-step pack)
Lane meanings owner-traced (lane2 b0=MI16, b1=MI17/MEMAC, b2:3=WA, b4:5=RA, b7=CSIGN; lane3 b0=XFER, b1=ZERO, b2:7=coeff; device (MI17,MI16)=11 read/10 write/01 sub-decoder/00 NC). But the **bit-for-bit assembly** into the final 32-bit microword happens in the AB39 terminator tail (AB80-ABA5: `AND 3`/`CP 2`, `AND 0x30` over 0x4000-0x41FF) + coeff pass and is **not proven bit-for-bit** here. The slot-keyed **binding** is CONFIRMED; the WA/RA/XFER/ZERO per-step provenance is INFERRED.

### 2.5 Paired read/write taps — finder's "+0x33" is **REFUTED**
Taps come in **coeff-matched consecutive pairs** (B510 fetches consecutive, identical coeff bytes) — CONFIRMED. But the "+0x33 constant / high-copy = −1 write-tap" story is overturned: measured index diffs are **0x33, 0x34, and 0x04** (not constant; the finder's own evidence even lists 0x34); pair 0x44/0x40 = offsets 6000/4855 (neither −1); pair 0x77/0x73 = both −1. → "coeff-matched paired taps" stands (PARTIAL); the index rule and −1-sentinel meaning are GUESS pending a DMEM-write trace.

---

## 3. Track C: what is mem[0x4000:0x4200]? (CONFIRMED — decommission as offset source)

`mem[0x4000:0x4200]` is the interpreter's **coefficient/bytecode working region** (a 4-byte-stride control/coeff image), **NOT** the per-step offset table.
- `0x4003 + 4*k` is the coeff-source-index base (`LD DE,0x4003` @0xAB16; `capture_coeffs` uses `idx=((DE-0x4003)//4)`).
- It is a real, **freshly-rebuilt-per-program** memory-mapped image: 464–512/512 nonzero for **all 20 programs**, FE and non-FE alike (REFUTING the prior expectation that it would be empty for non-FE). Distinct per program; not stale.
- Hardware reads the 0x4000 window **directly**: a ROM-wide scan found **zero** block-I/O (OTIR/OUTI/OTDR/OUTD). Ports 0/1/2/3 are single-byte strobes.

Why it is **not** the offset source (the `aru_datapath` read `offset = ~(l0|l1<<8)`):
- CONCERT: **100/110** active steps |offset|>16384 (clustered near 65535 = whole-DRAM) — the Session-11 garbage.
- All 20 programs: the two decoders share **essentially zero** offset magnitudes (18 share 0; 20/20 material disagreement).
- **Not a polarity bug:** the non-inverted decode is still garbage (35/110 >16384).
- **Structural proof:** lane0 of the 0x4000 image is a **constant 0x89** across CONCERT steps — an offset low-byte cannot be constant across steps with varying delays.

**Verdict:** DECOMMISSION `mem[0x4000:0x4200]` as an offset source. Validated offset pipeline = `B55B → 0x3F4D-downward buffer → aru224_emulate.tap_map`. Likewise `aru224_emulate.decode_image(0x3E4E)` does not reproduce validated delays (per-lane intermediate, not the hardware microword) and must not be an offset source.

**Decommission is NOT cosmetic:** `import aru_datapath` has ~110 importers **including `tools/export_golden_224.py`** (the golden/C++ export pipeline). Rewire the golden/experiment tools to source offsets from `tap_map`/0x3F4D before retiring `load_microcode`; it may be kept only for the coeff/control-image side or diagnostic diffs.

---

## 4. Confidence summary (post-adversarial)

| Item | Tag |
|---|---|
| FE selector recbase+0x30==0xFE | CONFIRMED |
| FE offsets from pre-baked tag-routed table @recbase+0x2A8 | CONFIRMED |
| Offset stored downward to 0x3F4D via 0x3CF1 | CONFIRMED |
| Units = SAMPLES | PARTIAL (DMEM-address layer untested) |
| No NEG/CPL in B55B | CONFIRMED |
| **delay = −offset** | **REFUTED** (physical taps are positive) |
| Wrap (w−var_DA)+BASE; 6007→6008 | CONFIRMED |
| BASE=var_DA+1 at SIZE=0 | CONFIRMED |
| 19679 vs 6008 = SIZE param; both physical | CONFIRMED |
| BASE SIZE-scale slope ≈284.8 | PARTIAL (endpoint exact, constant fit) |
| 0x3CE7=35770 = artifact base | CONFIRMED |
| B714/B6FA/0x1137/0x11FB/0x120B helpers | CONFIRMED |
| Non-FE B65A strided 2-of-4 copy | CONFIRMED |
| Non-FE byte-identical to live at B67A | CONFIRMED (steady-state differs) |
| Non-FE format == FE format | CONFIRMED |
| 0xB510 fetch = recbase+0xAD+4·slot | CONFIRMED |
| Slot-index-keyed alignment (not sequential) | CONFIRMED |
| AA38 OFFTAB[k]==offbuf[k] | CONFIRMED |
| VM 0xAA9F 3-byte descriptor / 32-step CONCERT | CONFIRMED |
| **"+0x33 / high-copy=−1 modulated tank"** | **REFUTED** |
| coeff-matched paired taps | PARTIAL |
| mem[0x4000] = per-program working image, not stale | CONFIRMED |
| No OUT upload loop; ports 0-3 strobes | CONFIRMED |
| Lane3 coeff separate pass, active-low | CONFIRMED |
| Dispatcher→B55B→AA9F→strobes order | CONFIRMED |
| AA38 is the dominant OFST writer (not AA9F body) | CONFIRMED |
| 0x4000 OFST packing non-trivial | CONFIRMED |
| tap_map sane / 0x4000 garbage / decommission | CONFIRMED |
| 20 program bases/IDs | CONFIRMED |
| Live≠isolated 0x3F4D (= SIZE shift) | PARTIAL (live 0x4000 decode-back not shown) |
| FE/non-FE bytecode entry; non-FE skipped 2 bytes = control | INFERRED |
| /32 coeff scale, ±2^18 rail | INFERRED (offset path only; untested here) |

---

## 5. Open questions for Tracks B / D / E
1. **Track B (POST):** make a faithful ARU pass the suppressed POST self-test (the 0x0E95/0x0F2C pattern-and-OUT path), end-to-end.
2. **Track E (lane packing / rebuild):** decode the bit-for-bit packing of OFST into the 0x4000 microword (lane0 overwritten to 0x89 by B4FD/AC05/AD0C/AD33 — recover the repack map); then prove the live 0x4000 image decodes back to the validated delays. Prerequisite for the datapath rebuild.
3. **Sign→physical-delay:** prove delay=+offset for the sensible band; resolve the −1/−12353 entries via the DMEM-write logic (AB39 tail + WR-DA/ node).
4. **WA/RA/XFER/ZERO per-step provenance:** header sub-op bits vs a separate baked field; map image bytes to the microword fieldmap.
5. **Paired-tap semantics:** index relationship (0x33/0x34/0x04) and read-vs-write-tap role; the −1 sentinel meaning.
6. **SIZE closed form:** reduce BASE=(var_DA+1)+k·(stepscale−16) (k≈284.8).
7. **Track D (decommission rewiring):** rewire `export_golden_224.py` + experiment tools off `aru_datapath.load_microcode`; verify slot-keyed alignment beyond CONCERT/CHAMBER.
8. **0x3E4E retirement:** decide whether `decode_image(0x3E4E)` is retired entirely.
9. **var_DC vs var_D8:** find a record where D8≠DC to separate the B6A4/B6B2 threshold roles.
10. **0xADA5 modulation animator:** confirm it consumes the 0x3CF4 descriptors and how it perturbs OFFTAB[k] per-sample (the always-on tank).