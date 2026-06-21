#!/usr/bin/env python3
"""PCM60 ARU microword decoder  --  Phase-1 "Rosetta Stone".

Rebuilt from the Phase-1 field map (docs/plans/480L_reversing_roadmap.md, Phase 1
RESULTS).  The PCM60 (V1.0 firmware set, four 2732 / 4 KB ROMs) has NO control
processor: the 128-step microprogram is fully static in ROM, and the panel knobs
drive the upper address lines to select a precomputed coefficient/offset frame.

GEOMETRY
--------
The four ROMs are parallel 8-bit byte-lanes of ONE 32-bit microword.  Each 4 KB
ROM = 32 frames x 128 steps.  ROM address decodes as:

    addr (A11..A0) = program(A11) | param(A10..A7) | step(A6..A0)

  -> program  = bit 11      (2 programs: A=0, B=1)
  -> param    = bits 10..7  (16 parameter frames, 0..15  = panel-knob position)
  -> step     = bits 6..0   (128 microcode steps, 0..127)

FIELD MAP (microword = 32 bits, one byte per lane)
--------------------------------------------------
  U38 : U32   16-bit SIGNED offset (2's complement); U38 = hi byte, U32 = lo byte
              -> MMU.  delay = -offset samples.
              negative offset => positive delay  => READ a delay tap.
              positive offset => write target near the write pointer => WRITE.
  U35         coefficient (8-bit, /256).  ARU multiplier.  0x7F = 0.496 ~= x0.5 scalar.
  U43         control (8-bit).  low nibble = opcode (n0 = WRITE; n3/n7/nF = READ/MAC).
              bit 3 = section marker, bit 2 = phase.

CHIP -> LANE mapping (V1.0 set, per ROMs/Lexicon PCM60/lexicon_pcm60.txt):
  v1_1 = U32 (offset LOW)   v1_2 = U35 (coefficient)
  v1_3 = U38 (offset HIGH)  v1_4 = U43 (control)

This module is parameterized by FIELD_MAP so the same machinery can be re-aimed at
sibling boxes (PCM70 U67, 224XL) with a per-device field table.
"""
from __future__ import annotations
import os, sys, struct
import numpy as np

# --------------------------------------------------------------------------- #
#  Configuration
# --------------------------------------------------------------------------- #
PCM60_DIR = os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
    "ROMs", "Lexicon PCM60",
)

# chip role -> filename (V1.0 clean set)
PCM60_LANES = {
    "U32": "lexicon_pcm60_v1_1.bin",  # offset low
    "U35": "lexicon_pcm60_v1_2.bin",  # coefficient
    "U38": "lexicon_pcm60_v1_3.bin",  # offset high
    "U43": "lexicon_pcm60_v1_4.bin",  # control
}

# Address-decode geometry (bit widths within the 4 KB / 12-bit ROM address)
STEP_BITS  = 7   # 128 steps
PARAM_BITS = 4   # 16 param frames
PROG_BITS  = 1   # 2 programs
N_STEPS    = 1 << STEP_BITS   # 128
N_PARAMS   = 1 << PARAM_BITS  # 16
N_PROGS    = 1 << PROG_BITS   # 2

OPCODE_MASK = 0x0F
SECTION_BIT = 0x08   # control bit 3
PHASE_BIT   = 0x04   # control bit 2


# --------------------------------------------------------------------------- #
#  Loading
# --------------------------------------------------------------------------- #
def load_pcm60(rom_dir: str = PCM60_DIR) -> dict[str, np.ndarray]:
    """Return {chip: uint8 array} for the four PCM60 lanes."""
    lanes = {}
    for chip, fn in PCM60_LANES.items():
        path = os.path.join(rom_dir, fn)
        lanes[chip] = np.fromfile(path, dtype=np.uint8)
    return lanes


def frame_index(program: int, param: int) -> tuple[int, int]:
    """Return (start, stop) byte slice in a lane for (program, param)."""
    base = (program << (PARAM_BITS + STEP_BITS)) | (param << STEP_BITS)
    return base, base + N_STEPS


# --------------------------------------------------------------------------- #
#  Decode one frame -> 128 step records
# --------------------------------------------------------------------------- #
def decode_frame(lanes: dict[str, np.ndarray], program: int, param: int) -> list[dict]:
    """Decode a single (program, param) frame into 128 microword step records."""
    a, b = frame_index(program, param)
    u32 = lanes["U32"][a:b]   # offset lo
    u35 = lanes["U35"][a:b]   # coeff
    u38 = lanes["U38"][a:b]   # offset hi
    u43 = lanes["U43"][a:b]   # control

    steps = []
    for s in range(N_STEPS):
        raw_off = (int(u38[s]) << 8) | int(u32[s])      # unsigned 16
        soff = raw_off - 0x10000 if raw_off & 0x8000 else raw_off  # signed
        delay = -soff
        coeff = int(u35[s])
        ctrl = int(u43[s])
        opcode = ctrl & OPCODE_MASK
        # Read/write is classified by the OFFSET SIGN (Phase-1 ground truth):
        # negative offset => read a delay tap (delay>0); positive => write target.
        # The opcode nibble correlates (writes cluster on n0/n8, reads on n3/n7/nB/nF)
        # but is kept as a separate annotation rather than the classifier.
        rw = "R" if delay > 0 else "W" if delay < 0 else "Z"
        steps.append(dict(
            step=s,
            offset=soff,
            delay=delay,
            coeff=coeff,
            coeff_f=coeff / 256.0,
            ctrl=ctrl,
            opcode=opcode,
            op3=opcode & 0x07,           # low 3 bits (core op, if bit3 is the section marker)
            section=bool(ctrl & SECTION_BIT),
            phase=bool(ctrl & PHASE_BIT),
            rw=rw,
        ))
    return steps


# --------------------------------------------------------------------------- #
#  Integrity / Phase-0 checks (reuse of phase0 analysis ideas)
# --------------------------------------------------------------------------- #
def shannon(b: np.ndarray) -> float:
    if len(b) == 0:
        return 0.0
    cnt = np.bincount(b, minlength=256).astype(float)
    p = cnt / cnt.sum(); p = p[p > 0]
    return float(-(p * np.log2(p)).sum())


def autocorr(b: np.ndarray, stride: int) -> float:
    if stride >= len(b):
        return 0.0
    return float((b[:-stride] == b[stride:]).mean())


def longest_ascii_run(b: np.ndarray) -> int:
    printable = ((b >= 0x20) & (b < 0x7F))
    runs = []; cur = 0
    for p in printable:
        if p: cur += 1
        else:
            if cur: runs.append(cur); cur = 0
    if cur: runs.append(cur)
    return max(runs) if runs else 0


def integrity_report(lanes: dict[str, np.ndarray]) -> dict:
    """Phase-0 integrity: distinctness, period-128 autocorr, fill, ASCII contamination."""
    rep = {}
    hashes = {}
    for chip, b in lanes.items():
        h = hash(b.tobytes())
        hashes[chip] = h
        rep[chip] = dict(
            size=len(b),
            entropy=round(shannon(b), 3),
            ff_pct=round(100 * float((b == 0xFF).mean()), 1),
            zero_pct=round(100 * float((b == 0x00).mean()), 1),
            ac128=round(autocorr(b, 128), 3),
            ac127=round(autocorr(b, 127), 3),
            ascii_run=longest_ascii_run(b),
            n_unique_frames=count_unique_frames(b),
        )
    rep["_distinct_images"] = (len(set(hashes.values())) == len(hashes))
    return rep


def count_unique_frames(b: np.ndarray) -> int:
    """Number of distinct 128-byte step-frames in a lane (32 frames total)."""
    nframes = len(b) // N_STEPS
    frames = {b[i * N_STEPS:(i + 1) * N_STEPS].tobytes() for i in range(nframes)}
    return len(frames)


# --------------------------------------------------------------------------- #
#  Topology summary for one program (across the default param frame)
# --------------------------------------------------------------------------- #
def program_tap_map(lanes: dict[str, np.ndarray], program: int, param: int = 0) -> dict:
    steps = decode_frame(lanes, program, param)
    reads = [s for s in steps if s["rw"] == "R"]   # negative offset => delay tap
    writes = [s for s in steps if s["rw"] == "W"]  # positive offset => write target
    # true reverb taps = distinct read delays, dropping the -1/-3 (0xFFFF/0xFFFD)
    # idle/sentinel markers (delay < SENTINEL_MAX) -> matches Phase-1's 68..27,100
    SENTINEL_MAX = 8
    tap_delays = sorted({s["delay"] for s in reads if s["delay"] >= SENTINEL_MAX})
    sentinels = sum(1 for s in reads if 0 < s["delay"] < SENTINEL_MAX)
    return dict(
        program=program, param=param,
        n_reads=len(reads), n_writes=len(writes),
        n_taps=len(tap_delays),
        tap_min=tap_delays[0] if tap_delays else None,
        tap_max=tap_delays[-1] if tap_delays else None,
        n_sentinels=sentinels,
        opcodes=_opcode_histogram(steps),
    )


def _opcode_histogram(steps):
    h = {}
    for s in steps:
        h[s["opcode"]] = h.get(s["opcode"], 0) + 1
    return sorted(h.items())


# --------------------------------------------------------------------------- #
#  Self-test against Phase-1 published results
# --------------------------------------------------------------------------- #
def verify_phase1(lanes: dict[str, np.ndarray]) -> None:
    print("=" * 72)
    print("PCM60 DECODER  --  Phase-1 verification")
    print("=" * 72)
    rep = integrity_report(lanes)
    print(f"distinct images: {rep['_distinct_images']}")
    for chip in ("U32", "U35", "U38", "U43"):
        r = rep[chip]
        print(f"  {chip}: {r['size']}B  H={r['entropy']}  ac128={r['ac128']}  "
              f"FF%={r['ff_pct']}  uniqFrames={r['n_unique_frames']}  asciiRun={r['ascii_run']}")

    print("\nGeometry expectations:")
    print(f"  U43 unique frames = {rep['U43']['n_unique_frames']}  (expect 2 = two programs)")
    print(f"  U43 ac128 = {rep['U43']['ac128']}  (expect ~0.98, strong period-128)")
    print(f"  U38 ac128 = {rep['U38']['ac128']}  (expect ~0.82)")

    print("\nProgram tap maps (param frame 0):")
    for prog in range(N_PROGS):
        tm = program_tap_map(lanes, prog, 0)
        print(f"  program {prog}: reads={tm['n_reads']} writes={tm['n_writes']} "
              f"taps(distinct read delays)={tm['n_taps']} "
              f"tapRange={tm['tap_min']}..{tm['tap_max']} samples "
              f"(sentinels={tm['n_sentinels']})")
        print(f"     opcode hist (nibble:count): "
              + ", ".join(f"{op:X}:{c}" for op, c in tm["opcodes"]))


def dump_frame(lanes, program, param, limit=N_STEPS):
    steps = decode_frame(lanes, program, param)
    print(f"\n--- program {program} param {param} : {limit} steps ---")
    print("step  off(signed)  delay   coeff(/256)   ctrl  op  rw  sec ph")
    for s in steps[:limit]:
        print(f"{s['step']:3d}   {s['offset']:7d}   {s['delay']:7d}   "
              f"0x{s['coeff']:02X}={s['coeff_f']:+.3f}   0x{s['ctrl']:02X}  "
              f"{s['opcode']:X}   {s['rw']}   {int(s['section'])}  {int(s['phase'])}")


if __name__ == "__main__":
    lanes = load_pcm60()
    verify_phase1(lanes)
    if "--dump" in sys.argv:
        dump_frame(lanes, 0, 0, 32)
