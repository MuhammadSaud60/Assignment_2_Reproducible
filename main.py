"""
NAME: MUHAMMAD SAUD
ROLL NO: PSEB-AI-PEW-01
DATE: 26-NOV-2026

Main entry point for the NYC 311 data engineering
and machine learning workflow.
"""

from src.assignment_2.pipeline import run_pipeline
from src.assignment_2.prepare_regression_data import prepare_regression_data
from src.assignment_2.train import run_training_pipeline



def main():

    print("\n" + "=" * 60)
    print("NYC 311 END-TO-END DATA AND ML PIPELINE")
    print("=" * 60)

    # PART A: Data cleaning and validation
    print("\n[1/3] RUNNING DATA QUALITY PIPELINE")

    run_pipeline()

    # Prepare regression dataset
    print("\n[2/3] PREPARING REGRESSION DATA")

    prepare_regression_data()

    # PART B: Model training and evaluation
    print("\n[3/3] RUNNING MACHINE LEARNING PIPELINE")

    run_training_pipeline()

    print("\n" + "=" * 60)
    print("COMPLETE WORKFLOW FINISHED SUCCESSFULLY")
    print("=" * 60)


if __name__ == "__main__":
    main()