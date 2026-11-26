from pathlib import Path

import joblib
import pandas as pd

from sklearn.model_selection import train_test_split, KFold, cross_validate
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import StandardScaler, OneHotEncoder

from sklearn.dummy import DummyRegressor
from sklearn.ensemble import RandomForestRegressor, ExtraTreesRegressor

from sklearn.metrics import (
    mean_absolute_error,
    mean_squared_error,
    r2_score
)


PROJECT_ROOT = Path(__file__).resolve().parents[2]

DATA_PATH = (
    PROJECT_ROOT
    / "data"
    / "processed"
    / "nyc_311_regression.csv"
)

MODEL_DIR = PROJECT_ROOT / "outputs" / "models"
REPORT_DIR = PROJECT_ROOT / "outputs" / "reports"


def load_data():

    df = pd.read_csv(
        DATA_PATH,
        parse_dates=["created_date"]
    )

    print("REGRESSION DATA LOADED")
    print("Dataset shape:", df.shape)

    return df


def prepare_features(df):

    candidate_features = [
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

    model_df = df[
        candidate_features + ["completion_hours"]
    ].copy()

    # Extract time-based features
    model_df["created_hour"] = model_df["created_date"].dt.hour
    model_df["created_dayofweek"] = model_df["created_date"].dt.day_of_week
    model_df["created_month"] = model_df["created_date"].dt.month

    # Remove original timestamp
    model_df = model_df.drop(columns=["created_date"])

    X = model_df.drop(columns=["completion_hours"])
    y = model_df["completion_hours"]

    print("FEATURES PREPARED")
    print("Feature matrix:", X.shape)
    print("Target:", y.shape)

    return X, y


def define_feature_types(X):

    numeric_features = [
        "incident_zip",
        "council_district",
        "latitude",
        "longitude",
        "created_hour",
        "created_dayofweek",
        "created_month"
    ]

    categorical_features = [
        "agency",
        "complaint_type",
        "descriptor",
        "location_type",
        "address_type",
        "city",
        "community_board",
        "police_precinct",
        "borough",
        "open_data_channel_type",
        "park_borough"
    ]

    print("Numeric features:", len(numeric_features))
    print("Categorical features:", len(categorical_features))

    return numeric_features, categorical_features


def split_data(X, y):

    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,
        test_size=0.20,
        random_state=42
    )

    print("DATA SPLIT COMPLETED")
    print("Training features:", X_train.shape)
    print("Testing features:", X_test.shape)

    return X_train, X_test, y_train, y_test


def create_preprocessor(numeric_features, categorical_features):

    numeric_transformer = Pipeline(steps=[
        ("imputer", SimpleImputer(strategy="median")),
        ("scaler", StandardScaler())
    ])

    categorical_transformer = Pipeline(steps=[
        ("imputer", SimpleImputer(strategy="most_frequent")),
        ("encoder", OneHotEncoder(handle_unknown="ignore"))
    ])

    preprocessor = ColumnTransformer(transformers=[
        ("num", numeric_transformer, numeric_features),
        ("cat", categorical_transformer, categorical_features)
    ])

    return preprocessor



def create_models(preprocessor):

    baseline_model = Pipeline(steps=[
        ("preprocessor", preprocessor),
        ("model", DummyRegressor(strategy="median"))
    ])

    random_forest_model = Pipeline(steps=[
        ("preprocessor", preprocessor),
        ("model", RandomForestRegressor(
            n_estimators=100,
            random_state=42,
            n_jobs=-1
        ))
    ])

    extra_trees_model = Pipeline(steps=[
        ("preprocessor", preprocessor),
        ("model", ExtraTreesRegressor(
            n_estimators=100,
            random_state=42,
            n_jobs=-1
        ))
    ])

    models = {
        "Median Baseline": baseline_model,
        "Random Forest": random_forest_model,
        "Extra Trees": extra_trees_model
    }

    return models


def evaluate_models(models, X_train, y_train):

    cv = KFold(
        n_splits=5,
        shuffle=True,
        random_state=42
    )

    scoring = {
        "mae": "neg_mean_absolute_error",
        "rmse": "neg_root_mean_squared_error",
        "r2": "r2"
    }

    results = []

    for name, model in models.items():

        scores = cross_validate(
            model,
            X_train,
            y_train,
            cv=cv,
            scoring=scoring,
            n_jobs=-1
        )

        results.append({
            "Model": name,
            "CV MAE": -scores["test_mae"].mean(),
            "CV RMSE": -scores["test_rmse"].mean(),
            "CV R2": scores["test_r2"].mean()
        })

        print(f"{name} evaluation completed.")

    comparison = pd.DataFrame(results)

    return comparison


def train_best_model(models, X_train, y_train):

    best_model = models["Random Forest"]

    print("TRAINING SELECTED MODEL: RANDOM FOREST")

    best_model.fit(X_train, y_train)

    MODEL_DIR.mkdir(parents=True, exist_ok=True)

    model_path = MODEL_DIR / "nyc_311_completion_model.joblib"

    joblib.dump(best_model, model_path)

    print("MODEL TRAINED AND SAVED")
    print("Model path:", model_path)

    return best_model


def evaluate_test_set(model, X_test, y_test):

    predictions = model.predict(X_test)

    mae = mean_absolute_error(y_test, predictions)
    rmse = mean_squared_error(y_test, predictions) ** 0.5
    r2 = r2_score(y_test, predictions)

    print("\nFINAL TEST RESULTS")
    print("-----------------------")
    print(f"MAE:  {mae:.6f}")
    print(f"RMSE: {rmse:.6f}")
    print(f"R2:   {r2:.6f}")

    return predictions




def run_training_pipeline():

    df = load_data()

    X, y = prepare_features(df)

    numeric_features, categorical_features = define_feature_types(X)

    X_train, X_test, y_train, y_test = split_data(X, y)

    preprocessor = create_preprocessor(
        numeric_features,
        categorical_features
    )

    models = create_models(preprocessor)

    comparison = evaluate_models(models, X_train, y_train)

    print("\nMODEL COMPARISON")
    print(comparison.to_string(index=False))

    REPORT_DIR.mkdir(parents=True, exist_ok=True)

    report_path = REPORT_DIR / "model_comparison.csv"
    comparison.to_csv(report_path, index=False)

    print("\nComparison report saved:", report_path)

    best_model = train_best_model(
        models,
        X_train,
        y_train
    )

    evaluate_test_set(
        best_model,
        X_test,
        y_test
    )

    print("\nTRAINING PIPELINE COMPLETED")


if __name__ == "__main__":
    run_training_pipeline()