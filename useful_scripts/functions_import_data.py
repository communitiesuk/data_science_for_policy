''' Importing packages & fixing pathway '''
# Import pacakges
import numpy as np
import pandas as pd
import os
import sys
import requests

# Fix pathway
module_path = os.path.abspath(os.path.join(''))
if module_path not in sys.path:
    sys.path.append(module_path)



''' Define some variables '''
# Config
from config import USER_DETAILS as UD

#
import useful_scripts.functions_data_manipulation as fdm
filepath = "data/"



''' Define Functinos '''
# Download data from NOMIS
def NOMIS(file,
          date,
          geog,
          measure,
          id=UD.NOMIS_API,
          **kwargs):
    # Create url
    url = f"https://www.nomisweb.co.uk/api/v01/dataset/{file}.data.csv?date={date}"
    url = url + f"&geography={geog}"
    for key, value in kwargs.items():
        val = value if isinstance(value,str) else str(value)
        url = url + f"&{key}={val}"
    url = url + f"&measures={measure}&uid={id}"

    # Download data
    data = pd.read_csv(url)

    # Output
    return data

# Geoportal download
def geoportal_json(file,
                   outFields="*",
                   where="1%3D1",
                   f="json",
                   resultType="standard",
                   **kwargs):
    # Create API url
    url = f"https://services1.arcgis.com/ESMARspQHYMw9BZ9/arcgis/rest/services/"
    url = url + file + "/FeatureServer/0/query?"
    url = url + f"outFields={outFields}&where={where}&f={f}&resultType={resultType}"
    for key, value in kwargs.items():
        val = value if isinstance(value,str) else str(value)
        url = url + f"&{key}={val}"
        
    # Download the data
    r = requests.get(url)

    # Convert from JSON to DataFrame
    df = pd.DataFrame()
    for row in r.json()["features"]:
        df = pd.concat([df,pd.DataFrame.from_dict(row["attributes"], orient='index').transpose()])

    # Output
    return df.reset_index(drop=True)

