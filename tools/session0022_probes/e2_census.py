#!/usr/bin/env python3
"""E2 — I/O-census convention fit, run on the E1 WCS cache.

For a candidate convention (t = stored l2&3 value meaning tcWR, b = stored-bit level that
asserts an OFST command line) decode every program's executed window (reversed order,
words 127 down to 128-L) and census the I/O structure against the hardware anchors:

  - exactly ONE reset, at the LAST executed step (its falling event clocks CPC + syncs FPC)
  - ~2 RD-AD reads (CH1/CH2 on opposite frame halves, fig-3.5)
  - ~4 WR-DA writes, spaced >= ~20 steps (FPC BUSY: strobe counter 0x2A..0x40 = 22 steps),
    jointly covering channels A..D (SDA = OFST11/..OFST8/ one-hot-reversed)
  - WR-DA steps co-select a DAB source (sel 01=RDRREG result reg, 11=RD-AD, 10=XREG)

Command-bit decode (netlist 2T.1-2T.5): on a tcWR step the OFST lines are device selects:
  bit3=RESET  bit4=DP  bit5=TEST  bit6=WR XREG (MS7-gated)  bit7=WR DA
  bits8-11 = SDA D,C,B,A (independent enables)  bits12-13 = dec-2 source select
Line asserted iff stored bit == b. Source select VALUE uses line levels:
  sel = ((s13 ^ inv)<<1) | (s12 ^ inv), inv = (b==0);  1=RDRREG 2=XREG 3=RD-AD 0=none.
Type classes from (MEMAC,MI16) levels = stored bits ^ inv2, inv2 = (t==2):
  (0,0)=idle (0,1)=tcWR/IO (1,0)=MEMW (1,1)=MEMR.
"""
import sys, os, json, argparse

SCRATCH = os.path.dirname(os.path.abspath(__file__))
CACHE = os.path.join(SCRATCH, "wcs_cache.json")

CH = {8: "D", 9: "C", 10: "B", 11: "A"}
SRC = {0: "-", 1: "RDRREG", 2: "XREG", 3: "RD-AD"}

def words(wcs_hex):
    b = bytes.fromhex(wcs_hex)
    return [(b[4*k], b[4*k+1], b[4*k+2], b[4*k+3]) for k in range(128)]

def classify(l2, t):
    if t == 1:   inv2 = 0
    elif t == 2: inv2 = 1
    else:        inv2 = None            # incoherent with dec-1 wiring; treat t as IO only
    if (l2 & 3) == t:
        return "IO"
    if inv2 is None:
        return f"?{l2 & 3}"
    memac = ((l2 >> 1) & 1) ^ inv2
    mi16 = (l2 & 1) ^ inv2
    return {(0, 0): "idle", (0, 1): "IO", (1, 0): "MEMW", (1, 1): "MEMR"}[(memac, mi16)]

def decode_io(ofst, b):
    inv = 1 if b == 0 else 0
    bit = lambda n: 1 if ((ofst >> n) & 1) == b else 0
    sel = ((((ofst >> 13) & 1) ^ inv) << 1) | (((ofst >> 12) & 1) ^ inv)
    chans = "".join(CH[n] for n in (11, 10, 9, 8) if bit(n))
    return {"RESET": bit(3), "DP": bit(4), "TEST": bit(5), "WRX": bit(6),
            "WRDA": bit(7), "chans": chans, "sel": sel}

def census(ws, t, b, L):
    """Execution order: words 127 down to 128-L (exec index 0..L-1)."""
    w0 = 128 - L
    rows = []
    for ei in range(L):
        k = 127 - ei
        l0, l1, l2, l3 = ws[k]
        cls = classify(l2, t)
        row = {"exec": ei, "word": k, "cls": cls, "ofst": l0 | (l1 << 8),
               "l2": l2, "l3": l3}
        if cls == "IO":
            row.update(decode_io(row["ofst"], b))
        rows.append(row)
    io = [r for r in rows if r["cls"] == "IO"]
    resets = [r for r in io if r.get("RESET")]
    wrda = [r for r in io if r.get("WRDA")]
    rdad = [r for r in io if r.get("sel") == 3]
    spacing = [b2["exec"] - a["exec"] for a, b2 in zip(wrda, wrda[1:])]
    return {
        "rows": rows,
        "n": {c: sum(1 for r in rows if r["cls"] == c)
              for c in ("IO", "MEMW", "MEMR", "idle")},
        "resets": [(r["exec"], r["word"]) for r in resets],
        "reset_last": bool(resets) and resets[-1]["exec"] == L - 1 and len(resets) == 1,
        "wrda": [(r["exec"], r["word"], r["chans"], SRC[r["sel"]]) for r in wrda],
        "wrda_minspace": min(spacing) if spacing else None,
        "chan_cover": "".join(sorted(set("".join(r["chans"] for r in wrda)))),
        "rdad": [(r["exec"], r["word"]) for r in rdad],
    }

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("-t", type=int, required=True)
    ap.add_argument("-b", type=int, required=True)
    ap.add_argument("-L", type=int, default=0, help="program length; 0 = auto per program (128 - max firing word)")
    ap.add_argument("--full", type=int, default=None, help="print full decode for this id")
    args = ap.parse_args()

    cache = {int(k): v for k, v in json.load(open(CACHE)).items() if v.get("ok")}
    print(f"convention t={args.t} b={args.b} L={args.L}; programs={sorted(cache)}\n")
    hdr = f"{'id':>3} {'IO':>3} {'MEMW':>4} {'MEMR':>4} {'idle':>4} | resets(exec,word) | " \
          f"{'1@end':>5} | WR-DA (exec,word,ch,src) minsp | chans | RD-AD"
    print(hdr); print("-" * len(hdr))
    def auto_L(ws):
        F = [k for k, (l0, l1, l2, l3) in enumerate(ws)
             if (l2 & 3) == args.t and ((l0 >> 3) & 1) == args.b]
        return 128 - max(F) if F else 100

    for pid, rec in sorted(cache.items()):
        ws = words(rec["wcs"])
        L = args.L or auto_L(ws)
        c = census(ws, args.t, args.b, L)
        print(f"{pid:>3} L={L:>3} {c['n']['IO']:>3} {c['n']['MEMW']:>4} {c['n']['MEMR']:>4} "
              f"{c['n']['idle']:>4} | {c['resets']} | {str(c['reset_last']):>5} | "
              f"{c['wrda']} {c['wrda_minspace']} | {c['chan_cover']:>4} | {c['rdad']}")

    if args.full is not None and args.full in cache:
        print(f"\n=== full decode, id {args.full} (execution order) ===")
        ws = words(cache[args.full]["wcs"])
        c = census(ws, args.t, args.b, args.L or auto_L(ws))
        for r in c["rows"]:
            extra = ""
            if r["cls"] == "IO":
                flags = "".join(n for n in ("RESET", "DP", "TEST", "WRX", "WRDA") if r.get(n))
                extra = f" [{flags}] ch={r['chans']} src={SRC[r['sel']]}"
            print(f"  exec {r['exec']:>3} = word {r['word']:>3}: {r['cls']:<5} "
                  f"ofst=0x{r['ofst']:04X} l2=0x{r['l2']:02X} l3=0x{r['l3']:02X}{extra}")

if __name__ == "__main__":
    main()
