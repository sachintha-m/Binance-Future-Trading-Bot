import pandas as pd

from src.config.settings import config
from src.strategies.technical_strategy import TechnicalStrategy
from src.risk.risk_manager import RiskManager


class BacktestEngine:

    def __init__(self):

        self.risk_manager = RiskManager()

        self.trades = []

        self.balance = config.STARTING_BALANCE

    def check_exit(
        self,
        candle,
        signal,
        stop_loss,
        take_profit
    ):

        if signal == "BUY":

            sl_hit = candle["low"] <= stop_loss
            tp_hit = candle["high"] >= take_profit

        else:

            sl_hit = candle["high"] >= stop_loss
            tp_hit = candle["low"] <= take_profit

        # Conservative assumption: SL first
        if sl_hit:
            return stop_loss, "STOP_LOSS"

        if tp_hit:
            return take_profit, "TAKE_PROFIT"

        return None, None

    def calculate_pnl(
        self,
        signal,
        entry_price,
        exit_price,
        position_size
    ):

        if signal == "BUY":
            gross_pnl = (
                exit_price - entry_price
            ) * position_size

        else:
            gross_pnl = (
                entry_price - exit_price
            ) * position_size

        fee = (
            entry_price + exit_price
        ) * position_size * config.FEE_RATE

        slippage = (
            entry_price + exit_price
        ) * position_size * config.SLIPPAGE_RATE

        net_pnl = gross_pnl - fee - slippage

        return net_pnl

    def run(self, df: pd.DataFrame):

        self.trades = []
        self.balance = config.STARTING_BALANCE
        self.risk_manager = RiskManager()

        open_trade = None

        for index in range(1, len(df)):

            candle = df.iloc[index]

            # Manage an existing trade
            if open_trade is not None:

                exit_price, exit_reason = self.check_exit(
                    candle,
                    open_trade["signal"],
                    open_trade["stop_loss"],
                    open_trade["take_profit"]
                )

                if exit_price is not None:

                    pnl = self.calculate_pnl(
                        open_trade["signal"],
                        open_trade["entry_price"],
                        exit_price,
                        open_trade["position_size"]
                    )

                    self.balance += pnl

                    self.risk_manager.record_trade(
                        pnl,
                        trading_day=candle["timestamp"].date()
                    )

                    open_trade["exit_price"] = exit_price
                    open_trade["exit_reason"] = exit_reason
                    open_trade["pnl"] = pnl
                    open_trade["balance"] = self.balance

                    self.trades.append(open_trade)

                    open_trade = None

                continue

            # Generate signal using previous candles only
            current_data = df.iloc[:index]

            signal = TechnicalStrategy.generate_signal(
                current_data
            )

            if signal == "HOLD":
                continue

            entry_price = candle["open"]
            atr = current_data.iloc[-1]["ATR_14"]

            stop_loss = self.risk_manager.calculate_stop_loss(
                entry_price, atr, signal
            )

            take_profit = self.risk_manager.calculate_take_profit(
                entry_price, stop_loss, signal
            )

            position_size = self.risk_manager.calculate_position_size(
                entry_price, stop_loss
            )

            if not self.risk_manager.validate_trade(
                signal,
                entry_price,
                stop_loss,
                position_size,
                trading_day=candle["timestamp"].date()
            ):
                continue

            open_trade = {
                "signal": signal,
                "entry_price": entry_price,
                "stop_loss": stop_loss,
                "take_profit": take_profit,
                "position_size": position_size,
                "entry_time": candle["timestamp"]
            }

        return self.trades

    def calculate_metrics(self):

        if not self.trades:
            return {
                "total_trades": 0,
                "winning_trades": 0,
                "losing_trades": 0,
                "win_rate": 0.0,
                "net_profit": 0.0,
                "profit_factor": 0.0,
                "final_balance": self.balance
            }

        pnls = [
            trade["pnl"]
            for trade in self.trades
        ]

        winning_trades = [
            pnl for pnl in pnls if pnl > 0
        ]

        losing_trades = [
            pnl for pnl in pnls if pnl < 0
        ]

        gross_profit = sum(winning_trades)
        gross_loss = abs(sum(losing_trades))

        total_trades = len(self.trades)

        win_rate = (
            len(winning_trades) / total_trades
        ) * 100

        profit_factor = (
            gross_profit / gross_loss
            if gross_loss > 0
            else float("inf") if gross_profit > 0 else 0.0
        )

        net_profit = sum(pnls)

        return {
            "total_trades": total_trades,
            "winning_trades": len(winning_trades),
            "losing_trades": len(losing_trades),
            "win_rate": round(win_rate, 2),
            "gross_profit": round(gross_profit, 2),
            "gross_loss": round(gross_loss, 2),
            "net_profit": round(net_profit, 2),
            "profit_factor": round(profit_factor, 2),
            "final_balance": round(self.balance, 2)
        }