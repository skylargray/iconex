# 224XL Bit-exact ARU Core + Diff Harness (Scaffold) — Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Scaffold a header-only C++17 Lexicon 224XL ARU reverb core (`224xl.hpp`) and a desktop diff harness that proves the core reproduces the Python `aru_datapath.py` reference integer-exact for CONCERT (static), with the Service-Manual multiplier coefficients/saturation anchored.

**Architecture:** One header-only class `sgdsp::reverb::Lexicon224XLCore` with an integer ARU datapath (16-bit register file, int64 accumulator, 64K DMEM ring, 128-step microprogram with NOPs skipped) and a thin float boundary. The bit-exact reference is the Python model (the Z80 emulator does not compute audio); Python tools export on-disk goldens (WCS image + decoded fields + per-step/per-sample trace) that three CMake-built C++ tools diff against. All not-yet-resolved arithmetic lives behind a named `ArithProfile` so tuning is a one-line change.

**Tech Stack:** C++17 (header-only, MSVC/GCC/Clang desktop), CMake, Python 3 + numpy (existing `tools/`), the sgdsp library at `libs/sgdsp/include/sgdsp/`.

**Reference spec:** `docs/superpowers/specs/2026-06-22-224xl-aru-core-and-diff-harness-design.md`. Read it before starting.

**Branch:** Work happens on `224xl-aru-core-scaffold` (already created).

---

## Critical correctness rules (apply in every relevant task)

These were derived from the actual `tools/aru_datapath.py` source. Violating any breaks integer parity:

1. **Floor division, not truncation.** The reference computes `(R[ra] * coeff) // 128` (Python floor division, toward −∞). In C++ use **arithmetic right shift `>> 7`** on a signed `int64_t` — it floors toward −∞ for negatives and matches Python `//`. Never use `/ 128` (C++ integer division truncates toward zero and diverges on negative products).
2. **Skip NOP steps.** A NOP step is `lane2 == 0xFF && lane3 == 0xFF`. If executed it decodes to `coeff = -127` (because `l3=0xFF` → mag `0x7F`, sign set) and would corrupt the accumulator. The reference removes NOPs from the program list; the core must do the same at load time.
3. **Saturation is `sat16`** to `[-32768, 32767]` applied after each accumulate AND on the result-register load — exactly as the reference.
4. **Input injection is additive at the first active step.** The reference replaces `dab` with `imp` only at sample 0, first active step. Because DMEM and RES are zero at sample 0, an *additive* model (`dab += in` at the first active step every sample, driven with `in=imp` at sample 0 and `in=0` afterward) is identically equal to the reference and also generalizes to continuous input.
5. **RA is `(ctl >> 4) & 3`** (the datapath-validated `b5<<1 | b4`). Hardcode it; do not parameterize.

---

## File structure

| File | New/Mod | Responsibility |
|---|---|---|
| `tools/aru_datapath.py` | Modify (additive) | Add `run_trace()` beside `run()`; existing API untouched. |
| `tools/test_run_trace.py` | Create | Pytest-free assert script: `run_trace` esum == `run` esum (non-breaking proof). |
| `tools/gen_224xl_programs.py` | Create | Boot firmware, emit generated C++ table header. |
| `libs/sgdsp/include/sgdsp/reverb/224xl_programs.hpp` | Create (generated) | CONCERT WCS image + metadata, `#include`-able. |
| `tools/export_golden_224.py` | Create | Write `golden/<id>_{meta.json,wcs.bin,fields.json,esum.bin,steps.bin}`. |
| `libs/sgdsp/include/sgdsp/reverb/224xl.hpp` | Create | The header-only ARU core. |
| `tools/harness/224xl/CMakeLists.txt` | Create | Build the three tools. |
| `tools/harness/224xl/golden_io.hpp` | Create | Shared golden-file readers (used by diff_harness). |
| `tools/harness/224xl/mult_vectors_test.cpp` | Create | Multiplier/saturation unit tests. |
| `tools/harness/224xl/diff_harness.cpp` | Create | Layer-1 decode parity + layer-2 arithmetic parity. |
| `tools/harness/224xl/wav_ir_tool.cpp` | Create | WAV in→out + impulse/IR dump. |
| `tools/harness/224xl/golden/` | Create (gitignored) | Exported goldens (build artifact). |

---

## Task 1: Add `run_trace()` to the Python reference (additive)

**Files:**
- Modify: `tools/aru_datapath.py` (append a new function; do not touch `run`/`load_microcode`/`sat16`)
- Test: `tools/test_run_trace.py`

- [ ] **Step 1: Write the failing test**

Create `tools/test_run_trace.py`:

```python
#!/usr/bin/env python3
"""Verify run_trace() reproduces run()'s per-sample energy exactly (non-breaking)."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import aru_datapath as A

def main():
    prog = A.load_microcode(0x01)
    ra_pick = lambda st: (st['b5'] << 1) | st['b4']
    base = A.run(prog, ra_pick, nsamp=300)
    esum, steps = A.run_trace(prog, ra_pick, nsamp=300, trace_window=8)
    assert esum == base, "run_trace esum diverges from run()"
    # trace_window=8 samples, each with len(prog) active steps, 8 fields per record
    assert len(steps) == 8 * len(prog), f"unexpected step count {len(steps)}"
    assert all(len(r) == 8 for r in steps), "each step record must have 8 fields"
    # res field is sentinel (INT64_MIN) on non-XFER steps, a valid 16-bit value on XFER
    SENT = -(1 << 63)
    assert any(r[7] != SENT for r in steps), "expected at least one XFER step in trace"
    print(f"OK: run_trace matches run() over 300 samples; {len(steps)} step records")

if __name__ == '__main__':
    main()
```

- [ ] **Step 2: Run test to verify it fails**

Run: `python tools/test_run_trace.py`
Expected: FAIL with `AttributeError: module 'aru_datapath' has no attribute 'run_trace'`

- [ ] **Step 3: Implement `run_trace`**

Append to `tools/aru_datapath.py` (after `decay_metric`, before `if __name__`):

```python
def run_trace(prog, ra_pick, nsamp=4000, imp=20000, trace_window=64):
    """Instrumented twin of run(). Returns (esum_list, steps).

    esum_list[n]  : per-sample output energy, identical to run().
    steps         : flat list of per-step probe tuples for samples n < trace_window,
                    each = (n, s, addr, dab, racc_in, prod, acc, res) where
                    res = the RES value after this step if XFER else INT64_MIN sentinel.
    Mirrors run() bit-for-bit (floor division, sat16, additive impulse at first active step).
    """
    SENT = -(1 << 63)
    R = [0, 0, 0, 0]
    ACC = 0
    RES = 0
    DM = [0] * (DMASK + 1)
    pos = 0
    esum_list = []
    steps = []
    for n in range(nsamp):
        pos = (pos + 1) & DMASK
        esum = 0
        for st in prog:
            addr = (pos - st['offset']) & DMASK
            if st['XFER']:
                DM[addr] = RES
                dab = RES
            else:
                dab = DM[addr]
            if n == 0 and st is prog[0]:
                dab = imp
            R[st['WA']] = dab
            ra = ra_pick(st)
            racc_in = R[ra]
            if st['ZERO']:
                ACC = 0
            prod = (racc_in * st['coeff']) // 128
            ACC = sat16(ACC + prod)
            if st['XFER']:
                RES = sat16(ACC)
                esum += abs(RES)
                res_val = RES
            else:
                res_val = SENT
            if n < trace_window:
                steps.append((n, st['s'], addr, dab, racc_in, prod, ACC, res_val))
        esum_list.append(esum)
    return esum_list, steps
```

- [ ] **Step 4: Run test to verify it passes**

Run: `python tools/test_run_trace.py`
Expected: `OK: run_trace matches run() over 300 samples; <N> step records`

- [ ] **Step 5: Commit**

```bash
git add tools/aru_datapath.py tools/test_run_trace.py
git commit -m "224XL: add non-breaking run_trace() probe twin to aru_datapath"
```

---

## Task 2: Generate the program table header

**Files:**
- Create: `tools/gen_224xl_programs.py`
- Create (generated): `libs/sgdsp/include/sgdsp/reverb/224xl_programs.hpp`

- [ ] **Step 1: Write the generator**

Create `tools/gen_224xl_programs.py`:

```python
#!/usr/bin/env python3
"""Generate libs/sgdsp/include/sgdsp/reverb/224xl_programs.hpp from firmware.

Boots the v8.2.1 firmware for each requested program id, reads the 128-step WCS
image (mem[0x4000:0x4200]), and emits a header embedding the raw image + metadata.
Single source of truth: the C++ core and the Python reference read identical bytes.

Usage: python tools/gen_224xl_programs.py [id_hex ...]   (default: 0x01 CONCERT)
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import boot_xl as B

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(REPO, "libs", "sgdsp", "include", "sgdsp", "reverb", "224xl_programs.hpp")

NAMES = {0x01: "CONCERT_HALL"}  # extend as more programs are brought up


def wcs_image(power_up_id):
    cpu, mem, *_ = B.boot(power_up_id=power_up_id, verbose=False)
    return bytes(mem[0x4000:0x4200])  # 512 bytes


def emit(ids):
    progs = [(i, wcs_image(i)) for i in ids]
    lines = []
    lines.append("#pragma once")
    lines.append("// =============================================================================")
    lines.append("// sgdsp - Lexicon 224XL program WCS tables (GENERATED - do not edit by hand)")
    lines.append("// =============================================================================")
    lines.append("// Source: tools/gen_224xl_programs.py, firmware ROMs/Lexicon 224/224XL v8_21.")
    lines.append("// Each image is the 128-step microprogram (4 active-low bytes per step).")
    lines.append("")
    lines.append("#include <cstdint>")
    lines.append("")
    lines.append("namespace sgdsp::reverb::programs {")
    lines.append("")
    for pid, img in progs:
        assert len(img) == 512, f"bad image length {len(img)}"
        name = NAMES.get(pid, f"PROGRAM_{pid:02X}")
        lines.append(f"// power_up_id = 0x{pid:02X} ({name})")
        lines.append(f"static constexpr uint8_t k{name}_WCS[512] = {{")
        for row in range(0, 512, 16):
            chunk = ", ".join(f"0x{b:02X}" for b in img[row:row+16])
            lines.append(f"    {chunk},")
        lines.append("};")
        lines.append(f"static constexpr uint8_t k{name}_ID = 0x{pid:02X};")
        lines.append("")
    lines.append("}  // namespace sgdsp::reverb::programs")
    lines.append("")
    with open(OUT, "w", newline="\n") as f:
        f.write("\n".join(lines))
    print(f"wrote {OUT} ({len(progs)} program(s))")


if __name__ == '__main__':
    ids = [int(a, 16) for a in sys.argv[1:]] or [0x01]
    emit(ids)
```

- [ ] **Step 2: Run the generator**

Run: `python tools/gen_224xl_programs.py 0x01`
Expected: `wrote .../224xl_programs.hpp (1 program(s))`

- [ ] **Step 3: Verify the generated header is well-formed**

Run: `python -c "p=open('libs/sgdsp/include/sgdsp/reverb/224xl_programs.hpp').read(); assert 'kCONCERT_HALL_WCS[512]' in p; assert p.count('0x')>=512; print('header OK')"`
Expected: `header OK`

- [ ] **Step 4: Commit**

```bash
git add tools/gen_224xl_programs.py libs/sgdsp/include/sgdsp/reverb/224xl_programs.hpp
git commit -m "224XL: program-table generator + generated CONCERT WCS header"
```

---

## Task 3: Export golden files for the harness

**Files:**
- Create: `tools/export_golden_224.py`
- Create (output, gitignored): `tools/harness/224xl/golden/01_*`

- [ ] **Step 1: Add a .gitignore for the golden artifacts**

Create `tools/harness/224xl/golden/.gitignore`:

```
# Generated golden artifacts (reproducible via tools/export_golden_224.py)
*.bin
*.json
```

- [ ] **Step 2: Write the exporter**

Create `tools/export_golden_224.py`:

```python
#!/usr/bin/env python3
"""Export bit-exact golden artifacts for the C++ diff harness.

For each program id writes, under tools/harness/224xl/golden/:
  <id>_meta.json  - {power_up_id, n_active, nsamp, trace_window, imp}
  <id>_wcs.bin    - the raw 512-byte WCS image
  <id>_fields.json- decoded active-step fields (layer-1 parity reference)
  <id>_esum.bin   - nsamp x int64 LE per-sample energy (layer-2 parity)
  <id>_steps.bin  - trace_window x n_active x 8 int64 LE probe records (layer-2)

Usage: python tools/export_golden_224.py [id_hex ...]   (default 0x01)
"""
import sys, os, json, struct
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import boot_xl as B
import aru_datapath as A

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
GOLD = os.path.join(REPO, "tools", "harness", "224xl", "golden")
RA_PICK = lambda st: (st['b5'] << 1) | st['b4']
NSAMP = 4000
TRACE_WINDOW = 64
IMP = 20000


def export(power_up_id):
    os.makedirs(GOLD, exist_ok=True)
    tag = f"{power_up_id:02x}"
    cpu, mem, *_ = B.boot(power_up_id=power_up_id, verbose=False)
    img = bytes(mem[0x4000:0x4200])
    prog = A.load_microcode(power_up_id)
    esum, steps = A.run_trace(prog, RA_PICK, nsamp=NSAMP, imp=IMP, trace_window=TRACE_WINDOW)

    with open(os.path.join(GOLD, f"{tag}_wcs.bin"), "wb") as f:
        f.write(img)

    fields = [dict(s=p['s'], offset=p['offset'], coeff=p['coeff'],
                   ZERO=p['ZERO'], b3=p['b3'], XFER=p['XFER'], WA=p['WA'],
                   RA=(p['b5'] << 1) | p['b4']) for p in prog]
    with open(os.path.join(GOLD, f"{tag}_fields.json"), "w") as f:
        json.dump(fields, f)

    with open(os.path.join(GOLD, f"{tag}_esum.bin"), "wb") as f:
        f.write(struct.pack(f"<{len(esum)}q", *esum))

    with open(os.path.join(GOLD, f"{tag}_steps.bin"), "wb") as f:
        for rec in steps:                       # rec = 8-tuple of ints
            f.write(struct.pack("<8q", *rec))

    meta = dict(power_up_id=power_up_id, n_active=len(prog),
                nsamp=NSAMP, trace_window=TRACE_WINDOW, imp=IMP)
    with open(os.path.join(GOLD, f"{tag}_meta.json"), "w") as f:
        json.dump(meta, f)
    print(f"exported golden for 0x{tag}: {len(prog)} active steps, {NSAMP} samples")


if __name__ == '__main__':
    ids = [int(a, 16) for a in sys.argv[1:]] or [0x01]
    for i in ids:
        export(i)
```

- [ ] **Step 3: Run the exporter**

Run: `python tools/export_golden_224.py 0x01`
Expected: `exported golden for 0x01: <N> active steps, 4000 samples`

- [ ] **Step 4: Verify the artifacts round-trip**

Run:
```bash
python -c "import json,struct,os; g='tools/harness/224xl/golden'; m=json.load(open(g+'/01_meta.json')); n=m['n_active']; assert os.path.getsize(g+'/01_wcs.bin')==512; assert os.path.getsize(g+'/01_esum.bin')==m['nsamp']*8; assert os.path.getsize(g+'/01_steps.bin')==m['trace_window']*n*8*8; print('golden OK', m)"
```
Expected: `golden OK {...}`

- [ ] **Step 5: Commit**

```bash
git add tools/export_golden_224.py tools/harness/224xl/golden/.gitignore
git commit -m "224XL: golden exporter (wcs/fields/esum/steps) for the diff harness"
```

---

## Task 4: Core header — skeleton, types, and arithmetic primitives

**Files:**
- Create: `libs/sgdsp/include/sgdsp/reverb/224xl.hpp`

This task builds the file up to (and including) the arithmetic primitives that Task 5 tests. The full datapath comes in Task 6.

- [ ] **Step 1: Create the header skeleton with types, ArithProfile, and primitives**

Create `libs/sgdsp/include/sgdsp/reverb/224xl.hpp`:

```cpp
#pragma once
// =============================================================================
// sgdsp - Lexicon224XL - bit-exact 224XL ARU reverb reconstruction (integer)
// =============================================================================
// Reproduces the discrete-ARU datapath of the Lexicon 224XL: a 128-step WCS
// microprogram executed once per output sample over a 64K-word circular delay
// memory (DMEM), a 4x16-bit register file, a saturating multiply-accumulate, and
// a 16-bit result register. The reverb tank lives in DMEM + register feedback.
//
// The bit-exact reference is the Python model tools/aru_datapath.py (the 224XL's
// Z80 SBC builds/modulates microcode but does not compute audio). This core is
// authored to match that reference integer-exact; arithmetic details still being
// resolved (tech-ref 4/10) are isolated in ArithProfile so tuning is one line.
//
// Float appears ONLY at the I/O boundary. Everything between floatToAru and
// aruToFloat is integer. See docs/reference/224/224XL_technical_reference.md and
// docs/superpowers/specs/2026-06-22-224xl-aru-core-and-diff-harness-design.md.

#include "../core/types.hpp"       // Sample, SampleRate
#include "../core/platform.hpp"    // SGDSP_INLINE, SGDSP_NOINLINE, SGDSP_ASSERT
#include <cstdint>
#include <array>

namespace sgdsp::reverb
{
using namespace core;

// 16-bit signed ARU word carried in int32 for headroom; accumulator carried in
// int64. DMEM is a hardware-fixed 64K ring (mask 0xFFFF).
using AruWord  = int32_t;
using AruAccum = int64_t;

// ---- OPEN-arithmetic profile (tech-ref 4/10). First-cut values reproduce the
// current aru_datapath.py reference exactly. Move toward hardware by editing here. ----
struct ArithProfile
{
    static constexpr int      kCoeffShift = 7;        // the "/128" denominator (arithmetic >>)
    static constexpr AruAccum kSatMax     = 32767;    // sat16 high rail (reference uses 16-bit sat)
    static constexpr AruAccum kSatMin     = -32768;   // sat16 low rail
    // Hardware targets, NOT yet applied (enabled when matching hardware, not the
    // current reference): 20-bit accumulator, 2-LSB coeff packing, 20->16 result
    // shift, the operand20 = sign_extend(x,17)<<3 alignment.
};

// Saturate to the 16-bit result/accumulator rails (reference sat16).
SGDSP_INLINE AruAccum aruSat16(AruAccum x) noexcept
{
    if (x > ArithProfile::kSatMax) return ArithProfile::kSatMax;
    if (x < ArithProfile::kSatMin) return ArithProfile::kSatMin;
    return x;
}

// One multiply-accumulate step: acc + ((x * coeff) >> 7), saturated.
// Uses arithmetic right shift (floor toward -inf) to match Python `(x*coeff)//128`.
// NOTE: C++20 guarantees arithmetic shift on signed; on MSVC/GCC/Clang it already
// holds in C++17. Do NOT replace with `/ 128` (truncates toward zero on negatives).
SGDSP_INLINE AruAccum aruMac(AruAccum acc, AruWord x, int coeff) noexcept
{
    const AruAccum prod = (static_cast<AruAccum>(x) * coeff) >> ArithProfile::kCoeffShift;
    return aruSat16(acc + prod);
}

} // namespace sgdsp::reverb
```

- [ ] **Step 2: Sanity-compile the header standalone**

Run (from repo root):
```bash
echo "#include \"sgdsp/reverb/224xl.hpp\"
int main(){ return (int)sgdsp::reverb::aruMac(0, 100, 64); }" > /tmp/c224_compile.cpp
g++ -std=c++17 -I libs/sgdsp/include /tmp/c224_compile.cpp -o /tmp/c224_compile && /tmp/c224_compile; echo "exit=$?"
```
Expected: compiles; `exit=50` (100*64>>7 = 6400>>7 = 50). On Windows without g++, this is verified in Task 5 via CMake instead.

- [ ] **Step 3: Commit**

```bash
git add libs/sgdsp/include/sgdsp/reverb/224xl.hpp
git commit -m "224XL: core header skeleton - types, ArithProfile, MAC/sat primitives"
```

---

## Task 5: CMake + multiplier/saturation unit tests

**Files:**
- Create: `tools/harness/224xl/CMakeLists.txt`
- Create: `tools/harness/224xl/mult_vectors_test.cpp`

- [ ] **Step 1: Write the failing test**

Create `tools/harness/224xl/mult_vectors_test.cpp`:

```cpp
// Multiplier + saturation unit tests for the 224XL ARU primitives.
// Anchors: the Service-Manual multiplier diagnostic exercises coefficients
// +21/32, +42/32, +63/64 and x1, x1/2, x-1, x1/4, x5/4, and states "the last two
// coefficients should set the saturation" (Lexicon 224X Service Manual 5.3,
// E80-EB3). The 7-bit/128 first-cut datapath cannot represent x1, 42/32, 5/4
// exactly (that is the OPEN coeff-denominator/2-LSB item) - those exact
// coefficients become assertions once that knob resolves. This test pins the
// representable mechanics: sign-magnitude scaling, floor-shift, and saturation.
#include "sgdsp/reverb/224xl.hpp"
#include <cstdio>
#include <cstdint>

using sgdsp::reverb::aruMac;
using sgdsp::reverb::aruSat16;
using sgdsp::reverb::AruAccum;

static int g_fail = 0;

static void check(const char* name, AruAccum got, AruAccum want)
{
    if (got != want) {
        std::printf("FAIL %-28s got=%lld want=%lld\n", name,
                    (long long)got, (long long)want);
        ++g_fail;
    } else {
        std::printf("ok   %-28s = %lld\n", name, (long long)got);
    }
}

int main()
{
    // Representable coefficients (signed 7-bit magnitude, applied as coeff>>7):
    //   +1/2  -> coeff 64   (64/128)
    //   +1/4  -> coeff 32
    //   +21/32-> coeff 84   (84/128 == 21/32)
    //   +63/64-> coeff 126  (126/128 == 63/64)
    // MAC from acc=0: (x*coeff)>>7.
    check("half of 1000",        aruMac(0, 1000,  64),  500);   // 1000*64>>7 = 500
    check("quarter of 1000",     aruMac(0, 1000,  32),  250);   // 1000*32>>7 = 250
    check("21/32 of 3200",       aruMac(0, 3200,  84), 2100);   // 3200*84>>7 = 2100
    check("63/64 of 6400",       aruMac(0, 6400, 126), 6300);   // 6400*126>>7 = 6300

    // Floor division on negatives: (-1000*64)>>7 = -64000>>7 = -500 (exact here);
    // a non-exact case proves floor (toward -inf), not truncation toward zero:
    //   (-5 * 1) >> 7  ==  -1   (floor),  whereas  -5/128 == 0 (trunc).
    check("floor neg small",     aruMac(0,   -5,   1),   -1);

    // Saturation trips (the Manual's "last two coefficients set saturation"):
    //   large positive product clamps to +32767
    check("sat positive rail",   aruMac(0, 32767, 126), 32767); // 32767*126>>7=32255? no -> see note
    check("sat from big acc",    aruMac(32000, 1000, 126), 32767);
    check("sat negative rail",   aruMac(-32000, 1000, -126), -32768);

    // accumulate then saturate (sat applied to acc+prod each step)
    check("accumulate then add", aruMac(100, 1000, 64), 600);   // 100 + 500

    std::printf(g_fail ? "\n%d FAILURE(S)\n" : "\nALL PASS\n", g_fail);
    return g_fail ? 1 : 0;
}
```

> Implementer note on the two `sat positive rail` expectations: compute the exact
> value before trusting the literal. `32767*126 = 4,128,642`; `>>7 = 32255`, which
> does **not** saturate. Replace that line's `want` with `32255` and rename it
> `"126/128 of 32767"`, OR pick a coeff/x that actually exceeds the rail (e.g.
> `aruMac(0, 32767, 200)` is invalid — coeff max is 127). The reliable saturation
> trips are the `from big acc` cases below it (acc already near the rail). Keep
> `sat from big acc` and `sat negative rail`; fix the standalone-product line to
> its true value. This note exists because saturation from a single 7-bit-coeff
> product is impossible at this scale — saturation in the real datapath comes from
> *accumulation*, which the `from big acc` cases exercise.

- [ ] **Step 2: Write the CMake build**

Create `tools/harness/224xl/CMakeLists.txt`:

```cmake
cmake_minimum_required(VERSION 3.16)
project(iconex_224xl_harness CXX)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)
set(CMAKE_CXX_EXTENSIONS OFF)

# Repo root is three levels up from this file (tools/harness/224xl).
get_filename_component(REPO_ROOT "${CMAKE_CURRENT_SOURCE_DIR}/../../.." ABSOLUTE)
set(SGDSP_INCLUDE "${REPO_ROOT}/libs/sgdsp/include")

# Desktop build: portable headers only, no platform config, no CMSIS/STM.
add_executable(mult_vectors_test mult_vectors_test.cpp)
target_include_directories(mult_vectors_test PRIVATE "${SGDSP_INCLUDE}")

add_executable(diff_harness diff_harness.cpp)
target_include_directories(diff_harness PRIVATE "${SGDSP_INCLUDE}" "${CMAKE_CURRENT_SOURCE_DIR}")

add_executable(wav_ir_tool wav_ir_tool.cpp)
target_include_directories(wav_ir_tool PRIVATE "${SGDSP_INCLUDE}" "${CMAKE_CURRENT_SOURCE_DIR}")

enable_testing()
add_test(NAME mult_vectors COMMAND mult_vectors_test)
add_test(NAME diff_concert COMMAND diff_harness "${CMAKE_CURRENT_SOURCE_DIR}/golden" 01)
```

> Note: `diff_harness.cpp` and `wav_ir_tool.cpp` do not exist until Tasks 6–7. To
> build *only* this task's target now, configure then build the single target:
> `cmake --build build --target mult_vectors_test`.

- [ ] **Step 3: Run test to verify it fails**

Run:
```bash
cd tools/harness/224xl
cmake -S . -B build -DCMAKE_BUILD_TYPE=Release 2>NUL
cmake --build build --target mult_vectors_test --config Release
```
Expected: build FAILS — `diff_harness.cpp`/`wav_ir_tool.cpp` missing at configure, OR (if configure passes) the `mult_vectors_test` target builds but the `sat positive rail` line FAILS at runtime per the implementer note.

If configure aborts on the missing sources, temporarily comment out the `diff_harness` and `wav_ir_tool` `add_executable`/`target_include_directories`/`add_test` lines, reconfigure, and build `mult_vectors_test`. Re-enable them in Task 6/7.

- [ ] **Step 4: Fix the one wrong literal, then run to pass**

Edit `mult_vectors_test.cpp`: change the `"sat positive rail"` line to the true value:
```cpp
    check("126/128 of 32767",    aruMac(0, 32767, 126), 32255); // 32767*126>>7 = 32255
```

Run: `tools/harness/224xl/build/Release/mult_vectors_test` (or `.../build/mult_vectors_test` on single-config generators)
Expected: `ALL PASS`, exit 0.

- [ ] **Step 5: Commit**

```bash
git add tools/harness/224xl/CMakeLists.txt tools/harness/224xl/mult_vectors_test.cpp
git commit -m "224XL: CMake harness build + multiplier/saturation unit tests"
```

---

## Task 6: Core datapath + the diff harness (layer 1 + layer 2)

This task adds the executing datapath to the core and the harness that proves parity. Split into 6A (core) and 6B (harness).

### Task 6A: Core datapath

**Files:**
- Modify: `libs/sgdsp/include/sgdsp/reverb/224xl.hpp`

- [ ] **Step 1: Add the Probe struct, decoded-step storage, and the class**

In `224xl.hpp`, after `aruMac` and before the closing `} // namespace`, insert:

```cpp
// Per-step probe record (mirrors aru_datapath.run_trace tuple field order).
struct Probe
{
    int64_t n, s, addr, dab, racc_in, prod, acc, res;
};
static constexpr int64_t kProbeResSentinel = (int64_t)0x8000000000000000ULL; // INT64_MIN

// A decoded active microword step (NOP steps are dropped at load time).
struct AruStep
{
    int      s;        // original step index 0..127
    uint32_t offset;   // DMEM offset; addr = (pos - offset) & 0xFFFF
    int      coeff;    // signed 7-bit magnitude (-127..127)
    uint8_t  zero;     // clear accumulator before MAC
    uint8_t  xfer;     // load result register / write tank
    uint8_t  wa;       // write-register address (3 = pass-through)
    uint8_t  ra;       // read-register address (b5<<1 | b4)
    uint8_t  b3;       // RW/SRC (OPEN; recorded for parity, unused in first cut)
};

template <uint32_t DmemWords = 65536, uint32_t Channels = 2>
class Lexicon224XLCore
{
    static_assert(DmemWords >= 65536, "224XL DMEM is a 64K ring; size must be >= 65536");
    static_assert(Channels == 1 || Channels == 2, "Channels must be 1 or 2");

public:
    static constexpr uint32_t kDmemMask = 0xFFFFu;  // hardware 64K ring mask

    // ---- Lifecycle ----
    SGDSP_NOINLINE void prepare(SampleRate sampleRate, AruWord* dmem) noexcept
    {
        sampleRate_ = sampleRate;
        dmem_ = dmem;
        reset();
    }

    // Decode a 128-step WCS image (4 active-low bytes/step) into the active-step
    // list, skipping NOPs (lane2==lane3==0xFF). Matches aru_datapath.load_microcode.
    SGDSP_NOINLINE void loadProgram(const uint8_t wcs[512]) noexcept
    {
        nActive_ = 0;
        for (int s = 0; s < 128; ++s) {
            const uint8_t l0 = wcs[s*4+0], l1 = wcs[s*4+1];
            const uint8_t l2 = wcs[s*4+2], l3 = wcs[s*4+3];
            if (l2 == 0xFF && l3 == 0xFF) continue;          // NOP / pure-delay fill
            const uint8_t ctl = static_cast<uint8_t>(~l2);
            AruStep st;
            st.s      = s;
            st.offset = static_cast<uint32_t>(~(l0 | (l1 << 8))) & 0xFFFFu;
            st.coeff  = (l3 & 0x80) ? -static_cast<int>(l3 & 0x7F) : static_cast<int>(l3 & 0x7F);
            st.zero   = (ctl >> 7) & 1;
            st.xfer   = (ctl >> 2) & 1;
            st.wa     = ctl & 3;
            st.ra     = (ctl >> 4) & 3;     // datapath-validated RA = b5<<1 | b4
            st.b3     = (ctl >> 3) & 1;
            steps_[nActive_++] = st;
        }
        firstActive_ = (nActive_ > 0) ? 0 : -1;
    }

    SGDSP_NOINLINE void reset() noexcept
    {
        for (auto& r : R_) r = 0;
        acc_ = 0;
        res_ = 0;
        if (dmem_) for (uint32_t i = 0; i <= kDmemMask; ++i) dmem_[i] = 0;
        pos_ = 0;
        sampleIndex_ = 0;
    }

    int activeStepCount() const noexcept { return nActive_; }
    const AruStep& step(int i) const noexcept { return steps_[i]; }

    // ---- Integer surface (harness) ----
    SGDSP_INLINE void processFixed(AruWord in, AruWord& outL, AruWord& outR) noexcept
    {
        const AruWord o = executeSample<false>(in, nullptr, nullptr);
        outL = o; outR = o;   // first cut: mono datapath duplicated; FPC L/R split deferred
    }

    // Instrumented twin for the diff harness. Records up to maxProbes per-step
    // probes (caller sizes the buffer); returns the per-sample energy in esumOut.
    SGDSP_NOINLINE AruWord processFixedTraced(AruWord in, Probe* probes, int* nProbesOut,
                                              int64_t* esumOut) noexcept
    {
        int n = 0;
        int64_t esum = 0;
        const AruWord o = executeSample<true>(in, probes, &n, &esum);
        if (nProbesOut) *nProbesOut = n;
        if (esumOut) *esumOut = esum;
        return o;
    }

    // ---- Float boundary (DPF/sgdsp); only float in the signal path ----
    SGDSP_INLINE void process(Sample in, Sample& outL, Sample& outR) noexcept
    {
        AruWord l, r;
        processFixed(floatToAru(in), l, r);
        outL = aruToFloat(l);
        outR = aruToFloat(r);
    }

    // ---- Parameters (scaffolded; static CONCERT is the bring-up target) ----
    void setParameter(int index, float value01) noexcept { (void)index; (void)value01; }

private:
    static constexpr float kAruScale = 32768.0f;
    SGDSP_INLINE static AruWord floatToAru(Sample x) noexcept
    {
        float s = x * kAruScale;
        if (s >  32767.0f) s =  32767.0f;
        if (s < -32768.0f) s = -32768.0f;
        return static_cast<AruWord>(s >= 0.0f ? s + 0.5f : s - 0.5f);
    }
    SGDSP_INLINE static Sample aruToFloat(AruWord v) noexcept
    {
        return static_cast<Sample>(v) * (1.0f / kAruScale);
    }

    // The 128-step microprogram for one output sample. Trace==true records probes
    // and the energy sum, exactly mirroring aru_datapath.run_trace. The two
    // instantiations share ONE datapath (DRY); tracing compiles out of the hot path.
    template <bool Trace>
    SGDSP_INLINE AruWord executeSample(AruWord in, Probe* probes, int* nProbes,
                                       int64_t* esumOut = nullptr) noexcept
    {
        pos_ = (pos_ + 1) & kDmemMask;
        int np = 0;
        int64_t esum = 0;
        AruWord lastRes = res_;
        for (int i = 0; i < nActive_; ++i) {
            const AruStep& st = steps_[i];
            const uint32_t addr = (pos_ - st.offset) & kDmemMask;
            AruWord dab;
            if (st.xfer) { dmem_[addr] = res_; dab = res_; }
            else         { dab = dmem_[addr]; }
            if (i == firstActive_) dab += in;     // additive input == reference at sample 0
            R_[st.wa] = dab;
            const AruWord raccIn = R_[st.ra];
            if (st.zero) acc_ = 0;
            const AruAccum prod = (static_cast<AruAccum>(raccIn) * st.coeff)
                                  >> ArithProfile::kCoeffShift;
            acc_ = aruSat16(acc_ + prod);
            int64_t resVal = kProbeResSentinel;
            if (st.xfer) {
                res_ = static_cast<AruWord>(aruSat16(acc_));
                esum += (res_ < 0) ? -res_ : res_;
                lastRes = res_;
                resVal = res_;
            }
            if (Trace && probes) {
                probes[np++] = Probe{ (int64_t)sampleIndex_, (int64_t)st.s, (int64_t)addr,
                                      (int64_t)dab, (int64_t)raccIn, (int64_t)prod,
                                      (int64_t)acc_, resVal };
            }
        }
        if (Trace) { if (nProbes) *nProbes = np; if (esumOut) *esumOut = esum; }
        ++sampleIndex_;
        return lastRes;   // first-cut audio proxy = last RES of the sample
    }

    // Group 1: hot per-sample state
    AruWord  R_[4] = {0, 0, 0, 0};
    AruAccum acc_ = 0;
    AruWord  res_ = 0;
    uint32_t pos_ = 0;
    int64_t  sampleIndex_ = 0;
    // Group 2: program
    AruStep  steps_[128];
    int      nActive_ = 0;
    int      firstActive_ = -1;
    // Group 3: external DMEM + rate
    AruWord*   dmem_ = nullptr;
    SampleRate sampleRate_ = 0;
};

template <uint32_t N = 65536> using Lexicon224XL     = Lexicon224XLCore<N, 2>;
template <uint32_t N = 65536> using Lexicon224XLMono = Lexicon224XLCore<N, 1>;
```

> Note the `processFixed` signature ignores `Channels` for output duplication in
> the first cut (documented in the spec, §4.4). The `Channels` template still sizes
> the public typedefs and gates future per-channel state.

- [ ] **Step 2: Commit the core (compile verified in 6B build)**

```bash
git add libs/sgdsp/include/sgdsp/reverb/224xl.hpp
git commit -m "224XL: core datapath - decode, executeSample<Trace>, fixed/float entries"
```

### Task 6B: The diff harness

**Files:**
- Create: `tools/harness/224xl/golden_io.hpp`
- Create: `tools/harness/224xl/diff_harness.cpp`

- [ ] **Step 1: Write the golden readers**

Create `tools/harness/224xl/golden_io.hpp`:

```cpp
#pragma once
// Minimal readers for the golden artifacts written by tools/export_golden_224.py.
// Binary files are little-endian int64 arrays; JSON is parsed with a tiny scanner
// sufficient for the flat, generator-produced shapes (no general JSON needed).
#include <cstdint>
#include <cstdio>
#include <string>
#include <vector>

namespace golden {

inline std::vector<uint8_t> readBytes(const std::string& path)
{
    std::vector<uint8_t> v;
    FILE* f = std::fopen(path.c_str(), "rb");
    if (!f) return v;
    std::fseek(f, 0, SEEK_END); long n = std::ftell(f); std::fseek(f, 0, SEEK_SET);
    v.resize(n > 0 ? (size_t)n : 0);
    if (n > 0) { size_t got = std::fread(v.data(), 1, (size_t)n, f); v.resize(got); }
    std::fclose(f);
    return v;
}

inline std::vector<int64_t> readI64(const std::string& path)
{
    std::vector<uint8_t> b = readBytes(path);
    std::vector<int64_t> out(b.size() / 8);
    for (size_t i = 0; i < out.size(); ++i) {
        int64_t v = 0;
        for (int k = 0; k < 8; ++k) v |= (int64_t)b[i*8+k] << (8*k);
        out[i] = v;
    }
    return out;
}

// One decoded field record from <id>_fields.json (flat objects, integer values).
struct Field { int s, offset, coeff, ZERO, b3, XFER, WA, RA; };

// Scan flat JSON like [{"s":0,"offset":123,"coeff":-7,"ZERO":0,"b3":0,"XFER":1,"WA":0,"RA":1}, ...].
inline std::vector<Field> readFields(const std::string& path)
{
    std::vector<uint8_t> bytes = readBytes(path);
    std::string j(bytes.begin(), bytes.end());
    std::vector<Field> out;
    size_t i = 0;
    auto readKeyVal = [&](const char* key, int& dst) {
        // assumes keys appear in object order; find next "key": then parse int
        std::string pat = std::string("\"") + key + "\":";
        size_t p = j.find(pat, i);
        if (p == std::string::npos) return false;
        p += pat.size();
        dst = std::strtol(j.c_str() + p, nullptr, 10);
        i = p;
        return true;
    };
    while (true) {
        size_t obj = j.find('{', i);
        if (obj == std::string::npos) break;
        i = obj;
        Field f{};
        if (!readKeyVal("s", f.s)) break;
        readKeyVal("offset", f.offset);
        readKeyVal("coeff", f.coeff);
        readKeyVal("ZERO", f.ZERO);
        readKeyVal("b3", f.b3);
        readKeyVal("XFER", f.XFER);
        readKeyVal("WA", f.WA);
        readKeyVal("RA", f.RA);
        out.push_back(f);
        size_t end = j.find('}', i);
        if (end == std::string::npos) break;
        i = end + 1;
    }
    return out;
}

// Pull a single integer value for `key` out of a flat meta.json.
inline int readMetaInt(const std::string& path, const char* key, int dflt)
{
    std::vector<uint8_t> bytes = readBytes(path);
    std::string j(bytes.begin(), bytes.end());
    std::string pat = std::string("\"") + key + "\":";
    size_t p = j.find(pat);
    if (p == std::string::npos) return dflt;
    return (int)std::strtol(j.c_str() + p + pat.size(), nullptr, 10);
}

} // namespace golden
```

> The flat-JSON scanner relies on the exporter's key order (`s, offset, coeff,
> ZERO, b3, XFER, WA, RA`). It is intentionally minimal — these files are
> machine-generated with a fixed shape, so a full JSON parser is YAGNI.

- [ ] **Step 2: Write the diff harness**

Create `tools/harness/224xl/diff_harness.cpp`:

```cpp
// 224XL diff harness: proves the C++ core reproduces the Python aru_datapath
// reference integer-exact for one program.
//   Layer 1 (microcode parity): core decode of <id>_wcs.bin == <id>_fields.json.
//   Layer 2 (arithmetic parity): per-step probes + per-sample energy == golden.
// Usage: diff_harness <golden_dir> <id_hex2>   e.g.  diff_harness ./golden 01
#include "sgdsp/reverb/224xl.hpp"
#include "golden_io.hpp"
#include <cstdio>
#include <cstdlib>
#include <string>
#include <vector>

using namespace sgdsp::reverb;

int main(int argc, char** argv)
{
    if (argc < 3) { std::printf("usage: diff_harness <golden_dir> <id_hex2>\n"); return 2; }
    const std::string dir = argv[1];
    const std::string id  = argv[2];
    const std::string base = dir + "/" + id + "_";

    const int nsamp       = golden::readMetaInt(base + "meta.json", "nsamp", 0);
    const int traceWindow = golden::readMetaInt(base + "meta.json", "trace_window", 0);
    const int impVal      = golden::readMetaInt(base + "meta.json", "imp", 0);
    const int nActiveMeta = golden::readMetaInt(base + "meta.json", "n_active", 0);
    if (nsamp == 0) { std::printf("ERROR: cannot read %smeta.json\n", base.c_str()); return 2; }

    std::vector<uint8_t> wcs = golden::readBytes(base + "wcs.bin");
    if (wcs.size() != 512) { std::printf("ERROR: %swcs.bin not 512 bytes\n", base.c_str()); return 2; }
    std::vector<golden::Field> fields = golden::readFields(base + "fields.json");
    std::vector<int64_t> esumGold = golden::readI64(base + "esum.bin");
    std::vector<int64_t> stepsGold = golden::readI64(base + "steps.bin");

    static AruWord dmem[65536];
    static Lexicon224XLCore<65536, 2> core;
    core.prepare(34130, dmem);
    core.loadProgram(wcs.data());

    // ---------- Layer 1: microcode decode parity ----------
    int l1fail = 0;
    if (core.activeStepCount() != (int)fields.size()) {
        std::printf("L1 FAIL: active step count core=%d gold=%zu\n",
                    core.activeStepCount(), fields.size());
        ++l1fail;
    }
    int nCmp = core.activeStepCount() < (int)fields.size()
               ? core.activeStepCount() : (int)fields.size();
    for (int i = 0; i < nCmp; ++i) {
        const AruStep& c = core.step(i);
        const golden::Field& g = fields[i];
        if (c.s != g.s || (int)c.offset != g.offset || c.coeff != g.coeff ||
            c.zero != g.ZERO || c.b3 != g.b3 || c.xfer != g.XFER ||
            c.wa != g.WA || c.ra != g.RA) {
            std::printf("L1 FAIL @active %d (step %d): "
                        "core{off=%u coeff=%d Z=%d b3=%d XF=%d WA=%d RA=%d} "
                        "gold{off=%d coeff=%d Z=%d b3=%d XF=%d WA=%d RA=%d}\n",
                        i, c.s, c.offset, c.coeff, c.zero, c.b3, c.xfer, c.wa, c.ra,
                        g.offset, g.coeff, g.ZERO, g.b3, g.XFER, g.WA, g.RA);
            if (++l1fail >= 10) { std::printf("...stopping after 10\n"); break; }
        }
    }
    if (!l1fail) std::printf("L1 OK: %d active steps decode-match\n", core.activeStepCount());

    // ---------- Layer 2: arithmetic parity ----------
    const int nActive = core.activeStepCount();
    (void)nActiveMeta;
    std::vector<Probe> probes(nActive > 0 ? nActive : 1);
    int l2fail = 0;
    size_t gIdx = 0;                       // index into flattened stepsGold (8 ints/record)
    for (int n = 0; n < nsamp; ++n) {
        const AruWord in = (n == 0) ? (AruWord)impVal : 0;
        AruWord outL, outR; (void)outL; (void)outR;
        int np = 0; int64_t esum = 0;
        core.processFixedTraced(in, probes.data(), &np, &esum);

        if (esum != esumGold[n]) {
            std::printf("L2 FAIL esum @sample %d: core=%lld gold=%lld\n",
                        n, (long long)esum, (long long)esumGold[n]);
            if (++l2fail >= 10) break;
        }
        if (n < traceWindow) {
            for (int k = 0; k < np; ++k) {
                const Probe& p = probes[k];
                const int64_t* g = &stepsGold[gIdx];
                gIdx += 8;
                if (p.n!=g[0]||p.s!=g[1]||p.addr!=g[2]||p.dab!=g[3]||
                    p.racc_in!=g[4]||p.prod!=g[5]||p.acc!=g[6]||p.res!=g[7]) {
                    std::printf("L2 FAIL probe @sample %d step %lld: "
                        "core{addr=%lld dab=%lld racc=%lld prod=%lld acc=%lld res=%lld} "
                        "gold{addr=%lld dab=%lld racc=%lld prod=%lld acc=%lld res=%lld}\n",
                        n, (long long)p.s,
                        (long long)p.addr,(long long)p.dab,(long long)p.racc_in,
                        (long long)p.prod,(long long)p.acc,(long long)p.res,
                        (long long)g[2],(long long)g[3],(long long)g[4],
                        (long long)g[5],(long long)g[6],(long long)g[7]);
                    if (++l2fail >= 10) { std::printf("...stopping after 10\n"); break; }
                }
            }
            if (l2fail >= 10) break;
        }
    }
    if (!l2fail) std::printf("L2 OK: %d samples energy + %d-sample probe trace match\n",
                             nsamp, traceWindow);

    const int rc = (l1fail || l2fail) ? 1 : 0;
    std::printf(rc ? "\nDIFF FAILED\n" : "\nDIFF PASSED (integer-exact vs reference)\n");
    return rc;
}
```

- [ ] **Step 3: Re-enable the harness targets in CMake (if disabled in Task 5)**

Ensure `tools/harness/224xl/CMakeLists.txt` has the `diff_harness` and `wav_ir_tool`
targets uncommented. `wav_ir_tool.cpp` still does not exist, so build only what's ready:

Run:
```bash
cd tools/harness/224xl
cmake -S . -B build -DCMAKE_BUILD_TYPE=Release
cmake --build build --target diff_harness --config Release
```
Expected: `diff_harness` compiles and links (this is the first full compile of `224xl.hpp`'s datapath).

- [ ] **Step 4: Run the diff harness against the golden**

Run: `tools/harness/224xl/build/Release/diff_harness tools/harness/224xl/golden 01`
(single-config generators: `.../build/diff_harness ...`)
Expected:
```
L1 OK: <N> active steps decode-match
L2 OK: 4000 samples energy + 64-sample probe trace match

DIFF PASSED (integer-exact vs reference)
```
exit 0.

- [ ] **Step 5: If it fails, debug at the first divergence**

The harness prints the first divergent sample/step/field. Common causes, in order:
- L1 field mismatch → decode bug in `loadProgram` (recheck active-low masks, RA bits).
- L2 `dab` mismatch at sample 0 first step → injection model (must be additive at `firstActive_`).
- L2 `prod` mismatch on negative values → using `/128` instead of `>>7` somewhere.
- L2 `acc`/`res` drift after many steps → saturation rails or `zero`/`xfer` handling.
Fix in `224xl.hpp`, rebuild, rerun until `DIFF PASSED`.

- [ ] **Step 6: Commit**

```bash
git add tools/harness/224xl/golden_io.hpp tools/harness/224xl/diff_harness.cpp tools/harness/224xl/CMakeLists.txt
git commit -m "224XL: diff harness - layer-1 decode + layer-2 arithmetic parity (CONCERT exact)"
```

---

## Task 7: WAV / IR listening tool

**Files:**
- Create: `tools/harness/224xl/wav_ir_tool.cpp`

- [ ] **Step 1: Write the tool**

Create `tools/harness/224xl/wav_ir_tool.cpp`:

```cpp
// 224XL listening / IR tool: drives the core's FLOAT boundary and writes a WAV.
//   impulse mode: wav_ir_tool ir  <out.wav> [nsamp]   -> dumps the impulse response
//   process mode: wav_ir_tool wav <in.wav> <out.wav>  -> filters a mono 16-bit WAV
// Stereo out (L/R duplicated in the first cut). For ears + spectrogram/EDC, not for
// bit-exact checks (that is diff_harness). Loads CONCERT from the generated header.
#include "sgdsp/reverb/224xl.hpp"
#include "sgdsp/reverb/224xl_programs.hpp"
#include <cstdio>
#include <cstdint>
#include <cstring>
#include <string>
#include <vector>

using namespace sgdsp::reverb;

#pragma pack(push, 1)
struct WavHeader {
    char riff[4] = {'R','I','F','F'}; uint32_t chunkSize = 0;
    char wave[4] = {'W','A','V','E'};
    char fmt[4]  = {'f','m','t',' '}; uint32_t fmtSize = 16;
    uint16_t audioFormat = 1; uint16_t numChannels = 2;
    uint32_t sampleRate = 34130; uint32_t byteRate = 34130*2*2;
    uint16_t blockAlign = 4; uint16_t bitsPerSample = 16;
    char data[4] = {'d','a','t','a'}; uint32_t dataSize = 0;
};
#pragma pack(pop)

static void writeStereoWav(const std::string& path, const std::vector<int16_t>& interleaved,
                           uint32_t sr)
{
    WavHeader h;
    h.sampleRate = sr; h.byteRate = sr*2*2;
    h.dataSize = (uint32_t)(interleaved.size() * sizeof(int16_t));
    h.chunkSize = 36 + h.dataSize;
    FILE* f = std::fopen(path.c_str(), "wb");
    if (!f) { std::printf("ERROR: cannot open %s\n", path.c_str()); return; }
    std::fwrite(&h, sizeof(h), 1, f);
    std::fwrite(interleaved.data(), sizeof(int16_t), interleaved.size(), f);
    std::fclose(f);
}

// Read a mono 16-bit PCM WAV's samples (skips to 'data'); returns float [-1,1].
static std::vector<float> readMonoWav(const std::string& path, uint32_t& srOut)
{
    std::vector<float> out;
    FILE* f = std::fopen(path.c_str(), "rb");
    if (!f) { std::printf("ERROR: cannot open %s\n", path.c_str()); return out; }
    WavHeader h;
    if (std::fread(&h, sizeof(h), 1, f) != 1) { std::fclose(f); return out; }
    srOut = h.sampleRate;
    std::vector<int16_t> pcm(h.dataSize / sizeof(int16_t));
    if (!pcm.empty()) std::fread(pcm.data(), sizeof(int16_t), pcm.size(), f);
    std::fclose(f);
    const int ch = h.numChannels ? h.numChannels : 1;
    out.reserve(pcm.size() / ch);
    for (size_t i = 0; i + ch <= pcm.size(); i += ch)
        out.push_back(pcm[i] / 32768.0f);   // take channel 0
    return out;
}

int main(int argc, char** argv)
{
    if (argc < 3) {
        std::printf("usage:\n  wav_ir_tool ir  <out.wav> [nsamp]\n"
                    "  wav_ir_tool wav <in.wav> <out.wav>\n");
        return 2;
    }
    const std::string mode = argv[1];

    static AruWord dmem[65536];
    static Lexicon224XLCore<65536, 2> core;
    core.prepare(34130, dmem);
    core.loadProgram(programs::kCONCERT_HALL_WCS);

    std::vector<int16_t> outBuf;
    uint32_t sr = 34130;

    auto pushOut = [&](float l, float r) {
        auto clamp16 = [](float x){ x*=32768.0f; if(x>32767)x=32767; if(x<-32768)x=-32768;
                                    return (int16_t)(x>=0?x+0.5f:x-0.5f); };
        outBuf.push_back(clamp16(l)); outBuf.push_back(clamp16(r));
    };

    if (mode == "ir") {
        const std::string outPath = argv[2];
        const int nsamp = (argc > 3) ? std::atoi(argv[3]) : 34130; // ~1 s
        for (int n = 0; n < nsamp; ++n) {
            Sample inS = (n == 0) ? 0.61f : 0.0f;   // ~20000/32768 impulse
            Sample l, r; core.process(inS, l, r);
            pushOut(l, r);
        }
        writeStereoWav(outPath, outBuf, sr);
        std::printf("wrote IR %s (%d samples)\n", outPath.c_str(), nsamp);
    } else if (mode == "wav") {
        if (argc < 4) { std::printf("usage: wav_ir_tool wav <in.wav> <out.wav>\n"); return 2; }
        std::vector<float> in = readMonoWav(argv[2], sr);
        core.prepare(sr ? sr : 34130, dmem);
        core.loadProgram(programs::kCONCERT_HALL_WCS);
        for (float x : in) { Sample l, r; core.process(x, l, r); pushOut(l, r); }
        writeStereoWav(argv[3], outBuf, sr ? sr : 34130);
        std::printf("wrote %s (%zu frames)\n", argv[3], in.size());
    } else {
        std::printf("unknown mode '%s'\n", mode.c_str());
        return 2;
    }
    return 0;
}
```

- [ ] **Step 2: Build it**

Run:
```bash
cd tools/harness/224xl
cmake --build build --target wav_ir_tool --config Release
```
Expected: compiles and links.

- [ ] **Step 3: Produce an impulse response and sanity-check (non-silent + bounded)**

Run: `tools/harness/224xl/build/Release/wav_ir_tool ir /tmp/concert_ir.wav 17000`
Expected: `wrote IR /tmp/concert_ir.wav (17000 samples)`; the file exists and is ~68 KB.

Verify it is non-silent and bounded/not-railed (Python, no extra deps):
```bash
python -c "import wave,struct; w=wave.open('/tmp/concert_ir.wav'); d=w.readframes(w.getnframes()); s=struct.unpack('<%dh'%(len(d)//2), d); L=s[0::2]; e=lambda a:sum(abs(x) for x in a); peak=max(abs(x) for x in L); early=e(L[:2000]); late=e(L[12000:14000]); railed=sum(1 for x in L[12000:14000] if abs(x)>=32767)/2000.0; print('early',early,'late',late,'peak',peak,'railed_frac',round(railed,3)); assert early>0, 'silent'; assert peak<=32768; assert railed<0.5, 'tank pinned at rail (unstable)'; print('IR non-silent + bounded (not railed): OK; clean decay deferred to ArithProfile tuning')"
```
Expected: prints `early ... late ... peak ... railed_frac ...` then `IR non-silent + bounded (not railed): OK; clean decay deferred to ArithProfile tuning`.

NOTE: the first-cut CONCERT tank sustains (late energy >= early energy) — this is non-silent and bounded (not railed), faithfully matching the reference arithmetic. Clean decay is deferred to ArithProfile tuning (see design spec §8 — the result-register shift / coeff denominator that set loop gain/decay are OPEN items).

- [ ] **Step 4: Commit**

```bash
git add tools/harness/224xl/wav_ir_tool.cpp
git commit -m "224XL: WAV/IR listening tool (float boundary, non-silent bounded CONCERT IR)"
```

---

## Task 8: Full build + test sweep, README, final commit

**Files:**
- Create: `tools/harness/224xl/README.md`

- [ ] **Step 1: Configure + build all three targets clean**

Run:
```bash
cd tools/harness/224xl
cmake -S . -B build -DCMAKE_BUILD_TYPE=Release
cmake --build build --config Release
```
Expected: `mult_vectors_test`, `diff_harness`, `wav_ir_tool` all build with no warnings-as-errors.

- [ ] **Step 2: Run the CTest suite**

Run: `cd tools/harness/224xl && ctest --test-dir build --output-on-failure -C Release`
Expected: `100% tests passed, 0 tests failed out of 2` (mult_vectors, diff_concert).

- [ ] **Step 3: Write the harness README**

Create `tools/harness/224xl/README.md`:

```markdown
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

## Scope

Validated: C++ == Python reference (CONCERT static), multiplier vectors, builds.
Deferred (knobs/interfaces in place): hardware-anchored arithmetic (ArithProfile),
per-program FPC position base + true stereo L/R split, params/modulation dynamic
parity, all 20 programs, DPF/Seed2 wrappers. See the design spec for the full list.
```

- [ ] **Step 4: Add a root .gitignore entry for build dirs (if not present)**

Append to `.gitignore` at repo root:
```
build/
tools/harness/**/build/
```

- [ ] **Step 5: Commit**

```bash
git add tools/harness/224xl/README.md .gitignore
git commit -m "224XL: harness README + ignore build dirs; scaffold complete"
```

---

## Self-review (completed during planning)

**Spec coverage:** Core (§4) → Tasks 4, 6A. Generated tables (§5) → Task 2. Golden export + `run_trace` (§6) → Tasks 1, 3. Diff harness three tools (§7) → Tasks 5 (mult), 6B (diff), 7 (wav/ir). CMake (§2 decision 4) → Task 5. ArithProfile knobs (§4.3) → Task 4. Validated-now vs deferred (§8) → Task 8 README + spec. All spec sections map to tasks.

**Placeholder scan:** No "TBD"/"implement later". The one judgment call (the wrong saturation literal) is called out explicitly with the corrected value and the reason, and is fixed in Task 5 Step 4 — not left open.

**Type consistency:** `AruWord`/`AruAccum`/`AruStep`/`Probe`/`ArithProfile` names are consistent across Tasks 4/6/6B. `aruMac`/`aruSat16` used in both the core datapath and `mult_vectors_test`. The 8-field probe order `(n,s,addr,dab,racc_in,prod,acc,res)` is identical in `run_trace` (Task 1), the exporter (Task 3), the core probe (Task 6A), and the harness comparison (Task 6B). `loadProgram(const uint8_t[512])` and `processFixedTraced(...)` signatures match between core and harness.

**Known judgment point for the implementer:** Task 5's `mult_vectors_test` saturation expectations — verify each `want` by hand (the note explains why a single 7-bit-coeff product cannot saturate at 16-bit scale; saturation is exercised via the `from big acc` cases). This is the only spot requiring arithmetic verification rather than transcription.
