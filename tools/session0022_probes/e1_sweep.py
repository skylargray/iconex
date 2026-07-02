#!/usr/bin/env python3
"""E1 — reversed-window validity scan across all factory programs.

Keystone (pin-verified 2026-07-01): the WCS word address reaches the SRAMs through
complemented Multibus ADRn/ lines with NO compensation (tc_U42/U28 A-side), while the
run-mode PC drives true levels. So CPU word k = physical row 127-k, and the DSP executes
CPU words 127,126,... DESCENDING. A 100-step program = CPU words 127..28, reset at word 28.

This scan asks: under which (tcWR type value t, reset-bit polarity b, window model W)
does every factory program contain EXACTLY ONE reset microword, at the window edge?

  t in {0,1,2,3}: step is an IO-write (tcWR) iff (l2 & 3) == t
                  (t=1 = project's historical decode; t=2 = data-complement rotation)
  b in {1,0}:     reset asserted iff ((l0>>3)&1) == b   (b=1 = historical)
  W:  A  identity-100:  executed = words 0..99 ascending, reset must be {99}
      B  identity-var:  exists L in [88,112]: firing set within [0,L-1] == {L-1}
      C  reversed-var:  exists w*: firing set within [w*,127] == {w*}, L=128-w* in [88,112]

Boot: verified kosarev core, stub-ARU boot + PGM-2 bypass (byte-identical to the faithful
POST-passing boot for CONCERT, per session 0021). Program select: patch the power-up
selector LDA 0xB800 at 0x8160 -> MVI A,id ; NOP (session-0021 method).
"""
import sys, os, json

TOOLS = r"d:\OneDrive\Gray Instruments\iconex\tools"
sys.path.insert(0, TOOLS)
SCRATCH = os.path.dirname(os.path.abspath(__file__))
CACHE = os.path.join(SCRATCH, "wcs_cache.json")

import boot8080

ORIG_LOAD = boot8080.load_mem

def load_mem_patched(pid):
    mem = ORIG_LOAD()
    orig = bytes(mem[0x8160:0x8163])
    assert orig == b"\x3a\x00\xb8", f"selector bytes changed: {orig.hex()}"  # LDA 0xB800
    mem[0x8160:0x8163] = bytes([0x3E, pid & 0xFF, 0x00])                     # MVI A,id ; NOP
    return mem

def build_all(ids):
    """Boot each program id, cache the 0x4000..0x41FF WCS image (hex)."""
    cache = {}
    if os.path.exists(CACHE):
        cache = json.load(open(CACHE))
    for pid in ids:
        key = str(pid)
        if key in cache:
            continue
        boot8080.load_mem = (lambda p: (lambda: load_mem_patched(p)))(pid)
        try:
            m, ms = boot8080.boot(verbose=False)
            ok = "mainloop" in ms and "prog_load" in ms
            wcs = bytes(m.memory[0x4000:0x4200])
            nz = sum(1 for i in range(128) if wcs[4*i:4*i+4] != b"\x00\x00\x00\x00")
            cache[key] = {"ok": ok, "wcs": wcs.hex(), "nonzero_steps": nz,
                          "milestones": {k: int(v) for k, v in ms.items()}}
            print(f"id {pid:2d}: boot {'OK  ' if ok else 'FAIL'} nonzero steps={nz}")
        except Exception as e:
            cache[key] = {"ok": False, "error": repr(e)}
            print(f"id {pid:2d}: EXCEPTION {e!r}")
        finally:
            boot8080.load_mem = ORIG_LOAD
        json.dump(cache, open(CACHE, "w"))
    return cache

def words(wcs_hex):
    b = bytes.fromhex(wcs_hex)
    return [(b[4*k], b[4*k+1], b[4*k+2], b[4*k+3]) for k in range(128)]

def firing_set(ws, t, bpol):
    return sorted(k for k, (l0, l1, l2, l3) in enumerate(ws)
                  if (l2 & 3) == t and ((l0 >> 3) & 1) == bpol)

def score_A(F):                                   # identity-100
    inw = [k for k in F if k <= 99]
    return (inw == [99], 100 if inw == [99] else None)

def score_B(F):                                   # identity, variable end
    for L in range(88, 113):
        inw = [k for k in F if k < L]
        if inw == [L-1]:
            return (True, L)
    return (False, None)

def score_C(F):                                   # reversed, variable end
    for L in range(88, 113):
        w = 128 - L
        inw = [k for k in F if k >= w]
        if inw == [w]:
            return (True, L)
    return (False, None)

def main():
    ids = list(range(1, 22))
    cache = build_all(ids)
    built = {int(k): v for k, v in cache.items() if v.get("ok")}
    print(f"\nbuilt OK: {sorted(built)}  ({len(built)} programs)\n")

    scorers = {"A id-100": score_A, "B id-var": score_B, "C REV-var": score_C}
    print(f"{'t':>2} {'b':>2} | " + " | ".join(f"{n:>10}" for n in scorers))
    print("-" * 60)
    results = {}
    for t in range(4):
        for bpol in (1, 0):
            row = []
            per = {}
            for name, fn in scorers.items():
                nv, Ls = 0, []
                for pid, rec in built.items():
                    F = firing_set(words(rec["wcs"]), t, bpol)
                    okv, L = fn(F)
                    if okv:
                        nv += 1
                        Ls.append(L)
                    per.setdefault(name, {})[pid] = (okv, L, F)
                row.append(f"{nv:>3}/{len(built)}")
            results[(t, bpol)] = per
            print(f"{t:>2} {bpol:>2} | " + " | ".join(f"{c:>10}" for c in row))

    # detail for any (t,b,window) validating >= 15 programs
    print("\n=== detail on strong combos ===")
    for (t, bpol), per in results.items():
        for name, d in per.items():
            nv = sum(1 for ok, _, _ in d.values() if ok)
            if nv >= 10:
                Ls = sorted(L for ok, L, _ in d.values() if ok)
                fails = [pid for pid, (ok, _, _) in sorted(d.items()) if not ok]
                print(f"\n(t={t}, b={bpol}, {name}): {nv}/{len(built)} valid; L values={Ls}")
                for pid, (okv, L, F) in sorted(d.items()):
                    print(f"    id {pid:2d}: L={L}  reset word={128-L if L else None}  firing={F}")
                if fails:
                    print(f"  failing ids: {fails}")

    # CONCERT (id 1) firing sets for every combo, for eyeballing
    print("\n=== CONCERT (id 1) firing sets ===")
    if 1 in built:
        ws = words(built[1]["wcs"])
        for t in range(4):
            for bpol in (1, 0):
                print(f"  t={t} b={bpol}: {firing_set(ws, t, bpol)}")

if __name__ == "__main__":
    main()
