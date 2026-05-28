# CLAUDE.md

Conventions for AI-assisted work in this repo. Read alongside `README.md`.

## What this repo is

A monorepo of independent **qualitative→quantitative** analyses. Each answers a question
whose evidence is scattered across the open web, scores that evidence against an explicit
rubric, and aggregates it into a composite metric plus a standout visual. The output of
most analyses is a blog post at `rorads.github.io`; this repo is the research bundle behind it.

## The method (every analysis follows it)

1. **Freeze the methodology first.** Write `METHODOLOGY.md` — question, scope, unit of
   analysis, rubric, theme/dimension definitions, scoring scale, composite weights, source
   allowlist, confidence policy — and get it agreed *before* scoring anything. Treat the
   frozen rubric as the contract; if scoring forces a rubric change, change `METHODOLOGY.md`
   deliberately and note it, don't quietly drift.
2. **Build the corpus into `data/raw/`.** Evidence exactly as fetched, never hand-edited.
   Record provenance for each item in `sources.md`.
3. **Score against the rubric into `data/processed/`.** Each non-zero score carries a
   quoted evidence line and a confidence level (`low`/`med`/`high`). LLM-assisted scoring
   must ground every score in the supplied source text, not model recall.
4. **Human spot-check.** Review a stratified sample, including known/extreme cases, against
   the LLM scores; recalibrate the rubric or weights if there's systematic divergence; re-run.
5. **Aggregate + visualise.** Compute composites; export SVG figures to `outputs/`.

## Starting a new analysis

Copy `_template/` to `<analysis-name>/` and fill in `README.md` and `METHODOLOGY.md`.
Add a row to the Analyses table in the top-level `README.md`.

## Conventions

- One directory per analysis; analyses never import from each other. Extract a shared
  helper into a `shared/` package only on the *second* real use, not in anticipation.
- `data/raw/` is immutable evidence; derived/scored data goes in `data/processed/`.
- Figures export as **SVG** into `outputs/`, sized and themed to drop into the blog's
  `assets/images/<slug>/`.
- Every analysis names its open-web sources explicitly and records a confidence level per
  scored item. No walled gardens (anything requiring a login).
- Tooling is **uv** on Python 3.12 (`uv sync`, `uv run`).

## Git

- Repo is public (Apache-2.0). Default branch is `main`.
- Commits attributed to `Rory Scott <rory09@gmail.com>`.
- Don't create pull requests unless explicitly asked.
