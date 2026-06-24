#!/usr/bin/env python3
"""Trace the ZERO DELAY datapath cycle-by-cycle to understand the passthrough path.

The diag steps all have XFER=0, ZERO=0, so the existing aru_datapath.run never updates
RES (RES only changes on XFER) -> output is forced 0. That means the existing model's
datapath does NOT implement the diagnostic passthrough. We trace every register here to
see what SHOULD happen and where the gain lives.
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import aru_datapath as A
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import importlib.util
spec = importlib.util.spec_from_file_location("_hd", os.path.join(os.path.dirname(__file__), "_hunt_diagunity.py"))
_hd = importlib.util.module_from_spec(spec); spec.loader.exec_module(_hd)

DMASK = A.DMASK
PICK = _hd.PICK


def trace(prog, mode='int', imp=20000, nsamp=4, ra_pick=PICK):
    R = [0, 0, 0, 0] if mode == 'int' else [0.0]*4
    ACC = 0 if mode == 'int' else 0.0
    RES = 0 if mode == 'int' else 0.0
    DM = ([0]*(DMASK+1)) if mode == 'int' else ([0.0]*(DMASK+1))
    pos = 0
    in_step = A.fpc_input_step(prog)
    print(f"  in_step={in_step}")
    for n in range(nsamp):
        pos = (pos + 1) & DMASK
        print(f"\n--- sample n={n} (pos={pos}) ---")
        for st in prog:
            addr = (pos - st['offset']) & DMASK
            if in_step is not None and st['s'] == in_step:
                dab = imp if n == 0 else 0
                src = 'FPC-IN'
            else:
                dab = RES if st['b3'] else DM[addr]
                src = 'RES' if st['b3'] else 'DM'
            mag = abs(st['coeff']); csign = st['coeff'] < 0
            Cs = -(mag >> 1) if csign else (mag >> 1)
            ra = ra_pick(st)
            x = R[ra]
            R[st['WA']] = dab
            if st['ZERO']:
                ACC = 0 if mode == 'int' else 0.0
            if mode == 'int':
                ACC = A.sat20(ACC + (((x << 3) * Cs) >> 6))
                if st['XFER']:
                    RES = A.sat16(ACC >> 3)
            else:
                ACC = ACC + x*8.0*Cs/64.0
                if st['XFER']:
                    RES = ACC/8.0
            if st['b3']:
                DM[addr] = RES
            tag = ''
            if st['WA'] == 3 and (st['offset'] & 0x8000):
                tag = '  <== FPC OUTPUT (drives RES to DAC)'
            print(f"   s{st['s']:3d} WA{st['WA']} ra{ra} b3{st['b3']} XF{st['XFER']} Z{st['ZERO']} "
                  f"src={src:6s} dab={dab!r:>8} x={x!r:>8} Cs={Cs:+3d} -> ACC={ACC!r:>10} RES={RES!r:>8} "
                  f"R={R}{tag}")


if __name__ == '__main__':
    print("===== ZERO DELAY trace (int) =====")
    img = _hd.build_image(zero_delay=True)
    prog = _hd.decode(img)
    trace(prog, mode='int', nsamp=3)
