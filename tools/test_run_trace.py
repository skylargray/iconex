#!/usr/bin/env python3
"""Verify run_trace() reproduces run()'s per-sample energy exactly (non-breaking)."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import aru_datapath as A

def main():
    prog = A.load_microcode(0x01)
    ra_pick = lambda st: (st['b5'] << 1) | st['b4']
    base = A.run(prog, ra_pick, nsamp=300)
    esum, steps = A.run_trace(prog, ra_pick, nsamp=300, trace_window=8)
    assert esum == base, "run_trace esum diverges from run()"
    # trace_window=8 samples, each with len(prog) active steps, 8 fields per record
    assert len(steps) == 8 * len(prog), f"unexpected step count {len(steps)}"
    assert all(len(r) == 8 for r in steps), "each step record must have 8 fields"
    # res field is sentinel (INT64_MIN) on non-XFER steps, a valid 16-bit value on XFER
    SENT = -(1 << 63)
    assert any(r[7] != SENT for r in steps), "expected at least one XFER step in trace"
    print(f"OK: run_trace matches run() over 300 samples; {len(steps)} step records")

if __name__ == '__main__':
    main()
