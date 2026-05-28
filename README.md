# open-web-analysis

A collection of ground-up **qualitative→quantitative** analyses, most destined for
my blog at [rorads.github.io](https://rorads.github.io).

Each analysis answers a question whose evidence is *not* sitting in a clean dataset.
Instead the evidence is scattered, qualitative, and associative across the **open web**
— official pages, Wikipedia/Wiktionary, archives, public-domain texts, standards bodies,
lyrics, and so on. The value is the *synthesis*: scour that fuzzy evidence, score it against
a deliberately explicit rubric, and process it into composite numbers, indices, and graphs.
The interesting design choice is the rubric/ontology, not the cleverness of any one step.

This is the repeatable version of the [konbini convenience-benchmark](https://rorads.github.io)
method: define a rubric, score each item against it with per-item sources + a confidence
level, then aggregate into one clean composite and one memorable visual.

## Repository layout

This is a **monorepo of independent analyses**. Each analysis is a self-contained
directory; copy `_template/` to start a new one.

```
open-web-analysis/
├── README.md              # this file — index + conventions
├── CLAUDE.md              # conventions for AI-assisted work
├── pyproject.toml         # uv-managed deps, Python 3.12
├── .python-version
├── _template/             # skeleton — copy to start a new analysis
└── <analysis-name>/       # one directory per analysis (see below)
```

Each analysis directory has the same shape:

```
<analysis-name>/
├── README.md              # what / why / status / link to the published post
├── METHODOLOGY.md         # the rubric/ontology — FROZEN before scoring begins
├── sources.md             # consolidated bibliography with per-item confidence
├── data/
│   ├── raw/               # evidence exactly as fetched (never hand-edited)
│   └── processed/         # scored / derived data
├── src/                   # code
└── outputs/               # SVG figures + tables, blog-ready
```

## Conventions

- **Self-contained.** Analyses do not import from each other. If two analyses genuinely
  need the same helper, lift it into a `shared/` package *then* (extract on the second
  use, not in anticipation of it).
- **Freeze the methodology first.** `METHODOLOGY.md` — the rubric, theme definitions,
  scoring scale, weights, source allowlist, confidence policy — is written and agreed
  *before* any scoring. This is the konbini "co-write the methodology, then run it" pattern.
- **Sources + confidence per item.** Every scored item records where the evidence came
  from and a confidence level (`low` / `med` / `high`).
- **Raw vs processed.** `data/raw/` is evidence as fetched and is never hand-edited;
  scoring and derivations land in `data/processed/`.
- **Blog-ready visuals.** Export figures as SVG into `outputs/` so they drop straight
  into the blog's `assets/images/<slug>/`. Match the blog's dark palette where it helps
  consistency.
- **Public by default.** This repo is public (Apache-2.0). Keep an analysis open unless
  the underlying evidence or a per-item caveat says otherwise.

## Running

Dependencies are managed with [uv](https://docs.astral.sh/uv/) on Python 3.12.

```sh
uv sync          # create the environment
uv run <script>  # run any analysis script
```

## Analyses

| Analysis | Status | Post |
|----------|--------|------|
| [`anthem-belligerence/`](anthem-belligerence/) | Methodology draft (not frozen) | — |
