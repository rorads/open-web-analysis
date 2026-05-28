# Anthem belligerence

**Status:** Methodology draft — **not frozen**. Awaiting review before any corpus build or scoring.

**Question.** What do nations actually sing about themselves — and how warlike is it, both
in the full official text and in the verses people actually perform?

**Why it's interesting.** "Warlike anthems" is a well-trodden listicle topic, and an
academic study has measured "fighting"-word frequency across ~186 anthems. What hasn't been
done: (1) a multi-theme **rubric** treating each anthem as a vector rather than one bucket;
(2) scoring the **full text vs. the customarily-sung verses** and reporting the gap — how
much belligerence each nation has quietly retired from performance (think La Marseillaise's
"impure blood", the rarely-sung 3rd verse of the US anthem); (3) a **two-axis "God vs Guns"**
map. The sung/written gap is the headline novelty.

**Composite + visual.**
- Composites: a **belligerence index**, a **deity index**, and the **retired-belligerence
  gap** (full minus as-sung).
- Standout visual: a "God vs Guns" scatter/world map (belligerence × deity), plus a
  dumbbell chart ranking how far each nation's as-sung belligerence falls below its full text.

**Source idea:** `rorads.github.io/todo.md` → "How belligerent is each national anthem?"

**Post:** —

## Layout

- `METHODOLOGY.md` — the rubric (draft; freeze before scoring).
- `sources.md` — seed bibliography.
- `data/raw/` — anthem lyrics + translations + sung-verse notes, as fetched.
- `data/processed/` — per-anthem scores.
- `src/` — fetch + score + viz code.
- `outputs/` — SVG figures.
