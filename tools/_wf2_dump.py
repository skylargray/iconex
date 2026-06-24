#!/usr/bin/env python3
"""Dump decoded fields for the closer blocks + band-split + MID FF taps under J."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import aru_datapath as A
from exp_J_order import setfields, J_EDITS

prog = A.load_microcode(0x01)
J = setfields(prog, J_EDITS)

MID = {43,44,62,63,64,66,67,68,95,96,113,114,115,117,118,119}
# closer region steps of interest per task
CLOSERS = {36,54,61,65,69,73,88}
FF = set(range(62,69)) | set(range(113,120))
BAND = set(range(37,47)) | set(range(89,99))

PICK = lambda st: (st['b5']<<1)|st['b4']

def show(steps, label):
    print(f"\n=== {label} ===")
    print("  s  off    coeff CSGN  C/64    RA  WA  b3 XFER ZERO  isMID")
    bys = {p['s']: p for p in J}
    for s in sorted(steps):
        if s not in bys:
            print(f"  {s}: (inactive)")
            continue
        st = bys[s]
        mag = abs(st['coeff']); Cs = -(mag>>1) if st['coeff']<0 else (mag>>1)
        print(f"  {s:3d} {st['offset']:5d}  {st['coeff']:+4d}  {'neg' if st['coeff']<0 else 'pos'}  "
              f"{Cs/64:+.4f}  R{PICK(st)}  W{st['WA']}  {st['b3']}  {st['XFER']}   {st['ZERO']}   "
              f"{'MID' if s in MID else ''}")

show(BAND, "BAND-SPLIT s37-46 / s89-98 (under J)")
show(range(60,75), "FIRST-HALF CLOSER/FF region s60-74")
show(range(111,120), "SECOND-HALF FF region s111-119")
