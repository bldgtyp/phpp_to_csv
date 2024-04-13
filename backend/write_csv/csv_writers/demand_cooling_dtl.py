# -*- coding: utf-8 -*-
# -*- Python Version: 3.11 -*-

"""Export Annual Cooling Energy Demand CSV files from the Main PHPP DataFrame"""


import pandas as pd


def clean_file_name(_filename: str) -> str:
    """Clean an input file name and remove disallowed characters ("/", etc..)"""
    return str(_filename).replace("/", "_").replace("\\", "_")


def create_csv_detailed_cooling_demand(_df_main: pd.DataFrame, _cert_limits_abs: pd.DataFrame) -> list[tuple[str, str]]:
    """Creates the Annual Cooling Demand data CSV files for each Variant based on the PHPP Climate DataFrame.

    Arguments:
    ----------
        * _df_climate (pd.DataFrame): The Main PHPP DataFrame to get the data from.
        * _cert_limits_abs (pd.DataFrame): The Certification Limits DataFrame.
        * _output_path (pathlib.Path): The full output file path for the CSV.

    Returns:
    --------
        * List[Tuple[str, str]]: A list of Tuples with the filename and the CSV file as a string.
    """

    # Create the Detailed Heating Demand CSV
    demand_cooling_losses_df = _df_main.loc[350:364]
    demand_cooling_gains_df = _df_main.loc[365:371]

    # Get the variant column names (ignore the first two items 'Datatype' and 'Units')
    cols = demand_cooling_losses_df.columns[2:].tolist()

    # Get the datatype and units values for both losses and gains
    dTtpes = pd.concat(
        [demand_cooling_losses_df["Datatype"], demand_cooling_gains_df["Datatype"]],
        sort=True,
    )
    units = pd.concat([demand_cooling_losses_df["Units"], demand_cooling_gains_df["Units"]], sort=True)

    # Create the 'Demand Limit' items in a way that matches the format of the main DF
    tempLimits = {}
    for colName in cols:
        index_temp = ["Datatype", "Units", "Losses", "Gains"]
        vals = [
            "Cooling Demand Limit",
            "kWh",
            _cert_limits_abs.loc[318][colName],
            _cert_limits_abs.loc[318][colName],
        ]
        newSeries = pd.Series(vals, index=index_temp)
        tempLimits[colName] = newSeries

    # Create the main DF for outputting
    def create_new_DF(_colHead, _colName, _df):
        frame = {_colHead: _df[_colName]}
        r = pd.DataFrame(frame)
        return r

    losses = {}
    gains = {}
    for colName in cols:
        losses[colName] = create_new_DF("Losses", colName, demand_cooling_losses_df)
        gains[colName] = create_new_DF("Gains", colName, demand_cooling_gains_df)

    output = {}
    for k, v in losses.items():
        r1 = pd.concat([losses[k], gains[k]], sort=True)
        r2 = pd.concat([dTtpes, units, r1["Losses"], r1["Gains"]], axis=1)
        output[k] = r2.fillna(0)

    # Add the Demand Limits to the main DFs
    for k, v in output.items():
        output[k] = v._append(tempLimits[k], ignore_index=True)

    # Create the CSV file for each of the variants
    output_tuples_: list[tuple[str, str]] = []
    for k, v in output.items():
        new_filename = clean_file_name("cooling_demand_{}".format(k))
        output_tuples_.append((new_filename, v.to_csv(index=False)))
    return output_tuples_
