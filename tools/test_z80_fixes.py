#!/usr/bin/env python3
"""Exhaustive verification of the z80emu.py fixes: CCF H-flag, DAA H-flag,
DD/FD IXH/IXL half-register substitution. Independent references (not the impl).

Run: python tools/test_z80_fixes.py
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from z80emu import Z80, FS, FZ, FH, FPV, FN, FC, PARITY

fails = 0
def check(name, cond, detail=""):
    global fails
    if not cond:
        fails += 1
        print(f"  FAIL {name}: {detail}")


def run_op(setup, code):
    """Build a tiny machine, apply setup(cpu), execute the bytes `code` once-each."""
    mem = bytearray(0x10000)
    for i, b in enumerate(code):
        mem[i] = b
    cpu = Z80(mem)
    setup(cpu)
    cpu.PC = 0
    for _ in code_steps(code):
        cpu.step()
    return cpu

def code_steps(code):
    # number of instructions in `code` (we feed exactly one logical instruction here)
    return [0]


# ---------------------------------------------------------------- CCF
def test_ccf():
    # CCF (0x3F): H = old C, C = ~C, N = 0, S/Z/P preserved.
    for f in range(256):
        cpu = run_op(lambda c, f=f: setattr(c, 'F', f), [0x3F])
        oldc = f & FC
        exp = (f & (FS | FZ | FPV)) | (FH if oldc else 0) | (0 if oldc else FC)
        check("CCF", cpu.F == exp, f"F_in={f:02X} got {cpu.F:02X} exp {exp:02X}")
    print("CCF: exhaustive over 256 F values done")


# ---------------------------------------------------------------- DAA
def daa_ref(A, fN, fH, fC):
    """Canonical ZEXALL-compatible DAA reference (nibble test for both directions;
    H = bit-4 carry/borrow). Returns (A_out, F_out)."""
    corr = 0; c = 0
    if fH or (A & 0xF) > 9: corr |= 0x06
    if fC or A > 0x99: corr |= 0x60; c = FC
    if fN:
        h = FH if (fH and (A & 0xF) < 6) else 0
        A2 = (A - corr) & 0xFF
    else:
        h = FH if (A & 0xF) > 9 else 0
        A2 = (A + corr) & 0xFF
    F = (A2 & FS) | (FZ if A2 == 0 else 0) | PARITY[A2] | (FN if fN else 0) | c | h
    return A2, F


def test_daa_flags():
    # exhaustive over A x (N,H,C) vs the canonical reference
    for A in range(256):
        for bits in range(8):
            fN = FN if bits & 1 else 0
            fH = FH if bits & 2 else 0
            fC = FC if bits & 4 else 0
            fin = fN | fH | fC
            cpu = run_op(lambda c, A=A, fin=fin: (setattr(c, 'A', A), setattr(c, 'F', fin)), [0x27])
            eA, eF = daa_ref(A, fN, fH, fC)
            check("DAA", cpu.A == eA and cpu.F == eF,
                  f"A={A:02X} N={bool(fN)} H={bool(fH)} C={bool(fC)}: "
                  f"got A={cpu.A:02X} F={cpu.F:02X} exp A={eA:02X} F={eF:02X}")
    print("DAA: exhaustive over 256 A x 8 (N,H,C) vs reference done")


def test_daa_bcd_decimal():
    # INDEPENDENT ground truth: valid BCD add/sub then DAA == decimal-correct BCD.
    def bcd(x): return ((x // 10) << 4) | (x % 10)
    for a in range(100):
        for b in range(100):
            # ADD: bcd(a)+bcd(b) ; ADD then DAA must give bcd((a+b)%100), carry=(a+b>=100)
            cpu = run_op(lambda c, A=bcd(a), B=bcd(b): (setattr(c, 'A', A), setattr(c, 'B', B)),
                         [0x80, 0x27])              # ADD A,B ; DAA
            for _ in range(2): pass
            # run_op only steps once; do it manually:
            mem = bytearray(0x10000); mem[0] = 0x80; mem[1] = 0x27
            cpu = Z80(mem); cpu.A = bcd(a); cpu.B = bcd(b); cpu.PC = 0
            cpu.step(); cpu.step()
            exp = bcd((a + b) % 100); expc = 1 if a + b >= 100 else 0
            check("DAA+ADD", cpu.A == exp and (cpu.F & FC) == (FC if expc else 0),
                  f"{a}+{b}: got {cpu.A:02X} C={(cpu.F&FC)!=0} exp {exp:02X} C={bool(expc)}")
            # SUB: a-b (only when a>=b for a clean BCD borrow model; test all, track borrow)
            mem = bytearray(0x10000); mem[0] = 0x90; mem[1] = 0x27
            cpu = Z80(mem); cpu.A = bcd(a); cpu.B = bcd(b); cpu.PC = 0
            cpu.step(); cpu.step()
            exp = bcd((a - b) % 100); expc = 1 if a < b else 0
            check("DAA+SUB", cpu.A == exp and (cpu.F & FC) == (FC if expc else 0),
                  f"{a}-{b}: got {cpu.A:02X} C={(cpu.F&FC)!=0} exp {exp:02X} C={bool(expc)}")
    print("DAA: all 100x100 BCD ADD & SUB vs decimal ground truth done")


# ---------------------------------------------------------------- DD/FD IXH/IXL
def test_idx_half():
    def mk(code, setup):
        mem = bytearray(0x10000)
        for i, b in enumerate(code): mem[i] = b
        cpu = Z80(mem); setup(cpu); cpu.PC = 0; cpu.step(); return cpu

    # DD 26 nn = LD IXH,n
    c = mk([0xDD, 0x26, 0xAB], lambda c: setattr(c, 'IX', 0x1234))
    check("LD IXH,n", c.IX == 0xAB34, f"IX={c.IX:04X}")
    # DD 2E nn = LD IXL,n
    c = mk([0xDD, 0x2E, 0xCD], lambda c: setattr(c, 'IX', 0x1234))
    check("LD IXL,n", c.IX == 0x12CD, f"IX={c.IX:04X}")
    # DD 7C = LD A,IXH
    c = mk([0xDD, 0x7C], lambda c: setattr(c, 'IX', 0x9A55))
    check("LD A,IXH", c.A == 0x9A, f"A={c.A:02X}")
    # DD 7D = LD A,IXL
    c = mk([0xDD, 0x7D], lambda c: setattr(c, 'IX', 0x9A55))
    check("LD A,IXL", c.A == 0x55, f"A={c.A:02X}")
    # DD 67 = LD IXH,A
    c = mk([0xDD, 0x67], lambda c: (setattr(c, 'IX', 0x1234), setattr(c, 'A', 0xEE)))
    check("LD IXH,A", c.IX == 0xEE34, f"IX={c.IX:04X}")
    # DD 84 = ADD A,IXH
    c = mk([0xDD, 0x84], lambda c: (setattr(c, 'IX', 0x1000), setattr(c, 'A', 0x05)))
    check("ADD A,IXH", c.A == 0x15, f"A={c.A:02X}")
    # DD 24 = INC IXH ; DD 2C = INC IXL
    c = mk([0xDD, 0x24], lambda c: setattr(c, 'IX', 0x12FF))
    check("INC IXH", c.IX == 0x13FF, f"IX={c.IX:04X}")
    c = mk([0xDD, 0x2C], lambda c: setattr(c, 'IX', 0x12FF))
    check("INC IXL", c.IX == 0x1200, f"IX={c.IX:04X}")
    # DD 25 = DEC IXH
    c = mk([0xDD, 0x25], lambda c: setattr(c, 'IX', 0x1234))
    check("DEC IXH", c.IX == 0x1134, f"IX={c.IX:04X}")
    # FD variants hit IY: FD 26 = LD IYH,n
    c = mk([0xFD, 0x26, 0x77], lambda c: setattr(c, 'IY', 0x1234))
    check("LD IYH,n", c.IY == 0x7734, f"IY={c.IY:04X}")
    # prefix no-effect opcode: DD 3C = INC A (prefix ignored)
    c = mk([0xDD, 0x3C], lambda c: setattr(c, 'A', 0x41))
    check("DD INC A (no-op prefix)", c.A == 0x42, f"A={c.A:02X}")
    # explicit (IX+d) still works: DD 7E d = LD A,(IX+d)
    def s(c):
        c.IX = 0x100; c.m[0x105] = 0x99
    c = mk([0xDD, 0x7E, 0x05], s)
    check("LD A,(IX+d)", c.A == 0x99, f"A={c.A:02X}")
    print("DD/FD IXH/IXL: targeted opcodes done")


# ---------------------------------------------------------------- boot regression
def test_boot():
    import boot_xl as B
    cpu, mem, *_ = B.boot(power_up_id=0x01, verbose=False)
    wcs = bytes(mem[0x4000:0x4200])
    nonff = sum(1 for i in range(0, 512, 4) if not (wcs[i+2] == 0xFF and wcs[i+3] == 0xFF))
    check("boot WCS built", nonff >= 100, f"only {nonff} active steps")
    print(f"boot regression: WCS built, {nonff} active steps")


if __name__ == '__main__':
    test_ccf()
    test_daa_flags()
    test_daa_bcd_decimal()
    test_idx_half()
    test_boot()
    print(f"\n{'ALL Z80 FIX TESTS PASS' if fails == 0 else f'{fails} FAILURES'}")
    sys.exit(1 if fails else 0)
