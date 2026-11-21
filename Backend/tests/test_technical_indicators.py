import unittest
import pandas as pd

from src.indicators.technical import TechnicalIndicators


class TestTechnicalIndicators(unittest.TestCase):

    def setUp(self):
        self.indicators = TechnicalIndicators()

        self.close = pd.Series(
            [10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20],
            dtype=float
        )

        self.df = pd.DataFrame({
            "open": self.close,
            "high": self.close + 1,
            "low": self.close - 1,
            "close": self.close,
            "volume": [100] * len(self.close)
        })

    def test_ema(self):
        result = self.indicators.ema(self.close, 9)

        self.assertEqual(len(result), len(self.close))
        self.assertFalse(result.isna().all())

    def test_rsi(self):
        result = self.indicators.rsi(self.close, 14)

        self.assertEqual(len(result), len(self.close))
        self.assertTrue(result.dropna().between(0, 100).all())

    def test_macd(self):
        macd, signal, histogram = self.indicators.macd(self.close)

        self.assertEqual(len(macd), len(self.close))
        self.assertEqual(len(signal), len(self.close))
        self.assertEqual(len(histogram), len(self.close))

    def test_atr(self):
        result = self.indicators.atr(self.df, 14)

        self.assertEqual(len(result), len(self.df))
        self.assertTrue((result.dropna() >= 0).all())

    def test_calculate_all(self):
        result = self.indicators.calculate_all(self.df)

        expected_columns = [
            "EMA_9",
            "EMA_21",
            "RSI_14",
            "MACD",
            "MACD_Signal",
            "MACD_Histogram",
            "ATR_14"
        ]

        for column in expected_columns:
            self.assertIn(column, result.columns)

    def test_original_dataframe_unchanged(self):
        original = self.df.copy()

        self.indicators.calculate_all(self.df)

        pd.testing.assert_frame_equal(self.df, original)


if __name__ == "__main__":
    unittest.main()