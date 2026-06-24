#!/usr/bin/env python3
"""Boot every program ONCE, cache decoded microcode + clean-boot status to a pickle.
All later losslessness sweeps load the cache (no re-boot per experiment).

clean = boot reached the firmware main loop (0x8169) AND ran a program load (0x13B6).
Programs that only "ran full 20M ins" without reaching mainloop are load-unreliable;
their decoded WCS may be garbage, so their lambda must be discounted.
"""
import sys, os, pickle
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import boot_xl as B

CACHE = os.path.join(os.path.dirname(os.path.abspath(__file__)), '_progcache.pkl')


def decode_img(img):
    prog = []
    for s in range(128):
        l0, l1, l2, l3 = img[s*4], img[s*4+1], img[s*4+2], img[s*4+3]
        if l2 == 0xFF and l3 == 0xFF:
            continue
        ctl = (~l2) & 0xFF
        offset = (~(l0 | (l1 << 8))) & 0xFFFF
        coeff = (-(l3 & 0x7F) if l3 & 0x80 else (l3 & 0x7F))
        prog.append(dict(s=s, offset=offset, coeff=coeff,
                         ZERO=(ctl >> 7) & 1, b3=(ctl >> 3) & 1, XFER=(ctl >> 2) & 1,
                         WA=ctl & 3, b5=(ctl >> 5) & 1, b4=(ctl >> 4) & 1))
    return prog


def build(pids=range(1, 0x17)):
    cache = {}
    for pid in pids:
        cpu, mem, larc, aru, ms, cap, snap = B.boot(power_up_id=pid, verbose=False)
        img = bytes(mem[0x4000:0x4200])
        prog = decode_img(img)
        clean = (ms.get('mainloop') is not None) and (ms.get('prog_load') is not None)
        cache[pid] = dict(prog=prog, clean=clean,
                          mainloop=ms.get('mainloop'), prog_load=ms.get('prog_load'),
                          nsteps=len(prog))
        print(f"  pid={pid:#04x} steps={len(prog):3d} clean={clean} "
              f"mainloop={ms.get('mainloop')} prog_load={ms.get('prog_load')}")
    with open(CACHE, 'wb') as f:
        pickle.dump(cache, f)
    print(f"\nwrote {CACHE} ({len(cache)} programs, "
          f"{sum(1 for v in cache.values() if v['clean'])} clean)")
    return cache


def load():
    with open(CACHE, 'rb') as f:
        return pickle.load(f)


if __name__ == '__main__':
    build()
