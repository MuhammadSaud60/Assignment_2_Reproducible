"""
NAME: MUHAMMAD SAUD
ROLL NO: PSEB-AI-PEW-01
DATE: 20-NOV-2026
"""


from pathlib import Path
import pandas as pd

from assignment_2.cleaning import (
    fix_data_types,
    standardize_categories,
    drop_duplicate,
    handle_missing_values,
    fill_missing_values
)

from assignment_2.validation import (
    validate_unique_key,
    validate_data_types,
    validate_required_fields,
)

from assignment_2.quality_report import save_quality_reports


PROJECT_ROOT = Path(__file__).resolve().parents[2]

RAW_DATA_PATH = PROJECT_ROOT / "data" / "raw" / "nyc_311_raw.csv"
CLEANED_DATA_DIR = PROJECT_ROOT / "data" / "cleaned"
CLEANED_DATA_PATH = CLEANED_DATA_DIR / "nyc_311_cleaned.csv"


def run_pipeline() -> pd.DataFrame:
    """
    Execute the complete data cleaning and validation pipeline.
    """
    if not RAW_DATA_PATH.exists():
        raise FileNotFoundError(
            f"Raw dataset not found: {RAW_DATA_PATH}"
        )

    raw_df = pd.read_csv(RAW_DATA_PATH)
    df = raw_df.copy()

    print("RAW DATA LOADED")
    print(f"Initial rows: {len(df):,}")

    # Cleaning
    df = fix_data_types(df)
    df = standardize_categories(df)
    df = drop_duplicate(df)
    df = handle_missing_values(df)
    df = fill_missing_values(df)

    # Validation
    validation_results = {
    "unique_key": validate_unique_key(df),
    "data_types": validate_data_types(df),
    "required_fields": validate_required_fields(df),
    }

    # Save cleaned data
    CLEANED_DATA_DIR.mkdir(parents=True, exist_ok=True)
    df.to_csv(CLEANED_DATA_PATH, index=False)

    save_quality_reports(
    raw_df=raw_df,
    cleaned_df=df,
    validation_results=validation_results,
    )

    print("\nPIPELINE COMPLETED")
    print("-" * 40)
    print(f"Final rows: {len(df):,}")
    print(f"Final columns: {len(df.columns)}")
    print(f"Saved to: {CLEANED_DATA_PATH}")

    return df


if __name__ == '__main__':
    run_pipeline()