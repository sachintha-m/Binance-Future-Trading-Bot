
import unittest
from datetime import date, timedelta

from src.risk.risk_manager import RiskManager
from src.config.settings import config


class TestRiskManager(unittest.TestCase):

    def setUp(self):
        self.risk = RiskManager()
        self.today = date.today()

    # --------------------------------------------------
    # can_trade()
    # --------------------------------------------------

    def test_can_trade_initially(self):
        self.assertTrue(self.risk.can_trade())

    def test_can_trade_after_daily_loss_limit(self):
        loss = -(self.risk.balance * config.DAILY_LOSS_LIMIT)
        self.risk.record_trade(loss)

        self.assertFalse(self.risk.can_trade())

    def test_can_trade_after_max_trades(self):
        self.risk.trades_today = config.MAX_TRADES_PER_DAY

        self.assertFalse(self.risk.can_trade())

    # --------------------------------------------------
    # record_trade()
    # --------------------------------------------------

    def test_record_trade_profit(self):
        self.risk.record_trade(50)

        self.assertEqual(self.risk.balance, 1050)
        self.assertEqual(self.risk.daily_realized_pnl, 50)
        self.assertEqual(self.risk.trades_today, 1)

    def test_record_trade_loss(self):
        self.risk.record_trade(-25)

        self.assertEqual(self.risk.balance, 975)
        self.assertEqual(self.risk.daily_realized_pnl, -25)
        self.assertEqual(self.risk.trades_today, 1)

    # --------------------------------------------------
    # reset_daily_stats()
    # --------------------------------------------------

    def test_reset_daily_stats(self):
        self.risk.record_trade(-20)

        next_day = self.today + timedelta(days=1)
        self.risk.reset_daily_stats(next_day)

        self.assertEqual(self.risk.daily_realized_pnl, 0)
        self.assertEqual(self.risk.trades_today, 0)
        self.assertEqual(self.risk.current_day, next_day)

    def test_reset_same_day_does_not_clear_stats(self):
        self.risk.record_trade(-20)

        self.risk.reset_daily_stats(self.today)

        self.assertEqual(self.risk.daily_realized_pnl, -20)
        self.assertEqual(self.risk.trades_today, 1)

    # --------------------------------------------------
    # calculate_position_size()
    # --------------------------------------------------

    def test_calculate_position_size(self):
        result = self.risk.calculate_position_size(60000, 59850)

        expected = (
            self.risk.balance * config.RISK_PER_TRADE
        ) / 150

        self.assertAlmostEqual(result, expected)

    def test_position_size_zero_distance(self):
        result = self.risk.calculate_position_size(60000, 60000)

        self.assertEqual(result, 0)

    # --------------------------------------------------
    # calculate_stop_loss()
    # --------------------------------------------------

    def test_buy_stop_loss(self):
        result = self.risk.calculate_stop_loss(60000, 100, "BUY")

        self.assertEqual(result, 59850)

    def test_sell_stop_loss(self):
        result = self.risk.calculate_stop_loss(60000, 100, "SELL")

        self.assertEqual(result, 60150)

    def test_invalid_signal_stop_loss(self):
        result = self.risk.calculate_stop_loss(60000, 100, "HOLD")

        self.assertEqual(result, 0)

    # --------------------------------------------------
    # calculate_take_profit()
    # --------------------------------------------------

    def test_buy_take_profit(self):
        result = self.risk.calculate_take_profit(
            60000, 59850, "BUY"
        )

        self.assertEqual(result, 60300)

    def test_sell_take_profit(self):
        result = self.risk.calculate_take_profit(
            60000, 60150, "SELL"
        )

        self.assertEqual(result, 59700)

    def test_invalid_signal_take_profit(self):
        result = self.risk.calculate_take_profit(
            60000, 59850, "HOLD"
        )

        self.assertEqual(result, 0)

    # --------------------------------------------------
    # validate_trade()
    # --------------------------------------------------

    def test_valid_buy_trade(self):
        result = self.risk.validate_trade(
            "BUY", 60000, 59850, 0.0666666667
        )

        self.assertTrue(result)

    def test_valid_sell_trade(self):
        result = self.risk.validate_trade(
            "SELL", 60000, 60150, 0.0666666667
        )

        self.assertTrue(result)

    def test_invalid_signal(self):
        result = self.risk.validate_trade(
            "HOLD", 60000, 59850, 0.06
        )

        self.assertFalse(result)

    def test_invalid_entry_price(self):
        result = self.risk.validate_trade(
            "BUY", 0, -100, 0.06
        )

        self.assertFalse(result)

    def test_invalid_position_size(self):
        result = self.risk.validate_trade(
            "BUY", 60000, 59850, 0
        )

        self.assertFalse(result)

    def test_invalid_buy_stop_loss(self):
        result = self.risk.validate_trade(
            "BUY", 60000, 60100, 0.06
        )

        self.assertFalse(result)

    def test_invalid_sell_stop_loss(self):
        result = self.risk.validate_trade(
            "SELL", 60000, 59900, 0.06
        )

        self.assertFalse(result)

    def test_excessive_risk(self):
        result = self.risk.validate_trade(
            "BUY", 60000, 59850, 1
        )

        self.assertFalse(result)

    def test_has_open_trade(self):
        result = self.risk.validate_trade(
            "BUY", 60000, 59850, 0.06,
            has_open_trade=True
        )

        self.assertFalse(result)

    def test_historical_day_loss_limit(self):
        historical_day = self.today - timedelta(days=1)

        self.risk.current_day = historical_day
        self.risk.daily_realized_pnl = -30
        self.risk.balance = 970
        self.risk.trades_today = 1

        result = self.risk.validate_trade(
            "BUY",
            60000,
            59850,
            0.06,
            trading_day=historical_day
        )

        self.assertFalse(result)


if __name__ == "__main__":
    unittest.main()
