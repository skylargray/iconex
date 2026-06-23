#!/usr/bin/env python3
"""Decisive topology test: stabilize the model with a small FLAT per-pass leak (the
calibrated-leak hypothesis itself), inject at the real input s76, and compare its
resonance/comb structure + decay to the real P85 (20 s default).
 - If the stabilized model's comb peaks line up with P85 -> topology correct, the
   ~0.08% is a flat gain excess, and a documented leak reproduces a real-looking reverb.
 - If the comb structure is unlike P85 -> a tap-delay/routing error remains.
The leak is applied as RES *= (1-leak) at each XFER (frequency-flat, preserves the
all-pass coefficients and thus the resonance FREQUENCIES; only lowers Q / loop gain).
"""
import sys, os, math, numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import aru_datapath as A
OUT=os.path.join(os.path.dirname(__file__),'_ir'); DMASK=A.DMASK; NATIVE=34130.0

def model_ir_leak(prog, pick, nsamp, leak, imp=8000):
    R=[0,0,0,0]; ACC=0; RES=0; DM=[0]*(DMASK+1); pos=0; out=[]
    g=1.0-leak
    s76 = next((p for p in prog if p['s']==76), prog[0])   # inject at the FPC input read
    for n in range(nsamp):
        pos=(pos+1)&DMASK; lastres=RES
        for st in prog:
            addr=(pos-st['offset'])&DMASK
            dab=RES if st['b3'] else DM[addr]
            if n==0 and st is s76: dab+=imp
            mag=abs(st['coeff']); Cs=-(mag>>1) if st['coeff']<0 else (mag>>1)
            x=R[pick(st)]; R[st['WA']]=dab
            if st['ZERO']: ACC=0
            ACC=A.sat20(ACC+(((x<<3)*Cs)>>6))
            if st['XFER']:
                RES=A.sat16(int((ACC>>3)*g)); lastres=RES
            if st['b3']: DM[addr]=RES
        out.append(lastres)
    return np.array(out,float)

def rt60(x, fs):
    e=np.abs(np.asarray(x,float))
    B=256; nb=len(e)//B
    if nb<10: return float('inf')
    env=np.array([np.sqrt((e[i*B:(i+1)*B]**2).mean()) for i in range(nb)])
    # use only the early/mid decay region (peak to peak-40dB) for a clean RT
    pk=env.max() or 1.0
    env=np.where(env>pk*1e-4, env, pk*1e-4)
    y=20*np.log10(env); pkb=int(np.argmax(env))
    lo=pkb+1; hi=min(len(y), pkb+1+int(fs*0.4/B)*3)
    if hi-lo<8: return float('inf')
    xs=np.arange(lo,hi)
    sl=np.polyfit(xs, y[lo:hi],1)[0]
    dbs=sl*fs/B
    return (-60.0/dbs) if dbs<-1e-3 else float('inf')

def comb(x, fs, lo=200, hi=8000, n=16):
    seg=np.asarray(x,float); seg=seg[:int(fs*0.5)]
    seg=(seg-seg.mean())*np.hanning(len(seg))
    S=np.abs(np.fft.rfft(seg)); f=np.fft.rfftfreq(len(seg),1/fs)
    b=(f>=lo)&(f<=hi); fb,Sb=f[b],S[b]
    mx=Sb.max()
    if not np.isfinite(mx) or mx<=0: return []
    Sb=Sb/mx
    idx=[i for i in range(1,len(Sb)-1) if Sb[i]>Sb[i-1] and Sb[i]>Sb[i+1] and Sb[i]>0.25]
    idx.sort(key=lambda i:Sb[i],reverse=True)
    return sorted(round(float(fb[i])) for i in idx[:n])

def main():
    prog=A.load_microcode(0x01); pick=lambda st:(st['b5']<<1)|st['b4']
    p=np.load(os.path.join(OUT,'p85_ir.npy')); FP=48000.0
    print("Sweeping leak to find a clean decay; comparing comb to P85.\n")
    print("P85 comb (Hz):", comb(p,FP))
    print(f"P85 RT60 ~ {rt60(p,FP):.1f}s\n")
    for leak in (0.01, 0.02, 0.05, 0.10, 0.20):
        m=model_ir_leak(prog,pick,int(NATIVE*0.6),leak,imp=500)
        rt=rt60(m,NATIVE); rts='SUSTAIN' if rt==float('inf') else f'{rt:.2f}s'
        print(f"leak={leak*100:5.1f}%  peak={np.abs(m).max():>7.0f}  RT60={rts:<8} comb(Hz)={comb(m,NATIVE)}")

if __name__=='__main__':
    main()
