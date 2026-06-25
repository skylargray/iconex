#!/usr/bin/env python3
"""Capture the firmware-built Diagnostic Program 3 (ARU SIGNAT) WCS image.

Session 8/9: the diag-menu jump table at 0x0330 is indexed by program number;
index 8 -> 0x0EF4 (Max-Delay, Session-8 confirmed), index 7 -> 0x0EFD (Zero-Delay),
so program 3 (ARU SIGNAT) -> handler 0x0CF0.

The handler tail-calls a frame-sync wait at 0x0627 (spins until mem[0x3C14]==0x80,
set by an ISR that does not fire on a direct jump); we patch that wait to RET so the
WCS build proceeds, exactly as boot_xl patches the POST error handlers.

The handler only WRITES steps 96-127 of the WCS (the 30-step ARU signature program);
steps 0-95 retain whatever was loaded before. To isolate exactly the handler-written
bytes we run it twice -- prefilling the WCS with 0xFF and with 0x00 -- and take the
bytes both runs agree on (deterministic = handler-written); the rest are NOP (0xFF).

Result (verified): 30 active steps, all in 98..127; START=STOP=RESET/ feedback window
spans the 30 steps * 3 ARUCK = 90 ARUCK (matches the signature calibration N_fb=90).
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import boot_xl as B

DIAG3_HANDLER = 0x0CF0
SYNC_WAIT = 0x0627          # spins on mem[0x3C14]==0x80; patch to RET (0xC9)
BUILD_DONE = 0x0D10         # handler reaches its signature-pulse loop here


def _run(prefill):
    cpu, mem, larc, aru, *_ = B.boot(verbose=False)
    mem[SYNC_WAIT] = 0xC9                       # frame-sync wait -> RET
    for a in range(0x4000, 0x4200):
        mem[a] = prefill                        # blank the WCS
    def outh(p, v):
        if p in (0xEE, 0xEF):
            larc.out(cpu, p, v); return
        aru.out(p, v)
    cpu.out_hook = outh
    cpu.push(0xFFFF); cpu.PC = DIAG3_HANDLER
    for _ in range(2_000_000):
        if cpu.PC in (BUILD_DONE, 0xFFFF):
            break
        cpu.step()
    return bytes(mem[0x4000:0x4200])


def capture_wcs():
    """Return the 512-byte true Diag-3 WCS image (handler-written bytes; the rest
    forced to 0xFF = NOP). Deterministic across WCS prefill."""
    wff = _run(0xFF)
    w00 = _run(0x00)
    true = bytearray([0xFF] * 0x200)
    for a in range(0x200):
        if wff[a] == w00[a]:                    # written by handler (prefill-independent)
            true[a] = wff[a]
    return bytes(true)


_CACHE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "_diag3_wcs.bin")


def load_wcs(rebuild=False):
    """Cached accessor for the Diag-3 WCS (avoids re-booting the emulator)."""
    if not rebuild and os.path.exists(_CACHE):
        with open(_CACHE, "rb") as f:
            return f.read()
    wcs = capture_wcs()
    with open(_CACHE, "wb") as f:
        f.write(wcs)
    return wcs


if __name__ == "__main__":
    import aru_datapath as A
    wcs = load_wcs(rebuild=True)
    prog = A.decode_image(wcs)
    print(f"Diag-3 ARU SIGNAT: {len(prog)} active steps (cached to {_CACHE})")
    nx = sum(s['XFER'] for s in prog); nz = sum(s['ZERO'] for s in prog)
    nd = sum(1 for s in prog if s['MI17'])
    print(f"  XFER={nx} ZERO={nz} MI17(DMEM)={nd}; step range "
          f"{prog[0]['s']}..{prog[-1]['s']}")
