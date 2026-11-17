"""Regression tests for the final Project 2 portfolio decision engine."""

from pathlib import Path
import unittest

import pandas as pd

from Lab_15_portfolio import estimates_from_prices, lowest_risk_mix
from app import run_search


ROOT = Path(__file__).resolve().parents[1]
PRICES = ROOT / "Lab_15_prices.csv"
CPI = ROOT / "ALFRED_CPIAUCSL_vintages.csv"


class Project2EngineTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.prices = pd.read_csv(PRICES)
        cls.sleeves, cls.correlation = estimates_from_prices(cls.prices)

    def test_default_known_answer(self):
        """README headline result must remain reproducible from the committed CSV."""
        result = run_search(self.sleeves, self.correlation, 0.06, 0.10, 0.0)
        self.assertIsNotNone(result)
        self.assertEqual(result["weights"], {"BIL": 0.70, "IEF": 0.0, "LQD": 0.0, "VT": 0.30})
        self.assertAlmostEqual(result["net_return"], 0.0606995967, places=8)
        self.assertAlmostEqual(result["volatility"], 0.0454181353, places=8)
        self.assertAlmostEqual(result["reserve_weight"], 0.70, places=8)

    def test_vt_stress_known_answer_uses_five_percent_grid(self):
        stressed_sleeves = {ticker: values.copy() for ticker, values in self.sleeves.items()}
        stressed_sleeves["VT"]["return"] -= 0.01
        result = run_search(stressed_sleeves, self.correlation, 0.06, 0.10, 0.0)
        self.assertIsNotNone(result)
        self.assertEqual(result["weights"], {"BIL": 0.65, "IEF": 0.0, "LQD": 0.0, "VT": 0.35})
        self.assertAlmostEqual(result["net_return"], 0.0611359340, places=8)
        self.assertAlmostEqual(result["volatility"], 0.0527547108, places=8)

    def test_higher_nonbinding_reserve_floor_keeps_known_answer(self):
        result = run_search(self.sleeves, self.correlation, 0.06, 0.20, 0.0)
        self.assertIsNotNone(result)
        self.assertEqual(result["weights"]["BIL"], 0.70)

    def test_invalid_reserve_floor_is_rejected(self):
        with self.assertRaises(ValueError):
            lowest_risk_mix(self.sleeves, self.correlation, 0.06, {"BIL"}, 1.01)

    def test_cpi_gate_excludes_unpublished_september_observation(self):
        cpi = pd.read_csv(CPI, parse_dates=["Month measured", "Published on"])
        cutoff = pd.Timestamp("2026-09-30")
        available = cpi[cpi["Published on"] <= cutoff]
        self.assertEqual(available.iloc[-1]["Month measured"], pd.Timestamp("2026-08-01"))


if __name__ == "__main__":
    unittest.main(verbosity=2)
