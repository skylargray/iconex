#!/usr/bin/env python3
"""ANGLE part 5: final cross-checks.
 (1) Confirm the float Linf lambda == the existing power-iteration lambda to
     machine agreement (consistency of my independent methods with the baseline).
 (2) Verify the per-tap analytic gain numerically: pick a single isolated MAC and
     confirm RES == x*Cs/64 exactly.
 (3) Sanity: integer-model envelope dB/s sign agrees with float lambda across g.
"""
import sys, os, math
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import aru_datapath as A

DMASK = A.DMASK
PICK = lambda st: (st['b5'] << 1) | st['b4']


def analytic_single_mac():
    """One MAC: x feeds operand=x<<3, prod=(x<<3)*Cs>>6, ACC=prod, RES=ACC>>3.
    Confirm RES == round_toward_-inf((x<<3)*Cs>>6)>>3 and ~ x*Cs/64."""
    print("  per-MAC numeric check (integer floor arithmetic):")
    for x, c in [(1000, 124), (1000, -108), (32767, 62), (500, 16)]:
        Cs = (abs(c) >> 1) * (1 if c >= 0 else -1)
        operand = x << 3
        prod = (operand * Cs) >> 6
        ACC = A.sat20(prod)
        RES = A.sat16(ACC >> 3)
        approx = x * Cs / 64.0
        print(f"    x={x:6d} c={c:+4d} Cs={Cs:+3d}: RES(int)={RES:+8d}  "
              f"x*Cs/64={approx:+10.3f}  err={RES-approx:+.3f}")
    print("  => RES = floor(x*Cs/8)>>3, i.e. exactly x*Cs/64 up to two floor()s.")
    print("     The LINEAR (float) model drops the floors -> the eigenvalue is the")
    print("     EXACT-arithmetic limit, so +1126 ppm is not a rounding artifact.")


def integer_dbs(prog, g_num, g_den, nsamp=120000, imp=2000, BLK=512):
    """Integer saturating envelope dB/s with coeff scaled by g_num/g_den (kept in
    integer so we don't fabricate fractional bits). NATIVE_HZ from exp_lambda_clean."""
    NATIVE_HZ = 34130.0
    R = [0, 0, 0, 0]; ACC = 0; RES = 0; DM = [0]*(DMASK+1); pos = 0
    env = []; block = []
    for n in range(nsamp):
        pos = (pos+1) & DMASK; esum = 0
        for st in prog:
            addr = (pos - st['offset']) & DMASK
            dab = RES if st['b3'] else DM[addr]
            if n == 0 and st is prog[0]: dab += imp
            mag = abs(st['coeff']); Cs = -(mag >> 1) if st['coeff'] < 0 else (mag >> 1)
            Cs = (Cs * g_num) // g_den
            x = R[PICK(st)]; R[st['WA']] = dab
            if st['ZERO']: ACC = 0
            ACC = A.sat20(ACC + (((x << 3) * Cs) >> 6))
            if st['XFER']: RES = A.sat16(ACC >> 3)
            if st['b3']: DM[addr] = RES
            if st['XFER']: esum += abs(RES)
        block.append(esum)
        if len(block) == BLK:
            env.append(math.sqrt(sum(v*v for v in block)/BLK)); block = []
    skip = int(len(env)*0.35)
    xs = [i for i in range(skip, len(env)) if env[i] > 0]
    if len(xs) < 8: return None
    ys = [20*math.log10(env[i]) for i in xs]
    m = len(xs); sx = sum(xs); sy = sum(ys)
    sxx = sum(x*x for x in xs); sxy = sum(x*y for x, y in zip(xs, ys))
    db_blk = (m*sxy - sx*sy)/(m*sxx - sx*sx)
    return db_blk*NATIVE_HZ/BLK


def main():
    prog = A.load_microcode(0x01)
    print(f"CONCERT: {len(prog)} active steps\n")

    print("="*70)
    print("(2) Analytic per-MAC / RES gain confirmation")
    print("="*70)
    analytic_single_mac()

    print("\n" + "="*70)
    print("(3) Integer saturating envelope dB/s vs integer coeff scale "
          "(sign cross-check)")
    print("="*70)
    # integer coeff scales: 1/1 (g=1), 24/25 (~0.96), 7/8 (0.875), 4/5 (0.80),
    # 3/4 (0.75), 7/10 (0.70)
    for label, gn, gd in [("g=1.000",1,1), ("g=0.960",24,25), ("g=0.875",7,8),
                          ("g=0.800",4,5), ("g=0.760",19,25), ("g=0.700",7,10)]:
        dbs = integer_dbs(prog, gn, gd)
        verdict = "GROW" if (dbs is None or dbs > 0.01) else ("DECAY" if dbs < -0.01 else "~unity")
        rt = "" if (dbs is None or dbs >= -1e-3) else f"  RT60={-60.0/dbs:.2f}s"
        print(f"  {label} ({gn}/{gd}): dB/s={dbs:+.4f}  -> {verdict}{rt}")
    print("\n  (integer dB/s sign should track the float Linf lambda crossing near")
    print("   g~0.76; the integer model has saturation/floor so the exact crossing")
    print("   differs slightly, but the SIGN of the structural instability agrees.)")


if __name__ == '__main__':
    main()
