# -*- coding: utf-8 -*-
# -*- Python Version: 3.11 -*-

"""Export Variant Data Table CSV files from the Main PHPP DataFrame"""

import numpy as np
import pandas as pd

pd.options.mode.chained_assignment = None  # default='warn'


def create_csv_variant_table(
    _df_main: pd.DataFrame,
    _variant_names: pd.Series,
    _omitted_assemblies: list[str],
) -> tuple[str, str]:
    """Create the comprehensive Variant Data Table with bits from all over the place.

    Arguments:
    ----------
        * _df_vent (pd.DataFrame): The PHPP Ventilation DataFrame.
        * _variant_names (pd.Series): A Series with all the Variant Names.
        * _omitted_assemblies (list[str]): A list of assembly names to omit from the final table.

    Returns:
    --------
        * Tuple[str, str]: A Tuple with the filename and the CSV file as a string.
    """
    #  START = 202 # PHPP-9
    START = 270  # PHPP-10

    # Certification?
    cert_df1 = _df_main.loc[189 + START]

    # Energy and Load values
    # --------------------------------------------------------------------------
    # Total Primary Energy
    pe_df1 = _df_main.loc[121 + START : 135 + START]
    pe_df2 = pe_df1[_variant_names].sum()
    pe_df3 = pd.Series(["Total Primary Energy", "kWh/yr"], index=["Datatype", "Units"])
    pe_df4 = pe_df3._append(pe_df2)

    # Total Primary Energy Renewable
    per_df1 = _df_main.loc[138 + START : 152 + START]
    per_df2 = per_df1[_variant_names].sum()
    per_df3 = pd.Series(["Total Primary Energy Renewable", "kWh/yr"], index=["Datatype", "Units"])
    per_df4 = per_df3._append(per_df2)

    # Total Site Energy
    se_df1 = _df_main.loc[104 + START : 118 + START]
    se_df2 = se_df1[_variant_names].sum()
    se_df3 = pd.Series(["Total Site Energy", "kWh/yr"], index=["Datatype", "Units"])
    se_df4 = se_df3._append(se_df2)

    # TFA
    tfa_df = _df_main.loc[210]

    # Heating and Cooling Demand
    hd_df1 = _df_main.loc[155 + START]
    hd_df2 = pd.concat([tfa_df, hd_df1], axis=1).T[_variant_names].prod()
    hd_df3 = pd.Series(["Heat Demand", "kWh/yr"], index=["Datatype", "Units"])
    hd_df4 = hd_df3._append(hd_df2)

    cd_df1 = _df_main.loc[158 + START]
    cd_df2 = pd.concat([tfa_df, cd_df1], axis=1).T[_variant_names].prod()
    cd_df3 = pd.Series(["Cooling Demand", "kWh/yr"], index=["Datatype", "Units"])
    cd_df4 = cd_df3._append(cd_df2)

    demand_results_df1 = pd.concat([cert_df1, pe_df4, per_df4, se_df4, hd_df4, hd_df1, cd_df4, cd_df1], axis=1)
    demand_results_df2 = demand_results_df1.T

    # Peak Loads
    ld_df1 = _df_main.loc[193 + START : 195 + START]

    # Combine it all together
    key_results_df = demand_results_df2._append(ld_df1).reset_index(drop=True)

    # Envelope R-Values and Airtightness
    # --------------------------------------------------------------------------
    env_df1 = _df_main.loc[19 + START : 31 + START]
    env_df1a = pd.DataFrame(env_df1)
    new_datatype_column = env_df1["Datatype"].str.replace("_", " ").str.replace("Generic ", "")
    env_df1a["Datatype"] = new_datatype_column

    def is_unused_assembly(_in):
        if _in in _omitted_assemblies:
            return True
        else:
            return False

    # Filter out any surfaces that aren't actually used in the model
    env_df2 = env_df1a[env_df1a["Datatype"].map(is_unused_assembly) == False]

    # Convert in the envelope leakage rate
    q50_ip1 = env_df2.loc[START + 31][_variant_names] * 0.054680665
    q50_ip2 = pd.Series(["Envelope Air Leakage Rate (q50)", "cfm/ft2"], index=["Datatype", "Units"])
    q50_ip3 = q50_ip2._append(q50_ip1)
    env_df2.loc[START + 31] = q50_ip3
    env_results_df2 = env_df2.dropna(how="any")

    # Systems
    # --------------------------------------------------------------------------
    # Mech System info
    sys_df1 = _df_main.loc[34 + START : 42 + START]

    # Re-set the units for duct
    ductLen_s1 = sys_df1.loc[308][_variant_names] * 3.280839895
    ductLen_s2 = pd.Series(["Cold Air Duct Length (ea)", "ft"], index=["Datatype", "Units"])
    ductLen_s3 = ductLen_s2._append(ductLen_s1)

    sys_df2 = sys_df1.copy(deep=True)
    sys_df2.loc[START + 38] = ductLen_s3

    # Insulation
    ductInsul_s1 = sys_df2.loc[START + 39][_variant_names] * 0.039370079
    ductInsul_s2 = pd.Series(["Cold Air Duct Insulation Thickness", "inches"], index=["Datatype", "Units"])
    ductInsul_s3 = ductInsul_s2._append(ductInsul_s1)

    sys_df3 = sys_df2.copy(deep=True)
    sys_df3.loc[START + 39] = ductInsul_s3
    sys_df4 = sys_df3.reset_index(drop=True)

    # Add the breaks
    brk_env = pd.DataFrame(np.nan, index=["break"], columns=_df_main.columns.tolist())
    brk_env["Datatype"] = "ENVELOPE"

    brk_sys = pd.DataFrame(np.nan, index=["break"], columns=_df_main.columns.tolist())
    brk_sys["Datatype"] = "SYSTEMS"

    brk_results = pd.DataFrame(np.nan, index=["break"], columns=_df_main.columns.tolist())
    brk_results["Datatype"] = "RESULTS"

    # --------------------------------------------------------------------------
    # -- Build the final df in the right order
    variantsData_df = pd.concat([brk_env, env_results_df2, brk_sys, sys_df4, brk_results, key_results_df])
    variantsData_df2 = variantsData_df.fillna("")

    # --------------------------------------------------------------------------
    # Export to csv
    return ("variant_inputs", variantsData_df2.to_csv(index=False))
