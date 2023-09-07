''' Importing packages & fixing pathway '''
# Import pacakges
import os
import sys
import numpy as np
import pandas as pd
os.environ['USE_PYGEOS'] = '0'
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
import useful_scripts.functions_data_vis as fdv
ons_colours = ["#cde594", "#80c6a3", "#1f9eb7", "#186290", "#080c54"]
census_cmap = LinearSegmentedColormap.from_list('census_cmap', ons_colours, N=5) 
colours = mpl.colormaps["tab10"]
filepath = "data/"



''' Map files '''
# England LA
map_eng_la22 = gpd.read_file("shapefiles\England_ltla_2022\england_ltla_2022.shp")
map_eng_la22 = map_eng_la22.sort_values(by="ltla22cd").drop(columns=["ltla22nmw","name"]).reset_index(drop=True)
map_eng_la22.columns = ["label","code","name","geometry"]
map_eng_la22["name"] = fm.compact_text(map_eng_la22["name"].astype(str),threshold=8)
fm.dimensions(map_eng_la22)

# Welsh LA
map_wal_la22 = gpd.read_file("shapefiles\Wales_ltla_2022\wales_ltla_2022.shp")
map_wal_la22 = map_wal_la22.sort_values(by="ltla22cd").drop(columns=["ltla22nmw","name"]).reset_index(drop=True)
map_wal_la22.columns = ["label","code","name","geometry"]
map_wal_la22["name"] = fm.compact_text(map_wal_la22["name"].astype(str),threshold=8)
fm.dimensions(map_wal_la22)

# England & Wales LA
map_la22 = pd.concat([map_eng_la22,map_wal_la22])



''' Create visuals '''
# Working from home
df = pd.read_csv("data/travel_to_work_la.csv")
df.value = 100 * df.value
df_work_homne = df[df.variable == "Work from home"]
fdv.create_map(
    df_work_homne,
    map_la22,
    "Percentage of employees who work from home in\nEngland & Wales by Local Authority",
    "work_from_home",
    "Work from home (%)",
    text_inc = False
)

# Travel by car
df_car = df[df.variable == "Car"]
fdv.create_map(
    df_car,
    map_la22,
    "Percentage of employees who travel to work by car\nin England & Wales by Local Authority",
    "travel_by_car",
    "Travel by car (%)",
    text_inc = False
)

# Travel by other means
df_green = df[(df.variable != "Car") & (df.variable != "Work from home")]\
             .groupby(["code","name"]).value.sum().reset_index()
fdv.create_map(
    df_green,
    map_la22,
    "Percentage of employees who travel to work other than by\ncar in England & Wales by Local Authority",
    "travel_by_not_car",
    "Travel by non-car (%)",
    text_inc = False
)

# Consumer price inted - 14 years
df = pd.read_csv("data\CPI_type_last_14_years.csv")
df.rename(inplace=True,columns={"variable":"date"})
df = df[df.CPI_type.isin(["CPI (overall index)","Transport services"])].reset_index(drop=True)
df["date"] = pd.to_datetime(df["date"])
df.date = [x.year for x in df.date]
df = df.sort_values(by=["CPI_type","date"]).reset_index(drop=True)
fdv.line_chart(
    df,
    "Annual Consumer Price Index changes",
    "cpi_annual",
    var = "CPI_type",
    data_format = "{:,.0f}%",
    y_title="Percentage change over 12 months"
)

# Consumer price inted - 13 months
df = pd.read_csv("data/CPI_type_last_12_months.csv")
df.rename(inplace=True,columns={"variable":"date"})
df = df[df.CPI_type.isin(["CPI (overall index)","Transport services"])].reset_index(drop=True)
df["date"] = pd.to_datetime(df["date"])
df = df.sort_values(by=["CPI_type","date"]).reset_index(drop=True)
df.date = [x.strftime("%b") + " " + str(x.year)[-2:] for x in df.date]
fdv.line_chart(
    df,
    "Monthly Consumer Price Index changes",
    "cpi_monthly",
    var = "CPI_type",
    data_format = "{:,.0f}%",
    y_title="Percentage change over 12 months"
)

# Gas prices
df = pd.read_csv("data/gas_prices.csv")
df["date"] = pd.to_datetime(df["date"])
f, ax = plt.subplots(1, figsize=(6,3))
df.plot(x="date",y="value",rot=0,linewidth=2,ax=ax)
plt.ylabel("£ / Megawatt-hour (MWh")
ax.set(xlabel=None)
ax.get_legend().remove()
ax.set_title("Gas price trend", fontweight='bold')
plt.savefig(f"output/visualisations/gas_prices.png",format="png",bbox_inches="tight",dpi=1000)

# Travel to work
df = pd.read_csv("data/transport_type_commuting.csv")
df.rename(inplace=True,columns={"year":"date"})
df.value = 100 * df.value
df["date"] = pd.to_datetime(df["date"],format="%Y")
df = df.sort_values(by=["variable","date"]).reset_index(drop=True)
fdv.line_chart(
    df,
    "Method of transport to work",
    "transport_commute",
    data_format = "{:,.0f}%",
    y_title = "Percentage of commuters",
    y_limit = [0,75]
)

# Transport general
df = pd.read_csv("data/transport_type_all.csv")
df.rename(inplace=True,columns={"year":"date"})
df.value = 100 * df.value
df["date"] = pd.to_datetime(df["date"],format="%Y")
df = df.sort_values(by=["variable","date"]).reset_index(drop=True)
fdv.line_chart(
    df,
    "Method of transport",
    "transport_general",
    data_format = "{:,.0f}%",
    y_title = "Percentage of transport users",
    y_limit = [0,70]
)

# Working from home by income
df = pd.read_csv("data/working_from_home_by_income.csv")
df.value = df.value / 100
df_input = df.pivot(index="variable",columns="type",values="value").reset_index()
df_input.columns.name=None
df_input.index = df_input["variable"]
df_input = df_input[df_input.columns.to_list()[1:]]
# Plot
f, ax = plt.subplots(1, figsize=(6,3))
df_input.plot(kind='barh',stacked=True, ax=ax, legend=False, zorder=3,color=ons_colours)
# Fix axis
ax.grid(axis='x',zorder=0)
ax.set_xlabel('Percentage of workers')
ax.set_ylabel('Income')
# Adding labels - only show if % is greater than 4%
i = 0
for c in ax.containers:
    labels = ['{:,.0%}'.format(w) if (w := v.get_width()) > 0.04 else '' for v in c ]
    if i < 2:
        ax.bar_label(c, labels=labels, label_type='center', fontsize=7, color="#186290")
    else:
        ax.bar_label(c, labels=labels, label_type='center', fontsize=7, color="#cde594")
    i += 1
# Edit x-axis
vals = ax.get_xticks()
ax.set_xticks(vals)
ax.set_xticklabels(["{:,.0%}".format(x) for x in vals])
plt.xlim(0,1)
# Set title
ax.set_title("Homeworking by income",weight="bold")
# Set Legend
ax.legend(loc='center',bbox_to_anchor=(0.5,-0.35), ncol=2, frameon=False)
# Remove outer box
plt.box(False)
# Switch the order of the plot to have the LA on top
plt.gca().invert_yaxis()
# Save chart
plt.savefig(f"output/visualisations/homeworking_income.png",format="png",bbox_inches="tight",dpi=1000)
