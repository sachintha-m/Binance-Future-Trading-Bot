from src.data.binance_demo_client import BinanceDemoClient

client = BinanceDemoClient()
client.sync_time()

try:
    order = client.signed_get(
        "/fapi/v1/order",
        {
            "symbol": "BTCUSDT",
            "orderId": 28689036059
        }
    )

    print("\nCLOSE ORDER STATUS")
    print("Order ID:", order["orderId"])
    print("Status:", order["status"])
    print("Executed:", order["executedQty"])
    print("Average Price:", order.get("avgPrice", "N/A"))

    positions = client.signed_get(
        "/fapi/v3/positionRisk",
        {"symbol": "BTCUSDT"}
    )

    print("\nCURRENT POSITION")

    for p in positions:
        print("Position Amount:", p["positionAmt"])
        print("Entry Price:", p["entryPrice"])

except Exception as error:
    print("ERROR:", error)