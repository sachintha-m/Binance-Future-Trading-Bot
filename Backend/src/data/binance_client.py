import requests

class BinanceClient:

    BASE_URL = "https://fapi.binance.com"

    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            "User-Agent": "Binance-Future-Signal-Bot/1.0"
        })

    def get_server_time(self):
        endpoint = "/fapi/v1/time"

        url = self.BASE_URL + endpoint

        response = self.session.get(url, timeout=10)

        response.raise_for_status()

        return response.json()

    def get_kline(self, symbol, interval, limit=100):
        endpoint = "/fapi/v1/klines"

        url = self.BASE_URL + endpoint

        params = {
            "symbol": symbol,
            "interval": interval,
            "limit": limit
        }

        responce = self.session.get(
            url,
            params=params,
            timeout=10
        )

        responce.raise_for_status()

        return responce.json()