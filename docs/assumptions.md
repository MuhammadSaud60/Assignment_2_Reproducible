# Data and Modeling Assumptions

## 1. Data Assumptions

- The NYC 311 dataset is treated as a snapshot of service requests available at the time of data collection.
- Each `unique_key` is assumed to identify one service request uniquely.
- The original raw dataset is preserved, and cleaning operations are performed on a separate DataFrame.
- Missing borough values are replaced with `UNSPECIFIED`.
- Missing descriptor values are replaced with `NOT SPECIFIED`.
- Duplicate records are removed during data cleaning.
- Date columns are converted to appropriate datetime types before calculating time-based values.

## 2. Target Variable Assumptions

The regression target is `completion_hours`, calculated as:

`(closed_date - created_date)` in hours.

The following decisions were made:

- Records without a valid `closed_date` are excluded because their completion duration cannot be calculated.
- Negative completion durations are excluded because they indicate invalid date relationships.
- Zero-hour completion durations are retained because they are valid observations in the collected dataset.
- The resulting regression dataset contains 4,668 records.

## 3. Feature Selection and Leakage Prevention

Only information intended to be available when a service request is created is used for prediction.

Columns that reveal the outcome or contain information recorded after request creation are excluded. These include:

- `closed_date`
- `status`
- `resolution_description`
- `resolution_action_updated_date`
- `due_date`
- `completion_hours`

Identifier and unsuitable high-cardinality fields are also excluded from the model.

The `created_date` field is converted into time-based features, including creation hour, day of the week, and month.

## 4. Preprocessing Assumptions

- Missing numerical values are replaced using the median.
- Missing categorical values are replaced using the most frequent category.
- Numerical features are standardized using `StandardScaler`.
- Categorical features are encoded using `OneHotEncoder` with `handle_unknown="ignore"`.
- Preprocessing is fitted only on training data through the scikit-learn pipeline to prevent information leakage.

## 5. Model Evaluation Assumptions

- The dataset is divided into 80% training data and 20% testing data.
- A fixed random state of 42 is used for reproducibility.
- Five-fold cross-validation is used for model comparison.
- MAE, RMSE, and R² are used to evaluate regression performance.
- Random Forest is selected as the final model based on its overall cross-validation performance.

## 6. Limitations

- The dataset contains only a short observation period, approximately 19 hours across two dates. It may not represent long-term NYC 311 request patterns.
- A random train/test split does not evaluate performance on a completely separate future time period.
- The model may perform poorly on requests with unusually long completion times.
- The model's predictions are estimates and should not be treated as guaranteed completion times.
- The collected dataset may not represent every type of NYC service request or seasonal pattern.

## 7. Reproducibility

The workflow uses a fixed random state for model splitting and cross-validation. The preprocessing and selected model are saved as a fitted pipeline so that predictions can be generated on new records using the same transformations.

The complete workflow can be executed from the project root using:

```powershell
python main.py
```
