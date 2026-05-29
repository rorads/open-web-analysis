"""Bonus data-mining over the scored corpus (beyond METHODOLOGY.md s8): theme prevalence,
region thematic fingerprints, most distinctive vs most generic anthems, deity x crown
typology, belligerence distribution, and a wildcard-label taxonomy.

Reads  data/processed/indices.json, data/processed/scores.json, data/countries.json,
       data/raw/anthems.json
Writes data/processed/findings_extra.json + outputs/theme-prevalence.svg,
       outputs/region-theme-heatmap.svg, outputs/belligerence-dist.svg
Run:   uv run anthem-belligerence/src/explore_extra.py
"""
from __future__ import annotations

import json
import re
from collections import Counter, defaultdict
from pathlib import Path

import matplotlib
import numpy as np

matplotlib.use("Agg")
import matplotlib.pyplot as plt

HERE = Path(__file__).resolve().parent.parent
THEMES = [
    "war_arms", "blood_death", "enemy_threat", "sacrifice", "deity", "monarch",
    "land_nature", "freedom_liberty", "unity_brotherhood", "glory_pride",
    "labour_work", "flag", "ancestors_heritage",
]
NICE = {t: t.replace("_", " ") for t in THEMES}
BG, PANEL, FG, GRID = "#0f172a", "#1e293b", "#e2e8f0", "#334155"

# wildcard taxonomy: ordered keyword buckets (first match wins)
WILDCARD_BUCKETS = [
    ("flag", ["flag", "tricolo", "banner", "standard", "colours", "colors"]),
    ("labour / work", ["labour", "labor", "work", "toil", "industr", "build"]),
    ("peace", ["peace", "anti-war", "war as peace", "non-violen"]),
    ("religion / faith", ["religio", "faith", "islam", "buddh", "christ", "allah", "god", "prophet", "cross", "sacred", "holy"]),
    ("a named place / river / mountain", ["river", "mountain", "peak", "named", "city", "andes", "nile", "volcano", "lake", "specific place", "geograph"]),
    ("the sea / islands", ["sea", "ocean", "island", "coast", "wave", "maritime"]),
    ("sun / dawn / light", ["sun", "dawn", "light", "star", "sky", "morning"]),
    ("revolution / a historical event", ["revolut", "uprising", "historical", "independence day", "fourth of", "date"]),
    ("the people's virtue / morality", ["virtue", "moral", "honour", "honor", "dignit", "truth", "justice", "ethic"]),
    ("women / family / motherhood", ["women", "woman", "mother", "family", "wives", "daughter"]),
    ("food / wine / drink", ["wine", "food", "drink", "coffee", "harvest", "bread", "vine"]),
    ("monarch / dynasty / leader", ["dynast", "leader", "king", "ruler", "throne", "president"]),
    ("hope / future / progress", ["hope", "future", "progress", "renewal", "tomorrow", "develop"]),
    ("nature / wildlife / biodiversity", ["nature", "biodiversit", "wildlife", "animal", "forest", "flora", "fauna", "bird"]),
]


def bucket_wildcard(label: str) -> str:
    low = label.lower()
    for name, kws in WILDCARD_BUCKETS:
        if any(k in low for k in kws):
            return name
    return "other / unique"


def load():
    idx = json.loads((HERE / "data/processed/indices.json").read_text())["by_country"]
    region = {c["name"]: c["region"] for c in json.loads((HERE / "data/countries.json").read_text())["countries"]}
    rows = []
    for c, d in idx.items():
        if "no-lyrics" in d.get("flags", []):
            continue
        w, s = d.get("as-written"), d.get("as-sung")
        if not w or not s:
            continue
        rows.append({
            "country": c, "region": region.get(c, "?"),
            "vec": w["vector"], "vec_sung": s["vector"],
            "bell_w": w["belligerence"], "bell_s": s["belligerence"],
            "gap": round(w["belligerence"] - s["belligerence"], 1),
            "deity": w["vector"]["deity"], "crown": w["vector"]["monarch"],
        })
    return rows


def theme_prevalence(rows) -> dict:
    n = len(rows)
    out = {}
    for t in THEMES:
        scores = [r["vec"][t] for r in rows]
        out[t] = {
            "share_ge1": round(sum(x >= 1 for x in scores) / n, 3),
            "share_ge2": round(sum(x >= 2 for x in scores) / n, 3),
            "share_eq3": round(sum(x == 3 for x in scores) / n, 3),
            "mean": round(float(np.mean(scores)), 2),
        }
    order = sorted(THEMES, key=lambda t: out[t]["share_ge1"], reverse=True)
    # bar chart
    fig, ax = plt.subplots(figsize=(8, 5.5))
    fig.patch.set_facecolor(BG); ax.set_facecolor(PANEL)
    y = range(len(order))
    ax.barh(list(y), [out[t]["share_ge1"] * 100 for t in order], color="#2d8cff", alpha=0.55, label="mentions (≥1)")
    ax.barh(list(y), [out[t]["share_ge2"] * 100 for t in order], color="#2d8cff", label="explicit (≥2)")
    ax.set_yticks(list(y)); ax.set_yticklabels([NICE[t] for t in order], color=FG, fontsize=9)
    ax.invert_yaxis()
    ax.set_xlabel("% of anthems (as written)", color=FG)
    ax.set_title("What do anthems sing about? Theme prevalence (n=%d)" % len(rows), color="white", pad=12)
    ax.tick_params(colors=FG)
    for sp in ax.spines.values():
        sp.set_color(GRID)
    leg = ax.legend(facecolor=PANEL, edgecolor=GRID, fontsize=8)
    for tx in leg.get_texts():
        tx.set_color(FG)
    fig.tight_layout(); fig.savefig(HERE / "outputs/theme-prevalence.svg", facecolor=BG, bbox_inches="tight"); plt.close(fig)
    return {"per_theme": out, "ranked_by_mentions": order}


def region_fingerprint(rows) -> dict:
    regions = sorted({r["region"] for r in rows})
    mat = np.zeros((len(regions), len(THEMES)))
    for i, reg in enumerate(regions):
        sub = [r for r in rows if r["region"] == reg]
        for j, t in enumerate(THEMES):
            mat[i, j] = np.mean([r["vec"][t] for r in sub])
    # VECTOR rectangles (not imshow) so the colour survives SVG sanitisers (e.g. GitHub).
    from matplotlib.patches import Rectangle
    from matplotlib.cm import ScalarMappable
    from matplotlib.colors import Normalize
    fig, ax = plt.subplots(figsize=(9, 4.5))
    fig.patch.set_facecolor(BG); ax.set_facecolor(PANEL)
    nr, nc = len(regions), len(THEMES)
    cmap = plt.get_cmap("magma"); norm = Normalize(vmin=0, vmax=mat.max())
    for i in range(nr):
        for j in range(nc):
            ax.add_patch(Rectangle((j - 0.5, i - 0.5), 1, 1, facecolor=cmap(norm(mat[i, j])),
                                   edgecolor=BG, linewidth=0.5))
            ax.text(j, i, f"{mat[i, j]:.1f}", ha="center", va="center",
                    color="white" if mat[i, j] < mat.max() * 0.6 else "black", fontsize=7)
    ax.set_xlim(-0.5, nc - 0.5); ax.set_ylim(nr - 0.5, -0.5); ax.set_aspect("auto")
    ax.set_xticks(range(nc)); ax.set_xticklabels([NICE[t] for t in THEMES], rotation=45, ha="right", color=FG, fontsize=8)
    ax.set_yticks(range(nr)); ax.set_yticklabels(regions, color=FG, fontsize=9)
    ax.set_title("Region thematic fingerprints — mean theme score (as written)", color="white", pad=12)
    sm = ScalarMappable(cmap=cmap, norm=norm); sm.set_array([])
    cb = fig.colorbar(sm, ax=ax, fraction=0.025); cb.ax.tick_params(colors=FG)
    cb.solids.set_rasterized(False)
    fig.tight_layout(); fig.savefig(HERE / "outputs/region-theme-heatmap.svg", facecolor=BG, bbox_inches="tight"); plt.close(fig)
    # each region's top-3 distinctive themes vs global mean
    gmean = {t: np.mean([r["vec"][t] for r in rows]) for t in THEMES}
    sig = {}
    for i, reg in enumerate(regions):
        diffs = sorted(((t, round(mat[i, j] - gmean[t], 2)) for j, t in enumerate(THEMES)), key=lambda x: x[1], reverse=True)
        sig[reg] = diffs[:3]
    return {"matrix": {reg: {t: round(mat[i, j], 2) for j, t in enumerate(THEMES)} for i, reg in enumerate(regions)},
            "signature_themes": sig}


def distinctiveness(rows) -> dict:
    X = np.array([[r["vec"][t] for t in THEMES] for r in rows], float)
    mu, sd = X.mean(0), X.std(0) + 1e-9
    Z = (X - mu) / sd
    dist = np.linalg.norm(Z, axis=1)
    order = np.argsort(dist)
    most = [(rows[i]["country"], round(float(dist[i]), 2)) for i in order[::-1][:8]]
    generic = [(rows[i]["country"], round(float(dist[i]), 2)) for i in order[:8]]
    return {"most_distinctive": most, "most_generic": generic,
            "global_mean_vector": {t: round(float(mu[j]), 2) for j, t in enumerate(THEMES)}}


def typology(rows) -> dict:
    def q(pred):
        return [r["country"] for r in rows if pred(r)]
    theocratic = q(lambda r: r["deity"] >= 2 and r["crown"] < 2)
    monarchic = q(lambda r: r["crown"] >= 2 and r["deity"] < 2)
    both = q(lambda r: r["deity"] >= 2 and r["crown"] >= 2)
    secular = q(lambda r: r["deity"] < 2 and r["crown"] < 2)
    return {"counts": {"god_not_king": len(theocratic), "king_not_god": len(monarchic),
                       "god_and_king": len(both), "neither": len(secular)},
            "god_and_king_examples": both[:12], "king_not_god_examples": monarchic[:12]}


def belligerence_dist(rows) -> dict:
    bw = np.array([r["bell_w"] for r in rows])
    bs = np.array([r["bell_s"] for r in rows])
    fig, ax = plt.subplots(figsize=(8, 5))
    fig.patch.set_facecolor(BG); ax.set_facecolor(PANEL)
    bins = np.arange(0, 105, 7.7)
    ax.hist(bw, bins=bins, color="#ef4444", alpha=0.55, label="as written")
    ax.hist(bs, bins=bins, color="#10b981", alpha=0.6, label="as sung")
    ax.set_xlabel("Belligerence index", color=FG); ax.set_ylabel("# anthems", color=FG)
    ax.set_title("Belligerence distribution: written vs sung (n=%d)" % len(rows), color="white", pad=12)
    ax.tick_params(colors=FG)
    for sp in ax.spines.values():
        sp.set_color(GRID)
    leg = ax.legend(facecolor=PANEL, edgecolor=GRID, fontsize=9)
    for tx in leg.get_texts():
        tx.set_color(FG)
    fig.tight_layout(); fig.savefig(HERE / "outputs/belligerence-dist.svg", facecolor=BG, bbox_inches="tight"); plt.close(fig)
    return {"written": {"mean": round(float(bw.mean()), 1), "median": round(float(np.median(bw)), 1),
                        "zero": int((bw == 0).sum()), "ge50": int((bw >= 50).sum())},
            "sung": {"mean": round(float(bs.mean()), 1), "median": round(float(np.median(bs)), 1),
                     "zero": int((bs == 0).sum()), "ge50": int((bs >= 50).sum())}}


def wildcard_taxonomy() -> dict:
    recs = json.loads((HERE / "data/processed/scores.json").read_text())["records"]
    raw = []
    for r in recs:
        wc = r.get("themes", {}).get("wildcard")
        if wc and wc.get("label"):
            raw.append((r["country"], wc["label"].strip()))
    buckets = defaultdict(list)
    for country, label in raw:
        buckets[bucket_wildcard(label)].append(f"{country}: {label}")
    counts = {k: len(set(v)) for k, v in sorted(buckets.items(), key=lambda kv: -len(kv[1]))}
    uniques = sorted(set(f"{c}: {l}" for c, l in raw if bucket_wildcard(l) == "other / unique"))
    return {"bucket_counts": counts, "n_wildcard_records": len(raw),
            "unique_examples": uniques[:40]}


def main() -> int:
    rows = load()
    res = {
        "n": len(rows),
        "theme_prevalence": theme_prevalence(rows),
        "region_fingerprint": region_fingerprint(rows),
        "distinctiveness": distinctiveness(rows),
        "typology": typology(rows),
        "belligerence_distribution": belligerence_dist(rows),
        "wildcard_taxonomy": wildcard_taxonomy(),
    }
    (HERE / "data/processed/findings_extra.json").write_text(json.dumps(res, ensure_ascii=False, indent=2))

    tp = res["theme_prevalence"]
    print("=== theme prevalence (share mentioning ≥1, as written) ===")
    for t in tp["ranked_by_mentions"]:
        d = tp["per_theme"][t]
        print(f"  {NICE[t]:18} ≥1 {d['share_ge1']*100:4.0f}%   ≥2 {d['share_ge2']*100:4.0f}%   mean {d['mean']}")
    print("\n=== region signature themes (vs global mean) ===")
    for reg, sig in res["region_fingerprint"]["signature_themes"].items():
        print(f"  {reg:9}: " + ", ".join(f"{NICE[t]} (+{d})" for t, d in sig))
    print("\n=== most distinctive anthems ===")
    print("  " + ", ".join(f"{c}" for c, _ in res["distinctiveness"]["most_distinctive"]))
    print("=== most generic (closest to the world-average anthem) ===")
    print("  " + ", ".join(f"{c}" for c, _ in res["distinctiveness"]["most_generic"]))
    print("\n=== deity x crown typology ===", res["typology"]["counts"])
    print("  God+King:", ", ".join(res["typology"]["god_and_king_examples"]))
    print("\n=== belligerence distribution ===", res["belligerence_distribution"])
    print("\n=== wildcard taxonomy (distinct country-labels per bucket) ===")
    for k, v in res["wildcard_taxonomy"]["bucket_counts"].items():
        print(f"  {k:38} {v}")
    print("\nWrote findings_extra.json + theme-prevalence / region-theme-heatmap / belligerence-dist SVGs")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
