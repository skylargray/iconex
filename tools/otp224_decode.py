#!/usr/bin/env python3
"""Decode the ORIGINAL 224 static ARU microcode (the OTP mask-ROM set), PCM60-style.

The 4 OTP ROMs (2 KB each) are parallel byte-lanes of one microword (like the PCM60's
U32/U35/U38/U43):
  OTP4 (3500401860_4) = control/opcode   (low-nibble alphabet n7>>n3/nF>n0 = family opcodes)
  OTP3 (3500401860_3) = offset HIGH       (FC/FB/FE sign-extended negatives)
  OTP1 (3500401660_1) = offset LOW        (sparse)
  OTP2 (3500401760_2) = coefficient/curve (smooth descending ramps; autocorr period ~96-100)
Program length ~100 steps (OTP2 autocorr peak @96-100; roadmap: 224 = 100 steps).
"""
import os, sys
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

DIR=os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),"ROMs","Lexicon 224","OTP")
L={"ctrl":"3500401860_4.BIN","offhi":"3500401860_3.BIN","offlo":"3500401660_1.BIN","coeff":"3500401760_2.BIN"}
R={k:np.fromfile(os.path.join(DIR,fn),dtype=np.uint8) for k,fn in L.items()}

def decode_frame(start, n):
    steps=[]
    for s in range(n):
        i=start+s
        hi=int(R["offhi"][i]); lo=int(R["offlo"][i])
        raw=(hi<<8)|lo; off=raw-0x10000 if raw&0x8000 else raw
        ctrl=int(R["ctrl"][i]); coeff=int(R["coeff"][i])
        steps.append(dict(step=s,off=off,delay=-off,coeff=coeff,coeff_f=coeff/256.0,
                          ctrl=ctrl,op=ctrl&0x0F,rw=("R" if off<0 else "W" if off>0 else "Z")))
    return steps

def tap_summary(steps):
    reads=[s for s in steps if s["rw"]=="R"]
    taps=sorted({s["delay"] for s in reads if s["delay"]>=8})
    return len(reads), len(taps), (taps[0] if taps else 0, taps[-1] if taps else 0)

def main():
    print("OTP ROM sizes:", {k:len(v) for k,v in R.items()})
    for F in (96,100,128):
        print(f"\n=== frame size {F}: per-frame tap sanity over {2048//F} frames ===")
        for fr in range(min(8,2048//F)):
            steps=decode_frame(fr*F,F)
            nr,nt,rng=tap_summary(steps)
            print(f"  frame {fr} @0x{fr*F:04X}: reads={nr} taps={nt} range={rng[0]}..{rng[1]}")
    # detailed dump of frame 0 at F=100
    print("\n=== frame 0 (F=100) first 32 steps ===")
    print("step  off    delay   coeff      ctrl op rw")
    for s in decode_frame(0,32):
        print(f"{s['step']:3d} {s['off']:6d} {s['delay']:6d}  0x{s['coeff']:02X}={s['coeff_f']:+.3f}  0x{s['ctrl']:02X} {s['op']:X}  {s['rw']}")

if __name__=="__main__":
    main()
