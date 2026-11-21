from src.data.market_data import MarketData
from src.indicators.technical import TechnicalIndicators
from src.strategies.technical_strategy import TechnicalStrategy

market = MarketData()

df = market.fetch_ohlcv(
    symbol="BTCUSDT",
    interval="1m",
    limit=100
)

df = TechnicalIndicators.calculate_all(df)

signal = TechnicalStrategy.generate_signal(df)

print("BTCUSDT Signal:", signal)