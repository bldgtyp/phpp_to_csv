# -*- coding: utf-8 -*-
# -*- Python Version: 3.11 -*-

"""Export Airtightness CSV data from the Main PHPP DataFrame"""


import pandas as pd


def create_csv_airtightness(_df_main: pd.DataFrame) -> tuple[str, str]:
    """Creates the Airtightness (HR%, Vv, Vn50, etc.) CSV file based on the PHPP DataFrame.

    Arguments:
    ----------
        * _df_main (pd.DataFrame): The Main PHPP DataFrame to get the data from.

    Returns:
    --------
        * tuple[str, str]: A Tuple with the filename and the CSV file as a string.
    """

    airflow_df = _df_main.loc[436:442]
    return ("envelope_airflow", airflow_df.to_csv(index=False))
