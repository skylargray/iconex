#!/usr/bin/env python3
"""E2a part 2: capture per-slot-ref the (slot k, raw bytecode bytes consumed,
image bytes emitted) for each handler, and decode the image bytes as lane2/lane3
control fields. Then boot live CONCERT and decode 0x4000 lanes 2,3 to compare."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import aru224_emulate as A
import boot_xl as B

RECBASE = 0xB800
CCE = 0xFF

def build_and_trace(recbase, cce):
    cpu = A.new_cpu()
    A.seed_record(cpu, recbase, cce, 0)
    fe = cpu.m[(recbase+0x30)&0xFFFF]==0xFE
    cpu.call(0xB55B, max_ins=2_000_000)
    bc_ptr = recbase + (0x44 if fe else 0x35)
    cpu.DE = bc_ptr; cpu.HL=0x3e4e; cpu.BC=0x3cf4; cpu.PC=0xAA9F

    refs = []   # per slot ref dict
    steps = []  # per step: subop, ncount, header byte, slot refs idx range
    n=0
    cur = None
    step_idx=-1
    cur_step=None
    while cpu.PC != 0xAB39:
        pc = cpu.PC
        if pc == 0xAAB2:
            # about to dispatch: A holds header byte (DE points at it)
            hdr = cpu.m[cpu.DE & 0xFFFF]
            step_idx += 1
            cur_step = dict(step=step_idx, hdr=hdr, subop=hdr&0x30, ncount=hdr&0x0F, refs=[])
            steps.append(cur_step)
        # AB0C entry: DE points at the slot-ref bytecode byte (bit7=CSIGN|bits0-6=k)
        if pc == 0xAB0C:
            slotbyte = cpu.m[cpu.DE & 0xFFFF]
            cur = dict(slotbyte=slotbyte, k=slotbyte&0x7f, csign_hi=(slotbyte>>7)&1,
                       img=[], img_addr=cpu.HL&0xFFFF, handler=None, bc=[slotbyte])
            if cur_step is not None: cur_step['refs'].append(cur)
            refs.append(cur)
        # image byte stores
        if pc in (0xAB30,):       # AB26
            cur['handler']='AB26'; cur['img'].append(('img', cpu.A&0xFF, cpu.HL&0xFFFF))
        if pc in (0xAAFB,):       # AAE8 csign byte
            cur['handler']='AAE8'; cur['img'].append(('csign', cpu.A&0xFF, cpu.HL&0xFFFF))
        if pc in (0xAB02,):       # AAE8 main byte
            cur['handler']='AAE8'; cur['img'].append(('main', cpu.A&0xFF, cpu.HL&0xFFFF))
        if pc in (0xAAD7,):       # AACD byte0
            cur['handler']='AACD'; cur['img'].append(('b0', cpu.A&0xFF, cpu.HL&0xFFFF))
        if pc in (0xAADB,):
            cur['img'].append(('b1', cpu.A&0xFF, cpu.HL&0xFFFF))
        if pc in (0xAADF,):
            cur['img'].append(('b2', cpu.A&0xFF, cpu.HL&0xFFFF))
        cpu.step(); n+=1
        if n>2_000_000: raise RuntimeError("runaway")
    return cpu, refs, steps

def main():
    cpu, refs, steps = build_and_trace(RECBASE, CCE)
    print(f"=== per-step header dispatch (CONCERT cce=0x{CCE:02X}) ===")
    for st in steps[:14]:
        print(f"step{st['step']:2d} hdr=0x{st['hdr']:02X} subop=0x{st['subop']:02X} N={st['ncount']} nrefs={len(st['refs'])}")
    print(f"\ntotal steps={len(steps)}  total refs={len(refs)}")

    print(f"\n=== first 16 slot refs: slot k, csign_hi, handler, image bytes ===")
    for i,r in enumerate(refs[:16]):
        imgs = " ".join(f"{tag}=0x{v:02X}" for tag,v,a in r['img'])
        print(f"ref{i:2d} k=0x{r['k']:02X}({r['k']:3d}) sb=0x{r['slotbyte']:02X} csH={r['csign_hi']} {r['handler']:<5} | {imgs}")
    return cpu, refs, steps

if __name__=="__main__":
    main()
