import pandas as pd


class TechnicalStrategy:

    @staticmethod
    def generate_signal(df: pd.DataFrame) -> str:

        last = df.iloc[-1]

        buy_condition = (
            last["EMA_9"] > last["EMA_21"]
            and last["RSI_14"] > 50
            and last["MACD"] > last["MACD_Signal"]
        )

        sell_condition = (
            last["EMA_9"] < last["EMA_21"]
            and last["RSI_14"] < 50
            and last["MACD"] < last["MACD_Signal"]
        )

        if buy_condition:
            return "BUY"

        if sell_condition:
            return "SELL"

        return "HOLD"