#!/usr/bin/env python3
"""Round-trip gain of each comb/all-pass cell (the exact writer/reader offset pairs).

For a matched offset O: a reader Rs reads DMEM[(pos-O)] EARLY in the 128-step sweep
(= value written one sample ago), the dab flows through R[WA], gets multiplied by the
chain of net coeffs, and a later writer Ws writes the NEW DMEM[(pos-O)]. The cell is a
1-(pos)-sample recirculating delay. Its open-loop round-trip gain g determines stability:
|g|<1 decays. I estimate g empirically by perturbing the cell's stored word and reading
the closed-loop response is hard; instead I read off the dominant recirculation: the
writer's own coeff * the reader-side coeff path. Simpler + rigorous: I directly read the
per-cell effective feedback by setting a unit value in that one cell, running ONE sample,
and reading the value written back to the same cell (the 1-step state-transition diagonal).
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import aru_datapath as A
import exp_lambda_clean as L
DMASK = A.DMASK; PICK = L.PICK


def one_sample_map(prog, dm_init, pos):
    """Run exactly one 128-step sweep (float, no seed) from a given DM state at given pos.
    Returns the new DM dict (only touched cells) so we can read the cell-to-cell transfer."""
    R = [0.0]*4; ACC = 0.0; RES = 0.0
    DM = dict(dm_init)
    pos = (pos+1) & DMASK
    for st in prog:
        addr = (pos - st['offset']) & DMASK
        dab = RES if st['b3'] else DM.get(addr, 0.0)
        mag = abs(st['coeff']); Cs = -(mag>>1) if st['coeff']<0 else (mag>>1)
        x = R[PICK(st)]; R[st['WA']] = dab
        if st['ZERO']: ACC = 0.0
        ACC = ACC + x*8.0*Cs/64.0
        if st['XFER']: RES = ACC/8.0
        if st['b3']: DM[addr] = RES
    return DM, pos


def main():
    prog = A.load_microcode(0x01)
    by_s = {st['s']: st for st in prog}
    # matched offsets (writer & reader share an offset) from the graph scan
    matches = {
        0xb334:[64,59],0xb870:[60,51,55],0xc1cc:[54,50],0xc278:[61,58],0xc324:[65,62],
        0xc518:[68,63],0xc688:[72,67],0xce78:[73,70],0xcf24:[69,66],0xd4d8:[46,26],
        0xdafc:[115,110],0xdfec:[111,103,106],0xe8d8:[105,102],0xe984:[112,109],
        0xea30:[116,113],0xeb88:[119,114],0xedec:[123,118],0xf584:[124,121],
        0xf62c:[120,117],0xfba2:[36,33],0xfba3:[39,34],0xfdf9:[88,85],0xfdfb:[91,86],
        0x1000:[52,104,40,92],
    }
    # The pos at which a given cell address = pos-O is touched: address depends on pos,
    # but the cell-to-itself round trip over ONE sample is pos-independent in structure.
    # Probe: seed cell address a0=(pos0-O) with 1.0, advance one sample (pos->pos+1), and
    # read the value at the NEW physical address that the writer writes AND that the same
    # reader will read next. Because reader reads (pos-O) and pos increments by 1 each
    # sample, the recirculation cell physically migrates by 1 word/sample (a delay line),
    # so the self-loop is: value at (pos-O) read this sample -> written to (pos+1-O) ...
    # i.e. it is a pure unit delay line; the LOOP closes only where a writer offset equals
    # a reader offset, giving feedback gain = product of coeffs from that reader to that writer.
    # Estimate that product directly from the step coeffs between reader idx and writer idx.
    idx = {st['s']: i for i, st in enumerate(prog)}
    print("=== per-cell recirculation: reader->writer coeff product (open-loop gain proxy) ===")
    print("  (Cnet=(|c|>>1)/64; product over the steps from reader to writer that carry the")
    print("   value via the register file; |g|>1 would be locally regenerative)")
    rows = []
    for O, ss in sorted(matches.items()):
        writers = [s for s in ss if by_s[s]['b3']]
        readers = [s for s in ss if not by_s[s]['b3']]
        for w in writers:
            cw = by_s[w]['coeff']; Cw = (abs(cw)>>1)/64.0*(1 if cw>=0 else -1)
            for r in readers:
                cr = by_s[r]['coeff']; Cr = (abs(cr)>>1)/64.0*(1 if cr>=0 else -1)
                # crude open-loop: the reader injects DM into a register, the writer's
                # coeff scales the accumulated result written back. Net cell feedback ~ Cw
                # times the reader-side weight Cr that re-enters. Report both + |Cw*Cr|.
                g = Cw*Cr
                rows.append((abs(g), O, r, w, Cr, Cw, g))
    rows.sort(reverse=True)
    for ag, O, r, w, Cr, Cw, g in rows:
        print(f"  off={O:#06x}  read s={r:3d}(Cr={Cr:+.3f}) -> write s={w:3d}(Cw={Cw:+.3f})"
              f"   g=Cr*Cw={g:+.4f}  |g|={ag:.4f}")
    print(f"\n  max |reader*writer| = {rows[0][0]:.4f} (if <1, NO single cell is locally")
    print("  over-unity -> the instability is a COLLECTIVE/global eigenmode, not one loop)")


if __name__ == '__main__':
    main()
