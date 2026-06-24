#!/usr/bin/env python3
"""Round 3: HFD->RA3 + MID s44->RA0 gave lambda=0.9998883 (DECAYS!).
Pin it down: coupling, isolate which change matters, try MID RA0 alone,
try MID->other regs, and refine toward target 0.9999899.
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import aru_datapath as A
from exp_symfix import conv_lambda, coupling, setfields

TARGET = 0.9999899
prog = A.load_microcode(0x01)
MIR = {40:92,41:93,43:95,44:96,45:97,46:98}
def mir(e):
    f={}
    for s,x in e.items():
        f[s]=dict(x)
        if s in MIR: f[MIR[s]]=dict(x)
    return f

HFD_RA3 = {40:{'b5':1,'b4':1},41:{'b5':1,'b4':1}}
def merge(*ds):
    out={}
    for d in ds:
        for k,v in d.items(): out.setdefault(k,{}).update(v)
    return out

VARIANTS = {
 "W: HFD RA3 + MID s44 RA0":        merge(HFD_RA3, {44:{'b5':0,'b4':0}}),
 "X: MID s44 RA0 ONLY (no HFD)":    {44:{'b5':0,'b4':0}},
 "Y: MID s44 RA1":                  merge(HFD_RA3, {44:{'b5':0,'b4':1}}),
 "Z: MID s44 RA2":                  merge(HFD_RA3, {44:{'b5':1,'b4':0}}),
 "AA: HFD RA3 + MID RA0 + LOW RA3": merge(HFD_RA3, {44:{'b5':0,'b4':0},43:{'b5':1,'b4':1}}),
 "BB: HFD RA3 + MID RA0, only s40": merge({40:{'b5':1,'b4':1}}, {44:{'b5':0,'b4':0}}),
 "CC: HFD RA3 + MID RA0, only s41": merge({41:{'b5':1,'b4':1}}, {44:{'b5':0,'b4':0}}),
}

def main():
    base = conv_lambda(prog)
    print(f"BASE = {base:.7f} ({(base-1)*1e6:+.0f} ppm)  TARGET {TARGET}")
    res=[]
    for n,e in VARIANTS.items():
        v=setfields(prog,mir(e)); lam=conv_lambda(v)
        print(f"{n:34s} lambda={lam:.7f} ({(lam-1)*1e6:+.0f} ppm) {'DECAY' if lam<1 else 'grow'}")
        res.append((n,e,lam))
    print("\n--- coupling for DECAY or near-target variants ---")
    for n,e,lam in res:
        if lam<1.00005:
            v=setfields(prog,mir(e)); c=coupling(v)
            print(f"{n}: base={c['base']:.7f} HFD{c['HFD']*1e6:+.0f} LOW{c['LOW']*1e6:+.0f} MID{c['MID']*1e6:+.0f}")

if __name__=='__main__': main()
