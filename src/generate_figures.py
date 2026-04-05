#!/usr/bin/env python3
"""
generate_figures.py — Generate all publication-quality figures.

Runs both scoring_matrix and bibliometric analysis, plus additional figures.

Usage:
  python src/generate_figures.py
"""
import sys, os
sys.path.insert(0, os.path.dirname(__file__))

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from utils import load_scoring_matrix, DIMENSION_COLS, GBRS_COLORS, FIG_DIR


def bipv_application_heatmap():
    """Heatmap showing BIPV application type support across GBRS.
    Based on expanded CSV analysis of GBRS manuals."""
    import seaborn as sns

    # Data: GBRS × BIPV application type (0=absent, 1=partial, 2=implicit, 3=explicit)
    data = {
        "GBRS":     ["LEED", "BREEAM", "Green Mark", "Green Star", "ASGB", "BEAM Plus", "CASBEE", "DGNB"],
        "Roof PV":  [3, 3, 3, 3, 3, 3, 3, 3],
        "Façade\nBIPV": [1, 1, 2, 1, 1, 1, 1, 3],
        "Window/\nCurtain Wall": [0, 1, 1, 1, 0, 0, 0, 2],
        "Shading\nDevice PV":  [1, 1, 2, 1, 1, 1, 0, 2],
    }
    import pandas as pd
    df = pd.DataFrame(data).set_index("GBRS")

    fig, ax = plt.subplots(figsize=(8, 6))
    cmap = plt.cm.colors.ListedColormap(["#f0f0f0", "#fee8c8", "#fdbb84", "#e34a33"])
    sns.heatmap(df, annot=True, fmt="d", cmap=cmap,
                linewidths=1, linecolor="white",
                vmin=0, vmax=3, ax=ax,
                cbar_kws={"label": "Support Level", "ticks": [0, 1, 2, 3]})
    ax.set_title("BIPV Application Type Recognition in GBRS",
                 fontsize=14, fontweight="bold")
    ax.set_ylabel("")

    # Custom legend
    labels = ["0: Absent", "1: Partial mention", "2: Implicit support", "3: Explicit criteria"]
    colors = ["#f0f0f0", "#fee8c8", "#fdbb84", "#e34a33"]
    patches = [mpatches.Patch(facecolor=c, edgecolor="grey", label=l) for c, l in zip(colors, labels)]
    ax.legend(handles=patches, loc="upper left", bbox_to_anchor=(1.25, 1.0), fontsize=8, title="Score")

    plt.tight_layout()
    fig.savefig(os.path.join(FIG_DIR, "bipv_application_heatmap.png"))
    fig.savefig(os.path.join(FIG_DIR, "bipv_application_heatmap.pdf"))
    plt.close()
    print("  ✓ bipv_application_heatmap.png/pdf")


def gbrs_evolution_timeline():
    """Timeline showing when GBRS updated PV/renewable criteria."""
    import matplotlib.dates as mdates
    from datetime import datetime

    events = [
        ("BREEAM", 1990, "Launched"),
        ("LEED", 1998, "v1.0"),
        ("CASBEE", 2002, "Launched"),
        ("Green Mark", 2005, "Launched"),
        ("Green Star", 2003, "Launched"),
        ("BEAM Plus", 2010, "v1.0"),
        ("DGNB", 2009, "Launched"),
        ("LEED", 2013, "v4 (RE credits expanded)"),
        ("BREEAM", 2014, "UK NC (Ene04 LZC)"),
        ("Green Mark", 2015, "v2015 (PV bonus pts)"),
        ("ASGB", 2019, "GB/T 50378-2019"),
        ("Green Mark", 2021, "GM:2021 (solar mandatory)"),
        ("BREEAM", 2018, "INC 2018"),
        ("LEED", 2021, "v4.1 (RE updated)"),
        ("DGNB", 2023, "NB 2023 (BIPV in facade)"),
        ("BEAM Plus", 2019, "v2.0 (solar study)"),
        ("Green Star", 2020, "v1.3 (net-zero pathway)"),
    ]

    # Sort by year
    events.sort(key=lambda x: x[1])

    fig, ax = plt.subplots(figsize=(14, 6))

    gbrs_list = list(GBRS_COLORS.keys())
    y_map = {g: i for i, g in enumerate(gbrs_list)}

    for gbrs, year, label in events:
        if gbrs not in y_map:
            continue
        y = y_map[gbrs]
        color = GBRS_COLORS[gbrs]
        ax.scatter(year, y, s=80, color=color, zorder=5, edgecolors="white", linewidth=0.5)
        ax.annotate(label, (year, y), textcoords="offset points",
                    xytext=(5, 8), fontsize=7, color=color, rotation=30)

    ax.set_yticks(range(len(gbrs_list)))
    ax.set_yticklabels(gbrs_list, fontsize=10)
    ax.set_xlabel("Year", fontsize=12)
    ax.set_title("Evolution of PV/BIPV Criteria in Green Building Rating Systems",
                 fontsize=14, fontweight="bold")
    ax.set_xlim(1988, 2026)
    ax.grid(axis="x", alpha=0.3)

    # Highlight the "BIPV-aware" era
    ax.axvspan(2018, 2026, alpha=0.08, color="green", label="BIPV-aware era")
    ax.legend(fontsize=9)

    plt.tight_layout()
    fig.savefig(os.path.join(FIG_DIR, "gbrs_evolution_timeline.png"))
    fig.savefig(os.path.join(FIG_DIR, "gbrs_evolution_timeline.pdf"))
    plt.close()
    print("  ✓ gbrs_evolution_timeline.png/pdf")


def credit_weight_comparison():
    """Stacked bar chart: PV credits vs. other energy credits vs. rest."""
    import pandas as pd

    data = {
        "GBRS": ["LEED", "BREEAM", "Green Mark", "Green Star", "ASGB", "BEAM Plus", "CASBEE", "DGNB"],
        "PV/RE specific (%)":    [4.5, 11, 20, 5, 2.5, 8, 3, 10],
        "Other Energy (%)":      [12, 8, 15, 20, 10, 10, 15, 12],
        "Non-Energy (%)":        [83.5, 81, 65, 75, 87.5, 82, 82, 78],
    }
    df = pd.DataFrame(data)

    fig, ax = plt.subplots(figsize=(10, 5))
    x = np.arange(len(df))
    w = 0.5

    ax.bar(x, df["PV/RE specific (%)"], w, label="PV/Renewable specific", color="#F18F01")
    ax.bar(x, df["Other Energy (%)"], w, bottom=df["PV/RE specific (%)"],
           label="Other Energy credits", color="#2E86AB")
    ax.bar(x, df["Non-Energy (%)"], w,
           bottom=df["PV/RE specific (%)"] + df["Other Energy (%)"],
           label="Non-Energy categories", color="#d0d0d0")

    ax.set_xticks(x)
    ax.set_xticklabels(df["GBRS"], fontsize=10)
    ax.set_ylabel("Share of Total Points (%)")
    ax.set_title("Credit Allocation: PV/Renewable Energy Weight in GBRS",
                 fontsize=14, fontweight="bold")
    ax.legend(loc="upper right", fontsize=9)
    ax.set_ylim(0, 105)

    plt.tight_layout()
    fig.savefig(os.path.join(FIG_DIR, "credit_weight_comparison.png"))
    fig.savefig(os.path.join(FIG_DIR, "credit_weight_comparison.pdf"))
    plt.close()
    print("  ✓ credit_weight_comparison.png/pdf")


def main():
    print("=" * 60)
    print("Generating All Figures")
    print("=" * 60)

    # 1. Scoring matrix figures
    print("\n── Scoring Matrix Figures ──")
    from scoring_matrix import (
        radar_chart_all, heatmap_scores, ranking_bar,
        dimension_analysis, sensitivity_analysis, export_latex_table
    )
    df, score_cols = load_scoring_matrix()
    radar_chart_all(df, score_cols)
    heatmap_scores(df, score_cols)
    ranking_bar(df)
    dimension_analysis(df, score_cols)
    sensitivity_analysis(df, score_cols)
    export_latex_table(df, score_cols)

    # 2. Additional figures
    print("\n── Additional Figures ──")
    bipv_application_heatmap()
    gbrs_evolution_timeline()
    credit_weight_comparison()

    # 3. Bibliometric (demo or real data)
    print("\n── Bibliometric Figures ──")
    from bibliometric_analysis import main as biblio_main
    biblio_main()

    print("\n" + "=" * 60)
    print("✅ ALL FIGURES GENERATED")
    print(f"   Location: {FIG_DIR}")
    print("=" * 60)


if __name__ == "__main__":
    main()
