"""Single-point evaluator for the recirculation-damping search.

Model TF (white-noise excited, FPC right-output tap) with a recirculation loss =
  uniform per-sample state leak (flat, sets overall RT, GUARANTEES stability)
  + per-b3 one-pole lowpass (pole a -> frequency-dependent HF/mid rolloff in the loop).
Reports the full-spectrum correlation with the P85 hardware IR (the success metric;
V7.2 real-vs-real benchmark ~0.92) and the self-consistency (2 seeds).

Usage: python damp_probe.py <lam_eff> <lp_pole> [nsamp]
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np, scipy.io.wavfile as wav
import aru_datapath as A
from modal_tf import spec, corr_scale, est_lam, NATIVE_HZ

DMASK = A.DMASK
PICK = lambda st: (st['b5'] << 1) | st['b4']
_P85 = None


def p85_spec():
    global _P85
    if _P85 is None:
        sr, d = wav.read('IR/Lexicon 224XL/P85 - 20.0 Seconds A.wav')
        _P85 = spec(d[:, 0].astype(float), sr)
    return _P85


def out_steps(prog, want14):
    return set(p['s'] for p in prog if (p['offset'] & 0x8000) and p['WA'] == 3
              and (p['offset'] & 0x4000) == want14)


def tf(prog, lam_eff, a, nsamp, seed, lam_struct):
    g = lam_eff/lam_struct; s0 = prog[0]['s']
    rng = np.random.default_rng(seed); drive = rng.standard_normal(nsamp)*4000.0
    steps = [(st, PICK(st), (-(abs(st['coeff'])>>1) if st['coeff']<0 else (abs(st['coeff'])>>1)), st['offset']) for st in prog]
    fr = out_steps(prog, 0)               # right channel (best-correlating in scouting)
    lp = {st['s']: 0.0 for st in prog if st['b3']}
    R=[0.0]*4; ACC=0.0; RES=0.0; DM=np.zeros(DMASK+1); pos=0
    o=np.empty(nsamp)
    for n in range(nsamp):
        pos=(pos+1)&DMASK; rs=0.0
        for st,ra,cs,off in steps:
            addr=(pos-off)&DMASK
            dab=RES if st['b3'] else DM[addr]
            if st['s']==s0: dab+=drive[n]
            x=R[ra]; R[st['WA']]=dab
            if st['ZERO']: ACC=0.0
            ACC=ACC+x*8.0*cs/64.0
            if st['XFER']: RES=ACC/8.0
            if st['b3']:
                s=st['s']
                if a>0: lp[s]=(1.0-a)*RES+a*lp[s]; DM[addr]=lp[s]
                else: DM[addr]=RES
            if st['s'] in fr: rs+=RES
        o[n]=rs
        DM*=g; R=[v*g for v in R]; ACC*=g; RES*=g
        if not np.isfinite(o[n]) or abs(o[n])>1e120: return None
    return o


def main():
    lam_eff = float(sys.argv[1]); a = float(sys.argv[2])
    nsamp = int(sys.argv[3]) if len(sys.argv) > 3 else 130000
    pf, pl = p85_spec()
    prog = A.load_microcode(0x01); ls = est_lam(prog)
    o1 = tf(prog, lam_eff, a, nsamp, 3, ls)
    if o1 is None:
        print(f"lam_eff={lam_eff} a={a}: UNSTABLE"); return
    f1, l1 = spec(o1, NATIVE_HZ); c1, k1 = corr_scale(f1, l1, pf, pl)
    o2 = tf(prog, lam_eff, a, nsamp, 17, ls)
    f2, l2 = spec(o2, NATIVE_HZ); selfc = corr_scale(f1, l1, f2, l2)[0]
    print(f"lam_eff={lam_eff:.5f} a={a:.2f}: P85corr={c1:+.3f} @scale={k1:.4f}  "
          f"self={selfc:.3f}  corr_corr={c1/max(selfc,0.1)**0.5:+.3f}")


if __name__ == '__main__':
    main()
