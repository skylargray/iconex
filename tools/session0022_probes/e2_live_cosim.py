#!/usr/bin/env python3
"""E2 (plan 023) — the TRUE live co-sim: the verified 8080 runs interleaved with the
RTL engine at per-frame granularity (62 CPU ticks/frame, the 0022-measured budget),
with the frame-sync ISR flag 0x3C14 fed per frame. Retires the frozen-LFO/50k-tick
approximations (d4lite) and formally closes D2b's last gap.

Structure: the audio path does not feed back into the 8080 (the stop-decay level
detector is untraced — E2d), so the WCS trajectory depends only on ticks: capture the
per-frame mover bytes ONCE from the interleaved run, then render burst + silence with
the SAME per-frame trajectory (floor subtraction stays valid; results identical to
fully-inline rendering).

Verdicts: per-band RT60 (Schroeder T30, Lundeby-truncated, floor-subtracted) vs the
documented presets (LF 3.0 / mid 2.0 / avg 2.6) and the benchmark IR (2.85/1.92/1.99);
LFO period vs 224XL_modulation_lfo.md (~345k instructions); mover trajectory rate vs
the d4lite 50k-tick snapshots.

Usage:  python e2_live_cosim.py [--chorus HEX]   (default: factory recall state)
"""
import sys, os, json, argparse

TOOLS = r"d:\OneDrive\Gray Instruments\iconex\tools"
sys.path.insert(0, TOOLS)
HERE = os.path.dirname(os.path.abspath(__file__))
RENDERS = os.path.join(HERE, "renders")

import numpy as np
from scipy.signal import butter, sosfiltfilt
import reverb_metrics as RM
import boot8080
from probe_run import run_ticks
from aru_freerun22_rtl import RTL22, program_rows22, fs22, decode_word

TICKS_PER_FRAME = 62
REN_S = 6.5
BURST_S = 0.30
MOVER_WORDS = (56, 57, 107, 108)
SETTLE_TICKS = 6_000_000
FLAG = 0x3C14
CHORUS_DEPTH = 0x3CD4
CHORUS_RATE = 0x3CD3


def capture_trajectory(n_frames, chorus=None, check_every=4096):
    """Boot + settle, then per frame: set the ISR flag, run 62 ticks, harvest the mover
    bytes. Full-image spot check every check_every frames catches non-mover drift."""
    m, ms = boot8080.boot(verbose=False)
    assert "mainloop" in ms
    print(f"  settling {SETTLE_TICKS/1e6:.0f}M ticks ...")
    run_ticks(m, SETTLE_TICKS)
    if chorus is not None:
        m.memory[CHORUS_DEPTH] = chorus & 0xFF
        run_ticks(m, 500_000)                          # let the apply chain react
        print(f"  chorus depth byte 0x3CD4 <- 0x{chorus:02X} "
              f"(rate 0x3CD3 = 0x{m.memory[CHORUS_RATE]:02X})")
    base = bytes(m.memory[0x4000:0x4200])
    mv_addr = [4 * w + o for w in MOVER_WORDS for o in range(4)]
    traj = np.empty((n_frames, len(mv_addr)), dtype=np.uint8)
    extra_writes = set()
    print(f"  interleaving {n_frames} frames x {TICKS_PER_FRAME} ticks ...")
    for n in range(n_frames):
        m.memory[FLAG] = 0x80
        run_ticks(m, TICKS_PER_FRAME, chunk=TICKS_PER_FRAME)
        for j, a in enumerate(mv_addr):
            traj[n, j] = m.memory[0x4000 + a]
        if n % check_every == check_every - 1:
            cur = bytes(m.memory[0x4000:0x4200])
            for a in range(0x200):
                if cur[a] != base[a] and a not in mv_addr:
                    extra_writes.add(a)
    return m, base, traj, mv_addr, sorted(extra_writes)


def render(base, traj, mv_addr, sig, n_frames):
    wcs = [(base[4*k], base[4*k+1], base[4*k+2], base[4*k+3]) for k in range(128)]
    rows, L, w_reset = program_rows22(wcs)
    fs = fs22(L)
    row_of = {w: 127 - w for w in MOVER_WORDS}
    eng = RTL22()
    chans = {c: np.zeros(n_frames, dtype=np.int32) for c in "ABCD"}
    cur = [None] * len(MOVER_WORDS)
    for n in range(n_frames):
        for i, w in enumerate(MOVER_WORDS):
            b = traj[n, 4*i:4*i+4]
            t = (int(b[0]), int(b[1]), int(b[2]), int(b[3]))
            if t != cur[i]:
                rows[row_of[w]] = decode_word(t)
                cur[i] = t
        for c, v in eng.run_sample(rows, int(sig[n]) & 0xFFFF):
            chans[c][n] = v
    return chans, fs, L


def band(x, kind, f0, fs):
    sos = butter(4, f0 / (fs / 2), kind, output="sos")
    return sosfiltfilt(sos, x)


def rt60(tail, fs):
    t = RM._noise_floor_truncate(np.asarray(tail, np.float64), fs)
    edc = RM._schroeder_db(t)
    rt, r2, npts = RM._fit_decay(edc, fs, -5.0, -35.0)
    if rt is None:
        rt, r2, npts = RM._fit_decay(edc, fs, -5.0, -25.0)
    return rt


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--chorus", type=lambda s: int(s, 16), default=None)
    args = ap.parse_args()
    tag = "factory" if args.chorus is None else f"chorus{args.chorus:02X}"

    fs_nom = 32508.0
    n_frames = int(REN_S * fs_nom)
    print(f"[E2a] live co-sim capture ({tag}) ...")
    m, base, traj, mv_addr, extra = capture_trajectory(n_frames, chorus=args.chorus)
    print(f"  non-mover WCS drift at spot checks: "
          f"{[hex(0x4000+a) for a in extra] if extra else 'NONE'}")

    # --- trajectory diagnostics: sweep span + period of the mover offsets ---
    ofs = traj[:, 0].astype(np.int32) | (traj[:, 1].astype(np.int32) << 8)   # w56 ofst
    print(f"  w56 ofst: min {ofs.min()} max {ofs.max()} span {ofs.max()-ofs.min()} frames")
    ac = ofs - ofs.mean()
    # dominant period via zero crossings of the smoothed trajectory
    sm = np.convolve(ac, np.ones(201) / 201, mode="same")
    zc = np.where(np.diff(np.signbit(sm)))[0]
    if len(zc) > 3:
        period_frames = 2 * np.mean(np.diff(zc))
        print(f"  LFO period ~ {period_frames:.0f} frames = "
              f"{period_frames*TICKS_PER_FRAME/1e3:.0f}k ticks "
              f"(~{period_frames*TICKS_PER_FRAME/4.5/1e3:.0f}k instructions; "
              f"doc ~345k instructions)")
    json.dump(dict(tag=tag, span=int(ofs.max() - ofs.min()),
                   extra=[int(a) for a in extra],
                   w56_ofst_ds16=[int(v) for v in ofs[::16]]),
              open(os.path.join(HERE, f"e2_cosim_{tag}.json"), "w"), indent=1)

    print(f"[E2b] rendering burst + silence under the live trajectory ...")
    wcs0 = [(base[4*k], base[4*k+1], base[4*k+2], base[4*k+3]) for k in range(128)]
    _, L0, _ = program_rows22(wcs0)
    fs = fs22(L0)
    rng = np.random.default_rng(224)
    exc = np.zeros(n_frames, dtype=np.int64)
    sil = np.zeros(n_frames, dtype=np.int64)
    nb = int(BURST_S * fs)
    exc[:nb] = rng.integers(-8000, 8001, nb)
    silch, fs, L = render(base, traj, mv_addr, sil, n_frames)
    burch, fs, L = render(base, traj, mv_addr, exc, n_frames)

    DOCXOV = 720.0
    print(f"\n### live co-sim per-band RT60 ({tag}; L={L}, fs={fs:.0f}) ###")
    print(f"{'':8}{'LF(<720)':>10}{'mid(>720)':>11}{'broadband':>11}   "
          f"[documented 3.0/2.0/2.6avg; benchmark 2.85/1.92/1.99; d4lite 3.20/2.22/2.67]")
    out = {}
    for c in "AC":
        d = np.asarray(burch[c], np.float64) - np.asarray(silch[c], np.float64)
        tail = d[nb:]
        vals = (rt60(band(tail, "lowpass", DOCXOV, fs), fs),
                rt60(band(tail, "highpass", DOCXOV, fs), fs),
                rt60(tail, fs))
        out[c] = vals
        RM.write_wav(RENDERS, f"e2_cosim_{tag}_ch{c}",
                     np.clip(burch[c], -32768, 32767).astype(np.int16), int(fs))
        print(f"ch{c:6}" + "".join(f"{v if v else float('nan'):>11.2f}" for v in vals))
    print(f"\nWAVs -> renders/e2_cosim_{tag}_ch*.wav")


if __name__ == "__main__":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass
    main()
