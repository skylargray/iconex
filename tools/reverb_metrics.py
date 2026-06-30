#!/usr/bin/env python3
"""Error-proof reverb measurement harness (plan 020 § Metric). It physically cannot report reverb on
a dry signal, and re-proves itself against known controls (tools/reverb_metrics_selftest.py) before
it is allowed to judge real audio.

Six non-negotiable principles, each killing a specific past failure:
  P1  Measure ONLY the emitted output (the int16 D/A stream == the WAV). NEVER buf_RMS / DMEM / an
      accumulator. *(Kills the "delay-memory sustains but the output is dry" false positive.)*
  P2  Always render the WAV + provenance atomically with the number; the WAV filename MUST start with
      a YYYYMMDD-HHMMSS timestamp. A reported metric is the triple (number, WAV, sha256).
  P3  DRY-GATE FIRST: refuse to compute RT60/density on a dry signal.
  P4  Three independent RT60 estimators; disagree or fail the quality gates -> INDETERMINATE.
  P5  Self-calibrate against the control battery (selftest) in the same process before judging CONCERT.
  P6  Three-state, pre-registered verdicts: DRY / WET-PASS / FAIL / INDETERMINATE.

analyze(output_int16, excitation_int16, fs, name, ...) -> verdict dict. `excitation_int16` is always a
tools/stimulus array (S1/S2), never improvised.
"""
import os
import wave
import hashlib
import datetime

import numpy as np

# ---- pre-registered thresholds (decided before looking at CONCERT) ----
SILENCE_PEAK = 4            # |output| peak below this (int16 LSB) -> no signal
DRY_WETNESS = 0.02         # wet/total energy below this ...
DRY_LATE_DB = -40.0        # ... AND late/early energy below this -> DRY
RT60_MIN_RANGE_DB = 35.0   # need this much clean decay above the noise floor
RT60_MIN_R2 = 0.90         # decay must be this log-linear (exponential = reverb-like)
RT60_AGREE = 0.20          # the 3 estimators must agree within ±20%
OVER_UNITY_DB = 3.0        # late-third energy exceeding early-third by this -> growing (over-unity)
NED_DENSE = 0.85           # max normalized echo density at/above this -> (candidate) DENSE
SFM_DENSE = 0.10           # tail spectral flatness at/above this -> broadband (not a ringing tone)
ERFC_1_SQRT2 = 0.317310507 # E[fraction beyond 1σ] for a Gaussian (NED normaliser)


def _energy(x):
    return float(np.dot(x, x))


def _to_float(x):
    return np.asarray(x, dtype=np.float64)


def write_wav(out_dir, name, samples_int16, fs):
    """P2: render the exact analyzed samples to a 16-bit WAV whose filename starts with a
    YYYYMMDD-HHMMSS timestamp. Returns (path, sha256)."""
    os.makedirs(out_dir, exist_ok=True)
    ts = datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
    fname = f"{ts}_{name}.wav"
    path = os.path.join(out_dir, fname)
    data = np.asarray(samples_int16, dtype="<i2").tobytes()
    with wave.open(path, "wb") as w:
        w.setnchannels(1)
        w.setsampwidth(2)
        w.setframerate(int(fs))
        w.writeframes(data)
    sha = hashlib.sha256(data).hexdigest()
    return path, sha


def _estimate_dry(output, exc, fs, max_lag_s=0.05):
    """Best-fit direct/dry component a·exc[n-d] (small non-negative lag d). Returns (dry_hat, d, a)."""
    n = len(output)
    e = np.zeros(n)
    m = min(len(exc), n)
    e[:m] = exc[:m]
    if _energy(e) < 1e-9:
        return np.zeros(n), 0, 0.0
    nf = 1 << int(np.ceil(np.log2(2 * n)))
    corr = np.fft.irfft(np.fft.rfft(output, nf) * np.conj(np.fft.rfft(e, nf)), nf)
    max_lag = int(max_lag_s * fs)
    d = int(np.argmax(corr[:max_lag + 1]))           # direct path = small non-negative lag
    es = e[: n - d]
    seg = output[d: d + len(es)]
    a = float(np.dot(seg, es) / (np.dot(es, es) + 1e-12))
    dry_hat = np.zeros(n)
    dry_hat[d: d + len(es)] = a * es
    return dry_hat, d, a


def _schroeder_db(tail):
    e = tail ** 2
    edc = np.cumsum(e[::-1])[::-1]
    edc = edc / (edc[0] + 1e-30)
    return 10.0 * np.log10(edc + 1e-30)


def _fit_decay(curve_db, fs, lo_db, hi_db):
    """Linear fit of a dB-decay curve between lo_db and hi_db (e.g. -5..-35). Returns
    (rt60_or_None, r2, n_pts). RT60 = -60/slope."""
    mask = (curve_db <= lo_db) & (curve_db >= hi_db)
    npts = int(mask.sum())
    if npts < 16:
        return None, 0.0, npts
    t = np.arange(len(curve_db))[mask] / fs
    y = curve_db[mask]
    A = np.vstack([t, np.ones_like(t)]).T
    sol, *_ = np.linalg.lstsq(A, y, rcond=None)
    slope = sol[0]
    pred = A @ sol
    ss_res = float(np.sum((y - pred) ** 2))
    ss_tot = float(np.sum((y - y.mean()) ** 2)) + 1e-30
    r2 = 1.0 - ss_res / ss_tot
    if slope >= 0:
        return None, r2, npts
    return -60.0 / slope, r2, npts


def _block_rms_db(tail, fs, win_ms=10.0):
    w = max(1, int(win_ms * fs / 1000.0))
    nblk = len(tail) // w
    if nblk < 4:
        return None, None
    blk = tail[: nblk * w].reshape(nblk, w)
    rms = np.sqrt(np.mean(blk ** 2, axis=1) + 1e-30)
    rms_db = 20.0 * np.log10(rms / (np.max(rms) + 1e-30) + 1e-30)
    t = (np.arange(nblk) * w + w / 2) / fs
    return rms_db, t


def _rt60_from_block_rms(tail, fs, lo_db=-5.0, hi_db=-35.0):
    rms_db, t = _block_rms_db(tail, fs)
    if rms_db is None:
        return None, 0.0
    mask = (rms_db <= lo_db) & (rms_db >= hi_db)
    if mask.sum() < 8:
        return None, 0.0
    A = np.vstack([t[mask], np.ones(mask.sum())]).T
    sol, *_ = np.linalg.lstsq(A, rms_db[mask], rcond=None)
    slope = sol[0]
    pred = A @ sol
    ss_res = float(np.sum((rms_db[mask] - pred) ** 2))
    ss_tot = float(np.sum((rms_db[mask] - rms_db[mask].mean()) ** 2)) + 1e-30
    r2 = 1.0 - ss_res / ss_tot
    if slope >= 0:
        return None, r2
    return -60.0 / slope, r2


def normalized_echo_density(tail, fs, win_ms=20.0):
    """Abel–Huang NED profile. ~1.0 for a diffuse (Gaussian) tail, ~0 for a lone echo."""
    w = max(8, int(win_ms * fs / 1000.0))
    hop = max(1, w // 4)
    ned = []
    for start in range(0, max(1, len(tail) - w), hop):
        seg = tail[start:start + w]
        sigma = float(np.std(seg))
        if sigma < 1e-9:
            ned.append(0.0)
            continue
        frac = float(np.mean(np.abs(seg) > sigma))
        ned.append(frac / ERFC_1_SQRT2)
    return np.array(ned) if ned else np.array([0.0])


def spectral_flatness(x):
    """Geometric-mean / arithmetic-mean of the power spectrum. ~1 for broadband (diffuse) noise,
    ~0 for a pure tone — the guard that stops a decaying SINE from reading as a 'dense reverb'."""
    if len(x) < 16:
        return 0.0
    X = np.abs(np.fft.rfft(x * np.hanning(len(x)))) ** 2 + 1e-20
    X = X[1:]                                          # drop DC
    gm = np.exp(np.mean(np.log(X)))
    am = np.mean(X)
    return float(gm / am)


def _peaks_per_sec(tail, fs):
    if len(tail) < 3:
        return 0.0
    a = np.abs(tail)
    thr = 0.1 * float(np.max(a))
    if thr <= 0:
        return 0.0
    loc = (a[1:-1] > a[:-2]) & (a[1:-1] >= a[2:]) & (a[1:-1] > thr)
    return float(np.sum(loc)) / (len(tail) / fs)


def analyze(output_int16, excitation_int16, fs, name, out_dir=None, burst_end_s=0.0):
    """Measure the EMITTED output and return a three-state verdict. See module docstring (P1–P6)."""
    if out_dir is None:
        out_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "renders")
    out = _to_float(output_int16)
    exc = _to_float(excitation_int16)
    n = len(out)

    # P2 — always render the WAV + provenance, first.
    wav, sha = write_wav(out_dir, name, output_int16, fs)
    v = dict(name=name, wav=wav, sha256=sha, fs=int(fs), n=n,
             peak=int(np.max(np.abs(output_int16))) if n else 0,
             rms=float(np.sqrt(np.mean(out ** 2))) if n else 0.0,
             verdict=None, subverdict=None, is_wet=False,
             wetness=0.0, late_ratio_db=float("-inf"),
             density=None, ned_max=0.0, peaks_per_s=0.0,
             rt60_s=None, rt60_estimates={}, reasons=[])

    # silence -> INDETERMINATE (empty). Never invent a number from no signal.
    if v["peak"] < SILENCE_PEAK:
        v.update(verdict="INDETERMINATE", subverdict="empty")
        v["reasons"].append(f"output peak {v['peak']} < {SILENCE_PEAK} LSB (no signal)")
        return v

    # P3 — DRY-GATE FIRST.
    dry_hat, d, a = _estimate_dry(out, exc, fs)
    wet = out - dry_hat
    wetness = _energy(wet) / (_energy(out) + 1e-30)
    exc_end = int(np.max(np.nonzero(np.abs(exc) > 0)[0])) if np.any(np.abs(exc) > 0) else 0
    if burst_end_s:
        exc_end = max(exc_end, int(burst_end_s * fs))
    guard = int(0.005 * fs)
    e_during = _energy(out[: exc_end + 1])
    e_after = _energy(out[exc_end + guard:])
    late_db = 10.0 * np.log10(e_after / (e_during + 1e-30) + 1e-30)
    v.update(wetness=float(wetness), late_ratio_db=float(late_db))
    # DRY iff the output is (essentially) a scaled+delayed copy of the input — i.e. the residual after
    # removing the best-fit dry path is negligible (wetness≈0), OR there is no post-input energy at all.
    # A delayed dry copy has wetness≈0 but non-trivial late energy, so this is an OR, not an AND.
    if wetness < DRY_WETNESS or late_db < DRY_LATE_DB:
        v.update(verdict="DRY", subverdict="passthrough", is_wet=False)
        v["reasons"].append(f"wetness {wetness:.4f} (<{DRY_WETNESS}?) / late {late_db:.1f}dB (<{DRY_LATE_DB}?)")
        return v
    v["is_wet"] = True

    # tail = output strictly after the excitation ends (decay/density use the TAIL only).
    tail = out[exc_end + guard:]
    if len(tail) < int(0.05 * fs):
        v.update(verdict="INDETERMINATE", subverdict="tail-too-short")
        v["reasons"].append("tail shorter than 50 ms")
        return v

    # over-unity: late-third energy materially exceeds early-third (growing) -> FAIL.
    third = len(tail) // 3
    e_early = _energy(tail[:third]) / max(1, third)
    e_late = _energy(tail[-third:]) / max(1, third)
    growth_db = 10.0 * np.log10((e_late + 1e-30) / (e_early + 1e-30))
    v["growth_db"] = float(growth_db)
    if growth_db > OVER_UNITY_DB:
        v.update(verdict="FAIL", subverdict="over-unity")
        v["reasons"].append(f"tail energy grows {growth_db:.1f}dB (>{OVER_UNITY_DB}) — over-unity")
        return v

    # density: DENSE requires BOTH high normalized echo density AND a broadband (flat) spectrum, so a
    # ringing tone (high NED, near-zero flatness) cannot pass as a diffuse reverb tail.
    ned = normalized_echo_density(tail, fs)
    ned_max = float(np.max(ned))
    pps = _peaks_per_sec(tail, fs)
    sfm = spectral_flatness(tail)
    if ned_max >= NED_DENSE and sfm >= SFM_DENSE:
        density = "DENSE"
    elif ned_max >= NED_DENSE and sfm < SFM_DENSE:
        density = "TONAL"                              # high NED but not broadband -> a tone, not reverb
    else:
        density = "SPARSE"
    v.update(density=density, ned_max=ned_max, peaks_per_s=float(pps), spectral_flatness=round(sfm, 4))

    # P4 — RT60 three independent estimators + quality gates.
    edc = _schroeder_db(tail)
    clean_range = float(-edc[edc > -120].min()) if np.any(edc > -120) else 0.0
    rt_t30, r2_t30, _ = _fit_decay(edc, fs, -5.0, -35.0)
    rt_t20, r2_t20, _ = _fit_decay(edc, fs, -5.0, -25.0)
    rt_env, r2_env = _rt60_from_block_rms(tail, fs)
    ests = {"schroeder_t30": rt_t30, "schroeder_t20": rt_t20, "block_rms": rt_env}
    v["rt60_estimates"] = {k: (round(x, 4) if x else None) for k, x in ests.items()}
    v["rt60_quality"] = dict(clean_range_db=round(clean_range, 1),
                             r2_t30=round(r2_t30, 3), r2_t20=round(r2_t20, 3),
                             r2_env=round(r2_env, 3))

    vals = [x for x in ests.values() if x is not None and x > 0]
    gates_ok = (clean_range >= RT60_MIN_RANGE_DB and r2_t30 >= RT60_MIN_R2
                and r2_t20 >= RT60_MIN_R2 and len(vals) == 3)
    agree = False
    if len(vals) == 3:
        med = float(np.median(vals))
        agree = all(abs(x - med) / med <= RT60_AGREE for x in vals)
    if gates_ok and agree:
        v["rt60_s"] = round(float(np.median(vals)), 4)
    else:
        reason = []
        if clean_range < RT60_MIN_RANGE_DB:
            reason.append(f"clean range {clean_range:.0f}dB<{RT60_MIN_RANGE_DB}")
        if not (r2_t30 >= RT60_MIN_R2 and r2_t20 >= RT60_MIN_R2):
            reason.append(f"decay not log-linear (R²={r2_t30:.2f}/{r2_t20:.2f})")
        if len(vals) < 3:
            reason.append("an estimator failed")
        elif not agree:
            reason.append(f"estimators disagree ({[round(x,2) for x in vals]})")
        v["reasons"].append("RT60 INDETERMINATE: " + "; ".join(reason))

    # P6 — combine.
    if v["rt60_s"] is not None and density == "DENSE":
        v.update(verdict="WET-PASS", subverdict="dense-decaying")
    else:
        sub = {"SPARSE": "sparse", "TONAL": "tonal"}.get(density, "rt60-indeterminate")
        v.update(verdict="INDETERMINATE", subverdict=sub)
    return v


def assert_calibrated():
    """P5 — refuse to judge real audio unless the control battery passes in this process."""
    import reverb_metrics_selftest as ST
    if not ST.run_battery(verbose=False):
        raise RuntimeError("reverb_metrics control battery FAILED — metric is not trusted; do not "
                           "report any CONCERT number until reverb_metrics_selftest passes.")


if __name__ == "__main__":
    import reverb_metrics_selftest as ST
    ST.run_battery()
