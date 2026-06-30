#!/usr/bin/env python3
"""Full write + I/O trace harness on the VERIFIED kosarev `z80.I8080Machine`.

WHY: every 224XL reverse-engineering error so far came from US *interpreting* a firmware-built byte
layout (4-byte stride, lane polarity, offset source, one-hot channels). This harness removes the
interpretation: it captures EVERY memory write and EVERY I/O in/out the firmware actually performs,
on the core that passes the canonical 8080 exercisers (cputest/8080pre/8080exm) — so the microcode
and the hardware boundary are OBSERVED, not assumed.

DESIGN (respecting "track everything" without drowning in volume):
  • ALWAYS, globally, for the whole run:
      - every memory WRITE -> aggregate by 256-byte page: count, writer-PC set, phase set, first/last
        write order, and the final byte image (we perform the write ourselves, since the kosarev
        write-callback INTERCEPTS the write rather than observing it).
      - every I/O IN/OUT -> full ordered log (low volume; this is the true hardware boundary — the WCS
        SRAM is SBC-address-decoded, but anything the firmware streams to the T&C goes out as OUT).
  • ON DEMAND, windowed between two phase markers:
      - full per-write log (order, writer-PC, addr, val) and optional full read log.
    (A global full read/opcode trace would route every fetch through Python = 10x slower + GBs, so it
     is windowed — nothing is pre-FILTERED; the aggregate already covers all 64K, any window expands.)

The point: the write-target histogram DISCOVERS where the firmware writes microcode (instead of us
asserting "0x4000 is the WCS"); the I/O log DISCOVERS whether microcode is also/instead streamed out.

Use via boot8080.boot(trace=Trace8080()) — see trace_concert.py.
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))


class Trace8080:
    def __init__(self, full_writes=False, capture_window=None, capture_reads=False, watch_range=None):
        """full_writes: keep the full per-write log for the WHOLE run (memory-heavy).
        capture_window: (start_label, end_label) -> keep the full per-write log only between those
            two phase markers (the recommended way to see a build sequence in detail).
        capture_reads: also capture reads inside the window (needs set_read_callback; slower).
        watch_range: (lo, hi) -> ALWAYS log the full per-write history (order,pc,addr,val) for just
            this address range, cheaply, across the WHOLE run (e.g. the 0x4000 WCS, to see per-frame
            evolution past mainloop without logging all 64K)."""
        self.m = None
        self.full_writes = full_writes
        self.capture_window = capture_window
        self.capture_reads = capture_reads
        self.watch_range = watch_range
        self.watch = []                 # [(order, pc, addr, val)] for watch_range, always

        self.n = 0                      # monotonic write counter (event order)
        self.cur_label = "init"

        # aggregate (always on, covers all 64K)
        self.page_count = {}            # page -> total writes
        self.page_writers = {}          # page -> set(writer-PC)  (capped)
        self.page_phases = {}           # page -> set(phase label)
        self.page_first = {}            # page -> first write order
        self.page_last = {}             # page -> last write order

        # full ordered logs
        self.io = []                    # [(order, 'IN'/'OUT', port, val)]  -- ALL i/o, always
        self.markers = []               # [(order, label)]
        self.writes = []                # [(order, pc, addr, val)] -- full or windowed
        self.reads = []                 # [(order, pc, addr, val)] -- windowed only

        self._capturing = full_writes   # currently logging full writes?
        self._read_cb_on = False

    # ---- attached by boot8080.boot() right after the machine is created ----
    def attach(self, m):
        self.m = m
        mem = m.memory
        wr = self.watch_range

        def wcb(a, v):
            mem[a] = v                  # PERFORM the write (callback intercepts it)
            self.n += 1
            pg = a >> 8
            self.page_count[pg] = self.page_count.get(pg, 0) + 1
            pcset = self.page_writers.get(pg)
            if pcset is None:
                pcset = self.page_writers[pg] = set()
            if len(pcset) < 96:
                pcset.add(m.pc)
            phset = self.page_phases.get(pg)
            if phset is None:
                phset = self.page_phases[pg] = set()
            phset.add(self.cur_label)
            if pg not in self.page_first:
                self.page_first[pg] = self.n
            self.page_last[pg] = self.n
            if self._capturing:
                self.writes.append((self.n, m.pc, a, v))
            if wr is not None and wr[0] <= a <= wr[1]:
                self.watch.append((self.n, m.pc, a, v))

        m.set_write_callback(wcb)

        if self.capture_reads and self.capture_window:
            def rcb(a):
                if self._read_cb_on:
                    self.reads.append((self.n, m.pc, a, mem[a]))
                return mem[a]
            # only install when window opens (set in mark()); store the fn
            self._rcb = rcb

    # ---- called by boot8080 on every IN/OUT ----
    def on_io(self, direction, port, val):
        self.io.append((self.n, direction, port & 0xFF, val & 0xFF))

    # ---- called by boot8080 at each milestone ----
    def mark(self, label):
        self.markers.append((self.n, label))
        self.cur_label = label
        if self.capture_window:
            start, end = self.capture_window
            if label == start:
                self._capturing = True
                if self.capture_reads and getattr(self, "_rcb", None):
                    self.m.set_read_callback(self._rcb)
                    self._read_cb_on = True
            if label == end:
                self._capturing = self.full_writes
                self._read_cb_on = False

    # =====================================================================
    # reporting
    # =====================================================================
    def phase_of_order(self, order):
        lab = "init"
        for o, l in self.markers:
            if o <= order:
                lab = l
            else:
                break
        return lab

    def write_histogram(self, top=None):
        """Every 256-byte page written, sorted by address. Returns list of dicts."""
        rows = []
        for pg in sorted(self.page_count):
            rows.append(dict(
                page=pg, base=pg << 8, count=self.page_count[pg],
                first=self.page_first[pg], last=self.page_last[pg],
                phases=sorted(self.page_phases[pg]),
                writers=sorted(self.page_writers[pg])))
        rows.sort(key=lambda r: r["count"], reverse=True)
        return rows[:top] if top else rows

    def print_report(self, region_detail=None):
        sys.stdout.reconfigure(encoding="utf-8")
        print("=" * 78)
        print("WRITE-TARGET HISTOGRAM  (every 256-byte page the firmware wrote; DISCOVERED, not assumed)")
        print("=" * 78)
        print(f"  total writes captured: {self.n}")
        print(f"  phase markers (write-order): " +
              ", ".join(f"{l}@{o}" for o, l in self.markers))
        print(f"\n  {'page':>6} {'count':>8} {'first':>9} {'last':>9}  phases / example writer-PCs")
        for r in sorted(self.write_histogram(), key=lambda r: r["base"]):
            wr = " ".join(f"{p:04X}" for p in r["writers"][:8])
            ph = ",".join(r["phases"])
            print(f"  0x{r['base']:04X} {r['count']:>8} {r['first']:>9} {r['last']:>9}  [{ph}]  PCs:{wr}")

        print("\n" + "=" * 78)
        print("I/O LOG SUMMARY  (the other hardware boundary — every IN/OUT)")
        print("=" * 78)
        from collections import Counter
        oc = Counter((d, p) for _, d, p, _ in self.io)
        for (d, p), c in sorted(oc.items()):
            vals = sorted(set(v for _, dd, pp, v in self.io if dd == d and pp == p))
            vshow = " ".join(f"{v:02X}" for v in vals[:16]) + (" ..." if len(vals) > 16 else "")
            print(f"  {d} port 0x{p:02X}: {c:>6} events; values: {vshow}")

        if region_detail is not None:
            base, n = region_detail
            print("\n" + "=" * 78)
            print(f"REGION DETAIL 0x{base:04X}..0x{base+n-1:04X}  (final bytes + last-writer)")
            print("=" * 78)
            self.print_region(base, n)

    def print_region(self, base, n, width=16):
        mem = self.m.memory
        # last writer PC per address from the full write log (if available)
        lastw = {}
        for o, pc, a, v in self.writes:
            if base <= a < base + n:
                lastw[a] = (pc, o)
        for row in range(0, n, width):
            a0 = base + row
            hexs = " ".join(f"{mem[a0+i]:02X}" for i in range(min(width, n - row)))
            print(f"  0x{a0:04X}: {hexs}")
        if lastw:
            print(f"  (last-writer PCs in window: " +
                  ", ".join(f"{a:04X}<-{pc:04X}" for a, (pc, o) in sorted(lastw.items())[:24]) + ")")
