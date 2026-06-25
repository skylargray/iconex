#!/usr/bin/env python3
"""Independent inv_l3 discriminator: microcode-structure plausibility (no datapath sim).
A correct l3 inversion yields a sane microprogram: many pure-delay 'move' steps (coeff=0),
XFER firing on a sensible fraction (the result-transfer/closers), ZERO opening MAC groups.
A wrong inversion forces every step to multiply (0 zero-coeff steps) and/or makes XFER/ZERO
fire on almost all or almost no steps. Reports aggregate stats over all 13 clean programs for
inv_l3 True/False (frontier map: XFER=l3.b0, ZERO=l3.b1, coeff=l3[2:7], CSIGN=l2.b7)."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import _hunt_rawcache as RC
import _hunt_rebuild2 as R2


def main():
    cache = RC.load()
    clean = [p for p in sorted(cache) if cache[p]['clean']]
    for inv_l3 in (True, False):
        tot = dict(n=0, zc=0, xfer=0, zero=0, both=0)
        hist = {}
        per = []
        for p in clean:
            prog = R2.decode(cache[p]['steps'], inv_l2=False, inv_l3=inv_l3)
            n = len(prog)
            zc = sum(1 for st in prog if st['Cs'] == 0)
            xf = sum(1 for st in prog if st['XFER'])
            zr = sum(1 for st in prog if st['ZERO'])
            bo = sum(1 for st in prog if st['XFER'] and st['ZERO'])
            tot['n'] += n; tot['zc'] += zc; tot['xfer'] += xf; tot['zero'] += zr; tot['both'] += bo
            for st in prog:
                m = abs(st['Cs']); hist[m] = hist.get(m, 0) + 1
            per.append((p, n, zc, xf, zr))
        print(f"===== inv_l3 = {inv_l3} =====")
        print(f"  totals over {len(clean)} programs: steps={tot['n']}  zero-coeff(move)={tot['zc']} "
              f"({100*tot['zc']/tot['n']:.0f}%)  XFER={tot['xfer']} ({100*tot['xfer']/tot['n']:.0f}%)  "
              f"ZERO={tot['zero']} ({100*tot['zero']/tot['n']:.0f}%)  XFER&ZERO={tot['both']}")
        # coeff magnitude histogram (top of range matters: real diffusion coeffs cluster near max)
        near_max = sum(c for m, c in hist.items() if m >= 60)
        mids = sum(c for m, c in hist.items() if 1 <= m < 60)
        print(f"  coeff mag: zero={hist.get(0,0)}  mid(1..59)={mids}  near-max(60..63)={near_max}  "
              f"max-mag-seen={max(hist)}")
        print(f"  per-program (pid:steps zc xf zr): " +
              "  ".join(f"{('%#x'%p)}:{n} {zc}/{xf}/{zr}" for p, n, zc, xf, zr in per))
        print()


if __name__ == '__main__':
    main()
