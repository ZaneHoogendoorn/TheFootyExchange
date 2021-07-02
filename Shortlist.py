import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import warnings
import re
import time

from pandas import DataFrame

def Shortlist():
    players_and_prices = pd.read_csv('Players_and_Prices.csv')
    players_and_prices.drop("Unnamed: 0", axis=1, inplace=True)
    shortlist = pd.read_csv('Shortlist.csv')
    shortlist.drop("Unnamed: 0", axis=1, inplace=True)

    for q in range(len(shortlist)):
        name = shortlist.loc[0][0]
        for r in range(len(players_and_prices)):
            if name == players_and_prices.loc[0][0]:
                shortlist.loc[q] = players_and_prices.loc[r]
                break

    function = input("Would you like to view shortlist, add player or remove player?\nEnter 'View', 'Add' or 'Remove'\n\n: ")

    if function == 'View' or function == 'view':
        shortlist.columns = ['Name','Buy','Price','Sell','Last Rd %','L5 %', 'L10 %', "Valuation"]
        if len(shortlist) == 1:
            return "Shortlist empty"
        else:
            return shortlist
    
    elif function == 'Add' or function == 'add':
        shortlist = shortlist.values.tolist()
        First_Last = input("Enter Player Name\nSeperate Names by Space, Case Sensitive\ne.g 'Jack_Steele, Reilly_OBrien, Jordan_de Goey'\n\n: ")
        
        Player_in = False
            
        for i in range(len(players_and_prices)):
            if First_Last == players_and_prices.loc[i][0]:
                Player_in = True
                index = i
                break

        if Player_in == False:
            return "Player Not Found"
        else:
            shortlist.append(list(players_and_prices.loc[i]))
            edited_shortlist = pd.DataFrame.from_records(shortlist)
            edited_shortlist.columns = ['Name','Buy','Price','Sell','Last Rd %','L5 %', 'L10 %', "Valuation"]
            edited_shortlist.to_csv('Shortlist.csv')
            return "Player added to Shortlist"
        
    elif function == 'Remove' or function == 'remove':
        shortlist = shortlist.values.tolist()

        if len(shortlist) == 1:
            return "Shortlist is empty"
        
        First_Last = input("Enter Player Name\nSeperate Names by Space, Case Sensitive\ne.g 'Jack_Steele, Reilly_OBrien, Jordan_de Goey'\n\n: ")
        
        Player_in = False
            
        for i in range(1,len(players_and_prices)):
            if First_Last == shortlist[i][0]:
                Player_in = True
                index = i
                break
        if Player_in == False:
            return "Player Not Found"
        else:
            shortlist.remove(list(shortlist[i]))
            edited_shortlist = pd.DataFrame.from_records(shortlist)
            edited_shortlist.columns = ['Name','Buy','Price','Sell','Last Rd %','L5 %', 'L10 %', "Valuation"]
            edited_shortlist.to_csv('Shortlist.csv')
            return "Player removed from Shortlist"
        
    else:
        return "Invalid command"
