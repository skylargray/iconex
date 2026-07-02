# 224XL ARU core — desktop diff harness (RTL-parity flow, plan 024 F1d)

Proves `libs/sgdsp/include/sgdsp/reverb/224xl.hpp` (+ `224xl_booth.hpp`)
reproduces the Python pin-locked RTL engine `tools/aru_freerun22_rtl.py`
(class RTL22 — session-0022 coordinate system, traced fig-3.3/3.4 pipeline
alignment, complement-domain physical MAC law of sessions 0027/0028)
**bit-exactly**: per-frame CPU-domain outputs on all four channels over every
frame, plus the per-step phys trace {step, ACC, RES, DAB, R0..R3} on the first
3 frames of each case.

## Regenerate goldens (Python 3 + numpy; run from the repo root)

    python tools/export_golden_224xl_rtl.py     # -> tools/harness/224xl/golden_rtl/

Cases (stimulus is exported to `<case>_in.bin` and READ by the C++ harness —
never regenerated — so both sides consume identical bits):

- `d1zero` / `d1max` — the two D1 diagnostic images
  (`tools/session0022_probes/wcs_diag.json`), h1-only impulse amp 16000 at
  frame 50; nsamp = 50 + lag + 600 with lag 1 / 0x3FFF.
- `concert` — the settled CONCERT image
  (`tools/session0022_probes/wcs_settled_concert.json`), mono 0.30 s noise
  burst (default_rng(224), ±8000) then silence, nsamp = 66000 — deliberately
  crossing the 65536-frame CPC wrap.
- `sig6` — the diag-6 FPC-signature image (`wcs_diag.json["sig6"]`, L=97),
  zero input with the host latch parked at XREG_host = 0xFAAA (meta key
  `xreg_host`; the harness calls `setXregHost` after `loadProgram`): the
  program's SRC_XREG word unity-MACs the latch to WR-DA channel D (-1366
  every frame) — the XREG host-latch boundary golden.
- `booth_vectors.bin` — 4000 `raw3` gate-array vectors + 200 `backend20`
  sat-mux vectors (both clamp rails covered).

## Build + test (CMake; MSVC — see toolchain note)

    cd tools/harness/224xl
    cmake -S . -B build-rtl -G "Visual Studio 18 2026"
    cmake --build build-rtl --config Release
    ctest --test-dir build-rtl -C Release --output-on-failure

Toolchain note: the DaisyToolchain `g++` is an `arm-none-eabi` cross-compiler
(bare-metal ARM); its binaries cannot run on the Windows host, so the desktop
harness builds with MSVC (any host C++17 compiler works).

- `booth_vectors_test golden_rtl/booth_vectors.bin` — the gate-level comb
  array (NAND taps + 5-adder carry chain + 74194 shifter, owner-corrected
  tables) and the back-end adder + sat-mux, vector-exact vs the reference.
- `diff_harness golden_rtl [case ...]` — layer 1: program extraction parity
  (frameSteps()-1 == golden L); layer 2: all-frame 4-channel output equality +
  first-3-frame per-step trace equality. Nonzero exit on any mismatch.
- `wav_ir_tool ir|wav <wcs.bin> ...` — listening tool on the same core
  (mono-duplicated input h1=h2; WAV L = channel A, R = channel C). For ears,
  not for the gate.

## Scope

**Validated:** C++ == the pin-locked RTL engine, integer/bit-exact, on
D1 zero/max (impulse, both diag delay taps), settled CONCERT (noise burst +
34 s tail including the 65536-frame CPC wrap), and diag-6 sig6 (the XREG
host-latch boundary) — outputs every frame, phys state every step of the
traced frames; plus 4200 primitive vectors. The C++ walk includes the
complement-domain datapath (phys R/DM/RES/DAB/ACC), raw3 product-register
loads, backend20 sat-mux with clamp-into-ACC (#35), own-sign retirement, XFER
PP-bus capture `(sum>>3)&0xFFFF`, ZERO sync-clear, write-through operand
read, stereo RD-AD half alternation, WR-DA channel decode, the XREG
host->DAB complement bridge, and CPC-offset DMEM addressing.

**Not exercised by these goldens:** the WR-XREG readback latch
(`xregReadback()`, DSP->host direction) is ported 1:1 but no golden program
writes it; FPC float codec is not ported (the diff gate is the fixed-point
path). Params/modulation remain CPU-side (out of ARU scope).

**History:** everything this harness proved before 2026-07-02 (the
`golden/` directory, `aru_datapath.py` parity, `mult_vectors_test`,
`export_golden_224.py`, `gen_224xl_programs.py`, `224xl_programs.hpp`) is
pre-0022-era and OBSOLETE — decode, execution order, and arithmetic were all
superseded (sessions 0022/0025/0027). Those files stay on disk for the record
but are out of the build; `golden_rtl/` + `export_golden_224xl_rtl.py` is the
live flow.
