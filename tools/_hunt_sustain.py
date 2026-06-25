#!/usr/bin/env python3
"""Why does the CONCERT impulse die in ~60ms? Test injection point + 'idle'-step DAB source.
Float closed loop, impulse injected, track tank energy E[n], report decay over a long window.

Variants:
  inject = 'all3' (impulse at every sub==3 step) | 'fp' (only the offset-fingerprint input step)
  idle   = 'zero' (MI17=0&MI16=0 -> DAB=0, frontier) | 'dmem' (idle reads DMEM[addr], delay tap)
"""
import sys, os, math
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import aru_datapath as A
MASK = 0xFFFF
FS = 34130.0


def find_fp(prog):
    for st in prog:
        if (st['offset'] & 0x8000) and (st['offset'] & 0x3FFF) == 0x3FFF:
            return st['s']
    return None


def run(prog, inject='fp', idle='zero', nsamp=60000, imp=1.0, read_bit=1):
    R = [0.0]*4; ACC = 0.0; RES = 0.0; ACCp = 0.0
    DM = [0.0]*(MASK+1); nz = set(); pos = 0
    fp = find_fp(prog)
    E = []
    for n in range(nsamp):
        pos = (pos+1) & MASK
        for st in prog:
            addr = (pos - st['offset']) & MASK
            is_read = st['MI17'] == 1 and st['MI16'] == read_bit
            is_write = st['MI17'] == 1 and not is_read
            is_sub = st['MI17'] == 0 and st['MI16'] == 1
            ad = 0.0
            if n == 0:
                if inject == 'all3' and is_sub and st['sub'] == 3:
                    ad = imp
                elif inject == 'fp' and st['s'] == fp:
                    ad = imp
            if is_sub and st['sub'] == 3:
                dab = ad
            elif is_read:
                dab = DM[addr]
            elif is_sub and st['sub'] == 1:
                dab = RES
            elif is_write:
                dab = RES
            else:  # idle (MI17=0 & MI16=0) and sub0/sub2
                dab = DM[addr] if (idle == 'dmem' and not is_sub) else 0.0
            x = R[st['RA']]; R[st['WA']] = dab
            if st['ZERO']:
                ACC = 0.0
            ACC += x * 8.0 * st['cs'] / 64.0
            if st['XFER']:
                RES = ACCp / 8.0
            if is_write:
                DM[addr] = RES; nz.add(addr)
            ACCp = ACC
        E.append(ACC*ACC + RES*RES + sum(v*v for v in R) + sum(DM[i]*DM[i] for i in nz))
    return E


def report(E, label):
    nsamp = len(E)
    pk = max(range(nsamp), key=lambda i: E[i]); pkv = E[pk]
    # find where energy drops 60 dB below peak (RT60)
    floor = pkv * 1e-6
    rt = None
    for i in range(pk, nsamp):
        if E[i] < floor:
            rt = (i - pk) / FS; break
    # late-window slope (last 40% after warmup)
    w0 = max(pk + 200, int(nsamp*0.3))
    xs = [i for i in range(w0, nsamp) if E[i] > 0]
    if len(xs) > 100:
        ys = [0.5*math.log(E[i]) for i in xs]
        mx = sum(xs)/len(xs); my = sum(ys)/len(ys)
        sxx = sum((x-mx)**2 for x in xs); sxy = sum((x-mx)*(y-my) for x, y in zip(xs, ys))
        slope = sxy/sxx if sxx else 0.0
        rt60_slope = (math.log(1000.0)/(-slope))/FS if slope < 0 else float('inf')
        lam = math.exp(slope)
    else:
        rt60_slope = float('nan'); lam = float('nan')
    e_end = E[-1]/pkv if pkv else 0
    print(f"  {label:22s} peak@{pk:>6} E_end/E_pk={e_end:.2e}  RT60(60dB)={rt if rt else '>win':>8} "
          f"RT60(slope)={rt60_slope:8.2f}s  lam-1={(lam-1)*1e6:+.1f}ppm")


def main():
    pid = int(os.environ.get('PID', '0x01'), 16)
    NS = int(os.environ.get('NS', '60000'))
    prog = A.load_microcode(pid)
    print(f"sustain test pid={pid:#x}, {len(prog)} steps, {NS} samples ({NS/FS*1000:.0f}ms)")
    for inject in ('fp', 'all3'):
        for idle in ('zero', 'dmem'):
            E = run(prog, inject=inject, idle=idle, nsamp=NS)
            report(E, f"inj={inject} idle={idle}")


if __name__ == '__main__':
    main()
