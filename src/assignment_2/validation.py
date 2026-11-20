"""
NAME: MUHAMMAD SAUD
ROLL NO: PSEB-AI-PEW-01
DATE: 20-NOV-2026
"""

import pandas as pd



def validate_unique_key(df: pd.DataFrame) -> bool:

    """
    Check that unique_key contains no missing or duplicate values.

    """

    if df["unique_key"].isna().any():
        raise ValueError("unique_key contains missing values.")

    if df["unique_key"].duplicated().any():
        raise ValueError("Duplicate unique_key values found.")

    return True



def validate_data_types(df: pd.DataFrame) -> bool:
    """
    Validate the expected data types of important columns.
    """
    expected_columns = {
        "unique_key": "string",
        "created_date": "datetime",
        "closed_date": "datetime",
        "resolution_action_updated_date": "datetime",
        "incident_zip": "integer",
        "council_district": "integer",
        "bbl": "integer",
        "latitude": "float",
        "longitude": "float",
    }

    for column, expected_type in expected_columns.items():
        if column not in df.columns:
            raise ValueError(f"Required column missing: {column}")

        dtype = df[column].dtype

        if expected_type == "string" and str(dtype) != "string":
            raise TypeError(f"{column} must have string dtype.")

        elif expected_type == "datetime" and not pd.api.types.is_datetime64_any_dtype(dtype):
            raise TypeError(f"{column} must have datetime dtype.")

        elif expected_type == "integer" and not pd.api.types.is_integer_dtype(dtype):
            raise TypeError(f"{column} must have integer dtype.")

        elif expected_type == "float" and not pd.api.types.is_float_dtype(dtype):
            raise TypeError(f"{column} must have float dtype.")

    return True



def validate_required_fields(df: pd.DataFrame) -> bool:
    """
    Check that essential fields contain no missing values.
    """
    required_columns = [
        "created_date",
        "agency",
        "complaint_type",
        "status",
    ]

    for column in required_columns:
        if column not in df.columns:
            raise ValueError(f"Required column missing: {column}")

        if df[column].isna().any():
            raise ValueError(f"{column} contains missing values.")

    return True