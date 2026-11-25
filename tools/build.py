"""Generate the profile SVGs into the profile repo's assets folder.

Usage (from the tools folder): python3 build.py ..
"""
import random
import sys
from pathlib import Path

from content import CONTENT
from svgkit import (BRONZE, BRONZE_LT, FOAM, GOLD, LAKE, LAKE_DEEP, LAKE_LINE, MIST,
                    SILVER, SVG)

REDUCED = "@media (prefers-reduced-motion:reduce){.p{animation-play-state:paused!important}}"


# --------------------------------------------------------------------------- hero
def hero(c):
    W, H = 1200, 340
    s = SVG(W, H, c["title"], c["desc"])
    s.add(f'<rect width="{W}" height="{H}" rx="20" fill="{LAKE}"/>')

    # left column: identity
    x = 64
    s.text(x, 96, c["location"], "PPTextMed", 18, fill=MIST)
    s.text(x - 3, 184, c["name"], "PPDisplay", 86, fill=FOAM, letter_spacing=-1.5)
    s.text(x, 236, c["sub"][0], "PPText", 25, fill=FOAM, opacity=0.92)
    s.text(x, 270, c["sub"][1], "PPText", 25, fill=FOAM, opacity=0.92)

    # right column: medallion flow
    x0, x1 = 748, 1144
    seg = (x1 - x0) / 3
    top, bot = 70, 262
    bx, sx, gx = x0, x0 + seg, x0 + 2 * seg

    # faint layer bands, each a little lighter: data gets refined left to right
    for i, col in enumerate([BRONZE, SILVER, GOLD]):
        s.add(f'<rect x="{x0 + i * seg + 2:.1f}" y="{top}" width="{seg - 4:.1f}" '
              f'height="{bot - top}" rx="10" fill="{col}" opacity="0.06"/>')
    for i, (label, col) in enumerate(zip(c["layers"], [BRONZE_LT, SILVER, GOLD])):
        s.text(x0 + i * seg + seg / 2, bot + 34, label, "PPTextMed", 16, fill=col, anchor="middle")

    rnd = random.Random(7)
    css = []
    # bronze: irregular shards, wobbling
    for k in range(3):
        a, b, c3 = (rnd.choice([-1, 1]) * rnd.uniform(6, 12) for _ in range(3))
        css.append(
            f"@keyframes b{k}{{0%{{transform:translate(0,0);opacity:0}}"
            f"12%{{opacity:1}}"
            f"33%{{transform:translate({seg * .33:.0f}px,{a:.0f}px)}}"
            f"66%{{transform:translate({seg * .66:.0f}px,{b:.0f}px)}}"
            f"88%{{opacity:1}}"
            f"100%{{transform:translate({seg:.0f}px,{c3:.0f}px);opacity:0}}}}"
        )
    css.append(f"@keyframes sv{{0%{{transform:translateX(0);opacity:0}}12%{{opacity:1}}"
               f"88%{{opacity:1}}100%{{transform:translateX({seg:.0f}px);opacity:0}}}}")
    css.append(".p{animation-timing-function:linear;animation-iteration-count:infinite}")
    s.css.extend(css)

    parts = []
    for i in range(24):
        y = rnd.uniform(top + 18, bot - 18)
        w, h = rnd.uniform(5, 13), rnd.uniform(3.5, 9)
        rot = rnd.uniform(0, 90)
        dur = rnd.uniform(4.6, 6.2)
        delay = -rnd.uniform(0, dur)
        op = rnd.uniform(0.55, 1)
        k = i % 3
        parts.append(
            f'<g transform="translate({bx + 6:.1f},{y:.1f})">'
            f'<g class="p" style="animation-name:b{k};animation-duration:{dur:.2f}s;'
            f'animation-delay:{delay:.2f}s">'
            f'<rect x="{-w / 2:.1f}" y="{-h / 2:.1f}" width="{w:.1f}" height="{h:.1f}" '
            f'fill="{BRONZE}" opacity="{op:.2f}" transform="rotate({rot:.0f})"/></g></g>'
        )
    # silver: aligned dashes in five lanes
    lanes = [102, 134, 166, 198, 230]
    dur = 3.4
    for li, y in enumerate(lanes):
        n = 3
        for j in range(n):
            delay = -(dur / n) * j - li * 0.37
            parts.append(
                f'<g transform="translate({sx + 4:.1f},{y})">'
                f'<g class="p" style="animation-name:sv;animation-duration:{dur}s;'
                f'animation-delay:{delay:.2f}s">'
                f'<rect x="0" y="-1.5" width="14" height="3" rx="1.5" fill="{SILVER}"/></g></g>'
            )
    # gold: uniform dots in three lanes
    lanes = [134, 166, 198]
    dur = 2.8
    for li, y in enumerate(lanes):
        n = 4
        for j in range(n):
            delay = -(dur / n) * j - li * 0.23
            parts.append(
                f'<g transform="translate({gx + 8:.1f},{y})">'
                f'<g class="p" style="animation-name:sv;animation-duration:{dur}s;'
                f'animation-delay:{delay:.2f}s">'
                f'<circle r="3.6" fill="{GOLD}"/></g></g>'
            )
    s.add("".join(parts))
    s.css.append(REDUCED)
    return s


# -------------------------------------------------------------------------- about
def about(c):
    W = 1000
    rows = c["rows"]
    row_h = 40
    table_top = 300
    H = table_top + row_h * (len(rows) + 1) + 40
    s = SVG(W, H, c["title"], c["desc"])
    s.add(f'<rect width="{W}" height="{H}" rx="16" fill="{LAKE}"/>')
    # tab strip
    s.add(f'<path d="M0 16 a16 16 0 0 1 16 -16 h{W - 32} a16 16 0 0 1 16 16 v36 h-{W} z" '
          f'fill="{LAKE_DEEP}"/>')
    tw = s.width(c["tab"], "PPMono", 15) + 36
    s.add(f'<rect x="24" y="12" width="{tw:.0f}" height="40" rx="8" fill="{LAKE}"/>')
    s.text(42, 38, c["tab"], "PPMono", 15, fill=FOAM, opacity=0.85)

    code = [
        [(c["comment"], MIST)],
        [("SELECT", GOLD), (" *", FOAM)],
        [("FROM", GOLD), ("   gold.engineers", FOAM)],
        [("WHERE", GOLD), ("  github_user ", FOAM), ("=", MIST), (" 'PabloPerezTI'", BRONZE_LT),
         (";", MIST)],
    ]
    y = 98
    for i, line in enumerate(code, 1):
        s.text(40, y, str(i), "PPMono", 17, fill=MIST, opacity=0.5, anchor="end",
               extra='dx="8"')
        s.spans(76, y, line, "PPMono", 19)
        y += 34
    s.add(f'<line x1="0" x2="{W}" y1="{y - 8}" y2="{y - 8}" stroke="{LAKE_LINE}"/>')
    s.text(40, y + 34, c["result"], "PPTextMed", 15, fill=MIST)

    # result table
    tx0, tx1, col2 = 40, W - 40, 300
    ty = table_top
    s.add(f'<rect x="{tx0}" y="{ty}" width="{tx1 - tx0}" height="{row_h}" rx="6" '
          f'fill="{LAKE_DEEP}"/>')
    s.text(tx0 + 20, ty + 26, c["head"][0], "PPTextMed", 15, fill=MIST)
    s.text(col2, ty + 26, c["head"][1], "PPTextMed", 15, fill=MIST)
    for i, (k, v) in enumerate(rows):
        ry = ty + row_h * (i + 1)
        s.text(tx0 + 20, ry + 26, k, "PPMono", 16.5, fill=SILVER)
        s.text(col2, ry + 27, v, "PPText", 18.5, fill=FOAM)
        if i < len(rows) - 1:
            s.add(f'<line x1="{tx0}" x2="{tx1}" y1="{ry + row_h}" y2="{ry + row_h}" '
                  f'stroke="{LAKE_LINE}" stroke-width="1"/>')
    s.add(f'<line x1="{col2 - 20}" x2="{col2 - 20}" y1="{ty}" y2="{ty + row_h * (len(rows) + 1)}" '
          f'stroke="{LAKE_LINE}"/>')
    return s


# ----------------------------------------------------------------- project cards
def _chips(s, x, y, tags, max_x):
    cx, cy = x, y
    for t in tags:
        w = s.width(t, "PPTextMed", 14) + 26
        if cx + w > max_x:
            cx = x
            cy += 38
        s.add(f'<rect x="{cx:.1f}" y="{cy}" width="{w:.1f}" height="28" rx="14" fill="none" '
              f'stroke="{MIST}" stroke-opacity="0.45"/>')
        s.text(cx + w / 2, cy + 19, t, "PPTextMed", 14, fill=FOAM, anchor="middle", opacity=0.9)
        cx += w + 8
    return cy


def _node(s, x, y, w, label, stroke, fill="none", text_fill=FOAM):
    s.add(f'<rect x="{x:.1f}" y="{y}" width="{w:.1f}" height="30" rx="8" fill="{fill}" '
          f'stroke="{stroke}" stroke-opacity="0.9"/>')
    s.text(x + w / 2, y + 20, label, "PPTextMed", 13.5, fill=text_fill, anchor="middle")


def _arrow(s, x1, x2, y, color=MIST):
    s.add(f'<line x1="{x1:.1f}" x2="{x2 - 5:.1f}" y1="{y}" y2="{y}" stroke="{color}" '
          f'stroke-opacity="0.7" stroke-width="1.5"/>'
          f'<path d="M{x2 - 6:.1f} {y - 4} L{x2:.1f} {y} L{x2 - 6:.1f} {y + 4}" fill="none" '
          f'stroke="{color}" stroke-opacity="0.7" stroke-width="1.5"/>')


def project_card(c, kind):
    W, H = 600, 380
    pad = 36
    s = SVG(W, H, c["title"], " ".join(c["desc"]))
    s.add(f'<rect width="{W}" height="{H}" rx="16" fill="{LAKE}"/>')

    # status, top right
    sw = s.width(c["status"], "PPTextMed", 14)
    dot = GOLD if kind == "lakehouse" else SILVER
    s.add(f'<circle cx="{W - pad - sw - 12:.1f}" cy="{pad + 9}" r="4" fill="{dot}"/>')
    s.text(W - pad, pad + 14, c["status"], "PPTextMed", 14, fill=MIST, anchor="end")

    # mini architecture diagram
    d = c["diagram"]
    y = pad + 30
    if kind == "lakehouse":
        src_w = 74
        _node(s, pad, y - 20, src_w, d[0], MIST)
        _node(s, pad, y + 20, src_w, d[1], MIST)
        mx = pad + src_w
        # merge lines
        s.add(f'<path d="M{mx} {y - 5} C{mx + 22} {y - 5} {mx + 18} {y + 15} {mx + 40} {y + 15}" '
              f'fill="none" stroke="{MIST}" stroke-opacity="0.7" stroke-width="1.5"/>'
              f'<path d="M{mx} {y + 35} C{mx + 22} {y + 35} {mx + 18} {y + 15} {mx + 40} {y + 15}" '
              f'fill="none" stroke="{MIST}" stroke-opacity="0.7" stroke-width="1.5"/>')
        bx = mx + 46
        nw = 80
        for i, (label, col) in enumerate(zip(d[2:], [BRONZE, SILVER, GOLD])):
            _node(s, bx, y, nw, label, col, fill=col, text_fill=LAKE)
            if i < 2:
                _arrow(s, bx + nw + 4, bx + nw + 26, y + 15)
            bx += nw + 30
        _arrow(s, mx + 40, mx + 46, y + 15)
    else:
        widths = [s.width(t, "PPTextMed", 13.5) + 30 for t in d]
        x = pad
        for i, (label, w) in enumerate(zip(d, widths)):
            last = i == len(d) - 1
            _node(s, x, y, w, label, SILVER if last else MIST,
                  fill=SILVER if last else "none", text_fill=LAKE if last else FOAM)
            if not last:
                # two-way arrow: requests and responses
                _arrow(s, x + w + 4, x + w + 40, y + 10)
                _arrow(s, x + w + 40, x + w + 4, y + 20)
            x += w + 44

    ty = 170
    s.text(pad, ty, c["title"], "PPTitle", 27, fill=FOAM, letter_spacing=-0.3)
    for i, line in enumerate(c["desc"]):
        s.text(pad, ty + 38 + i * 27, line, "PPText", 18, fill=FOAM, opacity=0.78)
    last_row = _chips(s, pad, 300, c["tags"], W - pad)
    assert last_row == 300, c["tags"]
    return s


# -------------------------------------------------------------------------- stack
def stack(c):
    W = 1200
    stages = c["stages"]
    n_items = max(len(items) for _, items in stages)
    H = 150 + n_items * 32 + 20
    s = SVG(W, H, c["title"], c["desc"])
    s.add(f'<rect width="{W}" height="{H}" rx="16" fill="{LAKE}"/>')
    x0, step = 64, 232
    line_y = 58
    last_x = x0 + step * (len(stages) - 1)
    s.defs.append(
        f'<linearGradient id="flow" gradientUnits="userSpaceOnUse" x1="{x0}" x2="{last_x + 90}" y1="0" y2="0">'
        f'<stop offset="0" stop-color="{BRONZE}"/><stop offset="0.5" stop-color="{SILVER}"/>'
        f'<stop offset="1" stop-color="{GOLD}"/></linearGradient>'
    )
    s.add(f'<line x1="{x0}" x2="{last_x + 90}" y1="{line_y}" y2="{line_y}" stroke="url(#flow)" '
          f'stroke-width="3" stroke-linecap="round"/>')
    node_cols = [BRONZE, "#C69E83", SILVER, "#CDBD8A", GOLD]
    for i, (stage, items) in enumerate(stages):
        x = x0 + step * i
        s.add(f'<circle cx="{x + 7}" cy="{line_y}" r="8" fill="{LAKE}" stroke="{node_cols[i]}" '
              f'stroke-width="3"/>')
        assert s.width(stage, "PPTitle", 20) < step - 18, stage
        s.text(x, 108, stage, "PPTitle", 20, fill=FOAM)
        for j, item in enumerate(items):
            assert s.width(item, "PPText", 17.5) < step - 18, item
            s.text(x, 150 + j * 32, item, "PPText", 17.5, fill=FOAM, opacity=0.78)
    return s


# -------------------------------------------------------------------------- certs
def certs(c):
    W, H = 1200, 150
    s = SVG(W, H, c["title"], c["desc"])
    s.add(f'<rect width="{W}" height="{H}" rx="16" fill="{LAKE}"/>')
    items = c["items"]
    colw = (W - 64 * 2) / len(items)
    for i, (issuer, lines) in enumerate(items):
        x = 64 + i * colw
        if i:
            s.add(f'<line x1="{x - 24:.1f}" x2="{x - 24:.1f}" y1="34" y2="{H - 34}" '
                  f'stroke="{LAKE_LINE}"/>')
        # small medal ring
        s.add(f'<circle cx="{x + 9:.1f}" cy="52" r="8" fill="none" stroke="{GOLD}" stroke-width="2.5"/>')
        s.text(x + 28, 58, issuer, "PPTextMed", 15, fill=MIST)
        for ln in lines:
            assert s.width(ln, "PPTitle", 18.5) < colw - 40, ln
        s.text(x, 94, lines[0], "PPTitle", 18.5, fill=FOAM)
        s.text(x, 120, lines[1], "PPTitle", 18.5, fill=FOAM)
    return s


def main(repo: str):
    out = Path(repo) / "assets"
    out.mkdir(exist_ok=True)
    for lang, c in CONTENT.items():
        sfx = "" if lang == "en" else "-es"
        files = {
            f"hero{sfx}.svg": hero(c["hero"]),
            f"about{sfx}.svg": about(c["about"]),
            f"project-lakehouse{sfx}.svg": project_card(c["lakehouse"], "lakehouse"),
            f"project-tickets{sfx}.svg": project_card(c["tickets"], "tickets"),
            f"stack{sfx}.svg": stack(c["stack"]),
            f"certs{sfx}.svg": certs(c["certs"]),
        }
        for name, svg in files.items():
            data = svg.render()
            (out / name).write_text(data, encoding="utf-8")
            print(f"{name:28s} {len(data) / 1024:6.1f} KB")


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else ".")
