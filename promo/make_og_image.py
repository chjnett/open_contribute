#!/usr/bin/env python3
"""Generate a 1280x640 social-preview / Open Graph image for the repo.

Usage: python3 promo/make_og_image.py
Output: promo/social-preview.png
"""
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch

INK = "#1f2328"
MUTED = "#59636e"
GREEN = "#1a7f37"
RED = "#cf222e"
GREY = "#d1d9e0"
BG = "#ffffff"

W, H = 12.8, 6.4
fig = plt.figure(figsize=(W, H), dpi=100)
ax = fig.add_axes([0, 0, 1, 1])
ax.set_xlim(0, W)
ax.set_ylim(0, H)
ax.axis("off")

# background
ax.add_patch(plt.Rectangle((0, 0), W, H, color=BG, zorder=0))

# thin accent bar
ax.add_patch(plt.Rectangle((0.9, H - 0.28), 3.2, 0.06, color=GREEN, zorder=1))

# wordmark
ax.text(0.9, H - 0.75, "first-contribution",
        fontsize=34, fontweight="bold", color=INK, va="top", family="DejaVu Sans")

# tagline
ax.text(0.9, H - 1.75,
        "An Agent Skill that finds open-source issues you can actually get merged",
        fontsize=17.5, color=INK, va="top", family="DejaVu Sans")

# sub-line
ax.text(0.9, H - 2.25,
        "It measures whether a repo really merges outside PRs before recommending anything.",
        fontsize=12.5, color=MUTED, va="top", family="DejaVu Sans")

# mini stat cards (bottom-left)
cards = [
    ("grafana", "70%", "outside PRs merged", GREEN),
    ("chroma", "8%", "outside PRs merged", RED),
    ("2", "real PRs", "from a cold start", GREEN),
]
cx = 0.9
for label, big, small, color in cards:
    box = FancyBboxPatch((cx, 0.85), 2.6, 1.7,
                         boxstyle="round,pad=0.08,rounding_size=0.12",
                         linewidth=1.0, edgecolor=GREY, facecolor="#f6f8fa", zorder=2)
    ax.add_patch(box)
    ax.text(cx + 0.18, 2.12, label, fontsize=10.5, color=MUTED, va="top",
            family="DejaVu Sans", zorder=3)
    ax.text(cx + 0.18, 1.42, big, fontsize=24, fontweight="bold", color=color,
            va="top", family="DejaVu Sans", zorder=3)
    ax.text(cx + 0.18, 1.02, small, fontsize=9.5, color=MUTED, va="top",
            family="DejaVu Sans", zorder=3)
    cx += 2.85

# footer
ax.text(0.9, 0.32, "github.com/chjnett/open_contribute  ·  Claude Code plugin  ·  MIT  ·  EN / KO / RAG",
        fontsize=10.5, color=MUTED, va="center", family="DejaVu Sans", zorder=3)

fig.savefig("promo/social-preview.png", dpi=100, facecolor=BG)
plt.close(fig)
print("wrote promo/social-preview.png")
