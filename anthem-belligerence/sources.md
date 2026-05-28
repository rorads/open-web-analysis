# Sources — Anthem belligerence

Seed bibliography. Every scored anthem will link back to a source here, with a confidence
level. (Filled out during the corpus build.)

## Primary sources

| Source | URL | Coverage | Notes |
|--------|-----|----------|-------|
| NationalAnthems.info | https://nationalanthems.info | Lyrics, English translations, performed-verse notes for most states | Primary source; cross-check translations against Wikipedia |
| Wikipedia (per-country anthem articles) | https://en.wikipedia.org | Lyrics, history, sung-verse customs | Good for "which verse is sung" context |
| Wikisource | https://wikisource.org | Public-domain original-language texts | Use for original-language evidence lines |
| Official government / constitution pages | (per country) | Authoritative designation of the official verse(s) | Highest confidence for the as-sung determination |

## Prior art (to cite, not reuse)

| Work | URL | Relevance |
|------|-----|-----------|
| Trends in the texts of national anthems: a comparative study (2023) | https://pmc.ncbi.nlm.nih.gov/articles/PMC10458337/ | Measures topic frequencies incl. "fighting" across ~186 anthems; no belligerence index |
| The emotional geography of national anthems (Nature, 2025) | https://www.nature.com/articles/s41598-025-08956-6 | Predicts emotion from the *melody*, not lyrics — different axis |
| "Not Sports: A Color Coded Map of Every National Anthem's Subject" (2016) | https://www.allmysportsteamssuck.com/2016/06/23/not-sports-a-color-coded-map-of-every-national-anthems-subject/ | Casual single-bucket theme map; closest prior viz |
| national-anthems-clustering | https://github.com/lucas-de-sa/national-anthems-clustering | Unsupervised NLP clustering of anthem lyrics |

## Per-anthem provenance

To be recorded as a column in `data/processed/scores.csv`: source URL, retrieval date, and
confidence (`low` / `med` / `high`) per anthem and per as-written / as-sung determination.
