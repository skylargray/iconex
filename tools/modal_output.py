"""Control the output-tap confound: the full-spectrum P85 correlation depends on which
output tap the model TF uses (mode amplitudes are I/O-dependent, though pole frequencies
are not). The prior runs used a single arbitrary tap (last RES). Here we compute the TF
for several faithful output definitions and correlate each with P85. If ANY representative
output gives a high correlation, the topology is fine and the earlier low score was a
bad-output-tap artifact.
"""
import sys, os, json
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np, scipy.io.wavfile as wav
import aru_datapath as A
from modal_tf import spec, corr_scale, est_lam, scrambled, NATIVE_HZ

DMASK = A.DMASK
PICK = lambda st: (st['b5'] << 1) | st['b4']


def fpc_output_steps(prog, channel='left'):
    # FPC output = pass-through WA=3, bit15 set; channel from bit14 (1=left->A,D /
    # 0=right->B,C). P85 ch0 = Left. (doc 12)
    want14 = 0x4000 if channel == 'left' else 0
    return [p['s'] for p in prog if (p['offset'] & 0x8000) and p['WA'] == 3
            and (p['offset'] & 0x4000) == want14]


def noise_tf_multi(prog, nsamp=200000, lam_eff=0.999, lam_struct=None, seed=3):
    """Return faithful output streams: last-RES, sum of signed XFER RES, and the LEFT
    and RIGHT FPC-output-tap sums (the actual DAC writes)."""
    if lam_struct is None: lam_struct = est_lam(prog)
    g = lam_eff/lam_struct; s0 = prog[0]['s']
    rng = np.random.default_rng(seed); drive = rng.standard_normal(nsamp)*4000.0
    steps = [(st, PICK(st), (-(abs(st['coeff'])>>1) if st['coeff']<0 else (abs(st['coeff'])>>1)), st['offset']) for st in prog]
    flout = set(fpc_output_steps(prog, 'left')); frout = set(fpc_output_steps(prog, 'right'))
    R=[0.0]*4; ACC=0.0; RES=0.0; DM=np.zeros(DMASK+1); pos=0
    o_last=np.empty(nsamp); o_sum=np.empty(nsamp); o_L=np.empty(nsamp); o_R=np.empty(nsamp)
    for n in range(nsamp):
        pos=(pos+1)&DMASK; last=RES; ssum=0.0; lsum=0.0; rsum=0.0
        for st,ra,cs,off in steps:
            addr=(pos-off)&DMASK
            dab=RES if st['b3'] else DM[addr]
            if st['s']==s0: dab+=drive[n]
            x=R[ra]; R[st['WA']]=dab
            if st['ZERO']: ACC=0.0
            ACC=ACC+x*8.0*cs/64.0
            if st['XFER']: RES=ACC/8.0; last=RES; ssum+=RES
            if st['b3']: DM[addr]=RES
            if st['s'] in flout: lsum+=RES
            elif st['s'] in frout: rsum+=RES
        o_last[n]=last; o_sum[n]=ssum; o_L[n]=lsum; o_R[n]=rsum
        DM*=g; R=[v*g for v in R]; ACC*=g; RES*=g
    return dict(last=o_last, sum=o_sum, fpcL=o_L, fpcR=o_R)


def main():
    sr, d = wav.read('IR/Lexicon 224XL/P85 - 20.0 Seconds A.wav')
    pf, pl = spec(d[:, 0].astype(float), sr)
    srv, dv = wav.read('IR/Lexicon 224XL/Concert Hall V7.2.L.wav')
    vf, vl = spec(dv.astype(float), srv)
    print(f"benchmark V7.2 vs P85: {corr_scale(vf, vl, pf, pl)[0]:+.3f}")
    print(f"FPC output steps: {fpc_output_steps(A.load_microcode(0x01))}\n")

    prog = A.load_microcode(0x01)
    outs = noise_tf_multi(prog)
    print("model P85-correlation by OUTPUT tap:")
    best = -2
    for name, sig in outs.items():
        if np.all(sig == 0) or not np.isfinite(sig).all():
            print(f"  {name:12}: (empty/nan)"); continue
        f, l = spec(sig, NATIVE_HZ); c, k = corr_scale(f, l, pf, pl)
        best = max(best, c)
        print(f"  {name:12}: corr={c:+.3f} @ scale={k:.4f}")
    # self-consistency: model(seedA) vs model(seedB) on the 'sum' output -> should be high
    o2 = noise_tf_multi(prog, seed=99)['sum']
    f1, l1 = spec(outs['sum'], NATIVE_HZ); f2, l2 = spec(o2, NATIVE_HZ)
    print(f"\nmetric sanity: model 'sum' seedA vs seedB corr = {corr_scale(f1, l1, f2, l2)[0]:+.3f} (should be ~1.0)")
    print(f"\nbest model output vs P85 = {best:+.3f}  (V7.2 benchmark 0.92)")


if __name__ == '__main__':
    main()
