#!/usr/bin/env python3
"""LEAD 1 (reframed): is the recirculating core supposed to be LOSSLESS?

_hunt_symflow proved +124 is NOT the comb feedback (self-loops are all sub-unity,
max |g|=0.766). So the over-unity is in the COUPLING. The principled, design-justified
diagnostic for a reverb's feedback core is its coupling matrix C (old stored words
M[off] -> new stored words M'[off], restricted to offsets that are BOTH written and
read = the feedback nodes). A lossless reverb prototype has C paraunitary: every
singular value == 1, energy is conserved (lambda_prototype = 1), and the designed RT60
is a separate small damping coefficient. If sigma_max(C) > 1 the core CREATES energy
-> that is the over-unity, and the gap sigma_max-1 quantifies the design/decode error.

Uses numpy SVD. Reports sigma spectrum, deviation from orthogonality (||C^T C - I||),
and the dominant singular vectors (which delay lines / cells carry the hot mode)."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import aru_datapath as A
import _hunt_symflow as SF
import numpy as np


def build_coupling(prog):
    res = SF.sym_sweep(prog)
    dm_new = res['dm_new']                       # offset -> combo of atoms
    written = sorted(dm_new.keys())
    wset = set(written)
    # read offsets that feed each written word
    read_off = set()
    for v in dm_new.values():
        for a in v:
            if a[0] == 'M':
                read_off.add(a[1])
    core = sorted(wset & read_off)               # feedback nodes (written AND read)
    ext  = sorted(read_off - wset)               # external inputs (read, never written)
    idx = {o: i for i, o in enumerate(core)}
    n = len(core)
    C = np.zeros((n, n))
    Cext = {}                                     # external contribution per written core node
    for o in core:
        for a, c in dm_new[o].items():
            if a[0] == 'M':
                if a[1] in idx:
                    C[idx[o], idx[a[1]]] = c
                else:
                    Cext.setdefault(o, []).append((a[1], c))
    return core, ext, C


def main():
    prog = A.load_microcode(0x01)
    core, ext, C = build_coupling(prog)
    n = len(core)
    print(f"recirculating core: {n} feedback offsets (written AND read)")
    print(f"external input offsets (read, never written): {len(ext)}\n")

    U, S, Vt = np.linalg.svd(C)
    print(f"=== coupling matrix C singular values ({n}x{n}) ===")
    print("  sigma:", "  ".join(f"{s:.4f}" for s in S[:12]),
          ("..." if n > 12 else ""))
    print(f"  sigma_max = {S[0]:.6f}   sigma_min = {S[-1]:.6f}")
    print(f"  >1 sigmas: {int((S>1+1e-9).sum())} of {n}")
    ortho = np.linalg.norm(C.T @ C - np.eye(n))
    print(f"  ||C^T C - I||_F = {ortho:.4f}   (0 => perfectly lossless/orthogonal core)")
    print(f"  det(C) = {np.linalg.det(C):+.4f}   spectral radius rho(C) = "
          f"{max(abs(np.linalg.eigvals(C))):.6f}")

    # dominant mode: right singular vector v0 (the input mix that gets amplified most)
    v0 = Vt[0]; u0 = U[:, 0]
    print(f"\n=== dominant singular mode (sigma_max={S[0]:.4f}): which delay lines dominate ===")
    order = np.argsort(-np.abs(v0))
    for k in order[:10]:
        print(f"  off={core[k]:#06x}  v_in={v0[k]:+.3f}  u_out={u0[k]:+.3f}")

    # per-row gain (how hot each written node is) and per-col
    rg = np.abs(C).sum(axis=1)
    print(f"\n=== rows with largest L1 gain (most energy injected into that line) ===")
    for k in np.argsort(-rg)[:8]:
        print(f"  M'[{core[k]:#06x}]  rowL1={rg[k]:.3f}  selfdiag={C[k,k]:+.4f}")


if __name__ == '__main__':
    main()
