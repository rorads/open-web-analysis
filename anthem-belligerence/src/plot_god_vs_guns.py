"""Draft 'God vs Guns' scatter for the calibration sample.

Reads  data/processed/indices.json
Writes outputs/god-vs-guns-sample.svg
Run:   uv run anthem-belligerence/src/plot_god_vs_guns.py   (from repo root)

x = belligerence index (as sung), y = deity index (as sung). No-lyrics anthems excluded.
Styled dark to match the blog. This is a draft on n<=10 for the calibration checkpoint.
"""

from __future__ import annotations

import json
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt

HERE = Path(__file__).resolve().parent.parent
INDICES = HERE / "data" / "processed" / "indices.json"
OUT = HERE / "outputs" / "god-vs-guns-sample.svg"

BG = "#0f172a"
PANEL = "#1e293b"
ACCENT = "#2d8cff"
FG = "#e2e8f0"

# small per-label nudges (dx, dy) to stop overlapping annotations
NUDGE = {
    "Switzerland": (2, 4), "South Africa": (2, -7), "Germany": (2, 4),
    "Japan": (2, 0), "Nepal": (2, 3), "United Kingdom": (-3, 4),
    "United States": (2, 3), "France": (-4, 4), "Algeria": (-6, 4),
}


def main() -> int:
    rows = [r for r in json.loads(INDICES.read_text())["table"] if not r["no_lyrics"]]

    fig, ax = plt.subplots(figsize=(8, 6))
    fig.patch.set_facecolor(BG)
    ax.set_facecolor(PANEL)

    xs = [r["belligerence_sung"] for r in rows]
    ys = [r["deity_sung"] for r in rows]
    ax.scatter(xs, ys, s=90, c=ACCENT, edgecolors="white", linewidths=0.8, zorder=3)

    for r in rows:
        dx, dy = NUDGE.get(r["country"], (2, 3))
        ax.annotate(r["country"], (r["belligerence_sung"], r["deity_sung"]),
                    xytext=(r["belligerence_sung"] + dx, r["deity_sung"] + dy),
                    color=FG, fontsize=9, zorder=4)

    ax.set_xlim(-5, 108)
    ax.set_ylim(-8, 112)
    ax.set_xlabel("Belligerence index  (as sung)  →", color=FG, fontsize=11)
    ax.set_ylabel("Deity index  (as sung)  →", color=FG, fontsize=11)
    ax.set_title("God vs Guns — national anthems (calibration sample, n=%d)" % len(rows),
                 color="white", fontsize=13, pad=14)

    for spine in ax.spines.values():
        spine.set_color("#475569")
    ax.tick_params(colors=FG)
    ax.grid(True, color="#334155", linewidth=0.5, zorder=0)

    OUT.parent.mkdir(parents=True, exist_ok=True)
    fig.tight_layout()
    fig.savefig(OUT, format="svg", facecolor=BG)
    print(f"Wrote {OUT.relative_to(HERE.parent)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
