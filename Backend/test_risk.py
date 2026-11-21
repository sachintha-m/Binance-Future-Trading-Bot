from src.risk.risk_manager import RiskManager

risk = RiskManager()

entry = 60000
atr = 100

stop_loss = risk.calculate_stop_loss(
    entry, atr, "BUY"
)

take_profit = risk.calculate_take_profit(
    entry, stop_loss, "BUY"
)

position_size = risk.calculate_position_size(
    entry, stop_loss
)

print("Balance:", risk.balance)
print("Entry:", entry)
print("Stop Loss:", stop_loss)
print("Take Profit:", take_profit)
print("Position Size:", position_size)