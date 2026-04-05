# PRISMA Search Strategy: BIPV × GBRS Meta-Review

## Database: Scopus

### Search String
```
TITLE-ABS-KEY(
  ("BIPV" OR "building integrated photovoltaic*" OR "building-integrated photovoltaic*" 
   OR "photovoltaic facade" OR "PV facade" OR "solar facade" OR "PV window" 
   OR "semi-transparent photovoltaic" OR "semitransparent PV")
  AND
  ("green building" OR "rating system" OR "certification" OR "assessment system"
   OR "LEED" OR "BREEAM" OR "Green Mark" OR "Green Star" OR "CASBEE" 
   OR "DGNB" OR "BEAM Plus" OR "ASGB" OR "net zero energy building"
   OR "zero energy building" OR "sustainable building")
)
AND PUBYEAR > 2009 AND PUBYEAR < 2026
AND DOCTYPE(ar OR re)
AND LANGUAGE(english)
```

### Alternative broader search (if too few results)
```
TITLE-ABS-KEY(
  ("photovoltaic" OR "solar panel" OR "solar energy" OR "renewable energy")
  AND
  ("building" OR "facade" OR "envelope" OR "roof")
  AND
  ("green building rating" OR "LEED" OR "BREEAM" OR "Green Mark" 
   OR "certification" OR "rating system")
)
AND PUBYEAR > 2009 AND PUBYEAR < 2026
AND DOCTYPE(ar OR re)
```

## Database: Web of Science

### Search String
```
TS=("BIPV" OR "building integrated photovoltaic*" OR "building-integrated photovoltaic*")
AND
TS=("green building" OR "rating system" OR "LEED" OR "BREEAM" OR "Green Mark" 
    OR "Green Star" OR "CASBEE" OR "DGNB" OR "certification")

Timespan: 2010–2025
Document types: Article, Review
Language: English
```

## Inclusion Criteria
1. Peer-reviewed journal article or review (not conference paper only)
2. English language
3. Published 2010–2025
4. Discusses PV or BIPV in the context of green building assessment/rating
5. Provides analysis, comparison, or data on PV/BIPV criteria in GBRS

## Exclusion Criteria
1. Pure PV technology paper with no GBRS discussion
2. Pure GBRS comparison with no PV/renewable energy focus
3. Conference abstracts without full paper
4. Non-English
5. Duplicate entries across databases

## Data Extraction Fields
For each included paper:
- Authors, Year, Journal
- GBRS studied (which systems)
- BIPV type discussed (roof/facade/window/shading)
- Method used (review/case study/simulation/survey)
- Key findings related to PV criteria in GBRS
- Country/region focus

## Export Instructions
### Scopus
1. Run search → Select all results
2. Export → CSV format
3. Select: Citation info, Bibliographical info, Abstract, Keywords, Affiliations
4. Save as `data/raw/scopus_export.csv`

### Web of Science
1. Run search → Export
2. Format: Tab-delimited (or BibTeX)  
3. Record content: Full Record + Cited References
4. Save as `data/raw/wos_export.txt`
