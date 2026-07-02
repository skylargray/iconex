#!/usr/bin/env python3
"""F4a (plan 024) — pages 2-5 display calibration WITH the display page set by the real
LARC PAGE key (0x3E), fixing the 0027 E3a wrinkle: writing the apply-page byte 0x3C34
alone moves the APPLY page but not the DISPLAY page (registry #33), so 0027's page 2-5
sweeps rendered with PAGE-1 formatters. Here: press PAGE until the parsed display legend
shows the target page ("PAGE n"), THEN run the ascend-then-descend calibration per slider
(soft takeover, registry #32) exactly as e3_display_calibration did for page 1.

Per slider the probe also records the firmware's own value-formatter LABEL (via the
param-select keys 0x23/0x27/0x2B/0x2F/0x33/0x37, which display without touching), the
recalled preset byte (flat array 0x3CA3 + apply_page*6 + slider, apply_page = the
OBSERVED 0x3C34 after the PAGE press, slots snapshotted at BOOT — the live slots mutate
as sweeps apply) and its render, and runs two consistency checks: (a) the descending
curve is monotonic where numeric (corner-formatter rows are unit-normalized — sub-1k
values render 'nnn   HZ' inside a KHZ ladder), (b) injecting the preset byte
post-pickup re-displays the recalled-preset value.

Measured wrinkles the first run pinned (recorded in the affected records' notes):
- display page 5 pairs with apply-page byte 0x3C34 = 5 — the PAGE key SKIPS apply
  page 4 on CONCERT B1P1 (refines registry #33);
- page-4 ascending slider writes render exactly 25 slider-bytes LOW vs descending
  writes at the same byte (both page-4 formatters); the DOWN pass is the calibration;
- the page-4 select renders (preset values 5.00/9.75/17.5/25.0/0.36/10.2 MSEC) are
  NOT on the slider formatter's byte grid — the recalled preset store is finer than
  (or different from) the slider byte scale.

Merges into display_map.json under the same p{page}s{slider} keys; the page-1 entries
are preserved byte-for-byte (asserted after the merge). Bank wrinkle recorded, not
fixed: banks B2/B3 label slider 5 "ATT" (bank-dependent legends; this calibration is
B1P1 CONCERT only — see program_names.json).
"""
import sys, os, json, re, time, copy

TOOLS = r"d:\OneDrive\Gray Instruments\iconex\tools"
sys.path.insert(0, TOOLS)
HERE = os.path.dirname(os.path.abspath(__file__))
CACHE = os.path.join(HERE, "display_map.json")

import boot8080
from probe_run import run_ticks
from e4_variations import SerialIO, send_key

# e3 naming kept for record compatibility; 'label' carries the firmware's own text.
PAGES = {
    2: ["LF Stop", "Mid Stop", "Chorus", "HF Bwidth", "Diffusion", "Definition"],
    3: ["PE1 Level", "PE2 Level", "PE3 Level", "PE4 Level", "sl5", "sl6"],
    4: ["PE1 Delay", "PE2 Delay", "PE3 Delay", "PE4 Delay", "FinePD L", "FinePD R"],
    5: ["Size", "sl2", "Gate", "sl4", "sl5", "sl6"],
}
UP = [0x02, 0x20, 0x40, 0x60, 0x80, 0xA0, 0xC0, 0xE0, 0xFE]        # pickup pass
DOWN = [0xF8, 0xF0, 0xE0, 0xD0, 0xC0, 0xB0, 0xA0, 0x90, 0x80, 0x70, 0x60, 0x50,
        0x40, 0x30, 0x20, 0x18, 0x10, 0x08, 0x02]                  # post-pickup f(byte)
SETTLE = 3_000_000
PAGEKEY = 0x3E
SELKEYS = [0x23, 0x27, 0x2B, 0x2F, 0x33, 0x37]                     # sliders 1..6
PRESET_BASE = 0x3CA3                                               # + page0*6 + slider


def disp_val(m):
    """The e3 value-field convention (25 chars at the buffer start)."""
    b = bytes(m.memory[0x3F4F:0x3F68])
    return "".join(chr(c & 0x7F) if 32 <= (c & 0x7F) < 127 else " " for c in b).rstrip()


def disp_full(m):
    """Whole 48-char line: 12 name + 12 header + 24 legend (key_map geometry)."""
    b = bytes(m.memory[0x3F4F:0x3F7F])
    return "".join(chr(c & 0x7F) if 32 <= (c & 0x7F) < 127 else " " for c in b)


def page_of(full):
    g = re.search(r"PAGE\s*(\d)", full)
    if g:
        return int(g.group(1))
    if re.search(r"B\d\s*P\d\s*V\d", full):                        # home banner = page 1
        return 1
    return None


def full_tok(line):
    """Value token of a FULL label render (label cols 0-11, value field cols 12-17)."""
    t = line[12:18].split()
    return t[0] if t else None


def sweep_tok(line, label):
    """Value token of a sweep render: in-place value field (cols 0-5), or a full
    re-render of the same label."""
    if label and line[:12].rstrip() == label:
        return full_tok(line)
    t = line[:6].split()
    return t[0] if t else None


def num(tok):
    try:
        return float(tok)
    except (TypeError, ValueError):
        return None


def unit_of(select_disp):
    """The unit token of the full select render (e.g. SEC / KHZ / MSEC / METERS)."""
    toks = select_disp.split()
    return toks[-1] if toks and toks[-1].isalpha() else None


def norm_num(line, label, unit):
    """Numeric value for the monotonic check, unit-normalized: the corner-frequency
    ladder renders sub-1-kHz values as 'nnn   HZ' inside a KHZ-labeled range."""
    v = num(sweep_tok(line, label))
    if v is None:
        return None
    if unit == "KHZ" and not re.match(r"^\s*\d+\s+HZ\b", line):
        v *= 1000.0
    return v


def monotonic(vals):
    """True iff the numeric sequence is monotone (either direction; flats allowed)."""
    v = [x for x in vals if x is not None]
    if len(v) < 3:
        return None
    return all(a >= b for a, b in zip(v, v[1:])) or all(a <= b for a, b in zip(v, v[1:]))


def goto_page(m, io, target, log):
    """Press PAGE until the display legend shows the target page. Returns the landing
    full line, or None on contradiction (evidence in log)."""
    for attempt in range(8):
        full = disp_full(m)
        p = page_of(full)
        log.append(f"   page_of({full!r}) = {p}")
        if p == target:
            return full
        send_key(m, io, PAGEKEY)
        full2 = disp_full(m)
        if page_of(full2) is None:                     # press didn't render a page banner
            run_ticks(m, 500_000)                      # the caution's timing recheck
            full2 = disp_full(m)
            log.append(f"   (+500k recheck) {full2!r}")
    return None


def main():
    print("F4a — pages 2-5 display calibration via the PAGE key (plan 024)", flush=True)
    merged = json.load(open(CACHE))
    p1_snapshot = copy.deepcopy({k: v for k, v in merged.items() if k.startswith("p1")})

    print("booting CONCERT to mainloop + settle ...", flush=True)
    t0 = time.time()
    m, ms = boot8080.boot(verbose=False, extra_ticks_after_mainloop=6_000_000)
    assert "mainloop" in ms
    io = SerialIO(m)
    print(f"boot {time.time()-t0:.0f}s; settled display: {disp_full(m)!r}", flush=True)
    # snapshot the RECALLED preset slots at boot — the live slots mutate as sweeps apply
    preset_blk = bytes(m.memory[0x3CA3:0x3CC7])                    # apply pages 0..5
    print("recalled param block 0x3CA3..0x3CC6:", preset_blk.hex(), flush=True)

    checks = []
    for page in (2, 3, 4, 5):
        log = []
        landing = goto_page(m, io, page, log)
        if landing is None:
            print(f"!! CONTRADICTION: PAGE key never reached page {page}; evidence:")
            for line in log:
                print(line)
            print("!! aborting the remaining pages (per plan-024 caution).")
            break
        legend = landing[24:].rstrip()
        page34 = m.memory[0x3C34]
        print(f"\n### page {page}: landed {landing!r}  legend={legend!r} "
              f"0x3C34={page34} (expect {page-1})", flush=True)

        for sl in range(6):
            key = f"p{page}s{sl+1}"
            t1 = time.time()
            slot = page34 * 6 + sl                     # OBSERVED apply page (page 5 -> 5)
            preset_byte = preset_blk[slot] if slot < len(preset_blk) else 0

            send_key(m, io, SELKEYS[sl])               # display-only: the preset render
            sel = disp_val(m)
            label = sel[:12].rstrip() if sel[:1].isalpha() else None
            tok_sel = full_tok(sel)
            unit = unit_of(sel)

            up, down = [], []
            sweep_label = None
            for v in UP:
                m.memory[0x3C00 + sl] = v
                run_ticks(m, SETTLE)
                txt = disp_val(m)
                up.append((v, txt))
                if txt[:1].isalpha() and txt[:12].rstrip() not in (label, sweep_label):
                    sweep_label = txt[:12].rstrip()
            for v in DOWN:
                m.memory[0x3C00 + sl] = v
                run_ticks(m, SETTLE)
                down.append((v, disp_val(m)))

            if preset_byte == DOWN[-1]:                # nudge so the write is a change
                m.memory[0x3C00 + sl] = 0x08
                run_ticks(m, SETTLE)
            m.memory[0x3C00 + sl] = preset_byte
            run_ticks(m, SETTLE)
            chk = disp_val(m)
            tok_chk = sweep_tok(chk, label)

            mono = monotonic([norm_num(t, label, unit) for _, t in down])
            preset_ok = (tok_chk == tok_sel) if (tok_chk and tok_sel) else None

            note = ("F4a plan024: display page set via PAGE key 0x3E before the sweep "
                    "(0027's p2-p5 data used page-1 formatters). B1P1 CONCERT; banks "
                    "B2/B3 label slider 5 ATT (bank-dependent legends, not covered). "
                    "preset_byte = boot-recalled slot 0x3CA3+apply_page34*6+slider.")
            if page == 4:
                note += (" MEASURED page-4 wrinkle: ascending slider writes render "
                         "exactly 25 slider-bytes LOW vs descending writes at the same "
                         "byte (up(b)==down(b-25), both formatters) — the DOWN pass is "
                         "the calibration; and the select-render preset values are NOT "
                         "on the slider byte grid (finer preset store). preset_ok=False "
                         "reflects those two measured facts, not a formatter error.")
            if page == 5:
                note += (" MEASURED page-5 wrinkle: display page 5 pairs with apply-page "
                         "byte 0x3C34=5 — the PAGE key SKIPS apply page 4 on CONCERT "
                         "(refines registry #33); the apply-5 recalled slots read 0x00 "
                         "and SIZE's select render (40 METERS = f(0xF8..)) matches no "
                         "flat-array slot — the page-5 preset storage is unresolved.")

            merged[key] = dict(
                name=PAGES[page][sl], label=label, legend=legend,
                display_page=page, apply_page34=page34,
                select_display=sel, preset_byte=preset_byte,
                preset_slot=hex(PRESET_BASE + slot),
                preset_check=[preset_byte, chk], preset_ok=preset_ok,
                monotonic=mono, up=up, down=down, note=note)
            if sweep_label:
                merged[key]["sweep_label"] = sweep_label
            json.dump(merged, open(CACHE, "w"), indent=1)

            checks.append((key, label, preset_byte, tok_sel, tok_chk, preset_ok, mono))
            print(f"[{key}] label={label!r} preset 0x{preset_byte:02X}->{tok_sel!r} "
                  f"(check {tok_chk!r} ok={preset_ok}) mono={mono} "
                  f"({time.time()-t1:.0f}s)", flush=True)
            for v, txt in down:
                print(f"   0x{v:02X}: {txt!r}")

    # return the display to page 1 (home) for cleanliness
    log = []
    goto_page(m, io, 1, log)

    # verify the merge preserved page 1 byte-for-byte
    reread = json.load(open(CACHE))
    p1_after = {k: v for k, v in reread.items() if k.startswith("p1")}
    assert p1_after == p1_snapshot, "page-1 entries changed — MERGE BUG"
    print("\npage-1 entries preserved byte-for-byte: OK", flush=True)

    print("\n### consistency summary (byte -> value: endpoints + interior) ###")
    print(f"{'key':6} {'label':13} {'preset':>13} {'ok':>5} {'mono':>5}   curve (DOWN)")
    for key, label, pb, ts, tc, ok, mono in checks:
        rec = reread[key]
        lab = rec.get("label")
        pts = []
        for want in (0xF8, 0xC0, 0x80, 0x40, 0x02):
            for v, txt in rec["down"]:
                if v == want:
                    pts.append(f"0x{v:02X}->{sweep_tok(txt, lab) or '?'}")
                    break
        print(f"{key:6} {str(label):13} 0x{pb:02X}->{str(ts):7} {str(ok):>5} "
              f"{str(mono):>5}   " + "  ".join(pts))
    print(f"\ncached -> {CACHE}")


if __name__ == "__main__":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass
    main()
