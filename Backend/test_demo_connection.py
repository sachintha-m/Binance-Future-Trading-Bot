
from src.data.binance_demo_client import BinanceDemoClient


def main():

    print("Connecting to Binance Futures Demo...")

    try:
        client = BinanceDemoClient()

        balances = client.get_balance()

        print("\nConnection Successful!")
        print("\nFutures Account Balances:")

        for item in balances:
            if item["asset"] == "USDT":
                print("Asset:", item["asset"])
                print("Wallet Balance:", item["balance"])
                print("Available Balance:", item["availableBalance"])

    except Exception as error:
        print("\nConnection Failed!")
        print("Error:", error)


if __name__ == "__main__":
    main()
