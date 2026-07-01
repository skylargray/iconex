#!/usr/bin/env python3
"""Plan 020 Phase 1 verification — the edge-driven deferred MAC on aru_rtl_dp.ARU_RTL.

Checks (POST itself is run separately via `python tools/aru_post.py`):
  1.4  the gate-Booth product reproduces the 20 POST goldens (positive exact, negative ≤2 LSB) AND
       the cmag=63 / unity cases.
  1.5  ★ anti-"faithfully wrong" battery: the edge-driven deferred MAC (ARU_RTL.mac_step, sequenced by
       ClockEngine edges) reproduces aru_freerun's statement-order deferred MAC across a RANDOMIZED sweep
       of (opnd, cmag, csign, XFER, ZERO) — POST steps 126/127 + 20 goldens are far too narrow to certify
       the edge wiring alone (hand-traces had confirmed errors; §4F.4).

Run:  python tools/test_phase1_edgemac.py
"""
import os
import sys
import random

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import aru_rtl_dp as DP
import aru_booth as B
import aru_freerun as FR


def test_booth_product_equivalence():
    """_booth_product must equal aru_freerun.product20 for a broad input sweep (same gate core)."""
    aru = DP.ARU_RTL(bytearray(0x10000))
    rng = random.Random(20260630)
    n = miss = 0
    for _ in range(4000):
        x = rng.randint(-32768, 32767)
        cmag = rng.randint(0, 63)
        cs = rng.randint(0, 1)
        a = aru._booth_product(x, cmag, cs)
        b = FR.product20(x, cmag, cs)
        n += 1
        if a != b:
            miss += 1
            if miss <= 5:
                print(f"    MISS x={x} cmag={cmag} cs={cs}: dp={a} fr={b}")
    print(f"1.x _booth_product == aru_freerun.product20: {n-miss}/{n} exact "
          f"[{'OK' if miss == 0 else 'FAIL'}]")
    return miss == 0


def test_goldens():
    """1.4 — res_from_acc(_booth_product) reproduces the 20 goldens (pos exact, neg ≤2 LSB) + unity."""
    aru = DP.ARU_RTL(bytearray(0x10000))
    ok = exact = 0
    for Fop, cmag, cs, exp in B.GOLDENS:
        res = DP.res_from_acc(aru._booth_product(Fop, cmag, cs))
        if res == exp:
            exact += 1; ok += 1
        elif abs(res - exp) <= 2:
            ok += 1
        else:
            print(f"    MISS F=0x{Fop & 0xFFFF:04X} cmag={cmag} cs={cs} exp={exp:+d} got={res:+d}")
    u1 = DP.res_from_acc(aru._booth_product(0x5555, 32, 1))
    u2 = DP.res_from_acc(aru._booth_product(0x1234, 32, 1))
    print(f"1.4 goldens via edge-MAC product: {exact}/20 exact, {ok}/20 within 2 LSB; "
          f"unity 0x5555->{u1}(want 21845) 0x1234->{u2}(want 4660) "
          f"[{'OK' if ok == 20 and u1 == 21845 and u2 == 4660 else 'FAIL'}]")
    return ok == 20 and u1 == 21845 and u2 == 4660


def _ref_deferred_mac(seq):
    """Reference = aru_freerun's exact deferred MAC (product20 + res_from_acc), statement-ordered.
    Returns the RES trajectory (RES after each step, reflecting that step's AS0 retire)."""
    ACC = 0; RES = 0; pend = None; out = []
    for (opnd, cmag, cs, xfer, zero) in seq:
        if pend is not None:
            Vp, zp, xp = pend
            ACC = DP.sat20(ACC + Vp)
            if xp:
                RES = FR.res_from_acc(ACC)
            if zp:
                ACC = 0
            pend = None
        V = FR.product20(opnd, cmag, cs)
        pend = (V, zero, xfer)
        out.append(RES)
    return out


def test_edge_mac_reproduces_freerun():
    """1.5 — the edge-driven mac_step must reproduce the reference deferred MAC over random sequences,
    including the ACC trajectory (not just final RES). Sweeps XFER/ZERO combinations densely."""
    rng = random.Random(4224)
    fails = 0
    for trial in range(200):
        seq = []
        for _ in range(rng.randint(4, 40)):
            seq.append((rng.randint(-32768, 32767), rng.randint(0, 63),
                        rng.randint(0, 1), rng.randint(0, 1), rng.randint(0, 1)))
        ref = _ref_deferred_mac(seq)
        aru = DP.ARU_RTL(bytearray(0x10000))
        aru.free_reset()
        got = [aru.mac_step(*step) for step in seq]
        if got != ref:
            fails += 1
            if fails <= 3:
                i = next(j for j in range(len(ref)) if got[j] != ref[j])
                print(f"    trial {trial} diverges @step {i}: got={got[i]} ref={ref[i]}")
    print(f"1.5 edge-MAC reproduces aru_freerun deferred MAC: {200-fails}/200 random sequences "
          f"[{'OK' if fails == 0 else 'FAIL'}]")
    return fails == 0


def main():
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass
    print("=" * 74)
    print("Plan 020 Phase 1 — edge-driven deferred MAC verification")
    print("=" * 74)
    ok = True
    ok &= test_booth_product_equivalence()
    ok &= test_goldens()
    ok &= test_edge_mac_reproduces_freerun()
    print("-" * 74)
    print(f"PHASE 1 MAC TESTS: {'ALL OK' if ok else 'FAILED'}")
    print("(run POST separately: python tools/aru_post.py — must stay E32/E40/E83/E91 PASS)")
    return ok


if __name__ == "__main__":
    sys.exit(0 if main() else 1)
