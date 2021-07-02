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

# The one where you can enter a player name
def Premiums():
    players_and_prices = pd.read_csv('Players_and_Prices.csv')
    players_and_prices.drop("Unnamed: 0", axis=1, inplace=True)
    
    premos = players_and_prices.sort_values(by='Price', ascending=False)
    return premos[:60]

def Basements():
    players_and_prices = pd.read_csv('Players_and_Prices.csv')
    players_and_prices.drop("Unnamed: 0", axis=1, inplace=True)
    
    basements = players_and_prices.sort_values(by='Price', ascending=True)
    return basements[:60]
