
from src.data.binance_demo_client import BinanceDemoClient


client = BinanceDemoClient()
client.sync_time()

print("BINANCE FUTURES DEMO - MARKET ORDER TEST")
print("----------------------------------------")

symbol = "BTCUSDT"
quantity = "0.001"

try:
    # Check existing position first
    positions = client.signed_get(
        "/fapi/v3/positionRisk",
        {"symbol": symbol}
    )

    for position in positions:
        if float(position["positionAmt"]) != 0:
            raise RuntimeError(
                "Existing BTCUSDT position detected. "
                "Close or inspect it before testing."
            )

    print("Symbol:", symbol)
    print("Quantity:", quantity)

    side = input("Enter BUY or SELL: ").strip().upper()

    if side not in ("BUY", "SELL"):
        raise ValueError("Invalid side.")

    confirmation = input(
        f"Place {side} MARKET order for {quantity} BTC? Type YES: "
    )

    if confirmation != "YES":
        print("Order cancelled.")
        raise SystemExit

    leverage = client.set_leverage(symbol, 1)
    print("Leverage configured:", leverage["leverage"])

    order = client.place_market_order(
        symbol,
        side,
        quantity
    )

    print("\nORDER RESPONSE")
    print("Order ID:", order["orderId"])
    print("Status:", order["status"])
    print("Executed Quantity:", order["executedQty"])
    print("Average Price:", order["avgPrice"])

except Exception as error:
    print("\nTEST FAILED:", error)
