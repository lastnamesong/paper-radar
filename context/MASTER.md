# Paper Radar
> Research scout for wearable robotics and tactile dexterous manipulation.

---

# Research Context — Wearables and Touch

> **Agent usage**: This file is the *static, cross-cutting* **global anchor** — Identity, Purpose, the Pillars overview, and cross-pillar references. Per-pillar working context (Decision Log, Tracked Literature, Anti-topics) lives in `context/P0.md` and `context/P1.md`. Read-only for the agent.

---

## 0. How to use this file [STABLE]

- This document is the **global anchor**: cross-cutting content that is not specific to one pillar.
- `context/P0.md` and `context/P1.md` own their pillar's Decision Log, Tracked Literature and Anti-topics. Edit the pillar file for pillar content; edit this anchor only for cross-cutting content.
- Markers: `[STABLE]` changes rarely; `[LIVING]` is updated as research progresses; `[AGENT-INPUT]` is what the retrieval agent conditions on — keep it signal-dense.
- All formatting rules (emoji system, link format, Korean authoring principles) are in **`scouting/AUTHORING.md`**.

---

## 1. Identity [STABLE] [AGENT-INPUT]

> Research on **wearable robots, sensors and human biomechanics** (P0) and on **tactile sensing and dexterous manipulation** (P1). Both are about the same thing from two sides: how a body or a hand senses contact and acts on it. A paper is relevant when it changes what a device senses through the body or through touch, or how that signal is turned into assistance or manipulation.

---

## 2. Purpose [STABLE]

Surface the few papers a day that bear on the open decisions in `context/P0.md` and `context/P1.md`, scored against them, and turn the ones the maintainer names into Korean rewrites.

---

## 3. Long-term Context [STABLE → semi-LIVING]

The wearable side supplies the body signal and the assistance problem; the tactile side supplies the contact signal and the manipulation problem. Where the two meet — intent from the body, touch at the hand — is the long-term interest.

---

## 4. Pillars [STABLE structure, LIVING content] [AGENT-INPUT]

**Two pillars (P0–P1).** They are independent tracks sharing one scouting run.

Each pillar file owns its own scope, scouting lens, anti-topics, Decision Log and tracked literature. This table is the index — what a pillar owns in one line, how many decisions it holds, and where the rest of it lives. The ids themselves are mapped in `context/CLAUDE.md`.

| Pillar | Owns | Decisions | File |
|---|---|---|---|
| P0 — Wearable Robots, Sensors & Biomechanics | exoskeletons, wearable sensing, intent/gait estimation from worn devices, and the biomechanics they assist | 2 | `context/P0.md` |
| P1 — Tactile Sensing & Dexterous Manipulation | tactile sensors, VTLA policies, and dexterous and in-hand manipulation | 2 | `context/P1.md` |

Retired: none.

---

## 5. Venue Priority [AGENT-INPUT]

| Tier | Venues |
|------|--------|
| 1 | Science Robotics, Nature Machine Intelligence, CoRL, RSS |
| 2 | T-RO, TNSRE, ICRA, IROS |
| 3 | RA-L, Sensors/Soft Robotics journals (archival weight) |
| 4 | arXiv raw (cs.RO, cs.LG, eess.SP) — noisiest, lowest default weight |

---

## 6. Cross-pollination Budget [AGENT-INPUT]

1 paper per pillar per slot from an adjacent field that plausibly transfers. A
slot is a 14-day block counted from Monday 2026-01-05, numbered
`n = ⌊days since 2026-01-05 ÷ 14⌋`; its field is A–D by `n mod 4` (A at 0), so
the four fields cycle in eight weeks. Rotating:
- **Slot A**: prosthetics and rehabilitation robotics (P0 adjacency)
- **Slot B**: VLA architecture advances broadly
- **Slot C**: flexible electronics and e-skin materials (P0 and P1 adjacency)
- **Slot D**: tactile sensing in neuroscience and haptics (P1 adjacency)

---

*End.*
