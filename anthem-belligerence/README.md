# Anthem belligerence

**Status:** **Complete & validated — all 195 states, v2 rubric (14 themes)** (2026-05-28).
Blind second-rater spot-check: 96% within ±1. **Write-up: [`FINDINGS.md`](FINDINGS.md)**;
process narrative: [`PROCESS_LOG.md`](PROCESS_LOG.md); run log: `data/processed/run.md`.

**Question.** What do nations actually sing about themselves — and how warlike is it, both
in the full official text and in the verses people actually perform?

## Headline findings (n=195; 192 with lyrics)

- **God and Guns don't travel together.** Deity does *not* correlate with the warlike themes
  (war/blood/enemy) — the most belligerent anthems are overwhelmingly *secular/revolutionary*
  (Algeria, France, Vietnam, Palestine, Tunisia, Cuba, all at deity 0). The belligerence
  themes themselves cohere tightly (blood↔sacrifice r=0.58, war↔enemy r=0.52), which validates
  the composite. Sudan ("army of God") is the rare high-God, high-Guns outlier.
- **The retired-belligerence gap is real and large for many.** Senegal (56→0, found in the
  spot-check), Congo-Brazzaville (51→0), Albania (49→0), New Zealand (36→0), Romania (92→54),
  the UK (44→10) and USA (56→28) all carry warlike content they no longer perform. See the dumbbell.
- **Most belligerent regions:** Americas (mean 34.5) > Africa (26.0) > Asia (22.1) ≈ Europe
  (22.0) ≫ Oceania (5.9). **Crown** is an Asia/Europe phenomenon and **zero** in the Americas
  (all republics). Region signatures: Africa = labour/unity, Europe = heritage, Oceania = God/land.
- **Anthem age is a null result:** r=−0.10 between year-of-lyrics and belligerence. Old ≠ warlike.
- **Five thematic families** (k-means, 13 themes): royal/devotional · pastoral/civic ·
  **labour/developmental** · **revolutionary/martial (52)** · **flag/patriotic** (incl. the USA).
- **The wildcard earned its keep:** *labour/work*, *the flag* and *ancestors/heritage* recurred
  so often they were **promoted to numbered themes in v2** (ancestors 39% is now more common than
  the enemy). The next candidate the wildcard is flagging: *peace* (13 anthems).

**Figures (`outputs/`):** `god-vs-guns.svg` (belligerence × deity, by region) ·
`retired-gap.svg` (written→sung dumbbell) · `region-theme-heatmap.svg` (region fingerprints) ·
`theme-prevalence.svg` (what anthems sing about) · `belligerence-dist.svg` ·
`theme-corr-heatmap.svg` · `age-vs-belligerence.svg`.

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
