import unittest
from unittest.mock import patch, Mock

import pandas as pd

from src.data.market_data import MarketData


class TestMarketData(unittest.TestCase):

    @patch("src.data.market_data.BinanceClient")
    def setUp(self, mock_client):
        self.mock_client = mock_client.return_value
        self.market = MarketData()

    def test_fetch_ohlcv_returns_dataframe(self):
        self.mock_client.get_kline.return_value = [
            [1795176000000, "60000", "60100", "59900", "60050",
             "10", 1795176059999, "600000", 100, "5", "300000", "0"],
            [1795176060000, "60050", "60200", "60000", "60150",
             "12", 1795176119999, "720000", 120, "6", "360000", "0"]
        ]

        self.mock_client.get_server_time.return_value = {
            "serverTime": 1795176200000
        }

        result = self.market.fetch_ohlcv("BTCUSDT", "1m", 2)

        self.assertIsInstance(result, pd.DataFrame)
        self.assertEqual(len(result), 2)

    def test_numeric_columns(self):
        self.mock_client.get_kline.return_value = [
            [1795176000000, "60000", "60100", "59900", "60050",
             "10", 1795176059999, "600000", 100, "5", "300000", "0"]
        ]

        self.mock_client.get_server_time.return_value = {
            "serverTime": 1795176200000
        }

        result = self.market.fetch_ohlcv("BTCUSDT", "1m", 1)

        for column in ["open", "high", "low", "close", "volume"]:
            self.assertTrue(
                pd.api.types.is_numeric_dtype(result[column])
            )

    @patch("src.data.market_data.BinanceClient")
    def test_api_error(self, mock_client):
        mock_client.return_value.get_kline.side_effect = Exception("API Error")

        market = MarketData()

        with self.assertRaisesRegex(Exception, "API Error"):
            market.fetch_ohlcv("BTCUSDT", "1m", 10)


if __name__ == "__main__":
    unittest.main()