from src.data.market_data import MarketData
from src.indicators.technical import TechnicalIndicators


market = MarketData()

df = market.fetch_ohlcv(
    symbol="BTCUSDT",
    interval="1m",
    limit=100
)

df = TechnicalIndicators.calculate_all(df)

print(df[[
    "close",
    "EMA_9",
    "EMA_21",
    "RSI_14",
    "MACD",
    "MACD_Signal",
    "MACD_Histogram",
    "ATR_14"
]].tail(10))