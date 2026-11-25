"""Tiny SVG builder that tracks which characters each font family needs."""
from collections import defaultdict
from xml.sax.saxutils import escape

from fonts import font_face, text_width

LAKE = "#0F2A3D"
LAKE_DEEP = "#0B2232"
LAKE_LINE = "#1E4258"
BRONZE = "#C07A45"
BRONZE_LT = "#D9925C"
SILVER = "#B8C4CC"
GOLD = "#E3B448"
FOAM = "#EAF2F5"
MIST = "#8FA9B8"

FALLBACK = {
    "PPDisplay": "'Arial Black',Helvetica,Arial,sans-serif",
    "PPTitle": "Helvetica,Arial,sans-serif",
    "PPText": "Helvetica,Arial,sans-serif",
    "PPTextMed": "Helvetica,Arial,sans-serif",
    "PPMono": "ui-monospace,Menlo,Consolas,monospace",
}


class SVG:
    def __init__(self, width, height, title, desc=""):
        self.w, self.h = width, height
        self.title, self.desc = title, desc
        self.body = []
        self.defs = []
        self.css = []
        self.chars = defaultdict(str)

    def add(self, raw: str):
        self.body.append(raw)

    def text(self, x, y, s, family, size, fill=FOAM, anchor="start", opacity=None,
             letter_spacing=None, extra=""):
        self.chars[family] += s
        attrs = [f'x="{x:g}"', f'y="{y:g}"', f'class="{family}"', f'font-size="{size:g}"',
                 f'fill="{fill}"']
        if anchor != "start":
            attrs.append(f'text-anchor="{anchor}"')
        if opacity is not None:
            attrs.append(f'opacity="{opacity:g}"')
        if letter_spacing is not None:
            attrs.append(f'letter-spacing="{letter_spacing:g}"')
        if extra:
            attrs.append(extra)
        self.body.append(f"<text {' '.join(attrs)}>{escape(s)}</text>")

    def spans(self, x, y, parts, family, size, extra=""):
        """parts: list of (text, fill). Rendered as tspans on one line."""
        self.chars[family] += "".join(p for p, _ in parts)
        inner = "".join(f'<tspan fill="{c}">{escape(t)}</tspan>' for t, c in parts)
        self.body.append(
            f'<text x="{x:g}" y="{y:g}" class="{family}" font-size="{size:g}" '
            f'xml:space="preserve" {extra}>{inner}</text>'
        )

    @staticmethod
    def width(s, family, size, letter_spacing=0.0):
        return text_width(family, s, size, letter_spacing)

    def render(self) -> str:
        faces = "".join(font_face(f, c) for f, c in self.chars.items())
        classes = "".join(f".{f}{{font-family:'{f}',{FALLBACK[f]};}}" for f in self.chars)
        style = f"<style>{faces}{classes}{''.join(self.css)}</style>"
        defs = f"<defs>{''.join(self.defs)}</defs>" if self.defs else ""
        return (
            f'<svg xmlns="http://www.w3.org/2000/svg" width="{self.w}" height="{self.h}" '
            f'viewBox="0 0 {self.w} {self.h}" role="img" aria-labelledby="t d">'
            f'<title id="t">{escape(self.title)}</title><desc id="d">{escape(self.desc)}</desc>'
            f"{style}{defs}{''.join(self.body)}</svg>\n"
        )
