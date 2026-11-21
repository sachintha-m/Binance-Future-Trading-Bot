import pandas as pd

from src.data.binance_client import BinanceClient

class MarketData:

    COLUMNS = [
        "open_time",
        "open",
        "high",
        "low",
        "close",
        "volume",
        "close_time",
        "quote_volume",
        "trades",
        "taker_buy_base",
        "taker_buy_quote",
        "ignore"
    ]

    def __init__(self):
        self.client = BinanceClient()

    def fetch_ohlcv(self, symbol, interval, limit=100):

        raw_data = self.client.get_kline(
            symbol=symbol,
            interval=interval,
            limit=limit
        )

        df = pd.DataFrame(
            raw_data,
            columns=self.COLUMNS
        )

        numeric_columns = [
            "open",
            "high",
            "low",
            "close",
            "volume"
        ]

        for column in numeric_columns:
            df[column] = pd.to_numeric(df[column])

        df["timestamp"] = pd.to_datetime(
            df["open_time"],
            unit="ms",
            utc=True
        )

        # Remove the currently forming candle
        server_time = self.client.get_server_time()["serverTime"]

        df = df[df["close_time"] < server_time].copy()

        return df.reset_index(drop=True)