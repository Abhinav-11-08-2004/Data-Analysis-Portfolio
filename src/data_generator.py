"""
data_generator.py
Generates realistic simulated datasets for all 5 portfolio projects.
Run once before executing any project notebook/script.
"""

import pandas as pd
import numpy as np
import os

RNG = np.random.default_rng(42)
OUT = os.path.join(os.path.dirname(__file__), "..", "data")
os.makedirs(OUT, exist_ok=True)



# ── Project 2 : Student Performance ──────────────────────────────────────────
def gen_students(n: int = 1500) -> None:
    subjects = ["Maths", "Science", "English", "History", "CS"]
    sections = ["A", "B", "C", "D"]
    genders  = ["Male", "Female"]

    student_ids = [f"S{i:04d}" for i in range(1, n + 1)]
    gender      = RNG.choice(genders, n, p=[0.52, 0.48])
    section     = RNG.choice(sections, n)
    attendance  = RNG.beta(7, 2, n) * 100            # skewed toward 70-95 %
    study_hrs   = RNG.normal(4, 1.5, n).clip(0.5, 10)

    records = []
    for i in range(n):
        for sub in subjects:
            base  = 45 + attendance[i] * 0.3 + study_hrs[i] * 2
            score = float(np.clip(RNG.normal(base, 10), 0, 100))
            records.append({
                "StudentID":    student_ids[i],
                "Gender":       gender[i],
                "Section":      section[i],
                "Attendance_%": round(attendance[i], 1),
                "StudyHrs_day": round(study_hrs[i], 1),
                "Subject":      sub,
                "Score":        round(score, 1),
                "Pass":         "Pass" if score >= 40 else "Fail",
            })

    df = pd.DataFrame(records)
    path = os.path.join(OUT, "student_performance.csv")
    df.to_csv(path, index=False)
    print(f"[GEN] student_performance.csv → {len(df):,} rows")


# ── Project 3 : Weather Data ──────────────────────────────────────────────────
def gen_weather(n_years: int = 3) -> None:
    dates = pd.date_range("2022-01-01",
                          f"{2022 + n_years - 1}-12-31", freq="D")
    doy   = dates.dayofyear.values
    # Seasonal temperature (India-style): hot summer, cool winter
    base_temp = 25 + 10 * np.sin((doy - 80) * 2 * np.pi / 365)
    temp_max  = (base_temp + RNG.normal(4, 2, len(dates))).round(1)
    temp_min  = (base_temp - RNG.normal(8, 2, len(dates))).round(1)
    temp_avg  = ((temp_max + temp_min) / 2).round(1)

    # Monsoon June-Sep: higher rainfall
    is_monsoon = (dates.month >= 6) & (dates.month <= 9)
    rain_base  = np.where(is_monsoon, 8, 0.5)
    rainfall   = RNG.exponential(rain_base).round(1)
    rainfall    = np.where(rainfall > 200, 200, rainfall)

    humidity   = (55 + 25 * np.sin((doy - 150) * 2 * np.pi / 365)
                  + RNG.normal(0, 5, len(dates))).clip(20, 100).round(1)
    wind_speed = RNG.weibull(2, len(dates)) * 15

    df = pd.DataFrame({
        "Date":         dates.date,
        "Month":        dates.month,
        "Season":       pd.cut(dates.month,
                               bins=[0, 2, 5, 8, 11, 12],
                               labels=["Winter","Spring","Summer",
                                       "Monsoon","Winter2"]).astype(str),
        "TempMax_C":    temp_max,
        "TempMin_C":    temp_min,
        "TempAvg_C":    temp_avg,
        "Rainfall_mm":  rainfall,
        "Humidity_%":   humidity,
        "WindSpeed_kmh": wind_speed.round(1),
        "Extreme":      (rainfall > 50) | (temp_max > 44) | (temp_min < 5),
    })
    path = os.path.join(OUT, "weather_data.csv")
    df.to_csv(path, index=False)
    print(f"[GEN] weather_data.csv       → {len(df):,} rows")


# ── Project 4 : Healthcare / COVID Trends ────────────────────────────────────
def gen_covid(n_days: int = 730) -> None:
    dates  = pd.date_range("2021-01-01", periods=n_days, freq="D")
    states = ["Telangana", "Maharashtra", "Karnataka",
              "Tamil Nadu", "Delhi", "Uttar Pradesh"]

    records = []
    for state in states:
        peak_day   = RNG.integers(60, 200)
        peak_cases = RNG.integers(5000, 50000)
        # Wave shape: rise then fall
        wave1 = peak_cases * np.exp(-0.5 * ((np.arange(n_days) - peak_day) / 40) ** 2)
        peak2 = RNG.integers(100, 300)
        peak2_val  = peak_cases * RNG.uniform(0.5, 1.5)
        wave2 = peak2_val * np.exp(-0.5 * ((np.arange(n_days) - peak2) / 50) ** 2)
        daily_cases = (wave1 + wave2 + RNG.normal(0, 300, n_days)).clip(0).round(0)

        pop      = RNG.integers(5_000_000, 80_000_000)
        vaccinated = np.cumsum(RNG.integers(0, 50000, n_days)).clip(0, pop)
        deaths   = (daily_cases * RNG.uniform(0.01, 0.025)).round(0)
        recovered= (daily_cases * RNG.uniform(0.80, 0.95)).round(0)

        for i, d in enumerate(dates):
            records.append({
                "Date":         d.date(),
                "State":        state,
                "DailyCases":   int(daily_cases[i]),
                "Deaths":       int(deaths[i]),
                "Recovered":    int(recovered[i]),
                "Vaccinated":   int(vaccinated[i]),
                "Population":   pop,
                "Vax_pct":      round(vaccinated[i] / pop * 100, 2),
            })

    df = pd.DataFrame(records)
    path = os.path.join(OUT, "covid_trends.csv")
    df.to_csv(path, index=False)
    print(f"[GEN] covid_trends.csv       → {len(df):,} rows")



# ── Entry Point ───────────────────────────────────────────────────────────────
if __name__ == "__main__":
    print("\n Generating simulated datasets (Projects 2, 3, 4) …\n")
    print("  Note: Projects 1 and 5 use real uploaded datasets.")
    gen_students()
    gen_weather()
    gen_covid()
    print("\n All datasets ready in ./data/\n")
