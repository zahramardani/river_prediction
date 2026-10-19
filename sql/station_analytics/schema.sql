-- SQLite schema for a SYNTHETIC hydrology time-series portfolio dataset.
PRAGMA foreign_keys = ON;

CREATE TABLE stations (
    station_id INTEGER PRIMARY KEY,
    station_name TEXT NOT NULL,
    basin TEXT NOT NULL,
    country TEXT NOT NULL DEFAULT 'Portugal'
);

CREATE TABLE daily_flow (
    station_id INTEGER NOT NULL,
    observed_date TEXT NOT NULL,       -- ISO 8601: YYYY-MM-DD
    flow_m3s REAL NOT NULL CHECK (flow_m3s >= 0),
    PRIMARY KEY (station_id, observed_date),
    FOREIGN KEY (station_id) REFERENCES stations (station_id)
);

CREATE TABLE daily_weather (
    basin TEXT NOT NULL,
    observed_date TEXT NOT NULL,
    rainfall_mm REAL NOT NULL CHECK (rainfall_mm >= 0),
    PRIMARY KEY (basin, observed_date)
);

CREATE INDEX idx_daily_flow_date ON daily_flow(observed_date);
