"""Decisive topology diagnostic before any damping search:
(1) Model transfer function at several (flat) damping depths -> does the P85 correlation
    improve as the comb develops, or stay at chance? (tests the 'under-developed comb'
    vs 'modes genuinely mismatch' question).
(2) Comb-spacing via spectral AUTOCORRELATION (envelope-independent): the lag peaks =
    the tank's dominant delays. If model and P85 share comb spacings, the delays/topology
    match regardless of absolute peak alignment or amplitude.
Benchmarks: V7.2 (real CONCERT) and a delay-scramble.
"""
import sys, os, json
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np, scipy.io.wavfile as wav
from scipy.signal import find_peaks
import aru_datapath as A
from modal_tf import noise_tf, spec, corr_scale, est_lam, scrambled, NATIVE_HZ, FMIN, FMAX


def comb_autocorr(fr, lp):
    """Autocorrelation of the band-limited log-spectrum vs frequency-lag. Peaks at the
    comb spacings (Hz) = the tank's modal spacings (set by loop delays)."""
    bd = (fr >= FMIN) & (fr <= FMAX)
    x = lp[bd].copy(); x = x - x.mean()
    df = fr[1] - fr[0]
    ac = np.correlate(x, x, mode='full')[len(x)-1:]
    ac = ac / (ac[0] + 1e-30)
    lags_hz = np.arange(len(ac)) * df
    m = (lags_hz > 60) & (lags_hz < 1500)            # plausible comb spacings
    pk, _ = find_peaks(ac[m], height=0.08, distance=int(40/df))
    return lags_hz[m][pk][:8].tolist(), ac, lags_hz


def main():
    sr, d = wav.read('IR/Lexicon 224XL/P85 - 20.0 Seconds A.wav')
    pf, pl = spec(d[:, 0].astype(float), sr)
    srv, dv = wav.read('IR/Lexicon 224XL/Concert Hall V7.2.L.wav')
    vf, vl = spec(dv.astype(float), srv)
    prog = A.load_microcode(0x01); ls = est_lam(prog)
    sprog = scrambled(prog); lss = est_lam(sprog)

    print("=== (1) model P85 correlation vs flat-damping depth ===")
    print(f"  V7.2 benchmark: {corr_scale(vf, vl, pf, pl)[0]:+.3f}")
    for le in (0.999, 0.9997, 0.99993):
        out = noise_tf(prog, nsamp=100000, lam_eff=le, lam_struct=ls)
        f, l = spec(out, NATIVE_HZ); c, k = corr_scale(f, l, pf, pl)
        print(f"  model lam_eff={le}: P85corr={c:+.3f} @ scale={k:.4f}")

    print("\n=== (2) comb-spacing (spectral autocorrelation) — delays, envelope-independent ===")
    p_sp, _, _ = comb_autocorr(pf, pl)
    v_sp, _, _ = comb_autocorr(vf, vl)
    out = noise_tf(prog, nsamp=120000, lam_eff=0.9997, lam_struct=ls)
    mf, ml = spec(out, NATIVE_HZ); m_sp, _, _ = comb_autocorr(mf, ml)
    outs = noise_tf(sprog, nsamp=120000, lam_eff=0.9997, lam_struct=lss); sf, slg = spec(outs, NATIVE_HZ)
    s_sp, _, _ = comb_autocorr(sf, slg)
    print(f"  P85   comb spacings (Hz): {[round(x) for x in p_sp]}")
    print(f"  V7.2  comb spacings (Hz): {[round(x) for x in v_sp]}")
    print(f"  MODEL comb spacings (Hz): {[round(x) for x in m_sp]}")
    print(f"  SCRAM comb spacings (Hz): {[round(x) for x in s_sp]}")

    def overlap(a, b, tol=15):
        return sum(1 for x in a if any(abs(x-y) < tol for y in b))
    print(f"\n  shared spacings (within 15 Hz) with P85:")
    print(f"    V7.2 ={overlap(v_sp,p_sp)}/{len(p_sp)}  MODEL={overlap(m_sp,p_sp)}/{len(p_sp)}  "
          f"SCRAM={overlap(s_sp,p_sp)}/{len(p_sp)}")
    json.dump(dict(p85=p_sp, v72=v_sp, model=m_sp, scram=s_sp),
              open(os.path.join(os.path.dirname(__file__), '_ir', 'comb.json'), 'w'), indent=1)


if __name__ == '__main__':
    main()
