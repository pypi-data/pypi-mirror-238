import numpy as np
from volstreet.config import logger
from volstreet.decorators import retry_angel_api
from volstreet.angel_interface.active_session import ActiveSession


@retry_angel_api(data_type="ltp")
def fetch_ltp(exchange_seg, symbol, token):
    price_data = ActiveSession.obj.ltpData(exchange_seg, symbol, token)
    return price_data


@retry_angel_api(max_attempts=10)
def fetch_book(book: str) -> list:
    def fetch_data(fetch_func):
        data = fetch_func()
        return data

    if book == "orderbook":
        return fetch_data(ActiveSession.obj.orderBook)
    elif book in {"positions", "position"}:
        return fetch_data(ActiveSession.obj.position)
    else:
        raise ValueError(f"Invalid book type '{book}'.")


def lookup_and_return(
    book, field_to_lookup, value_to_lookup, field_to_return
) -> np.ndarray | dict:
    def filter_and_return(data: list):
        if not isinstance(field_to_lookup, (list, tuple, np.ndarray)):
            field_to_lookup_ = [field_to_lookup]
            value_to_lookup_ = [value_to_lookup]
        else:
            field_to_lookup_ = field_to_lookup
            value_to_lookup_ = value_to_lookup

        if isinstance(
            field_to_return, (list, tuple, np.ndarray)
        ):  # Return a dict as multiple fields are requested
            bucket = {field: [] for field in field_to_return}
            for entry in data:
                if all(
                    (
                        entry[field] == value
                        if not isinstance(value, (list, tuple, np.ndarray))
                        else entry[field] in value
                    )
                    for field, value in zip(field_to_lookup_, value_to_lookup_)
                ) and all(entry[field] != "" for field in field_to_lookup_):
                    for field in field_to_return:
                        bucket[field].append(entry[field])

            if all(len(v) == 0 for v in bucket.values()):
                return {}
            else:
                # Flatten the dictionary if all fields contain only one value
                if all(len(v) == 1 for v in bucket.values()):
                    bucket = {k: v[0] for k, v in bucket.items()}
                return bucket
        else:  # Return a numpy array as only one field is requested
            # Check if 'orderid' is in field_to_lookup_
            if "orderid" in field_to_lookup_:
                sort_by_orderid = True
                orderid_index = field_to_lookup_.index("orderid")
            else:
                sort_by_orderid = False
                orderid_index = None

            bucket = [
                (entry["orderid"], entry[field_to_return])
                if sort_by_orderid
                else entry[field_to_return]
                for entry in data
                if all(
                    (
                        entry[field] == value
                        if not isinstance(value, (list, tuple, np.ndarray))
                        else entry[field] in value
                    )
                    for field, value in zip(field_to_lookup_, value_to_lookup_)
                )
                and all(entry[field] != "" for field in field_to_lookup_)
            ]

            if len(bucket) == 0:
                return np.array([])
            else:
                if sort_by_orderid:
                    # Create a dict mapping order ids to their index in value_to_lookup
                    orderid_to_index = {
                        value: index
                        for index, value in enumerate(value_to_lookup_[orderid_index])
                    }
                    # Sort the bucket based on the order of 'orderid' in value_to_lookup
                    bucket.sort(key=lambda x: orderid_to_index[x[0]])
                    # Return only the field_to_return values
                    return np.array([x[1] for x in bucket])
                else:
                    return np.array(bucket)

    if not (
        isinstance(field_to_lookup, (str, list, tuple, np.ndarray))
        and isinstance(value_to_lookup, (str, list, tuple, np.ndarray))
    ):
        raise ValueError(
            "Both 'field_to_lookup' and 'value_to_lookup' must be strings or lists."
        )

    if isinstance(field_to_lookup, list) and isinstance(value_to_lookup, str):
        raise ValueError(
            "Unsupported input: 'field_to_lookup' is a list and 'value_to_lookup' is a string."
        )

    if isinstance(book, list):
        return filter_and_return(book)
    elif isinstance(book, str) and book in {"orderbook", "positions"}:
        book_data = fetch_book(book)
        return filter_and_return(book_data)
    else:
        logger.error(f"Invalid book type '{book}'.")
        raise ValueError("Invalid book type.")
