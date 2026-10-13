from pathlib import Path
import numpy as np
import pandas as pd


def main() -> None:
    rng = np.random.default_rng(42)
    periods = 24 * 120
    ts = pd.date_range("2025-01-01", periods=periods, freq="h")
    hour = ts.hour.to_numpy()
    day = np.arange(periods) / 24.0

    upstream = 80 + 12 * np.sin(2 * np.pi * hour / 24) + 5 * np.sin(2 * np.pi * day / 14)
    rain = np.maximum(0, rng.gamma(1.2, 1.8, periods) - 1.2)
    temperature = 15 + 7 * np.sin(2 * np.pi * (hour - 8) / 24) + rng.normal(0, 0.8, periods)
    target = (
        25
        + 0.72 * upstream
        + 1.8 * np.roll(rain, 3)
        - 0.25 * temperature
        + rng.normal(0, 2.0, periods)
    )
    target[:3] = target[3]

    df = pd.DataFrame(
        {
            "timestamp": ts,
            "upstream_flow": upstream,
            "rainfall": rain,
            "temperature": temperature,
            "target_flow": target,
        }
    )

    out = Path("data")
    out.mkdir(exist_ok=True)
    df.to_csv(out / "sample_timeseries.csv", index=False)
    print(f"Wrote {len(df)} rows to data/sample_timeseries.csv")


if __name__ == "__main__":
    main()
