# Scoring run log

| Field | Value |
|-------|-------|
| Run | **Full run — 195 states** (extends the 10-anthem calibration pass; same rubric) |
| Scorer | Claude (Opus) — **16 parallel agent sessions**, one per batch (no temperature/seed control, see METHODOLOGY.md §6) |
| Date | 2026-05-28 |
| Rubric version | `METHODOLOGY.md` @ git `e668eec` (incl. the calibration refinement: *as-written* = complete **official** text, excludes non-official historical verses) |
| Records | 390 (195 anthems × {as-written, as-sung}) |
| Validation | PASS (`uv run anthem-belligerence/src/aggregate.py`) |

## What this run is

The full population: **193 UN members + 2 observers (Holy See, State of Palestine) = 195**
(`../countries.json`). 192 are scored on themes; 3 are word-less (below). It extends the
calibration sample (still in the corpus) using the same frozen rubric — a scale-up, not a
re-score, so it is one continuous run.

## Method (re-executable pipeline)

1. `src/make_batches.py` → `data/batches.json` (16 batches of ≤12 not-yet-scored states).
2. 16 Opus **agent sessions** research + score each batch, following the frozen instruction
   set in `../../scoring_brief.md`, → `data/{raw,processed}/parts/batch_*.json` (transient,
   git-ignored). A 12-anthem pilot (batch 1) was hand-reviewed before the other 15 were
   dispatched. Per-agent sources: nationalanthems.info, Wikipedia per-country anthem articles,
   lyricstranslate.com, OAS / official government pages; per-anthem URLs in `data/raw/anthems.json`.
3. `src/merge_parts.py` → merges parts into `anthems.json` (195) + `scores.json` (390),
   coverage-checked against all 195. Never overwrites existing records.
4. `src/aggregate.py` → validates + writes `indices.{json,csv}`.
5. `src/explore.py` (§8) → `exploratory.json` + correlation/age figures.
6. `src/plot_full.py` → `outputs/god-vs-guns.svg`, `outputs/retired-gap.svg`.

## Provenance & grounding

- Every non-zero score is grounded in a verbatim line the scoring agent retrieved via web
  search (the §6 "grounding over recall" rule); a theme with no quotable line scores 0.
- Scores are LLM-produced (agent sessions), kept distinct from fetched evidence and from human
  overrides. No fixed seed; reproducibility = frozen rubric + `scoring_brief.md` + preserved
  raw evidence + per-score quote/rationale/confidence.

## Data quality (post-run audit)

- **Validation:** all 390 records pass.
- **Confidence of the 2,026 non-zero theme cells:** 1,456 high / 549 med / 21 low.
- **Flags:** `translation-sensitive` 54, `sung-assumed` 20, `no-lyrics` 6 (3 anthems × 2).
- **No-lyrics** (scored 0, excluded from index distributions): Spain, San Marino, Bosnia and
  Herzegovina. (Holy See *has* official Latin lyrics → scored.)
- **Logical check:** as-sung belligerence ≤ as-written for every country (after one override).

## Validation: blind second-rater spot-check (§7)

An independent Opus session re-scored a stratified 15 anthems **blind** to the v1 scores
(`data/processed/audit_sample.json`). Cell-by-cell vs v1: **70.3% exact, 96.0% within ±1**
(300 cells); only 4 of 150 as-written cells diverged by ≥2. Method judged reliable; the residual
risk is **under-scoring multi-verse anthems**, not systematic bias. Two corrections applied below.

## Overrides (spot-check, §6 — recorded, not silently overwritten)

- **Mali** — as-sung `sacrifice` lowered 3 → 2 to match the as-written score from the *same*
  line ("On the ramparts, we are ready to stand and die"): as-sung ⊆ as-written. Inline `override`.
- **Senegal** — as-written gained war/enemy/sacrifice/blood: v1 scored only the koras/balafons
  opening and missed the martial **chorus 5** ("the enemy violates our frontiers… weapons in our
  hands"), verified in source. As-sung (verse 1 + refrain) left benign → Senegal becomes the
  **#1 retired-gap (56→0)**. Inline `override`; flag `spotcheck-corrected`.
- **Mongolia** — `blood_death`/`sacrifice` removed: "our sweat and blood to lend [to build the
  homeland]" is the effort idiom (labour), not literal blood (rubric excludes metaphorical
  lifeblood); kept a mild enemy allusion. Belligerence 23 → 7.7. Flag `spotcheck-corrected`.

## Known limitations carried into the write-up

- Some long multi-verse anthems are `completeness: PARTIAL` (e.g. France, Afghanistan, Uruguay,
  Denmark, Micronesia, Vanuatu): later verses summarised, not transcribed line-by-line. Where
  flagged the headline score is robust (already at ceiling or unseen verses only reinforce the
  dominant theme), but the precise vector could move a point.
- `sung-assumed` (20 records): customarily-sung verse not firmly documented; as-sung defaulted
  to verse 1 (+ chorus).
- A few agents emitted free-text flags beyond the controlled set (`v3-sometimes-omitted` on
  Algeria; `mentions-war-as-peace` on South Africa) — descriptive only, no effect on indices.
- Region is a coarse 5-way macro-grouping; `year_lyrics` is a best-estimate authorship/adoption
  year per anthem (for the age correlate).

## Calibration sample (the original 10, retained in-corpus)

Algeria (max belligerence, no gap) · France (sung belligerence, small gap) · USA (big gap:
violent v3 + deity v4 unsung) · UK (deity+monarch, big gap) · Japan (pure crown, zero
belligerence) · Switzerland (deity anchor) · Spain (no-lyrics) · Germany (wildcard test:
"women, wine, song") · Nepal (unity/land) · South Africa (anti-war trap: "banish wars" → 0).
