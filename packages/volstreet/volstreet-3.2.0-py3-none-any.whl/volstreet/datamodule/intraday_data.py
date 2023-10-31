from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.expected_conditions import url_changes
from kiteconnect import KiteConnect
from time import sleep
from functools import partial
import pyotp
import pandas as pd
from datetime import datetime, timedelta, time
from math import ceil
from SmartApi.smartExceptions import DataException
from volstreet.config import scrips
from volstreet.utils import (
    current_time,
    word_to_num,
    last_market_close_time,
    get_symbol_token,
)
from volstreet.dealingroom import get_index_constituents
from volstreet.angel_interface.active_session import ActiveSession


def get_historical_prices(
    interval,
    last_n_intervals=None,
    from_date=None,
    to_date=None,
    token=None,
    name=None,
    expiry=None,
    strike=None,
    option_type=None,
):
    """Available intervals:

    ONE_MINUTE	1 Minute
    THREE_MINUTE 3 Minute
    FIVE_MINUTE	5 Minute
    TEN_MINUTE	10 Minute
    FIFTEEN_MINUTE	15 Minute
    THIRTY_MINUTE	30 Minute
    ONE_HOUR	1 Hour
    ONE_DAY	1 Day

    """

    MAX_DAYS = 25

    if token is None and name is None:
        raise ValueError("Either name or token must be specified.")

    if last_n_intervals is None and from_date is None:
        raise ValueError("Either last_n_intervals or from_date must be specified.")

    if last_n_intervals is not None and from_date is not None:
        raise ValueError("Only one of last_n_intervals or from_date must be specified.")

    if to_date is None:
        to_date = last_market_close_time()
    else:
        to_date = pd.to_datetime(to_date)

    if from_date is None and last_n_intervals is not None:
        interval_digit, interval_unit = interval.lower().split("_")
        interval_unit = (
            interval_unit + "s" if interval_unit[-1] != "s" else interval_unit
        )
        interval_digit = word_to_num(interval_digit)
        time_delta = interval_digit * last_n_intervals
        from_date = to_date - timedelta(**{interval_unit: time_delta})
    else:
        from_date = pd.to_datetime(from_date)

    total_days = (to_date - from_date).days
    num_requests = ceil(total_days / MAX_DAYS)

    if token is None:
        _, token = get_symbol_token(name, expiry, strike, option_type)

    exchange_seg = scrips.loc[scrips.token == token, "exch_seg"].values[0]

    all_data = []

    while from_date < to_date:
        current_to_date = min(from_date + timedelta(days=MAX_DAYS), to_date)
        historic_param = {
            "exchange": exchange_seg,
            "symboltoken": token,
            "interval": interval,
            "fromdate": from_date.strftime("%Y-%m-%d %H:%M"),
            "todate": current_to_date.strftime("%Y-%m-%d %H:%M"),
        }
        try:
            data = ActiveSession.obj.getCandleData(historic_param)
        except DataException as e:
            sleep(1)
            continue
        data = pd.DataFrame(data["data"])
        all_data.append(data)
        from_date = current_to_date

    # Concatenate all the data
    final_data = pd.concat(all_data, ignore_index=True)
    final_data.set_index(pd.Series(final_data.iloc[:, 0], name="date"), inplace=True)
    final_data.index = pd.to_datetime(final_data.index)
    final_data.index = final_data.index.tz_localize(None)
    final_data.drop(final_data.columns[0], axis=1, inplace=True)
    final_data.columns = ["open", "high", "low", "close", "volume"]

    return final_data.drop_duplicates()


def extend_historical_minute_prices(symbol, path="C:\\Users\\Administrator\\"):
    main_df = pd.read_csv(
        f"{path}{symbol}_onemin_prices.csv", index_col=0, parse_dates=True
    )
    from_date = main_df.index[-1]

    end_date = last_market_close_time()

    new_prices = get_historical_prices(
        interval="ONE_MINUTE",
        from_date=from_date,
        to_date=end_date,
        name=symbol,
    )
    new_prices.to_csv(
        f"{path}{symbol}_onemin_prices.csv",
        mode="a",
        header=False,
    )
    print(
        f"Finished fetching data for {symbol}. Fetched data from {new_prices.index[0]} to {new_prices.index[-1]}"
    )
    full_df = pd.concat([main_df, new_prices])

    return full_df


def get_greenlit_kite(
    kite_api_key,
    kite_api_secret,
    kite_user_id,
    kite_password,
    kite_auth_key,
    chrome_path=None,
):
    if chrome_path is None:
        driver = webdriver.Chrome()
    else:
        driver = webdriver.Chrome(chrome_path)

    authkey_obj = pyotp.TOTP(kite_auth_key)
    kite = KiteConnect(api_key=kite_api_key)
    login_url = kite.login_url()

    driver.get(login_url)
    wait = WebDriverWait(driver, 10)  # waits for up to 10 seconds

    userid = wait.until(EC.presence_of_element_located((By.ID, "userid")))
    userid.send_keys(kite_user_id)

    password = wait.until(EC.presence_of_element_located((By.ID, "password")))
    password.send_keys(kite_password)

    submit = wait.until(
        EC.presence_of_element_located((By.CLASS_NAME, "button-orange"))
    )
    submit.click()

    sleep(10)  # wait for the OTP input field to be clickable
    otp_input = wait.until(EC.element_to_be_clickable((By.TAG_NAME, "input")))
    otp_input.send_keys(authkey_obj.now())

    # wait until the URL changes
    wait.until(url_changes(driver.current_url))

    # now you can safely get the current URL
    current_url = driver.current_url

    split_url = current_url.split("=")
    request_token = None
    for i, string in enumerate(split_url):
        if "request_token" in string:
            request_token = split_url[i + 1]
            request_token = (
                request_token.split("&")[0] if "&" in request_token else request_token
            )
            break

    driver.quit()

    if request_token is None:
        raise Exception("Request token not found")

    data = kite.generate_session(request_token, api_secret=kite_api_secret)
    kite.set_access_token(data["access_token"])

    return kite


def fetch_minute_data_from_kite(kite, symbol, path="C:\\Users\\Administrator\\"):
    def _fetch_minute_data_from_kite(_kite, _token, _from_date, _to_date):
        date_format = "%Y-%m-%d %H:%M:%S"
        _prices = _kite.historical_data(
            _token,
            from_date=_from_date.strftime(date_format),
            to_date=_to_date.strftime(date_format),
            interval="minute",
        )
        return _prices

    instruments = kite.instruments(exchange="NSE")
    token = [
        instrument["instrument_token"]
        for instrument in instruments
        if instrument["tradingsymbol"] == symbol
    ][0]

    try:
        main_df = pd.read_csv(
            f"{path}{symbol}_onemin_prices.csv", index_col=0, parse_dates=True
        )
        from_date = main_df.index[-1] + timedelta(minutes=1)
    except FileNotFoundError:
        print(f"No existing data for {symbol}, starting from scratch.")
        main_df = False
        from_date = datetime(2015, 1, 1, 9, 16)

    end_date = current_time()
    mainlist = []

    fetch_data_partial = partial(_fetch_minute_data_from_kite, kite, token)

    default_time_delta_days = 34
    while from_date < end_date:
        to_date = from_date + timedelta(days=default_time_delta_days)
        prices = fetch_data_partial(from_date, to_date)
        if (
            len(prices) < 2 and not mainlist
        ):  # if there is no data for the period and no data at all
            print(
                f'No data for {from_date.strftime("%Y-%m-%d %H:%M:%S")} to {to_date.strftime("%Y-%m-%d %H:%M:%S")}'
            )
            if to_date > current_time():
                return None
            else:
                from_date += timedelta(days=default_time_delta_days)
                continue
        else:  # if there is data for the period
            mainlist.extend(prices)
            from_date += timedelta(days=default_time_delta_days)

    df = pd.DataFrame(mainlist).set_index("date")
    df.index = df.index.tz_localize(None)
    df = df[~df.index.duplicated(keep="first")]
    df = df[(df.index.time >= time(9, 15)) & (df.index.time <= time(15, 30))]
    df.to_csv(
        f"{path}{symbol}_onemin_prices.csv",
        mode="a",
        header=not isinstance(main_df, pd.DataFrame),
    )
    print(
        f"Finished fetching data for {symbol}. Fetched data from {df.index[0]} to {df.index[-1]}"
    )
    full_df = pd.concat([main_df, df]) if isinstance(main_df, pd.DataFrame) else df
    return full_df


def get_constituent_1m_data(kite_object, index_name, path="C:\\Users\\Administrator\\"):
    tickers, _weights = get_index_constituents(index_name)
    for ticker in tickers:
        print(f"Fetching data for {ticker}")
        fetch_minute_data_from_kite(kite_object, ticker, path=path)
