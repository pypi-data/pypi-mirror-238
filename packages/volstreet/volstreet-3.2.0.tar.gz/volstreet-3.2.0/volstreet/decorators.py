import functools
import traceback
from datetime import datetime
from time import sleep
from SmartApi.smartExceptions import DataException
from volstreet import config
from volstreet.config import logger, thread_local
from volstreet.utils import current_time, notifier
from volstreet.exceptions import APIFetchError


def timeit(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        start = datetime.now()
        result = func(*args, **kwargs)
        end = (datetime.now() - start).total_seconds()
        logger.info(f"Time taken for {func.__name__}: {end:.2f} seconds")
        return result

    return wrapper


def log_errors(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            user_prefix = config.ERROR_NOTIFICATION_SETTINGS.get("user", "")
            logger.error(
                f"{user_prefix}Error in function {func.__name__}: {e}\nTraceback:{traceback.format_exc()}"
            )
            notifier(
                f"{user_prefix}Error in function {func.__name__}: {e}\nTraceback:{traceback.format_exc()}",
                config.ERROR_NOTIFICATION_SETTINGS["url"],
                "ERROR",
            )
            raise e

    return wrapper


def retry_angel_api(data_type=None, max_attempts=10, wait_increase_factor=1.5):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            for attempt in range(1, max_attempts + 1):
                sleep_duration = 1
                data = {}

                try:
                    data = func(*args, **kwargs)
                    if data_type == "ltp":
                        return data["data"]["ltp"]
                    else:
                        return data["data"]
                except Exception as e:
                    msg = f"Attempt {attempt}: Error in function {func.__name__}: {e}"
                    additional_msg = data.get(
                        "message", "No additional message available"
                    )

                    # Invalid book type error in fetch_book
                    if isinstance(e, ValueError) and "Invalid book type" in e.args[0]:
                        raise e

                    # Access rate error
                    elif (
                        isinstance(e, DataException)
                        and "exceeding access rate" in e.args[0]
                    ):
                        if attempt == max_attempts:
                            logger.error(
                                f"{msg}. Additional info from payload: {additional_msg}"
                            )
                            raise e

                        sleep_duration *= wait_increase_factor  # Exponential backoff

                    # Other errors
                    else:
                        if getattr(thread_local, "robust_handling", False):
                            if attempt == max_attempts:
                                logger.error(
                                    f"{msg}. Additional info from payload: {additional_msg}"
                                )
                                raise e

                            elif (
                                attempt == max_attempts - 2
                            ):  # Approaching max attempts
                                logger.info(
                                    f"Attempt {attempt} failed. Trying big sleep."
                                )
                                seconds_to_day_end: int = (
                                    datetime(
                                        *current_time().date().timetuple()[:3],
                                        hour=15,
                                        minute=29,
                                    )
                                    - current_time()
                                ).seconds

                                max_sleep = max(min(60, seconds_to_day_end // 2), 1)

                                sleep(max_sleep)
                                continue

                            sleep_duration *= (
                                wait_increase_factor  # Exponential backoff
                            )

                        elif attempt == 5:
                            logger.error(
                                f"{msg}. Additional info from payload: {additional_msg}"
                            )
                            raise APIFetchError(msg)

                    logger.info(
                        f"{msg}. Additional info from payload: {additional_msg}. "
                        f"Retrying in {sleep_duration} seconds."
                    )
                    sleep(sleep_duration)
                    continue

        return wrapper

    return decorator


def increase_robustness(func):
    """This decorator will set a flag in the thread local storage that will be used by the other functions in the same
    thread to increase robustness. Currently, it is used to increase the number of attempts in retry_angel_api
    decorator. But in the future, it can be used to increase robustness in other ways too (by other functions running
    in the same thread).
    """

    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        # Set the flag to True before calling the actual function
        thread_local.robust_handling = True
        try:
            result = func(*args, **kwargs)
        finally:
            # Ensure the flag is set back to False after the function ends
            thread_local.robust_handling = False
        return result

    return wrapper
