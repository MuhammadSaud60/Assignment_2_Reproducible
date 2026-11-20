"""
    NAME: MUHAMMAD SAUD
    PSEB-AI-PEW-01 (PSEB-AI-PEW-01)
    DATE: 20-NOV-2026
"""


from pathlib import Path

import pandas as pd


# Project root directory
PROJECT_ROOT = Path(__file__).resolve().parents[2]

RAW_DATA_DIR = PROJECT_ROOT / "data" / "raw"
RAW_DATA_PATH = RAW_DATA_DIR / "nyc_311_raw.csv"

# NYC Open Data API
URL = "https://data.cityofnewyork.us/resource/erm2-nwe9.csv?$limit=10000"


def download_raw_data() -> pd.DataFrame:
    
    """Download NYC 311 records and save the original CSV locally."""

    RAW_DATA_DIR.mkdir(parents=True, exist_ok=True)

    if RAW_DATA_PATH.exists():
        raise FileExistsError(
            f"Raw dataset already exists: {RAW_DATA_PATH}. " )

    df = pd.read_csv(URL)

    if df.empty:
        raise ValueError("The API returned an empty dataset.")

    df.to_csv(RAW_DATA_PATH, index=False)

    print("DATA DOWNLOAD COMPLETED")
    print("-" * 40)
    print(f"Rows: {len(df):,}")
    print(f"Columns: {len(df.columns)}")
    print(f"Saved to: {RAW_DATA_PATH}")

    return df


if __name__ == "__main__":
    download_raw_data()