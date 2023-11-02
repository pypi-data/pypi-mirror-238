import os
import json
import pandas as pd
import re


def return_strategy_data(user: str, strat: str) -> pd.DataFrame:
    # Add user to path
    user_files = os.listdir(user)
    strangle_files = [file for file in user_files if strat in file]

    strat_data = pd.DataFrame()
    for file in strangle_files:
        with open(f"{user}\\{file}", "r") as f:
            data = json.load(f)
        d = pd.DataFrame(data)
        if "trend" in strat:
            matches = re.findall(r"([A-Z0-9a-z]+)", file)
            index = [*filter(lambda x: "NIFTY" in x, matches)][0]
            d["Index"] = index
        strat_data = pd.concat([strat_data, d])

    return strat_data
