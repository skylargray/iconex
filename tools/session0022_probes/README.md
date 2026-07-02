# session-0022 probes + WCS caches

Rescued from the 2026-07-01 session scratchpad so later sessions don't re-boot/re-derive.
Context: `docs/sessions/0022 - the-wcs-coordinate-system-was-reversed-and-the-programs-are-valid.md`
and `docs/plans/021 - 224XL-RTL-arbiter-and-first-tail.md`.

- `wcs_cache.json` — built WCS images (mainloop snapshot) for the 13 building program ids
  {1..6,8,10,12,16,17,18,20}; key = id, `wcs` = 512-byte hex. CONCERT = "1".
- `wcs_run_concert.json` — CONCERT RUN-state image (40M ticks past mainloop; LFO mid-phase).
- `e1_sweep.py` — rebuilds the cache (boots every id via the 0x8160 selector patch) + the
  (type × polarity × window) validity scan that proved the 0022 coordinate system (13/13).
- `e2_census.py` — per-program I/O census + full program decode (`-t 2 -b 0 --full 1`).
- `e3_concert.py` — metric-gated first-light render (impulse + burst, all channels).
- `e3d_tank.py` — tank probe. ⚠ its DM_rms column is RMS-over-touched-cells; use ENERGY = RMS²·N
  (the "tank drains" misread came from this — see plan 021 dead-end #11).
- `e3e_dataflow.py` — frame-level dataflow microscope (per-step probe rows).
- `e3l_flow.py` — taint tracer: logs significant products with operand provenance; the instrument
  that mapped the severed register handoffs (plan 021 §3).

Scripts reference `wcs_cache.json` relative to their own directory and the tools dir absolutely —
they run as-is from here: `python e2_census.py -t 2 -b 0`.

## Session-0023 additions (plan-021 execution — the RTL arbiter; engine = `tools/aru_freerun22_rtl.py`)

- `b3_rtl_taint.py` — B3 taint/provenance on the RTL engine: both handoffs CONNECT.
- `b45_cell_and_tank.py` — B4 (in-place cells = bounded recursive nodes, pole = −(h−pairC)/32) +
  B5 (tank ENERGY decays smoothly through the 0.7-s bulldozer; the parked trail was never in the loop).
- `c1_concert_render_rtl.py` — the metric-gated first-tail render (boot + run images):
  **WET-PASS/DENSE ×4 ch** on the burst; impulse verdicts read the residue floor (see c3).
- `c2_race_falsification.py` — the clear-owner race: no-lag (owner = w_n) renders EXACTLY ZERO;
  the lag owner (= the capture's owner, w_{n−1}) is the machine.
- `c3_floor_subtracted_ir.py` — subtract the zero-input render (the ±2.5-LSB deterministic Booth
  residue limit cycle) to expose the true linear response; writes ×64 diff WAVs.
- `c4_csign_and_prot.py` — CSIGN polarity re-derived ON this alignment (both stable — the old
  dead↔rail bimodality was a behavioral-frame artifact); PROT census (asserted ~everywhere = inactive).
- `c5_rt60.py` — floor-subtracted RT60: boot 1.83–1.91 s, run-state 1.37–1.42 s (all 4 channels).
- `d0_all_programs.py` — all 13 factory programs through engine + metrics (cross-program oracle).
- `idiom_check.py` (scratchpad-born, kept in session log) — the ZERO/XFER idiom scan that surfaced
  the row-L idles (the L+1 frame) and the pairA-free h-word compilation rule.
