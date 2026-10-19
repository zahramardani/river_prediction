-- name: join_flow_weather
-- JOIN station metadata and matching basin rainfall on the observation date.
SELECT s.station_name, f.observed_date, f.flow_m3s, w.rainfall_mm
FROM daily_flow AS f
JOIN stations AS s ON s.station_id = f.station_id
LEFT JOIN daily_weather AS w ON w.basin = s.basin AND w.observed_date = f.observed_date
ORDER BY s.station_id, f.observed_date;

-- name: summary_by_station
-- GROUP BY and aggregates for quick quality/coverage analysis.
SELECT s.station_name, COUNT(f.flow_m3s) AS observed_days,
       ROUND(AVG(f.flow_m3s), 2) AS average_flow,
       MAX(f.flow_m3s) AS peak_flow
FROM stations AS s
LEFT JOIN daily_flow AS f ON f.station_id = s.station_id
GROUP BY s.station_id, s.station_name
ORDER BY s.station_id;

-- name: latest_measurement
-- ROW_NUMBER to find exactly one newest record per station.
WITH ranked AS (
    SELECT f.station_id, s.station_name, f.observed_date, f.flow_m3s,
           ROW_NUMBER() OVER (PARTITION BY f.station_id ORDER BY f.observed_date DESC) AS rn
    FROM daily_flow AS f
    JOIN stations AS s ON s.station_id = f.station_id
)
SELECT station_id, station_name, observed_date, flow_m3s
FROM ranked WHERE rn = 1 ORDER BY station_id;

-- name: point_in_time_features
-- Build lag-1 and lag-3 (strict DAILY spacing), and a past-only 3-day mean.
-- Today's flow is excluded from all features; gaps produce NULL rather than fake daily lags.
WITH history AS (
    SELECT station_id, observed_date, flow_m3s,
           LAG(flow_m3s, 1) OVER win AS previous_1,
           LAG(observed_date, 1) OVER win AS previous_1_date,
           LAG(flow_m3s, 3) OVER win AS previous_3,
           LAG(observed_date, 3) OVER win AS previous_3_date,
           AVG(flow_m3s) OVER (
              PARTITION BY station_id ORDER BY observed_date
              ROWS BETWEEN 3 PRECEDING AND 1 PRECEDING
           ) AS past_3_observation_mean
    FROM daily_flow
    WINDOW win AS (PARTITION BY station_id ORDER BY observed_date)
)
SELECT station_id, observed_date, flow_m3s AS target_flow,
       CASE WHEN julianday(observed_date) - julianday(previous_1_date) = 1
            THEN previous_1 END AS lag_1_day,
       CASE WHEN julianday(observed_date) - julianday(previous_3_date) = 3
            THEN previous_3 END AS lag_3_days,
       CASE WHEN julianday(observed_date) - julianday(previous_3_date) = 3
            THEN ROUND(past_3_observation_mean, 2) END AS past_3_day_mean
FROM history ORDER BY station_id, observed_date;

-- name: missing_station_days
-- Recursive CTE builds a date calendar, CROSS JOIN checks all stations.
WITH RECURSIVE calendar(day) AS (
    SELECT '2026-01-01'
    UNION ALL
    SELECT date(day, '+1 day') FROM calendar WHERE day < '2026-01-07'
)
SELECT s.station_name, c.day AS missing_date
FROM stations AS s CROSS JOIN calendar AS c
LEFT JOIN daily_flow AS f ON f.station_id = s.station_id AND f.observed_date = c.day
WHERE f.station_id IS NULL
ORDER BY s.station_id, c.day;

-- name: chronological_split_counts
-- Dates, not random rows, determine train/test assignments.
SELECT CASE WHEN observed_date < '2026-01-06' THEN 'train' ELSE 'test' END AS split,
       COUNT(*) AS observation_count
FROM daily_flow
GROUP BY split ORDER BY split;
