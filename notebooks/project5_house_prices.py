# Project 5 - House Price Analysis
# Domain: Finance / Real Estate
# Dataset: house_prices.csv (real data - 300 properties)
# Run this file from the data_portfolio/ folder

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

print("=" * 50)
print("Project 5 - House Price Analysis")
print("=" * 50)

df = pd.read_csv("data/house_prices.csv")
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

print("\nLocations:", df["Location"].unique().tolist())
print("Property Types:", df["Property_Type"].unique().tolist())
print("Bedrooms range:", df["Bedrooms"].min(), "to", df["Bedrooms"].max())
print("Bathrooms range:", df["Bathrooms"].min(), "to", df["Bathrooms"].max())

df["Price_per_sqft"] = (df["Price"] / df["Area"]).round(0)

df["Age_Category"] = pd.cut(df["Age"],
                             bins=[-1, 5, 15, 30, 50],
                             labels=["New (0-5 yrs)", "Mid (6-15 yrs)",
                                     "Old (16-30 yrs)", "Very Old (31+ yrs)"])

avg_price      = df["Price"].mean()
median_price   = df["Price"].median()
max_price      = df["Price"].max()
min_price      = df["Price"].min()
avg_area       = df["Area"].mean()
avg_price_sqft = df["Price_per_sqft"].mean()
total_props    = len(df)

print("\n--- Key Numbers ---")
print(f"Total Properties  : {total_props}")
print(f"Average Price     : {avg_price:,.0f}")
print(f"Median Price      : {median_price:,.0f}")
print(f"Max Price         : {max_price:,.0f}")
print(f"Min Price         : {min_price:,.0f}")
print(f"Avg Area          : {avg_area:.0f} sq ft")
print(f"Avg Price/sqft    : {avg_price_sqft:,.0f}")

location_avg   = df.groupby("Location")["Price"].mean().sort_values(ascending=False)
type_avg       = df.groupby("Property_Type")["Price"].mean().sort_values(ascending=False)
bedroom_avg    = df.groupby("Bedrooms")["Price"].mean().sort_values(ascending=False)
location_count = df.groupby("Location")["Property_ID"].count()
type_count     = df.groupby("Property_Type")["Property_ID"].count()

print("\n--- Average Price by Location ---")
print(location_avg.apply(lambda x: f"{x:,.0f}"))
print("\n--- Average Price by Property Type ---")
print(type_avg.apply(lambda x: f"{x:,.0f}"))
print("\n--- Average Price by Bedrooms ---")
print(bedroom_avg.apply(lambda x: f"{x:,.0f}"))

numeric_cols = ["Area", "Bedrooms", "Bathrooms", "Age", "Price"]
correlation  = df[numeric_cols].corr()
print("\n--- Correlation Matrix ---")
print(correlation.round(3))

best_location = location_avg.idxmax()
best_type     = type_avg.idxmax()

plt.figure(figsize=(10, 5))
plt.hist(df["Price"] / 1e6, bins=25, color="steelblue", edgecolor="white")
plt.axvline(avg_price / 1e6, color="tomato", linestyle="--",
            linewidth=2, label=f"Mean: {avg_price/1e6:.1f}M")
plt.axvline(median_price / 1e6, color="seagreen", linestyle="--",
            linewidth=2, label=f"Median: {median_price/1e6:.1f}M")
plt.title("Property Price Distribution", fontsize=14)
plt.xlabel("Price (Millions)")
plt.ylabel("Number of Properties")
plt.legend()
plt.tight_layout()
plt.savefig("visualizations/project5/1_price_distribution.png", dpi=150, bbox_inches="tight")
plt.close()
print("\nSaved chart 1: price distribution")

plt.figure(figsize=(8, 5))
plt.bar(location_avg.index, location_avg.values / 1e6,
        color=["steelblue","coral","seagreen"])
plt.title("Average Property Price by Location", fontsize=14)
plt.xlabel("Location")
plt.ylabel("Average Price (Millions)")
for i, val in enumerate(location_avg.values):
    plt.text(i, val / 1e6 + 0.3, f"{val/1e6:.1f}M", ha="center", fontsize=10, fontweight="bold")
plt.tight_layout()
plt.savefig("visualizations/project5/2_price_by_location.png", dpi=150, bbox_inches="tight")
plt.close()
print("Saved chart 2: price by location")

plt.figure(figsize=(8, 5))
plt.bar(type_avg.index, type_avg.values / 1e6,
        color=["orchid","orange","tomato"])
plt.title("Average Property Price by Type", fontsize=14)
plt.xlabel("Property Type")
plt.ylabel("Average Price (Millions)")
for i, val in enumerate(type_avg.values):
    plt.text(i, val / 1e6 + 0.3, f"{val/1e6:.1f}M", ha="center", fontsize=10, fontweight="bold")
plt.tight_layout()
plt.savefig("visualizations/project5/3_price_by_type.png", dpi=150, bbox_inches="tight")
plt.close()
print("Saved chart 3: price by property type")

type_colors = {"House": "steelblue", "Villa": "coral", "Apartment": "seagreen"}
dot_colors  = df["Property_Type"].map(type_colors)

plt.figure(figsize=(10, 6))
for ptype, color in type_colors.items():
    subset = df[df["Property_Type"] == ptype]
    plt.scatter(subset["Area"], subset["Price"] / 1e6,
                c=color, label=ptype, alpha=0.65, s=30)
m, b = np.polyfit(df["Area"], df["Price"] / 1e6, 1)
x_line = np.linspace(df["Area"].min(), df["Area"].max(), 100)
plt.plot(x_line, m * x_line + b, color="black", linewidth=1.5,
         linestyle="--", label="Trend line")
plt.title("Property Area vs Price", fontsize=14)
plt.xlabel("Area (sq ft)")
plt.ylabel("Price (Millions)")
plt.legend()
plt.tight_layout()
plt.savefig("visualizations/project5/4_area_vs_price.png", dpi=150, bbox_inches="tight")
plt.close()
print("Saved chart 4: area vs price")

plt.figure(figsize=(8, 5))
plt.bar(bedroom_avg.index.astype(str), bedroom_avg.values / 1e6,
        color=["steelblue","coral","seagreen","orchid","orange"])
plt.title("Average Price by Number of Bedrooms", fontsize=14)
plt.xlabel("Bedrooms")
plt.ylabel("Average Price (Millions)")
for i, (beds, val) in enumerate(bedroom_avg.items()):
    plt.text(i, val / 1e6 + 0.2, f"{val/1e6:.1f}M", ha="center", fontsize=9)
plt.tight_layout()
plt.savefig("visualizations/project5/5_price_by_bedrooms.png", dpi=150, bbox_inches="tight")
plt.close()
print("Saved chart 5: price by bedrooms")

loc_colors = {"Rural": "steelblue", "Suburb": "coral", "City Center": "seagreen"}

plt.figure(figsize=(10, 6))
for loc, color in loc_colors.items():
    subset = df[df["Location"] == loc]
    plt.scatter(subset["Age"], subset["Price"] / 1e6,
                c=color, label=loc, alpha=0.65, s=30)
m2, b2 = np.polyfit(df["Age"], df["Price"] / 1e6, 1)
x2 = np.linspace(df["Age"].min(), df["Age"].max(), 100)
plt.plot(x2, m2 * x2 + b2, color="black", linewidth=1.5,
         linestyle="--", label="Trend line")
plt.title("Property Age vs Price", fontsize=14)
plt.xlabel("Age (Years)")
plt.ylabel("Price (Millions)")
plt.legend()
plt.tight_layout()
plt.savefig("visualizations/project5/6_age_vs_price.png", dpi=150, bbox_inches="tight")
plt.close()
print("Saved chart 6: age vs price")

fig, axes = plt.subplots(1, 2, figsize=(13, 5))
sns.boxplot(data=df, x="Location", y="Price_per_sqft",
            palette=["steelblue","coral","seagreen"], ax=axes[0])
axes[0].set_title("Price per Sq Ft by Location", fontsize=12)
axes[0].set_xlabel("Location")
axes[0].set_ylabel("Price per Sq Ft")

sns.boxplot(data=df, x="Property_Type", y="Price_per_sqft",
            palette=["orchid","orange","tomato"], ax=axes[1])
axes[1].set_title("Price per Sq Ft by Property Type", fontsize=12)
axes[1].set_xlabel("Property Type")
axes[1].set_ylabel("Price per Sq Ft")

plt.suptitle("Price per Square Foot Analysis", fontsize=14, fontweight="bold")
plt.tight_layout()
plt.savefig("visualizations/project5/7_price_per_sqft.png", dpi=150, bbox_inches="tight")
plt.close()
print("Saved chart 7: price per sqft boxplots")

plt.figure(figsize=(7, 5))
sns.heatmap(correlation, annot=True, fmt=".2f", cmap="RdYlGn", center=0, linewidths=0.5)
plt.title("Correlation Between Property Features and Price", fontsize=13)
plt.tight_layout()
plt.savefig("visualizations/project5/8_correlation_heatmap.png", dpi=150, bbox_inches="tight")
plt.close()
print("Saved chart 8: correlation heatmap")

age_price_r = correlation.loc["Age", "Price"]
area_price_r = correlation.loc["Area", "Price"]

print("\n--- Insights ---")
print(f"1. Most expensive location : {best_location}  ({location_avg[best_location]/1e6:.2f}M avg)")
print(f"2. Most expensive type     : {best_type}  ({type_avg[best_type]/1e6:.2f}M avg)")
print(f"3. Area–Price correlation  : {area_price_r:.3f}  (larger = more expensive)")
print(f"4. Age–Price correlation   : {age_price_r:.3f}  (newer = more expensive)")
print(f"5. Avg price per sq ft     : {avg_price_sqft:,.0f}")
print(f"6. Price range             : {min_price/1e6:.1f}M  to  {max_price/1e6:.1f}M")

print("\n--- Recommendations ---")
print(f"1. Invest in {best_location} properties - highest average returns.")
print(f"2. {best_type}s command the highest prices - prioritise them for premium listings.")
print(f"3. Larger area strongly predicts higher price (r={area_price_r:.2f}) - highlight sq footage in listings.")
print(f"4. Newer properties fetch higher prices - renovation of old properties can add value.")
print(f"5. City Center properties have highest price per sqft - best for smaller, high-value units.")

print("\nProject 5 complete!")

