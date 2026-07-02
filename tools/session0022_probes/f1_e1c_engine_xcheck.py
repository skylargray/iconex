#!/usr/bin/env python3
"""F1c gate 4 (plan 024) — the e1c <-> engine bit-equality lock: the re-synced RTL22 core
must walk the diag-3 bench BIT-IDENTICALLY to the e1_aru_signatures Emitter at the champion
variant (PRLOAD=raw, RAIL=cs, DUAL3=0, CAPB=0) — the object the §5.7 tables verify at
1469/1469 pins (owner-corrected tables; feedback 710/710 + no-feedback 759/759).

Method (the plan's "assert bit-equality per step against it across the steady frame"):
  1. build the Emitter at the champion variant and the engine with the SAME bench state
     (regfile = the E1a pump values as phys patterns; XREG_host = 0x607F; diag-3 rows);
  2. run BOTH to the frame-periodic fixed point;
  3. lock-step N frames comparing AFTER EVERY STEP: ACC (20-bit phys), RES (16-bit phys),
     the regfile, and the end-of-step DAB.

STALE-CELL FINDING (this probe's original coverage assert, resolved by
f1_dmem_stale_reads.py): the diag-3 steady frame is NOT write-before-read closed — MEMR
rows 1/4/5 read cells last written by the rows-8/9 MEMWs 54426 / 5555 / 65536 frames
earlier (through the CPC wrap; steady written value V* = phys 0x8000, the saturated-tail
capture). The read value NEVER reaches a MAC operand (every row writes R3; every RA=3
operand load samples R3 one step after an IO overwrote it) and differs from the unwritten
default ONLY in DAB bit 15 — and BOTH DAB15-carrying pins (U29.15, U43.6) are UNLISTED in
the tables, so H0 (stale reads decay to phys 0) and H1 (DRAM retains across the wrap ->
0x8000) BOTH score 1469/1469: the convention is measured-inert to the lock and stays an
open bench question. Here the engine's unwritten-DMEM default (phys 0xFFFF = CPU silence)
is aligned to the Emitter's (phys 0) per stale read — convention alignment, not physics.

A state mismatch here re-opens registry #31 (engine != physical law) or #35 (the
clamp-into-ACC path).
"""
import sys, os

TOOLS = r"d:\OneDrive\Gray Instruments\iconex\tools"
sys.path.insert(0, TOOLS)
HERE = os.path.dirname(os.path.abspath(__file__))

import e1_aru_signatures as E1                     # module-level: loads diag-3 rows + selftests
from aru_freerun22_rtl import RTL22

CHAMPION = (0, 0, 0, 0)                            # PRLOAD=raw, RAIL=cs, DUAL3=0, CAPB=0
CONVERGE_FRAMES = 64                               # e1c fixed point lands in ~33
LOCKSTEP_FRAMES = 8

rows = E1.rows


def bench_engine():
    eng = RTL22()
    eng.R = [(~v) & 0xFFFF for v in (0xAAAA, 0x9999, 0xC787, 0x607F)]   # the E1a pump (phys)
    eng.XREG_host = E1.XREG_CONST                  # 0x607F, static (E1a: the loop is silent)
    return eng


def align_stale_reads(em, eng, cpc):
    """Give the engine the Emitter's stale-cell convention (phys 0) for this frame's
    unwritten MEMR targets (rows 1/4/5 — see the module docstring finding)."""
    n = 0
    for d in rows:
        if d["typ"] == 0:
            addr = (cpc - d["ofst"]) & 0xFFFF
            if addr not in em.DM:
                eng.DM.setdefault(addr, 0x0000)
                n += 1
    return n


def main():
    em = E1.Emitter(CHAMPION)
    eng = bench_engine()

    for f in range(CONVERGE_FRAMES):
        align_stale_reads(em, eng, em.CPC)
        em.run_frame()
        eng.run_sample(rows, 0)

    assert em.CPC == eng.CPC, (em.CPC, eng.CPC)

    n_steps = 0
    n_stale = 0
    for f in range(LOCKSTEP_FRAMES):
        n_stale += align_stale_reads(em, eng, em.CPC)
        for i, d in enumerate(rows):
            em.step(d)
            eng.step(d, 0)
            state_em = (em.ACC, em.RES, tuple(em.R), em.dab)
            state_en = (eng.ACC, eng.RES, tuple(eng.R), eng.DAB)
            assert state_em == state_en, (
                f"BIT MISMATCH at steady frame {f} step {i} (typ={d['typ']}):\n"
                f"  Emitter ACC={em.ACC:05X} RES={em.RES:04X} R={[f'{v:04X}' for v in em.R]} "
                f"dab={em.dab:04X}\n"
                f"  engine  ACC={eng.ACC:05X} RES={eng.RES:04X} R={[f'{v:04X}' for v in eng.R]} "
                f"dab={eng.DAB:04X}\n"
                f"  (re-opens registry #31/#35)")
            n_steps += 1
        em.CPC = (em.CPC + 1) & 0xFFFF
        eng.CPC = (eng.CPC + 1) & 0xFFFF
        eng.sample_count += 1

    print(f"e1c<->engine lock: {n_steps} lock-stepped steps over {LOCKSTEP_FRAMES} steady "
          f"frames — ACC/RES/regfile/DAB BIT-IDENTICAL at every step")
    print(f"stale-cell reads aligned to the Emitter convention: {n_stale} "
          f"(3/frame: rows 1/4/5; measured-inert to the 1469/1469 lock — "
          f"see f1_dmem_stale_reads.py)")
    print("VERDICT: the re-synced engine core IS the pin-locked physical walk on the "
          "diag-3 bench (registry #31 closed at the engine level)")


if __name__ == "__main__":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass
    main()
