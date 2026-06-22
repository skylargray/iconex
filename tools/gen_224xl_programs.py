#!/usr/bin/env python3
"""Generate libs/sgdsp/include/sgdsp/reverb/224xl_programs.hpp from firmware.

Boots the v8.2.1 firmware for each requested program id, reads the 128-step WCS
image (mem[0x4000:0x4200]), and emits a header embedding the raw image + metadata.
Single source of truth: the C++ core and the Python reference read identical bytes.

Usage: python tools/gen_224xl_programs.py [id_hex ...]   (default: 0x01 CONCERT)
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import boot_xl as B

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(REPO, "libs", "sgdsp", "include", "sgdsp", "reverb", "224xl_programs.hpp")

# values must be valid C++ identifier fragments (no spaces); used as k<NAME>_WCS
NAMES = {0x01: "CONCERT_HALL"}  # extend as more programs are brought up


def wcs_image(power_up_id):
    cpu, mem, *_ = B.boot(power_up_id=power_up_id, verbose=False)
    return bytes(mem[0x4000:0x4200])  # 512 bytes


def emit(ids):
    progs = [(i, wcs_image(i)) for i in ids]
    lines = []
    lines.append("#pragma once")
    lines.append("// =============================================================================")
    lines.append("// sgdsp - Lexicon 224XL program WCS tables (GENERATED - do not edit by hand)")
    lines.append("// =============================================================================")
    lines.append("// Source: tools/gen_224xl_programs.py, firmware ROMs/Lexicon 224/224XL v8_21.")
    lines.append("// Each image is the 128-step microprogram (4 active-low bytes per step).")
    lines.append("")
    lines.append("#include <cstdint>")
    lines.append("")
    lines.append("namespace sgdsp::reverb::programs {")
    lines.append("")
    for pid, img in progs:
        assert len(img) == 512, f"bad image length {len(img)}"
        name = NAMES.get(pid, f"PROGRAM_{pid:02X}")
        lines.append(f"// power_up_id = 0x{pid:02X} ({name})")
        lines.append(f"static constexpr uint8_t k{name}_WCS[512] = {{")
        for row in range(0, 512, 16):
            chunk = ", ".join(f"0x{b:02X}" for b in img[row:row+16])
            lines.append(f"    {chunk},")
        lines.append("};")
        lines.append(f"static constexpr uint8_t k{name}_ID = 0x{pid:02X};")
        lines.append("")
    lines.append("}  // namespace sgdsp::reverb::programs")
    lines.append("")
    with open(OUT, "w", newline="\n") as f:
        f.write("\n".join(lines))
    print(f"wrote {OUT} ({len(progs)} program(s))")


if __name__ == '__main__':
    ids = [int(a, 16) for a in sys.argv[1:]] or [0x01]
    ids = list(dict.fromkeys(ids))   # de-dup, preserve order (avoid duplicate C++ definitions)
    emit(ids)
