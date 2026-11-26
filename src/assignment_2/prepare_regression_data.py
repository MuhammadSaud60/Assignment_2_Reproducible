from pathlib import Path

import pandas as pd


PROJECT_ROOT = Path(__file__).resolve().parents[2]

INPUT_PATH = (
    PROJECT_ROOT
    / "data"
    / "cleaned"
    / "nyc_311_cleaned.csv"
)

OUTPUT_DIR = PROJECT_ROOT / "data" / "processed"

OUTPUT_PATH = OUTPUT_DIR / "nyc_311_regression.csv"


def prepare_regression_data():

    df = pd.read_csv(
        INPUT_PATH,
        parse_dates=["created_date", "closed_date"]
    )

    print("Initial dataset:", df.shape)

    # Calculate completion time in hours
    df["completion_hours"] = (
        df["closed_date"] - df["created_date"]
    ).dt.total_seconds() / 3600

    # Remove missing and negative completion durations
    df = df.dropna(subset=["completion_hours"])
    df = df[df["completion_hours"] >= 0].copy()

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    df.to_csv(OUTPUT_PATH, index=False)

    print("REGRESSION DATA PREPARED")
    print("Final dataset:", df.shape)
    print("Saved to:", OUTPUT_PATH)


if __name__ == "__main__":
    prepare_regression_data()



