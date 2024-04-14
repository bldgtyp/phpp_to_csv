# -*- coding: utf-8 -*-
# -*- Python Version: 3.11 -*-

"""Export CO2e Data CSV files from the PHPP Main DataFrame"""

import pandas as pd
from backend.read_phpp.load_phpp_data import PHPPData


def get_kg_co2_emissions_as_df(_df_main: pd.DataFrame) -> pd.DataFrame:
    """Return the building's CO2e emissions (kgCO2) consumption data in a DataFrame
                            Datatype	            Units	Code Minimum	As-Drawn	Improve Windows	Improve ERV	Improve Insulation
    Datatype
    Heating	                Heating	                kWh	18894.013298	11304.857062	7352.375323	6497.584214	3725.545278
    Cooling	                Cooling	                kWh	413.618352	454.330187	807.137649	608.668385	690.842606
    DHW	                    DHW	                    kWh	3114.843722	3059.251984	2986.819659	2974.217884	2941.724216
    Dishwashing	            Dishwashing	            kWh	178.75	178.75	178.75	178.75	178.75
    Clothes Washing	        Clothes Washing	        kWh	47.025	47.025	47.025	47.025	47.025
    Clothes Drying	        Clothes Drying	        kWh	972.5625	972.5625	972.5625	972.5625	972.5625
    Refrigerator	        Refrigerator	        kWh	445.3	445.3	445.3	445.3	445.3
    Cooking	                Cooking	                kWh	625	625	625	625	625
    PHI Lighting	        PHI Lighting	        kWh	0	0	0	0	0
    PHI Consumer Elec.	    PHI Consumer Elec.	    kWh	0	0	0	0	0
    PHI Small Appliances	PHI Small Appliances	kWh	0	0	0	0	0
    Phius Int. Lighting	    Phius Int. Lighting	    kWh	6991.1	6991.1	6991.1	6991.1	6991.1
    Phius Ext. Lighting	    Phius Ext. Lighting	    kWh	2417.5	2417.5	2417.5	2417.5	2417.5
    Phius MEL	            Phius MEL	            kWh	130.8	130.8	130.8	130.8	130.8
    Aux Elec	            Aux Elec	            kWh	0	0	0	0	0
    Solar PV                Solar PV                kWh 0   0   0   0   0
    """
    df1 = _df_main.loc[468:483]
    df2 = df1.dropna(axis=0, how="all")
    df3 = df2.set_index("Datatype", drop=False)

    return df3


def create_csv_CO2E(phpp_data: PHPPData, co2e_limit_tons_yr: float) -> tuple[str, str]:

    # -- Get the Data
    df_site_energy = get_kg_co2_emissions_as_df(phpp_data.df_main)

    # -- Try and delete tow "Solar PV" from the DataFrame
    try:
        df_site_energy.drop("Solar PV", inplace=True)
    except KeyError:
        pass

    # -- Convert from kg/CO2-->tons/CO2 by multiplying everything by 0.001
    for variant_name in phpp_data.variant_names:
        df_site_energy[variant_name] = df_site_energy[variant_name] * 0.001

    # -- Export to csv
    return ("energy_TonsCO2", df_site_energy.to_csv(index=False))
