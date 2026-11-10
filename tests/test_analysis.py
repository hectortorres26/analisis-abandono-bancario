import tempfile
import unittest
from pathlib import Path
import pandas as pd
from src.analysis import load_data, segment_rates, wilson_interval


class BankTests(unittest.TestCase):
    def fixture(self):
        return pd.DataFrame(
            {
                "customer_id": [1, 2],
                "credit_score": [600, 700],
                "country": ["France", "Spain"],
                "gender": ["Female", "Male"],
                "age": [30, 45],
                "tenure": [1, 2],
                "balance": [0.0, 100.0],
                "products_number": [1, 2],
                "credit_card": [1, 0],
                "active_member": [0, 1],
                "estimated_salary": [1000.0, 2000.0],
                "churn": [1, 0],
            }
        )

    def test_identifier_is_not_returned(self):
        with tempfile.TemporaryDirectory() as d:
            p = Path(d) / "bank.csv"
            self.fixture().to_csv(p, index=False)
            self.assertNotIn("customer_id", load_data(p).columns)

    def test_duplicate_identifier_rejected(self):
        with tempfile.TemporaryDirectory() as d:
            p = Path(d) / "bank.csv"
            frame = self.fixture()
            frame["customer_id"] = 1
            frame.to_csv(p, index=False)
            with self.assertRaisesRegex(ValueError, "único"):
                load_data(p)

    def test_invalid_target_rejected(self):
        with tempfile.TemporaryDirectory() as d:
            p = Path(d) / "bank.csv"
            frame = self.fixture()
            frame.loc[0, "churn"] = 2
            frame.to_csv(p, index=False)
            with self.assertRaisesRegex(ValueError, "0 y 1"):
                load_data(p)

    def test_small_segments_suppressed(self):
        frame = pd.DataFrame(
            {"grupo": ["a"] * 30 + ["b"] * 2, "churn": [0] * 15 + [1] * 15 + [1] * 2}
        )
        result = segment_rates(frame, "grupo")
        self.assertEqual(result.segmento.tolist(), ["a"])
        self.assertAlmostEqual(result.tasa.iloc[0], 0.5)
        lower, upper = wilson_interval(15, 30)
        self.assertLess(lower, 0.5)
        self.assertGreater(upper, 0.5)

    def test_wilson_at_boundaries(self):
        self.assertEqual(wilson_interval(0, 30)[0], 0)
        self.assertEqual(wilson_interval(30, 30)[1], 1)


if __name__ == "__main__":
    unittest.main()
