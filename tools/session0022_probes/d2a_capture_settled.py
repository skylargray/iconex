#!/usr/bin/env python3
"""D2a (plan 022) — pin the WCS capture point: which snapshot is the SETTLED power-up default?

Boots CONCERT (power-up variation 1.1) on the verified core with NO key events and NO audio
input, then snapshots the 0x4000 WCS every 1M ticks (~0.5 s of machine time, ~16k frames)
for 80M ticks past the mainloop. De-zipper/apply activity IS WCS writes, so byte-level
snapshot diffing is the direct quiescence detector:

  - bytes that change early then FREEZE      = the power-up apply/de-zipper transient;
  - bytes that keep changing to the end      = the always-on modulation targets (LFO);
  - settled default = the last snapshot, with the persistent movers named (its LFO phase
    is frozen-arbitrary — the D4 co-sim retires that approximation).

Also diffs the three capture points against each other: the 0022 mainloop snapshot
(wcs_cache.json id 1), the 40M-tick RUN image (wcs_run_concert.json), and today's settled
image -> wcs_settled_concert.json.
"""
import sys, os, json
from collections import Counter

TOOLS = r"d:\OneDrive\Gray Instruments\iconex\tools"
sys.path.insert(0, TOOLS)
HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "wcs_settled_concert.json")

import boot8080

EXTRA = 80_000_000
EVERY = 1_000_000

snaps = []
print(f"booting CONCERT power-up + {EXTRA/1e6:.0f}M ticks free-run "
      f"(snapshot every {EVERY/1e6:.0f}M) ...")
m, ms = boot8080.boot(verbose=False, extra_ticks_after_mainloop=EXTRA,
                      snapshot_cb=lambda img, tick: snaps.append((tick, img)),
                      snapshot_every=EVERY)
assert "mainloop" in ms, ms
t_main = ms["mainloop"]
final = bytes(m.memory[0x4000:0x4200])
print(f"mainloop at {t_main/1e6:.1f}M ticks; {len(snaps)} snapshots; "
      f"final at {snaps[-1][0]/1e6:.1f}M ticks\n")

# ---- per-interval changed-byte sets ----
imgs = [(t_main, None)] + snaps            # sentinel for indexing; diffs start at snaps[0]
diffs = []                                  # (tick, set of changed byte addrs vs previous)
prev_t, prev = snaps[0]
for t, img in snaps[1:]:
    ch = {a for a in range(0x200) if img[a] != prev[a]}
    diffs.append((t, ch))
    prev = img

# persistent movers = bytes changing in the LAST quarter of the run
tail_from = snaps[-1][0] - (snaps[-1][0] - snaps[0][0]) // 4
movers = set().union(*[ch for t, ch in diffs if t >= tail_from]) if diffs else set()
# transient bytes = changed at some point but NOT a persistent mover
all_changed = set().union(*[ch for _, ch in diffs]) if diffs else set()
transient = all_changed - movers

# when did the non-mover bytes last change?
last_nonmover_change = max((t for t, ch in diffs if ch - movers), default=None)

def wordset(addrs):
    return sorted({a // 4 for a in addrs})

print(f"bytes changing per 1M-tick interval (first 12): "
      f"{[len(ch) for _, ch in diffs[:12]]}")
print(f"persistent movers (last-quarter changers): {len(movers)} bytes, "
      f"CPU words {wordset(movers)}")
print(f"lanes of movers: {sorted({a % 4 for a in movers})}")
print(f"transient (froze) bytes: {len(transient)}, CPU words {wordset(transient)}")
print(f"last non-mover change: "
      f"{'NONE (quiescent from first snapshot)' if last_nonmover_change is None else f'{(last_nonmover_change - t_main)/1e6:.0f}M ticks past mainloop'}")

# ---- compare the three capture points ----
boot_img = bytes.fromhex(json.load(open(os.path.join(HERE, "wcs_cache.json")))["1"]["wcs"])
run_img = bytes.fromhex(json.load(open(os.path.join(HERE, "wcs_run_concert.json")))["wcs"])
settled = snaps[-1][1]

for name, a, b in (("mainloop-vs-settled", boot_img, settled),
                   ("run40M-vs-settled", run_img, settled),
                   ("mainloop-vs-run40M", boot_img, run_img)):
    d = [x for x in range(0x200) if a[x] != b[x]]
    inmov = [x for x in d if x in movers]
    out = [x for x in d if x not in movers]
    print(f"\n{name}: {len(d)} byte diffs; {len(inmov)} inside the mover set, "
          f"{len(out)} OUTSIDE")
    if out:
        print(f"  outside-mover diffs at CPU words {wordset(out)} "
              f"(lanes {sorted({x % 4 for x in out})})")

json.dump({"wcs": settled.hex(),
           "ticks_past_mainloop": int(snaps[-1][0] - t_main),
           "movers": sorted(movers),
           "mover_words": wordset(movers),
           "transient": sorted(transient),
           "last_nonmover_change_ticks": (None if last_nonmover_change is None
                                          else int(last_nonmover_change - t_main))},
          open(OUT, "w"))
print(f"\nsettled image -> {OUT}")
