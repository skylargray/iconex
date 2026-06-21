#!/usr/bin/env python3
"""224XL v8_21 structural analysis: locate the ARU microcode within the NVS ROMs,
find the microword organization (period / byte-lane pairing), and map program data.

The 224 ARU is a VARIANT (two multiplier bits at once + a dedicated shift register)
and the program is ~100 steps (vs PCM60/70's 128).  NVS ROMs are NOT uniform
byte-lanes (entropy 4.2-7.0, FF% 0.1-42), so we look for: hi/lo pairings, the
~100-step period, region maps (code/strings/data/fill), and coefficient regions.
"""
from __future__ import annotations
import os, sys, glob
import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from pcm60_decode import shannon

DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                   "ROMs", "Lexicon 224", "224XL v8_21")


def load():
    out = {}
    for f in sorted(glob.glob(os.path.join(DIR, "NVS*.BIN"))):
        name = os.path.basename(f).split()[0]   # NVS1..NVS8
        out[name] = np.fromfile(f, dtype=np.uint8)
    return out


def autocorr(b, s):
    if s >= len(b): return 0.0
    nb = b[b != 0xFF]
    if len(nb) < 64: nb = b
    a, c = nb[:-s], nb[s:]
    return float((a == c).mean())


def region_map(b, win=256):
    """Coarse per-window entropy/FF map to spot code vs data vs fill transitions."""
    out = []
    for i in range(0, len(b), win):
        seg = b[i:i+win]
        out.append((i, round(shannon(seg), 2), round(100*float((seg == 0xFF).mean()))))
    return out


def main():
    roms = load()
    names = list(roms)
    print("#" * 78)
    print("# 224XL v8_21  NVS structural analysis")
    print("#" * 78)

    # ---- period scan per ROM over many strides (find ~100-step microword) ---- #
    print("\n=== per-ROM autocorrelation over candidate periods ===")
    strides = [80, 96, 100, 102, 104, 110, 120, 128, 192, 200, 204, 208, 220, 240,
               256, 300, 384, 400, 512]
    for nm in names:
        b = roms[nm]
        ac = {s: round(autocorr(b, s), 3) for s in strides}
        best = max(ac, key=ac.get)
        line = ", ".join(f"{s}:{ac[s]:.2f}" for s in strides)
        print(f"  {nm}: peak@{best}({ac[best]:.2f})  {line}")

    # ---- pairwise hi/lo offset sanity (which two ROMs form 16-bit offsets) ---- #
    print("\n=== pairwise hi/lo 16-bit reverb-sanity (offsets across ROM pairs) ===")
    def sane(hi, lo):
        n = min(len(hi), len(lo))
        raw = (hi[:n].astype(np.int32) << 8) | lo[:n].astype(np.int32)
        off = np.where(raw & 0x8000, raw - 0x10000, raw)
        delays = -off
        taps = delays[(delays >= 8) & (delays < 60000)]
        return len(np.unique(taps)), (int(taps.min()) if len(taps) else 0,
                                       int(taps.max()) if len(taps) else 0)
    best_pairs = []
    for i in range(len(names)):
        for j in range(len(names)):
            if i == j: continue
            d, rng = sane(roms[names[i]], roms[names[j]])
            best_pairs.append((d, names[i], names[j], rng))
    best_pairs.sort(reverse=True)
    for d, hi, lo, rng in best_pairs[:8]:
        print(f"  hi={hi} lo={lo}: distinct-taps={d} range={rng[0]}..{rng[1]}")

    # ---- region maps for a few key ROMs ---- #
    for nm in ["NVS3", "NVS8", "NVS1"]:
        print(f"\n=== region map {nm} (offset: entropy, FF%) ===")
        rm = region_map(roms[nm])
        for off, ent, ff in rm:
            bar = "#" * int(ent)
            print(f"  0x{off:04X}: H={ent:4.2f} FF%={ff:3d}  {bar}")

    # ---- look for the program-name table extent in NVS3 ---- #
    b3 = roms["NVS3"]
    print("\n=== NVS3 program-name region (first 256 bytes as text) ===")
    txt = "".join(chr(x) if 0x20 <= x < 0x7F else "." for x in b3[:256])
    for r in range(0, 256, 64):
        print(f"  0x{r:04X}: {txt[r:r+64]}")


if __name__ == "__main__":
    main()
