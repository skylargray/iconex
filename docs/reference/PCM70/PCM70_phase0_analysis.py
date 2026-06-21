import numpy as np, sys, math, re

files = ["Lexicon_PCM-70-V2_0-U62.BIN","Lexicon_PCM-70-V2_0-U67.BIN","Lexicon_PCM-70-V2_0-U95.BIN"]

def shannon(b):
    if len(b)==0: return 0.0
    cnt=np.bincount(b,minlength=256).astype(float)
    p=cnt/cnt.sum(); p=p[p>0]
    return float(-(p*np.log2(p)).sum())

def autocorr_strides(b, strides):
    # normalized match rate at each candidate period
    out={}
    for s in strides:
        if s>=len(b): continue
        a=b[:-s]; c=b[s:]
        out[s]=float((a==c).mean())
    return out

for f in files:
    raw=np.fromfile(f,dtype=np.uint8)
    b=raw
    n=len(b)
    print("="*72)
    print(f"{f}  ({n} bytes = {n//1024}KB)")
    H=shannon(b)
    print(f"  entropy: {H:.3f} bits/byte  (8.0=random, ~4-6=code, low=structured/sparse)")
    # fill / blank analysis
    ff=(b==0xFF).sum(); zz=(b==0x00).sum()
    print(f"  0xFF: {ff} ({100*ff/n:.1f}%)   0x00: {zz} ({100*zz/n:.1f}%)")
    # top bytes
    hist=np.bincount(b,minlength=256)
    top=np.argsort(hist)[::-1][:8]
    print("  top bytes: " + ", ".join(f"{v:02X}:{hist[v]}" for v in top))
    # ASCII contamination: runs of printable ASCII >= 8 chars
    printable=((b>=0x20)&(b<0x7F))|(b==0x0A)|(b==0x0D)|(b==0x09)
    # find longest printable run
    runs=[]; cur=0
    for p in printable:
        if p: cur+=1
        else:
            if cur>0: runs.append(cur); cur=0
    if cur>0: runs.append(cur)
    longest=max(runs) if runs else 0
    pct_print=100*printable.sum()/n
    print(f"  printable ASCII: {pct_print:.1f}%   longest run: {longest} chars")
    # Z80 RST vector check: look at bytes 0x00,0x08,0x10,...,0x38 and entry region
    print(f"  first 16 bytes: " + " ".join(f"{x:02X}" for x in b[:16]))
    # Z80 opcode-ish density: count common Z80 opcodes
    # 0xC3=JP, 0xCD=CALL, 0xC9=RET, 0x21=LD HL, 0x3E=LD A, 0xCB/0xDD/0xED/0xFD prefixes, 0x18=JR, 0x20/28/30/38=JR cc
    z80ops={0xC3:'JP',0xCD:'CALL',0xC9:'RET',0x18:'JR',0x21:'LD HL,nn',0x3E:'LD A,n',0xCB:'CBpfx',0xED:'EDpfx',0xDD:'DDpfx',0xFD:'FDpfx',0x00:'NOP',0x76:'HALT',0xF3:'DI',0xFB:'EI'}
    print("  Z80 opcode counts: " + ", ".join(f"{nm}({op:02X}):{int((b==op).sum())}" for op,nm in z80ops.items()))
import numpy as np, re
files = ["Lexicon_PCM-70-V2_0-U62.BIN","Lexicon_PCM-70-V2_0-U67.BIN","Lexicon_PCM-70-V2_0-U95.BIN"]
def extract(b, minlen=4):
    out=[]; cur=bytearray(); start=0
    for i,x in enumerate(b):
        if 0x20<=x<0x7F:
            if not cur: start=i
            cur.append(x)
        else:
            if len(cur)>=minlen: out.append((start,cur.decode('ascii',errors='replace')))
            cur=bytearray()
    if len(cur)>=minlen: out.append((start,cur.decode('ascii')))
    return out
for f in files:
    b=np.fromfile(f,dtype=np.uint8)
    s=extract(b,4)
    print("="*72); print(f"{f}: {len(s)} strings(>=4)")
    # contamination signature: Intel HEX records start with ':' followed by hex
    hexrec=[t for t in s if re.match(r':[0-9A-Fa-f]{6,}',t[1])]
    print(f"  Intel-HEX-record-looking strings: {len(hexrec)}  <-- contamination flag if >0")
    if hexrec[:3]:
        for off,t in hexrec[:3]: print(f"    @{off:04X}: {t[:50]}")
    # show first 40 interesting strings
    shown=0
    for off,t in s:
        if len(t)>=5:
            print(f"  @{off:04X}: {t}")
            shown+=1
        if shown>=40: break
import numpy as np
files = ["Lexicon_PCM-70-V2_0-U62.BIN","Lexicon_PCM-70-V2_0-U67.BIN","Lexicon_PCM-70-V2_0-U95.BIN"]
for f in files:
    b=np.fromfile(f,dtype=np.uint8); n=len(b)
    print(f"{f} ({n}B):")
    # mirror/alias check: compare each half-split for equality (address-line dump errors)
    for div in [2,4]:
        seg=n//div
        segs=[b[i*seg:(i+1)*seg] for i in range(div)]
        eqs=[bool(np.array_equal(segs[0],segs[k])) for k in range(1,div)]
        match0=[float((segs[0]==segs[k]).mean()) for k in range(1,div)]
        print(f"   split/{div}: seg0==segk exact={eqs}  bytewise-match-rate={['%.3f'%m for m in match0]}")
    # check stuck high address bit: is upper half all-FF (unprogrammed)? 
    half=n//2
    up_ff=float((b[half:]==0xFF).mean()); lo_ff=float((b[:half]==0xFF).mean())
    print(f"   lower-half %FF={lo_ff:.3f}  upper-half %FF={up_ff:.3f}")
import numpy as np
files = ["Lexicon_PCM-70-V2_0-U62.BIN","Lexicon_PCM-70-V2_0-U67.BIN","Lexicon_PCM-70-V2_0-U95.BIN"]
def smooth_runs(b, max_step=4, min_len=16):
    # runs where |consecutive diff| <= max_step (as signed bytes) -> candidate sine/exp/LFO tables
    d=np.abs(np.diff(b.astype(np.int16)))
    smooth = d<=max_step
    runs=[]; cur=0; start=0
    for i,s in enumerate(smooth):
        if s:
            if cur==0: start=i
            cur+=1
        else:
            if cur>=min_len: runs.append((start,start+cur))
            cur=0
    if cur>=min_len: runs.append((start,start+cur))
    return runs
for f in files:
    b=np.fromfile(f,dtype=np.uint8)
    runs=smooth_runs(b)
    # filter out all-same (FF/00 fills) -> require some variation
    interesting=[(s,e) for s,e in runs if b[s:e].std()>3]
    print(f"=== {f}: {len(interesting)} smooth varying runs (len>=16) ===")
    for s,e in interesting[:12]:
        seg=b[s:e]
        print(f"   0x{s:04X}-0x{e:04X} (len {e-s}): min={seg.min()} max={seg.max()} "
              f"vals=[{' '.join('%02X'%x for x in seg[:14])}{'...' if e-s>14 else ''}]")
import numpy as np
b=np.fromfile("Lexicon_PCM-70-V2_0-U67.BIN",dtype=np.uint8)
act=b[:0x400]  # 1KB active
# treat FF as "padding"; autocorr on non-padding match
def matchrate(a,s):
    if s>=len(a): return 0
    x=a[:-s]; y=a[s:]
    # only count positions where neither is FF
    m=(x!=0xFF)&(y!=0xFF)
    if m.sum()<20: return 0
    return float((x[m]==y[m]).mean())
print("stride : non-FF match-rate (looking for the step/plane period)")
for s in [16,32,48,64,80,96,100,128,160,192,200,256,320,384,512]:
    print(f"  {s:4d} : {matchrate(act,s):.3f}")
# Also: where does the active 1KB split into planes? show block density per 128-byte page
print("\n128-byte page populated counts:")
for p in range(8):
    seg=b[p*128:(p+1)*128]
    print(f"  page {p} (0x{p*128:03X}): {int((seg!=0xFF).sum())} non-FF")
