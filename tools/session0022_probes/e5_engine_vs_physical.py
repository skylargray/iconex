#!/usr/bin/env python3
"""E5 (plan 023) — differential: RTL22 (CPU-domain value engine) vs the PHYSICAL
complement-domain datapath locked by the E1c signature co-sim (1467/1469 pins).

The physical law (E1c champion): DAB carries ~value; PR = comb_array(SR(~x)); back-end
B = PR ^ rail, rail = cs (i.e. inv(CSIGN/)), cin = inv(rail); ACC <- sat-mux(sum);
capture RES = PP3..18 bits by pure truncation; CPU-domain readback = ~RES.

RTL22's value model: product20 terms + res_from_acc((ACC+ppC+4)>>3 sat16). The E83
goldens match both; the question is whether they are bit-identical for ALL programs
(esp. captures of negative/odd-group MACs the goldens never exercised).

Method: random programs (random cmag/csign/XFER/ZERO structure, MEMR/MEMW/IO mix,
random audio) run through both; compare every WR-DA output value. Any divergence is
characterized (engine erratum candidate for the re-sync).
"""
import sys, os, random

TOOLS = r"d:\OneDrive\Gray Instruments\iconex\tools"
sys.path.insert(0, TOOLS)
HERE = os.path.dirname(os.path.abspath(__file__))

import aru_booth as B
from aru_freerun22_rtl import RTL22, decode_word
from aru_freerun22 import (enc_memr, enc_memw, enc_idle, enc_io,
                           SRC_NONE, SRC_RDRREG, SRC_XREG, SRC_RDAD)

MASK20 = 0xFFFFF


def s16(v):
    v &= 0xFFFF
    return v - 0x10000 if v & 0x8000 else v


def raw_phases(opnd_phys, cmag):
    C = [(cmag >> i) & 1 for i in range(6)]
    SR = B.load_SR(s16(opnd_phys))
    out = []
    for p, (m0, m1) in enumerate([(C[4], C[5]), (C[2], C[3]), (C[0], C[1])]):
        if p > 0:
            SR = B.shift_right2(SR)
        out.append(B.comb_array(SR, m0, m1))
    return out


class Phys:
    """Minimal physical-domain MAC/bus walk (E1c-locked semantics, no pin emission)."""

    def __init__(self):
        self.R = [0xFFFF] * 4            # phys ~0
        self.ACC = 0
        self.RES = 0
        self.dab = 0xFFFF
        self.DM = {}
        self.CPC = 0
        self.wp = None
        self.pipe = None                 # (rawB, rawC, cs) of w_{n-2}

    def backend(self, acc, raw, cs):
        rail = cs
        cin = 1 - rail
        xorb = raw ^ (MASK20 if rail else 0)
        ssum = (acc + xorb + cin) & MASK20
        sat = ((ssum >> 19) ^ (ssum >> 18)) & 1
        if sat:
            topb = (xorb >> 19) & 1
            pp = (topb << 19) | (topb << 18) | (0x3FFFF if not topb else 0)
        else:
            pp = ssum
        return pp

    def step(self, d, x_phys):
        wp = self.wp
        if wp is not None:
            opnd = self.R[wp["RA"]]
            ph = raw_phases(opnd, wp["cmag"])
        else:
            ph = raw_phases(0, 0)
        p2 = self.pipe or (ph[1] * 0, ph[2] * 0, 1)
        rawB2, rawC2, cs2 = (p2 if isinstance(p2, tuple) else p2)

        sum0 = self.backend(self.ACC, rawB2, cs2)
        sum1 = self.backend(sum0, rawC2, cs2)
        if wp is not None and wp["XFER"]:
            self.RES = (sum1 >> 3) & 0xFFFF
        acc4 = 0 if (wp is not None and wp["ZERO"]) else sum1
        csn = wp["cs"] if wp is not None else 1
        sum2 = self.backend(acc4, ph[0], csn)

        typ = d["typ"]
        addr = (self.CPC - d["ofst"]) & 0xFFFF
        out = []
        if typ == 0:
            self.dab = self.DM.get(addr, 0xFFFF)     # unwritten DRAM -> phys ~0
        elif typ == 1:
            self.dab = self.RES
            self.DM[addr] = self.dab
        elif typ == 2:
            sel = d["sel"]
            if sel == SRC_RDRREG:
                self.dab = self.RES
            elif sel == SRC_RDAD:
                self.dab = (~x_phys) & 0xFFFF        # A/D drives the complement
            elif sel == SRC_XREG:
                self.dab = 0xFFFF                    # host latch ~0 in free-run
            if d.get("WRDA"):
                out = [(c, s16((~self.dab) & 0xFFFF)) for c in d["chans"]]
        self.R[d["WA"]] = self.dab
        self.ACC = sum2
        if wp is not None:
            self.pipe = (ph[1], ph[2], wp["cs"])
        self.wp = d
        return out

    def run_sample(self, rows, x):
        outs = []
        for d in rows:
            outs.extend(self.step(d, x))
        self.CPC = (self.CPC + 1) & 0xFFFF
        return outs


def compare_program(words, inputs, tag):
    rows = [decode_word(w) for w in words]
    eng = RTL22()
    phy = Phys()
    ndiff = 0
    first = None
    for n, x in enumerate(inputs):
        oe = dict(eng.run_sample(rows, x & 0xFFFF))
        op = dict(phy.run_sample(rows, x & 0xFFFF))
        if oe != op:
            ndiff += 1
            if first is None:
                first = (n, oe, op)
    print(f"[{tag}] {len(inputs)} frames: {ndiff} differing frames"
          + (f"; first at n={first[0]}: engine={first[1]} phys={first[2]}"
             if first else "  — BIT-IDENTICAL"))
    return ndiff


def main():
    rnd = random.Random(27)
    total = 0

    # 1. the passthrough (unity, positive)
    words = [
        enc_io(sel=SRC_RDAD, wa=1, cmag=0, zero=1, csign=0),
        enc_idle(ra=1, cmag=32, csign=1),
        enc_idle(xfer=1),
        enc_io(sel=SRC_RDRREG, wrda=True, chans="A", reset=True),
    ]
    xs = [1000, -2000, 12345, -30000, 0, 7, 16383, -16384]
    total += compare_program(words, xs, "passthrough")

    # 2. lone NEGATIVE unity (the -M-1 territory no oracle covered)
    words = [
        enc_io(sel=SRC_RDAD, wa=1, cmag=0, zero=1, csign=1),
        enc_idle(ra=1, cmag=32, csign=0),
        enc_idle(xfer=1, csign=1),
        enc_io(sel=SRC_RDRREG, wrda=True, chans="A", reset=True),
    ]
    total += compare_program(words, xs, "negative unity")

    # 3. odd coefficients both signs (pairC alive)
    for cmag, cs in ((21, 1), (21, 0), (5, 1), (5, 0), (47, 1), (47, 0), (63, 1)):
        words = [
            enc_io(sel=SRC_RDAD, wa=1, cmag=0, zero=1, csign=0),
            enc_idle(ra=1, cmag=cmag, csign=cs),
            enc_idle(xfer=1),
            enc_io(sel=SRC_RDRREG, wrda=True, chans="A", reset=True),
        ]
        total += compare_program(words, xs, f"cmag={cmag} cs={cs}")

    # 4. random multi-word group programs with feedback
    for trial in range(6):
        body = [enc_io(sel=SRC_RDAD, wa=0, cmag=rnd.randint(0, 63), zero=1,
                       csign=rnd.randint(0, 1))]
        for k in range(rnd.randint(2, 5)):
            body.append(enc_memr(rnd.randint(10, 60), wa=rnd.randint(0, 2),
                                 ra=rnd.randint(0, 2), cmag=rnd.randint(0, 63),
                                 csign=rnd.randint(0, 1)))
        body.append(enc_idle(ra=0, cmag=rnd.randint(0, 63), csign=rnd.randint(0, 1),
                             xfer=1))
        body.append(enc_memw(rnd.randint(0, 5)))
        body.append(enc_io(sel=SRC_RDRREG, wrda=True, chans="A", reset=True))
        xin = [rnd.randint(-12000, 12000) if i < 40 else 0 for i in range(160)]
        total += compare_program(body, xin, f"random#{trial}")

    print(f"\nTOTAL differing frames across all cases: {total}")
    print("VERDICT:", "RTL22 == physical (bit-identical on this battery)" if total == 0
          else "DIVERGENCE FOUND — engine re-sync required (characterize above)")


if __name__ == "__main__":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass
    main()
