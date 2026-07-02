#!/usr/bin/env python3
"""E3e — dataflow microscope: CONCERT frame-by-frame with full probes (csinv=1).

Frame 0 gets the impulse (16422). Print every step of frame 0; for frames 1-4 print only
rows with significant values. Track where the input value flows: DAB, regfile, ACC, RES,
DM writes."""
import sys, os, json
TOOLS = r"d:\OneDrive\Gray Instruments\iconex\tools"
sys.path.insert(0, TOOLS)
SCRATCH = os.path.dirname(os.path.abspath(__file__))

from aru_freerun22 import FreeRun22, program_from_wcs, decode22

cache = json.load(open(os.path.join(SCRATCH, "wcs_cache.json")))
b = bytes.fromhex(cache["1"]["wcs"])
wcs = [(b[4*k], b[4*k+1], b[4*k+2], b[4*k+3]) for k in range(128)]
prog, L, w_reset = program_from_wcs(wcs)

CLS = {0: "MEMR", 1: "MEMW", 2: "IO  ", 3: "idle"}
eng = FreeRun22(csign_invert=True)

def s(v):
    v &= 0xFFFF
    return v - 0x10000 if v & 0x8000 else v

for frame in range(5):
    probe = []
    x = 16422 if frame == 0 else 0
    eng.run_sample(prog, x & 0xFFFF, probe=probe)
    print(f"\n===== frame {frame} (input={x}) =====")
    for ei, p in enumerate(probe):
        d = p["d"]
        interesting = (abs(s(p["dab"])) > 8 or abs(p["opnd"]) > 8 or abs(p["ACC"]) > 64
                       or abs(p["RES"]) > 8 or p["out_da"])
        if frame == 0 or interesting:
            w = 127 - ei
            extra = ""
            if d["typ"] == 2:
                extra = f" sel={d['sel']} wrda={int(d.get('WRDA', 0))}ch={''.join(d.get('chans', []))}" \
                        f"{' RESET' if d.get('RESET') else ''}"
            memw = f" DM[{p['addr']:5d}]<-{s(p['dab']):6d}" if d["typ"] == 1 else ""
            out = f" OUT{p['out_da']}" if p["out_da"] else ""
            print(f" e{ei:3d} w{w:3d} {CLS[d['typ']]} of={d['ofst']:5d} wa{d['WA']} ra{d['RA']} "
                  f"cm{d['cmag']:2d} cs{d['CSIGN']} x{d['XFER']}z{d['ZERO']} | "
                  f"DAB={s(p['dab']):6d} op={p['opnd']:6d} ACC={p['ACC']:7d} RES={p['RES']:6d}"
                  f"{memw}{extra}{out}")
    print(f"  end-of-frame: R={eng.R} RES={eng.RES} ACC={eng.ACC} "
          f"DM cells>8: {sum(1 for v in eng.DM.values() if abs(s(v)) > 8)}")
