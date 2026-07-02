#!/usr/bin/env python3
"""export_golden_224xl_rtl — golden exporter for the C++ RTL-parity harness (plan 024 F1d).

Runs the Python reference engine tools/aru_freerun22_rtl.py (class RTL22 — the pin-locked
complement-domain engine, sessions 0027/0028) and writes bit-exact goldens under
tools/harness/224xl/golden_rtl/ for the C++ core libs/sgdsp/include/sgdsp/reverb/224xl.hpp:

  <case>_wcs.bin    512 bytes — the stored WCS image (CPU word order, 4 bytes/word)
  <case>_in.bin     int16 LE, nsamp x 2 (h1, h2) — the EXACT input stream; the C++
                    harness reads this rather than regenerating the stimulus
  <case>_outs.bin   int16 LE, nsamp x 4 — per-frame CPU-domain outputs, channels
                    A,B,C,D interleaved (run_free semantics: last write wins,
                    unwritten channel -> 0 that frame)
  <case>_trace.bin  int64 LE flat records {step, ACC, RES, DAB, R0, R1, R2, R3}
                    (phys patterns, state AFTER each step) for the first
                    trace_frames frames — (L+1) records per frame
  <case>_meta.json  nsamp, trace_frames, L, w_reset, fs_hz, stimulus spec

Cases (trace_frames = 3 for all):
  d1zero   wcs_diag.json["zero"]  — stereo h1-only impulse amp 16000 at frame 50,
           nsamp = 50 + 1 + 600            (lag 1)
  d1max    wcs_diag.json["max"]   — same impulse, nsamp = 50 + 0x3FFF + 600
  concert  wcs_settled_concert.json — mono 0.30 s noise burst (numpy
           default_rng(224), integers -8000..8001) then silence, nsamp = 66000
           (deliberately crossing the 65536-frame CPC wrap)
  sig6     wcs_diag.json["sig6"] (diag-6 FPC SIGNAT) — zero input, XREG_host =
           0xFAAA (meta key "xreg_host"), nsamp = 400: the XREG host-latch
           boundary golden (ch D = -1366 steady, A/B/C = 0)

Also writes booth_vectors.bin — primitive vectors for the gate-array port:
  header  <4sII>  magic b"B224", n_raw (4000), n_be (200)
  n_raw x <HB3I>  {opnd_phys u16, cmag u8, rawA, rawB, rawC u32}   from raw3()
  n_be  x <IIBI>  {acc u32, raw u32, cs u8, out u32}               from backend20()
                  (constructed so both SAT clamp branches 0xC0000/0x3FFFF appear)

Run from the repo root:  python tools/export_golden_224xl_rtl.py [case ...]
(default: all three cases + booth_vectors)
"""
import json
import os
import random
import struct
import sys

import numpy as np

TOOLS = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, TOOLS)
from aru_freerun22_rtl import RTL22, program_rows22, raw3, backend20, fs22  # noqa: E402

PROBES = os.path.join(TOOLS, "session0022_probes")
OUTDIR = os.path.join(TOOLS, "harness", "224xl", "golden_rtl")

TRACE_FRAMES = 3


class TracedRTL22(RTL22):
    """RTL22 with a per-step phys-state trace for the first trace_frames frames.
    Records (step-in-frame, ACC, RES, DAB, R0..R3) AFTER each step completes —
    exactly what Lexicon224XLCore::processFrameTraced records."""

    def __init__(self, trace_frames):
        super().__init__()
        self.trace_frames = trace_frames
        self.trace = []

    def step(self, d, audio_in, probe=None, fidx=0, sidx=0):
        out = super().step(d, audio_in, probe=probe, fidx=fidx, sidx=sidx)
        if self.sample_count < self.trace_frames:
            self.trace.append((sidx, self.ACC, self.RES, self.DAB,
                               self.R[0], self.R[1], self.R[2], self.R[3]))
        return out


def load_wcs(path, key=None):
    rec = json.load(open(path))
    if key is not None:
        rec = rec[key]
    b = bytes.fromhex(rec["wcs"])
    assert len(b) == 512, len(b)
    return b


def wcs_tuples(b):
    return [(b[4 * k], b[4 * k + 1], b[4 * k + 2], b[4 * k + 3]) for k in range(128)]


def export_case(name, wcs_bytes, h1, h2, nsamp, stimulus, xreg_host=None, check=None):
    rows, L, w_reset = program_rows22(wcs_tuples(wcs_bytes))
    fs = fs22(L)
    assert len(h1) == len(h2) == nsamp

    # the exact input stream the C++ harness will read back (int16 LE, h1/h2 interleaved)
    in_arr = np.zeros((nsamp, 2), dtype="<i2")
    in_arr[:, 0] = np.asarray(h1, dtype=np.int64).astype("<i2")
    in_arr[:, 1] = np.asarray(h2, dtype=np.int64).astype("<i2")

    # drive the engine with EXACTLY those samples, as (h1, h2) pairs
    sig = [(int(a) & 0xFFFF, int(b) & 0xFFFF) for a, b in in_arr]
    eng = TracedRTL22(TRACE_FRAMES)
    if xreg_host is not None:
        eng.XREG_host = xreg_host          # host->DSP latch, CPU-domain value
    chans = eng.run_free(rows, sig, nsamp)

    outs = np.zeros((nsamp, 4), dtype="<i2")
    for ci, c in enumerate("ABCD"):
        outs[:, ci] = np.asarray(chans[c], dtype=np.int64).astype("<i2")

    trace = np.asarray(eng.trace, dtype="<i8")
    assert trace.shape == (TRACE_FRAMES * (L + 1), 8), trace.shape
    if check is not None:
        check(outs)                        # case sanity gate BEFORE any file is written

    base = os.path.join(OUTDIR, name + "_")
    with open(base + "wcs.bin", "wb") as f:
        f.write(wcs_bytes)
    with open(base + "in.bin", "wb") as f:
        f.write(in_arr.tobytes())
    with open(base + "outs.bin", "wb") as f:
        f.write(outs.tobytes())
    with open(base + "trace.bin", "wb") as f:
        f.write(trace.tobytes())
    meta = {
        "case": name,
        "nsamp": nsamp,
        "trace_frames": TRACE_FRAMES,
        "L": L,
        "w_reset": w_reset,
        "frame_steps": L + 1,
        "fs_hz": fs,
        "stimulus": stimulus,
        "in_format": "int16le nsamp x 2 (h1,h2)",
        "outs_format": "int16le nsamp x 4 (A,B,C,D; last-write-wins, unwritten=0)",
        "trace_format": "int64le (step,ACC,RES,DAB,R0,R1,R2,R3) x trace_frames*(L+1); phys, post-step",
    }
    if xreg_host is not None:
        meta["xreg_host"] = xreg_host      # harness calls setXregHost(value) after loadProgram
    with open(base + "meta.json", "w") as f:
        json.dump(meta, f, separators=(",", ":"))
    nz = int(np.count_nonzero(outs))
    print(f"  {name:8s} L={L} w_reset={w_reset} fs={fs:.1f} Hz nsamp={nsamp} "
          f"trace={trace.shape[0]} recs nonzero-outs={nz}")
    return L


def case_d1(name, key, lag):
    wcs = load_wcs(os.path.join(PROBES, "wcs_diag.json"), key)
    AMP, T0 = 16000, 50
    nsamp = T0 + lag + 600
    h1 = np.zeros(nsamp, dtype=np.int64)
    h1[T0] = AMP
    h2 = np.zeros(nsamp, dtype=np.int64)
    export_case(name, wcs, h1, h2, nsamp,
                {"kind": "impulse-h1only", "amp": AMP, "t0": T0, "lag": lag})


def case_concert():
    wcs = load_wcs(os.path.join(PROBES, "wcs_settled_concert.json"))
    rows, L, w_reset = program_rows22(wcs_tuples(wcs))
    fs = fs22(L)
    nsamp = 66000                       # crosses the 65536-frame CPC wrap on purpose
    nb = int(0.30 * fs)
    rng = np.random.default_rng(224)
    sig = np.zeros(nsamp, dtype=np.int64)
    sig[:nb] = rng.integers(-8000, 8001, nb)
    export_case("concert", wcs, sig, sig, nsamp,   # mono: both halves carry the signal
                {"kind": "noise-burst-mono", "seed": 224, "lo": -8000, "hi": 8000,
                 "burst_frames": nb, "burst_s": 0.30})


def case_sig6():
    """The diag-6 FPC-signature image: the XREG host-latch golden (the one datapath
    boundary the first three cases never drive). Zero input, regfile left at its
    default init (phys 0xFFFF = CPU 0), XREG_host parked at 0xFAAA: the program's
    SRC_XREG read word (CPU w76) unity-MACs the latch to WR-DA channel D each frame,
    so from frame 2 on (steady, f2_fpc_foundations.py) ch D = s16(0xFAAA) = -1366
    and ch A/B/C = 0 (unity captures of the CPU-0 default registers)."""
    XREG = 0xFAAA
    nsamp = 400

    def check(outs):
        exp_d = np.int16(XREG - 0x10000)               # s16(0xFAAA) = -1366
        assert (outs[2:, 3] == exp_d).all(), \
            ("sig6 ch D != XREG constant", np.unique(outs[2:, 3]))
        assert (outs[2:, :3] == 0).all(), \
            ("sig6 ch A/B/C != 0", [np.unique(outs[2:, c]) for c in range(3)])
        print(f"  sig6 sanity: ch D = {int(exp_d)} (0x{XREG:04X}) frames 2..{nsamp - 1}, "
              f"A/B/C = 0  -- OK")

    wcs = load_wcs(os.path.join(PROBES, "wcs_diag.json"), "sig6")
    z = np.zeros(nsamp, dtype=np.int64)
    export_case("sig6", wcs, z, z, nsamp,
                {"kind": "zero-mono-xreg", "xreg_host_hex": f"0x{XREG:04X}"},
                xreg_host=XREG, check=check)


def export_booth_vectors():
    """Primitive vectors: 4000 raw3 records + 200 backend20 records (SAT-covering)."""
    rnd = random.Random(224)
    blob = bytearray()
    N_RAW, N_BE = 4000, 200
    blob += struct.pack("<4sII", b"B224", N_RAW, N_BE)
    for _ in range(N_RAW):
        opnd = rnd.randrange(0, 0x10000)
        cmag = rnd.randrange(0, 64)
        a, b, c = raw3(opnd, cmag)
        blob += struct.pack("<HB3I", opnd, cmag, a, b, c)
    n_sat_hi = n_sat_lo = 0
    for i in range(N_BE):
        cs = rnd.randrange(2)
        raw = rnd.randrange(0, 1 << 20)
        if i % 2 == 0:
            acc = rnd.randrange(0, 1 << 20)          # random walk of the adder
        else:
            # constructed SAT hit: target the 20-bit sum into a s19^s18 band
            band = rnd.choice((0x40000, 0x80000))
            target = band + rnd.randrange(0, 0x40000)
            xorb = raw ^ (0xFFFFF if cs else 0)
            acc = (target - xorb - (1 - cs)) & 0xFFFFF
        out = backend20(acc, raw, cs)
        if out == 0x3FFFF:
            n_sat_hi += 1
        elif out == 0xC0000:
            n_sat_lo += 1
        blob += struct.pack("<IIBI", acc, raw, cs, out)
    assert n_sat_hi > 10 and n_sat_lo > 10, (n_sat_hi, n_sat_lo)
    path = os.path.join(OUTDIR, "booth_vectors.bin")
    with open(path, "wb") as f:
        f.write(blob)
    print(f"  booth_vectors: {N_RAW} raw3 + {N_BE} backend20 "
          f"(clamps: +rail {n_sat_hi}, -rail {n_sat_lo}) -> {os.path.basename(path)}")


CASES = {
    "d1zero": lambda: case_d1("d1zero", "zero", 1),
    "d1max": lambda: case_d1("d1max", "max", 0x3FFF),
    "concert": case_concert,
    "sig6": case_sig6,
    "booth_vectors": export_booth_vectors,
}


def main(argv):
    os.makedirs(OUTDIR, exist_ok=True)
    names = argv[1:] if len(argv) > 1 else list(CASES)
    print(f"### export_golden_224xl_rtl -> {OUTDIR}")
    for n in names:
        if n not in CASES:
            print(f"unknown case '{n}' (have: {', '.join(CASES)})")
            return 2
        CASES[n]()
    print("done")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
