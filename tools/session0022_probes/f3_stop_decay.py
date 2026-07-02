#!/usr/bin/env python3
"""F3 (plan 024) — the stop-decay dynamic, closed end-to-end: the ONE documented
audio->8080 feedback edge, fed live.

F3a FINDINGS (disassembly, this session — tools/dis224.py on the NVS window):
  * The input-level detector's SOURCE = the DSP->host X-REGISTER readback:
      0x829D..0x82CD:  IN A,(0x07); |.|; if 0 -> IN A,(0x06); |.|   (one's-comp abs)
                       0x3E38 <- max(0x3E38, |XREG|)                (peak hold)
    and the WCS supplies it: CONCERT row 0 (CPU w127) — the RD-AD INPUT word itself —
    carries WR XREG (sel=3, WRX): THE RAW A/D INPUT SAMPLE is posted to the latch
    every frame. The detector is a true INPUT-level detector.
  * 0x82F8..0x830A: the peak is log-compressed (MSB-normalize + 0x0FB7) and GATED:
    below 0xBC the instant level clamps to the floor 0x10 -> 0x3E3D.
  * 0x8317..: 0x3E10 = the RUNNING level (instant attack, decay via the 0x3E15..0x3E1F
    10-deep history ring shifted per tick, 0x83F8).
  * 0x83A4..0x83C6: on a level JUMP >= 0x27 with the DynDecay toggle armed
    (0x3CCD bit 0) and 0x3C51 bit 0 clear: 0x3C51 <- 0xC1 (the DynDecay state byte —
    the same value the V6/V7 variation recalls park there).
  * 0x83D1..: a second path gated by 0x3CCD bit 7 stages 0x3E11/0x3E12/0x3E14 from
    deltas of the ring (0x16/0x18 thresholds) — the stop/run scheduling state.

F3b (this probe): extend the co-sim with that one edge — per frame the engine's
XREG_wr (the re-synced RTL22 maintains the CPU-domain readback of the WRX step) is
served to the 8080 at IN 0x06/0x07 — and drive burst-then-silence on V6 (DynDecay ON,
recalled through the REAL variation keys).

PREDICTIONS (declared before the runs):
  P1  the level state (0x3E10/0x3E3D) tracks the burst and falls after it stops;
  P2  V6 run A (live feed): the w44-family coefficient FLIPS between the burst phase
      and the silent tail (the captured parked value 9 <-> its mirror 22), the
      running<->stopped switch;
  P3  V6 run B (level forced loud through the tail): NO flip — the tail renders under
      the RUNNING coefficients; the mid-band tail decay of run A differs from run B
      (the documented direction for V1: stops 3.0 vs running 2.0 — stopping LENGTHENS
      the mid decay; direction for V6 recorded here);
  P4  V1 control (DynDecay toggle off): no flip under the live feed.

RESULTS (two runs + f3b_switch_hunt.py — the correction to P2/P3's TARGET):
  P1 PASS (0x3E10 tracks the burst; the forced-loud control holds it); P4 PASS.
  P2/P3 as WRITTEN failed because the w44 family was the WRONG TARGET: w44's 9-vs-22
  is the V6-vs-V7 VARIATION difference, not the runtime dynamic. The hunt shows the
  real mechanism: ~151 ms after the input stops (the documented switch DELAY), the
  stop event stages (0x3E11<-1, 0x3E14<-0x0F) and a de-zipper walk (~24 frames/word)
  steps the cmag of the TWELVE-word family w62/63/64/66/67/68 (+51 mirrors
  w113/114/115/117/118/119) DOWN one unit at a time (11 -> 10 -> 9) as the level
  falls through the ring-history thresholds — and back UP when level returns: a
  GRADUATED decay-coefficient scheduler, not a binary flip. The loudness gates
  0x80/0xBC sit above the XREG-log ceiling (~0x37 for near-FS input) — those paths
  belong to another source (0x3C62 OR-term, an overload flag candidate).
  Named leftovers: the late-tail 0x3E10 hops (0x07<->0x17 at ~LFO period under
  zero input — a firmware-side interaction, source untraced); the audible
  stop-vs-running tail contrast (needs the page-2 Stop sliders set apart from the
  running decays, next session).
"""
import sys, os, json

TOOLS = r"d:\OneDrive\Gray Instruments\iconex\tools"
sys.path.insert(0, TOOLS)
HERE = os.path.dirname(os.path.abspath(__file__))
RENDERS = os.path.join(HERE, "renders")
os.makedirs(RENDERS, exist_ok=True)

import numpy as np
import boot8080
from probe_run import run_ticks
from aru_freerun22_rtl import RTL22, program_rows22, fs22, decode_word
from e4_variations import SerialIO, send_key
import reverb_metrics as RM

TICKS_PER_FRAME = 62
SETTLE = 6_000_000
FLAG = 0x3C14
KEY_VAR = 0x26
KEY_NUM = {1: 0x2C, 2: 0x30, 3: 0x34, 4: 0x38, 5: 0x3C, 6: 0x2D, 7: 0x31, 8: 0x35}
WATCH = (43, 44, 45, 95, 96, 97)              # the shelf/decay corrective family
BURST_S, TAIL_S = 0.60, 4.00
AMP = 28000        # the 0x82F8 loudness gate floors instant levels below 0xBC:
                   # a -8.7 dB burst (12000) never crossed it (first run) — drive near FS


def boot_variation(var):
    m, ms = boot8080.boot(verbose=False)
    assert "mainloop" in ms
    run_ticks(m, SETTLE)
    io = SerialIO(m)
    if var != 1:
        send_key(m, io, KEY_VAR)
        send_key(m, io, KEY_NUM[var])
        run_ticks(m, SETTLE)
    return m


def cosim(m, force_loud=None, seed=224):
    """Inline co-sim with the level feedback edge. force_loud: after the burst, feed
    the 8080 a constant loud |sample| instead of the true (silent) XREG_wr."""
    base = bytes(m.memory[0x4000:0x4200])
    wcs = [(base[4*k], base[4*k+1], base[4*k+2], base[4*k+3]) for k in range(128)]
    rows, L, w_reset = program_rows22(wcs)
    fs = fs22(L)
    nb, n = int(BURST_S * fs), int((BURST_S + TAIL_S) * fs)
    rng = np.random.default_rng(seed)
    exc = np.zeros(n, dtype=np.int64)
    exc[:nb] = rng.integers(-AMP, AMP + 1, nb)

    eng = RTL22()
    prev = bytes(base)
    state = {"xw": 0}

    def on_input(port):
        p = port & 0xFF
        if p == 0x06:
            return state["xw"] & 0xFF
        if p == 0x07:
            return (state["xw"] >> 8) & 0xFF
        if p == 0xEF:
            return 0x01
        if p == 0xEE:
            return 0xFF
        return 0x00

    m.set_input_callback(on_input)

    chans = {c: np.zeros(n, dtype=np.int32) for c in "AC"}
    log = {k: np.zeros(n, np.uint8) for k in
           ("w44", "w96", "lvl10", "lvl3d", "st51", "e11", "e12", "e14")}
    for i in range(n):
        for c, v in eng.run_sample(rows, int(exc[i]) & 0xFFFF):
            if c in chans:
                chans[c][i] = v
        state["xw"] = eng.XREG_wr if (force_loud is None or i < nb) else force_loud
        m.memory[FLAG] = 0x80
        run_ticks(m, TICKS_PER_FRAME, chunk=TICKS_PER_FRAME)
        cur = bytes(m.memory[0x4000:0x4200])
        if cur != prev:
            for w in range(128):
                o = 4 * w
                if cur[o:o+4] != prev[o:o+4]:
                    r = 127 - w
                    if 0 <= r < len(rows):
                        rows[r] = decode_word((cur[o], cur[o+1], cur[o+2], cur[o+3]))
            prev = cur
        log["w44"][i] = ((cur[4*44+3] ^ 0xFF) >> 2) & 0x3F
        log["w96"][i] = ((cur[4*96+3] ^ 0xFF) >> 2) & 0x3F
        log["lvl10"][i] = m.memory[0x3E10]
        log["lvl3d"][i] = m.memory[0x3E3D]
        log["st51"][i] = m.memory[0x3C51]
        log["e11"][i] = m.memory[0x3E11]
        log["e12"][i] = m.memory[0x3E12]
        log["e14"][i] = m.memory[0x3E14]
    return chans, log, fs, nb, n, exc


def phases(a, nb, fs):
    """Distinct values of a per phase + the flip frame (first change after the burst)."""
    burst = sorted(set(int(v) for v in a[nb//2:nb]))
    tail = sorted(set(int(v) for v in a[nb + int(0.8*fs):]))
    flips = np.nonzero(np.diff(a[nb:].astype(np.int16)))[0]
    return burst, tail, (int(flips[0]) if len(flips) else None)


def midband_t30(x, fs):
    from scipy.signal import butter, sosfiltfilt
    sos = butter(4, 720.0 / (fs / 2), "highpass", output="sos")
    t = RM._noise_floor_truncate(sosfiltfilt(sos, np.asarray(x, np.float64)), fs)
    edc = RM._schroeder_db(t)
    rt, r2, npts = RM._fit_decay(edc, fs, -5.0, -35.0)
    if rt is None:
        rt, r2, npts = RM._fit_decay(edc, fs, -5.0, -25.0)
    return rt


def report(tag, chans, log, fs, nb, n):
    b44, t44, flip = phases(log["w44"], nb, fs)
    b96, t96, _ = phases(log["w96"], nb, fs)
    lvl_b = int(log["lvl10"][nb//2:nb].max())
    lvl_t = int(log["lvl10"][n - int(0.5*fs):].max())
    l3d_b = int(log["lvl3d"][nb//2:nb].max())
    st = sorted(set(int(v) for v in log["st51"]))
    print(f"[{tag}] w44 burst={b44} tail={t44} (flip @tail+{flip} fr"
          f"{f' = {flip/fs*1000:.0f} ms' if flip is not None else ''}); w96 {b96}->{t96}")
    print(f"       level 0x3E10 burst max=0x{lvl_b:02X} tail-end max=0x{lvl_t:02X}; "
          f"instant 0x3E3D burst max=0x{l3d_b:02X} (gate 0xBC); "
          f"0x3C51 states={[hex(v) for v in st]}")
    print(f"       stage bytes: 0x3E11 {sorted(set(int(v) for v in log['e11']))} "
          f"0x3E12 {sorted(set(int(v) for v in log['e12']))} "
          f"0x3E14 {sorted(set(int(v) for v in log['e14']))}")
    rts = {}
    for c in "AC":
        rts[c] = midband_t30(chans[c][nb:], fs)
        RM.write_wav(RENDERS, f"f3_{tag}_ch{c}",
                     np.clip(chans[c], -32768, 32767).astype(np.int16), int(fs))
    print(f"       tail mid-band T30: chA={rts['A'] if rts['A'] else float('nan'):.2f} s  "
          f"chC={rts['C'] if rts['C'] else float('nan'):.2f} s")
    return dict(b44=b44, t44=t44, flip=flip, rts=rts, lvl_b=lvl_b, lvl_t=lvl_t)


def main():
    print(__doc__.split("PREDICTIONS")[1])
    print("=== run A: V6, live level feed (burst then true silence) ===", flush=True)
    m = boot_variation(6)
    tgl = m.memory[0x3CCD]
    print(f"V6 recalled: toggles 0x3CCD=0x{tgl:02X} (bit0 = DynDecay arm = {tgl & 1})")
    A = report("V6-live", *cosim(m)[0:5])

    print("\n=== run B: V6, level FORCED LOUD through the tail (running control) ===",
          flush=True)
    m = boot_variation(6)
    B = report("V6-forced", *cosim(m, force_loud=0x6000)[0:5])

    print("\n=== run C: V1 control (DynDecay off), live feed ===", flush=True)
    m = boot_variation(1)
    tgl = m.memory[0x3CCD]
    print(f"V1: toggles 0x3CCD=0x{tgl:02X}")
    C = report("V1-live", *cosim(m)[0:5])

    print("\n### verdicts ###")
    p1 = A["lvl_b"] > A["lvl_t"]
    print(f"P1 level tracks the burst: {'PASS' if p1 else 'FAIL'} "
          f"(burst 0x{A['lvl_b']:02X} -> tail 0x{A['lvl_t']:02X})")
    p2 = A["flip"] is not None and set(A["b44"]) != set(A["t44"])
    print(f"P2 V6 running<->stopped flip: {'PASS' if p2 else 'FAIL'} "
          f"(w44 {A['b44']} -> {A['t44']})")
    fmt = lambda x: f"{x:.2f}" if x else "n/a"
    p3 = B["flip"] is None or set(B["b44"]) == set(B["t44"])
    print(f"P3 forced-loud holds the running state: {'PASS' if p3 else 'FAIL'} "
          f"(w44 {B['b44']} -> {B['t44']}); tail mid T30 A vs B: "
          f"{fmt(A['rts']['A'])}/{fmt(A['rts']['C'])} vs {fmt(B['rts']['A'])}/{fmt(B['rts']['C'])}")
    p4 = C["flip"] is None
    print(f"P4 V1 (unarmed) does not flip: {'PASS' if p4 else 'FAIL'} "
          f"(w44 {C['b44']} -> {C['t44']})")
    print("\nfailures here re-open: the F3a XREG-source reading (none of the registry "
          "entries — this is the first dynamics probe).")


if __name__ == "__main__":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass
    main()
