"""Aggregate anthem theme scores into composite indices, and validate the scores.

Reads  data/processed/scores.json
Writes data/processed/indices.json and data/processed/indices.csv
Run:   uv run anthem-belligerence/src/aggregate.py   (from repo root)

Stdlib only, no third-party deps. The fetch->score steps are done in-session by the
agent (see METHODOLOGY.md s6); this script is the deterministic aggregate + validate stage.
"""

from __future__ import annotations

import csv
import json
import sys
from pathlib import Path

THEME_KEYS = [
    "war_arms", "blood_death", "enemy_threat", "sacrifice", "deity", "monarch",
    "land_nature", "freedom_liberty", "unity_brotherhood", "glory_pride",
    "labour_work", "flag", "ancestors_heritage", "wildcard",
]
CONFIDENCES = {"low", "med", "high"}

# Belligerence index weights (see METHODOLOGY.md s5). Normalised against the max.
BELL_WEIGHTS = {"war_arms": 1.0, "blood_death": 1.0, "enemy_threat": 0.75, "sacrifice": 0.5}
BELL_MAX = 3 * sum(BELL_WEIGHTS.values())  # 9.75

HERE = Path(__file__).resolve().parent.parent
SCORES_PATH = HERE / "data" / "processed" / "scores.json"
OUT_JSON = HERE / "data" / "processed" / "indices.json"
OUT_CSV = HERE / "data" / "processed" / "indices.csv"


def vector(themes: dict) -> dict:
    """Full 11-theme vector, filling unlisted themes with 0."""
    return {k: int(themes.get(k, {}).get("score", 0)) for k in THEME_KEYS}


def belligerence(vec: dict) -> float:
    raw = sum(BELL_WEIGHTS[k] * vec[k] for k in BELL_WEIGHTS)
    return round(raw / BELL_MAX * 100, 1)


def idx(score: int) -> float:
    return round(score / 3 * 100, 1)


def validate(records: list[dict]) -> list[str]:
    errors: list[str] = []
    seen: dict[str, set[str]] = {}
    for r in records:
        tag = f"{r.get('country')} [{r.get('version')}]"
        seen.setdefault(r.get("country", "?"), set()).add(r.get("version", "?"))
        no_lyrics = "no-lyrics" in r.get("flags", [])
        themes = r.get("themes", {})
        if no_lyrics and themes:
            errors.append(f"{tag}: flagged no-lyrics but has theme scores")
        for k, v in themes.items():
            if k not in THEME_KEYS:
                errors.append(f"{tag}: unknown theme '{k}'")
                continue
            s = v.get("score")
            if not isinstance(s, int) or not (1 <= s <= 3):
                errors.append(f"{tag}/{k}: listed score must be int 1-3, got {s!r}")
            if not v.get("quote"):
                errors.append(f"{tag}/{k}: listed theme missing evidence quote")
            if not v.get("rationale"):
                errors.append(f"{tag}/{k}: missing rationale")
            if v.get("confidence") not in CONFIDENCES:
                errors.append(f"{tag}/{k}: confidence must be one of {CONFIDENCES}")
            if k == "wildcard" and not v.get("label"):
                errors.append(f"{tag}/wildcard: wildcard score needs a free-text label")
    for country, versions in seen.items():
        if {"as-sung", "as-written"} - versions:
            errors.append(f"{country}: expected both as-sung and as-written records, got {versions}")
    return errors


def main() -> int:
    data = json.loads(SCORES_PATH.read_text())
    records = data["records"]

    errors = validate(records)
    print("=== validation ===")
    if errors:
        for e in errors:
            print(f"  FAIL  {e}")
        print(f"  {len(errors)} problem(s) found.")
        return 1
    print(f"  OK - {len(records)} records, all listed themes have quote+rationale+confidence.\n")

    by_country: dict[str, dict] = {}
    for r in records:
        c = r["country"]
        vec = vector(r["themes"])
        by_country.setdefault(c, {"country": c, "flags": set()})
        by_country[c]["flags"].update(r.get("flags", []))
        by_country[c][r["version"]] = {
            "vector": vec,
            "belligerence": belligerence(vec),
            "deity_index": idx(vec["deity"]),
            "crown_index": idx(vec["monarch"]),
        }

    rows = []
    for c, d in by_country.items():
        no_lyrics = "no-lyrics" in d["flags"]
        w, s = d.get("as-written", {}), d.get("as-sung", {})
        rows.append({
            "country": c,
            "no_lyrics": no_lyrics,
            "belligerence_written": w.get("belligerence", 0.0),
            "belligerence_sung": s.get("belligerence", 0.0),
            "retired_gap": round(w.get("belligerence", 0.0) - s.get("belligerence", 0.0), 1),
            "deity_written": w.get("deity_index", 0.0),
            "deity_sung": s.get("deity_index", 0.0),
            "crown_written": w.get("crown_index", 0.0),
            "crown_sung": s.get("crown_index", 0.0),
        })

    scored = [r for r in rows if not r["no_lyrics"]]
    scored.sort(key=lambda r: r["belligerence_sung"], reverse=True)

    OUT_JSON.write_text(json.dumps({"by_country": {c: {k: (sorted(v) if isinstance(v, set) else v)
                                                       for k, v in d.items()}
                                                   for c, d in by_country.items()},
                                    "table": rows}, indent=2))
    with OUT_CSV.open("w", newline="") as f:
        wtr = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        wtr.writeheader()
        wtr.writerows(rows)

    print("=== belligerence (as-sung, desc) - excludes no-lyrics ===")
    print(f"  {'country':16} {'bell_sung':>9} {'bell_writ':>9} {'gap':>5} {'deity_s':>7} {'crown_s':>7}")
    for r in scored:
        print(f"  {r['country']:16} {r['belligerence_sung']:9.1f} {r['belligerence_written']:9.1f} "
              f"{r['retired_gap']:5.1f} {r['deity_sung']:7.1f} {r['crown_sung']:7.1f}")
    nl = [r["country"] for r in rows if r["no_lyrics"]]
    if nl:
        print(f"\n  no-lyrics (reported separately): {', '.join(nl)}")
    print("\n  biggest retired-belligerence gaps:")
    for r in sorted(scored, key=lambda r: r["retired_gap"], reverse=True)[:4]:
        print(f"    {r['country']:16} gap {r['retired_gap']:+.1f}  ({r['belligerence_written']:.1f} written -> {r['belligerence_sung']:.1f} sung)")

    print(f"\nWrote {OUT_JSON.relative_to(HERE.parent)} and {OUT_CSV.relative_to(HERE.parent)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
