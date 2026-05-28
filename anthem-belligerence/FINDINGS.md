# Findings — Anthem belligerence (PROVISIONAL)

> **Status: PROVISIONAL.** Full run of all 195 states, scored 2026-05-28 by parallel Claude
> Opus agent sessions against rubric `e668eec`. Not yet through a human stratified spot-check
> (METHODOLOGY §7). Numbers may shift at the margin; the directional findings are robust.
> Provenance: `data/processed/run.md`. Underlying data: `data/processed/{indices,exploratory,findings_extra}.json`.

## The question

What do nations sing about themselves, how warlike is it, and how much of that warlikeness
sits in the **full official text** but is dropped from the **verses actually performed**?
Each of 195 anthems (193 UN members + Holy See + Palestine) was scored on 11 themes (0–3),
twice — *as written* and *as sung*. 192 have lyrics; 3 are word-less (Spain, San Marino,
Bosnia and Herzegovina).

## 1. God and Guns repel; God and Crown attract

The marquee result. Across the 192 anthems with lyrics, the **deity** score is *negatively*
correlated with belligerence (Pearson **r = −0.26**; deity↔blood −0.25, deity↔war −0.20).
The most warlike anthems are overwhelmingly **secular-revolutionary** — Algeria, France,
Vietnam, Palestine, Tunisia, Cuba — all at deity 0. Meanwhile deity↔**monarch** is *positive*
(**r = +0.26**): where God appears, a king often does too (UK, Holy See, Tonga, Brunei, Oman).
So the "God vs Guns" axis genuinely pulls apart — devotion pairs with monarchy, not militarism.
Sudan ("We are the army of God") is the rare high-God, high-Guns exception.

The four belligerence themes cohere tightly, which validates treating them as one index:
blood↔sacrifice **r = 0.58**, war↔enemy **0.52**, war↔blood 0.46, war↔sacrifice 0.44.

*Figure: `outputs/god-vs-guns.svg`* (belligerence × deity, coloured by region; the deity axis
is a single 0–3 theme so it forms four bands — points are jittered within each band).

## 2. The retired-belligerence gap is real — and one-directional

Performance systematically *defangs* anthems. Aggregate belligerence falls from a written
mean of **24.1** to a sung mean of **19.5**; anthems scoring **zero** belligerence rise from
57 (written) to **72** (sung), and those scoring ≥50 fall from 31 to 23. No country's sung
version is *more* belligerent than its written one (enforced as a consistency check).

Biggest "quietly defanged" anthems (written → sung belligerence):

| Country | Written | Sung | Gap | What drops out when sung |
|---|---|---|---|---|
| Congo (Rep.) | 51 | 0 | **+51** | later verses ("if we have to die… triumph through battle") |
| Albania | 49 | 0 | **+49** | martial later stanzas |
| Haiti | 49 | 8 | +41 | the fight-for-the-flag verses |
| Romania | 92 | 54 | +38 | only v1 routine; the four martial official verses on 1 Dec |
| El Salvador, New Zealand, Mauritania | ~46/36/46 | low | +36 | NZ's "Lord of battles / put our enemies to flight" (vv4–5) |
| United Kingdom | 44 | 10 | +33 | "scatter our enemies" (v2, rarely sung) |
| United States | 56 | 28 | +28 | "hireling and slave… gloom of the grave" (v3) |

*Figure: `outputs/retired-gap.svg`* (written→sung dumbbell, top 20).

## 3. What anthems actually sing about

Most common themes (share of anthems scoring ≥1, as written):

| Theme | ≥1 | explicit (≥2) |
|---|---|---|
| Glory / pride | 71% | 46% |
| Land / nature | 70% | 42% |
| Freedom / liberty | 64% | 44% |
| Unity / brotherhood | 58% | 41% |
| Deity | 54% | 38% |
| Sacrifice | 45% | 30% |
| War / arms | 45% | 28% |
| Blood / death | 42% | 23% |
| Enemy / threat | 36% | 22% |
| **Monarch** | **12%** | 10% |

So ~7 in 10 anthems boast of glory or paint the landscape; **45% reach for arms and 42% for
blood**; and the monarch — the thing we stereotypically associate with anthems — is the
**rarest** theme, in just 1 in 8. *Figure: `outputs/theme-prevalence.svg`.*

## 4. Regions have signatures

Mean theme score by region (vs the global mean) gives each region a fingerprint
(*figure: `outputs/region-theme-heatmap.svg`*):

- **Americas** — the martial region: war **+0.42**, blood +0.32, sacrifice +0.29 (independence-
  war anthems), and monarch **0.0** (all republics). Most belligerent region overall (mean 34.5).
- **Africa** — unity **+0.44**, freedom +0.22, enemy +0.14: the post-colonial liberation profile.
- **Asia** — monarch **+0.30** (highest), blood +0.17, sacrifice +0.16: crown and sacrifice.
- **Europe** — mild and broad: land, deity, a little monarch; nothing extreme.
- **Oceania** — the pious pastoral: deity **+0.69**, land +0.31, unity +0.33, and almost no
  war/blood/enemy at all (mean belligerence 5.9, the lowest region by far).

## 5. A deity × crown typology

Classifying anthems by whether they invoke God (deity ≥2) and/or a ruler (monarch ≥2):

- **Neither (secular) — 111** anthems (58%). The modern default.
- **God, no King — 61.** Devotional republics.
- **God *and* King — 13:** UK, Netherlands, Liechtenstein, Holy See, Tonga, Eswatini, Bhutan,
  Brunei, Cambodia, Kuwait, Malaysia, Oman.
- **King, no God — only 7.** A secular monarchy in song is rare.

## 6. Five thematic families (k-means on the fingerprint)

Clustering the 192 anthems on their 10-theme vectors yields interpretable families:

1. **Royal / devotional** (n=19, low belligerence): UK, Netherlands, Jordan, Malaysia, Kuwait, Morocco.
2. **Pastoral** (n=27, land-dominant): Norway, Zimbabwe, Luxembourg, Guyana, Malawi.
3. **Civic-devotional** (n=37, deity+unity+freedom): Ghana, New Zealand, UAE, South Sudan.
4. **Revolutionary / martial** (n=54, mean belligerence 55.8): Algeria, France, Mexico, Tunisia, Romania.
5. **Proud / patriotic** (n=55, glory+land+unity): Portugal, Chile, Angola, Benin, Syria.

That a **54-country martial family** exists — over a quarter of all anthems — is itself the story.

## 7. The most distinctive — and the most average — anthem

Standardising the theme vectors and measuring distance from the global mean:

- **Most distinctive:** United Kingdom, Algeria, France, Romania, Netherlands, Tonga, Brunei,
  Oman — the extremes of crown+God (UK/Tonga/Brunei/Oman) and of belligerence (Algeria/France/Romania).
- **Most "average" anthem on Earth:** **Mongolia**, followed by the Maldives, Kenya, Saint
  Kitts and Nevis and Djibouti — anthems that hit the global mean across the board.

The world-average anthem vector is roughly: glory 1.2, land 1.3, freedom 1.2, unity 1.0,
deity 1.0, with low-to-moderate everything else.

## 8. Age is a non-finding

The most-cited intuition — that older anthems are more warlike — does **not** hold:
Pearson r = **−0.10** between year-of-lyrics and belligerence (n=192). Report it as a null.

## 9. The wildcard catalogue — themes the rubric missed

Theme 11 ("anything not covered by 1–10") was used on ~190 records and clusters into clear
recurring buckets — strong evidence the fixed rubric is missing real themes:

| Recurring wildcard | Distinct anthems | Promote to a v2 theme? |
|---|---|---|
| **Labour / work** | 21 | **Yes** — clearly a theme ("toil builds the nation") |
| **The flag** | 15 | **Yes** — anthems-to-the-flag are common |
| **Peace** (often explicitly anti-war) | 13 | Probably — the pacifist counter-theme |
| Religion/faith (beyond a bare deity invocation) | 12 | Maybe — refine the deity theme |
| A named place / river / mountain | 11 | Fold into land/nature |
| **Ancestors / forefathers / heritage** | ~9 | **Yes** — recurs across continents |

And the entertaining tail — **national emblems and oddities** each nation sings about:
Guatemala's **quetzal**, Lebanon's **cedar**, China's **Great Wall**, Mongolia's **Soyombo**
symbol, Montenegro's **Mount Lovćen**, Senegal's **koras and balafons** (musical instruments),
**Moldova singing about the Moldovan language itself**, **Uzbekistan about knowledge & science**,
Denmark's **Norse myth** (Freya's hall), and Paraguay's blunt motto **"Republic or Death."**

## Caveats (state these openly in any post)

- **Provisional / single-rater LLM scoring.** Grounded in a quoted line per score, but not yet
  human spot-checked at scale. Confidence: 1,456 high / 549 med / 21 low of 2,026 non-zero cells.
- **Translation bias** — 54 records flagged `translation-sensitive` (esp. "blood" vs "struggle"
  across Arabic/Slavic/Turkic anthems); these are confidence-capped.
- **"As-sung" is contested** for 20 anthems (`sung-assumed`); as-sung defaulted to verse 1.
- **Partial completeness** on a few long anthems (France, Afghanistan, Uruguay, Denmark,
  Micronesia, Vanuatu) — later verses summarised, not transcribed; headline scores robust.
- **Archaism** — a high deity/monarch score reflects the text's era, not the country's current
  religiosity or government.
- **Deity/crown indices are single 0–3 themes** → four discrete levels (the banding in the
  scatter is the data's true granularity, not an artefact).
- **Prior art:** the 2023 "fighting-word frequency" study and casual anthem-subject maps; this
  work's novelty is the **rubric-as-vector** + the **sung-vs-written gap**.
