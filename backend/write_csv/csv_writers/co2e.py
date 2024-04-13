# -*- coding: utf-8 -*-
# -*- Python Version: 3.11 -*-

"""Export CO2e Data CSV files from the PHPP Main DataFrame"""

from copy import deepcopy
import pandas as pd

from backend.read_phpp.load_phpp_data import PHPPData
from backend.write_csv.csv_writers.site_energy import get_site_energy_as_df


def get_final_energy_heating_df(_df_main):
    """
    Returns:
    --------
        Datatype	                    Units	    Code Minimum	As-Drawn	Improve Windows	Improve ERV	Improve Insulation
    0
    1	Electricity (HP compact unit)	kWh/(m²a)	0	0	0	0	0
    2   Electricity (heat pump)	        Wh/(m²a)	7	4	2	2	1
    3   District heating: 1-None	    kWh/(m²a)	0	0	0	0	0
    4   Boiler                          kWh/(m²a)	0	0	0	0	0
    5   Solar thermal system	        kWh/(m²a)	0	0	0	0	0
    6   Other (heating)	                kWh/(m²a)	0	0	0	0	0
    """
    df1 = _df_main.loc[26:31]
    df2 = df1.reset_index(drop=True)
    return df2


def get_final_energy_cooling_df(_df_main: pd.DataFrame) -> pd.DataFrame:
    """
    Returns:
    --------
            Datatype	                                    Units	Code Minimum	As-Drawn	Improve Windows	Improve ERV	Improve Insulation
        0	Electricity cooling (heat pump)	                kWh/(m²a)	0.891159	0.337406	1.836116	1.836116	2.185189
        1	Auxiliary electricity cooling ventilation summerkWh/(m²a)	0.865874	1.592568	1.592568	0.74948	0.74948
        2	Electricity dehumidification (heat pump)	    kWh/(m²a)	0	0	0	0	0
        3	Auxiliary electricity (dehumidification)	    kWh/(m²a)	0	0	0	0	0
    """
    df1 = _df_main.loc[34:37]
    df2 = df1.reset_index(drop=True)
    return df2


def get_final_energy_DHW_df(_df_main: pd.DataFrame) -> pd.DataFrame:
    """
    Returns
    -------
            Datatype	                    Units	Code Minimum	As-Drawn	Improve Windows	Improve ERV	Improve Insulation
        0	Electricity (HP compact unit)	kWh/(m²a)	0	0	0	0	0
        1	Electricity (heat pump)	        kWh/(m²a)	1	1 	1	1	1
        2	District heating: 1-None	    kWh/(m²a)	0	0	0	0	0
        3	Boiler               	        kWh/(m²a)	0	0	0	0	0
        4	Solar thermal system	        kWh/(m²a)	0	0	0	0	0
        5	Electricity (direct)	        kWh/(m²a)	0	0	0	0	0
    """
    df1 = _df_main.loc[38:43]
    df2 = df1.reset_index(drop=True)
    return df2


def create_csv_CO2E(
    phpp_data: PHPPData,
    co2e_limit_tons_yr: float,
    co2e_factors: dict,
) -> tuple[str, str]:
    """Create the CO2-equiv CSV data file.

    Arguments:
    ----------
        * _df_main (pd.DataFrame): The Main PHPP DataFrame/
        * _co2e_limit_tons_yr (float): The total CO2e (tons/yr) limit for the building.
        * _source_energy_factors (dict): A dict of all the equipment fuel types use by the building.
        * _fuel_source_factors (dict): A dict of all the source-energy factors to use.
        * _fuel_emission_factors (dict): A dict of all the CO2e conversion factors to use.

    Returns:
    --------
        * Tuple[str, str]: A Tuple with the filename and the CSV file as a string.
    """

    df_site_energy = get_site_energy_as_df(phpp_data.df_main)

    # -- Remove the last row of the DataFrame, since it it represents Solar PV Yield, not consumption
    df_site_energy = df_site_energy.iloc[:-1]

    # -- Break off the heating and cooling from the final-energy DataFrame
    df_site_energy_MEL = df_site_energy[~df_site_energy["Datatype"].isin(["Heating", "Cooling", "DHW"])]

    # -- Get the data for Heating, Cooling and DHW from the main PHPP DataFrame
    df_heating_final_energy = get_final_energy_heating_df(phpp_data.df_main)
    df_cooling_final_energy = get_final_energy_cooling_df(phpp_data.df_main)
    df_DHW_final_energy = get_final_energy_DHW_df(phpp_data.df_main)

    # -- Set the Fuel Type for all the PHPP Uses.
    fuel_map = {
        "Electricity dehumidification (HP)": "ELECTRIC",
        "Electricity cooling (HP)": "ELECTRIC",
        "Other (heating)": "ELECTRIC",
        "Electricity (HP compact unit)": "ELECTRIC",
        "Electricity (heat pump)": "ELECTRIC",
        "District heating: 1-None": "ELECTRIC",
        "District heating": "ELECTRIC",
        "Wood and other biomass": "WOOD",
        "Natural gas / RE gas": "NATURAL_GAS",
        "Boiler": "FUEL_OIL_NO2",
        "Heating oil / RE methanol": "FUEL_OIL_NO2",
        "Heating oil / Methanol": "FUEL_OIL_NO2",
        "Solar thermal system": "SOLAR_THERMAL",
        "Electricity (direct)": "ELECTRIC",
        "Electricity cooling (heat pump)": "ELECTRIC",
        "Auxiliary electricity cooling ventilation summer": "ELECTRIC",
        "Auxiliary electricity cooling ventilation  summer": "ELECTRIC",
        "Auxiliary electricity cooling  ventilation summer": "ELECTRIC",
        "Auxiliary electricity cooling, ventilation summer": "ELECTRIC",
        "Electricity dehumidification (heat pump)": "ELECTRIC",
        "Auxiliary electricity (dehumidification)": "ELECTRIC",
        "Aux. electricity (DHW + solar DHW)": "ELECTRIC",
        "Dishwashing": "ELECTRIC",
        "Clothes Washing": "ELECTRIC",
        "Clothes Drying": "ELECTRIC",
        "Refrigerator": "ELECTRIC",
        "Cooking": "ELECTRIC",
        "PHI Lighting": "ELECTRIC",
        "PHI Consumer Elec.": "ELECTRIC",
        "PHI Small Appliances": "ELECTRIC",
        "Phius MEL": "ELECTRIC",
        "Phius Int Lighting": "ELECTRIC",
        "Phius Ext Lighting": "ELECTRIC",
        "Aux Elec": "ELECTRIC",
    }
    """
    # -- Replace the 'Datatype' column values with the standard format fuel-type name. 
    # -- ie: 'Electricity (HP compact unit)' --> 'ELECTRIC', etc...
    Return:
    -------	
            Datatype	    Units	    Code Minimum	As-Drawn	Improve Windows	Improve ERV	Improve Insulation
        0	ELECTRICITY	    kWh/(m²a)	0	0	0	0	0
        1	ELECTRICITY	    kWh/(m²a)	79.164444	45.1267	28.336734	25.773248	13.99775
        2	ELECTRICITY	    kWh/(m²a)	0	0	0	0	0
        3	WOOD	        kWh/(m²a)	0	0	0	0	0
        4	NATURAL_GAS	    kWh/(m²a)	0	0	0	0	0
        5	FUEL_OIL_NO2	kWh/(m²a)	0	0	0	0	0
        6	SOLAR_THERMAL	kWh/(m²a)	0	0	0	0	0
        7	ELECTRICITY	    kWh/(m²a)	0	0	0	0	0
    """
    df_heating_final_energy["FUEL"] = df_heating_final_energy["Datatype"].replace(fuel_map, inplace=False)
    df_heating_final_energy["CATEGORY"] = "SPACE_HEATING"
    df_cooling_final_energy["FUEL"] = df_cooling_final_energy["Datatype"].replace(fuel_map, inplace=False)
    df_cooling_final_energy["CATEGORY"] = "SPACE_COOLING"
    df_DHW_final_energy["FUEL"] = df_DHW_final_energy["Datatype"].replace(fuel_map, inplace=False)
    df_DHW_final_energy["CATEGORY"] = "DHW"

    # -- Re-shape the TFA Data for easier DF multiplying
    df_tfa = pd.DataFrame(phpp_data.df_tfa)
    df_tfa = df_tfa.T
    df_tfa = df_tfa.reset_index(drop=True)

    # -- Convert all the values from kWh/m2 to total kWh
    def to_gross_energy(_df, phpp_data):
        """Multiply the base DataFrame by the TFA for the variant to convert from kWh/m2 -> kWh"""
        df_gross = pd.DataFrame(
            _df[phpp_data.variant_names].values * phpp_data.df_tfa[phpp_data.variant_names].values,
            columns=phpp_data.variant_names,
        )
        df_ids = _df.loc[:, ["Datatype", "Units", "FUEL", "CATEGORY"]]
        df_ids["Units"].replace({"kWh/(m²a)": "kWh"}, inplace=True)
        df_gross.index = df_ids.index.copy()
        return pd.concat([df_ids, df_gross], axis=1)

    df_heating_final_energy_gross = to_gross_energy(df_heating_final_energy, phpp_data)
    df_cooling_final_energy_gross = to_gross_energy(df_cooling_final_energy, phpp_data)
    df_DHW_final_energy_gross = to_gross_energy(df_DHW_final_energy, phpp_data)

    # -- Deal with the MEL part
    df_site_energy_MEL_gross = deepcopy(df_site_energy_MEL)
    df_site_energy_MEL_gross["FUEL"] = "ELECTRIC"
    df_site_energy_MEL_gross["CATEGORY"] = "MEL"
    # -- Join all the final energy DataFrames together
    final_energy_gross_full_df = pd.concat(
        [
            df_heating_final_energy_gross,
            df_cooling_final_energy_gross,
            df_DHW_final_energy_gross,
            df_site_energy_MEL_gross,
        ],
        ignore_index=False,
    )
    final_energy_gross_full_df.reset_index(inplace=True, drop=True)

    # -- Create a new Dataframe with all the CO2e conversion factors for each of the values in the site energy DF
    final_energy_co2_conversion_factors = final_energy_gross_full_df.set_index(
        final_energy_gross_full_df["FUEL"], inplace=False, drop=True
    )
    for fuel_type in final_energy_co2_conversion_factors.FUEL.values:
        final_energy_co2_conversion_factors.loc[fuel_type, phpp_data.variant_names] = co2e_factors["fuels"][fuel_type][
            "value"
        ]
    final_energy_co2_conversion_factors.reset_index(inplace=True, drop=True)

    # -- Multiply the data-frames together to get Tons/CO2 for each of the items
    tonsCO2_df = deepcopy(final_energy_gross_full_df)
    tonsCO2_df[phpp_data.variant_names] = pd.DataFrame(
        final_energy_gross_full_df[phpp_data.variant_names].values
        * final_energy_co2_conversion_factors[phpp_data.variant_names].values,
        columns=phpp_data.variant_names,
    )

    # -- Sum the Heating, Cooling and DHW Groups
    tonsCO2_heating = tonsCO2_df.loc[tonsCO2_df["CATEGORY"] == "SPACE_HEATING"]
    heating_total_df = pd.DataFrame(pd.Series(tonsCO2_heating[phpp_data.variant_names].sum())).T
    heating_total_df["Units"] = "tons CO2/yr"
    heating_total_df["Datatype"] = "Heating"

    tonsCO2_cooling = tonsCO2_df.loc[tonsCO2_df["CATEGORY"] == "SPACE_COOLING"]
    cooling_total_df = pd.DataFrame(pd.Series(tonsCO2_cooling[phpp_data.variant_names].sum())).T
    cooling_total_df["Units"] = "tons CO2/yr"
    cooling_total_df["Datatype"] = "Cooling"

    tonsCO2_DHW = tonsCO2_df.loc[tonsCO2_df["CATEGORY"] == "DHW"]
    DHW_total_df = pd.DataFrame(pd.Series(tonsCO2_DHW[phpp_data.variant_names].sum())).T
    DHW_total_df["Units"] = "tons CO2/yr"
    DHW_total_df["Datatype"] = "DHW"

    # -- Pull out the MEL part
    MEL_df = tonsCO2_df.loc[tonsCO2_df["CATEGORY"] == "MEL"]
    MEL_df_copy = deepcopy(MEL_df)
    MEL_df_copy.loc[:, ["Units"]] = "tons CO2/yr"

    # -- Put together the final DF for output
    final_CO2_df = pd.concat([heating_total_df, cooling_total_df, DHW_total_df, MEL_df_copy])
    final_CO2_df.drop("FUEL", axis=1, inplace=True)
    final_CO2_df.drop("CATEGORY", axis=1, inplace=True)
    final_CO2_df = final_CO2_df[["Datatype", "Units", *phpp_data.variant_names]]
    final_CO2_df.reset_index(drop=True, inplace=True)

    # -- Add in the target / limit
    vals = pd.Series([co2e_limit_tons_yr] * len(phpp_data.variant_names))
    front = pd.Series(["IPCC Limit", "tons CO2/yr"])
    f = pd.DataFrame(pd.concat([front, vals]).reset_index(drop=True)).T
    f.columns = final_CO2_df.columns

    final_CO2_df_with_limit = pd.concat([final_CO2_df, f], ignore_index=True, axis=0)

    # -- Export to csv
    return ("energy_TonsCO2", final_CO2_df_with_limit.to_csv(index=False))
