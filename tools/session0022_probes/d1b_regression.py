#!/usr/bin/env python3
"""D1b regression — CONCERT mono behavior through RTL22 must be bit-identical before/after
the stereo-input extension. Renders a fixed 20k-sample burst through the boot image and
prints a sha256 per channel. Run pre-edit, save digests; run post-edit, diff."""
import sys, os, json, hashlib

TOOLS = r"d:\OneDrive\Gray Instruments\iconex\tools"
sys.path.insert(0, TOOLS)
HERE = os.path.dirname(os.path.abspath(__file__))

import numpy as np
from aru_freerun22_rtl import RTL22, program_rows22

rec = json.load(open(os.path.join(HERE, "wcs_cache.json")))["1"]
b = bytes.fromhex(rec["wcs"])
rows, L, w_reset = program_rows22([(b[4*k], b[4*k+1], b[4*k+2], b[4*k+3]) for k in range(128)])
assert (L, w_reset) == (104, 24)

N = 20000
rng = np.random.default_rng(224)
exc = np.zeros(N, dtype=np.int16)
exc[:5000] = rng.integers(-8000, 8001, 5000).astype(np.int16)

eng = RTL22()
chans = eng.run_free(rows, exc, N)
for c in "ABCD":
    h = hashlib.sha256(np.asarray(chans[c], dtype=np.int64).tobytes()).hexdigest()[:16]
    print(f"ch{c}: {h}")

# stereo-tuple path (post-edit only): mono x == tuple (x, x) must be bit-identical too
try:
    eng2 = RTL22()
    ch2 = eng2.run_free(rows, [(int(x), int(x)) for x in exc], N)
    same = all(chans[c] == ch2[c] for c in "ABCD")
    print(f"tuple(x,x) == mono x: {'IDENTICAL' if same else 'MISMATCH'}")
except TypeError as e:
    print(f"tuple input unsupported (pre-edit engine): {e}")
