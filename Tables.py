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
def Display_Players_and_Prices():
    players_and_prices = pd.read_csv('Players_and_Prices.csv')
    players_and_prices.drop("Unnamed: 0", axis=1, inplace=True)
    return players_and_prices

def Display_Names_and_Link():
    Names_and_Link = pd.read_csv('Names_and_Link.csv')
    Names_and_Link.drop("Unnamed: 0", axis=1, inplace=True)
    return Names_and_Link

def Display_Market():
    Market_Value = pd.read_csv('Market_Value.csv')
    Market_Value.drop("Unnamed: 0", axis=1, inplace=True)
    r1 = 0
    r2 = 0
    r3 = 0
    r4 = 0
    r5 = 0
    r6 = 0
    r7 = 0
    r8 = 0
    r9 = 0
    r10 = 0
    r11 = 0
    r12 = 0
    r13 = 0
    r14 = 0
    r15 = 0

    for i in range(len(Market_Value)):
        r1 += float(Market_Value.loc[i][0])
        r2 += float(Market_Value.loc[i][1])
        r3 += float(Market_Value.loc[i][2])
        r4 += float(Market_Value.loc[i][3])
        r5 += float(Market_Value.loc[i][4])
        r6 += float(Market_Value.loc[i][5])
        r7 += float(Market_Value.loc[i][6])
        r8 += float(Market_Value.loc[i][7])
        r9 += float(Market_Value.loc[i][8])
        r10 += float(Market_Value.loc[i][9])
        r11 += float(Market_Value.loc[i][10])
        r12 += float(Market_Value.loc[i][11])
        r13 += float(Market_Value.loc[i][12])
        r14 += float(Market_Value.loc[i][13])
        r15 += float(Market_Value.loc[i][14])

    values = []

    values.append(r1)
    values.append(r2)
    values.append(r3)
    values.append(r4)
    values.append(r5)
    values.append(r6)
    values.append(r7)
    values.append(r8)
    values.append(r9)
    values.append(r10)
    values.append(r11)
    values.append(r12)
    values.append(r13)
    values.append(r14)
    values.append(r15)

    for i in range(len(values)):
        values[i] = round(values[i], 2)

    plt.title('Market Index')
    plt.xlabel('Round')
    plt.ylabel('Index')
    plt.plot(values, label = "Price", color='black')
    plt.grid()
    plt.show()

    print("Current Market Index is: ", values[14])
