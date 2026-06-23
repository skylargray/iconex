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


def sat20(x):
    """Saturate to the ARU's 20-bit signed accumulator (+/-524287)."""
    return 524287 if x > 524287 else (-524287 if x < -524287 else x)


def run(prog, ra_pick, nsamp=4000, imp=20000):
    """Run nsamp samples; inject one impulse into the input register at sample 0.

    Firmware/schematic-resolved cycle-accurate ARU model. Per output sample:
    pos advances by 1; then each active step (in order) executes the resolved datapath:
      6-bit coefficient C = (abs(coeff) >> 1) applied with CSIGN; b3 selects RES->DAB
      (and writes RES back to DMEM, post-XFER); LS670 read-before-write register file;
      ZERO clears the accumulator first; MAC uses operand = x<<3, prod = (operand*Cs)>>6,
      20-bit saturating accumulator; XFER loads RES = sat16(ACC>>3) BEFORE the b3
      write-back so comb closers store the just-computed (post-XFER) RES.
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
            # 1. delay address
            addr = (pos - st['offset']) & DMASK
            # 2. DAB source: b3 -> result register drives DAB (the CURRENT, pre-XFER RES);
            #    else read DMEM. Impulse injected additively at first active step of sample 0.
            if st['b3']:
                dab = RES
            else:
                dab = DM[addr]
            if n == 0 and st is prog[0]:
                dab += imp
            # 3. 6-bit coefficient with sign
            mag = abs(st['coeff'])
            csign = st['coeff'] < 0
            Cs = -(mag >> 1) if csign else (mag >> 1)
            # 4. LS670 read-before-write: read multiplicand FIRST, then write the bus.
            ra = ra_pick(st)
            x = R[ra]
            R[st['WA']] = dab
            # 5. ZERO clears the accumulator before this step's product.
            if st['ZERO']:
                ACC = 0
            # 6. multiply-accumulate: operand<<3, 6-bit fractional coeff, 20-bit acc
            operand = x << 3
            prod = (operand * Cs) >> 6
            ACC = sat20(ACC + prod)
            # 7. XFER then write-back: RES loads from ACC (net x*Cs/64), then the b3
            #    write-back stores the POST-XFER RES into DMEM.
            if st['XFER']:
                RES = sat16(ACC >> 3)
            if st['b3']:
                DM[addr] = RES
            # 8. energy probe
            if st['XFER']:
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


def run_trace(prog, ra_pick, nsamp=4000, imp=20000, trace_window=64):
    """Instrumented twin of run(). Returns (esum_list, steps).

    esum_list[n]  : per-sample output energy, identical to run().
    steps         : flat list of per-step probe tuples for samples n < trace_window,
                    each = (n, s, addr, dab, racc_in, prod, acc, res) where
                    res = the RES value after this step if XFER else INT64_MIN sentinel.
    Mirrors run() bit-for-bit (floor division, sat16, injected impulse at first active step of sample 0).
    """
    SENT = -(1 << 63)
    R = [0, 0, 0, 0]
    ACC = 0
    RES = 0
    DM = [0] * (DMASK + 1)
    pos = 0
    esum_list = []
    steps = []
    for n in range(nsamp):
        pos = (pos + 1) & DMASK
        esum = 0
        for st in prog:
            # 1. delay address
            addr = (pos - st['offset']) & DMASK
            # 2. DAB source (b3 -> pre-XFER RES; else DMEM read), additive impulse.
            if st['b3']:
                dab = RES
            else:
                dab = DM[addr]
            if n == 0 and st is prog[0]:
                dab += imp
            # 3. 6-bit coefficient with sign
            mag = abs(st['coeff'])
            csign = st['coeff'] < 0
            Cs = -(mag >> 1) if csign else (mag >> 1)
            # 4. LS670 read-before-write
            ra = ra_pick(st)
            racc_in = R[ra]            # x: multiplicand read BEFORE this cycle's write
            R[st['WA']] = dab
            # 5. ZERO clears accumulator first
            if st['ZERO']:
                ACC = 0
            # 6. MAC: operand<<3, 6-bit coeff, 20-bit saturating accumulator
            operand = racc_in << 3
            prod = (operand * Cs) >> 6
            ACC = sat20(ACC + prod)
            # 7. XFER then post-XFER b3 write-back
            if st['XFER']:
                RES = sat16(ACC >> 3)
            if st['b3']:
                DM[addr] = RES
            # 8. energy + probe
            if st['XFER']:
                esum += abs(RES)
                res_val = RES
            else:
                res_val = SENT
            if n < trace_window:
                steps.append((n, st['s'], addr, dab, racc_in, prod, ACC, res_val))
        esum_list.append(esum)
    return esum_list, steps


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
