#!/usr/bin/env python3
"""Renders the link-preview cards assets/og-tr.png and assets/og-en.png (1200×630) on macOS.

    python3 tools/og.py

The card is an SVG built from the site's own fonts and the game's tower drawings, rendered by QuickLook (qlmanage,
WebKit) and cropped with sips: no third-party image tools needed. QuickLook renders a square thumbnail, so the card
is laid out in the middle 630 px band of a 1200×1200 canvas and cropped afterwards.
"""
import base64, json, pathlib, re, subprocess, tempfile

SITE = pathlib.Path(__file__).resolve().parent.parent
ASSETS = SITE / "assets"
GAME = json.loads((SITE / "data" / "game.json").read_text())
NAVY, CREAM50, CREAM100 = "#1E2A4A", "#FFF8EC", "#FBEEDA"
SHOWN = ("tas", "antik", "buhar", "dijital", "kozmik")   # five ages, small to tall
TEXT = {
    "tr": ("Kilden kuleni", "çağlar boyunca koru.", "{levels} seviye · {ages} çağ · {realms} mitoloji diyarı", "iPhone için kule savunma"),
    "en": ("Guard your clay tower", "through the ages.", "{levels} levels · {ages} ages · {realms} mythic realms", "Tower defense for iPhone"),
}

def font(name):
    return base64.b64encode((ASSETS / "fonts" / name).read_bytes()).decode()

def nested(rel, x, y, w, h):
    """The game SVG as a nested <svg> (QuickLook does not draw SVG data URIs in <image>)."""
    src = (ASSETS / "art" / rel).read_text()
    return re.sub(r'^<svg [^>]*?viewBox="([^"]*)"[^>]*>', lambda m: f'<svg x="{x}" y="{y}" width="{w}" height="{h}" viewBox="{m.group(1)}">', src, count=1)

def card(lang):
    l1, l2, stats, kicker = TEXT[lang]
    c = GAME["counts"]
    stats = stats.format(**c)
    ages = {a["id"]: a for a in GAME["ages"]}
    towers, x = [], 540
    for i, pid in enumerate(SHOWN):
        h = 150 + i * 25
        w = h * 120 / 150
        towers.append(nested(ages[pid]["towers"][2], x, 530 - h, w, h))
        x += w - 40
    return f"""<svg xmlns="http://www.w3.org/2000/svg" width="1200" height="1200" viewBox="0 0 1200 1200">
<style>@font-face{{font-family:B;src:url(data:font/woff2;base64,{font('Baloo2-700-800.woff2')}) format("woff2");font-weight:800}}
@font-face{{font-family:N;src:url(data:font/woff2;base64,{font('Nunito-500-800.woff2')}) format("woff2");font-weight:800}}</style>
<rect width="1200" height="1200" fill="{CREAM50}"/>
<g transform="translate(0 285)">
<ellipse cx="860" cy="522" rx="320" ry="62" fill="#F3C9A8"/>
<ellipse cx="860" cy="522" rx="320" ry="62" fill="none" stroke="{NAVY}" stroke-width="5"/>
{''.join(towers)}
<rect x="60" y="62" width="{len(kicker) * 14 + 52}" height="52" rx="26" fill="{CREAM100}" stroke="{NAVY}" stroke-width="4"/>
<circle cx="88" cy="88" r="9" fill="#4FA85A"/>
<text x="108" y="97" font-family="N" font-weight="800" font-size="24" fill="{NAVY}">{kicker}</text>
<text x="56" y="250" font-family="B" font-weight="800" font-size="128" fill="{NAVY}">Kilkule</text>
<text x="60" y="330" font-family="B" font-weight="800" font-size="48" fill="{NAVY}">{l1}</text>
<text x="60" y="388" font-family="B" font-weight="800" font-size="48" fill="#A2401C">{l2}</text>
<text x="60" y="560" font-family="N" font-weight="800" font-size="28" fill="#34446E">{stats}</text>
</g>
</svg>"""

def main():
    with tempfile.TemporaryDirectory() as tmp:
        tmp = pathlib.Path(tmp)
        for lang in TEXT:
            svg = tmp / f"og-{lang}.svg"
            svg.write_text(card(lang))
            subprocess.run(["qlmanage", "-t", "-s", "1200", "-o", str(tmp), str(svg)], check=True, capture_output=True)
            out = ASSETS / f"og-{lang}.png"
            # sips crops around the centre; the card sits in the middle band of the square
            subprocess.run(["sips", "-c", "630", "1200", str(tmp / f"og-{lang}.svg.png"), "--out", str(out)],
                           check=True, capture_output=True)
            print(out.relative_to(SITE))

if __name__ == "__main__":
    main()
