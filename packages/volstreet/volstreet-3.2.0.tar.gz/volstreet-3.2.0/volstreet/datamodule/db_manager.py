from attrs import define, field
from collections import defaultdict
from sqlalchemy import create_engine, text, TextClause
from itertools import product
import numpy as np
from typing import Optional, Iterable, List
import os
from volstreet import timeit
import pandas as pd


@define
class DBManager:
    # Database attributes
    _DB_NAME: str = field(default=None)
    _DB_USER: str = field(default=None)
    _DB_PASS: str = field(default=None)
    _DB_HOST: str = field(default=None)
    _DB_PORT: str = field(default=None)
    _database_connection_url: str = field(default=None)
    _alchemy_engine_url: str = field(default=None)

    # SQLAlchemy engine
    alchemy_engine = field(default=None, init=False)

    # Storing queries to see if caching is possible
    _queries: defaultdict = field(factory=lambda: defaultdict(list), init=False)

    def __attrs_post_init__(self):
        self._set_db_credentials()
        self._set_database_connection_urls()

    @staticmethod
    def _get_env_var(var_name: str):
        """Fetch environment variables safely."""
        var_value = os.getenv(var_name)
        if var_value is None:
            raise EnvironmentError(f"Environment variable '{var_name}' is not set.")
        return var_value

    def _set_db_credentials(self):
        self._DB_NAME = self._get_env_var("TSDB_DBNAME")
        self._DB_USER = self._get_env_var("TSDB_USER")
        self._DB_PASS = self._get_env_var("TSDB_PASS")
        self._DB_HOST = self._get_env_var("TSDB_HOST")
        self._DB_PORT = self._get_env_var("TSDB_PORT")

    def _set_database_connection_urls(self):
        self._database_connection_url = (
            f"postgres://{self._DB_USER}:{self._DB_PASS}@{self._DB_HOST}:"
            f"{self._DB_PORT}/{self._DB_NAME}?sslmode=require"
        )
        self._alchemy_engine_url = self._database_connection_url.replace(
            "postgres", "postgresql"
        )

    def set_alchemy_engine(self):
        self.alchemy_engine = create_engine(self._alchemy_engine_url)

    def get_executed_queries(self):
        return self._queries

    @staticmethod
    def generate_query_for_option_prices_df(
        index: str,
        df: pd.DataFrame,
        option_type: Optional[str] = None,
        cols_to_return: Optional[Iterable[str]] = None,
    ) -> text:
        if cols_to_return is None:
            cols_to_return = ["timestamp", "expiry", "strike", "option_type", "close"]

        columns_str = ", ".join([f"index_options.{x}" for x in cols_to_return])

        # Check if 'strike' contains tuples or floats
        first_strike = df.iloc[0]["strikes"]
        if isinstance(first_strike, (tuple, list)):
            cte_entries = [
                f"('{row.timestamp}'::timestamp, {strikes[0]}::integer, '{row.expiry}'::text, 'CE'::text), "
                f"('{row.timestamp}'::timestamp, {strikes[1]}::integer, '{row.expiry}'::text, 'PE'::text)"
                for row in df.itertuples(index=False)
                for strikes in [row.strikes]
            ]
        else:
            if option_type is None:
                raise ValueError(
                    "Option type must be provided if single strikes are provided."
                )

            # Add option_type column if it doesn't exist
            df["option_type"] = option_type

            cte_entries = [
                f"('{row.timestamp}'::timestamp, {row.strikes}::integer, '{row.expiry}'::text, '{row.option_type}'::text)"
                for row in df.itertuples(index=False)
            ]

        cte_entries_str = ", ".join(cte_entries)
        cte = f"WITH conditions AS (SELECT * FROM (VALUES {cte_entries_str}) AS t(timestamp, strike, expiry, option_type))"

        sql_query = text(
            f"""
            {cte}
            SELECT {columns_str}
            FROM index_options
            INNER JOIN conditions
            ON index_options.timestamp = conditions.timestamp 
               AND index_options.expiry = conditions.expiry
               AND index_options.strike = conditions.strike
               AND index_options.option_type = conditions.option_type
            WHERE index_options.underlying = '{index}';
            """
        )

        return sql_query

    @staticmethod
    def generate_query_for_option_prices_product(
        index: str,
        timestamps: List[str],
        expirys: List[str],
        strikes: List[float | int],
        option_type: Optional[str] = None,
        cols_to_return: Optional[Iterable[str]] = None,
    ) -> TextClause:  # Changed return type to str as SQLAlchemy is not available
        if cols_to_return is None:
            cols_to_return = [
                "timestamp",
                "expiry",
                "strike",
                "option_type",
                "close",
            ]

        # Sanity run np.unique on timestamps, expirys, strikes, option_type
        timestamps = list(np.unique(timestamps))
        expirys = list(np.unique(expirys))
        strikes = list(np.unique(strikes))

        columns_str = ", ".join([f"index_options.{x}" for x in cols_to_return])

        # Convert strikes to int if its a float
        strikes = [
            int(strike) if isinstance(strike, float) else strike for strike in strikes
        ]

        # Generate all possible combinations of timestamp, expiry, and strike
        all_combinations = list(product(timestamps, strikes, expirys))

        cte_entries_list = []
        for timestamp, strike, expiry in all_combinations:
            if option_type:
                cte_entries_list.append(
                    (
                        timestamp,
                        strike,
                        expiry,
                        f"'{option_type}'::text",
                    )
                )
            else:
                cte_entries_list.extend(
                    [
                        (timestamp, strike, expiry, "'CE'::text"),
                        (timestamp, strike, expiry, "'PE'::text"),
                    ]
                )

        # Sort the conditions by timestamp and strike
        cte_entries_list.sort(key=lambda x: (x[0], x[1]))
        cte_entries = ", ".join(
            [
                f"('{timestamp}'::timestamp, {strike}::integer, '{expiry}'::text, {option_type})"
                for timestamp, strike, expiry, option_type in cte_entries_list
            ]
        )
        cte = f"WITH conditions AS (SELECT * FROM (VALUES {cte_entries}) AS t(timestamp, strike, expiry, option_type))"

        # Base query string
        sql_query = text(
            f"""
            {cte}
            SELECT {columns_str}
            FROM index_options
            INNER JOIN conditions
            ON index_options.timestamp = conditions.timestamp 
               AND index_options.expiry = conditions.expiry
               AND index_options.strike = conditions.strike
               AND index_options.option_type = conditions.option_type
            WHERE index_options.underlying = '{index}';
        """
        )

        return sql_query

    @timeit
    def fetch_option_prices_from_tsdb(self, query: str | TextClause) -> pd.DataFrame:
        """Fetch option prices from TimescaleDB using the provided query."""
        engine = create_engine(self._alchemy_engine_url)
        with engine.connect() as connection:
            option_prices = pd.read_sql(query, connection)

        # Store the query
        self._queries["index_options"].append(query)
        return option_prices
