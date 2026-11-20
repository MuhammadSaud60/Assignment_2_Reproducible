"""
NAME: MUHAMMAD SAUD
ROLL NO: PSEB-AI-PEW-01
DATE: 20-NOV-2026
"""

import pandas as pd


DATE_COLUMNS = [
    "created_date",
    "closed_date",
    "due_date",
    "resolution_action_updated_date"
]

INTEGER_CODE_COLUMNS = [
    "incident_zip",
    "council_district",
    "bbl"
]


def fix_data_types(df: pd.DataFrame) -> pd.DataFrame:
    """
    Convert identifier, date, and integer-code columns to appropriate
    data types while preserving missing values.

    Returns a cleaned copy.
    """
    cleaned = df.copy()

    required_columns = (
        ["unique_key"] + DATE_COLUMNS + INTEGER_CODE_COLUMNS
    )

    missing_columns = [
        col for col in required_columns if col not in cleaned.columns
    ]

    if missing_columns:
        raise ValueError(
            f"Required columns are missing: {missing_columns}"
        )

    cleaned["unique_key"] = cleaned["unique_key"].astype("string")

    # Convert date columns to datetime.
    for column in DATE_COLUMNS:
        cleaned[column] = pd.to_datetime(
            cleaned[column],
            errors="coerce"
        )

    # Convert numeric codes to integers.
    for column in INTEGER_CODE_COLUMNS:
        cleaned[column] = pd.to_numeric(
            cleaned[column],
            errors="raise"
        ).astype("Int64")

    return cleaned
