#!/usr/bin/env python3
"""D1a (plan 022) — capture the firmware-built diagnostic WCS images on the VERIFIED core.

Route (plan 022 §3 D1a, preference 1 = direct-call patch): boot8080 (kosarev I8080Machine,
exerciser-verified) to the mainloop exactly as e1_sweep, then drive PC straight at the
diag-menu handler and let the ROM builder write 0x4000-0x41FF.

Handlers (SBC1 disassembly, re-read this session):
  0x0EF4  item 8 MAX (.5 s) DELAY : CALL 0x03D5 ; CALL 0x0F2C(builder) ; JP 0x0F17
  0x0EFD  item 7 ZERO DELAY      : same + patches 0x41F8<-01 0x41F9<-00 (word 126 ofst=0x0001)
                                          and 0x4130<-01 0x4131<-40 (word  76 ofst=0x4001)
          then falls into 0x0F17.
  0x0F17  = the post-build display loop (never returns) -> FIRST ARRIVAL = all WCS writes done.
  0x0CF0  item 3 ARU SIGNAT (session 9): stops at its signature-pulse loop 0x0D10; re-captured
          here on the verified core for D3c provenance (diag3.py used the retired z80emu core).

The frame-sync wait 0x0627 (spins on mem[0x3C14]==0x80, an ISR flag that never fires under a
direct jump) is patched to RET — the same patch diag3.py proved out.

Provenance discipline (diag3 recipe): each image is captured twice with the WCS prefilled
0xFF and 0x00; only bytes both runs agree on are kept (prefill-independent = handler-written;
disagreeing bytes forced to 0xFF NOP and counted). For items 7/8 the builder's own 512-byte
0xFF fill makes the agreement total — recorded, not assumed.

Built-in route checksum (plan 022 §8): the ZERO and MAX images must differ in EXACTLY the four
patched offset low bytes 0x4130/0x4131 and 0x41F8/0x41F9.

Cache: wcs_diag.json  {"zero"|"max"|"sig3": {"wcs": hex, ...}, "meta": ...}
"""
import sys, os, json

TOOLS = r"d:\OneDrive\Gray Instruments\iconex\tools"
sys.path.insert(0, TOOLS)
HERE = os.path.dirname(os.path.abspath(__file__))
CACHE = os.path.join(HERE, "wcs_diag.json")

import boot8080
from aru_freerun22_rtl import program_rows22, fs22

SYNC_WAIT = 0x0627
NOP4 = (0xFF, 0xFF, 0xFF, 0xFF)

# name -> (handler entry, stop PC = first arrival means the WCS is complete)
DIAGS = {
    "max":  (0x0EF4, 0x0F17),   # item 8: .5 s delay line through DMEM
    "zero": (0x0EFD, 0x0F17),   # item 7: zero delay (post-build 4-byte offset patch)
    "sig3": (0x0CF0, 0x0D10),   # item 3: ARU SIGNAT stimulus (D3c re-capture, verified core)
}


def _run_handler(handler, stop_pc, prefill, budget=60_000_000):
    """Boot to mainloop, prefill the WCS, direct-call the handler, run to stop_pc."""
    m, ms = boot8080.boot(verbose=False)
    assert "mainloop" in ms and "prog_load" in ms, f"boot did not reach mainloop: {ms}"
    m.memory[SYNC_WAIT] = 0xC9                       # frame-sync wait -> RET
    for a in range(0x4000, 0x4200):
        m.memory[a] = prefill
    sp = (m.sp - 2) & 0xFFFF                         # sentinel return (handlers never RET)
    m.memory[sp] = 0xFF
    m.memory[(sp + 1) & 0xFFFF] = 0xFF
    m.sp = sp
    m.pc = handler
    m.set_breakpoint(stop_pc)
    ticks = 0
    while ticks < budget:
        m.ticks_to_stop = 200_000
        ev = m.run()
        ticks += 200_000 - m.ticks_to_stop
        if ev & m._BREAKPOINT_HIT:
            if m.pc == stop_pc:
                break
            m.clear_breakpoint(m.pc)                 # stale boot milestone breakpoint
            m.ticks_to_stop = 1
            m.run()
    else:
        raise RuntimeError(f"handler 0x{handler:04X} never reached 0x{stop_pc:04X} "
                           f"(PC=0x{m.pc:04X} after {ticks} ticks)")
    return bytes(m.memory[0x4000:0x4200])


def capture(name):
    handler, stop_pc = DIAGS[name]
    wff = _run_handler(handler, stop_pc, 0xFF)
    w00 = _run_handler(handler, stop_pc, 0x00)
    img = bytearray([0xFF] * 0x200)
    agree = 0
    for a in range(0x200):
        if wff[a] == w00[a]:
            img[a] = wff[a]
            agree += 1
    return bytes(img), agree


def words_of(img):
    return [(img[4 * k], img[4 * k + 1], img[4 * k + 2], img[4 * k + 3]) for k in range(128)]


def main(recapture=False):
    cache = json.load(open(CACHE)) if (os.path.exists(CACHE) and not recapture) else {}
    for name in DIAGS:
        if name in cache:
            print(f"[{name}] cached")
            continue
        print(f"[{name}] booting verified core + direct-calling 0x{DIAGS[name][0]:04X} "
              f"(2 prefills) ...")
        img, agree = capture(name)
        active = [k for k, w in enumerate(words_of(img)) if w != NOP4]
        cache[name] = {"wcs": img.hex(), "agree_bytes": agree,
                       "handler": DIAGS[name][0], "stop_pc": DIAGS[name][1],
                       "active_words": active}
        print(f"  agreement {agree}/512 bytes; active CPU words: {active}")
        json.dump(cache, open(CACHE, "w"), indent=1)

    zero = bytes.fromhex(cache["zero"]["wcs"])
    mx = bytes.fromhex(cache["max"]["wcs"])

    # --- built-in route checksum: exactly the 4 patched offset low bytes differ ---
    diffs = [a for a in range(0x200) if zero[a] != mx[a]]
    exp = [0x130, 0x131, 0x1F8, 0x1F9]
    print(f"\nzero-vs-max byte diffs (rel 0x4000): {[hex(a) for a in diffs]}")
    assert diffs == exp, f"route checksum FAILED: expected {[hex(a) for a in exp]}"
    print("  == the four ZERO-patch bytes exactly -> route checksum PASS")
    print(f"  word  76 ofst: max=0x{mx[0x131]<<8 | mx[0x130]:04X}  zero=0x{zero[0x131]<<8 | zero[0x130]:04X}")
    print(f"  word 126 ofst: max=0x{mx[0x1F9]<<8 | mx[0x1F8]:04X}  zero=0x{zero[0x1F9]<<8 | zero[0x1F8]:04X}")

    # --- both images must extract as L=99 / 100-step frames (plan 022 §8) ---
    for name in ("zero", "max"):
        img = bytes.fromhex(cache[name]["wcs"])
        rows, L, w_reset = program_rows22(words_of(img))
        assert (L, w_reset) == (99, 29), (name, L, w_reset)
        assert len(rows) == 100
        assert rows[99]["typ"] == 3 and rows[99]["cmag"] == 0        # row-L idle (NOP)
        print(f"  [{name}] extraction OK: reset word 29, L=99, 100-step frame, "
              f"fs={fs22(L):.1f} Hz")

    # --- D3c provenance: verified-core sig3 vs the cached z80emu-era capture ---
    old = os.path.join(TOOLS, "_diag3_wcs.bin")
    if os.path.exists(old) and "sig3" in cache:
        ob = open(old, "rb").read()
        same = ob == bytes.fromhex(cache["sig3"]["wcs"])
        print(f"\nsig3 (verified core) vs tools/_diag3_wcs.bin: "
              f"{'BYTE-IDENTICAL' if same else 'DIFFER'}")
        if not same:
            d = [a for a in range(0x200) if ob[a] != bytes.fromhex(cache['sig3']['wcs'])[a]]
            print(f"  differing bytes: {[hex(a) for a in d][:16]}{'...' if len(d) > 16 else ''}")
    print("\nD1a capture complete ->", CACHE)


if __name__ == "__main__":
    main(recapture="--recapture" in sys.argv)
