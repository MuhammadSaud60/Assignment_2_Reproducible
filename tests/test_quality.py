import pandas as pd
import pytest
from pathlib import Path
from assignment_2.quality_report import calculate_missing_metrics, compare_missing_metrics, calculate_row_metrics, calculate_validation_metrics, build_quality_summary, save_quality_reports


def test_calculate_missing_metrics():
    df = pd.DataFrame({
        "agency": ["NYPD", None, "DOT", None],
        "status": ["Closed", "Open", None, "Closed"],
    })

    result = calculate_missing_metrics(df, "raw")

    assert result.loc[result["column"] == "agency", "missing_count"].iloc[0] == 2
    assert result.loc[result["column"] == "agency", "missing_percentage"].iloc[0] == 50.0

    assert result.loc[result["column"] == "status", "missing_count"].iloc[0] == 1
    assert result.loc[result["column"] == "status", "missing_percentage"].iloc[0] == 25.0

    assert (result["dataset"] == "raw").all()




def test_compare_missing_metrics():
    
    raw_df = pd.DataFrame({
        "agency": ["NYPD", None, "DOT", None],
        "status": ["Closed", "Open", None, "Closed"],
        "facility_type": [None, None, None, "Precinct"],
    })

    cleaned_df = pd.DataFrame({
        "agency": ["NYPD", "NYPD", "DOT"],
        "status": ["Closed", "Open", "Closed"],
    })

    result = compare_missing_metrics(raw_df, cleaned_df)

    # Existing columns appear in the comparison.
    assert "agency" in result["column"].values
    assert "status" in result["column"].values

    # Removed columns must still appear.
    assert "facility_type" in result["column"].values

    facility = result[result["column"] == "facility_type"].iloc[0]

    assert facility["missing_count_before"] == 3
    assert pd.isna(facility["missing_count_after"])



def test_calculate_row_metrics():
    
    raw_df = pd.DataFrame({
    "unique_key": ["101", "102", "102", "103"],
    "agency": ["NYPD", "DOT", "NYPD", "NYPD"],
    })

    cleaned_df = raw_df.drop_duplicates(
        subset=["unique_key"],
        keep="first",
    )

    result = calculate_row_metrics(raw_df, cleaned_df)

    assert result["initial_rows"] == 4
    assert result["final_rows"] == 3
    assert result["rows_removed"] == 1
    assert result["duplicate_rows"] == 0
    assert result["duplicate_keys"] == 1



def test_calculate_validation_metrics():
    validation_results = {
        "unique_key": True,
        "data_types": True,
        "coordinates": True,
        "required_fields": True,
    }

    result = calculate_validation_metrics(validation_results)

    assert result["total_checks"] == 4
    assert result["passed_checks"] == 4
    assert result["failed_checks"] == 0
    assert result["validation_pass_rate"] == 100.0



def test_calculate_validation_metrics_empty():
    with pytest.raises(ValueError):
        calculate_validation_metrics({})


def test_build_quality_summary():
    raw_df = pd.DataFrame({
        "unique_key": ["101", "102", "103"],
        "agency": ["NYPD", "DOT", "NYPD"],
    })

    cleaned_df = raw_df.copy()

    validation_results = {
        "unique_key": True,
        "data_types": True,
        "coordinates": True,
        "required_fields": True,
    }

    result = build_quality_summary(
        raw_df,
        cleaned_df,
        validation_results,
    )

    assert result.loc[
        result["metric"] == "initial_rows", "value"
    ].iloc[0] == 3

    assert result.loc[
        result["metric"] == "rows_removed", "value"
    ].iloc[0] == 0

    assert result.loc[
        result["metric"] == "validation_pass_rate", "value"
    ].iloc[0] == 100.0



def test_save_quality_reports(tmp_path):
    raw_df = pd.DataFrame({
        "unique_key": ["101", "102", "103"],
        "agency": ["NYPD", None, "DOT"],
    })

    cleaned_df = pd.DataFrame({
        "unique_key": ["101", "102", "103"],
        "agency": ["NYPD", "UNSPECIFIED", "DOT"],
    })

    validation_results = {
        "unique_key": True,
        "data_types": True,
        "coordinates": True,
        "required_fields": True,
    }

    save_quality_reports(
        raw_df,
        cleaned_df,
        validation_results,
        output_dir=tmp_path,
    )

    assert (tmp_path / "missing_values_comparison.csv").exists()
    assert (tmp_path / "data_quality_report.csv").exists()