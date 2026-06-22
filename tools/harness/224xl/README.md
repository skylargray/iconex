# 224XL ARU core — desktop diff harness

Proves `libs/sgdsp/include/sgdsp/reverb/224xl.hpp` reproduces the Python
`tools/aru_datapath.py` reference integer-exact for CONCERT (static microcode).

## Regenerate goldens (Python 3 + numpy)

    python tools/gen_224xl_programs.py 0x01     # -> libs/.../reverb/224xl_programs.hpp
    python tools/export_golden_224.py 0x01      # -> tools/harness/224xl/golden/01_*

## Build + test (CMake)

    cd tools/harness/224xl
    cmake -S . -B build -DCMAKE_BUILD_TYPE=Release
    cmake --build build --config Release
    ctest --test-dir build -C Release --output-on-failure

- `mult_vectors_test` — multiplier/saturation primitives (Service-Manual coeff set).
- `diff_harness golden 01` — layer-1 decode parity + layer-2 arithmetic parity.
- `wav_ir_tool ir out.wav` — float-boundary impulse response for listening.

Note: under the first-cut arithmetic the CONCERT tank **sustains** rather than decays
(faithfully matching the Python reference). A cleanly decaying IR follows the deferred
`ArithProfile` tuning (result-register shift / coeff denominator) — see the design spec.

## Scope

Validated: C++ == Python reference (CONCERT static), multiplier vectors, builds.
Deferred (knobs/interfaces in place): hardware-anchored arithmetic (ArithProfile, governs
loop gain/decay), per-program FPC position base + true stereo L/R split, params/modulation
dynamic parity, all 20 programs, DPF/Seed2 wrappers. See the design spec for the full list.
