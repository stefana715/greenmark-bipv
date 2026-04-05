# Updated Review Paper Framework: Meta-Review Approach (No Survey Required)

## Revised Title
**"Building-Integrated Photovoltaics in Green Building Rating Systems: A meta-review and content-based criteria assessment"**

---

## Why Meta-Review Works Here

A meta-review (also called "review of reviews" or "systematic mapping study") synthesizes findings from **existing review papers and primary studies** rather than collecting new primary data. This is legitimate and publishable in RSER when:

1. The topic has enough existing reviews to synthesize (✓ — BIPV reviews + GBRS reviews both exist, but not at their intersection)
2. You add a structured analytical framework beyond just summarizing (✓ — our content-based scoring matrix)
3. You identify gaps across the literature landscape (✓)

**Published precedents in RSER:**
- Meta-reviews and bibliometric-based reviews are common in RSER
- The journal accepts "critical reviews" that analyze GBRS manuals directly (like Doan et al. 2017)
- Content analysis of official documents (GBRS manuals) counts as primary data in built environment research

---

## Revised Methodology: Three Layers, Zero Surveys

### Layer 1: Bibliometric Meta-Analysis
- Search Scopus/WOS for papers at the intersection of BIPV + GBRS
- Map the research landscape: who studies what, where, when
- Tool: VOSviewer for keyword co-occurrence and citation networks
- **Output:** Research trend figures, gap identification

### Layer 2: Direct GBRS Manual Content Analysis
- Systematically read official GBRS manuals (these are public/purchasable documents)
- Extract every criterion related to PV/BIPV
- This is YOUR primary data — no survey needed
- Apply a structured scoring framework (see below)
- **Output:** Master comparison tables

### Layer 3: Content-Based Scoring Matrix (replaces AHP)
Instead of asking experts to weight criteria, you **derive weights from the literature itself**:

**Method A: Frequency-based weighting (from literature)**
- Count how many published papers identify each criterion as "important" for BIPV adoption
- Example: if 15 out of 20 papers say "dedicated renewable energy credits" matter most → highest weight
- This is objective, reproducible, no expert panel needed

**Method B: GBRS-derived scoring (from manuals)**
- For each GBRS, calculate the actual % of total points allocated to PV/BIPV-related criteria
- Normalize across systems to compare
- Completely objective — just math from the manuals

**Method C: Multi-dimensional scoring matrix (qualitative but systematic)**
- Define 6–8 assessment dimensions based on literature consensus
- Score each GBRS on each dimension using a defined rubric (0-1-2-3 scale)
- Justify each score with specific manual clause references
- This is content analysis — a well-established research method

→ **Method C is the strongest choice for RSER.** It's rigorous, transparent, and doesn't require external data collection.

---

## Revised Paper Structure

### 1. Introduction (≈1,000 words)
Same as before — context, gap, objectives.

**Three research questions:**
- RQ1: How is the intersection of BIPV and GBRS represented in the existing literature?
- RQ2: How do major GBRS address BIPV in their criteria, and what are the key differences?
- RQ3: Which GBRS design features most effectively promote BIPV adoption, and what improvements are needed?

### 2. Methodology (≈1,200 words)

#### 2.1 Bibliometric search strategy
- Databases: Scopus + WOS
- Search strings: ("BIPV" OR "building integrated photovoltaic*" OR "building-integrated photovoltaic*") AND ("green building" OR "rating system" OR "certification" OR "LEED" OR "BREEAM" OR "Green Mark" OR "Green Star" OR "CASBEE" OR "DGNB" OR "BEAM Plus" OR "ASGB")
- Inclusion criteria: English, peer-reviewed, 2010–2025
- Exclusion: conference abstracts only, non-English, pure technology papers with no GBRS discussion
- PRISMA 2020 flow diagram
- Bibliometric tools: VOSviewer, Bibliometrix R package

#### 2.2 GBRS manual selection and analysis
- 8 systems selected (with justification: geographic coverage, market share, availability)
- Latest version of each manual analyzed
- Extraction protocol: every section/credit mentioning PV, solar, renewable, BIPV, facade energy, etc.
- Data recorded: credit name, category, max points, requirement type, BIPV-specific language

#### 2.3 Content-based assessment framework
**Assessment dimensions (derived from synthesizing the literature):**

| Dimension | Description | Scoring rubric |
|-----------|-------------|----------------|
| D1: Credit Weight | % of total available points allocated to PV/renewables | 0: <3%, 1: 3-8%, 2: 8-15%, 3: >15% |
| D2: BIPV Specificity | Whether BIPV is explicitly recognized vs. generic PV | 0: no PV mention, 1: PV mentioned, 2: BIPV mentioned, 3: BIPV has dedicated criteria |
| D3: Application Coverage | How many BIPV types are recognized (roof/façade/window/shading) | 0: none, 1: roof only, 2: roof + 1 other, 3: all types |
| D4: Design Integration | Whether solar studies/design integration is required | 0: none, 1: optional, 2: encouraged, 3: mandatory feasibility study |
| D5: Ambition Level | Target for renewable energy contribution | 0: none, 1: <5%, 2: 5-20%, 3: >20% or net-zero pathway |
| D6: Performance Verification | Whether actual PV output is measured post-occupancy | 0: none, 1: commissioning only, 2: operational data, 3: ongoing M&V |
| D7: Synergy with Envelope | Whether BIPV counts toward envelope/materials credits too | 0: energy only, 1: minor crossover, 2: dual-counting, 3: integrated assessment |
| D8: Innovation Pathway | Whether innovative BIPV can earn extra points | 0: none, 1: generic innovation credit, 2: renewable-specific innovation, 3: BIPV-specific innovation |

- Each score is justified by citing the specific GBRS manual clause
- Total score per GBRS = sum across dimensions (max 24)
- Radar charts and heatmaps for visualization

### 3. BIPV Technology and GBRS Background (≈1,200 words)
- Brief BIPV technology overview (types, performance, market)
- Brief GBRS landscape overview (history, major systems, evolution)
- How PV/BIPV typically fits within GBRS structures
- Urban morphology factors affecting BIPV (reference to uploaded figure)

### 4. Bibliometric Results (≈1,500 words) — Answers RQ1
- Publication trend (year-by-year, showing growth at intersection)
- Top journals, top authors, top institutions
- Geographic distribution of research
- Keyword co-occurrence analysis → identify research clusters
- Citation network → most influential papers
- **Key finding: the gap** — separate streams of BIPV tech and GBRS research rarely intersect

**Figures:** publication trend chart, keyword map, geographic distribution, PRISMA

### 5. Comparative Analysis of BIPV in GBRS (≈3,000 words) — Answers RQ2
★ CORE SECTION

#### 5.1 System-by-system analysis
For each of the 8 GBRS, a structured paragraph covering:
- Where PV/BIPV sits in the scoring structure
- Specific credits and their requirements
- Whether BIPV is distinguished from BAPV
- How criteria have evolved across versions
- Notable strengths and gaps

#### 5.2 Cross-system comparison
- Master comparison table (all 8 systems × key parameters)
- Theme 1: Weight allocation — who gives most to renewables?
- Theme 2: Performance vs. prescriptive approaches
- Theme 3: BIPV specificity — who actually says "BIPV"?
- Theme 4: Façade and window BIPV — the blind spot
- Theme 5: Net-zero pathways and the role of PV

#### 5.3 BIPV application type coverage
- Expanded version of your CSV data → proper table with manual references
- Scoring: explicit support (3), implicit support (2), partial mention (1), absent (0)
- Heatmap visualization
- **Key finding:** Roof PV is well-supported everywhere; façade BIPV is poorly recognized; window/glazing BIPV is almost invisible in criteria

**Tables:** Master comparison, Application type matrix, Evolution timeline
**Figures:** Radar chart, Heatmap, Stacked bar chart

### 6. Content-Based Assessment Results (≈1,500 words) — Answers RQ3
- Present the 8-dimension scoring for each GBRS
- Overall ranking by total score
- Dimension-by-dimension analysis:
  * Which dimension shows most variation across systems?
  * Which dimension is universally weak?
- Spider/radar charts for visual comparison
- Identify "best-in-class" for each dimension
- Sensitivity check: does ranking change if certain dimensions are weighted 2×?

**Tables:** Full scoring matrix with justifications
**Figures:** Radar chart per GBRS, Overall ranking bar chart

### 7. Discussion (≈1,500 words)
#### 7.1 Synthesis of findings
- Green Mark and Green Star most BIPV-friendly overall
- LEED and ASGB treat PV as optional within energy performance
- No system adequately recognizes façade BIPV as a building material
- BREEAM's mandatory feasibility study is a best practice others should adopt

#### 7.2 Barriers identified from literature
- Technical uncertainty of BIPV performance
- Regulatory gap: BIPV standards (IEC 63092) not yet referenced in most GBRS
- Economic: higher cost not reflected in credit value
- Knowledge gap among assessors and designers

#### 7.3 Recommendations
For GBRS developers:
1. Create BIPV-specific sub-credits (not just "renewable energy")
2. Recognize façade and window BIPV with dedicated pathways
3. Mandate solar feasibility studies at design stage
4. Reference IEC 63092 BIPV standards
5. Adopt climate-adjusted PV targets
6. Link credits to measured operational performance
7. Allow BIPV to contribute to multiple categories (energy + envelope + materials)

For future research:
1. Empirical studies linking GBRS criteria to actual BIPV adoption rates
2. Development of BIPV-specific performance benchmarks for GBRS
3. Integration of urban morphology assessment into GBRS criteria
4. Life cycle assessment of BIPV within GBRS frameworks

#### 7.4 Limitations
- Content analysis involves judgment (mitigated by transparent rubric)
- Only English-language manuals and papers analyzed
- GBRS evolve rapidly — findings are a snapshot
- Some GBRS manuals not freely available (CASBEE, DGNB)

### 8. Conclusion (≈500 words)

### References (≈80–100 references)

---

## What You Can Start Doing RIGHT NOW with Claude Code

### Step 1: Bibliometric Analysis (I can write the Python scripts)
```
Input: Scopus/WOS export files (.csv or .bib)
Process: Parse, clean, analyze publication trends, keyword frequencies
Output: Publication trend charts, keyword co-occurrence data for VOSviewer
```
→ You need to run the Scopus/WOS searches yourself and download the results
→ I build the analysis pipeline

### Step 2: GBRS Manual Analysis Template
→ I create a structured Excel template for you to fill as you read each manual
→ Standardized extraction protocol ensures consistency

### Step 3: Scoring Matrix Calculation
→ Once you fill the scores, I calculate totals, generate radar charts, heatmaps
→ I also do sensitivity analysis automatically

### Step 4: Visualization Suite
→ All figures created programmatically for publication quality
→ Radar charts, heatmaps, stacked bars, PRISMA diagrams

### Step 5: Writing
→ I draft each section following RSER conventions
→ You review, revise, add your domain expertise

---

## Comparison: Old Approach vs. New Approach

| Aspect | Old (AHP + Survey) | New (Meta-Review + Content Analysis) |
|--------|-------------------|-------------------------------------|
| Data collection | Need 10+ expert surveys | Library + manual reading only |
| Time to complete | 8-10 weeks (survey delays) | 4-6 weeks |
| Novelty | AHP is common in GBRS research | Content-based scoring at BIPV×GBRS intersection is new |
| Objectivity | AHP weights are subjective | Scoring rubric is transparent and reproducible |
| Reviewer acceptance | "Where's your expert justification?" | "Clear methodology, reproducible" |
| RSER fit | Good but expected | Good — systematic and rigorous |

---

## Immediate Next Step

Tell me which of these you want me to build first:
1. The bibliometric analysis Python pipeline (you provide Scopus export)
2. The GBRS extraction template (Excel file for your manual reading)
3. The scoring matrix calculator + visualization tool
4. A draft of any specific section
5. The full PRISMA search strategy document
