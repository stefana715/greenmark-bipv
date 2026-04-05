#!/usr/bin/env python3
"""
scoring_matrix.py — Content-based scoring analysis for BIPV in GBRS.

Generates:
  1. Radar/spider charts comparing all GBRS
  2. Heatmap of scores across dimensions
  3. Overall ranking bar chart
  4. Individual radar per GBRS
  5. Dimension-level analysis
  6. LaTeX table output

Usage:
  python src/scoring_matrix.py
"""
import sys, os
sys.path.insert(0, os.path.dirname(__file__))

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
from matplotlib.patches import FancyBboxPatch
import seaborn as sns
from utils import (
    load_scoring_matrix, DIMENSION_COLS, DIMENSION_LABELS,
    GBRS_COLORS, FIG_DIR, TABLE_DIR
)

# ── Style ──────────────────────────────────────────────
plt.rcParams.update({
    "font.family": "sans-serif",
    "font.sans-serif": ["Arial", "Helvetica", "DejaVu Sans"],
    "font.size": 11,
    "axes.titlesize": 13,
    "axes.labelsize": 11,
    "figure.dpi": 300,
    "savefig.dpi": 300,
    "savefig.bbox": "tight",
    "savefig.pad_inches": 0.15,
})


def radar_chart_all(df, score_cols):
    """Overlay radar chart for all GBRS on one plot."""
    N = len(score_cols)
    angles = np.linspace(0, 2 * np.pi, N, endpoint=False).tolist()
    angles += angles[:1]  # close the loop

    fig, ax = plt.subplots(figsize=(9, 9), subplot_kw=dict(polar=True))

    for _, row in df.iterrows():
        name = row["GBRS"]
        values = row[score_cols].values.tolist()
        values += values[:1]
        color = GBRS_COLORS.get(name, "#888888")
        ax.plot(angles, values, "o-", linewidth=2, label=name, color=color, markersize=5)
        ax.fill(angles, values, alpha=0.08, color=color)

    # Labels
    labels_short = [
        "D1: Credit\nWeight", "D2: BIPV\nSpecificity",
        "D3: Application\nCoverage", "D4: Design\nIntegration",
        "D5: Ambition\nLevel", "D6: Performance\nVerification",
        "D7: Envelope\nSynergy", "D8: Innovation\nPathway"
    ]
    ax.set_xticks(angles[:-1])
    ax.set_xticklabels(labels_short, fontsize=9)
    ax.set_ylim(0, 3.5)
    ax.set_yticks([0, 1, 2, 3])
    ax.set_yticklabels(["0", "1", "2", "3"], fontsize=8, color="grey")
    ax.set_title("BIPV Promotion Effectiveness Across Green Building Rating Systems",
                 fontsize=14, fontweight="bold", pad=25)
    ax.legend(loc="upper right", bbox_to_anchor=(1.35, 1.1), fontsize=9, frameon=True)

    plt.tight_layout()
    fig.savefig(os.path.join(FIG_DIR, "radar_all_gbrs.png"))
    fig.savefig(os.path.join(FIG_DIR, "radar_all_gbrs.pdf"))
    plt.close()
    print("  ✓ radar_all_gbrs.png/pdf")


def heatmap_scores(df, score_cols):
    """Heatmap: GBRS × Dimensions."""
    matrix = df.set_index("GBRS")[score_cols].copy()
    matrix.columns = [c.split("_", 1)[1].replace("_", " ") for c in score_cols]

    fig, ax = plt.subplots(figsize=(12, 5))
    sns.heatmap(
        matrix, annot=True, fmt="d", cmap="YlOrRd",
        linewidths=0.8, linecolor="white",
        vmin=0, vmax=3, cbar_kws={"label": "Score (0–3)", "shrink": 0.7},
        ax=ax
    )
    ax.set_title("Content-Based Assessment: BIPV Criteria in GBRS", fontsize=14, fontweight="bold")
    ax.set_xlabel("Assessment Dimension", fontsize=11)
    ax.set_ylabel("")
    ax.tick_params(axis="x", rotation=30)

    plt.tight_layout()
    fig.savefig(os.path.join(FIG_DIR, "heatmap_scoring.png"))
    fig.savefig(os.path.join(FIG_DIR, "heatmap_scoring.pdf"))
    plt.close()
    print("  ✓ heatmap_scoring.png/pdf")


def ranking_bar(df):
    """Horizontal bar chart of total scores with percentage."""
    df_sorted = df.sort_values("Total_Score", ascending=True)

    fig, ax = plt.subplots(figsize=(10, 5))
    colors = [GBRS_COLORS.get(g, "#888") for g in df_sorted["GBRS"]]
    bars = ax.barh(df_sorted["GBRS"], df_sorted["Total_Score"], color=colors, edgecolor="white", height=0.6)

    max_score = df_sorted["Max_Possible"].iloc[0]
    ax.set_xlim(0, max_score + 2)
    ax.set_xlabel("Total Score", fontsize=12)
    ax.set_title("GBRS Ranking by BIPV Promotion Effectiveness", fontsize=14, fontweight="bold")

    # Add percentage labels
    for bar, pct in zip(bars, df_sorted["Percentage"]):
        ax.text(bar.get_width() + 0.3, bar.get_y() + bar.get_height() / 2,
                f"{pct:.0f}%", va="center", fontsize=10, fontweight="bold")

    # Add max line
    ax.axvline(x=max_score, color="grey", linestyle="--", alpha=0.5, label=f"Max possible ({max_score})")
    ax.legend(fontsize=9)
    ax.grid(axis="x", alpha=0.3)

    plt.tight_layout()
    fig.savefig(os.path.join(FIG_DIR, "ranking_bar.png"))
    fig.savefig(os.path.join(FIG_DIR, "ranking_bar.pdf"))
    plt.close()
    print("  ✓ ranking_bar.png/pdf")


def dimension_analysis(df, score_cols):
    """Bar chart showing average + std for each dimension across all GBRS."""
    means = df[score_cols].mean()
    stds = df[score_cols].std()

    labels = [c.split("_", 1)[1].replace("_", "\n") for c in score_cols]

    fig, ax = plt.subplots(figsize=(11, 5))
    x = np.arange(len(score_cols))
    bars = ax.bar(x, means, yerr=stds, capsize=4,
                  color="#2E86AB", edgecolor="white", alpha=0.85)
    ax.set_xticks(x)
    ax.set_xticklabels(labels, fontsize=9)
    ax.set_ylabel("Average Score (0–3)", fontsize=11)
    ax.set_ylim(0, 3.5)
    ax.set_title("Dimension-Level Analysis: Average Scores Across All GBRS",
                 fontsize=14, fontweight="bold")
    ax.axhline(y=1.5, color="orange", linestyle="--", alpha=0.5, label="Midpoint (1.5)")
    ax.legend()
    ax.grid(axis="y", alpha=0.3)

    # Highlight weakest
    min_idx = means.argmin()
    bars[min_idx].set_color("#E94F37")
    bars[min_idx].set_edgecolor("#E94F37")

    plt.tight_layout()
    fig.savefig(os.path.join(FIG_DIR, "dimension_analysis.png"))
    fig.savefig(os.path.join(FIG_DIR, "dimension_analysis.pdf"))
    plt.close()
    print("  ✓ dimension_analysis.png/pdf")


def export_latex_table(df, score_cols):
    """Export scoring matrix as LaTeX table."""
    cols_display = ["GBRS", "Country"] + score_cols + ["Total_Score", "Percentage"]
    df_out = df[cols_display].copy()
    # Shorten column names
    rename = {c: c.split("_", 1)[1].replace("_", " ")[:12] for c in score_cols}
    rename["Total_Score"] = "Total"
    rename["Percentage"] = "%"
    df_out = df_out.rename(columns=rename)

    latex = df_out.to_latex(index=False, float_format="%.0f",
                            caption="Content-based scoring of BIPV criteria in eight GBRS (0=absent, 1=low, 2=moderate, 3=high).",
                            label="tab:scoring_matrix")
    path = os.path.join(TABLE_DIR, "scoring_matrix.tex")
    with open(path, "w") as f:
        f.write(latex)
    print(f"  ✓ {path}")

    # Also save as clean CSV
    csv_path = os.path.join(TABLE_DIR, "scoring_summary.csv")
    df[["GBRS", "Country"] + score_cols + ["Total_Score", "Percentage"]].to_csv(csv_path, index=False)
    print(f"  ✓ {csv_path}")


def sensitivity_analysis(df, score_cols):
    """Test if ranking changes when each dimension is weighted 2×."""
    results = {"Baseline": df.set_index("GBRS")["Total_Score"].rank(ascending=False)}

    for dim in score_cols:
        temp = df[score_cols].copy()
        temp[dim] = temp[dim] * 2  # double this dimension
        total = temp.sum(axis=1)
        rank = total.rank(ascending=False)
        results[dim.split("_", 1)[1][:15]] = rank.values

    sens_df = pd.DataFrame(results, index=df["GBRS"])

    fig, ax = plt.subplots(figsize=(14, 5))
    sns.heatmap(sens_df, annot=True, fmt=".0f", cmap="RdYlGn_r",
                linewidths=0.5, ax=ax, vmin=1, vmax=8,
                cbar_kws={"label": "Rank (1=best)"})
    ax.set_title("Sensitivity Analysis: Ranking Stability Under 2× Dimension Weighting",
                 fontsize=13, fontweight="bold")
    ax.set_xlabel("Scenario (Baseline + each dimension doubled)")

    plt.tight_layout()
    fig.savefig(os.path.join(FIG_DIR, "sensitivity_analysis.png"))
    fig.savefig(os.path.join(FIG_DIR, "sensitivity_analysis.pdf"))
    plt.close()
    print("  ✓ sensitivity_analysis.png/pdf")


# ── Main ───────────────────────────────────────────────
def main():
    print("=" * 60)
    print("BIPV × GBRS Scoring Matrix Analysis")
    print("=" * 60)

    df, score_cols = load_scoring_matrix()
    print(f"\nLoaded {len(df)} GBRS with {len(score_cols)} dimensions.\n")

    # Summary
    print("── Score Summary ──")
    for _, row in df.sort_values("Total_Score", ascending=False).iterrows():
        bar = "█" * int(row["Total_Score"]) + "░" * (24 - int(row["Total_Score"]))
        print(f"  {row['GBRS']:<12s} {bar} {row['Total_Score']:2.0f}/24 ({row['Percentage']:.0f}%)")

    print("\n── Generating Figures ──")
    radar_chart_all(df, score_cols)
    heatmap_scores(df, score_cols)
    ranking_bar(df)
    dimension_analysis(df, score_cols)
    sensitivity_analysis(df, score_cols)

    print("\n── Exporting Tables ──")
    export_latex_table(df, score_cols)

    print("\n✅ All outputs saved to outputs/figures/ and outputs/tables/")


if __name__ == "__main__":
    main()
