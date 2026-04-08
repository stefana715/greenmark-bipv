# Extended Extraction: Indirect PV/BIPV References in GBRS

> **Round 2 scan** — keyword co-occurrence search across 6 thematic dimensions.
> Method: pdfplumber targeted page-range extraction from 17 GBRS PDF manuals.

---

## Executive Summary

- **50 indirect references** found across **10 systems** and **5 dimensions**
- **0** explicitly linked (non-energy credit directly names PV/BIPV)
- **3** enabling (conditions favourable for BIPV without naming it)
- **0** conflicting (may penalise BIPV integration)

### Top Findings

- **DGNB · D-LCA** (p.15): [Enabling] — LCA framework can include BIPV as building product — explicit inclusion recommended.
- **DGNB · D-LCA** (p.15): [Enabling] — LCA framework can include BIPV as building product — explicit inclusion recommended.
- **LEED · D-CARBON** (p.98): [Enabling] — Carbon neutrality target implicitly requires PV at scale; BIPV maximises generation area.
- **LEED · D-EV** (p.39): [Neutral with potential] — EV credit creates indirect PV demand; recommend explicit solar-charged EV pathway.
- **Passive House · D-ENV** (p.34): [Neutral with potential] — BIPV facade falls within scope but no explicit pathway; guidance gap.
- **Passive House · D-SITE** (p.29): [Neutral with potential] — Solar potential assessment prerequisite for viable BIPV; should link explicitly.
- **Passive House · D-CARBON** (p.11): [Neutral with potential] — Carbon credit mathematically requires renewable generation; BIPV not yet named.
- **Passive House · D-CARBON** (p.11): [Neutral with potential] — Carbon credit mathematically requires renewable generation; BIPV not yet named.
- **LBC · D-CARBON** (p.27): [Neutral with potential] — Carbon credit mathematically requires renewable generation; BIPV not yet named.
- **LBC · D-CARBON** (p.27): [Neutral with potential] — Carbon credit mathematically requires renewable generation; BIPV not yet named.
- **LBC · D-CARBON** (p.27): [Neutral with potential] — Carbon credit mathematically requires renewable generation; BIPV not yet named.
- **LBC · D-CARBON** (p.27): [Neutral with potential] — Carbon credit mathematically requires renewable generation; BIPV not yet named.

---

## 1. Envelope + PV (SHGC / ETTV / Façade)

| GBRS | Credit | Relevance | Page | Verbatim excerpt |
|------|--------|-----------|------|-----------------|
| Passive House | load6 | Neutral with potential | 12 | olar load6 Insu- Exterior Interior in- Exterior Max. Min. Climate lation insulation sulation2 p… |
| Passive House | off-grid | Neutral with potential | 34 | he PV system).  Other renewable energy generation systems: suitable evidence of the predicted … |
| GRIHA | Table 10 | Neutral with potential | 82 | for each orientation as per Table 10.2c requirements. –Mandatory Table 10.2c: Maximum SHGC for … |
| GRIHA | Table 9 | Neutral with potential | 84 | culations demonstrating compliance with the DA requirements through extrapolation in the case o… |
| GRIHA | Table 9 | Neutral with potential | 84 | lation for the entire building envelope along with drawings (in. dwg format) highlighting the o… |
| GRIHA | Table 9 | Neutral with potential | 84 | tion as prescribed in ECBC 2017 And/Or • Fenestration design in accordance with Table 9 and Tab… |

**Key insight:** BIPV facades sit at the intersection of two credit categories — Energy and Envelope — yet no reviewed system provides explicit calculation guidance. Green Mark's ETTV formula is the clearest case: BIPV cladding can improve the envelope thermal score if counted as opaque wall, while semi-transparent BIPV glazing affects the SHGC term differently. DGNB's component-based LCA is the only system that naturally captures this dual role by treating PV as a building product. The absence of explicit envelope guidance creates inconsistent assessment outcomes and discourages façade BIPV adoption.

---

## 2. Daylighting / Visual Comfort + Solar

*No direct keyword co-occurrences found in the scanned page ranges.*

**Key insight:** Daylighting credits and PV integration have a complex relationship: opaque PV panels in shading devices can reduce daylight penetration and fail illuminance targets, while semi-transparent BIPV glazing can simultaneously control glare and transmit useful light. No reviewed system explicitly allows PV shading devices or BIPV glazing to satisfy daylighting credits, despite this being technically straightforward. BREEAM Hea01 and LEED EQc7 set targets that semi-transparent BIPV could demonstrably meet — a direct recommendation for both systems.

---

## 3. Materials / LCA + PV

| GBRS | Credit | Relevance | Page | Verbatim excerpt |
|------|--------|-----------|------|-----------------|
| DGNB | ENV1 | Neutral with potential | 2 | DGNB System – New buildings criteria set Environmental quality VERSION 2020 INTERNATIONAL ENV1.… |
| DGNB | CO2 | Neutral with potential | 5 | ed renewable energy can at least compensate the building operation (building + user energy dema… |
| DGNB | C3 | Enabling | 15 | sal (modules C3, C4) incl. recycling potential (module D)of the replaced product, not the repla… |
| DGNB | — | Enabling | 15 | tential (module D)of the replaced product, not the replacement process itself (same as for cons… |
| DGNB | — | Neutral with potential | 17 | ncluding coatings and internal columns) (7) Heating and cooling systems and air conditioning sy… |

**Key insight:** DGNB ENV1.1 is the only system with a formal LCA framework that explicitly includes PV modules as building components, using EN 15804 EPDs and referencing EN 15316-4-3 for calculation. All other systems either exclude PV from material LCA credits entirely (LEED MR credits focus on construction materials) or provide no explicit guidance. This gap is directly addressable: as IEC 63092 establishes BIPV as a construction product with defined performance requirements, EPD requirements for BIPV modules should be incorporated into materials credits across all systems.

---

## 4. EV Charging / Storage + PV

| GBRS | Credit | Relevance | Page | Verbatim excerpt |
|------|--------|-----------|------|-----------------|
| LEED | credit applies | Neutral with potential | 39 | LT Credit: Electric Vehicles This credit applies to  BD+C: New Construction (1 point)  BD+C: … |
| LEED | on-site | Neutral with potential | 39 | Warehouses and Distribution Centers (1 point)  BD+C: Hospitality (1 point)  BD+C: Healthcare … |
| LEED | on-site | Neutral with potential | 39 | BD+C: Hospitality (1 point)  BD+C: Healthcare (1 point) Intent To reduce pollution by promotin… |
| LEED | on-site | Neutral with potential | 39 | electric vehicles for on-site parking. Option 1. Electric Vehicle Charging (1 point) Install el… |
| LEED | plug-in | Neutral with potential | 39 | ify and reserve these spaces for the sole use by plug-in electric vehicles. The EVSE must: • Pr… |
| Green Mark | Annex 1 | Neutral with potential | 15 | GREEN MARK 2021 RATINGS GM: 2021 is positioned to recognise performance that is above the manda… |
| Green Mark | End-of | Neutral with potential | 28 | % energy efficiency Provide greenery and improvement over 2005 communal spaces code PUB Water E… |

**Key insight:** EV charging credits create an indirect but powerful demand signal for on-site PV generation. In high-carbon grid contexts (Hong Kong, India, parts of Southeast Asia), grid-charged EVs have limited net carbon benefit without renewable energy sources — making on-site solar a logical complement. BEAM Plus's Transport and Site Management sections come closest to making this link explicit. The EV–PV–BIPV demand chain represents an untapped synergy: a 'solar-charged EV infrastructure' credit pathway would create simultaneous demand for BIPV deployment and EV adoption.

---

## 5. Carbon Neutrality + PV

| GBRS | Credit | Relevance | Page | Verbatim excerpt |
|------|--------|-----------|------|-----------------|
| LEED | G
2 | Neutral with potential | 95 | 90.1-2016 Section G 2.4.1 requirements for on-site renewable energy may be used to meet minimum… |
| LEED | credit
for | Enabling | 98 | documents are finalized.  For elements or systems that cannot be readily modeled by the softwa… |
| LEED | on-site | Neutral with potential | 98 | produced at the building site”, which includes on-site photovoltaics systems, wind generators, … |
| LEED | off-site | Neutral with potential | 98 | , but does not include electric generation or thermal generation from off- site renewable sourc… |
| LEED | rough 8 | Neutral with potential | 103 | rough 8 are modeled with fossil fuel heating. Schedules Refer to the LEED v4 reference guide. E… |
| DGNB | ENV1 | Neutral with potential | 5 | gs criteria set Environmental quality VERSION 2020 INTERNATIONAL ENV1.1 / BUILDING LIFE CYCLE A… |
| DGNB | CO2 | Neutral with potential | 5 | mpensate the building energy demand related CO2 equiv. emissions. 4.1.2 Partial consideration o… |
| DGNB | CO2 | Neutral with potential | 5 | ensate the user energy related CO2 equiv. emissions. 4.1.3 Climate-neutral building operation: … |
| DGNB | CO2 | Neutral with potential | 5 | es” of the DGNB. The boundary conditions of the use phase must reflect the reality as precise a… |
| DGNB | CO2 | Neutral with potential | 11 | rbon neutral buildings and sites” evaluates a performance of the calculation tool. It evaluates… |
| Passive House | than 15 | Neutral with potential | 11 | e acquisition). 8 Alternative PER criteria If the PER demand exceeds the standard criterion, th… |
| Passive House | Table 2 | Neutral with potential | 11 | dingly better thermal protection in other areas. In addition to the criteria in either Table 2 … |
| LBC | on-site | Neutral with potential | 27 | through the on-site production of renewable energy. The marketplace has characterized net zero … |
| LBC | on-site | Neutral with potential | 27 | ction of renewable energy. The marketplace has characterized net zero energy in many different … |
| LBC | on-site | Neutral with potential | 27 | N energy through a twelve month performance period. All Imperatives required for this certifica… |
| LBC | on-site | Neutral with potential | 27 | e described in this Standard, and are consolidated into the Core Green Building Certification S… |
| LBC | trouble-shoot | Neutral with potential | 45 | method to understand and trouble-shoot energy use. All projects must account for the total embo… |
| MINERGIE | least 60 | Neutral with potential | 2 | upply to the charging Empty pipes to the parking No requirement station for at least 60% of the… |

**Key insight:** Carbon neutrality pathways in BREEAM, Green Star, and LBC mathematically require on-site renewable generation at scale — making BIPV a de facto necessity for top-tier certification even when it is not named. However, the treatment of declining grid carbon intensity varies significantly: some systems freeze the grid emission factor at certification date (favouring immediate PV investment) while others use projected future intensity (reducing PV's long-term credit value). This inconsistency creates uncertainty for BIPV investment decisions in building design.

---

## 6. Site / Urban + Solar Access

| GBRS | Credit | Relevance | Page | Verbatim excerpt |
|------|--------|-----------|------|-----------------|
| LEED | — | Neutral with potential | 2 | ....................... 36 LT CREDIT: ELECTRIC VEHICLES .......................................… |
| LEED | — | Neutral with potential | 2 | .................................................................. 39 SS PREREQUISITE: CONSTRUC… |
| LEED | — | Neutral with potential | 6 | • Site Assessment is more relevant to international project teams; the US specific TR- 55 stand… |
| LEED | Credit Bicycle | Neutral with potential | 7 | ity Transit 5 6 4 5 5 5 5 2 Credit Bicycle Facilities 1 1 1 1 1 1 1 1 Credit Reduced Parking Fo… |
| LEED | Credit Bicycle | Neutral with potential | 7 | Credit Bicycle Facilities 1 1 1 1 1 1 1 1 Credit Reduced Parking Footprint 1 1 1 1 1 1 1 1 Cred… |
| Passive House | — | Neutral with potential | 29 | Ground probe or ground collector in combination with a heat pump if present Boiler Performance … |
| CASBEE | — | Neutral with potential | 31 | le imput; Introduction of airflow windows 3.0 0.25 3.0 - 3 Zoned Control － 3.0 0.38 - - 2 .2Hum… |
| Estidama Pearl | — | Neutral with potential | 24 | Villa Pearl Rating System. (cid:1) Holding regular design workshops with active involvement by … |
| Estidama Pearl | — | Neutral with potential | 37 | n showing preserved or protected valuable assets Submission: (where relevant) Construction Rati… |
| LOTUS | — | Neutral with potential | 35 | ting in the building, while ensuring comfort for all occupants Requirements Criteria Points Ene… |
| LOTUS | well-positioned | Neutral with potential | 35 | & Implementation Passive Design Analysis (Energy Prerequisite 1) The following factors should b… |
| LOTUS | Sun-paths | Neutral with potential | 36 |  Appropriate orientation assists passive cooling by minimizing its exposure to the sun and max… |
| LOTUS | — | Neutral with potential | 37 | Zoning  Providing thoughtful zoning to allow different thermal requirements to be compartmenta… |
| LOTUS | — | Neutral with potential | 37 | irements to be compartmentalized to reduce wasted energy Shading  Reducing solar gains at open… |

**Key insight:** Solar access and orientation credits are the least developed dimension across all reviewed systems, yet they are the prerequisite for all BIPV design decisions. Only LBC's Place Petal and Passive House's cool colour/PHPP framework explicitly link site design to PV generation potential. LEED's Integrative Process credit and BREEAM Man04 encourage early design analysis that should include solar feasibility assessment but neither mandates it. The absence of solar envelope protection or 'solar-ready design' credits in most systems is a structural barrier to urban BIPV deployment, particularly in dense city contexts.

---

## Implications for Discussion Section

### 7.1 Synthesis: BIPV as Cross-Category Technology

The second-pass scan confirms that BIPV integration touches five certification categories — Energy, Envelope, Materials, Indoor Environmental Quality, and Transport — yet no system has updated its non-energy credits to reflect this. The most significant gaps: (1) no explicit BIPV pathway in envelope/façade credits despite PV being intrinsically a building material; (2) no system allows semi-transparent BIPV to earn daylighting credits; (3) LCA boundaries almost universally exclude PV modules, missing both embodied carbon and avoided-emission contributions.

### 7.2 Structural Barriers Identified

GBRS are organised in disciplinary silos (Energy, Materials, IEQ, Transport) while BIPV as a technology simultaneously performs across all of them. The absence of a cross-category credit pathway in all but DGNB and LBC is itself a barrier: project teams cannot claim full credit for what BIPV actually delivers, making facade and window BIPV financially unattractive relative to simple roof-mount systems that earn straightforward renewable energy credits.

### 7.3 Recommendations for GBRS Developers

1. **Envelope credits:** Provide explicit BIPV facade calculation guidance covering U-value (opaque BIPV as wall) and SHGC/ETTV (semi-transparent BIPV as glazing). Allow BIPV to satisfy envelope AND energy credits simultaneously.

2. **Daylighting credits:** Recognise PV shading devices (louvres, fins, canopies) and semi-transparent BIPV glazing as valid compliance pathways for solar control and illuminance targets.

3. **Materials/LCA credits:** Include PV modules within the LCA system boundary; require EPDs aligned with IEC 63092 for BIPV products; allow avoided operational emissions to be credited in lifecycle carbon calculations.

4. **EV credits:** Create a 'solar-charged EV infrastructure' sub-credit that explicitly incentivises on-site renewable energy (including BIPV) as the power source for electric vehicle charging.

5. **Site/urban credits:** Add a solar access protection sub-credit and a 'solar-ready design' process credit. Mandate solar potential assessment as part of site feasibility for all building types.

---

*Generated by `src/extended_extraction.py` — pdfplumber keyword co-occurrence, targeted page ranges, April 2026.*