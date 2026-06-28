#!/usr/bin/env python3
"""Render 224XL timing_spec.json -> (a) round-trip waveform PNGs and (b) the markdown spec.

Single source of truth = timing_spec.json. This script is the ONLY producer of both the human doc
and the verification waveforms, so they cannot drift. To error-proof a transcription: edit the JSON,
re-run this, and lay the rendered PNG next to the original Service-Manual figure (figs 3.2-3.6).

Usage:
  python render_timing.py [--json PATH] [--pngdir DIR] [--md PATH]

wave tokens (one per grid column): 0 low | 1 high | . hold-prev | p clock-pulse |
  = valid/data box (label from data[]) | x invalid/unspecified | z hi-Z
"""
import json, os, argparse
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle

HERE = os.path.dirname(os.path.abspath(__file__))

def resolve(wave, data):
    """Return list of cells: each dict {kind,level,label}. kind in {lvl,clk,box,inv,hiz}."""
    cells = []
    di = 0
    prev = {"kind": "lvl", "level": 0, "label": None, "boxhead": True}
    for ch in wave:
        if ch == ".":
            c = dict(prev); c["boxhead"] = False
        elif ch in "01":
            c = {"kind": "lvl", "level": int(ch), "label": None, "boxhead": True}
        elif ch in "pP":
            c = {"kind": "clk", "level": 0, "label": None, "boxhead": True}
        elif ch == "=":
            lbl = data[di] if data and di < len(data) else ""
            di += 1
            c = {"kind": "box", "level": None, "label": lbl, "boxhead": True}
        elif ch == "x":
            c = {"kind": "inv", "level": None, "label": None, "boxhead": True}
        elif ch == "z":
            c = {"kind": "hiz", "level": None, "label": None, "boxhead": True}
        else:
            c = {"kind": "lvl", "level": 0, "label": None, "boxhead": True}
        cells.append(c); prev = c
    return cells

def draw_bus(ax, cells, y0, ylo, yhi, data):
    """Render a multi-bit BUS as a data-valid band: parallel top/bottom lines when valid
    ('=' cells), a single mid-line when changing/invalid ('x' cells), with opening/closing
    wedges (the data-valid crossover) at each transition. No logic level is implied."""
    yb, yt, ym = y0 + ylo, y0 + yhi, y0 + (ylo + yhi) / 2.0
    valid = [c["kind"] == "box" for c in cells]
    n = len(cells)
    w = 0.16
    for i in range(n):
        if valid[i]:
            l = i + (w if (i == 0 or not valid[i - 1]) else 0)
            r = (i + 1) - (w if (i == n - 1 or not valid[i + 1]) else 0)
            ax.plot([l, r], [yt, yt], color="black", lw=1.2)
            ax.plot([l, r], [yb, yb], color="black", lw=1.2)
        else:
            ax.plot([i, i + 1], [ym, ym], color="black", lw=1.1)
    for i in range(n + 1):
        L = valid[i - 1] if i - 1 >= 0 else False
        R = valid[i] if i < n else False
        if (not L) and R:                       # opening wedge "<"
            ax.plot([i, i + w], [ym, yt], color="black", lw=1.0)
            ax.plot([i, i + w], [ym, yb], color="black", lw=1.0)
        elif L and (not R):                     # closing wedge ">"
            ax.plot([i - w, i], [yt, ym], color="black", lw=1.0)
            ax.plot([i - w, i], [yb, ym], color="black", lw=1.0)
    # label centered in the longest valid run
    best = (0, 0, 0)
    i = 0
    while i < n:
        if valid[i]:
            j = i
            while j < n and valid[j]:
                j += 1
            if j - i > best[0]:
                best = (j - i, i, j)
            i = j
        else:
            i += 1
    if best[0] and data:
        ax.text((best[1] + best[2]) / 2.0, ym, data[0], va="center", ha="center", fontsize=7.5)


def draw_figure(fig_spec, path):
    sigs = fig_spec["signals"]
    grid = fig_spec["grid"]
    N = len(grid)
    H = len(sigs)
    fig, ax = plt.subplots(figsize=(max(8, N * 1.25), max(3, H * 0.62)))
    ylo, yhi, rowh = 0.28, 0.72, 1.0
    for r, s in enumerate(sigs):
        y0 = (H - 1 - r) * rowh
        cells = resolve(s["wave"], s.get("data"))
        if s.get("kind") == "bus-valid":
            draw_bus(ax, cells, y0, ylo, yhi, s.get("data"))
            conf = s.get("conf", "")
            mark = {"high": "", "med": "  ~", "low": "  ??"}.get(conf, "")
            ax.text(-0.15, y0 + 0.5, s["name"] + mark, va="center", ha="right", fontsize=9)
            continue
        # baseline level for vertical-edge tracking
        prev_top = None
        for i, c in enumerate(cells):
            x0, x1 = i, i + 1
            if c["kind"] == "lvl":
                yy = y0 + (yhi if c["level"] else ylo)
                ax.plot([x0, x1], [yy, yy], color="black", lw=1.4)
                if prev_top is not None and abs(prev_top - yy) > 1e-6:
                    ax.plot([x0, x0], [prev_top, yy], color="black", lw=1.4)
                prev_top = yy
            elif c["kind"] == "clk":
                yb = y0 + ylo; yt = y0 + yhi
                # 50%-duty tick whose RISING edge sits ON the cell boundary (the MS edge),
                # since the clock edge is what defines the state transition. high x0..x0+0.5, low to x1.
                ax.plot([x0, x0, x0 + .5, x0 + .5, x1],
                        [yb, yt, yt, yb, yb], color="black", lw=1.2)
                prev_top = yb
            elif c["kind"] == "box":
                ax.plot([x0, x1], [y0 + yhi, y0 + yhi], color="black", lw=1.2)
                ax.plot([x0, x1], [y0 + ylo, y0 + ylo], color="black", lw=1.2)
                if c["boxhead"]:
                    ax.plot([x0, x0], [y0 + ylo, y0 + yhi], color="black", lw=1.2)  # left edge
                    # span = this head + following continuation cells -> center the label
                    j = i + 1
                    while j < len(cells) and cells[j]["kind"] == "box" and not cells[j]["boxhead"]:
                        j += 1
                    if c["label"]:
                        ax.text((i + j) / 2.0, y0 + 0.5, c["label"], va="center", ha="center",
                                fontsize=7.5)
                # close the right edge if the next cell is not a box continuation
                nxt = cells[i + 1] if i + 1 < len(cells) else None
                if nxt is None or nxt["kind"] != "box" or nxt["boxhead"]:
                    ax.plot([x1, x1], [y0 + ylo, y0 + yhi], color="black", lw=1.2)
                prev_top = None
            elif c["kind"] == "inv":
                ax.add_patch(Rectangle((x0, y0 + ylo), 1, yhi - ylo, facecolor="0.85",
                                       edgecolor="0.6", lw=0.6))
                prev_top = None
            elif c["kind"] == "hiz":
                ym = y0 + 0.5
                ax.plot([x0, x1], [ym, ym], color="0.5", lw=1.0, ls="--")
                prev_top = None
        # signal label + conf
        conf = s.get("conf", "")
        mark = {"high": "", "med": "  ~", "low": "  ??"}.get(conf, "")
        ax.text(-0.15, y0 + 0.5, s["name"] + mark, va="center", ha="right", fontsize=9)
    # grid columns
    for i in range(N + 1):
        ax.plot([i, i], [-0.1, H * rowh - 0.1], color="0.85", lw=0.6, zorder=0)
    for i, g in enumerate(grid):
        ax.text(i + 0.5, H * rowh - 0.02, g, va="bottom", ha="center", fontsize=8, color="0.3")
    ax.set_xlim(-2.2, N + 0.1); ax.set_ylim(-0.2, H * rowh + 0.25)
    ax.axis("off")
    ax.set_title(f'{fig_spec["id"]}: {fig_spec["title"]}   (round-trip of {fig_spec["src"]})',
                 fontsize=10, loc="left")
    fig.tight_layout()
    fig.savefig(path, dpi=120, bbox_inches="tight")
    plt.close(fig)

def cell_token(c):
    if c["kind"] == "lvl": return "1" if c["level"] else "0"
    if c["kind"] == "clk": return "⎍"
    if c["kind"] == "box": return c["label"] if c["boxhead"] and c["label"] else "→"
    if c["kind"] == "inv": return "·"
    if c["kind"] == "hiz": return "Z"
    return "?"

def emit_md(spec, md_path, pngdir):
    L = []
    L.append("# 224XL — timing spec (figs 3.2–3.6), MS/AS/step-grid form\n")
    L.append("> **GENERATED from `tools/timing/timing_spec.json` by `tools/timing/render_timing.py` — do not hand-edit.**")
    L.append("> Edit the JSON and re-run the renderer (it also emits round-trip waveform PNGs to lay beside the")
    L.append("> original Service-Manual figures). Everything is quantized to each figure's discrete grid")
    L.append("> (MS-state / AS-state / sample-step); nanosecond values are annotations only.\n")
    L.append("**Cell tokens:** `0`/`1` level · `⎍` clock pulse · `·` invalid/unspecified · `Z` hi-Z · "
             "a label = start of a valid/data box, `→` = box continues. **Conf:** signal name suffix "
             "`~`=medium, `??`=low (else high).\n")
    L.append("**value_source** distinguishes *fixed-cadence* signals (pure timing — fully specified here) "
             "from *microword-decoded* signals (timing here, but their VALUE each step comes from the decode "
             "map — NOT derivable from a timing diagram).\n")
    for f in spec["figures"]:
        L.append(f'\n## {f["id"]} — {f["title"]}')
        L.append(f'*Source figure:* `{f["src"]}` · *round-trip render:* `{f["id"]}.png`\n')
        L.append(f'> {f["grid_note"]}\n')
        grid = f["grid"]
        # grid table
        L.append("| signal | " + " | ".join(grid) + " |")
        L.append("|" + "---|" * (len(grid) + 1))
        for s in f["signals"]:
            cells = resolve(s["wave"], s.get("data"))
            toks = [cell_token(c) for c in cells]
            toks += [""] * (len(grid) - len(toks))
            nm = s["name"] + {"high": "", "med": " ~", "low": " ??"}.get(s.get("conf"), "")
            L.append(f'| {nm} | ' + " | ".join(toks) + " |")
        # catalog
        L.append("\n**Signal catalog:**\n")
        L.append("| signal | module | kind | value_source | conf | note |")
        L.append("|---|---|---|---|---|---|")
        for s in f["signals"]:
            L.append(f'| {s["name"]} | {s.get("src_mod","")} | {s.get("kind","")} | '
                     f'{s.get("value_source","")} | {s.get("conf","")} | {s.get("note","")} |')
    L.append("\n---\n## Global signal catalog — fixed-cadence vs microword-decoded\n")
    L.append("The model generates **fixed-cadence** signals straight from the MS/AS counters; "
             "**microword-decoded** signals need the decode map (their timing is here, their value is not).\n")
    L.append("| signal | figure | fixed-cadence? | value_source |")
    L.append("|---|---|---|---|")
    seen = set()
    for f in spec["figures"]:
        for s in f["signals"]:
            key = s["name"]
            vs = s.get("value_source", "")
            # authoritative per-signal flag (set in the JSON), NOT a value_source keyword guess
            fixed = "yes" if s.get("fixed") else "**NO (decode)**"
            seen.add(key)
            L.append(f'| {s["name"]} | {f["id"]} | {fixed} | {vs} |')
    open(md_path, "w", encoding="utf-8").write("\n".join(L) + "\n")

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--json", default=os.path.join(HERE, "timing_spec.json"))
    ap.add_argument("--pngdir", default=os.path.join(HERE, "renders"))
    ap.add_argument("--md", default=os.path.join(HERE, "..", "..", "docs", "reference", "224",
                                                  "224XL_timing_spec.md"))
    a = ap.parse_args()
    spec = json.load(open(a.json, encoding="utf-8"))
    os.makedirs(a.pngdir, exist_ok=True)
    for f in spec["figures"]:
        draw_figure(f, os.path.join(a.pngdir, f["id"] + ".png"))
    emit_md(spec, os.path.abspath(a.md), a.pngdir)
    print("rendered", len(spec["figures"]), "figures ->", a.pngdir)
    print("md ->", os.path.abspath(a.md))

if __name__ == "__main__":
    main()
