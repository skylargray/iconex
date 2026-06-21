#!/usr/bin/env python3
"""Verify where the PCM70 delay-offsets / coefficients actually live.

Hypothesis (from U67 analysis): U67 holds ONLY static opcode/control/routing
planes (0-6) + a banner (plane 7).  The modulated coefficient/offset data is
slave-managed in the WCS, whose INITIAL values sub_02b6h lddr-copies from U95 ROM
0x2ACD-0x2C4C (3 x 128-byte planes) into WCS 0x8180/0x8280/0x8300.

This script:
  (1) dumps/【interprets the U95 0x2ACD region as candidate offset(16-bit)/coeff data;
  (2) tests whether it forms a sane reverb tap map (=> offsets live in U95);
  (3) per-BIT constancy analysis of the 7 U67 control planes (which bits are fixed
      opcode vs varying => coeff/sign sub-fields).
"""
from __future__ import annotations
import os, sys
import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from pcm60_decode import load_pcm60, frame_index, shannon

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
U95 = np.fromfile(os.path.join(ROOT, "ROMs", "Lexicon PCM70", "Lexicon_PCM-70-V2_0-U95.BIN"), dtype=np.uint8)
U67 = np.fromfile(os.path.join(ROOT, "ROMs", "Lexicon PCM70", "Lexicon_PCM-70-V2_0-U67.BIN"), dtype=np.uint8)[:0x400]


def signed16(hi, lo):
    raw = (hi.astype(np.int32) << 8) | lo.astype(np.int32)
    return np.where(raw & 0x8000, raw - 0x10000, raw)


def sane_taps(off):
    delays = -off
    taps = sorted(set(int(d) for d in delays if 8 <= d < 60000))
    return taps


def main():
    print("=" * 78)
    print("U95 ROM 0x2ACD-0x2C4C  (3 x 128-byte planes -> WCS 0x8180/0x8280/0x8300)")
    print("=" * 78)
    region = U95[0x2ACD:0x2ACD + 0x180]
    p = [region[i*128:(i+1)*128] for i in range(3)]
    for i, pl in enumerate(p):
        wcs = [0x8180, 0x8280, 0x8300][i]
        print(f"\n--- U95 plane {i} -> WCS 0x{wcs:04X}: "
              f"H={shannon(pl):.3f} std={pl.std():.1f} uniq={len(np.unique(pl))} "
              f"mean={pl.mean():.1f} min={pl.min()} max={pl.max()} ---")
        for r in range(0, 128, 16):
            print("   " + " ".join(f"{int(pl[r+k]):02X}" for k in range(16)))

    # Test pairings of these 3 planes as offset hi/lo
    print("\n=== reverb-sanity of U95-plane pairings as 16-bit offsets ===")
    for hi in range(3):
        for lo in range(3):
            if hi == lo:
                continue
            off = signed16(p[hi], p[lo])
            taps = sane_taps(off)
            if taps:
                print(f"  hi=U95p{hi} lo=U95p{lo}: taps={len(taps)} "
                      f"range={taps[0]}..{taps[-1]} neg/pos={int((off<0).sum())}/{int((off>0).sum())}")

    # Also test each plane alone as a "descending ramp / curve" (de-zipper table)
    print("\n=== monotonic-run check (de-zipper / coefficient curve signature) ===")
    for i, pl in enumerate(p):
        d = np.diff(pl.astype(np.int16))
        desc = int((d < 0).sum()); asc = int((d > 0).sum()); flat = int((d == 0).sum())
        print(f"  U95 plane {i}: descending steps={desc} ascending={asc} flat={flat} "
              f"(ramp if one direction dominates)")

    # ---- Per-bit constancy of the 7 U67 control planes ---- #
    print("\n" + "=" * 78)
    print("U67 control planes (0-6): per-bit constancy  (1=bit always set, 0=always clear,")
    print("  '.'=varies)  -> fixed bits are opcode/routing; varying low bits = coeff/sign field")
    print("=" * 78)
    print("plane  b7 b6 b5 b4 b3 b2 b1 b0   uniq  role-hint")
    for pidx in range(7):
        pl = U67[pidx*128:(pidx+1)*128]
        bits = []
        for b in range(7, -1, -1):
            col = (pl >> b) & 1
            if col.all():
                bits.append("1")
            elif not col.any():
                bits.append("0")
            else:
                bits.append(".")
        uniq = len(np.unique(pl))
        # crude hint: many varying low bits + few uniq => packed coeff/control
        print(f"  {pidx}     " + "  ".join(bits) + f"   {uniq:3d}")

    # Low-nibble vs high-nibble entropy per U67 plane (coeff sub-field detection)
    print("\n=== U67 planes: low-nibble vs high-nibble unique-count ===")
    for pidx in range(7):
        pl = U67[pidx*128:(pidx+1)*128]
        lo = len(np.unique(pl & 0x0F)); hi = len(np.unique(pl >> 4))
        print(f"  plane {pidx}: low-nib uniq={lo:2d}  high-nib uniq={hi:2d}  "
              f"low-nib vals={sorted(set(int(x) for x in (pl & 0x0F)))}")


if __name__ == "__main__":
    main()
