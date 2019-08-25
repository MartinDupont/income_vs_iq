# -*- coding: utf-8 -*-
"""
Created on Sat Aug 24 21:15:47 2019

@author: martin
"""
import pandas as pd

def age_correction(age):
    """
    The AFQT is an intelligence test facilitated by the military.
    The participants take the test at different ages,
    some of them as young as 16, which influences their score.
    Applied the same correction as: http://www.jsmp.dk/files/nlsy_data.html
    """
    if (age >= 20):
        return 13700
    elif age == 19:
        return 10500
    elif age == 18:
        return 9200
    elif age == 17:
        return 8000
    else:
        return 5200


def read_in_and_clean(path, min_income):
    data  = pd.read_csv(path)


    column_names = {"R0000500" : "birthyear", 
                    "R0618301" : "afqt",     
                    "R6365001" : "business98",
                    "R6364601" : "wage98",
                    "R6911101" : "business00",
                    "R6909701" : "wage00",
                    "R7609000" : "business02",
                    "R7607800" : "wage02",
                    "R8318200" : "business04",
                    "R8316300" : "wage04",
                    "T0913900" : "business06",
                    "T0912400" : "wage06",
                    "T2078800" : "business08",
                    "T2076700" : "wage08",
                    "T3047500" : "business10",
                    "T3045300" : "wage10",
                    "T3979400" : "business12",
                    "T3977400" : "wage12",
                    "T4917800" : "business14",
                    "T4915800" : "wage14" }
    
    
    data = data.rename(columns = column_names)
    
    data = data[[c for c in column_names.values()]]
    
    # Data is full of erroneous negative values, probably specifying missing
    data[data < 0] = 0
    
    
    years = ["98", "00", "02", "04", "06", "08", "10", "12", "14"]
    income_cols = ["income" + year for year in years]
    
    # correct for inflation relative to 2014
    inflation = {
              "98": 28.52 / 19.64,
              "00":  28.52 / 20.75,
              "02": 28.52 / 21.67,
              "04": 28.52 / 22.76,
              "06": 28.52 / 24.29,
              "08": 28.52 / 25.94,
              "10": 28.52 / 26.27,
              "12": 28.52 / 27.66,
              "14": 1
              }
    
    
    for year in years:
        data["income" + year] = (data["business" + year] + data["wage" + year]) * inflation[year]

    data["age_at_test"] = 80 - data["birthyear"]
        
    # Apply age correction 
    temp = data["afqt"] - data["afqt"].apply(age_correction)
    
    # Normalize scores
    data["iq"] = ((temp-temp.mean())/temp.std())
    
    # Income averaged over multiple years.
    data["income"] = data[income_cols].sum(axis=1) / len(income_cols)
    
    data = data[["iq", "income"]]
    
    # data = data[data["income"] >  MIN_INCOME]
    data.loc[data['income'] < min_income, 'income'] = min_income
    
    return data["iq"].values, data["income"].values