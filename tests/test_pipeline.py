import pandas as pd

from src.features import FEATURE_COLUMNS, build_features, chronological_split
from src.monitor import missing_rate, retraining_recommendation, rolling_mae


def sample_frame(n=80):
    ts = pd.date_range("2026-01-01", periods=n, freq="h")
    return pd.DataFrame(
        {
            "timestamp": ts,
            "upstream_flow": range(n),
            "rainfall": [0.0] * n,
            "temperature": [15.0] * n,
            "target_flow": [20.0 + i * 0.5 for i in range(n)],
        }
    )


def test_feature_generation_and_chronological_split():
    featured = build_features(sample_frame())
    assert set(FEATURE_COLUMNS).issubset(featured.columns)

    train, val, test = chronological_split(featured)
    assert train["timestamp"].max() < val["timestamp"].min()
    assert val["timestamp"].max() < test["timestamp"].min()


def test_monitoring_helpers():
    current = pd.DataFrame({col: [1.0, 2.0] for col in FEATURE_COLUMNS})
    rates = missing_rate(current)
    assert all(v == 0.0 for v in rates.values())
    assert rolling_mae([1, 2], [1, 3]) == 0.5

    result = retraining_recommendation(
        drift_scores={col: 0.1 for col in FEATURE_COLUMNS},
        missing_rates=rates,
        error_ratio_to_baseline=0.9,
    )
    assert result["retrain"] is False
