# Scoring brief — v2 promotion pass (3 new themes only)

The v1 full run is done. v2 **promotes three recurring wildcards to numbered themes**. Your job
is narrow: for your batch of anthems, score ONLY these three new themes, for both versions.
The other 10 themes are carried over unchanged from v1, so do not re-score them.

## Your batch
You are given a **batch id**. Read `/home/user/open-web-analysis/anthem-belligerence/data/batches.json`
and process ONLY the countries under `batches["<id>"]`.

## Reuse, then verify
For each country, first read its entry in `/home/user/open-web-analysis/anthem-belligerence/data/raw/anthems.json`
(match on `country`): `key_lines` holds verbatim lines already gathered, `sung_rule` tells you
the as-written vs as-sung split. Those lines were selected for the v1 themes, so they often will
NOT mention the flag / labour / ancestors — therefore **run 1–2 targeted WebSearches per anthem**
to check for the three new themes in the full lyrics (e.g. `<country> anthem lyrics flag banner`,
`<country> anthem forefathers ancestors heritage`, `<country> anthem work toil labour build`).

## THE RULE (unchanged): ground every non-zero score in a VERBATIM line you actually found.
No quotable line ⇒ score 0 (omit). Never invent quotes.

## The three themes (score 0–3 each)
- `labour_work` — labour, toil, industry, building the nation through *effort/work*.
  Counts: "let us work", "sons of toil", "build our land", "through our labour". Does NOT count:
  generic "strive/struggle/effort" with no work imagery; armed struggle (that's war).
- `flag` — the national **flag / banner / colours / standard** as a thing addressed or raised.
  Counts: "our flag flies high", "the tricolour", "raise the banner", "our colours". Does NOT
  count: a flag as an incidental prop inside a battle scene with no focus on the flag itself.
- `ancestors_heritage` — **forefathers, ancestors, ancient lineage, inherited legacy**.
  Counts: "our forefathers", "land of our ancestors", "heritage handed down", "from of old".
  Does NOT count: generic "history/tradition"; "sons/children of the nation" (that is unity).

Scale: 0 absent · 1 alluded (single oblique mention) · 2 present (explicit/recurring) · 3 dominant.

## as-written vs as-sung
Same split as v1 (see the anthem's `sung_rule`). as-written = full official text; as-sung = the
performed verse(s). If a new theme appears only in an unsung verse, it scores lower (or 0) as-sung.
If there is no sung/written gap, the two records are identical.

## OUTPUT — write `/home/user/open-web-analysis/anthem-belligerence/data/processed/parts_v2/batch_<ID>.json`
(UTF-8, do not print it). Include ONLY the new themes that score ≥1.
```json
{"records":[
  {"country":"<exact name>","version":"as-written",
   "new_themes":{"flag":{"score":2,"quote":"<verbatim>","rationale":"<why>","confidence":"high"}}},
  {"country":"<exact name>","version":"as-sung","new_themes":{...}}
]}
```
Two records per country. If a country scores 0 on all three themes for a version, still emit the
record with `"new_themes":{}` (so we know it was checked). `confidence` low/med/high; if a score
hinges on translation, use med.

## Final reply (under 120 words)
Count of countries processed; which anthems scored notably on the flag / labour / ancestors; any
you were unsure about. Do not paste the JSON.
