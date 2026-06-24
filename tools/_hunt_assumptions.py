#!/usr/bin/env python3
"""Systematic elimination: enumerate EVERY structural assumption in the CONCERT datapath
model, flip each one to its plausible alternative(s), and measure the float linear-map
eigenvalue lambda. Baseline = +1126 ppm GROW; target = decay (lambda<1). Any flip that
yields lambda<1 is a CANDIDATE root cause; everything else is ELIMINATED.

Assumptions covered:
  DECODE: offset polarity/direction; coeff sign-magnitude; ctl inversion; field bit-map
          (ZERO/XFER/b3/WA/RA assignments).
  DATAPATH: addr=pos-offset; b3 read source + write timing; register read-before-write;
            WA=3 write vs pass-through; ZERO before/after; coeff width (>>1); operand <<3;
            RES >>3; DMEM 64K vs bit15=FPC; per-sample state reset.
"""
import sys, os, math
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import aru_datapath as A

DMASK = 0xFFFF
DEFAULT_PICK = lambda st: (st['b5'] << 1) | st['b4']


def lam(prog, *, pick=DEFAULT_PICK, coeff_shift=1, operand_shift=3, res_shift=3, prod_shift=6,
        b3_read='RES', b3_write='post', write_first=False, zero_after=False, addr_plus=False,
        suppress=frozenset(), wa3_nowrite=False, reset_per_sample=False, coeff_mode='sm',
        nsamp=40000, K=128, seed=1e4):
    """Parameterized float linear-map power iteration. Defaults == the committed model."""
    R = [0.0]*4; ACC = 0.0; RES = 0.0
    DM = [0.0]*(DMASK+1); pos = 0
    nz = set(); seeded = False; logs = []
    gain_num = float(1 << operand_shift)
    gain_den = float(1 << prod_shift)
    res_div = float(1 << res_shift)
    for n in range(nsamp):
        pos = (pos+1) & DMASK
        if reset_per_sample:
            ACC = 0.0; RES = 0.0; R = [0.0]*4
        for st in prog:
            off = st['offset']
            addr = ((pos + off) if addr_plus else (pos - off)) & DMASK
            sup = st['s'] in suppress
            if sup:
                dab = 0.0
            elif st['b3']:
                dab = RES if b3_read == 'RES' else DM[addr]
            else:
                dab = DM[addr]
            if not seeded and st is prog[0]:
                dab += seed; seeded = True
            # reconstruct the raw lane3 byte, then decode per coeff_mode (tests the coeff
            # DECODE itself -- the multiply test vectors validate the MULTIPLY, not the l3->coeff
            # decode, so the sign convention / active-low-ness of lane3 is UNVERIFIED).
            mag0 = abs(st['coeff']); l3 = (mag0 | 0x80) if st['coeff'] < 0 else mag0
            cm = coeff_mode
            if cm == 'sm':            # current: bit7=1 -> negative
                signed = -(l3 & 0x7F) if (l3 & 0x80) else (l3 & 0x7F)
            elif cm == 'siginv':      # bit7=0 -> negative (active-low SIGN)
                signed = (l3 & 0x7F) if (l3 & 0x80) else -(l3 & 0x7F)
            elif cm == 'inv':         # fully active-low lane3 (~l3) then sign-mag
                il3 = (~l3) & 0xFF
                signed = -(il3 & 0x7F) if (il3 & 0x80) else (il3 & 0x7F)
            elif cm == 'invmag':      # sign bit7, but active-low MAGNITUDE (127-mag)
                m = (~(l3 & 0x7F)) & 0x7F
                signed = -m if (l3 & 0x80) else m
            elif cm == 'twos':        # lane3 as 8-bit two's complement (not sign-mag)
                signed = l3 - 256 if (l3 & 0x80) else l3
            else:
                signed = st['coeff']
            mag = abs(signed)
            Cs = -(mag >> coeff_shift) if signed < 0 else (mag >> coeff_shift)
            wa = st['WA']
            do_write = not (wa3_nowrite and wa == 3)
            if write_first:
                if do_write: R[wa] = dab
                x = R[pick(st)]
            else:
                x = R[pick(st)]
                if do_write: R[wa] = dab
            if st['ZERO'] and not zero_after:
                ACC = 0.0
            ACC = ACC + x*gain_num*Cs/gain_den
            res_old = RES
            if st['XFER']:
                RES = ACC/res_div
            if st['ZERO'] and zero_after:
                ACC = 0.0
            if st['b3'] and not sup:
                DM[addr] = (res_old if b3_write == 'pre' else RES); nz.add(addr)
        if (n+1) % K == 0:
            s = math.sqrt(ACC*ACC + RES*RES + sum(v*v for v in R)
                          + sum(DM[i]*DM[i] for i in nz)) + 1e-300
            logs.append(math.log(s)); f = 1.0/s
            R = [v*f for v in R]; ACC *= f; RES *= f
            for i in nz:
                DM[i] *= f
    tail = logs[len(logs)//3:]
    return math.exp(sum(tail)/len(tail)/K) if tail else float('nan')


def ppm(l):
    return (l-1)*1e6


def main():
    prog = A.load_microcode(0x01)
    base = lam(prog)
    print(f"BASELINE (committed model): lambda={base:.7f}  {ppm(base):+.1f} ppm  "
          f"{'GROW' if base > 1 else 'DECAY'}\n")
    print(f"{'#':>3} {'ASSUMPTION (alternative tested)':52} {'lambda':>11} {'ppm':>10}  verdict")
    print("-"*92)

    # candidate alternative picks (RA / field-bit assignments)
    picks = {
        'RA=(b5,b4) [current]': DEFAULT_PICK,
        'RA=(b5,b3)':  lambda st: (st['b5']<<1)|st['b3'],
        'RA=(b4,b3)':  lambda st: (st['b4']<<1)|st['b3'],
        'RA=(b4,b5)':  lambda st: (st['b4']<<1)|st['b5'],
        'RA=(b3,b4)':  lambda st: (st['b3']<<1)|st['b4'],
        'RA=(b3,b5)':  lambda st: (st['b3']<<1)|st['b5'],
        'RA=WA(b1,b0)': lambda st: st['WA'],
    }

    # build the FPC-output suppress set candidates (steps that look like FPC writes, NOT closers)
    # closer = XFER and b3 (recirculation); pure-output candidate = WA==3 + bit15 + NOT(XFER and b3)
    fpc_out = frozenset(p['s'] for p in prog
                        if (p['offset'] & 0x8000) and p['WA'] == 3 and not (p['XFER'] and p['b3']))
    fpc_all15 = frozenset(p['s'] for p in prog if (p['offset'] & 0x8000) and not (p['XFER'] and p['b3']))

    tests = []
    # ---- COEFFICIENT DECODE (most likely "one wrong structural assumption": a designed
    # reverb decays by DESIGN in its coefficients, so a sign/inversion decode error on lane3
    # would flip the whole loop from regenerative to decaying). These are NOT covered by the
    # multiply test vectors. ----
    tests += [
        ("COEFF sign inverted (bit7=0 -> negative)",  dict(coeff_mode='siginv')),
        ("COEFF lane3 active-low (~l3) sign-mag",     dict(coeff_mode='inv')),
        ("COEFF active-low magnitude (127-mag)",      dict(coeff_mode='invmag')),
        ("COEFF lane3 as 8-bit two's complement",     dict(coeff_mode='twos')),
    ]
    for name, pk in list(picks.items())[1:]:
        tests.append((f"RA/register decode: {name}", dict(pick=pk)))
    tests += [
        ("coeff width: Cs=mag (7-bit, no >>1)",      dict(coeff_shift=0)),
        ("coeff width: Cs=mag>>2 (5-bit)",           dict(coeff_shift=2)),
        ("operand align: x<<2 (not <<3)",            dict(operand_shift=2)),
        ("operand align: x<<4 (not <<3)",            dict(operand_shift=4)),
        ("RES shift: ACC>>2 (not >>3)",              dict(res_shift=2)),
        ("RES shift: ACC>>4 (not >>3)",              dict(res_shift=4)),
        ("prod shift: >>5 (looser gain)",            dict(prod_shift=5)),
        ("prod shift: >>7 (tighter gain)",           dict(prod_shift=7)),
        ("addr direction: pos+offset (not pos-)",    dict(addr_plus=True)),
        ("b3 read source: DM[addr] (not RES)",       dict(b3_read='DM')),
        ("b3 write timing: pre-XFER RES",            dict(b3_write='pre')),
        ("register file: write-before-read",         dict(write_first=True)),
        ("ZERO: clear AFTER the MAC",                dict(zero_after=True)),
        ("WA=3: pass-through (no R[3] write)",        dict(wa3_nowrite=True)),
        ("state: reset R/ACC/RES each sample",       dict(reset_per_sample=True)),
        ("DMEM: bit15=FPC, suppress non-closer outs", dict(suppress=fpc_out)),
        ("DMEM: bit15=FPC, suppress ALL non-closers", dict(suppress=fpc_all15)),
    ]

    candidates = []
    for i, (name, opts) in enumerate(tests, 1):
        try:
            l = lam(prog, **opts)
        except Exception as e:
            print(f"{i:>3} {name:52} {'ERR':>11} {str(e)[:20]}")
            continue
        decay = l < 1.0
        verdict = "*** CANDIDATE (DECAY) ***" if decay else ("eliminated" if l > 1 else "neutral")
        if decay:
            candidates.append((name, l))
        print(f"{i:>3} {name:52} {l:>11.7f} {ppm(l):>+10.1f}  {verdict}")

    print("-"*92)
    if candidates:
        print(f"\n{len(candidates)} CANDIDATE(S) that flip to decay:")
        for name, l in candidates:
            print(f"   {name}: lambda={l:.7f} ({ppm(l):+.1f} ppm)")
    else:
        print("\nNO single assumption-flip yields decay. The over-unity survives every single-"
              "\nassumption alternative -> consistent with a DISTRIBUTED/physical loss, not one"
              "\nwrong structural assumption. (FPC-output suppress sets printed above.)")
    print(f"\nFPC pure-output candidate steps (suppressed in test 'non-closer outs'): {sorted(fpc_out)}")


if __name__ == '__main__':
    main()
