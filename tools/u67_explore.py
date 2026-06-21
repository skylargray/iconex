#!/usr/bin/env python3
"""Deeper U67 exploration: plane-major vs interleaved slicing, cross-column
similarity, per-step dump, and offset-pair tap extraction.  Used to nail the
plane field-map (carry-over 1)."""
from __future__ import annotations
import os, sys
import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from pcm60_decode import load_pcm60, frame_index, shannon

U67_PATH = os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
    "ROMs", "Lexicon PCM70", "Lexicon_PCM-70-V2_0-U67.BIN",
)
RAW = np.fromfile(U67_PATH, dtype=np.uint8)[:0x400]   # active 1 KB


def cols_plane_major():
    return [RAW[p * 128:(p + 1) * 128] for p in range(8)]


def cols_interleaved():
    # 128 steps x 8 bytes/step, column j = byte j of each step
    return [RAW[j::8][:128] for j in range(8)]


def signed16(hi, lo):
    raw = (hi.astype(np.int32) << 8) | lo.astype(np.int32)
    return np.where(raw & 0x8000, raw - 0x10000, raw)


def offset_pair_search(cols, label):
    print(f"\n=== offset hi/lo search [{label}] ===")
    res = []
    for ph in range(8):
        for pl in range(8):
            if ph == pl:
                continue
            if (cols[ph] == 0xFF).mean() > 0.9 or (cols[pl] == 0xFF).mean() > 0.9:
                continue
            off = signed16(cols[ph], cols[pl])
            delays = -off
            taps = delays[(delays >= 8) & (delays < 60000)]
            distinct = len(np.unique(taps))
            mx = int(taps.max()) if len(taps) else 0
            sane = 200 < mx < 40000
            score = (distinct / 128.0) * (1.0 if sane else 0.15)
            res.append((score, ph, pl, distinct, int(taps.min()) if len(taps) else 0, mx,
                        int((off < 0).sum()), int((off > 0).sum())))
    res.sort(reverse=True)
    for score, ph, pl, d, mn, mx, nneg, npos in res[:5]:
        print(f"  hi=c{ph} lo=c{pl}: score={score:.3f} taps={d} range={mn}..{mx} "
              f"neg/pos={nneg}/{npos}")
    return res[0]


def corr_matrix(cols, label):
    print(f"\n=== cross-column byte-match-rate matrix [{label}] ===")
    print("     " + " ".join(f"c{j}" for j in range(8)))
    for i in range(8):
        row = []
        for j in range(8):
            row.append(f"{float((cols[i] == cols[j]).mean()):.2f}")
        print(f"  c{i} " + "   ".join(row))


def dump_steps(cols, label, n=32):
    print(f"\n=== per-step dump [{label}] steps 0..{n-1} (8 columns hex) ===")
    print("step  " + " ".join(f" c{j}" for j in range(8)))
    for s in range(n):
        print(f"{s:3d}   " + " ".join(f"{int(cols[j][s]):02X}" for j in range(8)))


def main():
    pm = cols_plane_major()
    il = cols_interleaved()

    for cols, label in [(pm, "PLANE-MAJOR"), (il, "INTERLEAVED")]:
        print("#" * 70)
        print(f"# {label}")
        print("#" * 70)
        for j in range(8):
            c = cols[j]
            print(f"  c{j}: H={shannon(c):.3f} std={c.std():.1f} uniq={len(np.unique(c))} "
                  f"mean={c.mean():.1f} nonFF={int((c!=0xFF).sum())} "
                  f"top={[f'{v:02X}:{int((c==v).sum())}' for v in np.argsort(np.bincount(c,minlength=256))[::-1][:4]]}")
        best = offset_pair_search(cols, label)
        corr_matrix(cols, label)

    # Detailed look at the winning plane-major interpretation
    print("\n" + "=" * 70)
    print("PLANE-MAJOR per-step dump (the established slicing)")
    print("=" * 70)
    dump_steps(pm, "PLANE-MAJOR", 40)

    # Plane 7 full content (the outlier)
    print("\n=== plane 7 (0x380) full 128 bytes ===")
    for r in range(0, 128, 16):
        print(f"  {r:3d}: " + " ".join(f"{int(pm[7][r+i]):02X}" for i in range(16)))

    # Best offset pair -> full tap list
    print("\n=== plane3(hi):plane6(lo) decoded delays (full 128 steps) ===")
    off = signed16(pm[3], pm[6])
    delays = -off
    line = []
    for s in range(128):
        line.append(f"{delays[s]:+6d}")
        if (s + 1) % 8 == 0:
            print("  " + " ".join(line)); line = []
    taps = sorted(set(int(d) for d in delays if 8 <= d < 60000))
    print(f"\n  distinct positive delays (taps>=8): {len(taps)}")
    print(f"  tap list: {taps}")


if __name__ == "__main__":
    main()
