"""Chunk the not-yet-scored countries into batches for parallel scoring agents.

Reads data/countries.json, writes data/batches.json mapping batch-id -> [country].
Run: uv run anthem-belligerence/src/make_batches.py [batch_size]
"""
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
BATCH_SIZE = int(sys.argv[1]) if len(sys.argv) > 1 else 12


def main() -> None:
    countries = json.loads((ROOT / "data/countries.json").read_text())["countries"]
    todo = [c for c in countries if not c.get("done")]
    batches = {}
    for i in range(0, len(todo), BATCH_SIZE):
        bid = str(i // BATCH_SIZE + 1)
        batches[bid] = [
            {"name": c["name"], "iso3": c["iso3"], "region": c["region"]}
            for c in todo[i : i + BATCH_SIZE]
        ]
    out = {
        "_about": "Work assignment for scoring agents. Each agent processes one batch id.",
        "batch_size": BATCH_SIZE,
        "n_todo": len(todo),
        "n_batches": len(batches),
        "batches": batches,
    }
    (ROOT / "data/batches.json").write_text(json.dumps(out, ensure_ascii=False, indent=2))
    print(f"{len(todo)} countries -> {len(batches)} batches of <= {BATCH_SIZE}")
    for bid, items in batches.items():
        print(f"  batch {bid:>2}: {', '.join(c['name'] for c in items)}")


if __name__ == "__main__":
    main()
