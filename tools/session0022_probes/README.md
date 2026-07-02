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
