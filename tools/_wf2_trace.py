#!/usr/bin/env python3
"""Trace closer blocks: which DMEM addr / register each FF tap and closer reads/writes.

Run J for a few samples, dump the per-step (addr, reg-read source, value flow) for the
first closer block s60-65 and its mirror, so we can see what R2 (third-FF source) holds
and which prior step wrote it, and what cross-block DMEM the closer feedback pulls."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import aru_datapath as A
from exp_J_order import setfields, J_EDITS

DMASK = A.DMASK
PICK = lambda st: (st['b5']<<1)|st['b4']

prog = setfields(A.load_microcode(0x01), J_EDITS)
bys = {p['s']: p for p in prog}

# Build a map: which step most recently wrote register r before step s (static, in-order)
def reg_writer_before(target_s, reg):
    last = None
    for st in prog:
        if st['s'] >= target_s: break
        if st['WA'] == reg: last = st['s']
    return last

WATCH = list(range(60,66)) + list(range(111,117))
print("Static register-write provenance (who last wrote the read-reg before each step):")
for s in WATCH:
    st = bys[s]
    rd = PICK(st)
    w = reg_writer_before(s, rd)
    print(f"  s{s}: reads R{rd} (last written by s{w}), writes R{st['WA']}, off={st['offset']}, b3={st['b3']}, XFER={st['XFER']}, ZERO={st['ZERO']}")

# Now trace actual addresses + values at steady-ish state (sample 5000)
print("\nAddress + value trace at sample n=3000 (converged-ish):")
R = [0.0]*4; ACC=0.0; RES=0.0; DM=[0.0]*(DMASK+1); pos=0; seeded=False
TARGET=3000
for n in range(TARGET+1):
    pos=(pos+1)&DMASK
    for st in prog:
        addr=(pos-st['offset'])&DMASK
        dab = RES if st['b3'] else DM[addr]
        if not seeded and st is prog[0]:
            dab += 1e4; seeded=True
        mag=abs(st['coeff']); Cs=-(mag>>1) if st['coeff']<0 else (mag>>1)
        x=R[PICK(st)]; R[st['WA']]=dab
        if st['ZERO']: ACC=0.0
        ACC = ACC + x*8.0*Cs/64.0
        if st['XFER']: RES=ACC/8.0
        if st['b3']: DM[addr]=RES
        if n==TARGET and st['s'] in WATCH:
            print(f"  s{st['s']:3d} addr={addr:5d} dab={dab:+.3f} x(R{PICK(st)})={x:+.3f} C={Cs/64:+.4f} -> ACC={ACC:+.3f}"
                  + (f"  XFER RES={RES:+.3f}" if st['XFER'] else "")
                  + (f"  WROTE DM[{addr}]={DM[addr]:+.3f}" if st['b3'] else ""))
