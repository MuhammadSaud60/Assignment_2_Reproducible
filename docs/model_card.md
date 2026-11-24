# Model Card: NYC 311 Completion Time Prediction

## 1. Model Overview

- Model name: NYC 311 Completion Time Predictor
- Model type: Random Forest Regressor
- Framework: Scikit-learn
- Task: Regression
- Target: completion_hours
- Output: Predicted service request completion time in hours

## 2. Intended Use

The model estimates how many hours an NYC 311 service request may take to close.

Intended users:
- NYC 311 operations analysts
- Service planning teams

The predictions are estimates for planning and analysis, not guaranteed completion times.

## 3. Dataset

- Source: NYC 311 service request dataset
- Eligible records: 4,668
- Training records: 3,734
- Testing records: 934
- Dataset coverage: Approximately 19 hours across two calendar dates.

Records with missing closure dates and negative completion durations were excluded.

## 4. Features

The model uses:
- Agency
- Complaint type
- Descriptor
- Location information
- Borough
- Geographic coordinates
- Request creation hour
- Request creation day of week
- Request creation month

## 5. Model Performance

Five-fold cross-validation:

- MAE: 0.960 hours
- RMSE: 1.612 hours
- R²: 0.561

Final test results:

- MAE: 0.994 hours
- RMSE: 1.787 hours
- R²: 0.550

## 6. Limitations and Risks

- The dataset covers a very short time period.
- Long-running requests have higher prediction errors.
- Some relevant operational factors are not available in the dataset.
- Performance on future dates and different periods is not established.
- Predictions should not be treated as guaranteed service completion times.

## 7. Model Artifact

Saved pipeline:

outputs/models/nyc_311_completion_model.joblib

Inference script:

src/assignment_2/predict.py