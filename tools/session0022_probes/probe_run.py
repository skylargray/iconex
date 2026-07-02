#!/usr/bin/env python3
"""Shared helper: continue a boot8080 machine PAST boot() under the same conditions boot()
itself maintains. boot()'s loop fires the RST-7 serial interrupt every ~1500 ticks (the
8251 TxRDY is interrupt-driven after EI); the firmware HLTs waiting for it, so a naive
"m.ticks_to_stop = N; m.run()" loop STARVES (session 0024: d2a2 burned 45 min inside its
first 4M-tick run). Mirror boot(): small chunks + fire_int + step over stale breakpoints."""


def _fire_int(m):
    """RST-7 by hand, exactly as boot8080.boot()'s fire_int: push PC, jump 0x0038, DI."""
    if m._I8080State__iff[0] == 0:
        return False
    sp = (m.sp - 2) & 0xFFFF
    m.memory[sp] = m.pc & 0xFF
    m.memory[(sp + 1) & 0xFFFF] = (m.pc >> 8) & 0xFF
    m.sp = sp
    m.pc = 0x0038
    m._I8080State__iff[0] = 0
    return True


def run_ticks(m, n, chunk=1500):
    """Run ~n ticks with boot()-equivalent interrupt service."""
    left = n
    while left > 0:
        c = min(chunk, left)
        m.ticks_to_stop = c
        ev = m.run()
        done = c - m.ticks_to_stop
        if ev & m._BREAKPOINT_HIT:                       # stale boot milestone breakpoint
            m.clear_breakpoint(m.pc)
            m.ticks_to_stop = 1
            m.run()
            done += 1
        _fire_int(m)
        left -= max(done, 1)
