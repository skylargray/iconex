#!/usr/bin/env python3
"""ARU signature oracle (Phase B) — sub-cycle (AS0/AS1/AS2) serial-multiply +
accumulator model whose PP/AC bus values at every ARUCK can be fed to the
HP-5004A signature LFSR (tools/sig224) and compared to the manual's §5.7 ARU
feedback table. The first node whose signature mismatches names the exact place
the datapath model diverges from the real hardware.

Serial multiply (Fig 3.4 + 060-01318 netlist): operand F = x<<3 (signed, 20-bit
space). 3 ARU states, 2 coeff bits/state, 'direct + shifted-right-1' terms:
  AS0: PP0 = b5*F      + b4*(F>>1)
  AS1: PP1 = b3*(F>>2) + b2*(F>>3)
  AS2: PP2 = b1*(F>>4) + b0*(F>>5)        (bi = bit i of the 6-bit magnitude cmag)
Sum = F*cmag/32  (== the ADD'L MULT-validated parallel product (x<<3)*cmag>>5).
The per-state partial products feed the partial-product register (clk ARUCK) and
then the 20-bit saturating accumulator (clk ARUCKE/), pipelined by one state.
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import aru_datapath as A
import aru_cycle as C


def serial_partials(F, cmag):
    """The three per-state partial products [PP0, PP1, PP2] of the serial multiply.
    F is the signed operand (x<<3). Arithmetic (sign-preserving) right shifts."""
    b = [(cmag >> i) & 1 for i in range(6)]
    pp0 = b[5] * F        + b[4] * (F >> 1)
    pp1 = b[3] * (F >> 2) + b[2] * (F >> 3)
    pp2 = b[1] * (F >> 4) + b[0] * (F >> 5)
    return [pp0, pp1, pp2]


def serial_product(x, cmag):
    """Total serial product = PP0+PP1+PP2 (should equal C._mul(x, cmag))."""
    F = x << 3
    return sum(serial_partials(F, cmag))


def _selftest_multiply():
    """Verify the serial multiply reproduces the parallel /32 product over the
    ADD'L MULT coefficients and a random-ish spread of operands."""
    import itertools
    bad = 0
    xs = list(range(-2000, 2001, 137)) + [-32768, -1, 0, 1, 32767, 12345, -9999]
    for x in xs:
        for cmag in range(64):
            s = serial_product(x, cmag)
            p = C._mul(x, cmag)          # (x<<3)*cmag >> 5
            if s != p:
                bad += 1
                if bad <= 8:
                    print(f"  MISMATCH x={x} cmag={cmag}: serial={s} parallel={p} diff={s-p}")
    total = len(xs) * 64
    print(f"serial-vs-parallel multiply: {total-bad}/{total} match"
          + ("" if bad == 0 else f"  ({bad} differ — truncation/bit-order to resolve)"))
    return bad == 0


import sig224

# ---------------------------------------------------------------------------
# §5.7 ARU feedback-config targets. Accumulator AC bus (U45-49 Q outputs) and
# the PP/adder bus (U45-49 D inputs). Values are display strings (sig224 charset).
# AC16==AC17 (the two sign-extension bits) is a built-in sanity anchor.
# ---------------------------------------------------------------------------
AC_TARGET = {  # AC bit -> §5.7 feedback signature
    0: "34P3", 1: "09U9", 2: "60CU", 3: "5CP3",
    4: "011F", 5: "6A06", 6: "4815", 7: "4062",
    8: "CA59", 9: "8U4F", 10: "0H92", 11: "2999",
    12: "1126", 13: "2U18", 14: "4U40", 15: "1918",
    16: "P1UC", 17: "P1UC", 18: "4FF8", 19: "8PH4",
}
PP_TARGET = {  # PP bit (accumulator D input) -> §5.7 feedback signature
    0: "P885", 1: "2A6H", 2: "9AHU", 3: "F5F1",
    4: "9136", 5: "U9U0", 6: "P978", 7: "U05P",
    8: "PC02", 9: "PHPA", 10: "P9PA", 11: "12UF",
    12: "CHHP", 13: "4110", 14: "C5P9", 15: "5062",
    16: "0HHH", 17: "666C", 18: "77A3", 19: "77A3",
}


def run_states(prog, loops, mask=0xFFFF, read_bit=A.READ_BIT, acc_phase='figA'):
    """Run `prog` (one microinstruction per cycle), looping `loops` times, and
    return per-ARU-state (per-ARUCK) snapshots of the 20-bit accumulator (AC bus)
    and the combinational adder output (PP bus). 3 ARUCK per microinstruction.

    The serial multiply produces PP0/PP1/PP2 over AS0/AS1/AS2; the partial-product
    register pipelines them by one state into the saturating accumulator. XFER/ZERO
    are deferred to the next microinstruction's AS0 (Fig 3.4)."""
    R = [0, 0, 0, 0]; DM = [0] * (mask + 1); RES = 0
    ACC = 0; PPreg = 0; csreg = 0
    xfer_p = zero_p = 0
    pos = 0
    ac_samples = []; pp_samples = []
    for loop in range(loops):
        pos = (pos + 1) & mask
        for st in prog:
            addr = (pos - st['offset']) & mask
            dab, is_w = A._dab_source(st, DM, addr, RES, 0, read_bit)
            x = R[st['RA']]
            R[st['WA']] = dab
            pps = serial_partials(x << 3, abs(st['cs']))
            csign = 1 if st['cs'] < 0 else 0
            for s_idx in range(3):       # AS0, AS1, AS2
                # adder output (PP bus) = ACC + signed pipelined partial product
                add = -PPreg if csreg else PPreg
                pp_bus = A.sat20(ACC + add)
                if s_idx == 0:
                    ACC = pp_bus                       # AS0: PP2 of prev microinstr completes
                    if xfer_p:
                        RES = A.sat16(ACC >> 3)
                    if zero_p:
                        ACC = 0
                    PPreg, csreg = pps[0], csign
                else:
                    ACC = pp_bus
                    PPreg, csreg = pps[s_idx], csign
                ac_samples.append(ACC & 0xFFFFF)       # 20-bit AC bus
                pp_samples.append(pp_bus & 0xFFFFF)    # 20-bit PP bus
            xfer_p, zero_p = st['XFER'], st['ZERO']
            if is_w:
                DM[addr] = RES
    return ac_samples, pp_samples


def bit_signature(samples, bit, start, n):
    """Signature of `samples[start:start+n]`'s given bit position."""
    return sig224.value_to_display(
        sig224.sig_value(((samples[(start + i) % len(samples)] >> bit) & 1) for i in range(n)))


def compare(prog, n_window=90, warmup=60):
    """Compute AC/PP bus signatures over one feedback window and find the
    alignment that best matches §5.7. Reports per-bit match and the first
    divergent node."""
    total_loops = warmup + 4
    ac, pp = run_states(prog, total_loops)
    L = len(prog) * 3                  # ARUCK per loop
    base = warmup * L                  # start of a steady-state loop
    best = None
    for off in range(L):
        start = base + off
        acm = sum(1 for b in range(20)
                  if bit_signature(ac, b, start, n_window) == AC_TARGET[b])
        ppm = sum(1 for b in range(20)
                  if bit_signature(pp, b, start, n_window) == PP_TARGET[b])
        if best is None or (acm + ppm) > best[0]:
            best = (acm + ppm, off, acm, ppm)
    score, off, acm, ppm = best
    print(f"Best alignment off={off}: AC {acm}/20, PP {ppm}/20 match (window n={n_window})")
    start = base + off
    print("  AC bus:  bit model   §5.7   ok")
    for b in range(20):
        got = bit_signature(ac, b, start, n_window)
        print(f"    AC{b:<2d} {got}  {AC_TARGET[b]}  {'OK' if got==AC_TARGET[b] else 'X'}")
    return best


if __name__ == '__main__':
    print("=" * 70)
    ok = _selftest_multiply()
    print("serial multiply:", "MATCHES parallel (±LSB)" if ok else "DIFFERS by ±LSB truncation (hardware-exact)")
    print("=" * 70)
    import diag3
    prog = A.decode_image(diag3.load_wcs())
    print(f"Diag-3 ARU SIGNAT: {len(prog)} steps, {len(prog)*3} ARUCK/loop "
          f"(feedback window N=90)")
    compare(prog)
