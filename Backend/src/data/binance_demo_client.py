
import os
import time
import hmac
import hashlib
from urllib import response
from urllib.parse import urlencode

import requests
from dotenv import load_dotenv


class BinanceDemoClient:

    BASE_URL = "https://demo-fapi.binance.com"

    def __init__(self):
        load_dotenv()

        self.time_offset = 0
        self.api_key = os.getenv("BINANCE_API_KEY")
        self.api_secret = os.getenv("BINANCE_API_SECRET")

        configured_url = os.getenv("BINANCE_BASE_URL")

        if configured_url != self.BASE_URL:
            raise ValueError(
                "Only Binance Demo API is allowed."
            )

        if not self.api_key or not self.api_secret:
            raise ValueError(
                "Binance API credentials are missing."
            )

        self.session = requests.Session()
        self.session.headers.update({
            "X-MBX-APIKEY": self.api_key,
            "User-Agent": "Binance-Futures-Bot/1.0"
        })

    def sync_time(self):
        response = self.session.get(
            f"{self.BASE_URL}/fapi/v1/time",
            timeout=10
        )
        response.raise_for_status()

        server_time = response.json()["serverTime"]
        local_time = int(time.time() * 1000)

        self.time_offset = server_time - local_time

        print("Time synchronized. Offset:", self.time_offset, "ms")

    def signed_get(self, endpoint, params=None):

        if params is None:
            params = {}

        params["timestamp"] = int(time.time() * 1000) + self.time_offset
        params["recvWindow"] = 5000

        query_string = urlencode(params)

        signature = hmac.new(
            self.api_secret.encode("utf-8"),
            query_string.encode("utf-8"),
            hashlib.sha256
        ).hexdigest()

        url = (
            f"{self.BASE_URL}{endpoint}"
            f"?{query_string}&signature={signature}"
        )

        response = self.session.get(url, timeout=10)
        if not response.ok:
            raise RuntimeError(
                f"HTTP {response.status_code}: {response.text}"
            )
    
        return response.json()

    def get_balance(self):

        return self.signed_get("/fapi/v3/balance")


    def get_mark_price(self, symbol):

        response = self.session.get(
            f"{self.BASE_URL}/fapi/v1/premiumIndex",
            params={"symbol": symbol},
            timeout=10
        )

        response.raise_for_status()
        return response.json()

    def get_symbol_info(self, symbol):

        response = self.session.get(
            f"{self.BASE_URL}/fapi/v1/exchangeInfo",
            timeout=10
        )

        response.raise_for_status()

        data = response.json()

        for item in data["symbols"]:
            if item["symbol"] == symbol:
                return item

        raise ValueError(f"Symbol not found: {symbol}")

    
    def signed_post(self, endpoint, params=None):

        if params is None:
            params = {}

        params["timestamp"] = int(time.time() * 1000) + self.time_offset
        params["recvWindow"] = 5000

        query_string = urlencode(params)

        signature = hmac.new(
            self.api_secret.encode("utf-8"),
            query_string.encode("utf-8"),
            hashlib.sha256
        ).hexdigest()

        url = (
            f"{self.BASE_URL}{endpoint}"
            f"?{query_string}&signature={signature}"
        )

        response = self.session.post(url, timeout=10)
        response.raise_for_status()

        return response.json()

    def set_leverage(self, symbol, leverage=1):

        return self.signed_post(
            "/fapi/v1/leverage",
            {
                "symbol": symbol,
                "leverage": leverage
            }
        )

    def place_market_order(self, symbol, side, quantity):

        if symbol != "BTCUSDT":
            raise ValueError("Only BTCUSDT is allowed in this test.")

        if side not in ("BUY", "SELL"):
            raise ValueError("Invalid order side.")

        if quantity != "0.001":
            raise ValueError("Only 0.001 BTC is allowed in this test.")

        return self.signed_post(
            "/fapi/v1/order",
            {
                "symbol": symbol,
                "side": side,
                "type": "MARKET",
                "quantity": quantity
            }
        )

    def close_btc_position(self, quantity):
        if quantity != "0.001":
            raise ValueError("Only 0.001 BTC close is allowed.")

        return self.signed_post(
            "/fapi/v1/order",
            {
                "symbol": "BTCUSDT",
                "side": "SELL",
                "type": "MARKET",
                "quantity": quantity,
                "reduceOnly": "true"
            }
        )

