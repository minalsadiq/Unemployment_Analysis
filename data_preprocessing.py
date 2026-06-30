"""
data_preprocessing.py
Handles dataset acquisition, cleaning, and preprocessing for the
Unemployment Analysis project.
"""

import os

import numpy as np
import pandas as pd

import config
from utils import get_logger

logger = get_logger(__name__)


class DataPreprocessor:
    """Encapsulates all data loading, cleaning and preprocessing logic."""

    def __init__(self, dataset_path: str = config.DATASET_PATH):
        self.dataset_path = dataset_path

    # ------------------------------------------------------------------
    # Dataset acquisition
    # ------------------------------------------------------------------
    def load_or_create_dataset(self) -> pd.DataFrame:
        """
        Load the unemployment dataset from disk. If it is not present,
        generate a realistic synthetic monthly unemployment-rate dataset
        (across multiple regions) covering a pre-COVID, COVID, and
        post-COVID period, and persist it as a CSV for reproducibility.

        Returns
        -------
        pd.DataFrame
            Raw unemployment dataset.
        """
        if os.path.exists(self.dataset_path):
            logger.info("Loading existing dataset from %s", self.dataset_path)
            df = pd.read_csv(self.dataset_path, parse_dates=[config.DATE_COLUMN])
        else:
            logger.info("Dataset not found locally. Generating synthetic dataset.")
            df = self._generate_synthetic_dataset()
            df.to_csv(self.dataset_path, index=False)
            logger.info("Dataset saved to %s", self.dataset_path)
        return df

    @staticmethod
    def _generate_synthetic_dataset() -> pd.DataFrame:
        """Create a realistic synthetic monthly unemployment dataset."""
        rng = np.random.default_rng(config.RANDOM_STATE)
        regions = ["North", "South", "East", "West", "Central"]
        dates = pd.date_range("2019-01-01", "2022-12-01", freq="MS")

        records = []
        for region in regions:
            base_rate = rng.uniform(5.0, 8.0)
            for date in dates:
                # Baseline seasonal pattern
                seasonal = 0.5 * np.sin(2 * np.pi * date.month / 12)

                # COVID shock: large spike March 2020 - mid 2021, then recovery
                if pd.Timestamp(config.COVID_START) <= date <= pd.Timestamp("2020-07-01"):
                    covid_shock = rng.uniform(8.0, 14.0)
                elif pd.Timestamp("2020-07-01") < date <= pd.Timestamp(config.COVID_END):
                    covid_shock = rng.uniform(3.0, 7.0)
                else:
                    covid_shock = 0.0

                noise = rng.normal(0, 0.4)
                rate = max(base_rate + seasonal + covid_shock + noise, 1.0)

                labour_participation = max(
                    rng.uniform(58, 68) - (covid_shock * 0.3), 40
                )
                employed = round(rng.uniform(0.3, 0.5) * 1_000_000 * (1 - rate / 100))

                records.append(
                    {
                        config.DATE_COLUMN: date,
                        config.REGION_COLUMN: region,
                        config.UNEMPLOYMENT_COLUMN: round(rate, 2),
                        config.LABOUR_PARTICIPATION_COLUMN: round(labour_participation, 2),
                        config.EMPLOYED_COLUMN: employed,
                    }
                )

        # Inject a few missing values to simulate real-world messiness
        df = pd.DataFrame(records)
        missing_idx = rng.choice(df.index, size=int(len(df) * 0.02), replace=False)
        df.loc[missing_idx, config.UNEMPLOYMENT_COLUMN] = np.nan
        return df

    # ------------------------------------------------------------------
    # Cleaning
    # ------------------------------------------------------------------
    @staticmethod
    def clean_data(df: pd.DataFrame) -> pd.DataFrame:
        """
        Clean the raw dataframe: parse dates, drop duplicates, and
        impute missing unemployment rate values per region.
        """
        df = df.copy()
        df[config.DATE_COLUMN] = pd.to_datetime(df[config.DATE_COLUMN])

        before = len(df)
        df = df.drop_duplicates().reset_index(drop=True)
        logger.info("Removed %d duplicate rows", before - len(df))

        missing = df[config.UNEMPLOYMENT_COLUMN].isnull().sum()
        if missing > 0:
            logger.info("Imputing %d missing unemployment rate values", missing)
            df[config.UNEMPLOYMENT_COLUMN] = df.groupby(config.REGION_COLUMN)[
                config.UNEMPLOYMENT_COLUMN
            ].transform(lambda s: s.fillna(s.mean()))

        df = df.sort_values([config.REGION_COLUMN, config.DATE_COLUMN]).reset_index(
            drop=True
        )
        return df

    # ------------------------------------------------------------------
    # Feature engineering
    # ------------------------------------------------------------------
    @staticmethod
    def add_period_labels(df: pd.DataFrame) -> pd.DataFrame:
        """Add a categorical column flagging pre-COVID / COVID / post-COVID periods."""
        df = df.copy()

        def label_period(date):
            if date < pd.Timestamp(config.COVID_START):
                return "Pre-COVID"
            if date <= pd.Timestamp(config.COVID_END):
                return "COVID Period"
            return "Post-COVID"

        df["period"] = df[config.DATE_COLUMN].apply(label_period)
        df["year"] = df[config.DATE_COLUMN].dt.year
        df["month"] = df[config.DATE_COLUMN].dt.month
        df["month_name"] = df[config.DATE_COLUMN].dt.month_name()
        return df

    def run_pipeline(self):
        """Execute the full preprocessing pipeline end-to-end."""
        df = self.load_or_create_dataset()
        df = self.clean_data(df)
        df = self.add_period_labels(df)
        return df
