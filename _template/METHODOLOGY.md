# Methodology — <Analysis name>

> **Freeze this before scoring.** The rubric below is the contract for the analysis. If
> scoring forces a change, edit this document deliberately and note what changed and why —
> don't let the rubric drift silently.

**Status:** _DRAFT — not frozen_

## 1. Question

<The precise question. Narrow is good — the narrowness is the argument.>

## 2. Scope & unit of analysis

- **Population:** <what set of items is scored, and how it's bounded>
- **Unit:** <what exactly gets one score — and any sub-units, e.g. variants>
- **Exclusions:** <what's deliberately out of scope, and why>

## 3. Corpus & sources

- **Source allowlist:** <the open-web sources that are acceptable; no walled gardens>
- **Provenance:** every item records its source URL + retrieval date in `sources.md`.
- **Translation / normalisation policy:** <if relevant, how non-English or messy evidence
  is handled, and how that affects confidence>

## 4. Rubric

For each item, score each dimension on the scale below, with a quoted evidence line and a
confidence level.

| Dimension | Definition | What counts / doesn't |
|-----------|------------|-----------------------|
| <dim 1>   | <…>        | <…>                   |

**Scale (per dimension):**

- **0 — Absent**
- **1 — …**
- **2 — …**
- **3 — …**

**Evidence requirement:** every non-zero score cites a specific quoted line/fact from the
source, plus a confidence level (`low` / `med` / `high`).

## 5. Composite indices

- **<Index name>** = <formula over the dimension scores, with explicit weights>, normalised
  to 0–100. Weights are a starting proposal, subject to calibration in §7.

## 6. Scoring process

1. LLM-assisted scoring grounded in the supplied source text (not model recall).
2. Output: one row per item with dimension scores, evidence lines, confidences.

## 7. Calibration & human spot-check

- Stratified sample to review by hand: <which items, including known/extreme cases>.
- If LLM scores diverge systematically from human review, adjust the rubric/weights here,
  note the change, and re-run.

## 8. Visuals

- <The one standout visual, and any supporting ones.>

## 9. Threats to validity / caveats

- <Known biases and limitations to acknowledge openly in the post.>
