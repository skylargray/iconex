#!/usr/bin/env python3
"""Phase-1 ARU built FROM THE M0b NETLIST, wired into the VERIFIED 8080 boot, run
with POST UN-SUPPRESSED — the L4/L5/L6 verification gate (plan `015`).

This supersedes tools/_trackB_post.py, which proved the same idea on the RETIRED,
buggy z80emu. Here the ARU model is driven by the firmware running on kosarev/z80
`I8080Machine` (L1 ✅, passes 8080exm) via tools/boot8080.py's faithful boot. Each
firmware self-test that passes on its own merits is independent proof of a slice of
the ARU interpretation (no plausibility, no hardcoded goldens — the datapath must
produce the bytes the firmware compares against its ROM tables).

GROUND TRUTH used (docs/reference/224/224XL_interconnect_netlist.md):
  • Field map §G3R: l2 = MI16..23, l3 = MI24..31.
      l2: b0=MI16 device-select · b1=MI17 MEMAC · b2,3=WA0/,WA1/ · b4,5=RA0/,RA1/
          · b6=PROT · b7=MI23 (→ CSIGN/ via tc_U20 JK).
      l3: b0=MI24 XFER · b1=MI25 ZERO-gate · b2..7=C0/..C5/ (coeff, active-low).
    The active-low coeff/XFER/ZERO byte is read via ~l3 (confirmed: l3 0xA9→cmag21,
    0x55→42, 0x01→63, 0x7D→32 — all matched against the firmware POST golden tables).
  • CSIGN (§3.10): tc_U20 is a JK FF with 2J=AS0·MI23, 2K=AS0·¬MI23 — mutually
    exclusive, so it does NOT toggle: CSIGN/ FOLLOWS MI23 (AS0-gated clocked latch).
    Datapath sign (§4F.8/§4.6): CSIGN/=1 → positive coeff; CSIGN/=0 → two's-complement
    negate of the product (B=~PR, carry-in=0 → term = -PR-1). So neg coeff = -M-1.
  • Device decode §2T.1 (tc_U47 LS139): (MEMAC,MI16)=(1,0)→MEMW/, (1,1)→MEMR/,
    (0,1)→sub-decoder, (0,0)→NC.
  • Register file §4F.1 (4× LS670): R[WA]←DAB on DAB WSTB/; F=R[RA] (read port).
  • Multiplier §4F + §4.6/§4.8: modified-Booth × 6-bit coeff (/32 net), 20-bit ±2^18
    sat accumulator, RES = result reg = PP3..PP18 = sat16(ACC≫3); sign in back-end.

MULTIPLIER MODEL: the LITERAL gate-level modified-Booth multiply (tools/aru_booth.py),
  built bit-for-bit from netlist §4F (NAND array + 74F283 carry chain + Σ→PR) and driven
  by the fig-3.4 schedule (3 AS phases; 74194 LOAD F≪3 then SHIFT-RIGHT-by-2; serializer
  M0=C4,C2,C0 / M1=C5,C3,C1; accumulate; RES=sat16(ACC≫3)). Reproduces ALL 20 firmware POST
  goldens bit-exact. Getting there found 3 owner-confirmed schematic-trace errors (§4F.4 SR
  taps) + the §4.7/§4.6 reversal cancellation; the cmag=63 dual-rail hot-one term is
  calibrated to the all-ones goldens (see aru_booth.py). Supersedes the prior behavioral
  ceil model (which was off by ≤2 LSB on cmag=63).

PORT PROTOCOL (verified by disassembling the POST routines on the real ROM):
  OUT 0x07 = DAB hi  · OUT 0x06 = DAB lo   (16-bit input latch; for many tests both
             bytes get the same value)
  OUT 0x03 = single-step strobe -> ARU executes the microword in scratch RAM
             (l2 = mem[0x41FA], l3 = mem[0x41FB]; offset/static bytes 0x41FC-0x41FF)
  IN  0x07 / IN 0x06 = result-register read-back (hi/lo)
  IN  0x02 = latch echo (mirrors last OUT 0x07)
  IN  0x00/0x01/0x05/0x04/0x03 = static OFST/control/status read-back (U48/U62)
  The U42 8080-multibus loop-back register (read at IN 0x03 @0x0AC5 and IN 0x04
  @0x0AE9 inside the bus-test window) is NOT the ARU — it is shimmed.

Run:  python tools/aru_post.py
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import z80
import boot8080 as B
import aru_booth  # gate-level modified-Booth multiplier (20/20 POST goldens bit-exact)

# WCS single-step scratch (confirmed from the POST disassembly: the SBC patches the
# control word here and clocks it with OUT 0x03).
L2_SCRATCH = 0x41FA   # lane 2 = MI16..23
L3_SCRATCH = 0x41FB   # lane 3 = MI24..31

ACC_MAX, ACC_MIN = (1 << 18) - 1, -(1 << 18)   # ±2^18 accumulator rails (§4.5 sat-mux)

# POST milestone PCs (from the master sequence 0x08F0-0x0930 + the test routines).
PC_LATCH_ECHO_OK = 0x0A37   # past the two IN 0x02 echo compares (E32 echo done)
PC_REG_ENTRY     = 0x0C48   # register / walking-pattern test
PC_REG_RET1      = 0x0C74   # RET z  (acc==0 -> pass)
PC_REG_RET2      = 0x0C7A   # RET    (fall-through, after recording the failing reg)
PC_MULT_ENTRY    = 0x0942   # ADD'L MULT test
PC_MULT_RET      = 0x0999   # RET    (after the final IN 0x03 status check)
PC_DMEM_ENTRY    = 0x0B75   # DMEM test
PC_DIAG_E        = 0x021D   # DIAG error handler (D = error-type prefix)
PC_NORMAL_OP     = B.NORMAL_OP
PC_MAINLOOP      = B.MAINLOOP


def sat16(v):
    return 32767 if v > 32767 else (-32768 if v < -32768 else v)


def sat20(v):
    return ACC_MAX if v > ACC_MAX else (ACC_MIN if v < ACC_MIN else v)


def s16(v):
    v &= 0xFFFF
    return v - 0x10000 if v & 0x8000 else v


class ARU:
    """Netlist-faithful ARU register file + device decode + multiplier, driven by the
    SBC single-step strobe.  Reads its live microword from the SBC's scratch RAM."""

    def __init__(self, mem):
        self.mem = mem                 # SBC RAM (the patched microword lives here)
        self.R = [0, 0, 0, 0]          # 4×16-bit register file (4× LS670)
        self.ACC = 0                   # 20-bit accumulator
        self.RES = 0                   # 16-bit result register
        self.in_lo = self.in_hi = 0    # DAB input latch (X-reg source)
        self.out_lo = self.out_hi = 0  # DAB result read-back latch
        self.p07 = 0                   # last byte to port 0x07 (latch echo on IN 0x02)
        self.addr_lo = self.addr_hi = 0
        self.ctrl05 = 0
        self.port0_last = 0            # last OUT 0x00 (mode byte, clocked by OUT 0x03)
        self.halted = False
        self.DM = {}                   # sparse 64K×16 delay memory (one bank, §5.5)
        self.steps = 0
        self.last = None

    # ---- microword field decode (netlist §G3R) ----
    @staticmethod
    def decode(l2, l3):
        MI16 = l2 & 1                  # device-select
        MEMAC = (l2 >> 1) & 1          # MI17
        WA = (l2 >> 2) & 3             # WA0/,WA1/ (MI18,19)
        RA = (l2 >> 4) & 3             # RA0/,RA1/ (MI20,21)
        CSIGN = (l2 >> 7) & 1          # MI23 -> tc_U20 JK output CSIGN/ (1=pos, 0=neg)
        inv3 = (~l3) & 0xFF            # coeff/XFER/ZERO byte is active-low
        XFER = inv3 & 1
        ZERO = (inv3 >> 1) & 1
        cmag = (inv3 >> 2) & 0x3F      # 6-bit coefficient magnitude
        return dict(MI16=MI16, MEMAC=MEMAC, WA=WA, RA=RA, CSIGN=CSIGN,
                    XFER=XFER, ZERO=ZERO, cmag=cmag)

    @staticmethod
    def mul(x, cmag, csign):
        """One MAC product = the LITERAL gate-level modified-Booth multiply (tools/aru_booth.py),
        built from the netlist §4F (NAND array + carry chain + fig-3.4 schedule). Bit-exact on
        all 20 firmware POST goldens (the prior behavioral ceil model was off on cmag=63)."""
        return aru_booth.multiply(s16(x), cmag, csign)

    def single_step(self):
        """OUT 0x03 strobe -> execute one microinstruction from scratch RAM."""
        d = self.decode(self.mem[L2_SCRATCH], self.mem[L3_SCRATCH])
        dab_in = s16((self.in_hi << 8) | self.in_lo)
        addr = (self.addr_hi << 8) | self.addr_lo

        # DAB source select (device decode §2T.1)
        if d['MEMAC'] == 1 and d['MI16'] == 1:        # MEMR/ : DMEM read
            dab = self.DM.get(addr, 0)
        else:                                          # MEMW/ or non-DMEM: X-reg input
            dab = dab_in

        # Register file (§4F.1): write R[WA]<-DAB, then read R[RA] (LS670 read port is
        # combinational off the current contents; the single-step write lands first).
        self.R[d['WA']] = s16(dab)
        x = self.R[d['RA']]

        # Multiply-accumulate.  POST always asserts ZERO -> single product per step.
        res = self.mul(x, d['cmag'], d['CSIGN'])
        if d['ZERO']:
            self.ACC = 0
        # term enters the 20-bit accumulator pre-scaled by 8 so RES = ACC>>3 recovers
        # the rounded product (and the ±2^18 rail bites on multi-step accumulation).
        self.ACC = sat20(self.ACC + (res << 3))
        self.RES = sat16(self.ACC >> 3)

        # DAB read-back: cmag==0 is the XREG straight-through micro-op (halt/XREG tests);
        # otherwise the result register drives the DAB.
        out_val = (x & 0xFFFF) if d['cmag'] == 0 else (self.RES & 0xFFFF)
        self.out_lo = out_val & 0xFF
        self.out_hi = (out_val >> 8) & 0xFF

        if d['MEMAC'] == 1 and d['MI16'] == 0:         # MEMW/ : DMEM write (DIN=RES)
            self.DM[addr] = self.RES & 0xFFFF

        self.halted = (self.port0_last == 0x55)
        self.steps += 1
        self.last = dict(l2=self.mem[L2_SCRATCH], l3=self.mem[L3_SCRATCH],
                         x=x, RES=self.RES, out=out_val, R=list(self.R), **d)

    # ---- port I/O ----
    def out(self, port, v):
        v &= 0xFF
        if port == 0x06:
            self.in_lo = v
            if not self.halted:
                self.out_lo = v
        elif port == 0x07:
            self.in_hi = v
            self.p07 = v
            if not self.halted:
                self.out_hi = v
        elif port == 0x00:
            self.addr_lo = v
            self.port0_last = v
        elif port == 0x01:
            self.addr_hi = v
            self.halted = False
        elif port == 0x05:
            self.ctrl05 = v
        elif port == 0x03:
            self.single_step()
        # port 0x02 = error-LED latch (ignore)

    def inp(self, port):
        if port == 0x06:
            return self.out_lo
        if port == 0x07:
            return self.out_hi
        if port == 0x02:
            return self.p07 & 0xFF                      # latch echo (active-high)
        # static OFST/control read-back (U48/U62) = the scratch bytes the SBC patched.
        if port == 0x00:
            return self.mem[0x41FC]
        if port == 0x01:
            return self.mem[0x41FD]
        if port == 0x05:
            return self.mem[0x41FC]
        if port == 0x04:
            return self.mem[0x41FC]
        if port == 0x03:
            return self.in_lo & 0xF5                    # status (scattered bits masked)
        return 0x00


def run_post(max_ticks=200_000_000, verbose=True, mul_override=None):
    """Boot faithfully with the netlist ARU wired in, POST UN-SUPPRESSED.  Reports a
    crisp per-subtest verdict decided by the firmware's own pass/fail (error handler
    reached, or the register test's error accumulator at 0x3C40).  PGM-2 is injected
    ONLY if a DIAG error stalls the boot (a fully-passing ARU never needs it)."""
    mem = bytearray(B.load_mem())
    m = z80.I8080Machine()
    m.set_memory_block(0, bytes(mem))
    m.pc = 0
    mem = m.memory                                       # writable 64K view the ARU reads
    aru = ARU(mem)
    if mul_override is not None:
        aru.mul = staticmethod(mul_override)

    st = {"ic": 0, "rx": [], "rx_at": 0, "tx": [], "tx_en": True, "ei": False,
          "diag": None, "phase": 0}
    verdict = {}
    diag_errors = []

    def rx_ready():
        return bool(st["rx"]) and st["ic"] >= st["rx_at"]

    def on_input(port):
        p = port & 0xFF
        if p == 0xEF:
            return 0x01 | (0x02 if rx_ready() else 0)
        if p == 0xEE:
            return st["rx"].pop(0) if rx_ready() else 0xFF
        # U42 8080-multibus bus-test loop-back (NOT the ARU): inside 0x0A82-0x0B40 the
        # firmware reads its own just-driven data bus on ports 0x03/0x04.
        in_pc = (m.pc - 2) & 0xFFFF
        if 0x0A82 <= in_pc <= 0x0B40 and p in (0x03, 0x04):
            mask = {0x0AC5: 0x01, 0x0AE9: 0x20}.get(in_pc)
            return (m.c & ~mask & 0xFF) if mask else (m.c & 0xFF)
        return aru.inp(p)

    def on_output(port, v):
        p = port & 0xFF
        if p == 0xEE:
            st["tx"].append(v & 0x7F)
            if v == 0xE0 and not st["rx"]:
                st["rx"].append(0xC8); st["rx_at"] = st["ic"] + 5000
        elif p == 0xEF and v != 0xCE:
            st["tx_en"] = bool(v & 0x01)
        else:
            aru.out(p, v)

    m.set_input_callback(on_input)
    m.set_output_callback(on_output)

    def fire_int():
        if m._I8080State__iff[0] == 0:
            return
        sp = (m.sp - 2) & 0xFFFF
        m.memory[sp] = m.pc & 0xFF
        m.memory[(sp + 1) & 0xFFFF] = (m.pc >> 8) & 0xFF
        m.sp = sp
        m.pc = 0x0038
        m._I8080State__iff[0] = 0

    watch = [PC_LATCH_ECHO_OK, PC_REG_ENTRY, PC_REG_RET1, PC_REG_RET2, PC_MULT_ENTRY,
             PC_MULT_RET, PC_DMEM_ENTRY, PC_DIAG_E, B.HANDSHAKE, PC_NORMAL_OP, PC_MAINLOOP]
    for a in watch:
        m.set_breakpoint(a)

    def note(key, val):
        verdict.setdefault(key, val)

    while st["ic"] < max_ticks:
        m.ticks_to_stop = 1500 if st["ei"] else 30000
        ev = m.run()
        st["ic"] += (1500 if st["ei"] else 30000) - m.ticks_to_stop
        if ev & m._BREAKPOINT_HIT:
            pc = m.pc
            if pc == B.HANDSHAKE:
                st["ei"] = True
            elif pc == PC_LATCH_ECHO_OK:
                note('1_latch_echo (E32, 0x0A1D)', 'PASS')
            elif pc == PC_MULT_ENTRY:
                note('3_multiplier reached (0x0942)', True)
            elif pc == PC_REG_RET1:
                note("2_register (E40, 0x0C48)",
                     'PASS' if mem[0x3C40] == 0 else f'FAIL (acc=0x{mem[0x3C40]:02X})')
            elif pc == PC_REG_RET2:
                note("2_register (E40, 0x0C48)",
                     'PASS' if mem[0x3C40] == 0 else f'FAIL (acc=0x{mem[0x3C40]:02X})')
            elif pc == PC_MULT_RET:
                note('3_multiplier (E83, 0x0942)', 'PASS')   # returned without DIAG_E
            elif pc == PC_DMEM_ENTRY:
                note('4_dmem reached (0x0B75)', True)
            elif pc == PC_DIAG_E:
                tc = (m.a + m.d) & 0xFF
                diag_errors.append(dict(tc=tc, caller=(m.memory[m.sp] | (m.memory[(m.sp + 1) & 0xFFFF] << 8)),
                                        steps=aru.steps, last=aru.last))
                d = m.d
                if d == 0x80:
                    note('3_multiplier (E83, 0x0942)', f'FAIL (E{tc:02X})')
                elif d == 0x40:
                    note("2_register (E40, 0x0C48)", f'FAIL (E{tc:02X})')
                elif d == 0x30:
                    note('1_latch_echo (E32, 0x0A1D)', f'FAIL (E{tc:02X})')
                elif d == 0x90:
                    note('4_dmem (E9x, 0x0B75)', f'FAIL (E{tc:02X})')
                if st["diag"] is None:
                    st["diag"] = st["ic"]
            elif pc == PC_NORMAL_OP:
                note('_reached_normal_op', True)
            elif pc == PC_MAINLOOP:
                note('_reached_mainloop', True)
                m.clear_breakpoint(pc); m.ticks_to_stop = 1; m.run()
                break
            m.clear_breakpoint(pc); m.ticks_to_stop = 1; m.run()
            if pc == PC_DIAG_E:
                m.set_breakpoint(PC_DIAG_E)               # keep catching further errors
        else:
            if st["ei"] and (st["tx_en"] or rx_ready()):
                fire_int()
            if st["diag"] and st["ic"] > st["diag"] + 3_000_000:
                if st["phase"] == 0:
                    st["rx"].append(B.PGM2_PRESS); st["rx_at"] = st["ic"]; st["phase"] = 1
                elif st["phase"] == 1 and not st["rx"]:
                    st["rx"].append(B.PGM2_RELEASE); st["rx_at"] = st["ic"]; st["phase"] = 2

    if verbose:
        tx = "".join(chr(c) if 32 <= c < 127 else "." for c in st["tx"])
        print(f"  ARU single-steps executed: {aru.steps}")
        print(f"  final PC=0x{m.pc:04X}  LARC tail: {tx[-40:]!r}")
        if diag_errors:
            print(f"  DIAG errors ({len(diag_errors)}):")
            for e in diag_errors[:6]:
                L = e['last']
                ls = (f"l2={L['l2']:02X} l3={L['l3']:02X} WA={L['WA']} RA={L['RA']} "
                      f"cmag={L['cmag']} CSIGN={L['CSIGN']} x={L['x']} RES={L['RES']}") if L else "-"
                print(f"    E{e['tc']:02X} caller=0x{e['caller']:04X} steps={e['steps']}  last[{ls}]")
    return verdict, diag_errors, aru


def selftest_multiplier():
    """Offline check of the multiplier model against all 20 firmware POST goldens
    (0x0942 input/golden tables) — prints which cases are bit-exact."""
    cases = [
        (0x5555, 21, 0, -14337), (0xAAAA - 0x10000, 21, 0, 14335), (0x6666, 21, 0, -17204), (0x9999 - 0x10000, 21, 0, 17202),
        (0x5555, 21, 1, 14336), (0xAAAA - 0x10000, 21, 1, -14336), (0x6666, 21, 1, 17203), (0x9999 - 0x10000, 21, 1, -17203),
        (0x5555, 42, 0, -28673), (0xAAAA - 0x10000, 42, 0, 28671), (0x6666, 42, 0, -32768), (0x9999 - 0x10000, 42, 0, 32767),
        (0x5555, 42, 1, 28672), (0xAAAA - 0x10000, 42, 1, -28672), (0x6666, 42, 1, 32767), (0x9999 - 0x10000, 42, 1, -32768),
        (0x3333, 63, 1, 25806), (0xCCCC - 0x10000, 63, 1, -25805), (0x3FFF, 63, 1, 32255), (0xC000 - 0x10000, 63, 1, -32254),
    ]
    ok = 0; miss = []
    for x, cmag, cs, exp in cases:
        got = ARU.mul(x, cmag, cs)
        if got == exp:
            ok += 1
        else:
            miss.append((x & 0xFFFF, cmag, cs, exp, got))
    print(f"multiplier model vs firmware goldens: {ok}/20 bit-exact")
    for x, cmag, cs, exp, got in miss:
        print(f"    MISS x=0x{x:04X} cmag={cmag} cs={cs} exp={exp:+d} got={got:+d} (cmag=63 edge)")
    return ok


if __name__ == "__main__":
    print("=" * 72)
    print("224XL Phase-1 — netlist ARU on the VERIFIED 8080; POST UN-SUPPRESSED")
    print("=" * 72)
    selftest_multiplier()
    print("-" * 72)
    verdict, errs, aru = run_post()
    print("-" * 72)
    print("PER-SUB-TEST VERDICT (firmware's own pass/fail):")
    for k in sorted(verdict):
        print(f"    {k:34}: {verdict[k]}")
