# Project 2 - Student Performance Analysis
# Domain: Education
# Run this file from the data_portfolio/ folder

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

print("=" * 50)
print("Project 2 - Student Performance Analysis")
print("=" * 50)

df = pd.read_csv("data/student_performance.csv")
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

total_students = df["StudentID"].nunique()
total_subjects = df["Subject"].nunique()
pass_rate      = (df["Pass"] == "Pass").mean() * 100
avg_score      = df["Score"].mean()
avg_attendance = df["Attendance_%"].mean()
avg_study_hrs  = df["StudyHrs_day"].mean()

print("\n--- Key Numbers ---")
print(f"Total Students  : {total_students}")
print(f"Subjects        : {total_subjects}")
print(f"Pass Rate       : {pass_rate:.1f}%")
print(f"Average Score   : {avg_score:.1f} / 100")
print(f"Avg Attendance  : {avg_attendance:.1f}%")
print(f"Avg Study Hours : {avg_study_hrs:.1f} hrs/day")

subject_avg   = df.groupby("Subject")["Score"].mean().sort_values(ascending=False)
subject_pass  = df.groupby("Subject").apply(
    lambda x: (x["Pass"] == "Pass").mean() * 100
).sort_values(ascending=False)

print("\n--- Average Score per Subject ---")
print(subject_avg.round(1))

print("\n--- Pass Rate per Subject (%) ---")
print(subject_pass.round(1))

section_pass = df.groupby("Section").apply(
    lambda x: (x["Pass"] == "Pass").mean() * 100
).sort_values(ascending=False)

gender_subject = df.groupby(["Gender","Subject"])["Score"].mean().unstack()

corr_cols   = ["Attendance_%","StudyHrs_day","Score"]
correlation = df[corr_cols].corr()
corr_attend = correlation.loc["Attendance_%","Score"]
corr_study  = correlation.loc["StudyHrs_day","Score"]

print("\n--- Correlation Matrix ---")
print(correlation.round(3))
print(f"\nAttendance vs Score correlation : {corr_attend:.3f}")
print(f"Study Hours vs Score correlation: {corr_study:.3f}")

student_summary = df.groupby("StudentID").agg(
    AvgScore    = ("Score",        "mean"),
    AvgAttend   = ("Attendance_%", "mean"),
    FailCount   = ("Pass",         lambda x: (x == "Fail").sum())
).reset_index()

at_risk = student_summary[
    (student_summary["AvgScore"] < 45) | (student_summary["AvgAttend"] < 60)
]
top_10 = student_summary.nlargest(10, "AvgScore")

print(f"\nAt-risk students (score < 45 or attendance < 60%): {len(at_risk)}")
print("\nTop 10 students by average score:")
print(top_10[["StudentID","AvgScore","AvgAttend"]].to_string(index=False))

pass_counts = df["Pass"].value_counts()

plt.figure(figsize=(7, 7))
plt.pie(pass_counts.values, labels=pass_counts.index, autopct="%1.1f%%",
        colors=["seagreen","tomato"], startangle=90)
plt.title("Overall Pass / Fail Distribution", fontsize=14)
plt.tight_layout()
plt.savefig("visualizations/project2/1_pass_fail_pie.png", dpi=150, bbox_inches="tight")
plt.close()
print("\nSaved chart 1: pass/fail pie")

plt.figure(figsize=(9, 5))
plt.bar(subject_avg.index, subject_avg.values,
        color=["steelblue","coral","seagreen","orchid","orange"])
plt.title("Average Score by Subject", fontsize=14)
plt.xlabel("Subject")
plt.ylabel("Average Score (/100)")
for i, val in enumerate(subject_avg.values):
    plt.text(i, val + 0.5, f"{val:.1f}", ha="center", fontsize=10)
plt.ylim(0, 110)
plt.tight_layout()
plt.savefig("visualizations/project2/2_subject_avg_score.png", dpi=150, bbox_inches="tight")
plt.close()
print("Saved chart 2: average score by subject")

subjects = df["Subject"].unique()
colors   = ["steelblue","coral","seagreen","orchid","orange"]

plt.figure(figsize=(11, 5))
for i, sub in enumerate(subjects):
    subset = df[df["Subject"] == sub]["Score"]
    subset.plot.kde(label=sub, color=colors[i], linewidth=2)
plt.axvline(40, color="red", linestyle="--", alpha=0.7, label="Pass mark (40)")
plt.title("Score Distribution by Subject", fontsize=14)
plt.xlabel("Score")
plt.ylabel("Density")
plt.legend()
plt.tight_layout()
plt.savefig("visualizations/project2/3_score_distributions.png", dpi=150, bbox_inches="tight")
plt.close()
print("Saved chart 3: score distributions")

sample = df.sample(800, random_state=1)
dot_colors = sample["Pass"].map({"Pass":"seagreen","Fail":"tomato"})

plt.figure(figsize=(9, 5))
plt.scatter(sample["Attendance_%"], sample["Score"],
            c=dot_colors, alpha=0.5, s=15)
m, b = np.polyfit(df["Attendance_%"], df["Score"], 1)
x_line = np.linspace(df["Attendance_%"].min(), df["Attendance_%"].max(), 100)
plt.plot(x_line, m * x_line + b, color="steelblue", linewidth=2, label="Trend line")
plt.title("Attendance vs Score  (Green = Pass, Red = Fail)", fontsize=14)
plt.xlabel("Attendance (%)")
plt.ylabel("Score")
plt.legend()
plt.tight_layout()
plt.savefig("visualizations/project2/4_attendance_vs_score.png", dpi=150, bbox_inches="tight")
plt.close()
print("Saved chart 4: attendance vs score")

plt.figure(figsize=(9, 5))
plt.scatter(sample["StudyHrs_day"], sample["Score"],
            c=dot_colors, alpha=0.5, s=15)
m2, b2 = np.polyfit(df["StudyHrs_day"], df["Score"], 1)
x_line2 = np.linspace(df["StudyHrs_day"].min(), df["StudyHrs_day"].max(), 100)
plt.plot(x_line2, m2 * x_line2 + b2, color="coral", linewidth=2, label="Trend line")
plt.title("Study Hours vs Score  (Green = Pass, Red = Fail)", fontsize=14)
plt.xlabel("Study Hours per Day")
plt.ylabel("Score")
plt.legend()
plt.tight_layout()
plt.savefig("visualizations/project2/5_study_hours_vs_score.png", dpi=150, bbox_inches="tight")
plt.close()
print("Saved chart 5: study hours vs score")

plt.figure(figsize=(10, 5))
x     = range(len(gender_subject.columns))
width = 0.35
plt.bar([i - width/2 for i in x], gender_subject.loc["Female"], width,
        label="Female", color="orchid")
plt.bar([i + width/2 for i in x], gender_subject.loc["Male"],   width,
        label="Male",   color="steelblue")
plt.xticks(list(x), gender_subject.columns)
plt.title("Average Score by Gender across Subjects", fontsize=14)
plt.ylabel("Average Score")
plt.xlabel("Subject")
plt.legend()
plt.tight_layout()
plt.savefig("visualizations/project2/6_gender_subject.png", dpi=150, bbox_inches="tight")
plt.close()
print("Saved chart 6: gender by subject")

plt.figure(figsize=(7, 5))
plt.bar(section_pass.index, section_pass.values,
        color=["seagreen","steelblue","coral","orchid"])
plt.title("Pass Rate by Section (%)", fontsize=14)
plt.xlabel("Section")
plt.ylabel("Pass Rate (%)")
for i, val in enumerate(section_pass.values):
    plt.text(i, val + 0.3, f"{val:.1f}%", ha="center", fontsize=10)
plt.ylim(0, 115)
plt.tight_layout()
plt.savefig("visualizations/project2/7_section_pass_rate.png", dpi=150, bbox_inches="tight")
plt.close()
print("Saved chart 7: section pass rate")

plt.figure(figsize=(6, 4))
sns.heatmap(correlation, annot=True, fmt=".2f", cmap="RdYlGn",
            center=0, linewidths=0.5)
plt.title("Correlation: Attendance, Study Hours & Score", fontsize=13)
plt.tight_layout()
plt.savefig("visualizations/project2/8_correlation.png", dpi=150, bbox_inches="tight")
plt.close()
print("Saved chart 8: correlation heatmap")

best_subject = subject_avg.idxmax()
weak_subject = subject_avg.idxmin()
weak_section = section_pass.idxmin()

print("\n--- Insights ---")
print(f"1. Overall pass rate    : {pass_rate:.1f}%")
print(f"2. Strongest subject    : {best_subject}  (avg {subject_avg[best_subject]:.1f})")
print(f"3. Weakest subject      : {weak_subject}  (avg {subject_avg[weak_subject]:.1f})")
print(f"4. Attendance-score r   : {corr_attend:.3f}")
print(f"5. Study hrs-score r    : {corr_study:.3f}")
print(f"6. At-risk students     : {len(at_risk)}")
print(f"7. Lowest pass section  : Section {weak_section}")

print("\n--- Recommendations ---")
print(f"1. Start extra classes for {weak_subject} - it has the lowest average score.")
print(f"2. Require minimum 75% attendance - strong link with better scores.")
print(f"3. Help Section {weak_section} students with peer tutoring.")
print(f"4. Encourage students to study at least 3 hours per day.")
print(f"5. Create a list of {len(at_risk)} at-risk students and monitor them closely.")

