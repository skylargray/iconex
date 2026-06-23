#!/usr/bin/env python3
"""Rigorous, bias-free test of the modal match: do the model's tank resonances align
with P85's beyond chance? Uses a NULL DISTRIBUTION of random peak-sets (same count,
same band) so the dense-comb nearest-neighbour bias is controlled.

Reads tools/_ir/modal_match.json (p85_peaks, model_peaks).
"""
import sys, os, json
import numpy as np

J = json.load(open(os.path.join(os.path.dirname(__file__), '_ir', 'modal_match.json')))
P85 = np.array(sorted(J['p85_peaks']))
MODEL = np.array(sorted(J['model_peaks']))
FMIN, FMAX = 2200.0, 11900.0   # the well-populated band on both


def band(a):
    return a[(a >= FMIN) & (a <= FMAX)]


def align_metrics(test, ref):
    """For each test peak, nearest ref peak: relative error |df|/f."""
    err = np.array([np.min(np.abs(ref - f))/f for f in test])
    return dict(median_rel=float(np.median(err)),
                mean_rel=float(np.mean(err)),
                tight10=int(np.sum(np.array([np.min(np.abs(ref - f)) for f in test]) < 10.0)),
                tight20=int(np.sum(np.array([np.min(np.abs(ref - f)) for f in test]) < 20.0)),
                n=len(test))


def null_distribution(n, ref, ntrials=4000, seed=7):
    rng = np.random.default_rng(seed)
    meds = np.empty(ntrials); tights = np.empty(ntrials)
    for i in range(ntrials):
        rp = np.sort(rng.uniform(FMIN, FMAX, n))
        err = np.array([np.min(np.abs(ref - f))/f for f in rp])
        meds[i] = np.median(err)
        tights[i] = np.sum(np.array([np.min(np.abs(ref - f)) for f in rp]) < 10.0)
    return meds, tights


def main():
    m = band(MODEL); p = band(P85)
    print(f"P85 peaks in band: {len(p)}   model peaks in band: {len(m)}")
    print(f"band {FMIN:.0f}-{FMAX:.0f} Hz, mean P85 spacing ~ {(FMAX-FMIN)/len(p):.0f} Hz\n")

    obs = align_metrics(m, p)
    print(f"MODEL vs P85:  median |df|/f = {obs['median_rel']*100:.3f}%   "
          f"tight(<10Hz)={obs['tight10']}/{obs['n']}   tight(<20Hz)={obs['tight20']}/{obs['n']}")

    meds, tights = null_distribution(len(m), p)
    p_med = float(np.mean(meds <= obs['median_rel']))
    p_tight = float(np.mean(tights >= obs['tight10']))
    print(f"\nNULL (random peak-sets, same count, same band, 4000 trials):")
    print(f"  median |df|/f : null mean={np.mean(meds)*100:.3f}%  null p5={np.percentile(meds,5)*100:.3f}%"
          f"   -> model p-value = {p_med:.4f}")
    print(f"  tight(<10Hz)  : null mean={np.mean(tights):.1f}  null p95={np.percentile(tights,95):.0f}"
          f"   -> model p-value = {p_tight:.4f}")

    # symmetric direction
    obs2 = align_metrics(p, m)
    meds2, tights2 = null_distribution(len(p), m)
    p_med2 = float(np.mean(meds2 <= obs2['median_rel']))
    print(f"\nP85 vs MODEL (reverse): median |df|/f={obs2['median_rel']*100:.3f}%  "
          f"tight<10={obs2['tight10']}/{obs2['n']}  -> p-value={p_med2:.4f}")

    # implied native Fs from the median ratio (model_f/p85_f over tight matches)
    ratios = []
    for f in m:
        nf = p[np.argmin(np.abs(p - f))]
        if abs(f-nf) < 25:
            ratios.append(f/nf)
    if ratios:
        rmed = float(np.median(ratios))
        print(f"\nmedian model/P85 ratio over tight matches = {rmed:.4f}  "
              f"-> implied true native Fs ~ {34130.0/rmed:.0f} Hz (assumed 34130)")

    verdict = "MODES ALIGN BEYOND CHANCE (delays/topology correct)" if (p_med < 0.05 and p_tight < 0.05) \
        else "NOT clearly beyond chance"
    print(f"\nVERDICT: {verdict}  (p_median={p_med:.4f}, p_tight={p_tight:.4f})")


if __name__ == '__main__':
    main()
