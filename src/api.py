from pathlib import Path

import joblib
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

from src.features import FEATURE_COLUMNS

MODEL_PATH = Path("artifacts/model.joblib")

app = FastAPI(title="Time-Series Forecasting API", version="1.0.0")


class ForecastRequest(BaseModel):
    upstream_flow: float
    rainfall: float = Field(ge=0)
    temperature: float
    target_lag_1: float
    target_lag_3: float
    target_lag_24: float
    target_roll_24_mean: float
    hour_sin: float = Field(ge=-1, le=1)
    hour_cos: float = Field(ge=-1, le=1)


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok" if MODEL_PATH.exists() else "model_missing"}


@app.post("/predict")
def predict(payload: ForecastRequest) -> dict[str, float]:
    if not MODEL_PATH.exists():
        raise HTTPException(status_code=503, detail="Model artifact not found. Run training first.")

    model = joblib.load(MODEL_PATH)
    row = [[getattr(payload, col) for col in FEATURE_COLUMNS]]
    prediction = float(model.predict(row)[0])
    return {"prediction": prediction}
