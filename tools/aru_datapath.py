#!/usr/bin/env python3
"""224XL ARU datapath model (reference for bit-exact reconstruction).

Resolves the lane2[5:2] RA-vs-XFER ambiguity by running the decoded CONCERT microcode
through a cycle-faithful ARU datapath and checking which RA bit-assignment produces a
coherent, decaying reverb (vs. garbage). Field map (lane2 = ~stored control byte):

  b7 = ZERO  (clear accumulator)        b3 = DMEM read/write select (or DAB source)
  b6 = PROTECT (WCS access; ignored)    b2 = XFER (load result register, write tank)
  b5,b4 = RA (read register addr)       b1:0 = WA (write register addr; 3 = pass-through)
  lane3 = coeff (7-bit sign-mag), lanes0-1 = OFST (delay; addr = position - offset).

ARU (Service Manual 3.7): 4x16 register file (WA write / RA read), 16x6 saturating multiplier
+ CSIGN, 20-bit accumulator, 16-bit result register, DMEM addressed by position-offset.
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import boot_xl as B

DMASK = 0xFFFF          # 64K-word DMEM (1 bank of 64K DRAM per manual)


def load_microcode(power_up_id=0x01):
    cpu, mem, *_ = B.boot(power_up_id=power_up_id, verbose=False)
    img = bytes(mem[0x4000:0x4200])
    prog = []
    for s in range(128):
        l0, l1, l2, l3 = img[s*4], img[s*4+1], img[s*4+2], img[s*4+3]
        if l2 == 0xFF and l3 == 0xFF:
            prog.append(None); continue
        ctl = (~l2) & 0xFF
        offset = (~(l0 | (l1 << 8))) & 0xFFFF
        coeff = (-(l3 & 0x7F) if l3 & 0x80 else (l3 & 0x7F))   # signed 7-bit magnitude
        prog.append(dict(s=s, offset=offset, coeff=coeff,
                         ZERO=(ctl >> 7) & 1, b3=(ctl >> 3) & 1, XFER=(ctl >> 2) & 1,
                         WA=ctl & 3, b5=(ctl >> 5) & 1, b4=(ctl >> 4) & 1))
    return [p for p in prog if p]


def sat16(x):
    return 32767 if x > 32767 else (-32768 if x < -32768 else x)


def run(prog, ra_pick, nsamp=4000, imp=20000):
    """Run nsamp samples; inject one impulse into the input register at sample 0.
    ra_pick(step)->0..3 selects the read register. Returns the per-sample output energy
    (sum |RES at XFER steps|) to gauge whether a coherent reverb decay forms."""
    R = [0, 0, 0, 0]
    ACC = 0
    RES = 0
    DM = [0] * (DMASK + 1)
    pos = 0
    out = []
    for n in range(nsamp):
        pos = (pos + 1) & DMASK
        esum = 0
        for st in prog:
            addr = (pos - st['offset']) & DMASK
            # bus value: XFER step writes RES to DMEM; else read DMEM
            if st['XFER']:
                DM[addr] = RES
                dab = RES
            else:
                dab = DM[addr]
            # input injection: first non-XFER step of sample 0 gets the impulse
            if n == 0 and st is prog[0]:
                dab = imp
            # register write (addr 3 = pass-through transient, still latches the bus)
            R[st['WA']] = dab
            # multiply-accumulate
            ra = ra_pick(st)
            if st['ZERO']:
                ACC = 0
            ACC = sat16(ACC + (R[ra] * st['coeff']) // 128)  # 7-bit sign-mag coeff / 128
            if st['XFER']:
                RES = sat16(ACC)
                esum += abs(RES)
        out.append(esum)
    return out


def decay_metric(out):
    """How reverb-like: peak, then late-energy ratio + smoothness."""
    peak = max(out) or 1
    early = sum(out[:200]) / 200
    late = sum(out[2000:2200]) / 200
    return dict(peak=peak, early=round(early), late=round(late),
                late_ratio=round(late / (early or 1), 4),
                blown=any(o >= 32767 * len([1]) for o in out[-50:]))


if __name__ == '__main__':
    prog = load_microcode(0x01)
    print(f"CONCERT: {len(prog)} active steps")
    for name, pick in [("RA=(b5,b4)", lambda st: (st['b5'] << 1) | st['b4']),
                       ("RA=(b5,b3)", lambda st: (st['b5'] << 1) | st['b3']),
                       ("RA=(b4,b3)", lambda st: (st['b4'] << 1) | st['b3'])]:
        out = run(prog, pick)
        m = decay_metric(out)
        print(f"  {name}: peak={m['peak']:>9} early={m['early']:>8} late={m['late']:>8} "
              f"late/early={m['late_ratio']:.4f}")
