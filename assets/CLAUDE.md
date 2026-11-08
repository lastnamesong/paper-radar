# assets/CLAUDE.md

Rules for the images the root `README.md` embeds. The site's own images live
under `site/builder/assets/` and are unrelated to this folder. Repo-wide rules
are in the root `CLAUDE.md`.

## What is in here

Every image is a light/dark pair (`<name>.svg` + `<name>-dark.svg`) selected by
`<picture>` + `prefers-color-scheme`, and the two files of a pair differ only in
their colours.

| File | Role |
|---|---|
| `own.svg` (880×204) | The picture under How it works — who writes what: you and `context/`, the probe that reads it, and the three folders it writes |
| `probe-scouting.svg`, `probe-analysis.svg`, `probe-comparison.svg`, `probe-ideation.svg` | The four track icons, each above its track's name in the How-it-works table |
| `build-art.py` | Generates `own`. The four track icons are hand-authored |

## Drawing rules

**Text is live `<text>`.** Every file is SVG whose text is real text, so the
fonts are stacks (`ui-monospace`, `system-ui`) and every run is anchored with
room to spare, so a wider substituted face grows into space rather than into
its neighbour. An image that carries text repeats it in `aria-label` and in the
`alt` the README embeds it with.

**Rectangles are files.** A row in `own.svg` is a folder, a frame holds files.

**The accent draws the edge a reader meets first.** A frame standing on the
README's own page — the two frames in `own.svg` — takes the
accent (`#D97757`, `#E8916F`) over the shared card ground (`#FFFCFA`,
`#211C19`). A shape inside a frame keeps the neutral border (`#E8CDBD`,
`#3D3129`). `context/`'s frame also carries a hairline just inside its edge:
the one set of files the agent may not write, held in a matte.

**The character's parts carry meaning, so they are not mixed.** Eyes belong to
the probe alone, and so does the sprout on its head — a stem and two leaves
that sway about the stem's root on a 3.2 s cycle, off the bob's beat. The
person in `own.svg` is the probe's clay and shadow with no face and no sprout,
and breathes on its own 4.6 s cycle rather than the probe's bob. A prop is placed
or worn, never gripped: a handless probe holds nothing, so the page rides
under its eyes, the scouter hangs from the
hull's edge, the deerstalker sits on its head with the reading stone lying on
the page, and the bulb hangs over it where a thought would.

**Each track icon shows its track working, and its outline is what does the
work.** At the 64 px a table cell gives them, the only thing that survives is
the shape around the face: `probe-scouting.svg` takes a reading (a scouter over
the right eye — a round green lens in a purple ring, the earpiece on the hull's
edge, and on its antenna a green Wi-Fi mark of a dot and two arcs that never
touch and light in turn — whose dial, dots in the ring's purple, fills one by
one until the lens flashes, the scouter shakes and both pupils shrink),
`probe-analysis.svg` reads like a detective (a tweed deerstalker whose ear
flaps hang at the hull's sides, one wide page under the eyes and a reading
stone sliding along its first line, until the stone stops, the flaps spring
up and a red `!` pops over the cap), `probe-comparison.svg` spots the
difference (two bar-chart pages standing side by side under the eyes, alike
but for their third bar, the pupils and the hull turning from one to the
other faster each time, until a red pen ring draws itself round the same
spot on both pages, the probe hops and both pupils shrink), and
`probe-ideation.svg` has an idea (pupils up at a bulb over the head that
flickers like a tired tube, catches, and glows so bright the probe squints). A new track needs a
new outline, not a variation on one of these.

**Every track icon builds to one beat.** The scouter's dial is the model:
something mounts over the cycle and a single beat releases it — the flash,
the `!`, the pen ring, the glare — so each icon lands a punchline
rather than idling in a loop. Hues outside the clay come only with a prop
and stay on it: the scouter's green and purple, which no other icon uses,
the deerstalker's tweed, the bulb's yellow, and the red of the `!` and the
pen ring. With motion off, an icon rests before its beat — the pages
unmarked, the eyes open.

**An icon shares its track's cell, never a column of its own.** A table
column that holds only an image has no minimum width — GitHub caps every image
at `max-width: 100%` — so when the page is narrower than the table, the
browser squeezes that column first and the icons shrink to nothing. Stacked
above the track's name, the name holds the cell open.

**Animation is inlined and stays in step with the site.** A README image
carries no external stylesheet, so every motion lives in the file's own
`<style>`, and `prefers-reduced-motion` stops all of it. The character is
`site/builder/components.py`'s `mark()` redrawn: change `mark()` and these
change with it.

## Who writes what

`own.svg` is one row: you, the `context/` frame, the probe, and the frame of
three folders, symmetric about the two frames. The one wire is `context/` into
the probe, labelled *reads*. Nothing is drawn from the probe to its folders —
the PROBE WRITES label says it — and nothing back into `context/`, which the
agent never writes; the caption says a change comes to you as a proposal. The
frame names `P#.md`, never a count of pillars, so adding one does not date the
picture.

## Generating

`own` is written by `build-art.py` from one source,
light and dark from the same markup. Edit the script, never the SVG. Before
pushing a change here: `python3 assets/build-art.py --check`.
