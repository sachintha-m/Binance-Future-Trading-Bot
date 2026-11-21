from src.data.market_data import MarketData

market = MarketData()

df = market.fetch_ohlcv(
    symbol="BTCUSDT",
    interval="1m",
    limit=10
)

print("\nBTCUSDT MARKET DATA")
print("-------------------")

print(df[[
    "timestamp",
    "open",
    "high",
    "low",
    "close",
    "volume"
]])

print("\nTotal candles:", len(df))
print("Data type:", type(df))
