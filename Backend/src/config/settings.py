from dataclasses import dataclass

@dataclass(frozen=True)
class BotConfig:

    # Trading symbols
    SYMBOLS: tuple = (
        "BTC/USDT:USDT",
        "ETH/USDT:USDT",
        "SOL/USDT:USDT"
    )

    # Timeframes
    ENTRY_TIMEFRAME: str = "1m"
    TREND_TIMEFRAME: str = "5m"

    # Risk management
    STARTING_BALANCE: float = 1000.0
    RISK_PER_TRADE: float = 0.01
    MAX_TRADES_PER_DAY: int = 15
    DAILY_LOSS_LIMIT: float = 0.03

    # Trading costs
    FEE_RATE: float = 0.0005
    SLIPPAGE_RATE: float = 0.0002

    # Trading mode
    PAPER_TRADING: bool = True


config = BotConfig()