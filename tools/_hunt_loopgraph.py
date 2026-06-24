#!/usr/bin/env python3
"""ANGLE: decompose WHERE the >1 gain originates.

Build the DMEM write->read feedback graph from the CONCERT microprogram, then
quantify how the +1126 ppm structural eigenvalue is distributed: localized in one
loop (=> a decode bug, nameable steps) or spread across many (=> uniform loss).

Method:
  - Static graph: each b3-write step writes RES (=ACC/8) to DMEM at addr=(pos-offset).
    A later step READS that address when its own (pos-offset) collides modulo delay.
    Two steps with offsets o_w (writer) and o_r (reader) form an edge with sample
    delay D = (o_w - o_r) mod 2^16 = how many samples later (in 'pos' units) the
    written word is read. Round-trip = path back to the writer.
  - But the REAL coupling is also through the register file (R[WA] <- dab; x=R[pick]).
    DMEM is the only LONG-delay memory (registers are overwritten within one sample),
    so the structural recirculation MUST close through DMEM. So I focus on the DMEM
    write/read bipartite graph and the per-edge coefficient gains.
  - Eigen-localization: compute the float eigenvalue, then do a leave-one-loop-out:
    for each candidate damping closer (b3 write step), measure d(lambda) when its
    coeff is scaled, to see if the excess concentrates in one closer or spreads.
"""
import sys, os, math
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import aru_datapath as A
import exp_lambda_clean as L

DMASK = A.DMASK
PICK = L.PICK


def conv_lambda(prog, pick=PICK, nsamp=40000, K=128):
    traj = L.lambda_trajectory(prog, pick=pick, nsamp=nsamp, K=K)
    tail = sorted(l for _, l in traj[-60:])
    return tail[len(tail)//2]


def main():
    prog = A.load_microcode(0x01)
    print(f"CONCERT: {len(prog)} active steps\n")

    # ---- dump every step with its decode + role ----
    print("=== STEP TABLE (idx, s, offset, coeff, Cnet=(|c|>>1)/64, ZERO, b3, XFER, WA, pick) ===")
    writers = []   # b3 steps that write DMEM
    readers = []   # steps that read DMEM (b3==0)  -> dab = DM[addr]
    for i, st in enumerate(prog):
        mag = abs(st['coeff']); Cs = -(mag >> 1) if st['coeff'] < 0 else (mag >> 1)
        Cnet = Cs / 64.0
        role = []
        if st['b3']: role.append("Wb3(read RES, write DM)")
        else: role.append("readDM")
        if st['XFER']: role.append("XFER")
        if st['ZERO']: role.append("ZERO")
        print(f"  [{i:3d}] s={st['s']:3d} off={st['offset']:#06x} coeff={st['coeff']:+4d} "
              f"Cnet={Cnet:+.4f} Z={st['ZERO']} b3={st['b3']} X={st['XFER']} "
              f"WA={st['WA']} pick={PICK(st)}  {' '.join(role)}")
        if st['b3']:
            writers.append(st)
        else:
            readers.append(st)

    print(f"\n  b3 writers (read RES->DAB, write DM): {len(writers)}")
    print(f"  DMEM readers (b3==0, dab=DM[addr]):  {len(readers)}")

    # ---- the structural DMEM write->read edge graph ----
    # A word written by writer W at absolute pos P lands at DMEM[(P - oW) & M].
    # A reader R at absolute pos P' reads DMEM[(P' - oR) & M].
    # Same physical cell <=> (P - oW) == (P' - oR) (mod 2^16)
    #   => P' - P == (oR - oW) (mod 2^16) = number of whole-sample 'pos' ticks between
    #      the write and the read. Since pos advances by exactly 1 per audio sample,
    #      delay_samples D = (oR - oW) & M. (D can be up to 65535 samples ~ 1.9s @34k.)
    # Round-trip loop W->R->...->back-to-W gives total delay (sum of D) and gain
    #   (product of the per-step net coefficients on the path through registers).
    # NOTE many readers also feed (via registers + later b3 steps) other writers in
    # the SAME sample, so loops can be intra-sample (D contributions of 0) too.
    print("\n=== DMEM write->read edges (writer offset -> reader offset, delay D samples) ===")
    # group by exact offset since address = pos-offset and pos is shared
    from collections import defaultdict
    edges = []
    for W in writers:
        for Rd in readers:
            D = (Rd['offset'] - W['offset']) & DMASK
            edges.append((W['s'], Rd['s'], D, W['offset'], Rd['offset']))
    # Also a writer can read its OWN cell next time only via a reader at a matching
    # offset; but a b3 step both reads RES (not DM) and writes DM, so a b3 writer is
    # NOT a DMEM reader. The recirculation is writer-offset == reader-offset (D=0 in
    # pos terms means SAME sample, same cell) up to D large.
    # Show the small-D (tight) edges and the count distribution.
    edges.sort(key=lambda e: e[2])
    print("  tightest 25 edges by delay D (D=0 => same-sample same-cell coupling):")
    for e in edges[:25]:
        print(f"    W.s={e[0]:3d}(off={e[3]:#06x}) -> R.s={e[1]:3d}(off={e[4]:#06x})  D={e[2]:6d} samp")
    # offset histogram: which writer offsets exactly match a reader offset (D=0)
    woff = defaultdict(list); roff = defaultdict(list)
    for W in writers: woff[W['offset']].append(W['s'])
    for Rd in readers: roff[Rd['offset']].append(Rd['s'])
    common = sorted(set(woff) & set(roff))
    print(f"\n  EXACT offset matches (writer & reader share an offset -> a true recirc cell):")
    for o in common:
        print(f"    off={o:#06x}: writers {woff[o]}  readers {roff[o]}")
    if not common:
        print("    (none -- DMEM recirc is via DIFFERENT offsets, i.e. pure delay lines)")

    print("\n  bit15-set DMEM addresses among writers/readers (the FPC-vs-DMEM question):")
    for st in writers:
        if st['offset'] & 0x8000:
            print(f"    WRITER s={st['s']} off={st['offset']:#06x} (bit15 set) writes DM")
    for st in readers:
        if st['offset'] & 0x8000:
            print(f"    READER s={st['s']} off={st['offset']:#06x} (bit15 set) reads DM")

    print("\n=== baseline converged lambda ===")
    lam0 = conv_lambda(prog)
    print(f"  lambda0 = {lam0:.7f}  ({(lam0-1)*1e6:+.1f} ppm)  target 0.9999899")


if __name__ == '__main__':
    main()
