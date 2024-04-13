# -*- coding: utf-8 -*-
# -*- Python Version: 3.11 -*-


"""Wrapper functions to create all the CSV files from the PHPP Data."""


from backend.read_phpp import PHPPData
from backend.write_csv.csv_writers.airtightness import create_csv_airtightness
from backend.write_csv.csv_writers.bldg_data_basics import create_csv_bldg_basic_data_table
from backend.write_csv.csv_writers.climate import create_csv_radiation, create_csv_temperatures
from backend.write_csv.csv_writers.co2e import create_csv_CO2E
from backend.write_csv.csv_writers.demand_cooling_dtl import create_csv_detailed_cooling_demand
from backend.write_csv.csv_writers.demand_heating_dtl import create_csv_detailed_heating_demand
from backend.write_csv.csv_writers.heating_and_cooling import (
    create_csv_cooling_demand,
    create_csv_cooling_load,
    create_csv_heating_and_cooling_demand,
    create_csv_heating_demand,
    create_csv_heating_load,
)
from backend.write_csv.csv_writers.mech import create_csv_fresh_air_flowrates
from backend.write_csv.csv_writers.phi_primary_energy_renewable import create_csv_Phi_primary_energy_renewable
from backend.write_csv.csv_writers.phius_net_source import create_csv_Phius_net_source_energy
from backend.write_csv.csv_writers.r_value import create_csv_rValues
from backend.write_csv.csv_writers.site_energy import create_csv_SiteEnergy
from backend.write_csv.csv_writers.variant_table import create_csv_variant_table


def create_csv_files_from_phpp_data(
    phpp_data: PHPPData, co2e_limit_tons_yr: float, co2e_factors: dict[str, float], omitted_assemblies: list[str]
) -> list[tuple[str, str]]:
    """Generate all the .CSV files based on the input PHPPData object.

    Arguments:
    ----------
        * phpp_data (PHPPData): A PHPPData object with all the data pulled from the Excel file.
        * co2e_limit_tons_yr (float): The CO2e limit in tons/year.
        * co2e_factors (dict[str, float]): The CO2e factors for each energy source.
        * omitted_assemblies (list[str]): A list of the omitted assemblies.

    Returns:
    --------
        *  list[Tuple[str, str]]: A list of Tuples with: [(filename, csv_string), ...]
    """

    # format: [ (filename, csv_string), ... ]
    csv_file_names_and_data = [
        # -- Basic energy consumption
        create_csv_heating_and_cooling_demand(phpp_data.df_main, phpp_data.df_tfa, phpp_data.df_cert_limits),
        create_csv_heating_demand(phpp_data.df_main, phpp_data.df_tfa, phpp_data.df_cert_limits),
        create_csv_cooling_demand(phpp_data.df_main, phpp_data.df_tfa, phpp_data.df_cert_limits),
        create_csv_heating_load(phpp_data.df_main, phpp_data.df_tfa, phpp_data.df_cert_limits),
        create_csv_cooling_load(phpp_data.df_main, phpp_data.df_tfa, phpp_data.df_cert_limits),
        create_csv_Phius_net_source_energy(phpp_data.df_main, phpp_data.df_cert_limits),
        create_csv_SiteEnergy(phpp_data),
        create_csv_Phi_primary_energy_renewable(phpp_data.df_main, phpp_data.df_cert_limits),
        # --- CO2 Emissions
        # create_csv_CO2E(phpp_data, co2e_limit_tons_yr, co2e_factors),
        # --- Get the Model Variants info
        create_csv_variant_table(phpp_data.df_main, phpp_data.variant_names, omitted_assemblies),
        create_csv_bldg_basic_data_table(phpp_data.df_main),
        # --- Create Detailed Heating, Cooling Demand
        *create_csv_detailed_heating_demand(phpp_data.df_main, phpp_data.df_cert_limits),
        *create_csv_detailed_cooling_demand(phpp_data.df_main, phpp_data.df_cert_limits),
        # --- Airtightness
        create_csv_airtightness(phpp_data.df_main),
        *create_csv_rValues(phpp_data.df_main, phpp_data.variant_names),
        # --- Climate
        create_csv_radiation(phpp_data.df_climate),
        create_csv_temperatures(phpp_data.df_climate),
        # --- Mechanical
        create_csv_fresh_air_flowrates(phpp_data.df_vent),
    ]

    return csv_file_names_and_data
