# Scoring run log

| Field | Value |
|-------|-------|
| Run | Calibration sample (first pass) |
| Scorer | Claude Opus, agent session (no temperature/seed control - see METHODOLOGY.md §6) |
| Date | 2026-05-28 |
| Rubric version | `METHODOLOGY.md` @ git hash-object `2e67d5bc40c772ddf7064f284f6d53deb164b6b5` (**draft, not yet frozen**) |
| Records | 20 (10 anthems × {as-written, as-sung}) |
| Validation | PASS (`uv run anthem-belligerence/src/aggregate.py`) |

## What this run is

A deliberately stratified **10-anthem calibration sample**, not the full corpus. Its purpose
is to test the rubric and the scoring approach before locking the rubric and scaling to ~195
states. Awaiting human spot-check (§7).

## Sample composition & why each anthem is here

| Anthem | Stress-tests |
|--------|--------------|
| Algeria — Kassaman | Maximal belligerence; no gap (overtly martial, all verses official) |
| France — La Marseillaise | High belligerence that is **sung**, not retired → small gap |
| United States — Star-Spangled Banner | Big gap: violent v3 ("hireling and slave") + deity v4 ("In God is our trust") not sung |
| United Kingdom — God Save the King | Deity + monarch; biggest gap (anti-enemy v2 "scatter our enemies" not sung) |
| Japan — Kimigayo | Low/short anchor; pure monarch (crown), zero belligerence |
| Switzerland — Swiss Psalm | Deity anchor (+ nature); zero belligerence |
| Spain — Marcha Real | **No-lyrics edge case** (excluded from index distributions) |
| Germany — Deutschlandlied | Gap in *non-belligerence* themes; the **wildcard** test (st2 "German women, wine, song", not sung) |
| Nepal — Sayaun Thunga Phulka | Unity/land/beauty profile; minimal belligerence |
| South Africa — National Anthem | **Anti-war trap**: "Banish wars and strife" mentions war but scores belligerence 0 |

## Provenance & grounding

- All scores grounded in the evidence lines + cited sources in `data/raw/anthems.json`.
  Full verbatim lyrics are not stored (public-domain texts live at the source URLs); evidence
  quotes are short lines actually retrieved from the cited sources.
- Scores were produced in-session, not by an API call, so there is no fixed seed; reproducibility
  here means the frozen rubric + preserved raw inputs + per-score quote & rationale.
- Where a score depends on a translation choice, the record carries a `translation-sensitive`
  flag and confidence is capped.

## Known limitations of this pass

- "Key lines" rather than full verbatim text were scored; a fuller fetch could surface themes
  missed in the summary (most relevant for Nepal, flagged `translation-sensitive`).
- Single-rater; the human spot-check is the second rater.
- `as-sung` for France/Switzerland is `sung-assumed` (verse 1 + refrain); Algeria's v3 is
  officially sung but historically sometimes omitted (`v3-sometimes-omitted`).
