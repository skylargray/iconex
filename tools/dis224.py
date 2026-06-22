#!/usr/bin/env python3
"""Full-memory 224XL disassembler + I/O-site scanner (SBC 0x0000-0x17FF + NVS 0x8000-0xFFFF).
Usage:
  python tools/dis224.py <start_hex> <end_hex>      # disassemble a range
  python tools/dis224.py scan EE EF                 # find IN/OUT sites for ports
"""
import os, sys
import numpy as np
from z80dis import z80

DIR=os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),"ROMs","Lexicon 224","224XL v8_21")

def load():
    mem=bytearray(0x10000)
    for fn,base in [("SBC1 2716.BIN",0),("SBC2 2716.BIN",0x800),("SBC3 2716.BIN",0x1000)]:
        b=np.fromfile(os.path.join(DIR,fn),dtype=np.uint8); mem[base:base+len(b)]=b.tobytes()
    for n in range(1,9):
        b=np.fromfile(os.path.join(DIR,f"NVS{n} 2732.BIN"),dtype=np.uint8); mem[0x8000+(n-1)*0x1000:0x8000+n*0x1000]=b.tobytes()
    return mem

MEM=load()

def dis(a0,a1):
    a=a0
    while a<a1:
        d=z80.decode(bytes(MEM[a:a+4]),a)
        print(f"  {a:04X}: {' '.join('%02X'%MEM[a+i] for i in range(d.len)):<11} {z80.disasm(d)}")
        a+=max(1,d.len)

def scan(ports):
    ports=[int(p,16) for p in ports]
    print(f"I/O sites for ports {[hex(p) for p in ports]} (SBC 0x0000-0x17FF):")
    a=0
    while a<0x1800:
        op=MEM[a]
        if op in (0xDB,0xD3) and a+1<0x1800 and MEM[a+1] in ports:
            kind="IN A," if op==0xDB else "OUT"
            print(f"  {a:04X}: {kind}(0x{MEM[a+1]:02X})")
            a+=2; continue
        try:
            d=z80.decode(bytes(MEM[a:a+4]),a); a+=max(1,d.len)
        except: a+=1

if __name__=="__main__":
    if sys.argv[1]=="scan":
        scan(sys.argv[2:])
    else:
        dis(int(sys.argv[1],16), int(sys.argv[2],16))
