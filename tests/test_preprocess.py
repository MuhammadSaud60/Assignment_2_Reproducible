import pandas as pd

from assignment_2.preprocessing import create_preprocessor


def test_create_preprocessor():

    df = pd.DataFrame({
        "age": [20, 30, None, 40],
        "salary": [20000, 30000, 40000, None],
        "city": ["Mardan", "Peshawar", None, "Islamabad"],
        "department": ["IT", "HR", "IT", "Finance"]
    })

    numeric_features = ["age", "salary"]
    categorical_features = ["city", "department"]

    preprocessor = create_preprocessor(
        numeric_features,
        categorical_features
    )

    result = preprocessor.fit_transform(df)

    assert result.shape[0] == 4
    assert result.shape[1] == 8
    assert not pd.isna(result).any()