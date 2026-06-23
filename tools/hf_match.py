"""Break the circularity: find the physical recirculation loss that BOTH stabilizes
the model AND makes its transfer function resemble P85. A per-closer one-pole lowpass
on the b3 write-back models frequency-dependent (HF) damping in the delay-line feedback
(the 'air absorption' a real hall has). Sweep the pole; for each, measure stability and
the P85 transfer-function correlation. A plausible pole that lands a HIGH correlation
(approaching the V7.2 real-vs-real benchmark ~0.92) jointly validates the topology and
identifies the missing loss.
"""
import sys, os, json, math
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np, scipy.io.wavfile as wav
import aru_datapath as A
from modal_tf import spec, corr_scale, NATIVE_HZ, FMIN, FMAX

DMASK = A.DMASK
PICK = lambda st: (st['b5'] << 1) | st['b4']


def hf_tf(prog, a, extra_leak=0.0, nsamp=90000, seed=3):
    """White-noise transfer function with a per-closer one-pole lowpass (pole a) on
    the b3 recirculation write-back + an optional flat leak. Returns (out, peak)."""
    s0 = prog[0]['s']
    rng = np.random.default_rng(seed)
    drive = rng.standard_normal(nsamp) * 4000.0
    steps = [(st, PICK(st), (-(abs(st['coeff'])>>1) if st['coeff']<0 else (abs(st['coeff'])>>1)), st['offset']) for st in prog]
    lp = {st['s']: 0.0 for st in prog if st['b3']}        # per-closer one-pole state
    g = 1.0 - extra_leak
    R=[0.0]*4; ACC=0.0; RES=0.0; DM=np.zeros(DMASK+1); pos=0
    out=np.empty(nsamp)
    for n in range(nsamp):
        pos=(pos+1)&DMASK; last=RES
        for st,ra,cs,off in steps:
            addr=(pos-off)&DMASK
            dab=RES if st['b3'] else DM[addr]
            if st['s']==s0: dab+=drive[n]
            x=R[ra]; R[st['WA']]=dab
            if st['ZERO']: ACC=0.0
            ACC=ACC+x*8.0*cs/64.0
            if st['XFER']: RES=ACC/8.0
            if st['b3']:
                s=st['s']; lp[s]=(1.0-a)*RES + a*lp[s]      # one-pole LP on the feedback
                DM[addr]=lp[s]*g
            if st['XFER']: last=RES
        out[n]=last
        if not np.isfinite(out[n]) or abs(out[n])>1e150:
            return out[:n+1], float('inf')
    return out, float(np.max(np.abs(out)))


def main():
    sr,d=wav.read('IR/Lexicon 224XL/P85 - 20.0 Seconds A.wav')
    pf,pl=spec(d[:,0].astype(float), sr)
    srv,dv=wav.read('IR/Lexicon 224XL/Concert Hall V7.2.L.wav')
    vf,vl=spec(dv.astype(float), srv); cv=corr_scale(vf,vl,pf,pl)
    print(f"benchmark: V7.2 real vs P85 corr={cv[0]:.3f} @ {cv[1]:.4f}\n")
    prog=A.load_microcode(0x01)
    print("per-closer one-pole HF-damping pole sweep (a):")
    best=(-2,None)
    for a in (0.0,0.2,0.4,0.5,0.6,0.7,0.8,0.85,0.9,0.95):
        out,pk=hf_tf(prog,a)
        if not np.isfinite(pk) or pk>1e12:
            # add a small flat leak to bound, retry once
            out,pk=hf_tf(prog,a,extra_leak=2e-4)
        stable = np.isfinite(pk) and pk<1e10 and len(out)>=80000
        if stable and pk>1e-6:
            f,l=spec(out,NATIVE_HZ); c,k=corr_scale(f,l,pf,pl)
        else:
            c,k=float('nan'),float('nan')
        print(f"  a={a:.2f}: peak={pk:.2e} stable={stable}  P85corr={c:+.3f} @ scale={k if k==k else 0:.4f}")
        if c==c and c>best[0]: best=(c,a)
    print(f"\nbest HF-damping pole a={best[1]} -> P85 corr={best[0]:.3f}  (V7.2 benchmark {cv[0]:.3f})")
    if best[0]>0.6:
        print("=> a physical HF-damping loss makes the model RESEMBLE P85: topology + loss jointly validated.")
    elif best[0]>0.35:
        print("=> partial: HF damping helps but a gap remains.")
    else:
        print("=> HF damping alone does not reproduce P85; deeper structural/probe issue.")


if __name__=='__main__':
    main()
