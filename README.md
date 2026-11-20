# Reproducible Data Pipelines, Tabular ML and Systems Exploration — Part A

NYC 311 service requests: a reproducible data quality and insights pipeline.

## Dataset

- Source: NYC Open Data (Socrata API): https://data.cityofnewyork.us/resource/erm2-nwe9.csv?$limit=10000
- 10,000 rows, 44 columns. Accessed November 2026.
- Raw file: data/raw/nyc_311_raw.csv (never edited).

## Setup

- Python 3.13
- pip install pandas numpy matplotlib pytest

## Run

1. Download the raw data (first time only, from the src folder):
   cd src
   python -m assignment_2.load_data
2. Generate the schema (from the project root):
   python src/assignment_2/inspect_schema.py
3. Run the cleaning and validation pipeline (from the src folder):
   python -m assignment_2.pipeline
4. Run the notebooks in order: notebooks/01_explore_data.ipynb, then notebooks/02_exploratory_analysis.ipynb.

## What the pipeline does

- fix_data_types: unique_key to string; dates to datetime; incident_zip, council_district, bbl to int.
- standardize_categories: trims spaces and upper-cases 10 categorical columns.
- drop_duplicate: removes duplicate unique_key rows, keeps the first (0 found).
- handle_missing_values: drops 9 columns missing in over 95% of rows.
- fill_missing_values: borough to UNSPECIFIED, descriptor to NOT SPECIFIED.
- Validation (validation.py) raises an error on failure: unique_key has no missing or duplicate values; data types match; created_date, agency, complaint_type and status have no missing values. All 3 checks passed (100%).
