
import unittest
from unittest.mock import MagicMock, patch

from src.execution.order_executor import OrderExecutor


class TestOrderExecutor(unittest.TestCase):

    @patch("src.execution.order_executor.BinanceDemoClient")
    def setUp(self, mock_client_class):
        self.mock_client = mock_client_class.return_value
        self.executor = OrderExecutor()

    def test_existing_position_blocks_entry(self):
        self.executor.get_position = MagicMock(
            return_value={"positionAmt": "0.001"}
        )

        with self.assertRaises(RuntimeError):
            self.executor.execute_entry("BUY")

    def test_invalid_signal_rejected(self):
        with self.assertRaises(ValueError):
            self.executor.execute_entry("HOLD")

    def test_invalid_quantity_rejected(self):
        with self.assertRaises(ValueError):
            self.executor.execute_entry("BUY", "0.002")

    def test_buy_entry(self):
        self.executor.get_position = MagicMock(return_value=None)
        self.mock_client.place_market_order.return_value = {
            "status": "FILLED"
        }

        result = self.executor.execute_entry("BUY")

        self.mock_client.place_market_order.assert_called_once_with(
            "BTCUSDT", "BUY", "0.001"
        )

        self.assertEqual(result["status"], "FILLED")

    def test_sell_entry(self):
        self.executor.get_position = MagicMock(return_value=None)
        self.mock_client.place_market_order.return_value = {
            "status": "FILLED"
        }

        result = self.executor.execute_entry("SELL")

        self.mock_client.place_market_order.assert_called_once_with(
            "BTCUSDT", "SELL", "0.001"
        )

        self.assertEqual(result["status"], "FILLED")

    
    def test_close_long_position(self):
        self.executor.get_position = MagicMock(
            return_value={"positionAmt": "0.001"}
        )

        self.mock_client.signed_post.return_value = {
            "status": "FILLED"
        }

        result = self.executor.close_position()

        self.mock_client.signed_post.assert_called_once_with(
            "/fapi/v1/order",
            {
                "symbol": "BTCUSDT",
                "side": "SELL",
                "type": "MARKET",
                "quantity": "0.001",
                "reduceOnly": "true"
            }
        )

        self.assertEqual(result["status"], "FILLED")

    def test_close_short_position(self):
        self.executor.get_position = MagicMock(
            return_value={"positionAmt": "-0.001"}
        )

        self.mock_client.signed_post.return_value = {
            "status": "FILLED"
        }

        result = self.executor.close_position()

        self.mock_client.signed_post.assert_called_once_with(
            "/fapi/v1/order",
            {
                "symbol": "BTCUSDT",
                "side": "BUY",
                "type": "MARKET",
                "quantity": "0.001",
                "reduceOnly": "true"
            }
        )

        self.assertEqual(result["status"], "FILLED")

    def test_close_without_position(self):
        self.executor.get_position = MagicMock(return_value=None)

        with self.assertRaises(RuntimeError):
            self.executor.close_position()

    def test_close_unexpected_quantity(self):
        self.executor.get_position = MagicMock(
            return_value={"positionAmt": "0.002"}
        )

        with self.assertRaises(ValueError):
            self.executor.close_position()



if __name__ == "__main__":
    unittest.main()
