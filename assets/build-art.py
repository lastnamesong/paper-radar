#!/usr/bin/env python3
"""Bake the generated README image — each a light/dark pair.

    own.svg             How it works: who writes what

    python3 assets/build-art.py            # write every pair
    python3 assets/build-art.py --check    # fail if any file is out of date

The track icons in this folder are hand-authored. This one is generated so that
light and dark come from one markup: edit this script, never the SVG. What the images have to keep
saying is `assets/CLAUDE.md`.

Durations are literal, never `var()`: a custom property declared on `:root`
resolves only while the SVG is its own document, and an unresolved duration
drops the whole animation.
"""

from __future__ import annotations

import sys
from pathlib import Path
from string import Template

OUT = Path(__file__).resolve().parent

LIGHT = dict(
    CARD="#FFFCFA", BORDER="#E8CDBD", SOFT="#F2DFD3",
    ACCENT="#D97757", DEEP="#B06749", INK="#1F1611", MUTED="#7A6A60",
    HULL="#D97757", STALK="#CC785C", IRIS="#FFFAF7", PUPIL="#2A1A12",
    DIM="#C4B6AE", DIMSTALK="#B3A49B", DIMINK="#6B5A50", GHOST="#EFE4DC",
)
DARK = dict(
    CARD="#211C19", BORDER="#3D3129", SOFT="#332B26",
    ACCENT="#E8916F", DEEP="#C98A6D", INK="#F2EAE4", MUTED="#A08D80",
    HULL="#E8916F", STALK="#F0A183", IRIS="#FFF6F1", PUPIL="#2A1A12",
    DIM="#6E625B", DIMSTALK="#5E534C", DIMINK="#2A211C", GHOST="#2E2622",
)

# System stacks, not webfonts: a README image is rendered wherever GitHub is
# read, and every run is anchored with room to spare for a wider face.
MONO = "ui-monospace, SFMono-Regular, 'SF Mono', Menlo, Consolas, monospace"
SANS = "system-ui, -apple-system, 'Segoe UI', 'Apple SD Gothic Neo', 'Noto Sans KR', sans-serif"

# The character's parts and motions, redrawn from `site/builder/components.py`'s
# `mark()`. Animated classes sit on groups with no transform attribute, since a
# CSS transform replaces one.
CHARACTER_CSS = """
    .hull   { fill: ${HULL}; }
    .iris   { fill: ${IRIS}; }
    .pupil  { fill: ${PUPIL}; }
    .stem   { stroke: ${STALK}; stroke-width: 3.6; stroke-linecap: round; fill: none; }
    .leaf   { fill: ${STALK}; }
    .page   { fill: ${IRIS}; stroke: ${DEEP}; stroke-width: 2; }
    .line   { fill: ${DEEP}; opacity: .3; }
    .shadow { fill: ${STALK}; opacity: .45; }
    .dim    { fill: ${DIM}; }
    .dimst  { stroke: ${DIMSTALK}; stroke-width: 3.6; stroke-linecap: round; fill: none; }
    .dimbe  { fill: ${DIMSTALK}; }
    .cross  { fill: none; stroke: ${DIMINK}; stroke-width: 3.2; stroke-linecap: round; }
    .mug    { fill: ${IRIS}; stroke: ${DEEP}; stroke-width: 2; stroke-linejoin: round; }
    .handle { fill: none; stroke: ${DEEP}; stroke-width: 2.4; stroke-linecap: round; }
    .brew   { fill: ${DEEP}; }
    .steam  { fill: none; stroke: ${STALK}; stroke-width: 2.2; stroke-linecap: round; opacity: 0; }
    .rig    { animation: bob 3.4s ease-in-out infinite; }
    .sprout { transform-box: view-box; transform-origin: 48px 27px;
              animation: sway 3.2s ease-in-out infinite; }
    .lid    { transform-box: fill-box; transform-origin: 50% 50%;
              animation: blink 7s ease-in-out infinite; }
    .readp  { animation: read 3.6s ease-in-out infinite; }
    .l1     { animation: lit 4.8s ease-in-out infinite; }
    .l2     { animation: lit 4.8s ease-in-out 1.6s infinite; }
    .l3     { animation: lit 4.8s ease-in-out 3.2s infinite; }
    .s1     { animation: steam 3.8s ease-in-out infinite; }
    .s2     { animation: steam 3.8s ease-in-out 1.9s infinite; }
    .breathe { animation: breathe 4.6s ease-in-out infinite; }
    .drift  { transform-box: fill-box; transform-origin: 50% 100%;
              animation: drift 4.6s ease-in-out infinite; }
    @keyframes bob   { 0%, 100% { transform: translateY(0); } 50% { transform: translateY(-3px); } }
    @keyframes sway  { 0%, 100% { transform: rotate(-5deg); } 50% { transform: rotate(5deg); } }
    @keyframes blink { 0%, 44%, 50%, 100% { transform: scaleY(1); } 47% { transform: scaleY(.08); } }
    @keyframes read  { 0% { transform: translateX(-2.4px); } 72% { transform: translateX(2.4px); }
                       86%, 100% { transform: translateX(-2.4px); } }
    @keyframes lit   { 0%, 28% { opacity: .95; } 34%, 100% { opacity: .3; } }
    @keyframes steam { 0% { opacity: 0; transform: translateY(2px); } 30%, 55% { opacity: .7; }
                       100% { opacity: 0; transform: translateY(-6px); } }
    @keyframes drift { 0%, 100% { transform: rotate(-3deg); } 50% { transform: rotate(3deg); } }
    @keyframes breathe { 0%, 100% { transform: translateY(0); } 50% { transform: translateY(-1.6px); } }
"""

REDUCED = """
    @media (prefers-reduced-motion: reduce) {
      * { animation: none !important; }
    }
"""

PAGE = """<g transform="rotate(-5 48 75.5)">
        <rect class="page" x="25" y="67" width="46" height="17" rx="3"/>
        <rect class="line l1" x="31" y="70.6" width="34" height="2.2" rx="1.1"/>
        <rect class="line l2" x="31" y="74.4" width="34" height="2.2" rx="1.1"/>
        <rect class="line l3" x="31" y="78.2" width="22" height="2.2" rx="1.1"/>
      </g>"""


def probe(x: float, y: float, s: float, page: bool = False) -> str:
    """The character in its 96-unit box, top-left at (x, y), pupils down on
    the page and following its lines."""
    eyes = []
    for cx in (36, 60):
        pupil = f'<g class="readp"><circle class="pupil" cx="{cx}" cy="56.5" r="5"/></g>'
        eyes.append(f'<g class="lid"><circle class="iris" cx="{cx}" cy="52" r="11"/>{pupil}</g>')
    return f"""<g transform="translate({x} {y}) scale({s})">
    <ellipse class="shadow" cx="48" cy="90" rx="20" ry="4"/><g class="rig">
      <g class="sprout"><path class="stem" d="M48 26.5 V18.5"/><path class="leaf" d="M48 20.5 C43 20.6, 39.4 17.6, 38.5 13.5 C43.2 13, 47.2 15.6, 48 20.5 Z"/><path class="leaf" d="M48 18.2 C53.2 17.6, 57.6 14, 58.5 9.5 C53.2 9.5, 48.8 13, 48 18.2 Z"/></g>
      <rect class="hull" x="17" y="27" width="62" height="54" rx="19"/>
      {"".join(eyes)}
      {PAGE if page else ""}
    </g>
  </g>"""


def human(x: float, y: float, s: float) -> str:
    """You: the probe's clay and shadow, a head over a half-round torso, no
    face and no sprout — eyes are the character's alone. It breathes on a
    cycle of its own."""
    return f"""<g transform="translate({x} {y}) scale({s})">
    <ellipse class="shadow" cx="48" cy="90" rx="18" ry="4"/>
    <g class="breathe"><circle class="hull" cx="48" cy="33" r="14.5"/>
    <path class="hull" d="M21 76 a27 27 0 0 1 54 0 Z"/></g></g>"""


def svg(w: int, h: int, label: str, css: str, body: str, vb: str | None = None) -> str:
    return f"""<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="{vb or f'0 0 {w} {h}'}" role="img" aria-label="{label}">
  <style>{CHARACTER_CSS}{css}{REDUCED}  </style>
{body}
</svg>
"""


# ── own ───────────────────────────────────────────────────────────────
# You, the context/ frame, the probe, and the frame of folders it writes, on
# one row. Both frames share a top and a height with their labels above them,
# both bodies centre on the frames, and the probe stands as far from its
# folders as you do from context/.

OWN_CSS = f"""
    .mine  {{ fill: ${{CARD}}; stroke: ${{ACCENT}}; stroke-width: 1.2; }}
    .matte {{ fill: none; stroke: ${{SOFT}}; stroke-width: 1; }}
    .row   {{ fill: ${{CARD}}; stroke: ${{BORDER}}; stroke-width: 1.2; }}
    .eb    {{ fill: ${{DEEP}}; font: 9.5px {MONO}; letter-spacing: 1.8px; }}
    .p     {{ fill: ${{INK}}; font: 700 13px {MONO}; }}
    .ps    {{ fill: ${{MUTED}}; font: 11px {MONO}; }}
    .note  {{ fill: ${{MUTED}}; font: 12.5px {SANS}; }}
    .wire  {{ fill: none; stroke: ${{ACCENT}}; stroke-width: 1.6; stroke-dasharray: 4 5;
             animation: march 1.2s linear infinite; }}
    .head  {{ fill: ${{ACCENT}}; }}
    @keyframes march {{ to {{ stroke-dashoffset: -18; }} }}"""

FOLDERS = [("scouting/", "scheduled"), ("analysis/", "on demand"),
           ("comparison/", "on demand")]


def own() -> str:
    W, H, TOP, FH, PS = 880, 204, 52, 112, .9
    mid = TOP + FH / 2
    base = mid + 34                       # where both shadows sit
    hx = 20                               # you
    cx, cw = hx + 96, 196                 # the context/ frame
    px = cx + cw + 100                    # the probe's box
    gap = cx - (hx + 75 * .8)             # you → frame, reused probe → frame
    ox, ow = px + 79 * PS + gap, 262      # the folders' frame
    shift = (W - (ox + ow) - hx) / 2      # centre the row
    wx = cx + cw + 20                     # the arrow clears the frame
    tip = px + 17 * PS - 18               # and stops short of the hull
    b = [f'<text class="eb" x="{cx}" y="{TOP-10}">YOU WRITE</text>',
         human(hx, base - 90 * .8, .8),
         f'<rect class="mine" x="{cx}" y="{TOP}" width="{cw}" height="{FH}" rx="10"/>',
         f'<rect class="matte" x="{cx+5}" y="{TOP+5}" width="{cw-10}" height="{FH-10}" rx="7"/>',
         f'<text class="p" x="{cx+20}" y="{mid-12}">context/</text>',
         f'<text class="ps" x="{cx+20}" y="{mid+10}">MASTER.md</text>',
         f'<text class="ps" x="{cx+20}" y="{mid+28}">P#.md, one per pillar</text>',
         f'<path class="wire" d="M{wx} {mid} H{tip - 8}"/><path class="head" d="M{tip} {mid} l-8 -4.5 v9 Z"/>',
         f'<text class="note" x="{(wx + tip) / 2}" y="{mid-10}" text-anchor="middle">reads</text>',
         probe(px, base - 90 * PS, PS, page=True),
         f'<text class="eb" x="{ox}" y="{TOP-10}">PROBE WRITES</text>',
         f'<rect class="mine" x="{ox}" y="{TOP}" width="{ow}" height="{FH}" rx="10"/>']
    first = TOP + (FH - (len(FOLDERS) * 25 - 4)) / 2   # the rows, centred in the frame
    for k, (path, when) in enumerate(FOLDERS):
        y = first + k * 25
        b += [f'<rect class="row" x="{ox+9}" y="{y}" width="{ow-18}" height="21" rx="5"/>',
              f'<text class="p" x="{ox+20}" y="{y+15}">{path}</text>',
              f'<text class="ps" x="{ox+ow-20}" y="{y+15}" text-anchor="end">{when}</text>']
    b.append(f'<text class="note" x="{W/2 - shift}" y="{H-14}" text-anchor="middle">'
             'It reads context/ and never writes it. Changes come to you as proposals.</text>')
    return svg(W, H, "Who writes what: you write context/, and PROBE reads it and writes scouting/, "
               "analysis/ and comparison/. Changes to context/ come to you as proposals.",
               OWN_CSS, f'<g transform="translate({shift:.1f} 0)">' + "\n  ".join(b) + "</g>")


IMAGES = {"own": own}


def main() -> int:
    check = "--check" in sys.argv[1:]
    stale = []
    for name, build in IMAGES.items():
        src = build()
        for suffix, pal in (("", LIGHT), ("-dark", DARK)):
            path = OUT / f"{name}{suffix}.svg"
            text = Template(src).substitute(pal)
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
