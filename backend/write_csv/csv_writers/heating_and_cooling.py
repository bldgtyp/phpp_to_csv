# -*- coding: utf-8 -*-
# -*- Python Version: 3.11 -*-

"""Export Combined Heating/Cooling Energy Demand and Phius Certification CSV files from the Main PHPP DataFrame"""

import pandas as pd


def create_csv_heating_and_cooling_demand(
    _df_main: pd.DataFrame,
    _tfa_df: pd.DataFrame,
    _cert_limits_abs: pd.DataFrame,
) -> tuple[str, str]:
    # ---------------------------------------------------------------------------
    # Get the Cooling Demand results
    cooling_dem_df = _df_main.loc[428]
    cooling_dem_limit_df = _cert_limits_abs.loc[320]

    # Get the Heating Demand results
    heating_dem_df = _df_main.loc[426]
    heating_dem_limit_df = _cert_limits_abs.loc[317]

    return ("demand_HeatAndCool", output_csv([heating_dem_df, cooling_dem_df], _tfa_df, heating_dem_limit_df))


def create_csv_heating_demand(
    _df_main: pd.DataFrame,
    _tfa_df: pd.DataFrame,
    _cert_limits_abs: pd.DataFrame,
) -> tuple[str, str]:
    # Get the Heating Demand results
    heating_dem_df = _df_main.loc[425]
    heating_dem_limit_df = _cert_limits_abs.loc[317]

    return ("demand_Phius_heating", output_csv([heating_dem_df], _tfa_df, heating_dem_limit_df))


def create_csv_cooling_demand(
    _df_main: pd.DataFrame,
    _tfa_df: pd.DataFrame,
    _cert_limits_abs: pd.DataFrame,
) -> tuple[str, str]:
    # Get the Cooling Demand results
    cooling_dem_df = _df_main.loc[428]
    cooling_dem_limit_df = _cert_limits_abs.loc[320]

    return ("demand_Phius_cooling", output_csv([cooling_dem_df], _tfa_df, cooling_dem_limit_df))


def create_csv_heating_load(
    _df_main: pd.DataFrame,
    _tfa_df: pd.DataFrame,
    _cert_limits_abs: pd.DataFrame,
) -> tuple[str, str]:
    # Get the  Heating Load results
    heating_load_df = _df_main.loc[429]
    heating_load_limit_df = _cert_limits_abs.loc[321]

    return ("load_Phius_heating", output_csv([heating_load_df], _tfa_df, heating_load_limit_df))


def create_csv_cooling_load(
    _df_main: pd.DataFrame,
    _tfa_df: pd.DataFrame,
    _cert_limits_abs: pd.DataFrame,
) -> tuple[str, str]:
    # Get the Cooling Load results
    cooling_load_df = _df_main.loc[430]
    cooling_load_limit_df = _cert_limits_abs.loc[322]

    return ("load_Phius_cooling", output_csv([cooling_load_df], _tfa_df, cooling_load_limit_df))


def output_csv(
    _data: list[pd.Series],
    _tfa_df: pd.DataFrame,
    _limit_df: pd.Series,
) -> str:
    """Builds the CSV file based on the Heating/Cooling data given."""

    # ---------------------------------------------------------------------------
    # Construct a DataFrame from the input Series
    data_df = pd.concat(_data, axis=1).T

    # ---------------------------------------------------------------------------
    # --- Create the Header DF, join the data+header into a new DataFrame
    header_df = pd.DataFrame()

    for variant in data_df.columns[:2]:
        header_df[variant] = data_df[variant]

    header_df["Units"] = header_df["Units"].str.replace("/m2", "")  # 'm2' strings

    for variant in data_df.columns[2:]:
        # Convert to total kWh instead of kWh/m2
        header_df[variant] = data_df[variant].mul(_tfa_df[variant])

    # ---------------------------------------------------------------------------
    # ---- Output final data to CSV
    output_df = header_df._append(_limit_df)
    return output_df.to_csv(index=False)
