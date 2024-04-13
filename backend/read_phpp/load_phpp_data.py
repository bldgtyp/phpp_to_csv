# -*- coding: utf-8 -*-
# -*- Python Version: 3.11 -*-

"""Functions to read data from the PHPP File."""

from dataclasses import dataclass
import pandas as pd
from typing import BinaryIO

from backend.read_phpp.clean_phpp_data import (
    clean_main_DataFrame,
    get_absolute_certification_limits_as_DataFrame,
    get_tfa_as_DataFrame,
    get_variant_names_as_Series,
)


@dataclass
class PHPPData:
    """Collection of PHPP Data"""

    df_main: pd.DataFrame
    df_climate: pd.DataFrame
    df_vent: pd.DataFrame
    df_cert_limits: pd.DataFrame
    df_tfa: pd.DataFrame
    variant_names: pd.Series


def _find_number_of_vent_rooms(_phpp_file: BinaryIO) -> int:
    try:
        col = pd.read_excel(_phpp_file, sheet_name="Addl vent", header=52, usecols="D")
        mask = col.isin(
            ["Additional rows: please select full rows above, and copy and insert them multiple times."]
        )  # <-- marker to indicate end of sections
        masked = col[mask == True]
        masked.dropna(inplace=True)
        first_instance = list(masked.index)[0]
        return first_instance - 2  # Correct for 0 base
    except Exception as e:
        print('Error: Check "Additional Ventilation" worksheet format?', e)
        return 33


def _read_phpp_to_DataFrame(
    _phpp_file: BinaryIO,
) -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    """Reads in the PHPP Data from the Variants, Climate and Additional-Ventilation
    Worksheets and converts results to a pandas.DataFrame. This will read the data from:

    Variants: C7:K~
    Climate: C20:P32
    Additional Vent: D52:V85

    Arguments:
    ----------
        * _phpp_file (BinaryIO): The PHPP Excel file to read from.

    Returns:
    --------
        * (tuple)
            - [0] (pd.DataFrame): The Main DataFrame with the PHPP Data.
            - [1] (pd.DataFrame): The Climate DataFrame.
            - [2] (pd.DataFrame): The Room Ventilation DataFrame.
    """

    num_vent_rooms = _find_number_of_vent_rooms(_phpp_file)

    excel_data_df = pd.read_excel(_phpp_file, sheet_name="Variants", header=7, usecols="C:K")
    excel_data_climate_df = pd.read_excel(
        _phpp_file,
        sheet_name="Climate",
        header=22,
        usecols="C:P",
        nrows=10,
        index_col=1,
    )
    excel_data_room_vent = pd.read_excel(
        _phpp_file,
        sheet_name="Addl vent",
        header=52,
        usecols="D:V",
        nrows=num_vent_rooms,
    )
    excel_data_df = clean_main_DataFrame(excel_data_df)

    return (excel_data_df, excel_data_climate_df, excel_data_room_vent)


def load_phpp_data(_phpp_file: BinaryIO) -> PHPPData:
    """Reads the designated PHPP Excel file and pulls out the relevant data
    from the Variants worksheet. Returns a PHPPData collection of organized data
    items which can be further processed / parsed as needed.

    Arguments:
    ----------
        * _phpp_file (BinaryIO): The PHPP Excel file to read from.

    Returns:
    --------
        * (PHPPData): The PHPPData object with all the data from the specified PHPP.
    """

    df_main, df_climate, df_vent = _read_phpp_to_DataFrame(_phpp_file)
    df_cert_limits_abs = get_absolute_certification_limits_as_DataFrame(df_main)
    df_tfa = get_tfa_as_DataFrame(df_main)
    variant_names = get_variant_names_as_Series(df_main)

    return PHPPData(df_main, df_climate, df_vent, df_cert_limits_abs, df_tfa, variant_names)
