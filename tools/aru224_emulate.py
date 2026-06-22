#!/usr/bin/env python3
"""Run the real 224XL ARU build code in the Z80 emulator and read out the numeric
microword image, then decode offsets (delay = -offset) into a reverb tap map.

Memory map: SBC1@0x0000, SBC2@0x0800, SBC3@0x1000, NVS1..8 @0x8000+(n-1)*0x1000.
"""
import os, sys
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from z80emu import Z80, FC

DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                   "ROMs", "Lexicon 224", "224XL v8_21")

def load_mem():
    mem = bytearray(0x10000)
    for n,(base) in [(1,0x0000),(2,0x0800),(3,0x1000)]:
        b=np.fromfile(f"{DIR}/SBC{n} 2716.BIN",dtype=np.uint8)
        mem[base:base+len(b)]=b.tobytes()
    for n in range(1,9):
        b=np.fromfile(f"{DIR}/NVS{n} 2732.BIN",dtype=np.uint8)
        base=0x8000+(n-1)*0x1000
        mem[base:base+len(b)]=b.tobytes()
    return mem

def new_cpu(capture_out=True):
    cpu=Z80(load_mem())
    cpu.outs=[]
    if capture_out:
        cpu.out_hook=lambda p,v: cpu.outs.append((p,v))
    cpu.in_hook=lambda p: 0xFF
    return cpu

def run_until(cpu, stops, max_ins=5_000_000):
    n=0
    while cpu.PC not in stops:
        cpu.step(); n+=1
        if n>max_ins: raise RuntimeError(f"runaway @0x{cpu.PC:04X}")
    return n

def seed_record(cpu, recbase, cce=0, ccf=0):
    m=cpu.m
    cpu.ww(0x3e01, recbase)
    cpu.ww(0x3e03, recbase+4)
    cpu.ww(0x3e05, (recbase+0xC0AA)&0xFFFF)
    cpu.wb(0x3c5b, m[recbase+0x34])
    cpu.wb(0x3cd5, m[recbase+0x35])
    for i in range(13):
        m[0x3cd8+i]=m[(recbase+0x36+i)&0xFFFF]
    cpu.wb(0x3cce, cce); cpu.wb(0x3ccf, ccf)

def build_record(recbase, cce=0, ccf=0, verbose=True):
    cpu=new_cpu()
    seed_record(cpu, recbase, cce, ccf)
    fe = cpu.m[(recbase+0x30)&0xFFFF]==0xFE
    # 1) step-builder -> offset lanes into 0x3e4e / 0x3f4d
    try:
        cpu.call(0xB55B, max_ins=2_000_000)
    except Exception as e:
        if verbose: print(f"  B55B aborted: {e}")
    # 2) interpreter expander -> coeff lanes into 0x3e4e ; stop at terminator handler 0xAB39
    bc_ptr = recbase + (0x44 if fe else 0x35)
    cpu.DE = bc_ptr; cpu.HL=0x3e4e; cpu.BC=0x3cf4; cpu.PC=0xAA9F
    try:
        run_until(cpu, {0xAB39}, max_ins=2_000_000)
        interp_ok=True
    except Exception as e:
        interp_ok=False
        if verbose: print(f"  interp aborted: {e}")
    return cpu, fe, interp_ok

def decode_image(cpu, base=0x3e4e, n=128):
    """Read n 4-byte microword records; lane0:lane1 = 16-bit offset (delay=-offset)."""
    recs=[]
    for s in range(n):
        a=base+s*4
        b=[cpu.m[(a+i)&0xFFFF] for i in range(4)]
        raw=b[0]|(b[1]<<8); off=raw-0x10000 if raw&0x8000 else raw
        recs.append((s,b,off,-off))
    return recs

def tap_map(recbase, cce=0, ccf=0, verbose=True):
    """Run B55B and read the offset buffer it writes downward from 0x3F4D.
    Returns list of signed offsets (step order). delay = -offset (samples).

    Two record build paths (B55B @0xB55B checks recbase+0x30 == 0xFE):
      - FE path: offsets COMPUTED (ptr-writeptr) and written via the 0x3cf1 ptr.
      - non-FE path (0xB65A): a pre-built 128-entry offset table baked into the
        record at recbase+0xA7..0x2A7 is COPIED to 0x3F4D (0x3cf1 is NOT moved),
        so read a fixed 128 words. Validated byte-identical to the firmware load.
    """
    cpu=new_cpu(); seed_record(cpu,recbase,cce,ccf)
    cpu.ww(0x3cf1,0x3f4d)
    try: cpu.call(0xB55B, max_ins=2_000_000)
    except Exception as e:
        if verbose: print(f"  B55B aborted: {e}")
    fe = cpu.m[(recbase+0x30)&0xFFFF]==0xFE
    top=0x3f4d; bot=cpu.rw(0x3cf1)            # buffer = (bot, top], 2 bytes/step, written downward
    nwords=(top-bot)//2 if fe else 128       # non-FE: 0x3cf1 unchanged -> fixed 128-entry table
    offs=[]
    for s in range(nwords):
        a=top-s*2                              # hi @a, lo @a-1
        v=(cpu.m[a]<<8)|cpu.m[a-1]
        offs.append(v-0x10000 if v&0x8000 else v)
    return offs

def longest_monotonic_run(vals):
    """Longest strictly-increasing run (the multi-tap output delay line)."""
    best=(0,0); cur=1
    for i in range(1,len(vals)):
        if vals[i]>vals[i-1]: cur+=1
        else:
            if cur>best[1]: best=(i-cur,cur)
            cur=1
    if cur>best[1]: best=(len(vals)-cur,cur)
    return best  # (start_index, length)

def show_tap_map(recbase):
    from collections import Counter
    print(f"\n=== TAP MAP: record @0x{recbase:04X}  (delay = -offset, samples) ===")
    offs=tap_map(recbase)
    # active program = up to the -1 (0xFFFF) fill region
    fill_start=len(offs)
    run=0
    for i,v in enumerate(offs):
        if v==-1:
            run+=1
            if run>=6: fill_start=i-run+1; break
        else: run=0
    active=offs[:fill_start]
    print(f"  {len(offs)} words; active program ~{fill_start} steps, then -1 (0xFFFF) fill (={128-fill_start} steps)")
    delays=[-v for v in active]
    mags=[abs(d) for d in delays if 16<=abs(d)<0x4000]
    cnt=Counter(mags)
    loop=cnt.most_common(1)[0] if cnt else (0,0)
    pairs=sorted(d for d,c in cnt.items() if c>=2 and d!=loop[0])
    s,ln=longest_monotonic_run([abs(d) for d in delays])
    ramp=[abs(d) for d in delays[s:s+ln]]
    print(f"  delay taps (|offset|16..16383): {len(mags)}  distinct={len(cnt)}  range={min(cnt) if cnt else '-'}..{max(cnt) if cnt else '-'} samp")
    print(f"  recirculating-loop tap (most recurring): {loop[0]} samp x{loop[1]}")
    print(f"  allpass/comb pairs (delay used >=2x, excl loop): {len(pairs)}  -> {pairs[:18]}")
    print(f"  output multi-tap line (longest increasing run @step{s}, len {ln}): {ramp}")

def show_build(recbase, cce=0, ccf=0):
    print(f"\n=== build record @0x{recbase:04X} (cce=0x{cce:02X} ccf=0x{ccf:02X}) ===")
    cpu,fe,ok=build_record(recbase,cce,ccf)
    print(f"  FE-path={fe}  interp_ok={ok}  3ce9={cpu.m[0x3ce9]:02X} 3cea={cpu.m[0x3cea]:02X}")
    print("  --- image @0x3e4e as 4-byte records (lane0:1=offset, delay=-offset) ---")
    recs=decode_image(cpu,0x3e4e,40)
    for s,b,off,delay in recs:
        bs=" ".join("%02X"%x for x in b)
        print(f"   step {s:3d}: {bs}   off={off:+6d} delay={delay:+6d}")
    # offset stats over a wider window
    allrecs=decode_image(cpu,0x3e4e,128)
    delays=[d for _,_,_,d in allrecs if 8<=d<60000]
    print(f"  distinct sane delays(8..60000): {len(set(delays))}  range={min(delays) if delays else '-'}..{max(delays) if delays else '-'}")
    # raw dumps of candidate output buffers
    def hexrow(a,n): return " ".join("%02X"%cpu.m[(a+i)&0xFFFF] for i in range(n))
    print(f"  0x3cf1 ptr now = 0x{cpu.rw(0x3cf1):04X} (B55B wrote offsets from 0x3F4D downward)")
    print("  --- raw 0x3F00-0x3F50 (B55B offset buffer region) ---")
    for r in range(0x3F00,0x3F50,16): print(f"   {r:04X}: {hexrow(r,16)}")
    print("  --- B55B offsets read 0x3F4D DOWNWARD as 16-bit (hi@addr, lo@addr-1) ---")
    line=[]
    for s in range(40):
        a=0x3F4D - s*2
        v=(cpu.m[a]<<8)|cpu.m[a-1]
        sv=v-0x10000 if v&0x8000 else v
        line.append(f"{-sv:+6d}")
        if (s+1)%8==0: print("    "+" ".join(line)); line=[]
    print("  --- raw 0x4000-0x4080 (final ARU image region) ---")
    for r in range(0x4000,0x4080,16): print(f"   {r:04X}: {hexrow(r,16)}")

def test_multiply():
    print("=== emulator self-test: 0x120B shift-add multiply (A*DE -> HL) ===")
    ok=True
    for a,de in [(5,100),(7,1000),(0,1234),(255,255),(13,257)]:
        cpu=new_cpu()
        cpu.A=a; cpu.DE=de
        cpu.call(0x120B)
        exp=(a*de)&0xFFFF
        got=cpu.HL
        flag="OK" if got==exp else "FAIL"
        if got!=exp: ok=False
        print(f"  {a} * {de} = {got} (expect {exp})  {flag}")
    # test 0xB714 : HL = HL - BC
    cpu=new_cpu(); cpu.HL=5000; cpu.BC=1234; cpu.call(0xB714)
    print(f"  0xB714 5000-1234 = {cpu.HL} (expect {5000-1234})  {'OK' if cpu.HL==5000-1234 else 'FAIL'}")
    return ok

def all_records_summary():
    from collections import Counter
    print("\n=== ALL 21 records @0xB800 (stride 0x2AA): structural tap-map summary ===")
    print("  rec  recbase  actSteps  taps  range(samp)   loopTap(xN)   pairs  outLineLen")
    for k in range(21):
        rb=0xB800+k*0x2AA
        offs=tap_map(rb,verbose=False)
        # active = before >=6-long -1 fill
        fs=len(offs); run=0
        for i,v in enumerate(offs):
            if v==-1:
                run+=1
                if run>=6: fs=i-run+1; break
            else: run=0
        active=offs[:fs]
        delays=[abs(v) for v in active if 16<=abs(v)<0x4000]
        cnt=Counter(delays)
        loop=cnt.most_common(1)[0] if cnt else (0,0)
        pairs=sum(1 for d,c in cnt.items() if c>=2 and d!=loop[0])
        s,ln=longest_monotonic_run([abs(v) for v in [(-x) for x in active]])
        rng=f"{min(cnt)}..{max(cnt)}" if cnt else "-"
        print(f"  {k:3d}  0x{rb:04X}   {fs:5d}   {len(cnt):4d}  {rng:>11}   {loop[0]:5d}(x{loop[1]:2d})   {pairs:3d}    {ln:3d}")

def capture_coeffs(recbase):
    """Hook 0xB510 (coeff/offset source fetch) during the interpreter expander to
    capture the raw coefficient source bytes the bytecode references, in order."""
    cpu=new_cpu(); seed_record(cpu,recbase)
    cpu.ww(0x3cf1,0x3f4d)
    try: cpu.call(0xB55B, max_ins=2_000_000)
    except: pass
    fe=cpu.m[(recbase+0x30)&0xFFFF]==0xFE
    fetched=[]
    orig=cpu.step
    def hooked():
        if cpu.PC==0xB510:
            de=cpu.DE; a=(cpu.rw(0x3e05)+de)&0xFFFF
            fetched.append((de,cpu.m[a]))
        orig()
    cpu.step=hooked
    cpu.DE=recbase+(0x44 if fe else 0x35); cpu.HL=0x3e4e; cpu.BC=0x3cf4; cpu.PC=0xAA9F
    n=0
    while cpu.PC!=0xAB39 and n<2_000_000:
        cpu.step(); n+=1
    return fetched

if __name__ == "__main__":
    if not test_multiply():
        print("EMULATOR SELF-TEST FAILED -- aborting build"); sys.exit(1)
    for rb in (0xB800, 0xBAAA, 0xBD54):   # records 0,1,2
        show_tap_map(rb)
    all_records_summary()
    print("\n=== coefficient source bytes referenced by record 0 bytecode (via 0xB510 hook) ===")
    cf=capture_coeffs(0xB800)
    print(f"  {len(cf)} coeff fetches; first 32 (slot_idx, byte, sign-mag decode):")
    for de,b in cf[:32]:
        idx=((de-0x4003)//4)&0xFF
        sign='-' if b&0x80 else '+'; mag=b&0x7F
        print(f"    idx 0x{idx:02X}: 0x{b:02X} = {sign}{mag}/127 = {sign}{mag/127:.3f}")
