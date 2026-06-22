#!/usr/bin/env python3
"""Disassemble a range of the 224XL NVS window (0x8000-0xFFFF) at correct addresses.
Usage: python tools/disrange.py <start_hex> <end_hex>
"""
import os, sys
import numpy as np
from z80dis import z80

DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                   "ROMs", "Lexicon 224", "224XL v8_21")

def window():
    return np.concatenate([np.fromfile(os.path.join(DIR, f"NVS{n} 2732.BIN"), dtype=np.uint8)
                           for n in range(1, 9)])

def main():
    start = int(sys.argv[1], 16); end = int(sys.argv[2], 16)
    win = window()
    a = start
    while a < end:
        o = a - 0x8000
        try:
            d = z80.decode(bytes(win[o:o+4]), a)
            s = z80.disasm(d)
            raw = " ".join(f"{int(win[o+i]):02X}" for i in range(d.len))
            print(f"{a:04X}  {raw:<12}  {s}")
            a += max(1, d.len)
        except Exception as e:
            print(f"{a:04X}  {int(win[o]):02X}            ???")
            a += 1

if __name__ == "__main__":
    main()
