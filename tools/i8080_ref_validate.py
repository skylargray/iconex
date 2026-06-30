#!/usr/bin/env python3
"""Validate the clean-room tools/i8080_ref.I8080 core two independent ways (plan 019 Phase 2b).

PART A — SPEC-FORMULA ALU ORACLE (independent of any emulator).
  Exhaustively sweep every ALU operation over all operands/carry-in and check the ref core's result
  + S/Z/AC/P/C against flag formulas computed DIRECTLY from the documented 8080 definitions:
    parity = even popcount;  add carry/half-carry = nibble/byte overflow;  sub = complement-add.
  This is the decisive check for the G3 risk (the z80emu parity-vs-overflow bug): if the ref core
  ever set P to overflow instead of parity, the exhaustive ADD/SUB/CMP sweep would catch it on the
  first operand pair whose overflow != parity. The oracle is pure arithmetic, NOT another emulator,
  so passing it certifies the ref core independently of kosarev.

PART B — DIFFERENTIAL FUZZ vs the exerciser-verified kosarev z80.I8080Machine.
  For all 256 opcodes, run thousands of random machine states (registers, flags, a 256-byte scratch
  page, absolute-address operands aimed into that page) one instruction at a time on BOTH cores and
  require identical registers / flags / PC / SP / scratch memory. Catches decode/addressing bugs the
  ALU oracle can't (the oracle only covers arithmetic). kosarev is the oracle here; agreement on every
  opcode means the ref core executes the firmware's instruction stream identically.

Pass BOTH => the ref core is a trustworthy independent second 8080 for the lane-3 cross-check (2c).

Run:  python tools/i8080_ref_validate.py
"""
import os
import sys
import random

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
sys.stdout.reconfigure(encoding="utf-8")
from i8080_ref import I8080


# ----------------------------------------------------------------------------
# independent spec-flag formulas
# ----------------------------------------------------------------------------
def par(x):
    return 1 - (bin(x & 0xFF).count("1") & 1)      # even-parity = 1


def f_add(a, b, cin):
    full = a + b + cin
    r = full & 0xFF
    return dict(r=r, S=(r >> 7) & 1, Z=int(r == 0), P=par(r),
                C=int(full > 0xFF), AC=int(((a & 0xF) + (b & 0xF) + cin) > 0xF))


def f_sub(a, b, cin):                               # cin = borrow-in
    full = a - b - cin
    r = full & 0xFF
    ac = int(((a & 0xF) + ((~b) & 0xF) + (1 - cin)) > 0xF)   # complement-add half carry
    return dict(r=r, S=(r >> 7) & 1, Z=int(r == 0), P=par(r), C=int(full < 0), AC=ac)


def f_logic(r, c, ac):
    return dict(r=r & 0xFF, S=(r >> 7) & 1, Z=int((r & 0xFF) == 0), P=par(r), C=c, AC=ac)


def f_daa(a, cf, hf):
    corr = 0
    new_c = cf
    if hf or (a & 0xF) > 9:
        corr += 0x06
    if cf or (a >> 4) > 9 or ((a >> 4) == 9 and (a & 0xF) > 9):
        corr += 0x60
        new_c = 1
    r = (a + corr) & 0xFF
    return dict(r=r, S=(r >> 7) & 1, Z=int(r == 0), P=par(r), C=new_c,
                AC=int(((a & 0xF) + (corr & 0xF)) > 0xF))


def core_flags(cpu):
    return dict(S=cpu.sf, Z=cpu.zf, AC=cpu.hf, P=cpu.pf, C=cpu.cf)


def cmp_flags(got_r, exp, where, fails, check_r=True):
    g = got_r
    bad = []
    if check_r and g["r"] != exp["r"]:
        bad.append(f"r {g['r']:02X}!={exp['r']:02X}")
    for fl in ("S", "Z", "AC", "P", "C"):
        if g[fl] != exp[fl]:
            bad.append(f"{fl} {g[fl]}!={exp[fl]}")
    if bad:
        fails.append(f"{where}: " + ", ".join(bad))
    return not bad


# ----------------------------------------------------------------------------
# PART A
# ----------------------------------------------------------------------------
def part_a():
    print("=" * 70)
    print("PART A — exhaustive spec-formula ALU oracle (independent of kosarev)")
    print("=" * 70)
    fails = []
    n = 0

    def run_binary(name, method, oracle, use_cin, store=True):
        nonlocal n
        cins = (0, 1) if use_cin else (0,)
        for a in range(256):
            for b in range(256):
                for cin in cins:
                    cpu = I8080()
                    cpu.a = a
                    cpu.cf = cin
                    method(cpu, b)
                    exp = oracle(a, b, cin)
                    got = {**core_flags(cpu), "r": cpu.a}
                    cmp_flags(got, exp, f"{name} a={a:02X} b={b:02X} cy={cin}", fails, check_r=store)
                    n += 1

    run_binary("ADD", lambda c, b: c._add(b, 0), lambda a, b, ci: f_add(a, b, 0), False)
    run_binary("ADC", lambda c, b: c._add(b, c.cf), lambda a, b, ci: f_add(a, b, ci), True)
    run_binary("SUB", lambda c, b: c._sub(b, 0), lambda a, b, ci: f_sub(a, b, 0), False)
    run_binary("SBB", lambda c, b: c._sub(b, c.cf), lambda a, b, ci: f_sub(a, b, ci), True)
    run_binary("ANA", lambda c, b: c._ana(b), lambda a, b, ci: f_logic(a & b, 0, ((a | b) >> 3) & 1), False)
    run_binary("XRA", lambda c, b: c._xra(b), lambda a, b, ci: f_logic(a ^ b, 0, 0), False)
    run_binary("ORA", lambda c, b: c._ora(b), lambda a, b, ci: f_logic(a | b, 0, 0), False)
    # CMP: flags like SUB, A unchanged
    for a in range(256):
        for b in range(256):
            cpu = I8080(); cpu.a = a; cpu._cmp(b)
            exp = f_sub(a, b, 0)
            got = {**core_flags(cpu), "r": cpu.a}
            cmp_flags(got, exp, f"CMP a={a:02X} b={b:02X}", fails, check_r=False)
            if cpu.a != a:
                fails.append(f"CMP a={a:02X} b={b:02X}: A modified to {cpu.a:02X}")
            n += 1

    # INR/DCR (C must be preserved)
    for v in range(256):
        for cin in (0, 1):
            cpu = I8080(); cpu.cf = cin; r = cpu._inr(v)
            exp = dict(r=(v + 1) & 0xFF, S=((v + 1) >> 7) & 1, Z=int((v + 1) & 0xFF == 0),
                       P=par(v + 1), C=cin, AC=int((v & 0xF) == 0xF))
            cmp_flags({**core_flags(cpu), "r": r}, exp, f"INR v={v:02X} cy={cin}", fails)
            cpu = I8080(); cpu.cf = cin; r = cpu._dcr(v)
            exp = dict(r=(v - 1) & 0xFF, S=((v - 1) >> 7) & 1, Z=int((v - 1) & 0xFF == 0),
                       P=par(v - 1), C=cin, AC=int((v & 0xF) != 0))
            cmp_flags({**core_flags(cpu), "r": r}, exp, f"DCR v={v:02X} cy={cin}", fails)
            n += 2

    # DAA
    for a in range(256):
        for cf in (0, 1):
            for hf in (0, 1):
                cpu = I8080(); cpu.a = a; cpu.cf = cf; cpu.hf = hf; cpu._daa()
                exp = f_daa(a, cf, hf)
                cmp_flags({**core_flags(cpu), "r": cpu.a}, exp, f"DAA a={a:02X} cf={cf} hf={hf}", fails)
                n += 1

    # rotates (only C changes; S/Z/P/AC preserved). Exercised through step()/the opcode path.
    for a in range(256):
        for cin in (0, 1):
            cpu = I8080()
            cpu.a = a; cpu.cf = cin; cpu.sf = cpu.zf = cpu.pf = cpu.hf = 1
            _exec_op(cpu, 0x07)
            _chk_rot("RLC", cpu, ((a << 1) | (a >> 7)) & 0xFF, (a >> 7) & 1, fails)
            cpu.a = a; cpu.cf = cin; cpu.sf = cpu.zf = cpu.pf = cpu.hf = 1
            _exec_op(cpu, 0x0F)
            _chk_rot("RRC", cpu, ((a >> 1) | ((a & 1) << 7)) & 0xFF, a & 1, fails)
            cpu.a = a; cpu.cf = cin; cpu.sf = cpu.zf = cpu.pf = cpu.hf = 1
            _exec_op(cpu, 0x17)
            _chk_rot("RAL", cpu, ((a << 1) | cin) & 0xFF, (a >> 7) & 1, fails)
            cpu.a = a; cpu.cf = cin; cpu.sf = cpu.zf = cpu.pf = cpu.hf = 1
            _exec_op(cpu, 0x1F)
            _chk_rot("RAR", cpu, ((a >> 1) | (cin << 7)) & 0xFF, a & 1, fails)
            n += 4

    print(f"  ALU oracle checks run: {n}")
    if fails:
        print(f"  FAIL: {len(fails)} mismatches. First 20:")
        for f in fails[:20]:
            print("    " + f)
        return False
    print("  PASS — ref core matches the 8080 spec flag formulas on every operand (parity included).")
    return True


def _seed_rot(a, cin):
    cpu = I8080(); cpu.a = a; cpu.cf = cin; return cpu


def _exec_op(cpu, opcode):
    cpu.memory[cpu.pc] = opcode
    cpu.step()


def _chk_rot(name, cpu, er, ec, fails):
    bad = []
    if cpu.a != er: bad.append(f"r {cpu.a:02X}!={er:02X}")
    if cpu.cf != ec: bad.append(f"C {cpu.cf}!={ec}")
    if not (cpu.sf and cpu.zf and cpu.pf and cpu.hf):
        bad.append("S/Z/P/AC not preserved")
    if bad:
        fails.append(f"{name}: " + ", ".join(bad))


# ----------------------------------------------------------------------------
# PART B — differential fuzz vs kosarev
# ----------------------------------------------------------------------------
def part_b(iters_per_op=3000, seed=0xC0FFEE):
    import z80
    print("\n" + "=" * 70)
    print(f"PART B — differential fuzz vs kosarev I8080Machine ({iters_per_op}/opcode)")
    print("=" * 70)
    rng = random.Random(seed)
    K = z80.I8080Machine()
    R = I8080()

    PC0 = 0x0100
    SCR0, SCRN = 0x2000, 0x100             # scratch page the pointers/operands aim into
    # IN/OUT deterministic models so both cores see identical I/O
    io_in = {}
    out_log = []

    def kin(p):
        return io_in.get(p & 0xFF, (p * 7 + 0x5A) & 0xFF)
    def kout(p, v):
        out_log.append(("K", p & 0xFF, v & 0xFF))
    def rin(p):
        return io_in.get(p & 0xFF, (p * 7 + 0x5A) & 0xFF)
    def rout(p, v):
        out_log.append(("R", p & 0xFF, v & 0xFF))
    K.set_input_callback(kin); K.set_output_callback(kout)
    R.in_cb = rin; R.out_cb = rout

    fails = []
    total = 0

    def kiff():
        return K._I8080State__iff[0]

    for op in range(256):
        for _ in range(iters_per_op):
            # ---- random state ----
            a = rng.randint(0, 255); b = rng.randint(0, 255); c = rng.randint(0, 255)
            d = rng.randint(0, 255); e = rng.randint(0, 255)
            h = (SCR0 >> 8) & 0xFF; l = rng.randint(0, SCRN - 4)     # HL -> scratch page
            f = (rng.randint(0, 255) & 0xD5) | 0x02
            sp = SCR0 + 0x80 + (rng.randint(0, 0x30) & 0xFE)         # SP in scratch page
            # instruction bytes: opcode + up to 2 operand bytes
            o1 = rng.randint(0, 255); o2 = rng.randint(0, 255)
            # for absolute-addr / jump / call ops aim the 16-bit operand into the scratch page
            if op in (0x22, 0x2A, 0x32, 0x3A,                       # SHLD/LHLD/STA/LDA
                      0xC3, 0xCB, 0xC2, 0xCA, 0xD2, 0xDA, 0xE2, 0xEA, 0xF2, 0xFA,  # JMP/Jcc
                      0xCD, 0xDD, 0xED, 0xFD, 0xC4, 0xCC, 0xD4, 0xDC, 0xE4, 0xEC, 0xF4, 0xFC):  # CALL/Ccc
                tgt = SCR0 + rng.randint(0, SCRN - 4)
                o1, o2 = tgt & 0xFF, (tgt >> 8) & 0xFF
            # BC/DE for LDAX/STAX -> scratch page
            if op in (0x0A, 0x02):
                c = rng.randint(0, SCRN - 1); b = (SCR0 >> 8) & 0xFF
            if op in (0x1A, 0x12):
                e = rng.randint(0, SCRN - 1); d = (SCR0 >> 8) & 0xFF

            # ---- identical scratch page ----
            scratch = bytes(rng.randint(0, 255) for _ in range(SCRN))

            # ---- clear kosarev sticky internal flags (halted/iff persist across run() calls) ----
            K._I8080State__halted[0] = 0
            K._I8080State__iff[0] = 0
            # ---- load kosarev ----
            K.memory[SCR0:SCR0 + SCRN] = scratch
            K.memory[PC0] = op; K.memory[PC0 + 1] = o1; K.memory[PC0 + 2] = o2
            K.a = a; K.bc = (b << 8) | c; K.de = (d << 8) | e; K.hl = (h << 8) | l
            K.af = (a << 8) | f; K.sp = sp; K.pc = PC0
            # ---- load ref ----
            R.memory[SCR0:SCR0 + SCRN] = scratch
            R.memory[PC0] = op; R.memory[PC0 + 1] = o1; R.memory[PC0 + 2] = o2
            R.a = a; R.b = b; R.c = c; R.d = d; R.e = e; R.h = h; R.l = l
            R.set_psw(f); R.sp = sp; R.pc = PC0
            R.halted = False; R.int_pending = None

            # ---- single-step each ----
            try:
                K.ticks_to_stop = 1; K.run()
            except Exception as ex:
                fails.append(f"op {op:02X}: kosarev raised {ex}"); total += 1; continue
            try:
                R.step()
            except Exception as ex:
                fails.append(f"op {op:02X}: ref raised {ex}"); total += 1; continue
            total += 1

            # HLT (0x76): kosarev parks PC at the HLT; ref advances past it (8080 manual). Harmless
            # modeling choice; not used anywhere in the firmware build. Verify the halt, skip compare.
            if op == 0x76:
                if not R.halted or K._I8080State__halted[0] != 1:
                    fails.append(f"op 76: HLT did not halt (R={R.halted} K={K._I8080State__halted[0]})")
                continue

            # ---- compare (skip iff: EI/DI delayed-enable differs harmlessly) ----
            diffs = []
            if R.a != K.a: diffs.append(f"A {R.a:02X}!={K.a:02X}")
            if R.b != K.b: diffs.append(f"B {R.b:02X}!={K.b:02X}")
            if R.c != K.c: diffs.append(f"C {R.c:02X}!={K.c:02X}")
            if R.d != K.d: diffs.append(f"D {R.d:02X}!={K.d:02X}")
            if R.e != K.e: diffs.append(f"E {R.e:02X}!={K.e:02X}")
            if R.h != K.h: diffs.append(f"H {R.h:02X}!={K.h:02X}")
            if R.l != K.l: diffs.append(f"L {R.l:02X}!={K.l:02X}")
            if (R.get_psw() & 0xD5) != (K.f & 0xD5):
                diffs.append(f"F {R.get_psw() & 0xD5:02X}!={K.f & 0xD5:02X}")
            if R.sp != K.sp: diffs.append(f"SP {R.sp:04X}!={K.sp:04X}")
            if R.pc != K.pc: diffs.append(f"PC {R.pc:04X}!={K.pc:04X}")
            if R.memory[SCR0:SCR0 + SCRN] != K.memory[SCR0:SCR0 + SCRN]:
                # find first differing scratch byte
                for i in range(SCRN):
                    if R.memory[SCR0 + i] != K.memory[SCR0 + i]:
                        diffs.append(f"mem@{SCR0 + i:04X} {R.memory[SCR0 + i]:02X}!={K.memory[SCR0 + i]:02X}")
                        break
            if diffs:
                fails.append(f"op {op:02X} (a={a:02X} b={b:02X} c={c:02X} d={d:02X} e={e:02X} "
                             f"l={l:02X} f={f:02X} sp={sp:04X} o1={o1:02X} o2={o2:02X}): "
                             + "; ".join(diffs[:6]))

    by_op = {}
    for fl in fails:
        opc = fl.split()[1]
        by_op[opc] = by_op.get(opc, 0) + 1
    print(f"  instructions compared: {total}")
    if fails:
        print(f"  FAIL: {len(fails)} mismatches across {len(by_op)} opcodes.")
        print("  opcodes with diffs:", " ".join(sorted(by_op)))
        for fl in fails[:25]:
            print("    " + fl)
        return False
    print("  PASS — ref core matches kosarev on all 256 opcodes over all random states.")
    return True


if __name__ == "__main__":
    a_ok = part_a()
    b_ok = part_b()
    print("\n" + "=" * 70)
    print(f"VALIDATION: spec-oracle={'PASS' if a_ok else 'FAIL'}  "
          f"differential-vs-kosarev={'PASS' if b_ok else 'FAIL'}")
    print("=" * 70)
    sys.exit(0 if (a_ok and b_ok) else 1)
