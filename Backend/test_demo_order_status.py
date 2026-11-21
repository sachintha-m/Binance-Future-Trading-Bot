from src.data.binance_demo_client import BinanceDemoClient

client = BinanceDemoClient()
client.sync_time()

symbol = "BTCUSDT"
order_id = 28689024268

try:
    order = client.signed_get(
        "/fapi/v1/order",
        {
            "symbol": symbol,
            "orderId": order_id
        }
    )

    print("\nORDER STATUS")
    print("Order ID:", order["orderId"])
    print("Status:", order["status"])
    print("Side:", order["side"])
    print("Original Quantity:", order["origQty"])
    print("Executed Quantity:", order["executedQty"])
    print("Average Price:", order.get("avgPrice", "N/A"))

    positions = client.signed_get(
        "/fapi/v3/positionRisk",
        {"symbol": symbol}
    )

    print("\nPOSITION")
    for position in positions:
        print("Position Amount:", position["positionAmt"])
        print("Entry Price:", position["entryPrice"])

except Exception as error:
    print("ERROR:", error)