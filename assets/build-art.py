#!/usr/bin/env python3
"""Bake the generated README images — each a light/dark pair.

    hero.svg              the front door, English; hero-ko.svg is the Korean one
    own.svg               How it works: who writes what
    track-scouting.svg    the four track icons in the How-it-works table
    track-analysis.svg
    track-comparison.svg
    track-ideation.svg

    python3 assets/build-art.py            # write every pair
    python3 assets/build-art.py --check    # fail if any file is out of date

Every image is drawn from one mark: a 4×4 taxel grid, a tactile sensor read
while something presses it. Generated so that light and dark, and every image,
come from one markup: edit this script, never the SVG. What the images have
to keep saying is `assets/CLAUDE.md`.
"""
from __future__ import annotations

import sys
from pathlib import Path
from string import Template

OUT = Path(__file__).resolve().parent

# `site/builder/assets/site.css`'s tokens resolved to sRGB: a README image is
# fetched outside the site and cannot read a custom property.
LIGHT = dict(
    CARD="#FBFCFD", BORDER="#D3DBE3", SOFT="#E5EAF0",
    FRAME="#13283F", INK="#13283F", MUTED="#5B6B7C", SIGNAL="#C27C0E",
)
DARK = dict(
    CARD="#17202B", BORDER="#2E3B4A", SOFT="#243142",
    FRAME="#9FB4CC", INK="#E6ECF2", MUTED="#93A3B4", SIGNAL="#E3A23B",
)

# System stacks, not webfonts: a README image is rendered wherever GitHub is
# read, and every run is anchored with room to spare for a wider face.
MONO = "ui-monospace, SFMono-Regular, 'SF Mono', Menlo, Consolas, monospace"
SANS = "system-ui, -apple-system, 'Segoe UI', 'Apple SD Gothic Neo', 'Noto Sans KR', sans-serif"

TAXEL_CSS = """
    .tx-rest  { fill: ${INK}; opacity: .28; }
    .tx-halo  { fill: ${SIGNAL}; opacity: .42; }
    .tx-core  { fill: ${SIGNAL}; }
    .lens     { fill: none; stroke: ${INK}; stroke-width: 2.4; stroke-linecap: round; }
    .person   { fill: ${MUTED}; }
"""

REDUCED = """
    @media (prefers-reduced-motion: reduce) {
      * { animation: none !important; }
    }
"""

# The contact patch of `site/builder/components.py`'s `mark()`: the centre
# four pressed, their edge neighbours half pressed, the corners at rest.
CORE = {(1, 1), (1, 2), (2, 1), (2, 2)}
HALO = {(0, 1), (0, 2), (1, 0), (2, 0), (1, 3), (2, 3), (3, 1), (3, 2)}


def taxels(x: float, y: float, pitch: float, n: int = 4,
           level=lambda r, c: "core" if (r, c) in CORE else "halo" if (r, c) in HALO else "rest") -> str:
    """An n×n grid, top-left taxel centred at (x, y). A pressed taxel grows
    as well as lights, so the patch reads without its colour."""
    size = {"core": .43, "halo": .31, "rest": .18}
    return "".join(
        f'<circle class="tx-{level(r, c)}" cx="{x + c * pitch:.1f}" cy="{y + r * pitch:.1f}" '
        f'r="{pitch * size[level(r, c)]:.1f}"/>'
        for r in range(n) for c in range(n))


def person(x: float, y: float, s: float) -> str:
    """You: a head over a half-round torso, no face."""
    return (f'<g transform="translate({x} {y}) scale({s})">'
            f'<circle class="person" cx="48" cy="33" r="14.5"/>'
            f'<path class="person" d="M21 76 a27 27 0 0 1 54 0 Z"/></g>')


def svg(w: int, h: int, label: str, css: str, body: str) -> str:
    return f"""<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" role="img" aria-label="{label}">
  <style>{TAXEL_CSS}{css}{REDUCED}  </style>
{body}
</svg>
"""


# ── hero ──────────────────────────────────────────────────────────────
# The front door. On the right a field of resting taxels — the day's
# papers — and a sweep crossing it; the few it picks light as the band
# passes and stay lit until the cycle resets. With motion off the field rests
# in its end state, every pick lit, since the base style of a pick is lit and
# only the animation dims it.

FIELD_X, FIELD_Y, PITCH, COLS, ROWS = 500, 46, 30, 12, 6
PICKS = [(1, 2), (4, 4), (2, 7), (3, 10)]          # (row, col)
CYCLE = 7                                           # s
SWEEP_END = .78                                     # share of the cycle the band takes

HERO_CSS = f"""
    .card  {{ fill: ${{CARD}}; stroke: ${{BORDER}}; stroke-width: 1.2; }}
    .name  {{ fill: ${{INK}}; font: 800 46px {SANS}; letter-spacing: -1px; }}
    .line  {{ fill: ${{INK}}; font: 500 18px {SANS}; }}
    .sub   {{ fill: ${{MUTED}}; font: 14px {SANS}; }}
    .count {{ fill: ${{MUTED}}; font: 12px {SANS}; }}
    .btn   {{ fill: ${{INK}}; }}
    .btn-t {{ fill: ${{CARD}}; font: 600 14px {SANS}; }}
    .band  {{ fill: ${{SIGNAL}}; opacity: .14;
              animation: sweep {CYCLE}s linear infinite; }}
    @keyframes sweep {{ 0% {{ transform: translateX(0); }}
                       {SWEEP_END * 100:.0f}% {{ transform: translateX({COLS * PITCH}px); opacity: .14; }}
                       {SWEEP_END * 100 + 1:.0f}%, 100% {{ transform: translateX({COLS * PITCH}px); opacity: 0; }} }}"""


def hero(name_line: str, sub: str, count: str, label: str, button: str, bw: int) -> str:
    W, H = 880, 280
    picks, css = [], []
    for k, (r, c) in enumerate(PICKS):
        at = (c + .5) / COLS * SWEEP_END * 100      # when the band's centre reaches it
        css.append(f"    .pk{k} {{ animation: pick{k} {CYCLE}s linear infinite; }}\n"
                   f"    @keyframes pick{k} {{ 0%, {at:.1f}% {{ opacity: .28; transform: scale(.42); }}"
                   f" {at + 3:.1f}%, 96% {{ opacity: 1; transform: scale(1); }}"
                   f" 100% {{ opacity: .28; transform: scale(.42); }} }}")
        cx, cy = FIELD_X + c * PITCH, FIELD_Y + 20 + r * PITCH
        picks.append(f'<circle class="tx-core pk{k}" style="transform-box: fill-box; transform-origin: center" '
                     f'cx="{cx}" cy="{cy}" r="{PITCH * .3:.1f}"/>')
    rest = "".join(
        f'<circle class="tx-rest" cx="{FIELD_X + c * PITCH}" cy="{FIELD_Y + 20 + r * PITCH}" r="{PITCH * .1:.1f}"/>'
        for r in range(ROWS) for c in range(COLS) if (r, c) not in PICKS)
    band_h = (ROWS - 1) * PITCH + 28
    body = "\n  ".join([
        f'<rect class="card" x="1" y="1" width="{W-2}" height="{H-2}" rx="8"/>',
        taxels(64, 70, 15),
        f'<text class="name" x="142" y="112">paper-radar</text>',
        f'<text class="line" x="64" y="170">{name_line}</text>',
        f'<text class="sub" x="64" y="198">{sub}</text>',
        f'<rect class="btn" x="64" y="218" width="{bw}" height="36" rx="18"/>',
        f'<text class="btn-t" x="{64 + bw / 2}" y="241" text-anchor="middle">{button}</text>',
        f'<rect class="band" x="{FIELD_X - PITCH}" y="{FIELD_Y + 6}" width="{PITCH}" height="{band_h}" rx="{PITCH / 2}"/>',
        rest, "".join(picks),
        f'<text class="count" x="{FIELD_X - PITCH / 2}" y="{H - 28}">{count}</text>'])
    return svg(W, H, label, HERO_CSS + "\n" + "\n".join(css), body)


def hero_en() -> str:
    return hero("A literature radar for research.", "Scouted every morning, read in Korean.",
                "Dozens of new papers a day; a few pressed for you.",
                "paper-radar — a literature radar for research, scouted every morning and read in Korean. "
                "Open the reading site.", "Open the reading site", 196)


def hero_ko() -> str:
    return hero("연구를 위한 논문 레이더.", "매일 아침 스카우팅하고, 한국어로 읽습니다.",
                "하루 수십 편 가운데, 몇 편만 눌러 둡니다.",
                "paper-radar — 연구를 위한 논문 레이더. 매일 아침 스카우팅하고, 한국어로 읽습니다. "
                "읽기 사이트 열기.", "읽기 사이트 열기", 156)


# ── own ───────────────────────────────────────────────────────────────
# You, the context/ frame, the mark, and the frame of folders it writes, on
# one row. Both frames share a top and a height with their labels above them,
# and the mark stands as far from its folders as you do from context/.

OWN_CSS = f"""
    .mine  {{ fill: ${{CARD}}; stroke: ${{FRAME}}; stroke-width: 1.2; }}
    .matte {{ fill: none; stroke: ${{SOFT}}; stroke-width: 1; }}
    .row   {{ fill: ${{CARD}}; stroke: ${{BORDER}}; stroke-width: 1.2; }}
    .eb    {{ fill: ${{MUTED}}; font: 600 11px {SANS}; }}
    .p     {{ fill: ${{INK}}; font: 700 13px {MONO}; }}
    .ps    {{ fill: ${{MUTED}}; font: 11px {MONO}; }}
    .note  {{ fill: ${{MUTED}}; font: 12.5px {SANS}; }}
    .wire  {{ fill: none; stroke: ${{FRAME}}; stroke-width: 1.4; stroke-dasharray: 4 5; }}
    .head  {{ fill: ${{FRAME}}; }}"""

FOLDERS = [("scouting/", "every morning"), ("analysis/", "on request"),
           ("comparison/", "on request")]


def own() -> str:
    W, H, TOP, FH = 880, 204, 52, 112
    mid = TOP + FH / 2
    hx = 20                               # you
    cx, cw = hx + 96, 196                 # the context/ frame
    mx, ms = cx + cw + 104, 72            # the mark's box
    gap = cx - (hx + 60)                  # you → frame, reused mark → frame
    ox, ow = mx + ms + gap, 262           # the folders' frame
    shift = (W - (ox + ow) - hx) / 2      # centre the row
    wx, tip = cx + cw + 20, mx - 14       # the arrow clears both
    pitch = ms / 4
    b = [f'<text class="eb" x="{cx}" y="{TOP-10}">You write</text>',
         person(hx, mid - 44, .8),
         f'<rect class="mine" x="{cx}" y="{TOP}" width="{cw}" height="{FH}" rx="6"/>',
         f'<rect class="matte" x="{cx+5}" y="{TOP+5}" width="{cw-10}" height="{FH-10}" rx="4"/>',
         f'<text class="p" x="{cx+20}" y="{mid-12}">context/</text>',
         f'<text class="ps" x="{cx+20}" y="{mid+10}">MASTER.md</text>',
         f'<text class="ps" x="{cx+20}" y="{mid+28}">P#.md, one per research area</text>',
         f'<path class="wire" d="M{wx} {mid} H{tip - 8}"/><path class="head" d="M{tip} {mid} l-8 -4.5 v9 Z"/>',
         f'<text class="note" x="{(wx + tip) / 2}" y="{mid-10}" text-anchor="middle">reads</text>',
         taxels(mx + pitch / 2, mid - ms / 2 + pitch / 2, pitch),
         f'<text class="eb" x="{ox}" y="{TOP-10}">paper-radar writes</text>',
         f'<rect class="mine" x="{ox}" y="{TOP}" width="{ow}" height="{FH}" rx="6"/>']
    first = TOP + (FH - (len(FOLDERS) * 25 - 4)) / 2   # the rows, centred in the frame
    for k, (path, when) in enumerate(FOLDERS):
        y = first + k * 25
        b += [f'<rect class="row" x="{ox+9}" y="{y}" width="{ow-18}" height="21" rx="3"/>',
              f'<text class="p" x="{ox+20}" y="{y+15}">{path}</text>',
              f'<text class="ps" x="{ox+ow-20}" y="{y+15}" text-anchor="end">{when}</text>']
    b.append(f'<text class="note" x="{W/2 - shift}" y="{H-14}" text-anchor="middle">'
             'It reads context/ and never writes it. Changes come to you as proposals.</text>')
    return svg(W, H, "Who writes what: you write context/, and paper-radar reads it and writes "
               "scouting/, analysis/ and comparison/. Changes to context/ come to you as proposals.",
               OWN_CSS, f'<g transform="translate({shift:.1f} 0)">' + "\n  ".join(b) + "</g>")


# ── track icons ───────────────────────────────────────────────────────
# 64 px, one grid each, so the four read as one set. Each shows its track as
# a reading of the grid. Scouting alone moves — the sweep is what the track is.

def icon(label: str, body: str, css: str = "") -> str:
    return svg(64, 64, label, css, body)


def scouting() -> str:
    css = """
    .sweep { animation: sweep 3.2s ease-in-out infinite; }
    @keyframes sweep { 0%, 100% { transform: translateY(0); } 50% { transform: translateY(36px); } }"""
    band = '<rect class="tx-halo sweep" x="6" y="8" width="52" height="12" rx="6"/>'
    return icon("scouting: a sweep across the grid", band + taxels(14, 14, 12,
                level=lambda r, c: "rest"), css)


def analysis() -> str:
    pick = (1, 1)
    return icon("analysis: one taxel under a lens",
                taxels(14, 14, 12, level=lambda r, c: "core" if (r, c) == pick else "rest")
                + '<circle class="lens" cx="26" cy="26" r="9"/><path class="lens" d="M32.5 32.5 41 41"/>')


def comparison() -> str:
    same = {(0, 0), (1, 1)}
    left = taxels(9, 22, 8, 3, lambda r, c: "core" if (r, c) in same else "rest")
    right = taxels(39, 22, 8, 3, lambda r, c: "core" if (r, c) in same | {(2, 2)} else "rest")
    return icon("comparison: two readings, one taxel apart",
                left + right + '<circle class="lens" cx="55" cy="38" r="5.5"/>')


def ideation() -> str:
    rays = "".join(f'<path class="lens" d="M{32+dx*11} {32+dy*11} L{32+dx*15} {32+dy*15}"/>'
                   for dx, dy in ((0, -1), (0, 1), (-1, 0), (1, 0)))
    return icon("ideation: one taxel lights up",
                '<circle class="tx-core" cx="32" cy="32" r="7"/>' + rays
                + "".join(f'<circle class="tx-rest" cx="{x}" cy="{y}" r="2.2"/>'
                          for x in (10, 54) for y in (10, 54)))


IMAGES = {"hero": hero_en, "hero-ko": hero_ko,
          "own": own, "track-scouting": scouting, "track-analysis": analysis,
          "track-comparison": comparison, "track-ideation": ideation}


def main() -> int:
    check = "--check" in sys.argv[1:]
    stale = []
    for name, build in IMAGES.items():
        src = build()
        for suffix, pal in (("", LIGHT), ("-dark", DARK)):
            path = OUT / f"{name}{suffix}.svg"
            text = Template(src).substitute(pal)
            assert "${" not in text, f"{name}: unresolved colour"
            if check:
                if not path.exists() or path.read_text() != text:
                    stale.append(path.name)
            else:
                path.write_text(text)
    if stale:
        print(f"[build-art] out of date: {', '.join(stale)} — run python3 assets/build-art.py")
        return 1
    print(f"[build-art] {'clean' if check else 'wrote'} — {len(IMAGES) * 2} file(s)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
