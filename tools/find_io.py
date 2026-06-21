#!/usr/bin/env python3
"""Scan a Z80 ROM for I/O and block-move instructions to locate hardware drivers
(the ARU interface in the 224XL).  Reports OUT/IN port usage + ldir/lddr sites.

Usage: python tools/find_io.py "<rom path>" [base_hex]   (base = load address, default 0)
"""
from __future__ import annotations
import sys
import numpy as np
from z80dis import z80


def scan(path, base=0):
    b = np.fromfile(path, dtype=np.uint8)
    n = len(b)
    out_ports = {}; in_ports = {}; block = []
    a = 0
    insns = 0
    while a < n:
        try:
            d = z80.decode(bytes(b[a:a+4]), base + a)
            s = z80.disasm(d)
        except Exception:
            a += 1; continue
        op = b[a]
        if op == 0xD3:                      # OUT (n),A
            port = int(b[a+1]) if a+1 < n else -1
            out_ports[port] = out_ports.get(port, 0) + 1
        elif op == 0xDB:                    # IN A,(n)
            port = int(b[a+1]) if a+1 < n else -1
            in_ports[port] = in_ports.get(port, 0) + 1
        elif op == 0xED and a+1 < n and b[a+1] in (0xB0, 0xB8, 0xA0, 0xA8):
            kind = {0xB0: 'ldir', 0xB8: 'lddr', 0xA0: 'ldi', 0xA8: 'ldd'}[b[a+1]]
            block.append((base + a, kind))
        elif op == 0xED and a+1 < n and b[a+1] in (0x79, 0x41):  # OUT (C),A / OUT (C),B
            out_ports['(C)'] = out_ports.get('(C)', 0) + 1
        elif op == 0xED and a+1 < n and b[a+1] in (0x78, 0x40):  # IN A,(C) / IN B,(C)
            in_ports['(C)'] = in_ports.get('(C)', 0) + 1
        insns += 1
        a += max(1, d.len)
    return out_ports, in_ports, block, n, insns


def main():
    if len(sys.argv) < 2:
        print("usage: python tools/find_io.py <rom> [base_hex]"); return
    path = sys.argv[1]
    base = int(sys.argv[2], 16) if len(sys.argv) > 2 else 0
    op, ip, block, n, insns = scan(path, base)
    print(f"{path}  ({n}B, base 0x{base:04X}, ~{insns} linear insns)")
    def fmt(d):
        return ", ".join(f"{('0x%02X'%p) if isinstance(p,int) else p}:{c}"
                         for p, c in sorted(d.items(), key=lambda kv: -kv[1]))
    print(f"  OUT ports: {fmt(op)}")
    print(f"  IN  ports: {fmt(ip)}")
    print(f"  block moves ({len(block)}): " +
          ", ".join(f"{a:04X}:{k}" for a, k in block[:20]))


if __name__ == "__main__":
    main()
