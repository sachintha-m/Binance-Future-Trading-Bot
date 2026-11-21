from src.config.settings import config
from datetime import date
import math

class RiskManager:

    def __init__(self):
        self.balance = config.STARTING_BALANCE
        self.daily_realized_pnl = 0.0
        self.trades_today = 0
        self.current_day = date.today()

    def can_trade(self, trading_day=None):

        self.reset_daily_stats(trading_day)
        daily_loss_limit = (
            self.balance * config.DAILY_LOSS_LIMIT
        )

        if self.daily_realized_pnl <= -daily_loss_limit:
            return False

        if self.trades_today >= config.MAX_TRADES_PER_DAY:
            return False

        return True

    def record_trade(self, pnl: float, trading_day=None):

        self.reset_daily_stats(trading_day)

        self.daily_realized_pnl += pnl
        self.balance += pnl
        self.trades_today += 1

    def reset_daily_stats(self, trading_day=None):

        if trading_day is None:
            trading_day = date.today()

        if trading_day != self.current_day:
            self.daily_realized_pnl = 0.0
            self.trades_today = 0
            self.current_day = trading_day

    def calculate_position_size(
        self,
        entry_price: float,
        stop_loss: float
    ) -> float:

        risk_amount = (
            self.balance * config.RISK_PER_TRADE
        )

        price_difference = abs(
            entry_price - stop_loss
        )

        if price_difference <= 0:
            return 0.0

        position_size = (
            risk_amount / price_difference
        )

        return position_size

    def calculate_stop_loss(
        self,
        entry_price: float,
        atr: float,
        signal: str
    ) -> float:

        distance = atr * 1.5

        if signal == "BUY":
            return entry_price - distance

        if signal == "SELL":
            return entry_price + distance

        return 0.0

    def calculate_take_profit(
        self,
        entry_price: float,
        stop_loss: float,
        signal: str
    ) -> float:

        risk = abs(entry_price - stop_loss)

        reward = risk * 2

        if signal == "BUY":
            return entry_price + reward

        if signal == "SELL":
            return entry_price - reward

        return 0.0

    def validate_trade(
        self,
        signal,
        entry_price,
        stop_loss,
        position_size,
        has_open_trade=False,
        trading_day=None
    ):

        self.reset_daily_stats(trading_day)

        if signal not in ("BUY", "SELL"):
            return False

        if not self.can_trade(trading_day):
            return False

        if has_open_trade:
            return False

        if entry_price <= 0 or position_size <= 0:
            return False

        if signal == "BUY" and stop_loss >= entry_price:
            return False

        if signal == "SELL" and stop_loss <= entry_price:
            return False

        risk_amount = abs(
            entry_price - stop_loss
        ) * position_size

        max_risk = self.balance * config.RISK_PER_TRADE

        if (
            risk_amount > max_risk
            and not math.isclose(
                risk_amount,
                max_risk,
                rel_tol=1e-8
            )
        ):
            return False

        return True