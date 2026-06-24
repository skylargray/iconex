#!/usr/bin/env python3
"""3.1 Route A, step 3: FAITHFUL live-modulated CONCERT decay (EDC).

Replays the firmware's ACTUAL captured WCS frame stream (exp_modcap.py -> _modframes.npz)
through the bit-exact integer ARU datapath, one output sample at a time, advancing to the
next captured frame when sample-time crosses its (icount-mapped) timestamp.

Why this is faithful (not the approximate exp_modlive):
  * The modulated steps (56/57/107/108) carry the firmware's swept integer offset AND swept
    lane3 coefficient. That lane3 coeff IS the all-pass interpolation coefficient (0xAE8E
    write). Running the real microcode with these real swept values reproduces the all-pass
    fractional-delay chorus EXACTLY -- no linear interp, no guessed triangle/rate/depth.
  * The de-zipper param ramps are included (they are in the captured frames too).

The ONE free parameter is the SBC instruction rate (ins/sec), which sets samples-per-ins =
Fs / ins_per_sec, hence how fast the captured (icount-stamped) modulation maps to audio time.
The SBC Z80 clock is undocumented (the 4.608 MHz crystal in the docs is the LARC 8749, not the
SBC) and the emulator counts instructions, not T-states -- so we SWEEP a plausible band and
report whether the decay verdict is robust to that uncertainty (plan 3.4).

Static baseline for comparison: freeze frame 0 (no modulation) -> grows ~+1000 ppm (sustains).

Usage:
  python exp_live.py                 # sweep ins/sec band, summarize
  python exp_live.py <nsamp> <ins_per_sec> [imp]   # single faithful run
"""
import sys, os, math
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np
import aru_datapath as A

DMASK = A.DMASK
NATIVE_HZ = 34130.0
NPZ = os.path.join(os.path.dirname(os.path.abspath(__file__)), "_modframes.npz")


def prog_from_image(img):
    """Decode a 512-byte WCS image (active-low) into the active-step list, matching
    aru_datapath.load_microcode. cs = resolved 6-bit signed coeff (+/-(abs(coeff)>>1))."""
    prog = []
    for s in range(128):
        l0, l1, l2, l3 = int(img[s*4]), int(img[s*4+1]), int(img[s*4+2]), int(img[s*4+3])
        if l2 == 0xFF and l3 == 0xFF:
            continue
        ctl = (~l2) & 0xFF
        offset = (~(l0 | (l1 << 8))) & 0xFFFF
        coeff = (-(l3 & 0x7F) if l3 & 0x80 else (l3 & 0x7F))
        cs = -(abs(coeff) >> 1) if coeff < 0 else (abs(coeff) >> 1)
        prog.append(dict(offset=offset, cs=cs,
                         ZERO=(ctl >> 7) & 1, b3=(ctl >> 3) & 1,
                         XFER=(ctl >> 2) & 1, WA=ctl & 3, RA=(ctl >> 4) & 3))
    return prog


def load_frames():
    d = np.load(NPZ)
    fr = d['frames'].astype(np.uint8)
    ic = d['icounts'].astype(np.int64)
    start_ic = int(d['start_ic'])
    rel = (ic - start_ic)                    # ins since main loop, per frame
    progs = [prog_from_image(fr[k]) for k in range(len(fr))]
    return progs, rel, d


def run_replay(progs, frame_start_samp, nsamp, imp, BLK=512):
    """Integer datapath, time-varying microcode. State persists across frames.
    frame_start_samp[k] = output-sample index at which frame k becomes active."""
    R = [0, 0, 0, 0]; ACC = 0; RES = 0
    DM = [0] * (DMASK + 1); pos = 0
    nf = len(progs); fi = 0
    block = []; env = []
    sat20 = A.sat20; sat16 = A.sat16
    for n in range(nsamp):
        while fi + 1 < nf and frame_start_samp[fi + 1] <= n:
            fi += 1
        prog = progs[fi]
        pos = (pos + 1) & DMASK
        esum = 0
        for j, st in enumerate(prog):
            addr = (pos - st['offset']) & DMASK
            dab = RES if st['b3'] else DM[addr]
            if n == 0 and j == 0:
                dab += imp
            x = R[st['RA']]; R[st['WA']] = dab
            if st['ZERO']: ACC = 0
            ACC = sat20(ACC + (((x << 3) * st['cs']) >> 6))
            if st['XFER']: RES = sat16(ACC >> 3)
            if st['b3']: DM[addr] = RES
            if st['XFER']: esum += abs(RES)
        block.append(esum)
        if len(block) == BLK:
            env.append(math.sqrt(sum(v*v for v in block) / BLK)); block = []
    return env


def lyapunov_live(progs, fss, nsamp, K=128, seed=1e4, drop=0.34):
    """FLOAT (saturation-free) Lyapunov exponent of the time-varying linear map under live
    modulation -- the correct LTV generalization of the static structural lambda. Power
    iteration with proper L2-norm renorm every K samples; returns the per-sample growth
    factor (geometric mean over the converged tail). lam<1 => the live tank DECAYS even
    though every frozen snapshot has lam>1.  Mirrors exp_lambda_clean.lambda_trajectory but
    advances progs at the control-tick rate."""
    R = [0.0]*4; ACC = 0.0; RES = 0.0
    DM = [0.0]*(DMASK+1); pos = 0
    nz = set(); seeded = False
    nf = len(progs); fi = 0
    logs = []
    for n in range(nsamp):
        while fi + 1 < nf and fss[fi + 1] <= n:
            fi += 1
        prog = progs[fi]
        pos = (pos + 1) & DMASK
        for j, st in enumerate(prog):
            addr = (pos - st['offset']) & DMASK
            dab = RES if st['b3'] else DM[addr]
            if not seeded and j == 0:
                dab += seed; seeded = True
            x = R[st['RA']]; R[st['WA']] = dab
            if st['ZERO']: ACC = 0.0
            ACC = ACC + x*8.0*st['cs']/64.0
            if st['XFER']: RES = ACC/8.0
            if st['b3']: DM[addr] = RES; nz.add(addr)
        if (n+1) % K == 0:
            s = math.sqrt(ACC*ACC + RES*RES + sum(v*v for v in R)
                          + sum(DM[i]*DM[i] for i in nz)) + 1e-300
            logs.append(math.log(s))
            f = 1.0/s
            R = [v*f for v in R]; ACC *= f; RES *= f
            for i in nz: DM[i] *= f
    tail = logs[int(len(logs)*drop):]
    if not tail:
        return None, logs
    lam = math.exp(sum(tail)/len(tail)/K)
    return lam, logs


def edc_slope(env, frac_skip=0.3, BLK=512):
    """dB/s over the latter (1-frac_skip) of the envelope; RT60 = -60/dbs."""
    skip = int(len(env) * frac_skip)
    xs = [i for i in range(skip, len(env)) if env[i] > 0]
    if len(xs) < 8:
        return None, None, (max(env) if env else 0)
    ys = [20*math.log10(env[i]) for i in xs]
    m = len(xs); sx = sum(xs); sy = sum(ys)
    sxx = sum(x*x for x in xs); sxy = sum(x*y for x, y in zip(xs, ys))
    db_blk = (m*sxy - sx*sy) / (m*sxx - sx*sx)
    dbs = db_blk * NATIVE_HZ / BLK
    rt = (-60.0 / dbs) if dbs < -1e-4 else float('inf')
    return dbs, rt, max(env)


def fmt_rt(rt):
    return 'SUSTAIN/GROW' if (rt is None or rt == float('inf')) else f'{rt:.1f}s'


def fmt_dbs(dbs):
    return 'n/a' if dbs is None else f'{dbs:+.3f}'


def single(nsamp, ins_per_sec, imp):
    progs, rel, d = load_frames()
    k = NATIVE_HZ / ins_per_sec                       # samples per SBC instruction
    fss = [int(r * k) for r in rel]
    total_audio = rel[-1] * k / NATIVE_HZ
    print(f"frames={len(progs)}  timeline={rel[-1]} ins = {total_audio:.1f}s audio @ {ins_per_sec/1e6:.3f}M ins/s")
    print(f"requested nsamp={nsamp} ({nsamp/NATIVE_HZ:.1f}s); samples/ins k={k:.5f}")
    if nsamp < 5000:
        print("  (note: nsamp too small for a slope fit; use >= ~120000 for a real EDC)")
    # live modulated
    env = run_replay(progs, fss, nsamp, imp)
    dbs, rt, pk = edc_slope(env)
    print(f"\nLIVE modulated:  dB/s={fmt_dbs(dbs)}  RT60={fmt_rt(rt)}  peakEnv={pk:.0f}")
    # static baseline: freeze frame 0
    envs = run_replay([progs[0]], [0], nsamp, imp)
    dbs0, rt0, pk0 = edc_slope(envs)
    print(f"STATIC (frame0): dB/s={fmt_dbs(dbs0)}  RT60={fmt_rt(rt0)}  peakEnv={pk0:.0f}")
    if dbs is not None and dbs0 is not None:
        print(f"\n  modulation delta: {dbs-dbs0:+.3f} dB/s (negative = adds loss)")
    print("\n  NOTE: the integer EDC is masked by the saturation limit cycle; the decisive"
          "\n  decay metric is the saturation-free Lyapunov exponent -> run:  python exp_live.py lyap")


def sweep():
    progs, rel, d = load_frames()
    rate = int(d['rate']); depth = int(d['depth'])
    print(f"=== FAITHFUL live-modulated CONCERT decay (frame replay) ===")
    print(f"frames={len(progs)} timeline={rel[-1]} ins  rate={rate} depth={depth}")
    print(f"target hardware: clean single-exponential, RT60 ~ 20 s (P85)\n")
    imp = 20000
    # plausible SBC ins/sec band (Z80 ~2-4 MHz, avg ~6-12 T-states/ins => ~200k-660k ins/s)
    print(f"{'ins/sec':>9} {'~chorus':>8} {'audio_s':>8} | {'LIVE dB/s':>10} {'RT60':>13} | {'STATIC dB/s':>11} {'delta':>8}")
    # static baseline once at a reference length
    for ins_per_sec in (200_000, 300_000, 417_000, 550_000):
        k = NATIVE_HZ / ins_per_sec
        fss = [int(r * k) for r in rel]
        nsamp = int(rel[-1] * k)                       # cover whole captured timeline
        audio_s = nsamp / NATIVE_HZ
        f_chorus = ins_per_sec / 688000.0              # full triangle ~688k ins
        env = run_replay(progs, fss, nsamp, imp)
        dbs, rt, pk = edc_slope(env)
        envs = run_replay([progs[0]], [0], nsamp, imp)
        dbs0, rt0, _ = edc_slope(envs)
        print(f"{ins_per_sec:>9} {f_chorus:>7.2f}H {audio_s:>7.1f}s | {dbs:>+10.3f} {fmt_rt(rt):>13} | "
              f"{dbs0:>+11.3f} {dbs-dbs0:>+8.3f}")


def lyap_sweep():
    """Decisive saturation-free test: per-sample Lyapunov exponent of the FLOAT live-modulated
    linear map vs the frozen static snapshot, across the plausible SBC-clock band. lam<1 means
    the live tank decays (the modulation stabilizes the linearly-unstable static tank)."""
    progs, rel, d = load_frames()
    print("=== FLOAT Lyapunov: live-modulated vs static (saturation-free LTV growth) ===")
    print(f"frames={len(progs)} timeline={rel[-1]} ins\n")
    # static baseline (frozen frame 0), k-independent
    lam0, _ = lyapunov_live([progs[0]], [0], 60000, K=128)
    print(f"STATIC (frozen frame0): lambda={lam0:.7f}  ({(lam0-1)*1e6:+.1f} ppm, "
          f"{'GROW' if lam0 > 1 else 'DECAY'})\n")
    print(f"{'ins/sec':>9} {'~chorusHz':>9} {'nsamp':>8} | {'LIVE lambda':>12} {'ppm':>9} {'verdict':>7} {'dRT60(s)':>9}")
    for ins_per_sec in (200_000, 300_000, 417_000, 550_000, 700_000):
        k = NATIVE_HZ / ins_per_sec
        fss = [int(r * k) for r in rel]
        nsamp = int(rel[-1] * k)
        f_chorus = ins_per_sec / 688000.0
        lam, _ = lyapunov_live(progs, fss, nsamp, K=128)
        ppm = (lam - 1)*1e6
        verdict = 'GROW' if lam > 1 else 'DECAY'
        rt = (-3.0 / (math.log10(lam) * NATIVE_HZ)) if lam < 1 else float('inf')
        rts = f'{rt:.1f}' if rt != float('inf') else 'inf'
        print(f"{ins_per_sec:>9} {f_chorus:>8.2f}H {nsamp:>8} | {lam:>12.7f} {ppm:>+9.1f} {verdict:>7} {rts:>9}")


if __name__ == '__main__':
    if len(sys.argv) >= 2 and sys.argv[1] == 'lyap':
        lyap_sweep()
    elif len(sys.argv) >= 3:
        nsamp = int(sys.argv[1]); ins_per_sec = float(sys.argv[2])
        imp = int(sys.argv[3]) if len(sys.argv) > 3 else 20000
        single(nsamp, ins_per_sec, imp)
    else:
        sweep()
