#!/usr/bin/env python3
"""F2b foundations (plan 024) — everything needed for the FPC §5.7 per-pin emitter,
derived + validated this session; the emitter itself (766-line owner FPC trace, an
e1c-scale build) is staged for the next session.

ESTABLISHED HERE (all reproduced by this probe):
  1. The diag-6 (FPC SIGNAT) WCS, captured on the verified core via the 0x0330 menu
     table (item 6 -> handler 0x0E84; anchors: item3=0x0CF0, item7=0x0EFD, item8=0x0EF4;
     d1a route, 512/512 prefill agreement) -> wcs_diag.json["sig6"].
  2. The window length RECONCILED: diag-6 extracts as w_reset=31, L=97 -> a 98-step
     frame; SM CLOCK = FPCCLK (FPC U4.5) at one edge per step with START=STOP=RESET
     gives N=98 = sig224's calibration of the manual's +5V reference 96F6.
  3. The bench state: the 0x0D1E pump (block 0x0EEC, same routine as diag-3's 0x0D16
     block with the F6/FA/FE parked-word WA cycle) parks
         R0=0x5555  R1=0xCCCC  R2=0x1999  XREG=0xFAAA   (CPU domain; phys = ~each)
     and the free-run overwrites R3 every step (all rows WA=3).
  4. The steady frame delivers THE FOUR PUMP CONSTANTS to the four D/A channels
     (WR-DA A/B at steps 2/3 from the R0/R1 unity captures; C/D at steps 52/53 from
     the R2/XREG unity captures, half a frame apart) — diag-6 streams known bit
     patterns 5555/CCCC/1999/FAAA into the FPC output section every frame. Derived
     by hand from the complement-domain value law and confirmed on the engine here.
  5. The A/D side: the program has NO RD-AD step; the SM lift (AIN SAR U26.11 -> +5V)
     holds the SAR completion off — the AIN section runs its idle pattern, which the
     FPC table pins (and only they) can adjudicate: the e1c AD_CONST question lands
     here next session.

NEXT SESSION (the emitter): model the FPC board per pin from
`docs/reference/224/224XL FPC pinouts from 060-01320.txt` (owner trace) + fig-3.5/3.6
at fpcCLKA granularity, sampled at FPCCLK edges; stimulus = this frame; score the
FPC table (17 chips) with one global window phase, E1b-style.
"""
import sys, os, json

TOOLS = r"d:\OneDrive\Gray Instruments\iconex\tools"
sys.path.insert(0, TOOLS)
HERE = os.path.dirname(os.path.abspath(__file__))

import sig224
from aru_freerun22_rtl import RTL22, program_rows22, fs22

PUMP = (0x5555, 0xCCCC, 0x1999, 0xFAAA)          # R0, R1, R2, XREG (block 0x0EEC)


def main():
    assert sig224._selftest()
    ref = sig224.value_to_display(sig224.signature_const(98, 1))
    print(f"PREDICTION: diag-6 frame = L+1 steps; FPCCLK 1/step -> N = 98; "
          f"+5V over 98 -> '{ref}' (manual: 96F6)")
    assert ref == "96F6"

    img = bytes.fromhex(json.load(open(os.path.join(HERE, "wcs_diag.json")))["sig6"]["wcs"])
    rows, L, w_reset = program_rows22(
        [(img[4 * k], img[4 * k + 1], img[4 * k + 2], img[4 * k + 3]) for k in range(128)])
    assert (w_reset, L) == (31, 97), (w_reset, L)
    print(f"diag-6: w_reset={w_reset}, L={L} -> {L + 1}-step frame RECONCILED "
          f"(fs would be {fs22(L):.1f} Hz)")

    eng = RTL22()
    eng.R = [(~v) & 0xFFFF for v in PUMP]
    eng.XREG_host = PUMP[3]
    outs = {}
    for n in range(8):
        prev, outs = outs, dict(eng.run_sample(rows, 0))
        if n >= 2:
            assert outs == prev, (n, outs, prev)
    got = {c: outs[c] & 0xFFFF for c in "ABCD"}
    exp = dict(zip("ABCD", PUMP))
    assert got == exp, (got, exp)
    print("steady-frame D/A stream (engine == hand-derived value law):")
    for c, src in zip("ABCD", ("R0", "R1", "R2", "XREG")):
        print(f"  ch{c} = 0x{got[c]:04X}   ({src} pump constant)")
    print("\nFPC-emitter stimulus LOCKED; the per-pin model is staged for next session.")


if __name__ == "__main__":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass
    main()
