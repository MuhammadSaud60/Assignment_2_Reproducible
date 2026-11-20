import pandas as pd
import pytest
from assignment_2.validation import validate_unique_key, validate_data_types,  validate_required_fields


def test_validate_unique_key():
    df = pd.DataFrame({
        "unique_key": ["101", "102", "103"]
    })

    assert validate_unique_key(df) is True



def test_validate_data_types():
    df = pd.DataFrame({
        "unique_key": pd.Series(["101", "102"], dtype="string"),
        "created_date": pd.to_datetime(["2026-01-01", "2026-01-02"]),
        "closed_date": pd.to_datetime(["2026-01-03", "2026-01-04"]),
        "resolution_action_updated_date": pd.to_datetime(
            ["2026-01-03", "2026-01-04"]
        ),
        "incident_zip": pd.Series([10001, 10002], dtype="Int64"),
        "council_district": pd.Series([1, 2], dtype="Int64"),
        "bbl": pd.Series([1000010001, 1000010002], dtype="Int64"),
        "latitude": [40.7, 40.8],
        "longitude": [-73.9, -73.8],
    })

    assert validate_data_types(df) is True


def test_validate_data_types_with_wrong_date_type():
    df = pd.DataFrame({
        "unique_key": pd.Series(["101"], dtype="string"),
        "created_date": ["2026-01-01"],  # Incorrect: string, not datetime
        "closed_date": pd.to_datetime(["2026-01-03"]),
        "resolution_action_updated_date": pd.to_datetime(["2026-01-03"]),
        "incident_zip": pd.Series([10001], dtype="Int64"),
        "council_district": pd.Series([1], dtype="Int64"),
        "bbl": pd.Series([1000010001], dtype="Int64"),
        "latitude": [40.7],
        "longitude": [-73.9],
    })

    with pytest.raises(TypeError):
        validate_data_types(df)



def test_validate_required_fields_with_missing_values():
    df = pd.DataFrame({
        "created_date": pd.to_datetime(["2026-01-01", "2026-01-02"]),
        "agency": ["NYPD", None],
        "complaint_type": ["Noise", "Street Condition"],
        "status": ["Closed", "Open"],
    })

    with pytest.raises(ValueError):
        validate_required_fields(df)