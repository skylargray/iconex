#!/usr/bin/env python3
"""Batch-run the parameter sweep over a set of programs (one JSON per program).

Usage:  python tools/batch_sweep.py <comma-separated hex ids>
        python tools/batch_sweep.py 0x01,0x02,0x81,0x08,0x10
"""
import sys, os, json
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import param_sweep as P

OUT = os.path.join(os.path.dirname(__file__), '..', 'docs', 'reference', '224')


def main():
    ids = [int(x, 16) for x in sys.argv[1].split(',')]
    for pid in ids:
        try:
            r = P.sweep(pid, 6)
            path = os.path.join(OUT, f'224XL_param_sweep_{pid:02x}.json')
            with open(path, 'w') as f:
                json.dump(r, f, indent=1)
            npar = sum(1 for p in r['params'] if p['coeff_steps'] or p['delay_steps'])
            print(f"done 0x{pid:02x}: {npar} active params, modulated={r['modulated_steps']}", flush=True)
        except Exception as e:
            print(f"FAIL 0x{pid:02x}: {type(e).__name__}: {e}", flush=True)


if __name__ == '__main__':
    main()
