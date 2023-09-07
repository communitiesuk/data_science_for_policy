''' Importing packages & fixing pathway '''
# Import pacakges
import numpy as np
import pandas as pd
import os
import sys
import geopandas as gpd
import matplotlib as mpl
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap

# Fix pathway
module_path = os.path.abspath(os.path.join(''))
if module_path not in sys.path:
    sys.path.append(module_path)


''' Define some variables '''
import useful_scripts.functions_maps as fm
ons_colours = ["#cde594", "#80c6a3", "#1f9eb7", "#186290", "#080c54"]
census_cmap = LinearSegmentedColormap.from_list('census_cmap', ons_colours, N=5) 
colours = mpl.colormaps["tab10"]



''' Define functions '''
# 
def col_to_perc(data,
                denominator,
                col = "variable",
                val = "value",
                keep_col=True,
                compliment=False):
    # Create a column of denominators and numerators
    data = data.merge(data[data[col] == denominator],on=[c for c in data.columns.tolist() if c not in [col,val]])
    data.rename(inplace=True,columns={col+"_x":"numerator",
                                            val+"_x":"numerator_val",
                                            col+"_y":"denominator",
                                            val+"_y":"denominator_val"})

    # Calculate percentage (note if we want the compliment of the percentage or not)
    if compliment:
        data[val] = 1 - (data["numerator_val"] / data["denominator_val"])
    else:
        data[val] = data["numerator_val"] / data["denominator_val"]

    # Drop denominator column and filter out the denominator variable
    data = data[data["numerator"] != denominator]
    data.drop(inplace=True,columns=["numerator_val","denominator","denominator_val"])
    data.rename(inplace=True,columns={"numerator":col})

    # If the column of interest only has 2 variables, then we might want to drop the column
    if keep_col == False:
        data.drop(inplace=True,columns=col)
    
    # Output datafile
    return data
