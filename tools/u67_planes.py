#!/usr/bin/env python3
"""Carry-over 1 -- crack the PCM70 U67 microword PLANE field map.

U67 ("PCM70 OPCODES V1.20") active region = low 1 KB (0x000-0x3FF) = 8 x 128-byte
PLANES.  A linear read mixes fields; the ROM is plane-organized, so:

    plane[p] = U67[p*128 : (p+1)*128]      p = 0..7   (128 steps each)

We label each plane (opcode/control vs coefficient vs offset-hi vs offset-lo vs
fill) by cross-referencing the VERIFIED PCM60 reference lanes:

  - OPCODE/CONTROL  : low-nibble histogram resembles PCM60 U43 (n7 >> nF/n3 > n0 ...);
                      low entropy, repeated motifs, section/phase bits.
  - OFFSET hi/lo    : a hi/lo plane pairing that, read as signed 16-bit (hi:lo),
                      yields a sane reverb tap set (incommensurate spread,
                      max delay in the thousands..~30k, like PCM60 U38:U32).
  - COEFFICIENT     : values clustered high (near 0xFF) with the x0.5 scalar (~0x7F)
                      present and descending decay runs (like PCM60 U35).
  - FILL            : ~all 0xFF / 0x00, no structure.

Also emits the literal PCM70(U67)-vs-PCM60 microcode comparison (the reverb-tap
lineage diff).
"""
from __future__ import annotations
import os, sys
import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from pcm60_decode import (load_pcm60, frame_index, N_STEPS, shannon, autocorr)

U67_PATH = os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
    "ROMs", "Lexicon PCM70", "Lexicon_PCM-70-V2_0-U67.BIN",
)

# --------------------------------------------------------------------------- #
def load_u67_planes(path: str = U67_PATH) -> list[np.ndarray]:
    b = np.fromfile(path, dtype=np.uint8)
    return [b[p * N_STEPS:(p + 1) * N_STEPS] for p in range(8)], b


def nibble_hist(b: np.ndarray, low=True) -> dict[int, int]:
    n = (b & 0x0F) if low else (b >> 4)
    h = np.bincount(n, minlength=16)
    return {i: int(h[i]) for i in range(16) if h[i]}


def cosine(a: dict, b: dict) -> float:
    """Cosine similarity between two {key:count} histograms over 0..15."""
    va = np.array([a.get(i, 0) for i in range(16)], dtype=float)
    vb = np.array([b.get(i, 0) for i in range(16)], dtype=float)
    na, nb = np.linalg.norm(va), np.linalg.norm(vb)
    if na == 0 or nb == 0:
        return 0.0
    return float(va @ vb / (na * nb))


def fingerprint(b: np.ndarray) -> dict:
    nz = b[b != 0xFF]
    return dict(
        entropy=round(shannon(b), 3),
        ff_pct=round(100 * float((b == 0xFF).mean()), 1),
        zero_pct=round(100 * float((b == 0x00).mean()), 1),
        n_unique=int(len(np.unique(b))),
        std=round(float(b.std()), 1),
        mn=int(b.min()), mx=int(b.max()),
        mean=round(float(b.mean()), 1),
        low_nib=nibble_hist(b, low=True),
        top=[f"{v:02X}:{int((b == v).sum())}" for v in
             np.argsort(np.bincount(b, minlength=256))[::-1][:6]],
    )


def signed16(hi: np.ndarray, lo: np.ndarray) -> np.ndarray:
    raw = (hi.astype(np.int32) << 8) | lo.astype(np.int32)
    return np.where(raw & 0x8000, raw - 0x10000, raw)


def reverb_sanity(hi: np.ndarray, lo: np.ndarray) -> dict:
    """Score a (hi, lo) plane pairing as an offset field.  Reverb-sane offsets:
    many distinct negative values (= read taps), incommensurate, max delay in the
    low-thousands..~30k, not dominated by 0 / 0xFFFF sentinels."""
    off = signed16(hi, lo)
    delays = -off                      # delay = -offset
    taps = delays[(delays >= 8) & (delays < 60000)]
    distinct = len(np.unique(taps))
    return dict(
        n_taps=int(distinct),
        tap_min=int(taps.min()) if len(taps) else None,
        tap_max=int(taps.max()) if len(taps) else None,
        frac_distinct=round(distinct / max(1, len(taps)), 3),
        n_pos_off=int((off > 0).sum()),   # write targets
        n_neg_off=int((off < 0).sum()),   # read taps
        # "sane" if a good chunk are distinct taps spread over a wide range
        score=round((distinct / 128.0) *
                    (1.0 if (len(taps) and 200 < taps.max() < 40000) else 0.2), 3),
    )


# --------------------------------------------------------------------------- #
def main():
    planes, raw = load_u67_planes()
    print("=" * 78)
    print("U67 plane analysis  (active 1 KB = 8 x 128-byte planes)")
    print("=" * 78)
    print(f"U67 size {len(raw)}B, bytes 0x000-0x3FF active, 0x400-0x1FFF = "
          f"{100*float((raw[0x400:]==0xFF).mean()):.1f}% 0xFF fill")

    # ---- PCM60 reference fingerprints (program 0, param 0 frame) ---- #
    lanes = load_pcm60()
    a, b = frame_index(0, 0)
    ref = {chip: lanes[chip][a:b] for chip in ("U32", "U35", "U38", "U43")}
    ref_fp = {chip: fingerprint(ref[chip]) for chip in ref}
    print("\n--- PCM60 reference lanes (program 0 frame 0) ---")
    for chip, role in [("U43", "control/opcode"), ("U35", "coefficient"),
                       ("U38", "offset-hi"), ("U32", "offset-lo")]:
        fp = ref_fp[chip]
        print(f"  {chip} ({role:14s}): H={fp['entropy']} std={fp['std']} "
              f"uniq={fp['n_unique']} FF%={fp['ff_pct']} top={fp['top'][:4]}")
        if chip == "U43":
            print(f"       U43 low-nibble (opcode) hist: {fp['low_nib']}")

    # ---- U67 plane fingerprints ---- #
    print("\n--- U67 planes ---")
    fps = []
    for p, pl in enumerate(planes):
        fp = fingerprint(pl)
        fps.append(fp)
        nonff = int((pl != 0xFF).sum())
        print(f"  plane {p} (0x{p*128:03X}): nonFF={nonff:3d} H={fp['entropy']:5.3f} "
              f"std={fp['std']:5.1f} uniq={fp['n_unique']:3d} mean={fp['mean']:5.1f} "
              f"top={fp['top'][:4]}")

    # ---- Opcode-plane detection: nibble-histogram cosine vs U43 ---- #
    print("\n--- opcode/control plane test (low-nibble cosine vs PCM60 U43) ---")
    u43_lownib = ref_fp["U43"]["low_nib"]
    op_scores = []
    for p, pl in enumerate(planes):
        c_lo = cosine(nibble_hist(pl, low=True), u43_lownib)
        op_scores.append(c_lo)
        print(f"  plane {p}: low-nib cosine vs U43 = {c_lo:.3f}   "
              f"plane low-nib hist={nibble_hist(pl, low=True)}")
    best_op = int(np.argmax(op_scores))
    print(f"  => best opcode/control candidate: plane {best_op} (cosine {op_scores[best_op]:.3f})")

    # ---- Offset hi/lo pair search ---- #
    print("\n--- offset hi/lo pair search (reverb-sanity over ordered plane pairs) ---")
    pairs = []
    for ph in range(8):
        for pl in range(8):
            if ph == pl:
                continue
            # skip near-pure-fill planes as candidates
            if (planes[ph] == 0xFF).mean() > 0.9 or (planes[pl] == 0xFF).mean() > 0.9:
                continue
            sane = reverb_sanity(planes[ph], planes[pl])
            pairs.append((sane["score"], ph, pl, sane))
    pairs.sort(reverse=True)
    print("  top hi/lo pairings by reverb-sanity score:")
    for score, ph, pl, sane in pairs[:6]:
        print(f"    hi=plane{ph} lo=plane{pl}: score={score} taps={sane['n_taps']} "
              f"range={sane['tap_min']}..{sane['tap_max']} "
              f"neg/pos off={sane['n_neg_off']}/{sane['n_pos_off']} "
              f"fracDistinct={sane['frac_distinct']}")

    # PCM60 reference reverb-sanity for calibration
    ref_sane = reverb_sanity(ref["U38"], ref["U32"])
    print(f"  [PCM60 U38:U32 reference] score={ref_sane['score']} taps={ref_sane['n_taps']} "
          f"range={ref_sane['tap_min']}..{ref_sane['tap_max']}")

    # ---- Coefficient plane test: high-clustered + x0.5 scalar present ---- #
    print("\n--- coefficient plane test (high-clustered values + ~0x7F scalar) ---")
    for p, pl in enumerate(planes):
        if (pl == 0xFF).mean() > 0.9:
            continue
        frac_high = float((pl >= 0xC0).mean())      # coeffs cluster near 1.0
        has_scalar = int(((pl >= 0x7C) & (pl <= 0x82)).sum())  # ~0x7F x0.5 idiom
        print(f"  plane {p}: frac>=0xC0={frac_high:.2f}  ~0x7F-scalar count={has_scalar}  "
              f"mean={fps[p]['mean']}")


if __name__ == "__main__":
    main()
