
from src.data.binance_demo_client import BinanceDemoClient


client = BinanceDemoClient()

symbol = "BTCUSDT"

try:
    price_data = client.get_mark_price(symbol)
    symbol_data = client.get_symbol_info(symbol)

    print("Symbol:", symbol)
    print("Mark Price:", price_data["markPrice"])

    print("\nQuantity Rules:")

    for item in symbol_data["filters"]:
        if item["filterType"] in ("LOT_SIZE", "MARKET_LOT_SIZE", "MIN_NOTIONAL"):
            print(item)

except Exception as error:
    print("Error:", error)
