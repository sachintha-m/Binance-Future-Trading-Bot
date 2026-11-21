import pandas as pd

class TechnicalIndicators:

    @staticmethod
    def ema(data: pd.Series, period: int) -> pd.Series:
        """
        Calculate Exponential Moving Average.
        """

        return data.ewm(
            span=period,
            adjust=False
        ).mean()

    
    @staticmethod
    def rsi(data: pd.Series, period: int = 14) -> pd.Series:
        """
        Calculate Relative Strength Index.
        """

        delta = data.diff()

        gain = delta.clip(lower=0)
        loss = -delta.clip(upper=0)

        avg_gain = gain.ewm(
            alpha=1 / period,
            min_periods=period,
            adjust=False
        ).mean()

        avg_loss = loss.ewm(
            alpha=1 / period,
            min_periods=period,
            adjust=False
        ).mean()

        rs = avg_gain / avg_loss

        rsi = 100 - (100 / (1 + rs))

        return rsi

    @staticmethod
    def macd(data: pd.Series):
        """
        Calculate MACD, Signal Line and Histogram.
        """

        ema_12 = data.ewm(
            span=12,
            adjust=False
        ).mean()

        ema_26 = data.ewm(
            span=26,
            adjust=False
        ).mean()

        macd_line = ema_12 - ema_26

        signal_line = macd_line.ewm(
            span=9,
            adjust=False
        ).mean()

        histogram = macd_line - signal_line

        return macd_line, signal_line, histogram

    @staticmethod
    def atr(df: pd.DataFrame, period: int = 14) -> pd.Series:
        """
        Calculate Average True Range.
        """

        high_low = df["high"] - df["low"]

        high_close = (
            df["high"] - df["close"].shift(1)
        ).abs()

        low_close = (
            df["low"] - df["close"].shift(1)
        ).abs()

        true_range = pd.concat(
            [high_low, high_close, low_close],
            axis=1
        ).max(axis=1)

        atr = true_range.ewm(
            alpha=1 / period,
            min_periods=period,
            adjust=False
        ).mean()

        return atr

    @staticmethod
    def calculate_all(df: pd.DataFrame) -> pd.DataFrame:

        df = df.copy()

        df["EMA_9"] = TechnicalIndicators.ema(
            df["close"], 9
        )

        df["EMA_21"] = TechnicalIndicators.ema(
            df["close"], 21
        )

        df["RSI_14"] = TechnicalIndicators.rsi(
            df["close"], 14
        )

        (
            df["MACD"],
            df["MACD_Signal"],
            df["MACD_Histogram"]
        ) = TechnicalIndicators.macd(df["close"])

        df["ATR_14"] = TechnicalIndicators.atr(
            df, 14
        )

        return df