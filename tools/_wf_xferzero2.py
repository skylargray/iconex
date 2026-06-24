#!/usr/bin/env python3
"""XFER/ZERO reassignment round 2.

Round 1 findings:
  BASELINE                       +1121 ppm GROW
  A remove first-half ZEROs       +1165 GROW (symmetrize toward 2nd/capture-all)
  B add second-half ZEROs          -112 DECAY but HFD/LOW/MID all DECOUPLED (+0)
  C close XFER s43/95             +1916 GROW
  D/E remove early XFER s38/90    +8258 GROW (early XFER is essential)
  F split blocks                 +2065 GROW
  G                              +3576 GROW

B decays but discards the decay-control accumulation. A captures it but grows.
Oracle wants BOTH: capture HFD/LOW/MID accumulation AND decay AND authority.
So the captured accumulation must be a LOSS, not a gain -> test the SINGLE
clean-block (one ZERO-open + one XFER-close) per half, symmetric, keeping early
XFER, and variants where the close-capture polarity / which step closes differs.
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import aru_datapath as A
from exp_symfix import conv_lambda, coupling, setfields

TARGET = 0.9999899


def show(name, prog, full=False):
    lam = conv_lambda(prog)
    print(f"\n{name}\n  lambda={lam:.7f} ({(lam-1)*1e6:+.0f}ppm) {'GROW' if lam>1 else 'DECAY'}", flush=True)
    if full:
        c = coupling(prog)
        print(f"  coupling: HFD {c['HFD']*1e6:+.0f}  LOW {c['LOW']*1e6:+.0f}  MID {c['MID']*1e6:+.0f}", flush=True)
    return lam


def main():
    prog = A.load_microcode(0x01)
    print(f"target lambda = {TARGET}")
    base = conv_lambda(prog)
    print(f"BASELINE lambda={base:.7f} ({(base-1)*1e6:+.0f}ppm)")

    V = {}

    # H: symmetric capture-all (A) but ALSO remove second-half's role of the s45/97
    #    intra b3-write? No. Instead: A + move close XFER from s46/98 to s44/96
    #    so MID-block closes earlier and XOV is a fresh small block.
    V['H_A_closeXFER_at44_96'] = setfields(prog, {
        44:{'ZERO':0, 'XFER':1}, 96:{'XFER':1},
        46:{'ZERO':0}, 98:{}})

    # I: B (decays) but RE-ENABLE capture of HFD/LOW/MID by adding a close XFER at
    #    s43/95 with ZERO-open kept at s37/89 only. i.e. capture HFD/LOW/PDL block,
    #    then MID/XOV as separate ZERO-cleared block discarded -> does decay persist
    #    while HFD/LOW couple?
    V['I_B_plus_close43_95'] = setfields(prog, {
        43:{'XFER':1}, 95:{'XFER':1},
        96:{'ZERO':1}, 98:{'ZERO':1}})

    # J: single clean block per half KEEPING early XFER: ZERO-open@37/89,
    #    no mid ZEROs, XFER-close@46/98 (symmetric, capture-all). == A essentially
    #    but ensure second half identical: A removed first-half ZEROs; second already
    #    matches. Add: also clear the redundant b3-write at s39/91? keep.
    #    Try instead: open block at s40/92 (start of HFD) with ZERO, close at s46/98.
    V['J_openHFD_s40_92'] = setfields(prog, {
        40:{'ZERO':1}, 92:{'ZERO':1},
        44:{'ZERO':0}, 96:{'ZERO':0},
        46:{'ZERO':0}, 98:{'ZERO':0}})

    # K: B-style decay but only ONE of the two added ZEROs (s98 only) to see which
    #    ZERO drives the decay, then check authority.
    V['K_addZERO_s98_only'] = setfields(prog, {98:{'ZERO':1}})
    V['K2_addZERO_s96_only'] = setfields(prog, {96:{'ZERO':1}})

    # L: B but flip the close XFER coeff sign at s98 (capture with opposite polarity)
    V['L_B_flip_s46_s98'] = setfields(prog, {
        96:{'ZERO':1}, 98:{'ZERO':1, 'coeff':108}, 46:{'coeff':108}})

    # M: capture HFD/LOW/PDL accumulation to RES via close XFER at s43/95, and make
    #    the MID at s44/96 a ZERO-opened fresh accumulation in BOTH halves (symmetric),
    #    closing at s46/98 (symmetric). Two clean blocks per half.
    V['M_two_clean_blocks_sym'] = setfields(prog, {
        43:{'XFER':1}, 95:{'XFER':1},
        44:{'ZERO':1}, 96:{'ZERO':1},
        46:{'ZERO':0}, 98:{'ZERO':0}})  # 46/98 keep their XFER, no mid-ZERO

    lams = {nm: show(nm, p) for nm, p in V.items()}

    print("\n==== COUPLING (lambda<1 or closer than +560ppm) ====")
    for nm, p in V.items():
        if lams[nm] < 1.0 or abs(lams[nm]-1) < abs(base-1)*0.5:
            show(nm, p, full=True)


if __name__ == '__main__':
    main()
