import json
from abc import ABC, abstractmethod
import threading
import inspect
from threading import Thread
from datetime import time
from time import sleep
from typing import Optional
import os
from volstreet.config import logger
from volstreet.utils.data_io import load_combine_save_json_data
from volstreet.utils.communication import notifier
from volstreet.utils.core import current_time
from volstreet.dealingroom import Index, SharedData, get_strangle_indices_to_trade
from volstreet.angel_interface.login import login
from volstreet.strategies.strats import (
    intraday_strangle,
    intraday_trend,
    overnight_straddle,
    biweekly_straddle,
    buy_weekly_hedge,
)


class BaseStrategy(ABC):
    strats = []

    def __init__(
        self,
        parameters,  # Note: The type is not specified, it can be list or dict
        special_parameters: Optional[dict] = None,
        indices: Optional[list[str]] = None,
        start_time: tuple = (9, 16),
        strategy_tags: Optional[list[str]] = None,
        client_data: Optional[dict] = None,
    ):
        self.start_time = start_time
        self.client_data = {} if client_data is None else client_data
        self._strategy_tags = strategy_tags
        self._indices = indices
        self._parameters = parameters
        self._special_parameters = special_parameters

        # Initialize attributes that will be set in `run`
        self.strategy_tags = None
        self.indices_to_trade = None
        self.parameters = None
        self.special_parameters = None
        self.strategy_threads = None

    def __repr__(self):
        return (
            f"{self.__class__.__name__}("
            f"parameters="
            f"{self._truncate_or_str(self.parameters if self.parameters is not None else self._parameters)}, "
            f"indices={None if self.indices_to_trade is None else [index.name for index in self.indices_to_trade]}, "
            f"tags={self.strategy_tags if self.strategy_tags is not None else self._strategy_tags}, "
            f"client_data={self._truncate_or_str(self.client_data)})"
        )

    @staticmethod
    def _truncate_or_str(obj, max_len=50):
        s = str(obj)
        return s if len(s) <= max_len else s[:max_len] + "..."

    @abstractmethod
    def initialize_indices(self, indices: Optional[list] = None) -> list[Index]:
        pass

    @abstractmethod
    def set_strategy_tags(
        self, strategy_tags: Optional[list[str] | str] = None
    ) -> list[str]:
        pass

    @staticmethod
    def set_parameters(parameters, special_parameters):
        # Ensure parameters is a list of dictionaries
        parameters = [parameters] if isinstance(parameters, dict) else parameters

        # Ensure each item in special_parameters is a list of dictionaries
        if special_parameters:
            special_parameters = {
                key: [value] if isinstance(value, dict) else value
                for key, value in special_parameters.items()
            }

        return parameters, special_parameters

    def no_trade(self):
        notifier(
            f"No {self.__class__.__name__} trade today",
            self.client_data.get("webhook_url"),
        )

    def setup_thread(self, index: Index, tag: str, strategy) -> Thread:
        index_parameters = self.parameters[index.name][tag]
        return Thread(
            target=strategy, kwargs=index_parameters, name=f"{index.name}_{tag}".lower()
        )

    def setup_threads(self, indices: list[Index]) -> list[Thread]:
        if len(indices) == 0:
            return [Thread(target=self.no_trade)]
        strategy_threads = [
            self.setup_thread(index, tag, strategy)
            for index in indices
            for tag, strategy in zip(self.strategy_tags, self.strats)
        ]
        return strategy_threads

    def initialize_parameters(self, parameters, special_parameters) -> dict:
        """Returns a dictionary of parameters for each index and strategy tag."""

        # Add webhook url and strategy tag to each parameter dictionary
        for tag, param in zip(self.strategy_tags, parameters):
            param.update(
                {
                    "notification_url": self.client_data.get("webhook_url"),
                    "strategy_tag": tag,
                }
            )

        # Organize parameters by strategy tag
        param_by_tag = {
            tag: param for tag, param in zip(self.strategy_tags, parameters)
        }

        # Initialize final output dictionary
        final_parameters = {}

        # Iterate through each index to populate final_parameters
        for index in self.indices_to_trade:
            final_parameters[index.name] = {}

            # Initialize with base parameters and update the param with the underlying
            for tag in self.strategy_tags:
                param = param_by_tag[tag].copy()
                param.update({"underlying": index})
                final_parameters[index.name][tag] = param

            # Update with special parameters if available
            special_for_index = (
                special_parameters.get(index.name, [])
                if special_parameters is not None
                else []
            )
            for tag, special_param in zip(self.strategy_tags, special_for_index):
                if special_param:
                    final_parameters[index.name][tag].update(special_param)
        logger.info(
            f"Initializing {self.__class__.__name__} with parameters: {final_parameters}"
        )
        return final_parameters

    def run(self):
        """This function will run the strategy and IMPORTANTLY block until all threads are finished."""

        # Moved initialization methods here
        self.strategy_tags = self.set_strategy_tags(self._strategy_tags)
        self.indices_to_trade = self.initialize_indices(self._indices)
        self.parameters, self.special_parameters = self.set_parameters(
            self._parameters, self._special_parameters
        )
        self.parameters = self.initialize_parameters(
            self.parameters,
            self.special_parameters,
        )
        self.strategy_threads = self.setup_threads(self.indices_to_trade)

        while current_time().time() < time(*self.start_time):
            logger.info(
                f"Waiting for {self.__class__.__name__} to start at {self.start_time}"
            )
            sleep(5)

        # Start all threads
        for thread in self.strategy_threads:
            thread.start()

        # Join all threads
        for thread in self.strategy_threads:
            thread.join()

        # Save data
        for index in self.indices_to_trade:
            for strategy_tag in self.strategy_tags:
                save_strategy_data(
                    index=index,
                    strategy_tag=strategy_tag,
                    user=self.client_data.get("user"),
                    notification_url=self.client_data.get("webhook_url"),
                    default_structure=list,
                )

    def save_data(self, indices: list, strategy_tag: str = None):
        for index in indices:
            save_strategy_data(
                index=index,
                strategy_tag=strategy_tag,
                user=self.client_data.get("user"),
                notification_url=self.client_data.get("webhook_url"),
                default_structure=list,
            )


class IntradayStrangle(BaseStrategy):
    strats = [intraday_strangle]

    def __init__(
        self,
        parameters: dict,
        special_parameters: Optional[dict] = None,
        indices: Optional[list] = None,
        start_time: Optional[tuple] = (9, 16),
        safe_indices: Optional[list] = None,
        only_expiry: Optional[bool] = False,
        use_shared_data: Optional[bool] = False,
        strategy_tag: Optional[list[str]] = None,
        client_data: Optional[dict] = None,
    ):
        self.safe_indices = safe_indices
        self.only_expiry = only_expiry
        self.use_shared_data = use_shared_data
        self.shared_data = SharedData() if use_shared_data else None
        self.client_data = {} if client_data is None else client_data

        super().__init__(
            parameters=parameters,
            special_parameters=special_parameters,
            indices=indices,
            start_time=start_time,
            strategy_tags=strategy_tag,
            client_data=client_data,
        )

    def set_strategy_tags(self, strategy_tags: Optional[list[str]] = None) -> list[str]:
        return strategy_tags or ["Intraday strangle"]

    def initialize_indices(self, indices: Optional[list] = None) -> list[Index]:
        indices = indices or ["NIFTY", "BANKNIFTY", "FINNIFTY", "MIDCPNIFTY"]
        indices = [Index(index) for index in indices]
        indices: list[Index] | [] = get_strangle_indices_to_trade(
            *indices, safe_indices=self.safe_indices, only_expiry=self.only_expiry
        )
        if indices:
            notifier(
                f"Trading strangle on {', '.join([index.name for index in indices])}.",
                self.client_data.get("webhook_url"),
                "INFO",
            )
        return indices

    def initialize_parameters(self, parameters, special_parameters) -> dict:
        number_of_indices = len(self.indices_to_trade) if self.indices_to_trade else 1
        parameters[0]["quantity_in_lots"] = max(
            parameters[0]["quantity_in_lots"] // number_of_indices,
            1,
        )

        # Setting the shared data
        parameters[0]["shared_data"] = self.shared_data

        parameters = super().initialize_parameters(parameters, special_parameters)

        return parameters

    def run(self):
        # Start the data updater thread
        update_data_thread = (
            threading.Thread(target=self.shared_data.update_data)
            if self.use_shared_data
            else None
        )
        while current_time().time() < time(*self.start_time):
            logger.info(
                f"Waiting for {self.__class__.__name__} to start at {self.start_time}"
            )
            sleep(5)

        if self.use_shared_data and update_data_thread is not None:
            update_data_thread.start()

        # Run the strategy
        super().run()

        # Stop the data updater thread
        if self.use_shared_data and update_data_thread is not None:
            self.shared_data.force_stop = True
            update_data_thread.join()


class IntradayTrend(BaseStrategy):
    strats = [intraday_trend]

    def set_strategy_tags(
        self, strategy_tags: Optional[list[str] | str] = None
    ) -> list[str]:
        return strategy_tags or ["Intraday trend"]

    def initialize_indices(self, indices: Optional[list] = None) -> list[Index]:
        indices = indices or ["NIFTY", "BANKNIFTY", "FINNIFTY"]
        return [Index(index) for index in indices]


class OvernightStraddle(BaseStrategy):

    """Since the overnight straddle is a combination of two strategies (main and hedge),
    the parameters should be a list of two dictionaries. The first dictionary will be used
    for the main strategy and the second dictionary will be used for the hedge strategy.

    Similarly, the special parameters should be a dictionary of lists. The keys of the dictionary
    should be the index names and the values should be a list of two dictionaries. The first dictionary
    will be used for the main strategy and the second dictionary will be used for the hedge strategy.
    """

    strats = [buy_weekly_hedge, overnight_straddle]

    def set_strategy_tags(
        self, strategy_tags: Optional[list[str] | str] = None
    ) -> list[str]:
        return strategy_tags or ["Weekly hedge", "Overnight short straddle"]

    def initialize_indices(self, indices: Optional[list] = None) -> list[Index]:
        indices = indices or ["NIFTY"]
        return [Index(index) for index in indices]


class BiweeklyStraddle(BaseStrategy):
    """Since the biweekly straddle is a combination of two strategies (main and hedge),
    the parameters should be a list of two dictionaries. The first dictionary will be used
    for the main strategy and the second dictionary will be used for the hedge strategy.

    Similarly, the special parameters should be a dictionary of lists. The keys of the dictionary
    should be the index names and the values should be a list of two dictionaries. The first dictionary
    will be used for the main strategy and the second dictionary will be used for the hedge strategy.
    """

    strats = [buy_weekly_hedge, biweekly_straddle]

    def set_strategy_tags(
        self, strategy_tags: Optional[list[str] | str] = None
    ) -> list[str]:
        return strategy_tags or ["Biweekly hedge", "Biweekly straddle"]

    def initialize_indices(self, indices: Optional[list] = None) -> list[Index]:
        indices = indices or ["NIFTY"]
        return [Index(index) for index in indices]


class Client:
    config_file = "client_config.json"
    strategy_function_map = {
        "intraday_strangle": IntradayStrangle,
        "intraday_trend": IntradayTrend,
        "overnight_straddle": OvernightStraddle,
        "biweekly_straddle": BiweeklyStraddle,
    }

    def __init__(
        self,
        user: str,
        pin: str,
        authkey: str,
        apikey: str,
    ):
        self.user = user
        self.pin = pin
        self.apikey = apikey
        self.authkey = authkey
        self.webhook_urls = {}
        self.name = None
        self.strategies = []

    @classmethod
    def from_name(cls, client: str) -> "Client":
        try:
            user = __import__("os").environ[f"{client}_USER"]
            pin = __import__("os").environ[f"{client}_PIN"]
            apikey = __import__("os").environ[f"{client}_API_KEY"]
            authkey = __import__("os").environ[f"{client}_AUTHKEY"]
        except KeyError:
            raise KeyError(
                f"Environment variables for {client} not found. Please check if the environment variables are set."
            )

        instance = cls(user, pin, authkey, apikey)
        instance.name = client
        try:  # Try to set the webhook url
            instance.webhook_urls["default"] = __import__("os").environ[
                f"{client}_WEBHOOK_URL"
            ]
        except KeyError:
            pass

        return instance

    def set_webhook_urls(self) -> None:
        for strategy in self.strategy_function_map.keys():
            try:
                self.webhook_urls[strategy] = __import__("os").environ[
                    f"{self.name}_WEBHOOK_URL_{strategy.upper()}"
                ]
            except KeyError:
                pass

    def login(self) -> None:
        login(
            self.user,
            self.pin,
            self.apikey,
            self.authkey,
            self.webhook_urls.get("default"),
        )

    def load_strats(self) -> None:
        with open(self.config_file, "r") as f:
            config_data = json.load(f)

        client_info = config_data[self.name]

        for strategy_data in client_info["strategies"]:
            strategy_class = self.strategy_function_map[strategy_data["type"]]
            webhook_url = self.webhook_urls.get(
                strategy_data["type"], self.webhook_urls.get("default")
            )
            strategy = strategy_class(
                **strategy_data["init_params"],
                client_data={"user": self.user, "webhook_url": webhook_url},
            )
            self.strategies.append(strategy)


def run_client(client: Client) -> None:
    client.set_webhook_urls()
    client.login()
    client.load_strats()

    for strategy in client.strategies:
        t = Thread(target=strategy.run)
        t.start()


def save_strategy_data(
    index,
    strategy_tag,
    user,
    notification_url,
    default_structure,
    file_name=None,
):
    if file_name is None:
        strategy_tag_for_file_name = strategy_tag.lower().replace(" ", "_")
        file_name = f"{index.name}_{strategy_tag_for_file_name}.json"

    try:
        load_combine_save_json_data(
            new_data=index.strategy_log[strategy_tag],
            file_path=f"{user}\\{file_name}",
            default_structure=default_structure,
        )
        notifier(
            f"Appended data for {strategy_tag.lower()} on {index.name}.",
            notification_url,
        )
    except Exception as e:
        notifier(
            f"Appending {strategy_tag.lower()} data failed for {index.name}: {e}",
            notification_url,
        )


def add_env_vars_for_client(
    name: str,
    user: str,
    pin: str,
    api_key: str,
    auth_key: str,
    webhook_url: Optional[str] = None,
):
    # Specify the variable name and value
    var_dict = {
        f"{name}_USER": user,
        f"{name}_PIN": pin,
        f"{name}_API_KEY": api_key,
        f"{name}_AUTHKEY": auth_key,
    }

    if webhook_url is not None:
        var_dict[f"{name}_WEBHOOK_URL"] = webhook_url

    # Use the os.system method to set the system-wide environment variable
    for var_name, var_value in var_dict.items():
        os.system(f"setx {var_name} {var_value}")


def modify_strategy_params(client_config_data, client_name, strategy_name, init_params):
    """
    Update the init_params of a specific strategy for a specific client in the given JSON data.
    Adds the client and/or strategy if they don't exist.

    Parameters:
    - json_data (dict): The original JSON data as a Python dictionary.
    - client_name (str): The name of the client to update.
    - strategy_name (str): The name of the strategy to update.
    - new_init_params (dict): The new init_params to set.

    Returns:
    - bool: True if the update/addition was successful, False otherwise.
    """
    # If client does not exist, add it
    if client_name not in client_config_data:
        print(f"Client {client_name} not found. Adding new client.")
        client_config_data[client_name] = {"strategies": []}

    # Search for the strategy for the client
    for strategy in client_config_data[client_name]["strategies"]:
        if strategy["type"] == strategy_name:
            # Update the init_params
            strategy["init_params"].update(init_params)
            print(f"Updated {strategy_name} for {client_name}.")
            return True

    # If strategy not found, add it
    print(
        f"Strategy {strategy_name} not found for client {client_name}. Adding new strategy."
    )
    new_strategy = {"type": strategy_name, "init_params": init_params}
    client_config_data[client_name]["strategies"].append(new_strategy)

    return True


def get_default_params_for_strat(strat):
    """
    Given a function, it returns a dictionary containing all the default
    keyword arguments and their values.
    """
    signature = inspect.signature(strat)
    params = {
        k: v.default if v.default is not inspect.Parameter.empty else None
        for k, v in signature.parameters.items()
    }
    # Remove the 'underlying' parameter if it exists
    params.pop("underlying", None)
    return params
