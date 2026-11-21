from src.data.binance_demo_client import BinanceDemoClient

client = BinanceDemoClient()
client.sync_time()

symbol = "BTCUSDT"

try:
    positions = client.signed_get(
        "/fapi/v3/positionRisk",
        {"symbol": symbol}
    )

    position = next(
        (p for p in positions if float(p["positionAmt"]) > 0),
        None
    )

    if position is None:
        print("No BTC Long Position found.")
        raise SystemExit

    amount = float(position["positionAmt"])

    print("Current Position:", amount, "BTC")
    print("Entry Price:", position["entryPrice"])

    if amount != 0.001:
        raise ValueError("Position quantity is not 0.001 BTC. Aborting.")

    confirmation = input(
        "Close this Demo Long Position? Type CLOSE: "
    )

    if confirmation != "CLOSE":
        print("Close cancelled.")
        raise SystemExit

    order = client.close_btc_position("0.001")

    print("\nCLOSE ORDER RESPONSE")
    print("Order ID:", order["orderId"])
    print("Status:", order["status"])
    print("Executed Quantity:", order["executedQty"])

except Exception as error:
    print("ERROR:", error)