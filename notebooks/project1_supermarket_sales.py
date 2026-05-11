# Project 1 - Supermarket Sales Analysis
# Domain: Retail
# Dataset: supermarket_sales.csv (real data - 2000 transactions)
# Run this file from the data_portfolio/ folder

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

print("=" * 50)
print("Project 1 - Supermarket Sales Analysis")
print("=" * 50)

df = pd.read_csv("data/supermarket_sales.csv")
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
df["Month"] = df["Date"].dt.month_name()
df["DayOfWeek"] = df["Date"].dt.day_name()

df["Hour"] = df["Time"].str.split(":").str[0].astype(int)

df["COGS"] = df["Total"] - df["Tax"]

print("\nUnique Product Lines:", df["Product_Line"].unique().tolist())
print("Unique Cities:", df["City"].unique().tolist())
print("Unique Branches:", df["Branch"].unique().tolist())
print("Payment types:", df["Payment"].unique().tolist())
print("Customer types:", df["Customer_Type"].unique().tolist())

total_sales        = df["Total"].sum()
total_tax          = df["Tax"].sum()
total_transactions = len(df)
avg_transaction    = df["Total"].mean()
avg_rating         = df["Rating"].mean()
gross_margin_pct   = (total_tax / total_sales) * 100   # Tax = gross income = 5% of cogs

print("\n--- Key Performance Indicators ---")
print(f"Total Revenue      : {total_sales:,.2f}")
print(f"Total Gross Income : {total_tax:,.2f}")
print(f"Total Transactions : {total_transactions}")
print(f"Avg Transaction    : {avg_transaction:,.2f}")
print(f"Gross Margin       : {gross_margin_pct:.1f}%")
print(f"Average Rating     : {avg_rating:.2f} / 10")

product_sales  = df.groupby("Product_Line")["Total"].sum().sort_values(ascending=False)
product_qty    = df.groupby("Product_Line")["Quantity"].sum().sort_values(ascending=False)
city_sales     = df.groupby("City")["Total"].sum().sort_values(ascending=False)
branch_sales   = df.groupby("Branch")["Total"].sum().sort_values(ascending=False)
payment_sales  = df.groupby("Payment")["Total"].sum()
ctype_sales    = df.groupby("Customer_Type")["Total"].sum()

day_order = ["Monday","Tuesday","Wednesday","Thursday","Friday","Saturday","Sunday"]
day_sales = df.groupby("DayOfWeek")["Total"].sum().reindex(day_order)
hour_sales = df.groupby("Hour")["Total"].sum()

best_product  = product_sales.idxmax()
best_city     = city_sales.idxmax()
best_branch   = branch_sales.idxmax()
best_payment  = payment_sales.idxmax()
peak_hour     = hour_sales.idxmax()
best_day      = day_sales.idxmax()

member_avg = df.groupby("Customer_Type")["Total"].mean()
print("\n--- Avg Spending by Customer Type ---")
print(member_avg.round(2))

gender_sales = df.groupby("Gender")["Total"].sum()

numeric_cols = ["Unit_Price", "Quantity", "Tax", "Total", "Rating"]
correlation  = df[numeric_cols].corr()
print("\n--- Correlation Matrix ---")
print(correlation.round(3))

monthly_sales = df.groupby("Date")["Total"].sum()

plt.figure(figsize=(12, 5))
plt.plot(monthly_sales.index, monthly_sales.values, color="steelblue", linewidth=1.5)
plt.fill_between(monthly_sales.index, monthly_sales.values, alpha=0.2, color="steelblue")
plt.title("Daily Revenue Trend", fontsize=14)
plt.xlabel("Date")
plt.ylabel("Total Sales")
plt.xticks(rotation=30)
plt.tight_layout()
plt.savefig("visualizations/project1/1_daily_revenue.png", dpi=150, bbox_inches="tight")
plt.close()
print("\nSaved chart 1: daily revenue")

plt.figure(figsize=(10, 5))
colors = ["steelblue","coral","seagreen","orchid","orange","tomato"]
plt.bar(product_sales.index, product_sales.values, color=colors)
plt.title("Total Sales by Product Line", fontsize=14)
plt.xlabel("Product Line")
plt.ylabel("Total Sales")
plt.xticks(rotation=20, ha="right")
for i, val in enumerate(product_sales.values):
    plt.text(i, val + 200, f"{val:,.0f}", ha="center", fontsize=8)
plt.tight_layout()
plt.savefig("visualizations/project1/2_sales_by_product.png", dpi=150, bbox_inches="tight")
plt.close()
print("Saved chart 2: sales by product line")

plt.figure(figsize=(7, 7))
plt.pie(payment_sales.values, labels=payment_sales.index, autopct="%1.1f%%",
        colors=["steelblue","coral","seagreen"], startangle=140)
plt.title("Revenue by Payment Method", fontsize=14)
plt.tight_layout()
plt.savefig("visualizations/project1/3_payment_methods.png", dpi=150, bbox_inches="tight")
plt.close()
print("Saved chart 3: payment methods")

fig, axes = plt.subplots(1, 2, figsize=(12, 5))
axes[0].bar(branch_sales.index, branch_sales.values,
            color=["steelblue","coral","seagreen"])
axes[0].set_title("Total Sales by Branch", fontsize=12)
axes[0].set_xlabel("Branch")
axes[0].set_ylabel("Total Sales")
for i, val in enumerate(branch_sales.values):
    axes[0].text(i, val + 200, f"{val:,.0f}", ha="center", fontsize=9)

axes[1].bar(city_sales.index, city_sales.values,
            color=["orchid","orange","tomato"])
axes[1].set_title("Total Sales by City", fontsize=12)
axes[1].set_xlabel("City")
axes[1].set_ylabel("Total Sales")
for i, val in enumerate(city_sales.values):
    axes[1].text(i, val + 200, f"{val:,.0f}", ha="center", fontsize=9)

plt.suptitle("Branch and City Performance", fontsize=14, fontweight="bold")
plt.tight_layout()
plt.savefig("visualizations/project1/4_branch_city.png", dpi=150, bbox_inches="tight")
plt.close()
print("Saved chart 4: branch and city")

fig, axes = plt.subplots(1, 2, figsize=(11, 5))
axes[0].pie(ctype_sales.values, labels=ctype_sales.index, autopct="%1.1f%%",
            colors=["steelblue","coral"], startangle=90)
axes[0].set_title("Revenue: Member vs Normal", fontsize=12)

axes[1].pie(gender_sales.values, labels=gender_sales.index, autopct="%1.1f%%",
            colors=["orchid","steelblue"], startangle=90)
axes[1].set_title("Revenue by Gender", fontsize=12)

plt.suptitle("Customer Demographics", fontsize=14, fontweight="bold")
plt.tight_layout()
plt.savefig("visualizations/project1/5_customer_demographics.png", dpi=150, bbox_inches="tight")
plt.close()
print("Saved chart 5: customer demographics")

product_rating = df.groupby("Product_Line")["Rating"].mean().sort_values(ascending=False)

plt.figure(figsize=(10, 5))
bars = plt.bar(product_rating.index, product_rating.values,
               color=["seagreen" if v >= product_rating.mean() else "coral"
                      for v in product_rating.values])
plt.axhline(product_rating.mean(), color="steelblue", linestyle="--",
            linewidth=1.5, label=f"Avg rating ({product_rating.mean():.2f})")
plt.title("Average Customer Rating by Product Line", fontsize=14)
plt.xlabel("Product Line")
plt.ylabel("Average Rating (out of 10)")
plt.xticks(rotation=20, ha="right")
plt.ylim(0, 11)
for i, val in enumerate(product_rating.values):
    plt.text(i, val + 0.1, f"{val:.2f}", ha="center", fontsize=9)
plt.legend()
plt.tight_layout()
plt.savefig("visualizations/project1/6_product_ratings.png", dpi=150, bbox_inches="tight")
plt.close()
print("Saved chart 6: product ratings")

plt.figure(figsize=(11, 5))
peak_color = ["tomato" if h == peak_hour else "steelblue" for h in hour_sales.index]
plt.bar(hour_sales.index, hour_sales.values, color=peak_color)
plt.title(f"Sales by Hour of Day  (Red = Peak Hour {peak_hour}:00)", fontsize=14)
plt.xlabel("Hour")
plt.ylabel("Total Sales")
plt.xticks(hour_sales.index)
plt.tight_layout()
plt.savefig("visualizations/project1/7_hourly_sales.png", dpi=150, bbox_inches="tight")
plt.close()
print("Saved chart 7: hourly sales")

plt.figure(figsize=(7, 5))
sns.heatmap(correlation, annot=True, fmt=".2f", cmap="RdYlGn", center=0, linewidths=0.5)
plt.title("Correlation Between Key Variables", fontsize=14)
plt.tight_layout()
plt.savefig("visualizations/project1/8_correlation_heatmap.png", dpi=150, bbox_inches="tight")
plt.close()
print("Saved chart 8: correlation heatmap")

print("\n--- Business Insights ---")
print(f"1. Top product line  : {best_product}  ({product_sales[best_product]:,.2f})")
print(f"2. Top city          : {best_city}  ({city_sales[best_city]:,.2f})")
print(f"3. Best branch       : {best_branch}")
print(f"4. Preferred payment : {best_payment}")
print(f"5. Peak hour         : {peak_hour}:00")
print(f"6. Best day          : {best_day}")
print(f"7. Gross margin      : {gross_margin_pct:.1f}%")
print(f"8. Avg rating        : {avg_rating:.2f} / 10")

print("\n--- Recommendations ---")
print(f"1. Increase {best_product} stock - it is the best-selling product line.")
print(f"2. Invest more in Branch {best_branch} - highest revenue generator.")
print(f"3. Add extra staff during the {peak_hour}:00 peak hour.")
print(f"4. Offer discounts to Normal customers to convert them to Members.")
print(f"5. Promote {payment_sales.idxmin()} payments with incentives to diversify usage.")
print(f"6. Focus marketing on {best_city} and replicate strategies in other cities.")

print("\nProject 1 complete!")

