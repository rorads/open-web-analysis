"""Interactive 'God vs Guns' scatter (Plotly) for the blog.

Static labels can't fit the ~25 countries crammed into the bottom-right band, so this
emits a self-contained hover chart instead. Plotly is loaded from CDN to keep the file
small (~a few KB), so it embeds cleanly in Jekyll via an <iframe>.

Reads  data/processed/indices.json, data/countries.json
Writes <out>  (default: outputs/god-vs-guns-interactive.html)
Run:   uv run anthem-belligerence/src/plot_interactive.py [out.html]
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

import plotly.graph_objects as go

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


def main() -> int:
    out = Path(sys.argv[1]) if len(sys.argv) > 1 else HERE / "outputs/god-vs-guns-interactive.html"
    rows = load()
    import random
    random.seed(3)

    fig = go.Figure()
    for reg, col in REGION_COLORS.items():
        pts = [r for r in rows if r["region"] == reg]
        fig.add_trace(go.Scatter(
            x=[r["belligerence_sung"] for r in pts],
            # jitter Y within the 4 deity bands so points don't stack; ±7 never crosses a band
            y=[r["deity_sung"] + random.uniform(-7, 7) for r in pts],
            mode="markers",
            name=f"{reg} ({len(pts)})",
            marker=dict(size=9, color=col, line=dict(width=0.5, color="white")),
            customdata=[(r["country"], r["belligerence_sung"], r["deity_sung"],
                         r["crown_sung"], r["retired_gap"]) for r in pts],
            hovertemplate=(
                "<b>%{customdata[0]}</b><br>"
                "Belligerence (sung): %{customdata[1]:.0f}<br>"
                "Deity: %{customdata[2]:.0f} &nbsp; Crown: %{customdata[3]:.0f}<br>"
                "Retired gap (written→sung): %{customdata[4]:.0f}"
                "<extra></extra>"),
        ))

    fig.update_layout(
        title=dict(text="God vs Guns — national anthems as sung (hover for country)",
                   font=dict(color="white", size=18)),
        paper_bgcolor=BG, plot_bgcolor=PANEL, font=dict(color=FG),
        xaxis=dict(title="Belligerence index (as sung) →", range=[-5, 108],
                   gridcolor=GRID, zeroline=False),
        yaxis=dict(title="Deity (0–3 theme)", range=[-12, 114],
                   tickvals=[0, 33.3, 66.7, 100],
                   ticktext=["no God (0)", "passing (1)", "present (2)", "central (3)"],
                   gridcolor=GRID, zeroline=False),
        legend=dict(bgcolor=PANEL, bordercolor=GRID, borderwidth=1),
        margin=dict(l=70, r=30, t=60, b=110),
        annotations=[dict(
            text=("Deity is one 0–3 score (4 bands); points jittered vertically within their "
                  "band so they don't overlap. Belligerence combines 4 themes (near-continuous)."),
            showarrow=False, xref="paper", yref="paper", x=0.5, y=-0.22,
            font=dict(color="#94a3b8", size=11))],
    )
    fig.write_html(str(out), include_plotlyjs="cdn", full_html=True,
                   config={"displayModeBar": False, "responsive": True})
    print(f"wrote {out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
