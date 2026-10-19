# 5-Minute Recruiter Demo — Forecasting to API

**One-line summary:** A small reproducible example of taking time-series data through leakage-aware features, chronological model evaluation, and a REST prediction endpoint.

**Why it matters:** Demonstrates practical Python, time-series forecasting, XGBoost, FastAPI, Docker, automated tests, and basic monitoring concepts. This is a **portfolio demo using generated synthetic data**, not a production deployment or a claim about real river-forecasting accuracy.

## 1. Try it locally

From the root of this repository, with Python 3.11 or newer:

```bash
python -m venv .venv
source .venv/bin/activate       # Windows: .venv\Scripts\activate
pip install -r requirements.txt
python -m src.generate_data
python -m src.train
pytest -q
uvicorn src.api:app --host 127.0.0.1 --port 8000
```

Open [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs) for the interactive API documentation.

The training step creates `artifacts/metrics.json` with **MAE, RMSE, and R²** for an XGBoost model and a persistence baseline; inspect the file to see the actual results, rather than quoting unverified scores.

## 2. Send one prediction

With the API running, use a **second terminal**:

```bash
curl -X POST "http://127.0.0.1:8000/predict" \
  -H "Content-Type: application/json" \
  -d '{
    "upstream_flow": 80,
    "rainfall": 2,
    "temperature": 17,
    "target_lag_1": 76,
    "target_lag_3": 73,
    "target_lag_24": 70,
    "target_roll_24_mean": 74,
    "hour_sin": 0,
    "hour_cos": 1
  }'
```

Expected **response shape** (numerical value depends on the trained model):

```json
{"prediction": 0.0}
```

The number shown above is a shape illustration, **not** a verified forecast.

## 3. Explain the code in five sentences

1. `src/generate_data.py` produces a reproducible **synthetic hourly dataset**.
2. `src/features.py` creates lag-1, lag-3, lag-24 and past-only rolling-mean features.
3. `src/train.py` splits data chronologically and compares a persistence baseline with XGBoost.
4. `src/api.py` validates incoming JSON with Pydantic and serves `POST /predict`.
5. `tests/` and GitHub Actions demonstrate basic checks; `src/monitor.py` contains monitoring helpers.

## 4. Three technical questions to practice

**Q: Why not use a random train/test split?**  
A: In time-series forecasting we must simulate predicting the future from the past. A chronological split makes that separation explicit.

**Q: Why compare with a persistence baseline?**  
A: A more complex model is only worthwhile if it consistently adds value over a simple recent-value prediction.

**Q: How would you improve this for a real system?**  
A: Replace synthetic data with consented real sensor data, validate station alignment and missing periods, use rolling-origin backtesting, confirm that every exogenous input is available **at prediction time**, add stable model loading and monitoring, and only then consider production deployment.

## Scope and limitations

- Synthetic data and demo metrics do **not** represent scientific results from ML2++ or AI4RIVER.
- The example is a **single-step**, tabular XGBoost forecast; it is not a finished multistep river flood-warning system.
- Some inputs in the demo are time-aligned exogenous measurements; a real **future** forecast must use only measurements/forecasts available when the forecast is issued.
- The API is a local demonstration. Authentication, service-level objectives, persistent monitoring and cloud deployment are not implemented end-to-end.
- **Portfolio wording:** “I implemented a compact time-series forecasting and FastAPI/MLOps demo with synthetic data, chronological validation, and a baseline comparison.”

## Next: deeper source code

Start with [src/features.py](src/features.py), then [src/train.py](src/train.py), and finally [src/api.py](src/api.py). The main [README](README.md) covers the optional MLOps and GenAI extensions.
