"""
visualization.py
Visualizations for the Unemployment Analysis project: trend line charts,
heatmaps, and distribution plots. All plots auto-saved to results/.
"""

import os

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import seaborn as sns

import config
from utils import get_logger

logger = get_logger(__name__)
sns.set_theme(style="whitegrid")


class Visualizer:
    """Generates and saves all charts for the project."""

    def __init__(self, results_dir: str = config.RESULTS_DIR):
        self.results_dir = results_dir

    def _save(self, fig, filename: str):
        path = os.path.join(self.results_dir, filename)
        fig.savefig(path, bbox_inches="tight", dpi=150)
        plt.close(fig)
        logger.info("Saved figure: %s", path)

    def plot_national_trend(self, df):
        """Overall (national average) unemployment trend line chart with COVID shading."""
        national = df.groupby(config.DATE_COLUMN)[config.UNEMPLOYMENT_COLUMN].mean()

        fig, ax = plt.subplots(figsize=(12, 6))
        ax.plot(national.index, national.values, color="steelblue", linewidth=2)
        ax.axvspan(
            config.COVID_START, config.COVID_END, color="red", alpha=0.15,
            label="COVID-19 Period",
        )
        ax.set_title("National Average Unemployment Rate Over Time")
        ax.set_xlabel("Date")
        ax.set_ylabel("Unemployment Rate (%)")
        ax.legend()
        self._save(fig, "national_trend.png")

    def plot_regional_trends(self, df):
        """Line chart of unemployment trend per region."""
        fig, ax = plt.subplots(figsize=(12, 6))
        for region, group in df.groupby(config.REGION_COLUMN):
            group = group.sort_values(config.DATE_COLUMN)
            ax.plot(group[config.DATE_COLUMN], group[config.UNEMPLOYMENT_COLUMN], label=region)
        ax.axvspan(config.COVID_START, config.COVID_END, color="red", alpha=0.1)
        ax.set_title("Unemployment Rate Trend by Region")
        ax.set_xlabel("Date")
        ax.set_ylabel("Unemployment Rate (%)")
        ax.legend(title="Region")
        self._save(fig, "regional_trends.png")

    def plot_correlation_heatmap(self, corr):
        """Heatmap of correlation matrix."""
        fig, ax = plt.subplots(figsize=(6, 5))
        sns.heatmap(corr, annot=True, cmap="coolwarm", ax=ax)
        ax.set_title("Correlation Heatmap")
        self._save(fig, "correlation_heatmap.png")

    def plot_period_distribution(self, df):
        """Distribution of unemployment rate across COVID periods."""
        fig, ax = plt.subplots(figsize=(8, 6))
        sns.boxplot(
            data=df, x="period", y=config.UNEMPLOYMENT_COLUMN,
            order=["Pre-COVID", "COVID Period", "Post-COVID"], ax=ax,
        )
        ax.set_title("Unemployment Rate Distribution by Period")
        self._save(fig, "period_distribution.png")

    def plot_monthly_seasonality(self, monthly_summary):
        """Bar chart of average unemployment per calendar month."""
        fig, ax = plt.subplots(figsize=(10, 6))
        monthly_summary.plot(kind="bar", ax=ax, color="teal")
        ax.set_title("Average Unemployment Rate by Month (Seasonality)")
        ax.set_ylabel("Unemployment Rate (%)")
        ax.set_xlabel("Month")
        self._save(fig, "monthly_seasonality.png")

    def plot_regional_heatmap(self, regional_summary):
        """Heatmap of average unemployment per region x period."""
        fig, ax = plt.subplots(figsize=(8, 6))
        sns.heatmap(regional_summary, annot=True, fmt=".1f", cmap="YlOrRd", ax=ax)
        ax.set_title("Average Unemployment Rate: Region x Period")
        self._save(fig, "regional_period_heatmap.png")
