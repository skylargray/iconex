#!/usr/bin/env python3
"""ANGLE part 4: pin the unity crossing precisely + test PRINCIPLED coefficient
alternatives (not arbitrary scale) for a flip to decay.

Findings so far (independently confirmed): lambda = +1126 ppm is a real AMPLITUDE
eigenvalue (Linf == L2 == impulse-slope == matrix-free PM). A uniform global gain
g must drop to ~0.78 for unity, and the g->lambda curve is strongly SUB-LINEAR.

Now: is there a SINGLE-BIT / off-by-one PRINCIPLED coefficient convention that
lands at unity?  Candidates grounded in the FPC 7-bit sign-magnitude encoding:
  (A) Cs = round(|c|/2) instead of floor (|c|>>1): floor loses up to 0.5 LSB per
      coeff -> but floor gives SMALLER gain, so rounding would make it HOTTER. skip.
  (B) coefficient normalization /128 vs /127 vs /64. The model uses Cs/64 where
      Cs=|c|>>1, i.e. coeff/128 effectively. Try /127, and try treating the 7-bit
      field as the full magnitude /128 WITHOUT the >>1 (then /128 in prod).
  (C) An extra >>1 somewhere (e.g. the result register is PP[3..18] = >>3, but if
      it were PP[2..17] the net would differ). Already covered by RESSH bit-perturb
      (those were x0.5/x2, too coarse).
  (D) the coefficient is read 1's-complement vs 2's-complement for negatives:
      negative coeffs use -(mag>>1); if instead the hardware does ~mag (1s-comp)
      the negative-tap magnitudes shift by 1 LSB. Test the lambda effect.
"""
import sys, os, math, random
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import aru_datapath as A

DMASK = A.DMASK
PICK = lambda st: (st['b5'] << 1) | st['b4']


def lam_linf(prog, csfn, nsamp=40000, K=256, seed=1.0, pick=PICK):
    """Per-sample lambda from Linf amplitude growth (support-invariant), using a
    custom coefficient function csfn(coeff_signed)->Cs_value applied as
    ACC += x*8*Cs/64.  No renorm."""
    R = [0.0]*4; ACC = 0.0; RES = 0.0
    DM = [0.0]*(DMASK+1); pos = 0
    nz = set(); seeded = False; rec = []
    Cs_cache = {}
    for n in range(nsamp):
        pos = (pos+1) & DMASK
        for st in prog:
            addr = (pos - st['offset']) & DMASK
            dab = RES if st['b3'] else DM[addr]
            if not seeded and st is prog[0]:
                dab += seed; seeded = True
            c = st['coeff']
            Cs = Cs_cache.get(c)
            if Cs is None:
                Cs = csfn(c); Cs_cache[c] = Cs
            x = R[pick(st)]; R[st['WA']] = dab
            if st['ZERO']: ACC = 0.0
            ACC = ACC + x*8.0*Cs/64.0
            if st['XFER']: RES = ACC/8.0
            if st['b3']:
                DM[addr] = RES; nz.add(addr)
        if (n+1) % K == 0:
            linf = max([abs(ACC), abs(RES)] + [abs(v) for v in R]
                       + ([max(abs(DM[i]) for i in nz)] if nz else [0.0]))
            rec.append((n+1, linf))
    pts = [(a, b) for a, b in rec if b > 0]
    pts = pts[len(pts)//2:]
    xs = [p[0] for p in pts]; ys = [math.log(p[1]) for p in pts]
    m = len(xs); sx = sum(xs); sy = sum(ys)
    sxx = sum(x*x for x in xs); sxy = sum(x*y for x, y in zip(xs, ys))
    sl = (m*sxy - sx*sy)/(m*sxx - sx*sx)
    return math.exp(sl)


def baseline_cs(c):
    mag = abs(c); return -(mag >> 1) if c < 0 else (mag >> 1)


def main():
    prog = A.load_microcode(0x01)
    print(f"CONCERT: {len(prog)} active steps\n")

    print("="*70)
    print("Precise unity crossing under global gain g (Linf metric, bisection)")
    print("="*70)
    def lam_g(g):
        return lam_linf(prog, lambda c: g*baseline_cs(c))
    lo, hi = 0.70, 0.82
    llo, lhi = lam_g(lo), lam_g(hi)
    print(f"  g={lo:.3f}: {(llo-1)*1e6:+.1f} ppm   g={hi:.3f}: {(lhi-1)*1e6:+.1f} ppm")
    for _ in range(7):
        mid = 0.5*(lo+hi); lm = lam_g(mid)
        print(f"    g={mid:.4f}: lambda={lm:.7f} ({(lm-1)*1e6:+.1f} ppm)")
        if lm > 1: hi = mid
        else: lo = mid
    print(f"  => unity crossing g* ~ {0.5*(lo+hi):.4f}  "
          f"(uniform coeff reduction ~ {(1-0.5*(lo+hi))*100:.1f}%)")

    print("\n" + "="*70)
    print("PRINCIPLED coefficient-convention alternatives -> lambda (Linf)")
    print("="*70)
    base = lam_linf(prog, baseline_cs)
    print(f"  baseline floor(|c|/2), /64:          "
          f"lambda={base:.7f} ({(base-1)*1e6:+.1f} ppm)")

    alts = []
    # (B) divide by 127 instead of /128 (i.e. Cs/64 -> Cs/63.5): HOTTER, sanity
    alts.append(("Cs/63.5 (norm /127 not /128)",
                 lambda c: baseline_cs(c)*(64.0/63.5)))
    # (B2) treat 7-bit field as full magnitude /128 (no >>1): doubles gain
    alts.append(("|c|/2 (no >>1, /128 net) == same",
                 lambda c: (abs(c)/2.0)*(1 if c>=0 else -1)))
    # (A) round-to-nearest instead of floor for the >>1
    alts.append(("round(|c|/2) instead of floor",
                 lambda c: (round(abs(c)/2.0))*(1 if c>=0 else -1)))
    # (D) 1's-complement negative magnitude: negatives use (mag-? ) - test ~ via
    #     -((mag-1)>>1)-? ; simplest principled: negatives floor differently
    alts.append(("neg uses -((|c|+1)>>1) (1s-comp tilt)",
                 lambda c: (-(((abs(c))+1) >> 1) if c < 0 else (abs(c) >> 1))))
    # (C) ceil(|c|/2): upper-rounding, HOTTER, bracket
    alts.append(("ceil(|c|/2)",
                 lambda c: (math.ceil(abs(c)/2.0))*(1 if c>=0 else -1)))

    for name, fn in alts:
        lam = lam_linf(prog, fn)
        flip = " <<< FLIPS TO DECAY" if lam < 1.0 else ""
        print(f"  {name:38s}: lambda={lam:.7f} ({(lam-1)*1e6:+.1f} ppm){flip}")

    print("\n  NOTE: all floor/round/ceil variants change gain by <1 LSB on small")
    print("  coeffs but the dominant closers have |c|=124,108 (Cs=62,54); a 1-LSB")
    print("  tilt there is <2% and cannot reach the ~22% reduction unity needs.")


if __name__ == '__main__':
    main()
