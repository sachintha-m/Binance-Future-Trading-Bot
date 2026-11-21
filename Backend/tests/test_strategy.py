
import unittest
import pandas as pd

from src.strategies.technical_strategy import TechnicalStrategy


class TestTechnicalStrategy(unittest.TestCase):

    def create_dataframe(self, ema9, ema21, rsi, macd, signal):
        return pd.DataFrame({
            "EMA_9": [ema9],
            "EMA_21": [ema21],
            "RSI_14": [rsi],
            "MACD": [macd],
            "MACD_Signal": [signal]
        })

    def test_buy_signal(self):
        df = self.create_dataframe(110, 100, 60, 2, 1)
        self.assertEqual(
            TechnicalStrategy.generate_signal(df), "BUY"
        )

    def test_sell_signal(self):
        df = self.create_dataframe(90, 100, 40, 1, 2)
        self.assertEqual(
            TechnicalStrategy.generate_signal(df), "SELL"
        )

    def test_hold_signal(self):
        df = self.create_dataframe(100, 100, 50, 1, 1)
        self.assertEqual(
            TechnicalStrategy.generate_signal(df), "HOLD"
        )

    def test_buy_requires_all_conditions(self):
        df = self.create_dataframe(110, 100, 60, 1, 2)
        self.assertEqual(
            TechnicalStrategy.generate_signal(df), "HOLD"
        )

    def test_sell_requires_all_conditions(self):
        df = self.create_dataframe(90, 100, 40, 2, 1)
        self.assertEqual(
            TechnicalStrategy.generate_signal(df), "HOLD"
        )


if __name__ == "__main__":
    unittest.main()
