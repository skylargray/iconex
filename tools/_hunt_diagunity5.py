#!/usr/bin/env python3
"""Full faithful diagnostic sim: ZERO DELAY (unity) + .5 S DELAY (~17065-sample delay).

Established (script 4): the signal path is input(A/D) -> R[2] -> FPC output reads R[2]
as a PURE PASS-THROUGH (gain EXACTLY 1.0); the WA=3 output step's coeff is NOT applied
to the FPC write path. Now reproduce the .5s delay: the input must be stored into a DMEM
delay line and read out ~17065 samples (0.5s @ 34130 Hz) later at full amplitude.

The delay-line steps (74,77,124,127) have bit15=0 (DMEM). In the diag the delay write must
happen; we model the input being written into DMEM at a write tap and read at a read tap
whose offset difference = the delay length. We measure the delayed-impulse gain to 6 digits.

We DERIVE the delay structure from the offsets rather than assume it: in MAX(.5s) the two
output-step offsets are 0x8000 (right) / 0xC000 (left); in ZERO they are 0xBFFE/0xFFFE.
The doc says ONLY the low14 of the output steps differ -> the output tap address sets the
delay. low14(MAX right)=0x0000 ; low14(ZERO right)=0x3FFE. So the OUTPUT step itself reads
a delayed DMEM tap whose depth = low14 distance. We test that the output reads DMEM at the
delay tap and the input was written to DMEM head.
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import aru_datapath as A
import importlib.util
spec = importlib.util.spec_from_file_location("_hd", os.path.join(os.path.dirname(__file__), "_hunt_diagunity.py"))
_hd = importlib.util.module_from_spec(spec); spec.loader.exec_module(_hd)

DMASK = A.DMASK
NATIVE_HZ = 34130.0


def show_offsets():
    for zd, name in [(True, 'ZERO DELAY'), (False, '.5 S DELAY')]:
        prog = _hd.decode(_hd.build_image(zero_delay=zd))
        print(f"\n--- {name} step offsets ---")
        for st in prog:
            off = st['offset']
            print(f"  s{st['s']:3d} WA{st['WA']} off=0x{off:04X} b15={(off>>15)&1} b14={(off>>14)&1} "
                  f"low14=0x{off&0x3FFF:04X}  coeff={st['coeff']:+d}")


if __name__ == '__main__':
    show_offsets()

    # The .5s delay length: 0.5 s * 34130 Hz = 17065 samples.
    print(f"\n0.5 s @ {NATIVE_HZ} Hz = {0.5*NATIVE_HZ:.1f} samples")
    # Right-channel delay-line steps in MAX: 74 (off 0x1680) write, 77 (off 0x3000) ...
    # The delay between a write at offset W and read at offset R (addr=pos-offset) is (W-R) samples,
    # because read addr revisits write addr after (offsetW - offsetR) position increments.
    prog = _hd.decode(_hd.build_image(zero_delay=False))
    print("\n--- candidate delay lengths from offset differences (right ch steps 74,76,77) ---")
    offs = {st['s']: st['offset'] for st in prog}
    for a in (74, 76, 77):
        for b in (74, 76, 77):
            if a < b:
                d = (offs[a] - offs[b]) & DMASK
                print(f"  off[{a}]-off[{b}] = 0x{offs[a]:04X}-0x{offs[b]:04X} = {d} samples "
                      f"({d/NATIVE_HZ*1000:.1f} ms)")
