"""
 Name: Muhammad Saud
 PSEB-AI-PEW-01 (PSEB-AI-PEW-01)
 Date: 20 November 2026

"""

import os
import pandas as pd

df = pd.read_csv("data/raw/nyc_311_raw.csv", low_memory=False)

os.makedirs("docs", exist_ok=True)

with open("docs/schema.md", "w", encoding="utf-8") as file:
    file.write("# NYC 311 Dataset Schema\n\n")
    file.write(f"Rows: {len(df)}, Columns: {len(df.columns)}\n\n")
    file.write("| Column | Type | Missing | Missing % | Unique |\n")
    file.write("|---|---|---|---|---|\n")

    for column in df.columns:
        missing = int(df[column].isna().sum())
        percent = round(missing / len(df) * 100, 2)
        unique = int(df[column].nunique())
        file.write(f"| {column} | {df[column].dtype} | {missing} | {percent} | {unique} |\n")

print("Schema saved: docs/schema.md")
