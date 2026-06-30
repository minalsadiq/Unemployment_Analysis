"""
config.py
Configuration constants for the Unemployment Analysis project.
"""

import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATASET_DIR = os.path.join(BASE_DIR, "datasets")
RESULTS_DIR = os.path.join(BASE_DIR, "results")

DATASET_PATH = os.path.join(DATASET_DIR, "unemployment.csv")

RANDOM_STATE = 42

DATE_COLUMN = "date"
REGION_COLUMN = "region"
UNEMPLOYMENT_COLUMN = "unemployment_rate"
LABOUR_PARTICIPATION_COLUMN = "labour_participation_rate"
EMPLOYED_COLUMN = "employed"

# COVID period boundaries used for before/during/after comparison
COVID_START = "2020-03-01"
COVID_END = "2021-12-31"

for directory in (DATASET_DIR, RESULTS_DIR):
    os.makedirs(directory, exist_ok=True)
