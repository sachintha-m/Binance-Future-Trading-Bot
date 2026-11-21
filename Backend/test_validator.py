from src.risk.risk_manager import RiskManager

risk = RiskManager()

tests = [
    ("Valid BUY", "BUY", 60000, 59850, 0.0666666667, False),
    ("Invalid SL", "BUY", 60000, 60100, 0.05, False),
    ("Invalid Signal", "HOLD", 60000, 59850, 0.05, False),
    ("Open Trade", "BUY", 60000, 59850, 0.05, True),
    ("Excess Risk", "BUY", 60000, 59850, 0.10, False),
]

for name, signal, entry, sl, size, opened in tests:

    result = risk.validate_trade(
        signal=signal,
        entry_price=entry,
        stop_loss=sl,
        position_size=size,
        has_open_trade=opened
    )

    print(f"{name}: {result}")