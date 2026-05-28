"""Merge per-batch part files from scoring agents into the canonical data files.

- data/raw/parts/*.json        each: {"anthems": [ <anthem entry>, ... ]}
- data/processed/parts/*.json  each: {"records": [ <score record>, ... ]}

Merges into data/raw/anthems.json (key: country) and data/processed/scores.json
(key: country+version). Existing entries are NEVER overwritten (calibration set is
safe); only new countries are added. Light structural validation; full theme
validation lives in aggregate.py.

Run: uv run anthem-belligerence/src/merge_parts.py
"""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
THEME_KEYS = {
    "war_arms", "blood_death", "enemy_threat", "sacrifice", "deity", "monarch",
    "land_nature", "freedom_liberty", "unity_brotherhood", "glory_pride", "wildcard",
}
ANTHEM_REQ = {"country", "iso3", "title", "no_lyrics", "completeness", "source_urls"}


def _load(path: Path) -> dict:
    return json.loads(path.read_text())


def main() -> None:
    problems: list[str] = []

    # --- anthems ---
    anthems = _load(ROOT / "data/raw/anthems.json")
    have = {a["country"] for a in anthems["anthems"]}
    raw_parts = sorted((ROOT / "data/raw/parts").glob("*.json"))
    added_a = 0
    for p in raw_parts:
        for a in _load(p).get("anthems", []):
            miss = ANTHEM_REQ - set(a)
            if miss:
                problems.append(f"{p.name}: anthem {a.get('country','?')} missing {sorted(miss)}")
                continue
            if a["country"] in have:
                continue
            anthems["anthems"].append(a)
            have.add(a["country"])
            added_a += 1

    # --- scores ---
    scores = _load(ROOT / "data/processed/scores.json")
    have_r = {(r["country"], r["version"]) for r in scores["records"]}
    score_parts = sorted((ROOT / "data/processed/parts").glob("*.json"))
    added_r = 0
    for p in score_parts:
        for r in _load(p).get("records", []):
            if r.get("version") not in {"as-written", "as-sung"}:
                problems.append(f"{p.name}: {r.get('country','?')} bad version {r.get('version')}")
                continue
            bad = set(r.get("themes", {})) - THEME_KEYS
            if bad:
                problems.append(f"{p.name}: {r['country']}/{r['version']} unknown themes {sorted(bad)}")
                continue
            key = (r["country"], r["version"])
            if key in have_r:
                continue
            scores["records"].append(r)
            have_r.add(key)
            added_r += 1

    if problems:
        print("PROBLEMS (not merged):")
        for x in problems:
            print("  -", x)

    (ROOT / "data/raw/anthems.json").write_text(json.dumps(anthems, ensure_ascii=False, indent=2))
    (ROOT / "data/processed/scores.json").write_text(json.dumps(scores, ensure_ascii=False, indent=2))
    print(f"merged +{added_a} anthems (total {len(anthems['anthems'])}), "
          f"+{added_r} score records (total {len(scores['records'])})")

    # coverage check against master list
    master = {c["name"] for c in _load(ROOT / "data/countries.json")["countries"]}
    scored = {a["country"] for a in anthems["anthems"]}
    missing = sorted(master - scored)
    if missing:
        print(f"STILL MISSING {len(missing)}: {', '.join(missing)}")
    else:
        print("coverage: all 195 present")


if __name__ == "__main__":
    main()
