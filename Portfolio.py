import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import warnings
import re
import time

from pandas import DataFrame

def Portfolio():
    warnings.filterwarnings("ignore")
    
    players_and_prices = pd.read_csv('Players_and_Prices.csv')
    players_and_prices.drop("Unnamed: 0", axis=1, inplace=True)
    port_players = pd.read_csv('Portfolio_Players.csv')
    port_players.drop("Unnamed: 0", axis=1, inplace=True)
    port_data = pd.read_csv('Portfolio_Data.csv')
    port_data.drop("Unnamed: 0", axis=1, inplace=True)

    # Bank variables
    players_owned = (len(port_players)-1)
    bank_balance = port_data.loc[0][1]

    # Net worth
    net_worth = 0
    for j in range(1,len(port_players)):                                                            # for j in range of players in portfolio
        p_name = port_players.iloc[j][0]                                                            # set player name
        for m in range(len(players_and_prices)):                                                    # for m in all players
            if p_name == players_and_prices.iloc[m][0]:                                             # find player in database
                value = (float(players_and_prices.iloc[m][2]) * int(port_players.iloc[j][8]))       # value = price * quantity
                net_worth += value                                                                  # add value to net_worth

    # SET PLAYERS CURRENT PRICE          
    net_worth_2 = net_worth + bank_balance

    for q in range(1,len(port_players)):
        name = port_players.loc[q][0]
        for r in range(len(players_and_prices)):
            if name == players_and_prices.loc[r][0]:
                port_players.loc[q][2] = players_and_prices.loc[r][2]
                port_players.loc[q][3] = players_and_prices.loc[r][3]
                break

    function = input("Would you like to view portfolio, view bank, buy player or sell player?\nEnter 'View', 'Buy' or 'Sell'\n\n")

    if function == 'View' or function == 'view':
        if len(port_players) == 1:
            print("\nSorry, Your Portfolio is Empty\n")
            print("Bank Balance: $", round(bank_balance, 2))
            print("Net Worth: $", round(net_worth, 2))
        else:
            print("\nPlayers Owned: ", players_owned)
            print("Bank Balance: $", round(bank_balance, 2))
            print("Portfolio Value: $", round(net_worth, 2))
            print("")
            print("Net Worth: $", round(net_worth_2, 2))

            final_portfolio = port_players
            # final_portfolio = port_players.drop(['Sell'], axis=1)
            # final_portfolio = final_portfolio.drop(['Price'], axis=1)
            # final_portfolio.columns = ['Name','Purchase Price','Last Rd %', 'L5 %','L10 %','Valuation','Quantity']
            final_portfolio.columns = ['Name','Purchase Price','Current Price','Current Sell','Last Rd %', 'L5 %','L10 %','Valuation','Quantity']
            return final_portfolio
    
    elif function == 'Buy' or function == 'buy':
        port_players = port_players.values.tolist()
        First_Last = input("\nEnter Player Name\nSeperate Names by Space, Case Sensitive\ne.g 'Jack_Steele, Reilly_OBrien, Jordan_de Goey'\n\n")
        
        Player_in = False
            
        for i in range(len(players_and_prices)):
            if First_Last == players_and_prices.loc[i][0]:
                Player_in = True
                index = i
                break

        if Player_in == False:
            return "Player Not Found"

        try:
            quantity = int(input("\nHow many units would you like to purchase?\n\n"))
        except:
            print("\nError: Integer not entered\n")

        purchase_value = quantity*players_and_prices.loc[i][1]
        net_value = quantity*players_and_prices.loc[i][2]

        if purchase_value > bank_balance:
            return "You do not have sufficient funds for this purchase"
        
        confirmation = input("\nAre you sure you would like to make this purchase?\n\n")

        if confirmation == 'Yes' or confirmation == 'yes':
            port_data = port_data.values.tolist()
            
            bank_balance -= purchase_value
            port_data[0][1] = bank_balance
            port_data[0][2] = round(net_worth, 2)
            
            bracket = (list(players_and_prices.loc[i]))
            bracket.append(quantity)
            port_players.append(bracket)
            edited_shortlist = pd.DataFrame.from_records(port_players)
            edited_shortlist.columns = ['Name','Buy','Price','Sell','Last Rd %','L5 %', 'L10 %', 'Valuation', 'Quantity']
            port_data[0][0] = (len(port_players)-1)
            
            new_port_data = pd.DataFrame.from_records(port_data)
            new_port_data.to_csv('Portfolio_Data.csv')
            edited_shortlist.to_csv('Portfolio_Players.csv')
                                        
            return "Player added to Portfolio"
        elif confirmation == 'No' or confirmation == 'no':
            return "Purchase cancelled"
        else:
            return "Error: Invalid entry"
        
    elif function == 'Sell' or function == 'sell':
        port_players = port_players.values.tolist()
        port_data = port_data.values.tolist()

        if len(port_players) == 1:
            return "Portfolio is empty"
        
        First_Last = input("Enter Player Name\nSeperate Names by Space, Case Sensitive\ne.g 'Jack_Steele, Reilly_OBrien, Jordan_de Goey'\n\n")

        Player_in = False

        for i in range(1, len(port_players)):
            if First_Last == port_players[i][0]:
                Player_in = True
                index_port = i
                break
        if Player_in == False:
            return "Player Not Found in Portfolio"

        confirmation = input("\nAre you sure you would like to make this sale?\n\n")
        if confirmation == 'No' or confirmation == 'no':
            return "Sale cancelled"
        if confirmation != 'No' and confirmation != 'no' and confirmation != 'Yes' and confirmation != 'yes':
            return "Error: Invalid entry"
    
        quantity = port_players[i][8]

        for w in range(len(players_and_prices)):
            if First_Last == players_and_prices.loc[w][0]:
                break

        sale_value = int(quantity)*float(players_and_prices.iloc[w][3])
            
        port_players.remove(port_players[i])
        bank_balance = port_data[0][1]
        bank_balance += sale_value
        port_data[0][1] = bank_balance
            
        edited_portfolio = pd.DataFrame.from_records(port_players)
        edited_portfolio.columns = ['Name','Buy','Price','Sell','Last Rd %','L5 %', 'L10 %', 'Valuation', 'Quantity']
        edited_portfolio.to_csv('Portfolio_Players.csv')

        new_port_data = pd.DataFrame.from_records(port_data)
        new_port_data.to_csv('Portfolio_Data.csv')
        return "Player removed from Portfolio"
        
    else:
        return "Invalid command"
