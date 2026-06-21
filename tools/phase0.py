#!/usr/bin/env python3
"""Reusable Phase-0 integrity + classification battery (the discipline that caught
the corrupted V2.0 PCM60 set).  Generalizes PCM70_phase0_analysis.py to any dump
directory.

For each ROM in a directory it reports: size, MD5, entropy, FF/00 fill, top bytes,
ASCII contamination (Intel-HEX records + longest printable run + banner strings),
Z80 opcode density + RST-vector check, mirror/alias self-compare, microword-stride
autocorrelation, and a heuristic classification (Z80 code / microcode / data / blank).
Cross-file dedupe groups identical images.

Usage:  python tools/phase0.py "ROMs/Lexicon 224/224XL v8_21"
        python tools/phase0.py "<dir>" --stride            # extra stride scan
"""
from __future__ import annotations
import os, sys, glob, hashlib, re
import numpy as np

try:
    from z80dis import z80
    HAVE_Z80 = True
except Exception:
    HAVE_Z80 = False


def shannon(b):
    if len(b) == 0:
        return 0.0
    c = np.bincount(b, minlength=256).astype(float)
    p = c / c.sum(); p = p[p > 0]
    return float(-(p * np.log2(p)).sum())


def longest_printable(b):
    pr = ((b >= 0x20) & (b < 0x7F))
    runs = []; cur = 0
    for x in pr:
        if x: cur += 1
        else:
            if cur: runs.append(cur); cur = 0
    if cur: runs.append(cur)
    return max(runs) if runs else 0


def extract_strings(b, minlen=5):
    out = []; cur = bytearray(); start = 0
    for i, x in enumerate(b):
        if 0x20 <= x < 0x7F:
            if not cur: start = i
            cur.append(x)
        else:
            if len(cur) >= minlen: out.append((start, cur.decode('ascii', 'replace')))
            cur = bytearray()
    if len(cur) >= minlen: out.append((start, cur.decode('ascii', 'replace')))
    return out


def intel_hex_records(strings):
    return [t for t in strings if re.match(r':[0-9A-Fa-f]{6,}', t[1])]


def mirror_check(b):
    n = len(b); out = {}
    for div in (2, 4):
        seg = n // div
        if seg == 0: continue
        s0 = b[:seg]
        out[div] = [round(float((s0 == b[k*seg:(k+1)*seg]).mean()), 3) for k in range(1, div)]
    return out


def z80_validity(b, sample=2048):
    """Fraction of a linear decode that produces non-illegal opcodes (rough code signal)."""
    if not HAVE_Z80:
        return None
    a = 0; ok = 0; tot = 0; lim = min(len(b), sample)
    while a < lim:
        try:
            d = z80.decode(bytes(b[a:a+4]), a)
            s = z80.disasm(d)
            tot += 1
            if s and 'defb' not in s.lower() and '???' not in s and 'illegal' not in s.lower():
                ok += 1
            a += max(1, d.len)
        except Exception:
            a += 1; tot += 1
    return round(ok / max(1, tot), 3)


def rst_vector_signal(b):
    """Z80 code often has JP/JR/RST-ish bytes on the 8-byte RST grid 0x00..0x38."""
    if len(b) < 0x40:
        return 0
    grid = [int(b[a]) for a in range(0, 0x40, 8)]
    # 0xC3=JP, 0x18=JR, 0xC9=RET, 0xF3=DI, 0x00=NOP
    hits = sum(1 for g in grid if g in (0xC3, 0x18, 0xC9, 0xF3))
    return hits


def autocorr(b, s):
    if s >= len(b): return 0.0
    return round(float((b[:-s] == b[s:]).mean()), 3)


def classify(b, ent, ff, z80v, rst, asciirun):
    if ff > 0.95:
        return "BLANK/unprogrammed"
    if asciirun > 40 and ent < 3:
        return "ASCII/text (or contamination)"
    if z80v is not None and z80v > 0.80 and rst >= 2 and ent > 3.5:
        return "Z80 CODE (likely)"
    if 3.0 < ent < 6.0 and (z80v is None or z80v < 0.7):
        # structured but not clean code -> microcode/coefficient/data
        return "microcode/data (structured)"
    if ent >= 7.0:
        return "high-entropy (compressed/encrypted/data)"
    return "ambiguous"


def analyze_file(path, do_stride=False):
    b = np.fromfile(path, dtype=np.uint8)
    n = len(b)
    md5 = hashlib.md5(b.tobytes()).hexdigest()
    ent = shannon(b)
    ff = float((b == 0xFF).mean()); zz = float((b == 0x00).mean())
    strings = extract_strings(b)
    hexrec = intel_hex_records(strings)
    asciirun = longest_printable(b)
    z80v = z80_validity(b)
    rst = rst_vector_signal(b)
    hist = np.bincount(b, minlength=256)
    top = [f"{v:02X}:{int(hist[v])}" for v in np.argsort(hist)[::-1][:5]]
    mir = mirror_check(b)
    cls = classify(b, ent, ff, z80v, rst, asciirun)
    banners = [s for s in strings if len(s[1]) >= 8][:6]

    print(f"\n{'='*78}\n{os.path.basename(path)}  ({n}B={n//1024}KB)  md5={md5[:12]}")
    print(f"  entropy={ent:.3f}  FF%={100*ff:.1f}  00%={100*zz:.1f}  top={top}")
    print(f"  z80-valid-frac={z80v}  rst-grid-hits={rst}/8  asciiRun={asciirun}  "
          f"intelHEXrecs={len(hexrec)} {'<-- CONTAMINATION' if hexrec else ''}")
    print(f"  mirror self-compare {mir}  (>~0.9 on a half => address-line alias)")
    print(f"  >>> CLASS: {cls}")
    if banners:
        print("  strings: " + " | ".join(f"@{o:04X}:{t[:40]}" for o, t in banners))
    if do_stride:
        strides = [16, 32, 48, 64, 80, 96, 100, 128, 160, 192, 200, 256]
        ac = {s: autocorr(b[b != 0xFF] if ff > 0.3 else b, s) for s in strides}
        best = max(ac, key=ac.get)
        print("  stride autocorr: " + ", ".join(f"{s}:{ac[s]}" for s in strides))
        print(f"  >>> peak stride ~ {best} (candidate microword/period)")
    return md5, n


def main():
    if len(sys.argv) < 2:
        print("usage: python tools/phase0.py <rom_dir> [--stride]"); return
    root = sys.argv[1]
    do_stride = "--stride" in sys.argv
    files = sorted([f for f in glob.glob(os.path.join(root, "*"))
                    if f.lower().endswith((".bin",)) and os.path.isfile(f)])
    if not files:
        print(f"no .bin files in {root}"); return
    print("#" * 78)
    print(f"# PHASE-0 BATTERY: {root}  ({len(files)} files)")
    print("#" * 78)
    hashes = {}
    for f in files:
        md5, n = analyze_file(f, do_stride)
        hashes.setdefault(md5, []).append(os.path.basename(f))
    print("\n" + "=" * 78)
    print("CROSS-FILE DEDUPE (identical images share a group):")
    dupes = {h: g for h, g in hashes.items() if len(g) > 1}
    if dupes:
        for h, g in dupes.items():
            print(f"  DUPLICATE md5={h[:12]}: {g}  <-- distinct-image check FAILS for these")
    else:
        print("  all images distinct (good)")


if __name__ == "__main__":
    main()
