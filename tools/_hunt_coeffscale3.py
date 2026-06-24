#!/usr/bin/env python3
"""ANGLE part 3: WHY is lambda nearly invariant to a 20% global coeff scale-down,
and still > 1 at g=0.80?  A linear recirculation eigenvalue should scale ~ g.

Hypotheses:
 (H1) The L2 "norm" used by exp_lambda_clean (and my power iter) sums over a 'nz'
      set of DM addresses that GROWS over time (pos advances, new addresses get
      written every sample). If the per-sample growth of the *support size* (count
      of nonzero cells) contributes to the norm growth, the measured lambda is
      contaminated by support-spreading, which is gain-INDEPENDENT. That would
      explain both the insensitivity to g and the residual >1 at g=0.80.
 (H2) The true amplitude eigenvalue is < 1 (decaying) but a fixed, gain-independent
      front of newly-written cells keeps the L2 norm growing.

Tests:
 (T1) Track |nz| (support size) vs sample alongside the norm. If |nz| grows
      linearly/geometrically, decompose: norm^2 = sum over cells; compare the
      per-cell RMS growth (amplitude only) vs the count growth.
 (T2) Measure lambda using a FIXED-support norm (only the addresses touched in the
      first few samples, frozen) so support-spreading cannot inflate it.
 (T3) Measure lambda using the per-cell MAX |amplitude| (Linf) and the per-cell
      RMS over a FIXED window of cells -- pure amplitude, support-invariant.
 (T4) Re-run the gain sweep under the fixed-support / Linf metric.
"""
import sys, os, math, random
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import aru_datapath as A

DMASK = A.DMASK
PICK = lambda st: (st['b5'] << 1) | st['b4']


def run_track(prog, nsamp=60000, K=128, seed=1e4, g=1.0, pick=PICK,
              freeze_nz_at=None):
    """Run the linear float datapath; every K samples record:
       (n, full_norm, |nz|, rms_over_nz, linf, frozen_norm)
    where frozen_norm uses ONLY the addresses present in nz at sample
    freeze_nz_at (a support-invariant amplitude metric)."""
    R = [0.0]*4; ACC = 0.0; RES = 0.0
    DM = [0.0]*(DMASK+1); pos = 0
    nz = set(); seeded = False
    frozen = None
    rec = []
    for n in range(nsamp):
        pos = (pos+1) & DMASK
        for st in prog:
            addr = (pos - st['offset']) & DMASK
            dab = RES if st['b3'] else DM[addr]
            if not seeded and st is prog[0]:
                dab += seed; seeded = True
            mag = abs(st['coeff'])
            Cs = -(mag >> 1) if st['coeff'] < 0 else (mag >> 1)
            x = R[pick(st)]; R[st['WA']] = dab
            if st['ZERO']: ACC = 0.0
            ACC = ACC + x*8.0*g*Cs/64.0
            if st['XFER']: RES = ACC/8.0
            if st['b3']:
                DM[addr] = RES; nz.add(addr)
        if freeze_nz_at is not None and frozen is None and (n+1) >= freeze_nz_at:
            frozen = frozenset(nz)
        if (n+1) % K == 0:
            reg = ACC*ACC + RES*RES + sum(v*v for v in R)
            dmen = sum(DM[i]*DM[i] for i in nz)
            full = math.sqrt(reg + dmen) + 1e-300
            cnt = len(nz)
            rms = math.sqrt(dmen/cnt) if cnt else 0.0
            linf = max((abs(DM[i]) for i in nz), default=0.0)
            linf = max(linf, abs(ACC), abs(RES), max(abs(v) for v in R))
            fn = 0.0
            if frozen is not None:
                fn = math.sqrt(reg + sum(DM[i]*DM[i] for i in frozen)) + 1e-300
            rec.append((n+1, full, cnt, rms, linf, fn))
            # renormalize on full norm (so values stay bounded)
            f = 1.0/full
            R = [v*f for v in R]; ACC *= f; RES *= f
            for i in nz: DM[i] *= f
            # frozen/linf are computed BEFORE renorm so their inter-window ratios
            # are valid growth factors; record raw pre-renorm values already done.
    return rec


def lam_from_series(rec, idx, K=128, tailfrac=0.4):
    """Per-sample lambda from the geometric growth of column `idx` across the
    recorded windows (each window already renormalized on full norm, so to get
    the TRUE growth of a sub-metric we must UNDO the renorm). Easier: we instead
    re-derive lambda from the ratio of the metric to the full-norm metric, since
    full-norm was renormalized to 1 each window. So column idx already expresses
    'metric relative to a unit full-norm state'. Its geometric drift across
    windows * full-norm-lambda = true growth.

    Simpler & robust: run WITHOUT renorm for the sub-metrics. We instead recompute
    here using log-linear fit on log(metric) where metric is the per-window value
    AS IF not renormalized: but we DID renorm. So treat the per-window full norm
    growth as the master lambda and the per-window (sub/full) as a stationary
    ratio. If (sub/full) is stationary, sub grows at the same lambda as full.
    """
    pass  # replaced by explicit no-renorm runs below


def run_no_renorm(prog, nsamp=40000, K=256, seed=1.0, g=1.0, pick=PICK,
                  freeze_nz_at=2000):
    """Same datapath but NO renormalization (float64 has ~300 dB headroom; with
    g<=1 and lambda~1.001 over 40k samples log10 growth ~ 40000*0.0011/2.303 ~ 19
    decades -- safe). Record per-window metrics so each metric's own geometric
    slope gives ITS lambda independently. Metrics:
      full_norm, frozen_norm (fixed support), linf, support_count."""
    R = [0.0]*4; ACC = 0.0; RES = 0.0
    DM = [0.0]*(DMASK+1); pos = 0
    nz = set(); seeded = False; frozen = None
    rec = []
    for n in range(nsamp):
        pos = (pos+1) & DMASK
        for st in prog:
            addr = (pos - st['offset']) & DMASK
            dab = RES if st['b3'] else DM[addr]
            if not seeded and st is prog[0]:
                dab += seed; seeded = True
            mag = abs(st['coeff'])
            Cs = -(mag >> 1) if st['coeff'] < 0 else (mag >> 1)
            x = R[pick(st)]; R[st['WA']] = dab
            if st['ZERO']: ACC = 0.0
            ACC = ACC + x*8.0*g*Cs/64.0
            if st['XFER']: RES = ACC/8.0
            if st['b3']:
                DM[addr] = RES; nz.add(addr)
        if frozen is None and (n+1) >= freeze_nz_at:
            frozen = frozenset(nz)
        if (n+1) % K == 0:
            reg = ACC*ACC + RES*RES + sum(v*v for v in R)
            dmen = sum(DM[i]*DM[i] for i in nz)
            full = math.sqrt(reg + dmen)
            cnt = len(nz)
            linf = max([abs(ACC), abs(RES)] + [abs(v) for v in R]
                       + ([max(abs(DM[i]) for i in nz)] if nz else [0.0]))
            fn = math.sqrt(reg + sum(DM[i]*DM[i] for i in frozen)) if frozen else 0.0
            rec.append((n+1, full, cnt, linf, fn))
    return rec


def slope_lambda(rec, col, K=256, tailfrac=0.5):
    """Per-sample lambda = exp(slope of log(metric) vs sample) over the tail."""
    pts = [(r[0], r[col]) for r in rec if r[col] > 0]
    pts = pts[int(len(pts)*(1-tailfrac)):]
    if len(pts) < 4: return float('nan')
    xs = [p[0] for p in pts]; ys = [math.log(p[1]) for p in pts]
    m = len(xs); sx = sum(xs); sy = sum(ys)
    sxx = sum(x*x for x in xs); sxy = sum(x*y for x, y in zip(xs, ys))
    sl = (m*sxy - sx*sy)/(m*sxx - sx*sx)
    return math.exp(sl)


def support_growth(rec):
    """How the support count grows: first, last, and per-sample factor."""
    first = rec[len(rec)//2]; last = rec[-1]
    dn = last[0]-first[0]
    if dn <= 0 or first[2] <= 0: return None
    # count growth per sample
    cps = (last[2]-first[2])/dn
    return first[2], last[2], cps


def main():
    prog = A.load_microcode(0x01)
    print(f"CONCERT: {len(prog)} active steps\n")

    print("="*70)
    print("Decompose +1126 ppm: amplitude vs support-spreading (NO renorm)")
    print("="*70)
    rec = run_no_renorm(prog, nsamp=40000, K=256, g=1.0, freeze_nz_at=2000)
    lam_full   = slope_lambda(rec, 1)   # full L2 norm (what exp_lambda_clean uses)
    lam_linf   = slope_lambda(rec, 3)   # Linf amplitude (support-invariant)
    lam_frozen = slope_lambda(rec, 4)   # fixed-support L2 (support-invariant)
    sg = support_growth(rec)
    print(f"  lambda[full L2 norm]      = {lam_full:.7f}  ({(lam_full-1)*1e6:+.1f} ppm)"
          f"   <- the reported metric")
    print(f"  lambda[Linf amplitude]    = {lam_linf:.7f}  ({(lam_linf-1)*1e6:+.1f} ppm)"
          f"   <- pure peak amplitude, support-invariant")
    print(f"  lambda[frozen-support L2] = {lam_frozen:.7f}  ({(lam_frozen-1)*1e6:+.1f} ppm)"
          f"   <- fixed cell set")
    if sg:
        f0, f1, cps = sg
        print(f"  support |nz|: {f0} -> {f1} cells over the tail "
              f"({cps:+.3f} cells/sample)")
        # how much of full-norm^2 growth is count vs per-cell energy?
        print(f"  (if |nz| keeps growing, full L2 includes a support-spreading term)")

    print("\n" + "="*70)
    print("Gain sweep under SUPPORT-INVARIANT metrics (Linf & frozen-support)")
    print("="*70)
    print(f"  {'g':>5}  {'lam_full':>10}  {'lam_Linf':>10}  {'lam_frozen':>11}")
    for g in [0.70, 0.80, 0.85, 0.90, 0.95, 1.00]:
        r = run_no_renorm(prog, nsamp=40000, K=256, g=g, freeze_nz_at=2000)
        lf = slope_lambda(r, 1); ll = slope_lambda(r, 3); lz = slope_lambda(r, 4)
        mark = ""
        if ll < 1: mark += " Linf-DECAY"
        if lz < 1: mark += " frozen-DECAY"
        print(f"  {g:.3f}  {lf:.7f}  {ll:.7f}  {lz:.7f}"
              f"   ({(ll-1)*1e6:+.0f}ppm Linf){mark}")


if __name__ == '__main__':
    main()
