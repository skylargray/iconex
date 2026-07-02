#!/usr/bin/env python3
"""d2i (session 0026) — render oracles for the d2h parameter images (documented behavior
per ch.4/ch.8; comparisons are lo-vs-hi within a pair, so the post-Definition ladder
hysteresis in the cache cancels).

  DEP (p1s5)   ch.4: "the Depth slider affects Outputs A and C only" -> A/C early energy
               moves, B/D invariant.
  Treble(p1s4) 8 kHz-octave RT60 must move (doc corner 170 Hz..19 kHz).
  HF-BW(p2s4)  late-tail spectral corner must move (doc 170 Hz..19 kHz; default 9 kHz).
  Dif  (p2s5)  early normalized echo density must move (doc 0..99, default 25).
  Def  (p2s6)  hi rewrites the ladder+allpasses (word map); measure RT60/NED empirically.
  XOV  (p1s3)  BYTE oracle: w45/w97 cmag at lo/hi -> one-pole corner fs*ln(32/c)/2pi vs the
               documented endpoints 170 Hz / 19.0 kHz.
  PE levels    STEREO impulse renders: L-only -> taps on A (PE1) and C (PE4); R-only ->
               C (PE2) and A (PE3); tap positions must land at the DOCUMENTED default
               delays 5.00/9.75/17.5/25.0 ms (the fs and routing ride along).
  PE delays    BYTE oracle: words 80/28/79/27 ofst lanes at lo/hi vs the 0..188 ms range.
  FinePD       L: chA arrival shift (0..31.3 ms); R: byte oracle on word 31.
"""
import sys, os, json

TOOLS = r"d:\OneDrive\Gray Instruments\iconex\tools"
sys.path.insert(0, TOOLS)
HERE = os.path.dirname(os.path.abspath(__file__))

import numpy as np
from scipy.signal import butter, sosfiltfilt
import reverb_metrics as RM
from aru_freerun22_rtl import RTL22, program_rows22, fs22, decode_word

cache = json.load(open(os.path.join(HERE, "d2h_param_wcs.json")))


def img(key):
    return bytes.fromhex(cache[key])


def rows_of(b):
    return program_rows22([(b[4*k], b[4*k+1], b[4*k+2], b[4*k+3]) for k in range(128)])


def render(b, sig, n):
    rows, L, w = rows_of(b)
    return RTL22().run_free(rows, sig, n), fs22(L)


def burst_pair(key_lo, key_hi, seconds=5.0):
    out = {}
    for tag, key in (("lo", key_lo), ("hi", key_hi)):
        b = img(key)
        rows, L, w = rows_of(b)
        fs = fs22(L)
        n = int(seconds * fs)
        nb = int(0.30 * fs)
        exc = np.zeros(n, dtype=np.int64)
        exc[:nb] = np.random.default_rng(224).integers(-8000, 8001, nb)
        sil = RTL22().run_free(rows, [0] * n, n)
        bur = RTL22().run_free(rows, list(int(v) for v in exc), n)
        out[tag] = (bur, sil, fs, nb)
    return out


def rt60_band(tail, fs, kind=None, f0=None, f1=None):
    x = tail
    if kind:
        ny = fs / 2
        sos = (butter(4, [f0 / ny, min(f1 / ny, 0.98)], "bandpass", output="sos")
               if kind == "band" else butter(4, f0 / ny, kind, output="sos"))
        x = sosfiltfilt(sos, tail)
    t = RM._noise_floor_truncate(np.asarray(x, np.float64), fs)
    edc = RM._schroeder_db(t)
    for win in ((-5.0, -35.0), (-5.0, -25.0), (-3.0, -15.0)):
        rt, r2, npts = RM._fit_decay(edc, fs, *win)
        if rt:
            return rt
    return float("nan")


def diff_ch(bur, sil, c):
    return np.asarray(bur[c], np.float64) - np.asarray(sil[c], np.float64)


print("### DEP (p1s5) — ch.4: 'affects Outputs A and C only' ###")
pair = burst_pair("p1s5-lo", "p1s5-hi", 2.5)
for c in "ABCD":
    e = {}
    for tag in ("lo", "hi"):
        bur, sil, fs, nb = pair[tag]
        d = diff_ch(bur, sil, c)
        e[tag] = float(np.sqrt(np.mean(d[:int(0.08 * fs)] ** 2)))
    ratio = 20 * np.log10(e["hi"] / max(e["lo"], 1e-9))
    print(f"  ch{c}: early(80ms) RMS lo={e['lo']:7.1f} hi={e['hi']:7.1f}  ({ratio:+5.1f} dB)"
          f"{'   <- must move' if c in 'AC' else '   <- must NOT move'}")

print("\n### Treble Decay (p1s4) — 8 kHz octave RT60 ###")
pair = burst_pair("p1s4-lo", "p1s4-hi", 5.0)
for tag in ("lo", "hi"):
    bur, sil, fs, nb = pair[tag]
    d = diff_ch(bur, sil, "A")[nb:]
    print(f"  {tag}: 8k-band RT60 = {rt60_band(d, fs, 'band', 8000/2**0.5, 8000*2**0.5):.2f} s"
          f"   (mid ref {rt60_band(d, fs, 'high', 720.0):.2f})")

print("\n### HF Bandwidth (p2s4) — late-tail spectral corner ###")
pair = burst_pair("p2s4-lo", "p2s4-hi", 3.0)
for tag in ("lo", "hi"):
    bur, sil, fs, nb = pair[tag]
    d = diff_ch(bur, sil, "A")
    seg = d[nb:nb + int(1.0 * fs)]
    spec = np.abs(np.fft.rfft(seg * np.hanning(len(seg))))
    fr = np.fft.rfftfreq(len(seg), 1 / fs)
    smooth = np.convolve(spec ** 2, np.ones(64) / 64, "same")
    ref = np.mean(smooth[(fr > 500) & (fr < 2000)])
    above = np.where((fr > 2000) & (smooth > ref / 10))[0]
    corner = fr[above[-1]] if len(above) else 0.0
    print(f"  {tag}: -10 dB(re 0.5-2k) upper edge ~ {corner:6.0f} Hz")

print("\n### Diffusion (p2s5) — early echo density (NED) ###")
pair = burst_pair("p2s5-lo", "p2s5-hi", 2.0)
for tag in ("lo", "hi"):
    bur, sil, fs, nb = pair[tag]
    d = diff_ch(bur, sil, "A")
    ned = RM.normalized_echo_density(d[nb:nb + int(0.25 * fs)], fs)
    ned_v = float(np.mean(ned)) if np.ndim(ned) else float(ned)
    print(f"  {tag}: early NED = {ned_v:.3f}")

print("\n### Definition (p2s6) — empirical (hi rewrites ladder+allpasses) ###")
pair = burst_pair("p2s6-lo", "p2s6-hi", 5.0)
for tag in ("lo", "hi"):
    bur, sil, fs, nb = pair[tag]
    d = diff_ch(bur, sil, "A")[nb:]
    print(f"  {tag}: broadband RT60 = {rt60_band(d, fs):.2f} s")

print("\n### Crossover (p1s3) — BYTE oracle: w45 cmag -> one-pole corner ###")
for tag in ("lo", "hi"):
    b = img(f"p1s3-{tag}")
    d45 = decode_word((b[4*45], b[4*45+1], b[4*45+2], b[4*45+3]))
    c = d45["cmag"]
    fs0 = 32508.0
    fc = fs0 * np.log(32.0 / max(c, 1)) / (2 * np.pi)
    print(f"  {tag}: w45 cmag={c:2d} cs={d45['cs']} -> corner ~ {fc:7.0f} Hz "
          f"(documented range 170 Hz .. 19.0 kHz)")

print("\n### Preecho LEVELS (p3s1-4) — stereo impulse taps at the DOCUMENTED delays ###")
print("    (doc defaults: PE1 5.00ms L>A, PE2 9.75ms R>C, PE3 17.5ms R>A, PE4 25.0ms L>C)")


def early_taps(b, side, chan, label):
    rows, L, w = rows_of(b)
    fs = fs22(L)
    T0 = 400
    n = T0 + int(0.30 * fs)
    imp = [(0, 0)] * n
    imp[T0] = (16000, 0) if side == "L" else (0, 16000)
    sil = RTL22().run_free(rows, [(0, 0)] * n, n)
    out = RTL22().run_free(rows, imp, n)
    d = np.asarray(out[chan], np.float64) - np.asarray(sil[chan], np.float64)
    seg = np.abs(d[T0:T0 + int(0.20 * fs)])
    th = 0.15 * seg.max()
    pk = []
    for i in range(1, len(seg) - 1):
        if seg[i] > th and seg[i] >= seg[i - 1] and seg[i] >= seg[i + 1]:
            if not pk or (i - pk[-1][0]) > int(0.0015 * fs):
                pk.append((i, seg[i]))
            elif seg[i] > pk[-1][1]:
                pk[-1] = (i, seg[i])
    print(f"  {label}: peaks(ms) " +
          ", ".join(f"{i / fs * 1000:5.2f}({v / seg.max():.2f})" for i, v in pk[:6]))


base = img("base")
early_taps(base, "L", "A", "base      L->A")
early_taps(img("p3s1-hi"), "L", "A", "PE1-hi    L->A")
early_taps(img("p3s2-hi"), "R", "C", "PE2-hi    R->C")
early_taps(img("p3s3-hi"), "R", "A", "PE3-hi    R->A")
early_taps(img("p3s4-hi"), "L", "C", "PE4-hi    L->C")

print("\n### Preecho DELAYS (p4s1-4) + FinePD-R — BYTE oracle on the tap words ###")
TAPW = {("p4s1", 80): "PE-Dly1", ("p4s2", 28): "PE-Dly2", ("p4s3", 79): "PE-Dly3",
        ("p4s4", 27): "PE-Dly4", ("p4s6", 31): "FinePD-R"}
fs0 = 32508.0
for (slot, w), name in TAPW.items():
    line = [f"  {name} (w{w}):"]
    for tag in ("lo", "hi"):
        b = img(f"{slot}-{tag}")
        bb = img("base")
        db, dl = decode_word((bb[4*w], bb[4*w+1], bb[4*w+2], bb[4*w+3])), \
                 decode_word((b[4*w], b[4*w+1], b[4*w+2], b[4*w+3]))
        line.append(f"{tag}: ofst 0x{db['ofst']:04X}->0x{dl['ofst']:04X} "
                    f"(D {abs(dl['ofst'] - db['ofst'])} fr = "
                    f"{abs(dl['ofst'] - db['ofst']) / fs0 * 1000:6.2f} ms)")
    print("  ".join(line))

print("\n### FinePD-L (p4s5) — chA arrival shift ###")
for tag, key in (("base", "base"), ("hi", "p4s5-hi")):
    b = img(key)
    rows, L, w = rows_of(b)
    fs = fs22(L)
    T0 = 400
    n = T0 + int(0.30 * fs)
    imp = [(0, 0)] * n
    imp[T0] = (16000, 0)
    sil = RTL22().run_free(rows, [(0, 0)] * n, n)
    out = RTL22().run_free(rows, imp, n)
    d = np.asarray(out["A"], np.float64) - np.asarray(sil["A"], np.float64)
    seg = np.abs(d[T0:])
    first = int(np.argmax(seg > 0.05 * seg.max()))
    print(f"  {tag}: chA first arrival {first / fs * 1000:6.2f} ms "
          f"(doc range 0..31.3 ms; hi byte 0xF0 = 240/8 = 30 ms)")
