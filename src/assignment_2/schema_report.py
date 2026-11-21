"""
 Name: Muhammad Saud
 PSEB-AI-PEW-01 (PSEB-AI-PEW-01)
 Date: 20 November 2026

"""


from pathlib import Path
import pandas as pd

PROJECT_ROOT = Path(__file__).resolve().parents[2]

RAW_PATH = PROJECT_ROOT / "data" / "raw" / "nyc_311_raw.csv"
OUTPUT_PATH = PROJECT_ROOT / "docs" / "data_schema.csv"


def generate_schema_report():
    """Generate a schema report from the original raw dataset."""

    df = pd.read_csv(RAW_PATH)

    schema = pd.DataFrame({
        "column": df.columns,
        "data_type": df.dtypes.astype(str).values,
        "non_null_count": df.notna().sum().values,
        "missing_count": df.isna().sum().values,
        "missing_percentage": (
            df.isna().mean().values * 100
        ).round(2),
        "sample_value": [
            df[col].dropna().iloc[0]
            if df[col].notna().any()
            else None
            for col in df.columns
        ]
    })

    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    schema.to_csv(OUTPUT_PATH, index=False)

    print("SCHEMA REPORT GENERATED")
    print(f"Columns documented: {len(schema)}")
    print(f"Saved to: {OUTPUT_PATH}")


if __name__ == "__main__":
    generate_schema_report()
