#!/usr/bin/env python3
"""Pin down s=94: is it an FPC output (should it be a sink) or a genuine recirculation read?

s=94 (off=0xb31f, WA=3, b3=0, XFER=0, bit15=1) is the ONLY 'candidate' whose read drives
the +1126->-198 ppm flip. We must decide on PRINCIPLE whether it is FPC-output or a real tap.

Tests:
 1. What rel-addr does s=94 read? Is that addr WRITTEN by some b3 step (=> real recirc read)?
 2. Compare to its sibling block. The CONCERT structure is repeating allpass/comb sections;
    s=94 sits in the 2nd channel block (s=78..98). Find its analogue in block1 (s=29..46) and
    block3-ish. Is s=94 structurally a comb-closer READ or a unique DAC write?
 3. Does s=94 read an address that a closer writes (XFER+b3)? If so it's recirculation.
"""
import sys, math
sys.path.insert(0, 'tools')
import aru_datapath as A
DMASK = A.DMASK
PICK = lambda st: (st['b5'] << 1) | st['b4']


def main():
    prog = A.load_microcode(0x01)
    byS = {p['s']: p for p in prog}

    # writers: rel-addr -> [(s, XFER)]
    writers = {}
    for p in prog:
        if p['b3']:
            rel = (-p['offset']) & DMASK
            writers.setdefault(rel, []).append((p['s'], p['XFER']))

    for s in [94, 29, 45, 97, 125, 60, 64, 68, 72]:
        p = byS[s]
        rel = (-p['offset']) & DMASK
        w = writers.get(rel, [])
        print(f"s={s:3d} off={p['offset']:#06x} rel={rel:#06x} WA={p['WA']} b3={p['b3']} XFER={p['XFER']} "
              f"coeff={p['coeff']:5d}  read-addr written by={w}")

    print("\n--- structural context around s=94 (block: s=78..98) ---")
    for p in prog:
        if 78 <= p['s'] <= 98:
            rel = (-p['offset']) & DMASK
            isclz = p['b3'] and p['XFER']
            readw = writers.get(rel, []) if not p['b3'] else []
            print(f"  s={p['s']:3d} off={p['offset']:#06x} WA={p['WA']} b3={p['b3']} XFER={p['XFER']} ZERO={p['ZERO']} "
                  f"coeff={p['coeff']:5d}  {'CLOSER(XFER+b3)' if isclz else ''}"
                  f"{'  reads-written-addr '+str(readw) if readw else ''}")

    # The analogous block1 is s=29..46 and block "57..73"
    print("\n--- compare: s=94 vs s=125 vs s=29 (the WA=3 b3=0 bit15 'dead/live' members) ---")
    print("    These are the per-block ALLPASS-FORWARD READ feeding the next section's accumulate.")

    # Direct check: does s=94's read addr match any closer's write addr (real damping recirc)?
    p94 = byS[94]; rel94 = (-p94['offset']) & DMASK
    print(f"\n  s=94 reads rel={rel94:#06x}; closers writing it: "
          f"{[w for w in writers.get(rel94,[]) if w[1]==1]}; any-writer: {writers.get(rel94,[])}")


if __name__ == '__main__':
    main()
