"""Grid search: recirculation loss = uniform flat leak (lam_eff) + per-b3 one-pole LP
(pole a, HF rolloff). Maximize the FPC-right transfer-function correlation with P85
(success benchmark: V7.2 real-vs-real = 0.92). Reports each point; the best identifies
the loss that makes the model most resemble the real hardware.
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np, scipy.io.wavfile as wav
import aru_datapath as A
from modal_tf import spec, corr_scale, est_lam, NATIVE_HZ
from damp_probe import tf

NSAMP = 110000


def main():
    sr, d = wav.read('IR/Lexicon 224XL/P85 - 20.0 Seconds A.wav')
    pf, pl = spec(d[:, 0].astype(float), sr)
    srv, dv = wav.read('IR/Lexicon 224XL/Concert Hall V7.2.L.wav')
    vf, vl = spec(dv.astype(float), srv)
    print(f"benchmark V7.2 vs P85 = {corr_scale(vf, vl, pf, pl)[0]:.3f}; scramble ~0.30\n")
    prog = A.load_microcode(0x01); ls = est_lam(prog)
    best = (-2, None)
    for lam_eff in (0.999, 0.997, 0.995, 0.99, 0.985):
        row = []
        for a in (0.0, 0.3, 0.5, 0.6, 0.7, 0.8, 0.85):
            o = tf(prog, lam_eff, a, NSAMP, 3, ls)
            if o is None:
                row.append((a, None)); print(f"  lam_eff={lam_eff} a={a}: UNSTABLE"); continue
            f, l = spec(o, NATIVE_HZ); c, k = corr_scale(f, l, pf, pl)
            row.append((a, c))
            if c > best[0]: best = (c, (lam_eff, a, k))
            print(f"  lam_eff={lam_eff:.4f} a={a:.2f}: P85corr={c:+.3f} @scale={k:.4f}")
        print()
    print(f"BEST: corr={best[0]:.3f} at lam_eff,a,scale={best[1]}")
    print(f"(V7.2 real benchmark 0.92; scramble 0.30; flat-leak-only baseline ~0.53)")


if __name__ == '__main__':
    main()
