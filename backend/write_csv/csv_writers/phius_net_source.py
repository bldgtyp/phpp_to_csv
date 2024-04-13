# -*- coding: utf-8 -*-
# -*- Python Version: 3.11 -*-

"""Export Mechanical System Data CSV files from the Main PHPP DataFrame"""

import pandas as pd


def create_csv_Phius_net_source_energy(_df_main: pd.DataFrame, _cert_limits_abs: pd.DataFrame) -> tuple[str, str]:
    """Outputs a formatted .CSV with the Net-Primary-Energy information as per Phius.

    Arguments:
    ----------
        * _df_main (pd.DataFrame): The Main Excel DF with all the Data.
        * _cert_limits_abs (pd.DataFrame): The PHPP Certification Limits DataFrame.

    Returns:
    --------
        * Tuple[str, str]: A Tuple with the filename and the CSV file as a string.
    """

    # Create the PE data csv
    PE_df1 = _df_main.loc[391:405]

    PE_df2 = reduce_energy_by_solar(_df_main, PE_df1)

    # -- Little bit of cleanup
    PE_df3 = PE_df2.dropna(axis=0, how="all")
    PE_df4 = PE_df3._append(_cert_limits_abs.loc[325])

    return ("Phius_net_source_energy", PE_df4.to_csv(index=False))


def reduce_energy_by_solar(_df_main: pd.DataFrame, _pe_df: pd.DataFrame) -> pd.DataFrame:
    """Reduces Energy consumption by %, based on Variant's Solar PV

    Arguments:
    ----------
        * _df_main (pd.DataFrame): The Main PHPP DataFrame with all the Data.
        * _pe_df (pd.DataFrame): The 'PE' dataframe.

    Returns:
    --------
        * (pd.DataFrame) A new DF with all the consumption values reduced by some
            amount, based on the Solar PV.

    """

    PE_solar_df = _df_main.loc[406:406]
    PE_solar_data_df = PE_solar_df.iloc[:, -5:]
    PE_solar_data_df = PE_solar_data_df.apply(pd.to_numeric)
    PE_solar_data_df = PE_solar_data_df * 1.8

    # --- Add 'totals' row to each colum
    totals = _pe_df.sum(axis=0, numeric_only=False)
    totals["Datatype"] = "Totals"
    totals["Units"] = None
    PE_df2 = _pe_df._append(totals, ignore_index=True)

    # --- Separate out the 'data' columns and the 'datatype' columns
    PE_datatype_cols_df = PE_df2.iloc[:, :2]
    PE_df_data = PE_df2.iloc[:, -5:]
    PE_df_data = PE_df_data.apply(pd.to_numeric).fillna(0)

    totals_data = PE_df_data.iloc[-1]

    # -- Compute the % of total for each of the consumption areass
    pe_percentage_values_df = pd.DataFrame(PE_df_data.values / totals_data.values)
    pe_percentage_values_df.columns = PE_df_data.columns

    # -- Compute a reduction from solar for each of the consumption areas based on %
    reduction_from_solar_df = pe_percentage_values_df.mul(PE_solar_data_df.iloc[-1]).fillna(0)
    PE_NET_data_df = PE_df_data  # - reduction_from_solar_df

    # -- Recombine the final DF
    PE_NET_df = pd.concat([PE_datatype_cols_df, PE_NET_data_df], axis=1)
    PE_NET_df.drop(PE_NET_df.tail(1).index, inplace=True)

    return PE_NET_df
