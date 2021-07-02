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
def Player_Value():
    warnings.filterwarnings("ignore")
    
    First_Last = input("Enter Player Name\nSeperate Names by Space, Case Sensitive\ne.g 'Jack_Steele, Reilly_OBrien, Jordan_de Goey'\n\n: ")

    name_and_link = pd.read_csv('Names_and_Link.csv')
    name_and_link.drop("Unnamed: 0", axis=1, inplace=True)
 
    # Checking name exists in list 'name_and_link'
    player_found = False
    for m in range(len(name_and_link)):
        if First_Last == name_and_link.loc[m][0]:
            link = name_and_link.loc[m][1]
            player_found = True
            break
    if player_found == False:
        return "Player Not Found"
    
    url = "https://afltables.com/afl/stats/" + link
    html = urlopen(url)
    
    soup = BeautifulSoup(html, 'lxml')
    
    title = soup.title
    
    rows = soup.find_all('tr')
    
    for row in rows:
        row_td = row.find_all('td')
        
    str_cells = str(row_td)
    cleantext = BeautifulSoup(str_cells, "lxml").get_text()

    list_rows = []
    for row in rows:
        cells = row.find_all('td')
        str_cells = str(cells)
        clean = re.compile('<.*?>')
        clean2 = (re.sub(clean, '',str_cells))
        list_rows.append(clean2)
        
    df = pd.DataFrame(list_rows)
    
    df1 = df[0].str.split(',', expand=True)
    
    df1[0] = df1[0].str.strip('[')
    
    df6 = df1.dropna(axis=0, how='any')
    
    df6[0] = df6[0].str.strip('↑↓')
    
    df6[27] = df6[27].str.strip(']')
    
    df6.columns = ['GP','Opponent','Rnd','Res','#','K','M','HB','DIS','G','B','HO','TKL','R50','I50','Clear','Clang','FF','FA','BrownV','CP','UP','CM','MI50','1%','BO','GA','TOG%']
    
    df6 = df6.reset_index()
    
    for e in range(len(df6)-1):
        if int(df6['GP'][e]) > 1000:
            df6 = df6.drop(e, axis=0)
        
    df6 = df6.reset_index()
    
    for i in df6.columns:
        df6[i][df6[i].apply(lambda i: True if re.search('^\s*$', str(i)) else False)]=None
    df6.fillna(0, inplace=True)
    
    pd.to_numeric(df6["GP"])
    pd.to_numeric(df6["K"])
    pd.to_numeric(df6["M"])
    pd.to_numeric(df6["HB"])
    pd.to_numeric(df6["G"])
    pd.to_numeric(df6["B"])
    pd.to_numeric(df6["HO"])
    pd.to_numeric(df6["TKL"])
    pd.to_numeric(df6["R50"])
    pd.to_numeric(df6["I50"])
    pd.to_numeric(df6["Clear"])
    pd.to_numeric(df6["Clang"])
    pd.to_numeric(df6["FF"])
    pd.to_numeric(df6["FA"])
    pd.to_numeric(df6["CP"])
    pd.to_numeric(df6["UP"])
    pd.to_numeric(df6["CM"])
    pd.to_numeric(df6["MI50"])
    pd.to_numeric(df6["1%"])
    pd.to_numeric(df6["BO"])
    pd.to_numeric(df6["GA"])
    pd.to_numeric(df6["TOG%"])
    
    df6.columns = ['1','2','GP','Opponent','Rnd','Res','#','K','M','HB','DIS','G','B','HO','TKL','R50','I50','Clear','Clang','FF','FA','BrownV','CP','UP','CM','MI50','1%','BO','GA','TOG%']
    df6.drop('1', axis=1, inplace=True)
    df6.drop('2', axis=1, inplace=True)
    
    for w in range(len(df6)):
        if int(df6["TOG%"][w]) <= 25:
            df6 = df6.drop(w, axis=0)
    df6 = df6.reset_index()
            
    df6.drop('TOG%', axis=1, inplace=True)
    df6.drop('BrownV', axis=1, inplace=True)
    df6.drop('#', axis=1, inplace=True)
    df6.drop('Opponent', axis=1, inplace=True)
    df6.drop('DIS', axis=1, inplace=True)
    df6.drop('index', axis=1, inplace=True)
    
    prices = []
    final_prices = []

    for i in range(0, len(df6)):
        price = 0
        price += int(df6.loc[i, "K"])*0.25
        price += int(df6.loc[i, "M"])*0.1
        price += int(df6.loc[i, "HB"])*0.15
        price += int(df6.loc[i, "G"])*1.25
        price += int(df6.loc[i, "B"])*-0.1
        price += int(df6.loc[i, "HO"])*0.05
        price += int(df6.loc[i, "TKL"])*0.05
        price += int(df6.loc[i, "R50"])*0.05
        price += int(df6.loc[i, "I50"])*0.05
        price += int(df6.loc[i, "Clear"])*0.25
        price += int(df6.loc[i, "Clang"])*-0.05
        price += int(df6.loc[i, "FF"])*0.05
        price += int(df6.loc[i, "FA"])*-0.05
        price += int(df6.loc[i, "CP"])*0.1
        price += int(df6.loc[i, "UP"])*0
        price += int(df6.loc[i, "CM"])*0.2
        price += int(df6.loc[i, "MI50"])*0.15
        price += int(df6.loc[i, "1%"])*0.15
        price += int(df6.loc[i, "BO"])*0.25
        price += int(df6.loc[i, "GA"])*0.05
        prices.append(price)

    for j in range(len(prices)):
        final_prices.append(round(prices[j],2))
        
    plt.title('Price over Career')
    plt.xlabel('Game Number')
    plt.ylabel('Price $')
    plt.plot(final_prices)
    plt.grid()
    plt.show()
    
    # Current Round Price
    base_value = 6
    lenn = len(final_prices)-1

    if len(final_prices)-1 >= 3:     # If he has played 4 or more games
        player_price = (final_prices[lenn]*0.35) + (final_prices[lenn-1]*0.25) + (final_prices[lenn-2]*0.2) + (final_prices[lenn-3]*0.2)
    elif len(final_prices)-1 == 2:   # If he has played 3 games
        player_price = (final_prices[lenn]*0.35) + (final_prices[lenn-1]*0.25) + (final_prices[lenn-2]*0.2) + (base_value*0.2)
    elif len(final_prices)-1 == 1:   # If he has played 2 games
        player_price = (final_prices[lenn]*0.35) + (final_prices[lenn-1]*0.25) + (base_value*0.2) + (base_value*0.2)
    elif len(final_prices)-1 == 0:   # If he has played 1 game
        player_price = (final_prices[lenn]*0.35) + (base_value*0.25) + (base_value*0.2) + (base_value*0.2)
    else:                            # If he has played 0 games
        player_price = base_value

    R1 = round(player_price, 2)
    c_R1 = R1
    c_purchase_price = R1*0.95 + 1
    c_sale_price = R1*1.05 - 1
    
    # Previous Round Price
    base_value = 6
    lenn = len(final_prices)-2

    if len(final_prices)-2 >= 3:     # If he has played 5 or more games
        player_price = (final_prices[lenn]*0.35) + (final_prices[lenn-1]*0.25) + (final_prices[lenn-2]*0.2) + (final_prices[lenn-3]*0.2)
    elif len(final_prices)-2 == 2:   # If he has played 4 games
        player_price = (final_prices[lenn]*0.35) + (final_prices[lenn-1]*0.25) + (final_prices[lenn-2]*0.2) + (base_value*0.2)
    elif len(final_prices)-2 == 1:   # If he has played 3 games
        player_price = (final_prices[lenn]*0.35) + (final_prices[lenn-1]*0.25) + (base_value*0.2) + (base_value*0.2)
    elif len(final_prices)-2 == 0:   # If he has played 2 game
        player_price = (final_prices[lenn]*0.35) + (base_value*0.25) + (base_value*0.2) + (base_value*0.2)
    else:                            # If he has played 0 games
        player_price = base_value

    R2 = round(player_price, 2)
    purchase_price = R2*0.95 + 1
    sale_price = R2*1.05 - 1
    
    # Round-2 Price
    base_value = 6
    lenn = len(final_prices)-3

    if len(final_prices)-3 >= 3:     # If he has played 6 or more games
        player_price = (final_prices[lenn]*0.35) + (final_prices[lenn-1]*0.25) + (final_prices[lenn-2]*0.2) + (final_prices[lenn-3]*0.2)
    elif len(final_prices)-3 == 2:   # If he has played 5 games
        player_price = (final_prices[lenn]*0.35) + (final_prices[lenn-1]*0.25) + (final_prices[lenn-2]*0.2) + (base_value*0.2)
    elif len(final_prices)-3 == 1:   # If he has played 4 games
        player_price = (final_prices[lenn]*0.35) + (final_prices[lenn-1]*0.25) + (base_value*0.2) + (base_value*0.2)
    elif len(final_prices)-3 == 0:   # If he has played 3 games
        player_price = (final_prices[lenn]*0.35) + (base_value*0.25) + (base_value*0.2) + (base_value*0.2)
    else:                            # If he has played 2 games
        player_price = base_value

    R3 = round(player_price, 2)
    purchase_price = R3*0.95 + 1
    sale_price = R3*1.05 - 1
    
    # Round-3 Price
    base_value = 6
    lenn = len(final_prices)-4

    if len(final_prices)-4 >= 3:     # If he has played 7 or more games
        player_price = (final_prices[lenn]*0.35) + (final_prices[lenn-1]*0.25) + (final_prices[lenn-2]*0.2) + (final_prices[lenn-3]*0.2)
    elif len(final_prices)-4 == 2:   # If he has played 6 games
        player_price = (final_prices[lenn]*0.35) + (final_prices[lenn-1]*0.25) + (final_prices[lenn-2]*0.2) + (base_value*0.2)
    elif len(final_prices)-4 == 1:   # If he has played 5 games
        player_price = (final_prices[lenn]*0.35) + (final_prices[lenn-1]*0.25) + (base_value*0.2) + (base_value*0.2)
    elif len(final_prices)-4 == 0:   # If he has played 4 games
        player_price = (final_prices[lenn]*0.35) + (base_value*0.25) + (base_value*0.2) + (base_value*0.2)
    else:                            # If he has played 3 games
        player_price = base_value

    R4 = round(player_price, 2)
    purchase_price = R4*0.95 + 1
    sale_price = R4*1.05 - 1
    
    # Round-4 Price
    base_value = 6
    lenn = len(final_prices)-5

    if len(final_prices)-5 >= 3:     # If he has played 8 or more games
        player_price = (final_prices[lenn]*0.35) + (final_prices[lenn-1]*0.25) + (final_prices[lenn-2]*0.2) + (final_prices[lenn-3]*0.2)
    elif len(final_prices)-5 == 2:   # If he has played 7 games
        player_price = (final_prices[lenn]*0.35) + (final_prices[lenn-1]*0.25) + (final_prices[lenn-2]*0.2) + (base_value*0.2)
    elif len(final_prices)-5 == 1:   # If he has played 6 games
        player_price = (final_prices[lenn]*0.35) + (final_prices[lenn-1]*0.25) + (base_value*0.2) + (base_value*0.2)
    elif len(final_prices)-5 == 0:   # If he has played 5 games
        player_price = (final_prices[lenn]*0.35) + (base_value*0.25) + (base_value*0.2) + (base_value*0.2)
    else:                            # If he has played 4 games
        player_price = base_value

    R5 = round(player_price, 2)
    purchase_price = R5*0.95 + 1
    sale_price = R5*1.05 - 1
    
    # Round-5 Price
    base_value = 6
    lenn = len(final_prices)-6

    if len(final_prices)-6 >= 3:     # If he has played 9 or more games
        player_price = (final_prices[lenn]*0.35) + (final_prices[lenn-1]*0.25) + (final_prices[lenn-2]*0.2) + (final_prices[lenn-3]*0.2)
    elif len(final_prices)-6 == 2:   # If he has played 8 games
        player_price = (final_prices[lenn]*0.35) + (final_prices[lenn-1]*0.25) + (final_prices[lenn-2]*0.2) + (base_value*0.2)
    elif len(final_prices)-6 == 1:   # If he has played 7 games
        player_price = (final_prices[lenn]*0.35) + (final_prices[lenn-1]*0.25) + (base_value*0.2) + (base_value*0.2)
    elif len(final_prices)-6 == 0:   # If he has played 6 games
        player_price = (final_prices[lenn]*0.35) + (base_value*0.25) + (base_value*0.2) + (base_value*0.2)
    else:                            # If he has played 5 games
        player_price = base_value

    R6 = round(player_price, 2)
    purchase_price = R6*0.95 + 1
    sale_price = R6*1.05 - 1
    
    # Round-6 Price
    base_value = 6
    lenn = len(final_prices)-7

    if len(final_prices)-7 >= 3:     # If he has played 9 or more games
        player_price = (final_prices[lenn]*0.35) + (final_prices[lenn-1]*0.25) + (final_prices[lenn-2]*0.2) + (final_prices[lenn-3]*0.2)
    elif len(final_prices)-7 == 2:   # If he has played 8 games
        player_price = (final_prices[lenn]*0.35) + (final_prices[lenn-1]*0.25) + (final_prices[lenn-2]*0.2) + (base_value*0.2)
    elif len(final_prices)-7 == 1:   # If he has played 7 games
        player_price = (final_prices[lenn]*0.35) + (final_prices[lenn-1]*0.25) + (base_value*0.2) + (base_value*0.2)
    elif len(final_prices)-7 == 0:   # If he has played 6 games
        player_price = (final_prices[lenn]*0.35) + (base_value*0.25) + (base_value*0.2) + (base_value*0.2)
    else:                            # If he has played 5 games
        player_price = base_value

    R7 = round(player_price, 2)
    purchase_price = R7*0.95 + 1
    sale_price = R7*1.05 - 1
    
    # Round-7 Price
    base_value = 6
    lenn = len(final_prices)-8

    if len(final_prices)-8 >= 3:     # If he has played 9 or more games
        player_price = (final_prices[lenn]*0.35) + (final_prices[lenn-1]*0.25) + (final_prices[lenn-2]*0.2) + (final_prices[lenn-3]*0.2)
    elif len(final_prices)-8 == 2:   # If he has played 8 games
        player_price = (final_prices[lenn]*0.35) + (final_prices[lenn-1]*0.25) + (final_prices[lenn-2]*0.2) + (base_value*0.2)
    elif len(final_prices)-8 == 1:   # If he has played 7 games
        player_price = (final_prices[lenn]*0.35) + (final_prices[lenn-1]*0.25) + (base_value*0.2) + (base_value*0.2)
    elif len(final_prices)-8 == 0:   # If he has played 6 games
        player_price = (final_prices[lenn]*0.35) + (base_value*0.25) + (base_value*0.2) + (base_value*0.2)
    else:                            # If he has played 5 games
        player_price = base_value

    R8 = round(player_price, 2)
    purchase_price = R8*0.95 + 1
    sale_price = R8*1.05 - 1
    
    # Round-8 Price
    base_value = 6
    lenn = len(final_prices)-9

    if len(final_prices)-9 >= 3:     # If he has played 9 or more games
        player_price = (final_prices[lenn]*0.35) + (final_prices[lenn-1]*0.25) + (final_prices[lenn-2]*0.2) + (final_prices[lenn-3]*0.2)
    elif len(final_prices)-9 == 2:   # If he has played 8 games
        player_price = (final_prices[lenn]*0.35) + (final_prices[lenn-1]*0.25) + (final_prices[lenn-2]*0.2) + (base_value*0.2)
    elif len(final_prices)-9 == 1:   # If he has played 7 games
        player_price = (final_prices[lenn]*0.35) + (final_prices[lenn-1]*0.25) + (base_value*0.2) + (base_value*0.2)
    elif len(final_prices)-9 == 0:   # If he has played 6 games
        player_price = (final_prices[lenn]*0.35) + (base_value*0.25) + (base_value*0.2) + (base_value*0.2)
    else:                            # If he has played 5 games
        player_price = base_value

    R9 = round(player_price, 2)
    purchase_price = R9*0.95 + 1
    sale_price = R9*1.05 - 1
    
    # Round-9 Price
    base_value = 6
    lenn = len(final_prices)-10

    if len(final_prices)-10 >= 3:     # If he has played 9 or more games
        player_price = (final_prices[lenn]*0.35) + (final_prices[lenn-1]*0.25) + (final_prices[lenn-2]*0.2) + (final_prices[lenn-3]*0.2)
    elif len(final_prices)-10 == 2:   # If he has played 8 games
        player_price = (final_prices[lenn]*0.35) + (final_prices[lenn-1]*0.25) + (final_prices[lenn-2]*0.2) + (base_value*0.2)
    elif len(final_prices)-10 == 1:   # If he has played 7 games
        player_price = (final_prices[lenn]*0.35) + (final_prices[lenn-1]*0.25) + (base_value*0.2) + (base_value*0.2)
    elif len(final_prices)-10 == 0:   # If he has played 6 games
        player_price = (final_prices[lenn]*0.35) + (base_value*0.25) + (base_value*0.2) + (base_value*0.2)
    else:                            # If he has played 5 games
        player_price = base_value

    R10 = round(player_price, 2)
    purchase_price = R10*0.95 + 1
    sale_price = R10*1.05 - 1
    
    # Round-10 Price
    base_value = 6
    lenn = len(final_prices)-11

    if len(final_prices)-11 >= 3:     # If he has played 10 or more games
        player_price = (final_prices[lenn]*0.35) + (final_prices[lenn-1]*0.25) + (final_prices[lenn-2]*0.2) + (final_prices[lenn-3]*0.2)
    elif len(final_prices)-11 == 2:   # If he has played 9 games
        player_price = (final_prices[lenn]*0.35) + (final_prices[lenn-1]*0.25) + (final_prices[lenn-2]*0.2) + (base_value*0.2)
    elif len(final_prices)-11 == 1:   # If he has played 8 games
        player_price = (final_prices[lenn]*0.35) + (final_prices[lenn-1]*0.25) + (base_value*0.2) + (base_value*0.2)
    elif len(final_prices)-11 == 0:   # If he has played 7 games
        player_price = (final_prices[lenn]*0.35) + (base_value*0.25) + (base_value*0.2) + (base_value*0.2)
    else:                            # If he has played 6 games
        player_price = base_value

    R11 = round(player_price, 2)
    purchase_price = R11*0.95 + 1
    sale_price = R11*1.05 - 1

    # Round-11 Price
    base_value = 6
    lenn = len(final_prices)-12

    if len(final_prices)-12 >= 3:     # If he has played 11 or more games
        player_price = (final_prices[lenn]*0.35) + (final_prices[lenn-1]*0.25) + (final_prices[lenn-2]*0.2) + (final_prices[lenn-3]*0.2)
    elif len(final_prices)-12 == 2:   # If he has played 10 games
        player_price = (final_prices[lenn]*0.35) + (final_prices[lenn-1]*0.25) + (final_prices[lenn-2]*0.2) + (base_value*0.2)
    elif len(final_prices)-12 == 1:   # If he has played 9 games
        player_price = (final_prices[lenn]*0.35) + (final_prices[lenn-1]*0.25) + (base_value*0.2) + (base_value*0.2)
    elif len(final_prices)-12 == 0:   # If he has played 8 games
        player_price = (final_prices[lenn]*0.35) + (base_value*0.25) + (base_value*0.2) + (base_value*0.2)
    else:                            # If he has played 7 games
        player_price = base_value

    R12 = round(player_price, 2)
    purchase_price = R12*0.95 + 1
    sale_price = R12*1.05 - 1

    # Round-12 Price
    base_value = 6
    lenn = len(final_prices)-13

    if len(final_prices)-13 >= 3:     # If he has played 12 or more games
        player_price = (final_prices[lenn]*0.35) + (final_prices[lenn-1]*0.25) + (final_prices[lenn-2]*0.2) + (final_prices[lenn-3]*0.2)
    elif len(final_prices)-13 == 2:   # If he has played 11 games
        player_price = (final_prices[lenn]*0.35) + (final_prices[lenn-1]*0.25) + (final_prices[lenn-2]*0.2) + (base_value*0.2)
    elif len(final_prices)-13 == 1:   # If he has played 10 games
        player_price = (final_prices[lenn]*0.35) + (final_prices[lenn-1]*0.25) + (base_value*0.2) + (base_value*0.2)
    elif len(final_prices)-13 == 0:   # If he has played 9 games
        player_price = (final_prices[lenn]*0.35) + (base_value*0.25) + (base_value*0.2) + (base_value*0.2)
    else:                            # If he has played 8 games
        player_price = base_value

    R13 = round(player_price, 2)
    purchase_price = R13*0.95 + 1
    sale_price = R13*1.05 - 1

    # Round-13 Price
    base_value = 6
    lenn = len(final_prices)-14

    if len(final_prices)-14 >= 3:     # If he has played 13 or more games
        player_price = (final_prices[lenn]*0.35) + (final_prices[lenn-1]*0.25) + (final_prices[lenn-2]*0.2) + (final_prices[lenn-3]*0.2)
    elif len(final_prices)-14 == 2:   # If he has played 12 games
        player_price = (final_prices[lenn]*0.35) + (final_prices[lenn-1]*0.25) + (final_prices[lenn-2]*0.2) + (base_value*0.2)
    elif len(final_prices)-14 == 1:   # If he has played 11 games
        player_price = (final_prices[lenn]*0.35) + (final_prices[lenn-1]*0.25) + (base_value*0.2) + (base_value*0.2)
    elif len(final_prices)-14 == 0:   # If he has played 10 games
        player_price = (final_prices[lenn]*0.35) + (base_value*0.25) + (base_value*0.2) + (base_value*0.2)
    else:                            # If he has played 9 games
        player_price = base_value

    R14 = round(player_price, 2)
    purchase_price = R14*0.95 + 1
    sale_price = R14*1.05 - 1

    # Round-14 Price
    base_value = 6
    lenn = len(final_prices)-15

    if len(final_prices)-15 >= 3:     # If he has played 14 or more games
        player_price = (final_prices[lenn]*0.35) + (final_prices[lenn-1]*0.25) + (final_prices[lenn-2]*0.2) + (final_prices[lenn-3]*0.2)
    elif len(final_prices)-15 == 2:   # If he has played 13 games
        player_price = (final_prices[lenn]*0.35) + (final_prices[lenn-1]*0.25) + (final_prices[lenn-2]*0.2) + (base_value*0.2)
    elif len(final_prices)-15 == 1:   # If he has played 12 games
        player_price = (final_prices[lenn]*0.35) + (final_prices[lenn-1]*0.25) + (base_value*0.2) + (base_value*0.2)
    elif len(final_prices)-15 == 0:   # If he has played 11 games
        player_price = (final_prices[lenn]*0.35) + (base_value*0.25) + (base_value*0.2) + (base_value*0.2)
    else:                            # If he has played 10 games
        player_price = base_value

    R15 = round(player_price, 2)
    purchase_price = R15*0.95 + 1
    sale_price = R15*1.05 - 1

    # Round-15 Price
    base_value = 6
    lenn = len(final_prices)-16

    if len(final_prices)-16 >= 3:     # If he has played 15 or more games
        player_price = (final_prices[lenn]*0.35) + (final_prices[lenn-1]*0.25) + (final_prices[lenn-2]*0.2) + (final_prices[lenn-3]*0.2)
    elif len(final_prices)-16 == 2:   # If he has played 14 games
        player_price = (final_prices[lenn]*0.35) + (final_prices[lenn-1]*0.25) + (final_prices[lenn-2]*0.2) + (base_value*0.2)
    elif len(final_prices)-16 == 1:   # If he has played 13 games
        player_price = (final_prices[lenn]*0.35) + (final_prices[lenn-1]*0.25) + (base_value*0.2) + (base_value*0.2)
    elif len(final_prices)-16 == 0:   # If he has played 12 games
        player_price = (final_prices[lenn]*0.35) + (base_value*0.25) + (base_value*0.2) + (base_value*0.2)
    else:                            # If he has played 11 games
        player_price = base_value

    R16 = round(player_price, 2)
    purchase_price = R16*0.95 + 1
    sale_price = R16*1.05 - 1
    
    
    # Price Vaulation
    Valuation = None
    L10mean = (R2+R3+R4+R5+R6+R7+R8+R9+R10+R11)/10
    if len(final_prices) < 14:
        Valuation = 'Inconclusive'
    elif R1<(L10mean*1.1) and R1>(L10mean*0.9):
        Valuation = 'Fair Value'
    elif R1<(L10mean*1.2) and R1>=(L10mean*1.1):
        Valuation = 'Overpriced'
    elif R1>(L10mean*0.8) and R1<=(L10mean*0.9):
        Valuation = 'Underpriced'
    elif R1>(L10mean*1.2):
        Valuation = 'Very Overpriced'
    elif R1<(L10mean*0.8):
        Valuation = 'Very Underpriced'
    
    price_history = []
    price_history.append(R16)
    price_history.append(R15)
    price_history.append(R14)
    price_history.append(R13)
    price_history.append(R12)
    price_history.append(R11)
    price_history.append(R10)
    price_history.append(R9)
    price_history.append(R8)
    price_history.append(R7)
    price_history.append(R6)
    price_history.append(R5)
    price_history.append(R4)
    price_history.append(R3)
    price_history.append(R2)
    price_history.append(R1)
    
    purchase_history = []
    purchase_history.append(R16*0.95 + 1)
    purchase_history.append(R15*0.95 + 1)
    purchase_history.append(R14*0.95 + 1)
    purchase_history.append(R13*0.95 + 1)
    purchase_history.append(R12*0.95 + 1)
    purchase_history.append(R11*0.95 + 1)
    purchase_history.append(R10*0.95 + 1)
    purchase_history.append(R9*0.95 + 1)
    purchase_history.append(R8*0.95 + 1)
    purchase_history.append(R7*0.95 + 1)
    purchase_history.append(R6*0.95 + 1)
    purchase_history.append(R5*0.95 + 1)
    purchase_history.append(R4*0.95 + 1)
    purchase_history.append(R3*0.95 + 1)
    purchase_history.append(R2*0.95 + 1)
    purchase_history.append(R1*0.95 + 1)
    
    sale_history = []
    sale_history.append(R16*1.05 - 1)
    sale_history.append(R15*1.05 - 1)
    sale_history.append(R14*1.05 - 1)
    sale_history.append(R13*1.05 - 1)
    sale_history.append(R12*1.05 - 1)
    sale_history.append(R11*1.05 - 1)
    sale_history.append(R10*1.05 - 1)
    sale_history.append(R9*1.05 - 1)
    sale_history.append(R8*1.05 - 1)
    sale_history.append(R7*1.05 - 1)
    sale_history.append(R6*1.05 - 1)
    sale_history.append(R5*1.05 - 1)
    sale_history.append(R4*1.05 - 1)
    sale_history.append(R3*1.05 - 1)
    sale_history.append(R2*1.05 - 1)
    sale_history.append(R1*1.05 - 1)
    
    plt.title('Price in Last 15')
    plt.xlabel('Game Number')
    plt.ylabel('Price $')
    plt.plot(price_history, label = "Price", color='black')
    plt.plot(sale_history, label = "Sell", color='red')
    plt.plot(purchase_history, label = "Buy", color='green')
    plt.legend()
    plt.grid()
    plt.show()
    
    punc_list = [".",";",":","!","?","/","\\",",","#","_","$","&",")","(","'","\""]
    playername = ''
    for i in First_Last:
        if i not in punc_list:
            playername += i
        else:
            playername += ' '
    CAPNAME = playername.upper()
    
    lastr = ((R1-R2)/R2)*100
    last5 = ((R1-R6)/R6)*100
    last10 = ((R1-R11)/R11)*100

    # Current Price
    print(CAPNAME, "CURRENT ROUND PRICE")
    print("Purchase Price: ", round(c_purchase_price, 2))
    print("Current Price: ", c_R1)
    print("Sale Price: ", round(c_sale_price, 2))
    print("Last Round Price Change: ", round(lastr,2), "%")
    print("5 Round Price Change: ", round(last5,2), "%")
    print("10 Round Price Change: ", round(last10,2), "%")
    print("Price Valuation: ", Valuation)
