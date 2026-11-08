# assets/CLAUDE.md

Rules for the images the root `README.md` and `README.ko.md` embed. The site's
own images live under `site/builder/assets/` and are unrelated to this folder.
Repo-wide rules are in the root `CLAUDE.md`.

## What is in here

Every image is a light/dark pair (`<name>.svg` + `<name>-dark.svg`) selected by
`<picture>` + `prefers-color-scheme`, and the two files of a pair differ only in
their colours.

| File | Role |
|---|---|
| `hero.svg`, `hero-ko.svg` (880×280) | The front door of `README.md` and of `README.ko.md`, linked to the reading site: the name and one line on the left, and on the right a field of resting taxels a sweep crosses, lighting the few it picks |
| `own.svg` (880×204) | The picture under How it works — who writes what: you and `context/`, the mark that reads it, and the three folders it writes |
| `track-scouting.svg`, `track-analysis.svg`, `track-comparison.svg`, `track-ideation.svg` | The four track icons (64×64), each above its track's name in the How-it-works table |
| `build-art.py` | Generates every image here, from one taxel grid |

## Drawing rules

**One mark draws everything.** The mark is a 4×4 taxel grid read while
something presses it — `site/builder/components.py`'s `mark()`: the centre
four pressed, their edge neighbours half pressed, the corners at rest. Every
image here is that grid or a reading of it, so a reader who meets the nav, the
favicon and the README sees one sensor rather than several drawings. Change
`mark()`'s patch and `CORE`/`HALO` in `build-art.py` move with it.

**A pressed taxel grows as well as lights.** Rest, half-pressed and pressed
differ in radius as well as colour, so the patch reads in forced colours and
for a reader who cannot tell the amber apart.

**Amber is the signal, and only the signal.** The amber (`#C27C0E`,
`#E3A23B`) marks what was pressed. Frames, wires and text take the navy ink
(`#13283F`) or, in dark, its light counterpart (`#9FB4CC`), so the one warm
colour on the page is the thing being pointed at.

**Text is live `<text>`.** Every file is SVG whose text is real text, so the
fonts are stacks (`ui-monospace`, `system-ui`) and every run is anchored with
room to spare, so a wider substituted face grows into space rather than into
its neighbour. An image that carries text repeats it in `aria-label` and in the
`alt` the READMEs embed it with.

**Each track icon is the grid doing its track's job.** At 64 px only the
pattern survives: `track-scouting` is a band sweeping the resting grid,
`track-analysis` is one pressed taxel under a lens, `track-comparison` is two
small readings that differ in one ringed taxel, and `track-ideation` is one
taxel lit with four rays. A new track needs a new reading of the grid, not a
new drawing.

**Motion is spent on the sweep.** The hero's sweep and the scouting icon's
band are the only animations, because sweeping is what the radar does. Every image carries its motion in its own
`<style>`, and `prefers-reduced-motion` stops it.

**An icon shares its track's cell, never a column of its own.** A table
column that holds only an image has no minimum width — GitHub caps every image
at `max-width: 100%` — so when the page is narrower than the table, the
browser squeezes that column first and the icons shrink to nothing. Stacked
above the track's name, the name holds the cell open.

## The hero

The field is the day's papers and the picks are what the radar presses for
you, so the count line under it says that in words and the field never carries
a number. A pick lights when the band's centre reaches its column and stays
lit until the cycle resets, so the end state — every pick lit — is also the
base style: with motion off the picture rests there. The English and Korean
heroes differ only in their text.

## Who writes what

`own.svg` is one row: you, the `context/` frame, the mark, and the frame of
three folders. The one wire is `context/` into the mark, labelled *reads*.
Nothing is drawn from the mark to its folders — the label over the frame says
it — and nothing back into `context/`, which the agent never writes; the
caption says a change comes to you as a proposal. The frame names `P#.md`,
never a count of pillars, so adding one does not date the picture.

## Generating

Every image is written by `build-art.py`, light and dark from the same markup.
Edit the script, never the SVG. Before pushing a change here:
`python3 assets/build-art.py --check`.
