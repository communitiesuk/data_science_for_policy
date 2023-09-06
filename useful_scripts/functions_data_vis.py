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
colours = mpl.colormaps["tab10"].colors



''' Define Functions '''
# Create map
def create_map(data,
               map,
               title,
               filename,
               text_inc = True,
               text_size = 3,
               dpi = 1000):
                
    # Merge map data to visual data
    data = data.merge(map,on="code",how="left")
    data = gpd.GeoDataFrame(data, crs='epsg:27700', geometry='geometry')
    fm.dimensions(data)

    # Create figure
    f, ax = plt.subplots(1, figsize=(6,18))

    # Plot Local Authorities greyed out
    map.plot(color='grey', ax=ax)

    # Plot LA data
    data_vis = data.plot(column='value', 
                         cmap=census_cmap, legend_kwds={'loc': "upper left"}, 
                         linewidth=0.2, edgecolor='white', legend=True, ax=ax,scheme="quantiles")

    # Add Labelling
    if text_inc:
        text = map.apply(lambda x: ax.annotate(text=x['name'], 
                                    xy=x.geometry.centroid.coords[0], 
                                    ha='center', clip_on=True, size = text_size,
                                    color='white', fontweight='bold'), axis=1)
    
    ## Format the legend using the custom add_legend() function
    lgd = data_vis.get_legend()
    fm.add_legend(lgd, ax, title="School Absence (%)",text_size=9)

    # Remove axis
    ax.axis('off')

    # Add title & save
    ax.set_title(title, fontweight='bold')
    plt.savefig(f"output/visualisations/{filename}.png",format="png",bbox_inches="tight",dpi=dpi)

# Create line chart
def line_chart(data,
               title,
               filename,
               col = "date",
               var = "variable",
               val = "value",
               colours = colours):
    f, ax = plt.subplots(1, figsize=(6,3))

    names = data[var].unique().tolist()
    colours = colours[0:len(names)]
    chart_input = zip(names,colours)
    for la,colour in chart_input:
        df_filtered = data[data[var] == la].rename(columns={"value":var})
        df_filtered.plot(x="date",y=la,rot=0,linewidth=2,ax=ax,color=colour)

    handles, labels = ax.get_legend_handles_labels()
    leg = data[var].unique().tolist()
    ax.legend(handles[::-1],leg,loc='center',bbox_to_anchor=(0.5,-0.35), ncol=3, frameon=False)

    vals = ax.get_yticks()
    ax.set_yticks(vals)
    ax.set_yticklabels(["{:,.1f}%".format(x) for x in vals])

    ax.set(xlabel=None)

    ax.set_title(title, fontweight='bold')
    plt.savefig(f"output/visualisations/{filename}.png",format="png",bbox_inches="tight",dpi=1000)


