# Project structure

[Main README](README.md) · [All projects](https://github.com/zahramardani/ML2PP-Artifacts/blob/main/PROJECTS.md)

## Code and documentation

| Path | Responsibility |
|---|---|
| [src/generate_data.py](src/generate_data.py) | Reproducible synthetic hourly observations |
| [src/features.py](src/features.py) | Shared feature definitions and chronological split |
| [src/train.py](src/train.py) | XGBoost training, persistence comparison and artifact export |
| [src/api.py](src/api.py) | Request schema, health check and prediction endpoint |
| [src/monitor.py](src/monitor.py) | Local drift, missingness and error helpers |
| [tests/test_pipeline.py](tests/test_pipeline.py) | Forecasting feature and split tests |
| [genai_rag_demo/](genai_rag_demo/) | Small retrieval and tool-routing example |
| [sql/station_analytics/](sql/station_analytics/) | Self-contained SQLite project and tests |
| [sql/forecast_features.sql](sql/forecast_features.sql) | Separate illustrative SQL feature query |
| [deploy/aws/README.md](deploy/aws/README.md) | Proposed AWS component mapping |
| [RECRUITER_QUICKSTART.md](RECRUITER_QUICKSTART.md) | Local walkthrough and sample API request |
| [.github/workflows/ci.yml](.github/workflows/ci.yml) | CI entry point |

## Generated locally

| Path | Produced by | Contents |
|---|---|---|
| `data/sample_timeseries.csv` | `python -m src.generate_data` | Synthetic hourly data |
| `artifacts/model.joblib` | `python -m src.train` | Trained demo model |
| `artifacts/metrics.json` | Training | Actual demo scores and split sizes |
| `artifacts/reference_stats.json` | Training | Training-feature reference statistics |

These generated files and the virtual environment are excluded from version control. Run training from the repository root because the demo uses repository-relative paths.

## Working on each component

Use the SQL project's own standard-library tests for SQL changes. After installing the main requirements, run `pytest -q` for the Python tests. Keep synthetic demonstration outputs separate from research results.

The similarly named [river_prediction1](https://github.com/zahramardani/river_prediction1) repository contains the historical Django application. Its web views are not part of this FastAPI service.
