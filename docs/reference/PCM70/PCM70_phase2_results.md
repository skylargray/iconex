# Phase 2 — PCM70: the modulation / live-update axis

**Input set:** `Lexicon_PCM-70-V2_0-U62.BIN` (32K), `…U67.BIN` (8K), `…U95.BIN` (16K).
**Legend:** ✅ verified by our disassembly · 🟡 strong structural evidence · ❓ open.

---

## Phase 0 — integrity verdict: **PASS** ✅

Unlike the corrupted V2.0 PCM60 set, this one is clean and usable:

- Three **distinct** images (distinct MD5/SHA1) — no dedupe-collapse.
- **No Intel-HEX ASCII contamination** (zero `:NNNNNN…`-style records anywhere — the exact failure that poisoned the V2.0 PCM60 tails).
- **No address-line aliasing/mirroring** (half/quarter self-compare ≈ 0.01–0.02; U67's elevated 0.77 is just shared 0xFF fill, not a true mirror).
- Sensible fill: U62 fully programmed; **U67 active only in the lower 1 KB** (0x000–0x3FF), rest 0xFF; U95 lower half full + partial upper.

**Version skew (worth banking):** master **U62 = ©1986, V2.0**; slave **U95 + opcodes U67 = ©1985, V1.20**. The V2.0 revision touched only the host firmware; the slave/microcode are the unrevised V1.20 parts.

---

## ROM roles (from embedded banners + structure) ✅

| ROM | Size / type | Banner | Role |
|---|---|---|---|
| **U62** | 32K / 27256 | `(C) Copyright LEXICON, Inc. 1986` | **Master host Z80** — RST-vector table at 0x00 (`JP 1800h` on the 8-byte grid), program-name strings (CONCERT HALL, RICH PLATE/CHAMBER, INFINITE CHAMBER, CHORUS+ECHO, MULTIBAND DELAY, RES/RHYTHMIC CHORDS…), category + BPM tables. UI / program & parameter manager. |
| **U95** | 16K / 27128 | `PCM70 SLAVE AND SPACEWARE V1.20 1985` | **Slave Z80** — the SpaceWare algorithm + live-coefficient engine. **This is the modulation axis.** |
| **U67** | 8K / 2764 | `PCM70 OPCODES V1.20 1985` | **ARU microcode (control-store image).** Active 1 KB = 8 × 128-byte pages, plane-organized → **128-step program** (matches roadmap PCM60/70 = 128). Repeated step motifs = chained allpass stages. |

This is the roadmap's PCM70 model confirmed: PCM60's static microcode (**U67**) + a slave Z80 (**U95**) that reloads/modulates it, with a new master UI layer (**U62**).

---

## Slave (U95) machine model ✅

- Z80, **IM 1** → interrupt vector `0x38` → ISR at **0x02D3**. **RAM 0x4000–0x47FF** (stack 0x47FF).
- **I/O port map:**

  | Port | Direction | Function |
  |---|---|---|
  | `0x00` | out | WCS/data strobe (write 0 → settle → strobe) |
  | `0x30` | out | control / reset (init value `0x69`) |
  | `0x40` | out | address / latch |
  | `0x50` | in | status & master handshake (bit 0) |

- **Foreground (0x80):** command dispatcher. Polls port 0x50 + RAM command flags (0x4343–0x4348) the master pokes, dispatches handlers.
- **ISR (0x2D3):** lightweight **÷8 timekeeping divider** (alt-bank counter via `ex af,af'`/`exx`, reload = 8), maintains tick counters. This is the **tempo/BPM clock**, *not* the DSP coefficient modulation — modulation runs in the foreground, paced by these ticks.

---

## The live-update / modulation mechanism — core Phase 2 result ✅

**Where the control store lives.** The ARU **WCS is memory-mapped at ≈0x8000–0x83FF** in the slave's space, organized as multiple **128-byte byte-planes**. Evidence:
- `sub_02b6h` loads three 128-byte planes via `lddr` into **0x8180 / 0x8280 / 0x8300**, sourced contiguously from ROM **0x2ACD–0x2C4C** — a region that *contains the smooth descending ramps* found by the table scan (0x2B4D, 0x2B8E). So those curves are **coefficient/offset plane data**.
- Read-back base is a pointer in **RAM[0x42EE]** (`sub_0e51h`: `HL = (42EE) + DE`).
- Structural planes come from **U67 (OPCODES)**; the slave-managed coefficient/offset planes are what get modulated.

**Per-coefficient write primitive — `sub_0ecch` / `sub_0e59h`.** A read-modify-write into one microword byte (preserving opcode/control bits, updating only the coefficient/offset field). Encoding, straight from the code:

- magnitude `>> 2` (÷4) → `cpl` (1's-complement) → mask to **3 bits** (single-byte mode) or **4 bits** (two-byte mode), then `OR` into the preserved upper bits;
- **two packing modes selected by control bit 4** of the existing word (`bit 4,a → jp z`): 3-bit field in one byte, or a wider field spanning two bytes;
- **sign:** `sub_0e59h` does `bit 7,b → set 3,a` — the value's bit 7 (sign) maps to **microword control bit 3**;
- every write is mirrored to a **RAM shadow at 0xBE00 + offset** (the hardware store is write-only; the shadow makes RMW possible).

> **Resolves §9 "unsigned /256 vs signed + SIGN bit":** the ARU coefficient field is **signed — separate sign control bit + complemented, ÷4-shifted magnitude**. (Also concrete input to §8 ARU arithmetic: the shift/complement idiom is explicit here.)

**Update / animation engine — `sub_071dh`.** Walks a list of **3-byte entries `{addr_lo, addr_hi, value}`**: forms `DE = WCS target`, **steps the value** (`−4`/pass if bit 7 = 0, `−1`/pass if bit 7 = 1 — a multi-rate ramp), writes it back, and pushes it via `sub_0ecch`; self-loops (`jp 0725h`). This is the **de-zipper / envelope / coefficient-animation engine** — it smooths parameter changes and is the substrate slow modulation rides on. It also rotates a **48-byte (0x30) double-buffered parameter block** (0x4000 / 0x4040 / 0x4080) and indexes per-algorithm data via a pointer at **top-of-ROM (0x3FFE)**.

**Change detection — `sub_0527h`.** Diffs working params (0x4000–0x402F) against the loaded copy (0x4040–0x406F); on change runs the reload: `di → sub_071dh → sub_02b6h →` port-0x40/0x00 strobe + 16-cycle `djnz` settle → clear 0x00/0x30/0x40.

**End-to-end:** master writes params → slave RAM 0x4000+ → `sub_0527h` detects change → `sub_071dh` ramps each `{WCS-addr, value}` entry toward target → `sub_0ecch` RMW-encodes it into the memory-mapped WCS plane (+0xBE00 shadow). **Modulation injection points = the WCS addresses in the animated list; "modulation" = time-varying values fed to them.** This is exactly the 480L's open "modulation injection" mechanism, one generation simpler.

---

## What Phase 2 closes for the 480L (§9)

- ✅ **Modulation/live-update mechanism** — slave maintains a list of `(WCS-address, value)` entries pushed through a memory-mapped control-store window with a RAM shadow + RMW. The 480L's `0x48000`-window streaming is the bigger-iron version of this.
- ✅ **Coefficient encoding / sign convention** — signed, separate sign control bit, complemented + ÷4-shifted magnitude; two field-packing modes.
- ✅ **Live-coefficient streaming pattern** (§9 last bullet analogue) — `sub_071dh` + `sub_0ecch`; RMW updates only the coefficient/offset field, leaving opcode/control bits intact.
- 🟡 **Parameter smoothing** is multi-rate ramping in the update list, not instantaneous writes (de-zippering by design).

---

## Carry-over 1 — U67 microword plane field-map: **RESOLVED** ✅ (2026-06, byte-verified)

Re-ran the Phase-1 decoder against U67 **plane-resolved** with the clean PCM60 V1.0 set
loaded, then adversarially verified (two independent verifiers, both `agree=true`, no
successful refutations). Tooling: `tools/u67_planes.py`, `tools/u67_explore.py`,
`tools/u95_wcs_source.py`, cross-referenced against `tools/pcm60_decode.py`.

**Result: U67's active 1 KB = 8 plane-major 128-byte pages = 7 microword data planes (0-6)
+ 1 banner plane (7). Every data plane is a static ARU control / opcode / routing lane.
There is NO resident delay-offset or coefficient-VALUE plane in U67.** The offset and
coefficient *values* are slave-managed at runtime by U95 into the WCS (below).

| U67 plane | Bytes | Label | Evidence | Conf. |
|---|---|---|---|---|
| **0** | 0x000 | control/opcode — most static (section/stride lane) | only **16 unique bytes**, H=2.81; low-nib 98% in PCM60 opcode alphabet; cosine vs PCM60 U43 = 0.944 | ✅ |
| **1** | 0x080 | control/opcode | 27 uniq, H=4.05; low-nib dominated by n7; cosine vs U43 = 0.969 | ✅ |
| **2** | 0x100 | control/opcode — sparse, high-FF, **boundary-marker-like** | 18 uniq, H=3.42, FF/F7 dominant; cosine vs U43 = 0.975 | ✅ |
| **3** | 0x180 | control/opcode — most varied (the *false* "offset-hi" candidate) | highest uniq (39), H=4.60, but high-nibble is the fixed control set, **not** a delay ramp; cosine vs U43 = 0.979 | ✅ |
| **4** | 0x200 | control/opcode (pairs with plane 5) | 29 uniq; 37/3F/27 motifs; cosine 0.982; loNib matches plane 5 78/128 | ✅ |
| **5** | 0x280 | control/opcode — **best** cosine to PCM60 control | 30 uniq; cosine vs U43 = **0.984**; same motif family as plane 4 | ✅ |
| **6** | 0x300 | control/opcode (paired with plane 3 in the spurious offset search) | 29 uniq; n7 dominant; cosine 0.981 | ✅ |
| **7** | 0x380 | **ASCII banner — NOT microcode** | contiguous text `COPYRIGHT 1985  LEXICON INC.  PCM70 OPCODES  V1.20`, 0x1A pad; cosine vs U43 collapses to 0.160 | ✅ |

**Why "all control, no value planes" holds (refutation tests that all FAILED):**
- **Per-bit layout is identical across planes 0-6** — bit5≈0.98, bit4≈0.77, bit3≈0.30 in
  *every* data plane. A free 16-bit address/offset field would have every bit ≈0.5; constant
  bit positions prove structured control words, not value tables. (This also matches the
  Phase-2 coeff encoding: sign → ctrl **bit 3**, packing mode → ctrl **bit 4**.)
- **No offset-lo plane** — PCM60's real offset-lo (U32) has 64 unique bytes; the most-varied
  U67 plane (3) has only 39. None reaches offset-lo entropy.
- **No offset-hi plane** — a genuine offset-hi (PCM60 U38) is dominated by sign-extension
  bytes 0xFF/0xFC/0xFB; no U67 plane shows this (high nibbles are the fixed control set).
- **No coefficient plane** — zero 0x7F (×0.5) scalars in any plane; longest decay run 21 vs
  59 for the genuine U95-sourced WCS envelope.
- **The "60-tap plane3:plane6 offset" was a coincidence** — only 82/128 16-bit pairs are
  distinct and the *repeats* are control-byte pairs (`0x3737`×9, `0x3FFF`×7, `0x2727`,
  `0x27E7`, `0x3F3F`, `0xB737`), i.e. two opcode lanes arithmetically combining — not reused
  delay magnitudes (PCM60's real offset repeats are `0xFFFF` sentinels).
- **Plane-major confirmed** (slicing, not interleave): the banner is *contiguous* at 0x380;
  stride-2/4 "columns" show no field specialization (all columns 42-58 uniq, all 16 low-nibbles
  used) — a real packed microword would expose one high-entropy offset-lo column.

**Open nuance** (🟡 medium): planes 0-6 could **not** be crisply split into orthogonal
sub-roles — they are all control-domain variants (likely different microcode banks / sections /
algorithm-routing columns rather than one-field-per-plane). Pinning which plane feeds which ARU
microword bit-field wants the U95 dispatcher's WCS-write address arithmetic mapped onto the ARU
bit layout.

**Where offset/coefficient values actually live (the corrected lineage):** computed at runtime
in the U95 slave and written into the memory-mapped **WCS (~0x8000-0x83FF, write-only, RAM shadow
0xBE00)**. The static curve source is U95 ROM ~0x2ACD (the smooth descending 0xFF..0x81 envelope),
plus per-algorithm coefficient blocks (record+0x133/+0x233). **So the reverb-tap lineage diff vs
PCM60 must be run U95-WCS-source-vs-PCM60, *not* U67-vs-PCM60** — U67 carries no taps.

**Coefficient WCS plane pinned = WCS plane 6 (0x8300-0x837F)** ✅ (byte-verified): `sub_0655h`
@0x065D stamps `LD DE,0x8300` + `(idx & 0x7F)` as the RMW target for every per-coefficient list
entry (addr_hi = **0x83** for all of them); `sub_0ecch`/`sub_0e59h` write `(DE)`=0x83xx with the
0xBE00+DE shadow; read-back `sub_0e51h` uses `(0x42EE)=algo_base+0x7F33` so DE=0x8300 ⇒
algo_base+0x233 = exactly the per-algorithm coeff block bulk-LDIR'd to WCS 0x8300 @0x06B2. Planes
3 (0x8180) and 5 (0x8280) get only one-shot static curve preloads (`sub_02b6h` lddr); plane 4
(0x8200) only the 0x0A21 dual-pointer load; **only plane 6 receives the moving-index per-coefficient
de-zipper RMW.** (2-byte coeff mode `inc de`; at top index 0x7F the 2nd byte spills to 0x8380.)

---

## Carry-over 2 — LFO phase accumulator in U95: **RESOLVED** ✅ (2026-06, byte-verified)

The phase-accumulator idiom (RAM word incremented per tick, masked/wrapped, used to index a
table) is unambiguously **`sub_0ad2h` @0x0AD2**, the LFO/vibrato modulation engine. Core at
**0x0B6B-0x0B79**:

```
0B6B  2A 35 43   LD HL,(0x4335)     ; phase accumulator (16-bit word)
0B6E  23         INC HL             ; step = +1 per fire
0B6F  7C         LD A,H
0B70  E6 07      AND 7              ; wrap: H constrained 0..7  (0x0800 window)
0B72  67         LD H,A
0B73  22 35 43   LD (0x4335),HL
0B76  7E         LD A,(HL)          ; dereference table -> waveform/direction sample
0B77  32 37 43   LD (0x4337),A      ; cache sampled value
```
Init: `0x06A0 LD HL,0x0010 / LD (0x4335),HL` at algorithm load.

- **Accumulator** = RAM word **0x4335** (lo) / 0x4336 (hi); dereferenced sample cached at **0x4337**.
- **Step** = fixed **+1**. The LFO *rate* is set NOT by step magnitude but by **two cascaded
  software reload dividers** — inner **0x4333** (reloaded from per-algo byte **0x418C**; coarse
  reload 0x40 @0x0AF1) and outer **0x4332** (reloaded from **0x418B**). 0x418B/0x418C come from
  the **RATE-knob handler @0x04F0** (`CP 0x10 / SUB 0x10 / CPL / INC A / INC A → 0x418B`) and the
  per-algorithm `LDIR` @0x05A3 (record+0x4C, 3 bytes → 0x418C/D/E).
- **Wrap** = `AND 7` on the high byte → 8-page / 0x800-byte window from base 0x0010.
- **Depth** = param **0x402D** low nibble (clamped to per-algo cap 0x41E4), scaled by the 8×16
  shift-add multiply **`sub_10d3h` @0x10D3** using depth word **0x418D/0x418E**.
- **Output** → the routine walks the per-algorithm modulation list at **(0x41E2)** (stride 5),
  applies the cached sample × depth, and stages `{target,value}` into the **0x40B0 de-zipper
  queue** (head ptr 0x40D0). The de-zipper **`sub_071dh`** (list head 0x41FA) / **`sub_0883h`**
  (head 0x4206) then converge each value toward target (−4/pass if bit7=0, −1 if bit7=1) and
  commit to the WCS via the RMW writer **`sub_0ecch`/`sub_0e59h`** (plane 6, above).
- **Paced by** the **foreground dispatcher** (`CALL 0x0AD2` @0x00EF every loop pass), self-rate-
  limited by the cascaded dividers — **NOT** the ISR. ISR 0x02D3 re-confirmed as a pure ÷8 BPM
  divider with no modulation role.
- **Entry gating:** `0x0AD2 LD A,(0x418A)/OR A/JP m` (per-algo LFO-enable) + `0x0AD9
  LD A,(0x402B)/AND 0x40/JP z` (user mod-enable, param 0x402B bit 6).

**Waveform caveat** (🟡 open): the dereferenced "table" base is 0x0010 with `H AND 7`, so it
reads low ROM/RAM 0x0010-0x07FF — which physically overlaps the U95 copyright banner/code bytes —
and 0x4337 is XOR/sign-toggled downstream (~0x0C14) as a direction bit. So this behaves as a
**triangle / up-down ramp generator** (the depth multiply, not a smooth amplitude LUT, shapes the
output), unless a per-algorithm setup relocates the table base before `sub_0ad2h` runs (needs a
trace of any writer of the 0x4335 *base* beyond the 0x06A0 init). A separate exponential rate→
period table at **0x0D3F** (indexed by `0x0CFA`) maps the RATE param to a period and is
complementary, not the phase index.

**Per-algorithm record table (corrects the "0x3FFE pointer" framing):** there is **no live
pointer at 0x3FFE**. `0x3FFE` is the **end boundary** of a **7-entry record table at 0x299A**,
stride **0x0333** (records IDs 0-6 at 0x299A/0x2CCD/0x3000/0x3333/0x3666/0x3999/0x3CCC; table ends
0x3FFF). Algorithm selected by **linear ID-scan `sub_0ab3h` @0x0AB3**; record base cached in RAM
**0x4185**. Record layout (0x333 bytes): `[0]`=algo ID · `+0x4C` (3B) rate words → 0x418C · `+0x51`
(11B) LFO/delay-range setup → 0x418F · `+0x5D` tagged modulation-list source · `+0x133` (0x80) WCS
coeff block · `+0x233` (0x80) plane block → WCS 0x8300 / RAM 0x4100. Param block roles:
**0x4000**=algo# · **0x402B bit6**=mod enable · **0x402C**=delay/size (feeds `sub_0953h` range
calc) · **0x402D**=LFO rate/depth (low nibble depth, bit7 direction).

*(Method note: resolved via an 8-agent verification+trace workflow — 2 adversarial U67 verifiers,
5 independent U95 trace lenses, 1 synthesis. One lens (forward-from-curve-tables) initially
concluded "no accumulator / host-side LFO" by searching only the curve-table read paths; it was
overruled by re-disassembly in synthesis, but its 0x0D3F rate→period finding stands.)*

---

## Open after Phase 2 (updated)

- ✅ **LFO phase accumulator** — `sub_0ad2h` @0x0AD2 (accumulator 0x4335, sample 0x4337). *(was ❓)*
- ✅ **U67 microword field map** — 7 control/opcode/routing planes (0-6) + banner (7); no resident
  offset/coeff value planes. *(was ❓)*
- ✅ **Coefficient WCS plane** — plane 6 (0x8300). *(was ❓ "exact WCS window decode", now largely pinned)*
- 🟡 **Fine sub-role split of U67 planes 0-6** — all control-domain; the per-plane → ARU-bit-field
  mapping (banks/sections/routing) is not crisply resolved.
- 🟡 **LFO waveform source** — confirm whether the 0x4335 base (0x0010, H&7) is an intentional
  triangle/ramp over low ROM or relocated per algorithm.
- ❓ **Literal PCM70-vs-PCM60 reverb-tap diff** — must be run **U95-WCS-source vs PCM60** (U67 has
  no taps); PCM70's delay topology assembles at runtime from the per-algorithm record blocks.

**Next:** **Phase 3 — 224XL** (Phase-0 integrity PASS, see roadmap §Phase 3 RESULTS).

---

### Artifacts
- `PCM70_U95_slave_disasm_org0.asm` — full z80dasm of the slave (origin 0, addresses = file offsets).
- `PCM70_phase0_analysis.py` — integrity / entropy / autocorrelation / string / table-scan scripts.
- `tools/pcm60_decode.py` — PCM60 Rosetta microword decoder (verified: program 0 = 60 taps, 68..27137).
- `tools/u67_planes.py`, `tools/u67_explore.py`, `tools/u95_wcs_source.py` — U67 plane field-map analysis.
