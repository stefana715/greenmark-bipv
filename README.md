# BIPV × Green Building Rating Systems: Meta-Review

**Paper Title:** "Building-Integrated Photovoltaics in Green Building Rating Systems: A meta-review and content-based criteria assessment"

**Target Journal:** Renewable and Sustainable Energy Reviews (RSER)

---

## Project Structure

```
bipv-gbrs-review/
├── README.md
├── requirements.txt
├── src/
│   ├── bibliometric_analysis.py    # Scopus/WOS data processing
│   ├── scoring_matrix.py           # Content-based scoring & visualization
│   ├── generate_figures.py         # All publication-quality figures
│   └── utils.py                    # Shared utilities
├── data/
│   ├── raw/                        # Scopus/WOS exports (.csv, .bib)
│   ├── processed/                  # Cleaned datasets
│   ├── manuals/                    # GBRS manual extraction notes
│   └── scoring_matrix.csv          # The core scoring data
├── outputs/
│   ├── figures/                    # Generated figures (PNG, SVG, PDF)
│   └── tables/                     # Generated tables (CSV, LaTeX)
├── templates/
│   └── gbrs_extraction_template.csv
├── docs/
│   ├── framework_v2.md             # Paper framework document
│   └── search_strategy.md          # PRISMA search protocol
└── paper/                          # Manuscript drafts (added later)
```

## Quick Start (in Claude Code terminal)

```bash
# 1. Clone and setup
git clone https://github.com/YOUR_USERNAME/bipv-gbrs-review.git
cd bipv-gbrs-review
pip install -r requirements.txt

# 2. Run scoring matrix visualization (after filling scoring_matrix.csv)
python src/scoring_matrix.py

# 3. Run bibliometric analysis (after placing Scopus export in data/raw/)
python src/bibliometric_analysis.py

# 4. Generate all figures
python src/generate_figures.py
```

## Workflow

1. **Scopus/WOS Search** → export to `data/raw/`
2. **Run `bibliometric_analysis.py`** → publication trends, keyword analysis
3. **Read GBRS manuals** → fill `data/scoring_matrix.csv` using rubric
4. **Run `scoring_matrix.py`** → radar charts, heatmaps, rankings
5. **Run `generate_figures.py`** → all publication-quality figures
6. **Write paper** → use outputs in manuscript

## GBRS Systems Analyzed

| # | System | Country | Version | Manual Available |
|---|--------|---------|---------|-----------------|
| 1 | LEED | USA | v4.1 BD+C | Public |
| 2 | BREEAM | UK | NC 2018 | Public |
| 3 | Green Mark | Singapore | GM:2021 | Public |
| 4 | Green Star | Australia | v1.3 | Public |
| 5 | ASGB (3-Star) | China | 2019 | Partial |
| 6 | BEAM Plus | Hong Kong | v2.0 | Public |
| 7 | CASBEE | Japan | 2021 | Partial |
| 8 | DGNB | Germany | 2023 | Public |
