from __future__ import annotations

import json
from pathlib import Path
from typing import Iterable

import numpy as np
import pandas as pd

from src.features import FEATURE_COLUMNS


def load_reference(path: str = "artifacts/reference_stats.json") -> dict:
    return json.loads(Path(path).read_text())


def feature_drift_score(current: pd.DataFrame, reference: dict) -> dict[str, float]:
    """Simple standardized mean-shift indicator for interview/demo purposes."""
    scores: dict[str, float] = {}
    for col in FEATURE_COLUMNS:
        if col not in current.columns:
            scores[col] = float("inf")
            continue
        ref_mean = reference[col]["mean"]
        ref_std = max(reference[col]["std"], 1e-8)
        scores[col] = float(abs(current[col].mean() - ref_mean) / ref_std)
    return scores


def missing_rate(current: pd.DataFrame) -> dict[str, float]:
    return {col: float(current[col].isna().mean()) if col in current else 1.0 for col in FEATURE_COLUMNS}


def rolling_mae(actual: Iterable[float], predicted: Iterable[float]) -> float:
    a = np.asarray(list(actual), dtype=float)
    p = np.asarray(list(predicted), dtype=float)
    if len(a) != len(p) or len(a) == 0:
        raise ValueError("actual and predicted must have the same non-zero length")
    return float(np.mean(np.abs(a - p)))


def retraining_recommendation(
    drift_scores: dict[str, float],
    missing_rates: dict[str, float],
    error_ratio_to_baseline: float | None = None,
) -> dict[str, object]:
    drifted = [k for k, v in drift_scores.items() if v > 1.0]
    bad_missing = [k for k, v in missing_rates.items() if v > 0.05]
    degraded = error_ratio_to_baseline is not None and error_ratio_to_baseline > 1.1

    reasons = []
    if drifted:
        reasons.append(f"feature drift: {', '.join(drifted)}")
    if bad_missing:
        reasons.append(f"missing-data increase: {', '.join(bad_missing)}")
    if degraded:
        reasons.append("forecast error degraded versus reference/baseline")

    return {"retrain": bool(reasons), "reasons": reasons}
