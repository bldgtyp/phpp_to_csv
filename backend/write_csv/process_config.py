# -*- coding: utf-8 -*-
# -*- Python Version: 3.11 -*-

"""Process configuration class with cross-OS folder and file path handler methods."""

from dataclasses import dataclass, field
import os
import pathlib
from typing import Callable


@dataclass
class ProcessConfigWriteCSV:
    """App configuration settings and paths (Mac/PC OS)"""

    # Site--to--Source Factors by Fuel Type
    # https://portfoliomanager.energystar.gov/pdf/reference/Source%20Energy.pdf
    fuel_source_factors = {
        "ELECTRIC": 2.8,
        "NATURAL_GAS": 1.1,
        "FUEL_OIL_NO2": 1.01,
        "FUEL_OIL_NO4": 1.01,
    }

    def __init__(
        self,
        phpp_file_name: str = "",
        csv_save_path: str = "",
        num_variants: int = 5,
        co2e_factors: dict = field(default_factory=dict),
        co2e_limit_tons_yr: float = 1,
        omitted_assemblies: list[str] = field(default_factory=list),
        message: Callable = print,
    ):

        self._phpp_file_path = phpp_file_name
        self._csv_save_path = csv_save_path
        self.num_variants = num_variants
        self.co2e_factors = co2e_factors
        self.co2e_limit_tons_yr = co2e_limit_tons_yr

        self.omitted_assemblies = omitted_assemblies

        self.message = message
        self.check_paths()

    @property
    def phpp_file_path(self) -> pathlib.Path:
        return pathlib.Path(self._phpp_file_path).resolve()

    @property
    def csv_save_path(self) -> pathlib.Path:
        return pathlib.Path(self._csv_save_path).resolve()

    def csv_file_path(self, filename: str = "") -> pathlib.Path:
        return pathlib.Path(self._csv_save_path, filename).resolve()

    def check_paths(self) -> None:
        """Check if the PHPP-file and the CSV save folder exist.
        If the CSV folder does not exist, creates it.
        """
        if not self.phpp_file_path:
            print(f"Configuration Error: Please supply a valid PHPP File name to begin.")
            return

        if not os.path.exists(self.phpp_file_path):
            print(
                f'Configuration Error: Cannot find the PHPP file: "{self.phpp_file_path}". Please check the path and name?'
            )
            return

        if not os.path.exists(self.csv_save_path):
            self.message(f'No folder: "{self.csv_save_path}" found. Creating folder.')
            os.mkdir(self.csv_save_path)
