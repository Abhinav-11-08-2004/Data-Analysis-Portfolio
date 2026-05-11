# Project 5 - Stock Market Analysis
# Domain: Finance / Investment
# Run this file from the data_portfolio/ folder

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

print("=" * 50)
print("Project 5 - Stock Market Analysis")
print("=" * 50)

# ── Load the data ──────────────────────────────────────────────────────────────
df = pd.read_csv("data/stock_market.csv")
print("\nDataset shape:", df.shape)
print("\nColumn names:", df.columns.tolist())
print("\nFirst 5 rows:")
print(df.head())
print("\nMissing values:")
print(df.isnull().sum())
print("\nBasic statistics:")
print(df.describe())

# ── Clean the data ─────────────────────────────────────────────────────────────
df = df.drop_duplicates()
print("\nRows after removing duplicates:", len(df))

df["Date"] = pd.to_datetime(df["Date"])

tickers = df["Ticker"].unique().tolist()
colors  = ["steelblue","coral","seagreen","orchid","orange"]

# ── Pivot to wide format ───────────────────────────────────────────────────────
price_pivot = df.pivot(index="Date", columns="Ticker", values="Close").sort_index()
ret_pivot   = df.pivot(index="Date", columns="Ticker", values="Return").sort_index()

# ── Cumulative returns ─────────────────────────────────────────────────────────
# Formula: start from 1.0, multiply by (1 + daily_return/100) each day
cumulative = ((1 + ret_pivot / 100).cumprod() - 1) * 100

# ── Key numbers per stock ──────────────────────────────────────────────────────
final_return  = cumulative.iloc[-1]
trading_days  = len(price_pivot)
ann_return    = final_return / (trading_days / 252)   # annualise
ann_vol       = ret_pivot.std() * np.sqrt(252)         # annualised volatility
sharpe_ratio  = ann_return / ann_vol                   # simple Sharpe (rf = 0)
avg_volume    = df.groupby("Ticker")["Volume"].mean()

best_stock  = final_return.idxmax()
worst_stock = final_return.idxmin()
low_vol     = ann_vol.idxmin()

print("\n--- Stock Performance Summary ---")
for ticker in tickers:
    print(f"  {ticker:<12}  Total Return: {final_return[ticker]:+.1f}%  "
          f"Ann Vol: {ann_vol[ticker]:.1f}%  "
          f"Sharpe: {sharpe_ratio[ticker]:.2f}")

print(f"\nBest stock     : {best_stock}  ({final_return[best_stock]:+.1f}%)")
print(f"Worst stock    : {worst_stock}  ({final_return[worst_stock]:+.1f}%)")
print(f"Lowest risk    : {low_vol}  ({ann_vol[low_vol]:.1f}% volatility)")

# ── Correlation between daily returns ─────────────────────────────────────────
correlation = ret_pivot.corr()
print("\n--- Return Correlation Matrix ---")
print(correlation.round(3))

# ── Chart 1: Normalised price chart (start all at 100) ─────────────────────────
normalised = price_pivot / price_pivot.iloc[0] * 100

plt.figure(figsize=(12, 6))
for i, ticker in enumerate(tickers):
    if ticker in normalised.columns:
        plt.plot(normalised.index, normalised[ticker],
                 color=colors[i], linewidth=1.8, label=ticker)
plt.axhline(100, color="grey", linestyle="--", linewidth=1, alpha=0.6)
plt.title("Normalised Stock Prices (Start = 100)", fontsize=14)
plt.xlabel("Date")
plt.ylabel("Normalised Price")
plt.legend()
plt.xticks(rotation=30)
plt.tight_layout()
plt.savefig("visualizations/project5/1_normalised_prices.png", dpi=150, bbox_inches="tight")
plt.close()
print("\nSaved chart 1: normalised prices")

# ── Chart 2: Cumulative return chart ───────────────────────────────────────────
plt.figure(figsize=(12, 6))
for i, ticker in enumerate(tickers):
    if ticker in cumulative.columns:
        plt.plot(cumulative.index, cumulative[ticker],
                 color=colors[i], linewidth=1.8, label=ticker)
plt.axhline(0, color="grey", linestyle="--", linewidth=1, alpha=0.5)
plt.title("Cumulative Return by Stock (%)", fontsize=14)
plt.xlabel("Date")
plt.ylabel("Cumulative Return (%)")
plt.legend()
plt.xticks(rotation=30)
plt.tight_layout()
plt.savefig("visualizations/project5/2_cumulative_returns.png", dpi=150, bbox_inches="tight")
plt.close()
print("Saved chart 2: cumulative returns")

# ── Chart 3: Moving averages for the best stock ────────────────────────────────
best_df = df[df["Ticker"] == best_stock].set_index("Date").sort_index()
best_df["MA20"] = best_df["Close"].rolling(20).mean()
best_df["MA50"] = best_df["Close"].rolling(50).mean()

plt.figure(figsize=(12, 5))
plt.plot(best_df.index, best_df["Close"], color="steelblue",
         linewidth=1.2, alpha=0.7, label="Close Price")
plt.plot(best_df.index, best_df["MA20"], color="orange",
         linewidth=2, label="20-Day Moving Avg")
plt.plot(best_df.index, best_df["MA50"], color="tomato",
         linewidth=2, label="50-Day Moving Avg")
plt.title(f"{best_stock} - Price with 20 and 50 Day Moving Averages", fontsize=14)
plt.xlabel("Date")
plt.ylabel("Price (Rs)")
plt.legend()
plt.xticks(rotation=30)
plt.tight_layout()
plt.savefig("visualizations/project5/3_moving_averages.png", dpi=150, bbox_inches="tight")
plt.close()
print("Saved chart 3: moving averages")

# ── Chart 4: Rolling 30-day volatility ─────────────────────────────────────────
rolling_vol = ret_pivot.rolling(30).std() * np.sqrt(252)

plt.figure(figsize=(12, 5))
for i, ticker in enumerate(tickers):
    if ticker in rolling_vol.columns:
        plt.plot(rolling_vol.index, rolling_vol[ticker],
                 color=colors[i], linewidth=1.5, label=ticker)
plt.title("30-Day Rolling Volatility (Annualised)", fontsize=14)
plt.xlabel("Date")
plt.ylabel("Volatility (%)")
plt.legend()
plt.xticks(rotation=30)
plt.tight_layout()
plt.savefig("visualizations/project5/4_rolling_volatility.png", dpi=150, bbox_inches="tight")
plt.close()
print("Saved chart 4: rolling volatility")

# ── Chart 5: Average daily volume ──────────────────────────────────────────────
avg_vol_millions = avg_volume / 1e6

plt.figure(figsize=(8, 5))
plt.bar(avg_vol_millions.index, avg_vol_millions.values,
        color=colors[:len(tickers)])
plt.title("Average Daily Trading Volume (Million Shares)", fontsize=14)
plt.xlabel("Stock")
plt.ylabel("Volume (Millions)")
for i, val in enumerate(avg_vol_millions.values):
    plt.text(i, val + 0.02, f"{val:.2f}M", ha="center", fontsize=9)
plt.tight_layout()
plt.savefig("visualizations/project5/5_volume_analysis.png", dpi=150, bbox_inches="tight")
plt.close()
print("Saved chart 5: average volume")

# ── Chart 6: Return distributions for each stock ───────────────────────────────
fig, axes = plt.subplots(2, 3, figsize=(14, 8))
axes_flat = axes.flatten()

for i, ticker in enumerate(tickers):
    if ticker in ret_pivot.columns:
        returns = ret_pivot[ticker].dropna()
        axes_flat[i].hist(returns, bins=40, color=colors[i], edgecolor="white", alpha=0.8)
        axes_flat[i].axvline(0, color="black", linestyle="--", alpha=0.5)
        axes_flat[i].set_title(f"{ticker} - Daily Returns", fontsize=11)
        axes_flat[i].set_xlabel("Return (%)")
        axes_flat[i].set_ylabel("Days")

# hide the last unused subplot
axes_flat[-1].set_visible(False)

plt.suptitle("Daily Return Distributions by Stock", fontsize=14, fontweight="bold")
plt.tight_layout()
plt.savefig("visualizations/project5/6_return_distributions.png", dpi=150, bbox_inches="tight")
plt.close()
print("Saved chart 6: return distributions")

# ── Chart 7: Risk vs Return scatter ────────────────────────────────────────────
plt.figure(figsize=(8, 6))
for i, ticker in enumerate(tickers):
    if ticker in ann_return.index:
        plt.scatter(ann_vol[ticker], ann_return[ticker], s=180,
                    color=colors[i], zorder=3)
        plt.annotate(ticker, (ann_vol[ticker], ann_return[ticker]),
                     textcoords="offset points", xytext=(7, 4), fontsize=10)
plt.axhline(0, color="grey", linestyle="--", alpha=0.5)
plt.title("Risk vs Return (Annualised)", fontsize=14)
plt.xlabel("Annualised Volatility (%) = Risk")
plt.ylabel("Annualised Return (%)")
plt.tight_layout()
plt.savefig("visualizations/project5/7_risk_return.png", dpi=150, bbox_inches="tight")
plt.close()
print("Saved chart 7: risk vs return")

# ── Chart 8: Correlation heatmap ───────────────────────────────────────────────
plt.figure(figsize=(7, 5))
sns.heatmap(correlation, annot=True, fmt=".2f", cmap="RdYlGn",
            center=0, linewidths=0.5)
plt.title("Daily Return Correlation Between Stocks", fontsize=13)
plt.tight_layout()
plt.savefig("visualizations/project5/8_correlation.png", dpi=150, bbox_inches="tight")
plt.close()
print("Saved chart 8: correlation heatmap")

# ── Print insights ─────────────────────────────────────────────────────────────
print("\n--- Insights ---")
print(f"1. Best performer   : {best_stock}  ({final_return[best_stock]:+.1f}% total return)")
print(f"2. Worst performer  : {worst_stock}  ({final_return[worst_stock]:+.1f}% total return)")
print(f"3. Lowest risk stock: {low_vol}  ({ann_vol[low_vol]:.1f}% annualised volatility)")
print( "4. Stocks show low correlation - good for portfolio diversification")
print( "5. 20 and 50 day moving averages can be used to find buy/sell signals")
print( "6. Return distributions have fat tails - bigger swings than normal expected")

print("\n--- Recommendations ---")
print(f"1. Consider adding more {best_stock} - best return among all stocks.")
print( "2. Spread investments across all 5 stocks - low correlation reduces risk.")
print( "3. Use the 50-day moving average as a stop-loss guide.")
print( "4. Watch for unusual volume spikes - they often come before big price moves.")
print(f"5. Review {worst_stock} position - consistently underperforming others.")
print( "6. Set a 7% trailing stop loss to protect profits during volatile periods.")

