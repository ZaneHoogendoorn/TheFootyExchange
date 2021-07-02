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

def Last_Round_Risers():
    players_and_prices = pd.read_csv('Players_and_Prices.csv')
    players_and_prices.drop("Unnamed: 0", axis=1, inplace=True)
    
    risers = players_and_prices.sort_values(by='Last Rd %', ascending=False)
    return risers[:40]

def Last_Round_Fallers():
    players_and_prices = pd.read_csv('Players_and_Prices.csv')
    players_and_prices.drop("Unnamed: 0", axis=1, inplace=True)
    
    fallers = players_and_prices.sort_values(by='Last Rd %', ascending=True)
    return fallers[:40]

def Last_5_Risers():
    players_and_prices = pd.read_csv('Players_and_Prices.csv')
    players_and_prices.drop("Unnamed: 0", axis=1, inplace=True)
    
    risers = players_and_prices.sort_values(by='L5 %', ascending=False)
    return risers[:40]

def Last_5_Fallers():
    players_and_prices = pd.read_csv('Players_and_Prices.csv')
    players_and_prices.drop("Unnamed: 0", axis=1, inplace=True)
    
    fallers = players_and_prices.sort_values(by='L5 %', ascending=True)
    return fallers[:40]

def Last_10_Risers():
    players_and_prices = pd.read_csv('Players_and_Prices.csv')
    players_and_prices.drop("Unnamed: 0", axis=1, inplace=True)
    
    risers = players_and_prices.sort_values(by='L10 %', ascending=False)
    return risers[:40]

def Last_10_Fallers():
    players_and_prices = pd.read_csv('Players_and_Prices.csv')
    players_and_prices.drop("Unnamed: 0", axis=1, inplace=True)
    
    fallers = players_and_prices.sort_values(by='L10 %', ascending=True)
    return fallers[:40]
