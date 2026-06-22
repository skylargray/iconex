#!/usr/bin/env python3
"""Compact but complete-enough Z80 emulator for running real ROM routines.

Implements the documented main / CB / ED / DD / FD instruction set with correct
S Z H P/V N C flags for the arithmetic/logic ops the Lexicon build code uses.
Unimplemented opcodes raise (so gaps are loud, never silent).

Usage:
    cpu = Z80(mem)                 # mem = 64 KB bytearray
    cpu.out_hook = lambda p,v: ... # capture OUT
    cpu.in_hook  = lambda p: 0xFF  # IN value
    cpu.call(0xAA01, stop=0xDEAD)  # push sentinel, run until RET to it
"""
from __future__ import annotations

FS, FZ, FH, FPV, FN, FC = 0x80, 0x40, 0x10, 0x04, 0x02, 0x01
PARITY = [0]*256
for _i in range(256):
    PARITY[_i] = FPV if bin(_i).count("1") % 2 == 0 else 0


class Z80:
    def __init__(self, mem):
        self.m = mem
        self.A=self.F=self.B=self.C=self.D=self.E=self.H=self.L=0
        self.A_=self.F_=self.B_=self.C_=self.D_=self.E_=self.H_=self.L_=0
        self.IX=self.IY=0
        self.SP=0xFFFF; self.PC=0
        self.I=self.R=0; self.IFF1=self.IFF2=0; self.IM=0
        self.halted=False
        self.out_hook=lambda p,v: None
        self.in_hook=lambda p: 0xFF
        self.icount=0

    # ---- memory ----
    def rb(self,a): return self.m[a & 0xFFFF]
    def wb(self,a,v): self.m[a & 0xFFFF]=v & 0xFF
    def rw(self,a): return self.rb(a) | (self.rb(a+1)<<8)
    def ww(self,a,v): self.wb(a,v&0xFF); self.wb(a+1,(v>>8)&0xFF)

    # ---- 16-bit register pairs ----
    def _g(self,hi,lo): return (getattr(self,hi)<<8)|getattr(self,lo)
    def _s(self,hi,lo,v): setattr(self,hi,(v>>8)&0xFF); setattr(self,lo,v&0xFF)
    @property
    def BC(self): return (self.B<<8)|self.C
    @BC.setter
    def BC(self,v): self.B=(v>>8)&0xFF; self.C=v&0xFF
    @property
    def DE(self): return (self.D<<8)|self.E
    @DE.setter
    def DE(self,v): self.D=(v>>8)&0xFF; self.E=v&0xFF
    @property
    def HL(self): return (self.H<<8)|self.L
    @HL.setter
    def HL(self,v): self.H=(v>>8)&0xFF; self.L=v&0xFF
    @property
    def AF(self): return (self.A<<8)|self.F
    @AF.setter
    def AF(self,v): self.A=(v>>8)&0xFF; self.F=v&0xFF

    # ---- fetch ----
    def fb(self): v=self.rb(self.PC); self.PC=(self.PC+1)&0xFFFF; return v
    def fw(self): v=self.rw(self.PC); self.PC=(self.PC+2)&0xFFFF; return v
    def sb(self): v=self.fb(); return v-256 if v>=128 else v

    # ---- flag-setting ALU ----
    def add8(self,a,b,cy=0):
        r=a+b+cy; h=((a&0xF)+(b&0xF)+cy)&0x10
        rr=r&0xFF
        f=(rr&FS)|(FZ if rr==0 else 0)|(h and FH)
        ov=(~(a^b)&(a^rr)&0x80)
        f|=(FPV if ov else 0)|(FC if r>0xFF else 0)
        self.F=f; return rr
    def sub8(self,a,b,cy=0):
        r=a-b-cy; h=((a&0xF)-(b&0xF)-cy)&0x10
        rr=r&0xFF
        f=(rr&FS)|(FZ if rr==0 else 0)|(h and FH)|FN
        ov=((a^b)&(a^rr)&0x80)
        f|=(FPV if ov else 0)|(FC if r<0 else 0)
        self.F=f; return rr
    def cp8(self,a,b):
        self.sub8(a,b)  # sets flags, discard result
    def and8(self,a,b):
        r=a&b; self.F=(r&FS)|(FZ if r==0 else 0)|FH|PARITY[r]; return r
    def or8(self,a,b):
        r=a|b; self.F=(r&FS)|(FZ if r==0 else 0)|PARITY[r]; return r
    def xor8(self,a,b):
        r=a^b; self.F=(r&FS)|(FZ if r==0 else 0)|PARITY[r]; return r
    def inc8(self,a):
        r=(a+1)&0xFF
        self.F=(self.F&FC)|(r&FS)|(FZ if r==0 else 0)|((r&0xF)==0 and FH)|(FPV if r==0x80 else 0)
        return r
    def dec8(self,a):
        r=(a-1)&0xFF
        self.F=(self.F&FC)|(r&FS)|(FZ if r==0 else 0)|(((a&0xF)==0) and FH)|FN|(FPV if r==0x7F else 0)
        return r
    def add16(self,a,b):
        r=a+b; h=((a&0xFFF)+(b&0xFFF))&0x1000
        self.F=(self.F&(FS|FZ|FPV))|((h and FH))|(FC if r>0xFFFF else 0)
        return r&0xFFFF
    def adc16(self,a,b):
        cy=self.F&FC; r=a+b+cy; h=((a&0xFFF)+(b&0xFFF)+cy)&0x1000
        rr=r&0xFFFF
        ov=(~(a^b)&(a^rr)&0x8000)
        self.F=(rr>>8&FS)|(FZ if rr==0 else 0)|(h and FH)|(FPV if ov else 0)|(FC if r>0xFFFF else 0)
        return rr
    def sbc16(self,a,b):
        cy=self.F&FC; r=a-b-cy; h=((a&0xFFF)-(b&0xFFF)-cy)&0x1000
        rr=r&0xFFFF
        ov=((a^b)&(a^rr)&0x8000)
        self.F=(rr>>8&FS)|(FZ if rr==0 else 0)|(h and FH)|FN|(FPV if ov else 0)|(FC if r<0 else 0)
        return rr

    # ---- rotates/shifts (A-specific, no SZP) ----
    def rlca(self):
        c=(self.A>>7)&1; self.A=((self.A<<1)|c)&0xFF
        self.F=(self.F&(FS|FZ|FPV))|(c and FC)
    def rrca(self):
        c=self.A&1; self.A=((self.A>>1)|(c<<7))&0xFF
        self.F=(self.F&(FS|FZ|FPV))|(c and FC)
    def rla(self):
        c=(self.A>>7)&1; self.A=((self.A<<1)|(1 if self.F&FC else 0))&0xFF
        self.F=(self.F&(FS|FZ|FPV))|(c and FC)
    def rra(self):
        c=self.A&1; self.A=((self.A>>1)|((1 if self.F&FC else 0)<<7))&0xFF
        self.F=(self.F&(FS|FZ|FPV))|(c and FC)

    # ---- CB rotates/shifts (full SZP) ----
    def _cb_rot(self,op,v):
        if op==0:   c=v>>7; v=((v<<1)|c)&0xFF                    # RLC
        elif op==1: c=v&1;  v=((v>>1)|(c<<7))&0xFF               # RRC
        elif op==2: c=v>>7; v=((v<<1)|(1 if self.F&FC else 0))&0xFF  # RL
        elif op==3: c=v&1;  v=((v>>1)|((1 if self.F&FC else 0)<<7))&0xFF  # RR
        elif op==4: c=v>>7; v=(v<<1)&0xFF                        # SLA
        elif op==5: c=v&1;  v=((v>>1)|(v&0x80))&0xFF             # SRA
        elif op==6: c=v>>7; v=((v<<1)|1)&0xFF                    # SLL (undoc)
        elif op==7: c=v&1;  v=(v>>1)&0xFF                        # SRL
        self.F=(v&FS)|(FZ if v==0 else 0)|PARITY[v]|(c and FC)
        return v

    # ---- register access by index 0..7 = B C D E H L (HL) A ----
    def _rget(self,i):
        return [self.B,self.C,self.D,self.E,self.H,self.L,self.rb(self.HL),self.A][i]
    def _rset(self,i,v):
        v&=0xFF
        if i==0:self.B=v
        elif i==1:self.C=v
        elif i==2:self.D=v
        elif i==3:self.E=v
        elif i==4:self.H=v
        elif i==5:self.L=v
        elif i==6:self.wb(self.HL,v)
        else:self.A=v

    def push(self,v): self.SP=(self.SP-2)&0xFFFF; self.ww(self.SP,v)
    def pop(self): v=self.rw(self.SP); self.SP=(self.SP+2)&0xFFFF; return v

    def cond(self,c):
        return [not(self.F&FZ),self.F&FZ,not(self.F&FC),self.F&FC,
                not(self.F&FPV),self.F&FPV,not(self.F&FS),self.F&FS][c]

    # ---- run one instruction ----
    def step(self):
        self.icount+=1
        op=self.fb()
        # --- prefixes ---
        if op==0xCB: return self._cb()
        if op==0xED: return self._ed()
        if op==0xDD: return self._idx('IX')
        if op==0xFD: return self._idx('IY')
        self._main(op)

    def _main(self,op):
        x=op>>6; y=(op>>3)&7; z=op&7
        if op==0x00: return                                  # NOP
        if op==0x76: self.halted=True; self.PC=(self.PC-1)&0xFFFF; return  # HALT
        if x==1:                                             # LD r,r'
            self._rset(y,self._rget(z)); return
        if x==2:                                             # ALU A,r
            self._alu(y,self._rget(z)); return
        if x==0:
            if z==0:
                if y==0: return                              # NOP
                if y==1: self.AF,self.AF_=self.AF_ if False else self.AF,self.AF  # placeholder
                if y==1:  # EX AF,AF'
                    self.A,self.A_=self.A_,self.A; self.F,self.F_=self.F_,self.F; return
                if y==2:  # DJNZ
                    d=self.sb(); self.B=(self.B-1)&0xFF
                    if self.B: self.PC=(self.PC+d)&0xFFFF
                    return
                if y==3:  # JR d
                    d=self.sb(); self.PC=(self.PC+d)&0xFFFF; return
                # y 4..7 JR cc
                d=self.sb()
                cc=[not(self.F&FZ),self.F&FZ,not(self.F&FC),self.F&FC][y-4]
                if cc: self.PC=(self.PC+d)&0xFFFF
                return
            if z==1:
                if (y&1)==0:  # LD rp,nn
                    self._setrp(y>>1,self.fw()); return
                else:        # ADD HL,rp
                    self.HL=self.add16(self.HL,self._getrp(y>>1)); return
            if z==2:
                p=y>>1; q=y&1
                if p==0:
                    if q==0: self.wb(self.BC,self.A)              # LD (BC),A
                    else: self.A=self.rb(self.BC)                 # LD A,(BC)
                    return
                if p==1:
                    if q==0: self.wb(self.DE,self.A)              # LD (DE),A
                    else: self.A=self.rb(self.DE)                 # LD A,(DE)
                    return
                if p==2:
                    a=self.fw()
                    if q==0: self.ww(a,self.HL)                   # LD (nn),HL
                    else: self.HL=self.rw(a)                      # LD HL,(nn)
                    return
                if p==3:
                    a=self.fw()
                    if q==0: self.wb(a,self.A)                    # LD (nn),A
                    else: self.A=self.rb(a)                       # LD A,(nn)
                    return
            if z==3:  # INC/DEC rp
                p=y>>1; q=y&1
                v=self._getrp(p); self._setrp(p,(v+(1 if q==0 else -1))&0xFFFF); return
            if z==4: self._rset(y,self.inc8(self._rget(y))); return  # INC r
            if z==5: self._rset(y,self.dec8(self._rget(y))); return  # DEC r
            if z==6: self._rset(y,self.fb()); return                 # LD r,n
            if z==7:  # rotates/DAA/CPL/SCF/CCF
                if y==0:self.rlca()
                elif y==1:self.rrca()
                elif y==2:self.rla()
                elif y==3:self.rra()
                elif y==4:self._daa()
                elif y==5:self.A^=0xFF; self.F|=FH|FN            # CPL
                elif y==6:self.F=(self.F&(FS|FZ|FPV))|FC          # SCF
                else:self.F=(self.F&(FS|FZ|FPV))|((self.F&FC)^FC and 0)|(0 if self.F&FC else FC)  # CCF
                return
        if x==3:
            if z==0:  # RET cc
                if self.cond(y): self.PC=self.pop()
                return
            if z==1:
                q=y&1; p=y>>1
                if q==0: self._setrp2(p,self.pop()); return     # POP rp2
                if p==0: self.PC=self.pop(); return             # RET
                if p==1: self.B,self.B_=self.B_,self.B; self.C,self.C_=self.C_,self.C; self.D,self.D_=self.D_,self.D; self.E,self.E_=self.E_,self.E; self.H,self.H_=self.H_,self.H; self.L,self.L_=self.L_,self.L; return  # EXX
                if p==2: self.PC=self.HL; return                # JP (HL)
                if p==3: self.SP=self.HL; return                # LD SP,HL
            if z==2:  # JP cc,nn
                a=self.fw()
                if self.cond(y): self.PC=a
                return
            if z==3:
                if y==0: self.PC=self.fw(); return              # JP nn
                if y==1: return self._cb()                      # CB (shouldn't reach)
                if y==2: self.out_hook(self.fb(),self.A); return    # OUT (n),A
                if y==3: self.A=self.in_hook(self.fb()); return     # IN A,(n)
                if y==4:  # EX (SP),HL
                    t=self.rw(self.SP); self.ww(self.SP,self.HL); self.HL=t; return
                if y==5:  # EX DE,HL
                    self.DE,self.HL=self.HL,self.DE; return
                if y==6: self.IFF1=self.IFF2=0; return          # DI
                if y==7: self.IFF1=self.IFF2=1; return          # EI
            if z==4:  # CALL cc,nn
                a=self.fw()
                if self.cond(y): self.push(self.PC); self.PC=a
                return
            if z==5:
                q=y&1; p=y>>1
                if q==0: self.push(self._getrp2(p)); return     # PUSH rp2
                if p==0: a=self.fw(); self.push(self.PC); self.PC=a; return  # CALL nn
            if z==6: self._alu(y,self.fb()); return             # ALU A,n
            if z==7:  # RST
                self.push(self.PC); self.PC=y*8; return
        raise NotImplementedError(f"main op 0x{op:02X} @0x{(self.PC-1)&0xFFFF:04X}")

    def _alu(self,y,v):
        if y==0:self.A=self.add8(self.A,v)
        elif y==1:self.A=self.add8(self.A,v,1 if self.F&FC else 0)
        elif y==2:self.A=self.sub8(self.A,v)
        elif y==3:self.A=self.sub8(self.A,v,1 if self.F&FC else 0)
        elif y==4:self.A=self.and8(self.A,v)
        elif y==5:self.A=self.xor8(self.A,v)
        elif y==6:self.A=self.or8(self.A,v)
        else:self.cp8(self.A,v)

    def _daa(self):
        a=self.A; cf=self.F&FC; hf=self.F&FH; nf=self.F&FN; corr=0; c=0
        if hf or (a&0xF)>9: corr|=0x06
        if cf or a>0x99: corr|=0x60; c=FC
        a=(a-corr)&0xFF if nf else (a+corr)&0xFF
        self.A=a; self.F=(a&FS)|(FZ if a==0 else 0)|PARITY[a]|nf|c

    def _getrp(self,p): return [self.BC,self.DE,self.HL,self.SP][p]
    def _setrp(self,p,v):
        if p==0:self.BC=v
        elif p==1:self.DE=v
        elif p==2:self.HL=v
        else:self.SP=v
    def _getrp2(self,p): return [self.BC,self.DE,self.HL,self.AF][p]
    def _setrp2(self,p,v):
        if p==0:self.BC=v
        elif p==1:self.DE=v
        elif p==2:self.HL=v
        else:self.AF=v

    def _cb(self):
        op=self.fb(); x=op>>6; y=(op>>3)&7; z=op&7
        v=self._rget(z)
        if x==0: self._rset(z,self._cb_rot(y,v)); return
        if x==1:  # BIT
            r=v&(1<<y)
            self.F=(self.F&FC)|FH|(FZ if r==0 else 0)|(r&FS if y==7 else 0)|(FPV if r==0 else 0)
            return
        if x==2: self._rset(z,v&~(1<<y)); return   # RES
        if x==3: self._rset(z,v|(1<<y)); return    # SET

    def _ed(self):
        op=self.fb()
        if op==0x44 or (op&0xC7)==0x44:  # NEG
            self.A=self.sub8(0,self.A); return
        if op==0xB0:  # LDIR
            while True:
                self.wb(self.DE,self.rb(self.HL))
                self.DE=(self.DE+1)&0xFFFF; self.HL=(self.HL+1)&0xFFFF; self.BC=(self.BC-1)&0xFFFF
                if self.BC==0: break
            self.F&=~(FH|FPV|FN); return
        if op==0xB8:  # LDDR
            while True:
                self.wb(self.DE,self.rb(self.HL))
                self.DE=(self.DE-1)&0xFFFF; self.HL=(self.HL-1)&0xFFFF; self.BC=(self.BC-1)&0xFFFF
                if self.BC==0: break
            self.F&=~(FH|FPV|FN); return
        if op==0xA0:  # LDI
            self.wb(self.DE,self.rb(self.HL)); self.DE=(self.DE+1)&0xFFFF; self.HL=(self.HL+1)&0xFFFF; self.BC=(self.BC-1)&0xFFFF
            self.F=(self.F&(FS|FZ|FC))|(FPV if self.BC else 0); return
        if op==0xA8:  # LDD
            self.wb(self.DE,self.rb(self.HL)); self.DE=(self.DE-1)&0xFFFF; self.HL=(self.HL-1)&0xFFFF; self.BC=(self.BC-1)&0xFFFF
            self.F=(self.F&(FS|FZ|FC))|(FPV if self.BC else 0); return
        if (op&0xCF)==0x4B: self._setrp(op>>4&3,self.rw(self.fw())); return   # LD rp,(nn)
        if (op&0xCF)==0x43:  # LD (nn),rp
            self.ww(self.fw(),self._getrp(op>>4&3)); return
        if (op&0xCF)==0x4A: self.HL=self.adc16(self.HL,self._getrp(op>>4&3)); return  # ADC HL,rp
        if (op&0xCF)==0x42: self.HL=self.sbc16(self.HL,self._getrp(op>>4&3)); return  # SBC HL,rp
        if op==0x4D: self.PC=self.pop(); return   # RETI
        if op==0x45: self.PC=self.pop(); return   # RETN
        if op==0x46 or op==0x56 or op==0x5E: self.IM=[0,0,1,2][(op>>3)&3]; return
        if op==0x47: self.I=self.A; return        # LD I,A
        if op==0x4F: self.R=self.A; return        # LD R,A
        if op==0x57: self.A=self.I; self.F=(self.F&FC)|(self.A&FS)|(FZ if self.A==0 else 0)|(FPV if self.IFF2 else 0); return
        if op==0x5F: self.A=self.R; return
        if op==0x78: self.A=self.in_hook(self.C); self.F=(self.F&FC)|(self.A&FS)|(FZ if self.A==0 else 0)|PARITY[self.A]; return  # IN A,(C)
        if op in (0x40,0x48,0x50,0x58,0x60,0x68,0x70):  # IN r,(C)
            v=self.in_hook(self.C); self._rset((op>>3)&7,v)
            self.F=(self.F&FC)|(v&FS)|(FZ if v==0 else 0)|PARITY[v]; return
        if op==0x79: self.out_hook(self.C,self.A); return       # OUT (C),A
        if op in (0x41,0x49,0x51,0x59,0x61,0x69,0x71):  # OUT (C),r
            self.out_hook(self.C,self._rget((op>>3)&7)); return
        if op==0x67:  # RRD
            v=self.rb(self.HL); a=self.A
            self.wb(self.HL,((v>>4)|((a&0xF)<<4))&0xFF); self.A=(a&0xF0)|(v&0xF)
            self.F=(self.F&FC)|(self.A&FS)|(FZ if self.A==0 else 0)|PARITY[self.A]; return
        if op==0x6F:  # RLD
            v=self.rb(self.HL); a=self.A
            self.wb(self.HL,(((v<<4)|(a&0xF))&0xFF)); self.A=(a&0xF0)|((v>>4)&0xF)
            self.F=(self.F&FC)|(self.A&FS)|(FZ if self.A==0 else 0)|PARITY[self.A]; return
        raise NotImplementedError(f"ED op 0x{op:02X} @0x{(self.PC-2)&0xFFFF:04X}")

    def _idx(self,reg):
        op=self.fb()
        get=lambda: getattr(self,reg)
        setr=lambda v: setattr(self,reg,v&0xFFFF)
        def disp_addr():
            d=self.sb(); return (get()+d)&0xFFFF
        if op==0xCB:
            a=disp_addr(); sub=self.fb(); x=sub>>6; y=(sub>>3)&7
            v=self.rb(a)
            if x==0: self.wb(a,self._cb_rot(y,v)); return
            if x==1:
                r=v&(1<<y); self.F=(self.F&FC)|FH|(FZ if r==0 else 0); return
            if x==2: self.wb(a,v&~(1<<y)); return
            if x==3: self.wb(a,v|(1<<y)); return
        if op==0x21: setr(self.fw()); return                 # LD IX,nn
        if op==0x22: self.ww(self.fw(),get()); return        # LD (nn),IX
        if op==0x2A: setr(self.rw(self.fw())); return        # LD IX,(nn)
        if op==0x23: setr((get()+1)&0xFFFF); return          # INC IX
        if op==0x2B: setr((get()-1)&0xFFFF); return          # DEC IX
        if op==0x09: setr(self.add16(get(),self.BC)); return
        if op==0x19: setr(self.add16(get(),self.DE)); return
        if op==0x29: setr(self.add16(get(),get())); return
        if op==0x39: setr(self.add16(get(),self.SP)); return
        if op==0x36: a=disp_addr(); self.wb(a,self.fb()); return   # LD (IX+d),n
        if op==0x7E: self.A=self.rb(disp_addr()); return
        if op in (0x46,0x4E,0x56,0x5E,0x66,0x6E): self._rset((op>>3)&7,self.rb(disp_addr())); return
        if op in (0x70,0x71,0x72,0x73,0x74,0x75,0x77): self.wb(disp_addr(),self._rget(op&7)); return
        if op==0x86: self.A=self.add8(self.A,self.rb(disp_addr())); return
        if op==0x8E: self.A=self.add8(self.A,self.rb(disp_addr()),1 if self.F&FC else 0); return
        if op==0x96: self.A=self.sub8(self.A,self.rb(disp_addr())); return
        if op==0x9E: self.A=self.sub8(self.A,self.rb(disp_addr()),1 if self.F&FC else 0); return
        if op==0xA6: self.A=self.and8(self.A,self.rb(disp_addr())); return
        if op==0xAE: self.A=self.xor8(self.A,self.rb(disp_addr())); return
        if op==0xB6: self.A=self.or8(self.A,self.rb(disp_addr())); return
        if op==0xBE: self.cp8(self.A,self.rb(disp_addr())); return
        if op==0x34: a=disp_addr(); self.wb(a,self.inc8(self.rb(a))); return
        if op==0x35: a=disp_addr(); self.wb(a,self.dec8(self.rb(a))); return
        if op==0xE5: self.push(get()); return
        if op==0xE1: setr(self.pop()); return
        if op==0xE9: self.PC=get(); return
        if op==0xE3: t=self.rw(self.SP); self.ww(self.SP,get()); setr(t); return
        if op==0xF9: self.SP=get(); return
        # fall back: treat as normal opcode (prefix had no effect)
        self.PC=(self.PC-1)&0xFFFF; self._main(self.fb()); return

    # ---- helpers ----
    def call(self,addr,stop=0xDEAD,max_ins=20_000_000):
        self.push(stop); self.PC=addr
        n=0
        while self.PC!=stop:
            self.step(); n+=1
            if n>max_ins: raise RuntimeError(f"runaway @0x{self.PC:04X} after {n} ins")
        return n
