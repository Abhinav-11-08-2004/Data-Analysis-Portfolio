# Project 3 - Weather Data Analysis
# Domain: Meteorology / Climate
# Run this file from the data_portfolio/ folder

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

print("=" * 50)
print("Project 3 - Weather Data Analysis")
print("=" * 50)

df = pd.read_csv("data/weather_data.csv")
print("\nDataset shape:", df.shape)
print("\nColumn names:", df.columns.tolist())
print("\nFirst 5 rows:")
print(df.head())
print("\nMissing values:")
print(df.isnull().sum())
print("\nBasic statistics:")
print(df.describe())

df = df.drop_duplicates()
print("\nRows after removing duplicates:", len(df))

df["Date"] = pd.to_datetime(df["Date"])
df["Year"] = df["Date"].dt.year

avg_temp     = df["TempAvg_C"].mean()
max_temp     = df["TempMax_C"].max()
min_temp     = df["TempMin_C"].min()
total_rain   = df["Rainfall_mm"].sum()
avg_humidity = df["Humidity_%"].mean()
extreme_days = df["Extreme"].sum()
total_days   = len(df)

print("\n--- Key Numbers ---")
print(f"Total Days      : {total_days}")
print(f"Avg Temperature : {avg_temp:.1f} °C")
print(f"Max Temperature : {max_temp:.1f} °C")
print(f"Min Temperature : {min_temp:.1f} °C")
print(f"Total Rainfall  : {total_rain:.0f} mm")
print(f"Avg Humidity    : {avg_humidity:.1f}%")
print(f"Extreme Days    : {extreme_days}")

month_names = {1:"Jan",2:"Feb",3:"Mar",4:"Apr",5:"May",6:"Jun",
               7:"Jul",8:"Aug",9:"Sep",10:"Oct",11:"Nov",12:"Dec"}

monthly_temp = df.groupby("Month")["TempAvg_C"].mean()
monthly_temp.index = [month_names[m] for m in monthly_temp.index]

monthly_rain = df.groupby("Month")["Rainfall_mm"].sum() / df["Year"].nunique()
monthly_rain.index = [month_names[m] for m in monthly_rain.index]

hottest_month = monthly_temp.idxmax()
wettest_month = monthly_rain.idxmax()

season_map = {
    1:"Winter", 2:"Winter", 3:"Spring", 4:"Spring",
    5:"Summer", 6:"Summer", 7:"Monsoon", 8:"Monsoon",
    9:"Monsoon", 10:"Autumn", 11:"Autumn", 12:"Winter"
}
df["SeasonCalc"] = df["Month"].map(season_map)

monsoon_rain = df[df["SeasonCalc"] == "Monsoon"]["Rainfall_mm"].sum()
monsoon_pct  = monsoon_rain / total_rain * 100

corr_cols   = ["TempMax_C","TempMin_C","TempAvg_C","Rainfall_mm","Humidity_%","WindSpeed_kmh"]
correlation = df[corr_cols].corr()
print("\n--- Correlation Matrix ---")
print(correlation.round(3))

df_sorted = df.sort_values("Date").set_index("Date")
rolling_avg = df_sorted["TempAvg_C"].rolling(30).mean()
rolling_max = df_sorted["TempMax_C"].rolling(30).mean()
rolling_min = df_sorted["TempMin_C"].rolling(30).mean()

plt.figure(figsize=(12, 5))
plt.plot(rolling_avg.index, rolling_avg.values, color="tomato", linewidth=2, label="Avg Temp")
plt.plot(rolling_max.index, rolling_max.values, color="orange", linewidth=1.2,
         linestyle="--", label="Max Temp")
plt.plot(rolling_min.index, rolling_min.values, color="steelblue", linewidth=1.2,
         linestyle="--", label="Min Temp")
plt.fill_between(rolling_min.index, rolling_min.values, rolling_max.values,
                 alpha=0.1, color="orange")
plt.title("Temperature Trend - 30 Day Rolling Average", fontsize=14)
plt.xlabel("Date")
plt.ylabel("Temperature (°C)")
plt.legend()
plt.xticks(rotation=30)
plt.tight_layout()
plt.savefig("visualizations/project3/1_temperature_trend.png", dpi=150, bbox_inches="tight")
plt.close()
print("\nSaved chart 1: temperature trend")

plt.figure(figsize=(10, 5))
plt.bar(monthly_rain.index, monthly_rain.values, color="steelblue")
plt.title("Average Monthly Rainfall (mm)", fontsize=14)
plt.xlabel("Month")
plt.ylabel("Rainfall (mm)")
for i, val in enumerate(monthly_rain.values):
    plt.text(i, val + 1, f"{val:.0f}", ha="center", fontsize=8)
plt.tight_layout()
plt.savefig("visualizations/project3/2_monthly_rainfall.png", dpi=150, bbox_inches="tight")
plt.close()
print("Saved chart 2: monthly rainfall")

season_order = ["Winter","Spring","Summer","Monsoon","Autumn"]
season_order = [s for s in season_order if s in df["SeasonCalc"].unique()]

fig, axes = plt.subplots(1, 2, figsize=(12, 5))
sns.boxplot(data=df, x="SeasonCalc", y="TempAvg_C", order=season_order,
            palette=["steelblue","seagreen","orange","coral","orchid"], ax=axes[0])
axes[0].set_title("Temperature by Season", fontsize=13)
axes[0].set_xlabel("Season")
axes[0].set_ylabel("Avg Temp (°C)")

sns.boxplot(data=df, x="SeasonCalc", y="Humidity_%", order=season_order,
            palette=["steelblue","seagreen","orange","coral","orchid"], ax=axes[1])
axes[1].set_title("Humidity by Season", fontsize=13)
axes[1].set_xlabel("Season")
axes[1].set_ylabel("Humidity (%)")

plt.suptitle("Seasonal Weather Patterns", fontsize=15, fontweight="bold")
plt.tight_layout()
plt.savefig("visualizations/project3/3_seasonal_patterns.png", dpi=150, bbox_inches="tight")
plt.close()
print("Saved chart 3: seasonal patterns")

rainy_days = df[df["Rainfall_mm"] > 0]["Rainfall_mm"]

plt.figure(figsize=(9, 5))
plt.hist(rainy_days, bins=30, color="steelblue", edgecolor="white")
plt.title("Rainfall Distribution (rainy days only)", fontsize=14)
plt.xlabel("Rainfall (mm)")
plt.ylabel("Number of Days")
plt.tight_layout()
plt.savefig("visualizations/project3/4_rainfall_distribution.png", dpi=150, bbox_inches="tight")
plt.close()
print("Saved chart 4: rainfall distribution")

extreme_by_month = df[df["Extreme"] == True].groupby("Month").size()
all_months_extreme = pd.Series(0, index=range(1, 13))
for month_num, count in extreme_by_month.items():
    all_months_extreme[month_num] = count
all_months_extreme.index = list(month_names.values())

plt.figure(figsize=(10, 5))
plt.bar(all_months_extreme.index, all_months_extreme.values, color="tomato")
plt.title("Extreme Weather Events by Month (2022-2024)", fontsize=14)
plt.xlabel("Month")
plt.ylabel("Number of Events")
plt.tight_layout()
plt.savefig("visualizations/project3/5_extreme_events.png", dpi=150, bbox_inches="tight")
plt.close()
print("Saved chart 5: extreme events by month")

yoy_temp = df.groupby("Year")["TempAvg_C"].mean()

plt.figure(figsize=(7, 5))
plt.bar(yoy_temp.index.astype(str), yoy_temp.values, color="orange")
plt.title("Year over Year Average Temperature", fontsize=14)
plt.xlabel("Year")
plt.ylabel("Avg Temperature (°C)")
for i, val in enumerate(yoy_temp.values):
    plt.text(i, val + 0.1, f"{val:.1f}°C", ha="center", fontsize=11)
plt.tight_layout()
plt.savefig("visualizations/project3/6_yoy_temperature.png", dpi=150, bbox_inches="tight")
plt.close()
print("Saved chart 6: year over year temperature")

plt.figure(figsize=(8, 5))
plt.hist(df["WindSpeed_kmh"], bins=30, color="seagreen", edgecolor="white")
plt.title("Wind Speed Distribution", fontsize=14)
plt.xlabel("Wind Speed (km/h)")
plt.ylabel("Number of Days")
plt.tight_layout()
plt.savefig("visualizations/project3/7_wind_speed.png", dpi=150, bbox_inches="tight")
plt.close()
print("Saved chart 7: wind speed distribution")

plt.figure(figsize=(8, 6))
sns.heatmap(correlation, annot=True, fmt=".2f", cmap="RdYlGn", center=0, linewidths=0.5)
plt.title("Correlation Between Weather Variables", fontsize=13)
plt.tight_layout()
plt.savefig("visualizations/project3/8_correlation.png", dpi=150, bbox_inches="tight")
plt.close()
print("Saved chart 8: correlation heatmap")

print("\n--- Insights ---")
print(f"1. Hottest month       : {hottest_month} ({monthly_temp[hottest_month]:.1f}°C)")
print(f"2. Wettest month       : {wettest_month} ({monthly_rain[wettest_month]:.0f}mm avg)")
print(f"3. Extreme events      : {extreme_days} days ({extreme_days/total_days*100:.1f}% of all days)")
print(f"4. Monsoon rainfall    : {monsoon_pct:.0f}% of annual total")
print(f"5. Temp range          : {min_temp:.1f}°C to {max_temp:.1f}°C")
print(f"6. Avg humidity        : {avg_humidity:.1f}%")

print("\n--- Recommendations ---")
print("1. Set up flood warning systems - most extreme rain events happen in Monsoon.")
print(f"2. Prepare cooling plans for {hottest_month} heatwave period.")
print(f"3. Farmers should plan crops before {wettest_month} heavy rains begin.")
print("4. Track temperature rise every year to study climate change effects.")
print("5. Have water storage plans ready for Jan-Feb dry period.")

