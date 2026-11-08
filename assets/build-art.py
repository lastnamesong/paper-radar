#!/usr/bin/env python3
"""Bake the generated README images — each a light/dark pair.

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
         f'<text class="ps" x="{cx+20}" y="{mid+28}">P#.md, one per pillar</text>',
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


IMAGES = {"own": own, "track-scouting": scouting, "track-analysis": analysis,
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
