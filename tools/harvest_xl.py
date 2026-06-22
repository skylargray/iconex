#!/usr/bin/env python3
"""Harvest the complete 224XL v8.2.1 record -> name + reverb-algorithm mapping.

For each of the 21 coefficient/microcode records in the @0xB800 array:
  - name + bank/program: boot the REAL firmware with that record's selector ID as the
    power-up program (tools/boot_xl.boot(power_up_id=...)) and read the LARC display
    the firmware transmits (authoritative -- the firmware does the ID->name link).
  - delays + coefficient gains: run the proven build engine on the record
    (tools/aru224_emulate) at the CORRECT base (firmware page-wrap walk: stride 0x2AA,
    +2 whenever low byte hits 0xFE -- the routine at SBC 0x1343-0x135A).
"""
import sys, os, json
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from collections import Counter
import boot_xl as B
import aru224_emulate as A

MEM = B.load_mem()


def record_bases(n=21):
    """Firmware record-array walk (SBC 0x1343): HL=0xB800, +0x2AA, +2 if L==0xFE."""
    bases = []
    hl = 0xB800
    for _ in range(n):
        bases.append(hl)
        hl = (hl + 0x2AA) & 0xFFFF
        if (hl & 0xFF) == 0xFE:
            hl = (hl + 2) & 0xFFFF
    return bases


def decode_algo(base):
    """delays (tap_map) + coefficient gains (capture_coeffs) for a record."""
    offs = A.tap_map(base, verbose=False)
    # active program = up to the first >=6-long run of -1 (0xFFFF) fill
    fs = len(offs); run = 0
    for i, v in enumerate(offs):
        if v == -1:
            run += 1
            if run >= 6:
                fs = i - run + 1; break
        else:
            run = 0
    active = offs[:fs]
    delays = [abs(v) for v in active if 16 <= abs(v) < 0x4000]
    cnt = Counter(delays)
    loop = cnt.most_common(1)[0] if cnt else (0, 0)
    pairs = sorted(d for d, c in cnt.items() if c >= 2 and d != loop[0])
    s, ln = A.longest_monotonic_run([abs(v) for v in (-x for x in active)])
    # coefficient gains (sign-magnitude / 127)
    cf = A.capture_coeffs(base)
    gains = []
    seen = set()
    for de, b in cf:
        if b in seen:
            continue
        seen.add(b)
        sign = -1 if b & 0x80 else 1
        gains.append(round(sign * (b & 0x7F) / 127.0, 3))
    fe_path = MEM[(base + 0x30) & 0xFFFF] == 0xFE
    return dict(fe_path=fe_path, delays_decoded=len(cnt) > 0,
                active_steps=fs, distinct_taps=len(cnt),
                rng=[min(cnt) if cnt else 0, max(cnt) if cnt else 0],
                loop_tap=loop[0], loop_count=loop[1], pairs=len(pairs),
                out_line_len=ln, n_coeffs=len(cf), distinct_gains=sorted(set(gains)))


def harvest_name(idv):
    cpu, mem, larc, aru, ms, _off, _snap = B.boot(power_up_id=idv, verbose=False)
    name = B.ascii7(mem[0x3F4F:0x3F5B]).strip()
    meta = B.ascii7(mem[0x3F5B:0x3F73]).strip()     # "Bx Px Vx ... param labels"
    return name, meta, ms.get('mainloop')


def main():
    bases = record_bases()
    rows = []
    print(f"{'rec':>3} {'base':>6} {'ID':>4}  {'name':<14} {'bank/prog/params':<26} "
          f"{'steps':>5} {'taps':>4} {'range(samp)':>14} {'loopx':>10}")
    for k, base in enumerate(bases):
        idv = MEM[base]
        if idv == 0xFF:                  # directory/array terminator, not a real program
            print(f"{k:>3} 0x{base:04X} 0x{idv:02X}  (terminator -- end of record array)")
            continue
        name, meta, ml = harvest_name(idv)
        algo = decode_algo(base)
        rng = f"{algo['rng'][0]}..{algo['rng'][1]}"
        loopx = f"{algo['loop_tap']}x{algo['loop_count']}"
        print(f"{k:>3} 0x{base:04X} 0x{idv:02X}  {name:<14} {meta:<26} "
              f"{algo['active_steps']:>5} {algo['distinct_taps']:>4} {rng:>14} {loopx:>10}")
        rows.append(dict(rec=k, base=base, id=idv, name=name, meta=meta, **algo))
    out = os.path.join(os.path.dirname(__file__), "..", "docs", "reference", "224",
                       "224XL_record_name_map.json")
    with open(out, "w") as f:
        json.dump(rows, f, indent=2)
    print(f"\nwrote {os.path.abspath(out)}")
    # gains detail
    print("\n=== coefficient gains per record (sign-mag/127) ===")
    for r in rows:
        print(f"  rec{r['rec']:2d} {r['name']:<14}: {r['distinct_gains']}")
    return rows


if __name__ == "__main__":
    main()
