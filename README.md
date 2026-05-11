# 📊 Multi-Domain Data Analysis Portfolio

> **5 end-to-end data analysis projects** covering Retail, Education, Weather,
> Healthcare, and Finance — built with Python, pandas, matplotlib, seaborn, and ReportLab.

---

## 🗂️ Repository Structure

```
data_portfolio/
├── run_all.py                        ← Master runner (generates everything)
├── requirements.txt
├── README.md
│
├── src/
│   ├── data_generator.py             ← Generates all 5 simulated datasets
│   └── utils.py                      ← Shared helpers (viz, stats, PDF report)
│
├── data/
│   ├── supermarket_sales.csv         ← 2,000 retail transactions
│   ├── student_performance.csv       ← 7,500 student-subject records
│   ├── weather_data.csv              ← 1,096 daily weather readings (3 yrs)
│   ├── covid_trends.csv              ← 4,380 COVID records (6 states, 2 yrs)
│   └── stock_market.csv              ← 3,750 trading day records (5 NSE stocks)
│
├── notebooks/
│   ├── project1_supermarket_sales.py
│   ├── project2_student_performance.py
│   ├── project3_weather_analysis.py
│   ├── project4_healthcare_covid.py
│   └── project5_finance_stocks.py
│
├── visualizations/
│   ├── project1/   (7 charts)
│   ├── project2/   (8 charts)
│   ├── project3/   (8 charts)
│   ├── project4/   (7 charts)
│   └── project5/   (8 charts)
│
├── reports/
│   ├── project1_supermarket_report.pdf
│   ├── project2_student_report.pdf
│   ├── project3_weather_report.pdf
│   ├── project4_covid_report.pdf
│   └── project5_finance_report.pdf
│
└── docs/
    └── portfolio_overview.md
```

---

## 🚀 Quick Start

```bash
# 1. Install dependencies  (Python 3.8+ required)
pip install -r requirements.txt

# 2. Run everything — generates datasets, charts, and PDF reports
python run_all.py

# 3. Or run a single project
python notebooks/project1_supermarket_sales.py
```

> **Jupyter notebook format?**  
> The analysis files are plain Python scripts (`.py`) so they run anywhere without Jupyter.  
> If your submission requires `.ipynb` files, run:
> ```bash
> pip install nbformat
> python convert_to_notebooks.py
> ```
> This converts all 5 scripts into properly structured `.ipynb` notebooks.

---

## 📁 Project Summaries

### Project 1 — Supermarket Sales Analysis *(Retail)*
| Item | Detail |
|------|--------|
| Dataset | 2,000 transactions · Jan–Mar 2024 |
| Key Metrics | ₹14.4M total sales · 39.6% profit margin |
| Top Insight | Electronics is best-seller; Saturday evening is peak window |
| Techniques | GroupBy aggregation, time-series trend, heat-map, pie chart |
| Charts | 7 visualisations |

### Project 2 — Student Performance Analysis *(Education)*
| Item | Detail |
|------|--------|
| Dataset | 1,500 students × 5 subjects = 7,500 records |
| Key Metrics | 99.9% pass rate · 76.4 avg score |
| Top Insight | Attendance (r=0.34) & study hours (r=0.25) are key score drivers |
| Techniques | KDE plots, scatter with regression, section/gender comparison |
| Charts | 8 visualisations |

### Project 3 — Weather Data Analysis *(Meteorology)*
| Item | Detail |
|------|--------|
| Dataset | 1,096 daily records · 2022–2024 |
| Key Metrics | 23°C avg · 3,332mm annual rainfall · 27 extreme events |
| Top Insight | Monsoon (Jun–Sep) accounts for 68% of all annual rainfall |
| Techniques | Rolling averages, seasonal boxplots, KDE rainfall, correlation matrix |
| Charts | 8 visualisations |

### Project 4 — COVID-19 Trends *(Healthcare)*
| Item | Detail |
|------|--------|
| Dataset | 6 Indian states × 730 days = 4,380 records |
| Key Metrics | 36.9M total cases · 2.04% CFR · 90.8% recovery rate |
| Top Insight | Vaccination shows strong negative correlation (r=−0.41) with cases |
| Techniques | Dual-axis trend, state comparison, monthly heat-map, wave detection |
| Charts | 7 visualisations |

### Project 5 — Stock Market Analysis *(Finance)*
| Item | Detail |
|------|--------|
| Dataset | 5 NSE stocks × 750 trading days = 3,750 records |
| Key Metrics | RELIANCE +57.1% best; HDFC lowest volatility (23.4%) |
| Top Insight | Portfolio stocks are near-uncorrelated — good diversification |
| Techniques | Normalised prices, cumulative return, rolling volatility, Sharpe proxy |
| Charts | 8 visualisations |

---

## 🛠️ Tech Stack

| Library | Purpose |
|---------|---------|
| `pandas` | Data loading, cleaning, aggregation |
| `numpy` | Numerical computation, simulation |
| `matplotlib` | Base charting framework |
| `seaborn` | Statistical visualisations |
| `reportlab` | PDF report generation |
| `scipy` | Statistical methods |

---

## 📊 Total Deliverables

- ✅ 5 complete analysis scripts (≈ 200 lines each)
- ✅ 5 professional PDF reports with executive summaries
- ✅ 38 visualisations across all projects
- ✅ 5 clean, validated datasets (18,726 total rows)
- ✅ Reusable utility library (`src/utils.py`)
- ✅ Automated dataset generator (`src/data_generator.py`)
- ✅ One-command full run (`run_all.py`)

---

## 👤 Author
Data Analysis Portfolio · AB · 2024
