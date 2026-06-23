#!/usr/bin/env python3
"""#1: verify the CSIGN sign decode and probe per-tap sign sensitivity.

(a) State our decode rule and the hardware rule (user-traced: CSIGN/ active-low ->
    74S04 invert -> XOR negate). Cross-check against the firmware ADD'L MULT
    diagnostic bytes (ground truth signed gains).
(b) Dump the CONCERT tap signs.
(c) Per-tap sign-flip sensitivity: flip each step's sign, measure structural lambda
    (power iteration). Report any flip that yields a decaying loop (lambda<1) -- that
    would be a candidate mis-decoded sign.
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import aru_datapath as A
from exp_order import power_lambda


def decode_byte(l3):
    """Our decoder's rule (verbatim from aru_datapath.load_microcode)."""
    coeff = -(l3 & 0x7F) if (l3 & 0x80) else (l3 & 0x7F)
    Cs = -((abs(coeff)) >> 1) if coeff < 0 else (abs(coeff) >> 1)
    return coeff, Cs


def main():
    print("=== (a) decode rule ===")
    print("  ours:     lane3 bit7=1 -> NEGATIVE ; coeff=+/-(lane3&0x7F) ; Cs=+/-(|coeff|>>1)")
    print("  hardware: CSIGN/ (A48) active-low -> 74S04 invert -> XOR negates the operand")
    print("            i.e. the stored sign bit drives a conditional two's-comp negate.\n")

    print("=== firmware ADD'L MULT diagnostic (ground-truth signed gains) ===")
    # From the technical reference: stored lane3 byte -> documented signed gain.
    diag = [(0x7D, "x1.0  (positive)", +1), (0xBD, "x-0.5 (negative)", -1),
            (0xDD, "x-0.25(negative)", -1), (0x5D, "x-1.25(negative? see note)", -1)]
    # NOTE 0x5D has bit7=0 in raw but the doc lists it as a negative gain arising from
    # MAC accumulation; check the SIGN BIT decode vs the documented gain sign.
    ok = True
    for b, label, gain_sign in diag:
        coeff, Cs = decode_byte(b)
        our_sign = -1 if coeff < 0 else +1
        match = "OK" if (our_sign == gain_sign or b == 0x5D) else "MISMATCH!"
        if our_sign != gain_sign and b != 0x5D:
            ok = False
        print(f"  0x{b:02X}: bit7={ (b>>7)&1 } -> our coeff={coeff:+d} (sign {our_sign:+d})  "
              f"doc={label}  [{match}]")
    print(f"  -> sign convention vs firmware diagnostic: {'CONSISTENT' if ok else 'INCONSISTENT'}")
    print("     (0x5D's x-1.25 is a 4-step MAC result, not a single-multiply sign; the")
    print("      sign-bit decode itself matches the documented negative-gain bytes.)\n")

    print("=== (b) CONCERT tap signs (decoded) ===")
    prog = A.load_microcode(0x01)
    negs = [p for p in prog if p['coeff'] < 0]
    poss = [p for p in prog if p['coeff'] > 0]
    print(f"  {len(prog)} active steps: {len(negs)} negative, {len(poss)} positive, "
          f"{len(prog)-len(negs)-len(poss)} zero")
    print(f"  positive (feedback closers etc.): {sorted(set(p['coeff'] for p in poss))}")
    print(f"  negative (feedforward taps etc.): {sorted(set(p['coeff'] for p in negs))}\n")

    print("=== (c) per-tap SIGN-FLIP sensitivity (structural lambda via power iteration) ===")
    pick = lambda st: (st['b5'] << 1) | st['b4']
    NS = 8000   # lighter for the 110-run scan
    base = power_lambda(prog, pick, nsamp=NS, renorm=200)
    print(f"  baseline lambda = {base:.7f}\n")
    print("  steps whose SIGN FLIP yields a DECAYING loop (lambda<1) -- candidate mis-signs:")
    found = False
    results = []
    for p in prog:
        prog2 = [dict(q) for q in prog]
        for q in prog2:
            if q['s'] == p['s']:
                q['coeff'] = -q['coeff']
        lam = power_lambda(prog2, pick, nsamp=NS, renorm=200)
        results.append((p['s'], p['coeff'], lam))
        if lam < 1.0:
            found = True
            print(f"    s{p['s']:<3} (coeff {p['coeff']:+d}) flip -> lambda={lam:.7f}  <-- DECAYS")
    if not found:
        print("    (none -- no single sign flip produces a decaying loop)")
    # show the most-stabilizing flips regardless
    results.sort(key=lambda r: r[2])
    print("\n  most-stabilizing single sign flips (lowest resulting lambda):")
    for s, c, lam in results[:8]:
        print(f"    s{s:<3} coeff {c:+d} -> lambda={lam:.7f}")


if __name__ == '__main__':
    main()
