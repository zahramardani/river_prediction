# SQL for Time-Series: River Station Analytics (Portfolio Exercise)

**A small, runnable SQL mini-project inside the existing `river_prediction` repository.** It demonstrates database coursework in an applied forecasting context using SQLite and Python's standard library; no credentials, cloud accounts or external datasets are required.

> All flow and rainfall records are **synthetic teaching data**, NOT real Tejo/Mondego measurements. Built as a GitHub portfolio exercise in October 2026, not presented as prior professional SQL employment.

## Why this project?

A forecasting engineer must often use SQL to join station measurements to metadata/weather, check data coverage, retrieve the newest readings, and create time-aware model features. This example is small enough to explain in an interview but includes important correctness checks.

## Run it (Python 3.10+)

From the **repository root**:

```bash
python sql/station_analytics/run_demo.py
python -m unittest discover -s sql/station_analytics -p 'test_sql_project.py' -v
```

No `pip install` is required for this mini-project.

## What's inside?

| File | Purpose |
| --- | --- |
| `schema.sql` | Normalized tables, primary/foreign keys, CHECK constraints and an index |
| `seed.sql` | 3 synthetic stations, 20 daily flow measurements, 14 weather observations; one intentional missing day |
| `queries.sql` | Six named executable SQL analytics questions |
| `run_demo.py` | Build the SQLite database in memory and print query results |
| `test_sql_project.py` | Five automated tests including gap detection and anti-leakage checks |

## Six queries to explain in an interview

1. **JOIN:** combine station ID/name, daily flow and matching basin rainfall.
2. **GROUP BY:** compute observation count, mean and maximum flow by station.
3. **CTE + `ROW_NUMBER()`:** get the most recent measurement for every station.
4. **Window `LAG` + moving average:** generate daily lag and rolling features using only **earlier** flow values.
5. **Recursive CTE + LEFT JOIN:** find missing station dates.
6. **Date-based split:** count train/test observations without random shuffling.

## Important forecasting caveats

- A missing measurement must **not** be treated as yesterday's flow. The feature query checks elapsed **calendar days** before allowing lag values.
- The three-day rolling mean only appears when there are three contiguous prior daily observations; otherwise it returns `NULL`.
- `lag_1_day`, `lag_3_days` and historical rolling features are valid only if historical measurements would have been available **when the forecast is issued**.
- Rainfall in the JOIN example is observed rainfall. For a genuine forecast of a future date, use only forecasts or observations available at issuance time, not future measured rainfall.
- This is an **illustrative dataset** and does not establish model performance, operational deployment or extensive production SQL experience.

## Interview-ready English explanation

> I completed Database Systems and Advanced Database Systems coursework. To demonstrate my practical SQL knowledge, I added a reproducible SQLite project to my time-series portfolio. It uses joins, aggregations, CTEs, window functions and gap-aware lag features for synthetic river-station data, with Python unit tests to check data quality and avoid look-ahead leakage.

**Link to main project:** [Time-Series Forecasting & MLOps](../../README.md).
