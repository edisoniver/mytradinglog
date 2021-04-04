from flask import Flask
from binance_f import RequestClient
from binance_f.constant.test import *
from binance.client import Client
from binance_f.base.printobject import *
from binance_f.model.constant import *
from flask import Flask, request, render_template
import pandas as pd
import key
import time

app = Flask(__name__)

#Import Keys here from Binance Api
my_key = key.binanceapikey
that_secret = key.secretbinanceapikey

request_client = RequestClient(api_key=my_key, secret_key=that_secret)

@app.route("/")
def hello():
    while True:
        #Printing values to the html page
        finalbalance = str(final_balance())
        walletbalance = str(wallet_balance())
        crosspnl = str(mypnl())
        # binancepositions = positions()
        # column_names=binancepositions.columns.values, row_data=list(binancepositions.values.tolist()), link_column="My Positions"
        tradeinfo = trade_info()

        #print(finalbalance)
        time.sleep(1)
        return render_template('jumbotron.html', finalbalance=finalbalance, crosspnl=crosspnl, walletbalance =walletbalance,   
        column_names2=tradeinfo.columns.values, row_data2=list(tradeinfo.values.tolist()), link_column2="My positions 2", zip=zip)

    
# Gets current balance
def final_balance():
    
    result = request_client.get_account_information_v2()


    finalBalance = result.totalMarginBalance
 #-------------- My old code 
   # df = pd.DataFrame([t.__dict__ for t in result]
    # balance = df['balance'].values[0]
    # crosspnl = df['crossUnPnl'].values[0]
    # #print(df['crossUnPnl'].values[0])
    # #print(df['balance'].values[0])

    # finalBalance = float(balance) + float(crosspnl)
    # #print(finalBalance)
# ---------------
    return finalBalance
# Gets PNL
def mypnl():

    result = request_client.get_account_information_v2()
    crosspnl = result.totalUnrealizedProfit
    #----- Old code
    # result = request_client.get_balance_v2()
    # df = pd.DataFrame([t.__dict__ for t in result])
    # crosspnl = df['crossUnPnl'].values[0]
    # #print(crosspnl)

    return crosspnl

# Gets Wallet balance 
def wallet_balance():


    result = request_client.get_account_information_v2()
    balance = result.totalWalletBalance
    #-------Old Code -------
    # result = request_client.get_balance_v2()
    # df = pd.DataFrame([t.__dict__ for t in result])
    # balance = df['balance'].values[0]

    return balance

# Gets all available active positions
# def positions():
#     result2 = request_client.get_account_information()
#     df2 = pd.DataFrame([t.__dict__ for t in result2.positions])
 
#     #Prints out all columns in the dataframe
#     columnsNamesArr = df2.columns.values

#     initialMargin = df2['initialMargin'].tolist()
#     #unrealizedProfit = df['unrealizedProfit'].tolist()
#     #print(initialMargin)
#     #print(unrealizedProfit)


#     #For all values that are not empty, finds the row ID
#     #Then it append it to this data frame of the whole row
#     #Removes random dataframe columns
#     #Returns the value
#     df_all = pd.DataFrame()
#     for i in range(len(initialMargin)):
#         if initialMargin[i] == 0.0:
#             pass
#         else:
#             #print("ROW NUMBER: -> ", i)
#             #print("INITIAL MARGIN", initialMargin[i])
#             #active_positions.append(df.iloc[i, :])
#             position_results = df2.iloc[i, :]
#             df_all = df_all.append(position_results)
#             df_all = df_all.drop(['isolated'], axis=1)
#             df_all = df_all.drop(['positionSide'], axis=1)
#             df_all = df_all.drop(['maintMargin'], axis=1)
#     initialposition = df_all.pop('initialMargin')


        
#             #df_all.insert(0, 'symbol', first_column)
#     #print(df_all) Print active positions here.
#     print("""----
#     ---
#     ---
#     ---""")
#     print(initialposition)
#     return initialposition
    
def trade_info():
    #FOR TRADES
    result = request_client.get_position_v2()
    df = pd.DataFrame([t.__dict__ for t in result])
    #TO GET MARGIN DATA
    result2 = request_client.get_account_information()
    df2 = pd.DataFrame([t.__dict__ for t in result2.positions])
    #Initial Margin!
    initialMargin = df2['initialMargin'].tolist()
    #columnsNamesArr = df.columns.values
    entryprice = df['entryPrice'].tolist()

    
    df_all = pd.DataFrame()
    for i in range(len(initialMargin)):
        if initialMargin[i] == 0.0:
            pass
        else:
            #print("ROW NUMBER: -> ", i)
            #print("INITIAL MARGIN", initialMargin[i])
            #active_positions.append(df.iloc[i, :])
            position_results2 = df2.iloc[i, :]
            df_all = df_all.append(position_results2)
    positionInitialMargin = df_all.pop('initialMargin')
            
        
    all_pos = pd.DataFrame()
    for i in range(len(entryprice)):
        if entryprice[i] == 0.0:
            pass
        else:
            position_results = df.iloc[i, :]
            all_pos = all_pos.append(position_results)
            all_pos = all_pos.drop(['isolatedMargin'], axis=1)
            all_pos = all_pos.drop(['isAutoAddMargin'], axis=1)
            all_pos = all_pos.drop(['maxNotionalValue'], axis=1)
            #all_pos = all_pos.drop(['positionAmt'], axis=1)
            all_pos = all_pos.drop(['positionSide'], axis=1)
            first_column = all_pos.pop('symbol')
            all_pos.insert(0, 'symbol', first_column)
            second_column = all_pos.pop('marginType')
            all_pos.insert(1, 'marginType', second_column)
            third_column = all_pos.pop('leverage')
            all_pos.insert(1, 'leverage', third_column)
    all_pos.insert(1, 'initialMargin', positionInitialMargin)


    all_pos.columns = ['Pair', 'Margin', 'Leverage', 'Mode', 'Entry Price', 'LiqPrice', 'Mark Price', 'Amount', 'PNL']

    return all_pos
   
