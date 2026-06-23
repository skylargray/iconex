#!/usr/bin/env python3
"""P85 modal match: do the model's tank resonances line up with the hardware IR?

Generates a faithful, minimally-stabilized model impulse response (float-exact
datapath, impulse injected at the real FPC input step, a small uniform recirculation
leak so the otherwise-growing tank decays cleanly without moving the modal
frequencies), extracts its resonant-peak frequencies, and compares them to the P85
hardware IR's peaks. Three hypotheses are distinguished:
  - peaks align in Hz            -> delays/topology CORRECT; only a linear loss missing.
  - peaks uniformly scaled by k  -> native sample-rate (Fs) error of factor k.
  - peaks randomly mismatched    -> delay/topology error.

Outputs JSON to tools/_ir/modal_match.json plus a human summary.
"""
import sys, os, json, math
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np
import scipy.io.wavfile as wav
from scipy.signal import find_peaks, get_window
import aru_datapath as A

NATIVE_HZ = 34130.0
DMASK = A.DMASK
PICK = lambda st: (st['b5'] << 1) | st['b4']
OUT = os.path.join(os.path.dirname(__file__), '_ir')
os.makedirs(OUT, exist_ok=True)


def fpc_input_steps(prog):
    return [p['s'] for p in prog if (p['offset'] & 0x8000) and (p['offset'] & 0x3FFF) == 0x3FFF and p['WA'] == 2]


def model_ir(prog, nsamp=65536, lam_eff=0.99995, seed=20000.0, lam_struct=1.001126):
    """Float-exact datapath; impulse at prog[0]. The growing tank is bounded by a
    UNIFORM per-sample state scale g=lam_eff/lam_struct applied to ALL state (DMEM +
    registers + ACC/RES) at each sample boundary -> net per-sample gain = lam_eff < 1.
    This is a flat (frequency-independent) decay: it sets RT60 but does NOT move modal
    frequencies. Returns (out, peak_abs)."""
    s0 = prog[0]['s']
    inj_done = False
    R = [0.0]*4; ACC = 0.0; RES = 0.0
    DM = np.zeros(DMASK+1, dtype=np.float64); pos = 0
    g = lam_eff / lam_struct
    steps = [(st, PICK(st), abs(st['coeff']), st['offset']) for st in prog]
    cs = [(-(m>>1) if st['coeff']<0 else (m>>1)) for st,_,m,_ in steps]
    out = np.empty(nsamp, dtype=np.float64)
    for n in range(nsamp):
        pos = (pos+1) & DMASK
        last = RES
        for k,(st,ra,mag,off) in enumerate(steps):
            addr = (pos - off) & DMASK
            dab = RES if st['b3'] else DM[addr]
            if not inj_done and st['s'] == s0:
                dab += seed; inj_done = True
            x = R[ra]; R[st['WA']] = dab
            if st['ZERO']: ACC = 0.0
            ACC = ACC + x*8.0*cs[k]/64.0
            if st['XFER']: RES = ACC/8.0
            if st['b3']: DM[addr] = RES
            if st['XFER']: last = RES
        out[n] = last
        # uniform per-sample leak on all state (keeps the growing tank bounded)
        DM *= g; R = [v*g for v in R]; ACC *= g; RES *= g
    peak = float(np.max(np.abs(out)))
    return out, peak


def est_lam_struct(prog, nsamp=6000):
    """Quick structural per-sample growth estimate (renormalized float run)."""
    R=[0.0]*4; ACC=0.0; RES=0.0; DM=np.zeros(DMASK+1); pos=0; seeded=False
    logg=0.0
    for n in range(nsamp):
        pos=(pos+1)&DMASK
        for st in prog:
            addr=(pos-st['offset'])&DMASK
            dab=RES if st['b3'] else DM[addr]
            if not seeded and st is prog[0]: dab+=20000.0; seeded=True
            mag=abs(st['coeff']); Cs=-(mag>>1) if st['coeff']<0 else (mag>>1)
            x=R[PICK(st)]; R[st['WA']]=dab
            if st['ZERO']: ACC=0.0
            ACC=ACC+x*8.0*Cs/64.0
            if st['XFER']: RES=ACC/8.0
            if st['b3']: DM[addr]=RES
        if (n+1)%128==0:
            s=float(np.sqrt(ACC*ACC+RES*RES+sum(v*v for v in R)+float(np.dot(DM,DM))))+1e-300
            f=1.0/s; R=[v*f for v in R]; ACC*=f; RES*=f; DM*=f; logg+=math.log(s)
    return math.exp(logg/nsamp)


def tuned_model_ir(prog, nsamp=65536, lam_eff=0.99995):
    ls = est_lam_struct(prog)
    out, pk = model_ir(prog, nsamp=nsamp, lam_eff=lam_eff, lam_struct=ls)
    head = float(np.sqrt(np.mean(out[nsamp//5:2*nsamp//5]**2)))
    tail = float(np.sqrt(np.mean(out[-nsamp//5:]**2)))
    print(f"  lam_struct~{ls:.6f} lam_eff={lam_eff}: peak={pk:.3e} "
          f"head_rms={head:.2e} tail_rms={tail:.2e} "
          f"{'OK' if (np.isfinite(pk) and pk>1 and pk<1e12) else 'BAD'}")
    return out, lam_eff


def spectrum_peaks(sig, fs, fmin=200.0, fmax=12000.0, npk=40, nfft=8192, prom=1.5):
    """Welch spectrum with PER-SEGMENT normalization (so any residual growth/decay
    can't dominate the average). High zero-padded resolution; prominence peaks."""
    sig = np.asarray(sig, dtype=np.float64)
    sig = sig - np.mean(sig)
    n0 = min(len(sig)//5, int(0.2*fs))
    sig = sig[n0:]
    if len(sig) < nfft:
        return None
    seglen = 2048
    win = get_window('hann', seglen)
    step = seglen // 2
    acc = np.zeros(nfft//2 + 1)
    cnt = 0
    for i in range(0, len(sig)-seglen, step):
        seg = sig[i:i+seglen]
        rms = np.sqrt(np.mean(seg**2)) + 1e-30
        seg = (seg/rms) * win                       # normalize each segment
        sp = np.abs(np.fft.rfft(seg, nfft))**2
        acc += sp; cnt += 1
    if cnt == 0:
        return None
    psd = acc / cnt
    freqs = np.fft.rfftfreq(nfft, 1.0/fs)
    logp = 10*np.log10(psd + 1e-30)
    k = np.ones(7)/7
    logs = np.convolve(logp, k, mode='same')
    band = (freqs >= fmin) & (freqs <= fmax)
    fb = freqs[band]; lb = logs[band]
    dist = max(1, int(35.0/(freqs[1]-freqs[0])))
    pk, props = find_peaks(lb, distance=dist, prominence=prom)
    order = np.argsort(props['prominences'])[::-1][:npk]
    pk = pk[order]
    peak_f = np.sort(fb[pk])
    return dict(freqs=fb.tolist(), logspec=lb.tolist(), peaks=peak_f.tolist())


def rt60_edc(sig, fs):
    """EDC (Schroeder) RT60 estimate from a decaying IR."""
    sig = np.asarray(sig, dtype=np.float64)
    e = sig**2
    edc = np.cumsum(e[::-1])[::-1]
    edc = edc / (edc[0] + 1e-30)
    db = 10*np.log10(edc + 1e-30)
    # fit -5..-35 dB region
    i5 = np.argmax(db <= -5); i35 = np.argmax(db <= -35)
    if i35 <= i5:
        return None
    t = np.arange(i5, i35)/fs
    y = db[i5:i35]
    a, b = np.polyfit(t, y, 1)
    return -60.0/a if a < 0 else float('inf')


def match(model_pk, p85_pk):
    """For each model peak find nearest P85 peak; report Hz error and ratio."""
    mp = np.array(model_pk); pp = np.array(p85_pk)
    rows = []
    ratios = []
    for f in mp:
        j = int(np.argmin(np.abs(pp - f)))
        nf = pp[j]
        rows.append((float(f), float(nf), float(f-nf), float(f/nf)))
        if 0.5 < f/nf < 2.0:
            ratios.append(f/nf)
    ratios = np.array(ratios)
    return rows, (float(np.median(ratios)) if len(ratios) else None), \
           (float(np.std(ratios)) if len(ratios) else None)


def common_grid_logspec(spec, fmin=2200.0, fmax=11800.0, npts=2400):
    """Resample a spectrum_peaks() result onto a common linear Hz grid, z-scored."""
    f = np.array(spec['freqs']); s = np.array(spec['logspec'])
    grid = np.linspace(fmin, fmax, npts)
    v = np.interp(grid, f, s)
    v = v - v.mean()
    sd = v.std() + 1e-30
    return grid, v / sd


def corr_vs_scale(model_spec, ref_spec, scales=None):
    """Cross-correlate model vs reference full log-spectra over a frequency-SCALE
    sweep (model freq axis * k). Returns (best_k, best_corr) and a chance level from
    a frequency-shuffled model. Scale-invariant to the dense-comb nearest-neighbour
    bias: this correlates the WHOLE spectral shape, not matched peaks."""
    if scales is None:
        scales = np.linspace(0.93, 1.07, 281)
    grid, ref = common_grid_logspec(ref_spec)
    mf = np.array(model_spec['freqs']); ms = np.array(model_spec['logspec'])
    best = (-2, None)
    curve = []
    for k in scales:
        v = np.interp(grid, mf * k, ms)
        v = v - v.mean(); v = v / (v.std() + 1e-30)
        c = float(np.mean(v * ref))
        curve.append((float(k), c))
        if c > best[0]:
            best = (c, float(k))
    # chance level: shuffle the model spectrum in blocks, correlate at k=1
    rng_idx = np.arange(len(ms))
    block = 53
    shuf = ms.copy()
    for b in range(0, len(ms) - block, block):
        seg = shuf[b:b+block][::-1]
        shuf[b:b+block] = seg
    vsh = np.interp(grid, mf, shuf); vsh = vsh - vsh.mean(); vsh = vsh/(vsh.std()+1e-30)
    chance = float(np.mean(vsh * ref))
    return dict(best_corr=best[0], best_scale=best[1], chance=chance, curve=curve)


def scrambled_prog(prog, seed=12345):
    """Control: shuffle the offsets among active steps -> destroys the tank topology
    while preserving coefficients/field map. If the modal match is topology-driven, this
    should correlate with P85 no better than chance."""
    import random
    rng = random.Random(seed)
    offs = [p['offset'] for p in prog]
    rng.shuffle(offs)
    out = [dict(p) for p in prog]
    for p, o in zip(out, offs):
        p['offset'] = o
    return out


def main():
    sr, d = wav.read('IR/Lexicon 224XL/P85 - 20.0 Seconds A.wav')
    p85 = d[:, 0].astype(np.float64)
    p85_spec = spectrum_peaks(p85, sr)
    p85_rt = rt60_edc(p85, sr)

    # V7.2 (a SECOND real CONCERT IR) -> real-vs-real correlation upper bound
    srv, dv = wav.read('IR/Lexicon 224XL/Concert Hall V7.2.L.wav')
    v72_spec = spectrum_peaks(dv.astype(np.float64), srv)

    prog = A.load_microcode(0x01)
    print(f"FPC input steps: {fpc_input_steps(prog)}")
    print("model CONCERT IR:")
    ir, leak = tuned_model_ir(prog)
    m_spec = spectrum_peaks(ir, NATIVE_HZ)
    m_rt = rt60_edc(ir, NATIVE_HZ)

    print("scrambled-offset control IR:")
    ir_s, _ = tuned_model_ir(scrambled_prog(prog))
    s_spec = spectrum_peaks(ir_s, NATIVE_HZ)

    rows, ratio_med, ratio_std = match(m_spec['peaks'], p85_spec['peaks'])

    cc_model = corr_vs_scale(m_spec, p85_spec)
    cc_scram = corr_vs_scale(s_spec, p85_spec)
    cc_v72 = corr_vs_scale(v72_spec, p85_spec)            # real vs real upper bound

    result = dict(
        native_hz=NATIVE_HZ, p85_sr=sr,
        p85_peaks=p85_spec['peaks'], model_peaks=m_spec['peaks'],
        p85_rt60=p85_rt, model_rt60=m_rt,
        match_rows=rows, ratio_median=ratio_med, ratio_std=ratio_std,
        corr_model_vs_p85=cc_model, corr_scrambled_vs_p85=cc_scram,
        corr_v72_vs_p85=cc_v72,
    )
    with open(os.path.join(OUT, 'modal_match.json'), 'w') as f:
        json.dump(result, f, indent=1)

    print(f"\nP85 RT60 ~ {p85_rt:.1f}s   model(leaked) RT60 ~ {m_rt:.2f}")
    print(f"\nP85 peaks (Hz):   {[round(x) for x in p85_spec['peaks']]}")
    print(f"model peaks (Hz): {[round(x) for x in m_spec['peaks']]}")
    print(f"\nnearest-peak median model/P85 ratio = {ratio_med:.4f} (std {ratio_std:.4f})")
    print(f"\n=== BIAS-FREE full-spectrum cross-correlation (vs P85) ===")
    print(f"  model CONCERT : best_corr={cc_model['best_corr']:.3f} @ scale={cc_model['best_scale']:.4f}  "
          f"(chance~{cc_model['chance']:.3f})")
    print(f"  V7.2 real IR  : best_corr={cc_v72['best_corr']:.3f} @ scale={cc_v72['best_scale']:.4f}  "
          f"(real-vs-real upper bound)")
    print(f"  SCRAMBLED ctrl: best_corr={cc_scram['best_corr']:.3f} @ scale={cc_scram['best_scale']:.4f}  "
          f"(topology destroyed -> chance)")
    print(f"\n  best_scale {cc_model['best_scale']:.4f} -> implied native Fs ~ "
          f"{NATIVE_HZ*cc_model['best_scale']:.0f} Hz (vs assumed {NATIVE_HZ:.0f})")
    verdict = ("TOPOLOGY MATCHES (delays correct; only a linear loss missing)"
               if cc_model['best_corr'] > 2*max(cc_scram['best_corr'], cc_model['chance'])
               else "INCONCLUSIVE / topology suspect")
    print(f"\n  VERDICT: {verdict}")
    print(f"\nwrote {os.path.join(OUT,'modal_match.json')}")


if __name__ == '__main__':
    main()
