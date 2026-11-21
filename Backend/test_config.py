from src.config.settings import config

print("BOT CONFIGURATION")
print("-----------------")

print("Symbols:", config.SYMBOLS)
print("Entry timeframe:", config.ENTRY_TIMEFRAME)
print("Trend timeframe:", config.TREND_TIMEFRAME)
print("Starting balance:", config.STARTING_BALANCE)
print("Risk per trade:", config.RISK_PER_TRADE)
print("Max trades per day:", config.MAX_TRADES_PER_DAY)
print("Paper trading:", config.PAPER_TRADING)