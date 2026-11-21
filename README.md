# NYC 311 Reproducible Data Quality & Insights Pipeline

## Project Overview

This project implements a reproducible data quality and exploratory analysis pipeline using the NYC 311 Service Requests dataset.

The pipeline loads raw operational data, applies cleaning and validation procedures, generates data quality reports, and saves a cleaned dataset for further analysis.

## Dataset

- **Source:** [NYC 311 Service Requests from 2020 to Present](https://data.cityofnewyork.us/Social-Services/311-Service-Requests-from-2020-to-Present/erm2-nwe9)
- **Source platform:** NYC Open Data
- **Dataset ID:** `erm2-nwe9`
- **Records downloaded:** 10,000
- **Original columns:** 44
- **Access date:** 20 November 2026
- **Raw file:** `data/raw/nyc_311_raw.csv`

Check the source page for the applicable dataset licence and terms of use.

## Project Structure

```text
ASSIGNMENT2/
├── data/
│   ├── raw/
│   └── cleaned/
├── docs/
│   └── data_schema.csv
├── notebooks/
│   └── 02_exploratory_analysis.ipynb
├── outputs/
│   ├── figures/
│   └── reports/
├── sql/
├── src/
│   └── assignment/
│       ├── data_loader.py
│       ├── cleaning.py
│       ├── validation.py
│       ├── quality_report.py
│       ├── schema_report.py
│       └── pipeline.py
├── tests/
├── README.md
└── pyproject.toml
```

## Setup

Create and activate a virtual environment, then install the project dependencies.

```bash
uv sync
```

If your project does not use a uv lock file, install using the dependency configuration in `pyproject.toml`.

## Running the Pipeline

From the project root:

```bash
python -m assignment.pipeline
```

The pipeline reads the raw CSV, applies cleaning and validation, saves the cleaned dataset, and generates quality reports.

To generate the schema report:

```bash
python -m assignment.schema_report
```

## Running Tests

```bash
pytest
```

The tests cover cleaning, validation, and data quality reporting functions.

## Exploratory Analysis

Open `notebooks/02_exploratory_analysis.ipynb` to reproduce the exploratory analysis.

The analysis includes:

- Complaint type frequency analysis.
- Request distribution by borough.
- Request distribution by status.
- Borough-level aggregation using `groupby()` and `agg()`.
- Borough and status comparison using `pivot_table()`.
- NumPy vectorized operations.
- SQLite query for request counts by borough and status.

## Generated Outputs

| Output | Location |
|---|---|
| Cleaned dataset | `data/cleaned/nyc_311_cleaned.csv` |
| Schema report | `docs/data_schema.csv` |
| Missing values comparison | `outputs/reports/missing_values_comparison.csv` |
| Data quality summary | `outputs/reports/data_quality_report.csv` |
| Complaint types chart | `outputs/figures/top_10_complaint_types.png` |
| Borough chart | `outputs/figures/requests_by_borough.png` |
| Status chart | `outputs/figures/requests_by_status.png` |
| SQLite database | `outputs/nyc_311.db` |
| SQLite query result | `outputs/reports/borough_status_sql.csv` |

## Data Quality and Cleaning Decisions

- Converted identifier and date columns to appropriate data types.
- Standardised selected categorical values by trimming whitespace and converting text to uppercase.
- Removed columns with more than 95% missing values.
- Filled missing borough and descriptor values using explicit placeholder labels.
- Retained other missing values rather than applying unsupported imputations.
- Checked duplicate records and duplicate unique keys.
- Applied validation checks for required fields, data types, unique keys, and coordinates.

## Assumptions and Limitations

- The analysis uses a 10,000-record extract and does not represent the complete NYC 311 dataset.
- Columns with more than 95% missing values were removed due to insufficient information.
- Missing values in other fields were retained where imputation could introduce unsupported assumptions.
- Some records have a closure timestamp even when their status is not `CLOSED`. Status and closure timestamp are therefore treated as separate fields.
- A small number of records have closure timestamps earlier than creation timestamps. These anomalies were not silently corrected.
- The dataset contains operational reporting information, and observed request status does not independently establish service quality or resolution effectiveness.

## Reproducibility

Run the pipeline from the project root after installing dependencies. The original raw dataset is kept separate from the cleaned dataset. Analysis outputs and reports are saved to project directories rather than depending only on notebook state.

The raw dataset must be available locally at `data/raw/nyc_311_raw.csv` before running the pipeline.
