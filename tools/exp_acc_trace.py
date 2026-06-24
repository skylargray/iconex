#!/usr/bin/env python3
"""Trace ACC / RES / DMEM-writeback through the two band-split halves.

Converged float state, final sample. For steps in each band-split half, show:
  prod (this step's contribution), ACC after, whether XFER loads RES, whether b3
  writes RES back to DMEM (feedback), and the param each step carries. This shows
  exactly which steps' contributions reach a feedback write-back and which are
  discarded by a ZERO before any XFER -- i.e. why HFD/LOW are inert.
"""
import sys, os, math
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import aru_datapath as A

DMASK = A.DMASK
PICK = lambda st: (st['b5'] << 1) | st['b4']
PARAM = {40: 'HFD', 41: 'HFD', 42: 'PDL', 43: 'LOW', 44: 'MID', 45: 'XOV', 46: 'XOV',
         92: 'HFD', 93: 'HFD', 94: 'PDL', 95: 'LOW', 96: 'MID', 97: 'XOV', 98: 'XOV'}


def run_to_converged(prog, nsamp=30000, K=128, seed=1e4):
    R = [0.0]*4; ACC = 0.0; RES = 0.0
    DM = [0.0]*(DMASK+1); pos = 0; nz = set(); seeded = False
    for n in range(nsamp):
        pos = (pos+1) & DMASK
        last = (n == nsamp-1)
        for st in prog:
            addr = (pos - st['offset']) & DMASK
            dab = RES if st['b3'] else DM[addr]
            if not seeded and st is prog[0]:
                dab += seed; seeded = True
            mag = abs(st['coeff']); Cs = -(mag>>1) if st['coeff']<0 else (mag>>1)
            x = R[PICK(st)]; R[st['WA']] = dab
            if st['ZERO']: ACC = 0.0
            prod = x*8.0*Cs/64.0
            ACC = ACC + prod
            if st['XFER']: RES = ACC/8.0
            if st['b3']: DM[addr] = RES; nz.add(addr)
            if last and (36 <= st['s'] <= 48 or 88 <= st['s'] <= 100):
                tag = PARAM.get(st['s'], '')
                flags = []
                if st['ZERO']: flags.append('ZERO!')
                if st['XFER']: flags.append('XFER->RES')
                if st['b3']: flags.append('b3-write')
                print(f"  s{st['s']:>3} {tag:<4} RA{PICK(st)} c={st['coeff']:>5} "
                      f"prod={prod:+.3e} ACC={ACC:+.3e} RES={RES:+.3e}  {' '.join(flags)}")
        if (n+1) % K == 0:
            ssq = math.sqrt(ACC*ACC + RES*RES + sum(v*v for v in R)
                            + sum(DM[i]*DM[i] for i in nz)) + 1e-300
            f = 1.0/ssq
            R = [v*f for v in R]; ACC *= f; RES *= f
            for i in nz: DM[i] *= f
            if last: pass


def main():
    prog = A.load_microcode(0x01)
    print("FIRST HALF (s36-48) and SECOND HALF (s88-100), converged final sample:")
    print("watch where HFD(40,41/92,93) & LOW(43/95) contributions go vs the ZERO/XFER:\n")
    run_to_converged(prog)


if __name__ == '__main__':
    main()
