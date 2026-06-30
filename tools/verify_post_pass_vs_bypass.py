#!/usr/bin/env python3
"""Phase 3 — empirical POST-pass vs POST-bypass WCS comparison. Closes G2 empirically.

Two boots that reach the CONCERT WCS build by DIFFERENT paths:
  • POST-BYPASS: tools/boot8080.boot — POST runs, the stubbed ARU fails the self-test (DIAG E32),
    and we inject the PGM-2 'skip diagnostics' key to proceed (the path used everywhere else).
  • POST-PASS:  tools/aru_post.run_post — a netlist-faithful ARU is wired onto the ARU I/O ports so
    the firmware's self-test PASSES on its own merits (E32+E40+E83+E91 all PASS); the firmware then
    proceeds to load CONCERT with NO PGM-2 inject (a fully-passing ARU never needs it).

If m.memory[0x4000:0x4200] is byte-identical between the two, the WCS build is invariant to whether
POST passed or was bypassed -> G2 CLOSED empirically (the bypass we use everywhere is harmless).
Per plan 019, differ -> the POST-passing WCS is authoritative and the decode table must be regenerated.

Run:  python tools/verify_post_pass_vs_bypass.py
"""
import os
import sys
import json

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
sys.stdout.reconfigure(encoding="utf-8")
import boot8080 as B
import aru_post

SCR = (r"C:/Users/Skylar/AppData/Local/Temp/claude/"
       r"d--OneDrive-Gray-Instruments-iconex/ae30a9a1-b02b-4706-a6d3-7d89d4cefad3/scratchpad")
os.makedirs(SCR, exist_ok=True)


def main():
    print("### Phase 3 — POST-pass vs POST-bypass WCS comparison (G2) ###\n")

    print("[1/2] POST-BYPASS boot (boot8080, PGM-2 skip) ...")
    mb, msb = B.boot(verbose=False)
    assert "mainloop" in msb and "prog_load" in msb, f"bypass boot failed: {msb}"
    bypass_wcs = bytes(mb.memory[0x4000:0x4200])
    print(f"      reached mainloop; 0x4000[:8]={bypass_wcs[:8].hex()}")

    print("[2/2] POST-PASS boot (aru_post, faithful ARU, POST un-suppressed) ...")
    verdict, errs, aru = aru_post.run_post(verbose=False)
    reached = verdict.get("_reached_mainloop", False)
    pass_wcs = bytes(aru.mem[0x4000:0x4200])
    print(f"      POST sub-test verdict:")
    for k in sorted(verdict):
        if not k.startswith("_"):
            print(f"        {k}: {verdict[k]}")
    print(f"      reached_normal_op={verdict.get('_reached_normal_op', False)} "
          f"reached_mainloop={reached}; DIAG errors={len(errs)}")
    print(f"      0x4000[:8]={pass_wcs[:8].hex()}")

    post_all_pass = all(str(v) == "PASS" for k, v in verdict.items()
                        if not k.startswith("_") and ("PASS" in str(v) or "FAIL" in str(v)))

    if not reached:
        print("\n  POST-PASS boot did NOT reach mainloop — cannot complete the empirical comparison.")
        print(f"  (verdict={verdict})")
        # still report whatever WCS state exists
        ok = False
    else:
        diffs = [(i, bypass_wcs[i], pass_wcs[i]) for i in range(0x200)
                 if bypass_wcs[i] != pass_wcs[i]]
        lane_diffs = {ln: [d for d in diffs if d[0] & 3 == ln] for ln in range(4)}
        print("\n" + "=" * 70)
        print(f"0x4000..0x41FF: {len(diffs)} / 512 bytes differ (POST-pass vs POST-bypass)")
        for ln in range(4):
            print(f"  lane {ln}: {len(lane_diffs[ln])} diffs")
        if diffs:
            print("\n  first differing bytes:")
            for i, a, b in diffs[:24]:
                print(f"    step {i//4:>3} lane {i&3}: 0x{0x4000+i:04X} bypass={a:02X} pass={b:02X}")
        ok = not diffs
        print("\n" + "=" * 70)
        if ok:
            print("VERDICT: G2 CLOSED — WCS identical with POST-pass vs POST-bypass.")
        else:
            print("VERDICT: G2 OPEN — WCS DIFFERS; the POST-pass WCS is authoritative (regenerate decode).")
        print(f"  POST self-test all sub-tests PASS: {post_all_pass}")
        print(f"  AC3 (0x4000 identical POST-pass vs POST-bypass): {'PASS' if ok else 'FAIL'}")
        print("=" * 70)

    out = {
        "post_all_pass": post_all_pass,
        "reached_mainloop": reached,
        "bypass_wcs_8": bypass_wcs[:8].hex(),
        "pass_wcs_8": pass_wcs[:8].hex(),
        "identical": bool(reached and bypass_wcs == pass_wcs),
        "verdict_subtests": {k: str(v) for k, v in verdict.items()},
    }
    with open(os.path.join(SCR, "phase3_post_pass_vs_bypass.json"), "w") as f:
        json.dump(out, f, indent=1)
    print(f"\nwrote {SCR}/phase3_post_pass_vs_bypass.json")
    return out["identical"]


if __name__ == "__main__":
    ok = main()
    sys.exit(0 if ok else 1)
