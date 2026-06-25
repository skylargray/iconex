#!/usr/bin/env python3
"""Gate-level ARU datapath (060-01318), built from the netlist pinout. Models the
serial multiply (dual-rank shift register + 2-bit/state NAND-add → partial-product
register U10-12 @ARUCK), the negative-logic accumulate (CSIGN XOR U5-9 → 74F283
adder U19-23 → 74F157 saturation muxes U33-37 → PP bus → accumulator U45-49
@ARUCKE/), and the result register U43/44 @XFER-CK = PP[3..18].

Per-ARUCK PP/AC bus values are exposed for the §5.7 signature oracle. Decode and
the register-file preload (R[0..3]=AAAA,9999,C787,607F, firmware-determined) are
FIXED — only the genuine sub-cycle timing ambiguities (PP-register pipeline phase,
which ARU-state XFER/ZERO fire, the RES→register feedback phase, the sample edge,
and the window alignment) are calibrated against §5.7, since the netlist pins the
arithmetic but the figures leave the exact ARUCK phase open.
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import aru_datapath as A
import sig224

ACC_MAX, ACC_MIN = (1 << 18) - 1, -(1 << 18)     # 20-bit sat rails ±2^18


def sat20(v):
    return ACC_MAX if v > ACC_MAX else (ACC_MIN if v < ACC_MIN else v)


def serial_partials(F, cmag):
    """[PP0,PP1,PP2] of the dual-rank shift-add multiply (straight-binary, validated
    so Sum = (x<<3)*cmag>>5; per-state grouping per Fig 3.4 with M0=direct/M1=shift)."""
    b = [(cmag >> i) & 1 for i in range(6)]
    return [b[5] * F + b[4] * (F >> 1),
            b[3] * (F >> 2) + b[2] * (F >> 3),
            b[1] * (F >> 4) + b[0] * (F >> 5)]


def check_addl_mult():
    """RES = x*cmag/32, allowing the serial shift-add's ±1 LSB truncation on negatives."""
    ok = True
    for cmag, ratio in [(32, 1.0), (16, 0.5), (8, 0.25), (40, 1.25)]:
        for x in (1000, -1000, 5000, -5000, 100, -100):   # no overflow for x1.25
            res = max(-32768, min(32767, sum(serial_partials(x << 3, cmag)) >> 3))
            if abs(res - x * ratio) > 1.5:
                ok = False
    return ok


# §5.7 ARU feedback targets (AC bus = U45-49 Q; PP bus = their D inputs).
AC_TARGET = {0: "34P3", 1: "09U9", 2: "60CU", 3: "5CP3", 4: "011F", 5: "6A06",
             6: "4815", 7: "4062", 8: "CA59", 9: "8U4F", 10: "0H92", 11: "2999",
             12: "1126", 13: "2U18", 14: "4U40", 15: "1918", 16: "P1UC",
             17: "P1UC", 18: "4FF8", 19: "8PH4"}
PP_TARGET = {0: "P885", 1: "2A6H", 2: "9AHU", 3: "F5F1", 4: "9136", 5: "U9U0",
             6: "P978", 7: "U05P", 8: "PC02", 9: "PHPA", 10: "P9PA", 11: "12UF",
             12: "CHHP", 13: "4110", 14: "C5P9", 15: "5062", 16: "0HHH",
             17: "666C", 18: "77A3", 19: "77A3"}

PRELOAD = [0xAAAA - 0x10000, 0x9999 - 0x10000, 0xC787 - 0x10000, 0x607F]


def run(prog, loops, *, xfer_state=0, res_fb='pre', samp='post', mask=0xFFFF):
    """Gate-level run of `prog` (one microinstruction/cycle, 3 ARU states each).
    res_fb: 'pre'  -> a step's dab=RES uses RES before this step's XFER (held value)
            'post' -> uses RES after this step's XFER.
    Returns per-ARUCK (AC bus, PP bus) lists (20-bit)."""
    R = list(PRELOAD); DM = [0] * (mask + 1); RES = 0
    ACC = 0; PPreg = 0; csreg = 0
    xfer_p = zero_p = 0; pos = 0
    ac = []; pp = []
    for _ in range(loops):
        pos = (pos + 1) & mask
        for st in prog:
            addr = (pos - st['offset']) & mask
            is_sub = st['MI17'] == 0 and st['MI16'] == 1
            # --- datapath: DAB source (pre-XFER RES) ---
            if is_sub and st['sub'] == 2:   dab = 0x607F           # RD XREG/ seed
            elif is_sub and st['sub'] == 1: dab = RES
            elif st['MI17'] == 1 and st['MI16'] == 1: dab = DM[addr]
            elif st['MI17'] == 1 and st['MI16'] == 0: dab = RES
            else: dab = 0
            x = R[st['RA']]
            if res_fb == 'pre':
                R[st['WA']] = dab
            pps = serial_partials(x << 3, abs(st['cs']))
            csign = 1 if st['cs'] < 0 else 0
            # --- 3 ARU states: PP register pipelines into the saturating accumulator ---
            for si in range(3):
                add = -PPreg if csreg else PPreg
                ppbus = sat20(ACC + add)            # 74F283 + 74F157 sat-mux output
                ACC = ppbus                         # accumulator latches @ARUCKE/
                if si == xfer_state:
                    if xfer_p:
                        RES = max(-32768, min(32767, ACC >> 3))
                    if zero_p:
                        ACC = 0
                PPreg, csreg = pps[si], csign       # PP register latches @ARUCK
                ac.append(ACC & 0xFFFFF)
                pp.append(ppbus & 0xFFFFF)
            if res_fb == 'post':
                R[st['WA']] = dab if not (st['MI17'] == 1 and st['MI16'] == 0
                                          or (is_sub and st['sub'] == 1)) else RES
            if st['MI17'] == 1 and st['MI16'] == 0:
                DM[addr] = RES
            xfer_p, zero_p = st['XFER'], st['ZERO']
    return ac, pp


def _bsig(samples, bit, start, n):
    return sig224.value_to_display(
        sig224.sig_value(((samples[(start + i) % len(samples)] >> bit) & 1) for i in range(n)))


def sweep(prog, n=90):
    L = len(prog) * 3; base = 70 * L
    best = (0, None)
    for xs in (0, 1, 2):
        for fb in ('pre', 'post'):
            ac, pp = run(prog, 80, xfer_state=xs, res_fb=fb)
            for off in range(L):
                acm = sum(1 for b in range(20) if _bsig(ac, b, base + off, n) == AC_TARGET[b])
                ppm = sum(1 for b in range(20) if _bsig(pp, b, base + off, n) == PP_TARGET[b])
                if acm + ppm > best[0]:
                    best = (acm + ppm, dict(xfer_state=xs, res_fb=fb, off=off, ac=acm, pp=ppm))
    return best


if __name__ == '__main__':
    import diag3
    print("ADD'L MULT (gate-level multiply):", "PASS" if check_addl_mult() else "FAIL")
    prog = A.decode_image(diag3.load_wcs())
    score, cfg = sweep(prog)
    print(f"best §5.7 AC+PP match: {score}/40  cfg={cfg}")
