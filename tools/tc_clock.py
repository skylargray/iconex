#!/usr/bin/env python3
"""224XL T&C clock/state generator — emulated FROM MC through the real chips (plan 020, owner directive
"emulate the whole netlist from MC; nothing asserted"). This module builds MS0-8 (and later AS/ARUCK/
strobes) by ticking the master clock MC through the transcribed gate/register netlist of T&C sheet 1
(§6T / `224XL TC pinouts from 060-02475-D.txt`), NOT by asserting the fig-3.2 waveforms.

It then VALIDATES the EMERGENT signals against the clock figures (timing_spec.json fig-3.2/3.4) — the
figure is the CHECK, the netlist+MC is the SOURCE.

MS generator (§6T.2), transcribed pins:
  tc_U56 (74S163 ÷ counter, CLK=MC): A=B=C=GND, D=+5V (load val 8), ENP=ENT=+5V, /CLR=+5V,
      /LD=MS4, QD(11)=MS4, RCO(15)=MS3.
  tc_U39 (74F374 shift reg, CP=MC): D0=MS3, Q0→D1; Q1=MS5(D2=MS5→Q2=MS6→...); chain
      D0=MS3→Q0→Q1(MS5)→Q2(MS6)→Q3(MS7)→Q4(MS8)→Q5(MS0)→Q6(MS1)→Q7(MS2).

Run:  python tools/tc_clock.py    (build MS0-8 from MC, print the emergent waveform, check vs fig-3.2)
"""
import os
import sys
import json

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
HERE = os.path.dirname(os.path.abspath(__file__))
TIMING_JSON = os.path.join(HERE, "timing", "timing_spec.json")


class U56_163:
    """74S163 synchronous 4-bit counter, sync clear. Only QD + RCO used here."""
    def __init__(self):
        self.q = 0

    def qd(self):
        return (self.q >> 3) & 1

    def rco(self, ent=1):
        return 1 if (self.q == 15 and ent) else 0

    def clock(self, clr_n=1, ld_n=1, enp=1, ent=1, load_val=8):
        # sync clear > sync load > count > hold, all on the rising edge
        if clr_n == 0:
            self.q = 0
        elif ld_n == 0:
            self.q = load_val & 15
        elif enp and ent:
            self.q = (self.q + 1) & 15
        # else hold


class U39_374:
    """74F374 octal D flip-flop (rising CP). q[0..7]."""
    def __init__(self):
        self.q = [0] * 8

    def clock(self, d):
        self.q = list(d)


class U25_FF2:
    """tc_U25 74S74 FF2: D=tc_U38.pin8 (=NOR(MS8,MS5,MS2)), CLK=MC. ARUCKE = 2/Q (= NOT 2Q)."""
    def __init__(self):
        self.q = 0                                   # 2Q

    def arucke(self):
        return 1 - self.q                            # 2/Q

    def clock(self, d):
        self.q = d & 1


class U23_175:
    """tc_U23 74LS175 AS generator. Common CLK=ARUCK (rising), common /CLR=MS4-net (async, active-low).
    FF0: D0=+5V, Q0=AS1/; FF1: D1=/Q0, Q1; FF2: D2=Q1, Q2=AS0. (FF3 unused.)"""
    def __init__(self):
        self.q = [0, 0, 0]                           # Q0(AS1/), Q1, Q2(AS0)

    def clock(self):
        q0, q1, q2 = self.q
        # Q <- D on ARUCK rising edge: Q0<-1, Q1<-/Q0, Q2<-Q1
        self.q = [1, 1 - q0, q1]

    def clear(self):
        self.q = [0, 0, 0]

    def AS1n(self):
        return self.q[0]                             # AS1/

    def AS0(self):
        return self.q[2]                             # AS0 (active-high)

    def AS0n(self):
        return 1 - self.q[2]                          # AS0/


class U20_JK1:
    """tc_U20 74S112 FF1 (negative-edge JK). CLK=tcCLKB (=inv MC) → clocks on MC RISING. J=MS1, K=MS8.
    1Q=DAB RSTB, 1/Q=DAB RSTB/. /PRE=/CLR=+5V."""
    def __init__(self):
        self.q = 0

    def clock(self, j, k):
        if j and k:
            self.q ^= 1                              # toggle
        elif j:
            self.q = 1                               # set
        elif k:
            self.q = 0                               # reset
        # else hold

    def rstb(self):
        return self.q                                # DAB RSTB

    def rstb_n(self):
        return 1 - self.q                            # DAB RSTB/


def simulate_clock(n_slots=45, verbose=False):
    """Tick MC through the WHOLE sheet-1 clock skeleton and return the emergent signals per MC slot:
    MS0-8 (MS4 = active-low net), ARUCK/ARUCKE/ARUCKE-bar, AS0/AS0-bar/AS1-bar, DAB WSTB/, DAB RSTB/RSTB-bar,
    XFER CK, ZERO/. Nothing asserted. (XFER/ZERO microword gates held =1 for the clock-skeleton figure.)"""
    u56 = U56_163()
    u39 = U39_374()
    u25 = U25_FF2()
    u23 = U23_175()
    u20 = U20_JK1()
    sig = {n: [] for n in ("MS0", "MS1", "MS2", "MS3", "MS4", "MS5", "MS6", "MS7", "MS8",
                           "ARUCKE", "ARUCK", "ARUCKE/", "AS0", "AS0/", "AS1/",
                           "DAB WSTB/", "DAB RSTB", "DAB RSTB/", "XFER CK", "ZERO/")}
    aruck_prev = 0
    for _ in range(n_slots):
        # --- combinational read of CURRENT state (pre-edge) ---
        MS4 = u56.qd()                               # active-low net
        MS3 = u56.rco()
        q = u39.q
        MS5, MS6, MS7, MS8, MS0, MS1, MS2 = q[1], q[2], q[3], q[4], q[5], q[6], q[7]
        nor_852 = 1 if (MS8 == 0 and MS5 == 0 and MS2 == 0) else 0   # tc_U38.pin8 = NOR(MS8,MS5,MS2)
        arucke = u25.arucke()                        # tc_U25 2/Q (registered from last MC edge)
        arucke_n = 1 - arucke                        # tc_U40 pin6 = NOT ARUCKE
        aruck = 1 - arucke_n                         # tc_U40 pin8 = NOT ARUCKE/ = ARUCKE (re-buffered)
        # record
        MS = dict(MS0=MS0, MS1=MS1, MS2=MS2, MS3=MS3, MS4=MS4, MS5=MS5, MS6=MS6, MS7=MS7, MS8=MS8)
        for k, v in MS.items():
            sig[k].append(v)
        sig["ARUCKE"].append(arucke); sig["ARUCK"].append(aruck); sig["ARUCKE/"].append(arucke_n)
        # ARUCK-domain outputs: ARUCK rises ~0.3 MS INTO the slot (fig-3.2 rise-lag), so the FF outputs
        # it clocks settle mid-slot and are seen by the MS-domain strobe gates in the NEXT integer slot.
        # Record AS0/AS0//AS1/ from the PREVIOUS post-clock state = a 1-slot delay modeling that lag.
        as0 = u23.AS0()
        sig["AS0"].append(as0); sig["AS0/"].append(u23.AS0n()); sig["AS1/"].append(u23.AS1n())
        # --- strobes generated combinationally from the state (nothing asserted) ---
        # DAB WSTB/ = tc_U37 = NOT MS7 (MS7 active-high)
        sig["DAB WSTB/"].append(1 - MS7)
        # DAB RSTB / RSTB/ = tc_U20 FF1 (registered; recorded pre-edge)
        sig["DAB RSTB"].append(u20.rstb()); sig["DAB RSTB/"].append(u20.rstb_n())
        # --- MC rising edge: clock the MC-domain FFs (all sample pre-edge state) ---
        d39 = [MS3, q[0], q[1], q[2], q[3], q[4], q[5], q[6]]
        u56.clock(ld_n=MS4)
        u39.clock(d39)
        u25.clock(nor_852)                            # ARUCKE registers NOR(MS8,MS5,MS2)
        u20.clock(MS1, MS8)                           # DAB RSTB JK on MC rising (via tcCLKB neg edge)
        # ARUCK follows ARUCKE combinationally; U23 clocks on ARUCK RISING edge (post-edge value)
        aruck_new = u25.arucke()
        if aruck_new == 1 and aruck_prev == 0:
            u23.clock()
        aruck_prev = aruck_new
        # /CLR = MS4-net (active-low): async-clears U23 whenever MS4 net is low (the MS4 slot)
        if u56.qd() == 0:
            u23.clear()
    # ARUCK rise-lag: delay the ARUCK-clocked outputs by 1 integer slot (see recording note above).
    for nm in ("AS0", "AS0/", "AS1/"):
        sig[nm] = [sig[nm][-1]] + sig[nm][:-1]
    # AS0-gated strobes are combinational from the (rise-lagged) AS0 net:
    #   ZERO/  = tc_U48 = NAND(ZEROgate=1, AS0)             -> low while AS0
    #   XFER CK = tc_U36 = NAND(AS0, XFER=1, tc_U25.pin9)    where tc_U25.pin9 = 2Q = NOT ARUCKE = ARUCKE/.
    # The ARUCKE/ term is what makes XFER CK a NARROWER/LATER pulse than ZERO/ (the ~20 ns lag). NOT a
    # constant — my earlier XFER-gate probe wrongly assumed it was.
    n = len(sig["AS0"])
    sig["ZERO/"] = [1] * n
    sig["XFER CK"] = [1] * n
    for i in range(n):
        as0 = sig["AS0"][i]
        arucke_bar = sig["ARUCKE/"][i]                # = tc_U25.pin9 (2Q)
        sig["ZERO/"][i] = 1 - as0
        sig["XFER CK"][i] = 1 - (as0 and arucke_bar)
    return sig


def simulate_ms(n_slots=27, verbose=True):
    """Tick MC through tc_U56 + tc_U39 and return the emergent MS0..MS8 per MC slot."""
    u56 = U56_163()
    u39 = U39_374()
    rows = {f"MS{k}": [] for k in range(9)}
    for _ in range(n_slots):
        # --- combinational read of the CURRENT state (pre-edge) ---
        MS4 = u56.qd()
        MS3 = u56.rco()
        q = u39.q
        MS5, MS6, MS7, MS8, MS0, MS1, MS2 = q[1], q[2], q[3], q[4], q[5], q[6], q[7]
        MS = [MS0, MS1, MS2, MS3, MS4, MS5, MS6, MS7, MS8]
        for k in range(9):
            rows[f"MS{k}"].append(MS[k])
        # --- clock both FFs on the MC rising edge (both sample pre-edge state) ---
        ld_n = MS4                                   # /LD = MS4 = QD
        # tc_U39 D-inputs (from CURRENT state): D0=MS3, D1=q0, D2=MS5(=q1), D3=MS6(=q2),
        # D4=MS7(=q3), D5=MS8(=q4), D6=MS0(=q5), D7=MS1(=q6)
        d = [MS3, q[0], q[1], q[2], q[3], q[4], q[5], q[6]]
        u56.clock(ld_n=ld_n)
        u39.clock(d)
    if verbose:
        print("Emergent MS0-8 from MC (each column = one MC slot):")
        for k in range(9):
            print(f"  MS{k}: {''.join(str(b) for b in rows[f'MS{k}'])}")
    return rows


def check_vs_fig32(rows):
    """Compare the emergent MS to fig-3.2 (one-hot MS0..MS8). Find the steady period and align."""
    with open(TIMING_JSON, encoding="utf-8") as f:
        spec = json.load(f)
    fig = next(x for x in spec["figures"] if x["id"] == "fig32")
    want = {r["name"]: r["wave"] for r in fig["signals"] if r["name"].startswith("MS")}
    # a full MS cycle is 9 slots; take the last complete period from the emergent trace
    L = len(rows["MS0"])
    period = 9
    seg = {k: rows[k][L - period:] for k in rows}
    # ★ MS4 is an ACTIVE-LOW net (= tc_U56 QD): it drives ONLY tc_U56 /LD and tc_U23 /CLR, both
    # active-low inputs, so the design uses QD (low at the reload slot) directly. fig-3.2 draws the
    # conceptual active-HIGH state, i.e. fig MS4 = NOT(net MS4). Invert MS4 for the state comparison.
    ACTIVE_LOW = {"MS4"}

    def as_state(name, lst):
        return [1 - b for b in lst] if name in ACTIVE_LOW else list(lst)

    # Absolute phase is arbitrary (which MC slot we call "slot 0"), so anchor to MS0: rotate the
    # segment so MS0's active-high state fires at slot 0, then check MS1..MS8 land at slots 1..8.
    ms0_state = as_state("MS0", seg["MS0"])
    s = ms0_state.index(1)

    def rot2(lst):
        return lst[s:] + lst[:s]
    print(f"\nBest alignment (rotate emergent by {s}); per-signal vs fig-3.2 one-hot state:")
    total_ok = True
    for k in range(9):
        name = f"MS{k}"
        emk = rot2(as_state(name, seg[name]))
        wk = want[name]
        got = "".join(str(b) for b in emk)
        ok = got == wk
        total_ok &= ok
        tag = " (active-low net; shown as state)" if name in ACTIVE_LOW else ""
        print(f"  {name}: state={got}  fig32={wk}  [{'OK' if ok else 'MISMATCH'}]{tag}")
    print(f"\nMS0-8 emergent-from-MC == fig-3.2: {'YES — the MS generator emerges correctly from MC' if total_ok else 'NO'}")
    if total_ok:
        print("  KEY FINDING: MS4 is an ACTIVE-LOW net (=tc_U56 QD) driving tc_U56 /LD + tc_U23 /CLR.")
        print("  Any downstream logic that consumed MS4 active-high would be WRONG — carry the polarity.")
    return total_ok


def check_clock_vs_fig32(sig):
    """Validate the emergent ARUCK / AS0 (and MS) against fig-3.2. MS4 shown as its active-high state."""
    with open(TIMING_JSON, encoding="utf-8") as f:
        spec = json.load(f)
    fig = next(x for x in spec["figures"] if x["id"] == "fig32")
    want = {r["name"]: r["wave"] for r in fig["signals"]}
    ACTIVE_LOW = {"MS4"}
    period = 9
    L = len(sig["MS0"])
    seg = {k: sig[k][L - period:] for k in sig}

    def as_state(name, lst):
        return [1 - b for b in lst] if name in ACTIVE_LOW else list(lst)
    s = as_state("MS0", seg["MS0"]).index(1)          # anchor phase to MS0

    def rot(lst):
        return lst[s:] + lst[:s]
    # map emergent signal name -> fig-3.2 signal name
    pairs = [("MS0", "MS0"), ("MS1", "MS1"), ("MS2", "MS2"), ("MS3", "MS3"), ("MS4", "MS4"),
             ("MS5", "MS5"), ("MS6", "MS6"), ("MS7", "MS7"), ("MS8", "MS8"),
             ("ARUCK", "ARU CK"), ("AS0", "AS0")]
    print("\nEmergent clock skeleton (from MC) vs fig-3.2:")
    ok_all = True
    for em, fg in pairs:
        got = "".join(str(b) for b in rot(as_state(em, seg[em])))
        wk = want[fg]
        ok = got == wk
        ok_all &= ok
        tag = " (active-low net→state)" if em in ACTIVE_LOW else ""
        print(f"  {fg:7}: emergent={got}  fig={wk}  [{'OK' if ok else 'MISMATCH'}]{tag}")

    # strobes vs fig-3.3 (MS grid): DAB WSTB/ + DAB RSTB
    fig33 = next(x for x in spec["figures"] if x["id"] == "fig33")
    w33 = {r["name"]: r["wave"] for r in fig33["signals"]}
    print("\nEmergent strobes (from MC) vs fig-3.3 (MS grid):")
    for em, fg in [("DAB WSTB/", "DAB WSTB/"), ("DAB RSTB", "DAB RSTB")]:
        got = "".join(str(b) for b in rot(seg[em]))
        wk = w33[fg]
        ok = got == wk
        ok_all &= ok
        print(f"  {fg:10}: emergent={got}  fig={wk}  [{'OK' if ok else 'MISMATCH'}]")

    # ZERO/ + XFER CK: gate on AS0 (fig-3.4 is AS-grid; here shown on the MS grid). The KEY relation to
    # verify is that XFER CK's low pulse is a SUBSET of ZERO/'s (XFER CK later/narrower via the ARUCKE/
    # term) — the ~20 ns "XFER CK lags ZERO/" — not that either is a fixed constant.
    z = "".join(str(b) for b in rot(seg["ZERO/"]))
    x = "".join(str(b) for b in rot(seg["XFER CK"]))
    xfer_subset = all(not (x[i] == "0" and z[i] == "1") for i in range(len(x)))   # XFER-low ⊆ ZERO-low
    xfer_narrower = x.count("0") < z.count("0")
    print("\nZERO/ vs XFER CK (both gate AS0; XFER CK adds the ARUCKE/ term):")
    print(f"  ZERO/   (MS grid): {z}")
    print(f"  XFER CK (MS grid): {x}")
    print(f"  XFER-CK low pulse ⊆ ZERO/ low pulse AND narrower (the ~20 ns lag): "
          f"{'YES' if (xfer_subset and xfer_narrower) else 'NO'}  "
          f"[key finding: tc_U25.pin9 = ARUCKE/, NOT a constant]")

    print(f"\nWHOLE clock+strobe skeleton emergent-from-MC == figures: {'YES' if ok_all else 'NO'}")
    return ok_all


if __name__ == "__main__":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass
    print("=" * 72)
    print("224XL T&C — clock skeleton generated FROM MC through the real chips (vs fig-3.2)")
    print("=" * 72)
    rows = simulate_ms()
    check_vs_fig32(rows)
    sig = simulate_clock()
    check_clock_vs_fig32(sig)
