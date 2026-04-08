#!/usr/bin/env python3
"""
bibliometric_analysis.py — Process Scopus/WOS exports for BIPV × GBRS review.

Expected input: Scopus CSV export in data/raw/scopus_export.csv
                (with columns: Authors, Title, Year, Source title, Abstract, Author Keywords, etc.)

Generates:
  1. Publication trend by year
  2. Top journals bar chart
  3. Top countries bar chart
  4. Keyword frequency analysis
  5. Processed data for VOSviewer

Usage:
  python src/bibliometric_analysis.py
"""
import sys, os
sys.path.insert(0, os.path.dirname(__file__))

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from collections import Counter
from utils import RAW_DIR, PROCESSED_DIR, FIG_DIR

plt.rcParams.update({
    "font.family": "sans-serif",
    "font.size": 11,
    "figure.dpi": 300,
    "savefig.dpi": 300,
    "savefig.bbox": "tight",
})


def load_scopus_data():
    """Load Scopus CSV export. Try common filenames."""
    candidates = ["scopus_export.csv", "scopus.csv", "scopus_results.csv"]
    for fname in candidates:
        path = os.path.join(RAW_DIR, fname)
        if os.path.exists(path):
            df = pd.read_csv(path)
            print(f"Loaded {len(df)} records from {fname}")
            return df

    # If no file found, create a demo dataset
    print("⚠ No Scopus export found in data/raw/. Creating demo dataset.")
    print("  To use real data, export from Scopus as CSV and place in data/raw/scopus_export.csv")
    return create_demo_data()


def create_demo_data():
    """Create placeholder data for testing the pipeline."""
    np.random.seed(42)
    years = np.random.choice(range(2010, 2026), size=120, p=_year_weights())
    journals = np.random.choice(
        ["Energy and Buildings", "Building and Environment", "Renewable and Sustainable Energy Reviews",
         "Solar Energy", "Applied Energy", "Journal of Cleaner Production",
         "Buildings", "Sustainability", "Energies", "Solar Energy Materials and Solar Cells"],
        size=120
    )
    countries = np.random.choice(
        ["China", "USA", "Singapore", "UK", "Germany", "Australia", "Italy",
         "South Korea", "India", "Japan", "Hong Kong", "Netherlands"],
        size=120, p=[0.22, 0.15, 0.10, 0.10, 0.08, 0.07, 0.06, 0.05, 0.05, 0.04, 0.04, 0.04]
    )
    keywords_pool = [
        "BIPV", "building integrated photovoltaics", "green building", "rating system",
        "LEED", "BREEAM", "energy efficiency", "net zero energy building",
        "facade photovoltaic", "renewable energy", "solar energy", "PV integration",
        "building envelope", "daylighting", "semi-transparent PV", "carbon emissions",
        "Green Mark", "sustainable building", "life cycle assessment", "urban solar potential"
    ]
    keywords = ["; ".join(np.random.choice(keywords_pool, size=np.random.randint(3, 7), replace=False))
                for _ in range(120)]

    df = pd.DataFrame({
        "Year": years,
        "Source title": journals,
        "Affiliations": countries,
        "Author Keywords": keywords,
        "Title": [f"Study {i}" for i in range(120)],
        "Authors": [f"Author{i}A; Author{i}B" for i in range(120)],
    })
    return df


def _year_weights():
    """Approximate realistic publication growth curve."""
    w = np.array([1, 1, 2, 3, 4, 5, 7, 9, 11, 13, 15, 17, 18, 19, 20, 15])
    return w / w.sum()


def publication_trend(df):
    """Bar chart of publications per year."""
    counts = df["Year"].value_counts().sort_index()

    fig, ax = plt.subplots(figsize=(10, 5))
    ax.bar(counts.index, counts.values, color="#2E86AB", edgecolor="white", width=0.7)
    ax.set_xlabel("Year", fontsize=12)
    ax.set_ylabel("Number of Publications", fontsize=12)
    ax.set_title("Publication Trend: BIPV × Green Building Rating Systems Research",
                 fontsize=14, fontweight="bold")
    ax.grid(axis="y", alpha=0.3)

    # Add trend line
    z = np.polyfit(counts.index, counts.values, 2)
    p = np.poly1d(z)
    x_smooth = np.linspace(counts.index.min(), counts.index.max(), 100)
    ax.plot(x_smooth, p(x_smooth), "--", color="#E94F37", linewidth=2, alpha=0.7, label="Trend")
    ax.legend()

    plt.tight_layout()
    fig.savefig(os.path.join(FIG_DIR, "publication_trend.png"))
    fig.savefig(os.path.join(FIG_DIR, "publication_trend.pdf"))
    plt.close()
    print("  ✓ publication_trend.png/pdf")


def top_journals(df, n=10):
    """Top journals bar chart."""
    counts = df["Source title"].value_counts().head(n)

    fig, ax = plt.subplots(figsize=(10, 5))
    ax.barh(range(len(counts)), counts.values, color="#A23B72", edgecolor="white")
    ax.set_yticks(range(len(counts)))
    ax.set_yticklabels(counts.index, fontsize=9)
    ax.invert_yaxis()
    ax.set_xlabel("Number of Publications")
    ax.set_title(f"Top {n} Journals Publishing BIPV × GBRS Research",
                 fontsize=14, fontweight="bold")
    ax.grid(axis="x", alpha=0.3)

    plt.tight_layout()
    fig.savefig(os.path.join(FIG_DIR, "top_journals.png"))
    fig.savefig(os.path.join(FIG_DIR, "top_journals.pdf"))
    plt.close()
    print("  ✓ top_journals.png/pdf")


def top_countries(df, n=12):
    """Top contributing countries."""
    if "Affiliations" in df.columns:
        # Each affiliation entry ends with the country (last comma-separated token)
        def extract_countries(aff_str):
            if pd.isna(aff_str):
                return []
            result = []
            for entry in aff_str.split(";"):
                entry = entry.strip()
                if entry:
                    country = entry.split(",")[-1].strip()
                    if country:
                        result.append(country)
            return result

        all_countries = []
        for aff in df["Affiliations"]:
            all_countries.extend(extract_countries(aff))
        # Count unique countries per paper (use first affiliation per paper for paper-level count)
        paper_countries = df["Affiliations"].dropna().apply(
            lambda x: extract_countries(x)[0] if extract_countries(x) else "Unknown"
        )
        countries = paper_countries
    else:
        countries = pd.Series(["Unknown"] * len(df))

    counts = countries.value_counts().head(n)

    fig, ax = plt.subplots(figsize=(10, 5))
    ax.barh(range(len(counts)), counts.values, color="#F18F01", edgecolor="white")
    ax.set_yticks(range(len(counts)))
    ax.set_yticklabels(counts.index, fontsize=10)
    ax.invert_yaxis()
    ax.set_xlabel("Number of Publications")
    ax.set_title(f"Top {n} Contributing Countries/Regions",
                 fontsize=14, fontweight="bold")
    ax.grid(axis="x", alpha=0.3)

    # Add percentage
    total = counts.sum()
    for i, v in enumerate(counts.values):
        ax.text(v + 0.3, i, f"{v/total*100:.0f}%", va="center", fontsize=9)

    plt.tight_layout()
    fig.savefig(os.path.join(FIG_DIR, "top_countries.png"))
    fig.savefig(os.path.join(FIG_DIR, "top_countries.pdf"))
    plt.close()
    print("  ✓ top_countries.png/pdf")


def keyword_analysis(df, n=25):
    """Keyword frequency bar chart + export for VOSviewer."""
    kw_col = "Author Keywords" if "Author Keywords" in df.columns else "Index Keywords"
    if kw_col not in df.columns:
        print("  ⚠ No keyword column found. Skipping keyword analysis.")
        return

    all_kw = []
    for kwstr in df[kw_col].dropna():
        for kw in kwstr.split(";"):
            kw = kw.strip().lower()
            if len(kw) > 2:
                all_kw.append(kw)

    counts = Counter(all_kw)
    top = counts.most_common(n)
    labels, values = zip(*top)

    fig, ax = plt.subplots(figsize=(10, 7))
    ax.barh(range(len(labels)), values, color="#44BBA4", edgecolor="white")
    ax.set_yticks(range(len(labels)))
    ax.set_yticklabels(labels, fontsize=9)
    ax.invert_yaxis()
    ax.set_xlabel("Frequency")
    ax.set_title(f"Top {n} Author Keywords", fontsize=14, fontweight="bold")
    ax.grid(axis="x", alpha=0.3)

    plt.tight_layout()
    fig.savefig(os.path.join(FIG_DIR, "keyword_frequency.png"))
    fig.savefig(os.path.join(FIG_DIR, "keyword_frequency.pdf"))
    plt.close()
    print("  ✓ keyword_frequency.png/pdf")

    # Export keyword pairs for VOSviewer
    kw_df = pd.DataFrame(top, columns=["Keyword", "Frequency"])
    kw_df.to_csv(os.path.join(PROCESSED_DIR, "keyword_frequencies.csv"), index=False)
    print("  ✓ keyword_frequencies.csv (for VOSviewer)")


# ── Main ───────────────────────────────────────────────
def main():
    print("=" * 60)
    print("Bibliometric Analysis: BIPV × GBRS")
    print("=" * 60)

    df = load_scopus_data()
    print(f"\nDataset: {len(df)} records, years {df['Year'].min()}–{df['Year'].max()}")

    print("\n── Generating Figures ──")
    publication_trend(df)
    top_journals(df)
    top_countries(df)
    keyword_analysis(df)

    # Save processed data
    df.to_csv(os.path.join(PROCESSED_DIR, "processed_records.csv"), index=False)
    print(f"\n  ✓ processed_records.csv")
    print("\n✅ Bibliometric analysis complete.")


if __name__ == "__main__":
    main()
