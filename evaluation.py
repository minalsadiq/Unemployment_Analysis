"""
evaluation.py
Statistical evaluation and insight-generation for the Unemployment
Analysis project: correlation analysis, monthly summaries, and a
human-readable insight report.
"""

import os

import pandas as pd

import config
from utils import get_logger

logger = get_logger(__name__)


class InsightEvaluator:
    """Computes statistical summaries and generates an insight report."""

    def __init__(self, results_dir: str = config.RESULTS_DIR):
        self.results_dir = results_dir

    def correlation_analysis(self, df: pd.DataFrame) -> pd.DataFrame:
        """Correlation matrix between unemployment, participation, and employment."""
        numeric_cols = [
            config.UNEMPLOYMENT_COLUMN,
            config.LABOUR_PARTICIPATION_COLUMN,
            config.EMPLOYED_COLUMN,
        ]
        corr = df[numeric_cols].corr()
        corr_path = os.path.join(self.results_dir, "correlation_matrix.csv")
        corr.to_csv(corr_path)
        logger.info("Correlation matrix saved to %s", corr_path)
        return corr

    def monthly_summary(self, df: pd.DataFrame) -> pd.DataFrame:
        """Average unemployment rate per month-of-year (seasonality check)."""
        summary = (
            df.groupby("month_name")[config.UNEMPLOYMENT_COLUMN]
            .mean()
            .reindex(
                [
                    "January", "February", "March", "April", "May", "June",
                    "July", "August", "September", "October", "November", "December",
                ]
            )
            .round(2)
        )
        summary_path = os.path.join(self.results_dir, "monthly_seasonality.csv")
        summary.to_csv(summary_path)
        logger.info("Monthly seasonality summary saved to %s", summary_path)
        return summary

    def regional_summary(self, df: pd.DataFrame) -> pd.DataFrame:
        """Average unemployment rate per region per period."""
        summary = (
            df.groupby([config.REGION_COLUMN, "period"])[config.UNEMPLOYMENT_COLUMN]
            .mean()
            .round(2)
            .unstack()
        )
        summary_path = os.path.join(self.results_dir, "regional_period_summary.csv")
        summary.to_csv(summary_path)
        logger.info("Regional period summary saved to %s", summary_path)
        return summary

    def generate_insight_report(
        self, trends: dict, covid_test: dict, regional_summary: pd.DataFrame
    ) -> str:
        """Compose a human-readable insight summary and save it to disk."""
        lines = []
        lines.append("UNEMPLOYMENT ANALYSIS — INSIGHT SUMMARY")
        lines.append("=" * 60)
        lines.append("")
        lines.append(
            f"1. COVID-19 IMPACT: Average unemployment rose from "
            f"{covid_test['pre_covid_mean']:.2f}% (pre-COVID) to "
            f"{covid_test['covid_mean']:.2f}% (COVID period), an increase of "
            f"{covid_test['difference']:.2f} percentage points."
        )
        significance = (
            "statistically significant" if covid_test["significant_at_5pct"]
            else "not statistically significant"
        )
        lines.append(
            f"   This increase is {significance} at the 5% level "
            f"(p-value = {covid_test['p_value']:.5f})."
        )
        lines.append("")
        lines.append("2. REGIONAL TRENDS (linear slope of unemployment rate over time):")
        for region, t in trends.items():
            direction = "rising" if t["slope"] > 0 else "falling"
            lines.append(
                f"   - {region}: {direction} trend, slope={t['slope']:.4f} "
                f"(R^2={t['r_squared']:.3f}, p={t['p_value']:.4f})"
            )
        lines.append("")
        lines.append("3. REGIONAL/PERIOD AVERAGES (%):")
        lines.append(regional_summary.to_string())
        lines.append("")
        lines.append("4. POLICY IMPLICATIONS:")
        lines.append(
            "   - The sharp COVID-period spike highlights the need for "
            "rapid-response employment support programs during shocks."
        )
        lines.append(
            "   - Regions with persistent rising trends post-COVID may need "
            "targeted reskilling and job-creation initiatives."
        )
        lines.append(
            "   - Seasonal patterns suggest opportunities for counter-cyclical "
            "hiring incentives in historically higher-unemployment months."
        )

        report_text = "\n".join(lines)
        report_path = os.path.join(self.results_dir, "insight_summary.txt")
        with open(report_path, "w") as f:
            f.write(report_text)
        logger.info("Insight summary saved to %s", report_path)
        return report_text
