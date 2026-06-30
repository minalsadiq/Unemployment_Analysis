"""
main.py
Entry point for the Unemployment Analysis project.
Orchestrates preprocessing, statistical analysis, evaluation, and
visualization.
"""

import sys

import config
from data_preprocessing import DataPreprocessor
from model import TrendModel
from evaluation import InsightEvaluator
from visualization import Visualizer
from utils import get_logger, print_section

logger = get_logger(__name__)


def main():
    try:
        print_section("STEP 1: DATA PREPROCESSING")
        preprocessor = DataPreprocessor()
        df = preprocessor.run_pipeline()
        print(df.head())
        print(df.describe())

        print_section("STEP 2: VISUAL EXPLORATORY ANALYSIS")
        viz = Visualizer()
        viz.plot_national_trend(df)
        viz.plot_regional_trends(df)
        viz.plot_period_distribution(df)

        print_section("STEP 3: STATISTICAL MODELING")
        trend_model = TrendModel()
        trends = trend_model.fit_linear_trend(df)
        covid_test = trend_model.covid_impact_test(df)

        print_section("STEP 4: EVALUATION & INSIGHTS")
        evaluator = InsightEvaluator()
        corr = evaluator.correlation_analysis(df)
        monthly_summary = evaluator.monthly_summary(df)
        regional_summary = evaluator.regional_summary(df)

        viz.plot_correlation_heatmap(corr)
        viz.plot_monthly_seasonality(monthly_summary)
        viz.plot_regional_heatmap(regional_summary)

        report = evaluator.generate_insight_report(trends, covid_test, regional_summary)
        print(report)

        print_section("PROJECT COMPLETE")
        logger.info("All results saved under: %s", config.RESULTS_DIR)

    except Exception as exc:
        logger.exception("Pipeline failed with error: %s", exc)
        sys.exit(1)


if __name__ == "__main__":
    main()
