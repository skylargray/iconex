#!/usr/bin/env python3
"""Full, honest decode of all 100 steps of the CONCERT WCS microprogram.

Source = the 0x4000 WCS image read straight from a boot on the VERIFIED kosarev I8080 core
(byte-identical to the static snapshot, per the trace harness). Goal: PROVE the instruction-set
decode is complete (every one of the 32 microword bits accounted for) and HONEST (confidence split
into decode-confidence vs function-confidence; no invented DSP-role labels).

32-bit microword field map (gate-traced, netlist §3.6/§3.7/§3.8/§3.10/§G3R; classes per
docs/reference/224/224XL_provenance_ledger.md):
  MI0-15  = OFFSET (MEMR/MEMW) or I/O command bits (I/O step)         [hardware-verified bit layout]
  MI16    = device r/w select (with MEMAC)                            [verified]
  MI17    = MEMAC (DMEM access enable)                                [verified]
  MI18-19 = WA (regfile write addr)                                   [verified]
  MI20-21 = RA (regfile read addr)                                    [verified]
  MI22    = PROT (protect) -- tc_U18.QC; DOWNSTREAM EFFECT UNRESOLVED [bit verified, function UNKNOWN]
  MI23    = CSIGN source (AS0-gated JK, not a stored bit)             [verified]
  MI24    = XFER (result-reg transfer)                                [bit verified; gating untested]
  MI25    = ZERO (accumulator clear)                                  [verified]
  MI26-31 = cmag (6-bit coeff magnitude C0..C5)                       [verified]
Run: python tools/decode_concert_program.py   (boots ~1-2 min; caches the 0x4000 image)
"""
import os
import sys
import json

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
sys.stdout.reconfigure(encoding="utf-8")

FS = 34130.0
SCR = (r"C:/Users/Skylar/AppData/Local/Temp/claude/"
       r"d--OneDrive-Gray-Instruments-iconex/f950f5a4-d96d-4fdd-899a-08b03ca853c7/scratchpad")
CACHE = os.path.join(SCR, "verified_wcs_0x4000.json")
OUTDOC = (r"d:/OneDrive/Gray Instruments/iconex/docs/reference/224/224XL_CONCERT_program_decode.md")


def verified_wcs():
    """0x4000..0x41FF from a boot on the VERIFIED core (cached after first run)."""
    if os.path.exists(CACHE):
        return json.load(open(CACHE))
    import boot8080 as B
    print("booting v8.2.1 to CONCERT on the verified kosarev core (~1-2 min)...")
    m, ms = B.boot(verbose=True)
    assert "mainloop" in ms and "prog_load" in ms, f"boot did not reach mainloop: {ms}"
    img = [m.memory[0x4000 + i] for i in range(0x200)]
    json.dump(img, open(CACHE, "w"))
    print(f"  captured 0x4000..0x41FF from the verified boot; final PC reached mainloop.")
    return img


def decode_full(l0, l1, l2, l3):
    """Decode ALL 32 bits. Returns a dict; nothing dropped (incl. PROT=MI22)."""
    inv3 = (~l3) & 0xFF
    ofield = l0 | (l1 << 8)
    d = dict(
        word=l0 | (l1 << 8) | (l2 << 16) | (l3 << 24),
        offset_field=ofield,
        MI16=l2 & 1, MEMAC=(l2 >> 1) & 1, WA=(l2 >> 2) & 3, RA=(l2 >> 4) & 3,
        PROT=(l2 >> 6) & 1, CSIGN=(l2 >> 7) & 1,
        XFER=inv3 & 1, ZERO=(inv3 >> 1) & 1, cmag=(inv3 >> 2) & 0x3F)
    # device class from {MEMAC, MI16}
    if d["MEMAC"] == 1 and d["MI16"] == 0:
        d["dev"] = "MEMW"
    elif d["MEMAC"] == 1 and d["MI16"] == 1:
        d["dev"] = "MEMR"
    elif d["MEMAC"] == 0 and d["MI16"] == 1:
        d["dev"] = "IO"
    else:
        d["dev"] = "idle"
    # I/O command sub-decode (MI0-15 repurposed): §2T
    if d["dev"] == "IO":
        def ob(n):
            return (ofield >> n) & 1
        sel = (ob(13) << 1) | ob(12)
        d["io_read"] = {3: "RD_AD", 2: "RD_XREG", 1: "RDRREG", 0: "-"}[sel]
        d["wr_da"] = bool(ob(7))
        d["wr_xreg"] = bool(ob(6))
        chans = []
        if ob(8):
            chans.append("D")
        if ob(9):
            chans.append("C")
        if ob(10):
            chans.append("B")
        if ob(11):
            chans.append("A")
        d["da_chans"] = chans
    return d


# --- dataflow roles established by the 2026-06-30 traces (feedback-vs-output / excitation) ---
RECIRC_READ = {0, 1, 2, 3, 51}          # cmag>0 MEMR that read recirculated DMEM (the feedback/over-unity taps)
INERT_BLOCK = set(range(5, 23))         # 19 identical cmag=0+PROT=1 MEMR (offset 0x1AB3) — function UNKNOWN
MEMW_LIVE = {44, 75, 77, 96}            # MEMW with XFER=1 → DIN = just-XFER'd RES (live writeback; excites the loop)
MEMW_STALE = {24, 40, 52, 92}           # MEMW with XFER=0 → DIN = stale RES (recirc product orphaned here)
WET_OUT = {4, 99}                       # sel==01 RDRREG + WR DA → result-reg to D/A (the WET output path)
DRY_CLOBBER = {58, 62, 63, 70}          # RD_AD (sample input) that ALSO WR DA → output dry input, clobbering the wet
HELD_WET_OUT = {55}                     # HOLD WR DA that carries the held recirc value to the D/A (the visible echo)


def func_and_conf(d, k):
    """Function + crisp confidence, with the session's dataflow roles folded in.
    Confidence key: ★★★ VERIFIED (gate+POST) · ★★ GROUNDED (gate+SM+FPC, not POST) · ★ INFERRED (dataflow) · ? UNKNOWN."""
    cmag, cs = d["cmag"], d["CSIGN"]
    coeff = ("0 (mult OFF)" if cmag == 0 else f"{'+' if cs else '-'}{cmag}/32={cmag/32 if cs else -cmag/32:+.3f}")
    mac = f"R{d['RA']}×{coeff}" + ("  XFER→RES" if d["XFER"] else "") + ("  ZERO(clr)" if d["ZERO"] else "")
    dev = d["dev"]
    role, fconf = "", "?"
    if dev == "MEMR":
        base = f"DMEM READ @0x{d['offset_field']:04X} (delay) → R{d['WA']}; MAC {mac}"
        if k in RECIRC_READ:
            role = " — ★recirc/feedback tap (reads recirculated DMEM; cmag={} ⇒ over-unity).".format(cmag); fconf = "★ INFERRED (dataflow)"
        elif k in INERT_BLOCK:
            role = " — INERT block (cmag=0 mult-off, PROT=1, identical ×19; function UNKNOWN — refresh?)."; fconf = "? UNKNOWN"
        else:
            role = " — delay-line read."; fconf = "★★ GROUNDED (mech)"
    elif dev == "MEMW":
        base = f"DMEM WRITE @0x{d['offset_field']:04X} (delay) ← DIN=RES; MAC {mac}"
        if k in MEMW_LIVE:
            role = " — ★live writeback (XFER=1 → DIN = just-computed RES; excites/feeds the loop)."; fconf = "★ INFERRED (dataflow)"
        elif k in MEMW_STALE:
            role = " — writeback with XFER=0 → DIN = STALE RES (recirc product orphaned here)."; fconf = "★ INFERRED (dataflow)"
        else:
            role = " — delay-line write."; fconf = "★★ GROUNDED (mech)"
    elif dev == "IO":
        bits = []
        if d["io_read"] != "-":
            bits.append({"RD_AD": "read A/D (sample input)", "RD_XREG": "read X-reg (host=0)",
                         "RDRREG": "result-reg→DAB"}[d["io_read"]])
        if d["wr_da"]:
            bits.append(f"WR DA→ch {'+'.join(d['da_chans']) or '(none)'}")
        if d["wr_xreg"]:
            bits.append("WR XREG (host sink)")
        base = "I/O: " + ("; ".join(bits) if bits else "(no r/w flags)") + f"; MAC {mac}"
        if k in WET_OUT:
            role = " — ★WET OUTPUT (sel==01 RDRREG drives RES to the D/A; role INFERRED, not POST-proven)."; fconf = "★ INFERRED"
        elif k in DRY_CLOBBER:
            role = " — DRY passthrough (samples input AND outputs it; CLOBBERS the wet on overlapping channels)."; fconf = "★★ GROUNDED (FPC)"
        elif d["io_read"] == "RD_AD":
            role = " — input sampling (no WR DA)."; fconf = "★★ GROUNDED (FPC)"
        else:
            role = " — I/O move."; fconf = "★★ GROUNDED"
    else:
        base = f"COMPUTE-MAC (no bus device): {mac}; R{d['WA']}←held-DAB"
        role = ""; fconf = "★★★ VERIFIED (no device)"
        if k in HELD_WET_OUT:
            role = " — (held DAB here carries the recirc value to step-55 output window)."
    if k in HELD_WET_OUT and dev == "IO":
        role = " — ★the WET ECHO reaches the D/A here (HOLD WR DA outputs the held recirc value)."
        fconf = "★ INFERRED (dataflow)"
    fn = base + role
    if d["PROT"] and k not in INERT_BLOCK:
        fn += " [PROT=1; effect UNRESOLVED]"
    # decode-confidence: all fields VERIFIED except PROT(effect) + (now-settled) offset
    dconf = "★★★ decode" + (" (PROT effect ?)" if d["PROT"] else "")
    return fn, f"{dconf} · fn: {fconf}"


def main():
    img = verified_wcs()
    steps = [(img[4 * k], img[4 * k + 1], img[4 * k + 2], img[4 * k + 3]) for k in range(100)]
    rows = []
    devhist = {}
    cmag0 = []
    prot1 = []
    for k, (l0, l1, l2, l3) in enumerate(steps):
        d = decode_full(l0, l1, l2, l3)
        fn, conf = func_and_conf(d, k)
        rows.append((k, (l0, l1, l2, l3), d, fn, conf))
        devhist[d["dev"]] = devhist.get(d["dev"], 0) + 1
        if d["cmag"] == 0:
            cmag0.append(k)
        if d["PROT"]:
            prot1.append(k)

    out = []
    out.append("# CONCERT WCS — full 100-step decode (verified-core source)\n")
    out.append("**Source:** `m.memory[0x4000..0x41FF]` from a boot on the VERIFIED kosarev I8080 core "
               "(`tools/boot8080.boot`), captured at mainloop. This is the authoritative WCS the hardware "
               "fetches; byte-identical to the static snapshot (confirmed by `tools/trace8080`). Generated by "
               "`tools/decode_concert_program.py`.\n")
    out.append("**Honesty contract:** the *decode* (which bits = which field) is gate-traced + POST-verified "
               "(see `224XL_provenance_ledger.md`); the *DSP role* of each step (diffuser/allpass/tank/etc.) is "
               "**UNKNOWN** — no source traces a topology, so this column says what the step MECHANICALLY does, "
               "not what musical element it is. Two honestly-open items are flagged inline: **delay magnitude** "
               "(the MI0-15→samples complement convention isn't nailed vs E91) and **PROT** (MI22 — bit verified, "
               "downstream effect unresolved).\n")
    out.append("**Confidence legend:** *decode* = field extraction; *delay-magnitude* = offset→samples; "
               "*DSP-role* = which reverb element. HIGH = gate+POST; MED = gate but convention open; "
               "UNKNOWN/UNPROVEN = no grounding.\n")

    # bit-accounting proof
    out.append("## Bit-accounting proof (all 32 microword bits)\n")
    out.append("| bits | field | in decode() | class |\n|---|---|---|---|")
    out.append("| MI0-15 | offset / I/O-command | yes (offset_field; I/O sub-decode) | verified layout |")
    out.append("| MI16 | device r/w select | yes | verified |")
    out.append("| MI17 | MEMAC | yes | verified |")
    out.append("| MI18-19 | WA | yes | verified |")
    out.append("| MI20-21 | RA | yes | verified |")
    out.append("| **MI22** | **PROT (protect)** | **NO — dropped by aru_rtl_dp.decode()** | bit verified, **function UNKNOWN** |")
    out.append("| MI23 | CSIGN (AS0-gated JK) | yes | verified |")
    out.append("| MI24 | XFER | yes | bit verified; gating untested |")
    out.append("| MI25 | ZERO | yes | verified |")
    out.append("| MI26-31 | cmag (C0-C5) | yes | verified |")
    out.append("\n> ⚠ `aru_rtl_dp.decode()` and `aru_freerun` do not surface **MI22 / PROT**. It is a real "
               "control bit (tc_U18.QC). This decode includes it so no bit is silently ignored.\n")

    # histograms
    out.append("## Summary\n")
    out.append(f"- **Device-class histogram:** " +
               ", ".join(f"{k}={v}" for k, v in sorted(devhist.items())) + ".")
    out.append("- **What the device classes are (HIGH confidence — verified device decode):** `IO` = "
               "input sampling (`RD AD/`) and DAC output (`WR DA/`) + X-reg moves; `MEMR`/`MEMW` = delay-line "
               "read/write (`addr = CPC − OFST`); `COMPUTE` = MAC-only math steps (no bus device, ARU still "
               "clocks). This is a coherent DSP structure: ~26 I/O, 33 delay accesses (25R/8W), 41 compute. "
               "What is NOT known is the *DSP topology* those pieces form (diffuser/allpass/tank) — no source "
               "traces it (provenance ledger).")
    out.append(f"- **cmag=0 steps ({len(cmag0)}):** {cmag0}")
    out.append(f"- **PROT=1 steps ({len(prot1)}):** {prot1}")
    out.append("- **cmag=0 thread (GROUNDED conclusion):** `cmag=0` disables the *multiply* for that step "
               "(the Booth array with an all-zero coefficient → product rounds to ~0; gate-faithful, though the "
               "ledger flags the cross-step accumulation as not POST-tested). The step's *bus action still "
               "happens* — a `cmag=0` MEMR still reads DMEM and writes its regfile target. So cmag=0 is a "
               "'multiply-off' modifier, not a dead step.")
    out.append("- **PROT correlation (OBSERVED, role still UNKNOWN):** `PROT=1` occurs almost exclusively on "
               "the steps 5-22 block (the 19 identical `0x1AB3`/cmag=0 MEMR reads) plus steps 2, 4, 25, 55. So "
               "PROT marks that contiguous repeated-read block. HYPOTHESIS (NOT verified — needs the tc_U18.QC "
               "downstream trace): PROT may gate a DRAM-refresh / write-inhibit mode, making steps 5-22 a "
               "refresh sweep rather than signal taps. Do NOT assert this until the gate is traced.\n")

    # the table
    out.append("## Per-step table\n")
    out.append("| # | raw l0 l1 l2 l3 | decode (all 32 bits) | function (mechanism; role=UNKNOWN) | confidence |")
    out.append("|---|---|---|---|---|")
    for k, (l0, l1, l2, l3), d, fn, conf in rows:
        raw = f"{l0:02X} {l1:02X} {l2:02X} {l3:02X}"
        dec = (f"{d['dev']}"
               + (f" off=0x{d['offset_field']:04X}" if d["dev"] in ("MEMR", "MEMW") else "")
               + (f" rd={d['io_read']} wrDA={int(d['wr_da'])}{('('+'+'.join(d['da_chans'])+')') if d['wr_da'] else ''} wrX={int(d['wr_xreg'])}" if d["dev"] == "IO" else "")
               + f" · WA{d['WA']} RA{d['RA']} cmag{d['cmag']} CS{d['CSIGN']} X{d['XFER']} Z{d['ZERO']} PROT{d['PROT']}")
        out.append(f"| {k} | {raw} | {dec} | {fn} | {conf} |")

    out.append("\n## Open items this table makes explicit\n")
    out.append("1. **PROT (MI22)** — set on a subset of steps; downstream effect not traced. Could gate "
               "DMEM-write-protect or refresh. Needs the T&C sheet trace of tc_U18.QC's load.")
    out.append("2. **Delay magnitude** — offset_field is exact; the field→samples conversion depends on the "
               "MI0-15 complement convention (hardware complements MI→OFST/ per SM §3.6, giving addr=CPC−field; "
               "but `encode_step` stores the complement, the opposite convention). Nail vs E91 before trusting any "
               "delay-in-seconds.")
    out.append("3. **DSP role** — deliberately blank. Assigning diffuser/allpass/tank requires a traced "
               "read→MAC→write topology, which does not exist (provenance ledger).")
    out.append("4. **cmag=0** — multiply-disable is gate-faithful; the *purpose* of the cmag=0 bus-move steps "
               "is unresolved.\n")

    with open(OUTDOC, "w", encoding="utf-8") as f:
        f.write("\n".join(out) + "\n")
    print(f"wrote {OUTDOC}")
    print(f"device histogram: {devhist}")
    print(f"cmag=0 steps ({len(cmag0)}): {cmag0}")
    print(f"PROT=1 steps ({len(prot1)}): {prot1}")


if __name__ == "__main__":
    main()
