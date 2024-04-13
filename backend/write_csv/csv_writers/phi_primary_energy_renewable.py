# -*- coding: utf-8 -*-
# -*- Python Version: 3.11 -*-

"""Export Mechanical System Data CSV files from the Main PHPP DataFrame"""

import pandas as pd


def create_csv_Phi_primary_energy_renewable(_df_main: pd.DataFrame, _cert_limits_abs: pd.DataFrame) -> tuple[str, str]:
    """Outputs a formatted .CSV with the Net-Primary-Energy information as per Phius.

    Arguments:
    ----------
        * _df_main (pd.DataFrame): The Main Excel DF with all the Data.
        * _cert_limits_abs (pd.DataFrame): The PHPP Certification Limits DataFrame.

    Returns:
    --------
        * Tuple[str, str]: A Tuple with the filename and the CSV file as a string.
    """

    # Create the PER data csv
    PE_df1 = _df_main.loc[408:423]

    # -- Little bit of cleanup
    PE_df2 = PE_df1.dropna(axis=0, how="all")
    PE_df3 = PE_df2._append(_cert_limits_abs.loc[324])

    return ("energy_PER", PE_df3.to_csv(index=False))
