
from src.data.binance_demo_client import BinanceDemoClient


class OrderExecutor:

    SYMBOL = "BTCUSDT"
    MAX_QUANTITY = "0.001"

    def __init__(self):
        self.client = BinanceDemoClient()
        self.client.sync_time()

    def get_position(self):
        positions = self.client.signed_get(
            "/fapi/v3/positionRisk",
            {"symbol": self.SYMBOL}
        )

        for position in positions:
            amount = float(position["positionAmt"])

            if amount != 0:
                return position

        return None

    def get_order(self, order_id):
        return self.client.signed_get(
            "/fapi/v1/order",
            {
                "symbol": self.SYMBOL,
                "orderId": order_id
            }
        )

    def execute_entry(self, signal, quantity="0.001"):

        if signal not in ("BUY", "SELL"):
            raise ValueError("Invalid trading signal.")

        if quantity != self.MAX_QUANTITY:
            raise ValueError("Only 0.001 BTC is allowed.")

        if self.get_position() is not None:
            raise RuntimeError(
                "An existing BTC position was detected."
            )

        self.client.set_leverage(self.SYMBOL, 1)

        return self.client.place_market_order(
            self.SYMBOL,
            signal,
            quantity
        )

    
    def close_position(self):

        position = self.get_position()

        if position is None:
            raise RuntimeError("No open BTC position.")

        amount = float(position["positionAmt"])

        if abs(amount) != 0.001:
            raise ValueError(
                "Unexpected position quantity. Closing aborted."
            )

        side = "SELL" if amount > 0 else "BUY"

        return self.client.signed_post(
            "/fapi/v1/order",
            {
                "symbol": self.SYMBOL,
                "side": side,
                "type": "MARKET",
                "quantity": self.MAX_QUANTITY,
                "reduceOnly": "true"
            }
        )
