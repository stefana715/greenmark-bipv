# 2. Methodology

This study employs a three-phase mixed-methods design combining systematic bibliometric analysis, structured manual content analysis of primary GBRS documents, and a multi-dimensional scoring framework. The phases are sequential and cumulative: bibliometric findings inform the selection of GBRS for the manual review, and manual review findings populate the scoring framework that constitutes the core analytical output. Each phase is described below with sufficient procedural detail to permit replication.

## 2.1 Phase 1: Systematic Bibliometric Analysis

### 2.1.1 Search Strategy and Database

The literature search was conducted in Scopus, the largest multidisciplinary abstract and citation database. Four complementary search queries were executed to capture the full breadth of BIPV-related scholarship and its intersection with green building certification:

- Query A: TITLE-ABS-KEY ("building integrated photovoltaic" OR "BIPV") AND PUBYEAR > 1999
- Query B: TITLE-ABS-KEY ("building integrated solar" OR "integrated PV" OR "PV façade" OR "solar façade") AND PUBYEAR > 1999
- Query C: TITLE-ABS-KEY ("green building" OR "sustainable building") AND ("photovoltaic" OR "solar energy") AND PUBYEAR > 1999
- Query D: TITLE-ABS-KEY ("LEED" OR "BREEAM" OR "Green Star" OR "Green Mark" OR "DGNB") AND ("photovoltaic" OR "BIPV" OR "solar") AND PUBYEAR > 1999

The four result sets were exported as CSV files (N = 310, 785, 820, 415) and merged into a single corpus. Duplicate records were identified by normalised title comparison (lowercase, punctuation-stripped) and removed. The resulting deduplicated corpus comprised 2,330 unique records spanning the period 2000–2024.

### 2.1.2 Classification Framework

Each paper was classified using a keyword-scoring algorithm implemented in Python (src/literature_classification.py). Eight topic categories were defined with associated keyword patterns: (1) BIPV Technical Performance, (2) BIPV+GBRS Cross, (3) Thermal and Envelope, (4) Lifecycle Assessment, (5) Policy and Market, (6) Urban and Planning, (7) Indoor Environment Quality, and (8) General Green Building. Classification used a scoring approach in which all keyword patterns were applied to each record's title and abstract, yielding a score per topic; the topic with the highest score was assigned as the primary classification, with a minimum threshold applied to prevent misclassification of weakly matched records.

Separate detection passes identified whether each paper mentioned any of the 21 GBRS included in Phase 2 by name or standard acronym. A further set of six key-finding themes (carbon neutrality/net-zero, façade integration, urban-scale deployment, thermal performance, daylighting/visual comfort, policy/regulation) was extracted using phrase-level pattern matching.

### 2.1.3 Geographic and Temporal Analysis

Author country was extracted from the affiliation string of the first-listed author. Each affiliation was parsed by splitting on semicolons (to isolate individual affiliations) and then taking the last comma-delimited token of each fragment, which conventionally contains the country name in Scopus exports. Publication year was taken directly from the Scopus "Year" field. Temporal trends and geographic distributions were visualised using matplotlib and seaborn.

## 2.2 Phase 2: Manual Content Analysis of GBRS Documents

### 2.2.1 System Selection

Twenty-one GBRS were selected to achieve broad geographic and institutional coverage. Selection criteria were: (a) the system is currently operational and administers active certifications; (b) technical reference documents are publicly available or were obtained via institutional access; (c) the system is sufficiently developed to include quantitative performance credits (eliminating very nascent rating tools). The 21 systems span 19 countries across Asia-Pacific, Europe, North America, the Middle East, Africa, and South Asia (see Table 1 in results).

### 2.2.2 Document Collection

Primary technical reference documents were collected for all 21 systems, yielding 31 PDF files totalling approximately 8,400 pages. Documents included technical manuals, credit guides, assessment frameworks, and reference standards, prioritising the most recent publicly available version of each system as of the analysis date (Q1 2025). File names and versions are listed in the supplementary materials.

### 2.2.3 Extraction Protocol

A two-pass extraction protocol was applied to each document. In the first pass (direct extraction), targeted keyword searches were conducted for terms directly associated with PV and BIPV: "photovoltaic," "PV," "BIPV," "solar panel," "solar energy," "renewable energy," "solar power," "net zero energy," "net positive energy," and system-specific equivalents. All matching passages were recorded with page number, credit identifier, section heading, and exact quotation.

In the second pass (indirect extraction), separate keyword sets corresponding to each of the seven indirect performance dimensions were applied to relevant document chapters: "envelope" and "U-value" and "SHGC" for Dimension F (Thermal Envelope); "daylight" and "visual comfort" and "glare" and "VLT" for Dimension G (Daylighting/Visual); "lifecycle" and "LCA" and "embodied" and "EPD" for Dimension H (Materials/LCA); "carbon" and "net zero" and "greenhouse gas" for Dimension I (Carbon Accounting); "electric vehicle" and "EV charging" and "battery" and "storage" for Dimension J (EV/Storage Synergy); "design integration" and "integrative process" and "massing" and "solar orientation" for Dimension K (Design Integration); and "innovation" and "pilot" and "exemplary" for Dimension L (Innovation Pathways). To avoid memory issues with large documents, indirect extraction was implemented using targeted page-range scanning via the pdfplumber library, with explicit page ranges assigned per (GBRS, dimension) combination based on the table of contents structure of each document (src/extended_extraction.py).

All extracted passages were recorded in a structured database (data/processed/gbrs_extraction_full.csv for direct extraction; data/processed/gbrs_extraction_extended.csv for indirect extraction) with fields for GBRS name, dimension code, credit identifier, category, points available, total system points, requirement type (mandatory/optional), exact language quote, and verification status (Verified/Partial/Existing).

## 2.3 Phase 3: The 12-Dimension BIPV Mapping Framework

### 2.3.1 Dimension Definition

The mapping framework organises BIPV's building-relevant performance contributions into 12 dimensions, grouped into two clusters. Cluster 1 (Dimensions A–E) covers direct PV/BIPV application typologies; Cluster 2 (Dimensions F–L) covers indirect performance domains in which BIPV products interact with non-energy building performance criteria.

**Cluster 1 — Direct BIPV Applications:**
- Dimension A (A_Roof_PV): Roof-mounted PV systems, including BIPV roof tiles, shingles, and laminates integrated into the roof plane.
- Dimension B (B_Facade_PV): Façade-integrated PV, including opaque and semi-opaque cladding panels, rainscreen systems, and curtain wall spandrels.
- Dimension C (C_Window_Curtain_PV): Semi-transparent BIPV glazing in windows and curtain-wall vision areas.
- Dimension D (D_Shading_PV): PV-integrated external shading devices, including louvres, brise-soleil, and canopy elements.
- Dimension E (E_Glass_Energy_PV): Electrochromic or chromogenic PV glazing and other glass products with integrated energy functions beyond simple transparency.

**Cluster 2 — Indirect Performance Dimensions:**
- Dimension F (F_Thermal_Envelope): Credits or prerequisites relating to building envelope thermal performance in which BIPV products participate as envelope components.
- Dimension G (G_Daylighting_Visual): Credits relating to spatial daylight autonomy, daylight factor, glare control, and views in which BIPV glazing or shading devices affect the assessed metric.
- Dimension H (H_Materials_LCA): Lifecycle assessment, embodied carbon, Environmental Product Declaration (EPD), and responsible sourcing credits applicable to BIPV modules as building materials.
- Dimension I (I_Carbon_Accounting): Operational carbon and net-zero carbon accounting methodologies in which on-site PV generation is credited or counted.
- Dimension J (J_EV_Storage): Credits for EV charging infrastructure, on-site battery storage, or demand response in which solar PV plays an explicit supporting role.
- Dimension K (K_Design_Integration): Integrative design process credits, solar orientation and massing requirements, and site-level solar feasibility assessment mandates.
- Dimension L (L_Innovation): Innovation credits, pilot credits, or exemplary performance pathways through which novel BIPV applications can earn recognition beyond standard credit structures.

### 2.3.2 Scoring Rubric

Each of the 252 GBRS × dimension cells was assigned a score on the following four-level ordinal rubric:

- **Score 0 (Not Addressed):** The dimension is not mentioned in the GBRS documentation, or PV/BIPV is explicitly excluded from the relevant credit category.
- **Score 1 (Indirect/Implied):** The GBRS includes credits relevant to the dimension (e.g., a thermal envelope credit, a materials sustainability credit) but does not explicitly mention PV or BIPV products as eligible; BIPV could potentially qualify but the framework is silent on the matter.
- **Score 2 (Explicit Recognition):** The GBRS explicitly mentions PV, BIPV, or solar products in the context of the relevant credit category, indicating that such products are recognised within the credit's scope.
- **Score 3 (Dedicated Criteria):** The GBRS includes one or more credits or prerequisites specifically designed for, or that directly name, BIPV as a product category; or includes quantitative thresholds, modelling guidance, or product standards specific to integrated solar products.

Scores were assigned independently for each dimension by the lead researcher based on the extracted passages from Phase 2, with the Manual_Verified flag used to distinguish cells where primary document evidence was obtained (True) from cells where scores were inferred from secondary documentation or established system knowledge (False). The complete 21 × 12 matrix is provided in data/mapping_matrix_full.csv.

### 2.3.3 Analytical Outputs

The mapping matrix was analysed to produce four categories of output: (1) a master heatmap of all 252 scores (Fig. mapping_master_heatmap); (2) dimension-level coverage statistics across all 21 systems (Fig. mapping_dimension_coverage); (3) system-level GBRS profile plots showing dimensional strengths and weaknesses (Fig. mapping_gbrs_profiles); (4) application-typology coverage plots for Dimensions A–E (Fig. mapping_bipv_applications); and (5) a gap analysis identifying zero-coverage and below-mean cells (Fig. mapping_gap_analysis). Total scores per GBRS were computed as the sum of scores across all 12 dimensions (maximum possible: 36), and are provided in outputs/tables/mapping_gbrs_totals.csv.

All data processing, visualisation, and statistical analysis was conducted in Python 3.11 using pandas, numpy, matplotlib, and seaborn. Source code is available in the src/ directory of the project repository.
