import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import warnings
import re
import time

from urllib.request import urlopen
from bs4 import BeautifulSoup
from pandas import DataFrame

def Very_Underpriced():
    players_and_prices = pd.read_csv('Players_and_Prices.csv')
    players_and_prices.drop("Unnamed: 0", axis=1, inplace=True)

    value_buys_no_table = []
    
    for i in range(len(players_and_prices)-1):
        if players_and_prices['Valuation'][i] == 'Very Underpriced' and players_and_prices['Price'][i] > 4:
            value_buys_no_table.append(list(players_and_prices.loc[i]))
    value_buys = pd.DataFrame.from_records(value_buys_no_table)
    value_buys.columns = ['Name','Buy','Price','Sell','Prev. Change %','L5 %', 'L10 %', "Valuation"]
    value_buys = value_buys.sort_values(by='Price', ascending=False)

    return value_buys

def Underpriced():
    players_and_prices = pd.read_csv('Players_and_Prices.csv')
    players_and_prices.drop("Unnamed: 0", axis=1, inplace=True)

    value_buys_no_table = []
    
    for i in range(len(players_and_prices)-1):
        if players_and_prices['Valuation'][i] == 'Underpriced' and players_and_prices['Price'][i] > 4:
            value_buys_no_table.append(list(players_and_prices.loc[i]))
    value_buys = pd.DataFrame.from_records(value_buys_no_table)
    value_buys.columns = ['Name','Buy','Price','Sell','Prev. Change %','L5 %', 'L10 %', "Valuation"]
    value_buys = value_buys.sort_values(by='Price', ascending=False)

    return value_buys

def Unknowns():
    players_and_prices = pd.read_csv('Players_and_Prices.csv')
    players_and_prices.drop("Unnamed: 0", axis=1, inplace=True)

    value_buys_no_table = []
    
    for i in range(len(players_and_prices)-1):
        if players_and_prices['Valuation'][i] == 'Inconclusive' and players_and_prices['Price'][i] > 6:
            value_buys_no_table.append(list(players_and_prices.loc[i]))
    value_buys = pd.DataFrame.from_records(value_buys_no_table)
    value_buys.columns = ['Name','Buy','Price','Sell','Prev. Change %','L5 %', 'L10 %', "Valuation"]
    value_buys = value_buys.sort_values(by='Price', ascending=False)

    return value_buys
