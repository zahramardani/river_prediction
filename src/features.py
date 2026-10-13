from __future__ import annotations

import pandas as pd

FEATURE_COLUMNS = [
    "upstream_flow",
    "rainfall",
    "temperature",
    "target_lag_1",
    "target_lag_3",
    "target_lag_24",
    "target_roll_24_mean",
    "hour_sin",
    "hour_cos",
]


def build_features(df: pd.DataFrame) -> pd.DataFrame:
    data = df.copy()
    data["timestamp"] = pd.to_datetime(data["timestamp"], utc=False)
    data = data.sort_values("timestamp").reset_index(drop=True)

    data["target_lag_1"] = data["target_flow"].shift(1)
    data["target_lag_3"] = data["target_flow"].shift(3)
    data["target_lag_24"] = data["target_flow"].shift(24)
    data["target_roll_24_mean"] = data["target_flow"].shift(1).rolling(24).mean()

    hour = data["timestamp"].dt.hour
    import numpy as np

    data["hour_sin"] = np.sin(2 * np.pi * hour / 24.0)
    data["hour_cos"] = np.cos(2 * np.pi * hour / 24.0)

    return data.dropna().reset_index(drop=True)


def chronological_split(df: pd.DataFrame, train_ratio: float = 0.7, val_ratio: float = 0.15):
    if not 0 < train_ratio < 1 or not 0 < val_ratio < 1 or train_ratio + val_ratio >= 1:
        raise ValueError("Invalid split ratios")

    n = len(df)
    train_end = int(n * train_ratio)
    val_end = int(n * (train_ratio + val_ratio))
    return df.iloc[:train_end], df.iloc[train_end:val_end], df.iloc[val_end:]
