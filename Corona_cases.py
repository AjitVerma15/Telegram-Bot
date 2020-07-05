

# importing libraries 

import requests 
from bs4 import BeautifulSoup
from tabulate import tabulate 
import os 
import pandas as pd


url = "https://www.mohfw.gov.in/"

def get_cases():
    response = requests.get(url)
    response = response.content
    information = BeautifulSoup(response,"html5lib")
    tables = information.find_all('table',{'class':"table table-striped"})
    tables = tables[0]
    heading = tables.find_all('th')
    title = [ct.text for ct in heading]
    row_data = tables.find_all('tr')[1:]
    row_data = row_data[:-4]


    tables_row = []
    #tables_row.append(title)
    for row in row_data:
        current_row = []
        data = row.find_all('td')
        for d in data:
            current_row.append(d.text)
        tables_row.append(current_row)

    remove = tables_row[36]
    removes = []
    for r in remove:
        if '\n' in r:
            r = r[2:-2]
        removes.append(r)
        
    tables_row = tables_row[:-2]
    tables_row.append(removes)

    dp = pd.DataFrame(tables_row,columns=title,dtype=int)

   

    dp = dp.drop("S. No.",axis=1)
    
    dp = dp.sort_values("Total Confirmed cases*",ascending=False)
    dp = dp.rename(columns = {"Active Cases*":"Active Cases","Deaths**":"Deaths","Total Confirmed cases*":"Total Confirmed cases","Cured/Discharged/Migrated*":"Cured/Discharged/Migrated"})
    dp = dp.replace({"Total#":"Total"})
    #dp = dp.set_index("Name of State / UT")
    dp = dp.sort_values("Total Confirmed cases",ascending=False)
    Total = dp.values.tolist()
    Total = Total[:7]

    Title = ['Name of State / UT','Active Cases','Cured/Discharged/Migrated','Deaths','Total Confirmed cases']

    
    Data = dp.loc[dp["Name of State / UT"]=="Total"]
    Active_Case = Data["Active Cases"].values[0]
    Total_Case = Data["Total Confirmed cases"].values[0]
    Death = Data["Deaths"].values[0]
    Recovered = Data["Cured/Discharged/Migrated"].values[0]
    return Total_Case,Active_Case,Death,Recovered



