from src.data.binance_client import BinanceClient

client = BinanceClient()

result = client.get_server_time()

print("BINANCE API CONNECTION")
print("----------------------")
print("Server Time:", result["serverTime"])
print("Connection: SUCCESS")