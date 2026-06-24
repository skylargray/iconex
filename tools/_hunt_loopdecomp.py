#!/usr/bin/env python3
"""ANGLE part 2/3: localize the +1126 ppm.

Two complementary decompositions:

(A) STRUCTURAL: the exact writer/reader offset matches reveal nested comb/all-pass
    cells. For each matched offset O, writer Ws writes DMEM[(pos-O)] = RES_W, and a
    reader Rs (earlier in the SAME 128-step sweep) reads DMEM[(pos-O)] = the value
    written ONE sample ago (since pos advanced by 1). So each cell is a 1-sample (in
    pos units) recirculating delay whose round-trip gain is the product of net coeffs
    around the loop through the register file. I reconstruct the per-cell loop and its
    gain, and flag which cells have |round-trip gain| closest to (or above) 1.

(B) EIGEN-LOCALIZATION (the decisive test): scale EACH b3-writer's coeff by (1-eps)
    one at a time and measure d(lambda)/d(scale). The sum of sensitivities tells us if
    the +1126 ppm is concentrated in one closer (=> a localizable decode bug) or spread
    (=> uniform physical loss). Then the MINIMAL-FIX search: find the single principled
    change (one step's coeff off-by-one / sign / a single attenuation) that yields
    lambda ~ 0.99999, OR prove none exists and only a uniform scale works.
"""
import sys, os, math, copy
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import aru_datapath as A
import exp_lambda_clean as L

DMASK = A.DMASK
PICK = L.PICK


def conv_lambda(prog, pick=PICK, nsamp=30000, K=128):
    traj = L.lambda_trajectory(prog, pick=pick, nsamp=nsamp, K=K)
    tail = sorted(l for _, l in traj[-50:])
    return tail[len(tail)//2]


def main():
    prog = A.load_microcode(0x01)
    lam0 = conv_lambda(prog)
    print(f"baseline lambda = {lam0:.7f}  ({(lam0-1)*1e6:+.1f} ppm)\n")

    by_s = {st['s']: st for st in prog}
    idx_of = {st['s']: i for i, st in enumerate(prog)}

    # ---------- (B) per-writer eigen sensitivity ----------
    # scale one writer's coeff down by 5% and see lambda shift. dlam<0 means that
    # writer ADDS gain (its recirc is regenerative); the most-negative ones are the
    # hot closers.
    print("=== (B) per-b3-writer eigen sensitivity (scale that coeff *0.95) ===")
    writers = [st for st in prog if st['b3']]
    sens = []
    SCALE = 0.95
    for w in writers:
        # build a modified prog: we cannot pass a float coeff into the integer Cs path,
        # so scale at the *net coefficient* level by editing a float-coeff override.
        # The float datapath uses Cs=(|coeff|>>1) with sign. We emulate a fractional
        # scale by temporarily monkeypatching: easiest is to run a custom trajectory.
        lam = lam_with_writer_scale(prog, w['s'], SCALE)
        d = lam - lam0
        sens.append((w['s'], d))
    sens_sorted = sorted(sens, key=lambda t: t[1])  # most negative = hottest
    print("  (dlam for *0.95 of that writer; MOST NEGATIVE = removing its gain cools most)")
    for s, d in sens_sorted[:12]:
        print(f"    writer s={s:3d} off={by_s[s]['offset']:#06x} coeff={by_s[s]['coeff']:+4d}"
              f"  dlam={d*1e6:+8.1f} ppm")
    print("  ...")
    for s, d in sens_sorted[-4:]:
        print(f"    writer s={s:3d} off={by_s[s]['offset']:#06x} coeff={by_s[s]['coeff']:+4d}"
              f"  dlam={d*1e6:+8.1f} ppm")
    tot = sum(d for _, d in sens)
    print(f"\n  sum of single-writer dlam (at *0.95) = {tot*1e6:+.1f} ppm")
    print(f"  baseline excess to kill = {(lam0-0.9999899)*1e6:+.1f} ppm")
    # concentration ratio: top1 / total, top3 / total
    neg = sorted((d for _, d in sens if d < 0))
    if neg:
        top1 = neg[0]; top3 = sum(neg[:3]); allneg = sum(neg)
        print(f"  concentration: top1 writer = {100*top1/allneg:.1f}% of total cooling,"
              f"  top3 = {100*top3/allneg:.1f}%")


def lam_with_writer_scale(prog, target_s, scale, nsamp=30000, K=128, seed=1e4):
    """Float trajectory identical to L.lambda_trajectory but the NET coefficient of
    step target_s is multiplied by `scale` (fractional, principled attenuation test)."""
    R = [0.0]*4; ACC = 0.0; RES = 0.0
    DM = [0.0]*(DMASK+1); pos = 0
    nz = set(); seeded = False; traj = []
    for n in range(nsamp):
        pos = (pos+1) & DMASK
        for st in prog:
            addr = (pos - st['offset']) & DMASK
            dab = RES if st['b3'] else DM[addr]
            if not seeded and st is prog[0]:
                dab += seed; seeded = True
            mag = abs(st['coeff']); Cs = -(mag>>1) if st['coeff']<0 else (mag>>1)
            csf = float(Cs)
            if st['s'] == target_s:
                csf *= scale
            x = R[PICK(st)]; R[st['WA']] = dab
            if st['ZERO']: ACC = 0.0
            ACC = ACC + x*8.0*csf/64.0   # EXACT mirror of L.lambda_trajectory (csf==Cs unless scaled)
            if st['XFER']: RES = ACC/8.0
            if st['b3']: DM[addr] = RES; nz.add(addr)
        if (n+1) % K == 0:
            s = math.sqrt(ACC*ACC + RES*RES + sum(v*v for v in R)
                          + sum(DM[i]*DM[i] for i in nz)) + 1e-300
            traj.append(math.exp(math.log(s)/K))
            f = 1.0/s
            R = [v*f for v in R]; ACC *= f; RES *= f
            for i in nz: DM[i] *= f
    tail = sorted(traj[-50:])
    return tail[len(tail)//2]


if __name__ == '__main__':
    main()
