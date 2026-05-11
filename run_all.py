"""
run_all.py  —  Master runner for the Data Analysis Portfolio
Creates all required folders, generates datasets, then runs all 5 projects.

Usage (run from the data_portfolio/ folder):
    python run_all.py
"""

import subprocess
import sys
import os
import time

# Always run from the folder that contains this file
BASE = os.path.dirname(os.path.abspath(__file__))

# ── Create all output folders before the scripts start ────────────────────────
folders = [
    "data",
    "reports",
    "visualizations/project1",
    "visualizations/project2",
    "visualizations/project3",
    "visualizations/project4",
    "visualizations/project5",
]
for folder in folders:
    os.makedirs(os.path.join(BASE, folder), exist_ok=True)

# ── Steps to run in order ──────────────────────────────────────────────────────
STEPS = [
    ("Generating Datasets",      "src/data_generator.py"),
    ("Project 1 - Supermarket",  "notebooks/project1_supermarket_sales.py"),
    ("Project 2 - Students",     "notebooks/project2_student_performance.py"),
    ("Project 3 - Weather",      "notebooks/project3_weather_analysis.py"),
    ("Project 4 - COVID",        "notebooks/project4_healthcare_covid.py"),
    ("Project 5 - House Prices",      "notebooks/project5_house_prices.py"),
]


def run_step(label, script):
    print(f"\n{'─' * 55}")
    print(f"  Running: {label}")
    print(f"{'─' * 55}")
    t0 = time.time()
    result = subprocess.run(
        [sys.executable, os.path.join(BASE, script)],
        cwd=BASE           # notebooks use relative paths from here
    )
    elapsed = time.time() - t0
    if result.returncode == 0:
        print(f"  Done in {elapsed:.1f}s")
        return True
    else:
        print(f"  FAILED  (exit code {result.returncode})")
        return False


if __name__ == "__main__":
    print("\n" + "=" * 55)
    print("  DATA ANALYSIS PORTFOLIO - FULL RUN")
    print("=" * 55)

    t_start = time.time()
    results = []

    for label, script in STEPS:
        ok = run_step(label, script)
        results.append((label, ok))

    total = time.time() - t_start

    print("\n" + "=" * 55)
    print("  SUMMARY")
    print("=" * 55)
    for label, ok in results:
        status = "PASS" if ok else "FAIL"
        print(f"  [{status}]  {label}")

    passed = sum(1 for _, ok in results if ok)
    print(f"\n  {passed}/{len(results)} steps completed in {total:.0f}s")
    print(f"\n  Datasets       ->  {os.path.join(BASE, 'data/')}")
    print(f"  Visualisations ->  {os.path.join(BASE, 'visualizations/')}")
    print(f"  PDF Reports    ->  {os.path.join(BASE, 'reports/')}")
    print()
