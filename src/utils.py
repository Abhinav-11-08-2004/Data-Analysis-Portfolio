"""
utils.py — Reusable helper functions for the Data Analysis Portfolio.
Covers data loading/exploration, validation, visualization templates,
statistical summaries, and PDF report generation.
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import seaborn as sns
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm
from reportlab.platypus import (SimpleDocTemplate, Paragraph, Spacer,
                                Image as RLImage, Table, TableStyle,
                                HRFlowable)
from reportlab.lib.enums import TA_CENTER, TA_LEFT
import os
import warnings
warnings.filterwarnings("ignore")

# ── Global style ──────────────────────────────────────────────────────────────
PALETTE = ["#2E86AB", "#A23B72", "#F18F01", "#C73E1D", "#3B1F2B",
           "#44BBA4", "#E94F37", "#393E41", "#F5A623", "#7B2D8B"]
sns.set_theme(style="whitegrid", palette=PALETTE)
plt.rcParams.update({
    "figure.facecolor": "white",
    "axes.facecolor":   "#F8F9FA",
    "axes.spines.top":  False,
    "axes.spines.right": False,
    "font.family":      "DejaVu Sans",
})


# ── Data Exploration ──────────────────────────────────────────────────────────

def load_and_explore(filepath: str, label: str = "") -> pd.DataFrame:
    """Load a CSV and print a structured exploration summary."""
    df = pd.read_csv(filepath)
    tag = f"[{label}] " if label else ""
    print(f"\n{'='*60}")
    print(f"  {tag}DATASET EXPLORATION")
    print(f"{'='*60}")
    print(f"  Shape        : {df.shape[0]:,} rows × {df.shape[1]} columns")
    print(f"  Columns      : {df.columns.tolist()}")
    print(f"\n  Data Types:\n{df.dtypes.to_string()}")
    print(f"\n  Missing Values:\n{df.isnull().sum().to_string()}")
    print(f"\n  Descriptive Statistics:\n{df.describe(include='all').to_string()}")
    print(f"{'='*60}\n")
    return df


def validate_data(df: pd.DataFrame, required_cols: list) -> bool:
    """Check that required columns exist and there are no fully-empty columns."""
    missing = [c for c in required_cols if c not in df.columns]
    if missing:
        print(f"[VALIDATION FAIL] Missing columns: {missing}")
        return False
    empty = df.columns[df.isnull().all()].tolist()
    if empty:
        print(f"[VALIDATION WARN] Fully-empty columns: {empty}")
    print("[VALIDATION PASS] All required columns present.")
    return True


def clean_dataframe(df: pd.DataFrame) -> pd.DataFrame:
    """Drop duplicates and fill or drop nulls — generic baseline cleaner."""
    before = len(df)
    df = df.drop_duplicates()
    df = df.dropna(how="all")
    after = len(df)
    print(f"[CLEAN] Removed {before - after:,} duplicate / all-null rows. "
          f"Remaining: {after:,}")
    return df.reset_index(drop=True)


# ── Statistical Helpers ───────────────────────────────────────────────────────

def summary_stats(series: pd.Series, label: str = "") -> dict:
    """Return a dict of key statistics for a numeric series."""
    tag = f"[{label}] " if label else ""
    stats = {
        "mean":   round(series.mean(), 2),
        "median": round(series.median(), 2),
        "std":    round(series.std(), 2),
        "min":    round(series.min(), 2),
        "max":    round(series.max(), 2),
        "q25":    round(series.quantile(0.25), 2),
        "q75":    round(series.quantile(0.75), 2),
    }
    print(f"\n{tag}Statistics for '{series.name}':")
    for k, v in stats.items():
        print(f"  {k:8s}: {v}")
    return stats


def correlation_report(df: pd.DataFrame, cols: list) -> pd.DataFrame:
    """Print and return a correlation matrix for selected numeric columns."""
    corr = df[cols].corr().round(3)
    print("\nCorrelation Matrix:")
    print(corr.to_string())
    return corr


# ── Visualization Helpers ─────────────────────────────────────────────────────

def save_fig(fig: plt.Figure, path: str, dpi: int = 150) -> None:
    """Save a matplotlib figure, creating parent dirs as needed."""
    os.makedirs(os.path.dirname(path), exist_ok=True)
    fig.savefig(path, dpi=dpi, bbox_inches="tight")
    plt.close(fig)
    print(f"  [SAVED] {path}")


def bar_chart(data: pd.Series, title: str, xlabel: str, ylabel: str,
              save_path: str, color: str = PALETTE[0],
              horizontal: bool = False) -> None:
    """Generic bar chart with value annotations."""
    fig, ax = plt.subplots(figsize=(10, 5))
    if horizontal:
        bars = ax.barh(data.index.astype(str), data.values, color=color)
        for bar in bars:
            ax.text(bar.get_width() + bar.get_width() * 0.01,
                    bar.get_y() + bar.get_height() / 2,
                    f"{bar.get_width():,.1f}", va="center", fontsize=9)
    else:
        bars = ax.bar(data.index.astype(str), data.values, color=color)
        for bar in bars:
            ax.text(bar.get_x() + bar.get_width() / 2,
                    bar.get_height() + bar.get_height() * 0.01,
                    f"{bar.get_height():,.1f}", ha="center", fontsize=9)
        plt.xticks(rotation=30, ha="right")
    ax.set_title(title, fontsize=14, fontweight="bold", pad=12)
    ax.set_xlabel(xlabel); ax.set_ylabel(ylabel)
    fig.tight_layout()
    save_fig(fig, save_path)


def line_chart(x, y, title: str, xlabel: str, ylabel: str,
               save_path: str, color: str = PALETTE[0]) -> None:
    """Simple line chart with marker points."""
    fig, ax = plt.subplots(figsize=(12, 5))
    ax.plot(x, y, color=color, linewidth=2, marker="o", markersize=3)
    ax.set_title(title, fontsize=14, fontweight="bold", pad=12)
    ax.set_xlabel(xlabel); ax.set_ylabel(ylabel)
    plt.xticks(rotation=30, ha="right")
    fig.tight_layout()
    save_fig(fig, save_path)


def pie_chart(data: pd.Series, title: str, save_path: str) -> None:
    """Donut-style pie chart."""
    fig, ax = plt.subplots(figsize=(7, 7))
    wedges, texts, autotexts = ax.pie(
        data.values, labels=data.index, autopct="%1.1f%%",
        colors=PALETTE[:len(data)], startangle=140,
        wedgeprops={"width": 0.55}
    )
    for at in autotexts:
        at.set_fontsize(9)
    ax.set_title(title, fontsize=14, fontweight="bold", pad=12)
    fig.tight_layout()
    save_fig(fig, save_path)


def heatmap_chart(corr_df: pd.DataFrame, title: str, save_path: str) -> None:
    """Annotated correlation heatmap."""
    fig, ax = plt.subplots(figsize=(8, 6))
    sns.heatmap(corr_df, annot=True, fmt=".2f", cmap="RdYlGn",
                center=0, linewidths=0.5, ax=ax)
    ax.set_title(title, fontsize=14, fontweight="bold", pad=12)
    fig.tight_layout()
    save_fig(fig, save_path)


def histogram_chart(series: pd.Series, title: str, xlabel: str,
                    save_path: str, bins: int = 25,
                    color: str = PALETTE[1]) -> None:
    """Histogram with a KDE overlay."""
    fig, ax = plt.subplots(figsize=(10, 5))
    sns.histplot(series.dropna(), bins=bins, kde=True, color=color, ax=ax)
    ax.set_title(title, fontsize=14, fontweight="bold", pad=12)
    ax.set_xlabel(xlabel); ax.set_ylabel("Frequency")
    fig.tight_layout()
    save_fig(fig, save_path)


def boxplot_chart(df: pd.DataFrame, x: str, y: str, title: str,
                  save_path: str) -> None:
    """Category-wise boxplot."""
    fig, ax = plt.subplots(figsize=(10, 5))
    sns.boxplot(data=df, x=x, y=y, palette=PALETTE, ax=ax)
    ax.set_title(title, fontsize=14, fontweight="bold", pad=12)
    plt.xticks(rotation=30, ha="right")
    fig.tight_layout()
    save_fig(fig, save_path)


def scatter_chart(df: pd.DataFrame, x: str, y: str, title: str,
                  save_path: str, hue: str = None) -> None:
    """Scatter plot, optionally coloured by a hue column."""
    fig, ax = plt.subplots(figsize=(9, 5))
    sns.scatterplot(data=df, x=x, y=y, hue=hue,
                    palette=PALETTE, alpha=0.65, ax=ax)
    ax.set_title(title, fontsize=14, fontweight="bold", pad=12)
    fig.tight_layout()
    save_fig(fig, save_path)


# ── PDF Report Generator ──────────────────────────────────────────────────────

class PortfolioReport:
    """Builds a styled PDF report using ReportLab platypus."""

    BRAND   = colors.HexColor("#2E86AB")
    ACCENT  = colors.HexColor("#E8F0FE")
    W, H    = A4

    def __init__(self, project_title: str, subtitle: str = ""):
        self._title    = project_title
        self._subtitle = subtitle
        self._story    = []
        self._styles   = getSampleStyleSheet()
        self._add_header()

    # ── internal builders ─────────────────────────────────────────────────────
    def _style(self, name, **kw):
        base = self._styles["Normal"]
        return ParagraphStyle(name, parent=base, **kw)

    def _add_header(self):
        title_style = self._style(
            "Title",
            fontSize=20, textColor=colors.white,
            backColor=self.BRAND, leading=26,
            spaceAfter=4, alignment=TA_LEFT,
            leftIndent=12, rightIndent=12,
        )
        sub_style = self._style(
            "Sub",
            fontSize=11, textColor=colors.white,
            backColor=self.BRAND, leading=16,
            spaceAfter=12, alignment=TA_LEFT,
            leftIndent=12,
        )
        self._story.append(Paragraph(self._title, title_style))
        if self._subtitle:
            self._story.append(Paragraph(self._subtitle, sub_style))
        self._story.append(HRFlowable(color=self.BRAND, thickness=2,
                                       width="100%"))
        self._story.append(Spacer(1, 0.3 * cm))

    # ── public API ────────────────────────────────────────────────────────────
    def section_title(self, text: str):
        st = self._style("Sec", fontSize=13, textColor=self.BRAND,
                         backColor=self.ACCENT, leading=18,
                         spaceBefore=8, spaceAfter=4,
                         leftIndent=6, fontName="Helvetica-Bold")
        self._story.append(Paragraph(f"  {text}", st))

    def body_text(self, text: str):
        st = self._style("Body", fontSize=10, leading=14, spaceAfter=4)
        self._story.append(Paragraph(text, st))

    def bullet(self, items: list):
        st = self._style("Bul", fontSize=10, leading=14,
                         leftIndent=16, spaceAfter=2)
        for item in items:
            self._story.append(Paragraph(f"• {item}", st))
        self._story.append(Spacer(1, 0.2 * cm))

    def kpi_row(self, kpis: dict):
        """Render KPIs as a table row."""
        keys = list(kpis.keys())
        vals = [str(kpis[k]) for k in keys]
        data = [keys, vals]
        col_w = (self.W - 2.5 * cm) / len(keys)
        t = Table(data, colWidths=[col_w] * len(keys))
        t.setStyle(TableStyle([
            ("BACKGROUND",  (0, 0), (-1, 0), self.ACCENT),
            ("BACKGROUND",  (0, 1), (-1, 1), colors.white),
            ("TEXTCOLOR",   (0, 0), (-1, 0), colors.HexColor("#555")),
            ("TEXTCOLOR",   (0, 1), (-1, 1), colors.black),
            ("FONTNAME",    (0, 0), (-1, 0), "Helvetica"),
            ("FONTNAME",    (0, 1), (-1, 1), "Helvetica-Bold"),
            ("FONTSIZE",    (0, 0), (-1, -1), 9),
            ("ALIGN",       (0, 0), (-1, -1), "CENTER"),
            ("VALIGN",      (0, 0), (-1, -1), "MIDDLE"),
            ("ROWBACKGROUNDS", (0, 0), (-1, -1),
             [self.ACCENT, colors.HexColor("#F0F8FF")]),
            ("BOX",         (0, 0), (-1, -1), 0.5, self.BRAND),
            ("INNERGRID",   (0, 0), (-1, -1), 0.25, colors.lightgrey),
            ("TOPPADDING",  (0, 0), (-1, -1), 6),
            ("BOTTOMPADDING",(0, 0), (-1, -1), 6),
        ]))
        self._story.append(t)
        self._story.append(Spacer(1, 0.3 * cm))

    def add_image_full(self, img_path: str, caption: str = ""):
        if not os.path.exists(img_path):
            return
        img = RLImage(img_path, width=self.W - 2.5 * cm,
                      height=(self.W - 2.5 * cm) * 0.48)
        self._story.append(img)
        if caption:
            cap_st = self._style("Cap", fontSize=8,
                                  textColor=colors.grey,
                                  alignment=TA_CENTER, spaceAfter=4)
            self._story.append(Paragraph(caption, cap_st))
        self._story.append(Spacer(1, 0.2 * cm))

    def save(self, path: str):
        os.makedirs(os.path.dirname(path), exist_ok=True)
        doc = SimpleDocTemplate(
            path, pagesize=A4,
            leftMargin=1.25 * cm, rightMargin=1.25 * cm,
            topMargin=1 * cm, bottomMargin=1.5 * cm,
        )
        doc.build(self._story)
        print(f"  [REPORT] Saved → {path}")
