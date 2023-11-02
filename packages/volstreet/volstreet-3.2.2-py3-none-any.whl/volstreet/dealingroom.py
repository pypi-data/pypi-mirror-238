import numpy as np
import pandas as pd
from collections import defaultdict
from datetime import time, datetime, timedelta
import requests
from threading import Thread
from fuzzywuzzy import process
import itertools
from time import sleep
from volstreet.config import symbol_df, token_symbol_dict, logger
from volstreet import config
from volstreet.utils import (
    notifier,
    current_time,
    time_to_expiry,
    round_to_nearest,
    parse_symbol,
    splice_orders,
    find_strike,
    check_for_weekend,
    get_symbol_token,
    get_expiry_dates,
    get_base,
    get_lot_size,
    get_available_strikes,
)
from volstreet.exceptions import ScripsLocationError, IntrinsicValueError
from volstreet.decorators import log_errors, timeit
from volstreet.angel_interface import ActiveSession
from volstreet.angel_interface import (
    fetch_ltp,
    fetch_book,
    lookup_and_return,
    place_order,
    cancel_pending_orders,
    modify_open_orders,
)
from volstreet.SmartWebSocketV2 import SmartWebSocketV2
from volstreet import blackscholes as bs


class OptionChains(defaultdict):
    """An object for having option chains for multiple expiries.
    Each expiry is a dictionary with integer default values"""

    def __init__(self):
        super().__init__(lambda: defaultdict(lambda: defaultdict(int)))
        self.underlying_price = None
        self.exp_strike_pairs = []


class PriceFeed(SmartWebSocketV2):
    def __init__(self, webhook_url=None, correlation_id="default"):
        auth_token = ActiveSession.login_data["data"]["jwtToken"]
        feed_token = ActiveSession.obj.getfeedToken()
        api_key = ActiveSession.obj.api_key
        client_code = ActiveSession.obj.userId
        super().__init__(auth_token, api_key, client_code, feed_token)
        self.price_dict = {}
        self.symbol_option_chains = {}
        self.last_update_time = None
        self.iv_log = defaultdict(lambda: defaultdict(dict))
        self.webhook_url = webhook_url
        self.index_option_chains_subscribed = []
        self.correlation_id = correlation_id

    def start_websocket(self, tokens=None, mode=None, exchange_type=None):
        def _subscribe_tokens():
            self.subscribe_tokens(tokens, mode, exchange_type)

        def on_open(wsapp):
            _subscribe_tokens()

        # Assign the callbacks.
        self.on_open = on_open
        self.on_data = self.on_data_handler
        self.on_error = lambda wsapp, error: print(error)
        self.on_close = lambda wsapp: print("Close")
        Thread(target=self.connect).start()

    def subscribe_tokens(self, tokens=None, mode=None, exchange_type=None):
        if tokens is None:
            tokens = ["26000", "26009"]
        if mode is None:
            mode = 1
        if exchange_type is None:
            exchange_type = 1
        token_list = [{"exchangeType": exchange_type, "tokens": tokens}]
        self.subscribe(self.correlation_id, mode, token_list)

    def on_data_handler(self, wsapp, message):
        self.price_dict[message["token"]] = {
            "ltp": message["last_traded_price"] / 100,
            "best_bid": message["best_5_sell_data"][0]["price"] / 100
            if "best_5_sell_data" in message
            else None,
            # 'best_5_sell_data' is not present in 'mode 1' messages
            "best_bid_qty": message["best_5_sell_data"][0]["quantity"]
            if "best_5_sell_data" in message
            else None,
            "best_ask": message["best_5_buy_data"][0]["price"] / 100
            if "best_5_buy_data" in message
            else None,
            "best_ask_qty": message["best_5_buy_data"][0]["quantity"]
            if "best_5_buy_data" in message
            else None,
            "timestamp": datetime.fromtimestamp(
                message["exchange_timestamp"] / 1000
            ).strftime("%H:%M:%S"),
            **message,
        }
        self.last_update_time = current_time()

    def parse_price_dict(self):
        new_price_dict = {
            token_symbol_dict[token]: value for token, value in self.price_dict.items()
        }
        return new_price_dict

    def add_options(self, *underlyings, range_of_strikes=10, expiries=None, mode=1):
        """Adds options for the given underlyings to the symbol_option_chains dictionary.
        Params:
        underlyings is a list of underlying objects not strings
        If expiries is None, then the current, next and month expiry are added.
        If expiries is 'current', then only the current expiry is added.
        If expiries is a dictionary, then the respective expiries for each underlying are added.
        range_of_strikes is the number of strikes to be added on either side of the current price.
        mode is the mode of the websocket connection. 1 for LTP, 3 for full market depth.
        """

        def get_option_tokens(name, strike, expiry):
            _, c_token = get_symbol_token(name, expiry, strike, "CE")
            _, p_token = get_symbol_token(name, expiry, strike, "PE")
            return c_token, p_token

        for underlying in underlyings:
            if expiries is None:
                expiries_list = [
                    underlying.current_expiry,
                    underlying.next_expiry,
                    underlying.month_expiry,
                ]
            elif expiries == "current":
                expiries_list = [underlying.current_expiry]
            else:
                expiries_list = expiries[underlying.name]

            ltp = underlying.fetch_ltp()

            # Creating a OptionChains object for each index
            self.symbol_option_chains[underlying.name] = OptionChains()
            current_strike = find_strike(ltp, underlying.base)
            strike_range = np.arange(
                current_strike - (underlying.base * (range_of_strikes / 2)),
                current_strike + (underlying.base * (range_of_strikes / 2)),
                underlying.base,
            )
            strike_range = map(int, strike_range)
            data = []
            call_token_list, put_token_list = [], []
            for strike, expiry in list(itertools.product(strike_range, expiries_list)):
                try:
                    call_token, put_token = get_option_tokens(
                        underlying.name, strike, expiry
                    )
                    data.append((call_token, put_token))
                    call_token_list, put_token_list = zip(*data)
                    # Appending the expiry-strike pair to the container in OptionChains object
                    self.symbol_option_chains[underlying.name].exp_strike_pairs.append(
                        (expiry, strike)
                    )
                except Exception as e:
                    logger.error(
                        f"Error in fetching tokens for {strike, expiry} for {underlying.name}: {e}"
                    )
                    print(
                        f"Error in fetching tokens for {strike, expiry} for {underlying.name}: {e}"
                    )
                    call_token_list, put_token_list = ["abc"], ["abc"]
                    continue
            token_list = [
                {
                    "exchangeType": 2,
                    "tokens": list(call_token_list) + list(put_token_list),
                }
            ]
            self.subscribe(self.correlation_id, mode, token_list)
            self.index_option_chains_subscribed.append(underlying.name)

    @log_errors
    def update_option_chain(
        self,
        exit_time=(15, 30),
        process_price_iv_log=True,
        market_depth=True,
        calc_iv=True,
        stop_iv_calculation_hours=3,
        n_values=100,
    ):
        while current_time().time() < time(*exit_time):
            self.build_all_option_chains(
                market_depth=market_depth,
                process_price_iv_log=process_price_iv_log,
                calc_iv=calc_iv,
                stop_iv_calculation_hours=stop_iv_calculation_hours,
                n_values=n_values,
            )

    def build_option_chain(
        self,
        index: str,
        expiry: str,
        market_depth: bool = False,
        process_price_iv_log: bool = False,
        calc_iv: bool = False,
        n_values: int = 100,
        stop_iv_calculation_hours: int = 3,
    ):
        parsed_dict = self.parse_price_dict()
        instrument_info = parsed_dict[index]
        spot = instrument_info["ltp"]

        for symbol, info in parsed_dict.items():
            if symbol.startswith(index) and "CE" in symbol and expiry in symbol:
                strike = float(parse_symbol(symbol)[2])
                put_symbol = symbol.replace("CE", "PE")
                put_option = parsed_dict[put_symbol]
                call_price = info["ltp"]
                put_price = put_option["ltp"]

                self.symbol_option_chains[index][expiry][strike][
                    "call_price"
                ] = call_price
                self.symbol_option_chains[index][expiry][strike][
                    "put_price"
                ] = put_price
                self.symbol_option_chains[index].underlying_price = spot

                if calc_iv:
                    time_left_to_expiry = time_to_expiry(expiry)
                    if time_left_to_expiry < stop_iv_calculation_hours / (
                        24 * 365
                    ):  # If time to expiry is less than n hours stop calculating iv
                        if process_price_iv_log:
                            self.process_price_iv_log(
                                index,
                                strike,
                                expiry,
                                call_price,
                                put_price,
                                np.nan,
                                np.nan,
                                np.nan,
                                n_values,
                            )
                        continue
                    call_iv, put_iv, avg_iv = straddle_iv(
                        call_price, put_price, spot, strike, time_left_to_expiry
                    )
                    self.symbol_option_chains[index][expiry][strike][
                        "call_iv"
                    ] = call_iv
                    self.symbol_option_chains[index][expiry][strike]["put_iv"] = put_iv
                    self.symbol_option_chains[index][expiry][strike]["avg_iv"] = avg_iv

                    if process_price_iv_log:
                        self.process_price_iv_log(
                            index,
                            strike,
                            expiry,
                            call_price,
                            put_price,
                            call_iv,
                            put_iv,
                            avg_iv,
                            n_values,
                        )

                if market_depth:
                    self.symbol_option_chains[index][expiry][strike][
                        "call_best_bid"
                    ] = info["best_bid"]
                    self.symbol_option_chains[index][expiry][strike][
                        "call_best_ask"
                    ] = info["best_ask"]
                    self.symbol_option_chains[index][expiry][strike][
                        "put_best_bid"
                    ] = put_option["best_bid"]
                    self.symbol_option_chains[index][expiry][strike][
                        "put_best_ask"
                    ] = put_option["best_ask"]
                    self.symbol_option_chains[index][expiry][strike][
                        "call_best_bid_qty"
                    ] = info["best_bid_qty"]
                    self.symbol_option_chains[index][expiry][strike][
                        "call_best_ask_qty"
                    ] = info["best_ask_qty"]
                    self.symbol_option_chains[index][expiry][strike][
                        "put_best_bid_qty"
                    ] = put_option["best_bid_qty"]
                    self.symbol_option_chains[index][expiry][strike][
                        "put_best_ask_qty"
                    ] = put_option["best_ask_qty"]

    def build_all_option_chains(
        self,
        indices: list[str] | str | None = None,
        expiries: list[list[str]] | list[str] | str | None = None,
        market_depth: bool = False,
        process_price_iv_log: bool = False,
        calc_iv: bool = False,
        n_values: int = 100,
        stop_iv_calculation_hours: int = 3,
    ):
        if indices is None:
            indices = self.index_option_chains_subscribed
        elif isinstance(indices, str):
            indices = [indices]
        else:
            indices = indices
        if expiries is None:
            expiries = [
                set([*zip(*self.symbol_option_chains[index].exp_strike_pairs)][0])
                for index in indices
            ]
        elif isinstance(expiries, str):
            expiries = [[expiries]]
        elif all([isinstance(expiry, str) for expiry in expiries]):
            expiries = [expiries]
        else:
            expiries = expiries

        for index, exps in zip(indices, expiries):
            for expiry in exps:
                self.build_option_chain(
                    index,
                    expiry,
                    market_depth,
                    process_price_iv_log,
                    calc_iv,
                    n_values,
                    stop_iv_calculation_hours,
                )

    def process_price_iv_log(
        self,
        index,
        strike,
        expiry,
        call_ltp,
        put_ltp,
        call_iv,
        put_iv,
        avg_iv,
        n_values,
    ):
        if strike not in self.iv_log[index][expiry]:
            self.iv_log[index][expiry][strike] = {
                "call_ltps": [],
                "put_ltps": [],
                "call_ivs": [],
                "put_ivs": [],
                "total_ivs": [],
                "times": [],
                "count": 0,
                "last_notified_time": current_time(),
            }
        self.iv_log[index][expiry][strike]["call_ltps"].append(
            round_to_nearest(call_ltp, 2)
        )
        self.iv_log[index][expiry][strike]["put_ltps"].append(
            round_to_nearest(put_ltp, 2)
        )
        self.iv_log[index][expiry][strike]["call_ivs"].append(
            round_to_nearest(call_iv, 3)
        )
        self.iv_log[index][expiry][strike]["put_ivs"].append(
            round_to_nearest(put_iv, 3)
        )
        self.iv_log[index][expiry][strike]["total_ivs"].append(
            round_to_nearest(avg_iv, 3)
        )
        self.iv_log[index][expiry][strike]["times"].append(current_time())
        self.iv_log[index][expiry][strike]["count"] += 1

        call_ivs, put_ivs, total_ivs = self.get_recent_ivs(
            index, expiry, strike, n_values
        )

        running_avg_call_iv = sum(call_ivs) / len(call_ivs) if call_ivs else None
        running_avg_put_iv = sum(put_ivs) / len(put_ivs) if put_ivs else None
        running_avg_total_iv = sum(total_ivs) / len(total_ivs) if total_ivs else None

        self.symbol_option_chains[index][expiry][strike].update(
            {
                "running_avg_call_iv": running_avg_call_iv,
                "running_avg_put_iv": running_avg_put_iv,
                "running_avg_total_iv": running_avg_total_iv,
            }
        )

    def get_recent_ivs(self, index, expiry, strike, n_values):
        call_ivs = self.iv_log[index][expiry][strike]["call_ivs"][-n_values:]
        put_ivs = self.iv_log[index][expiry][strike]["put_ivs"][-n_values:]
        total_ivs = self.iv_log[index][expiry][strike]["total_ivs"][-n_values:]
        call_ivs = [*filter(lambda x: x is not None, call_ivs)]
        put_ivs = [*filter(lambda x: x is not None, put_ivs)]
        total_ivs = [*filter(lambda x: x is not None, total_ivs)]
        return call_ivs, put_ivs, total_ivs


class SharedData:
    def __init__(self):
        self.position_data = None
        self.orderbook_data = None
        self.updated_time = None
        self.error_info = None
        self.force_stop = False

    def fetch_data(self):
        try:
            self.position_data = fetch_book("position")
            self.orderbook_data = fetch_book("orderbook")
            self.updated_time = current_time()
        except Exception as e:
            self.position_data = None
            self.orderbook_data = None
            self.error_info = e

    def update_data(self, sleep_time=5, exit_time=(15, 30)):
        while current_time().time() < time(*exit_time) and not self.force_stop:
            self.fetch_data()
            sleep(sleep_time)


class Option:
    def __init__(self, strike: int, option_type: str, underlying: str, expiry: str):
        self.strike = round(int(strike), 0)

        option_type = option_type.upper()
        self.option_type = "CE" if option_type.startswith("C") else "PE"
        self.underlying = underlying.upper()
        self.underlying_symbol, self.underlying_token = get_symbol_token(
            self.underlying
        )
        self.underlying_exchange = (
            "BSE" if self.underlying in ["SENSEX", "BANKEX"] else "NSE"
        )
        self.exchange = "BFO" if self.underlying in ["SENSEX", "BANKEX"] else "NFO"
        self.expiry = expiry.upper()
        self.symbol, self.token = get_symbol_token(
            self.underlying, self.expiry, strike, self.option_type
        )
        self.lot_size = get_lot_size(self.underlying, expiry=self.expiry)
        self.order_id_log = []
        try:
            self.freeze_qty_in_shares = symbol_df[
                symbol_df["SYMBOL"] == self.underlying
            ]["VOL_FRZ_QTY"].values[0]
        except IndexError:
            self.freeze_qty_in_shares = self.lot_size * 20
        self.freeze_qty_in_lots = int(self.freeze_qty_in_shares / self.lot_size)

    def __repr__(self):
        return (
            f"{self.__class__.__name__}(strike={self.strike}, option_type={self.option_type}, "
            f"underlying={self.underlying}, expiry={self.expiry})"
        )

    def __hash__(self):
        return hash((self.strike, self.option_type, self.underlying, self.expiry))

    def __eq__(self, other):
        return (
            self.strike == other.strike
            and self.expiry == other.expiry
            and self.option_type == other.option_type
            and self.underlying == other.underlying
        )

    def __lt__(self, other):
        if isinstance(other, (int, float, np.int32, np.int64, np.float32, np.float64)):
            return self.strike < other
        return self.strike < other.strike

    def __gt__(self, other):
        if isinstance(other, (int, float, np.int32, np.int64, np.float32, np.float64)):
            return self.strike > other
        return self.strike > other.strike

    def __le__(self, other):
        if isinstance(other, (int, float, np.int32, np.int64, np.float32, np.float64)):
            return self.strike <= other
        return self.strike <= other.strike

    def __ge__(self, other):
        if isinstance(other, (int, float, np.int32, np.int64, np.float32, np.float64)):
            return self.strike >= other
        return self.strike >= other.strike

    def __ne__(self, other):
        if isinstance(other, (int, float, np.int32, np.int64, np.float32, np.float64)):
            return self.strike != other
        return self.strike != other.strike

    def __sub__(self, other):
        if isinstance(other, (int, float, np.int32, np.int64, np.float32, np.float64)):
            return self.strike - other
        return self.strike - other.strike

    def __add__(self, other):
        if isinstance(other, (int, float, np.int32, np.int64, np.float32, np.float64)):
            return self.strike + other
        return self.strike + other.strike

    def fetch_symbol_token(self):
        return self.symbol, self.token

    def fetch_ltp(self):
        return fetch_ltp(self.exchange, self.symbol, self.token)

    def underlying_ltp(self):
        return fetch_ltp(
            self.underlying_exchange, self.underlying_symbol, self.underlying_token
        )

    def fetch_iv(
        self,
        spot: float | None = None,
        price: float | None = None,
        t: float | None = None,
        effective_iv: bool = False,
    ):
        spot = spot if spot is not None else self.underlying_ltp()
        t = (
            t
            if t is not None
            else time_to_expiry(self.expiry, effective_time=effective_iv)
        )
        price = price if price is not None else self.fetch_ltp()
        return bs.implied_volatility(
            price,
            spot,
            self.strike,
            t,
            0.05,
            self.option_type,
        )

    def fetch_greeks(self):
        spot = self.underlying_ltp()
        t = time_to_expiry(self.expiry)
        return bs.greeks(
            self.underlying_ltp(),
            self.strike,
            time_to_expiry(self.expiry),
            0.05,
            self.fetch_iv(spot, t),
            self.option_type,
        )

    def simulate_price(
        self,
        atm_iv: float,
        new_spot: float | None = None,
        movement: float | None = None,
        time_delta: float | None = None,
        time_delta_minutes: float | int | None = None,
        effective_iv: bool = False,
        retain_original_iv: bool = False,
        original_spot: float | None = None,
        original_iv: float | None = None,
    ):
        """
        Effective iv should be set to true when the square off is going to be at a higher iv. In other words,
        this is practical when the square off is likely to be after a holiday after taking position.

        IMPORTANT: When effective_iv is set to True, the function automatically assumes that the square off is going
        to happen at the next trading day after the holiday/weekend. So ensure you are not double calculating the
        holiday/weekend effect.
        """

        original_time_to_expiry = time_to_expiry(
            self.expiry, effective_time=effective_iv
        )
        original_spot = (
            original_spot if original_spot is not None else self.underlying_ltp()
        )
        original_iv = (
            original_iv
            if original_iv is not None
            else self.fetch_iv(spot=original_spot, t=original_time_to_expiry)
        )

        simulated_price = bs.simulate_price(
            strike=self.strike,
            flag=self.option_type,
            original_atm_iv=atm_iv,
            original_iv=original_iv,
            original_spot=original_spot,
            original_time_to_expiry=original_time_to_expiry,
            movement=movement,
            new_spot=new_spot,
            time_delta=time_delta,
            time_delta_minutes=time_delta_minutes,
            retain_original_iv=retain_original_iv,
        )
        return simulated_price

    def place_order(
        self,
        transaction_type,
        quantity_in_lots,
        price="LIMIT",
        stop_loss_order=False,
        order_tag="",
    ):
        if isinstance(price, str):
            if price.upper() == "LIMIT":
                price = self.fetch_ltp()
                modifier = (
                    (1 + config.LIMIT_PRICE_BUFFER)
                    if transaction_type == "BUY"
                    else (1 - config.LIMIT_PRICE_BUFFER)
                )
                price = price * modifier
        spliced_orders = splice_orders(quantity_in_lots, self.freeze_qty_in_lots)
        order_ids = []
        for qty in spliced_orders:
            order_id = place_order(
                self.symbol,
                self.token,
                qty * self.lot_size,
                transaction_type,
                price,
                stop_loss_order=stop_loss_order,
                order_tag=order_tag,
            )
            order_ids.append(order_id)
        self.order_id_log.append(order_ids)
        return order_ids


class Strangle:
    def __init__(self, call_strike, put_strike, underlying, expiry):
        self.call_option = Option(call_strike, "CE", underlying, expiry)
        self.put_option = Option(put_strike, "PE", underlying, expiry)
        self.call_strike = self.call_option.strike
        self.put_strike = self.put_option.strike
        self.underlying = underlying.upper()
        self.underlying_exchange = (
            "BSE" if self.underlying in ["SENSEX", "BANKEX"] else "NSE"
        )
        self.exchange = "BFO" if self.underlying in ["SENSEX", "BANKEX"] else "NFO"
        self.expiry = expiry.upper()
        self.call_symbol, self.call_token = self.call_option.fetch_symbol_token()
        self.put_symbol, self.put_token = self.put_option.fetch_symbol_token()
        self.freeze_qty_in_shares = self.call_option.freeze_qty_in_shares
        self.freeze_qty_in_lots = self.call_option.freeze_qty_in_lots
        self.lot_size = self.call_option.lot_size

    def __repr__(self):
        return (
            f"{self.__class__.__name__}(callstrike={self.call_option.strike}, putstrike={self.put_option.strike}, "
            f"underlying={self.underlying}, expiry={self.expiry})"
        )

    def __hash__(self):
        return hash((self.call_strike, self.put_strike, self.underlying, self.expiry))

    def __eq__(self, other):
        return (
            self.call_option == other.call_option
            and self.put_option == other.put_option
        )

    def fetch_ltp(self):
        return fetch_ltp(self.exchange, self.call_symbol, self.call_token), fetch_ltp(
            self.exchange, self.put_symbol, self.put_token
        )

    def underlying_ltp(self):
        symbol, token = get_symbol_token(self.underlying)
        return fetch_ltp(self.underlying_exchange, symbol, token)

    def fetch_ivs(
        self,
        spot: float | None = None,
        prices: tuple[float, float] | None = None,
        t: float | None = None,
        effective_iv: bool = False,
    ) -> tuple[float | None, float | None, float | None]:
        spot = spot if spot is not None else self.underlying_ltp()
        t = (
            t
            if t is not None
            else time_to_expiry(self.expiry, effective_time=effective_iv)
        )

        call_price, put_price = prices if prices is not None else self.fetch_ltp()

        return strangle_iv(
            call_price,
            put_price,
            spot,
            self.call_strike,
            self.put_strike,
            timeleft=t,
        )

    def fetch_iv(self, spot=None, t=None, effective_iv=False):
        spot = spot if spot is not None else self.underlying_ltp()
        t = (
            t
            if t is not None
            else time_to_expiry(self.expiry, effective_time=effective_iv)
        )

        return strangle_iv(
            *self.fetch_ltp(),
            spot,
            self.call_strike,
            self.put_strike,
            timeleft=t,
        )[2]

    def fetch_total_ltp(self):
        call_ltp, put_ltp = fetch_ltp(
            self.exchange, self.call_symbol, self.call_token
        ), fetch_ltp(self.exchange, self.put_symbol, self.put_token)
        return call_ltp + put_ltp

    def price_disparity(self):
        call_ltp, put_ltp = self.fetch_ltp()
        disparity = abs(call_ltp - put_ltp) / min(call_ltp, put_ltp)
        return disparity

    def fetch_symbol_token(self):
        return self.call_symbol, self.call_token, self.put_symbol, self.put_token

    def simulate_price(
        self,
        atm_iv: float,
        new_spot: float | None = None,
        movement: float | None = None,
        time_delta: float | None = None,
        time_delta_minutes: float | int | None = None,
        effective_iv: bool = False,
        retain_original_iv: bool = False,
        return_total: bool = True,
        original_spot: float | None = None,
        original_ivs: tuple[float, float] | None = None,
    ):
        original_time_to_expiry = time_to_expiry(
            self.expiry, effective_time=effective_iv
        )
        original_spot = (
            original_spot if original_spot is not None else self.underlying_ltp()
        )

        if original_ivs is not None:
            call_original_iv, put_original_iv = original_ivs
        else:
            call_original_iv = self.call_option.fetch_iv(
                spot=original_spot, t=original_time_to_expiry
            )
            put_original_iv = self.put_option.fetch_iv(
                spot=original_spot, t=original_time_to_expiry
            )

        logger.debug(
            f"Call original iv: {call_original_iv}, Put original iv: {put_original_iv}"
        )
        call_simulated_price = self.call_option.simulate_price(
            atm_iv=atm_iv,
            new_spot=new_spot,
            movement=movement,
            time_delta=time_delta,
            time_delta_minutes=time_delta_minutes,
            effective_iv=effective_iv,
            retain_original_iv=retain_original_iv,
            original_spot=original_spot,
            original_iv=call_original_iv,
        )
        put_simulated_price = self.put_option.simulate_price(
            atm_iv=atm_iv,
            new_spot=new_spot,
            movement=movement,
            time_delta=time_delta,
            time_delta_minutes=time_delta_minutes,
            effective_iv=effective_iv,
            retain_original_iv=retain_original_iv,
            original_spot=original_spot,
            original_iv=put_original_iv,
        )
        if return_total:
            return call_simulated_price + put_simulated_price
        else:
            return call_simulated_price, put_simulated_price

    def simulate_price_both_directions(
        self,
        atm_iv: float,
        movement: float,
        time_delta: float | None = None,
        time_delta_minutes: float | int | None = None,
        effective_iv: bool = False,
        retain_original_iv: bool = False,
        return_total: bool = True,
        up_weightage: float = 0.55,
        original_spot: float | None = None,
        original_ivs: tuple[float, float] | None = None,
    ):
        """
        Movement should be absolute value as the function will simulate movement in both directions.
        The up weightage is the weightage given to the up movement. The down weightage is 1 - up weightage.
        The default up weightage is 0.55 which is based on analysis.
        """

        original_time_to_expiry = time_to_expiry(
            self.expiry, effective_time=effective_iv
        )
        original_spot = (
            original_spot if original_spot is not None else self.underlying_ltp()
        )
        original_ivs = (
            original_ivs
            if original_ivs is not None
            else (
                self.call_option.fetch_iv(
                    spot=original_spot, t=original_time_to_expiry
                ),
                self.put_option.fetch_iv(spot=original_spot, t=original_time_to_expiry),
            )
        )

        price_if_up = self.simulate_price(
            atm_iv=atm_iv,
            movement=movement,
            time_delta=time_delta,
            time_delta_minutes=time_delta_minutes,
            effective_iv=effective_iv,
            retain_original_iv=retain_original_iv,
            return_total=True,
            original_spot=original_spot,
            original_ivs=original_ivs,
        )
        price_if_down = self.simulate_price(
            atm_iv=atm_iv,
            movement=-movement,
            time_delta=time_delta,
            time_delta_minutes=time_delta_minutes,
            effective_iv=effective_iv,
            retain_original_iv=retain_original_iv,
            return_total=True,
            original_spot=original_spot,
            original_ivs=original_ivs,
        )
        if return_total:
            return (up_weightage * price_if_up) + ((1 - up_weightage) * price_if_down)
        else:
            return price_if_up, price_if_down

    def place_order(
        self,
        transaction_type,
        quantity_in_lots,
        prices="LIMIT",
        stop_loss_order=False,
        order_tag="",
    ):
        if stop_loss_order:
            assert isinstance(
                prices, (tuple, list, np.ndarray)
            ), "Prices must be a tuple of prices for stop loss order"
            call_price, put_price = prices
        else:
            if isinstance(prices, (tuple, list, np.ndarray)):
                call_price, put_price = prices
            elif prices.upper() == "LIMIT":
                call_price, put_price = self.fetch_ltp()
                modifier = (
                    (1 + config.LIMIT_PRICE_BUFFER)
                    if transaction_type == "BUY"
                    else (1 - config.LIMIT_PRICE_BUFFER)
                )
                call_price, put_price = call_price * modifier, put_price * modifier
            elif prices.upper() == "MARKET":
                call_price = put_price = prices
            else:
                raise ValueError(
                    "Prices must be either 'LIMIT' or 'MARKET' or a tuple of prices"
                )

        spliced_orders = splice_orders(quantity_in_lots, self.freeze_qty_in_lots)
        call_order_ids = []
        put_order_ids = []
        for qty in spliced_orders:
            call_order_id = place_order(
                self.call_symbol,
                self.call_token,
                qty * self.lot_size,
                transaction_type,
                call_price,
                stop_loss_order=stop_loss_order,
                order_tag=order_tag,
            )
            put_order_id = place_order(
                self.put_symbol,
                self.put_token,
                qty * self.lot_size,
                transaction_type,
                put_price,
                stop_loss_order=stop_loss_order,
                order_tag=order_tag,
            )
            call_order_ids.append(call_order_id)
            put_order_ids.append(put_order_id)
        return call_order_ids, put_order_ids


class Straddle(Strangle):
    def __init__(self, strike, underlying, expiry):
        super().__init__(strike, strike, underlying, expiry)
        self.strike = strike


class SyntheticFuture(Strangle):
    def __init__(self, strike, underlying, expiry):
        super().__init__(strike, strike, underlying, expiry)

    def place_order(
        self,
        transaction_type,
        quantity_in_lots,
        prices: str | tuple = "LIMIT",
        stop_loss_order=False,
        order_tag="",
    ):
        if isinstance(prices, (tuple, list, np.ndarray)):
            call_price, put_price = prices
        elif prices.upper() == "LIMIT":
            call_price, put_price = self.fetch_ltp()
            c_modifier, p_modifier = (
                (1 + config.LIMIT_PRICE_BUFFER, 1 - config.LIMIT_PRICE_BUFFER)
                if transaction_type.upper() == "BUY"
                else (1 - config.LIMIT_PRICE_BUFFER, 1 + config.LIMIT_PRICE_BUFFER)
            )
            call_price, put_price = call_price * c_modifier, put_price * p_modifier
        elif prices.upper() == "MARKET":
            call_price = put_price = prices
        else:
            raise ValueError(
                "Prices must be either 'LIMIT' or 'MARKET' or a tuple of prices"
            )

        call_transaction_type = "BUY" if transaction_type.upper() == "BUY" else "SELL"
        put_transaction_type = "SELL" if transaction_type.upper() == "BUY" else "BUY"

        spliced_orders = splice_orders(quantity_in_lots, self.freeze_qty_in_lots)
        call_order_ids = []
        put_order_ids = []
        for qty in spliced_orders:
            call_order_id = place_order(
                self.call_symbol,
                self.call_token,
                qty * self.lot_size,
                call_transaction_type,
                call_price,
                order_tag=order_tag,
            )
            put_order_id = place_order(
                self.put_symbol,
                self.put_token,
                qty * self.lot_size,
                put_transaction_type,
                put_price,
                order_tag=order_tag,
            )
            call_order_ids.append(call_order_id)
            put_order_ids.append(put_order_id)
        return call_order_ids, put_order_ids


class SyntheticArbSystem:
    def __init__(self, symbol_option_chains):
        self.symbol_option_chains = symbol_option_chains

    def find_arbitrage_opportunities(
        self,
        index: str,
        expiry: str,
        qty_in_lots: int,
        exit_time=(15, 28),
        threshold=3,  # in points
    ):
        def get_single_index_single_expiry_data(_index, _expiry):
            option_chain = self.symbol_option_chains[_index][_expiry]
            _strikes = [_s for _s in option_chain]
            _call_prices = [option_chain[_s]["call_price"] for _s in _strikes]
            _put_prices = [option_chain[_s]["put_price"] for _s in _strikes]
            _call_bids = [option_chain[_s]["call_best_bid"] for _s in _strikes]
            _call_asks = [option_chain[_s]["call_best_ask"] for _s in _strikes]
            _put_bids = [option_chain[_s]["put_best_bid"] for _s in _strikes]
            _put_asks = [option_chain[_s]["put_best_ask"] for _s in _strikes]
            _call_bid_qty = [option_chain[_s]["call_best_bid_qty"] for _s in _strikes]
            _call_ask_qty = [option_chain[_s]["call_best_ask_qty"] for _s in _strikes]
            _put_bid_qty = [option_chain[_s]["put_best_bid_qty"] for _s in _strikes]
            _put_ask_qty = [option_chain[_s]["put_best_ask_qty"] for _s in _strikes]

            return (
                np.array(_strikes),
                np.array(_call_prices),
                np.array(_put_prices),
                np.array(_call_bids),
                np.array(_call_asks),
                np.array(_put_bids),
                np.array(_put_asks),
                np.array(_call_bid_qty),
                np.array(_call_ask_qty),
                np.array(_put_bid_qty),
                np.array(_put_ask_qty),
            )

        def return_both_side_synthetic_prices(
            _strikes, _call_asks, _put_bids, _call_bids, _put_asks
        ):
            return (_strikes + _call_asks - _put_bids), (
                _strikes + _call_bids - _put_asks
            )

        (
            strikes,
            call_prices,
            put_prices,
            call_bids,
            call_asks,
            put_bids,
            put_asks,
            call_bid_qty,
            call_ask_qty,
            put_bid_qty,
            put_ask_qty,
        ) = get_single_index_single_expiry_data(index, expiry)
        synthetic_buy_prices, synthetic_sell_prices = return_both_side_synthetic_prices(
            strikes, call_asks, put_bids, call_bids, put_asks
        )
        min_price_index = np.argmin(synthetic_buy_prices)
        max_price_index = np.argmax(synthetic_sell_prices)
        min_price = synthetic_buy_prices[min_price_index]
        max_price = synthetic_sell_prices[max_price_index]

        last_print_time = current_time()
        while current_time().time() < time(*exit_time):
            if current_time() > last_print_time + timedelta(seconds=5):
                print(
                    f"{current_time()} - {index} - {expiry}:\n"
                    f"Minimum price: {min_price} at strike: {strikes[min_price_index]} "
                    f"Call Ask: {call_asks[min_price_index]} Put Bid: {put_bids[min_price_index]}\n"
                    f"Maximum price: {max_price} at strike: {strikes[max_price_index]} "
                    f"Call Bid: {call_bids[max_price_index]} Put Ask: {put_asks[max_price_index]}\n"
                    f"Price difference: {max_price - min_price}\n"
                )
                last_print_time = current_time()

            if max_price - min_price > threshold:
                print(
                    f"**********Trade Identified at {current_time()} on strike: Min {strikes[min_price_index]} "
                    f"and Max {strikes[max_price_index]}**********\n"
                    f"Minimum price: {min_price} at strike: {strikes[min_price_index]} "
                    f"Call Ask: {call_asks[min_price_index]} Put Bid: {put_bids[min_price_index]}\n"
                    f"Maximum price: {max_price} at strike: {strikes[max_price_index]} "
                    f"Call Bid: {call_bids[max_price_index]} Put Ask: {put_asks[max_price_index]}\n"
                    f"Price difference: {max_price - min_price}\n"
                )
                min_strike = strikes[min_price_index]
                max_strike = strikes[max_price_index]

                self.execute_synthetic_trade(
                    index,
                    expiry,
                    qty_in_lots,
                    min_strike,
                    max_strike,
                )

            for i, strike in enumerate(strikes):
                call_prices[i] = self.symbol_option_chains[index][expiry][strike][
                    "call_price"
                ]
                put_prices[i] = self.symbol_option_chains[index][expiry][strike][
                    "put_price"
                ]
                call_bids[i] = self.symbol_option_chains[index][expiry][strike][
                    "call_best_bid"
                ]
                call_asks[i] = self.symbol_option_chains[index][expiry][strike][
                    "call_best_ask"
                ]
                put_bids[i] = self.symbol_option_chains[index][expiry][strike][
                    "put_best_bid"
                ]
                put_asks[i] = self.symbol_option_chains[index][expiry][strike][
                    "put_best_ask"
                ]
                call_bid_qty[i] = self.symbol_option_chains[index][expiry][strike][
                    "call_best_bid_qty"
                ]
                call_ask_qty[i] = self.symbol_option_chains[index][expiry][strike][
                    "call_best_ask_qty"
                ]
                put_bid_qty[i] = self.symbol_option_chains[index][expiry][strike][
                    "put_best_bid_qty"
                ]
                put_ask_qty[i] = self.symbol_option_chains[index][expiry][strike][
                    "put_best_ask_qty"
                ]
            (
                synthetic_buy_prices,
                synthetic_sell_prices,
            ) = return_both_side_synthetic_prices(
                strikes, call_asks, put_bids, call_bids, put_asks
            )
            min_price_index = np.argmin(synthetic_buy_prices)
            max_price_index = np.argmax(synthetic_sell_prices)
            min_price = synthetic_buy_prices[min_price_index]
            max_price = synthetic_sell_prices[max_price_index]

    @staticmethod
    def execute_synthetic_trade(
        index,
        expiry,
        qty_in_lots,
        buy_strike,
        sell_strike,
    ):
        ids_call_buy, ids_put_sell = place_synthetic_fut_order(
            index, buy_strike, expiry, "BUY", qty_in_lots, "MARKET"
        )
        ids_call_sell, ids_put_buy = place_synthetic_fut_order(
            index, sell_strike, expiry, "SELL", qty_in_lots, "MARKET"
        )
        ids = np.concatenate((ids_call_buy, ids_put_sell, ids_call_sell, ids_put_buy))

        sleep(1)
        statuses = lookup_and_return("orderbook", "orderid", ids, "status")

        if any(statuses == "rejected"):
            logger.error(
                f"Order rejected for {index} {expiry} {qty_in_lots} Buy {buy_strike} Sell {sell_strike}"
            )


class IvArbitrageScanner:
    def __init__(self, symbol_option_chains, iv_log):
        self.symbol_option_chains = symbol_option_chains
        self.iv_log = iv_log
        self.trade_log = []

    @log_errors
    def scan_for_iv_arbitrage(
        self, iv_hurdle=1.5, exit_time=(15, 25), notification_url=None
    ):
        while current_time().time() < time(*exit_time):
            for index in self.symbol_option_chains:
                spot = self.symbol_option_chains[index].underlying_price
                for expiry in self.symbol_option_chains[index]:
                    for strike in self.symbol_option_chains[index][expiry]:
                        option_to_check = "avg"

                        # Check for IV spike
                        if spot < strike + 100:
                            option_to_check = "call"

                        if spot > strike - 100:
                            option_to_check = "put"

                        try:
                            opt_iv = self.symbol_option_chains[index][expiry][strike][
                                f"{option_to_check}_iv"
                            ]
                            running_avg_opt_iv = self.symbol_option_chains[index][
                                expiry
                            ][strike][f"running_avg_{option_to_check}_iv"]
                        except KeyError as e:
                            print(f"KeyError {e} for {index} {expiry} {strike}")
                            raise e

                        self.check_iv_spike(
                            opt_iv,
                            running_avg_opt_iv,
                            option_to_check.capitalize(),
                            index,
                            strike,
                            expiry,
                            iv_hurdle,
                            notification_url,
                        )

    def check_iv_spike(
        self,
        iv,
        running_avg_iv,
        opt_type,
        underlying,
        strike,
        expiry,
        iv_hurdle,
        notification_url,
    ):
        if (
            opt_type == "Avg"
            or iv is None
            or running_avg_iv is None
            or np.isnan(iv)
            or np.isnan(running_avg_iv)
        ):
            return

        iv_hurdle = 1 + iv_hurdle
        upper_iv_threshold = running_avg_iv * iv_hurdle
        lower_iv_threshold = running_avg_iv / iv_hurdle

        # print(
        #    f"Checking {opt_type} IV for {underlying} {strike} {expiry}\nIV: {iv}\n"
        #    f"Running Average: {running_avg_iv}\nUpper Threshold: {upper_iv_threshold}\n"
        #    f"Lower Threshold: {lower_iv_threshold}"
        # )

        if iv and (iv > upper_iv_threshold or iv < lower_iv_threshold):
            # Execute trade
            # signal = "BUY" if iv > upper_iv_threshold else "SELL"
            # self.execute_iv_arbitrage_trade(
            #     signal, underlying, strike, expiry, opt_type
            # )

            # Notify
            if self.iv_log[underlying][expiry][strike][
                "last_notified_time"
            ] < current_time() - timedelta(minutes=5):
                notifier(
                    f"{opt_type} IV for {underlying} {strike} {expiry} different from average.\nIV: {iv}\n"
                    f"Running Average: {running_avg_iv}",
                    notification_url,
                    "INFO",
                )
                self.iv_log[underlying][expiry][strike][
                    "last_notified_time"
                ] = current_time()

    def execute_iv_arbitrage_trade(
        self, signal, underlying, strike, expiry, option_type
    ):
        qty_in_lots = 1
        option_to_trade = Option(strike, option_type, underlying, expiry)
        order_ids = option_to_trade.place_order(signal, qty_in_lots, "MARKET")
        self.trade_log.append(
            {
                "traded_option": option_to_trade,
                "order_ids": order_ids,
                "signal": signal,
                "qty": qty_in_lots,
                "order_type": "MARKET",
                "time": current_time(),
            }
        )


class Index:
    """Initialize an index with the name of the index in uppercase"""

    EXPIRY_FREQUENCY: dict = {
        "MIDCPNIFTY": 0,
        "FINNIFTY": 1,
        "BANKNIFTY": 2,
        "NIFTY": 3,
        "SENSEX": 4,
    }

    def __init__(self, name):
        self.name = name.upper()
        self.previous_close = None
        self.current_expiry = None
        self.next_expiry = None
        self.far_expiry = None
        self.month_expiry = None
        self.fut_expiry = None
        self.exchange = "BSE" if self.name in ["SENSEX", "BANKEX"] else "NSE"
        self.fno_exchange = "BFO" if self.name in ["SENSEX", "BANKEX"] else "NFO"
        self.order_log = defaultdict(list)
        self.symbol, self.token = get_symbol_token(self.name)
        self.future_symbol_tokens = {}
        self.fetch_exps()
        self.lot_size = get_lot_size(self.name, self.current_expiry)
        self.freeze_qty = self.fetch_freeze_limit()
        self.available_strikes = None
        self.available_straddle_strikes = None
        self.intraday_straddle_forced_exit = False
        self.base = get_base(self.name, self.current_expiry)
        self.strategy_log = defaultdict(list)
        self.exchange_type = 1

        logger.info(
            f"Initialized {self.name} with lot size {self.lot_size}, base {self.base} and freeze qty {self.freeze_qty}"
        )

    def __repr__(self):
        return (
            f"{self.__class__.__name__}(Name: {self.name}, Lot Size: {self.lot_size}, "
            f"Freeze Qty: {self.freeze_qty}, Current Expiry: {self.current_expiry}, Symbol: {self.symbol}, "
            f"Token: {self.token})"
        )

    def fetch_freeze_limit(self):
        try:
            freeze_qty_url = "https://archives.nseindia.com/content/fo/qtyfreeze.xls"
            response = requests.get(freeze_qty_url, timeout=10)  # Set the timeout value
            response.raise_for_status()  # Raise an exception if the response contains an HTTP error status
            df = pd.read_excel(response.content)
            df.columns = df.columns.str.strip()
            df["SYMBOL"] = df["SYMBOL"].str.strip()
            freeze_qty = df[df["SYMBOL"] == self.name]["VOL_FRZ_QTY"].values[0]
            freeze_qty_in_lots = freeze_qty / self.lot_size
            return int(freeze_qty_in_lots)
        except requests.exceptions.Timeout as e:
            logger.error(f"Timeout error in fetching freeze limit for {self.name}: {e}")
            freeze_qty_in_lots = 20
            return int(freeze_qty_in_lots)
        except requests.exceptions.HTTPError as e:
            logger.error(f"HTTP error in fetching freeze limit for {self.name}: {e}")
            freeze_qty_in_lots = 20
            return int(freeze_qty_in_lots)
        except Exception as e:
            logger.error(f"Error in fetching freeze limit for {self.name}: {e}")
            freeze_qty_in_lots = 20
            return freeze_qty_in_lots

    def fetch_exps(self):
        exps = get_expiry_dates(self.EXPIRY_FREQUENCY.get(self.name, "monthly"))
        exps = pd.DatetimeIndex(exps).strftime("%d%b%y").str.upper().tolist()

        self.current_expiry = exps[0]
        self.next_expiry = exps[1]
        self.far_expiry = exps[2]

        if self.name in self.EXPIRY_FREQUENCY:
            self.fut_expiry = self.month_expiry = exps[3]
        else:
            self.fut_expiry = self.month_expiry = exps[0]

    def set_future_symbol_tokens(self):
        if not self.future_symbol_tokens:
            for i in range(0, 3):
                try:
                    self.future_symbol_tokens[i] = get_symbol_token(self.name, future=i)
                except ScripsLocationError:
                    self.future_symbol_tokens[i] = (None, None)
                    continue

    def fetch_ltp(self, future=None):
        """Fetch LTP of the index."""
        if isinstance(future, int):
            try:
                ltp = fetch_ltp(
                    self.fno_exchange,
                    self.future_symbol_tokens[future][0],
                    self.future_symbol_tokens[future][1],
                )
            except Exception as e:
                error_message_to_catch = (
                    "Error in fetching LTP: 'NoneType' object is not subscriptable"
                )
                if str(e) == error_message_to_catch:
                    ltp = np.nan
                else:
                    raise e
        else:
            ltp = fetch_ltp(self.exchange, self.symbol, self.token)
        return ltp

    def fetch_previous_close(self):
        self.previous_close = fetchpreviousclose(self.exchange, self.symbol, self.token)
        return self.previous_close

    def fetch_atm_info(self, expiry="current", effective_iv=False):
        expiry_dict = {
            "current": self.current_expiry,
            "next": self.next_expiry,
            "month": self.month_expiry,
            "future": self.fut_expiry,
            "fut": self.fut_expiry,
        }
        expiry = expiry_dict[expiry]
        price = self.fetch_ltp()
        atm_strike = find_strike(price, self.base)
        atm_straddle = Straddle(atm_strike, self.name, expiry)
        call_price, put_price = atm_straddle.fetch_ltp()
        total_price = call_price + put_price
        call_iv, put_iv, avg_iv = atm_straddle.fetch_ivs(
            spot=price, effective_iv=effective_iv
        )
        return {
            "underlying_price": price,
            "strike": atm_strike,
            "call_price": call_price,
            "put_price": put_price,
            "total_price": total_price,
            "call_iv": call_iv,
            "put_iv": put_iv,
            "avg_iv": avg_iv,
        }

    def fetch_otm_info(self, strike_offset, expiry="current", effective_iv=False):
        expiry_dict = {
            "current": self.current_expiry,
            "next": self.next_expiry,
            "month": self.month_expiry,
            "future": self.fut_expiry,
            "fut": self.fut_expiry,
        }
        expiry = expiry_dict[expiry]
        price = self.fetch_ltp()
        call_strike = price * (1 + strike_offset)
        put_strike = price * (1 - strike_offset)
        call_strike = find_strike(call_strike, self.base)
        put_strike = find_strike(put_strike, self.base)
        otm_strangle = Strangle(call_strike, put_strike, self.name, expiry)
        call_price, put_price = otm_strangle.fetch_ltp()
        total_price = call_price + put_price
        call_iv, put_iv, avg_iv = otm_strangle.fetch_ivs(
            spot=price, effective_iv=effective_iv
        )
        return {
            "underlying_price": price,
            "call_strike": call_strike,
            "put_strike": put_strike,
            "call_price": call_price,
            "put_price": put_price,
            "total_price": total_price,
            "call_iv": call_iv,
            "put_iv": put_iv,
            "avg_iv": avg_iv,
        }

    def get_available_strikes(self, both_pairs=False):
        available_strikes = get_available_strikes(self.name, both_pairs)
        if not both_pairs:
            self.available_strikes = available_strikes
        else:
            self.available_straddle_strikes = available_strikes
        return available_strikes

    def get_constituents(self, cutoff_pct=101):
        tickers, weights = get_index_constituents(self.name, cutoff_pct)
        return tickers, weights

    def get_range_of_strangles(
        self, c_strike, p_strike, strike_range, exp=None
    ) -> list[Strangle | Straddle]:
        """Gets a range of strangles around the given strikes. If c_strike == p_strike, returns a range of straddles"""

        if exp is None:
            exp = self.current_expiry

        if strike_range % 2 != 0:
            strike_range += 1
        c_strike_range = np.arange(
            c_strike - (strike_range / 2) * self.base,
            c_strike + (strike_range / 2) * self.base + self.base,
            self.base,
        )
        if c_strike == p_strike:
            return [Straddle(strike, self.name, exp) for strike in c_strike_range]
        else:
            p_strike_ranges = np.arange(
                p_strike - (strike_range / 2) * self.base,
                p_strike + (strike_range / 2) * self.base + self.base,
                self.base,
            )
            pairs = itertools.product(c_strike_range, p_strike_ranges)
            return [Strangle(pair[0], pair[1], self.name, exp) for pair in pairs]

    def splice_orders(self, quantity_in_lots):
        if quantity_in_lots > self.freeze_qty:
            loops = int(quantity_in_lots / self.freeze_qty)
            if loops > config.LARGE_ORDER_THRESHOLD:
                raise Exception(
                    "Order too big. This error was raised to prevent accidental large order placement."
                )

            remainder = quantity_in_lots % self.freeze_qty
            if remainder == 0:
                spliced_orders = [self.freeze_qty] * loops
            else:
                spliced_orders = [self.freeze_qty] * loops + [remainder]
        else:
            spliced_orders = [quantity_in_lots]
        return spliced_orders

    def place_synthetic_fut(
        self,
        strike,
        expiry,
        buy_or_sell,
        quantity_in_lots,
        prices="LIMIT",
        stop_loss_order=False,
        order_tag="",
    ):
        return place_synthetic_fut_order(
            self.name,
            strike,
            expiry,
            buy_or_sell,
            quantity_in_lots,
            prices,
            stop_loss_order,
            order_tag,
        )

    def return_greeks_for_strikes(self, strike_range=4, expiry=None, option_type="CE"):
        if expiry is None:
            expiry = self.current_expiry
        underlying_price = self.fetch_ltp()
        atm_strike = find_strike(underlying_price, self.base)
        strikes = (
            np.arange(atm_strike, atm_strike + strike_range * self.base, self.base)
            if option_type.lower()[0] == "c"
            else np.arange(
                atm_strike - strike_range * self.base, atm_strike + self.base, self.base
            )
        )
        options = [Option(strike, option_type, self.name, expiry) for strike in strikes]
        greek_dict = {option: option.fetch_greeks() for option in options}
        return greek_dict

    def most_equal_strangle(
        self,
        call_strike_offset=0,
        put_strike_offset=0,
        disparity_threshold=np.inf,
        exit_time=time(15, 25),
        range_of_strikes=4,
        expiry=None,
        notification_url=None,
    ) -> Strangle | Straddle | None:
        def get_range_of_strangles(c_strike, p_strike, exp, strike_range):
            if strike_range % 2 != 0:
                strike_range += 1
            c_strike_range = np.arange(
                c_strike - (strike_range / 2) * self.base,
                c_strike + (strike_range / 2) * self.base + self.base,
                self.base,
            )
            if c_strike == p_strike:
                return [Straddle(strike, self.name, exp) for strike in c_strike_range]
            else:
                p_strike_ranges = np.arange(
                    p_strike - (strike_range / 2) * self.base,
                    p_strike + (strike_range / 2) * self.base + self.base,
                    self.base,
                )
                pairs = itertools.product(c_strike_range, p_strike_ranges)
                return [Strangle(pair[0], pair[1], self.name, exp) for pair in pairs]

        if expiry is None:
            expiry = self.current_expiry

        underlying_ltp = self.fetch_ltp()
        temp_call_strike = underlying_ltp * (1 + call_strike_offset)
        temp_put_strike = underlying_ltp * (1 - put_strike_offset)
        temp_call_strike = find_strike(temp_call_strike, self.base)
        temp_put_strike = find_strike(temp_put_strike, self.base)

        strangles = get_range_of_strangles(
            temp_call_strike, temp_put_strike, expiry, range_of_strikes
        )
        logger.info(f"{self.name} prospective strangles: {strangles}")

        # Create a set of all distinct options
        options = set(
            option
            for strangle in strangles
            for option in (strangle.call_option, strangle.put_option)
        )

        # Define the price disparity function
        def price_disparity(strangle):
            call_ltp = ltp_cache[strangle.call_option]
            put_ltp = ltp_cache[strangle.put_option]
            return abs(call_ltp - put_ltp) / min(call_ltp, put_ltp)

        tracked_strangle = None

        last_notified_time = current_time() - timedelta(minutes=6)
        while current_time().time() < exit_time:
            # If there's no tracked strangle update all prices and find the most equal strangle
            if tracked_strangle is None:
                ltp_cache = {option: option.fetch_ltp() for option in options}
                most_equal, min_disparity = min(
                    ((s, price_disparity(s)) for s in strangles), key=lambda x: x[1]
                )
                if min_disparity < 0.10:
                    tracked_strangle = most_equal

            # If there's a tracked strangle, check its disparity
            else:
                ltp_cache = {
                    tracked_strangle.call_option: tracked_strangle.call_option.fetch_ltp(),
                    tracked_strangle.put_option: tracked_strangle.put_option.fetch_ltp(),
                }
                most_equal = tracked_strangle
                min_disparity = price_disparity(tracked_strangle)
                if min_disparity >= 0.10:
                    tracked_strangle = None

            logger.info(
                f"Most equal strangle: {most_equal} with disparity {min_disparity} "
                f"and prices {ltp_cache[most_equal.call_option]} and {ltp_cache[most_equal.put_option]}"
            )
            if last_notified_time < current_time() - timedelta(minutes=5):
                notifier(
                    f"Most equal strangle: {most_equal} with disparity {min_disparity} "
                    f"and prices {ltp_cache[most_equal.call_option]} and {ltp_cache[most_equal.put_option]}",
                    notification_url,
                    "INFO",
                )
                logger.info(f"Most equal ltp cache: {ltp_cache}")
                last_notified_time = current_time()
            # If the lowest disparity is below the threshold, return the most equal strangle
            if min_disparity < disparity_threshold:
                return most_equal
            else:
                pass
            sleep(0.5)

        else:
            return None

    @timeit
    def most_resilient_strangle(
        self,
        strike_range=40,
        expiry=None,
        extra_buffer=1.07,
    ) -> Strangle:
        def expected_movement(option: Option):
            print(ltp_cache[option])
            raise NotImplementedError

        def find_favorite_strike(expected_moves, options, benchmark_movement):
            for i in range(1, len(expected_moves)):
                if (
                    expected_moves[i] > benchmark_movement * extra_buffer
                    and expected_moves[i] > expected_moves[i - 1]
                ):
                    return options[i]
            return None

        if expiry is None:
            expiry = self.current_expiry

        spot_price = self.fetch_ltp()
        atm_strike = find_strike(spot_price, self.base)

        half_range = int(strike_range / 2)
        strike_range = np.arange(
            atm_strike - (self.base * half_range),
            atm_strike + (self.base * (half_range + 1)),
            self.base,
        )

        options_by_type = {
            "CE": [
                Option(
                    strike=strike, option_type="CE", underlying=self.name, expiry=expiry
                )
                for strike in strike_range
                if strike >= atm_strike
            ],
            "PE": [
                Option(
                    strike=strike, option_type="PE", underlying=self.name, expiry=expiry
                )
                for strike in strike_range[::-1]
                if strike <= atm_strike
            ],
        }

        ltp_cache = {
            option: option.fetch_ltp()
            for option_type in options_by_type
            for option in options_by_type[option_type]
        }

        expected_movements = {
            option_type: [expected_movement(option) for option in options]
            for option_type, options in options_by_type.items()
        }

        expected_movements_ce = np.array(expected_movements["CE"])
        expected_movements_pe = np.array(expected_movements["PE"])
        expected_movements_pe = expected_movements_pe * -1

        benchmark_movement_ce = expected_movements_ce[0]
        benchmark_movement_pe = expected_movements_pe[0]

        logger.info(
            f"{self.name} - Call options' expected movements: {list(zip(options_by_type['CE'], expected_movements_ce))}"
        )
        logger.info(
            f"{self.name} - Put options' expected movements:{list(zip(options_by_type['PE'], expected_movements_pe))}"
        )

        favorite_strike_ce = (
            find_favorite_strike(
                expected_movements_ce,
                options_by_type["CE"],
                benchmark_movement_ce,
            )
            or options_by_type["CE"][0]
        )  # If no favorite strike, use ATM strike
        favorite_strike_pe = (
            find_favorite_strike(
                expected_movements_pe,
                options_by_type["PE"],
                benchmark_movement_pe,
            )
            or options_by_type["PE"][0]
        )  # If no favorite strike, use ATM strike

        ce_strike = favorite_strike_ce.strike
        pe_strike = favorite_strike_pe.strike
        strangle = Strangle(ce_strike, pe_strike, self.name, expiry)

        return strangle


class Stock(Index):
    def __init__(self, name):
        if name not in symbol_df["SYMBOL"].values:
            closest_match, confidence = process.extractOne(
                name, symbol_df["SYMBOL"].values
            )
            if confidence > 80:
                raise Exception(
                    f"Index {name} not found. Did you mean {closest_match}?"
                )

            else:
                raise ValueError(f"Index {name} not found")
        super().__init__(name)


class IndiaVix:
    symbol, token = None, None

    @classmethod
    def fetch_ltp(cls):
        if cls.symbol is None or cls.token is None:
            cls.symbol, cls.token = get_symbol_token("INDIA VIX")
        return fetch_ltp("NSE", cls.symbol, cls.token)


def place_synthetic_fut_order(
    name,
    strike,
    expiry,
    buy_or_sell,
    quantity_in_lots,
    prices: str | tuple = "MARKET",
    stop_loss_order=False,
    order_tag="",
):
    """Places a synthetic future order. Quantity is in number of shares."""

    syn_fut = SyntheticFuture(strike, name, expiry)
    call_order_ids, put_order_ids = syn_fut.place_order(
        buy_or_sell, quantity_in_lots, prices, stop_loss_order, order_tag
    )
    return call_order_ids, put_order_ids


def check_and_notify_order_placement_statuses(
    statuses, target_status="complete", webhook_url=None, **kwargs
):
    order_prefix = (
        f"{kwargs['order_tag']}: "
        if ("order_tag" in kwargs and kwargs["order_tag"])
        else ""
    )
    order_message = [f"{k}-{v}" for k, v in kwargs.items() if k != "order_tag"]
    order_message = ", ".join(order_message)

    if all(statuses == target_status):
        notifier(
            f"{order_prefix}Order(s) placed successfully for {order_message}",
            webhook_url,
            "CRUCIAL",
        )
    elif any(statuses == target_status):
        notifier(
            f"{order_prefix}Some orders successful for {order_message}. Please repair the remaining orders.",
            webhook_url,
            "CRUCIAL",
        )
    elif any(statuses == "open"):
        notifier(
            f"{order_prefix}Orders open for {order_message}. Please repair.",
            webhook_url,
            "CRUCIAL",
        )
    elif all(statuses == "rejected"):
        notifier(
            f"{order_prefix}All orders rejected for {order_message}",
            webhook_url,
            "ERROR",
        )
        raise Exception("Orders rejected")
    else:
        notifier(
            f"{order_prefix}No orders successful. Raising exception.",
            webhook_url,
            "ERROR",
        )
        logger.error(f"{order_message} - No orders successful. Statuses: {statuses}")
        raise Exception("No orders successful.")


@timeit
def place_option_order_and_notify(
    instrument: Option | Strangle | Straddle | SyntheticFuture,
    action: str,
    qty_in_lots: int,
    prices: str | int | float | tuple | list | np.ndarray = "LIMIT",
    order_tag: str = "",
    webhook_url=None,
    stop_loss_order: bool = False,
    target_status: str = "complete",
    return_avg_price: bool = True,
    square_off_order: bool = False,
    **kwargs,
) -> list | tuple | float | None:
    """Returns either a list of order ids or a tuple of avg prices or a float of avg price"""

    def return_avg_price_from_orderbook(orderbook, ids):
        avg_prices = lookup_and_return(
            orderbook, ["orderid", "status"], [ids, "complete"], "averageprice"
        )
        return avg_prices.astype(float).mean() if avg_prices.size > 0 else None

    # If square_off_order is True, check if the expiry is within 5 minutes
    if square_off_order and time_to_expiry(instrument.expiry, in_days=True) < (
        5 / (24 * 60)
    ):
        logger.info(
            f"Square off order not placed for {instrument} as expiry is within 5 minutes"
        )
        return instrument.fetch_ltp() if return_avg_price else None

    notify_dict = {
        "order_tag": order_tag,
        "Underlying": instrument.underlying,
        "Action": action,
        "Expiry": instrument.expiry,
        "Qty": qty_in_lots,
    }

    order_params = {
        "transaction_type": action,
        "quantity_in_lots": qty_in_lots,
        "stop_loss_order": stop_loss_order,
        "order_tag": order_tag,
    }

    if isinstance(instrument, (Strangle, Straddle, SyntheticFuture)):
        notify_dict.update({"Strikes": [instrument.call_strike, instrument.put_strike]})
        order_params.update({"prices": prices})
    elif isinstance(instrument, Option):
        notify_dict.update(
            {"Strike": instrument.strike, "OptionType": instrument.option_type}
        )
        order_params.update({"price": prices})
    else:
        raise ValueError("Invalid instrument type")

    notify_dict.update(kwargs)

    if stop_loss_order:
        assert isinstance(
            prices, (int, float, tuple, list, np.ndarray)
        ), "Stop loss order requires a price"
        target_status = "trigger pending"

    # Placing the order
    order_ids = instrument.place_order(**order_params)

    if isinstance(order_ids, tuple):  # Strangle/Straddle/SyntheticFuture
        call_order_ids, put_order_ids = order_ids[0], order_ids[1]
        order_ids = list(itertools.chain(call_order_ids, put_order_ids))
    else:  # Option
        call_order_ids, put_order_ids = False, False

    # Critical to wait for 1 second before fetching orderbook so that orders reflect in orderbook
    sleep(1)
    order_book = fetch_book("orderbook")
    try:  # Remove this try-except block after testing for a few days
        modify_open_orders(
            order_ids,
            order_book,
            modify_percentage=0.05,
            max_modification=0.3,
            sleep_interval=0.05,
        )
    except Exception as e:
        logger.error(
            f"Faced error while handling open orders: {e}",
            exc_info=(type(e), e, e.__traceback__),
        )
        notifier(f"Faced error while handling open orders: {e}. ", webhook_url, "INFO")
    sleep(1)  # Critical to wait again
    order_book = fetch_book("orderbook")
    order_statuses_ = lookup_and_return(order_book, "orderid", order_ids, "status")
    check_and_notify_order_placement_statuses(
        statuses=order_statuses_,
        target_status=target_status,
        webhook_url=webhook_url,
        **notify_dict,
    )

    if return_avg_price:
        if call_order_ids and put_order_ids:  # Strangle/Straddle/SyntheticFuture
            call_avg_price = (
                return_avg_price_from_orderbook(order_book, call_order_ids)
                or instrument.call_option.fetch_ltp()
            )
            put_avg_price = (
                return_avg_price_from_orderbook(order_book, put_order_ids)
                or instrument.put_option.fetch_ltp()
            )
            result = call_avg_price, put_avg_price
        else:  # Option
            avg_price = (
                return_avg_price_from_orderbook(order_book, order_ids)
                or instrument.fetch_ltp()
            )
            result = avg_price
        return result

    return order_ids


def process_stop_loss_order_statuses(
    order_book,
    order_ids,
    context="",
    notify_url=None,
):
    pending_text = "trigger pending"
    context = f"{context.capitalize()} " if context else ""

    statuses = lookup_and_return(order_book, "orderid", order_ids, "status")

    if not isinstance(statuses, np.ndarray) or statuses.size == 0:
        logger.error(f"Statuses is {statuses} for orderid(s) {order_ids}")

    if all(statuses == pending_text):
        return False, False

    elif all(statuses == "rejected") or all(statuses == "cancelled"):
        rejection_reasons = lookup_and_return(order_book, "orderid", order_ids, "text")
        if all(rejection_reasons == "17070 : The Price is out of the LPP range"):
            return True, False
        else:
            notifier(
                f"{context}Order(s) rejected or cancelled. Reasons: {rejection_reasons[0]}",
                notify_url,
                "ERROR",
            )
            raise Exception(f"Order(s) rejected or cancelled.")

    elif all(statuses == "pending"):
        sleep(5)
        order_book = fetch_book("orderbook")
        statuses = lookup_and_return(order_book, "orderid", order_ids, "status")

        if all(statuses == "pending"):
            try:
                cancel_pending_orders(order_ids, "NORMAL")
            except Exception as e:
                try:
                    cancel_pending_orders(order_ids, "STOPLOSS")
                except Exception as e:
                    notifier(
                        f"{context}Could not cancel orders: {e}", notify_url, "ERROR"
                    )
                    raise Exception(f"Could not cancel orders: {e}")
            notifier(
                f"{context}Orders pending and cancelled. Please check.",
                notify_url,
                "ERROR",
            )
            return True, False

        elif all(statuses == "complete"):
            return True, True

        else:
            logger.error(
                f"Orders in unknown state. Statuses: {statuses}, Order ids: {order_ids}"
            )
            raise Exception(f"Orders in unknown state.")

    elif all(statuses == "complete"):
        return True, True

    else:
        notifier(
            f"{context}Orders in unknown state. Statuses: {statuses}",
            notify_url,
            "ERROR",
        )
        raise Exception(f"Orders in unknown state.")


def fetch_orderbook_if_needed(
    data_class: SharedData = None, refresh_needed: bool = False
):
    if data_class is None:
        return fetch_book("orderbook")
    if refresh_needed:
        data_class.fetch_data()
    if (
        current_time() - data_class.updated_time < timedelta(seconds=15)
        and data_class.orderbook_data is not None
    ):
        return data_class.orderbook_data
    return fetch_book("orderbook")


def fetchpreviousclose(exchange_seg, symbol, token):
    for attempt in range(3):
        try:
            previousclose = ActiveSession.obj.ltpData(exchange_seg, symbol, token)[
                "data"
            ]["close"]
            return previousclose
        except Exception as e:
            if attempt == 2:
                print(f"Error in fetchpreviousclose: {e}")
            else:
                print(
                    f"Error {attempt} in fetchpreviousclose: {e}\nRetrying again in 1 second"
                )
                sleep(1)


def get_strangle_indices_to_trade(
    *indices: Index, safe_indices: list[str] | None = None, only_expiry: bool = False
) -> list[Index] | list[None]:
    if safe_indices is None:
        safe_indices = ["NIFTY", "BANKNIFTY"]

    times_to_expiries = [
        time_to_expiry(index.current_expiry, effective_time=True, in_days=True)
        for index in indices
    ]

    # Check if any index has less than 1 day to expiry
    indices_less_than_1_day = [
        index
        for index, time_left_to_expiry in zip(indices, times_to_expiries)
        if time_left_to_expiry < 1
    ]

    if indices_less_than_1_day or only_expiry:
        return indices_less_than_1_day

    # If no index has less than 1 day to expiry
    min_expiry_time = min(times_to_expiries)
    indices_with_closest_expiries = [
        index
        for index, time_left_to_expiry in zip(indices, times_to_expiries)
        if time_left_to_expiry == min_expiry_time
    ]
    weekend_in_range = check_for_weekend(
        indices_with_closest_expiries[0].current_expiry
    )

    if weekend_in_range:
        # Checking if the closest indices are safe indices
        safe_and_close = [
            index
            for index in indices_with_closest_expiries
            if index.name in safe_indices
        ]
        if (
            safe_and_close
        ):  # If the indices with the closest expiry are safe indices then return the closest indices
            return safe_and_close
        else:  # If the indices with the closest expiry are not safe indices then return safe indices
            return [index for index in indices if index.name in safe_indices]

    return indices_with_closest_expiries


def calculate_iv(opt_price, spot, strike, tte, opt_type):
    try:
        return bs.implied_volatility(opt_price, spot, strike, tte, 0.06, opt_type)
    except IntrinsicValueError:
        return None
    except Exception as e:
        logger.error(f"Error in calculate_iv: {e}")
        return None


def straddle_iv(callprice, putprice, spot, strike, timeleft):
    call_iv = calculate_iv(callprice, spot, strike, timeleft, "CE")
    put_iv = calculate_iv(putprice, spot, strike, timeleft, "PE")

    if call_iv is not None and put_iv is not None:
        avg_iv = (call_iv + put_iv) / 2
    else:
        avg_iv = call_iv if put_iv is None else put_iv

    return call_iv, put_iv, avg_iv


def strangle_iv(callprice, putprice, spot, callstrike, putstrike, timeleft):
    call_iv = calculate_iv(callprice, spot, callstrike, timeleft, "CE")
    put_iv = calculate_iv(putprice, spot, putstrike, timeleft, "PE")

    if call_iv is not None and put_iv is not None:
        avg_iv = (call_iv + put_iv) / 2
    else:
        avg_iv = call_iv if put_iv is None else put_iv

    return call_iv, put_iv, avg_iv


def calc_combined_premium(
    spot,
    time_left,
    strike=None,
    call_strike=None,
    put_strike=None,
    iv=None,
    call_iv=None,
    put_iv=None,
):
    call_strike = call_strike if call_strike is not None else strike
    put_strike = put_strike if put_strike is not None else strike

    call_iv = call_iv if call_iv is not None else iv
    put_iv = put_iv if put_iv is not None else iv
    if time_left > 0:
        call_price = bs.call(spot, call_strike, time_left, 0.05, call_iv)
        put_price = bs.put(spot, put_strike, time_left, 0.05, put_iv)
        return call_price + put_price
    else:
        call_payoff = max(0, spot - call_strike)
        put_payoff = max(0, put_strike - spot)
        return call_payoff + put_payoff


def get_index_constituents(index_symbol, cutoff_pct=101):
    # Fetch and filter constituents
    constituents = (
        pd.read_csv(f"data/{index_symbol}_constituents.csv")
        .sort_values("Index weight", ascending=False)
        .assign(cum_weight=lambda df: df["Index weight"].cumsum())
        .loc[lambda df: df.cum_weight < cutoff_pct]
    )

    constituent_tickers, constituent_weights = (
        constituents.Ticker.to_list(),
        constituents["Index weight"].to_list(),
    )

    return constituent_tickers, constituent_weights


def convert_option_chains_to_df(option_chains, return_all=False, for_surface=False):
    def add_columns_for_surface(data_frame):
        data_frame = data_frame.copy()
        data_frame["atm_strike"] = data_frame.apply(
            lambda row: find_strike(row.spot, 50)
            if row.symbol == "NIFTY"
            else find_strike(row.spot, 100),
            axis=1,
        )
        data_frame["strike_iv"] = np.where(
            data_frame.strike > data_frame.atm_strike,
            data_frame.call_iv,
            np.where(
                data_frame.strike < data_frame.atm_strike,
                data_frame.put_iv,
                data_frame.avg_iv,
            ),
        )
        data_frame["atm_iv"] = data_frame.apply(
            lambda row: data_frame[
                (data_frame.strike == row.atm_strike)
                & (data_frame.expiry == row.expiry)
            ].strike_iv.values[0],
            axis=1,
        )
        data_frame.sort_values(["symbol", "expiry", "strike"], inplace=True)
        data_frame["distance"] = data_frame["strike"] / data_frame["spot"] - 1
        data_frame["iv_multiple"] = data_frame["strike_iv"] / data_frame["atm_iv"]
        data_frame["distance_squared"] = data_frame["distance"] ** 2

        return data_frame

    symbol_dfs = []
    for symbol in option_chains:
        spot_price = option_chains[symbol].underlying_price
        expiry_dfs = []
        for expiry in option_chains[symbol]:
            df = pd.DataFrame(option_chains[symbol][expiry]).T
            df.index = df.index.set_names("strike")
            df = df.reset_index()
            df["spot"] = spot_price
            df["expiry"] = expiry
            df["symbol"] = symbol
            df["time_to_expiry"] = time_to_expiry(expiry)
            expiry_dfs.append(df)
        symbol_oc = pd.concat(expiry_dfs)
        if for_surface:
            symbol_oc = add_columns_for_surface(symbol_oc)
        symbol_dfs.append(symbol_oc)

    if return_all:
        return pd.concat(symbol_dfs)
    else:
        return symbol_dfs
