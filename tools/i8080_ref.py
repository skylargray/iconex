#!/usr/bin/env python3
"""Clean-room Intel 8080 CPU core — an INDEPENDENT second implementation for plan 019 Phase 2.

Purpose: cross-validate the reverb-critical lane-3 (cmag/XFER/ZERO) WCS bytes on a core that does
NOT share the kosarev `z80.I8080Machine` implementation. The whole 224XL reconstruction trusts lane 3
from kosarev ONLY; the old tools/z80emu.py disagreed because of an 8080 PARITY-vs-overflow bug (it set
P/V to overflow like a Z80; the 8080 sets PARITY there, and the coeff build uses parity branches).

This core is written from the documented 8080 instruction/flag definitions (Intel 8080 Programmer's
Manual), NOT by reading kosarev. Its ALU/flag logic is then proven correct by an INDEPENDENT oracle —
8080 spec flag FORMULAS computed directly (parity = even popcount; add/sub half-carry via the
(res ^ a ^ b) bit-4/8 identity) — see tools/i8080_ref_validate.py. That spec oracle, not the kosarev
core, is what certifies this core, so lane-3 agreement between the two cores is genuine independence.

Flag byte (PSW) layout:  S Z 0 AC 0 P 1 C   (bit7..bit0).
"""

# Even-parity table: PF = 1 when the number of set bits in the low byte is EVEN (8080 convention).
_PARITY = [0] * 256
for _i in range(256):
    _PARITY[_i] = 1 - (bin(_i).count("1") & 1)   # 1 if even number of 1-bits


class I8080:
    __slots__ = ("a", "b", "c", "d", "e", "h", "l", "sp", "pc",
                 "sf", "zf", "hf", "pf", "cf", "iff", "halted",
                 "memory", "in_cb", "out_cb", "instr_count", "int_pending")

    def __init__(self):
        self.a = self.b = self.c = self.d = self.e = self.h = self.l = 0
        self.sp = 0
        self.pc = 0
        self.sf = self.zf = self.hf = self.pf = self.cf = 0
        self.iff = 0
        self.halted = False
        self.memory = bytearray(0x10000)
        self.in_cb = None          # in_cb(port) -> byte
        self.out_cb = None         # out_cb(port, val)
        self.instr_count = 0
        self.int_pending = None    # vector address if an interrupt is queued

    # ---- 16-bit register-pair accessors ----
    @property
    def bc(self): return (self.b << 8) | self.c
    @property
    def de(self): return (self.d << 8) | self.e
    @property
    def hl(self): return (self.h << 8) | self.l

    def set_bc(self, v): self.b = (v >> 8) & 0xFF; self.c = v & 0xFF
    def set_de(self, v): self.d = (v >> 8) & 0xFF; self.e = v & 0xFF
    def set_hl(self, v): self.h = (v >> 8) & 0xFF; self.l = v & 0xFF

    # ---- flag byte (PSW low byte) ----
    def get_psw(self):
        return ((self.sf << 7) | (self.zf << 6) | (self.hf << 4) |
                (self.pf << 2) | (1 << 1) | self.cf)

    def set_psw(self, f):
        self.sf = (f >> 7) & 1
        self.zf = (f >> 6) & 1
        self.hf = (f >> 4) & 1
        self.pf = (f >> 2) & 1
        self.cf = f & 1

    # ---- memory ----
    def rb(self, a): return self.memory[a & 0xFFFF]
    def wb(self, a, v): self.memory[a & 0xFFFF] = v & 0xFF
    def rw(self, a):
        a &= 0xFFFF
        return self.memory[a] | (self.memory[(a + 1) & 0xFFFF] << 8)
    def ww(self, a, v):
        a &= 0xFFFF
        self.memory[a] = v & 0xFF
        self.memory[(a + 1) & 0xFFFF] = (v >> 8) & 0xFF

    def _next_b(self):
        v = self.memory[self.pc]
        self.pc = (self.pc + 1) & 0xFFFF
        return v
    def _next_w(self):
        lo = self.memory[self.pc]
        hi = self.memory[(self.pc + 1) & 0xFFFF]
        self.pc = (self.pc + 2) & 0xFFFF
        return lo | (hi << 8)

    # ---- 8-register decode (0=B 1=C 2=D 3=E 4=H 5=L 6=M[HL] 7=A) ----
    def get_reg(self, i):
        if i == 0: return self.b
        if i == 1: return self.c
        if i == 2: return self.d
        if i == 3: return self.e
        if i == 4: return self.h
        if i == 5: return self.l
        if i == 6: return self.memory[self.hl]
        return self.a

    def set_reg(self, i, v):
        v &= 0xFF
        if i == 0: self.b = v
        elif i == 1: self.c = v
        elif i == 2: self.d = v
        elif i == 3: self.e = v
        elif i == 4: self.h = v
        elif i == 5: self.l = v
        elif i == 6: self.memory[self.hl] = v
        else: self.a = v

    # ---- flag helpers ----
    def _zsp(self, v):
        v &= 0xFF
        self.zf = 1 if v == 0 else 0
        self.sf = (v >> 7) & 1
        self.pf = _PARITY[v]

    # ---- ALU (A <- A op val) ----
    def _add(self, val, carry_in):
        a = self.a
        res = a + val + carry_in
        self.hf = ((res ^ a ^ val) >> 4) & 1
        self.cf = 1 if res > 0xFF else 0
        self.a = res & 0xFF
        self._zsp(self.a)

    def _sub(self, val, carry_in):
        # 8080 subtract = add of one's complement with inverted carry-in, then invert carry-out.
        a = self.a
        comp = (~val) & 0xFF
        cin = 1 - carry_in
        res = a + comp + cin
        self.hf = ((res ^ a ^ comp) >> 4) & 1
        self.cf = 0 if res > 0xFF else 1      # invert carry-out -> borrow
        self.a = res & 0xFF
        self._zsp(self.a)

    def _cmp(self, val):
        saved = self.a
        self._sub(val, 0)
        self.a = saved                         # CMP discards the result, keeps flags

    def _ana(self, val):
        self.hf = ((self.a | val) >> 3) & 1    # 8080 ANA: AC = OR of bit3s
        self.a &= val
        self.cf = 0
        self._zsp(self.a)

    def _xra(self, val):
        self.a ^= val
        self.cf = 0
        self.hf = 0
        self._zsp(self.a)

    def _ora(self, val):
        self.a |= val
        self.cf = 0
        self.hf = 0
        self._zsp(self.a)

    def _inr(self, val):
        res = (val + 1) & 0xFF
        self.hf = 1 if (res & 0xF) == 0 else 0
        self._zsp(res)
        return res

    def _dcr(self, val):
        res = (val - 1) & 0xFF
        self.hf = 0 if (res & 0xF) == 0xF else 1
        self._zsp(res)
        return res

    def _dad(self, val16):
        res = self.hl + val16
        self.cf = 1 if res > 0xFFFF else 0
        self.set_hl(res & 0xFFFF)

    def _daa(self):
        cy = self.cf
        correction = 0
        lsb = self.a & 0x0F
        msb = self.a >> 4
        if self.hf or lsb > 9:
            correction += 0x06
        if self.cf or msb > 9 or (msb >= 9 and lsb > 9):
            correction += 0x60
            cy = 1
        self._add(correction, 0)               # sets hf/zsp from the add
        self.cf = cy

    # ---- stack ----
    def _push(self, v):
        self.sp = (self.sp - 2) & 0xFFFF
        self.ww(self.sp, v)
    def _pop(self):
        v = self.rw(self.sp)
        self.sp = (self.sp + 2) & 0xFFFF
        return v

    # ---- interrupt: queue a vector (e.g. 0x38 for RST7); taken before next fetch if iff set ----
    def request_interrupt(self, vector):
        self.int_pending = vector

    def _take_interrupt(self):
        self.iff = 0
        self.halted = False
        self._push(self.pc)
        self.pc = self.int_pending & 0xFFFF
        self.int_pending = None

    # =====================================================================
    def step(self):
        if self.int_pending is not None and self.iff:
            self._take_interrupt()
        if self.halted:
            self.instr_count += 1
            return
        self.instr_count += 1
        op = self.memory[self.pc]
        self.pc = (self.pc + 1) & 0xFFFF

        hi = op >> 6           # 2-bit top
        # ---- 0x40..0x7F: MOV r,r  (0x76 = HLT) ----
        if hi == 1:
            if op == 0x76:
                self.halted = True
                return
            self.set_reg((op >> 3) & 7, self.get_reg(op & 7))
            return
        # ---- 0x80..0xBF: ALU A,r ----
        if hi == 2:
            val = self.get_reg(op & 7)
            kind = (op >> 3) & 7
            if kind == 0: self._add(val, 0)
            elif kind == 1: self._add(val, self.cf)
            elif kind == 2: self._sub(val, 0)
            elif kind == 3: self._sub(val, self.cf)
            elif kind == 4: self._ana(val)
            elif kind == 5: self._xra(val)
            elif kind == 6: self._ora(val)
            else: self._cmp(val)
            return

        # ---- everything else ----
        m = self.memory
        if op == 0x00 or op in (0x08, 0x10, 0x18, 0x20, 0x28, 0x30, 0x38):  # NOP + undocumented NOPs
            return
        # LXI rp,d16
        if op == 0x01: self.set_bc(self._next_w()); return
        if op == 0x11: self.set_de(self._next_w()); return
        if op == 0x21: self.set_hl(self._next_w()); return
        if op == 0x31: self.sp = self._next_w(); return
        # STAX/LDAX
        if op == 0x02: m[self.bc] = self.a; return
        if op == 0x12: m[self.de] = self.a; return
        if op == 0x0A: self.a = m[self.bc]; return
        if op == 0x1A: self.a = m[self.de]; return
        # SHLD/LHLD/STA/LDA
        if op == 0x22: self.ww(self._next_w(), self.hl); return
        if op == 0x2A: self.set_hl(self.rw(self._next_w())); return
        if op == 0x32: m[self._next_w()] = self.a; return
        if op == 0x3A: self.a = m[self._next_w()]; return
        # INX/DCX
        if op == 0x03: self.set_bc((self.bc + 1) & 0xFFFF); return
        if op == 0x13: self.set_de((self.de + 1) & 0xFFFF); return
        if op == 0x23: self.set_hl((self.hl + 1) & 0xFFFF); return
        if op == 0x33: self.sp = (self.sp + 1) & 0xFFFF; return
        if op == 0x0B: self.set_bc((self.bc - 1) & 0xFFFF); return
        if op == 0x1B: self.set_de((self.de - 1) & 0xFFFF); return
        if op == 0x2B: self.set_hl((self.hl - 1) & 0xFFFF); return
        if op == 0x3B: self.sp = (self.sp - 1) & 0xFFFF; return
        # DAD rp
        if op == 0x09: self._dad(self.bc); return
        if op == 0x19: self._dad(self.de); return
        if op == 0x29: self._dad(self.hl); return
        if op == 0x39: self._dad(self.sp); return
        # INR/DCR r
        if op in (0x04, 0x0C, 0x14, 0x1C, 0x24, 0x2C, 0x34, 0x3C):
            r = (op >> 3) & 7
            self.set_reg(r, self._inr(self.get_reg(r))); return
        if op in (0x05, 0x0D, 0x15, 0x1D, 0x25, 0x2D, 0x35, 0x3D):
            r = (op >> 3) & 7
            self.set_reg(r, self._dcr(self.get_reg(r))); return
        # MVI r,d8
        if op in (0x06, 0x0E, 0x16, 0x1E, 0x26, 0x2E, 0x36, 0x3E):
            self.set_reg((op >> 3) & 7, self._next_b()); return
        # rotates
        if op == 0x07:  # RLC
            b7 = (self.a >> 7) & 1; self.a = ((self.a << 1) | b7) & 0xFF; self.cf = b7; return
        if op == 0x0F:  # RRC
            b0 = self.a & 1; self.a = ((self.a >> 1) | (b0 << 7)) & 0xFF; self.cf = b0; return
        if op == 0x17:  # RAL
            b7 = (self.a >> 7) & 1; self.a = ((self.a << 1) | self.cf) & 0xFF; self.cf = b7; return
        if op == 0x1F:  # RAR
            b0 = self.a & 1; self.a = ((self.a >> 1) | (self.cf << 7)) & 0xFF; self.cf = b0; return
        # CMA/STC/CMC/DAA
        if op == 0x2F: self.a ^= 0xFF; return
        if op == 0x37: self.cf = 1; return
        if op == 0x3F: self.cf ^= 1; return
        if op == 0x27: self._daa(); return

        # ---- 0xC0..0xFF: control, ALU-immediate, stack, I/O ----
        # conditional flag test for ccc = (op>>3)&7
        def cond(ccc):
            if ccc == 0: return self.zf == 0   # NZ
            if ccc == 1: return self.zf == 1   # Z
            if ccc == 2: return self.cf == 0   # NC
            if ccc == 3: return self.cf == 1   # C
            if ccc == 4: return self.pf == 0   # PO (parity odd)
            if ccc == 5: return self.pf == 1   # PE (parity even)
            if ccc == 6: return self.sf == 0   # P (positive)
            return self.sf == 1                # M (minus)

        low = op & 0xF
        # RET / Rcc  (0xD9 = undocumented RET, as on the real 8080)
        if op == 0xC9 or op == 0xD9: self.pc = self._pop(); return
        if op in (0xC0, 0xC8, 0xD0, 0xD8, 0xE0, 0xE8, 0xF0, 0xF8):
            if cond((op >> 3) & 7): self.pc = self._pop()
            return
        # JMP / Jcc
        if op == 0xC3 or op == 0xCB:
            self.pc = self._next_w(); return
        if op in (0xC2, 0xCA, 0xD2, 0xDA, 0xE2, 0xEA, 0xF2, 0xFA):
            addr = self._next_w()
            if cond((op >> 3) & 7): self.pc = addr
            return
        # CALL / Ccc
        if op in (0xCD, 0xDD, 0xED, 0xFD):
            addr = self._next_w(); self._push(self.pc); self.pc = addr; return
        if op in (0xC4, 0xCC, 0xD4, 0xDC, 0xE4, 0xEC, 0xF4, 0xFC):
            addr = self._next_w()
            if cond((op >> 3) & 7):
                self._push(self.pc); self.pc = addr
            return
        # RST n
        if op in (0xC7, 0xCF, 0xD7, 0xDF, 0xE7, 0xEF, 0xF7, 0xFF):
            self._push(self.pc); self.pc = op & 0x38; return
        # PUSH rp
        if op == 0xC5: self._push(self.bc); return
        if op == 0xD5: self._push(self.de); return
        if op == 0xE5: self._push(self.hl); return
        if op == 0xF5: self._push((self.a << 8) | self.get_psw()); return
        # POP rp
        if op == 0xC1: self.set_bc(self._pop()); return
        if op == 0xD1: self.set_de(self._pop()); return
        if op == 0xE1: self.set_hl(self._pop()); return
        if op == 0xF1:
            v = self._pop(); self.a = (v >> 8) & 0xFF; self.set_psw(v & 0xFF); return
        # ALU immediate
        if op == 0xC6: self._add(self._next_b(), 0); return
        if op == 0xCE: self._add(self._next_b(), self.cf); return
        if op == 0xD6: self._sub(self._next_b(), 0); return
        if op == 0xDE: self._sub(self._next_b(), self.cf); return
        if op == 0xE6: self._ana(self._next_b()); return
        if op == 0xEE: self._xra(self._next_b()); return
        if op == 0xF6: self._ora(self._next_b()); return
        if op == 0xFE: self._cmp(self._next_b()); return
        # misc
        if op == 0xEB:  # XCHG
            self.h, self.d = self.d, self.h
            self.l, self.e = self.e, self.l
            return
        if op == 0xE3:  # XTHL
            t = self.rw(self.sp); self.ww(self.sp, self.hl); self.set_hl(t); return
        if op == 0xF9:  # SPHL
            self.sp = self.hl; return
        if op == 0xE9:  # PCHL
            self.pc = self.hl; return
        if op == 0xDB:  # IN port
            p = self._next_b()
            self.a = (self.in_cb(p) & 0xFF) if self.in_cb else 0xFF
            return
        if op == 0xD3:  # OUT port
            p = self._next_b()
            if self.out_cb: self.out_cb(p, self.a)
            return
        if op == 0xFB: self.iff = 1; return   # EI
        if op == 0xF3: self.iff = 0; return   # DI

        raise RuntimeError(f"unimplemented opcode 0x{op:02X} at pc=0x{(self.pc-1)&0xFFFF:04X}")


if __name__ == "__main__":
    # trivial smoke test: ADI parity + sub borrow
    cpu = I8080()
    cpu.a = 0x14
    cpu._add(0x01, 0)             # 0x15 -> parity of 0x15 (00010101 -> three 1s -> odd -> PF=0)
    print(f"A=0x{cpu.a:02X} PF={cpu.pf} (expect 0, odd parity)")
    cpu.a = 0x03
    cpu._add(0x03, 0)             # 0x06 (two 1s -> even -> PF=1)
    print(f"A=0x{cpu.a:02X} PF={cpu.pf} (expect 1, even parity)")
    cpu.a = 0x05
    cpu._sub(0x0A, 0)             # 5-10 -> borrow -> CF=1, A=0xFB
    print(f"A=0x{cpu.a:02X} CF={cpu.cf} (expect A=0xFB CF=1)")
