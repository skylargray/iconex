#!/usr/bin/env python3
"""224XL test-stimulus battery (plan 020 § Test stimulus). Deterministic, reproducible inputs.

ONE defined input battery used identically by Phase 0.5, the Milestone, and the metric's dry-gate —
never an improvised one-off. The 224XL is fixed-point (saturation + quantization) and, with
modulation on, time-varying, so input SHAPE, LEVEL, channel, and injection point all matter and are
pinned here. All generators return int16 numpy arrays (the int16 D/A full scale is 32767).

  S1  unit_impulse(level_dbfs, ...)  — calibrated impulse, LEVEL-SWEPT, for the IR-based metrics.
  S2  noise_burst(...)               — interrupted pseudo-random noise (ISO-3382-style decay).
  S3  impulse_phase_ensemble(...)    — S1 fired at N LFO phases (the caller injects at the offsets),
                                       for time-varying (modulated) runs.

The level sweep for S1 is MANDATORY at the call sites: RT60/density that move with level localize
saturation/quantization (gain), not topology.
"""
import numpy as np

FULL_SCALE = 32767
FS_DEFAULT = 34130
S1_LEVELS_DBFS = (-20.0, -12.0, -6.0, -1.0)     # the mandatory primary level sweep


def dbfs_to_amp(dbfs):
    """dBFS (relative to int16 full scale) -> integer amplitude."""
    return int(round(FULL_SCALE * (10.0 ** (dbfs / 20.0))))


def unit_impulse(level_dbfs, n_samples, fs=FS_DEFAULT):
    """S1: a single sample at `level_dbfs`, then silence. int16, length n_samples."""
    x = np.zeros(int(n_samples), dtype=np.int16)
    x[0] = dbfs_to_amp(level_dbfs)
    return x


def noise_burst(burst_s, total_s, fs=FS_DEFAULT, seed=0x1234):
    """S2: pseudo-random noise burst for `burst_s`, then silence to `total_s`.

    Uses the same LCG and amplitude (±8000) as tools/aru_freerun.src so the cross-check matches the
    behavioral reference exactly. Deterministic in `seed`."""
    n = int(total_s * fs)
    burst = int(burst_s * fs)
    x = np.zeros(n, dtype=np.int16)
    s = seed & 0x7FFFFFFF
    for i in range(min(burst, n)):
        s = (s * 1103515245 + 12345) & 0x7FFFFFFF
        x[i] = (s >> 8) % 16000 - 8000
    return x


def impulse_phase_ensemble(level_dbfs, n_samples, n_phases=8, lfo_period_s=None, fs=FS_DEFAULT):
    """S3: N impulse stimuli for a time-varying (modulated) run. Returns a list of
    (lfo_phase_index, injection_offset_samples, impulse_array). The caller fires each impulse at its
    offset relative to the LFO so the IR is averaged over LFO phase (a single-phase modulated IR is
    not trusted). If lfo_period_s is unknown, offsets are spread across n_samples as a proxy."""
    out = []
    span = int(lfo_period_s * fs) if lfo_period_s else int(n_samples)
    for k in range(n_phases):
        off = int(k * span / n_phases)
        out.append((k, off, unit_impulse(level_dbfs, n_samples, fs)))
    return out


if __name__ == "__main__":
    imp = unit_impulse(-6.0, 16, FS_DEFAULT)
    print("S1 -6 dBFS impulse[:4]:", imp[:4], "amp:", dbfs_to_amp(-6.0))
    nb = noise_burst(0.001, 0.003, FS_DEFAULT)
    print("S2 burst nonzero count:", int(np.count_nonzero(nb)), "peak:", int(np.max(np.abs(nb))))
    print("S1 level sweep amps:", [dbfs_to_amp(L) for L in S1_LEVELS_DBFS])
