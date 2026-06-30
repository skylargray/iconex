#!/usr/bin/env python3
"""Phase 1.4 — static/observed POST-state independence of the WCS build (helps close G2).

Question: does the WCS-build code (record builder @0xB55B, expander @0xAA9F->0xAB39, coeff fetch
@0xB510) read ANY memory cell whose value was produced by the POST/DIAG self-test? If not — if every
RAM cell the build reads was last written by the build itself or by power-on init (which runs
regardless of POST outcome) — then the build cannot depend on whether POST passed or was bypassed.

Method (OBSERVED, not a code-read — plan 019 ethos):
  • Install a read callback that records EVERY RAM read (0x1800..0x7FFF) the firmware performs in the
    build window (prog_load -> mainloop), with its event order.
  • Keep a full write log for the WHOLE run, tagged with the phase it occurred in.
  • For each build-window RAM read, find its LAST WRITER (the most recent write to that address at or
    before the read) and that writer's phase. If any build read's last-writer phase is a POST/DIAG
    phase, the build value came from POST -> POST-dependent. Otherwise POST-independent.

POST/DIAG phases = everything before 'normal_op' that is the self-test: handshake, DIAG_E, DIAG_H.
('init' = the unconditional power-on RAM setup that runs the same whether POST passes or is bypassed,
so an init-sourced read is NOT a POST dependence; it is reported separately for transparency.)

Run:  python tools/verify_post_independence.py
"""
import os
import sys
import json
import bisect

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
sys.stdout.reconfigure(encoding="utf-8")
import boot8080 as B

SCR = (r"C:/Users/Skylar/AppData/Local/Temp/claude/"
       r"d--OneDrive-Gray-Instruments-iconex/ae30a9a1-b02b-4706-a6d3-7d89d4cefad3/scratchpad")
os.makedirs(SCR, exist_ok=True)

RAM_LO, RAM_HI = 0x1800, 0x7FFF          # between SBC ROM (..0x17FF) and NVS ROM (0x8000..)
POST_PHASES = {"handshake", "DIAG_E", "DIAG_H"}
BUILD_PHASES = {"prog_load"}


class ReadWriteTracer:
    """Minimal tracer for boot8080.boot(trace=...): full write log (phase-tagged) for the whole run +
    RAM-read log limited to the build window."""

    def __init__(self):
        self.m = None
        self.n = 0
        self.cur_label = "init"
        self.in_window = False
        self.writes = []                  # (order, pc, addr, phase)  -- ALL writes
        self.reads = []                   # (order, addr)             -- RAM reads in build window only

    def attach(self, m):
        self.m = m
        mem = m.memory

        def wcb(a, v):
            mem[a] = v
            self.n += 1
            self.writes.append((self.n, m.pc, a, self.cur_label))

        m.set_write_callback(wcb)

        def rcb(a):
            if self.in_window and RAM_LO <= a <= RAM_HI:
                self.reads.append((self.n, a))
            return mem[a]

        self._rcb = rcb                   # installed at window open

    def on_io(self, direction, port, val):
        pass

    def mark(self, label):
        self.cur_label = label
        if label == "prog_load":
            self.in_window = True
            self.m.set_read_callback(self._rcb)
        elif label == "mainloop":
            self.in_window = False


def main():
    print("### Phase 1.4 — POST-state independence of the WCS build ###")
    print("booting CONCERT with full write log + build-window RAM-read capture (read cb = slower)...\n")
    tr = ReadWriteTracer()
    m, ms = B.boot(verbose=True, trace=tr)
    assert "mainloop" in ms and "prog_load" in ms, f"boot did not reach mainloop: {ms}"
    print(f"\nmilestones: {ms}")
    print(f"total writes logged: {len(tr.writes)}; build-window RAM reads logged: {len(tr.reads)}")

    # Build per-address sorted write index: addr -> ([orders], [phases])
    from collections import defaultdict
    waddr = defaultdict(lambda: ([], []))
    for (o, pc, a, ph) in tr.writes:
        waddr[a][0].append(o)
        waddr[a][1].append(ph)

    def last_writer_phase(addr, read_order):
        orders, phases = waddr.get(addr, ([], []))
        if not orders:
            return None                    # never written in RAM during this run -> ROM-init/constant
        i = bisect.bisect_right(orders, read_order) - 1
        return phases[i] if i >= 0 else None

    # Classify every distinct (addr) the build reads by the set of last-writer phases it saw.
    from collections import Counter
    phase_hits = Counter()                 # last-writer-phase -> #reads
    post_dependent = defaultdict(set)      # addr -> set(post phases) for any POST-sourced read
    addr_phase = defaultdict(set)          # addr -> set of last-writer phases
    never_written = set()
    for (o, a) in tr.reads:
        ph = last_writer_phase(a, o)
        if ph is None:
            never_written.add(a)
            phase_hits["<unwritten-RAM/never>"] += 1
        else:
            phase_hits[ph] += 1
            addr_phase[a].add(ph)
            if ph in POST_PHASES:
                post_dependent[a].add(ph)

    print("\nbuild-window RAM reads — count by last-writer phase:")
    for ph, c in phase_hits.most_common():
        flag = "  <<< POST/DIAG SOURCE!" if ph in POST_PHASES else ""
        print(f"   {ph:>22}: {c:>7}{flag}")

    distinct = sorted(set(a for (o, a) in tr.reads))
    print(f"\ndistinct RAM addresses read by the build: {len(distinct)}")
    print(f"  range: 0x{min(distinct):04X}..0x{max(distinct):04X}" if distinct else "  (none)")

    print("\nPOST-dependent reads (build read a cell whose last writer was a POST/DIAG phase):")
    if post_dependent:
        for a in sorted(post_dependent):
            print(f"   0x{a:04X}: sourced from {sorted(post_dependent[a])}")
    else:
        print("   NONE — no build read takes a value last written during POST/DIAG.")

    # Transparency: which non-POST phases sourced the build's reads
    nonpost = Counter()
    for a in distinct:
        for ph in addr_phase.get(a, set()):
            nonpost[ph] += 1
    print("\nlast-writer phases seen across distinct build-read addresses (transparency):")
    for ph, c in nonpost.most_common():
        print(f"   {ph:>22}: {c:>5} distinct addrs")
    if never_written:
        print(f"   <unwritten RAM (ROM-shadow/constant or read-before-write)>: {len(never_written)} addrs"
              f"  e.g. {[hex(x) for x in sorted(never_written)[:8]]}")

    independent = not post_dependent
    verdict = ("G2 (static): build is POST-INDEPENDENT — reads no POST/DIAG-sourced cell"
               if independent else
               "G2 (static): build reads POST/DIAG-sourced cells — NOT statically independent (see list)")
    print("\n" + "=" * 72)
    print(f"VERDICT: {verdict}")
    print("  (Phase 3 confirms empirically by diffing POST-pass vs POST-bypass.)")
    print("=" * 72)

    out = {
        "total_writes": len(tr.writes),
        "build_ram_reads": len(tr.reads),
        "distinct_read_addrs": len(distinct),
        "phase_hits": dict(phase_hits),
        "post_dependent_addrs": {hex(a): sorted(v) for a, v in post_dependent.items()},
        "independent": independent,
        "verdict": verdict,
    }
    with open(os.path.join(SCR, "phase1_4_post_indep.json"), "w") as f:
        json.dump(out, f, indent=1)
    print(f"\nwrote {SCR}/phase1_4_post_indep.json")
    return independent


if __name__ == "__main__":
    ok = main()
    sys.exit(0 if ok else 1)
