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
import useful_scripts.functions_data_manipulation as fdm
filepath = "data/"

# File to save
def save(df,
         filename,
         path = filepath):
    df.to_csv(f"{path}{filename}.csv",index=False)




''' Commuting '''
# Transport mapping:
transport_mapping = {
    "Walk":"Walk",
    'Pedal cycle':"Bicycle",
    'Motorcycle':"Bicycle",
    'Car or van driver':"Car",
    'Car or van passenger':"Car",
    'Bus in London':"Bus",
    'Other local bus':"Bus",
    'Non-local bus':"Bus",
    'London Underground':"Rail",
    'Surface Rail':"Rail",
    'Taxi or minicab':"Other",
    'Other public transport':"Other",
    'Other private transport':"Other"
}
# Commuting type
df = pd.read_csv("data/raw_data/average_trips_by_type.csv")
df = df[["Year","Main mode","Commuting"]]
df.columns = ["year","variable","value"]
df.variable = [x.split("[")[0].strip() for x in df.variable]
df.variable = [transport_mapping.get(x,x) for x in df.variable]
df = df.groupby(["year","variable"]).value.sum().reset_index()
df = fdm.col_to_perc(df,"All modes")
filename="transport_type_commuting"
df.to_csv(f"{filepath}{filename}.csv",index=False)

# Overall travel type
df = pd.read_csv("data/raw_data/average_trips_by_type.csv")
df = df[["Year","Main mode","All purposes"]]
df.columns = ["year","variable","value"]
df.variable = [x.split("[")[0].strip() for x in df.variable]
df.variable = [transport_mapping.get(x,x) for x in df.variable]
df = df.groupby(["year","variable"]).value.sum().reset_index()
df = fdm.col_to_perc(df,"All modes")
filename="transport_type_all"
df.to_csv(f"{filepath}{filename}.csv",index=False)



''' Working from home '''
# Working from home by income
df = pd.read_excel("data/raw_data/working_from_home_by_income.xlsx",skiprows=6)
df.rename(inplace=True, columns={"Unnamed: 0":"type"})
df = pd.melt(df,id_vars=["type"],value_vars=df.columns.tolist()[1:])
df.variable = [x[:-1] for x in df.variable]
inomce_mapping = { 
    '£10,000 up to £15,000':'£10,000 - £15,000', 
    '£15,000 up to £20,000':'£15,000 - £20,000',
    '£20,000 up to £30,000':'£20,000 - £30,000', 
    '£30,000 up to £40,000':'£30,000 - £40,000',
    '£40,000 up to £50,000':'£40,000 - £50,000',
    '£50,000 or more':'£50,000+'
}
df.variable = [inomce_mapping.get(x,x) for x in df.variable]
filename="working_from_home_by_income"
df.to_csv(f"{filepath}{filename}.csv",index=False)

# Travel to work - Census data
df = pd.read_csv("data/raw_data/TS061-2021-1.csv")
df.drop(inplace=True,columns="Method used to travel to workplace (12 categories) Code")
df.columns = ["code","name","variable","value"]
df = df[df.variable != "Not in employment or aged 15 years and under"].reset_index(drop=True)
transport_mapping = {
    'Other method of travel to work':"Other modes", 
    'Bicycle':"Bicycle", 
    'Motorcycle, scooter or moped':"Bicycle", 
    'Bus, minibus or coach':"Bus / coach", 
    'Taxi':"Bus / coach", 
    'Driving a car or van':"Car", 
    'Work mainly at or from home':"Work from home", 
    'On foot':"On foot", 
    'Passenger in a car or van':"Car", 
    'Train':"All rail", 
    'Underground, metro, light rail, tram':"All rail"
}
df.variable = [transport_mapping.get(x,np.nan) for x in df.variable]
df = df.groupby(["code","name","variable"]).value.sum().reset_index()
df = pd.concat([df,df.groupby(["code","name"]).value.sum().reset_index()]).fillna("total")
df = fdm.col_to_perc(df,"total")
save(df, "travel_to_work_la")



''' CPI '''
# CPI: Detailed goods and service breakdown
# Last 12 months
df = pd.read_excel(
    "data/raw_data/consumerpriceinflationdetailedreferencetables.xlsx",
    sheet_name="Table 28",
    skiprows=5
)
cols = []
for i in range(df.shape[1]-4):
    cols = cols + [df.iloc[0,4+i] + " " + str(df.columns[4+i]).split(".")[0]]
df.columns = df.columns.tolist()[0:4] + cols
df = df.iloc[1:,:]
df = df[df["Jul 2022"].notnull()]
df = df.drop(columns=["Unnamed: 0","Unnamed: 1",2022]).rename(columns={"Unnamed: 2":"CPI_type"})
df = pd.melt(df,id_vars="CPI_type",value_vars=df.columns.tolist()[1:])
df["variable"] = pd.to_datetime(df["variable"],format="%b %Y")
df.value = df.value.astype(float)
df.CPI_type = df.CPI_type.str.strip()
save(df, "CPI_type_last_12_months")
# Last 14 years
df = pd.read_excel(
    "data/raw_data/consumerpriceinflationdetailedreferencetables.xlsx",
    sheet_name="Table 30 ",
    skiprows=4
)
df = df[df[2008].notnull()]
df = df.drop(columns=["Unnamed: 0","Unnamed: 1"]).rename(columns={"Unnamed: 2":"CPI_type"})
df = pd.melt(df,id_vars="CPI_type",value_vars=df.columns.tolist()[1:])
df["variable"] = pd.to_datetime(df["variable"],format="%Y")
df.value = [np.nan if ["-"," -"].count(x)>0 else float(x) for x in df.value]
df.CPI_type = df.CPI_type.str.strip()
save(df, "CPI_type_last_14_years")



''' Gas prices '''
# Gas prices by month
df = pd.read_csv("data/raw_data/gas-prices-day-ahead-con.csv")
df.columns = ["date","value"]
df["date"] = pd.to_datetime(df["date"])
save(df, "gas_prices")

