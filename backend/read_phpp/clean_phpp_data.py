# -*- coding: utf-8 -*-
# -*- Python Version: 3.11 -*-

"""Function to organize / clean / parse the primary DataFrames pulled from the PHPP."""

import numpy as np
import pandas as pd


def clean_main_DataFrame(_df_main: pd.DataFrame) -> pd.DataFrame:
    """Cleans up the 'Main' DataFrame of PHPP Data from the Variants worksheet.

    Arguments:
    ----------
        * _df_main (pd.DataFrame): The raw DataFrame read from the PHPP.

    Returns:
    --------
        * (pd.DataFrame): The cleaned and re-organized DataFrame.
    """

    # -- Get rid of the 'active variant' columns
    clean_df = _df_main.drop(_df_main.columns[2], axis=1)
    clean_df = clean_df.drop(clean_df.columns[2], axis=1)

    # -- Change the column name for 'Select Active Variant...' to 'Units'
    clean_df.rename(columns={clean_df.columns[1]: "Units"}, inplace=True)
    clean_df.reset_index(drop=True, inplace=True)
    # change the index start so it aligns with Excel
    clean_df.index = np.arange(9, len(clean_df) + 9)
    # Remove the first row with the col numbers
    clean_df.drop([9], inplace=True)
    # Remove any columns without active variant data
    clean_df.dropna(axis=1, thresh=2, inplace=True)

    # -- Rename the 'index' column
    clean_df.rename(columns={clean_df.columns[0]: "Datatype"}, inplace=True)

    # -- clean up trailing white-space in datatype names...
    clean_df["Datatype"] = clean_df["Datatype"].str.strip()
    clean_df["Datatype"] = clean_df["Datatype"].str.replace(",", " ")

    return clean_df


def get_tfa_as_DataFrame(_df_main: pd.DataFrame) -> pd.Series:
    """Return the Treated Floor Area (TFA) for each Variant as a pandas.Series

    Arguments:
    ----------
        * _df_main (pd.DataFrame): The Main DataFrame with data from the Variants Worksheet.

    Returns:
    --------
        * (pd.Series): The TFA of each Variant.
    """
    return _df_main.loc[278]


def get_variant_names_as_Series(_df_main: pd.DataFrame) -> pd.Series:
    """Return the Variants Names for each Variant as a pandas.Series

    Arguments:
    ----------
        * _df_main (pd.DataFrame): The Main DataFrame with data from the Variants Worksheet.

    Returns:
    --------
        * (pd.Series): The Variant Name of each Variant.
    """
    return _df_main.columns[2::]


def get_absolute_certification_limits_as_DataFrame(
    _df_main: pd.DataFrame,
) -> pd.DataFrame:
    """Return a DataFrame with all the PH/Phius Certification limits found in the PHPP.

    Arguments:
    ----------
        * _df_main (pd.DataFrame): The Main DataFrame with data from the Variants Worksheet.

    Returns:
    --------
        * (pd.DataFrame): A new DataFrame with the Certification Limits
    """

    # Get all the certification LIMITS in ../m2 values
    cert_limits_specific = _df_main.loc[317:325]

    # Fill any string '-' values with 0
    # If its EnerPHit or LBI, will not have any values for Peak Load limits
    cert_limits_specific = cert_limits_specific.replace("-", 0.0)

    # Get the TFA for each variant
    tfa_df = get_tfa_as_DataFrame(_df_main)

    # Calc the total limits (not .../m2 results for certification values)
    cert_limits_abs = pd.DataFrame()  # Start with an empty DataFrame
    for variant in cert_limits_specific.columns[:2]:  # Data ID cols
        cert_limits_abs[variant] = cert_limits_specific[variant]

    cert_limits_abs["Units"] = cert_limits_specific["Units"].str.replace("/m2", "")  # 'm2' strings
    for variant in cert_limits_specific.columns[2:]:  # The data cols
        print(f"cert_limits_specific[variant]: {cert_limits_specific[variant]}")
        cert_limits_abs[variant] = cert_limits_specific[variant].mul(tfa_df[variant])

    return cert_limits_abs
