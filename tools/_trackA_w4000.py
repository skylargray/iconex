#!/usr/bin/env python3
"""Track A.5 / C.2: identify mem[0x4000:0x4200].

Boot the real v8.2.1 firmware (boot_xl machinery) for an FE program (CONCERT id=0x01)
and a non-FE program (CHAMBER id=0x08). Hook EVERY memory write into 0x4000..0x41FF,
record (PC, addr, value, icount, phase). Phase = which milestone window we're in.
Then dump final contents of 0x4000..0x41FF, and compare against:
  - the 0x3F4D offset buffer (validated tap source, read downward),
  - the 0x3E4E control image.
Conclude what 0x4000 is.
"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from collections import Counter
from z80emu import Z80
import boot_xl as B

LO, HI = 0x4000, 0x4200

class WatchMem(bytearray):
    def __init__(self, *a, **k):
        super().__init__(*a, **k)
        self.writes = []          # (icount, pc, addr, val)
        self.cpu = None
    def __setitem__(self, idx, val):
        if isinstance(idx, int) and LO <= idx < HI:
            pc = self.cpu.PC if self.cpu else -1
            ic = self.cpu.icount if self.cpu else -1
            self.writes.append((ic, pc, idx, val & 0xFF))
        super().__setitem__(idx, val)

def run(power_up_id, max_ins=20_000_000):
    base = B.load_mem()
    mem = WatchMem(base)
    cpu = Z80(mem)
    mem.cpu = cpu
    larc = B.LARC()
    aru = B.ARU()
    # suppress POST
    mem[B.ERR_H] = 0xC9
    mem[B.ERR_E] = 0xC9
    # patch power-up program id
    mem[0x8160] = 0x3E; mem[0x8161] = power_up_id & 0xFF; mem[0x8162] = 0x00

    def inh(p):
        if p == 0xEF: return larc.status(cpu)
        if p == 0xEE: return larc.data(cpu)
        return aru.inp(p)
    def outh(p, v):
        if p in (0xEE, 0xEF):
            larc.out(cpu, p, v); return
        aru.out(p, v)
    cpu.in_hook = inh; cpu.out_hook = outh
    cpu.PC = 0

    last_irq = 0; stop_count = 0
    milestones = {}
    for i in range(max_ins):
        pc = cpu.PC
        for key, mpc in (('handshake',0x0089),('normal_op',0x813B),
                         ('prog_load',0x13B6),('mainloop',0x8169)):
            if pc == mpc: milestones.setdefault(key, cpu.icount)
        if pc == 0x8169:
            stop_count += 1
            if stop_count >= 3: break
        if 64 and cpu.IFF1 and (cpu.icount-last_irq) >= 64 and (larc.tx_en or larc.rx_ready(cpu)):
            if cpu.interrupt(): last_irq = cpu.icount
        try:
            cpu.step()
        except Exception as e:
            print(f"  ABORT @0x{cpu.PC:04X} ic={cpu.icount}: {e}"); break
    return cpu, mem, milestones

def report(name, power_up_id):
    print("="*70)
    print(f"{name}  (power_up_id=0x{power_up_id:02X})")
    print("="*70)
    cpu, mem, ms = run(power_up_id)
    print("milestones icount:", {k:ms.get(k) for k in ('handshake','normal_op','prog_load','mainloop')})
    w = mem.writes
    pl = ms.get('prog_load')
    print(f"total writes into 0x4000..0x41FF: {len(w)}")
    # writes by PC
    by_pc = Counter((pc) for ic,pc,a,v in w)
    print("top writer PCs:")
    for pc,c in by_pc.most_common(15):
        print(f"    0x{pc:04X}: {c}")
    # writes that occur AFTER prog_load milestone (program-specific)
    if pl is not None:
        after = [t for t in w if t[0] >= pl]
        print(f"writes after prog_load ({pl}): {len(after)}")
        bypc2 = Counter(pc for ic,pc,a,v in after)
        for pc,c in bypc2.most_common(15):
            print(f"    0x{pc:04X}: {c}")
    # final contents
    final = bytes(mem[LO:HI])
    nonff = sum(1 for b in final if b != 0xFF)
    print(f"final 0x4000..0x41FF: {nonff}/512 bytes != 0xFF")
    # dump first 64 + a couple control words
    def hx(a,n): return " ".join(f"{mem[a+i]:02X}" for i in range(n))
    print(f"  0x4000: {hx(0x4000,32)}")
    print(f"  0x4020: {hx(0x4020,32)}")
    print(f"  0x4070: {hx(0x4070,16)}   (ctrl regs 4072/4074/4076)")
    print(f"  0x4130: {hx(0x4130,16)}   (4137 base / 4138)")
    print(f"  0x41E0: {hx(0x41E0,32)}")
    return cpu, mem, ms

if __name__ == "__main__":
    import aru224_emulate as AE
    for nm,pid in [("CHAMBER (non-FE)",0x08), ("CONCERT HALL (FE)",0x01)]:
        cpu, mem, ms = report(nm, pid)
        # compare with the validated 0x3F4D offset source as currently in memory
        print("  0x3F4D buffer (downward, 8 steps) signed offsets:")
        offs=[]
        for s in range(8):
            a = 0x3F4D - 2*s
            v = mem[a-1] | (mem[a]<<8)
            sv = v-0x10000 if v & 0x8000 else v
            offs.append(sv)
        print("   ", offs, " delays(-offset):", [-o for o in offs])
        print()
