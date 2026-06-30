#!/usr/bin/env python3
"""Phase 1.3 — STUB-VARIATION TEST (closes G1 of plan 019).

The decisive experiment: re-boot v8.2.1 to CONCERT several times, each with a DIFFERENT stub value
returned for every NON-serial input port (the ARU latch 0x06/0x07 and any other hardware port the
firmware reads, e.g. 0x02). Read m.memory[0x4000:0x4200] each time and diff.

  • byte-identical across all stub values  -> G1 CLOSED: the WCS build provably does not use those
    ports; the stubs cannot have corrupted the microwords, and the cmag=0 / PROT=1 block at steps
    5-22 is a REAL firmware output, not a stubbing artifact.
  • differs                                -> the build IS hardware-dependent: report which port/value
    it needs (obtain the real value from the faithful ARU model in Phase 3).

This is a real experiment, not a code-read (plan 019 ground rule). It also cross-checks the fresh
boot against the cached verified_wcs_0x4000.json from the prior session (default-stub baseline).

Run:  python tools/verify_build_hwindep.py
"""
import os
import sys
import json

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
sys.stdout.reconfigure(encoding="utf-8")
import boot8080 as B

SCR = (r"C:/Users/Skylar/AppData/Local/Temp/claude/"
       r"d--OneDrive-Gray-Instruments-iconex/ae30a9a1-b02b-4706-a6d3-7d89d4cefad3/scratchpad")
os.makedirs(SCR, exist_ok=True)
OLD_CACHE = (r"C:/Users/Skylar/AppData/Local/Temp/claude/"
             r"d--OneDrive-Gray-Instruments-iconex/f950f5a4-d96d-4fdd-899a-08b03ca853c7/"
             r"scratchpad/verified_wcs_0x4000.json")

STUBS = [0x00, 0xFF, 0x55, 0xAA]


def boot_wcs(hw_stub):
    """Boot to CONCERT with the given non-serial-port stub; return (wcs_bytes, milestones)."""
    m, ms = B.boot(verbose=False, hw_stub=hw_stub)
    ok = "mainloop" in ms and "prog_load" in ms
    if not ok:
        raise RuntimeError(f"hw_stub=0x{hw_stub:02X}: boot did not reach mainloop/prog_load: {ms}")
    wcs = bytes(m.memory[0x4000:0x4200])
    return wcs, ms


def main():
    print("### Phase 1.3 STUB-VARIATION TEST (G1) — booting CONCERT under varied hardware stubs ###")
    print(f"stub values: {[hex(s) for s in STUBS]}  (each ~1-2 min)\n")
    results = {}
    for s in STUBS:
        print(f"  booting hw_stub=0x{s:02X} ...", flush=True)
        wcs, ms = boot_wcs(s)
        results[s] = wcs
        print(f"    -> reached mainloop@{ms.get('mainloop')} prog_load@{ms.get('prog_load')} "
              f"| 0x4000[:8]={wcs[:8].hex()} | sha-ish={sum(wcs)&0xFFFFFFFF:08X}", flush=True)

    # --- diff every variation against the first ---
    base_s = STUBS[0]
    base = results[base_s]
    print(f"\nDIFF (reference = hw_stub=0x{base_s:02X}):")
    all_identical = True
    for s in STUBS[1:]:
        w = results[s]
        diffs = [(i, base[i], w[i]) for i in range(len(base)) if base[i] != w[i]]
        if diffs:
            all_identical = False
            print(f"  hw_stub=0x{s:02X}: {len(diffs)} byte diffs! first 12: "
                  + ", ".join(f"@0x{0x4000+i:04X} {a:02X}->{b:02X}" for i, a, b in diffs[:12]))
        else:
            print(f"  hw_stub=0x{s:02X}: IDENTICAL (0/512 bytes differ)")

    # --- cross-check fresh boot vs cached prior-session baseline (default stub) ---
    cache_note = ""
    if os.path.exists(OLD_CACHE):
        cached = bytes(json.load(open(OLD_CACHE)))
        # The cached image came from the DEFAULT stub (0xFF on 0x06/07, 0x00 else). Compare to a
        # fresh default boot for a true apples-to-apples fresh-vs-cached check.
        print("\n  cross-check: booting hw_stub=None (default) vs cached verified_wcs_0x4000.json ...", flush=True)
        fresh_default, _ = boot_wcs(None)
        cdiffs = [i for i in range(min(len(cached), len(fresh_default))) if cached[i] != fresh_default[i]]
        if not cdiffs and len(cached) == len(fresh_default):
            cache_note = "fresh default boot == cached prior-session WCS (byte-identical)"
        else:
            cache_note = (f"fresh default boot differs from cached at {len(cdiffs)} bytes "
                          f"(first: {[hex(0x4000+i) for i in cdiffs[:8]]}) — investigate")
        print("    " + cache_note)
        results["default"] = fresh_default

    # --- lane-3 focus (every 4k+3 byte — the reverb-critical coeff lane) ---
    print("\nlane-3 (4k+3 bytes) invariance across stubs:")
    l3_ok = True
    for s in STUBS[1:]:
        l3b = [i for i in range(3, 512, 4) if base[i] != results[s][i]]
        if l3b:
            l3_ok = False
            print(f"  hw_stub=0x{s:02X}: lane-3 differs at steps {[ (i-3)//4 for i in l3b][:16]}")
        else:
            print(f"  hw_stub=0x{s:02X}: lane-3 identical")

    verdict = "G1 CLOSED — build is hardware-independent" if all_identical else \
              "G1 OPEN — build depends on a hardware port (see diffs)"
    print("\n" + "=" * 70)
    print(f"VERDICT: {verdict}")
    print(f"  AC1 (0x4000 byte-invariant under hardware-stub variation): {'PASS' if all_identical else 'FAIL'}")
    print("=" * 70)

    out = {
        "stubs": [hex(s) for s in STUBS],
        "all_identical": all_identical,
        "lane3_invariant": l3_ok,
        "cache_crosscheck": cache_note,
        "wcs_hex": {("0x%02X" % s if isinstance(s, int) else s): results[s].hex() for s in results},
        "verdict": verdict,
    }
    with open(os.path.join(SCR, "phase1_stubvar.json"), "w") as f:
        json.dump(out, f, indent=1)
    print(f"\nwrote {SCR}/phase1_stubvar.json")
    return all_identical


if __name__ == "__main__":
    ok = main()
    sys.exit(0 if ok else 1)
