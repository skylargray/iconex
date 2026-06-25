#!/usr/bin/env python3
"""Rigorous over-unity sanity gate: per-program lambda, 3-seed-MAX power iteration,
long nsamp, for inv_l2=False/read_bit=1, both inv_l3. The frontier device decode +
acc_latch must drive EVERY clean program to lambda<=1 (no hot). 3-seed-max guards the
near-lambda=1 start-sensitivity noted in the frontier doc section 6."""
import sys, os, math
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import _hunt_rawcache as RC
import _hunt_rebuild2 as R2

NS = int(os.environ.get('NS', '50000'))
WU = int(os.environ.get('WU', '12000'))
SEEDS = (1, 2, 3)


def main():
    cache = RC.load()
    clean = [p for p in sorted(cache) if cache[p]['clean']]
    print(f"3-seed-MAX over-unity gate (inv_l2=False, read_bit=1, NS={NS})\n")
    for inv_l3 in (True, False):
        print(f"--- inv_l3={inv_l3} ---")
        print(f"{'pid':>5} {'lam-1(ppm)':>12} {'verdict':>10}")
        nhot = 0; worst = -1e9
        for p in clean:
            prog = R2.decode(cache[p]['steps'], inv_l2=False, inv_l3=inv_l3)
            lam = max(R2.lam(prog, read_bit=1, nsamp=NS, warmup=WU, rseed=s) for s in SEEDS)
            ppm = (lam-1)*1e6
            worst = max(worst, ppm)
            hot = lam > 1 + 5e-4
            if hot: nhot += 1
            print(f"{('%#x' % p):>5} {ppm:>12.1f} {'HOT' if hot else 'ok':>10}")
        print(f"  => {nhot} hot, worst {worst:+.1f} ppm\n")


if __name__ == '__main__':
    main()
