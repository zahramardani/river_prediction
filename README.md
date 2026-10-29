# Time-Series Forecasting API and Portfolio

A compact Python portfolio project that takes synthetic sensor data through feature engineering, chronological evaluation and a FastAPI prediction endpoint.

**Author:** Zahra Mardani Korani  
[All projects](https://github.com/zahramardani/ML2PP-Artifacts/blob/main/PROJECTS.md) · [Five-minute walkthrough](RECRUITER_QUICKSTART.md) · [Code map](PROJECT_STRUCTURE.md)

## Choose a starting point

| Area | What is implemented | Entry point |
|---|---|---|
| Forecasting | Lag features, chronological split, XGBoost and persistence baseline | [Training pipeline](src/train.py) |
| API | Validated prediction requests and a health endpoint | [FastAPI application](src/api.py) |
| SQL analytics | SQLite schema, joins, CTEs, window functions and gap-aware features | [Runnable SQL project](sql/station_analytics/README.md) |
| Retrieval demonstration | TF-IDF retrieval, prompt construction, deterministic tool routing and lexical support checks | [RAG demonstration](genai_rag_demo/README.md) |
| Monitoring helpers | Missing rates, mean-shift indicators, rolling MAE and retraining recommendations | [Monitoring module](src/monitor.py) |
| Packaging and checks | Docker build, automated tests and CI workflow | [Dockerfile](Dockerfile) · [CI](.github/workflows/ci.yml) |

## Run the forecasting API

From the repository root, using Python 3.11 or newer:

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
python -m src.generate_data
python -m src.train
uvicorn src.api:app --host 127.0.0.1 --port 8000
```

On Windows, activate the environment with `.venv\Scripts\activate`.

Open [the API documentation](http://127.0.0.1:8000/docs). Training writes the model, measured demo metrics and reference statistics into `artifacts/`. See the [walkthrough](RECRUITER_QUICKSTART.md) for a prediction request.

## Run the SQL example without extra dependencies

```bash
python sql/station_analytics/run_demo.py
python -m unittest discover -s sql/station_analytics -p 'test_sql_project.py' -v
```

This example uses Python's standard library and synthetic station records.

## Tests and Docker

After installing the forecasting dependencies:

```bash
pytest -q
docker build -t forecasting-api .
docker run --rm -p 8000:8000 forecasting-api
```

The Docker build generates sample data and trains its own demo model. The [CI workflow](.github/workflows/ci.yml) runs the forecasting pipeline, tests, SQL checks and Docker build.

## Validation and scope

Training, validation and test partitions are chronological. Historical lag and rolling target features use earlier observations. The model also accepts time-aligned upstream flow, rainfall and temperature; a future forecast must supply exogenous inputs available at forecast issuance.

All generated data and metrics here are **portfolio demonstration outputs**. They do not represent the scientific results of ML2++ or AI4RIVER. The API expects prepared feature values; it does not fetch live stations or automatically construct features from an incoming history.

The monitoring functions are local helpers. Managed monitoring, automated retraining and cloud hosting are not implemented by this repository. The [AWS document](deploy/aws/README.md) is an architecture mapping.

## Related work

- [ML2++ research artifacts](https://github.com/zahramardani/ML2PP-Artifacts): research models, datasets, retained evidence and reference workflows.
- [Django river-data prototype](https://github.com/zahramardani/river_prediction1): a separate historical web application.
- [ML2++ RAG Copilot](https://github.com/zahramardani/ML2PP-Artifacts/tree/main/portfolio/ml2pp-rag-copilot): a separate API with optional LLM generation.
