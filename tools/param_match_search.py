"""Does ANY reachable CONCERT parameter state make the model's transfer function
resemble P85? Honors the insight that P85 = default + max RT60 (a non-default state).
Sweeps decay/crossover/predelay params, generates each TF, correlates with P85.
If the best approaches the V7.2 real-vs-real benchmark (~0.92), topology is confirmed
at that state; if all stay near the scramble level (~0.30), the mismatch is structural.
"""
import sys, os, json
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np, scipy.io.wavfile as wav
import aru_datapath as A
from modal_tf import noise_tf, spec, corr_scale, est_lam, scrambled, NATIVE_HZ

SW = json.load(open(os.path.join(os.path.dirname(__file__), '..', 'docs', 'reference',
               '224', '224XL_param_sweep_01.json')))
CT = {p['param']: {int(k): v for k, v in p['coeff_table'].items()} for p in SW['params']}
DT = {p['param']: {int(k): v for k, v in p['delay_table'].items()} for p in SW['params']}


def apply(prog, coeff_set=None, delay_set=None):
    out = [dict(p) for p in prog]; bs = {p['s']: p for p in out}
    for par, idx in (coeff_set or {}).items():
        for s, v in CT.get(par, {}).items():
            if s in bs: bs[s]['coeff'] = v[idx]
    for par, idx in (delay_set or {}).items():
        for s, v in DT.get(par, {}).items():
            if s in bs: bs[s]['offset'] = v[idx]
    return out


def tf_corr(prog, pf, pl, nsamp=60000):
    ls = est_lam(prog)
    out = noise_tf(prog, nsamp=nsamp, lam_struct=ls)
    f, l = spec(out, NATIVE_HZ)
    return corr_scale(f, l, pf, pl)


def main():
    sr, d = wav.read('IR/Lexicon 224XL/P85 - 20.0 Seconds A.wav')
    pf, pl = spec(d[:, 0].astype(float), sr)
    srv, dv = wav.read('IR/Lexicon 224XL/Concert Hall V7.2.L.wav')
    vf, vl = spec(dv.astype(float), srv)
    cv = corr_scale(vf, vl, pf, pl)
    print(f"benchmark V7.2 (real) vs P85: corr={cv[0]:.3f} @ {cv[1]:.4f}\n")

    prog = A.load_microcode(0x01)
    settings = [
        ("default idx0", {}, {}),
        ("MID idx7 (short)", {1: 7}, {}),
        ("XOV idx6 (hottest)", {2: 6}, {}),
        ("XOV idx0", {2: 0}, {}),
        ("LOW idx7", {0: 7}, {}),
        ("max-RT: LOW7 MID0 XOV6", {0: 7, 1: 0, 2: 6}, {}),
        ("max-RT: LOW7 XOV6 HFD0 DEP0", {0: 7, 2: 6, 3: 0, 4: 0}, {}),
        ("all idx2", {0: 2, 1: 2, 2: 2, 3: 2, 4: 2}, {}),
        ("all idx5", {0: 5, 1: 5, 2: 5, 3: 5, 4: 5}, {}),
        ("PDL idx0 (max predelay)", {}, {5: 0}),
        ("PDL idx5 (min predelay)", {}, {5: 5}),
        ("max-RT + PDL0", {0: 7, 2: 6}, {5: 0}),
    ]
    rows = []
    for name, cs, ds in settings:
        p2 = apply(prog, cs, ds)
        c, k = tf_corr(p2, pf, pl)
        rows.append((c, k, name))
        print(f"  {name:30}: corr={c:+.3f} @ scale={k:.4f}")
    # scramble reference
    cscr = tf_corr(scrambled(prog), pf, pl)
    print(f"\n  [delay-scramble reference]      : corr={cscr[0]:+.3f} @ {cscr[1]:.4f}")
    rows.sort(reverse=True)
    best = rows[0]
    print(f"\nBEST param state: '{best[2]}' corr={best[0]:.3f} @ scale={best[1]:.4f}")
    print(f"V7.2 benchmark={cv[0]:.3f}; scramble={cscr[0]:.3f}")
    if best[0] > 0.6:
        print("=> a reachable param state RESEMBLES P85 -> topology OK; P85 was that state.")
    elif best[0] > cscr[0] + 0.2:
        print("=> partial resemblance; param state matters but gap remains.")
    else:
        print("=> NO param state resembles P85 (all near scramble) -> structural/topology or instability-confound.")
    json.dump([(name, c, k) for c, k, name in rows] + [("V72", cv[0], cv[1]), ("scram", cscr[0], cscr[1])],
              open(os.path.join(os.path.dirname(__file__), '_ir', 'param_match.json'), 'w'), indent=1)


if __name__ == '__main__':
    main()
