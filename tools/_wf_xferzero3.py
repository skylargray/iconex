#!/usr/bin/env python3
"""XFER/ZERO round 3 — build on J (the ONLY capturing variant with authority).

Round 2 key results:
  J_openHFD_s40_92   +556 ppm GROW  coupling HFD -92  LOW -77  MID -668  (ALL couple!)
  K_addZERO_s98_only -112 DECAY  but HFD/LOW/MID all +0 (decoupled; captures only XOV)
  All decay variants decay by NOT capturing the accumulation -> kill authority.

J = ZERO-open at s40/92 (start of HFD), no ZEROs at 44/96 or 46/98, XFER-close at
46/98 (capture-all from HFD onward). This HALVES the error AND gives all three
decay controls loop authority. The remaining +556 ppm net-gain must be removed
WITHOUT discarding the accumulation. Test:
  - J + remove early XFER s38/90 (the s37-39 sub-block then feeds the same RES?)
  - J + open at s40/92 but ALSO clear the s37 open ZERO (single open per half)
  - J with close moved to s45/97 vs s46/98
  - J + flip close coeff sign
  - J applied only to make halves symmetric (second half open at s92)
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import aru_datapath as A
from exp_symfix import conv_lambda, coupling, setfields

TARGET = 0.9999899


def show(name, prog, full=True):
    lam = conv_lambda(prog)
    print(f"\n{name}\n  lambda={lam:.7f} ({(lam-1)*1e6:+.0f}ppm) {'GROW' if lam>1 else 'DECAY'}", flush=True)
    if full:
        c = coupling(prog)
        print(f"  coupling: HFD {c['HFD']*1e6:+.0f}  LOW {c['LOW']*1e6:+.0f}  MID {c['MID']*1e6:+.0f}", flush=True)
    return lam


J = {40:{'ZERO':1}, 92:{'ZERO':1}, 44:{'ZERO':0}, 96:{'ZERO':0}, 46:{'ZERO':0}, 98:{'ZERO':0}}


def merge(*ds):
    out = {}
    for d in ds:
        for k, v in d.items():
            out.setdefault(k, {}).update(v)
    return out


def main():
    prog = A.load_microcode(0x01)
    print(f"target lambda = {TARGET}")
    base = conv_lambda(prog)
    print(f"BASELINE lambda={base:.7f} ({(base-1)*1e6:+.0f}ppm)")

    V = {}
    # N: J + remove early XFER (s38/90) so s37-39 accumulate into the SAME block
    V['N_J_noEarlyXFER'] = merge(J, {38:{'XFER':0}, 90:{'XFER':0}})

    # O: J but open at s37/89 instead (include s37-39 in captured block); i.e. just
    #    remove mid/close ZEROs, keep original open at 37, remove early XFER so it's
    #    one block 37..46.
    V['O_open37_noEarlyXFER'] = merge({38:{'XFER':0},90:{'XFER':0},
        44:{'ZERO':0},96:{'ZERO':0},46:{'ZERO':0},98:{'ZERO':0}})

    # P: J + close at s45/97 (capture HFD..MID, drop XOV s46/98 from RES)
    V['P_J_close45_97'] = merge(J, {45:{'XFER':1}, 97:{'XFER':1},
        46:{'XFER':0,'ZERO':0}, 98:{'XFER':0,'ZERO':0}})

    # Q: J + flip the close-XFER coeff sign at s46/98
    V['Q_J_flipClose'] = merge(J, {46:{'coeff':108}, 98:{'coeff':108}})

    # R: J + flip XOV pair s45/97 sign (XOV had +802 ppm coupling = energy adding)
    V['R_J_flipXOV'] = merge(J, {45:{'coeff':15}, 97:{'coeff':15},
        46:{'coeff':108}, 98:{'coeff':108}})

    # S: J but open block at s40/92 AND drop the s37 open-ZERO (keep s37 accumulating
    #    onto whatever prior RES) -> remove 37/89 ZERO
    V['S_J_no37open'] = merge(J, {37:{'ZERO':0}, 89:{'ZERO':0}})

    # T: J restricted to SECOND half only (the grow-half); first half keeps baseline
    V['T_J_2ndOnly'] = setfields(prog, {92:{'ZERO':1}, 96:{'ZERO':0}, 98:{'ZERO':0}})

    lams = {}
    for nm, e in V.items():
        lams[nm] = show(nm, setfields(prog, e))


if __name__ == '__main__':
    main()
