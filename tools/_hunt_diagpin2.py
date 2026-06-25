#!/usr/bin/env python3
"""Pin exact byte-inversions via the diagnostics, using the FULL device decode.
Inject an impulse at the RD AD/ step (MI17=0,MI16=1,sub=3); capture RES at sub-decoder
output steps. ZERO-DELAY should pass it to the output at ~unity, same sample; MAX-DELAY
should write it to DRAM and read it back ~17065 samples later at ~unity."""
import sys, os, math
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import _hunt_diagunity as D
import _hunt_rebuild2 as R2
MASK = 0xFFFF


def diag_steps(zero_delay):
    img = D.build_image(zero_delay=zero_delay)
    return [(s, img[s*4], img[s*4+1], img[s*4+2], img[s*4+3])
            for s in range(128) if not (img[s*4+2] == 0xFF and img[s*4+3] == 0xFF)]


def run(prog, read_bit, nsamp, imp=20000.0):
    R = [0.0]*4; ACC = 0.0; RES = 0.0; ACCc = 0.0; DM = [0.0]*(MASK+1); pos = 0
    ad_steps = [st['s'] for st in prog if st['MI17'] == 0 and st['MI16'] == 1 and st['sub'] == 3]
    out = []
    for n in range(nsamp):
        pos = (pos+1) & MASK; osum = 0.0
        for st in prog:
            addr = (pos - st['offset']) & MASK
            is_read = st['MI17'] == 1 and st['MI16'] == read_bit
            is_write = st['MI17'] == 1 and not is_read
            is_sub = st['MI17'] == 0 and st['MI16'] == 1
            if is_read: dab = DM[addr]
            elif is_sub and st['sub'] == 1: dab = RES                 # RDRREG/
            elif is_sub and st['sub'] == 3: dab = (imp if n == 0 else 0.0)  # RD AD/ input
            elif is_write: dab = RES
            else: dab = 0.0
            x = R[st['RA']]; R[st['WA']] = dab
            if st['ZERO']: ACC = 0.0
            ACC += x * 8.0 * st['Cs'] / 64.0
            if st['XFER']: RES = ACCc / 8.0
            if is_write: DM[addr] = RES
            ACCc = ACC
            # output candidate: any sub-decoder step that is NOT the input (D/A write side)
            if is_sub and st['sub'] != 3:
                osum += RES
        out.append(osum)
    return out, ad_steps


def main():
    import itertools
    print("DIAG PIN (full device decode). target: ZD unity passthrough; MAX unity echo ~17065\n")
    print(f"{'inv_l2':6s} {'inv_l3':6s} {'rb':3s}  {'ZD g@0':>8s} {'ZD peak':>14s}  {'MAX late-peak':>18s}  ADsteps")
    for inv_l2, inv_l3, rb in itertools.product((True, False), (True, False), (0, 1)):
        zd = R2.decode(diag_steps(True), inv_l2, inv_l3)
        md = R2.decode(diag_steps(False), inv_l2, inv_l3)
        zo, ad = run(zd, rb, 300); mo, _ = run(md, rb, 40000)
        g0 = zo[0]/20000.0
        zi = max(range(len(zo)), key=lambda i: abs(zo[i])); zpk = zo[zi]/20000.0
        late = [(i, v) for i, v in enumerate(mo) if i > 100]
        mi, mv = max(late, key=lambda t: abs(t[1])) if late else (0, 0.0)
        sval = f"{mv/20000.0:+.3f}@{mi}" if abs(mv) < 1e12 else "BLOWUP"
        print(f"{str(inv_l2):6s} {str(inv_l3):6s} {rb:3d}  {g0:+8.3f} {zpk:+.3f}@{zi:<4d}  {sval:>18s}  {ad}")


if __name__ == '__main__':
    main()
