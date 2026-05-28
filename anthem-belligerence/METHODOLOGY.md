# Methodology — Anthem belligerence

> **Freeze this before scoring.** The rubric below is the contract. If scoring forces a
> change, edit deliberately and note what changed — don't let it drift.

**Status:** _Used for the full 195-state run on 2026-05-28 (this file at git `e668eec`).
Calibration-stage refinements are noted inline (notably §2: as-written = official text only).
A v2 rubric should consider promoting the recurring wildcard themes — labour/work and the
flag — to numbered themes (see `data/processed/run.md` and `exploratory.json`)._

## 1. Question

What do nations sing about themselves, and how warlike is it — in the **full official text**
and in the **verses actually performed**? The interesting, under-explored quantity is the
*gap* between the two.

## 2. Scope & unit of analysis

- **Population:** the ~195 widely-recognised sovereign states (UN members + observers).
  Start here; decide later whether to include de-facto / contested states as a flagged
  secondary set.
- **Unit:** one anthem per state. Each anthem is scored **twice**:
  - **as-written** — the complete official lyrics. **All** official verses must be reviewed
    (record a per-anthem `completeness` note); scoring from a partial excerpt risks
    under-counting themes buried in later verses. **Non-official historical verses are
    documented but excluded** — e.g. the UK's c.1745 "rebellious Scots to crush" verse, which
    was never in the official text. "Official" is the bar, not "ever attested".
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
| 11 | **Other / wildcard** | Any salient theme *not* covered by 1–10. The scorer must **name** what it is in a free-text label | e.g. the beauty of the nation's women, wine/food, a named river or city, labour & industry, a specific historical episode, humour | Anything already captured by themes 1–10 |

**Wildcard handling.** Theme 11 is the escape hatch for rogue content the fixed rubric
can't see coming. It is scored 0–3 like the rest but **also** records a short free-text label
of *what* the theme is. The wildcard does **not** feed the belligerence/deity/crown indices
(it would be uninterpretable), but it does feed the thematic fingerprint and the exploratory
clustering (§8). If the same wildcard label recurs across many anthems, that's a signal the
fixed rubric is missing a real theme — promote it to a numbered theme and re-score.

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

A per-anthem **thematic fingerprint** (the theme vector — themes 1–10 plus the wildcard
intensity) is retained for clustering countries by profile, independent of the headline indices.

## 6. Scoring process

The scorer is **Claude (Opus) working directly in an agent session** — not an API script with
a temperature knob. The corpus is small (~195 short texts), so the agent fetches each anthem,
stores the raw text, and scores it against this rubric inline. This trades away *literal*
bit-for-bit reproducibility (no fixed seed/temperature) for the thing that actually matters
here: **method transparency** — frozen rubric, preserved raw inputs, and a quoted line +
rationale behind every score, so the result is reproducible *in spirit* and auditable line by line.

1. **Fetch** each anthem via web research → `data/raw/anthems.json`: original-language text,
   English translation, the sung-verse note + its source, and source URLs + retrieval date.
   Raw evidence is immutable once fetched.
2. **Score** in-session, grounded in the stored raw text → `data/processed/scores.json`, one
   record per (anthem × {as-written, as-sung}); each theme carries `score` (0–3), `quote`
   (translation), `original` (source language), `rationale` (one line on *why*, not just the
   quote), `confidence` (low/med/high), `label` (wildcard only). Record-level: `flags`
   (e.g. `translation-sensitive`, `sung-assumed`, `no-lyrics`).
3. **Aggregate** composites + fingerprints by **code** (`src/`, run via `uv run`) →
   `data/processed/indices.{json,csv}`. The fetch→score→aggregate→figure path is re-executable;
   `data/processed/` is generated and never hand-edited.

**Provenance & transparency (non-negotiable).**

- **Mark the source of every datum.** Scores are clearly labelled as agent-produced and kept
  distinct from fetched text and human input. Spot-check corrections (§7) are recorded as
  overrides with a note, never silently overwriting the original score.
- **Log the run.** A `data/processed/run.md` records: scorer (`Claude Opus, agent session`),
  date, the **rubric version** (git short-hash of this file at scoring time), and the source
  list. Re-scoring against a changed rubric is a new run, not an edit of the old one.
- **Grounding over recall.** Every score is justified from the stored raw text via a quoted
  line; a theme with no quotable line scores 0, regardless of what the model "knows" about a
  famous anthem. This is the main risk of one agent both fetching and scoring, so it is the
  rule held hardest.
- **Optional independent pass.** A fresh-context or API re-run against the same `data/raw/` +
  rubric is a cheap second-rater robustness check if ever wanted.

## 7. Calibration & human spot-check

- Hand-review a **stratified sample of ~20** before trusting the full run:
  - *Expected-high belligerence:* France, Algeria, Vietnam, Italy, Portugal, China, Mexico.
  - *Expected-low:* Japan (*Kimigayo*), and a spread of "land/beauty" anthems.
  - *Strong deity:* Switzerland, and several others.
  - *Big sung/written gap (known):* France, USA — verify the gap mechanic works end-to-end.
  - *Random tail* for coverage.
- If LLM scores diverge systematically from human review, adjust rubric wording or weights
  **here**, note the change, and re-run. Lock the rubric once the sample agrees.

## 8. Exploratory analysis (correlation & clustering)

Secondary to the headline indices, but worth doing — these may surface the most interesting
findings, or may turn up nothing, which is itself reportable. Treat as exploratory: report
what's genuinely striking, don't over-claim significance on a sample of ~195.

- **Theme–theme correlations.** Do the themes co-occur in revealing ways? Hypotheses to look
  for: belligerence ↔ deity (do God and Guns travel together?), monarch ↔ freedom (inverse?),
  land/nature ↔ low belligerence. A theme correlation matrix is a cheap, honest first look.
- **External correlates (open data only).** Cross the indices against open variables — region,
  **age of the anthem / lyrics**, official religion, system of government, and possibly
  democracy/military-spending indices. The age cut is the most defensible: are older anthems
  more belligerent? Flag any external index's own biases.
- **Clustering on the fingerprint.** Cluster countries by their theme vector (§5) to see if
  natural thematic families emerge (e.g. "revolutionary/martial", "devotional", "pastoral",
  "fraternal") and whether they track geography or shared history rather than the obvious
  colonial/linguistic lines. Note the method (e.g. hierarchical / k-means) and that cluster
  counts are exploratory.
- The **wildcard labels** (theme 11) are reviewed in aggregate here: recurring labels are
  candidate new themes (§4) and may be the most surprising part of the piece.

## 9. Visuals

- **Primary — "God vs Guns":** scatter (and/or choropleth) of belligerence index (x) vs
  deity index (y), one point per country, coloured by region. As-sung version is the default;
  toggle/secondary shows as-written.
- **Secondary — the gap:** a dumbbell/slope chart ranking countries by retired-belligerence
  gap (as-written → as-sung), surfacing who has quietly defanged their anthem.
- **Optional — fingerprints / clusters:** small-multiple radar charts, a country × theme
  heatmap, or a dendrogram of the §8 clusters.
- Export SVG to `outputs/`, themed for the blog.

## 10. Threats to validity / caveats (to state openly in the post)

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
