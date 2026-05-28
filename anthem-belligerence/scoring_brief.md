# Scoring brief — anthem belligerence (full run)

This is the exact instruction set handed to each parallel scoring agent (a Claude Opus
session, per METHODOLOGY.md §6). Kept in-repo as part of the run record. You are one such
agent: you will research and score a BATCH of national anthems and write two JSON files.
Work carefully — this data is published.

## Your batch
You are given a **batch id** (an integer). Read
`/home/user/open-web-analysis/anthem-belligerence/data/batches.json` and process ONLY the
countries under `batches["<your id>"]`. Each item has `name`, `iso3`, `region`.

## THE ONE RULE: ground every score in text you actually found
You "know" famous anthems from training — do NOT score from memory. Every non-zero theme
score must be backed by a VERBATIM line that appeared in YOUR web-search results. If you
cannot find a quotable line for a theme in the text you retrieved, that theme scores 0.
Never invent or paraphrase a quote into the `quote` field. A theme with no quotable line = 0.

## Research procedure (per country)
Use WebSearch (WebFetch refuses full song lyrics; WebSearch snippets DO return verbatim verse
text). Good sources: nationalanthems.info, the country's Wikipedia anthem article,
lyricstranslate.com. Run 1–3 searches per anthem to obtain:
1. Full lyrics in an English translation (grab the original-language line where easy).
2. ALL verses' content — not just verse 1. Belligerent content often hides in later verses;
   if your first search returned only verse 1, search again for the rest. Record completeness.
3. Which verse(s) are official / customarily SUNG at ceremonies vs. the full written text.
Query patterns: `<country> national anthem English translation full lyrics all verses`;
`<country> anthem which verse is sung official`; `<anthem title> lyrics meaning`.

## Score each anthem TWICE
- **as-written** = the complete OFFICIAL lyrics (all official verses). Exclude
  non-official/historical verses (note notable ones in the entry, don't score them).
- **as-sung** = only the verse(s) officially designated or customarily performed. If only
  verse 1 is sung, score as-sung on verse 1 alone.
- One short / all-verses-sung anthem ⇒ as-written and as-sung are IDENTICAL (two identical records).
- Can't determine the sung custom ⇒ default as-sung = verse 1 and add flag `sung-assumed`.

## Rubric — 11 themes, scored 0–3 (use these EXACT keys)
- `war_arms` — fighting, weapons, battle, soldiers, making war ("to arms", "the sword"). NOT generic "struggle".
- `blood_death` — literal blood, killing, dying, graves, the fallen. NOT metaphorical "lifeblood/heart".
- `enemy_threat` — naming/othering foes, invaders, tyrants, oppressors. NOT abstract "adversity".
- `sacrifice` — willingness to die for / give all to the nation, martyrdom. NOT generic "devotion/service".
- `deity` — invocation of God, divine protection/blessing/providence. Vague "heaven/fate" w/o deity = 1 max.
- `monarch` — king/queen/sovereign/ruler, loyalty to a ruler. NOT personified "motherland/nation".
- `land_nature` — geography, soil, mountains, rivers, natural beauty. NOT purely political "the republic".
- `freedom_liberty` — liberty, independence, breaking chains, self-rule. NOT "peace" alone.
- `unity_brotherhood` — togetherness, fraternity, one people. NOT first-person-singular pride.
- `glory_pride` — honour, glory, greatness, national pride. NOT neutral description of land.
- `wildcard` — any SALIENT theme NOT covered above; you MUST add a short free-text `label`
  naming it (e.g. "labour & industry", "a named river", "the nation's women", "wine",
  "a specific historical battle"). Don't use it for anything themes 1–10 already cover.

Scale: **0** absent · **1** alluded (single oblique/metaphorical mention) · **2** present
(explicit and/or recurring) · **3** dominant (a central organising theme of the scored text).

## Confidence & flags
- `confidence`: "high" / "med" / "low".
- Score hinges on a translation choice (e.g. "blood" vs "struggle") ⇒ cap at "med" + record
  flag `translation-sensitive`.
- Guessed the sung verse ⇒ flag `sung-assumed`. No official words ⇒ flag `no-lyrics`.

## no-lyrics / not-found
- No official lyrics (purely instrumental, e.g. San Marino, Bosnia and Herzegovina, Kosovo):
  `no_lyrics: true`, `completeness: "no official lyrics"`, `themes: {}` in BOTH records, flag `no-lyrics`.
- Genuinely can't find lyrics after trying: `completeness: "NOT FOUND — lyrics unavailable in searches"`,
  `themes: {}`, and LIST the country in your final report so it can be retried.

## OUTPUT — write exactly two files (UTF-8 JSON; replace <ID> with your batch id). Do not print JSON.

**File A:** `/home/user/open-web-analysis/anthem-belligerence/data/raw/parts/batch_<ID>.json`
```json
{"anthems": [
  {"country":"<exact name from batch list>","iso3":"<iso3>","region":"<region>",
   "title":"<title, romanized; original script if easy>","languages_scored":["<lang scored>"],
   "year_lyrics": <int year lyrics written/adopted, best estimate, or null>,
   "structure":"<e.g. '4 verses + chorus'>","sung_rule":"<sung vs written + basis>",
   "sung_assumed": <true|false>, "no_lyrics": <true|false>,
   "completeness":"<COMPLETE: all N verses reviewed | PARTIAL: ... | no official lyrics | NOT FOUND: ...>",
   "key_lines":{"evidence":["<verbatim translated lines you used>"]},
   "source_urls":["<url actually used>"]}
]}
```

**File B:** `/home/user/open-web-analysis/anthem-belligerence/data/processed/parts/batch_<ID>.json`
```json
{"records": [
  {"country":"<exact name>","version":"as-written","flags":[],
   "themes":{"<theme_key>":{"score":<1-3>,"quote":"<verbatim translated line>",
     "original":"<source-language line, optional>","rationale":"<one line on WHY>","confidence":"<high|med|low>"}}},
  {"country":"<exact name>","version":"as-sung","flags":[],"themes":{ ... }}
]}
```
Record rules: include ONLY themes scoring ≥1 (omitted = 0). `wildcard` additionally needs a
`"label"`. Every included theme needs quote+rationale+confidence. Two records per country
(as-written + as-sung), identical if there is no sung/written gap.

## Mini-example (format only — do your own research)
```json
{"country":"Exampleland","version":"as-written","flags":[],"themes":{
  "war_arms":{"score":2,"quote":"Sons of the soil, take up your guns","rationale":"explicit call to arms in v3","confidence":"high"},
  "deity":{"score":1,"quote":"God watch over our land","rationale":"one passing divine invocation","confidence":"high"},
  "land_nature":{"score":3,"quote":"green valleys and snow-capped peaks","rationale":"the land is the anthem's central subject","confidence":"high"}}}
```

## Final reply (under 150 words)
How many countries processed; which (if any) were NOT FOUND or no-lyrics; any anthem where
the sung/written distinction was genuinely unclear. Do not paste the JSON.
