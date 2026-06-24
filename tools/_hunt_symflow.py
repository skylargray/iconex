#!/usr/bin/env python3
"""LEAD 1 foundation: EXACT symbolic single-sample linear flow graph.

The datapath decouples coeff from DAB: at each step the coeff multiplies R[pick]
(a value loaded by an EARLIER step), while this step's DAB (a DM read or RES) is
written to R[WA] for a LATER step. So you CANNOT read off a cell's feedforward vs
feedback gain from raw step coeffs -- you must propagate symbolically.

This runs ONE 110-step sweep with every value carried as a linear combination of
"atoms" (sample-start state): R[0..3], ACC, RES, and the stored DM words M[offset].
The float arithmetic is mirrored EXACTLY from exp_lambda_clean.lambda_trajectory.

Output: for each written DM offset O, the new word M'[O] as a linear combo of the
old stored words M[.] (the delay lines read this sample) + carried RES/ACC/R.
This is the cycle-exact intra-sample flow graph with ZERO hand-tracing risk.

VALIDATION: applies the symbolic map to a random concrete state and compares to a
literal one-sample run of the same float datapath; they must agree to ~1e-9.
"""
import sys, os, math, random
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import aru_datapath as A

DMASK = A.DMASK
random.seed(12345)

# ---- tiny symbolic linear-combo algebra: value = dict{atom: float coeff} ----
def scale(v, k):
    if k == 0.0:
        return {}
    return {a: c * k for a, c in v.items()}

def add(v, w):
    r = dict(v)
    for a, c in w.items():
        r[a] = r.get(a, 0.0) + c
        if r[a] == 0.0:
            del r[a]
    return r


def sym_sweep(prog):
    """Run one symbolic 110-step sweep. Returns dict with:
        dm_new[O]  : new stored word at offset O  (linear combo of atoms)
        R_new[i], ACC_new, RES_new : carried state out
    Atoms: ('R',i) ('ACC',) ('RES',) ('M',offset).
    Mirrors exp_lambda_clean.lambda_trajectory float ops exactly (no seed, no renorm)."""
    R = [{('R', i): 1.0} for i in range(4)]
    ACC = {('ACC',): 1.0}
    RES = {('RES',): 1.0}
    DM = {}            # offset -> symbolic value (only touched offsets)
    # NOTE: 'pos' is symbolic-constant within a sample, so offset is a valid key:
    # within one sample addr=(pos-offset) is a bijection offset<->addr.
    def dm_read(off):
        if off not in DM:
            DM[off] = {('M', off): 1.0}     # the stored (delayed) word at this offset
        return DM[off]
    for st in prog:
        off = st['offset']
        dab = dict(RES) if st['b3'] else dm_read(off)
        mag = abs(st['coeff']); Cs = -(mag >> 1) if st['coeff'] < 0 else (mag >> 1)
        x = R[st['pickpick']] if 'pickpick' in st else R[(st['b5'] << 1) | st['b4']]
        # write bus AFTER reading multiplicand (LS670 read-before-write)
        R[st['WA']] = dict(dab)
        if st['ZERO']:
            ACC = {}
        ACC = add(ACC, scale(x, 8.0 * Cs / 64.0))   # exact mirror
        if st['XFER']:
            RES = scale(ACC, 1.0 / 8.0)
        if st['b3']:
            DM[off] = dict(RES)
    return dict(dm_new=DM, R_new=R, ACC_new=ACC, RES_new=RES)


def validate(prog, trials=4):
    """Apply symbolic map to a random concrete start state; compare to a literal
    one-sample float run of the SAME datapath. Must match to ~1e-9 relative."""
    res = sym_sweep(prog)
    maxerr = 0.0
    for t in range(trials):
        # random concrete start state
        cR = [random.uniform(-1, 1) for _ in range(4)]
        cACC = random.uniform(-1, 1)
        cRES = random.uniform(-1, 1)
        cM = {}
        for O in res['dm_new']:
            cM[O] = random.uniform(-1, 1)
        # also seed any M atom that appears in any expression
        atoms = set()
        for v in list(res['dm_new'].values()) + res['R_new'] + [res['ACC_new'], res['RES_new']]:
            atoms |= set(v.keys())
        for a in atoms:
            if a[0] == 'M' and a[1] not in cM:
                cM[a[1]] = random.uniform(-1, 1)

        def ev(v):
            s = 0.0
            for a, c in v.items():
                if a[0] == 'R': s += c * cR[a[1]]
                elif a[0] == 'ACC': s += c * cACC
                elif a[0] == 'RES': s += c * cRES
                elif a[0] == 'M': s += c * cM.get(a[1], 0.0)
            return s

        # literal float one-sample run from the same concrete state
        R = list(cR); ACC = cACC; RES = cRES
        DM = dict(cM)
        for st in prog:
            off = st['offset']
            dab = RES if st['b3'] else DM.get(off, 0.0)
            mag = abs(st['coeff']); Cs = -(mag >> 1) if st['coeff'] < 0 else (mag >> 1)
            x = R[(st['b5'] << 1) | st['b4']]
            R[st['WA']] = dab
            if st['ZERO']: ACC = 0.0
            ACC = ACC + x * 8.0 * Cs / 64.0
            if st['XFER']: RES = ACC / 8.0
            if st['b3']: DM[off] = RES
        # compare carried + all written offsets
        err = abs(ev(res['RES_new']) - RES)
        err = max(err, abs(ev(res['ACC_new']) - ACC))
        for i in range(4):
            err = max(err, abs(ev(res['R_new'][i]) - R[i]))
        for O, v in res['dm_new'].items():
            err = max(err, abs(ev(v) - DM[O]))
        maxerr = max(maxerr, err)
    return maxerr


def main():
    prog = A.load_microcode(0x01)
    res = sym_sweep(prog)
    err = validate(prog)
    print(f"symbolic-map validation max abs err vs literal float run = {err:.3e}  "
          f"({'OK' if err < 1e-9 else 'FAIL'})\n")

    closers = [36,46,54,61,65,69,73,88,98,105,112,116,120,124]
    by_s = {st['s']: st for st in prog}
    # map closer step -> its write offset
    print("=== per-CLOSER cell: new word M'[O] = combo of old stored words M[.] + carries ===")
    print("    (self = coeff of M[O] in M'[O] = the cell's own delay-line FEEDBACK gain)\n")
    for cs in closers:
        O = by_s[cs]['offset']
        v = res['dm_new'].get(O)
        if v is None:
            print(f"  closer s={cs} off={O:#06x}: NOT a final DM write?!"); continue
        self_g = v.get(('M', O), 0.0)
        # sort contributing terms by magnitude
        terms = sorted(v.items(), key=lambda kv: -abs(kv[1]))
        tstr = "  ".join(f"{_atom(a)}:{c:+.4f}" for a, c in terms if abs(c) > 5e-4)
        print(f"  s={cs:3d} off={O:#06x} closer_coeff={by_s[cs]['coeff']:+4d}  "
              f"SELF g(M[O])={self_g:+.4f}")
        print(f"        M'[O] = {tstr}")
    print("\n  (if SELF g ~ +0.969 for all -> +124 IS the comb feedback (Lead-1 premise).")
    print("   if SELF g ~ -0.77 -> the comb feedback is the -95 double-read, +124 is feedforward.)")


def _atom(a):
    if a[0] == 'M': return f"M[{a[1]:#06x}]"
    if a[0] == 'R': return f"R{a[1]}"
    return a[0]


if __name__ == '__main__':
    main()
