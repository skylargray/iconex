#!/usr/bin/env python3
"""D3 (plan 022) — SM §5.7 signature analysis: hardware-grade per-pin verification.

Stimulus = the firmware-built diag-3 (ARU SIGNAT) WCS, captured on the verified core
(wcs_diag.json["sig3"], byte-identical to tools/_diag3_wcs.bin). Analyzer = tools/sig224.py
(16-bit LFSR X^16+X^12+X^9+X^7+1, alphabet 0123456789ACFHPU — self-test re-run in-process).

T&C setup (SM §5.7): CLOCK = DAB RSTB/ (tc_U20.6) = ONE edge per hardware step, taken at the
step boundary (the DAB RSTB fall / RSTB/ rise, end of MS8); window = RESETD/-to-RESETD/ =
ONE FRAME. Under the 0023 frame model the diag-3 program is L=29 -> 30 hardware steps, so a
+5V (all-1) pin must read the manual's T&C reference "FP54" — which sig224 calibrates at
EXACTLY N=30. The manual's own reference signature encodes the L+1 frame length.

Per-pin DATA streams are generated from the netlist pin map (§3.1-3.11, §2T, §6T of
224XL_interconnect_netlist.md) + the 0023 pipeline alignment, sampled at the DAB RSTB/ edge
ending step n (setup-before):

  PC(b)     bit b of (n+1) mod F              (PC points at w_{n+1} during step n)
  F(k)      MI_k of the FETCHED word          (SRAM out at address PC = row n+1)
  S(k)      MI_k of w_n                       (stage-1/offset latch outputs, k=0..31;
                                               OFSTb/ = S(b), C-lines = S(26..31))
  stage-2   w_n's fields (tc_U19 loads in AS0 of step n)
  CSIGN/    MI23 of w_{n-1}                   (tc_U20 JK samples pre-load Q4)
  M0//M1/   ~MI26/~MI27 of w_{n-1}            (74195 /Q3 after the slot-6 P3=Q2 load = pairC)
  RESET/    constant 1 at the sample edge     (low only slots 0-6 of the post-reset step)
  RESETD/   0 exactly at the post-reset-step sample, else 1
  combs     tcWR = S16&~S17; MEMW/ = ~(S17&~S16); MEMR/ = ~(S17&S16); DP = tcWR&S4;
            RESET = tcWR&S3; WR DA/ = ~(tcWR&S7)   (DAB RSTB still high at the sample)

MI level = the PHYSICAL line = complement of the CPU-domain byte bit (Multibus data
complement, session 0022); row r = CPU word 127-r.

The one free constant is the global window phase (which step boundary RESETD/ starts the
window at) — scanned 0..F-1, shared by ALL pins; everything else is structure. Score =
match / mismatch / not-modeled per listed pin, mismatches named.
"""
import sys, os, json, re
from collections import defaultdict

TOOLS = r"d:\OneDrive\Gray Instruments\iconex\tools"
sys.path.insert(0, TOOLS)
HERE = os.path.dirname(os.path.abspath(__file__))
DOCS = os.path.join(os.path.dirname(TOOLS), "docs", "reference", "224")

import sig224
from aru_freerun22_rtl import program_rows22

# ---------------------------------------------------------------- D3a: analyzer self-test
print("### D3a: sig224 self-test (in-process) ###")
assert sig224._selftest(), "sig224 self-test FAILED"

# ---------------------------------------------------------------- the diag-3 frame
cache = json.load(open(os.path.join(HERE, "wcs_diag.json")))
img = bytes.fromhex(cache["sig3"]["wcs"])
old = open(os.path.join(TOOLS, "_diag3_wcs.bin"), "rb").read()
assert img == old, "sig3 capture != _diag3_wcs.bin"
wcs = [(img[4*k], img[4*k+1], img[4*k+2], img[4*k+3]) for k in range(128)]
rows, L, w_reset = program_rows22(wcs)
F = L + 1
print(f"\ndiag-3 frame: reset word {w_reset} -> L={L} -> F={F} hardware steps")
assert (w_reset, L, F) == (99, 29, 30), "diag-3 frame != 30 steps"

fp54 = sig224.value_to_display(sig224.signature_const(F, 1))
print(f"+5V over F={F} clocks -> '{fp54}' (manual T&C reference: FP54)")
assert fp54 == "FP54", "window length != the manual's reference signature"
print("*** the manual's own +5V reference signature CONFIRMS the L+1 frame (30 steps) ***")

# ---------------------------------------------------------------- physical bit streams
# cw(r) = CPU word of row r; MI_k(r) = complement of the CPU bit (physical line level)
def mi(r, k):
    l = wcs[127 - (r % F)][k // 8]
    return 1 - ((l >> (k % 8)) & 1)

r_reset = 127 - w_reset            # execution row index of the reset word (= L-1)
assert r_reset == L - 1

def S(k):      return [mi(n, k) for n in range(F)]                    # w_n field lines
def Fetch(k):  return [mi(n + 1, k) for n in range(F)]                # SRAM out @ PC
def PC(b):     return [((n + 1) % F >> b) & 1 for n in range(F)]
def CONST(v):  return [v] * F
def CSIGN():   return [mi(n - 1, 23) for n in range(F)]
def M0():      return [1 - mi(n - 1, 26) for n in range(F)]
def M1():      return [1 - mi(n - 1, 27) for n in range(F)]
def RCO14():   return [1 if ((n + 1) % F) & 15 == 15 else 0 for n in range(F)]
def AND(a, b): return [x & y for x, y in zip(a, b)]
def NOT(a):    return [1 - x for x in a]

TCWR   = AND(S(16), NOT(S(17)))
NTCWR  = NOT(TCWR)
MEMWN  = NOT(AND(S(17), NOT(S(16))))
MEMRN  = NOT(AND(S(17), S(16)))
DP     = AND(TCWR, S(4))
RESET  = AND(TCWR, S(3))
INVRES = NOT(RESET)
WRDAN  = NOT(AND(TCWR, S(7)))
INVQ4  = NOT(S(23))
RESETD = [0 if n == (r_reset + 1) % F else 1 for n in range(F)]
assert RESET == [1 if n == r_reset else 0 for n in range(F)], "reset comb != reset row"

# ---------------------------------------------------------------- netlist pin map
PM = {}
def put(u, pins, streams):
    for p, s in zip(pins, streams):
        PM[(u, p)] = s

for u, base in (("U43", 0), ("U29", 8), ("U15", 16), ("U2", 24)):     # WCS SRAMs (24-pin)
    put(u, range(2, 10), [("F", base + i) for i in range(8)])
    put(u, (23, 22, 21, 20, 19, 18, 17), [("PC", b) for b in range(7)])
    put(u, (16, 24), [("C", 1)] * 2)                                   # R/W=read, Vcc
    put(u, (1, 11, 12, 14, 15), [("C", 0)] * 5)                        # GND + /CS to GND
for u, base in (("U44", 0), ("U30", 8), ("U16", 16), ("U3", 24)):      # transceivers (20-pin)
    put(u, range(1, 9), [("F", base + i) for i in range(8)])
    put(u, (9, 11, 20), [("C", 1)] * 3)                                # CD, T/R, Vcc
    put(u, (10,), [("C", 0)])
for u, bs in (("U42", (0, 1, 2, 3)), ("U28", (4, 5, 6))):              # addr mux (16-pin)
    ys = {("U42", 0): 4, ("U42", 1): 7, ("U42", 2): 9, ("U42", 3): 12,
          ("U28", 4): 4, ("U28", 5): 7, ("U28", 6): 9}
    bpin = {0: 3, 1: 6, 2: 10, 3: 13, 4: 3, 5: 6, 6: 10}
    for b in bs:
        put(u, (bpin[b], ys[(u, b)]), [("PC", b)] * 2)
    put(u, (1, 16), [("C", 1)] * 2)
    put(u, (15, 8), [("C", 0)] * 2)
put("U14", (14, 13, 12, 11), [("PC", b) for b in range(4)])            # PC counters
put("U14", (7, 9, 10, 16), [("C", 1)] * 4)
put("U14", (8,), [("C", 0)])
put("U14", (15,), [("RCO",)])
put("U14", (1,), [("INVRES",)])
put("U1", (14, 13, 12), [("PC", b) for b in (4, 5, 6)])
put("U1", (7, 9, 16), [("C", 1)] * 3)
put("U1", (8,), [("C", 0)])
put("U1", (10,), [("RCO",)])
put("U1", (1,), [("INVRES",)])
for u, add in (("U45", 0), ("U31", 8)):                                # offset latches (20-pin)
    for dpin, qpin, bit in ((3, 2, 1), (4, 5, 3), (7, 6, 5), (8, 9, 7),
                            (13, 12, 6), (14, 15, 4), (17, 16, 2), (18, 19, 0)):
        PM[(u, dpin)] = ("F", bit + add)
        PM[(u, qpin)] = ("S", bit + add)
    put(u, (1, 10), [("C", 0)] * 2)
    put(u, (20,), [("C", 1)])
for u, base in (("U17", 16), ("U18", 20), ("U4", 24), ("U5", 28)):     # stage-1 regs (16-pin)
    put(u, (3, 4, 5, 6), [("F", base + i) for i in range(4)])
    put(u, (14, 13, 12, 11), [("S", base + i) for i in range(4)])
    put(u, (1, 16), [("C", 1)] * 2)
    put(u, (7, 9, 10, 8), [("C", 0)] * 4)
put("U19", (3, 2), [("DP",)] * 2)                                      # stage-2 (20-pin)
put("U19", (4, 5), [("S", 20)] * 2)
put("U19", (7, 6), [("S", 21)] * 2)
put("U19", (8,), [("C", 1)])                                           # RESET/ @ sample
put("U19", (9,), [("RESETD",)])
put("U19", (13, 12), [("S", 23)] * 2)
put("U19", (14, 15), [("S", 24)] * 2)
put("U19", (17, 16), [("S", 25)] * 2)
put("U19", (18, 19), [("C", 1)] * 2)                                   # n/c floats high
put("U19", (10,), [("C", 0)])
put("U19", (20,), [("C", 1)])
put("U20", (9,), [("CSIGN",)])                                         # CSIGN JK (16-pin)
put("U20", (10, 14, 16), [("C", 1)] * 3)
put("U20", (8,), [("C", 0)])
put("U10", (4, 5, 6, 7, 13), [("S", 27), ("S", 29), ("S", 31), ("S", 31), ("S", 31)])
put("U10", (11,), [("M1",)])                                           # serializers (16-pin)
put("U10", (1, 16), [("C", 1)] * 2)
put("U10", (8,), [("C", 0)])
put("U11", (4, 5, 6, 7, 13), [("S", 26), ("S", 28), ("S", 30), ("S", 30), ("S", 30)])
put("U11", (11,), [("M0",)])
put("U11", (1, 16), [("C", 1)] * 2)
put("U11", (8,), [("C", 0)])
put("U46", (1, 2, 14, 4, 5, 6, 7, 9, 10, 11, 12, 16), [("C", 1)] * 12)  # R/W decode idle
put("U46", (8,), [("C", 0)])
put("U47", (1, 8), [("C", 0)] * 2)                                     # device decode
put("U47", (2,), [("S", 16)])
put("U47", (3,), [("S", 17)])
put("U47", (5,), [("NTCWR",)])
put("U47", (6,), [("MEMWN",)])
put("U47", (7,), [("MEMRN",)])
put("U47", (14,), [("S", 12)])
put("U47", (13,), [("S", 13)])
put("U47", (16,), [("C", 1)])
put("U48", (1,), [("MEMWN",)])
put("U48", (4,), [("TCWR",)])
put("U48", (12,), [("S", 25)])
put("U48", (7,), [("C", 0)])
put("U48", (14,), [("C", 1)])
put("U49", (2, 4, 11), [("TCWR",)] * 3)
put("U49", (13,), [("S", 6)])
put("U49", (3,), [("S", 5)])
put("U49", (9,), [("S", 7)])
put("U49", (10, 14), [("C", 1)] * 2)
put("U49", (8,), [("WRDAN",)])
put("U49", (7,), [("C", 0)])
put("U32", (1, 2, 3), [("S", 8)] * 3)                                  # SDA buffers
put("U32", (4, 5, 6), [("S", 10)] * 3)
put("U32", (9, 10, 8), [("S", 11)] * 3)
put("U32", (12, 13, 11), [("S", 9)] * 3)
put("U32", (7,), [("C", 0)])
put("U32", (14,), [("C", 1)])
put("U33", (3,), [("NTCWR",)])
put("U33", (4,), [("TCWR",)])
put("U33", (7,), [("C", 0)])
put("U33", (14,), [("C", 1)])
put("U34", (1, 4), [("TCWR",)] * 2)
put("U34", (2,), [("S", 4)])
put("U34", (3,), [("DP",)])
put("U34", (5,), [("S", 3)])
put("U34", (6,), [("RESET",)])
put("U34", (13,), [("S", 23)])
put("U34", (10,), [("INVQ4",)])   # trace says pin10=AS0 (const 0 @sample); table decides —
put("U34", (7,), [("C", 0)])      # if INVQ4 matches, §2T.5 g3's input pins 9/10 are swapped
put("U34", (14,), [("C", 1)])

STREAMS = {"F": Fetch, "S": S, "PC": PC, "C": CONST}
SPECIAL = {"CSIGN": CSIGN, "M0": M0, "M1": M1, "RCO": RCO14,
           "DP": lambda: DP, "RESET": lambda: RESET, "INVRES": lambda: INVRES,
           "RESETD": lambda: RESETD, "TCWR": lambda: TCWR, "NTCWR": lambda: NTCWR,
           "MEMWN": lambda: MEMWN, "MEMRN": lambda: MEMRN, "WRDAN": lambda: WRDAN,
           "INVQ4": lambda: INVQ4}

def stream_of(spec):
    kind = spec[0]
    if kind in STREAMS:
        return STREAMS[kind](*spec[1:])
    return SPECIAL[kind]()

# ---------------------------------------------------------------- parse the SM table
txt = open(os.path.join(DOCS, "224-signature-value-tables.md"), encoding="utf-8").read()
m = re.search(r"#### T&C Module.*?```(.*?)```", txt, re.S)
assert m, "T&C table block not found"
table = {}
sides = [None, None]                       # current chip per column side
for line in m.group(1).splitlines():
    for side, seg in enumerate((line[:31], line[31:])):
        toks = seg.split()
        i = 0
        while i < len(toks):
            t = toks[i]
            if re.fullmatch(r"U\d+", t):
                sides[side] = t
                i += 1
            else:
                pin, sig = toks[i], toks[i + 1]
                if sig != "-" and sides[side]:
                    table[(sides[side], int(pin))] = sig
                i += 2
print(f"\nparsed T&C table: {len(table)} listed (chip,pin) signatures, "
      f"{len({c for c, _ in table})} chips")

# ---------------------------------------------------------------- score with window scan
def sig_disp(bits, rot):
    return sig224.value_to_display(
        sig224.sig_value(bits[rot:] + bits[:rot]))

candidates = {k: stream_of(v) for k, v in PM.items() if k in table}
not_modeled = sorted(k for k in table if k not in PM)

best = None
for rot in range(F):
    n_ok = sum(1 for k, bits in candidates.items()
               if sig_disp(bits, rot) == table[k])
    if best is None or n_ok > best[1]:
        best = (rot, n_ok)
rot, n_ok = best
print(f"window-phase scan: best start = sample index {rot} "
      f"(reset row = {r_reset}) -> {n_ok}/{len(candidates)} modeled pins match")

match, mismatch = [], []
for k in sorted(candidates, key=lambda x: (int(x[0][1:]), x[1])):
    got = sig_disp(candidates[k], rot)
    (match if got == table[k] else mismatch).append((k, table[k], got))

print(f"\n### D3c score (T&C table, diag-3 stimulus) ###")
print(f"  MATCH       : {len(match)}")
print(f"  MISMATCH    : {len(mismatch)}")
print(f"  not modeled : {len(not_modeled)}  {['%s.%d' % k for k in not_modeled]}")
if mismatch:
    print("\n  mismatches (each names its net — the per-pin falsifiers):")
    for (u, p), want, got in mismatch:
        print(f"    {u}.{p}: table {want} model {got}   spec={PM[(u, p)]}")

# distinct-net coverage: how many distinct signature VALUES did the model reproduce?
vals_ok = {want for (_, want, _) in match}
vals_all = set(table.values())
print(f"\n  distinct signature values matched: {len(vals_ok)}/{len(vals_all)}")
print("\nD3c: " + ("ALL MODELED PINS MATCH — the T&C control pipeline is signature-exact"
                   if not mismatch else
                   f"{len(mismatch)} named findings to investigate (top-down: clock/window first)"))
