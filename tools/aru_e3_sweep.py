#!/usr/bin/env python3
"""Track E.3: run >=3 programs across families through the validated run_trace engine using the
slot-keyed offset/coeff spine (build_concert_program.build_program, generalized to any recbase),
and measure a per-program decay metric. Sweep SIZE (cce 0x00..0xFF) on >=1 program and check
whether the decay metric / RT60 tracks SIZE monotonically.

REUSES (do not re-derive): build_concert_program.build_program (validated offset+coeff spine for
ANY recbase), aru_datapath2.build_engine_prog / inject_input / run / rt60 (the E.2 derived wiring
+ engine), aru_datapath.run_trace (owner-validated ARU arithmetic).

HONESTY: the E.2 derived WA/RA/XFER/ZERO/device wiring does NOT close sub-unity (marginal/lossless).
So a true -60 dB RT60 generally does not exist. We therefore report BOTH:
  (a) rt60() from aru_datapath2 (verdict: decayed / marginal_or_long / dead / runaway), and
  (b) a robust decay metric DECAY_RATIO = late_energy / peak_energy (over the IR). <1 = decaying,
      ~1 = marginal/lossless, >1 = runaway. Plus an effective decay-time T_eff from a log-linear
      fit of the smoothed energy envelope when it DOES fall, else 'inf'.
We also report the recirc loop delay (which IS validated and scales with SIZE) so the structural
SIZE-tracking can be demonstrated even where the gain wiring is unresolved.
"""
import sys, os, math
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import build_concert_program as B
import aru_datapath2 as E2
from collections import Counter

FS = 34130.0

PROGRAMS = [
    (0xB800, 'CONCERT HALL', 'hall'),
    (0xBAAA, 'PLATE',        'plate'),
    (0xC000, 'CHAMBER',      'room'),
    (0xC800, 'SMALL ROOM',   'room'),
    (0xDAAA, 'RES CHORDS',   'res'),
]


def recirc_tap(prog):
    reads = [p['offset'] for p in prog if p['role'] == 'READ' and p['offset'] > 0]
    if not reads:
        return (0, 0)
    return Counter(reads).most_common(1)[0]


def envelope_metrics(esum):
    """Robust decay metrics from the energy-sum envelope."""
    if not esum:
        return dict(peak=0, pk=0, decay_ratio=0.0, t_eff_s='inf', verdict='dead')
    pk = max(range(len(esum)), key=lambda i: esum[i])
    peak = esum[pk] or 1
    n = len(esum)
    # smoothed envelope (moving avg) over the tail
    W = 256
    tail = esum[pk:]
    sm = []
    acc = 0.0
    for i, v in enumerate(tail):
        acc += v
        if i >= W:
            acc -= tail[i - W]
        sm.append(acc / min(i + 1, W))
    speak = max(sm) or 1
    late = sum(esum[n - 4000:n - 2000]) / 2000 if n > 4000 else esum[-1]
    decay_ratio = late / peak
    # log-linear fit of smoothed envelope (only where strictly decaying region exists)
    # find first index past speak where it has dropped to 0.5*speak, fit to 1e-3
    t_eff = 'inf'
    lo_thr = speak * 1e-3
    # gather (i, log10(sm)) for sm in (lo_thr, speak]
    xs = []
    ys = []
    started = False
    for i, s in enumerate(sm):
        if s >= speak * 0.9:
            started = True
        if started and s > 0:
            xs.append(i)
            ys.append(math.log10(s))
    if len(xs) > 50 and (ys[0] - ys[-1]) > 0.5:  # at least 0.5 decade of fall
        nfit = len(xs)
        sx = sum(xs); sy = sum(ys)
        sxx = sum(x * x for x in xs); sxy = sum(x * y for x, y in zip(xs, ys))
        denom = nfit * sxx - sx * sx
        if denom != 0:
            slope = (nfit * sxy - sx * sy) / denom  # log10 per sample (negative if decaying)
            if slope < 0:
                # samples for 60 dB = 6 decades
                samp60 = 6.0 / (-slope)
                t_eff = samp60 / FS
    # verdict
    if decay_ratio < 1e-3:
        verdict = 'decays'
    elif decay_ratio > 1.5:
        verdict = 'runaway'
    else:
        verdict = 'marginal'
    return dict(peak=peak, pk=pk, decay_ratio=decay_ratio, t_eff_s=t_eff, verdict=verdict)


def run_program(recbase, cce=0xFE, variant='writeonly', nsamp=400000, imp=20000, in_step=0):
    prog = B.build_program(recbase=recbase, cce=cce)
    loop = recirc_tap(prog)
    eprog = E2.build_engine_prog(prog, variant)
    E2.inject_input(eprog, in_step)
    esum = E2.run(eprog, nsamp=nsamp, imp=imp)
    m = envelope_metrics(esum)
    rt, rts, rverdict = E2.rt60(esum)
    m['recirc_samp'] = loop[0]
    m['recirc_ms'] = loop[0] / FS * 1000
    m['recirc_count'] = loop[1]
    m['rt60_samp'] = rt
    m['rt60_s'] = rts
    m['rt60_verdict'] = rverdict
    m['nmw'] = len(prog)
    return m


def fmt_t(t):
    return f"{t:.3f}s" if isinstance(t, (int, float)) else str(t)


if __name__ == '__main__':
    variant = sys.argv[1] if len(sys.argv) > 1 else 'writeonly'
    print(f"=== E.3 multi-program decay survey (variant={variant}, cce=0xFE) ===")
    print(f"{'program':14s} {'fam':6s} {'mw':>4s} {'recirc(ms)':>11s} {'xN':>3s} "
          f"{'peak':>10s} {'decay_ratio':>12s} {'T_eff':>9s} {'rt60_verdict':>14s}")
    for rb, name, fam in PROGRAMS:
        m = run_program(rb, cce=0xFE, variant=variant)
        print(f"{name:14s} {fam:6s} {m['nmw']:4d} {m['recirc_ms']:11.1f} {m['recirc_count']:3d} "
              f"{m['peak']:10d} {m['decay_ratio']:12.3e} {fmt_t(m['t_eff_s']):>9s} "
              f"{m['rt60_verdict']:>14s}")

    print()
    print(f"=== SIZE sweep on CONCERT HALL (0xB800), variant={variant} ===")
    print(f"{'cce':>5s} {'recirc(ms)':>11s} {'peak':>10s} {'decay_ratio':>12s} "
          f"{'T_eff':>9s} {'rt60_verdict':>14s}")
    rows = []
    for cce in [0x00, 0x20, 0x40, 0x60, 0x80, 0xA0, 0xC0, 0xE0, 0xFF]:
        m = run_program(0xB800, cce=cce, variant=variant)
        rows.append((cce, m))
        print(f"0x{cce:02X} {m['recirc_ms']:11.1f} {m['peak']:10d} {m['decay_ratio']:12.3e} "
              f"{fmt_t(m['t_eff_s']):>9s} {m['rt60_verdict']:>14s}")
    # monotonic check on recirc and on T_eff (where finite)
    recs = [m['recirc_ms'] for _, m in rows]
    mono_rec = all(recs[i] <= recs[i + 1] for i in range(len(recs) - 1))
    print(f"\n  recirc-delay monotonic with SIZE: {mono_rec}  ({recs[0]:.1f} -> {recs[-1]:.1f} ms)")
    teffs = [(cce, m['t_eff_s']) for cce, m in rows if isinstance(m['t_eff_s'], (int, float))]
    if len(teffs) >= 2:
        vals = [t for _, t in teffs]
        mono_t = all(vals[i] <= vals[i + 1] for i in range(len(vals) - 1))
        print(f"  T_eff finite at {len(teffs)}/{len(rows)} sizes; monotonic where finite: {mono_t}")
    else:
        print(f"  T_eff finite at {len(teffs)}/{len(rows)} sizes -> not enough to assess RT60 monotonicity")
