#!/usr/bin/env python3
"""E1c-prep (plan 023) — resolve the PHYSICAL bit-level MAC back-end from the traced wiring.

The traced back-end (netlist §4.3/4.5/4.6/4F.8): B(adder) = PR XOR sub-ctrl (rail commoned),
sub-ctrl = inv(CSIGN/), carry-in = inv(sub-ctrl) = CSIGN/; PR = front-end comb_array output
("active-low" per §4F.9); ACC D = PP = sat-mux(adder Σ); result reg D = PP3..18 (§4.2/§4.8) —
a pure bit TAP, no rounding adder exists on the capture path.

The ENGINE's value model (golden-anchored E83 via aru_post/aru_booth.multiply) is
    RES = sat16((-Σraw + 3·dual + 4) >> 3)          [positive], and
    RES_neg = -RES_pos - 1                           [the POST -M-1 law],
where the '+4 round' and '+3 dual' are VALUE-level bookkeeping with no traced gate. The
free-run engine (product20 + res_from_acc) further applies (v+4)>>3 UNIFORMLY, which
DISAGREES with -M-1 by 1 LSB on lone negative products (untested by any prior oracle).

This probe enumerates the bit-level variant space and scores each against the 20 firmware
E83 goldens (the strongest hardware anchor), asking: WHICH physical bit convention makes
the traced adder chain + bit-tap reproduce the goldens by pure truncation?

Variant space:
  rail(cs)   : sub-ctrl level as function of cs_eff (1=pos): rail = cs  |  rail = 1-cs
  cin        : inv(rail) [traced]  |  rail  [anti-traced control]
  PRLOAD     : PR register bits = raw  |  ~raw      (raw = comb_array output)
  CLR        : ZERO clear state = 0x00000 | 0xFFFFF
  DUAL3      : +3 injected per dual-rail phase into the accumulate sum: no | yes
Golden semantics: clear -> accumulate phase A, phase B (registered) -> CAPTURE with phase C
on the PP bus (the 0024 PP-bus capture); readback = signed16 of PP bits 3..18; SAT-mux clamp
per §4.4/§4.5 (SAT = sum19 XOR sum18; clamp PP0-17=~topB, PP18=PP19=topB, topB=xorB bit19).
"""
import sys, os
from itertools import product as iproduct

TOOLS = r"d:\OneDrive\Gray Instruments\iconex\tools"
sys.path.insert(0, TOOLS)

import aru_booth as B

MASK20 = 0xFFFFF


def s16(v):
    v &= 0xFFFF
    return v - 0x10000 if v & 0x8000 else v


def raw_phases(F, cmag):
    """The three comb_array outputs (active-low front-end sums) + dual flags."""
    C = [(cmag >> i) & 1 for i in range(6)]
    SR = B.load_SR(s16(F))
    out = []
    for p, (m0, m1) in enumerate([(C[4], C[5]), (C[2], C[3]), (C[0], C[1])]):
        if p > 0:
            SR = B.shift_right2(SR)
        out.append((B.comb_array(SR, m0, m1), m0 and m1))
    return out


def backend_sum(acc_bits, pr_bits, rail, cin, dual3, dual):
    """One adder/sat-mux evaluation: returns (PP 20-bit, SAT flag). rail/cin are levels."""
    xorb = pr_bits ^ (MASK20 if rail else 0)
    s = acc_bits + xorb + cin + (3 if (dual3 and dual) else 0)
    s &= MASK20
    b19 = (s >> 19) & 1
    b18 = (s >> 18) & 1
    sat = b19 ^ b18
    if sat:
        topb = (xorb >> 19) & 1
        pp = (topb << 19) | (topb << 18) | ((MASK20 >> 2) if not topb else 0)
        # PP0-17 = ~topB (all-ones if topB=0), PP18=PP19=topB
    else:
        pp = s
    return pp, sat


def run_golden(F, cmag, cs, variant):
    """Single multiply: clear -> +A -> +B (registered) -> capture PP with C on the bus."""
    railf, cinf, prload, clrval, dual3 = variant
    rail = cs if railf == "cs" else 1 - cs
    cin = (1 - rail) if cinf == "inv" else rail
    acc = clrval
    ph = raw_phases(F, cmag)
    for k in (0, 1):                                    # phases A, B register into ACC
        raw, dual = ph[k]
        pr = raw if prload == "raw" else (~raw) & MASK20
        pp, _ = backend_sum(acc, pr, rail, cin, dual3, dual)
        acc = pp
    raw, dual = ph[2]                                   # phase C on the PP bus at capture
    pr = raw if prload == "raw" else (~raw) & MASK20
    pp, sat = backend_sum(acc, pr, rail, cin, dual3, dual)
    return s16((pp >> 3) & 0xFFFF), sat


def main():
    variants = list(iproduct(("cs", "inv_cs"), ("inv", "rail"),
                             ("raw", "inv_raw"), (0x00000, 0xFFFFF), (False, True)))
    print(f"enumerating {len(variants)} bit-level variants x 2 bus domains "
          f"against the 20 E83 goldens ...")
    results = []
    for dom in ("direct", "complement"):
        for v in variants:
            ok = 0
            miss = []
            for F, cmag, cs, exp in B.GOLDENS:
                if dom == "complement":
                    # physical DAB carries ~value (DATA0-7/ bridge): operand into the
                    # regfile/shifter = ~F; the CPU reads back ~(result-reg bits).
                    got_phys, sat = run_golden((~F) & 0xFFFF, cmag, cs, v)
                    got = s16((~got_phys) & 0xFFFF)
                else:
                    got, sat = run_golden(F, cmag, cs, v)
                if got == exp:
                    ok += 1
                else:
                    miss.append((F & 0xFFFF, cmag, cs, exp, got))
            results.append((ok, dom, v, miss))
    results.sort(key=lambda r: -r[0])
    for ok, dom, v, miss in results[:10]:
        rail, cin, pr, clr, d3 = v
        print(f"  {ok:2d}/20  dom={dom:10s} rail={rail:6s} cin={cin:4s} PR={pr:7s} "
              f"CLR=0x{clr:05X} dual3={d3}")
        if 14 <= ok < 20:
            for m in miss[:6]:
                print(f"        MISS F=0x{m[0]:04X} cmag={m[1]} cs={m[2]} exp={m[3]:+d} "
                      f"got={m[4]:+d} (d={m[4]-m[3]:+d})")
    winners = [(ok, dom, v) for ok, dom, v, _ in results if ok == 20]
    print(f"\nvariants at 20/20: {len(winners)}")
    for ok, dom, v in winners:
        print(f"  *** dom={dom} {v}")


if __name__ == "__main__":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass
    main()
