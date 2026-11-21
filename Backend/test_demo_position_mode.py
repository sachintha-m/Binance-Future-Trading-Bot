from src.data.binance_demo_client import BinanceDemoClient

client = BinanceDemoClient()
client.sync_time()

try:
    mode = client.signed_get(
        "/fapi/v1/positionSide/dual"
    )

    print("Hedge Mode:", mode["dualSidePosition"])

    if mode["dualSidePosition"]:
        print("Account Mode: Hedge Mode")
    else:
        print("Account Mode: One-way Mode")

except Exception as error:
    print("ERROR:", error)