import argparse
from pathlib import Path

import joblib
import pandas as pd


PROJECT_ROOT = Path(__file__).resolve().parents[2]

MODEL_PATH = (
    PROJECT_ROOT
    / "outputs"
    / "models"
    / "nyc_311_completion_model.joblib"
)

REQUIRED_COLUMNS = [
    "created_date",
    "agency",
    "complaint_type",
    "descriptor",
    "location_type",
    "incident_zip",
    "address_type",
    "city",
    "community_board",
    "council_district",
    "police_precinct",
    "borough",
    "open_data_channel_type",
    "park_borough",
    "latitude",
    "longitude"
]


def predict_from_csv(input_path, output_path):

    df = pd.read_csv(input_path)

    missing_columns = [
        col for col in REQUIRED_COLUMNS
        if col not in df.columns
    ]

    if missing_columns:
        raise ValueError(
            f"Missing required columns: {missing_columns}"
        )

    df["created_date"] = pd.to_datetime(
        df["created_date"],
        errors="coerce"
    )

    if df["created_date"].isna().any():
        raise ValueError("Invalid or missing created_date values.")

    df["created_hour"] = df["created_date"].dt.hour
    df["created_dayofweek"] = df["created_date"].dt.day_of_week
    df["created_month"] = df["created_date"].dt.month

    features = df[[
        "agency",
        "complaint_type",
        "descriptor",
        "location_type",
        "incident_zip",
        "address_type",
        "city",
        "community_board",
        "council_district",
        "police_precinct",
        "borough",
        "open_data_channel_type",
        "park_borough",
        "latitude",
        "longitude",
        "created_hour",
        "created_dayofweek",
        "created_month"
    ]]

    model = joblib.load(MODEL_PATH)

    predictions = model.predict(features)

    df["predicted_completion_hours"] = predictions

    df.to_csv(output_path, index=False)

    print(f"Predictions saved to: {output_path}")


if __name__ == "__main__":

    parser = argparse.ArgumentParser(
        description="Predict NYC 311 request completion time."
    )

    parser.add_argument("input", help="Input CSV file")
    parser.add_argument("output", help="Output CSV file")

    args = parser.parse_args()

    predict_from_csv(args.input, args.output)