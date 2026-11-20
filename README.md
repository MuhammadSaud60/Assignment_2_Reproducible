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

## Outputs

- data/cleaned/nyc_311_cleaned.csv (10,000 rows, 35 columns)
- outputs/reports/missing_values_comparison.csv (missing before/after per column)
- outputs/reports/data_quality_report.csv (row counts, duplicates, validation pass rate)
- outputs/figures/top_10_complaint_types.png, requests_by_borough.png, requests_by_status.png
- docs/schema.md (generated schema)

## Findings (short)

- Most requests from Brooklyn (3,219). Most common complaint: Illegal Parking (1,712).
- Status: Closed 4,370; Open 3,369; In Progress 2,238; Assigned 23.
- Highest closure rate: Queens 50.52%. Lowest: Staten Island 35.78%.
- Resolution time for closed requests: mean 1.98 hours, median 1.07 hours.

## Project layout

project/
  README.md
  requirements.txt
  src/
    assignment_2/
      __init__.py
      load_data.py
      inspect_schema.py
      cleaning.py
      validation.py
      quality_report.py
      pipeline.py
  data/
    raw/nyc_311_raw.csv
    cleaned/nyc_311_cleaned.csv
  notebooks/
    01_explore_data.ipynb
    02_exploratory_analysis.ipynb
  outputs/
    figures/
    reports/
  docs/
    schema.md

## Notes

- Raw data is never overwritten; cleaned data goes to data/cleaned/.
- 12 rows have closed_date before created_date (source rounds closed_date down to the minute; kept). 3,097 rows have resolution_action_updated_date before created_date (that field is date-only; never used for duration maths).
- AI assistance: an AI assistant was used for explanations and drafting; every submitted line was reviewed by the author and can be explained to the TA.
