# Process log — Anthem belligerence

> Informal narrative of how this analysis actually unfolded — decisions, surprises, dead ends,
> and course-corrections. Distinct from `data/processed/run.md` (formal provenance). Kept so the
> *process* can be written up later, not just the results. Newest entries at the bottom.

## 2026-05-28 — Calibration (10 anthems)

Wrote the rubric (`METHODOLOGY.md`) first and froze it in spirit before scoring. Hand-scored a
deliberately stratified 10-anthem sample to stress every part of the rubric: max belligerence
(Algeria), sung-vs-written gaps (USA, UK), a no-lyrics edge case (Spain), the wildcard
(Germany's "women, wine and song"), and an "anti-war trap" (South Africa's "banish wars" — names
war but scores belligerence 0). Built the deterministic `aggregate.py` (validate + composites).

## 2026-05-28 — Two reviewer catches (the useful kind)

A review pass flagged two real problems:
1. **Missing verses.** Raw data stored *excerpts*, not full text, so as-written scores risked
   under-counting. Nepal was the genuine miss — scored from a theme summary that omitted "from
   the blood of the braves, a nation free" (a real blood line); belligerence 5.1 → 15.4. Also
   confirmed the UK's "rebellious Scots to crush" verse is **non-official** → correctly excluded.
   Lesson baked into the rubric: as-written = complete *official* text; every verse reviewed.
2. **Deity/crown looked binary.** Turned out an artefact of the *as-sung* view; the as-written
   US deity is 66.7. The index is a single 0–3 theme, so it only takes 4 values — this resurfaces
   later as the "banded axis" question.

## 2026-05-28 — Full run (195 states)

Scaled from 10 → 195 via **16 parallel Claude Opus agent sessions** (one validated pilot batch
first, then 15 fanned out). Each agent grounds every score in verbatim web-search text per
`scoring_brief.md`, writes its own part file; `merge_parts.py` assembles + coverage-checks.
All 390 records validate. One logical inconsistency found and fixed (Mali: as-sung > as-written
on one line — capped). Surprises:
- **God and Guns repel** (deity↔belligerence r=−0.26), while **God and Crown attract** (+0.26).
- **Monarch is the rarest theme** (12%) — the opposite of the anthem stereotype.
- Region fingerprints are crisp: Americas martial, Oceania devotional/pastoral, Africa
  unity/freedom, Asia crown.
- **Age is a null** (r=−0.10).
- Wildcards point to missing themes: **labour/work, the flag, ancestors/heritage**.
- The world's most *average* anthem is **Mongolia's**.

Wrote up `FINDINGS.md` (marked PROVISIONAL) and the visuals. Fixed the "God vs Guns" banded
axis (it's the true granularity of a single 0–3 theme; relabelled bands + jittered).

## 2026-05-28 — Next: validate (spot-check) + v2 rubric (promote wildcards)

Decision: lift findings from provisional → validated via an **independent stratified spot-check**
(a fresh-context auditor re-scores ~15 anthems blind to the v1 scores; I adjudicate divergences),
then build a **v2 rubric** promoting labour/work, the flag, and ancestors/heritage to numbered
themes and re-score all 195. Doing the spot-check first so any lessons feed the v2 design.
Composites (belligerence/deity/crown) are unaffected by the 3 new themes, so the headline numbers
should stay stable — a useful built-in cross-check.

_(appended as work proceeds)_
