#!/usr/bin/env python3
"""Workflow scratch: b3 (write-back) and RA (read-register) hypothesis on band-split.

Inert steps HFD s40,41 / LOW s43 read RA0 and have b3=0. Coupled steps read RA2/RA3.
Test: give HFD/LOW b3=1 to close the loop; change their RA to read live feedback reg;
reassign closers; mirror every change in the second half (92,93 / 95).
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import aru_datapath as A
from exp_symfix import conv_lambda, coupling, setfields

TARGET = 0.9999899
prog = A.load_microcode(0x01)

# Mirror map first-half -> second-half
MIR = {40:92, 41:93, 43:95}

def mir_edits(edits):
    """Given first-half edits, produce full edits dict mirrored to second half."""
    full = {}
    for s, e in edits.items():
        full[s] = dict(e)
        if s in MIR:
            full[MIR[s]] = dict(e)
    return full

VARIANTS = {
    # 1: HFD steps write back (b3=1). Reading addr they currently target.
    "1: HFD s40,41 b3->1":            {40:{'b3':1}, 41:{'b3':1}},
    # 2: LOW step writes back
    "2: LOW s43 b3->1":               {43:{'b3':1}},
    # 3: HFD+LOW all write back
    "3: HFD+LOW b3->1":               {40:{'b3':1}, 41:{'b3':1}, 43:{'b3':1}},
    # 4: HFD read live fb reg RA2 (instead of RA0)
    "4: HFD RA0->RA2 (b5=1,b4=0)":    {40:{'b5':1,'b4':0}, 41:{'b5':1,'b4':0}},
    # 5: HFD read RA3
    "5: HFD RA0->RA3 (b5=1,b4=1)":    {40:{'b5':1,'b4':1}, 41:{'b5':1,'b4':1}},
    # 6: LOW read RA2
    "6: LOW RA0->RA2":                {43:{'b5':1,'b4':0}},
    # 7: LOW read RA3
    "7: LOW RA0->RA3":                {43:{'b5':1,'b4':1}},
    # 8: HFD b3=1 AND read RA2 (close loop reading live fb)
    "8: HFD b3->1 + RA2":             {40:{'b3':1,'b5':1,'b4':0}, 41:{'b3':1,'b5':1,'b4':0}},
    # 9: LOW b3=1 + RA2
    "9: LOW b3->1 + RA2":             {43:{'b3':1,'b5':1,'b4':0}},
    # 10: HFD+LOW b3=1 + RA2
    "10: HFD+LOW b3->1 + RA2":        {40:{'b3':1,'b5':1,'b4':0}, 41:{'b3':1,'b5':1,'b4':0}, 43:{'b3':1,'b5':1,'b4':0}},
}

def main():
    base = conv_lambda(prog)
    print(f"BASE lambda = {base:.7f}  ({(base-1)*1e6:+.0f} ppm)  target {TARGET}")
    results = []
    for name, e in VARIANTS.items():
        v = setfields(prog, mir_edits(e))
        lam = conv_lambda(v)
        flag = 'DECAY' if lam < 1 else 'grow'
        improved = lam < base - 1e-6
        print(f"{name:34s} lambda={lam:.7f} ({(lam-1)*1e6:+.0f} ppm) {flag} {'<--IMPROVED' if improved else ''}")
        results.append((name, e, lam, improved))
    # coupling for the most promising (lambda<1 or much closer)
    print("\n--- coupling for promising variants ---")
    for name, e, lam, improved in results:
        if lam < 1 or lam < base - 1e-4:
            v = setfields(prog, mir_edits(e))
            c = coupling(v)
            print(f"{name}: base={c['base']:.7f} HFD{c['HFD']*1e6:+.0f} LOW{c['LOW']*1e6:+.0f} MID{c['MID']*1e6:+.0f}")

if __name__ == '__main__':
    main()
