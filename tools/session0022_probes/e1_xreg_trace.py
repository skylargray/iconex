#!/usr/bin/env python3
"""E1a (plan 023) — trace the diag-3 signature-pulse loop at 0x0D10 for its XREG write
sequence + periodicity, on the VERIFIED kosarev core.

Static read (SBC2 disassembly, this session):
  0x0CF0  CALL 0x03D5 ; twice CALL 0x0D1E(HL=0x0D16) ; OUT 02 ;
          copy ROM 0x1639 -> 0x4180 (0x80 bytes = CPU words 96..127) ; OUT 01 ; OUT 03 ;
  0x0D10  CALL 0x02AD ; JP 0x0D10          <- the signature-pulse loop (bench state)
  0x0D1E  OUT 02/00/03 ; display; then 4x { XREG <- pair from (HL); OUT 03 ;
          poke 0x41FA <- F6/FA/FE (between pairs) } ; RET
          table @0x0D16 = AA AA 99 99 87 C7 7F 60  -> XREG 0xAAAA,0x9999,0xC787,0x607F

QUESTIONS (plan 023 E1a): what does the LOOP write per iteration? Is the OUT stream
periodic (byte-identical across iterations and boots)? What is the XREG value the ARU
sees during bench measurement? Both pacings: 0x0627->RET free-run vs 0x3C14-flag feed.

Method note: boot WITHOUT the write-trace harness (10x slower); install a lightweight
I/O logger post-boot (replicating the boot closure's port defaults: 0xEF->TxRDY,
0xEE->0xFF, 0x06/0x07->0xFF, else 0x00).

Deliverable: cache xreg_pulse.json {setup_outs, loop_outs per iteration, verdicts}.
"""
import sys, os, json

TOOLS = r"d:\OneDrive\Gray Instruments\iconex\tools"
sys.path.insert(0, TOOLS)
HERE = os.path.dirname(os.path.abspath(__file__))
CACHE = os.path.join(HERE, "xreg_pulse.json")

import boot8080
from probe_run import _fire_int

HANDLER, LOOP_PC = 0x0CF0, 0x0D10
SYNC_WAIT = 0x0627
FLAG = 0x3C14


class IOLog:
    """Post-boot I/O logger: replaces the boot closures with logging equivalents."""

    def __init__(self, m):
        self.log = []          # ('IN'/'OUT', port, val)
        self.tx = []

        def on_input(port):
            p = port & 0xFF
            if p == 0xEF:
                ret = 0x01                       # TxRDY, no Rx pending
            elif p == 0xEE:
                ret = 0xFF
            elif p in (0x06, 0x07):
                ret = 0xFF                       # ARU latch readback stub (boot default)
            else:
                ret = 0x00
            self.log.append(("IN", p, ret))
            return ret

        def on_output(port, v):
            p = port & 0xFF
            self.log.append(("OUT", p, v & 0xFF))
            if p == 0xEE:
                self.tx.append(v & 0x7F)

        m.set_input_callback(on_input)
        m.set_output_callback(on_output)

    def dsp_outs(self, i0=0):
        return [(d, p, v) for d, p, v in self.log[i0:] if d == "OUT" and p < 0x10]


def run_to_loop(m, budget=60_000_000, feed_flag=False):
    """Direct-call the diag-3 handler; run to first arrival at the 0x0D10 loop.
    feed_flag: keep mem[0x3C14]=0x80 so unpatched frame-sync waits proceed (pacing B)."""
    sp = (m.sp - 2) & 0xFFFF
    m.memory[sp] = 0xFF
    m.memory[(sp + 1) & 0xFFFF] = 0xFF
    m.sp = sp
    m.pc = HANDLER
    m.set_breakpoint(LOOP_PC)
    ticks = 0
    while ticks < budget:
        if feed_flag:
            m.memory[FLAG] = 0x80
        m.ticks_to_stop = 20_000
        ev = m.run()
        ticks += 20_000 - m.ticks_to_stop
        if ev & m._BREAKPOINT_HIT:
            if m.pc == LOOP_PC:
                return ticks
            m.clear_breakpoint(m.pc)
            m.ticks_to_stop = 1
            m.run()
    raise RuntimeError(f"never reached loop (PC=0x{m.pc:04X})")


def run_loop_iters(m, n_iters, feed_flag=False, tick_chunk=1500):
    """Run until n_iters arrivals at 0x0D10 (breakpoint stays set). Returns tick counts."""
    iters = []
    t = 0
    guard = 0
    while len(iters) < n_iters and guard < 100_000:
        guard += 1
        if feed_flag:
            m.memory[FLAG] = 0x80
        m.ticks_to_stop = tick_chunk
        ev = m.run()
        t += tick_chunk - m.ticks_to_stop
        if ev & m._BREAKPOINT_HIT:
            if m.pc == LOOP_PC:
                iters.append(t)
                t = 0
                m.ticks_to_stop = 1
                m.run()
            else:
                m.clear_breakpoint(m.pc)
                m.ticks_to_stop = 1
                m.run()
        _fire_int(m)
    if len(iters) < n_iters:
        raise RuntimeError(f"only {len(iters)}/{n_iters} loop arrivals (PC=0x{m.pc:04X})")
    return iters


def one_run(pacing, seed_tag):
    """Boot, patch per pacing, capture the OUT stream through setup + loop iterations."""
    m, ms = boot8080.boot(verbose=False)
    assert "mainloop" in ms, f"boot failed: {ms}"
    io = IOLog(m)
    if pacing == "free":
        m.memory[SYNC_WAIT] = 0xC9           # frame-sync wait -> RET (d1a-style)
    run_to_loop(m, feed_flag=(pacing == "flag"))
    setup = io.dsp_outs()
    per_iter_outs = []
    for k in range(6):
        j0 = len(io.log)
        run_loop_iters(m, 1, feed_flag=(pacing == "flag"))
        outs = [(d, p, v) for d, p, v in io.log[j0:] if d == "OUT" and p < 0x10]
        per_iter_outs.append(outs)
    wcs_after = bytes(m.memory[0x4000:0x4200]).hex()
    return dict(pacing=pacing, seed=seed_tag, milestones={k: int(v) for k, v in ms.items()},
                setup_outs=setup, per_iter_outs=per_iter_outs,
                wcs=wcs_after, flag_val=m.memory[FLAG])


def xreg_seq(outs):
    """Extract 16-bit XREG values from an OUT list (port6=lo then port7=hi pairing)."""
    vals, lo = [], None
    for d, p, v in outs:
        if d != "OUT":
            continue
        if p == 0x06:
            lo = v
        elif p == 0x07 and lo is not None:
            vals.append((v << 8) | lo)
            lo = None
    return vals


def main():
    results = []
    for pacing, tag in (("free", "boot1"), ("free", "boot2"), ("flag", "boot1")):
        print(f"[{pacing}/{tag}] booting + tracing ...", flush=True)
        r = one_run(pacing, tag)
        results.append(r)
        print(f"  setup: {len(r['setup_outs'])} dsp-port OUTs; "
              f"XREG sequence: {[hex(x) for x in xreg_seq(r['setup_outs'])]}")
        print(f"  setup OUT stream: {r['setup_outs']}")
        for k, outs in enumerate(r["per_iter_outs"]):
            print(f"  loop iter {k}: {len(outs)} dsp-port OUTs "
                  f"{outs[:8] if outs else '(none)'}")

    a, b, c = results
    v = {}
    v["setup_identical_across_boots"] = a["setup_outs"] == b["setup_outs"]
    v["setup_identical_across_pacings"] = a["setup_outs"] == c["setup_outs"]
    v["loop_writes_xreg"] = any(p in (6, 7) for outs in a["per_iter_outs"]
                                for d, p, _ in outs)
    v["loop_outs_periodic"] = all(outs == a["per_iter_outs"][0]
                                  for outs in a["per_iter_outs"][1:])
    v["loop_outs_same_across_pacings"] = a["per_iter_outs"][0] == c["per_iter_outs"][0]
    sq = xreg_seq(a["setup_outs"])
    v["final_xreg_setup"] = hex(sq[-1]) if sq else None
    v["wcs_identical_boots"] = a["wcs"] == b["wcs"]
    v["wcs_identical_pacings"] = a["wcs"] == c["wcs"]
    old = open(os.path.join(TOOLS, "_diag3_wcs.bin"), "rb").read()
    v["wcs_matches_diag3_bin"] = bytes.fromhex(a["wcs"]) == old

    print("\n### E1a verdicts ###")
    for k, val in v.items():
        print(f"  {k}: {val}")

    json.dump(dict(runs=results, verdicts=v), open(CACHE, "w"), indent=1)
    print(f"\ncached -> {CACHE}")


if __name__ == "__main__":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass
    main()
