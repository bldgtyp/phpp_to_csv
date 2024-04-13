# -*- coding: utf-8 -*-
# -*- Python Version: 3.11 -*-

"""Export Envelope Surface R-Value Data CSV files from the Main PHPP DataFrame"""

import re
import pandas as pd


def get_surface_values(_df_main: pd.DataFrame) -> pd.DataFrame:
    # Pull the R-Value and surface information
    srfcValues_df = _df_main.loc[446:457]
    srfcValues_df2 = srfcValues_df.dropna(how="any")

    return srfcValues_df2


def get_surface_R_value_info(_df_main: pd.DataFrame, _srfc_values: pd.DataFrame) -> pd.Series:
    # Pull out the Group information from the last column...
    # tempSeries = _srfc_values[cols[-1]]
    tempSeries = _srfc_values[_srfc_values.columns[-1]]
    tempSeries2 = tempSeries.str.split("-").tolist()

    groups = []
    for each in tempSeries2:
        try:
            groups.append(each[0])
        except:
            groups.append(None)

    return pd.Series(groups, index=_srfc_values.index, name="GroupNum")


def part_a(variant_names: pd.Series, _srfc_values: pd.DataFrame, _newSeries_groups: pd.Series) -> pd.DataFrame:
    # Determine the Exposure type based on the group Number
    exposures = []
    for each in _newSeries_groups.values:
        try:
            if int(each) == 9 or int(each) == 11 or int(each) == 17:
                exposures.append("B")
            else:
                exposures.append("A")
        except:
            exposures.append(None)
    newSeries_exposures = pd.Series(exposures, index=_srfc_values.index, name="Exposure")

    # Clean the Assembly names
    assmby_names_cleaned = []
    for each in _srfc_values["Datatype"].values.tolist():
        try:
            assmby_names_cleaned.append(each.split("_-_")[1].replace("_", " "))
        except:
            assmby_names_cleaned.append(each)

    datatype_clean = pd.Series(assmby_names_cleaned, index=_srfc_values.index, name="Datatype")

    srsLst = []
    # Add in the new categories
    srsLst.append(datatype_clean)
    srsLst.append(_srfc_values["Units"])
    srsLst.append(_newSeries_groups)
    srsLst.append(newSeries_exposures)

    # Remove the group nums from the column values
    for var in variant_names:
        vals = _srfc_values[var].values

        seriesVals = []
        for val in vals:
            try:
                seriesVals.append(val.split("-")[1])
            except:
                seriesVals.append(val)

        newSeries_temp = pd.Series(seriesVals, index=_srfc_values.index, name=var)
        srsLst.append(newSeries_temp)

    # Create the new DF for output
    srfcValues_df3 = pd.concat(srsLst, axis=1)

    return srfcValues_df3


def part_b(_part_a_df: pd.DataFrame) -> pd.DataFrame:
    # Clean up the Datatype (surface) names
    srfcTypeNames = _part_a_df["Datatype"].str.upper().values.tolist()
    pat = re.compile("\d\d+UD-")

    newNamesList = []
    for each in srfcTypeNames:
        grp = pat.search(each.upper())
        if grp != None:
            newNamesList.append((each[grp.span()[1] :].replace("_", " ")))
        else:
            newNamesList.append(each)

    srfcValues_df4 = _part_a_df
    srfcValues_df4["Datatype"] = newNamesList

    return srfcValues_df4


def create_csv_rValues(
    _df_main: pd.DataFrame,
    variant_names: pd.Series,
) -> list[tuple[str, str]]:
    """Creates the Envelope R-Values and Surface Data CSV files.

    Arguments:
    ----------
        * _df_main (pd.DataFrame): The Main PHPP DataFrame.
        * variant_names (pd.Series): A Series with the Variant Names.
        * _output_path_1 (pathlib.Path): The CSV output file path for the Surface Data CSV.
        * _output_path_2 (pathlib.Path): The CSV output file path for the R-Values CSV.

    Returns:
    --------
        * List[Tuple[str, str]]: A list of Tuples with the filename and the CSV file as a string.
    """

    srfc_values = get_surface_values(_df_main)
    newSeries_groups = get_surface_R_value_info(_df_main, srfc_values)
    part_a_df = part_a(variant_names, srfc_values, newSeries_groups)
    sfc_values_output_df = part_b(part_a_df)

    # Pull the R-Value information for each variant
    rValues_df = _df_main.loc[289:298]

    # rValues_df.columns = rValues_df.columns.str.upper()
    rValues_df2 = rValues_df.dropna(how="any").T
    cols = rValues_df2.loc["Datatype"]
    rValues_df2.columns = [cols.tolist()]

    # Clean up the column headings
    rValues_df2.columns = [x[0].upper().replace("_", " ") for x in rValues_df2.columns]

    # Clean up the 'Datatype' row
    rValues_df2.loc["Datatype"] = rValues_df2.loc["Datatype"].str.upper()
    rValues_df2.loc["Datatype"] = rValues_df2.loc["Datatype"].str.replace("_", " ")

    # Add the index as col
    newIndex = pd.Series(rValues_df2.index.tolist(), index=rValues_df2.index)
    rValues_df3 = rValues_df2.insert(0, "Name", newIndex)
    rValues_df4 = rValues_df2

    # Clean up the Surfaces List
    # Get the List of Assemblies actually used in the model
    surfaceNamesInTheModel = sfc_values_output_df["Datatype"].str.upper().tolist()
    surfaceNamesInTheModel.append("Name")

    # Filter out any surfaces that aren't actually used in the model
    rValues_df5 = rValues_df4.drop(columns=[col for col in rValues_df4 if col not in surfaceNamesInTheModel])

    # Export to csv
    return [
        ("envelope_rValues", sfc_values_output_df.to_csv(index=False)),
        ("envelope_srfcValues", rValues_df5.to_csv(index=False)),
    ]
