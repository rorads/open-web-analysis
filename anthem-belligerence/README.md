# Anthem belligerence

**Status:** **Full run complete — all 195 states scored** (2026-05-28). Rubric `e668eec`.
See `data/processed/run.md` for the run log and `data/processed/exploratory.json` for §8.

**Question.** What do nations actually sing about themselves — and how warlike is it, both
in the full official text and in the verses people actually perform?

## Headline findings (n=195; 192 with lyrics)

- **God and Guns don't travel together.** Deity does *not* correlate with the warlike themes
  (war/blood/enemy) — the most belligerent anthems are overwhelmingly *secular/revolutionary*
  (Algeria, France, Vietnam, Palestine, Tunisia, Cuba, all at deity 0). The belligerence
  themes themselves cohere tightly (blood↔sacrifice r=0.58, war↔enemy r=0.52), which validates
  the composite. Sudan ("army of God") is the rare high-God, high-Guns outlier.
- **The retired-belligerence gap is real and large for many.** Congo-Brazzaville (51→0),
  Albania (49→0), New Zealand (36→0), Romania (92→54), Haiti, El Salvador, Mauritania, the UK
  (44→10) and USA (56→28) all carry warlike content they no longer perform. See the dumbbell.
- **Most belligerent regions:** Americas (mean 34.5) > Africa (25.2) > Asia (22.4) ≈ Europe
  (22.0) ≫ Oceania (5.9). **Crown** is an Asia/Europe phenomenon and **zero** in the Americas
  (all republics). 57 of 192 anthems score zero belligerence.
- **Anthem age is a null result:** r=−0.10 between year-of-lyrics and belligerence. Old ≠ warlike.
- **Five thematic families** fall out of k-means on the fingerprint: royal/devotional ·
  pastoral · civic-devotional · **revolutionary/martial (54 countries)** · proud/patriotic.
- **The wildcard surfaced two themes the rubric missed:** *labour/work* and *the flag* both
  recur heavily — candidates to promote to numbered themes in a v2 rubric.

**Figures:** `outputs/god-vs-guns.svg` (belligerence × deity, by region) ·
`outputs/retired-gap.svg` (written→sung dumbbell) · `outputs/theme-corr-heatmap.svg` ·
`outputs/age-vs-belligerence.svg`.

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
- Exploratory: theme correlations, external correlates (esp. age of the anthem), and
  clustering countries by thematic fingerprint — to see whether anything interesting falls out.

**Source idea:** `rorads.github.io/todo.md` → "How belligerent is each national anthem?"

**Post:** —

## Layout

- `METHODOLOGY.md` — the rubric (draft; freeze before scoring).
- `sources.md` — seed bibliography.
- `data/raw/` — anthem lyrics + translations + sung-verse notes, as fetched.
- `data/processed/` — per-anthem scores.
- `src/` — fetch + score + viz code.
- `outputs/` — SVG figures.
