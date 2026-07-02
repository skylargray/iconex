#!/usr/bin/env python3
"""F2a (plan 024) — the DMEM §5.7 signature table: per-pin verification of the DMEM
address path (CPC counters + offset adders + row/col muxes + DRAM address bus) against
the manufacturer's table, under the SM's LIFT-JUMPER setup.

SM setup (ch.5): diag-3 running; "Lift U65 pin 13 and jumper to U65 pin 1";
START = STOP = U65.8 ("MSB of CPC"); CLOCK = RESET/ (U58A pin 1); +5V ref = 826P.

THE WINDOW-LENGTH DERIVATION (declared BEFORE scoring — the plan's built-in falsifier):
  Netlist §5.1: CPC = dmem_U51 (bits 0-7) + dmem_U65 (bits 8-15), 74LS393 ripple pairs,
  clocked once per frame (dmemRESET fall = RESET/ rise); U65's normal internal cascade is
  pin13 (2CP) <- pin6 (1QD = cpc11, falls every 4096 frames).
  The lift-jumper moves U65 pin13 onto the PIN-1 NET = cpc7 (U51.pin8), which falls every
  256 frames -> the high nibble now counts 16x faster: modified cpc12..15 MIRROR cpc8..11
  (same clock, same ripple, common clear), and U65.8 (2QD) = f[11] with period
  16 x 256 = 4096 frames — NOT the naive 65536/2.
  Window = one full period of the START signal (the E1b convention) = N = 4096 frames
  == sig224's calibration of the manual's +5V reference 826P. RECONCILED.
  (Why the SM rewires the counter at all: every sampled stream must be periodic IN the
  window for a stable signature; the unmodified 65536-frame MSB would leave the high
  address bits aperiodic over any shorter window.)

Sampling instant (pinned by the table's own constants, verified in the scan):
  CLOCK = RESET/ rising edge = the CPC bump instant (~MS6 of the post-reset row's step,
  row 29). At that instant: ROW SEL is LOW (fig-3.3: low MS3-7) -> the U18/U36 muxes
  select the A side = COLUMN = A8..A15 onto AD0..7 (the table's U18/U36 pin-1 = 0000
  agrees); the live stage-1/offset word is ROW 29 (the table's adder B-pin constants
  show OFST6/ and OFST12/ HIGH = stored bits 6/12 = 0 = WRX asserted + sel=1 — row 29's
  IO command word, NOT the reset word).

Streams (all pure functions of the frame index; no ARU state is listed in this table):
  cpc0-7 = f[0:8]; cpc8-11 = f[8:12]; cpc12-15 = f[8:12] (the lift-jumper mirror);
  adder A-pins = cpc nets; B-pins = OFST/ line constants (= ~stored l0l1 of row 29);
  Sigma = (CPC_mod + Bline + 1) & 0xFFFF (carry-in tied high); per-nibble carries;
  AD0..7 = A8..15 (column side); U17 = the 33R series pack (pin n <-> pin 17-n pairs);
  U48/U62 read-back buffers disabled (DPORT enables high; Y pins unlisted).

Every mismatch names its net; single-glyph errata need a same-net sister pin (rule §8).
"""
import sys, os, json, re

TOOLS = r"d:\OneDrive\Gray Instruments\iconex\tools"
sys.path.insert(0, TOOLS)
HERE = os.path.dirname(os.path.abspath(__file__))
DOCS = os.path.join(os.path.dirname(TOOLS), "docs", "reference", "224")

import sig224

N = 4096
F_START = 2048          # U65.8 = f[11] rises when f mod 4096 reaches 2048 (CLR-at-0 count)

# ---------------------------------------------------------------- self-test + stimulus
assert sig224._selftest(), "sig224 self-test FAILED"
ref_826p = sig224.value_to_display(sig224.signature_const(N, 1))
print(f"\nPREDICTION: lift-jumper CPC-MSB period = 16 x 256 = {N} frames; "
      f"+5V over N={N} -> '{ref_826p}' (manual: 826P)")
assert ref_826p == "826P", "window-length prediction FAILED - do not score"
print("*** window length RECONCILED before scoring ***\n")

cache = json.load(open(os.path.join(HERE, "wcs_diag.json")))
img = bytes.fromhex(cache["sig3"]["wcs"])
w29_l0, w29_l1 = img[4 * 98 + 0], img[4 * 98 + 1]      # row 29 = CPU word 127-29 = 98
w28_l0, w28_l1 = img[4 * 99 + 0], img[4 * 99 + 1]      # row 28 = the reset word (99)
BLINE = {29: (~((w29_l1 << 8) | w29_l0)) & 0xFFFF,
         28: (~((w28_l1 << 8) | w28_l0)) & 0xFFFF}
print(f"row-29 stored l1l0 = 0x{w29_l1:02X}{w29_l0:02X} -> OFST/ lines = 0x{BLINE[29]:04X}; "
      f"row-28 (reset) -> 0x{BLINE[28]:04X}")


def cpc_mod(f):
    """The lift-jumper CPC: low byte normal, high byte = f[8:12] duplicated."""
    lo = f & 0xFF
    mid = (f >> 8) & 0xF
    return lo | (mid << 8) | (mid << 12)


def build_streams(bline, delta):
    """All listed nets as 4096-bit streams over the window (g = 0..4095; sampled CPC =
    cpc_mod(F_START + g + delta) — delta scans the pre/post-bump race)."""
    cpc = [cpc_mod(F_START + g + delta) for g in range(N)]
    sig = [(c + bline + 1) & 0xFFFF for c in cpc]
    S = {}
    for b in range(16):
        S[f"CPC{b}"] = [(c >> b) & 1 for c in cpc]
        S[f"A{b}"] = [(s >> b) & 1 for s in sig]
        S[f"B{b}"] = [(bline >> b) & 1] * N
    for k in range(1, 5):
        mask = (1 << (4 * k)) - 1
        S[f"COUT{k}"] = [(((c & mask) + (bline & mask) + 1) >> (4 * k)) & 1 for c in cpc]
    for i in range(8):
        S[f"AD{i}"] = S[f"A{8 + i}"]                    # ROW SEL low -> column side
    S["C0"] = [0] * N
    S["C1"] = [1] * N
    return S


# ---------------------------------------------------------------- the pin map (netlist §5)
def build_pinmap():
    PM = {}
    def put(u, p, s):
        PM[(u, p)] = s

    # U51/U65 74LS393 CPC (§5.1). U65 pins 1/13 share the cpc7 net (the LIFT-JUMPER);
    # MR pins parked low (CPC CLR idle); CP=dmemRESET is the analyzer clock (pin1 of U51
    # unlisted); GND/Vcc.
    for p, s in ((3, "CPC0"), (4, "CPC1"), (5, "CPC2"), (6, "CPC3"),
                 (11, "CPC4"), (10, "CPC5"), (9, "CPC6"), (8, "CPC7"),
                 (13, "CPC3"),                            # 2CP = internal cascade = cpc3
                 (2, "C0"), (12, "C0"), (7, "C0"), (14, "C1")):
        put("U51", p, s)
    for p, s in ((1, "CPC7"),                             # 1CP <- U51.8 (cpc7 net)
                 (3, "CPC8"), (4, "CPC9"), (5, "CPC10"), (6, "CPC11"),
                 (11, "CPC12"), (10, "CPC13"), (9, "CPC14"), (8, "CPC15"),
                 (13, "CPC7"),                            # LIFTED, jumpered to pin 1's net
                 (2, "C0"), (12, "C0"), (7, "C0"), (14, "C1")):
        put("U65", p, s)

    # offset adders U49/U50/U63/U64 (74283 pins: B0=6 B1=2 B2=15 B3=11; A0=5 A1=3 A2=14
    # A3=12; S0=4 S1=1 S2=13 S3=10; C0=7 C4=9), §5.2. U64.C4 output floats unconnected
    # but still drives the full-sum carry.
    for k, u in enumerate(("U49", "U50", "U63", "U64")):
        base = 4 * k
        for i, p in enumerate((5, 3, 14, 12)):
            put(u, p, f"CPC{base + i}")
        for i, p in enumerate((6, 2, 15, 11)):
            put(u, p, f"B{base + i}")
        for i, p in enumerate((4, 1, 13, 10)):
            put(u, p, f"A{base + i}")
        put(u, 7, "C1" if k == 0 else f"COUT{k}")
        put(u, 9, f"COUT{k + 1}")
        put(u, 8, "C0")
        put(u, 16, "C1")

    # row/col muxes U36 (low AD) / U18 (high AD), 74157 (§5.3/5.4): SEL low = A side.
    mux = {"U36": [(2, "A8"), (3, "A0"), (4, "AD0"), (5, "A9"), (6, "A1"), (7, "AD1"),
                   (11, "A10"), (10, "A2"), (9, "AD2"), (14, "A11"), (13, "A3"), (12, "AD3")],
           "U18": [(2, "A12"), (3, "A4"), (4, "AD4"), (5, "A13"), (6, "A5"), (7, "AD5"),
                   (11, "A14"), (10, "A6"), (9, "AD6"), (14, "A15"), (13, "A7"), (12, "AD7")]}
    for u, pins in mux.items():
        for p, s in pins:
            put(u, p, s)
        put(u, 1, "C0")            # SEL = ROW SEL, LOW at the sample instant
        put(u, 15, "C0")           # G\ = GND
        put(u, 8, "C0")
        put(u, 16, "C1")

    # U17 = the 33R series pack on AD0..6 (pin n <-> pin 17-n; assignment read off the
    # DRAM-side listing: AD0=UH56 pair(4,13), AD1=861U (8,9), AD2=P279 (6,11),
    # AD3=A6F7 (3,14), AD4=FU8U (5,12), AD5=44U7 (7,10), AD6=0AU1 (2,15)).
    for (pa, pb), ad in (((4, 13), 0), ((8, 9), 1), ((6, 11), 2), ((3, 14), 3),
                         ((5, 12), 4), ((7, 10), 5), ((2, 15), 6)):
        put("U17", pa, f"AD{ad}")
        put("U17", pb, f"AD{ad}")

    # the DRAM array common pattern (U1-16 unpopulated + U20-35; pseudo-chip U999):
    # 4164 address pins 5(A0) 7(A1) 6(A2) 12(A3) 11(A4) 10(A5) 13(A6) <- AD0..6; 16=VSS.
    for p, s in ((5, "AD0"), (7, "AD1"), (6, "AD2"), (12, "AD3"),
                 (11, "AD4"), (10, "AD5"), (13, "AD6"), (16, "C0")):
        put("U999", p, s)

    # offset read-back buffers U48 (OFST0-7/) / U62 (OFST8-15/), 74LS244 (§5.7):
    # A pins carry the OFST/ constants; Y pins tri-stated (enables = DPORT0/1/ idle HIGH).
    ls244_a = {2: 0, 4: 1, 6: 2, 8: 3, 11: 4, 13: 5, 15: 6, 17: 7}
    for u, base in (("U48", 0), ("U62", 8)):
        # §5.7 per-line map: U48 A-order OFST 6,1,2,3,4,5,0,7; U62: 11,10,9,14,15,8,13,12
        order = ((6, 1, 2, 3, 4, 5, 0, 7) if u == "U48" else
                 (11, 10, 9, 14, 15, 8, 13, 12))
        for (pin, slot), off in zip(sorted(ls244_a.items()), order):
            put(u, pin, f"B{off}")
        put(u, 1, "C1")            # DPORT enable deasserted (reads +5V ref)
        put(u, 19, "C1")
        put(u, 10, "C0")
        put(u, 20, "C1")
    return PM


# ---------------------------------------------------------------- parse the table
def parse_dmem_table():
    txt = open(os.path.join(DOCS, "224-signature-value-tables.md"), encoding="utf-8").read()
    m = re.search(r"#### DMEM Module.*?```(.*?)```", txt, re.S)
    assert m, "DMEM table block not found"
    body = m.group(1)
    body = body.replace("U1–U16,", "U999   ").replace("U20–U35", "       ")
    body = body.replace("(common)", "        ")
    table = {}
    sides = [None, None]
    split_at = 31
    for line in body.splitlines():
        # the two column halves are fixed-width per block, but the DRAM-common block is
        # wider than the rest: re-anchor the split at each line carrying TWO designators
        desigs = [mm.start() for mm in re.finditer(r"\bU\d+\b", line)]
        if len(desigs) >= 2:
            split_at = desigs[1] - 1
        for side, seg in enumerate((line[:split_at], line[split_at:])):
            toks = seg.split()
            i = 0
            while i < len(toks):
                t = toks[i]
                if re.fullmatch(r"U\d+", t):
                    sides[side] = t
                    i += 1
                elif not t.isdigit():
                    i += 1
                else:
                    if i + 1 >= len(toks):
                        break
                    pin, sg = toks[i], toks[i + 1]
                    if sg != "-" and sides[side]:
                        table[(sides[side], int(pin))] = sg
                    i += 2
    return table


def main():
    table = parse_dmem_table()
    print(f"parsed DMEM table: {len(table)} listed (chip,pin) signatures "
          f"({len({c for c, _ in table})} chips incl. the DRAM-common pseudo-chip U999)")
    PM = build_pinmap()
    listed_mapped = [k for k in table if k in PM]
    print(f"pin map: {len(PM)} pins built; {len(listed_mapped)}/{len(table)} listed pins mapped")
    unmapped = sorted(k for k in table if k not in PM)
    if unmapped:
        print(f"  not modeled: {['%s.%d' % k for k in unmapped]}")

    def sig_of(bits, rot):
        seq = bits[rot % N:] + bits[:rot % N]
        return sig224.value_to_display(sig224.sig_value(seq))

    best = None
    for live_row in (29, 28):
        for delta in (0, -1):
            S = build_streams(BLINE[live_row], delta)
            for rot in (-2, -1, 0, 1, 2):
                tot = sum(1 for k in listed_mapped
                          if sig_of(S[PM[k]], rot) == table[k])
                cand = (tot, live_row, delta, rot)
                if best is None or tot > best[0]:
                    best = cand
                print(f"  live-row={live_row} delta={delta:+d} rot={rot:+d}: "
                      f"{tot}/{len(listed_mapped)}")

    tot, live_row, delta, rot = best
    S = build_streams(BLINE[live_row], delta)
    print(f"\n### CHAMPION: live-row={live_row} delta={delta:+d} rot={rot:+d} "
          f"-> {tot}/{len(listed_mapped)} ###")
    mismatches = [(k, table[k], sig_of(S[PM[k]], rot), PM[k])
                  for k in sorted(listed_mapped, key=lambda x: (int(x[0][1:]), x[1]))
                  if sig_of(S[PM[k]], rot) != table[k]]
    for (u, p), want, got, s in mismatches:
        print(f"  MISMATCH {u}.{p}: table {want} vs model {got}  [net {s}]")
        sisters = [(u2, p2) for (u2, p2), s2 in PM.items()
                   if s2 == s and (u2, p2) != (u, p) and (u2, p2) in table]
        for u2, p2 in sisters:
            print(f"    same-net sister {u2}.{p2}: table {table[(u2, p2)]} "
                  f"vs model {sig_of(S[PM[(u2, p2)]], rot)}")
    if not mismatches:
        print("  ALL MODELED PINS MATCH")
    print(f"\nverdict: the DMEM address path is signature-{'exact' if not mismatches else 'checked'} "
          f"under the derived lift-jumper window (N={N}); a window/convention failure here "
          f"would re-open the §5.1/§5.2 CPC/adder trace.")


if __name__ == "__main__":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass
    main()
