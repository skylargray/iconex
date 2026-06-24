#!/usr/bin/env python3
"""Cache the RAW microword bytes (l0,l1,l2,l3) per active step for every program, so the
corrected decode (from the owner's schematic trace) can be applied without re-booting.
Active step = NOT (l2==0xFF and l3==0xFF)."""
import sys, os, pickle
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import boot_xl as B

CACHE = os.path.join(os.path.dirname(os.path.abspath(__file__)), '_rawcache.pkl')


def build(pids=range(1, 0x17)):
    cache = {}
    for pid in pids:
        cpu, mem, larc, aru, ms, cap, snap = B.boot(power_up_id=pid, verbose=False)
        img = bytes(mem[0x4000:0x4200])
        steps = []
        for s in range(128):
            l0, l1, l2, l3 = img[s*4], img[s*4+1], img[s*4+2], img[s*4+3]
            if l2 == 0xFF and l3 == 0xFF:
                continue
            steps.append((s, l0, l1, l2, l3))
        clean = (ms.get('mainloop') is not None) and (ms.get('prog_load') is not None)
        cache[pid] = dict(clean=clean, steps=steps)
        print(f"  pid={pid:#04x} steps={len(steps):3d} clean={clean}")
    with open(CACHE, 'wb') as f:
        pickle.dump(cache, f)
    print(f"wrote {CACHE} ({sum(1 for v in cache.values() if v['clean'])} clean)")
    return cache


def load():
    with open(CACHE, 'rb') as f:
        return pickle.load(f)


if __name__ == '__main__':
    build()
