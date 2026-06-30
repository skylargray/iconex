#!/usr/bin/env python3
"""Phase 2c — cross-validate the CONCERT WCS (esp. lane 3) on TWO independent 8080 cores. Closes G3.

Boots the SAME firmware to CONCERT independently on:
  • the exerciser-verified kosarev z80.I8080Machine   (tools/boot8080)
  • the clean-room, spec-validated ref core           (tools/boot8080_ref + tools/i8080_ref)
then diffs m.memory[0x4000:0x4200]. The reverb-critical bytes are lane 3 (every 4k+3 byte → cmag /
XFER / ZERO). Per plan 019:
  • byte-identical (esp. lane 3) -> G3 CLOSED: lane 3 cross-validated on two independent correct cores.
  • differ -> dump the offending step + the instructions that produced it for adjudication vs the spec.

The ref core was certified independently of kosarev by the exhaustive spec-formula ALU oracle in
tools/i8080_ref_validate.py (parity included) + a full-opcode differential cross-check, so agreement
here is genuine independent confirmation, not a tautology.

Run:  python tools/verify_lane3_crosscore.py
"""
import os
import sys
import json

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
sys.stdout.reconfigure(encoding="utf-8")
import boot8080 as B
import boot8080_ref as BR

SCR = (r"C:/Users/Skylar/AppData/Local/Temp/claude/"
       r"d--OneDrive-Gray-Instruments-iconex/ae30a9a1-b02b-4706-a6d3-7d89d4cefad3/scratchpad")
os.makedirs(SCR, exist_ok=True)


def decode_lane3(l3):
    inv3 = (~l3) & 0xFF
    return dict(XFER=inv3 & 1, ZERO=(inv3 >> 1) & 1, cmag=(inv3 >> 2) & 0x3F)


def main():
    print("### Phase 2c — lane-3 cross-validation on two independent 8080 cores (G3) ###\n")

    print("[1/2] booting kosarev (verified core) to CONCERT ...")
    mk, msk = B.boot(verbose=False)
    assert "mainloop" in msk and "prog_load" in msk, f"kosarev boot failed: {msk}"
    kwcs = bytes(mk.memory[0x4000:0x4200])
    print(f"      kosarev reached mainloop; 0x4000[:8]={kwcs[:8].hex()}")

    print("[2/2] booting clean-room ref core to CONCERT ...")
    cr, msr = BR.boot(verbose=False)
    if not ("mainloop" in msr and "prog_load" in msr):
        print(f"      REF CORE DID NOT REACH MAINLOOP: {msr}")
        print("      (serial/interrupt timing needs adjustment; cannot run the cross-check)")
        return False
    rwcs = bytes(cr.memory[0x4000:0x4200])
    print(f"      ref core reached mainloop;  0x4000[:8]={rwcs[:8].hex()}")

    # ---- whole-image diff ----
    diffs = [(i, kwcs[i], rwcs[i]) for i in range(0x200) if kwcs[i] != rwcs[i]]
    # ---- lane-by-lane ----
    lane_diffs = {0: [], 1: [], 2: [], 3: []}
    for i, a, b in diffs:
        lane_diffs[i & 3].append((i // 4, a, b))

    print("\n" + "=" * 70)
    print(f"WHOLE 0x4000..0x41FF: {len(diffs)} / 512 bytes differ")
    for ln in range(4):
        tag = "  <-- LANE 3 (cmag/XFER/ZERO — reverb-critical)" if ln == 3 else ""
        print(f"  lane {ln} ({'4k+%d'%ln} bytes): {len(lane_diffs[ln])} diffs{tag}")

    if diffs:
        print("\nfirst differing steps:")
        for i, a, b in diffs[:24]:
            extra = ""
            if i & 3 == 3:
                dk, dr = decode_lane3(a), decode_lane3(b)
                extra = f"  kosarev{dk} vs ref{dr}"
            print(f"  step {i//4:>3} lane {i&3}: 0x{0x4000+i:04X} kosarev={a:02X} ref={b:02X}{extra}")

    identical = not diffs
    l3_identical = not lane_diffs[3]
    verdict = ("G3 CLOSED — WCS byte-identical on two independent verified cores (lane 3 included)"
               if identical else
               ("lane 3 IDENTICAL but other lanes differ (investigate non-coeff bytes)"
                if l3_identical else
                "G3 OPEN — lane 3 DIFFERS between cores; adjudicate vs 8080 spec (see steps above)"))
    print("\n" + "=" * 70)
    print(f"VERDICT: {verdict}")
    print(f"  AC2 (lane 3 identical on two independent cores): {'PASS' if l3_identical else 'FAIL'}")
    print("=" * 70)

    out = {
        "kosarev_wcs": kwcs.hex(),
        "ref_wcs": rwcs.hex(),
        "total_diffs": len(diffs),
        "lane_diff_counts": {ln: len(lane_diffs[ln]) for ln in range(4)},
        "lane3_identical": l3_identical,
        "identical": identical,
        "ref_milestones": msr,
        "verdict": verdict,
    }
    with open(os.path.join(SCR, "phase2_lane3_crosscore.json"), "w") as f:
        json.dump(out, f, indent=1)
    print(f"\nwrote {SCR}/phase2_lane3_crosscore.json")
    return l3_identical


if __name__ == "__main__":
    ok = main()
    sys.exit(0 if ok else 1)
