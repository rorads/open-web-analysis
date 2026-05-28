"""Full-run visuals (METHODOLOGY.md s9).

1) 'God vs Guns' scatter: belligerence (x) vs deity (y), one point per country,
   coloured by region. As-sung is the default panel.
2) Retired-belligerence gap: dumbbell of the top-N countries by as-written -> as-sung drop.

Reads  data/processed/indices.json, data/countries.json
Writes outputs/god-vs-guns.svg, outputs/retired-gap.svg
Run:   uv run anthem-belligerence/src/plot_full.py
"""
from __future__ import annotations

import json
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt

HERE = Path(__file__).resolve().parent.parent
BG, PANEL, FG, GRID = "#0f172a", "#1e293b", "#e2e8f0", "#334155"
REGION_COLORS = {
    "Africa": "#f59e0b", "Asia": "#ef4444", "Europe": "#2d8cff",
    "Americas": "#10b981", "Oceania": "#a855f7",
}


def load():
    rows = [r for r in json.loads((HERE / "data/processed/indices.json").read_text())["table"]
            if not r["no_lyrics"]]
    region = {c["name"]: c["region"]
              for c in json.loads((HERE / "data/countries.json").read_text())["countries"]}
    for r in rows:
        r["region"] = region.get(r["country"], "?")
    return rows


def god_vs_guns(rows) -> None:
    fig, ax = plt.subplots(figsize=(10, 7.5))
    fig.patch.set_facecolor(BG); ax.set_facecolor(PANEL)
    # jitter identical points slightly so clusters at 0,0 are visible
    import random
    random.seed(3)
    for reg, col in REGION_COLORS.items():
        pts = [r for r in rows if r["region"] == reg]
        xs = [r["belligerence_sung"] + random.uniform(-0.8, 0.8) for r in pts]
        ys = [r["deity_sung"] + random.uniform(-0.8, 0.8) for r in pts]
        ax.scatter(xs, ys, s=55, c=col, edgecolors="white", linewidths=0.4,
                   alpha=0.85, label=f"{reg} ({len(pts)})", zorder=3)
    # label the belligerence leaders (spread along x); the low-belligerence/high-deity
    # devotional cluster is described in text rather than labelled (it overlaps badly).
    notable = sorted(rows, key=lambda r: r["belligerence_sung"], reverse=True)[:15]
    for r in notable:
        ax.annotate(r["country"], (r["belligerence_sung"], r["deity_sung"]),
                    xytext=(r["belligerence_sung"] + 1.2, r["deity_sung"] + 1.8),
                    color=FG, fontsize=7.5, zorder=5)
    ax.set_xlim(-5, 108); ax.set_ylim(-8, 112)
    ax.set_xlabel("Belligerence index  (as sung)  →", color=FG, fontsize=11)
    ax.set_ylabel("Deity index  (as sung)  →", color=FG, fontsize=11)
    ax.set_title(f"God vs Guns — national anthems as sung (n={len(rows)})",
                 color="white", fontsize=14, pad=14)
    ax.tick_params(colors=FG)
    for sp in ax.spines.values():
        sp.set_color(GRID)
    leg = ax.legend(loc="upper right", facecolor=PANEL, edgecolor=GRID, fontsize=9)
    for t in leg.get_texts():
        t.set_color(FG)
    fig.tight_layout()
    fig.savefig(HERE / "outputs/god-vs-guns.svg", facecolor=BG, bbox_inches="tight")
    plt.close(fig)


def retired_gap(rows, top_n: int = 20) -> None:
    ranked = sorted(rows, key=lambda r: r["retired_gap"], reverse=True)
    ranked = [r for r in ranked if r["retired_gap"] > 0][:top_n]
    fig, ax = plt.subplots(figsize=(9, max(5, 0.42 * len(ranked) + 1)))
    fig.patch.set_facecolor(BG); ax.set_facecolor(PANEL)
    for i, r in enumerate(ranked):
        y = len(ranked) - i
        ax.plot([r["belligerence_sung"], r["belligerence_written"]], [y, y],
                color=GRID, lw=2, zorder=2)
        ax.scatter(r["belligerence_sung"], y, s=60, c="#10b981", zorder=3,
                   edgecolors="white", linewidths=0.5)
        ax.scatter(r["belligerence_written"], y, s=60, c="#ef4444", zorder=3,
                   edgecolors="white", linewidths=0.5)
        ax.text(-3, y, r["country"], ha="right", va="center", color=FG, fontsize=8)
    ax.scatter([], [], c="#ef4444", label="as written", edgecolors="white")
    ax.scatter([], [], c="#10b981", label="as sung", edgecolors="white")
    ax.set_yticks([]); ax.set_xlim(-30, 108)
    ax.set_ylim(0.3, len(ranked) + 0.7)
    ax.set_xlabel("Belligerence index  →", color=FG, fontsize=11)
    ax.set_title(f"Retired belligerence — top {len(ranked)} written→sung gaps",
                 color="white", fontsize=14, pad=12)
    ax.tick_params(colors=FG)
    for sp in ax.spines.values():
        sp.set_color(GRID)
    leg = ax.legend(loc="lower right", facecolor=PANEL, edgecolor=GRID, fontsize=9)
    for t in leg.get_texts():
        t.set_color(FG)
    fig.tight_layout()
    fig.savefig(HERE / "outputs/retired-gap.svg", facecolor=BG, bbox_inches="tight")
    plt.close(fig)


def main() -> int:
    rows = load()
    god_vs_guns(rows)
    retired_gap(rows)
    print(f"wrote outputs/god-vs-guns.svg and outputs/retired-gap.svg (n={len(rows)})")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
