import pandas as pd
from assignment_2.cleaning import fix_data_types, standardize_categories, drop_duplicate, handle_missing_values, fill_missing_values


def test_fix_data_types():
    df = pd.DataFrame({
        "unique_key": [71177549],
        "created_date": ["2026-11-19T02:06:04.000"],
        "closed_date": ["2026-11-19T02:04:36.000"],
        "due_date": ["2026-11-19T02:06:04.000"],
        "resolution_action_updated_date": ["2026-11-19T02:06:04.000"],
        "incident_zip": [11221.0],
        "council_district": [1.0],
        "bbl": [3033880000.0],
    })
    result = fix_data_types(df)
    assert pd.api.types.is_datetime64_any_dtype(result["created_date"])
    assert str(result["unique_key"].dtype) == "string"
    assert str(result["incident_zip"].dtype) == "Int64"
    assert result["incident_zip"].iloc[0] == 11221


def test_standardize_categories():
    df = pd.DataFrame({
        "complaint_type": ["  noise - street/sidewalk "],
        "status": ["closed"],
        "borough": ["brooklyn"],
        "agency": ["nypd"],
    })
    result = standardize_categories(df)
    assert result["complaint_type"].iloc[0] == "NOISE - STREET/SIDEWALK"
    assert result["status"].iloc[0] == "CLOSED"
    assert result["borough"].iloc[0] == "BROOKLYN"
    assert result["agency"].iloc[0] == "NYPD"



def test_drop_duplicate_complaints():
    df = pd.DataFrame({
        "unique_key": [1, 1, 2],
        "complaint_type": ["Noise", "Noise", "Blocked Driveway"],
    })
    result = drop_duplicate(df)
    assert len(result) == 2
    assert list(result["unique_key"]) == [1, 2]



def test_handle_missing_values():
    df = pd.DataFrame({
        "facility_type": [None, None, "X"],
        "complaint_type": ["Noise", "Noise", "Noise"],
    })
    result = handle_missing_values(df)
    assert "facility_type" not in result.columns
    assert "complaint_type" in result.columns



def test_fill_missing_values():
    df = pd.DataFrame({
        "borough": ["BROOKLYN", None],
        "descriptor": [None, "Loud Music"],
    })
    result = fill_missing_values(df)
    assert result["borough"].iloc[1] == "UNSPECIFIED"
    assert result["descriptor"].iloc[0] == "NOT SPECIFIED"
