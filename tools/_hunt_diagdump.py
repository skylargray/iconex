#!/usr/bin/env python3
"""Dump the FULL decoded structure of the ZERO-DELAY and MAX-DELAY diagnostic
programs under the new device decode, for inv_l2=False, read_bit=1, both inv_l3.
Goal: see the concrete A/D->ARU->D/A signal path so the WR DA/ output step (and
thus the inv_l3 pin) can be reasoned about from real numbers, not by hand."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import _hunt_diagunity as D
import _hunt_rebuild2 as R2
MASK = 0xFFFF


def diag_steps(zero_delay):
    img = D.build_image(zero_delay=zero_delay)
    return [(s, img[s*4], img[s*4+1], img[s*4+2], img[s*4+3])
            for s in range(128) if not (img[s*4+2] == 0xFF and img[s*4+3] == 0xFF)]


def classify(st, read_bit=1):
    is_dram = st['MI17'] == 1
    is_read = is_dram and (st['MI16'] == read_bit)
    is_write = is_dram and not is_read
    is_sub = (st['MI17'] == 0) and (st['MI16'] == 1)
    if is_read: kind = 'DMEM-READ'
    elif is_write: kind = 'DMEM-WRITE'
    elif is_sub:
        kind = {0: 'sub:IDLE', 1: 'sub:RDRREG(fb)', 2: 'sub:RD-XREG',
                3: 'sub:RD-AD(in)'}[st['sub']]
    else:
        kind = 'IDLE(00)'
    return kind


def dump(name, raw, inv_l3, read_bit=1):
    prog = R2.decode(raw, inv_l2=False, inv_l3=inv_l3)
    print(f"\n=== {name}  inv_l2=False inv_l3={inv_l3} read_bit={read_bit} "
          f"({len(prog)} active) ===")
    print(f"{'s':>3} {'offset':>6} {'kind':>14} {'WA':>2} {'RA':>2} "
          f"{'XFER':>4} {'ZERO':>4} {'Cs':>4}  {'raw l2,l3':>10}")
    for st, (s, l0, l1, l2, l3) in zip(prog, raw):
        k = classify(st, read_bit)
        print(f"{st['s']:>3} 0x{st['offset']:04X} {k:>14} {st['WA']:>2} {st['RA']:>2} "
              f"{st['XFER']:>4} {st['ZERO']:>4} {st['Cs']:>4}  "
              f"l2=0x{l2:02X},l3=0x{l3:02X}")


if __name__ == '__main__':
    for zd, nm in [(True, 'ZERO-DELAY'), (False, 'MAX-DELAY(0.5s)')]:
        raw = diag_steps(zd)
        for inv_l3 in (True, False):
            dump(nm, raw, inv_l3)
