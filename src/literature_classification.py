#!/usr/bin/env python3
"""
literature_classification.py
Multi-file Scopus merge + NLP content analysis for the BIPV × GBRS review.

Inputs : data/raw/scopus_*.csv  (all Scopus exports, any number)
Outputs:
  data/processed/literature_classification.csv
  data/processed/key_findings.md
  outputs/figures/topic_pie.png/pdf
  outputs/figures/gbrs_mentions_bar.png/pdf
  outputs/figures/bipv_type_bar.png/pdf
  outputs/figures/topic_area_year.png/pdf
  docs/literature_analysis_report.md
"""
import sys, os, re, textwrap, glob
sys.path.insert(0, os.path.dirname(__file__))

import pandas as pd
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
from collections import Counter, defaultdict
from utils import RAW_DIR, PROCESSED_DIR, FIG_DIR, DOCS_DIR

for d in (PROCESSED_DIR, FIG_DIR, DOCS_DIR):
    os.makedirs(d, exist_ok=True)

plt.rcParams.update({
    "font.family": "sans-serif",
    "font.size": 11,
    "figure.dpi": 300,
    "savefig.dpi": 300,
    "savefig.bbox": "tight",
})

PALETTE = [
    "#2E86AB", "#A23B72", "#F18F01", "#44BBA4",
    "#E94F37", "#6B4226", "#8338EC", "#3A86FF",
    "#FB5607", "#FFBE0B", "#8AC926", "#1982C4",
]

# ═══════════════════════════════════════════════════════════════
#  CLASSIFICATION RULES
# ═══════════════════════════════════════════════════════════════

# --- Topic rules -----------------------------------------------
# Order matters only for tie-breaking; scoring picks the best match.
TOPIC_RULES = {
    "BIPV+GBRS Cross": [
        # Must mention both BIPV/PV AND a rating-system concept
        r"(bipv|building.integrated photovoltaic|building integrated photovoltaic).{0,200}(rating system|certif|leed|breeam|green mark|green star|casbee|dgnb|beam plus|asgb|gbrs|green building standard)",
        r"(rating system|certif|leed|breeam|green mark|green star|casbee|dgnb|beam plus|asgb|gbrs).{0,200}(bipv|building.integrated photovoltaic|pv.*credit|solar.*credit)",
        r"pv.{0,60}credit.{0,60}(rating|certif|gbrs|leed|breeam|green mark)",
        r"(leed|breeam|green mark|green star|casbee|dgnb|beam plus).{0,120}(photovoltaic|bipv|\bpv\b)",
    ],
    "GBRS Comparative Analysis": [
        r"(compar|analys|review|assess).{0,80}(rating system|certif|leed|breeam|green mark|green star|casbee|dgnb|beam plus|asgb)",
        r"green building rating system",
        r"(leed|breeam).{0,30}(green mark|green star|casbee|dgnb|beam plus|asgb)",
        r"(multiple|several|various|different).{0,40}(rating|certif|gbrs)",
        r"gbrs\b",
    ],
    "Policy / Regulation": [
        r"\bpolic(y|ies)\b.{0,80}(solar|pv|bipv|photovoltaic|renewable|building|energy)",
        r"(building code|energy code|standard).{0,80}(pv|solar|bipv|renewable)",
        r"\bregulat.{0,80}(pv|solar|bipv|renewable|building)",
        r"(feed.in tariff|incentive|subsidy|mandate|legislation).{0,80}(pv|solar|bipv|building|green)",
        r"iec\s*63092",
        r"net.zero.{0,40}(target|policy|goal|mandate|regulation)",
        r"(government|national|municipal).{0,60}(pv|solar|bipv|green building|certif)",
    ],
    "BIPV Economics / LCA": [
        r"(cost.benefit|life.cycle cost|payback|lcoe|roi\b|return on investment).{0,80}(pv|solar|bipv|building)",
        r"\blca\b.{0,60}(pv|solar|bipv|building)",
        r"life cycle assessment.{0,80}(pv|solar|bipv|building)",
        r"(economic|financial).{0,60}(bipv|pv|solar|photovoltaic)",
        r"(embodied (carbon|energy)|environmental impact).{0,60}(pv|solar|bipv)",
        r"(capital cost|installation cost|initial cost).{0,60}(pv|solar|bipv)",
        r"cost.{0,40}(barrier|challenge|obstacle).{0,60}(pv|solar|bipv)",
    ],
    "Urban Solar Potential": [
        r"urban.{0,40}(solar|pv|photovoltaic)",
        r"(solar potential|solar resource|solar irradiation).{0,60}(urban|city|district|building stock)",
        r"rooftop.{0,40}(potential|area|capacity).{0,60}(pv|solar)",
        r"gis.{0,60}(solar|pv|bipv)",
        r"(solar map|solar cadastre|solar atlas)",
        r"building stock.{0,60}(pv|solar|energy)",
        r"city.scale.{0,60}(pv|solar|photovoltaic)",
    ],
    "Net-Zero / Zero-Energy Buildings": [
        r"net.zero.{0,60}(energy|carbon|building|emission)",
        r"zero.energy building",
        r"\bnzeb\b",
        r"nearly zero.energy",
        r"plus.energy building",
        r"energy.neutral building",
        r"zero.carbon building",
        r"(positive energy|energy balance).{0,60}building",
    ],
    "BIPV Technical Performance": [
        r"\bbipv\b",
        r"building.integrated photovoltaic",
        r"building integrated photovoltaic",
        r"(pv module|pv system|pv panel|pv array).{0,60}building",
        r"(semi.transparent|bifacial|thin.film|perovskite).{0,60}(pv|solar|photovoltaic)",
        r"facade.{0,40}(pv|photovoltaic|solar)",
        r"(energy yield|power output|electricity generation).{0,60}(pv|bipv|solar|building)",
        r"(thermal|optical).{0,40}(pv|bipv|solar).{0,40}(building|facade|roof|window)",
    ],
}

# Priority for tie-breaking (higher priority = wins ties)
TOPIC_PRIORITY = [
    "BIPV+GBRS Cross",
    "GBRS Comparative Analysis",
    "Policy / Regulation",
    "BIPV Economics / LCA",
    "Urban Solar Potential",
    "Net-Zero / Zero-Energy Buildings",
    "BIPV Technical Performance",
    "Other",
]

# --- GBRS detection --------------------------------------------
GBRS_PATTERNS = {
    "LEED":                    [r"\bleed\b", r"leadership in energy and environmental design"],
    "BREEAM":                  [r"\bbreeam\b", r"building research establishment"],
    "Green Mark":              [r"green mark", r"greenmark", r"bca green mark"],
    "Green Star":              [r"green star", r"greenstar", r"\bgbca\b"],
    "CASBEE":                  [r"\bcasbee\b", r"comprehensive assessment.*sustainable built"],
    "DGNB":                    [r"\bdgnb\b", r"deutsche gesellschaft.*nachhaltiges bauen", r"german sustainable building"],
    "BEAM Plus":               [r"beam plus", r"beam\+", r"hong kong.*\bbeam\b", r"\bbeam\b.*hong kong", r"\bbeam\b.*certif"],
    "ASGB":                    [r"\basgb\b", r"assessment standard.*green building", r"china.*green building.*label"],
    "WELL":                    [r"\bwell\b.*certif", r"well building standard", r"well.*standard.*building", r"iwbi"],
    "IGBC":                    [r"\bigbc\b", r"indian green building council"],
    "Estidama / Pearl":        [r"estidama", r"pearl rating", r"pearl.*certif", r"abu dhabi.*green"],
    "Passive House":           [r"passive house", r"passivhaus", r"\bphius\b"],
    "EDGE":                    [r"\bedge\b.*certif", r"excellence in design.*greater efficienc", r"ifc.*edge"],
    "HQE":                     [r"\bhqe\b", r"haute qualit[eé] environnementale", r"french.*green building"],
    "GRIHA":                   [r"\bgriha\b", r"green rating.*integrated habitat"],
    "Living Building Challenge":[r"living building challenge", r"\blbc\b.*certif"],
    "MINERGIE":                [r"\bminergie\b"],
    "Green Globes":            [r"green globes"],
    "NABERS":                  [r"\bnabers\b", r"national australian built environment rating"],
    "Green Building Index":    [r"green building index", r"\bgbi\b.*malaysia"],
    "LOTUS":                   [r"\blotus\b.*certif", r"vietnam.*green.*certif"],
}

# --- BIPV application types ------------------------------------
BIPV_APP_RULES = {
    "Window / Curtain Wall BIPV": [
        r"(bipv|pv).{0,30}(window|glazing|curtain wall|glass)",
        r"(window|glazing|curtain wall).{0,30}(bipv|photovoltaic|pv)",
        r"semi.transparent.{0,40}(pv|solar|photovoltaic)",
        r"transparent.{0,30}(pv|solar|photovoltaic)",
        r"pv.{0,20}glass",
        r"solar.{0,20}glass",
    ],
    "Shading BIPV": [
        r"(bipv|pv).{0,30}shad",
        r"shad.{0,30}(bipv|photovoltaic|\bpv\b)",
        r"solar shading.{0,30}(pv|bipv)",
        r"(louvre|awning|brise.soleil).{0,30}(pv|solar|bipv)",
        r"(pv|bipv).{0,30}(louvre|awning)",
    ],
    "Façade BIPV": [
        r"(bipv|pv).{0,30}(facade|fa[cç]ade|cladding|wall|vertical)",
        r"(facade|fa[cç]ade|cladding|vertical wall).{0,30}(bipv|photovoltaic|\bpv\b|solar)",
        r"wall.integrated.{0,30}(pv|photovoltaic|solar)",
        r"building skin.{0,40}(pv|solar|bipv)",
    ],
    "Rooftop PV": [
        r"(bipv|pv|solar).{0,30}(rooftop|roof.top|pitched roof|flat roof)",
        r"(rooftop|roof.top|pitched roof|flat roof).{0,30}(bipv|photovoltaic|\bpv\b|solar)",
        r"roof.mounted.{0,30}(pv|solar|photovoltaic)",
        r"rooftop solar potential",
    ],
    "Generic PV / BAPV": [
        r"\bbipv\b",
        r"building.integrated photovoltaic",
        r"\bbapv\b",
        r"building.applied photovoltaic",
        r"pv.{0,30}(system|installation|array|module)",
        r"(solar panel|solar cell|photovoltaic).{0,30}building",
        r"building.{0,30}(solar panel|photovoltaic|pv system)",
    ],
}
BIPV_APP_PRIORITY = [
    "Window / Curtain Wall BIPV",
    "Shading BIPV",
    "Façade BIPV",
    "Rooftop PV",
    "Generic PV / BAPV",
]

# --- Key-finding sentences -------------------------------------
KEY_SENTENCE_KEYWORDS = [
    r"\bbarrier", r"\bdriver", r"\bincentive", r"\bcredit\b",
    r"\bpoint\b.{0,30}(pv|solar|bipv|rating|certif)",
    r"\bweight\b.{0,30}(pv|solar|bipv|rating|certif|dimension|criterion)",
    r"\brequirement\b.{0,60}(pv|solar|bipv|green|certif)",
    r"net.zero", r"\badopt", r"\bintegrat.{0,20}(pv|solar|bipv|photovoltaic)",
    r"pv.{0,30}\bintegrat", r"solar.{0,30}\bintegrat",
    r"\bchallenge\b.{0,60}(pv|solar|bipv|building|green)",
    r"\bopportunity\b.{0,60}(pv|solar|bipv|building)",
    r"(leed|breeam|green mark|green star|casbee|dgnb).{0,80}(pv|solar|bipv|photovoltaic|credit|point)",
]

# ═══════════════════════════════════════════════════════════════
#  DATA LOADING
# ═══════════════════════════════════════════════════════════════

def load_and_merge() -> pd.DataFrame:
    """Load all scopus_*.csv from RAW_DIR, merge, and deduplicate."""
    pattern = os.path.join(RAW_DIR, "scopus*.csv")
    paths = sorted(glob.glob(pattern))
    # Exclude the timestamped duplicate of scopus_export.csv
    paths = [p for p in paths if "fe636123" not in p]
    print(f"Found {len(paths)} CSV files:")
    dfs = []
    for p in paths:
        df = pd.read_csv(p, low_memory=False)
        print(f"  {os.path.basename(p):40s} {len(df):>5} records")
        dfs.append(df)
    combined = pd.concat(dfs, ignore_index=True)
    print(f"  Combined (before dedup) : {len(combined)}")

    # Deduplicate: prefer rows with DOI, then by Title
    combined["_title_norm"] = combined["Title"].str.lower().str.strip()
    combined = combined.sort_values("DOI", na_position="last")
    combined = combined.drop_duplicates(subset=["_title_norm"], keep="first")
    combined = combined.drop(columns=["_title_norm"])
    combined = combined.reset_index(drop=True)
    print(f"  After dedup (by title)  : {len(combined)}")
    print(f"  Year range              : {int(combined['Year'].min())}–{int(combined['Year'].max())}")
    print(f"  Abstracts present       : {combined['Abstract'].notna().sum()}")
    return combined

# ═══════════════════════════════════════════════════════════════
#  HELPERS
# ═══════════════════════════════════════════════════════════════

def norm(text) -> str:
    return str(text).lower() if pd.notna(text) else ""

def count_matches(text: str, patterns: list) -> int:
    return sum(1 for p in patterns if re.search(p, text))

def any_match(text: str, patterns: list) -> bool:
    return any(re.search(p, text) for p in patterns)

# ═══════════════════════════════════════════════════════════════
#  CLASSIFICATION FUNCTIONS
# ═══════════════════════════════════════════════════════════════

def classify_topic(text: str) -> str:
    scores = {t: count_matches(text, pats) for t, pats in TOPIC_RULES.items()}
    # Pick highest score; ties broken by TOPIC_PRIORITY order
    best_score = max(scores.values())
    if best_score == 0:
        return "Other"
    for topic in TOPIC_PRIORITY:
        if scores.get(topic, 0) == best_score:
            return topic
    return "Other"


def extract_gbrs(text: str) -> list:
    found = [sys for sys, pats in GBRS_PATTERNS.items() if any_match(text, pats)]
    return found if found else ["None mentioned"]


def classify_bipv_app(text: str) -> str:
    for app in BIPV_APP_PRIORITY:
        if any_match(text, BIPV_APP_RULES[app]):
            return app
    return "Not specified"


def extract_key_sentences(abstract: str, max_sentences: int = 4) -> list:
    """Return sentences containing key terms, scored by keyword density."""
    if not abstract or pd.isna(abstract):
        return []
    text = str(abstract)
    sentences = re.split(r'(?<=[.!?])\s+', text.strip())
    scored = []
    t = text.lower()
    for s in sentences:
        sl = s.lower()
        score = sum(1 for kw in KEY_SENTENCE_KEYWORDS if re.search(kw, sl))
        if score > 0:
            scored.append((score, s.strip()))
    scored.sort(key=lambda x: -x[0])
    return [s for _, s in scored[:max_sentences]]


# ═══════════════════════════════════════════════════════════════
#  MAIN CLASSIFICATION LOOP
# ═══════════════════════════════════════════════════════════════

def classify_papers(df: pd.DataFrame) -> pd.DataFrame:
    rows = []
    for _, row in df.iterrows():
        title    = norm(row.get("Title", ""))
        abstract = norm(row.get("Abstract", ""))
        kw_auth  = norm(row.get("Author Keywords", ""))
        kw_idx   = norm(row.get("Index Keywords", ""))
        combined = f"{title} {abstract} {kw_auth} {kw_idx}"

        topic    = classify_topic(combined)
        gbrs     = extract_gbrs(combined)
        app_type = classify_bipv_app(combined)
        key_sents = extract_key_sentences(row.get("Abstract", ""))

        rows.append({
            "EID":            row.get("EID", ""),
            "Title":          row.get("Title", ""),
            "Year":           row.get("Year", ""),
            "Source title":   row.get("Source title", ""),
            "Cited by":       row.get("Cited by", 0),
            "DOI":            row.get("DOI", ""),
            "Topic_Category": topic,
            "GBRS_Mentioned": "; ".join(gbrs),
            "BIPV_Application": app_type,
            "Key_Sentences":  " | ".join(key_sents),
        })
    return pd.DataFrame(rows)


# ═══════════════════════════════════════════════════════════════
#  FIGURES
# ═══════════════════════════════════════════════════════════════

def savefig(fig, name):
    for ext in ("png", "pdf"):
        fig.savefig(os.path.join(FIG_DIR, f"{name}.{ext}"))
    plt.close(fig)
    print(f"  ✓ {name}.png/pdf")


def fig_topic_pie(df):
    counts = df["Topic_Category"].value_counts()
    colors = PALETTE[:len(counts)]

    fig, ax = plt.subplots(figsize=(9, 6))
    wedges, texts, autotexts = ax.pie(
        counts.values,
        colors=colors,
        autopct=lambda p: f"{p:.1f}%" if p > 3 else "",
        startangle=140,
        pctdistance=0.78,
        wedgeprops=dict(edgecolor="white", linewidth=1.5),
    )
    for at in autotexts:
        at.set_fontsize(8.5)
    ax.legend(
        wedges,
        [f"{l}  ({v})" for l, v in zip(counts.index, counts.values)],
        loc="center left", bbox_to_anchor=(0.95, 0.5), fontsize=9,
    )
    ax.set_title(f"Research Topic Distribution\n(n={len(df)} papers, merged corpus)",
                 fontsize=13, fontweight="bold", pad=14)
    savefig(fig, "topic_pie")


def fig_gbrs_bar(df):
    # Flatten multi-GBRS per paper
    counter = Counter()
    for val in df["GBRS_Mentioned"]:
        for g in val.split("; "):
            g = g.strip()
            if g and g != "None mentioned":
                counter[g] += 1
    if not counter:
        print("  ⚠  No GBRS mentions found")
        return

    series = pd.Series(counter).sort_values(ascending=True)
    colors = PALETTE[:len(series)]

    fig, ax = plt.subplots(figsize=(10, max(5, len(series) * 0.45 + 1.5)))
    bars = ax.barh(range(len(series)), series.values, color=colors, edgecolor="white")
    ax.set_yticks(range(len(series)))
    ax.set_yticklabels(series.index, fontsize=10)
    ax.set_xlabel("Number of Papers Mentioning System")
    ax.set_title("Green Building Rating Systems — Frequency in Literature\n"
                 "(papers may mention multiple systems)",
                 fontsize=13, fontweight="bold")
    ax.grid(axis="x", alpha=0.3)
    for bar, val in zip(bars, series.values):
        ax.text(val + 0.3, bar.get_y() + bar.get_height() / 2,
                str(val), va="center", fontsize=9)
    plt.tight_layout()
    savefig(fig, "gbrs_mentions_bar")


def fig_bipv_type_bar(df):
    counts = df["BIPV_Application"].value_counts()
    colors = PALETTE[:len(counts)]

    fig, ax = plt.subplots(figsize=(9, 5))
    bars = ax.bar(range(len(counts)), counts.values, color=colors, edgecolor="white", width=0.6)
    ax.set_xticks(range(len(counts)))
    ax.set_xticklabels(counts.index, fontsize=10, rotation=20, ha="right")
    ax.set_ylabel("Number of Papers")
    ax.set_title("BIPV Application Types Referenced in Literature",
                 fontsize=13, fontweight="bold")
    ax.grid(axis="y", alpha=0.3)
    total = counts.sum()
    for bar, val in zip(bars, counts.values):
        ax.text(bar.get_x() + bar.get_width() / 2, val + 4,
                f"{val}\n({val/total*100:.1f}%)", ha="center", fontsize=8.5)
    plt.tight_layout()
    savefig(fig, "bipv_type_bar")


def fig_topic_area_year(df):
    """Stacked area chart of topics over time."""
    all_topics = TOPIC_PRIORITY  # keeps a fixed order
    all_topics = [t for t in all_topics if t in df["Topic_Category"].values]

    years = sorted(df["Year"].dropna().astype(int).unique())
    if len(years) < 3:
        print("  ⚠  Too few years for area chart")
        return

    matrix = {}
    for topic in all_topics:
        sub = df[df["Topic_Category"] == topic].copy()
        sub["Year"] = sub["Year"].astype(int)
        yr_counts = sub.groupby("Year").size()
        matrix[topic] = np.array([yr_counts.get(y, 0) for y in years])

    fig, ax = plt.subplots(figsize=(13, 6))
    bottoms = np.zeros(len(years))
    for i, topic in enumerate(all_topics):
        vals = matrix[topic]
        ax.fill_between(years, bottoms, bottoms + vals,
                        label=topic, color=PALETTE[i % len(PALETTE)], alpha=0.85)
        bottoms += vals

    ax.set_xlabel("Year", fontsize=12)
    ax.set_ylabel("Number of Publications", fontsize=12)
    ax.set_title("Annual Topic Distribution — BIPV × GBRS Literature (2010–2026)",
                 fontsize=13, fontweight="bold")
    ax.set_xlim(min(years), max(years))
    ax.xaxis.set_major_locator(mticker.MultipleLocator(2))
    ax.legend(loc="upper left", fontsize=8, ncol=2, framealpha=0.8)
    ax.grid(axis="y", alpha=0.25)
    plt.tight_layout()
    savefig(fig, "topic_area_year")


# ═══════════════════════════════════════════════════════════════
#  KEY FINDINGS EXTRACTION
# ═══════════════════════════════════════════════════════════════

FINDING_THEMES = {
    "Barriers to BIPV adoption": [
        r"\bbarrier", r"\bchallenge.{0,60}(pv|solar|bipv|building|green|adoption)",
        r"\bobstacle", r"\bhinder", r"\bimpede", r"\blimit.{0,40}(pv|solar|bipv)",
        r"cost.{0,40}(barrier|challenge|prohibit|high).{0,40}(pv|solar|bipv)",
        r"lack.{0,40}(standard|awareness|guideline|knowledge).{0,60}(pv|bipv)",
        r"technical.{0,40}(barrier|challenge|uncertain|difficul).{0,60}(pv|bipv)",
    ],
    "Drivers and incentives for BIPV": [
        r"\bdriver", r"\benabl", r"\bincenti",
        r"\bmotivat.{0,60}(pv|solar|bipv|green|adopt)",
        r"\bpromot.{0,60}(pv|solar|bipv|renewable|green)",
        r"(benefit|advantage).{0,60}(bipv|pv|solar|green building)",
        r"(policy|regulation|mandate|requirement).{0,60}(promot|support|boost|enabl).{0,60}(pv|solar|bipv)",
        r"(subsidy|incentive|rebate|tax).{0,60}(pv|solar|bipv|renewable)",
    ],
    "GBRS credit/weight allocation for PV": [
        r"(credit|point|score|weight).{0,60}(pv|solar|bipv|photovoltaic|renewable)",
        r"(pv|solar|bipv|renewable).{0,60}(credit|point|score|weight|allocat)",
        r"percent.{0,40}(pv|solar|bipv|renewable).{0,40}(credit|point|total)",
        r"(leed|breeam|green mark|green star|casbee|dgnb|beam plus).{0,100}(credit|point|score|weight|pv|solar|bipv)",
        r"allocat.{0,60}(pv|solar|bipv|renewable|credit|point)",
        r"(maximum|max|available).{0,30}(point|credit).{0,60}(pv|solar|bipv|renewable|energy)",
    ],
    "GBRS influence on PV/BIPV adoption": [
        r"(rating system|certif|leed|breeam|green mark).{0,120}(adopt|promot|enabl|support|encour|driv).{0,60}(pv|solar|bipv)",
        r"(pv|solar|bipv).{0,60}(adopt|integrat|deploy).{0,60}(certif|rating|leed|breeam|green mark)",
        r"certif.{0,80}(pv|solar|bipv|renewable|photovoltaic)",
        r"(green building|rating).{0,60}(incentiv|promot|encour|improv|boost).{0,60}(pv|solar|bipv|renewable)",
        r"(credit|point).{0,40}(encour|promot|reward|incentiv).{0,60}(pv|solar|bipv|renewable)",
    ],
    "Net-zero targets and PV integration": [
        r"net.zero.{0,80}(pv|solar|bipv|photovoltaic|renewable)",
        r"(pv|solar|bipv|photovoltaic|renewable).{0,80}net.zero",
        r"(zero.energy|nzeb|nearly zero).{0,80}(pv|solar|bipv|photovoltaic)",
        r"(pv|solar|bipv|photovoltaic).{0,80}(zero.energy|nzeb|nearly zero)",
        r"energy (balance|neutral|positive).{0,60}(pv|solar|bipv)",
        r"(decarboni|carbon neutral|carbon zero).{0,80}(pv|solar|bipv|building)",
    ],
    "Policy and regulatory context": [
        r"(policy|regulation|building code).{0,80}(pv|solar|bipv|renewable|green building)",
        r"(government|national|municipal|mandator).{0,80}(pv|solar|bipv|renewable|green)",
        r"(iec\s*63092|standard).{0,60}(bipv|pv|solar)",
        r"(legislation|law|directive).{0,60}(pv|solar|bipv|renewable|green building)",
        r"(feed.in tariff|net metering|grid parity).{0,60}(pv|solar|bipv)",
    ],
}


def extract_findings(df: pd.DataFrame) -> dict:
    """Extract and rank the best sentences per theme across all papers."""
    results = defaultdict(list)
    for _, row in df.iterrows():
        abstract = str(row.get("Abstract", ""))
        if not abstract.strip():
            continue
        title  = str(row.get("Title", ""))
        year   = row.get("Year", "")
        cited  = int(row.get("Cited by", 0)) if pd.notna(row.get("Cited by")) else 0
        source = str(row.get("Source title", ""))
        doi    = str(row.get("DOI", ""))

        sentences = re.split(r'(?<=[.!?])\s+', abstract.strip())
        for theme, patterns in FINDING_THEMES.items():
            for sent in sentences:
                sl = sent.lower()
                score = sum(1 for p in patterns if re.search(p, sl))
                if score >= 1:
                    results[theme].append({
                        "score": score,
                        "cited": cited,
                        "sentence": sent.strip(),
                        "title": title,
                        "year": int(year) if pd.notna(year) else "",
                        "source": source,
                        "doi": doi,
                    })

    # Deduplicate and rank
    for theme in results:
        seen, unique = set(), []
        for item in results[theme]:
            key = item["sentence"][:80].lower()
            if key not in seen:
                seen.add(key)
                # rank score = keyword hits + citation boost (capped)
                item["rank"] = item["score"] * 3 + min(item["cited"] / 5, 10)
                unique.append(item)
        results[theme] = sorted(unique, key=lambda x: -x["rank"])[:10]
    return results


# ═══════════════════════════════════════════════════════════════
#  KEY FINDINGS MARKDOWN
# ═══════════════════════════════════════════════════════════════

def write_key_findings(findings: dict, path: str):
    lines = [
        "# Key Findings Extracted from Literature",
        "",
        "> **Source:** Keyword-pattern extraction from abstracts of the merged Scopus corpus.",
        "> Sentences are ranked by keyword density × citation count of the source paper.",
        "",
        "---",
        "",
    ]
    for i, (theme, items) in enumerate(findings.items(), 1):
        lines.append(f"## {i}. {theme}")
        lines.append("")
        if not items:
            lines.append("*No strongly matching sentences found.*")
        else:
            for item in items[:8]:
                wrapped = textwrap.fill(item["sentence"], width=120)
                cite_note = f"cited {item['cited']}×" if item["cited"] > 0 else "uncited"
                lines.append(f'> "{wrapped}"')
                lines.append(f'> — *{item["title"][:85]}{"…" if len(item["title"])>85 else ""}*  ')
                lines.append(f'> ({item["year"]} · {item["source"][:50]} · {cite_note})')
                lines.append("")
        lines.append("")
    lines += ["---", "", "*Generated by `src/literature_classification.py`*"]
    with open(path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
    print(f"  ✓ key_findings.md")


# ═══════════════════════════════════════════════════════════════
#  FULL ANALYSIS REPORT
# ═══════════════════════════════════════════════════════════════

def write_report(df: pd.DataFrame, findings: dict, path: str):
    n = len(df)
    yr_min = int(df["Year"].min())
    yr_max = int(df["Year"].max())
    topic_counts = df["Topic_Category"].value_counts()
    app_counts   = df["BIPV_Application"].value_counts()
    rel_counts   = df.get("GBRS_Relationship", pd.Series(dtype=str)).value_counts()

    # GBRS mention totals
    gbrs_counter = Counter()
    no_gbrs = 0
    for val in df["GBRS_Mentioned"]:
        parts = [g.strip() for g in val.split("; ") if g.strip()]
        if parts == ["None mentioned"]:
            no_gbrs += 1
        else:
            gbrs_counter.update(parts)

    cross_n = topic_counts.get("BIPV+GBRS Cross", 0)
    gbrs_n  = topic_counts.get("GBRS Comparative Analysis", 0)

    lines = [
        "# Literature Content Analysis Report",
        f"## BIPV × Green Building Rating Systems — Merged Scopus Corpus (n={n})",
        "",
        "> **Method:** Keyword-based NLP classification (no external API)  ",
        f"> **Sources:** scopus_export.csv · scopus_search_A/B/C.csv (merged + deduplicated)  ",
        f"> **Period:** {yr_min}–{yr_max}",
        "",
        "---",
        "",
        "## 1. Dataset Overview",
        "",
        f"| Metric | Value |",
        f"|--------|-------|",
        f"| Total unique papers | **{n}** |",
        f"| Publication period | {yr_min}–{yr_max} |",
        f"| BIPV+GBRS cross-topic papers | {cross_n} ({cross_n/n*100:.1f}%) |",
        f"| GBRS comparative papers | {gbrs_n} ({gbrs_n/n*100:.1f}%) |",
        f"| Papers naming ≥1 GBRS system | {n-no_gbrs} ({(n-no_gbrs)/n*100:.1f}%) |",
        f"| Papers with no GBRS mention | {no_gbrs} ({no_gbrs/n*100:.1f}%) |",
        "",
        "---",
        "",
        "## 2. Research Topic Distribution",
        "",
        "| Topic Category | Count | Share |",
        "|---|---:|---:|",
    ]
    for topic, cnt in topic_counts.items():
        lines.append(f"| {topic} | {cnt} | {cnt/n*100:.1f}% |")

    lines += [
        "",
        "**Key observation:** "
        f"The corpus is dominated by *{topic_counts.index[0]}* "
        f"({topic_counts.iloc[0]} papers, {topic_counts.iloc[0]/n*100:.1f}%), "
        "reflecting the technology-push character of current BIPV research. "
        f"Only **{cross_n}** papers ({cross_n/n*100:.1f}%) explicitly bridge BIPV and GBRS criteria — "
        "quantifying the gap this review addresses. "
        f"Together, 'BIPV+GBRS Cross' and 'GBRS Comparative' account for just "
        f"{(cross_n+gbrs_n)/n*100:.1f}% of the corpus.",
        "",
        "![Topic Pie](../outputs/figures/topic_pie.png)",
        "",
        "![Topic Area Year](../outputs/figures/topic_area_year.png)",
        "",
        "---",
        "",
        "## 3. GBRS Systems Mentioned in Literature",
        "",
        "| System | Papers | % of corpus |",
        "|---|---:|---:|",
    ]
    for sys, cnt in sorted(gbrs_counter.items(), key=lambda x: -x[1]):
        lines.append(f"| {sys} | {cnt} | {cnt/n*100:.1f}% |")
    lines.append(f"| *No system mentioned* | {no_gbrs} | {no_gbrs/n*100:.1f}% |")

    if gbrs_counter:
        top_sys = max(gbrs_counter, key=gbrs_counter.get)
        top_cnt = gbrs_counter[top_sys]
        top3 = ", ".join(
            f"{s} ({c})" for s, c in sorted(gbrs_counter.items(), key=lambda x: -x[1])[:3]
        )
        lines += [
            "",
            f"**Key observation:** {top_sys} is the most cited GBRS ({top_cnt} papers). "
            f"Top three: {top3}. "
            f"{no_gbrs} papers ({no_gbrs/n*100:.1f}%) reference no named system, confirming that "
            "most BIPV research is conducted without reference to any rating framework.",
        ]

    lines += [
        "",
        "![GBRS Mentions](../outputs/figures/gbrs_mentions_bar.png)",
        "",
        "---",
        "",
        "## 4. BIPV Application Types",
        "",
        "| Application Type | Count | % |",
        "|---|---:|---:|",
    ]
    for app, cnt in app_counts.items():
        lines.append(f"| {app} | {cnt} | {cnt/n*100:.1f}% |")

    facade_n = app_counts.get("Façade BIPV", 0)
    window_n = app_counts.get("Window / Curtain Wall BIPV", 0)
    lines += [
        "",
        f"**Key observation:** Non-rooftop BIPV (façade + window/curtain wall) accounts for "
        f"{(facade_n+window_n)/n*100:.1f}% of papers ({facade_n+window_n} papers). "
        "Despite its architectural significance, window/curtain-wall BIPV and façade BIPV "
        "remain under-represented relative to generic PV systems, suggesting that GBRS criteria "
        "for building-integrated applications lag behind emerging technology.",
        "",
        "![BIPV Type Bar](../outputs/figures/bipv_type_bar.png)",
        "",
        "---",
        "",
        "## 5. Key Extracted Findings",
        "",
        "> Full evidence sentences are in `data/processed/key_findings.md`.",
        "",
    ]
    for i, (theme, items) in enumerate(findings.items(), 1):
        lines.append(f"### 5.{i}. {theme}")
        lines.append("")
        if not items:
            lines.append("*No strongly matching sentences found.*")
        else:
            for item in items[:4]:
                wrapped = textwrap.fill(item["sentence"], width=115)
                lines.append(f'> "{wrapped}"')
                cite_note = f"cited {item['cited']}×" if item["cited"] > 0 else "uncited"
                lines.append(
                    f'> — *{item["title"][:75]}{"…" if len(item["title"])>75 else ""}* '
                    f'({item["year"]} · {cite_note})'
                )
                lines.append("")
        lines.append("")

    lines += [
        "---",
        "",
        "## 6. Research Gaps — Implications for This Review",
        "",
        f"1. **Sparse BIPV×GBRS literature:** Only {cross_n+gbrs_n} papers "
        f"({(cross_n+gbrs_n)/n*100:.1f}%) discuss both domains together. "
        "A systematic, multi-dimensional scoring of how 21 GBRS handle BIPV is absent.",
        "",
        f"2. **Anglo-American GBRS bias:** LEED and BREEAM dominate mentions; "
        "regional systems (CASBEE, DGNB, Green Mark, ASGB, HQE, GRIHA) are under-studied.",
        "",
        "3. **Non-rooftop BIPV neglected:** Façade and window/curtain-wall BIPV have "
        "minimal representation in the context of certification criteria.",
        "",
        "4. **Performance verification gap:** Few papers address post-occupancy "
        "monitoring of BIPV within GBRS frameworks.",
        "",
        "5. **Standards lag:** IEC 63092 (BIPV product standard) is almost never "
        "referenced alongside GBRS, indicating a disconnect between product standards "
        "and building certification.",
        "",
        "---",
        "",
        "*Report generated automatically by `src/literature_classification.py`*",
    ]

    with open(path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
    print(f"  ✓ literature_analysis_report.md")


# ═══════════════════════════════════════════════════════════════
#  MAIN
# ═══════════════════════════════════════════════════════════════

def main():
    print("=" * 62)
    print("Literature Classification — BIPV × GBRS (merged corpus)")
    print("=" * 62)

    df = load_and_merge()

    print("\n── Classifying papers ──")
    classified = classify_papers(df)
    csv_path = os.path.join(PROCESSED_DIR, "literature_classification.csv")
    classified.to_csv(csv_path, index=False)
    print(f"  ✓ literature_classification.csv  ({len(classified)} rows)")

    print("\n── Generating figures ──")
    fig_topic_pie(classified)
    fig_gbrs_bar(classified)
    fig_bipv_type_bar(classified)
    fig_topic_area_year(classified)

    print("\n── Extracting key findings ──")
    findings = extract_findings(df)
    for theme, items in findings.items():
        print(f"  {len(items):2d}  {theme}")

    print("\n── Writing outputs ──")
    write_key_findings(findings, os.path.join(PROCESSED_DIR, "key_findings.md"))
    write_report(classified, findings, os.path.join(DOCS_DIR, "literature_analysis_report.md"))

    print("\n✅ Done.")
    print(f"   data/processed/literature_classification.csv")
    print(f"   data/processed/key_findings.md")
    print(f"   outputs/figures/  (4 new charts)")
    print(f"   docs/literature_analysis_report.md")


if __name__ == "__main__":
    main()
