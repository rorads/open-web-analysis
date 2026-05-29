"""Exploratory analysis (METHODOLOGY.md s8): theme correlations, region & age
correlates, k-means clustering on the thematic fingerprint, and a wildcard-label tally.

Exploratory by design (n~195): report what's striking, don't over-claim significance.

Reads  data/processed/indices.json, data/processed/scores.json,
       data/raw/anthems.json, data/countries.json
Writes data/processed/exploratory.json, outputs/theme-corr-heatmap.svg,
       outputs/age-vs-belligerence.svg
Run:   uv run anthem-belligerence/src/explore.py
"""
from __future__ import annotations

import json
from pathlib import Path

import matplotlib
import numpy as np
import pandas as pd

matplotlib.use("Agg")
import matplotlib.pyplot as plt

HERE = Path(__file__).resolve().parent.parent
THEMES = [
    "war_arms", "blood_death", "enemy_threat", "sacrifice", "deity", "monarch",
    "land_nature", "freedom_liberty", "unity_brotherhood", "glory_pride",
    "labour_work", "flag", "ancestors_heritage",
]
BG, PANEL, FG = "#0f172a", "#1e293b", "#e2e8f0"


def build_frame() -> pd.DataFrame:
    idx = json.loads((HERE / "data/processed/indices.json").read_text())["by_country"]
    region = {c["name"]: c["region"] for c in json.loads((HERE / "data/countries.json").read_text())["countries"]}
    year = {a["country"]: a.get("year_lyrics") for a in json.loads((HERE / "data/raw/anthems.json").read_text())["anthems"]}
    rows = []
    for c, d in idx.items():
        if "no-lyrics" in d.get("flags", []):
            continue
        w = d.get("as-written", {})
        s = d.get("as-sung", {})
        if not w or not s:
            continue
        vec = w["vector"]
        row = {
            "country": c, "region": region.get(c, "?"), "year_lyrics": year.get(c),
            "bell_written": w["belligerence"], "bell_sung": s["belligerence"],
            "gap": round(w["belligerence"] - s["belligerence"], 1),
            "deity": w["deity_index"], "crown": w["crown_index"],
        }
        row.update({t: vec[t] for t in THEMES})
        rows.append(row)
    return pd.DataFrame(rows)


def theme_correlations(df: pd.DataFrame) -> dict:
    corr = df[THEMES].corr(method="pearson").round(3)
    # heatmap — drawn as VECTOR rectangles (not imshow), so the colour survives SVG
    # sanitisers (e.g. GitHub) that strip embedded raster <image> layers.
    from matplotlib.patches import Rectangle
    from matplotlib.cm import ScalarMappable
    from matplotlib.colors import Normalize
    fig, ax = plt.subplots(figsize=(8, 7))
    fig.patch.set_facecolor(BG); ax.set_facecolor(PANEL)
    n = len(THEMES)
    cmap = plt.get_cmap("RdBu_r"); norm = Normalize(vmin=-1, vmax=1)
    for i in range(n):
        for j in range(n):
            v = corr.values[i, j]
            ax.add_patch(Rectangle((j - 0.5, i - 0.5), 1, 1, facecolor=cmap(norm(v)),
                                   edgecolor=BG, linewidth=0.5))
            ax.text(j, i, f"{v:.2f}", ha="center", va="center",
                    color="white" if abs(v) > 0.5 else FG, fontsize=6)
    ax.set_xlim(-0.5, n - 0.5); ax.set_ylim(n - 0.5, -0.5); ax.set_aspect("equal")
    ax.set_xticks(range(n)); ax.set_yticks(range(n))
    ax.set_xticklabels(THEMES, rotation=45, ha="right", color=FG, fontsize=8)
    ax.set_yticklabels(THEMES, color=FG, fontsize=8)
    ax.set_title("Theme co-occurrence (as-written, Pearson)", color="white", pad=12)
    sm = ScalarMappable(cmap=cmap, norm=norm); sm.set_array([])
    cb = fig.colorbar(sm, ax=ax, fraction=0.046); cb.ax.tick_params(colors=FG)
    cb.solids.set_rasterized(False)
    fig.tight_layout()
    fig.savefig(HERE / "outputs/theme-corr-heatmap.svg", facecolor=BG, bbox_inches="tight")
    plt.close(fig)
    # strongest off-diagonal pairs
    pairs = []
    for i in range(len(THEMES)):
        for j in range(i + 1, len(THEMES)):
            pairs.append((THEMES[i], THEMES[j], float(corr.values[i, j])))
    pairs.sort(key=lambda p: abs(p[2]), reverse=True)
    return {"matrix": corr.to_dict(), "top_pairs": pairs[:10]}


def age_correlate(df: pd.DataFrame) -> dict:
    sub = df.dropna(subset=["year_lyrics"]).copy()
    sub["year_lyrics"] = sub["year_lyrics"].astype(float)
    out = {"n_with_year": int(len(sub))}
    if len(sub) >= 5:
        r = float(np.corrcoef(sub["year_lyrics"], sub["bell_written"])[0, 1])
        out["pearson_year_vs_bell_written"] = round(r, 3)
        fig, ax = plt.subplots(figsize=(7, 5))
        fig.patch.set_facecolor(BG); ax.set_facecolor(PANEL)
        ax.scatter(sub["year_lyrics"], sub["bell_written"], s=40, c="#2d8cff",
                   edgecolors="white", linewidths=0.5)
        ax.set_xlabel("Year lyrics written  →", color=FG)
        ax.set_ylabel("Belligerence (as written)  →", color=FG)
        ax.set_title(f"Anthem age vs belligerence (n={len(sub)}, r={r:.2f})", color="white", pad=10)
        ax.tick_params(colors=FG)
        for sp in ax.spines.values():
            sp.set_color("#334155")
        fig.tight_layout()
        fig.savefig(HERE / "outputs/age-vs-belligerence.svg", facecolor=BG, bbox_inches="tight")
        plt.close(fig)
    return out


def region_table(df: pd.DataFrame) -> dict:
    g = df.groupby("region").agg(
        n=("country", "size"),
        bell_written=("bell_written", "mean"),
        bell_sung=("bell_sung", "mean"),
        deity=("deity", "mean"),
        crown=("crown", "mean"),
    ).round(1)
    return g.reset_index().to_dict(orient="records")


def kmeans(X: np.ndarray, k: int, seed: int = 7, iters: int = 100) -> np.ndarray:
    rng = np.random.default_rng(seed)
    cent = X[rng.choice(len(X), k, replace=False)]
    labels = np.zeros(len(X), dtype=int)
    for _ in range(iters):
        d = ((X[:, None, :] - cent[None, :, :]) ** 2).sum(2)
        new = d.argmin(1)
        if (new == labels).all():
            break
        labels = new
        for c in range(k):
            if (labels == c).any():
                cent[c] = X[labels == c].mean(0)
    return labels


def cluster(df: pd.DataFrame, k: int = 5) -> dict:
    X = df[THEMES].to_numpy(float)
    Xs = (X - X.mean(0)) / (X.std(0) + 1e-9)
    labels = kmeans(Xs, k)
    df = df.assign(cluster=labels)
    profiles = []
    for c in range(k):
        m = df[df.cluster == c]
        means = m[THEMES].mean().round(2)
        top = means.sort_values(ascending=False).head(3)
        profiles.append({
            "cluster": int(c), "n": int(len(m)),
            "top_themes": {t: float(top[t]) for t in top.index},
            "mean_bell_written": round(float(m["bell_written"].mean()), 1),
            "example_countries": m.sort_values("bell_written", ascending=False)["country"].head(6).tolist(),
        })
    return {"k": k, "profiles": profiles,
            "assignment": df[["country", "region", "cluster"]].to_dict(orient="records")}


def wildcard_tally() -> dict:
    recs = json.loads((HERE / "data/processed/scores.json").read_text())["records"]
    from collections import Counter
    labels = Counter()
    for r in recs:
        wc = r.get("themes", {}).get("wildcard")
        if wc and wc.get("label"):
            labels[wc["label"].strip().lower()] += 1
    return {"distinct_labels": len(labels), "most_common": labels.most_common(20)}


def main() -> int:
    df = build_frame()
    print(f"frame: {len(df)} scored countries (with lyrics)")
    res = {
        "n": int(len(df)),
        "theme_correlations": theme_correlations(df),
        "age": age_correlate(df),
        "by_region": region_table(df),
        "clusters": cluster(df),
        "wildcard": wildcard_tally(),
    }
    (HERE / "data/processed/exploratory.json").write_text(json.dumps(res, ensure_ascii=False, indent=2))

    print("\n=== strongest theme correlations (as-written) ===")
    for a, b, r in res["theme_correlations"]["top_pairs"]:
        print(f"  {a:18} {b:18} r={r:+.2f}")
    print("\n=== by region ===")
    for row in res["by_region"]:
        print(f"  {row['region']:10} n={row['n']:>3}  bell_w={row['bell_written']:>5}  "
              f"bell_s={row['bell_sung']:>5}  deity={row['deity']:>5}  crown={row['crown']:>5}")
    print("\n=== age ===")
    print(f"  {res['age']}")
    print("\n=== clusters (k-means on as-written fingerprint) ===")
    for p in res["clusters"]["profiles"]:
        themes = ", ".join(f"{t}={v}" for t, v in p["top_themes"].items())
        print(f"  cluster {p['cluster']} (n={p['n']}, bell_w={p['mean_bell_written']}): {themes}")
        print(f"    e.g. {', '.join(p['example_countries'])}")
    print("\n=== wildcard labels ===")
    print(f"  {res['wildcard']['distinct_labels']} distinct; top: {res['wildcard']['most_common'][:12]}")
    print("\nWrote data/processed/exploratory.json + outputs/theme-corr-heatmap.svg, age-vs-belligerence.svg")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
