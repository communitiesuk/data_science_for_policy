''' Importing packages & fixing pathway '''
# Import pacakges
import numpy as np
import pandas as pd
import os
import sys

# Fix pathway
module_path = os.path.abspath(os.path.join(''))
if module_path not in sys.path:
    sys.path.append(module_path)

''' Define some variables '''
import useful_scripts.functions_import_data as fid
from config import NOMIS_AREAS as NA
filepath = "data/raw_data/"

# File to save
def save(df,
         filename,
         path = filepath):
    df.to_csv(f"{path}{filename}.csv",index=False)



''' Download & Save data '''
# Contributions to the Consumer Prices Index (CPI) by energy intensity
# Source - https://www.ons.gov.uk/economy/inflationandpriceindices/datasets/contributionstotheconsumerpricesindexcpibyenergyintensity
url = "https://www.ons.gov.uk/file?uri=/economy/inflationandpriceindices/datasets/contributionstotheconsumerpricesindexcpibyenergyintensity/contributionstotheconsumerpricesindexcpibyenergyintensity/cddataset.xlsx"
# Error 403: Forbidden - so need to manually download and put in raw_data
# Filename = cddataset.xlsx


# Average number of trips by purpose and main mode
# Source - https://www.gov.uk/government/statistical-data-sets/tsgb01-modal-comparisons#mode-share
url = "https://assets.publishing.service.gov.uk/government/uploads/system/uploads/attachment_data/file/821479/nts0409.ods"
df = pd.read_excel(
    url,
    engine="odf",
    sheet_name="NTS0409a_trips",
    skiprows=5
)
filename="average_trips_by_type"
df.to_csv(f"{filepath}{filename}.csv",index=False)


# Homeworking vs hybrid working per income band
url = "https://www.ons.gov.uk/visualisations/dvc2169/fig3/datadownload.xlsx"
# Error 403: Forbidden - so need to manually download and put in raw_data
# Filename = working_from_home_by_income.xlsx


# 2021 (Census) Travel to work
# Dataset - PP013
df = fid.NOMIS(
    file = "NM_2363_1",
    date = "latest",
    geog = NA.PARISH_22,
    c2021_ttwmeth_13 = "0...12",
    measure = 20100
)
filename="travel_to_work_2021"
df.to_csv(f"{filepath}{filename}.csv",index=False)


# Consumer price inflation tables
# Source - https://www.ons.gov.uk/economy/inflationandpriceindices/datasets/consumerpriceinflation
# Error 403: Forbidden - so need to manually download and put in raw_data
# Filename = consumerpriceinflationdetailedreferencetables.xlsx


# Wholesale market indicators
# Source - https://www.ofgem.gov.uk/energy-data-and-research/data-portal/wholesale-market-indicators
# Error 403: Forbidden - so need to manually download and put in raw_data
# File 1 - electricity-prices-day-a.csv
# File 2 - gas-prices-day-ahead-con.csv




''' Downloading lookup files '''
# Parish to Local Authority 2020
df = fid.geoportal_json(
    file = "PAR20_WD20_LAD20_EW_LU_v2_2bc58c34b63f4607b1a73eb61ce5f058",
    f = "geojson"
)
save(
    df,
    "parish_to_la_20",
    "data/lookups/"
)

