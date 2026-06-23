#!/usr/bin/env python3
"""Converged structural-lambda measurement (audit of exp_eig.power_iter).

exp_eig.power_iter gives nsamp-dependent answers (0.9998 @ 8k, 1.0006 @ 20k) ->
it has NOT converged, so its absolute GROW/DECAY verdict is unreliable. This uses
a PROPER L2 state norm (R, ACC, RES, full DM) renormalized every K samples, and
reports the per-sample growth of the LAST window (converged tail) plus the whole
trajectory so convergence is visible. Cross-checks against the directly-observed
integer envelope slope (no eigenvalue assumptions).
"""
import sys, os, math
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import aru_datapath as A

DMASK = A.DMASK
NATIVE_HZ = 34130.0
PICK = lambda st: (st['b5'] << 1) | st['b4']


def lambda_trajectory(prog, pick=PICK, nsamp=60000, K=128, seed=1e4):
    """Float-exact linear map, proper L2 norm renorm every K samples.
    Returns list of (sample, lambda_window) showing convergence of the per-sample
    growth measured over each K-sample window."""
    R = [0.0]*4; ACC = 0.0; RES = 0.0
    DM = [0.0]*(DMASK+1); pos = 0
    nz = set()
    seeded = False
    traj = []
    win_log = 0.0
    for n in range(nsamp):
        pos = (pos+1) & DMASK
        for st in prog:
            addr = (pos - st['offset']) & DMASK
            dab = RES if st['b3'] else DM[addr]
            if not seeded and st is prog[0]:
                dab += seed; seeded = True
            mag = abs(st['coeff']); Cs = -(mag>>1) if st['coeff']<0 else (mag>>1)
            x = R[pick(st)]; R[st['WA']] = dab
            if st['ZERO']: ACC = 0.0
            ACC = ACC + x*8.0*Cs/64.0
            if st['XFER']: RES = ACC/8.0
            if st['b3']: DM[addr] = RES; nz.add(addr)
        if (n+1) % K == 0:
            s = math.sqrt(ACC*ACC + RES*RES + sum(v*v for v in R)
                          + sum(DM[i]*DM[i] for i in nz)) + 1e-300
            # growth over this window = log(s / 1.0) since we renormalize to 1.0
            win_log = math.log(s)
            lam_win = math.exp(win_log / K)
            traj.append((n+1, lam_win))
            f = 1.0 / s
            R = [v*f for v in R]; ACC *= f; RES *= f
            for i in nz: DM[i] *= f
    return traj


def integer_envelope_slope(prog, pick=PICK, nsamp=120000, imp=200, BLK=512):
    """Ground-truth: saturating integer model, small impulse, dB/s of the envelope.
    No eigenvalue assumptions -- this is what the model actually does."""
    R = [0,0,0,0]; ACC = 0; RES = 0; DM = [0]*(DMASK+1); pos = 0
    block = []; env = []
    for n in range(nsamp):
        pos = (pos+1) & DMASK; esum = 0
        for st in prog:
            addr = (pos - st['offset']) & DMASK
            dab = RES if st['b3'] else DM[addr]
            if n == 0 and st is prog[0]: dab += imp
            mag = abs(st['coeff']); Cs = -(mag>>1) if st['coeff']<0 else (mag>>1)
            x = R[pick(st)]; R[st['WA']] = dab
            if st['ZERO']: ACC = 0
            ACC = A.sat20(ACC + (((x<<3)*Cs) >> 6))
            if st['XFER']: RES = A.sat16(ACC >> 3)
            if st['b3']: DM[addr] = RES
            if st['XFER']: esum += abs(RES)
        block.append(esum)
        if len(block) == BLK:
            env.append(math.sqrt(sum(v*v for v in block)/BLK)); block = []
    skip = int(len(env)*0.3)
    xs = [i for i in range(skip, len(env)) if env[i] > 0]
    if len(xs) < 8: return None, max(env) if env else 0, env
    ys = [20*math.log10(env[i]) for i in xs]
    m = len(xs); sx = sum(xs); sy = sum(ys); sxx = sum(x*x for x in xs); sxy = sum(x*y for x, y in zip(xs, ys))
    db_blk = (m*sxy - sx*sy)/(m*sxx - sx*sx)
    return db_blk*NATIVE_HZ/BLK, max(env), env


def main():
    prog = A.load_microcode(0x01)
    print("=== converged-lambda trajectory (proper L2 norm) ===")
    traj = lambda_trajectory(prog, nsamp=60000, K=128)
    # show a coarse trajectory + the converged tail (median of last 50 windows)
    pts = traj[::max(1, len(traj)//20)]
    for n, lam in pts:
        print(f"  n={n:6d}  lambda_window={lam:.7f}  ppm={(lam-1)*1e6:+.1f}")
    tail = sorted(l for _, l in traj[-60:])
    med = tail[len(tail)//2]
    print(f"\n  CONVERGED lambda (median of last 60 windows) = {med:.7f}  "
          f"({'GROW' if med>1 else 'DECAY'}, {(med-1)*1e6:+.1f} ppm)")
    print(f"  target = 0.9999899")

    print("\n=== ground-truth integer envelope (small impulse, no eig assumptions) ===")
    dbs, pk, env = integer_envelope_slope(prog, nsamp=120000)
    rt = (-60.0/dbs) if (dbs and dbs < -1e-4) else float('inf')
    print(f"  integer dB/s = {dbs:+.5f}  peakEnv={pk:.0f}  "
          f"RT60={'inf (sustain/grow)' if rt==float('inf') else f'{rt:.2f}s'}")
    print(f"  (lambda 0.99980 would imply RT60 ~ 1.0 s; sustain implies lambda ~ 1.0+)")


if __name__ == '__main__':
    main()
