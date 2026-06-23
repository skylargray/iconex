#!/usr/bin/env python3
"""Measure the CONCERT loop's per-sample amplitude growth/decay rate (lambda).

esum[n] = sum|RES| over XFER steps (the L1 amplitude envelope from run()).
For a single dominant mode  esum[n] ~ A * lambda^n , so a linear fit of
log(esum) vs n in the pre-saturation region gives ln(lambda).

Usage: python tools/measure_decay.py [nsamp]
"""
import sys, os, math
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import aru_datapath as A

NATIVE_HZ = 34130.0


def fit_lambda(esum, lo_frac=0.15, hi_frac=0.85):
    """Linear least-squares fit of ln(esum) vs n over [lo,hi] of the run.
    Returns (lambda_per_sample, ln_lambda_slope, r2)."""
    n = len(esum)
    lo, hi = int(n * lo_frac), int(n * hi_frac)
    xs, ys = [], []
    for i in range(lo, hi):
        if esum[i] > 0:
            xs.append(i)
            ys.append(math.log(esum[i]))
    if len(xs) < 10:
        return None
    m = len(xs)
    sx = sum(xs); sy = sum(ys)
    sxx = sum(x * x for x in xs); sxy = sum(x * y for x, y in zip(xs, ys))
    denom = m * sxx - sx * sx
    slope = (m * sxy - sx * sy) / denom
    intercept = (sy - slope * sx) / m
    # r^2
    ybar = sy / m
    ss_tot = sum((y - ybar) ** 2 for y in ys)
    ss_res = sum((y - (slope * x + intercept)) ** 2 for x, y in zip(xs, ys))
    r2 = 1 - ss_res / ss_tot if ss_tot else 0.0
    return math.exp(slope), slope, r2


def rt60_from_lambda(lam):
    """RT60 in seconds at the native rate, if lam < 1 (decaying)."""
    if lam >= 1.0:
        return float('inf')
    # amplitude lambda; -60 dB = factor 1e-3 in amplitude
    return math.log(1e-3) / math.log(lam) / NATIVE_HZ


def summarize(label, esum):
    peak = max(esum)
    npk = esum.index(peak)
    last = esum[-1]
    f = fit_lambda(esum)
    print(f"\n=== {label} ===")
    print(f"  nsamp={len(esum)}  peak={peak} @n={npk}  last={last}")
    if f:
        lam, slope, r2 = f
        target = 0.9999899
        print(f"  fit lambda={lam:.7f}  ln_slope={slope:+.6e}  r2={r2:.4f}")
        print(f"  target    ={target:.7f}  gap={lam - target:+.2e}")
        if lam < 1.0:
            print(f"  -> RT60 ~ {rt60_from_lambda(lam):.2f} s   (target ~20 s)")
        else:
            print(f"  -> GROWING (no decay); excess = {lam - 1.0:+.2e} per sample")
    return f


def main():
    nsamp = int(sys.argv[1]) if len(sys.argv) > 1 else 30000
    prog = A.load_microcode(0x01)
    print(f"CONCERT: {len(prog)} active steps; nsamp={nsamp}")
    pick = lambda st: (st['b5'] << 1) | st['b4']

    esum = A.run(prog, pick, nsamp=nsamp)
    summarize("baseline (current model)", esum)

    # Localization cross-check: zero s88, then s65, confirm the brief's claim.
    for kill in (88, 65):
        prog2 = [dict(p) for p in prog]
        for p in prog2:
            if p['s'] == kill:
                p['coeff'] = 0
        e2 = A.run(prog2, pick, nsamp=nsamp)
        summarize(f"with s{kill} coeff zeroed", e2)


if __name__ == '__main__':
    main()
