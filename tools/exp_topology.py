#!/usr/bin/env python3
"""Map the CONCERT tank topology: dump steps, find short-range DMEM feedback loops
(a b3 write at addr X followed later by a read near X), and locate the modulated
taps (56,57,107,108) and closers (65,88) within it.
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import aru_datapath as A

MOD = {56, 57, 107, 108}
CLOSERS = {65, 88}


def main():
    prog = A.load_microcode(0x01)
    print(f"{len(prog)} active steps. Columns: s | off | coeff Cs=mag>>1 | ZERO XFER b3 | WA RA | role")
    # offset stats to understand the delay scale
    offs = sorted(set(p['offset'] for p in prog))
    print(f"\noffset range: min={min(offs)} max={max(offs)}  (DMEM ring 65536)")
    # The position base is 0 anchored at the input read; relative delays are offset diffs.
    for p in prog:
        s = p['s']
        mag = abs(p['coeff']); Cs = -(mag >> 1) if p['coeff'] < 0 else (mag >> 1)
        ra = (p['b5'] << 1) | p['b4']
        tag = []
        if s in MOD: tag.append("<<MODULATED")
        if s in CLOSERS: tag.append("<<CLOSER")
        if Cs != 0 and abs(Cs) >= 60: tag.append(f"hi-gain {Cs}/64={Cs/64:.3f}")
        flag = ' '.join(tag)
        if s in MOD or s in CLOSERS or (abs(Cs) >= 60) or p['b3']:
            print(f"  s{s:<3} off={p['offset']:<6} coeff={p['coeff']:<5} Cs={Cs:<4} "
                  f"Z{p['ZERO']} X{p['XFER']} b3={p['b3']} WA{p['WA']} RA{ra}  {flag}")

    # Find short-range DMEM loops: a b3 write step and any read step whose offset is
    # within +-16 of it (a tight recirculation ~ a few samples).
    print("\nShort-range tap pairs (|offset difference| <= 16) — candidate tight loops:")
    writes = [(p['s'], p['offset']) for p in prog if p['b3']]
    reads = [(p['s'], p['offset']) for p in prog if not p['b3']]
    seen = set()
    for ws, wo in writes:
        for rs, ro in reads:
            d = wo - ro            # read is 'd' samples after the write in delay terms
            if 0 < d <= 16:
                key = (ws, rs)
                if key not in seen:
                    seen.add(key)
                    print(f"  write s{ws}(off {wo}) -> read s{rs}(off {ro})  delay={d} samples")


if __name__ == '__main__':
    main()
