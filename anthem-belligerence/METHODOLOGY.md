# Methodology — Anthem belligerence

> **Freeze this before scoring.** The rubric below is the contract. If scoring forces a
> change, edit deliberately and note what changed — don't let it drift.

**Status:** _DRAFT — not frozen. For review._

## 1. Question

What do nations sing about themselves, and how warlike is it — in the **full official text**
and in the **verses actually performed**? The interesting, under-explored quantity is the
*gap* between the two.

## 2. Scope & unit of analysis

- **Population:** the ~195 widely-recognised sovereign states (UN members + observers).
  Start here; decide later whether to include de-facto / contested states as a flagged
  secondary set.
- **Unit:** one anthem per state. Each anthem is scored **twice**:
  - **as-written** — the complete official lyrics.
  - **as-sung** — the verse(s) officially designated or customarily performed at ceremonies.
- **Exclusions:** anthems with no official lyrics (e.g. Spain's *Marcha Real*, San Marino,
  Kosovo's *Europe*) are recorded but scored 0 across themes and flagged `no-lyrics`; they
  appear in the corpus but are excluded from index distributions (reported separately).
- **Multiple official languages:** score from the primary official-language text; note if a
  second official version diverges materially in tone.

## 3. Corpus & sources

- **Source allowlist (open web, no logins):**
  - [nationalanthems.info](https://nationalanthems.info) — primary. Has original-language
    lyrics, English translations, *and* notes on which verses are official/performed.
  - Wikipedia per-country anthem articles — cross-check, sung-verse customs, history.
  - Wikisource / public-domain texts — original-language source where available.
  - Official government / constitution pages — authoritative "official verse" designation.
- **Provenance:** every anthem records source URL(s) + retrieval date in `sources.md`;
  raw fetched text lands in `data/raw/` and is never hand-edited.
- **Translation policy:** prefer an official English translation where one exists; otherwise
  a single named published translation, recorded per anthem. **Score from the translation but
  keep the original-language line beside each evidence quote.** Any score that hinges on a
  translation choice (e.g. "blood" vs "struggle") is capped at `med` confidence and flagged
  `translation-sensitive`.
- **"As-sung" determination:** record the rule used per country (constitutional designation,
  official protocol, or documented custom) and its source. Where the sung portion is genuinely
  ambiguous, default as-sung = verse 1 only and flag `sung-assumed`.

## 4. Rubric

Each anthem is scored on every theme below, on the 0–3 scale, **separately for as-written
and as-sung**. Every non-zero score carries a quoted evidence line (translation + original)
and a confidence level.

| # | Theme | Definition | Counts | Doesn't count |
|---|-------|------------|--------|---------------|
| 1 | **War & arms** | Fighting, weapons, battle, soldiers, the act of making war | "to arms", "the sword", "march to battle" | Generic "struggle"/"strive" with no martial imagery |
| 2 | **Blood & death** | Literal blood, killing, dying, graves, the fallen | "impure blood", "watered with blood", "our martyrs' graves" | Metaphorical "lifeblood", "heart" |
| 3 | **Enemy & threat** | Naming/othering of foes, invaders, tyrants, oppressors | "the tyrant", "the invader", "crush the foe" | Abstract "adversity", "hardship" |
| 4 | **Sacrifice for nation** | Willingness to die for / give all to the nation; martyrdom | "we will die for thee", "our lives we pledge" | Generic "devotion", "service" |
| 5 | **Deity / God** | Invocation of God, divine protection, blessing, providence | "God save", "God defend", "the Lord's hand" | Vague "heaven"/"fate" with no deity (score 1 at most) |
| 6 | **Monarch / ruler** | King/queen/sovereign/leader, loyalty to a ruler | "long live the King", "our sovereign" | Personified "motherland"/"nation" |
| 7 | **Land & nature** | Geography, soil, mountains, rivers, natural beauty | "our snowy peaks", "the sacred soil" | Purely political "the republic" |
| 8 | **Freedom / liberty** | Liberty, independence, breaking chains, self-rule | "liberty", "free at last", "broke our chains" | "peace" alone |
| 9 | **Unity / brotherhood** | Togetherness, fraternity, one people | "brothers", "united we stand", "one people" | First-person singular pride |
| 10 | **Glory & pride** | Honour, glory, greatness, national pride | "glory", "honour", "the proudest nation" | Neutral description of the land |

**Scale (per theme):**

- **0 — Absent.** No trace in the scored text.
- **1 — Alluded.** A single oblique or metaphorical mention.
- **2 — Present.** Explicit and/or recurring; clearly part of the text's content.
- **3 — Dominant.** A central organising theme of the scored text.

**Grounding rule.** Because LLMs "know" famous anthems, every score must be justified from
the supplied source text via a quoted line — not from recall. A theme with no quotable line
in the supplied text scores 0, regardless of what the model believes about the anthem.

## 5. Composite indices

Computed separately for as-written and as-sung. Weights below are a **starting proposal**,
to be sanity-checked in calibration (§7).

- **Belligerence index** = `1.0·War + 1.0·Blood + 0.75·Enemy + 0.5·Sacrifice`,
  normalised to 0–100 against the maximum possible (`3·(1.0+1.0+0.75+0.5) = 9.75`).
- **Deity index** = `Deity` theme, normalised 0–100 (`÷3`). Monarch is tracked as a
  separate **Crown index** (`÷3`) rather than folded in, since deity ≠ monarchy.
- **Retired-belligerence gap** = `Belligerence(as-written) − Belligerence(as-sung)`.
  Positive = the nation has warlike content it doesn't perform. **This is the headline metric.**

A per-anthem **thematic fingerprint** (the 10-vector) is retained for clustering countries
by profile, independent of the headline indices.

## 6. Scoring process

1. Fetch corpus → `data/raw/` (one file per anthem: original, translation, sung-verse note,
   source URLs).
2. LLM-assisted scoring grounded in the supplied text → `data/processed/scores.csv`, one row
   per (anthem × {as-written, as-sung}) with the 10 theme scores, evidence lines, and
   per-theme confidence.
3. Compute composites + fingerprints → `data/processed/indices.csv`.

## 7. Calibration & human spot-check

- Hand-review a **stratified sample of ~20** before trusting the full run:
  - *Expected-high belligerence:* France, Algeria, Vietnam, Italy, Portugal, China, Mexico.
  - *Expected-low:* Japan (*Kimigayo*), and a spread of "land/beauty" anthems.
  - *Strong deity:* Switzerland, and several others.
  - *Big sung/written gap (known):* France, USA — verify the gap mechanic works end-to-end.
  - *Random tail* for coverage.
- If LLM scores diverge systematically from human review, adjust rubric wording or weights
  **here**, note the change, and re-run. Lock the rubric once the sample agrees.

## 8. Visuals

- **Primary — "God vs Guns":** scatter (and/or choropleth) of belligerence index (x) vs
  deity index (y), one point per country, coloured by region. As-sung version is the default;
  toggle/secondary shows as-written.
- **Secondary — the gap:** a dumbbell/slope chart ranking countries by retired-belligerence
  gap (as-written → as-sung), surfacing who has quietly defanged their anthem.
- **Optional — fingerprints:** small-multiple radar charts or a country × theme heatmap.
- Export SVG to `outputs/`, themed for the blog.

## 9. Threats to validity / caveats (to state openly in the post)

- **Translation bias.** Belligerence can be amplified or softened in translation; flagged
  per-item and confidence-capped. The honest version reports where the result is translation-sensitive.
- **Archaism.** Many anthems are 19th-century; a high deity/monarch score reflects the text's
  era, **not** the country's current religiosity or system of government.
- **Rubric subjectivity.** A single rubric author. The 0–3 thresholds are judgement calls;
  the spot-check is the guard, and the rubric is published so others can argue with it.
- **"As-sung" is itself contested** for some countries — recorded as a per-item assumption
  with confidence, not asserted as fact.
- **Prior art to cite:** the academic "fighting-word frequency" study (Trends in the texts of
  national anthems, 2023) and the casual 6-category anthem-subject map — position this work as
  the rubric-scored, sung-vs-written extension, not a first-of-kind.
