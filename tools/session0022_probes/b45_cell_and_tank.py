#!/usr/bin/env python3
"""B4 + B5 (plan 021) on the RTL-aligned engine.

B4 — ladder-cell recursion: the in-place RMW pairs (write of=o, read of=o+1 one frame later)
must behave as bounded RECURSIVE nodes (a geometric per-frame return), not one-shot forward
FIR. Seed the cell via the input path and fit the per-frame ratio.

B5 — tank energy: charge with a 50 ms noise burst, then silence; track DM ENERGY (sum of
squares over all touched cells — dead-end #11: never RMS-over-touched-cells) and the output
energy per 100 ms block for >= 1.5 s. Acceptance: sustained-and-decaying (not instant-drain,
not divergent rail/limit-cycle).
"""
import sys, os, json, math, random, time
TOOLS = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, TOOLS)
from aru_freerun22_rtl import RTL22, program_rows22, fs22
from aru_rtl_dp import s16

HERE = os.path.dirname(os.path.abspath(__file__))
cache = json.load(open(os.path.join(HERE, "wcs_cache.json")))
b = bytes.fromhex(cache["1"]["wcs"])
wcs = [(b[4*k], b[4*k+1], b[4*k+2], b[4*k+3]) for k in range(128)]
rows, L, w_reset = program_rows22(wcs)
FS = fs22(L)
print(f"CONCERT: {len(rows)}-step frame, fs={FS:.1f} Hz")

# ---------------- B4: in-place cell recursion ----------------
print("\n--- B4: in-place RMW cell recursion (impulse-seeded) ---")
eng = RTL22()
IMP = 16422
cellA = None      # track the of=19678 write cell of frame 0
traj = []
for n in range(12):
    eng.run_sample(rows, IMP if n == 0 else 0)
    if n == 0:
        # frame-0 write head: addr = CPC(pre-bump)=0 - 19678
        cellA = (0 - 19678) & 0xFFFF
    traj.append(s16(eng.DM.get(((n - 19678) & 0xFFFF), 0)))   # the in-place cell written this frame
ratios = [traj[i + 1] / traj[i] for i in range(len(traj) - 1) if abs(traj[i]) > 20]
print(f"  cell(of=19678) per-frame write values: {traj}")
print(f"  per-frame ratios: {[f'{r:+.3f}' for r in ratios]}")
bounded = all(abs(v) <= 32767 for v in traj)
recursive = len([v for v in traj if abs(v) > 2]) >= 3
geometric = len(ratios) >= 2 and all(abs(r) < 1.0 for r in ratios)
print(f"  bounded={bounded} persists>=3frames={recursive} |ratio|<1={geometric}")
print(f"  B4 VERDICT: {'PASS (bounded recursive node)' if (bounded and recursive and geometric) else 'FAIL'}")

# ---------------- B5: tank energy over 2.0 s ----------------
print("\n--- B5: tank energy, 50 ms burst then silence (2.0 s) ---")
rnd = random.Random(21)
burst_n = int(0.050 * FS)
total_n = int(2.0 * FS)
eng = RTL22()
t0 = time.time()
block = int(0.100 * FS)
print(f"  {total_n} frames ({total_n * len(rows)} steps)...")
hist = []
out_acc = 0
for n in range(total_n):
    x = int(rnd.uniform(-12000, 12000)) if n < burst_n else 0
    outs = eng.run_sample(rows, x & 0xFFFF)
    for c, v in outs:
        out_acc += v * v
    if (n + 1) % block == 0:
        e = sum(s16(v) * s16(v) for v in eng.DM.values())
        ncells = len(eng.DM)
        hist.append((n + 1, e, ncells, out_acc))
        out_acc = 0
print(f"  done in {time.time()-t0:.1f} s")
print(f"  {'t(s)':>6} {'DM energy':>14} {'cells':>7} {'out E/blk':>12}")
peak = max(h[1] for h in hist)
for n, e, nc, oe in hist:
    bar = "#" * int(40 * e / peak) if peak else ""
    print(f"  {n/FS:6.2f} {e:14.0f} {nc:7d} {oe:12.0f}  {bar}")
# acceptance: energy at 0.2 s (post-burst) > 0; decaying but NOT gone within 0.3 s; not flat/divergent
e_02 = next(e for n, e, _, _ in hist if n / FS >= 0.19)
e_05 = next(e for n, e, _, _ in hist if n / FS >= 0.49)
e_10 = next(e for n, e, _, _ in hist if n / FS >= 0.99)
e_20 = hist[-1][1]
sustained = e_05 > e_02 * 0.001 and e_05 > 0
decaying = e_20 < e_02 and e_10 <= e_05 * 1.5
print(f"\n  E(0.2s)={e_02:.2e} E(0.5s)={e_05:.2e} E(1.0s)={e_10:.2e} E(2.0s)={e_20:.2e}")
if e_02 > 0 and e_20 > 0:
    # crude RT60 from the post-burst energy slope (energy ~ A^2 => 60 dB = 1e-6 energy ratio)
    if e_20 < e_02:
        rt60 = 60.0 * (2.0 - 0.2) / (10.0 * math.log10(e_02 / e_20))
        print(f"  crude RT60 from tank-energy slope: {rt60:.2f} s")
print(f"  B5 VERDICT: {'PASS (sustained-and-decaying)' if (sustained and decaying) else 'CHECK (see trajectory)'}")
