#!/usr/bin/env python3
"""Check the FUNDAMENTAL assumption: does the booted default (power_up_id=0x01)
param/modulation state correspond to P85's 20 s default? Read the LARC slider bytes
0x3c00-0x3c05 and the modulation params 0x3cd3/0x3cd4/0x3ccd at boot.
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import boot_xl as B

def main():
    cpu, mem, *rest = B.boot(power_up_id=0x01, verbose=False)
    print("Booted default (power_up_id=0x01) state:")
    print("  LARC sliders 0x3c00..0x3c05:",
          [hex(mem[0x3c00+i]) for i in range(6)],
          "=", [mem[0x3c00+i] for i in range(6)])
    print("  (labels: 0=LOW 1=MID 2=XOV 3=HFD 4=DEP 5=PDL; default ~0x20)")
    print(f"  modulation rate  0x3cd3 = {hex(mem[0x3cd3])} ({mem[0x3cd3]})  (CONCERT expects 0x20)")
    print(f"  modulation depth 0x3cd4 = {hex(mem[0x3cd4])} ({mem[0x3cd4]})  (CONCERT expects 4)")
    print(f"  modulation enable0x3ccd = {hex(mem[0x3ccd])} (bit6={ (mem[0x3ccd]>>6)&1 })  (CONCERT expects 0xC0)")
    # program id / record selection bytes
    print(f"  0x3c33 (param type) = {hex(mem[0x3c33])}")
    print(f"  0x3c14 = {hex(mem[0x3c14])}  0x3c16..0x3c1b =", [hex(mem[0x3c16+i]) for i in range(6)])
    # a few WCS coeff bytes for the closers s65/s88 (lane3 at 0x4000 + s*4 + 3)
    for s in (56,57,65,88,107,108):
        base = 0x4000 + s*4
        l3 = mem[base+3]
        mag = l3 & 0x7f; sign = '-' if (l3 & 0x80) else '+'
        print(f"  WCS s{s}: lane3=0x{l3:02x} -> coeff {sign}{mag} (Cs={('-' if sign=='-' else '')}{mag>>1})")

if __name__ == '__main__':
    main()
