#!/usr/bin/env python3
"""224XL: build the 0x8000-0xFFFF NVS window, verify the ROM->window mapping, and
dump the per-program ARU records (0xB800 array, 21 x 0x2AA bytes) + the program
directory (0xA446) and name table (0xA000).

Window mapping (from the ARU-interface workflow): NVSn -> 0x8000 + (n-1)*0x1000.
"""
from __future__ import annotations
import os, sys
import numpy as np

DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                   "ROMs", "Lexicon 224", "224XL v8_21")


def build_window():
    """Concatenate NVS1..NVS8 -> 32 KB image mapped at 0x8000 (window[a-0x8000])."""
    parts = []
    for n in range(1, 9):
        parts.append(np.fromfile(os.path.join(DIR, f"NVS{n} 2732.BIN"), dtype=np.uint8))
    return np.concatenate(parts)


def at(win, addr, n):
    o = addr - 0x8000
    return win[o:o+n]


def text(b):
    return "".join(chr(x) if 0x20 <= x < 0x7F else "." for x in b)


def main():
    win = build_window()
    print(f"window {len(win)} bytes (0x8000-0x{0x8000+len(win)-1:04X})")

    # ---- sanity: name table at 0xA000 (NVS3) ----
    print("\n=== sanity check: 0xA000 should be the program-name table (NVS3) ===")
    print("  " + text(at(win, 0xA000, 96)))

    # ---- program directory at 0xA446 (5-byte entries) ----
    print("\n=== program directory @0xA446 (first 24 x 5-byte entries) ===")
    print("  idx: b0  b1  b2  b3  b4   (flags, group, sub, page-hi, page-lo/len)")
    for i in range(24):
        e = at(win, 0xA446 + i*5, 5)
        if len(e) < 5: break
        print(f"  {i:3d}: " + " ".join(f"{int(x):02X}" for x in e))

    # ---- record array at 0xB800: 21 x 0x2AA ----
    print("\n=== ARU program records @0xB800 (21 x 0x2AA=682 bytes) ===")
    REC = 0x2AA
    for k in range(21):
        rec = at(win, 0xB800 + k*REC, REC)
        if len(rec) < REC:
            print(f"  rec {k}: TRUNCATED ({len(rec)} bytes)"); break
        nonff = int((rec != 0xFF).sum())
        print(f"  rec {k:2d} @0x{0xB800+k*REC:04X}: id=0x{int(rec[0]):02X} "
              f"nonFF={nonff:3d} first16=[{' '.join('%02X'%int(x) for x in rec[:16])}]")

    # ---- detailed dump of record 0 ----
    print("\n=== record 0 full dump (682 bytes, 16/row) ===")
    rec = at(win, 0xB800, REC)
    for r in range(0, REC, 16):
        seg = rec[r:r+16]
        print(f"  +0x{r:03X}: " + " ".join(f"{int(x):02X}" for x in seg) + "   " + text(seg))


if __name__ == "__main__":
    main()
