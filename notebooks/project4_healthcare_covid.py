# Project 4 - India COVID-19 Trends Analysis
# Domain: Healthcare
# Dataset: covid_trends.csv
# Source: Based on Our World in Data / MoHFW India national published figures
# Covers: 2021-01-01 to 2022-12-31 (730 days)
# Run this file from the data_portfolio/ folder

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

print("=" * 50)
print("Project 4 - India COVID-19 Trends Analysis")
print("=" * 50)

df = pd.read_csv("data/covid_trends.csv")
print("\nDataset shape:", df.shape)
print("\nColumn names:", df.columns.tolist())
print("\nFirst 5 rows:")
print(df.head())
print("\nMissing values:")
print(df.isnull().sum())
print("\nBasic statistics:")
print(df.describe())

df = df.drop_duplicates()
df["Date"] = pd.to_datetime(df["Date"])
df["Month"] = df["Date"].dt.to_period("M").astype(str)
df["Year"]  = df["Date"].dt.year

total_cases     = df["DailyCases"].sum()
total_deaths    = df["Deaths"].sum()
total_recovered = df["Recovered"].sum()
cfr             = total_deaths / total_cases * 100
rr              = total_recovered / df["DailyCases"].iloc[14:].sum() * 100
max_vax_pct     = df["Vax_pct"].max()
peak_cases      = df["DailyCases"].max()
peak_date       = df.loc[df["DailyCases"].idxmax(), "Date"].strftime("%Y-%m-%d")

print("\n--- Key Numbers ---")
print(f"Total Cases      : {total_cases:,.0f}")
print(f"Total Deaths     : {total_deaths:,.0f}")
print(f"Case Fatality %  : {cfr:.2f}%")
print(f"Peak Daily Cases : {peak_cases:,} on {peak_date}")
print(f"Max Vax Coverage : {max_vax_pct:.1f}%")

roll7  = df.set_index("Date")["DailyCases"].rolling(7).mean()
roll7d = df.set_index("Date")["Deaths"].rolling(7).mean()

plt.figure(figsize=(13, 5))
plt.fill_between(roll7.index, roll7.values, alpha=0.2, color="tomato")
plt.plot(roll7.index, roll7.values, color="tomato", linewidth=2, label="Daily Cases (7-day avg)")
ax2 = plt.gca().twinx()
ax2.plot(roll7d.index, roll7d.values, color="black", linewidth=1.5,
         linestyle="--", label="Deaths (7-day avg)")
ax2.set_ylabel("Daily Deaths")
lines1, labels1 = plt.gca().get_legend_handles_labels()
lines2, labels2 = ax2.get_legend_handles_labels()
plt.gca().legend(lines1 + lines2, labels1 + labels2, loc="upper right")
plt.title("India COVID-19 Daily Cases and Deaths - 7 Day Rolling Average", fontsize=14)
plt.gca().set_xlabel("Date")
plt.gca().set_ylabel("Daily Cases")
plt.xticks(rotation=30)
plt.tight_layout()
plt.savefig("visualizations/project4/1_national_cases_deaths.png", dpi=150, bbox_inches="tight")
plt.close()
print("\nSaved chart 1")

plt.figure(figsize=(12, 5))
plt.plot(df["Date"], df["Vax_pct"], color="steelblue", linewidth=2)
plt.axhline(70, color="darkgreen", linestyle="--", alpha=0.7, label="70% target")
plt.fill_between(df["Date"], df["Vax_pct"], alpha=0.15, color="steelblue")
plt.title("India Vaccination Coverage Progress (%)", fontsize=14)
plt.xlabel("Date"); plt.ylabel("Population Vaccinated (%)")
plt.legend(); plt.xticks(rotation=30)
plt.tight_layout()
plt.savefig("visualizations/project4/2_vaccination_progress.png", dpi=150, bbox_inches="tight")
plt.close()
print("Saved chart 2")

monthly = df.groupby("Month").agg(
    TotalCases=("DailyCases","sum"), TotalDeaths=("Deaths","sum")).reset_index()
monthly["CFR"] = (monthly["TotalDeaths"] / monthly["TotalCases"] * 100).round(2)

fig, axes = plt.subplots(2, 1, figsize=(13, 8))
axes[0].bar(range(len(monthly)), monthly["TotalCases"] / 1000,
            color=["tomato" if m >= "2022" else "steelblue" for m in monthly["Month"]])
axes[0].set_title("Monthly COVID-19 Cases (thousands)", fontsize=12)
axes[0].set_ylabel("Cases (thousands)")
axes[0].set_xticks(range(len(monthly)))
axes[0].set_xticklabels(monthly["Month"], rotation=45, ha="right", fontsize=7)

axes[1].bar(range(len(monthly)), monthly["CFR"],
            color=["coral" if v > 1 else "seagreen" for v in monthly["CFR"]])
axes[1].set_title("Monthly Case Fatality Rate (%)", fontsize=12)
axes[1].set_ylabel("CFR (%)")
axes[1].set_xticks(range(len(monthly)))
axes[1].set_xticklabels(monthly["Month"], rotation=45, ha="right", fontsize=7)
plt.suptitle("Monthly Case and Mortality Analysis", fontsize=14, fontweight="bold")
plt.tight_layout()
plt.savefig("visualizations/project4/3_monthly_analysis.png", dpi=150, bbox_inches="tight")
plt.close()
print("Saved chart 3")

roll30_cases = df.set_index("Date")["DailyCases"].rolling(30).mean()
roll30_vax   = df.set_index("Date")["Vax_pct"]

fig, ax1 = plt.subplots(figsize=(13, 5))
ax1.plot(roll30_cases.index, roll30_cases.values, color="tomato", linewidth=2, label="Cases (30-day avg)")
ax1.set_ylabel("Daily Cases (30-day avg)", color="tomato")
ax2 = ax1.twinx()
ax2.plot(roll30_vax.index, roll30_vax.values, color="steelblue", linewidth=2, label="Vax %")
ax2.set_ylabel("Vaccination Coverage (%)", color="steelblue")
lines1, labels1 = ax1.get_legend_handles_labels()
lines2, labels2 = ax2.get_legend_handles_labels()
ax1.legend(lines1 + lines2, labels1 + labels2, loc="upper left")
ax1.set_title("Vaccination Coverage vs Daily Cases", fontsize=14)
ax1.set_xlabel("Date")
plt.xticks(rotation=30)
plt.tight_layout()
plt.savefig("visualizations/project4/4_vax_vs_cases.png", dpi=150, bbox_inches="tight")
plt.close()
print("Saved chart 4")

plt.figure(figsize=(10, 6))
sns.heatmap(
    df[["DailyCases","Deaths","Recovered","Vax_pct"]].corr(),
    annot=True, fmt=".2f", cmap="RdYlGn", center=0, linewidths=0.5)
plt.title("Correlation: Cases, Deaths, Recovery and Vaccination", fontsize=13)
plt.tight_layout()
plt.savefig("visualizations/project4/5_correlation.png", dpi=150, bbox_inches="tight")
plt.close()
print("Saved chart 5")

wave1_cases = df[df["Date"] < "2021-07-01"]["DailyCases"].sum()
wave2_cases = df[(df["Date"] >= "2021-10-01") & (df["Date"] < "2022-04-01")]["DailyCases"].sum()

print("\n--- Insights ---")
print(f"1. Wave 2 (Delta) peak   : {peak_cases:,} daily cases on {peak_date}")
print(f"2. Total cases 2021-2022 : {total_cases:,.0f}")
print(f"3. Case fatality rate    : {cfr:.2f}%")
print(f"4. Max vaccination cover : {max_vax_pct:.1f}% of population")
print(f"5. Wave 2 total cases    : {wave1_cases:,.0f}")
print(f"6. Wave 3 total cases    : {wave2_cases:,.0f}")

print("\n--- Recommendations ---")
print("1. Accelerate vaccination to close the gap toward 70% herd immunity.")
print("2. Build more ICU capacity before projected future waves.")
print("3. Deploy real-time dashboards for early wave detection.")
print("4. Invest in booster dose programmes for high-risk groups.")
print("5. Integrate vaccination records with case data for richer analysis.")

print("\nProject 4 complete!")
