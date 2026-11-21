import unittest
from unittest.mock import Mock, patch

from src.data.binance_client import BinanceClient


class TestBinanceClient(unittest.TestCase):

    def setUp(self):
        self.client = BinanceClient()

    @patch("src.data.binance_client.requests.Session")
    def test_session_headers(self, mock_session):
        client = BinanceClient()

        mock_session.return_value.headers.update.assert_called_once_with({
            "User-Agent": "Binance-Future-Signal-Bot/1.0"
        })

    @patch("src.data.binance_client.requests.Session")
    def test_get_server_time(self, mock_session):
        mock_response = Mock()
        mock_response.json.return_value = {
            "serverTime": 123456789
        }

        mock_session.return_value.get.return_value = mock_response

        client = BinanceClient()
        result = client.get_server_time()

        self.assertEqual(result["serverTime"], 123456789)

    @patch("src.data.binance_client.requests.Session")
    def test_get_klines(self, mock_session):
        mock_response = Mock()
        mock_response.json.return_value = [[1, 2, 3]]

        mock_session.return_value.get.return_value = mock_response

        client = BinanceClient()
        result = client.get_kline("BTCUSDT", "1m", 100)

        self.assertEqual(result, [[1, 2, 3]])

    @patch("src.data.binance_client.requests.Session")
    def test_api_error(self, mock_session):
        mock_response = Mock()
        mock_response.raise_for_status.side_effect = Exception("API Error")

        mock_session.return_value.get.return_value = mock_response

        client = BinanceClient()

        with self.assertRaises(Exception):
            client.get_server_time()


if __name__ == "__main__":
    unittest.main()