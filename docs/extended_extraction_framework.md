# Extended Extraction Framework: Indirect PV/BIPV References in GBRS

## Purpose

First-pass manual review (Round 1) focused on Energy/Renewable Energy chapters only.
This second-pass framework targets **indirect** PV/BIPV relevance — criteria that create
enabling conditions or hidden barriers for BIPV integration without explicitly mentioning
renewable energy.

These findings are primary material for **Section 7 Discussion** of the paper, specifically:
- 7.1 Synthesis: "No system adequately recognizes façade BIPV as a building material"
- 7.2 Barriers: technical uncertainty, regulatory gap, knowledge gap
- 7.3 Recommendations for GBRS developers

---

## Dimension 1 — Envelope + PV

**Hypothesis:** Some systems assess building envelope performance (U-value, SHGC, ETTV)
in ways that either conflict with or could synergize with BIPV facade integration.

**Search terms (co-occurrence within ~3 paragraphs):**
- Primary: `envelope`, `façade`, `curtain wall`, `U-value`, `SHGC`, `ETTV`
- Co-occurring: `PV`, `solar`, `photovoltaic`, `BIPV`, `integrated`

**What to extract:**
- Does the envelope credit penalise BIPV facades (e.g. opaque BIPV counted as wall, not window)?
- Is BIPV facade explicitly excluded or included from SHGC/U-value calculations?
- Does the system allow BIPV to satisfy both envelope AND energy criteria simultaneously?
- Any mention of "building-integrated" materials in envelope context

---

## Dimension 2 — Daylighting / Visual Comfort + Solar

**Hypothesis:** Daylighting credits and shading requirements can conflict with PV (opaque
panels block daylight) or enable BIPV (semi-transparent PV satisfies both shading and
daylighting simultaneously).

**Search terms:**
- Primary: `daylight`, `visual comfort`, `VLT`, `glare`, `shading device`, `solar control`
- Co-occurring: `PV`, `solar`, `photovoltaic`, `louver`, `louvre`, `semi-transparent`

**What to extract:**
- Do daylighting credits explicitly allow PV shading devices as a compliant solution?
- Is semi-transparent PV recognized as a daylighting tool?
- Do shading requirements conflict with or enable BIPV integration?
- Any daylight-PV trade-off language

---

## Dimension 3 — Materials / LCA + PV

**Hypothesis:** LCA and materials credits could either recognize or ignore the lifecycle
benefits and burdens of PV as a building material component. DGNB is expected to lead here.

**Search terms:**
- Primary: `life cycle`, `LCA`, `embodied carbon`, `EPD`, `material`, `product declaration`
- Co-occurring: `PV`, `solar`, `photovoltaic`, `panel`, `module`, `BIPV`

**What to extract:**
- Is PV assessed as a building product with an EPD requirement?
- Does the LCA boundary include or exclude on-site PV generation?
- Is BIPV treated as a construction material (with associated embodied carbon)?
- Any interaction between Materials credits and Energy credits for PV

---

## Dimension 4 — EV / Storage + PV

**Hypothesis:** EV charging and battery storage credits are increasingly linked to on-site
renewable generation, creating indirect PV demand.

**Search terms:**
- Primary: `electric vehicle`, `EV charging`, `battery`, `storage`, `smart grid`, `demand response`
- Co-occurring: `PV`, `solar`, `renewable`, `on-site generation`, `grid`

**What to extract:**
- Do EV credits explicitly require or prefer on-site solar to power charging?
- Is battery storage linked to PV generation in credit requirements?
- Any "solar-ready" or "renewable-ready" infrastructure language

---

## Dimension 5 — Carbon + PV

**Hypothesis:** Carbon neutrality and net-zero carbon pathways implicitly require PV at
scale, even when PV is not mentioned explicitly.

**Search terms:**
- Primary: `net zero carbon`, `carbon neutral`, `operational carbon`, `carbon offset`,
  `greenhouse gas`, `Scope 1`, `Scope 2`, `carbon intensity`
- Co-occurring: `PV`, `solar`, `renewable`, `on-site generation`

**What to extract:**
- Does the carbon credit pathway implicitly require PV to achieve target?
- Is grid decarbonisation assumed (reducing PV's relative credit value over time)?
- Are avoided emissions from on-site PV generation counted in the carbon balance?
- Net-zero pathway language that implies PV integration

---

## Dimension 6 — Site / Urban + Solar

**Hypothesis:** Site assessment, orientation, massing, and solar access credits shape
early design decisions that determine BIPV feasibility — but are rarely connected to PV
explicitly.

**Search terms:**
- Primary: `orientation`, `massing`, `solar potential`, `site assessment`, `solar access`,
  `passive solar`, `solar rights`, `overshadowing`, `sky view factor`
- (No co-occurring PV term required — solar access IS the PV prerequisite)

**What to extract:**
- Do site/orientation credits explicitly state they enable future PV?
- Is solar access protection mentioned (protecting neighbour's PV potential)?
- Any solar envelope or solar rights language
- "Solar-ready design" or "PV-ready" infrastructure mentions

---

## Output Format

### gbrs_extraction_extended.csv columns

| Column | Description |
|--------|-------------|
| GBRS | System name |
| Version | Manual version |
| Dimension | One of D-ENV, D-DAY, D-LCA, D-EV, D-CARBON, D-SITE |
| Credit_ID | Credit or section identifier |
| Credit_Name | Full credit name |
| Category | Category within the system |
| PV_Relevance | Direct / Enabling / Conflicting / Neutral |
| Verbatim_Text | Exact quote from manual (max 300 chars) |
| Page_Ref | Page number(s) |
| Implication | Analysis note for Discussion section |
| Data_Quality | verified / partial / inferred |

### Priority systems for deep scan
Focus effort on systems most likely to have rich indirect references:
1. **DGNB** — LCA methodology covers PV as building component
2. **BREEAM** — extensive envelope, daylighting, and materials credits
3. **LEED** — Materials & Resources, Indoor Environmental Quality
4. **Green Mark** — ETTV/RETV envelope formula; EV credits; integrated design
5. **LBC** — Materials Petal, Place Petal (solar access)
6. **Passive House** — PHPP integrates PV with envelope; cool colour criterion
7. **Green Star** — Design & As Built has strong materials and IEQ sections
8. **BEAM Plus** — Hong Kong high-rise context; EV, daylight, and materials credits

---

*Created: April 2026 — for use in Round 2 manual scan*
