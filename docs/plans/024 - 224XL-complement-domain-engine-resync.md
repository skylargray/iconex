# 024 — 224XL: the complement-domain engine re-sync, the remaining signature tables, and dynamics

**Status:** READY TO EXECUTE (written 2026-07-02 at the close of session 0027).
**Read first:** `docs/sessions/0027 - the-complement-domain-and-the-aru-pin-lock.md` (the whole
thing — the complement domain reframes the arithmetic), then 0026/0025/0024 as needed. The engine
of record is still **`tools/aru_freerun22_rtl.py`** — but 0027 proved its MAC value model sits
±1-2 LSB off the pin-locked physical law on most captures (`e5_engine_vs_physical.py`). Trust
0027 > 0026 > 0025 > 0024 > 0022 > everything older.

**Mission.** Session 0027 locked the physical datapath at manufacturer-measured pins (ARU
signature tables 1467/1469; feedback table 710/710) and discovered the law it computes by:
**the DAB carries ACTIVE-LOW values, and in that complement domain the exactly-traced wiring
reproduces the E83 goldens by PURE TRUNCATION** — the '+4 round', '+3 dual-rail', and '-M-1'
were CPU-domain bookkeeping. The engine must now be re-expressed in that law (F1 — everything
else this session is gated on it or independent of it), then the remaining §5.7 tables, the
stop-decay dynamics, and the E3 leftovers.

---

## 1. Ground truth (established 0027; do not re-derive)

### 1.1 The physical MAC law (per-pin locked; `e1_aru_signatures.py` = the oracle)
- Domain: every DAB value is the COMPLEMENT of its CPU-domain meaning (XREG bridge U39/U41
  carries `DATA0-7/` levels straight onto the DAB, §5.6; the readback pair U38/U40 complements
  back; the FPC boundary likewise). The regfile, shifter, Booth array, and delay memory all
  carry phys (complemented) values.
- Back-end per accumulate: `B = PR ^ rail`, `rail = cs_eff` (i.e. inv(CSIGN/), the aru_U2
  inverters), `cin = 1 - rail` (traced), `sum = (ACC + B + cin) & 0xFFFFF`;
  `SAT = sum19 ^ sum18`; on SAT the sat-mux clamp (`PP19=PP18=topB, PP0-17=~topB`,
  `topB = xorB bit19`) **feeds BOTH the result path AND the accumulator D inputs** (the '163
  loads the clamp — pinned by the diag-3 tail; the engine's wrap-only ACC is registry #35).
- Capture: `RES = (PP >> 3) & 0xFFFF` — a pure bit tap of PP3..18, NO rounding hardware.
  PR = `comb_array` output loaded raw (no complement). '163 clear = 0. NO +3-dual term
  in the bits (registry #30 — `aru_booth.multiply`'s corrections are value-level identities).
- Sign schedule unchanged (own-sign at every pp; JK window as 0023/0025). PP-bus capture
  unchanged (0024). Frame/fs unchanged (L+1; CONCERT 32,508 Hz).
- Reference implementations: `e1c` Emitter (full, pin-emitting) and `e5_engine_vs_physical.Phys`
  (minimal). The divergence census: lone negative unity −2 LSB; odd cmags ±1; ~70% of random
  frames differ somewhere. Every headline oracle (POST/D1/D3/RT60) is blind to it.

### 1.2 Session-0027 tools you will reuse
- `e1_aru_signatures.py`: sig scorer — steady state in 33 frames, ~2 min full run; the champion
  variant is hardcoded-scanned; 1467/1469 must SURVIVE the re-sync unchanged.
- `e2_live_cosim.py`: the true co-sim (flag 0x3C14 + 62 ticks/frame; trajectory capture-then-
  render; `--chorus HEX`). Headlines: LF 3.27/3.25, mid 2.28/2.23, bb 2.68/2.64.
- Key harness (`e4_variations.SerialIO/send_key`): modal UI — 0x21/0x22/0x26 arm PGM/BANK/VAR
  select; number keys 1-8 = 0x2C/0x30/0x34/0x38/0x3C/0x2D/0x31/0x35; **0x3E = PAGE (sets the
  display page AND 0x3C34)**; param-select keys 0x23/0x27/0x2B/0x2F/0x33/0x37 display the
  current value WITHOUT touching it; 0x2E DynDecay prompt; 0x25 register recall; 0x3A 2nd fn.
- Display: the value formatter renders into **0x3F4F..** (parse `c & 0x7F`); soft takeover
  (registry #32): ascend past the preset to pick up, then move to the target.
- Caches: `display_map.json` (page-1 calibration solid; pages 2-5 were rendered with page-1
  formatters — redo AFTER pressing 0x3E), `key_map.json`, `program_names.json` (ids BIT-CODED:
  0x03 SMALL PLATE, 0x04 ROOM...), `variation_params.json` (V1-V7 blocks + settled WCS +
  toggles; V6/V7 have DynDecay ON), `e2_cosim_*.json`, `e3b_states.json`.

## 2. Dead-end / discipline registry
Plan 023 §2 (#13-28) stands. 0027 additions (session doc §8): **#29** CPU-domain bit back-end
DEAD; **#30** '+4'/'+3dual'/'-M-1' as hardware DISSOLVED; **#31** RTL22 ≠ physical at sub-LSB
(the re-sync target); **#32** soft takeover; **#33** 0x3C34 = apply page only; **#34** ids
bit-coded; **#35** ACC clamp-feed erratum.

---

## 3. Phase F1 — THE ENGINE RE-SYNC ★ (everything audio-numbered re-anchors here)

F1a. **Re-express the RTL22 MAC core in the physical law.** Keep the CPU-domain API
     (`run_sample(rows, audio_in)` returning CPU-domain ints) with an internal phys core:
     complement at the boundaries (RD-AD injects `~x`; WR-DA emits `s16(~dab)`; XREG read
     drives the phys latch value; DMEM/regfile/RES/DAB state all phys). Port the `Phys` walk
     (e5) into RTL22.step 1:1 — sums via `backend()` incl. the SAT clamp into ACC. DO NOT keep
     product20/res_from_acc in the hot path (they are now value-level history).
F1b. **Re-derive the self-tests from the physical law** — the closed forms CHANGE at sub-LSB
     (the ±3-residue idioms, the comb recurrences, `_test_csign_split`'s term algebra). Derive
     each from the phys recursion (never patch expected values to match the code — recompute
     them by hand/sympathetic script from the law in §1.1). Keep the falsified-variant pins
     (#23) working.
F1c. **The full oracle battery, in order, each a hard gate:**
     1. `aru_post` E83 goldens 20/20 (unchanged path — but re-run);  POST E32/E40/E83/E91 green.
     2. D1 diag oracles 16/16 (`d1_diag_oracles.py`) — unity must stay EXACT ±0.
     3. D3 T&C signatures 374/376 (`d3_signatures.py`).
     4. **E1c ARU signatures 1467/1469** — rebase the e1c Emitter to CALL the new engine core
        (or assert bit-equality per step against it across the steady frame); the score must
        not move.
     5. `e5_engine_vs_physical.py` → **ZERO differing frames** (the regression's purpose).
     6. Audio: D2b settled + `e2_live_cosim` re-run — expect headline RT60s within the
        LFO-phase noise of 0027's numbers (bb 2.6-2.7). The DC floor WILL change (the idle
        limit cycle is sub-LSB-shaped) — re-measure and re-note the floor signature.
        **If any headline verdict moves materially (>0.15 s band RT60), STOP — that would mean
        the divergence was NOT sub-LSB-confined; diagnose before proceeding.**
F1d. **Downstream re-syncs:** `aru_whole.py`, the C++ scaffold (`libs/.../reverb/224xl.hpp` +
     diff harness) — port the phys core verbatim; diff-harness vs the Python engine on the
     D1 programs + CONCERT settled frames.

## 4. Phase F2 — the remaining §5.7 signature tables (E1d holdover)

F2a. **DMEM table** (SM setup: "Lift U65 pin 13, jumper to U65 pin 1"; START=STOP=CPC MSB
     (U65.8), CLOCK=RESET/ → 1 clock per FRAME, window = 32,768 frames = the CPC-MSB half
     period; +5V ref `826P` @ N=4096?? — sig224 calibrates 826P at N=4096: RECONCILE the
     window length BEFORE scoring, E1b-style: the lift-jumper rewires the counter — derive
     what the modified CPC period is and predict N first). Streams: DMEM address/CPC/OFST//
     DIN/DOUT/strobe pins per frame under diag-3 (the same bench state; pin map netlist §5).
F2b. **FPC table** (diag-6): capture the diag-6 WCS via the 0x0330 menu-handler table
     (d1a direct-call route; menu item 6 = FPC SIGNAT, display E0F); SM setup lifts the SAR
     U26.11 to +5V (the A/D never completes — deterministic codes). Model the FPC codec pins
     (float↔fixed, netlist/FPC pinouts txt) at CLOCK=FPCCLK. This also pins the A/D idle
     pattern (useful for the AD_CONST question in e1c).
F2c. On completion: update the pinout txts / netlist §5/FPC per-pin as done for the ARU
     (owner-verify protocol for any discrepancy).

## 5. Phase F3 — stop decays (E2d holdover; the last documented dynamic)

F3a. Disassemble around **0x83B4** (the DynDecay gate) and **0x83D1**: find what the
     input-level detector READS (XREG readback of a WCS-written level word? an ARU port?).
     The NVS-ROM code is not in `_dis_SBC*.txt` — disassemble 0x8000+ on demand
     (`tools/dis224.py`/`disrange.py`).
F3b. If the source is a DSP-written value the co-sim can supply: extend `e2_live_cosim` to
     feed it (the co-sim currently has no audio→8080 path — this adds the ONE documented
     feedback edge); drive burst-then-silence on **V6/V7** (captured, DynDecay ON) and verify
     the running↔stopped coefficient switch (w44-family 9↔22). V1's documented stops 3.0/3.0
     vs running 3.0/2.0 = the mid-band observable.
F3c. If un-modelable, document why + what bench evidence would settle it.

## 6. Phase F4 — E3 clean-ups (all cheap, all keyed)

F4a. **Pages 2-5 display calibration**: press 0x3E (PAGE) between sweeps so the DISPLAY page
     matches the apply page; rerun `e3_display_calibration` per page (ascend-then-descend);
     complete `display_map.json` (Chorus/HFBW/Diffusion/Definition/stops/PE/Size/Gate
     formatters). Note B2/B3 banks label slider 5 "ATT" — bank-dependent legends.
F4b. **E3b redo with clean observables:** mid-lo with BOTH LF and Mid at 0.6 s (kills the
     crossover bleed); mid-hi 70 s under the CO-SIM (near-unity loops need live modulation);
     PDL arrival via main-peak (largest |peak|) detection, chC, vs the displayed value.
F4c. **The PDL range question:** the formatter tracks to 862 ms while ch.4 documents 216 max —
     check the manual's actual Table 4.2 row (216 could be another program's column) and name
     the LARC physical-scale byte for PDL. Cheap: the param-select key 0x37 displays the
     preset; the display map has the curve.
F4d. D2c re-score with `program_names.json` ids (correct name column; drop the id-3 'invalid'
     row — SMALL PLATE exists; check ROOM vs its documented 1.4 s under E83+settled) and
     extend to spec-scoring (Room V1 1.4; Plate V2 0.6/1.8 @ XOV 170; CD plates 1.8).

## 7. Phase F5 — consolidation

- `reverb_metrics`: first-class floor-subtraction mode (burst-minus-silence pairs); re-run
  its selftest battery after.
- Session doc 0028, memory index, this plan's banner. Keep the docs updated inline
  (system-architecture / technical-reference / timing-spec were brought current in 0027).

## 8. Verification rules (unchanged + additions)

- Defaults are the oracle; floor-subtract everything; per-band at 720 Hz; Schroeder T30 on
  truncated tails; WAVs on disk; POST green at every phase.
- **F1's battery order is mandatory** — no downstream render is quotable until e5 reads zero.
- Predictions before reads (F2a's DMEM window length is the built-in falsifier this time).
- Signature mismatches name their net; single-glyph table errata need a same-net sister pin
  before being called errata.
- Every probe's final message states which registry entry it would re-open.

## 9. Facts that will save time

- Boot ≈ 40 s; settle 6M ticks; `probe_run.run_ticks` for ALL post-boot running (HLT trap).
- The e1c fixed point: 33 frames; full 16-variant scan ≈ 2 min; single-variant ≈ 15 s.
- Co-sim: 211k frames ≈ 5 min capture + 2×45 s renders.
- Diag-3 bench state: XREG = 0x607F; regfile init R0-R2 = ~AAAA/~9999/~C787 (phys) via the
  pump; every diag-3 row writes R3; rows 25-29 carry no ZERO (the tail saturation window).
- Display parse: `bytes(m.memory[0x3F4F:0x3F68])`, chars `& 0x7F`; value field overwrites
  in place at the buffer start on subsequent moves of the same slider.
- Variation switch: send 0x26 then the number key, settle 6M ticks; V1 restore = 0x26,0x2C.
- The id patch (0x8160) does NOT reach diag programs or variations; use the keys.
- `renders/` is gitignored; caches are committed.

## 10. Artifacts

- Modified: `aru_freerun22_rtl.py` (the phys core), self-tests re-derived; `aru_whole.py`;
  C++ scaffold; `reverb_metrics.py` (floor mode).
- New: `f2_dmem_signatures.py`, `f2_fpc_signatures.py` (+ `wcs_diag6.json`),
  `f3_stop_decay.py`, page-2-5 additions to `display_map.json`, `d2c` re-score.
- Records: session doc 0028; memory update; this plan's execution banner.
