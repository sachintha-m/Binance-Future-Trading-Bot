import unittest

from src.config.settings import config


class TestBotConfig(unittest.TestCase):

    def test_symbols(self):
        self.assertEqual(
            len(config.SYMBOLS),
            3
        )

    def test_timeframes(self):
        self.assertEqual(config.ENTRY_TIMEFRAME, "1m")
        self.assertEqual(config.TREND_TIMEFRAME, "5m")

    def test_starting_balance(self):
        self.assertEqual(config.STARTING_BALANCE, 1000.0)

    def test_risk_per_trade(self):
        self.assertEqual(config.RISK_PER_TRADE, 0.01)

    def test_max_trades_per_day(self):
        self.assertEqual(config.MAX_TRADES_PER_DAY, 15)

    def test_paper_trading(self):
        self.assertTrue(config.PAPER_TRADING)


if __name__ == "__main__":
    unittest.main()