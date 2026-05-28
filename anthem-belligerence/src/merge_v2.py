"""Build the v2 scores from v1 + the v2 promotion pass.

v2 = v1's records (10 themes carried over verbatim) + the 3 promoted themes
(labour_work, flag, ancestors_heritage) scored in the v2 pass. Any v1 wildcard whose label
maps to one of the 3 promoted themes is folded into that theme (no double-count, no loss):
the v2 pass score wins; if the v2 pass didn't score it but a matching wildcard exists, the
wildcard's score is converted into the promoted theme.

Reads  data/processed/scores_v1.json (archived v1) + data/processed/parts_v2/*.json
Writes data/processed/scores.json (v2, canonical)
Run:   uv run anthem-belligerence/src/merge_v2.py
"""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
NEW_THEMES = ["labour_work", "flag", "ancestors_heritage"]
# wildcard-label keywords that map onto a promoted theme
MAP = {
    "labour_work": ["labour", "labor", "work", "toil", "industr", "nation-build", "build"],
    "flag": ["flag", "tricolo", "banner", "colour", "color", "standard", "ensign"],
    "ancestors_heritage": ["ancestor", "forefather", "forebear", "heritage", "lineage",
                           "inheritance", "ancient", "ancestral"],
}


def wildcard_target(label: str) -> str | None:
    low = label.lower()
    for theme, kws in MAP.items():
        if any(k in low for k in kws):
            return theme
    return None


def main() -> int:
    v1 = json.loads((ROOT / "data/processed/scores_v1.json").read_text())
    new_by_key: dict[tuple, dict] = {}
    for p in sorted((ROOT / "data/processed/parts_v2").glob("*.json")):
        for r in json.loads(p.read_text()).get("records", []):
            new_by_key[(r["country"], r["version"])] = r.get("new_themes", {})

    promoted = {t: 0 for t in NEW_THEMES}
    reclassified = 0
    for rec in v1["records"]:
        themes = rec["themes"]
        key = (rec["country"], rec["version"])
        agent_new = new_by_key.get(key, {})

        # 1) fold a matching wildcard into its promoted theme (kept as fallback evidence)
        wc = themes.get("wildcard")
        wc_target = wildcard_target(wc["label"]) if wc and wc.get("label") else None
        if wc_target:
            if wc_target not in agent_new:  # agent didn't score it -> use the wildcard
                agent_new = {**agent_new, wc_target: {k: wc[k] for k in
                             ("score", "quote", "rationale", "confidence") if k in wc}}
            del themes["wildcard"]
            reclassified += 1

        # 2) attach the promoted themes (score >= 1 only)
        for t in NEW_THEMES:
            v = agent_new.get(t)
            if v and int(v.get("score", 0)) >= 1:
                themes[t] = {k: v[k] for k in ("score", "quote", "rationale", "confidence", "original")
                             if k in v}
                promoted[t] += 1

    v1["_schema"]["theme_keys"] = [
        "war_arms", "blood_death", "enemy_threat", "sacrifice", "deity", "monarch",
        "land_nature", "freedom_liberty", "unity_brotherhood", "glory_pride",
        "labour_work", "flag", "ancestors_heritage", "wildcard",
    ]
    v1["_schema"]["version"] = "v2"
    v1["_schema"]["v2_note"] = ("Themes 11-13 (labour_work, flag, ancestors_heritage) promoted "
                                "from wildcard and scored in a 2026-05-28 augmentation pass; the "
                                "other 10 themes carried over from v1 unchanged. Composites "
                                "(belligerence/deity/crown) are identical to v1.")
    (ROOT / "data/processed/scores.json").write_text(json.dumps(v1, ensure_ascii=False, indent=2))
    print(f"v2 records: {len(v1['records'])}  (records w/ promoted theme, by theme: {promoted})")
    print(f"wildcards reclassified into a promoted theme: {reclassified}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
