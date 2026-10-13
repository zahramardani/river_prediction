-- Example SQL feature extraction for hourly forecasting.
-- Demonstrates a leakage-aware feature view: every feature at forecast time t
-- is based on observations available at or before t.

WITH ordered AS (
    SELECT
        timestamp,
        upstream_flow,
        rainfall,
        temperature,
        target_flow,
        LAG(target_flow, 1) OVER (ORDER BY timestamp)  AS target_lag_1,
        LAG(target_flow, 3) OVER (ORDER BY timestamp)  AS target_lag_3,
        LAG(target_flow, 24) OVER (ORDER BY timestamp) AS target_lag_24,
        AVG(target_flow) OVER (
            ORDER BY timestamp
            ROWS BETWEEN 24 PRECEDING AND 1 PRECEDING
        ) AS target_roll_24_mean
    FROM sensor_readings
)
SELECT
    timestamp,
    upstream_flow,
    rainfall,
    temperature,
    target_lag_1,
    target_lag_3,
    target_lag_24,
    target_roll_24_mean
FROM ordered
WHERE target_lag_24 IS NOT NULL
ORDER BY timestamp;
