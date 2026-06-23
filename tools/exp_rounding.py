#!/usr/bin/env python3
"""Diagnostic: is the CONCERT growth a STRUCTURAL instability (lambda>1) or a
floor-truncation LIMIT CYCLE (rounding-mode / amplitude dependent)?

Parametrized run() with selectable rounding at the two shift points:
  prod = round_q(operand * Cs, 6)     (multiplier output / acc input)
  RES  = sat16(round_q(ACC, 3))       (result register transfer)

Rounding modes:
  'floor'  : >>k                       (toward -inf; the current model)
  'near'   : (x + 2^(k-1)) >> k        (round half up / to +inf)
  'nearest': round-half-to-even        (unbiased)
  'zero'   : trunc toward zero         (sign-magnitude truncation)

We compare growth/decay across modes and impulse amplitudes to localize the cause.
"""
import sys, os, math
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import aru_datapath as A

DMASK = A.DMASK


def shift_round(x, k, mode):
    if k == 0:
        return x
    if mode == 'floor':
        return x >> k
    if mode == 'near':                       # round half toward +inf
        return (x + (1 << (k - 1))) >> k
    if mode == 'zero':                        # truncate toward zero (sign-magnitude)
        if x >= 0:
            return x >> k
        return -((-x) >> k)
    if mode == 'nearest':                     # round half to even (unbiased)
        q, r = divmod(x, 1 << k)              # python divmod floors; r in [0,2^k)
        half = 1 << (k - 1)
        if r > half or (r == half and (q & 1)):
            q += 1
        return q
    raise ValueError(mode)


def run_r(prog, pick, nsamp, imp, prod_mode='floor', res_mode='floor'):
    R = [0, 0, 0, 0]; ACC = 0; RES = 0
    DM = [0] * (DMASK + 1); pos = 0; out = []
    for n in range(nsamp):
        pos = (pos + 1) & DMASK
        esum = 0
        for st in prog:
            addr = (pos - st['offset']) & DMASK
            dab = RES if st['b3'] else DM[addr]
            if n == 0 and st is prog[0]:
                dab += imp
            mag = abs(st['coeff']); csign = st['coeff'] < 0
            Cs = -(mag >> 1) if csign else (mag >> 1)
            ra = pick(st); x = R[ra]; R[st['WA']] = dab
            if st['ZERO']:
                ACC = 0
            operand = x << 3
            prod = shift_round(operand * Cs, 6, prod_mode)
            ACC = A.sat20(ACC + prod)
            if st['XFER']:
                RES = A.sat16(shift_round(ACC, 3, res_mode))
            if st['b3']:
                DM[addr] = RES
            if st['XFER']:
                esum += abs(RES)
        out.append(esum)
    return out


def growth_segments(esum):
    """Local ln-slope over first / middle / last thirds -> amplitude dependence."""
    n = len(esum)
    def slope(lo, hi):
        xs = [i for i in range(lo, hi) if esum[i] > 0]
        if len(xs) < 5:
            return None
        ys = [math.log(esum[i]) for i in xs]
        m = len(xs); sx = sum(xs); sy = sum(ys)
        sxx = sum(x * x for x in xs); sxy = sum(x * y for x, y in zip(xs, ys))
        return (m * sxy - sx * sy) / (m * sxx - sx * sx)
    t = n // 3
    return slope(0, t), slope(t, 2 * t), slope(2 * t, n)


def report(label, esum):
    pk = max(esum); npk = esum.index(pk)
    s1, s2, s3 = growth_segments(esum)
    def f(s): return f"{s:+.3e}" if s is not None else "  n/a  "
    print(f"  {label:<34} peak={pk:>7}@{npk:<6} last={esum[-1]:>7}  "
          f"slope[lo/mid/hi]={f(s1)} {f(s2)} {f(s3)}")


def main():
    nsamp = int(sys.argv[1]) if len(sys.argv) > 1 else 20000
    prog = A.load_microcode(0x01)
    pick = lambda st: (st['b5'] << 1) | st['b4']
    print(f"CONCERT {len(prog)} steps; nsamp={nsamp}\n")
    print("slope = ln(lambda) per sample; >0 grows, <0 decays. "
          "amplitude-independent slope => structural; varying => quantization.\n")

    print("[A] baseline floor/floor, vary impulse amplitude (structural test):")
    for imp in (200, 2000, 20000):
        report(f"floor/floor imp={imp}", run_r(prog, pick, nsamp, imp, 'floor', 'floor'))

    print("\n[B] rounding-mode sweep at imp=20000 (lever test):")
    for pm in ('floor', 'near', 'zero', 'nearest'):
        for rm in ('floor', 'near', 'zero', 'nearest'):
            report(f"prod={pm} res={rm}", run_r(prog, pick, nsamp, 20000, pm, rm))


if __name__ == '__main__':
    main()
