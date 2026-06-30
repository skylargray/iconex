#!/usr/bin/env python3
"""Render the 224XL free-run DSP to a listenable WAV (impulse response or arbitrary input).

Drives tools/aru_freerun.FreeRunARU over a WCS image (cached JSON or a fresh boot) and captures the
WR DA/ output, writing a 16-bit PCM WAV at the native 34.13 kHz. Lets us actually HEAR the current
state of a program's reverb.

Usage:
  python tools/render_wav.py [out.wav] [seconds] [--wcs path.json | --boot] [--amp N] [--noise SEC]
Defaults: renders/CONCERT_impulse_5s.wav, 5.0 s, cached WCS, impulse amp=30000.
"""
import os
import sys
import json
import wave
import struct

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import aru_freerun as FR

FS = 34130   # 224XL audio sample rate (100 microinstructions x 292.97 ns)
CACHED_WCS = (r"C:/Users/Skylar/AppData/Local/Temp/claude/d--OneDrive-Gray-Instruments-iconex/"
              r"f950f5a4-d96d-4fdd-899a-08b03ca853c7/scratchpad/concert_wcs.json")


def load_wcs(path=None, boot=False):
    if boot:
        import boot8080 as B
        m, ms = B.boot(verbose=False)
        return FR.wcs_from_mem(m.memory)
    with open(path or CACHED_WCS) as f:
        return [tuple(s) for s in json.load(f)]


def render(wcs, n_samples, amp=30000, noise_sec=0.0, capture="monosum"):
    """Returns a list of per-sample output values.
    capture: 'monosum' = sum of all WR DA writes/sample; 'chA'..'chD' = last write to that channel."""
    aru = FR.FreeRunARU()
    noise_n = int(noise_sec * FS)
    seed = [0x1234]
    out = []
    ch_idx = {"chA": 0, "chB": 1, "chC": 2, "chD": 3}.get(capture)
    for s in range(n_samples):
        if noise_n and s < noise_n:
            seed[0] = (seed[0] * 1103515245 + 12345) & 0x7FFFFFFF
            ai = (seed[0] >> 8) % (2 * amp) - amp
        else:
            ai = amp if s == 0 else 0
        o = aru.run_sample(wcs, ai & 0xFFFF)
        if capture == "monosum":
            out.append(sum(v for _, v in o))
        else:
            last = 0
            for chan, val in o:
                if (chan & 3) == ch_idx:
                    last = val
            out.append(last)
    return out


def write_wav(path, samples, fs=FS, gain=1.0, nchannels=1):
    """Write 16-bit PCM WITHOUT normalization — absolute sample values (only an OPTIONAL explicit `gain`,
    default 1.0, and a 16-bit clamp). Normalization was REMOVED (owner directive 2026-06-29): it muddied
    absolute-gain analysis. `samples` = a flat list (mono) or a list of per-frame (L,R,...) tuples
    (multichannel). Returns (raw_peak, clip_count) so any clipping (e.g. the over-unity loop hitting the
    rail) is VISIBLE rather than hidden by auto-gain."""
    os.makedirs(os.path.dirname(path), exist_ok=True)
    clip = [0]

    def conv(v):
        iv = int(round(v * gain))
        if iv > 32767:
            clip[0] += 1; return 32767
        if iv < -32768:
            clip[0] += 1; return -32768
        return iv

    with wave.open(path, "w") as w:
        w.setnchannels(nchannels)
        w.setsampwidth(2)
        w.setframerate(fs)
        buf = bytearray()
        if nchannels == 1:
            for v in samples:
                buf += struct.pack("<h", conv(v))
        else:
            for fr in samples:
                for c in range(nchannels):
                    buf += struct.pack("<h", conv(fr[c]))
        w.writeframes(bytes(buf))
    flat = samples if nchannels == 1 else [x for fr in samples for x in fr]
    peak = max((abs(v) for v in flat), default=0)
    return peak, clip[0]


def read_wav_mono16(path):
    """Read a WAV (16/24/8-bit, any channel count) → (mono int16-scale sample list, framerate).
    24-bit is scaled to 16-bit (>>8); stereo+ is averaged to mono (the engine has one A/D feed)."""
    import numpy as np
    with wave.open(path) as w:
        nch, sw, fs, n = w.getnchannels(), w.getsampwidth(), w.getframerate(), w.getnframes()
        raw = w.readframes(n)
    a = np.frombuffer(raw, dtype=np.uint8)
    if sw == 3:                                        # 24-bit packed little-endian
        a = a.reshape(-1, 3).astype(np.int32)
        v = a[:, 0] | (a[:, 1] << 8) | (a[:, 2] << 16)
        v16 = np.where(v & 0x800000, v - 0x1000000, v) >> 8
    elif sw == 2:
        v16 = np.frombuffer(raw, dtype="<i2").astype(np.int32)
    elif sw == 1:
        v16 = (a.astype(np.int32) - 128) << 8
    else:
        raise ValueError(f"unsupported sampwidth {sw}")
    v16 = v16.reshape(-1, nch)
    mono = (v16.sum(axis=1) // nch).astype(np.int32)
    return mono.tolist(), fs


def process_file(in_path, out_path, wcs, offsets, tail_sec=3.0, in_gain=1.0, fs=FS):
    """Feed an input WAV through the reverb and write a STEREO output WAV (A=left, C=right), NO
    normalization. Captures the WR DA/ output per channel (sample-and-hold, like the FPC double-buffer).
    Returns (input_framerate, n_samples, out_peak, clip_count)."""
    insig, insr = read_wav_mono16(in_path)
    aru = FR.FreeRunARU(fpc_enabled=True)   # audio render → apply the FPC float↔fixed codec (12-bit A/D+D/A grain)
    n = len(insig) + int(tail_sec * fs)
    hold = {0: 0, 2: 0}            # A=channel0=left, C=channel2=right
    frames = []
    for s in range(n):
        ai = int(insig[s] * in_gain) if s < len(insig) else 0
        outs = aru.run_sample(wcs, ai & 0xFFFF, offsets=offsets)
        for chan, val in outs:
            if (chan & 3) in hold:
                hold[chan & 3] = val
        frames.append((hold[0], hold[2]))
    peak, clip = write_wav(out_path, frames, fs=fs, nchannels=2)
    return insr, n, peak, clip


def main():
    args = [a for a in sys.argv[1:]]
    out = next((a for a in args if a.endswith(".wav")), None) or os.path.join(
        os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "renders", "CONCERT_impulse_5s.wav")
    secs = next((float(a) for a in args if a.replace(".", "").isdigit()), 5.0)
    amp = int(args[args.index("--amp") + 1]) if "--amp" in args else 30000
    noise = float(args[args.index("--noise") + 1]) if "--noise" in args else 0.0
    wcs_path = args[args.index("--wcs") + 1] if "--wcs" in args else None
    boot = "--boot" in args
    cap = args[args.index("--cap") + 1] if "--cap" in args else "monosum"

    print(f"loading WCS ({'boot' if boot else (wcs_path or 'cached')}) ...")
    wcs = load_wcs(wcs_path, boot)
    n = int(secs * FS)
    print(f"rendering {secs}s = {n} samples x100 steps (impulse amp={amp}, noise={noise}s, cap={cap}) ...")
    sig = render(wcs, n, amp=amp, noise_sec=noise, capture=cap)
    peak, scale = write_wav(out, sig)
    nz = sum(1 for v in sig if abs(v) > peak * 0.001)
    print(f"  raw peak={peak}, applied gain x{scale:.2f}; nonzero(>-60dB) samples = {nz}/{n}")
    print(f"  wrote {os.path.abspath(out)}  ({secs}s, {FS} Hz, 16-bit mono)")


if __name__ == "__main__":
    main()
