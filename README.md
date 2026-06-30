# Task 2 — Unemployment Analysis with Python

## Overview
This project analyzes unemployment rate trends across multiple regions
from 2019 to 2022, with a specific focus on quantifying the impact of
the COVID-19 pandemic on labor markets.

## Objective
Clean and explore unemployment data, identify seasonal and regional
patterns, statistically validate the COVID-19 impact, and produce
actionable insights for economic/social policy.

## Project Structure
```
Task2_Unemployment_Analysis/
├── main.py                # Orchestrates the full analysis pipeline
├── data_preprocessing.py  # Dataset loading, cleaning, feature engineering
├── model.py                 # Linear trend fitting + COVID impact t-test
├── evaluation.py            # Correlation, seasonality, insight report
├── visualization.py         # Line charts, heatmaps, distribution plots
├── config.py                 # Paths and constants
├── utils.py                   # Logging helpers
├── requirements.txt
├── .gitignore
├── datasets/                 # Dataset + instructions
└── results/                   # Generated plots and reports (created at runtime)
```

## How to Run
```bash
pip install -r requirements.txt
python main.py
```

## Methodology
1. **Data Preprocessing** — load (or synthetically generate) monthly
   unemployment data per region, handle missing values via
   region-wise mean imputation, and tag each record with a
   Pre-COVID / COVID Period / Post-COVID label.
2. **Exploratory Visualization** — national and regional trend lines
   (with the COVID window shaded), and boxplots of rate distribution
   by period.
3. **Statistical Modeling** — an OLS linear trend is fit per region to
   quantify direction/strength of long-term movement; an independent
   t-test compares pre-COVID vs. COVID-period means to test
   statistical significance of the pandemic's impact.
4. **Evaluation** — correlation analysis (unemployment vs. labour
   participation vs. employment), monthly seasonality summary, and a
   regional x period summary table, all exported as CSVs.
5. **Insight Report** — a consolidated, human-readable summary
   (`insight_summary.txt`) combining statistical findings into policy
   recommendations.

## Results
All generated artifacts are saved automatically to `results/`:
- `national_trend.png`, `regional_trends.png`, `period_distribution.png`
- `correlation_heatmap.png`, `monthly_seasonality.png`,
  `regional_period_heatmap.png`
- `correlation_matrix.csv`, `monthly_seasonality.csv`,
  `regional_period_summary.csv`
- `insight_summary.txt`

## Key Learnings
- The COVID-19 period shows a statistically significant spike in
  unemployment across all regions.
- Seasonal effects are present but are dwarfed by the pandemic shock.
- Regional disparities persist even after the immediate shock
  subsides, suggesting differentiated recovery speeds.
