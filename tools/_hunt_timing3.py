#!/usr/bin/env python3
"""LEAD 2 part 3: ROBUST cross-hall timing sweep with RANDOM-START power iteration.

The single-seed lambda (exp_lambda_clean) injects at prog[0]; for halls whose prog[0]
does not couple to the tank the energy dissipates and lambda hits the renorm floor
(0.0045316 = exp(log(1e-300)/128)) -- a measurement artifact, NOT a dead tank. This
re-measures every hall under every timing variant with a RANDOM initial state (all
registers + RES + a warmup that lets energy populate DM), so power iteration converges
to the true dominant eigenvalue regardless of injection point. Multiple random seeds
guard against an unlucky start being orthogonal to the dominant mode.
"""
import sys, os, math, random
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import aru_datapath as A
DMASK = A.DMASK
PICK = lambda st: (st['b5'] << 1) | st['b4']
FLOOR = math.exp(math.log(1e-300)/128)   # 0.0045316 -- the artifact value


def lam_rand(prog, res_latch=False, acc_latch=False, reg_wbr=False, mac_pipe=False,
             nsamp=30000, K=128, warmup=4000, rseed=1):
    rng = random.Random(rseed)
    R = [rng.uniform(-1, 1) for _ in range(4)]
    ACC = rng.uniform(-1, 1); RES = rng.uniform(-1, 1)
    RESc = RES; ACCc = ACC; pend = 0.0
    DM = [0.0]*(DMASK+1); pos = 0
    nz = set(); traj = []
    for n in range(nsamp):
        pos = (pos+1) & DMASK
        for st in prog:
            addr = (pos - st['offset']) & DMASK
            mag = abs(st['coeff']); Cs = -(mag>>1) if st['coeff']<0 else (mag>>1)
            cf = 8.0*Cs/64.0
            res_for_b3 = RESc if res_latch else RES
            dab = res_for_b3 if st['b3'] else DM[addr]
            if reg_wbr:
                R[st['WA']] = dab; x = R[PICK(st)]
            else:
                x = R[PICK(st)]; R[st['WA']] = dab
            if st['ZERO']: ACC = 0.0
            if mac_pipe:
                ACC += pend; pend = x*cf
            else:
                ACC += x*cf
            xfer_src = (ACCc if acc_latch else ACC)
            if st['XFER']:
                newRES = xfer_src/8.0
                if res_latch:
                    if st['b3']: DM[addr] = res_for_b3; nz.add(addr)
                    RESc = newRES; RES = newRES
                else:
                    RES = newRES
                    if st['b3']: DM[addr] = RES; nz.add(addr)
            else:
                if st['b3']:
                    DM[addr] = res_for_b3 if res_latch else RES; nz.add(addr)
            if acc_latch: ACCc = ACC
        if (n+1) % K == 0:
            s = math.sqrt(ACC*ACC + RES*RES + RESc*RESc + ACCc*ACCc + pend*pend
                          + sum(v*v for v in R) + sum(DM[i]*DM[i] for i in nz)) + 1e-300
            if (n+1) > warmup:
                traj.append(math.exp(math.log(s)/K))
            f = 1.0/s
            R = [v*f for v in R]; ACC*=f; RES*=f; RESc*=f; ACCc*=f; pend*=f
            for i in nz: DM[i] *= f
    tail = sorted(traj[-60:])
    return tail[len(tail)//2] if tail else float('nan')


def best_lam(prog, **kw):
    """max over 2 random seeds (dominant mode = largest growth seen)."""
    return max(lam_rand(prog, rseed=1, **kw), lam_rand(prog, rseed=7, **kw))


def main():
    progs = {0x01: 'CONCERT', 0x02: 'BRIGHT', 0x03: 'DARK'}
    P = {p: A.load_microcode(p) for p in progs}
    combos = [dict(), {'res_latch': True}, {'acc_latch': True}, {'reg_wbr': True},
              {'acc_latch': True, 'reg_wbr': True},
              {'res_latch': True, 'reg_wbr': True},
              {'res_latch': True, 'acc_latch': True, 'reg_wbr': True}]
    def nm(c): return '+'.join(k for k in c) or 'base'
    print(f"=== ROBUST random-start lambda (ppm from 1.0), 2 seeds, warmup=4000 ===")
    print(f"    (floor artifact = {FLOOR:.6f}; shown as 'DEAD' if lambda<0.5)\n")
    hdr = f"{'variant':30s} " + "  ".join(f"{progs[p]:>12s}" for p in progs)
    print(hdr)
    for c in combos:
        cells = []
        for p in progs:
            l = best_lam(P[p], **c)
            if l < 0.5:
                cells.append(f"{l:9.4f}D")
            else:
                cells.append(f"{(l-1)*1e6:+9.1f}")
        print(f"{nm(c):30s} " + "  ".join(f"{x:>12s}" for x in cells))
    print("\n  A correct hardware timing should make ALL THREE halls converge to lambda<=~1")
    print("  (working reverbs), not just CONCERT. base/candidate compared above.")


if __name__ == '__main__':
    main()
