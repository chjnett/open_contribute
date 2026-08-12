#!/usr/bin/env python3
"""Charts for the open_contribute README, built only from measurements taken 2026-08-12."""
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Patch

INK = "#1f2328"
MUTED = "#59636e"
GREEN = "#1a7f37"
RED = "#cf222e"
GREY = "#d1d9e0"

plt.rcParams.update({
    "font.family": "DejaVu Sans",
    "figure.facecolor": "white",
    "axes.facecolor": "white",
    "text.color": INK,
    "axes.labelcolor": INK,
    "xtick.color": MUTED,
    "ytick.color": MUTED,
    "axes.edgecolor": GREY,
})

# ---------------------------------------------------------------- chart 1
# Share of merged PRs NOT authored by the repo's top-5 most frequent authors,
# bots excluded. One sample of up to 100 recently-merged PRs per repo.
repos = [
    ("grafana/grafana", 70), ("prometheus/prometheus", 66), ("argoproj/argo-cd", 59),
    ("run-llama/llama_index", 50), ("deepset-ai/haystack", 45),
    ("kubernetes-sigs/kustomize", 41), ("milvus-io/milvus", 38),
    ("Unstructured-IO/unstructured", 36), ("aquasecurity/trivy", 32),
    ("goharbor/harbor", 32), ("qdrant/qdrant", 29), ("langchain-ai/langchain", 23),
    ("weaviate/weaviate", 21), ("helm/helm", 13), ("chroma-core/chroma", 8),
]
THRESHOLD = 25
repos.sort(key=lambda r: r[1])
names = [r[0] for r in repos]
vals = [r[1] for r in repos]
colors = [GREEN if v >= THRESHOLD else RED for v in vals]

fig, ax = plt.subplots(figsize=(11, 7))
bars = ax.barh(names, vals, color=colors, height=0.68, zorder=3)
ax.axvline(THRESHOLD, color=MUTED, lw=1.3, ls="--", zorder=1)
ax.text(THRESHOLD + 1, -0.95, f"{THRESHOLD}% — healthy floor", fontsize=10,
        color=MUTED, va="center", style="italic")

for b, v in zip(bars, vals):
    ax.text(v + 2.2, b.get_y() + b.get_height() / 2, f"{v}%",
            va="center", fontsize=10.5, color=INK, fontweight="bold", zorder=4)

ax.set_xlim(0, 80)
ax.set_xlabel("Share of merged PRs from outside the top-5 authors", fontsize=11, labelpad=10)
ax.set_title("Do outside pull requests actually get merged?",
             fontsize=16, fontweight="bold", pad=26, loc="left")
ax.text(0, 1.035, "Bots excluded. One sample of up to 100 recently-merged PRs per repo, measured 2026-08-12.",
        transform=ax.transAxes, fontsize=10, color=MUTED)
ax.spines[["top", "right", "left"]].set_visible(False)
ax.tick_params(axis="y", length=0, labelsize=10.5)
ax.xaxis.grid(True, color=GREY, lw=0.7)
ax.set_axisbelow(True)
ax.legend(handles=[Patch(facecolor=GREEN, label="Passes the gate"),
                   Patch(facecolor=RED, label="Warning")],
          loc="lower right", frameon=False, fontsize=10.5)
fig.tight_layout()
fig.savefig("assets/merge_gate.png", dpi=170, bbox_inches="tight")
plt.close(fig)

# ---------------------------------------------------------------- chart 2
# Attrition when triaging candidate issues: how many still had no linked PR.
fig, ax = plt.subplots(figsize=(11, 4.2))
groups = [
    ("Contribution-labelled\n6 infra repos, since 2025-01", 40, 6),
    ("Recent unassigned bugs\n7 infra repos, since 2026-06-15", 121, 37),
]
y = [1.0, 0.0]
for (label, total, clean), yy in zip(groups, y):
    ax.barh(yy, total, color=GREY, height=0.5, zorder=3)
    ax.barh(yy, clean, color=GREEN, height=0.5, zorder=4)
    taken = total - clean
    ax.text(total + 3, yy, f"{taken} of {total} already taken  ·  {taken*100//total}%",
            va="center", fontsize=11.5, color=INK, fontweight="bold", zorder=5)
    ax.text(clean + 3 if clean < 20 else clean / 2, yy,
            f"{clean} open", va="center", ha="left" if clean < 20 else "center",
            fontsize=10.5, color=INK if clean < 20 else "white",
            fontweight="bold", zorder=5)

ax.set_yticks(y)
ax.set_yticklabels([g[0] for g in groups], fontsize=10.5)
ax.set_ylim(-0.55, 1.55)
ax.set_xlim(0, 215)
ax.set_xlabel("Candidate issues screened", fontsize=11, labelpad=8)
ax.set_title("Most candidates are already taken — labelled ones most of all",
             fontsize=15.5, fontweight="bold", pad=64, loc="left")
ax.text(0, 1.245, "Every candidate checked for a linked PR via the issue timeline. Measured 2026-08-12.",
        transform=ax.transAxes, fontsize=10, color=MUTED)
ax.spines[["top", "right", "left"]].set_visible(False)
ax.tick_params(axis="y", length=0)
ax.xaxis.grid(True, color=GREY, lw=0.7)
ax.set_axisbelow(True)
ax.legend(handles=[Patch(facecolor=GREEN, label="No linked PR — still claimable"),
                   Patch(facecolor=GREY, label="Already had a linked PR")],
          loc="lower left", bbox_to_anchor=(0, 1.03), ncol=2,
          frameon=False, fontsize=10.5)
fig.tight_layout()
fig.savefig("assets/triage_attrition.png", dpi=170, bbox_inches="tight")
plt.close(fig)

print("wrote assets/merge_gate.png and assets/triage_attrition.png")
