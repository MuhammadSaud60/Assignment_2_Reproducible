import pandas as pd
from src.assignment_2.cleaning import fix_data_types


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
