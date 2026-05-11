# Portfolio Overview — Multi-Domain Data Analysis

## Objective
Build a professional data analysis portfolio demonstrating end-to-end skills across
five real-world domains: **data ingestion → cleaning → analysis → visualisation → business reporting**.

---

## Methodology (applied consistently across all 5 projects)

### Step 1 — Data Loading & Exploration
- Load CSV with `pandas.read_csv()`
- Print shape, dtypes, missing value counts, and descriptive statistics
- Identify data quality issues before any analysis

### Step 2 — Validation & Cleaning
- Check all required columns are present (`validate_data`)
- Drop exact duplicates and all-null rows (`clean_dataframe`)
- Parse date columns, engineer derived features (Month, Season, Week, etc.)

### Step 3 — Statistical Analysis
- Compute summary statistics: mean, median, std, quartiles
- Calculate domain KPIs (pass rate, profit margin, CFR, Sharpe ratio, etc.)
- Generate correlation matrices to identify variable relationships

### Step 4 — Visualisation (3–8 charts per project)
Each chart answers a specific business question:

| Chart Type | Question Answered |
|---|---|
| Line / area chart | How does X change over time? |
| Bar chart | Which category performs best? |
| Pie / donut chart | What is the composition? |
| Heat-map | Where are the intensity hot-spots? |
| Scatter plot | Is there a relationship between X and Y? |
| Box plot | How does distribution differ across groups? |
| KDE / histogram | What is the shape of this distribution? |
| Correlation matrix | How are all variables inter-related? |

### Step 5 — Insight Generation
- Identify top/bottom performers
- Quantify key correlations with exact values
- Surface anomalies and at-risk entities

### Step 6 — Recommendations
- Translate each insight into a concrete, actionable recommendation
- Prioritise by impact and feasibility

### Step 7 — PDF Report
- Auto-generate a professional A4 PDF with KPI tables, charts, and narrative
- Suitable for stakeholder presentation

---

## Data Quality Standards
- Zero tolerance for undocumented null handling
- All cleaning steps logged with before/after row counts
- Validation gate runs before every analysis block
- Simulated datasets use fixed random seeds for reproducibility

---

## Key Skills Demonstrated

| Skill | Where Used |
|---|---|
| `groupby` + `agg` | All projects — category/state/ticker aggregations |
| Rolling windows | Project 1 (daily sales), 3 (temp trend), 5 (MA, volatility) |
| Multi-index pivot | Projects 4 & 5 — heat-maps and return matrices |
| Correlation analysis | All projects — final correlation matrix + heatmap |
| KDE & histogram | Projects 2, 3, 5 — distribution analysis |
| Dual-axis plots | Project 4 — cases + deaths on same chart |
| Log-return simulation | Project 5 — geometric Brownian motion for stock prices |
| Wave analysis | Project 4 — Gaussian wave modelling for COVID peaks |
| Reusable functions | `src/utils.py` — shared across all 5 projects |
| Automated PDF | `PortfolioReport` class — section titles, KPI tables, images |

---

## Project Timeline (as per brief)

| Week | Project | Domain |
|---|---|---|
| 1 | Supermarket Sales Analysis | Retail |
| 2 | Student Performance Analysis | Education |
| 3 | Weather Data Analysis | Meteorology |
| 4 | COVID-19 Trends Analysis | Healthcare |
| 4 | Stock Market Analysis | Finance |
| 5–6 | Portfolio integration, README, PDF reports | — |
