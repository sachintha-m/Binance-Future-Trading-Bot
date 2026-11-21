from datetime import date, timedelta

from src.risk.risk_manager import RiskManager

risk = RiskManager()

day1 = date(2026, 11, 19)
day2 = date(2026, 11, 20)

risk.record_trade(-20, day1)

print("Day 1 PnL:", risk.daily_realized_pnl)

risk.record_trade(-5, day2)

print("Day 2 PnL:", risk.daily_realized_pnl)
print("Balance:", risk.balance)
print("Trades Today:", risk.trades_today)