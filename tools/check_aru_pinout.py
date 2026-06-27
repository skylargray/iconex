#!/usr/bin/env python3
"""Adversarial internal-consistency audit of the owner's ARU pin trace.

The interconnect netlist for the bit-exact model is BUILT from
  docs/reference/224/224XL ARU pinouts from 060-01318.txt
so a single transcription swap (e.g. A2<->A3 on a 74F283, or QC<->QD on a 74LS163)
would silently poison the arithmetic.

Approach:
 1. STANDARD datasheet pinouts: pin -> (role, bit_weight)  (bit_weight 0..3 = physical
    weight within a 4-bit slice; None for ctrl/pwr/clk).
 2. SELF-TEST the datasheet encoding vs owner DUAL pin-name labels (74F157, 74F374).
 3. Parse the owner trace into {chip: {pin: net}} AND {chip: {pin: owner_role_label}}.
 4. WEIGHT consistency around the accumulate loop, BY DATASHEET PIN NUMBER:
       accumulator-Q[w] net == adder-A[w] net   (register feeds adder A at same weight)
       adder-Sigma[w] -> sat-mux -> PP == accumulator-D[w] net
 5. RECIPROCITY: "Ux.pinA=Uy.pinB" must be mirrored (only when target pin is present).
 6. DATASHEET-LABEL CONFORMANCE: owner's role label must sit on the datasheet-correct pin.
"""
import os, re, sys, json

HERE = os.path.dirname(os.path.abspath(__file__))
TRACE = os.path.join(HERE, "..", "docs", "reference", "224",
                     "224XL ARU pinouts from 060-01318.txt")

# ----------------------------------------------------------------------------
# 1. STANDARD DATASHEET PINOUTS  pin -> (role, bit_weight)
# ----------------------------------------------------------------------------
DS_374 = {   # 74F374/74LS374 octal D-FF
    1:("OE\\",None),2:("Q0",0),3:("D0",0),4:("D1",1),5:("Q1",1),6:("Q2",2),
    7:("D2",2),8:("D3",3),9:("Q3",3),10:("GND",None),11:("CP",None),12:("Q4",4),
    13:("D4",4),14:("D5",5),15:("Q5",5),16:("Q6",6),17:("D6",6),18:("D7",7),
    19:("Q7",7),20:("VCC",None),
}
DS_163 = {   # 74LS163 sync counter
    1:("CLR\\",None),2:("CP",None),3:("A",0),4:("B",1),5:("C",2),6:("D",3),
    7:("ENP",None),8:("GND",None),9:("LOAD\\",None),10:("ENT",None),
    11:("QD",3),12:("QC",2),13:("QB",1),14:("QA",0),15:("RCO",None),16:("VCC",None),
}
DS_157 = {   # 74F157 quad 2:1 mux ; lanes a,b,c,d carry weights 0,1,2,3
    1:("SEL",None),2:("I0a",0),3:("I1a",0),4:("Ya",0),5:("I0b",1),6:("I1b",1),
    7:("Yb",1),8:("GND",None),9:("Yd",3),10:("I1d",3),11:("I0d",3),12:("Yc",2),
    13:("I1c",2),14:("I0c",2),15:("G\\",None),16:("VCC",None),
}
DS_283 = {   # 74F283 4-bit adder — CORRECTED 2026-06-26 to the REAL pinout
    # (owner-verified against the Lexicon schematic + Jameco 1000766 datasheet).
    # PRIOR VERSION WAS WRONG: it had pins 10/12/13/14/15/11 for the bit-2/bit-3
    # pairs swapped (assumed a linear layout). The 74283 upper nibble is "crossed":
    # S3/A3/B3 = pins 13/14/15 (weight 2) and S4/A4/B4 = pins 10/12/11 (weight 3).
    1:("S2",1),2:("B2",1),3:("A2",1),4:("S1",0),5:("A1",0),6:("B1",0),
    7:("Cin",None),8:("GND",None),9:("Cout",None),
    10:("S4",3),11:("B4",3),12:("A4",3),13:("S3",2),14:("A3",2),15:("B3",2),16:("VCC",None),
}
DS_86 = {   # 74S86 quad XOR
    1:("1A",None),2:("1B",None),3:("1Y",None),4:("2A",None),5:("2B",None),
    6:("2Y",None),7:("GND",None),8:("3Y",None),9:("3A",None),10:("3B",None),
    11:("4Y",None),12:("4B",None),13:("4A",None),14:("VCC",None),
}
DS_175 = {   # 74S175 quad D-FF
    1:("CLR\\",None),2:("Q0",0),3:("Q0\\",None),4:("D0",0),5:("D1",1),
    6:("Q1\\",None),7:("Q1",1),8:("GND",None),9:("CP",None),10:("Q2",2),
    11:("Q2\\",None),12:("D2",2),13:("D3",3),14:("Q3\\",None),15:("Q3",3),16:("VCC",None),
}
CHIP_DS = {
    "U43":DS_374,"U44":DS_374,"U10":DS_374,"U11":DS_374,
    "U45":DS_163,"U46":DS_163,"U47":DS_163,"U48":DS_163,"U49":DS_163,
    "U33":DS_157,"U34":DS_157,"U35":DS_157,"U36":DS_157,"U37":DS_157,
    "U19":DS_283,"U20":DS_283,"U21":DS_283,"U22":DS_283,"U23":DS_283,
    "U5":DS_86,"U6":DS_86,"U7":DS_86,"U8":DS_86,"U9":DS_86,"U12":DS_175,
}

# ----------------------------------------------------------------------------
# 2. PARSE owner trace -> nets {chip:{pin:net}} and labels {chip:{pin:label}}
#    Handle: "U43 (74F374)" headers, "U33:" headers, and "Unique to U45:" headers.
# ----------------------------------------------------------------------------
def parse_trace(path):
    nets, labels = {}, {}
    cur = None
    hdr_paren = re.compile(r"^\s*(U\d+)\s*\(74")          # "U43 (74F374)"
    hdr_colon = re.compile(r"^\s*(U\d+)\s*:")              # "U33:"
    hdr_unique = re.compile(r"Unique to\s+(U\d+)\s*:", re.I)  # "Unique to U45:"
    pinline = re.compile(r"^\s*pin\s+(\d+)\s*(?:\(([^)]*)\))?\s*=\s*(.+?)\s*$")
    with open(path, "r", encoding="utf-8", errors="replace") as f:
        for raw in f:
            m = hdr_unique.search(raw) or hdr_paren.match(raw) or hdr_colon.match(raw)
            if m:
                cur = m.group(1)
                nets.setdefault(cur, {}); labels.setdefault(cur, {})
                continue
            pm = pinline.match(raw)
            if pm and cur is not None:
                pin = int(pm.group(1))
                lbl = (pm.group(2) or "").strip()
                net = pm.group(3).strip()
                nets[cur][pin] = net
                if lbl:
                    labels[cur][pin] = lbl
    return nets, labels

REF = re.compile(r"\b(U\d+)\b(?:\s*\([^)]*\))?\s*pin\s*(\d+)", re.I)
def refs_in(net):
    return [(m.group(1).upper(), int(m.group(2))) for m in REF.finditer(net or "")]

def pin_for_role(chip, role):
    for p,(r,w) in CHIP_DS[chip].items():
        if r == role: return p
    return None
def net_at(nets, chip, pin):
    return nets.get(chip, {}).get(pin)

def adder_A_pins(c): return {w:pin_for_role(c,r) for w,r in zip(range(4),["A1","A2","A3","A4"])}
def adder_S_pins(c): return {w:pin_for_role(c,r) for w,r in zip(range(4),["S1","S2","S3","S4"])}
def acc_Q_pins(c):   return {w:pin_for_role(c,r) for w,r in zip(range(4),["QA","QB","QC","QD"])}
def acc_D_pins(c):   return {w:pin_for_role(c,r) for w,r in zip(range(4),["A","B","C","D"])}

# ----------------------------------------------------------------------------
def main():
    out = {"selftest": [], "weight": [], "reciprocity": [], "datasheet": [], "other": []}
    nets, labels = parse_trace(TRACE)

    # ---- 2b. SELF-TEST datasheet encoding vs owner dual labels ----
    # 74F157: owner dual labels "A1/I0a","Y1/Za",... lane letter must match our DS lane.
    f157_ok = True
    for chip in ("U33","U34","U35","U36","U37"):
        for pin, lbl in labels.get(chip, {}).items():
            # owner second token after '/' encodes lane, e.g. I0a / Za / I1d
            parts = re.split(r"/", lbl)
            owner_lane_tok = parts[1].strip() if len(parts) > 1 else parts[0].strip()
            ds_role = DS_157[pin][0]
            # extract lane letter from owner token (last alpha) and from ds_role
            om = re.search(r"([abcd])\b", owner_lane_tok.lower())
            dm = re.search(r"([abcd])\b", ds_role.lower())
            if om and dm and om.group(1) != dm.group(1):
                f157_ok = False
                out["selftest"].append(f"74F157 {chip} pin{pin}: owner '{lbl}' lane {om.group(1)} "
                                       f"vs DS role {ds_role} lane {dm.group(1)}")
    out["selftest"].append(f"74F157 dual-label self-test: {'PASS' if f157_ok else 'FAIL'}")

    # 74F374: owner labels Q0,D0,... must match DS_374 role exactly.
    f374_ok = True
    for chip in ("U43","U44","U10","U11"):
        for pin, lbl in labels.get(chip, {}).items():
            base = re.split(r"[\s/]", lbl)[0].strip()
            ds_role = DS_374[pin][0].replace("\\","")
            if base.replace("\\","") != ds_role:
                f374_ok = False
                out["selftest"].append(f"74F374 {chip} pin{pin}: owner '{lbl}' vs DS '{DS_374[pin][0]}'")
    out["selftest"].append(f"74F374 label self-test: {'PASS' if f374_ok else 'FAIL'}")

    # NOTE: U44 in the trace was given 74LS163-style labels (transcription of the wrong
    # template); we report that separately rather than failing the 374 datasheet itself.

    # ---- 3. WEIGHT CONSISTENCY around the accumulate loop, by DATASHEET PIN NUMBER ----
    for n in range(5):
        adder, mux, acc = f"U{19+n}", f"U{33+n}", f"U{45+n}"
        Ap, Sp = adder_A_pins(adder), adder_S_pins(adder)
        Qp, Dp = acc_Q_pins(acc), acc_D_pins(acc)
        for w in range(4):
            loc = f"nibble{n} (adder {adder} bit{w})"
            probs = []

            qnet = net_at(nets, acc, Qp[w])      # accumulator Q at weight w
            anet = net_at(nets, adder, Ap[w])    # adder A at weight w
            if qnet is None or anet is None:
                probs.append(f"missing: {acc}.Q(pin{Qp[w]})={qnet} / {adder}.A(pin{Ap[w]})={anet}")
            elif qnet != anet:
                probs.append(f"Q!=A: {acc}.Q(pin{Qp[w]})='{qnet}' vs {adder}.A(pin{Ap[w]})='{anet}'")

            # adder Sigma[w] -> mux input -> mux Y -> PP -> acc D[w]
            snet = net_at(nets, adder, Sp[w])
            mux_in = [(c,p) for (c,p) in refs_in(snet) if c == mux]
            pp = ypin = inpin = None
            if not mux_in:
                probs.append(f"Sigma(pin{Sp[w]})='{snet}' has no ref to mux {mux}")
            else:
                inpin = mux_in[0][1]
                role, mw = DS_157.get(inpin,(None,None))
                if role is None or not role.startswith("I0"):
                    probs.append(f"Sigma(pin{Sp[w]}) -> {mux} pin{inpin} role '{role}' not an I0 lane input")
                else:
                    lane = role[2]
                    ypin = pin_for_role(mux, "Y"+lane)
                    pp = net_at(nets, mux, ypin)
                    if mw != w:
                        probs.append(f"mux {mux} lane weight {mw} != adder bit{w} (Sigma->pin{inpin})")
            dnet = net_at(nets, acc, Dp[w])
            if pp is None or dnet is None:
                probs.append(f"missing: mux {mux}.Y(pin{ypin})PP={pp} / {acc}.D(pin{Dp[w]})={dnet}")
            elif pp != dnet:
                probs.append(f"PP!=accD: {mux}.Y(pin{ypin})='{pp}' vs {acc}.D(pin{Dp[w]})='{dnet}'")

            if probs:
                out["weight"].append({"location":loc,"status":"inconsistent","detail":" | ".join(probs)})
            else:
                out["weight"].append({"location":loc,"status":"consistent",
                    "detail":(f"{acc}.Q(pin{Qp[w]})={qnet}=={adder}.A(pin{Ap[w]}); "
                              f"Sigma(pin{Sp[w]})->{mux} I0(pin{inpin})->Y(pin{ypin})={pp}=={acc}.D(pin{Dp[w]})")})

    # ---- 4. RECIPROCITY (only when target pin is actually present in the doc) ----
    seen = set()
    for chip, pins in nets.items():
        if chip not in CHIP_DS: continue
        for pin, net in pins.items():
            for (tc, tp) in refs_in(net):
                if tc not in CHIP_DS: continue
                key = tuple(sorted([(chip,pin),(tc,tp)]))
                if key in seen: continue
                seen.add(key)
                back = net_at(nets, tc, tp)
                if back is None:
                    # target pin not explicitly listed (e.g. 74S86 shorthand) -> not a contradiction
                    continue
                if (chip,pin) not in refs_in(back):
                    out["reciprocity"].append(
                        f"NON-RECIPROCAL: {chip}.pin{pin}='{net}' -> {tc}.pin{tp}, but "
                        f"{tc}.pin{tp}='{back}' does not point back")

    # ---- 5. DATASHEET-LABEL CONFORMANCE (owner role label must sit on datasheet pin) ----
    for chip, lbls in labels.items():
        if chip not in CHIP_DS: continue
        ds = CHIP_DS[chip]
        for pin, lbl in lbls.items():
            ds_role = ds.get(pin,(None,None))[0]
            if ds_role is None: continue
            if not _roles_match(chip, pin, lbl, ds_role):
                out["datasheet"].append(f"{chip} pin{pin}: owner label '{lbl}' vs datasheet '{ds_role}'")

    txt = json.dumps(out, indent=2, ensure_ascii=True)
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    print(txt)
    return out

def _roles_match(chip, pin, owner_label, ds_role):
    o = re.split(r"[\s/]", owner_label.strip())[0].upper().replace("Σ","S")
    d = ds_role.upper().replace("\\","")
    if o.replace("\\","") == d:
        return True
    if chip in ("U19","U20","U21","U22","U23"):
        # owner 0-based S0..S3/A0..A3/B0..B3 ; DS 1-based.  Map owner index k -> DS role index k+1.
        m = re.match(r"([SAB])(\d)", o)
        if m:
            kind,k = m.group(1), int(m.group(2))
            want = {"S":["S1","S2","S3","S4"],"A":["A1","A2","A3","A4"],
                    "B":["B1","B2","B3","B4"]}[kind][k]
            return want == d
        if "C0" in o or "CARRY-IN" in owner_label.upper(): return d == "CIN"
        if "C4" in o or "CARRY-OUT" in owner_label.upper(): return d == "COUT"
    if chip in ("U45","U46","U47","U48","U49"):
        alias = {"D0":"A","D1":"B","D2":"C","D3":"D","Q0":"QA","Q1":"QB","Q2":"QC","Q3":"QD",
                 "RCO":"RCO","CLR":"CLR","LOAD":"LOAD","ENP":"ENP","ENT":"ENT","CP":"CP","GND":"GND","VCC":"VCC"}
        return alias.get(o,o) == d
    if chip in ("U33","U34","U35","U36","U37"):
        alias = {"A1":"I0A","A2":"I0B","A3":"I0C","A4":"I0D","B1":"I1A","B2":"I1B","B3":"I1C","B4":"I1D",
                 "Y1":"YA","Y2":"YB","Y3":"YC","Y4":"YD","SEL":"SEL","G":"G"}
        return alias.get(o,o) == d
    return o == d

if __name__ == "__main__":
    main()
