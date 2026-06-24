#!/usr/bin/env python3
"""3.1 Route A, step 1: capture the LIVE modulated WCS frame stream from the booted
v8.2.1 firmware (CONCERT). The SBC modulation engine (0xAD5C) rewrites selected WCS
taps every control tick; we boot to the main loop, keep stepping the foreground, and
snapshot the ARU image (0x4000:0x4200) to record exactly which steps change, their
trajectory (settling de-zipper vs oscillating chorus), the cadence in SBC instructions,
and a distinct-frame timeline for the faithful live-modulation harness (exp_live.py).

Rather than re-deriving the engine math (Route B), we let the real firmware tell us the
frames. The modulated steps carry BOTH a swept integer offset (lane0/1) and a swept
coefficient (lane3) -- the firmware microcode itself realizes the all-pass fractional
delay, so replaying these frames is faithful by construction.

Usage: python exp_modcap.py [extra_instructions] [snap_every]
Saves: tools/_modframes.npz  (icounts[K], frames[K,512], boot_image[512])
"""
import os, sys, time
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np
import boot_xl as B

RGN_LO, RGN_HI = 0x4000, 0x4200          # WCS image (128 steps x 4 bytes)
MOD_STEPS = (56, 57, 107, 108)           # CONCERT chorus taps (doc)
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "_modframes.npz")


def decode_off(l0, l1):
    return (~(l0 | (l1 << 8))) & 0xFFFF


def main():
    extra = int(sys.argv[1]) if len(sys.argv) > 1 else 6_000_000
    snap_every = int(sys.argv[2]) if len(sys.argv) > 2 else 2_000

    t0 = time.time()
    cpu, mem, larc, aru, ms, cap, snap = B.boot(
        power_up_id=0x01, stop_pc=0x8169, stop_hits=1, suppress_post=True, verbose=False)
    print(f"booted to main loop in {time.time()-t0:.1f}s  icount={cpu.icount}")
    rate, depth = mem[0x3cd3], mem[0x3cd4]
    print(f"modulation enable 0x3ccd=0x{mem[0x3ccd]:02X} (bit6={'ON' if mem[0x3ccd]&0x40 else 'off'})  "
          f"rate=0x{rate:02X}({rate})  depth={depth}  LFO step=every {8*rate} foreground passes")

    boot_image = bytes(mem[RGN_LO:RGN_HI])
    start_ic = cpu.icount

    # distinct-frame timeline + per-step trajectories
    icounts = [start_ic]
    frames = [bytearray(boot_image)]
    last_frame = bytearray(boot_image)
    traj = {s: [] for s in range(128)}    # s -> list of (dic, off, l2, l3)
    def log_step(s, dic, fr):
        a = (s * 4)
        traj[s].append((dic, decode_off(fr[a], fr[a+1]), fr[a+2], fr[a+3]))

    # seed trajectory at t=0 for all steps that ever change
    # snap_every<=0 -> event-driven per-pass capture: snapshot at the modulation engine
    # entry (0xAD5C), a consistent point reflecting the previous pass's completed writes
    # (avoids catching a frame mid-update). Otherwise snapshot every snap_every instructions.
    per_pass = snap_every <= 0
    fg_passes = 0
    last_irq = cpu.icount
    next_snap = cpu.icount + (snap_every if not per_pass else 1 << 62)
    t0 = time.time()
    for _ in range(extra):
        pc = cpu.PC
        if pc == 0xAD5C:
            fg_passes += 1
        take = (pc == 0xAD5C) if per_pass else (cpu.icount >= next_snap)
        if take:
            cur = mem[RGN_LO:RGN_HI]
            if cur != last_frame:
                dic = cpu.icount - start_ic
                # record changed steps into trajectories
                for i in range(0, RGN_HI - RGN_LO):
                    if cur[i] != last_frame[i]:
                        s = i // 4
                        # log this step once per frame change
                # log every step that differs (dedup by step)
                changed_steps = set((i // 4) for i in range(RGN_HI - RGN_LO) if cur[i] != last_frame[i])
                for s in changed_steps:
                    log_step(s, dic, cur)
                icounts.append(cpu.icount)
                frames.append(bytearray(cur))
                last_frame = bytearray(cur)
            if not per_pass:
                next_snap = cpu.icount + snap_every
        if cpu.IFF1 and (cpu.icount - last_irq) >= 64 and (larc.tx_en or larc.rx_ready(cpu)):
            if cpu.interrupt():
                last_irq = cpu.icount
        try:
            cpu.step()
        except Exception as e:
            print(f"  ABORT @0x{cpu.PC:04X}: {e}")
            break

    dt = time.time() - t0
    ran = cpu.icount - start_ic
    print(f"ran {ran} ins in {dt:.1f}s ({ran/dt/1e6:.2f} M ins/s)  "
          f"foreground passes(0xAD5C)={fg_passes}  ~{ran//max(fg_passes,1)} ins/pass")
    print(f"distinct frames captured: {len(frames)}")

    # classify changed steps: oscillating (chorus) vs settling (de-zipper)
    changed = {s: t for s, t in traj.items() if t}
    print(f"\nsteps that changed ({len(changed)}): {sorted(changed)}")
    print("  step | field | first -> last | min..max | n | verdict")
    for s in sorted(changed):
        t = changed[s]
        offs = [o for _, o, _, _ in t]
        l3s = [l3 for _, _, _, l3 in t]
        off_swing = max(offs) - min(offs)
        l3_swing = max(l3s) - min(l3s)
        # does it reverse direction (oscillate) or monotone-settle?
        field = "off" if off_swing >= l3_swing else "l3"
        seq = offs if field == "off" else l3s
        # count direction reversals
        dirs = [1 if seq[i] > seq[i-1] else (-1 if seq[i] < seq[i-1] else 0) for i in range(1, len(seq))]
        nz = [d for d in dirs if d]
        rev = sum(1 for i in range(1, len(nz)) if nz[i] != nz[i-1])
        verdict = "OSC(chorus)" if rev >= 2 else "settle(dezip)"
        print(f"  {s:4d} | {field:3} | {seq[0]:5d} -> {seq[-1]:5d} | {min(seq):5d}..{max(seq):5d} "
              f"| {len(t):3d} | rev={rev} {verdict}")

    np.savez_compressed(OUT,
                        icounts=np.array(icounts, dtype=np.int64),
                        frames=np.array([bytes(f) for f in frames], dtype=np.uint8).reshape(len(frames), -1)
                                if False else np.frombuffer(b"".join(bytes(f) for f in frames), dtype=np.uint8).reshape(len(frames), RGN_HI-RGN_LO),
                        boot_image=np.frombuffer(boot_image, dtype=np.uint8),
                        start_ic=np.int64(start_ic), rate=np.int64(rate), depth=np.int64(depth),
                        ins_per_pass=np.float64(ran/max(fg_passes,1)))
    print(f"\nsaved frame timeline -> {OUT}  ({len(frames)} frames)")


if __name__ == '__main__':
    main()
