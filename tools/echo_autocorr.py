#!/usr/bin/env python3
"""Robust topology test: compare loop-delay / resonance structure via autocorrelation
and spectrum, which reflect the recirculation delays independent of injection point,
output tap, and loop gain. If the model's tank delays match the real P85 (same default
program), the topology is right and the ~0.08% is a flat gain excess (-> calibrated
leak). If the delay structure differs, there's a tap-delay error to hunt.
"""
import sys, os, numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
OUT=os.path.join(os.path.dirname(__file__),'_ir')

def autocorr_peaks(x, fs, lo_ms=1, hi_ms=60, n=12):
    x=np.asarray(x,float)
    # use an early-to-mid window to avoid the model's late growth dominating
    seg=x[:int(fs*0.5)]
    seg=seg-seg.mean()
    ac=np.correlate(seg,seg,'full')[len(seg)-1:]
    ac=ac/ (ac[0] or 1.0)
    lo=int(fs*lo_ms/1000); hi=int(fs*hi_ms/1000)
    peaks=[]
    for i in range(lo+1,hi-1):
        if ac[i]>ac[i-1] and ac[i]>ac[i+1] and ac[i]>0.05:
            peaks.append((i, ac[i]))
    peaks.sort(key=lambda p:p[1],reverse=True)
    return [(round(i/fs*1000,2), round(float(v),3)) for i,v in peaks[:n]]

def spec_comb(x, fs, lo=200, hi=8000, n=14):
    x=np.asarray(x,float)
    seg=x[:int(fs*0.5)]; seg=(seg-seg.mean())*np.hanning(len(seg))
    S=np.abs(np.fft.rfft(seg)); f=np.fft.rfftfreq(len(seg),1/fs)
    b=(f>=lo)&(f<=hi); fb,Sb=f[b],S[b]; Sb=Sb/Sb.max()
    idx=[i for i in range(1,len(Sb)-1) if Sb[i]>Sb[i-1] and Sb[i]>Sb[i+1] and Sb[i]>0.3]
    idx.sort(key=lambda i:Sb[i],reverse=True)
    return sorted([round(float(fb[i]),0) for i in idx[:n]])

def main():
    m=np.load(os.path.join(OUT,'model_ir.npy')); FM=34130.0
    p=np.load(os.path.join(OUT,'p85_ir.npy'));   FP=48000.0
    v=np.load(os.path.join(OUT,'v72_ir.npy'));   FV=96000.0
    print("=== Autocorrelation delay peaks (ms, normalized) -- the loop/comb spacing ===")
    print("  model:", autocorr_peaks(m,FM))
    print("  P85  :", autocorr_peaks(p,FP))
    print("  V7.2 :", autocorr_peaks(v,FV))
    print("\n=== Spectral comb peaks (Hz) -- resonance frequencies ===")
    print("  model:", spec_comb(m,FM))
    print("  P85  :", spec_comb(p,FP))
    print("  V7.2 :", spec_comb(v,FV))
    # Cross-check: do the model's strongest delay peaks have a counterpart in P85?
    md=[t for t,_ in autocorr_peaks(m,FM)]
    pd=[t for t,_ in autocorr_peaks(p,FP)]
    print("\n=== model delay peaks matched to nearest P85 delay peak (ms) ===")
    for t in md:
        if pd:
            nearest=min(pd,key=lambda u:abs(u-t))
            print(f"  model {t:>6.2f} ms  ->  P85 {nearest:>6.2f} ms   (|Δ|={abs(nearest-t):.2f} ms)")

if __name__=='__main__':
    main()
