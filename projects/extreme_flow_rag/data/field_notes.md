# Extreme-Flow Sensor Analytics — Demonstration Notes

## Peak events
Peak events can be explored by examining observed maxima and periods above a chosen flow threshold. A threshold must be calibrated to the station and context; 180 m3/s is used here solely to exercise the software and is not a risk threshold.

## Data quality
Before interpreting sensor records, check timestamps, unit consistency, duplicated measurements, gaps and sensor zero values. Do not interpret missing flow readings as zero discharge. Keep chronological order for downstream forecasting.

## Forecasting and validation
For forecasting tasks, separate train, validation and test periods chronologically and compare models against a persistence baseline. Long lead times and rare peak events can increase errors. Peak-focused evaluation should complement overall MAE/RMSE.

## Context and limitations
CONNECT / CONNECT+ research motivates the subject area, but these records are completely synthetic portfolio examples. They are not extracted from historical Portuguese hydrological observations or MOHID simulations. This application does not forecast flow, estimate flood probability, or send alerts.
