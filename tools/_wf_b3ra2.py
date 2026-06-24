#!/usr/bin/env python3
"""Round 2: HFD reading RA3 gave authority (+451) and improved lambda. Explore:
 - sign flips on HFD/LOW coeffs (energy-adding -> loss)
 - combine HFD-RA3 with LOW-RA3 and with b3 writeback
 - check both halves symmetric
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import aru_datapath as A
from exp_symfix import conv_lambda, coupling, setfields

TARGET = 0.9999899
prog = A.load_microcode(0x01)
base = None

MIR = {40:92, 41:93, 43:95}
def mir(edits):
    full = {}
    for s, e in edits.items():
        full[s] = dict(e);
        if s in MIR: full[MIR[s]] = dict(e)
    return full

# current coeffs: s40 -39, s41 -84, s43 -107 (already negative)
VARIANTS = {
    "A: HFD RA3 (repro v5)":              {40:{'b5':1,'b4':1}, 41:{'b5':1,'b4':1}},
    "B: HFD RA3 + sign-flip coeff":       {40:{'b5':1,'b4':1,'coeff':39}, 41:{'b5':1,'b4':1,'coeff':84}},
    "C: HFD RA3 + LOW RA3":               {40:{'b5':1,'b4':1}, 41:{'b5':1,'b4':1}, 43:{'b5':1,'b4':1}},
    "D: HFD RA3 + LOW RA3 + LOW sign":    {40:{'b5':1,'b4':1}, 41:{'b5':1,'b4':1}, 43:{'b5':1,'b4':1,'coeff':107}},
    "E: HFD RA3 + b3 writeback":          {40:{'b5':1,'b4':1,'b3':1}, 41:{'b5':1,'b4':1,'b3':1}},
    "F: only s40 RA3 (not 41)":           {40:{'b5':1,'b4':1}},
    "G: only s41 RA3 (not 40)":           {41:{'b5':1,'b4':1}},
    "H: HFD RA3 + flip only s41":         {40:{'b5':1,'b4':1}, 41:{'b5':1,'b4':1,'coeff':84}},
    "I: HFD RA3 + flip only s40":         {40:{'b5':1,'b4':1,'coeff':39}, 41:{'b5':1,'b4':1}},
}

def main():
    global base
    base = conv_lambda(prog)
    print(f"BASE = {base:.7f} ({(base-1)*1e6:+.0f} ppm)")
    res = []
    for name, e in VARIANTS.items():
        v = setfields(prog, mir(e))
        lam = conv_lambda(v)
        print(f"{name:34s} lambda={lam:.7f} ({(lam-1)*1e6:+.0f} ppm) {'DECAY' if lam<1 else 'grow'}")
        res.append((name,e,lam))
    print("\n--- coupling for lambda<base-1e-4 or <1 ---")
    for name,e,lam in res:
        if lam<1 or lam<base-1e-4:
            v=setfields(prog,mir(e)); c=coupling(v)
            print(f"{name}: base={c['base']:.7f} HFD{c['HFD']*1e6:+.0f} LOW{c['LOW']*1e6:+.0f} MID{c['MID']*1e6:+.0f}")

if __name__=='__main__': main()
