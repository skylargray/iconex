#!/usr/bin/env python3
"""Is the +1126 ppm excess CONCERT-specific or systematic across all programs?

A uniform missing per-pass loss would shift EVERY program's lambda by ~the same
amount, flipping only the near-unity (long) programs from decay to growth while
short programs still decay (just a bit too long). A CONCERT-specific topology bug
would leave other programs correct. Measures converged structural lambda for a
spread of programs of different nominal decay lengths.
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import aru_datapath as A
from exp_lambda_clean import lambda_trajectory

PROGS = [
    (0x01, "CONCERT HALL (~20s default)"),
    (0x20, "BRIGHT HALL"),
    (0x05, "DARK HALL"),
    (0x02, "PLATE"),
    (0x08, "CHAMBER"),
    (0x40, "SMALL ROOM (short)"),
    (0x81, "INVERSE ROOM"),
]


def conv_lambda(prog, nsamp=40000, K=128, tail=40):
    traj = lambda_trajectory(prog, nsamp=nsamp, K=K)
    vals = sorted(l for _, l in traj[-tail:])
    return vals[len(vals)//2]


def main():
    print("converged structural lambda by program (target: all should DECAY, <1):\n")
    print(f"  {'id':>4} {'name':28} {'#steps':>6} {'lambda':>11}   verdict")
    for pid, name in PROGS:
        try:
            prog = A.load_microcode(pid)
        except Exception as e:
            print(f"  0x{pid:02x} {name:28} boot/load FAILED: {e}")
            continue
        lam = conv_lambda(prog)
        v = 'GROW' if lam > 1 else 'DECAY'
        print(f"  0x{pid:02x} {name:28} {len(prog):>6} {lam:.7f}   {v} ({(lam-1)*1e6:+.0f} ppm)")


if __name__ == '__main__':
    main()
