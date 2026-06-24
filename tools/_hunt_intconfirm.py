#!/usr/bin/env python3
"""Independent audio-path confirmation: run the SATURATING INTEGER datapath (the real
signal path, real impulse) under the universal-lossless candidate (config A: RA=(b3,b4)
with b3 dual-use DMEM-select, timing acc_latch+reg_wbr) and measure the RMS-envelope
dB/s. Base model GROWS (CONCERT +1.81 dB/s); a correct lossless model should be ~0
(flat) or slightly negative. This is method-diverse (integer + impulse, not float
power-iteration) confirmation that the candidate is not a power-iteration artifact."""
import sys, os, math
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import aru_datapath as A
import _hunt_progcache as PC
DMASK = A.DMASK
NATIVE_HZ = 34130.0


def env_dbs(prog, mode='base', nsamp=120000, imp=200, BLK=512):
    """Integer envelope dB/s. mode='base' = current model; mode='cand' = config A
    (RA=(b3,b4), b3 dual-use DMEM, acc_latch+reg_wbr)."""
    R = [0,0,0,0]; ACC = 0; RES = 0; ACCc = 0; DM = [0]*(DMASK+1); pos = 0
    block = []; env = []
    cand = (mode == 'cand')
    for n in range(nsamp):
        pos = (pos+1) & DMASK; esum = 0
        for st in prog:
            addr = (pos - st['offset']) & DMASK
            b3 = st['b3']                                   # DMEM-select (same bit either way)
            dab = RES if b3 else DM[addr]
            if n == 0 and st is prog[0]: dab += imp
            mag = abs(st['coeff']); Cs = -(mag>>1) if st['coeff']<0 else (mag>>1)
            pk = ((st['b3']<<1)|st['b4']) if cand else ((st['b5']<<1)|st['b4'])
            if cand:
                R[st['WA']] = dab; x = R[pk]               # write-before-read
            else:
                x = R[pk]; R[st['WA']] = dab               # read-before-write
            if st['ZERO']: ACC = 0
            xfer_acc = ACCc if cand else None               # acc_latch: pre-product ACC
            ACC = A.sat20(ACC + (((x<<3)*Cs) >> 6))
            if st['XFER']:
                RES = A.sat16((xfer_acc if cand else ACC) >> 3)
            if b3: DM[addr] = RES
            if cand: ACCc = ACC
            if st['XFER']: esum += abs(RES)
        block.append(esum)
        if len(block) == BLK:
            env.append(math.sqrt(sum(v*v for v in block)/BLK)); block = []
    skip = int(len(env)*0.3)
    xs = [i for i in range(skip, len(env)) if env[i] > 0]
    if len(xs) < 8: return None, max(env) if env else 0
    ys = [20*math.log10(env[i]) for i in xs]
    m=len(xs); sx=sum(xs); sy=sum(ys); sxx=sum(x*x for x in xs); sxy=sum(x*y for x,y in zip(xs,ys))
    return (m*sxy - sx*sy)/(m*sxx - sx*sx)*NATIVE_HZ/BLK, max(env)


def main():
    cache = PC.load()
    print("INTEGER audio-path envelope dB/s (real impulse, saturating). base GROWS; cand should be ~<=0\n")
    print(f"{'pid':6s} {'base dB/s':>12s} {'cand dB/s':>12s}   verdict")
    for p in [0x01, 0x04, 0x05, 0x0c]:
        b, pkb = env_dbs(cache[p]['prog'], 'base')
        c, pkc = env_dbs(cache[p]['prog'], 'cand')
        bs = f"{b:+.4f}" if b is not None else "flat/uncpl"
        cs = f"{c:+.4f}" if c is not None else "flat/uncpl"
        verdict = ("base GROW -> cand "
                   + ("flat/decay GOOD" if (c is None or c < 0.01) else "still GROW"))
        print(f"{p:#06x} {bs:>12s} {cs:>12s}   {verdict}")


if __name__ == '__main__':
    main()
