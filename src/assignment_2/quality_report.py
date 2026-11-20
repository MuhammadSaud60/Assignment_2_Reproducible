from pathlib import Path
import pandas as pd

PROJECT_ROOT = Path(__file__).resolve().parents[2]

RAW_DATA_PATH = PROJECT_ROOT / "data" / "raw" / "nyc_311_raw.csv"
CLEANED_DATA_PATH = PROJECT_ROOT / "data" / "cleaned" / "nyc_311_cleaned.csv"

REPORT_DIR = PROJECT_ROOT / "outputs" / "reports"
REPORT_PATH = REPORT_DIR / "data_quality_report.csv"



def calculate_missing_metrics(df: pd.DataFrame, dataset_name: str) -> pd.DataFrame:
    """
    Calculate missing-value counts and percentages for a dataset.
    """
    total_rows = len(df)

    report = pd.DataFrame({
        "column": df.columns,
        "missing_count": df.isna().sum().values,
        "missing_percentage": (
            df.isna().sum().values / total_rows * 100
        ).round(2),
        "dataset": dataset_name,
    })

    return report



def compare_missing_metrics(raw_df: pd.DataFrame, cleaned_df: pd.DataFrame,) -> pd.DataFrame:
    """
    Compare missing-value metrics before and after cleaning.
    """
    raw_report = calculate_missing_metrics(raw_df, "before_cleaning")
    cleaned_report = calculate_missing_metrics(cleaned_df, "after_cleaning")

    comparison = raw_report.merge(
        cleaned_report,
        on="column",
        how="outer",
        suffixes=("_before", "_after"),
    )

    return comparison



def calculate_row_metrics(raw_df: pd.DataFrame, cleaned_df: pd.DataFrame,) -> dict:
    """
    Calculate row counts and duplicate-removal metrics.
    """
    duplicate_rows = int(raw_df.duplicated().sum())

    duplicate_keys = int(
        raw_df.drop_duplicates()
        .duplicated(subset=["unique_key"])
        .sum()
    )

    return {
        "initial_rows": len(raw_df),
        "final_rows": len(cleaned_df),
        "rows_removed": len(raw_df) - len(cleaned_df),
        "duplicate_rows": duplicate_rows,
        "duplicate_keys": duplicate_keys,
    }




def calculate_validation_metrics(validation_results: dict) -> dict:
    """
    Calculate the percentage of validation checks that passed.
    """
    if not validation_results:
        raise ValueError("No validation results provided.")

    total_checks = len(validation_results)
    passed_checks = sum(validation_results.values())

    return {
        "total_checks": total_checks,
        "passed_checks": passed_checks,
        "failed_checks": total_checks - passed_checks,
        "validation_pass_rate": round(
            (passed_checks / total_checks) * 100, 2
        ),
    }




def build_quality_summary(raw_df: pd.DataFrame,cleaned_df: pd.DataFrame,validation_results: dict,) -> pd.DataFrame:
   
    """
    Combine row-removal and validation metrics into a summary report.
    """
    row_metrics = calculate_row_metrics(raw_df, cleaned_df)
    validation_metrics = calculate_validation_metrics(validation_results)

    all_metrics = {
        **row_metrics,
        **validation_metrics,
    }

    summary = pd.DataFrame(
        list(all_metrics.items()),
        columns=["metric", "value"],
    )

    return summary




def save_quality_reports( raw_df: pd.DataFrame, cleaned_df: pd.DataFrame, validation_results: dict, output_dir: Path = REPORT_DIR,) -> None:
    
    """
    Generate and save missing-value and overall quality reports.
    """
    output_dir.mkdir(parents=True, exist_ok=True)

    missing_report = compare_missing_metrics(raw_df, cleaned_df)

    summary_report = build_quality_summary(
        raw_df,
        cleaned_df,
        validation_results,
    )

    missing_report.to_csv(
        output_dir / "missing_values_comparison.csv",
        index=False,
    )

    summary_report.to_csv(
        output_dir / "data_quality_report.csv",
        index=False,
    )

    print("QUALITY REPORTS SAVED")
    print(f"Output directory: {output_dir}")