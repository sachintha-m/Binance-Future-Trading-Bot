from src.data.market_data import MarketData
from src.indicators.technical import TechnicalIndicators
from src.backtesting.backtest_engine import BacktestEngine

market = MarketData()

df = market.fetch_ohlcv(
    symbol="BTCUSDT",
    interval="1m",
    limit=1000
)

df = TechnicalIndicators.calculate_all(df)

engine = BacktestEngine()

trades = engine.run(df)

metrics = engine.calculate_metrics()

print("\n===== BACKTEST RESULTS =====")

for key, value in metrics.items():
    print(f"{key}: {value}")