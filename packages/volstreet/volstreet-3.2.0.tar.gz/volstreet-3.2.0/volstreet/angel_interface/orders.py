from time import sleep
import numpy as np
from SmartApi.smartExceptions import DataException
from volstreet.config import token_exchange_dict, logger
from volstreet.angel_interface.fetching import fetch_book, lookup_and_return
from volstreet.angel_interface.active_session import ActiveSession
from volstreet.utils import custom_round


def place_order(
    symbol: str,
    token: str,
    qty: int,
    action: str,
    price: str | float,
    order_tag: str = "",
    stop_loss_order: bool = False,
) -> str:
    """Price can be a str or a float because "market" is an acceptable value for price."""
    action = action.upper()
    if isinstance(price, str):
        price = price.upper()
    exchange = token_exchange_dict[token]
    params = {
        "tradingsymbol": symbol,
        "symboltoken": token,
        "transactiontype": action,
        "exchange": exchange,
        "producttype": "CARRYFORWARD",
        "duration": "DAY",
        "quantity": int(qty),
        "ordertag": order_tag,
    }

    if stop_loss_order:
        execution_price = price * 1.1
        params.update(
            {
                "variety": "STOPLOSS",
                "ordertype": "STOPLOSS_LIMIT",
                "triggerprice": round(price, 1),
                "price": round(execution_price, 1),
            }
        )
    else:
        order_type, execution_price = (
            ("MARKET", 0) if price == "MARKET" else ("LIMIT", price)
        )
        execution_price = custom_round(execution_price)
        params.update(
            {"variety": "NORMAL", "ordertype": order_type, "price": execution_price}
        )

    for attempt in range(1, 4):
        try:
            return ActiveSession.obj.placeOrder(params)
        except Exception as e:
            if attempt == 3:
                raise e
            print(
                f"Error {attempt} in placing {'stop-loss ' if stop_loss_order else ''}order for {symbol}: {e}"
            )
            sleep(2)


def handle_open_orders(order_ids, action, modify_percentage=0.01, stage=0):
    """Modifies orders if they are pending by the provided modification percentage"""

    if stage >= 10:
        print("Stage >= 10, exiting function without modifying any orders")
        return None

    stage_increment = int(modify_percentage * 100)
    stage_increment = max(stage_increment, 1)
    print(f"Calculated stage_increment as: {stage_increment}")

    order_book = fetch_book("orderbook")
    sleep(1)

    statuses = lookup_and_return(order_book, "orderid", order_ids, "status")
    print(f"Looked up order statuses: {statuses}")

    if all(statuses == "complete"):
        print("All orders are complete, exiting function without modifying any orders")
        return None
    elif any(np.isin(statuses, ["rejected", "cancelled"])):
        print(
            "Some orders are rejected or cancelled, exiting function without modifying any orders"
        )
        return None
    elif any(statuses == "open"):
        print("Some orders are open, proceeding with modifications")

        open_order_ids = [
            order_id
            for order_id, status in zip(order_ids, statuses)
            if status == "open"
        ]
        print(f"Open order ids: {open_order_ids}")

        for order_id in open_order_ids:
            relevant_fields = [
                "orderid",
                "variety",
                "symboltoken",
                "price",
                "ordertype",
                "producttype",
                "exchange",
                "tradingsymbol",
                "quantity",
                "duration",
                "status",
            ]

            current_params = lookup_and_return(
                order_book, "orderid", order_id, relevant_fields
            )

            old_price = current_params["price"]

            new_price = (
                old_price * (1 + modify_percentage)
                if action == "BUY"
                else old_price * (1 - modify_percentage)
            )
            new_price = custom_round(new_price)

            modified_params = current_params.copy()
            modified_params["price"] = new_price
            modified_params.pop("status")

            ActiveSession.obj.modifyOrder(modified_params)
            print(
                f"Modified order {order_id} with new price: {new_price} from old price: {old_price}"
            )

        order_book = fetch_book("orderbook")
        sleep(1)

        statuses = lookup_and_return(order_book, "orderid", open_order_ids, "status")
        print(f"Looked up order statuses after modifications: {statuses}")

        if any(statuses == "open"):
            print("Some orders are still open, recalling function with increased stage")
            return handle_open_orders(
                *open_order_ids,
                action=action,
                modify_percentage=modify_percentage,
                stage=stage + stage_increment,
            )

        print("All orders are now complete or closed, exiting function")


def modify_orders(order_ids, new_price):
    order_book = fetch_book("orderbook")
    sleep(1)

    relevant_fields = [
        "orderid",
        "variety",
        "symboltoken",
        "price",
        "ordertype",
        "producttype",
        "exchange",
        "tradingsymbol",
        "quantity",
        "duration",
        "status",
    ]

    order_ids_and_their_params = {
        order_id: lookup_and_return(order_book, "orderid", order_id, relevant_fields)
        for order_id in order_ids
    }

    for order_id in order_ids:
        modified_params = order_ids_and_their_params[order_id].copy()
        modified_params["price"] = new_price
        order_ids_and_their_params[order_id]["price"] = new_price
        modified_params.pop("status")

        try:
            ActiveSession.obj.modifyOrder(modified_params)
        except Exception as e:
            logger.error(f"Error in modifying order: {e}")


def modify_open_orders(
    order_ids: list[str] | tuple[str] | np.ndarray[str],
    orderbook: str | list = "orderbook",
    modify_percentage: float = 0.02,
    max_modification: float = 0.1,
    sleep_interval: float = 1,
):
    """Modifies orders if they are pending by the provided modification percentage"""

    iterations = max_modification / modify_percentage
    iterations = int(iterations)
    iterations = max(iterations, 1)

    relevant_fields = [
        "orderid",
        "variety",
        "symboltoken",
        "price",
        "ordertype",
        "transactiontype",
        "producttype",
        "exchange",
        "tradingsymbol",
        "quantity",
        "duration",
        "status",
    ]
    orderbook = fetch_book(orderbook) if isinstance(orderbook, str) else orderbook
    order_ids_and_their_params = {
        order_id: lookup_and_return(orderbook, "orderid", order_id, relevant_fields)
        for order_id in order_ids
    }

    # Filtering down to only open orders
    order_ids_and_their_params = {
        order_id: params
        for order_id, params in order_ids_and_their_params.items()
        if params["status"] != "complete"
    }

    for i in range(iterations):
        for order_id in order_ids_and_their_params:
            old_price = order_ids_and_their_params[order_id]["price"]
            action = order_ids_and_their_params[order_id]["transactiontype"]

            increment = max(0.2, old_price * modify_percentage)
            new_price = (
                old_price + increment if action == "BUY" else old_price - increment
            )
            new_price = max(0.05, new_price)
            new_price = custom_round(new_price)

            modified_params = order_ids_and_their_params[order_id].copy()
            modified_params["price"] = new_price
            order_ids_and_their_params[order_id]["price"] = new_price
            modified_params.pop("status")

            try:
                ActiveSession.obj.modifyOrder(modified_params)
            except Exception as e:
                if isinstance(e, DataException):
                    sleep(1)
                logger.error(f"Error in modifying order: {e}")
            sleep(sleep_interval)


def cancel_pending_orders(order_ids, variety="STOPLOSS"):
    if isinstance(order_ids, (list, np.ndarray)):
        for order_id in order_ids:
            ActiveSession.obj.cancelOrder(order_id, variety)
    else:
        ActiveSession.obj.cancelOrder(order_ids, variety)
