# -*- coding: utf-8 -*-
# -*- Python Version: 3.10 -*-

"""Util Functions for reading json data files."""

import json
import os
from pathlib import Path


def import_dict_from_JSON_file(filepath: Path) -> dict:
    """Read in a dict from a JSON file."""
    if not os.path.exists(filepath):
        raise FileNotFoundError(f"File not found: {filepath}")

    try:
        with open(filepath, "r") as read_file:
            return json.load(read_file)
    except Exception as e:
        raise Exception(f"Error reading JSON file: {filepath}", e)
