#!/usr/bin/env python3
"""Process an arbitrary WAV through a 224XL factory program on the RTL engine
(aru_freerun22_rtl.RTL22) and write the wet result as a stereo WAV (channels A=L, C=R —
the opposite-half-frame output pair).

Pipeline: read WAV (16/24-bit, mono/stereo) -> mono mix -> polyphase resample to the
program's hardware rate (fs = 30.72e6/9/(L+1)) -> drive at -6 dBFS peak -> render with a
silent tail -> subtract the zero-input render (the deterministic Booth-residue limit cycle,
see session 0023 / c3 probe) -> normalize to -3 dBFS -> 16-bit stereo WAV at the engine rate.

Usage: python process_wav_rtl.py IN.wav [OUT.wav] [--image boot|run] [--tail 3.0] [--id 1]
"""
import sys, os, json, argparse, wave, struct
TOOLS = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, TOOLS)
import numpy as np
from fractions import Fraction
from scipy.signal import resample_poly
from aru_freerun22_rtl import RTL22, program_rows22, fs22

HERE = os.path.dirname(os.path.abspath(__file__))


def read_wav_mono(path):
    w = wave.open(path, "rb")
    nch, width, rate, n = w.getnchannels(), w.getsampwidth(), w.getframerate(), w.getnframes()
    raw = w.readframes(n)
    w.close()
    if width == 2:
        x = np.frombuffer(raw, dtype="<i2").astype(np.float64) / 32768.0
    elif width == 3:
        b = np.frombuffer(raw, dtype=np.uint8).reshape(-1, 3)
        x = (b[:, 0].astype(np.int32) | (b[:, 1].astype(np.int32) << 8)
             | (b[:, 2].astype(np.int32) << 16))
        x = np.where(x >= 1 << 23, x - (1 << 24), x).astype(np.float64) / (1 << 23)
    else:
        raise ValueError(f"unsupported sample width {width}")
    x = x.reshape(-1, nch).mean(axis=1)
    return x, rate


def write_wav_stereo(path, left, right, fs):
    y = np.stack([left, right], axis=1).astype("<i2").reshape(-1)
    w = wave.open(path, "wb")
    w.setnchannels(2)
    w.setsampwidth(2)
    w.setframerate(int(round(fs)))
    w.writeframes(y.tobytes())
    w.close()


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("infile")
    ap.add_argument("outfile", nargs="?")
    ap.add_argument("--image", choices=("boot", "run"), default="boot")
    ap.add_argument("--id", default="1", help="program id (boot image only; run has CONCERT)")
    ap.add_argument("--tail", type=float, default=3.0, help="seconds of silence appended")
    ap.add_argument("--drive", type=float, default=16422.0, help="input peak in int16 units")
    args = ap.parse_args()

    if args.image == "boot":
        rec = json.load(open(os.path.join(HERE, "wcs_cache.json")))[args.id]
    else:
        rec = json.load(open(os.path.join(HERE, "wcs_run_concert.json")))
    b = bytes.fromhex(rec["wcs"])
    wcs = [(b[4*k], b[4*k+1], b[4*k+2], b[4*k+3]) for k in range(128)]
    rows, L, w_reset = program_rows22(wcs)
    fs = fs22(L)

    x, in_rate = read_wav_mono(args.infile)
    print(f"in : {args.infile}  ({in_rate} Hz, {len(x)/in_rate:.2f} s, peak {np.abs(x).max():.3f} FS)")
    fr = Fraction(int(round(fs)), in_rate).limit_denominator(20000)
    xr = resample_poly(x, fr.numerator, fr.denominator)
    pk = np.abs(xr).max()
    xi = np.round(xr * (args.drive / max(pk, 1e-12))).astype(np.int64)
    n = len(xi) + int(args.tail * fs)
    sig = np.zeros(n, dtype=np.int64)
    sig[:len(xi)] = xi
    print(f"    resampled -> {fs:.0f} Hz ({fr.numerator}/{fr.denominator}), "
          f"drive peak {args.drive:.0f} (-{20*np.log10(32768/args.drive):.1f} dBFS), "
          f"render {n} frames ({n/fs:.2f} s) x2 (wet + floor)")

    wet = RTL22().run_free(rows, list(sig), n)
    flo = RTL22().run_free(rows, [0] * n, n)
    outs = {}
    for c in "AC":
        outs[c] = np.asarray(wet[c], dtype=np.float64) - np.asarray(flo[c], dtype=np.float64)
    peak = max(np.abs(outs[c]).max() for c in "AC")
    gain = (0.708 * 32767.0) / max(peak, 1e-9)          # normalize to -3 dBFS
    Lch = np.clip(np.round(outs["A"] * gain), -32768, 32767)
    Rch = np.clip(np.round(outs["C"] * gain), -32768, 32767)

    out = args.outfile or os.path.splitext(args.infile)[0] + f"_concert_{args.image}.wav"
    write_wav_stereo(out, Lch, Rch, fs)
    print(f"out: {out}  (stereo A/C, {int(round(fs))} Hz, wet peak {peak:.0f} raw, "
          f"normalized x{gain:.1f} to -3 dBFS, floor-subtracted)")


if __name__ == "__main__":
    main()
