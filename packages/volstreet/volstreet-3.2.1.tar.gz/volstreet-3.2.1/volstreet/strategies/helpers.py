import numpy as np
from attrs import define, field, validators
from volstreet.config import logger
from volstreet.blackscholes import greeks, Greeks
from volstreet.utils.core import time_to_expiry, current_time
from volstreet.utils.data_io import load_json_data, load_combine_save_json_data
from volstreet.dealingroom import (
    Strangle,
    Straddle,
    Option,
    place_option_order_and_notify,
)
from volstreet.angel_interface.active_session import ActiveSession


@define(slots=False)
class DeltaPositionMonitor:
    instrument: Straddle | Strangle = field(
        validator=validators.instance_of((Straddle, Strangle, Option))
    )
    initial_position_info: dict = field(validator=validators.instance_of(dict))
    _call_active_qty = field(validator=validators.instance_of(int))
    _put_active_qty = field(validator=validators.instance_of(int))
    _total_premium = field(validator=validators.instance_of((int, float)))
    underlying_ltp: float = field(
        validator=validators.instance_of((int, float)), repr=False, default=np.nan
    )
    call_ltp: float = field(
        validator=validators.instance_of((int, float)), repr=False, default=np.nan
    )
    put_ltp: float = field(
        validator=validators.instance_of((int, float)), repr=False, default=np.nan
    )
    call_greeks: Greeks = field(init=False, repr=False)
    put_greeks: Greeks = field(init=False, repr=False)
    positional_greeks: Greeks = field(init=False, repr=False)
    exit_triggers: dict[str, bool] = field(
        factory=lambda: {"end_time": False, "qty_breach": False}
    )

    @_call_active_qty.default
    def _call_active_qty_default(self):
        return self.initial_position_info["Initial Qty"] * -1

    @_put_active_qty.default
    def _put_active_qty_default(self):
        return self.initial_position_info["Initial Qty"] * -1

    @_total_premium.default
    def _total_premium_default(self):
        return (
            self.initial_position_info["Initial Qty"]
            * self.initial_position_info["Total Entry Price"]
        )

    @property
    def call_active_qty(self):
        return self._call_active_qty

    @call_active_qty.setter
    def call_active_qty(self, value):
        if value > self._call_active_qty:
            raise ValueError("Call active short qty should only increase.")
        self._call_active_qty = int(value)

    @property
    def put_active_qty(self):
        return self._put_active_qty

    @put_active_qty.setter
    def put_active_qty(self, value):
        if value > self._put_active_qty:
            raise ValueError("Put active short qty should only increase.")
        self._put_active_qty = int(value)

    @property
    def total_premium(self):
        return self._total_premium

    @total_premium.setter
    def total_premium(self, value):
        if value < self._total_premium:
            raise ValueError("Total premium should only increase.")
        self._total_premium = float(value)

    @property
    def mark_to_market(self) -> float | int:
        return (self.call_active_qty * self.call_ltp) + (
            self.put_active_qty * self.put_ltp
        )

    @property
    def pnl(self) -> float | int:
        return self.total_premium + self.mark_to_market

    def update_call_position(self, additional_qty: int, avg_price: float) -> None:
        self.call_active_qty -= additional_qty
        self.total_premium += additional_qty * avg_price

    def update_put_position(self, additional_qty: int, avg_price: float) -> None:
        self.put_active_qty -= additional_qty
        self.total_premium += additional_qty * avg_price

    def update_positional_greeks(self) -> None:
        call_position_greeks: Greeks = self.call_greeks * self.call_active_qty
        put_position_greeks: Greeks = self.put_greeks * self.put_active_qty
        positional_greeks: Greeks = call_position_greeks + put_position_greeks
        self.positional_greeks = positional_greeks

    def recommend_delta_action(
        self,
        straddle: Straddle,
        delta_threshold: float,
        max_qty_shares: int,
    ) -> tuple[Straddle, int, bool] | tuple[None, None, bool]:
        position_delta = self.positional_greeks.delta

        if (
            position_delta >= delta_threshold
        ):  # Net delta is positive, sell the required qty of calls
            qty_to_sell = int((abs(position_delta) - 0) / abs(self.call_greeks.delta))
            instrument_to_sell = straddle.call_option
            breach = (abs(self.call_active_qty) + qty_to_sell) > max_qty_shares
        elif (
            position_delta <= -delta_threshold
        ):  # Net delta is negative, sell the required qty of puts
            qty_to_sell = int((abs(position_delta) - 0) / abs(self.put_greeks.delta))
            instrument_to_sell = straddle.put_option
            breach = (abs(self.put_active_qty) + qty_to_sell) > max_qty_shares
        else:
            return None, None, False

        # Rounding the qty to sell to the nearest lot size and calculating the number of lots
        qty_to_sell = int(qty_to_sell / instrument_to_sell.lot_size)

        return (
            (None, None, False)
            if qty_to_sell == 0
            else (instrument_to_sell, qty_to_sell, breach)
        )

    def neutralize_delta(
        self,
        instrument_to_sell: Option,
        adj_qty_lots: int,
        strategy_tag: str = "",
        notifier_url: str = None,
    ) -> None:
        avg_price = place_option_order_and_notify(
            instrument_to_sell,
            "SELL",
            adj_qty_lots,
            "LIMIT",
            strategy_tag,
            notifier_url,
        )

        qty_in_shares = adj_qty_lots * instrument_to_sell.lot_size

        if instrument_to_sell.option_type.lower().startswith("c"):
            self.update_call_position(qty_in_shares, avg_price)
        elif instrument_to_sell.option_type.lower().startswith("p"):
            self.update_put_position(qty_in_shares, avg_price)
        else:
            raise ValueError("Invalid option type")
        self.update_positional_greeks()
        logger.info(
            f"Delta neutralized by selling {adj_qty_lots} lots of {instrument_to_sell}"
        )

    def exit_positions(self, strategy_tag: str = "", notifier_url: str = None) -> None:
        """Exit all positions."""
        max_combined_qty = min(abs(self.call_active_qty), abs(self.put_active_qty))
        qty_in_lots = int(max_combined_qty / self.instrument.call_option.lot_size)
        place_option_order_and_notify(
            self.instrument,
            "BUY",
            qty_in_lots,
            "LIMIT",
            strategy_tag,
            notifier_url,
        )
        option_to_exit = (
            self.instrument.call_option
            if abs(self.call_active_qty) > abs(self.put_active_qty)
            else self.instrument.put_option
        )
        exit_qty = (
            max(abs(self.call_active_qty), abs(self.put_active_qty)) - max_combined_qty
        )
        exit_qty = int(exit_qty / option_to_exit.lot_size)
        if exit_qty > 0:
            place_option_order_and_notify(
                option_to_exit,
                "BUY",
                exit_qty,
                "LIMIT",
                strategy_tag,
                notifier_url,
            )

    def record_position_status(self):
        """Designed to periodically save the position status to a file."""
        date = current_time().strftime("%Y-%m-%d")
        file_path = f"{ActiveSession.obj.userId}\\{self.instrument.underlying}_delta_data\\{date}.json"

        position_status = {
            "time": current_time().strftime("%Y-%m-%d %H:%M:%S"),
            "underlying_ltp": self.underlying_ltp,
            "call_strike": self.instrument.strike,
            "put_strike": self.instrument.strike,
            "call_ltp": self.call_ltp,
            "put_ltp": self.put_ltp,
            "call_iv": self.call_greeks.iv,
            "put_iv": self.put_greeks.iv,
            "call_delta": self.call_greeks.delta,
            "put_delta": self.put_greeks.delta,
            "positional_delta": self.positional_greeks.delta,
            "call_theta": self.call_greeks.theta,
            "put_theta": self.put_greeks.theta,
            "positional_theta": self.positional_greeks.theta,
            "call_vega": self.call_greeks.vega,
            "put_vega": self.put_greeks.vega,
            "positional_vega": self.positional_greeks.vega,
            "call_gamma": self.call_greeks.gamma,
            "put_gamma": self.put_greeks.gamma,
            "positional_gamma": self.positional_greeks.gamma,
            "call_active_qty": self.call_active_qty,
            "put_active_qty": self.put_active_qty,
            "total_premium": self.total_premium,
            "mark_to_market": self.mark_to_market,
            "pnl": self.pnl,
        }
        load_combine_save_json_data(
            position_status,
            file_path,
        )


def calculate_option_greeks(
    last_traded_prices: tuple[float, float, float],
    instrument: Straddle,
) -> tuple[Greeks, Greeks]:
    # Time to expiry
    tte = time_to_expiry(instrument.expiry)

    underlying_ltp, call_ltp, put_ltp = last_traded_prices

    call_iv, put_iv, _ = instrument.fetch_ivs(
        spot=underlying_ltp, prices=(call_ltp, put_ltp)
    )
    call_iv = np.nan if call_iv is None else call_iv
    put_iv = np.nan if put_iv is None else put_iv
    call_greeks = greeks(
        S=underlying_ltp,
        K=instrument.strike,
        t=tte,
        r=0.06,
        sigma=call_iv,
        flag="c",
    )
    put_greeks = greeks(
        S=underlying_ltp,
        K=instrument.strike,
        t=tte,
        r=0.06,
        sigma=put_iv,
        flag="p",
    )

    return call_greeks, put_greeks


def calculate_position_greeks(
    last_traded_prices: tuple[float, float, float],
    position_monitor: DeltaPositionMonitor,
    instrument: Straddle,
) -> tuple[Greeks, Greeks, Greeks]:
    call_greeks, put_greeks = calculate_option_greeks(last_traded_prices, instrument)
    call_position_greeks: Greeks = call_greeks * position_monitor.call_active_qty
    put_position_greeks: Greeks = put_greeks * position_monitor.put_active_qty
    positional_greeks: Greeks = call_position_greeks + put_position_greeks
    return call_greeks, put_greeks, positional_greeks


def load_current_straddle(
    underlying_str, user_id: str, file_appendix: str
) -> Straddle | None:
    """Load current position for a given underlying, user and strategy (file_appendix)."""

    # Loading current position
    trade_data = load_json_data(
        f"{user_id}\\{underlying_str}_{file_appendix}.json",
        default_structure=dict,
    )
    trade_data = trade_data.get(underlying_str, {})
    buy_strike = trade_data.get("strike", None)
    buy_expiry = trade_data.get("expiry", None)
    buy_straddle = (
        Straddle(strike=buy_strike, underlying=underlying_str, expiry=buy_expiry)
        if buy_strike is not None and buy_expiry is not None
        else None
    )
    return buy_straddle
