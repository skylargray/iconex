"""Definitive modal probe: continuous-noise-excited TRANSFER FUNCTION of the model
tank (poles = resonant frequencies, independent of I/O location), vs P85, with a
random-peak NULL and a delay-scrambled control. Fixes the over-damped single-impulse
probe (which smeared the modes and failed the null test).
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
FMIN, FMAX = 2200.0, 11900.0


def noise_tf(prog, nsamp=180000, lam_eff=0.999, lam_struct=None, seed=3):
    """Drive s0 with white noise; uniform per-sample state leak for stability; return
    the per-sample output (stationary). Spectrum of this = |H(f)| (all poles)."""
    if lam_struct is None:
        lam_struct = est_lam(prog)
    g = lam_eff/lam_struct
    s0 = prog[0]['s']
    rng = np.random.default_rng(seed)
    drive = rng.standard_normal(nsamp) * 4000.0
    R=[0.0]*4; ACC=0.0; RES=0.0; DM=np.zeros(DMASK+1); pos=0
    steps=[(st,PICK(st),(-(abs(st['coeff'])>>1) if st['coeff']<0 else (abs(st['coeff'])>>1)),st['offset']) for st in prog]
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
            if st['b3']: DM[addr]=RES
            if st['XFER']: last=RES
        out[n]=last
        DM*=g; R=[v*g for v in R]; ACC*=g; RES*=g
    return out


def est_lam(prog, nsamp=6000):
    R=[0.0]*4; ACC=0.0; RES=0.0; DM=np.zeros(DMASK+1); pos=0; seeded=False; logg=0.0
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


def spec(sig, fs, nfft=16384, seglen=8192):
    sig=np.asarray(sig,float); sig=sig-sig.mean()
    win=get_window('hann',seglen); step=seglen//2
    acc=np.zeros(nfft//2+1); cnt=0
    for i in range(0,len(sig)-seglen,step):
        seg=sig[i:i+seglen]; rms=np.sqrt(np.mean(seg**2))+1e-30
        acc+=np.abs(np.fft.rfft((seg/rms)*win,nfft))**2; cnt+=1
    psd=acc/max(cnt,1); fr=np.fft.rfftfreq(nfft,1.0/fs)
    logp=np.convolve(10*np.log10(psd+1e-30),np.ones(5)/5,mode='same')
    return fr, logp


def peaks(sig, fs, nfft=16384, seglen=8192, prom=1.2, npk=60):
    fr, logp = spec(sig, fs, nfft, seglen)
    bd=(fr>=FMIN)&(fr<=FMAX); fb=fr[bd]; lb=logp[bd]
    dist=max(1,int(30.0/(fr[1]-fr[0])))
    pk,pr=find_peaks(lb,distance=dist,prominence=prom)
    order=np.argsort(pr['prominences'])[::-1][:npk]
    return np.sort(fb[pk[order]])


def corr_scale(test_fr, test_lp, ref_fr, ref_lp, scales=None):
    if scales is None: scales=np.linspace(0.90,1.10,401)
    grid=np.linspace(FMIN,FMAX,2400)
    r=np.interp(grid,ref_fr,ref_lp); r=(r-r.mean())/(r.std()+1e-30)
    best=(-2,1.0)
    for k in scales:
        v=np.interp(grid,test_fr*k,test_lp); v=(v-v.mean())/(v.std()+1e-30)
        c=float(np.mean(v*r))
        if c>best[0]: best=(c,float(k))
    return best


def null_pvalue(test, ref, ntrials=4000, seed=7):
    test=test[(test>=FMIN)&(test<=FMAX)]; ref=ref[(ref>=FMIN)&(ref<=FMAX)]
    obs=np.median([np.min(np.abs(ref-f))/f for f in test])
    tight=int(np.sum([np.min(np.abs(ref-f))<10 for f in test]))
    rng=np.random.default_rng(seed); meds=[]; ts=[]
    for _ in range(ntrials):
        rp=rng.uniform(FMIN,FMAX,len(test))
        meds.append(np.median([np.min(np.abs(ref-f))/f for f in rp]))
        ts.append(np.sum([np.min(np.abs(ref-f))<10 for f in rp]))
    meds=np.array(meds); ts=np.array(ts)
    return dict(n=len(test), median_rel=float(obs), tight=tight,
                null_med=float(meds.mean()), p_median=float((meds<=obs).mean()),
                null_tight=float(ts.mean()), p_tight=float((ts>=tight).mean()))


def scrambled(prog, seed=12345):
    import random
    rng=random.Random(seed); offs=[p['offset'] for p in prog]; rng.shuffle(offs)
    out=[dict(p) for p in prog]
    for p,o in zip(out,offs): p['offset']=o
    return out


def main():
    sr,d=wav.read('IR/Lexicon 224XL/P85 - 20.0 Seconds A.wav')
    pf,pl=spec(d[:,0].astype(float), sr); p85=peaks(d[:,0].astype(float), sr)
    srv,dv=wav.read('IR/Lexicon 224XL/Concert Hall V7.2.L.wav')   # positive control (real CONCERT)
    vf,vl=spec(dv.astype(float), srv); v72=peaks(dv.astype(float), srv)
    prog=A.load_microcode(0x01); ls=est_lam(prog)
    print(f"model lam_struct~{ls:.6f}; white-noise transfer-function probe")
    mout=noise_tf(prog, lam_struct=ls); mf,ml=spec(mout,NATIVE_HZ); mpk=peaks(mout,NATIVE_HZ)
    sprog=scrambled(prog); sout=noise_tf(sprog, lam_struct=est_lam(sprog))
    sf,sl=spec(sout,NATIVE_HZ); spk=peaks(sout,NATIVE_HZ)

    print("\n--- PEAK-ALIGNMENT NULL TEST (p<0.05 = beats chance) ---")
    for name,pk,ref in [("MODEL vs P85",mpk,p85),("SCRAM vs P85",spk,p85),
                        ("V7.2  vs P85 [+ctrl]",v72,p85)]:
        r=null_pvalue(pk,ref)
        print(f"  {name:22}: median|df|/f={r['median_rel']*100:.3f}% (null {r['null_med']*100:.3f}%) "
              f"p_med={r['p_median']:.3f}  tight={r['tight']}/{r['n']}(null {r['null_tight']:.1f}) p_tight={r['p_tight']:.3f}")

    print("\n--- FULL-SPECTRUM CORRELATION vs P85, over Fs-scale (corr, best_scale) ---")
    cm=corr_scale(mf,ml,pf,pl); cs=corr_scale(sf,sl,pf,pl); cv=corr_scale(vf,vl,pf,pl)
    print(f"  MODEL : corr={cm[0]:+.3f} @ scale={cm[1]:.4f}")
    print(f"  SCRAM : corr={cs[0]:+.3f} @ scale={cs[1]:.4f}")
    print(f"  V7.2 [+ctrl]: corr={cv[0]:+.3f} @ scale={cv[1]:.4f}  (real CONCERT vs real CONCERT)")
    json.dump(dict(p85=p85.tolist(),model=mpk.tolist(),scram=spk.tolist(),v72=v72.tolist(),
                   corr_model=cm,corr_scram=cs,corr_v72=cv),
              open(os.path.join(os.path.dirname(__file__),'_ir','modal_tf.json'),'w'),indent=1)
    print("\nINTERPRETATION: if V7.2[+ctrl] clearly beats SCRAM but MODEL ~ SCRAM ->")
    print("  test HAS power and the model's tank resonances genuinely DIFFER from P85.")
    print("  if V7.2 ~ SCRAM too -> dense-comb test lacks power (inconclusive).")


if __name__=='__main__':
    main()
