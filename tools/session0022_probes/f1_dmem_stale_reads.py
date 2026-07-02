#!/usr/bin/env python3
"""F1c gate-4 side finding (plan 024) — the diag-3 STALE-CELL adjudication.

Discovery (f1_e1c_engine_xcheck coverage assert): the diag-3 steady frame is NOT
write-before-read closed — rows 1/4/5 are MEMRs whose cells were last written by the
rows-8/9 MEMWs 65536 (full CPC wrap), 5555, and ~54426 frames earlier:
    row 1 MEMR ofst=0      reads addr CPC       (last write: row 8, 54426 frames ago)
    row 4 MEMR ofst=16665  reads addr CPC-16665 (last write: row 8,  5555 frames ago)
    row 5 MEMR ofst=5555   reads addr CPC-5555  (last write: row 9, one wrap ago)
The values read NEVER reach a MAC operand (every row writes R3, and every RA=3 operand
load samples R3 one step after an IO write overwrote it) — they appear ONLY on the
DAB/DOUT streams (bit 15 is the only bit that can differ: the steady written value is
the saturated-tail capture V* = phys 0x8000, vs the never-written default phys 0x0000).

So the signature tables THEMSELVES adjudicate what the bench DRAM returned for a
~1.7-2.0 s-old cell. Two physical hypotheses, scored head-to-head at the champion
variant against BOTH ARU tables (corrected per the owner's errata):

  H0 (the e1c convention): stale cells read phys 0x0000 — the DRAM does not hand back
     the wrap-old value (no refresh reaches those cells / decayed readout).
  H1: the DRAM retains across the wrap (e.g. RAS-sweep refresh via the CPC walk) —
     reads return V* = 0x8000; modeled by pre-seeding every cell to 0x8000 (the true
     wrap-around fixed point: every cell was written 0x8000 by rows 8/9 last wrap).

PREDICTION (declared before the run): H1 flips the DAB15 stream at ~9 samples/frame
(steps 1/4/5 + the DOUT-register holdover), so exactly the DAB15-carrying listed pins
(result reg U43.6, regfile U29.15) should drop; H0 keeps the corrected-table score.
Whichever scores higher is the bench behavior; a mixed result would name its net.
"""
import sys, os

TOOLS = r"d:\OneDrive\Gray Instruments\iconex\tools"
sys.path.insert(0, TOOLS)

import e1_aru_signatures as E1

CHAMPION = (0, 0, 0, 0)


class WrapDM(dict):
    """The full-wrap steady DMEM: every cell was written V*=0x8000 one wrap ago."""
    def get(self, k, default=None):
        return super().get(k, 0x8000)


def patched_clone(em):
    c = E1.Emitter((em.prload, em.rail_pol, em.dual3, em.capb))
    c.R = list(em.R)
    c.ACC = em.ACC
    c.RES = em.RES
    c.dab = em.dab
    c.dout_reg = em.dout_reg
    c.DM = type(em.DM)(em.DM)          # preserve the DM subclass through the clone
    c.CPC = em.CPC
    c.wp = em.wp
    c.pipe = dict(em.pipe) if em.pipe else None
    return c


def main():
    txt = open(os.path.join(E1.DOCS, "224-signature-value-tables.md"), encoding="utf-8").read()
    t_nfb = E1.parse_table(txt, "#### ARU Module — Version 8.2.1 — no feedback")
    t_fb = E1.parse_table(txt, "#### ARU Module — Version 8.2.1 (feedback configuration)")
    tables = {"no-feedback(62)": (t_nfb, 62), "feedback(90)": (t_fb, 90)}
    PM = E1.build_pinmap()
    E1._clone = patched_clone

    results = {}
    for name, seed in (("H0 stale=0x0000 (e1c convention)", None),
                       ("H1 stale=0x8000 (wrap retention)", WrapDM)):
        orig_init = E1.Emitter.__init__
        if seed is not None:
            def seeded_init(self, variant, _orig=orig_init, _cls=seed):
                _orig(self, variant)
                self.DM = _cls()
            E1.Emitter.__init__ = seeded_init
        try:
            rot, tot, detail, iters = E1.score_variant(CHAMPION, tables, PM)
        finally:
            E1.Emitter.__init__ = orig_init
        nlisted = sum(len(d["match"]) + len(d["mismatch"]) for d in detail.values())
        results[name] = (tot, nlisted, rot, detail)
        print(f"\n[{name}] {tot}/{nlisted} @rot={rot} (steady in {iters} frames)")
        for tname, d in detail.items():
            if d["mismatch"]:
                print(f"  {tname} mismatches:")
                for (u, p), want, got, s in d["mismatch"]:
                    print(f"    {u}.{p}: table {want} vs model {got}  [{s}]")

    (t0, n0, _, _), (t1, n1, _, _) = results[list(results)[0]], results[list(results)[1]]
    print(f"\nVERDICT: H0 {t0}/{n0} vs H1 {t1}/{n1} -> the bench DRAM "
          + ("returns phys 0x0000 for the wrap-old cells (H0; the e1c convention is the "
         "measured physical behavior, not an assumption)" if t0 > t1 else
         "RETAINS across the wrap (H1) — the e1c convention must be re-based" if t1 > t0 else
         "TIE — the listed pins do not cover the stale-read streams"))


if __name__ == "__main__":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass
    main()
