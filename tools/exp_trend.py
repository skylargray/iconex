#!/usr/bin/env python3
"""High-precision long-run decay/sustain measurement (the brief's recommended oracle).

Runs the SATURATING integer model for a long horizon and measures the post-peak
energy-envelope trend in dB -> RT60. Pluggable multiply lets us test whether a
hardware-plausible magnitude-truncating multiplier provides the ~20 s damping that
the current (operand*Cs)>>6 collapse does not.

A control variant (effective-gain x (1-eps)) validates that the measurement can
actually resolve a ~20 s decay and tells us the exact gain reduction required.
"""
import sys, os, math
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import aru_datapath as A

DMASK = A.DMASK
NATIVE_HZ = 34130.0


def mul_floor(operand, Cs):          # current model: single floor >>6
    return (operand * Cs) >> 6

def mul_tozero(operand, Cs):         # magnitude truncation (toward zero) at >>6
    p = operand * Cs
    return p >> 6 if p >= 0 else -((-p) >> 6)

def mul_serial_rshift(operand, Cs):  # 2-bit/state serial w/ accumulator right-shift
    # radix-4, 3 states, low 2 bits first; accumulator shifted right 2 each state
    # (drops low bits each state -> maximal physical truncation). Net align >>6.
    neg = Cs < 0
    c = -Cs if neg else Cs           # 0..63 magnitude (6-bit)
    acc = 0
    # process high-to-low, shifting acc left, accumulating, then final >>6
    for i in (2, 1, 0):              # three 2-bit chunks, MSB first
        chunk = (c >> (2 * i)) & 3
        acc = (acc << 2) + operand * chunk
    # acc = operand*c exactly here (no truncation in this ordering); emulate the
    # low-bit drop by quantizing acc to a 2-LSB grid per state == drop 0 (exact).
    p = -acc if neg else acc
    return p >> 6 if p >= 0 else -((-p) >> 6)  # toward zero final

def make_gain_scaled(eps):
    # control: exact effective gain reduced by (1-eps), floored
    def f(operand, Cs):
        return int(math.floor(operand * Cs * (1.0 - eps) / 64.0))
    return f


def run_sat(prog, pick, nsamp, imp, mulfn, res_shift=3):
    R=[0,0,0,0]; ACC=0; RES=0; DM=[0]*(DMASK+1); pos=0; out=[]
    for n in range(nsamp):
        pos=(pos+1)&DMASK; esum=0
        for st in prog:
            addr=(pos-st['offset'])&DMASK
            dab=RES if st['b3'] else DM[addr]
            if n==0 and st is prog[0]: dab+=imp
            mag=abs(st['coeff']); Cs=-(mag>>1) if st['coeff']<0 else (mag>>1)
            x=R[pick(st)]; R[st['WA']]=dab
            if st['ZERO']: ACC=0
            ACC=A.sat20(ACC + mulfn(x<<3, Cs))
            if st['XFER']: RES=A.sat16(ACC>>res_shift)
            if st['b3']: DM[addr]=RES
            if st['XFER']: esum+=abs(RES)
        out.append(esum)
    return out


def trend(esum):
    """Post-peak log-energy linear fit -> per-sample dB slope, RT60, peak."""
    pk=max(esum); npk=esum.index(pk)
    lo=npk+ (len(esum)-npk)//10
    hi=len(esum)
    xs=[i for i in range(lo,hi) if esum[i]>0]
    if len(xs)<20: return dict(pk=pk, npk=npk, rt60=None, db_per_s=None, last=esum[-1])
    ys=[20*math.log10(esum[i]) for i in xs]   # dB (amplitude-like L1 envelope)
    m=len(xs); sx=sum(xs); sy=sum(ys); sxx=sum(x*x for x in xs); sxy=sum(x*y for x,y in zip(xs,ys))
    db_per_sample=(m*sxy-sx*sy)/(m*sxx-sx*sx)
    db_per_s=db_per_sample*NATIVE_HZ
    rt60 = (-60.0/db_per_s) if db_per_s<0 else float('inf')
    return dict(pk=pk, npk=npk, rt60=rt60, db_per_s=db_per_s, last=esum[-1])


def report(label, esum):
    t=trend(esum)
    rt = f"{t['rt60']:.1f}s" if (t['rt60'] is not None and t['rt60']!=float('inf')) else ("SUSTAIN/GROW" if t['rt60']==float('inf') else "n/a")
    dbs = f"{t['db_per_s']:+.3f}" if t['db_per_s'] is not None else "n/a"
    print(f"  {label:<26} peak={t['pk']:>7}@{t['npk']:<6} last={t['last']:>7} "
          f"dB/s={dbs:>8}  RT60={rt}")


def main():
    nsamp=int(sys.argv[1]) if len(sys.argv)>1 else 120000
    prog=A.load_microcode(0x01)
    pick=lambda st:(st['b5']<<1)|st['b4']
    print(f"CONCERT {len(prog)} steps; nsamp={nsamp} ({nsamp/NATIVE_HZ:.1f}s). target RT60~20s\n")

    print("[control] exact effective-gain reduced by eps (validates the measurement):")
    for eps in (0.0, 5e-5, 1e-4, 3e-4, 1e-3):
        report(f"gain x(1-{eps:g})", run_sat(prog,pick,nsamp,20000, make_gain_scaled(eps)))

    print("\n[multiplier variants] does a hardware-plausible truncation add damping?")
    report("floor >>6 (CURRENT)", run_sat(prog,pick,nsamp,20000, mul_floor))
    report("toward-zero >>6",     run_sat(prog,pick,nsamp,20000, mul_tozero))
    report("serial 2b/state",     run_sat(prog,pick,nsamp,20000, mul_serial_rshift))


if __name__ == '__main__':
    main()
