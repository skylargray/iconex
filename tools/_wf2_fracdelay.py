#!/usr/bin/env python3
"""Does a fractional-delay (interpolated) read on the modulated taps supply the missing loss?

The modulated taps s56/57 (and s107/108) read DMEM with a delay the firmware modulates
(engine 0xAE72). Our model uses integer offsets. A real fractional-delay interpolator
(linear: dab = (1-f)*DM[a] + f*DM[a-1]) is a one-pole-ish lowpass with HF magnitude < 1
=> a frequency-dependent recirculation LOSS, common to all programs (uniform deficit).

Test under J: replace the integer read on the modulated taps with a linearly-interpolated
read at a fixed fractional offset f, measure conv_lambda. If even a static fractional read
drops lambda toward unity, the omitted interpolation is a real structural loss; if it does
nothing (like static integer detune), it is not the lever and the residual is elsewhere.
"""
import sys, os, math
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import aru_datapath as A
from exp_J_order import setfields, J_EDITS

DMASK = A.DMASK
PICK = lambda st: (st['b5']<<1)|st['b4']
MOD = {56, 57, 107, 108}
MID = {43,44,62,63,64,66,67,68,95,96,113,114,115,117,118,119}
HFD={40,41,92,93}; LOW={43,95}; XOV={45,46,97,98}

def lam_frac(prog, frac=0.0, frac_steps=MOD, nsamp=30000, K=128, seed=1e4, tail=40):
    R=[0.0]*4; ACC=0.0; RES=0.0; DM=[0.0]*(DMASK+1); pos=0; nz=set(); seeded=False
    traj=[]
    for n in range(nsamp):
        pos=(pos+1)&DMASK
        for st in prog:
            addr=(pos-st['offset'])&DMASK
            if st['b3']:
                dab=RES
            elif st['s'] in frac_steps and frac>0:
                a2=(addr-1)&DMASK
                dab=(1-frac)*DM[addr]+frac*DM[a2]
            else:
                dab=DM[addr]
            if not seeded and st is prog[0]:
                dab+=seed; seeded=True
            mag=abs(st['coeff']); Cs=-(mag>>1) if st['coeff']<0 else (mag>>1)
            x=R[PICK(st)]; R[st['WA']]=dab
            if st['ZERO']: ACC=0.0
            ACC=ACC+x*8.0*Cs/64.0
            if st['XFER']: RES=ACC/8.0
            if st['b3']: DM[addr]=RES; nz.add(addr)
        if (n+1)%K==0:
            ssq=math.sqrt(ACC*ACC+RES*RES+sum(v*v for v in R)+sum(DM[i]*DM[i] for i in nz))+1e-300
            traj.append(math.exp(math.log(ssq)/K))
            f=1.0/ssq
            R=[v*f for v in R]; ACC*=f; RES*=f
            for i in nz: DM[i]*=f
    t=sorted(traj[-tail:]); return t[len(t)//2]

def coupling(prog, frac):
    base=lam_frac(prog,frac)
    out={'base':base}
    for nm,steps in [('HFD',HFD),('LOW',LOW),('MID',MID),('XOV',XOV)]:
        p2=setfields(prog,{s:{'coeff':0} for s in steps})
        out[nm]=(lam_frac(p2,frac)-base)*1e6
    return out

def main():
    J=setfields(A.load_microcode(0x01),J_EDITS)
    print("Fractional-delay read on modulated taps s56/57/107/108, under J:")
    for frac in (0.0,0.1,0.25,0.5,0.75,0.9):
        c=coupling(J,frac)
        b=c['base']
        print(f"  frac={frac:.2f}  lambda={b:.7f} ({(b-1)*1e6:+.1f} ppm) "
              f"{'DECAY' if b<1 else 'GROW'}  auth HFD {c['HFD']:+.0f} LOW {c['LOW']:+.0f} MID {c['MID']:+.0f} XOV {c['XOV']:+.0f}")

    # also apply fractional read on ALL non-b3 DMEM reads (a uniform interpolation loss)
    print("\nFractional read on ALL DMEM reads (uniform interpolation), under J:")
    ALL = set(p['s'] for p in J)
    for frac in (0.0,0.05,0.1,0.25,0.5):
        b=lam_frac(J,frac,frac_steps=ALL)
        print(f"  frac={frac:.2f}  lambda={b:.7f} ({(b-1)*1e6:+.1f} ppm) {'DECAY' if b<1 else 'GROW'}")

if __name__=='__main__':
    main()
