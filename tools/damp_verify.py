"""Verify the HF-damped model: clean exponential decay + HF<LF (matches V7.2's measured
3.79 s/5.25 s), with the best loss from the grid (flat leak + per-b3 one-pole, a~0.7).
Confirms the model now DECAYS (no growth/limit-cycle) and reproduces frequency-dependent
decay -- the 'definition of done' from the investigation.
"""
import sys, os, math
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np, scipy.io.wavfile as wav
from scipy.signal import butter, sosfiltfilt
import aru_datapath as A
from modal_tf import est_lam, NATIVE_HZ
from damp_probe import out_steps

DMASK = A.DMASK
PICK = lambda st: (st['b5'] << 1) | st['b4']


def impulse(prog, lam_eff, a, nsamp, lam_struct, seed_imp=20000.0):
    g = lam_eff/lam_struct; s0 = prog[0]['s']; injected = False
    steps = [(st, PICK(st), (-(abs(st['coeff'])>>1) if st['coeff']<0 else (abs(st['coeff'])>>1)), st['offset']) for st in prog]
    fr = out_steps(prog, 0)
    lp = {st['s']: 0.0 for st in prog if st['b3']}
    R=[0.0]*4; ACC=0.0; RES=0.0; DM=np.zeros(DMASK+1); pos=0; o=np.empty(nsamp)
    for n in range(nsamp):
        pos=(pos+1)&DMASK; rs=0.0
        for st,ra,cs,off in steps:
            addr=(pos-off)&DMASK
            dab=RES if st['b3'] else DM[addr]
            if not injected and st['s']==s0: dab+=seed_imp; injected=True
            x=R[ra]; R[st['WA']]=dab
            if st['ZERO']: ACC=0.0
            ACC=ACC+x*8.0*cs/64.0
            if st['XFER']: RES=ACC/8.0
            if st['b3']:
                s=st['s']
                if a>0: lp[s]=(1.0-a)*RES+a*lp[s]; DM[addr]=lp[s]
                else: DM[addr]=RES
            if st['s'] in fr: rs+=RES
        o[n]=rs; DM*=g; R=[v*g for v in R]; ACC*=g; RES*=g
    return o


def band_rt(sig, fs, f1, f2):
    sos = butter(4, [f1, f2], btype='band', fs=fs, output='sos')
    y = sosfiltfilt(sos, sig)
    e = y**2; edc = np.cumsum(e[::-1])[::-1]; edc /= edc[0]+1e-30
    db = 10*np.log10(edc+1e-30)
    i1 = np.argmax(db <= -5); i2 = np.argmax(db <= -25)
    if i2 <= i1: return None
    t = np.arange(i1, i2)/fs; sl = np.polyfit(t, db[i1:i2], 1)[0]
    return (-60.0/sl) if sl < 0 else float('inf')


def main():
    prog = A.load_microcode(0x01); ls = est_lam(prog)
    # choose flat leak so overall (LF) RT is a few seconds (measurable) with HF damping on
    lam_eff, a, nsamp = 0.99985, 0.7, 200000
    print(f"HF-damped model: lam_eff={lam_eff} (flat), a={a} (HF LP). Generating {nsamp/NATIVE_HZ:.1f}s IR...")
    o = impulse(prog, lam_eff, a, nsamp, ls)
    pk = float(np.max(np.abs(o)))
    grows = abs(o[-nsamp//10:]).mean() > abs(o[nsamp//3:nsamp//3+nsamp//10]).mean()
    print(f"  peak={pk:.1f}  {'GROWS (still unstable)' if grows else 'DECAYS (stable)'}")
    for f1, f2, name in [(300, 800, 'LF ~0.5kHz'), (1500, 2500, 'MID ~2kHz'),
                         (3000, 6000, 'HF ~4.5kHz'), (6000, 10000, 'VHF ~8kHz')]:
        rt = band_rt(o, NATIVE_HZ, f1, f2)
        print(f"  {name:12} RT60 = {rt if rt is None else round(rt,2)} s")
    print("\n  Hardware refs: P85 overall ~20-30 s; V7.2 LF 5.25 s / HF 3.79 s (HF<LF).")
    print("  Success = clean decay (no growth) AND HF RT60 < LF RT60 (frequency-dependent).")


if __name__ == '__main__':
    main()
