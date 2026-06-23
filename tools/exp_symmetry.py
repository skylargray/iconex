#!/usr/bin/env python3
"""Tank stereo-symmetry + loop-delay check (complements the offset/Z80 audit).

CONCERT is a symmetric stereo tank: each recirculating closer block in channel A
should have a mirror in channel B with identical coeff and identical RELATIVE loop
delay. An asymmetry = a build/decode/emulation anomaly. Also reports each closer's
recirculation loop delay (write-tap vs the feedback read that drives it) and the
dominant growing-mode period for cross-reference.
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import aru_datapath as A
from exp_eig import power_iter, dominant_freq

PICK = lambda st: (st['b5'] << 1) | st['b4']


def main():
    prog = A.load_microcode(0x01)
    bystep = {p['s']: p for p in prog}
    closers = [p for p in prog if p['b3'] == 1 and p['XFER'] == 1]
    print("loop closers (b3=1 & XFER=1): step  coeff  offset  RA  WA")
    for p in closers:
        print(f"   s{p['s']:<3} c={p['coeff']:>4}  off={p['offset']:>6}  RA={(p['b5']<<1)|p['b4']}  WA={p['WA']}")

    # Channel A vs B symmetric closer pairs by coeff+structure proximity:
    # the tank's two halves are roughly steps 23-77 (A) and 78-127 (B). Pair each
    # A-closer with the B-closer at the same intra-half position.
    A_cl = [p for p in closers if p['s'] < 78]
    B_cl = [p for p in closers if p['s'] >= 78]
    print(f"\nchannel A closers: {[p['s'] for p in A_cl]}")
    print(f"channel B closers: {[p['s'] for p in B_cl]}")
    print("\npairwise coeff comparison (A vs B, in order):")
    for a, b in zip(A_cl, B_cl):
        flag = "" if a['coeff'] == b['coeff'] else "  <-- COEFF MISMATCH"
        print(f"   s{a['s']}(c={a['coeff']}) <-> s{b['s']}(c={b['coeff']}){flag}")

    # offset deltas within each half (relative loop structure)
    print("\nintra-half offset deltas between consecutive closers:")
    da = [A_cl[i+1]['offset'] - A_cl[i]['offset'] for i in range(len(A_cl)-1)]
    db = [B_cl[i+1]['offset'] - B_cl[i]['offset'] for i in range(len(B_cl)-1)]
    print(f"   A: {da}")
    print(f"   B: {db}")
    print(f"   symmetric? {'YES' if da==db else 'NO (differs)'}")

    lam, proxy = power_iter(prog, PICK, nsamp=30000)
    df = dominant_freq(proxy)
    if df:
        f, lag, corr = df
        print(f"\ndominant growing mode ~ {f:.0f} Hz (period {lag} samples, autocorr {corr:.3f})")


if __name__ == '__main__':
    main()
