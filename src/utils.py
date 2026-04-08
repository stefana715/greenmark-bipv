"""
Shared utilities for BIPV-GBRS meta-review project.
"""
import os
import pandas as pd
import numpy as np

# ── Paths ──────────────────────────────────────────────
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(PROJECT_ROOT, "data")
RAW_DIR = os.path.join(DATA_DIR, "raw")
PROCESSED_DIR = os.path.join(DATA_DIR, "processed")
OUTPUT_DIR = os.path.join(PROJECT_ROOT, "outputs")
FIG_DIR = os.path.join(OUTPUT_DIR, "figures")
TABLE_DIR = os.path.join(OUTPUT_DIR, "tables")
DOCS_DIR = os.path.join(PROJECT_ROOT, "docs")

for d in [RAW_DIR, PROCESSED_DIR, FIG_DIR, TABLE_DIR, DOCS_DIR]:
    os.makedirs(d, exist_ok=True)

# ── Scoring rubric ─────────────────────────────────────
DIMENSIONS = {
    "D1_Credit_Weight":         "Credit Weight\n(% of total pts for PV/RE)",
    "D2_BIPV_Specificity":      "BIPV Specificity\n(explicit recognition)",
    "D3_Application_Coverage":  "Application Coverage\n(roof/façade/window/shading)",
    "D4_Design_Integration":    "Design Integration\n(feasibility studies)",
    "D5_Ambition_Level":        "Ambition Level\n(RE target / net-zero)",
    "D6_Performance_Verification": "Performance Verification\n(post-occupancy M&V)",
    "D7_Synergy_Envelope":      "Synergy with Envelope\n(multi-category credit)",
    "D8_Innovation_Pathway":    "Innovation Pathway\n(bonus for novel BIPV)",
}

DIMENSION_COLS = list(DIMENSIONS.keys())
DIMENSION_LABELS = list(DIMENSIONS.values())

# ── Color palette (colorblind-friendly) ────────────────
GBRS_COLORS = {
    "LEED":       "#2E86AB",
    "BREEAM":     "#A23B72",
    "Green Mark": "#F18F01",
    "Green Star": "#C73E1D",
    "ASGB":       "#3B1F2B",
    "BEAM Plus":  "#44BBA4",
    "CASBEE":     "#E94F37",
    "DGNB":       "#393E41",
}

def load_scoring_matrix(path=None):
    """Load and validate the scoring matrix CSV."""
    if path is None:
        path = os.path.join(DATA_DIR, "scoring_matrix.csv")
    df = pd.read_csv(path)
    # Extract score columns
    score_cols = [c for c in df.columns if c.startswith("D") and "_Justification" not in c and c in DIMENSION_COLS]
    df["Total_Score"] = df[score_cols].sum(axis=1)
    df["Max_Possible"] = len(score_cols) * 3
    df["Percentage"] = (df["Total_Score"] / df["Max_Possible"] * 100).round(1)
    return df, score_cols
