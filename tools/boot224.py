#!/usr/bin/env python3
"""Flexible 224-family boot harness: load a ROM set, start at a given PC, stub the
I/O ports, run, and report whether the program/preset RAM tables get populated
(getting past the diagnostic-reset blocker by entering the operational cold-boot)."""
import os, sys
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from z80emu import Z80
from collections import Counter

ROOT=os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),"ROMs","Lexicon 224")

SETS={
 "v8_21":  dict(dir="224XL v8_21", sbc=[("SBC1 2716.BIN",0),("SBC2 2716.BIN",0x800),("SBC3 2716.BIN",0x1000)],
                nvs=[f"NVS{n} 2732.BIN" for n in range(1,9)]),
 "224X_v8_1": dict(dir="224X v8_1", sbc=[("SBC1 2716.BIN",0),("SBC2 2716.BIN",0x800)],
                nvs=[f"NVS{n} 2732.BIN" for n in range(1,7)]),
}

def load(setname):
    s=SETS[setname]; d=os.path.join(ROOT,s["dir"]); mem=bytearray(0x10000)
    for fn,base in s["sbc"]:
        b=np.fromfile(os.path.join(d,fn),dtype=np.uint8); mem[base:base+len(b)]=b.tobytes()
    for i,fn in enumerate(s["nvs"]):
        b=np.fromfile(os.path.join(d,fn),dtype=np.uint8); base=0x8000+i*0x1000; mem[base:base+len(b)]=b.tobytes()
    return mem

def boot(setname, start, max_ins=15_000_000, in_val=0x00, in_map=None):
    mem=load(setname); cpu=Z80(mem)
    ins_ports=Counter()
    def inh(p):
        ins_ports.update([p])
        return in_map.get(p,in_val) if in_map else in_val
    cpu.in_hook=inh
    cpu.out_hook=lambda p,v:None
    cpu.PC=start; cpu.SP=0x4780
    # stuck = no progress in tables for a long window while PC stays in a tiny set
    def tabsig(): return sum(mem[0x2035:0x2100])+sum(mem[0x3c40:0x3d00])
    last_sig=tabsig(); last_change=0; first_pop=None
    recent=Counter(); win=0
    for i in range(max_ins):
        try: cpu.step()
        except Exception as e:
            print(f"  [{setname}@0x{start:04X}] ABORT @0x{cpu.PC:04X} after {i}: {e}"); break
        if (i & 0x3FFFF)==0:   # every ~256k ins, check progress
            sig=tabsig()
            if first_pop is None and (mem[0x2067]!=0 or mem[0x20af]!=0): first_pop=i
            if sig!=last_sig: last_sig=sig; last_change=i
            elif i-last_change>1_500_000:
                print(f"  [{setname}@0x{start:04X}] settled (no table change 1.5M ins) @0x{cpu.PC:04X} after {i}"); break
    else:
        print(f"  [{setname}@0x{start:04X}] ran {max_ins} ins, PC=0x{cpu.PC:04X}")
    print(f"    first table populate @ins {first_pop}")
    print(f"    IN ports: {[(hex(p),c) for p,c in ins_ports.most_common(6)]}")
    # program/preset table population check
    for label,addr,n in [("0x2035",0x2035,12),("0x2067",0x2067,12),("0x20AF",0x20AF,12),
                          ("0x3ca2",0x3ca2,12),("0x3c40",0x3c40,12)]:
        seg=mem[addr:addr+n]; nz=sum(1 for x in seg if x not in (0,0xFF))
        print(f"    RAM {label}: "+" ".join("%02X"%x for x in seg)+f"   (nz={nz})")
    return mem,cpu

if __name__=="__main__":
    print("### 224X v8_1 from reset 0x0000 (operational firmware), IN=0x00 ###")
    boot("224X_v8_1", 0x0000, in_val=0x00)
