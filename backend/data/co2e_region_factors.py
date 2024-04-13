# -*- coding: utf-8 -*-
# -*- Python Version: 3.11 -*-

"""Functions to Load in the CO2e Region Factors data."""

from pathlib import Path

from backend.data.json_file_io import import_dict_from_JSON_file


# -- Unit conversion functions
def lbsCO2perMWh_to_tCO2perkWh(_in: float) -> float:
    """Converts lbs-CO2-per-MWh into tons-CO2-per-kWh
    lbs-CO2/MWh * 0.0004536 metric tons/lb * 0.001 MWh/kWh = tCO2e/kWh

    ie:
    CAMEX WECC California Region Total (non-base-load): 498.7 lb-CO2e/MWh
    498.7 lbs CO2/MWh * ( 0.0004536 metric tons/lb) * 0.001 MWh/kWh = 0.0002262 metric tons CO2/kWh
    """
    return _in * 0.0004536 * 0.001


def tCO2perkWh_to_tCO2perkWh(_in) -> float:
    """Converts tons-CO2-per-kWh into tons-CO2-per-kWh"""
    return _in * 1


def tCO2perkBtu_to_tCO2perkWh(_in: float) -> float:
    """Converts tons-CO2-per-kBtu into tons-CO2-per-kWh"""
    return 1 / ((1 / _in) * 0.293071111)


def load_co2e_factors_as_dict() -> dict[str, float]:
    """Load in the CO2e Region Factors as a dictionary."""
    CONVERSION_FUNCTIONS = {
        "tons_co2_per_kWh": tCO2perkWh_to_tCO2perkWh,
        "lbs_co2_per_MWh": lbsCO2perMWh_to_tCO2perkWh,
        "tons_co2_per_kBtu": tCO2perkBtu_to_tCO2perkWh,
    }
    FILENAME = Path("backend", "data", "co2e_region_factors.json").resolve()
    data = import_dict_from_JSON_file(FILENAME)

    # -- Convert the Data in to the right units (SI)
    for region_data in data.values():
        for fuel_type_data in region_data["fuels"].values():
            fuel_unit = fuel_type_data["unit"]
            conversion_func = CONVERSION_FUNCTIONS[fuel_unit]
            fuel_type_data["value"] = conversion_func(fuel_type_data["value"])
            fuel_type_data["unit"] = "tons_co2_per_kWh"

    return data
