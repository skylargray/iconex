#!/usr/bin/env python3
"""Long integer impulse response: does CONCERT build a reverb tail over multiple delay
round-trips? Comb delays are ~0.8-1.5s, so a short window looks 'dead'. Run many seconds,
track DMEM occupancy + output energy over time."""
import sys, os, math
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import aru_datapath as A
MASK = 0xFFFF
FS = 34130.0


def run(prog, imp=20000, nsamp=300000, read_bit=1, idle_dmem=False):
    R = [0, 0, 0, 0]; ACC = 0; RES = 0; ACCp = 0
    DM = [0]*(MASK+1); nz = set(); pos = 0
    out = []          # per-sample |RES| at WA=3 (output candidate) steps
    occ = []          # (sample, nonzero DMEM cell count) snapshots
    for n in range(nsamp):
        pos = (pos+1) & MASK; ow = 0
        for st in prog:
            addr = (pos - st['offset']) & MASK
            ad = imp if n == 0 else 0
            dab, isw = A._dab_source(st, DM, addr, RES, ad, read_bit)
            if idle_dmem and dab == 0 and st['MI17'] == 0 and st['MI16'] == 0:
                dab = DM[addr]
            x = R[st['RA']]; R[st['WA']] = dab
            if st['ZERO']: ACC = 0
            prod = (x << 3) * st['cs'] >> 6
            ACC = A.sat20(ACC + prod)
            if st['XFER']: RES = A.sat16(ACCp >> 3)
            if isw: DM[addr] = RES; nz.add(addr)
            if st['WA'] == 3: ow += abs(RES)
            ACCp = ACC
        out.append(ow)
        if (n+1) % 10000 == 0:
            occ.append((n+1, sum(1 for i in nz if DM[i] != 0)))
    return out, occ


def main():
    pid = int(os.environ.get('PID', '0x01'), 16)
    NS = int(os.environ.get('NS', '300000'))
    idle = os.environ.get('IDLE_DMEM', '') == '1'
    prog = A.load_microcode(pid)
    print(f"long IR pid={pid:#x} {len(prog)} steps, {NS} samples ({NS/FS:.1f}s), idle_dmem={idle}")
    out, occ = run(prog, nsamp=NS, idle_dmem=idle)
    print("occupancy over time (sample: nonzero DMEM cells):")
    for s, c in occ:
        print(f"  n={s:>7} ({s/FS:5.2f}s): {c} nonzero DMEM cells   out_energy={out[s-1]}")
    # output envelope in windows
    print("output |RES@WA3| windowed RMS (dB rel peak):")
    win = NS // 20
    peak = max(out) or 1
    for w in range(20):
        seg = out[w*win:(w+1)*win]
        rms = math.sqrt(sum(v*v for v in seg)/len(seg)) if seg else 0
        db = 20*math.log10(rms/peak) if rms > 0 else -999
        print(f"  {w*win/FS:5.2f}-{(w+1)*win/FS:5.2f}s: RMS={rms:10.1f}  {db:7.1f} dB")


if __name__ == '__main__':
    main()
