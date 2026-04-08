#!/usr/bin/env python3
"""
mapping_analysis.py — Full BIPV/PV criteria mapping across 21 GBRS × 12 dimensions.

The core analytical framework: for every GBRS, map ALL PV/BIPV-related criteria
across 12 technical dimensions, showing how they exist (score 0-3), where they sit
(category/credit), and what form they take (mandatory/performance/prescriptive).

Generates:
  1. Master heatmap: 21 GBRS × 12 dimensions
  2. Dimension-level analysis: which dimensions are most/least covered
  3. GBRS-level profiles: stacked bar per system
  4. Existence vs absence summary
  5. Requirement type distribution
  6. Cross-tabulation tables for paper
"""
import sys, os
sys.path.insert(0, os.path.dirname(__file__))

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import seaborn as sns

# Paths
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(PROJECT_ROOT, "data")
FIG_DIR = os.path.join(PROJECT_ROOT, "outputs", "figures")
TABLE_DIR = os.path.join(PROJECT_ROOT, "outputs", "tables")
os.makedirs(FIG_DIR, exist_ok=True)
os.makedirs(TABLE_DIR, exist_ok=True)

plt.rcParams.update({
    "font.family": "sans-serif",
    "font.size": 10,
    "figure.dpi": 300,
    "savefig.dpi": 300,
    "savefig.bbox": "tight",
})

# Dimension labels (short and long)
DIM_MAP = {
    "A_Roof_PV":           "A: Roof PV",
    "B_Facade_PV":         "B: Façade PV",
    "C_Window_Curtain_PV": "C: Window/\nCurtain Wall PV",
    "D_Shading_PV":        "D: Shading\nDevice PV",
    "E_Glass_Energy_PV":   "E: Glass-\nIntegrated PV",
    "F_Thermal_Envelope":  "F: Thermal\nEnvelope",
    "G_Daylighting_Visual":"G: Daylighting\n& Visual",
    "H_Materials_LCA":     "H: Materials\n& LCA",
    "I_Carbon_Accounting": "I: Carbon\nAccounting",
    "J_EV_Storage":        "J: EV/Storage\nSynergy",
    "K_Design_Integration":"K: Design\nIntegration",
    "L_Innovation":        "L: Innovation\nPathway",
}

DIMS = list(DIM_MAP.keys())
DIM_LABELS = list(DIM_MAP.values())

# Group dimensions
DIM_GROUPS = {
    "Direct PV/BIPV Application": ["A_Roof_PV", "B_Facade_PV", "C_Window_Curtain_PV", "D_Shading_PV", "E_Glass_Energy_PV"],
    "Building Performance Integration": ["F_Thermal_Envelope", "G_Daylighting_Visual", "H_Materials_LCA", "I_Carbon_Accounting"],
    "System & Process": ["J_EV_Storage", "K_Design_Integration", "L_Innovation"],
}


def load_mapping():
    path = os.path.join(DATA_DIR, "mapping_matrix_full.csv")
    df = pd.read_csv(path, comment="#", skip_blank_lines=True)
    df = df.dropna(subset=["GBRS"])
    # Pivot to matrix form
    matrix = df.pivot_table(index="GBRS", columns="Dim", values="Score", aggfunc="first")
    matrix = matrix.reindex(columns=DIMS)
    return df, matrix


def fig1_master_heatmap(matrix):
    """THE key figure: 21 GBRS × 12 dimensions heatmap."""
    # Custom colormap: white(0) -> light yellow(1) -> orange(2) -> dark red(3)
    cmap = plt.cm.colors.ListedColormap(["#f5f5f5", "#fff3cd", "#fd7e14", "#c0392b"])

    fig, ax = plt.subplots(figsize=(16, 10))
    sns.heatmap(
        matrix, annot=True, fmt=".0f", cmap=cmap,
        linewidths=0.8, linecolor="white",
        vmin=0, vmax=3, ax=ax,
        cbar_kws={"label": "Score", "ticks": [0, 1, 2, 3], "shrink": 0.5},
        xticklabels=[DIM_MAP.get(d, d) for d in matrix.columns],
    )
    ax.set_title("Mapping of PV/BIPV-Related Criteria Across 21 Green Building Rating Systems",
                 fontsize=14, fontweight="bold", pad=15)
    ax.set_ylabel("")
    ax.set_xlabel("")

    # Add group separators
    ax.axvline(x=5, color="black", linewidth=2)   # After E
    ax.axvline(x=9, color="black", linewidth=2)   # After I

    # Group labels at top
    ax.text(2.5, -1.5, "Direct PV/BIPV\nApplication Types", ha="center", fontsize=9, fontweight="bold", color="#c0392b")
    ax.text(7, -1.5, "Building Performance\nIntegration", ha="center", fontsize=9, fontweight="bold", color="#2c3e50")
    ax.text(10.5, -1.5, "System &\nProcess", ha="center", fontsize=9, fontweight="bold", color="#27ae60")

    # Legend
    labels = ["0: Not mentioned", "1: Indirect mention", "2: Explicit mention", "3: Dedicated criteria"]
    colors = ["#f5f5f5", "#fff3cd", "#fd7e14", "#c0392b"]
    patches = [mpatches.Patch(facecolor=c, edgecolor="grey", label=l) for c, l in zip(colors, labels)]
    ax.legend(handles=patches, loc="lower right", fontsize=8, title="Recognition Level", ncol=2)

    plt.tight_layout()
    fig.savefig(os.path.join(FIG_DIR, "mapping_master_heatmap.png"))
    fig.savefig(os.path.join(FIG_DIR, "mapping_master_heatmap.pdf"))
    plt.close()
    print("  ✓ mapping_master_heatmap.png/pdf")


def fig2_dimension_coverage(matrix):
    """Bar chart: what % of GBRS mention each dimension at any level (>=1) vs dedicated (>=3)."""
    n = len(matrix)
    mentioned = (matrix >= 1).sum() / n * 100
    explicit = (matrix >= 2).sum() / n * 100
    dedicated = (matrix >= 3).sum() / n * 100

    fig, ax = plt.subplots(figsize=(14, 6))
    x = np.arange(len(DIMS))
    w = 0.25

    ax.bar(x - w, mentioned, w, label="Any mention (≥1)", color="#fff3cd", edgecolor="#f0ad4e")
    ax.bar(x, explicit, w, label="Explicit mention (≥2)", color="#fd7e14", edgecolor="#e67e22")
    ax.bar(x + w, dedicated, w, label="Dedicated criteria (=3)", color="#c0392b", edgecolor="#922b21")

    ax.set_xticks(x)
    ax.set_xticklabels(DIM_LABELS, fontsize=8)
    ax.set_ylabel("% of 21 GBRS", fontsize=11)
    ax.set_ylim(0, 105)
    ax.set_title("Coverage of PV/BIPV Dimensions Across 21 GBRS", fontsize=14, fontweight="bold")
    ax.legend(fontsize=9)
    ax.grid(axis="y", alpha=0.3)

    # Add group separators
    ax.axvline(x=4.5, color="black", linewidth=1, linestyle="--", alpha=0.5)
    ax.axvline(x=8.5, color="black", linewidth=1, linestyle="--", alpha=0.5)

    plt.tight_layout()
    fig.savefig(os.path.join(FIG_DIR, "mapping_dimension_coverage.png"))
    fig.savefig(os.path.join(FIG_DIR, "mapping_dimension_coverage.pdf"))
    plt.close()
    print("  ✓ mapping_dimension_coverage.png/pdf")


def fig3_gbrs_profiles(matrix):
    """Stacked bar: each GBRS total score breakdown by dimension group."""
    groups = {}
    for gname, dims in DIM_GROUPS.items():
        groups[gname] = matrix[[d for d in dims if d in matrix.columns]].sum(axis=1)

    gdf = pd.DataFrame(groups)
    gdf["Total"] = gdf.sum(axis=1)
    gdf = gdf.sort_values("Total", ascending=True)

    fig, ax = plt.subplots(figsize=(12, 8))
    colors = ["#c0392b", "#2c3e50", "#27ae60"]
    bottom = np.zeros(len(gdf))

    for i, (gname, color) in enumerate(zip(DIM_GROUPS.keys(), colors)):
        vals = gdf[gname].values
        ax.barh(range(len(gdf)), vals, left=bottom, color=color, edgecolor="white", label=gname, height=0.6)
        bottom += vals

    ax.set_yticks(range(len(gdf)))
    ax.set_yticklabels(gdf.index, fontsize=10)
    ax.set_xlabel("Total Mapping Score", fontsize=11)
    ax.set_title("GBRS Profiles: PV/BIPV Criteria Coverage by Dimension Group",
                 fontsize=14, fontweight="bold")
    ax.legend(loc="lower right", fontsize=9)

    # Add total labels
    for i, total in enumerate(gdf["Total"].values):
        ax.text(total + 0.3, i, f"{total:.0f}", va="center", fontsize=9, fontweight="bold")

    max_possible = sum(len(dims) * 3 for dims in DIM_GROUPS.values())
    ax.axvline(x=max_possible, color="grey", linestyle="--", alpha=0.4, label=f"Max ({max_possible})")

    plt.tight_layout()
    fig.savefig(os.path.join(FIG_DIR, "mapping_gbrs_profiles.png"))
    fig.savefig(os.path.join(FIG_DIR, "mapping_gbrs_profiles.pdf"))
    plt.close()
    print("  ✓ mapping_gbrs_profiles.png/pdf")


def fig4_bipv_application_detail(matrix):
    """Focused heatmap: just the 5 direct BIPV application dimensions."""
    app_dims = ["A_Roof_PV", "B_Facade_PV", "C_Window_Curtain_PV", "D_Shading_PV", "E_Glass_Energy_PV"]
    app_labels = ["Roof PV", "Façade PV", "Window/Curtain\nWall PV", "Shading\nDevice PV", "Glass-Integrated\nPV"]

    sub = matrix[app_dims].copy()
    sub.columns = app_labels

    cmap = plt.cm.colors.ListedColormap(["#f5f5f5", "#fff3cd", "#fd7e14", "#c0392b"])

    fig, ax = plt.subplots(figsize=(10, 10))
    sns.heatmap(sub, annot=True, fmt=".0f", cmap=cmap,
                linewidths=1, linecolor="white",
                vmin=0, vmax=3, ax=ax,
                cbar_kws={"label": "Score", "ticks": [0, 1, 2, 3]})
    ax.set_title("BIPV Application Type Recognition Across 21 GBRS",
                 fontsize=14, fontweight="bold")
    ax.set_ylabel("")

    plt.tight_layout()
    fig.savefig(os.path.join(FIG_DIR, "mapping_bipv_applications.png"))
    fig.savefig(os.path.join(FIG_DIR, "mapping_bipv_applications.pdf"))
    plt.close()
    print("  ✓ mapping_bipv_applications.png/pdf")


def fig5_gap_analysis(matrix):
    """Bubble chart showing the gap: what's covered vs what's missing."""
    # Calculate coverage stats
    stats = []
    for dim in DIMS:
        total = len(matrix)
        score_0 = (matrix[dim] == 0).sum()
        score_1 = (matrix[dim] == 1).sum()
        score_2 = (matrix[dim] == 2).sum()
        score_3 = (matrix[dim] == 3).sum()
        avg = matrix[dim].mean()
        stats.append({
            "Dimension": DIM_MAP[dim],
            "Not mentioned (0)": score_0,
            "Indirect (1)": score_1,
            "Explicit (2)": score_2,
            "Dedicated (3)": score_3,
            "Average Score": avg,
            "% Not mentioned": score_0 / total * 100,
        })
    sdf = pd.DataFrame(stats)

    fig, ax = plt.subplots(figsize=(14, 7))
    colors = ["#f5f5f5", "#fff3cd", "#fd7e14", "#c0392b"]
    labels_legend = ["Not mentioned (0)", "Indirect (1)", "Explicit (2)", "Dedicated (3)"]

    x = np.arange(len(sdf))
    bottom = np.zeros(len(sdf))

    for col, color, label in zip(labels_legend, colors, labels_legend):
        vals = sdf[col].values
        ax.bar(x, vals, bottom=bottom, color=color, edgecolor="white", label=label, width=0.7)
        bottom += vals

    ax.set_xticks(x)
    ax.set_xticklabels(sdf["Dimension"], fontsize=8, rotation=30, ha="right")
    ax.set_ylabel("Number of GBRS (out of 21)", fontsize=11)
    ax.set_title("Gap Analysis: How 21 GBRS Address Each PV/BIPV Dimension",
                 fontsize=14, fontweight="bold")
    ax.legend(fontsize=9, ncol=4, loc="upper center", bbox_to_anchor=(0.5, -0.15))
    ax.set_ylim(0, 22)
    ax.axhline(y=21, color="grey", linestyle="--", alpha=0.3)

    plt.tight_layout()
    fig.savefig(os.path.join(FIG_DIR, "mapping_gap_analysis.png"))
    fig.savefig(os.path.join(FIG_DIR, "mapping_gap_analysis.pdf"))
    plt.close()
    print("  ✓ mapping_gap_analysis.png/pdf")


def export_tables(df, matrix):
    """Export key tables for the paper."""
    # Table 1: Master mapping matrix (for paper)
    matrix.to_csv(os.path.join(TABLE_DIR, "mapping_matrix_pivot.csv"))

    # Table 2: Summary statistics
    stats = pd.DataFrame({
        "Dimension": [DIM_MAP[d] for d in DIMS],
        "Mean Score": matrix[DIMS].mean().values.round(2),
        "Std Dev": matrix[DIMS].std().values.round(2),
        "% Not Mentioned (=0)": ((matrix[DIMS] == 0).sum() / len(matrix) * 100).values.round(1),
        "% Dedicated (=3)": ((matrix[DIMS] == 3).sum() / len(matrix) * 100).values.round(1),
        "Max System": [matrix[d].idxmax() for d in DIMS],
    })
    stats.to_csv(os.path.join(TABLE_DIR, "mapping_dimension_stats.csv"), index=False)

    # Table 3: GBRS total scores
    totals = matrix[DIMS].sum(axis=1).sort_values(ascending=False)
    totals_df = pd.DataFrame({
        "GBRS": totals.index,
        "Total Score": totals.values,
        "Max Possible": 36,
        "Percentage": (totals.values / 36 * 100).round(1),
    })
    totals_df.to_csv(os.path.join(TABLE_DIR, "mapping_gbrs_totals.csv"), index=False)

    # LaTeX versions
    matrix_latex = matrix[DIMS].to_latex(
        caption="Mapping of PV/BIPV-related criteria across 21 GBRS (0=not mentioned, 1=indirect, 2=explicit, 3=dedicated criteria).",
        label="tab:mapping_matrix"
    )
    with open(os.path.join(TABLE_DIR, "mapping_matrix.tex"), "w") as f:
        f.write(matrix_latex)

    print("  ✓ mapping_matrix_pivot.csv")
    print("  ✓ mapping_dimension_stats.csv")
    print("  ✓ mapping_gbrs_totals.csv")
    print("  ✓ mapping_matrix.tex")


def main():
    print("=" * 60)
    print("BIPV/PV Mapping Analysis: 21 GBRS × 12 Dimensions")
    print("=" * 60)

    df, matrix = load_mapping()
    print(f"\nLoaded {len(matrix)} GBRS × {len(DIMS)} dimensions")
    print(f"Total data points: {len(matrix) * len(DIMS)}")

    # Quick summary
    print("\n── Coverage Summary ──")
    for dim in DIMS:
        n_mentioned = (matrix[dim] >= 1).sum()
        n_dedicated = (matrix[dim] == 3).sum()
        print(f"  {DIM_MAP[dim]:<25s}: {n_mentioned:2d}/21 mentioned, {n_dedicated:2d}/21 dedicated")

    print("\n── Generating Figures ──")
    fig1_master_heatmap(matrix)
    fig2_dimension_coverage(matrix)
    fig3_gbrs_profiles(matrix)
    fig4_bipv_application_detail(matrix)
    fig5_gap_analysis(matrix)

    print("\n── Exporting Tables ──")
    export_tables(df, matrix)

    print("\n✅ Mapping analysis complete.")


if __name__ == "__main__":
    main()
