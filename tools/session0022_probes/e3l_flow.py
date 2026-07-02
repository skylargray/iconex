#!/usr/bin/env python3
"""E3l — signal-flow tracer: log every significant MAC product with operand provenance
(which register, loaded at which exec step from which source), plus every significant DM
write/read and D/A out. csinv=1 baseline. Impulse at frame 0; trace frames 0-2 and then
sampled frames to see the long-hop structure."""
import sys, os, json
TOOLS = r"d:\OneDrive\Gray Instruments\iconex\tools"
sys.path.insert(0, TOOLS)
SCRATCH = os.path.dirname(os.path.abspath(__file__))

from aru_freerun22 import program_from_wcs, decode22, SRC_RDRREG, SRC_RDAD, SRC_XREG
from aru_freerun import product20, res_from_acc
from aru_rtl_dp import s16, sat20

cache = json.load(open(os.path.join(SCRATCH, "wcs_cache.json")))
b = bytes.fromhex(cache["1"]["wcs"])
wcs = [(b[4*k], b[4*k+1], b[4*k+2], b[4*k+3]) for k in range(128)]
prog, L, w_reset = program_from_wcs(wcs)
DEC = [decode22(*w) for w in prog]
TH = 40                                     # significance threshold

R = [0]*4
RSRC = ["init"]*4                           # provenance of each register value
ACC = 0; RES = 0; RESSRC = "init"; DAB = 0; DABSRC = "init"
DM = {}; DMSRC = {}
CPC = 0
vq = []                                     # (product, srcdesc)
xq = []

def frame(n, x, log):
    global ACC, RES, RESSRC, DAB, DABSRC, CPC
    for i, d in enumerate(DEC):
        w = 127 - i
        if vq:
            V, vsrc = vq.pop(0)
            ACC = sat20(ACC + V)
            if abs(V) > TH*8 and log:
                print(f"  f{n} e{i:3d}w{w:3d}: ACC += {V//8:6d}  [{vsrc}] -> ACC={ACC//8}")
        if xq:
            xf, zr = xq.pop(0)
            if xf:
                RES = res_from_acc(ACC); RESSRC = f"XFERcap@f{n}e{i}"
                if abs(RES) > TH and log:
                    print(f"  f{n} e{i:3d}w{w:3d}: RES <= {RES:6d}")
            if zr: ACC = 0
        opnd, osrc = R[d["RA"]], RSRC[d["RA"]]
        typ = d["typ"]; addr = (CPC - d["ofst"]) & 0xFFFF
        if typ == 0:
            DAB = DM.get(addr, 0) & 0xFFFF; DABSRC = DMSRC.get(addr, "dm0")
            if abs(s16(DAB)) > TH and log:
                print(f"  f{n} e{i:3d}w{w:3d}: MEMR of={d['ofst']:5d} -> {s16(DAB):6d}  [{DABSRC}]")
        elif typ == 1:
            DAB = RES & 0xFFFF; DABSRC = RESSRC
        elif typ == 2:
            sel = d["sel"]
            if sel == SRC_RDRREG: DAB = RES & 0xFFFF; DABSRC = RESSRC
            elif sel == SRC_RDAD: DAB = x & 0xFFFF; DABSRC = f"INPUT@f{n}"
            elif sel == SRC_XREG: DAB = 0; DABSRC = "xreg0"
        R[d["WA"]] = s16(DAB); RSRC[d["WA"]] = f"{DABSRC}>R{d['WA']}@e{i}"
        if typ == 1:
            DM[addr] = DAB & 0xFFFF; DMSRC[addr] = f"w{w}@f{n}({DABSRC})"
            if abs(s16(DAB)) > TH and log:
                print(f"  f{n} e{i:3d}w{w:3d}: MEMW of={d['ofst']:5d} <= {s16(DAB):6d}  [{DABSRC}]")
        if typ == 2 and d.get("WRDA") and abs(s16(DAB)) > TH and log:
            print(f"  f{n} e{i:3d}w{w:3d}: OUT {''.join(d['chans'])} = {s16(DAB):6d}  [{DABSRC}]")
        cs = d["CSIGN"] ^ 1                                   # csinv=1
        V = product20(opnd, d["cmag"], cs)
        vq.append((V, f"R{d['RA']}({osrc})x{'-' if not cs else ''}{d['cmag']}/32" if abs(V) > TH*8 else ""))
        xq.append((d["XFER"], d["ZERO"]))
    CPC = (CPC + 1) & 0xFFFF

for n in range(3):
    print(f"\n===== frame {n} =====")
    frame(n, 16422 if n == 0 else 0, log=True)
# run silently to selected checkpoints, then log one frame
mark = {610: "f610-612 (post first mid-hop ~612)", 1940: "f1940-1942 (~2k hop)", 16990: "f16990-92 (0.52s hop)"}
n = 3
for stop in (610, 1940, 16990):
    while n < stop:
        frame(n, 0, log=False); n += 1
    print(f"\n===== {mark[stop]} =====")
    for _ in range(3):
        frame(n, 0, log=True); n += 1
