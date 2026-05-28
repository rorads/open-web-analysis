# Findings — Anthem belligerence

> **Status: VALIDATED (v2 rubric, 14 themes).** All 195 states scored 2026-05-28 by parallel
> Claude Opus agent sessions against rubric `e668eec`, then **spot-checked by an independent
> blind second-rater** on a stratified 15 (70.3% exact / **96.0% within ±1** across 300 cells;
> two corrections applied). v2 promoted three recurring wildcards — labour/work, the flag,
> ancestors/heritage — to numbered themes; this leaves the belligerence/deity/crown composites
> **identical** to v1 (verified, 0 cells changed). Provenance: `data/processed/run.md`;
> process narrative: `PROCESS_LOG.md`; data: `data/processed/{indices,exploratory,findings_extra}.json`.

## The question

What do nations sing about themselves, how warlike is it, and how much warlikeness sits in the
**full official text** but is dropped from the **performed verses**? Each of 195 anthems
(193 UN members + Holy See + Palestine) was scored on 14 themes (0–3), twice — *as written* and
*as sung*. 192 have lyrics; 3 are word-less (Spain, San Marino, Bosnia and Herzegovina).

## 1. God and Guns repel; God and Crown attract

The marquee result. Across the 192 anthems with lyrics, **deity is *negatively* correlated with
belligerence** (Pearson **r = −0.26**; deity↔blood −0.25, deity↔war −0.20). The most warlike
anthems are overwhelmingly **secular-revolutionary** — Algeria, France, Vietnam, Palestine,
Tunisia, Cuba — all at deity 0. Meanwhile deity↔**monarch** is *positive* (**r = +0.26**): where
God appears, a king often does too (UK, Holy See, Tonga, Brunei, Oman). Devotion pairs with
monarchy, not militarism. Sudan ("We are the army of God") is the rare high-God, high-Guns case.

The belligerence themes cohere, which validates the composite: blood↔sacrifice **r = 0.58**,
war↔enemy **0.52**, war↔blood 0.46, war↔sacrifice 0.44. *Figure: `outputs/god-vs-guns.svg`*
(the deity axis is a single 0–3 theme, so it forms four labelled bands — points jittered within).

## 2. The retired-belligerence gap is real and one-directional

Performance systematically *defangs* anthems: belligerence falls from a written mean of **24.3**
to a sung mean of **19.4**; zero-belligerence anthems rise from 57 (written) to **72** (sung); no
country's sung version is more belligerent than its written one.

Biggest "quietly defanged" anthems (written → sung):

| Country | Written → Sung | Gap | What drops out when sung |
|---|---|---|---|
| **Senegal** | 56 → 0 | **+56** | chorus 5: "if the enemy violates our frontiers… weapons in our hands" |
| Congo (Rep.) | 51 → 0 | +51 | "if we have to die… triumph through battle" |
| Albania | 49 → 0 | +49 | martial later stanzas |
| Haiti | 49 → 8 | +41 | fight-for-the-flag verses |
| Romania | 92 → 54 | +38 | three martial official verses sung only on 1 Dec |
| New Zealand | 36 → 0 | +36 | "Lord of battles… put our enemies to flight" (vv4–5) |
| United Kingdom | 44 → 10 | +33 | "scatter our enemies" (v2) |
| United States | 56 → 28 | +28 | "hireling and slave… gloom of the grave" (v3) |

Senegal topping this list is a *spot-check discovery*: the original pass scored only its
koras-and-balafons opening; the blind auditor caught the unsung martial chorus 5. *Figure:
`outputs/retired-gap.svg`.*

## 3. What anthems actually sing about (14 themes)

Share of anthems scoring ≥1 (as written):

| Theme | ≥1 | | Theme | ≥1 |
|---|---|---|---|---|
| Glory / pride | 71% | | War / arms | 45% |
| Land / nature | 70% | | Blood / death | 42% |
| Freedom / liberty | 64% | | **Ancestors / heritage** | **39%** |
| Unity / brotherhood | 58% | | Enemy / threat | 36% |
| Deity | 54% | | **The flag** | **34%** |
| Sacrifice | 45% | | **Labour / work** | **25%** |
| | | | **Monarch** | **12%** |

The three promoted themes land mid-table: **ancestors/heritage (39%) is more common than the
enemy (36%)**, and the flag (34%) nearly so. The monarch — the anthem stereotype — is still the
**rarest** theme. *Figure: `outputs/theme-prevalence.svg`.*

## 4. Regions have signatures

Mean theme score by region vs the global mean (*figure: `outputs/region-theme-heatmap.svg`*):

- **Africa** — the *developmental* signature: **labour/work +0.49** (highest), unity +0.44,
  freedom +0.22. African anthems are about building and uniting the nation.
- **Americas** — the *martial* signature: war **+0.42**, blood +0.32, sacrifice +0.29; monarch
  **0.0** (all republics). Most belligerent region (mean 34.5).
- **Asia** — *crown & sacrifice*: monarch +0.30 (highest), blood, sacrifice.
- **Europe** — *heritage*: **ancestors/heritage +0.17** (highest), monarch, land — the oldest
  anthems leaning on forefathers.
- **Oceania** — the *pious pastoral*: deity **+0.69**, land +0.31, unity +0.33; almost no
  belligerence (mean 5.9, lowest).

## 5. A deity × crown typology

- **Neither (secular) — 111** anthems (58%). The modern default.
- **God, no King — 61.** Devotional republics.
- **God *and* King — 13:** UK, Netherlands, Liechtenstein, Holy See, Tonga, Eswatini, Bhutan,
  Brunei, Cambodia, Kuwait, Malaysia, Oman.
- **King, no God — only 7.** A secular monarchy in song is rare.

## 6. Thematic families (k-means on the 13-theme fingerprint)

Promoting the new themes **reorganised the clusters** — two new families split out:

1. **Royal / devotional** (n=19): UK, Netherlands, Jordan, Malaysia, Kuwait, Morocco.
2. **Pastoral / civic** (n=65, low belligerence): Serbia, New Zealand, Norway, Suriname, Guyana.
3. **Labour / developmental** (n=32) — *new*, driven by unity + **labour** + glory: Togo,
   Guinea-Bissau, Niger, Haiti, Syria, Mali. The post-colonial "build the nation" family.
4. **Revolutionary / martial** (n=52, belligerence 54): Algeria, France, Romania, Mexico, Tunisia.
5. **Flag / patriotic** (n=24) — *new*, driven by **flag** + freedom + glory: United States,
   Albania, Turkey, Honduras, Namibia, Zimbabwe.

## 7. The most distinctive — and most average — anthem

- **Most distinctive:** Romania, United Kingdom, Algeria, France, Netherlands, Armenia, Tonga,
  Brunei — the extremes of heritage+belligerence (Romania), crown+God (UK/Tonga/Brunei), pure
  martial (Algeria/France), and the all-flag anthem (Armenia).
- **Most "average" anthem on Earth:** **Saint Kitts and Nevis**, then Mongolia, Grenada and
  Sri Lanka — anthems that sit near the global mean on every theme.

## 8. Age is a non-finding

Pearson r = **−0.10** between year-of-lyrics and belligerence (n=192). Older ≠ more warlike.

## 9. The wildcard catalogue — and what's next

The wildcard (theme 14) self-corrected the rubric: labour/work, the flag and ancestors/heritage
recurred enough to be promoted in v2 (they now appear in 88 / 116 / 138 records respectively; 92
former wildcards folded in). The remaining wildcard tail (77 distinct labels) points to the
**next** candidate theme: **peace** (13 anthems, often explicitly anti-war — South Africa's
"banish wars", Nicaragua, Slovenia). After that, religion/faith beyond a bare deity invocation (12).

The entertaining residue — emblems and oddities nations sing about: Guatemala's **quetzal**,
Lebanon's **cedar**, China's **Great Wall**, Mongolia's **Soyombo**, Montenegro's **Mount Lovćen**,
Senegal's **koras and balafons**, **Moldova singing about the Moldovan language**, **Uzbekistan
about knowledge & science**, Denmark's **Norse myth**, and Paraguay's **"Republic or Death."**

## Validation & caveats (state openly)

- **Validated, not infallible.** Blind second-rater agreement 96% within ±1 (300 cells); only 4
  of 150 as-written cells diverged by ≥2. Two corrections applied (Senegal under-scored — missed
  an unsung martial verse; Mongolia over-scored — idiomatic "sweat and blood" = labour, not
  blood). **Residual risk: under-scoring long multi-verse anthems**, not systematic bias.
- **v1 → v2 is additive.** The 3 promoted themes don't feed belligerence/deity/crown, so those
  composites are identical across versions (a built-in regression check that passed, 0 cells).
- **Translation bias** — 54 records flagged `translation-sensitive`; confidence-capped.
- **"As-sung" contested** for 20 anthems (`sung-assumed`); defaulted to verse 1.
- **Partial completeness** on a few long anthems (e.g. France, Afghanistan, Uruguay) — later
  verses summarised; headline scores robust.
- **Archaism** — high deity/monarch reflects the text's era, not current religiosity/government.
- **The Holy See edge case:** the Pope scored as monarch (sovereign of Vatican City); arguable.
- **Prior art:** the 2023 "fighting-word frequency" study; this work's novelty is the
  rubric-as-vector + the sung-vs-written gap.
