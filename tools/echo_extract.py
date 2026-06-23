#!/usr/bin/env python3
"""Extract impulse-response features for the echo-pattern comparison:
  - model IR (booted-default CONCERT, audio proxy = last RES per sample, 34130 Hz)
  - real P85 IR (48 kHz stereo -> left), the 20 s default
  - real V7.2 IR (96 kHz mono), the 4.86 s state
Saves arrays to tools/_ir/ and prints onset/predelay, early-reflection peaks, and the
early-IR spectrum (does the real IR contain the model's spurious ~3653 Hz mode?).
"""
import sys, os, math
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np, soundfile as sf
import aru_datapath as A

DMASK = A.DMASK
NATIVE_HZ = 34130.0
OUT = os.path.join(os.path.dirname(__file__), '_ir')
os.makedirs(OUT, exist_ok=True)


def model_ir(prog, pick, nsamp, imp=20000):
    R=[0,0,0,0]; ACC=0; RES=0; DM=[0]*(DMASK+1); pos=0; out=[]
    for n in range(nsamp):
        pos=(pos+1)&DMASK; lastres=RES
        for st in prog:
            addr=(pos-st['offset'])&DMASK
            dab=RES if st['b3'] else DM[addr]
            if n==0 and st is prog[0]: dab+=imp
            mag=abs(st['coeff']); Cs=-(mag>>1) if st['coeff']<0 else (mag>>1)
            x=R[pick(st)]; R[st['WA']]=dab
            if st['ZERO']: ACC=0
            ACC=A.sat20(ACC+(((x<<3)*Cs)>>6))
            if st['XFER']: RES=A.sat16(ACC>>3); lastres=RES
            if st['b3']: DM[addr]=RES
        out.append(lastres)
    return np.array(out, dtype=float)


def onset_ms(x, fs, thresh_frac=0.02, win_ms=200):
    """time of first sample exceeding thresh_frac of the peak in the first win_ms."""
    nwin=int(fs*win_ms/1000)
    seg=np.abs(x[:nwin]); pk=seg.max() or 1.0
    idx=np.argmax(seg > thresh_frac*pk)
    return idx/fs*1000.0


def early_peaks(x, fs, n=12, span_ms=120, min_gap_ms=2):
    """times (ms) of the first n local energy maxima in the early IR (reflection pattern)."""
    nwin=int(fs*span_ms/1000)
    e=np.abs(x[:nwin]).astype(float)
    # smooth a touch
    k=max(1,int(fs*0.0003))
    if k>1: e=np.convolve(e,np.ones(k)/k,'same')
    peaks=[]; gap=int(fs*min_gap_ms/1000)
    order=np.argsort(e)[::-1]
    for i in order:
        if all(abs(i-p)>gap for p in peaks):
            peaks.append(i)
        if len(peaks)>=n: break
    peaks=sorted(peaks)
    return [round(p/fs*1000.0,2) for p in peaks]


def spectrum_peaks(x, fs, lo=200, hi=8000, n=6, start=0, length=8192):
    seg=x[start:start+length].astype(float)
    if len(seg)<length: seg=np.pad(seg,(0,length-len(seg)))
    seg=seg*np.hanning(len(seg))
    S=np.abs(np.fft.rfft(seg)); f=np.fft.rfftfreq(len(seg),1/fs)
    band=(f>=lo)&(f<=hi)
    fb,Sb=f[band],S[band]
    # top n local peaks
    idx=[]
    for i in range(1,len(Sb)-1):
        if Sb[i]>Sb[i-1] and Sb[i]>Sb[i+1]: idx.append(i)
    idx=sorted(idx,key=lambda i:Sb[i],reverse=True)[:n]
    return sorted([(round(float(fb[i]),1), round(float(Sb[i]/Sb.max()),3)) for i in idx])


def energy_at(x, fs, freq, bw=80, start=0, length=8192):
    seg=x[start:start+length].astype(float)
    if len(seg)<length: seg=np.pad(seg,(0,length-len(seg)))
    seg=seg*np.hanning(len(seg))
    S=np.abs(np.fft.rfft(seg)); f=np.fft.rfftfreq(len(seg),1/fs)
    band=(f>=freq-bw)&(f<=freq+bw)
    tot=np.sqrt((S**2).mean())
    return float(np.sqrt((S[band]**2).mean())/ (tot or 1.0))


def main():
    prog=A.load_microcode(0x01); pick=lambda st:(st['b5']<<1)|st['b4']
    print("Generating model IR (booted default, ~0.6 s)...")
    m=model_ir(prog,pick, int(NATIVE_HZ*0.6))
    np.save(os.path.join(OUT,'model_ir.npy'), m)

    p85,fs1=sf.read('IR/Lexicon 224XL/P85 - 20.0 Seconds A.wav', always_2d=True)
    p85=p85[:,0]
    v72,fs2=sf.read('IR/Lexicon 224XL/Concert Hall V7.2.L.wav', always_2d=True)
    v72=v72[:,0]
    np.save(os.path.join(OUT,'p85_ir.npy'), p85)
    np.save(os.path.join(OUT,'v72_ir.npy'), v72)

    print(f"\n{'IR':<14}{'fs':>8}{'onset ms':>10}")
    print(f"{'model':<14}{NATIVE_HZ:>8.0f}{onset_ms(m,NATIVE_HZ):>10.2f}")
    print(f"{'P85 (20s)':<14}{fs1:>8}{onset_ms(p85,fs1):>10.2f}")
    print(f"{'V7.2 (4.86s)':<14}{fs2:>8}{onset_ms(v72,fs2):>10.2f}")

    print("\nEarly reflection peak times (ms, first 120 ms):")
    print("  model:", early_peaks(m,NATIVE_HZ))
    print("  P85 : ", early_peaks(p85,fs1))
    print("  V7.2: ", early_peaks(v72,fs2))

    print("\nEarly-IR spectral peaks (Hz, rel-amp) over 200-8000 Hz:")
    print("  model:", spectrum_peaks(m,NATIVE_HZ))
    print("  P85 : ", spectrum_peaks(p85,fs1))
    print("  V7.2: ", spectrum_peaks(v72,fs2))

    print("\nRelative energy at the model's spurious 3653 Hz (rms-normalized):")
    print(f"  model @3653: {energy_at(m,NATIVE_HZ,3653):.3f}")
    print(f"  P85   @3653: {energy_at(p85,fs1,3653):.3f}")
    print(f"  V7.2  @3653: {energy_at(v72,fs2,3653):.3f}")
    print(f"\nArtifacts saved to {OUT}/ (model_ir.npy, p85_ir.npy, v72_ir.npy)")


if __name__ == '__main__':
    main()
