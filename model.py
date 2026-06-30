"""
model.py
Statistical trend modeling for the Unemployment Analysis project.
Although this task is primarily analytical (not predictive ML), this
module fits simple trend models to quantify unemployment dynamics.
"""

import numpy as np
import pandas as pd
from scipy import stats

import config
from utils import get_logger

logger = get_logger(__name__)


class TrendModel:
    """Fits simple statistical trend models on unemployment time series."""

    def __init__(self):
        self.region_trends = {}

    def fit_linear_trend(self, df: pd.DataFrame) -> dict:
        """
        Fit an ordinary least-squares linear trend (rate ~ time) for each
        region to quantify whether unemployment is structurally rising
        or falling over the observed period.

        Returns
        -------
        dict
            Mapping of region -> dict(slope, intercept, r_value, p_value)
        """
        for region, group in df.groupby(config.REGION_COLUMN):
            group = group.sort_values(config.DATE_COLUMN)
            x = np.arange(len(group))
            y = group[config.UNEMPLOYMENT_COLUMN].values

            slope, intercept, r_value, p_value, std_err = stats.linregress(x, y)
            self.region_trends[region] = {
                "slope": slope,
                "intercept": intercept,
                "r_squared": r_value ** 2,
                "p_value": p_value,
                "std_err": std_err,
            }
            logger.info(
                "[%s] trend slope=%.4f (p=%.4f, R^2=%.3f)",
                region,
                slope,
                p_value,
                r_value ** 2,
            )
        return self.region_trends

    @staticmethod
    def covid_impact_test(df: pd.DataFrame) -> dict:
        """
        Run an independent two-sample t-test comparing unemployment rates
        before COVID vs. during the COVID period, to statistically
        validate whether the observed increase is significant.

        Returns
        -------
        dict
            Test statistic, p-value, and group means.
        """
        pre = df.loc[df["period"] == "Pre-COVID", config.UNEMPLOYMENT_COLUMN]
        covid = df.loc[df["period"] == "COVID Period", config.UNEMPLOYMENT_COLUMN]

        t_stat, p_value = stats.ttest_ind(covid, pre, equal_var=False)

        result = {
            "pre_covid_mean": pre.mean(),
            "covid_mean": covid.mean(),
            "difference": covid.mean() - pre.mean(),
            "t_statistic": t_stat,
            "p_value": p_value,
            "significant_at_5pct": bool(p_value < 0.05),
        }
        logger.info(
            "COVID impact test: pre=%.2f%%, covid=%.2f%%, diff=%.2f, p=%.5f",
            result["pre_covid_mean"],
            result["covid_mean"],
            result["difference"],
            p_value,
        )
        return result
