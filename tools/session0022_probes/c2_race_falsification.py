#!/usr/bin/env python3
"""C2 — arbitrate the ONE wiring-allowed binary (the 163 /CLR sample race at the slot-4 edge:
does the clear obey the OLD stage-2 Q6 (lag => owner = w_{n-1}) or the NEW one (no-lag =>
owner = w_n)? Both meet marginal timing on paper (LS377 clk-to-Q + NAND vs 163 setup inside
one 32.6 ns MC slot); the factory program decides.

Registry note: re-opens no dead-end entry — this binary did not exist before the traced model.

Everything else is wiring-FORCED and identical in both variants:
  pps of word W land at slots 4(W+1), 7(W+1), 1(W+2); capture at slot-3(n) gated by
  w_{n-1}.XFER sees the MAC complete through w_{n-2}; operand = post-write regfile.

Measurements per variant (CONCERT boot image, impulse -6 dBFS, 2.0 s):
  early peak (0-100 ms), output RMS per 0.25 s block (ch A+C), tank energy at 0.5/1.0/2.0 s.
"""
import sys, os, json, math
TOOLS = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, TOOLS)
from aru_freerun22_rtl import RTL22, program_rows22, fs22, booth3, wrap20, res_from_acc
from aru_rtl_dp import s16

HERE = os.path.dirname(os.path.abspath(__file__))
cache = json.load(open(os.path.join(HERE, "wcs_cache.json")))
b = bytes.fromhex(cache["1"]["wcs"])
wcs = [(b[4*k], b[4*k+1], b[4*k+2], b[4*k+3]) for k in range(128)]
rows, L, w_reset = program_rows22(wcs)
FS = fs22(L)


class RTL22NoLag(RTL22):
    """clear-owner = the CURRENT word (w_n)."""
    def step(self, d, audio_in, probe=None, fidx=0, sidx=0):
        wp = self.wp
        R = self.R
        if wp is not None:
            opnd = R[wp["RA"]]
            ppA, ppB, ppC = booth3(opnd, wp["cmag"], wp["cs"])
        else:
            opnd, ppA, ppB, ppC = 0, 0, 0, 0
        self.ACC = wrap20(self.ACC + self.ppC_pend)
        if wp is not None and wp["XFER"]:
            self.RES = res_from_acc(self.ACC)
        if d["ZERO"]:                                   # << the ONLY difference vs RTL22
            self.ACC = 0
        else:
            self.ACC = wrap20(self.ACC + ppA)
        addr = (self.CPC - d["ofst"]) & 0xFFFF
        typ = d["typ"]
        out_da = []
        if typ == 0:
            self.DAB = self.DM.get(addr, 0) & 0xFFFF
        elif typ == 1:
            self.DAB = self.RES & 0xFFFF
            self.DM[addr] = self.DAB
        elif typ == 2:
            sel = d["sel"]
            if sel == 1:
                self.DAB = self.RES & 0xFFFF
            elif sel == 3:
                self.DAB = audio_in & 0xFFFF
            elif sel == 2:
                self.DAB = 0
            if d["WRDA"]:
                out_da = [(c, s16(self.DAB)) for c in d["chans"]]
        self.ACC = wrap20(self.ACC + ppB)
        R[d["WA"]] = s16(self.DAB)
        if typ == 2 and d["WRX"]:
            self.XREG_wr = self.DAB & 0xFFFF
        self.ppC_pend = ppC
        self.wp = d
        self.step_count += 1
        return out_da


def measure(engcls, tag, secs=2.0):
    n = int(secs * FS)
    blk = int(0.25 * FS)
    eng = engcls()
    acc = {c: 0 for c in "ABCD"}
    cnt = 0
    blocks = []
    early_peak = 0
    tank = {}
    for i in range(n):
        outs = eng.run_sample(rows, 16422 if i == 0 else 0)
        for c, v in outs:
            acc[c] += v * v
            if i < int(0.1 * FS):
                early_peak = max(early_peak, abs(v))
        cnt += 1
        if cnt == blk:
            blocks.append({c: math.sqrt(acc[c] / blk) for c in "ABCD"})
            acc = {c: 0 for c in "ABCD"}
            cnt = 0
        if i + 1 in (int(0.5 * FS), int(1.0 * FS), n):
            tank[round((i + 1) / FS, 1)] = sum(s16(v) * s16(v) for v in eng.DM.values())
    print(f"\n[{tag}] early peak(0-100ms)={early_peak}")
    print(f"  blk(0.25s) RMS A: " + " ".join(f"{b['A']:8.1f}" for b in blocks))
    print(f"  blk(0.25s) RMS C: " + " ".join(f"{b['C']:8.1f}" for b in blocks))
    print(f"  tank E: " + "  ".join(f"{t}s={e:.3e}" for t, e in sorted(tank.items())))
    return blocks, early_peak, tank


print(f"CONCERT boot image, impulse -6 dBFS, 2.0 s, fs={FS:.0f}")
measure(RTL22, "LAG   (clear owner = w_{n-1})")
measure(RTL22NoLag, "NO-LAG (clear owner = w_n)")
