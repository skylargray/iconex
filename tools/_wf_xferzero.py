#!/usr/bin/env python3
"""XFER/ZERO reassignment hypothesis for the CONCERT band-split region.

Band-split steps (first half | mirror), current decode:
  s37|89 ZERO-open read RA3 c-79   (WA2)
  s38|90 XFER+b3write RA2 c-16      (WA2)
  s39|91 b3write RA2 c-78           (WA3)
  s40|92 HFD read RA0 c-39          (WA1)
  s41|93 HFD read RA0 c-84          (WA3)
  s42|94 PDL read RA0 c-123         (WA3)
  s43|95 LOW read RA0 c-107         (WA2)
  s44|96 MID RA3 c-80  [ZERO=1 first vs 0 second]  (WA1)
  s45|97 XOV RA2 b3write c-15       (WA3)
  s46|98 XOV RA3 XFER+b3write c-108 [ZERO=1 first vs 0 second]  (WA3)

Goal: ZERO/XFER layout where loop DECAYS and HFD/LOW/MID all gain authority,
symmetric across halves.
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import aru_datapath as A
from exp_symfix import conv_lambda, coupling, setfields, clone

TARGET = 0.9999899


def show(name, prog, full=False):
    lam = conv_lambda(prog)
    grow = 'GROW' if lam > 1 else 'DECAY'
    print(f"\n{name}\n  lambda={lam:.7f} ({(lam-1)*1e6:+.0f}ppm) {grow}", flush=True)
    if full:
        c = coupling(prog)
        print(f"  coupling: HFD {c['HFD']*1e6:+.0f}  LOW {c['LOW']*1e6:+.0f}  MID {c['MID']*1e6:+.0f}", flush=True)
    return lam


def main():
    prog = A.load_microcode(0x01)
    print(f"target lambda = {TARGET}")
    base = show("BASELINE", prog)

    variants = {}

    # ----- Symmetrize toward SECOND half (remove first-half extra ZEROs) -----
    # (this is exp_symfix V2 but recorded here for the sweep)
    variants['A_sym2nd_noZERO_s44_s46'] = setfields(prog, {44:{'ZERO':0}, 46:{'ZERO':0}})

    # ----- Symmetrize toward FIRST half (add ZEROs to second) -----
    variants['B_sym1st_addZERO_s96_s98'] = setfields(prog, {96:{'ZERO':1}, 98:{'ZERO':1}})

    # ----- Capture HFD+LOW+PDL: add an XFER (close) at s43/s95 (end of HFD/LOW/PDL accum) -----
    # so the HFD+LOW accumulation is transferred to RES before MID/XOV block.
    variants['C_XFER_close_s43_s95'] = setfields(prog, {43:{'XFER':1}, 95:{'XFER':1}})

    # ----- Remove the early XFER@s38/s90 (so accumulation is not prematurely captured) -----
    variants['D_noXFER_s38_s90'] = setfields(prog, {38:{'XFER':0}, 90:{'XFER':0}})

    # ----- Clean MAC block: single ZERO-open at s37/s89, single XFER-close at s46/s98 -----
    # remove early XFER@s38/90, remove mid ZEROs@s44/46, keep open@37/89 & close@46/98.
    variants['E_clean_block'] = setfields(prog, {
        38:{'XFER':0}, 90:{'XFER':0},
        44:{'ZERO':0}, 46:{'ZERO':0},
    })
    # second half already has no mid ZEROs; only needs early XFER removed -> symmetric
    # (E applies symmetric edits: both halves end with ZERO-open@open, XFER-close@close)

    # ----- E + also drop the b3 short-feedback writes inside the block (s39/91, s45/97) off? no.

    # ----- F: clean block but move the close XFER to s43/95 (capture HFD/LOW/PDL only;
    #          let MID/XOV be a fresh block opened by ZERO@s44/96) -----
    variants['F_split_blocks'] = setfields(prog, {
        38:{'XFER':0}, 90:{'XFER':0},          # drop early xfer
        43:{'XFER':1}, 95:{'XFER':1},          # close HFD/LOW/PDL block
        44:{'ZERO':1}, 96:{'ZERO':1},          # open MID/XOV block (symmetric)
        46:{'XFER':1}, 98:{'XFER':1},          # close MID/XOV block (already xfer)
    })

    # ----- G: symmetric clean + ZERO open also at s44/96 (re-open before MID) but keep
    #          single early-removed; basically E with MID block re-opened -----
    variants['G_E_plus_MIDopen'] = setfields(prog, {
        38:{'XFER':0}, 90:{'XFER':0},
        44:{'ZERO':1}, 96:{'ZERO':1},
        46:{'XFER':1}, 98:{'XFER':1},
    })

    # First pass: lambda only
    lams = {}
    for nm, p in variants.items():
        lams[nm] = show(nm, p)

    # Coupling only for variants that decay or much closer to target
    print("\n==== COUPLING for promising variants (lambda<1 or closer than +1121ppm) ====")
    for nm, p in variants.items():
        lam = lams[nm]
        if lam < 1.0 or abs(lam-1) < abs(base-1)*0.5:
            show(nm, p, full=True)


if __name__ == '__main__':
    main()
