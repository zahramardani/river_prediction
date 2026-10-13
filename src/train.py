from __future__ import annotations

import json
from pathlib import Path

import joblib
import pandas as pd
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from xgboost import XGBRegressor

from src.features import FEATURE_COLUMNS, build_features, chronological_split


def metrics(y_true, y_pred) -> dict[str, float]:
    return {
        "mae": float(mean_absolute_error(y_true, y_pred)),
        "rmse": float(mean_squared_error(y_true, y_pred) ** 0.5),
        "r2": float(r2_score(y_true, y_pred)),
    }


def main() -> None:
    data = pd.read_csv("data/sample_timeseries.csv")
    featured = build_features(data)
    train, val, test = chronological_split(featured)

    x_train, y_train = train[FEATURE_COLUMNS], train["target_flow"]
    x_val, y_val = val[FEATURE_COLUMNS], val["target_flow"]
    x_test, y_test = test[FEATURE_COLUMNS], test["target_flow"]

    # Persistence baseline: next value ~= previous observed target.
    baseline_pred = test["target_lag_1"].to_numpy()

    model = XGBRegressor(
        n_estimators=350,
        max_depth=4,
        learning_rate=0.04,
        subsample=0.9,
        colsample_bytree=0.9,
        objective="reg:squarederror",
        random_state=42,
    )
    model.fit(x_train, y_train, eval_set=[(x_val, y_val)], verbose=False)
    pred = model.predict(x_test)

    result = {
        "model": metrics(y_test, pred),
        "persistence_baseline": metrics(y_test, baseline_pred),
        "train_rows": len(train),
        "validation_rows": len(val),
        "test_rows": len(test),
        "features": FEATURE_COLUMNS,
    }

    artifacts = Path("artifacts")
    artifacts.mkdir(exist_ok=True)
    joblib.dump(model, artifacts / "model.joblib")
    (artifacts / "metrics.json").write_text(json.dumps(result, indent=2))

    # Store simple reference statistics for monitoring.
    reference = {
        col: {"mean": float(x_train[col].mean()), "std": float(x_train[col].std() or 1.0)}
        for col in FEATURE_COLUMNS
    }
    (artifacts / "reference_stats.json").write_text(json.dumps(reference, indent=2))

    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
