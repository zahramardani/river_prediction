"""Executable tests for SQL joins, missing dates and no-lookahead features."""
import unittest
from run_demo import load_queries, make_database


class StationAnalyticsTests(unittest.TestCase):
    def setUp(self):
        self.db = make_database()
        self.queries = load_queries()

    def tearDown(self):
        self.db.close()

    def fetch(self, name):
        return [dict(row) for row in self.db.execute(self.queries[name])]

    def test_join_and_aggregates(self):
        self.assertEqual(len(self.fetch("join_flow_weather")), 20)
        counts = {r["station_name"]: r["observed_days"] for r in self.fetch("summary_by_station")}
        self.assertEqual(counts["Abrantes (synthetic)"], 6)
        self.assertEqual(len(self.fetch("latest_measurement")), 3)

    def test_calendar_detects_gap(self):
        self.assertEqual(self.fetch("missing_station_days"), [
            {"station_name": "Abrantes (synthetic)", "missing_date": "2026-01-04"}
        ])

    def test_lags_are_past_only_and_gap_aware(self):
        features = self.fetch("point_in_time_features")
        almourol_day_4 = next(r for r in features if r["station_id"] == 1 and r["observed_date"] == "2026-01-04")
        self.assertEqual(almourol_day_4["lag_1_day"], 95)
        self.assertEqual(almourol_day_4["lag_3_days"], 75)
        self.assertEqual(almourol_day_4["past_3_day_mean"], round((75 + 80 + 95) / 3, 2))
        abrantes_day_5 = next(r for r in features if r["station_id"] == 2 and r["observed_date"] == "2026-01-05")
        self.assertIsNone(abrantes_day_5["lag_1_day"])
        self.assertIsNone(abrantes_day_5["past_3_day_mean"])

    def test_changing_today_target_does_not_change_todays_features(self):
        def selected_features():
            return next(r for r in self.fetch("point_in_time_features") if r["station_id"] == 1 and r["observed_date"] == "2026-01-05")
        before = selected_features()
        self.db.execute("UPDATE daily_flow SET flow_m3s=999 WHERE station_id=1 AND observed_date='2026-01-05'")
        after = selected_features()
        for key in ("lag_1_day", "lag_3_days", "past_3_day_mean"):
            self.assertEqual(before[key], after[key])

    def test_chronological_split(self):
        counts = {r["split"]: r["observation_count"] for r in self.fetch("chronological_split_counts")}
        self.assertEqual(counts, {"test": 6, "train": 14})


if __name__ == "__main__":
    unittest.main()
