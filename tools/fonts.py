"""Font helpers: instance variable fonts, subset to used glyphs, embed as base64 woff2."""
import base64
import io
import os
from functools import lru_cache

from fontTools.ttLib import TTFont
from fontTools.varLib import instancer
from fontTools import subset

FONTSRC = os.environ.get("FONTSRC", os.path.join(os.path.dirname(__file__), "node_modules"))
ARCHIVO = f"{FONTSRC}/@fontsource-variable/archivo/files/archivo-latin-standard-normal.woff2"
FRAGMENT = f"{FONTSRC}/@fontsource/fragment-mono/files/fragment-mono-latin-400-normal.woff2"

# fixed font timestamps keep rebuilds byte-identical
FIXED_TS = 3_850_000_000

# family name -> (source file, axis location or None)
FAMILIES = {
    "PPDisplay": (ARCHIVO, {"wght": 760, "wdth": 125}),
    "PPTitle": (ARCHIVO, {"wght": 650, "wdth": 112}),
    "PPText": (ARCHIVO, {"wght": 420, "wdth": 100}),
    "PPTextMed": (ARCHIVO, {"wght": 580, "wdth": 100}),
    "PPMono": (FRAGMENT, None),
}


@lru_cache(maxsize=None)
def _instance(family: str) -> TTFont:
    path, loc = FAMILIES[family]
    font = TTFont(path)
    if loc:
        font = instancer.instantiateVariableFont(font, loc)
    buf = io.BytesIO()
    font.flavor = None
    font.recalcTimestamp = False
    font["head"].created = font["head"].modified = FIXED_TS
    font.save(buf)
    buf.seek(0)
    return TTFont(buf)


def text_width(family: str, text: str, size: float, letter_spacing: float = 0.0) -> float:
    font = _instance(family)
    cmap = font.getBestCmap()
    hmtx = font["hmtx"]
    upem = font["head"].unitsPerEm
    total = 0
    for ch in text:
        gname = cmap.get(ord(ch))
        if gname is None:
            raise ValueError(f"glyph missing for {ch!r} in {family}")
        total += hmtx[gname][0]
    return total * size / upem + letter_spacing * max(len(text) - 1, 0)


def font_face(family: str, chars: str) -> str:
    font = _instance(family)
    buf = io.BytesIO()
    font.save(buf)
    buf.seek(0)
    sub_font = TTFont(buf, recalcTimestamp=False)
    opts = subset.Options()
    opts.flavor = "woff2"
    opts.layout_features = ["kern", "liga", "calt"]
    opts.name_IDs = []
    opts.notdef_outline = True
    sub = subset.Subsetter(options=opts)
    sub.populate(text="".join(sorted(set(chars + " "))))
    sub.subset(sub_font)
    sub_font["head"].created = sub_font["head"].modified = FIXED_TS
    out = io.BytesIO()
    sub_font.flavor = "woff2"
    sub_font.save(out)
    b64 = base64.b64encode(out.getvalue()).decode()
    return (
        f"@font-face{{font-family:'{family}';"
        f"src:url(data:font/woff2;base64,{b64}) format('woff2');}}"
    )
