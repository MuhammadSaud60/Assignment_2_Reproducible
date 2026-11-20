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


categorical_columns = [
    "agency",
    "agency_name",
    "complaint_type",
    "descriptor",
    "location_type",
    "status",
    "borough",
    "open_data_channel_type",
    "address_type",
    "park_borough"
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





def standardize_categories(df: pd.DataFrame) -> pd.DataFrame:
    """
    Standardize text columns by removing leading/trailing spaces
    and normalizing capitalization in categorical values.

    """
    cleaned = df.copy()


    for column in categorical_columns:
        if column in cleaned.columns:
            cleaned[column] = (
                cleaned[column]
                .astype("string")
                .str.strip()
                .str.upper()
            )

    return cleaned


def drop_duplicate(df):
    """
    
    Remove duplicate rows by unique_key, keeping the first.
    
    """

    cleaned = df.copy()
    return cleaned.drop_duplicates(subset=["unique_key"], keep="first")





def handle_missing_values(df: pd.DataFrame) -> pd.DataFrame:
    """
    Drop highly sparse columns that provide insufficient information.


    """
    cleaned = df.copy()

    columns_to_drop = [
        "facility_type",
        "taxi_company_borough",
        "road_ramp",
        "bridge_highway_direction",
        "due_date",
        "bridge_highway_name",
        "bridge_highway_segment",
        "taxi_pick_up_location",
        "vehicle_type"
    ]

    existing_columns = [
        column for column in columns_to_drop
        if column in cleaned.columns
    ]

    cleaned = cleaned.drop(columns=existing_columns)


    return cleaned



def fill_missing_values(df):

    """
    
    Fill missing borough and descriptor with placeholder labels.
    
    """

    cleaned = df.copy()

    cleaned["borough"] = cleaned["borough"].fillna("UNSPECIFIED")
    cleaned["descriptor"] = cleaned["descriptor"].fillna("NOT SPECIFIED")

    return cleaned