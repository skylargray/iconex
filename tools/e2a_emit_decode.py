#!/usr/bin/env python3
"""TASK E2a: decode the interpreter emit formats AB26/AAE8/AACD field-by-field by
instrumenting a live CONCERT build. We single-step the AA9F interpreter, capturing
every store into the 0x3E4E intermediate image, attributing it to the store PC so
we know which handler/field wrote it. Then we decode the resulting 0x3E4E image as
4-byte microwords (lane2,lane3 per owner field map) and compare to the live 0x4000
image lanes 2,3 (authoritative control reference)."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import aru224_emulate as A
import boot_xl as B

RECBASE = 0xB800   # CONCERT
CCE = 0xFF         # full SIZE (matches Track E spine cce=FE/FF region)

# store-PC -> (handler, field-role)
STORE_PC = {
    # AB0C binder: writes coeff-source pointer lo,hi into image (HL+=2)
    0xAB1C: ("AB0C", "ptr_lo"),
    0xAB1E: ("AB0C", "ptr_hi"),
    # AB26 (sub 0x00): one image byte/ref = the coeff byte returned by AB0C
    0xAB30: ("AB26", "img_byte"),
    # AAE8 (sub 0x10): CSIGN-conditional dual byte
    0xAAFB: ("AAE8", "csign_byte"),   # only if bit7 set
    0xAB02: ("AAE8", "img_byte"),
    # AACD (sub 0x20): 3 image bytes/ref
    0xAAD7: ("AACD", "byte0"),
    0xAADB: ("AACD", "byte1"),
    0xAADF: ("AACD", "byte2"),
    # descriptor writes into 0x3CF4 area (AAA5/AAA8/AAAB) -- ignore for image
}

def build_and_trace(recbase, cce):
    cpu = A.new_cpu()
    A.seed_record(cpu, recbase, cce, 0)
    fe = cpu.m[(recbase+0x30)&0xFFFF]==0xFE
    cpu.call(0xB55B, max_ins=2_000_000)
    bc_ptr = recbase + (0x44 if fe else 0x35)
    cpu.DE = bc_ptr; cpu.HL=0x3e4e; cpu.BC=0x3cf4; cpu.PC=0xAA9F

    writes = []   # (img_addr, value, store_pc, handler, role, descriptor_idx)
    headers = []  # per emitted step: (step_idx, descriptor3, subop, ncount, img_start, img_end)
    n=0
    cur_desc_start = None
    cur_descriptor = []
    step_idx = -1
    # snapshot the 3-byte descriptor each time we pass AAAD (after writing it to 0x3CF4)
    while cpu.PC != 0xAB39:
        pc = cpu.PC
        # capture descriptor begin: AA9F loads A=(DE); if INC A==0 -> terminator
        if pc == 0xAAA4:   # 7D LD A,L  (descriptor first byte about to be written)
            # the descriptor low byte is the bytecode (DE) we'll read at AAAA
            step_idx += 1
            cur_desc_start = None
        if pc == 0xAAB2:   # about to read subop byte (DE) = the step's header byte
            hdr = cpu.m[cpu.DE & 0xFFFF]
        # record store
        if pc in STORE_PC:
            hl = cpu.HL & 0xFFFF
            val = cpu.rb(0xAAAA) if False else (cpu.A & 0xFF)  # A holds the byte being stored for LD (HL),A
            handler, role = STORE_PC[pc]
            writes.append((hl, cpu.A & 0xFF, pc, handler, role, step_idx))
        cpu.step(); n+=1
        if n>2_000_000: raise RuntimeError("runaway")
    return cpu, writes

def main():
    cpu, writes = build_and_trace(RECBASE, CCE)
    img_base = 0x3e4e
    # show first ~40 image bytes written, in order
    print(f"=== CONCERT recbase=0x{RECBASE:04X} cce=0x{CCE:02X}: first 40 image stores (0x3E4E up) ===")
    print(f"{'addr':>6} {'off':>4} {'val':>4} {'pc':>5} {'handler':<6} {'role':<11} step")
    for w in writes[:40]:
        hl,val,pc,handler,role,si = w
        print(f"0x{hl:04X} {hl-img_base:>4} 0x{val:02X} {pc:04X} {handler:<6} {role:<11} {si}")
    print(f"\ntotal image stores: {len(writes)}")
    # role histogram
    from collections import Counter
    print("by handler:", Counter(w[3] for w in writes))
    print("by role   :", Counter(w[4] for w in writes))
    return cpu, writes

if __name__=="__main__":
    main()
