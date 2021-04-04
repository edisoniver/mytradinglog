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
        binancepositions = positions()
        


        print(finalbalance)
        time.sleep(1)
        return render_template('home.html', finalbalance=finalbalance, crosspnl=crosspnl, walletbalance=walletbalance, 
        column_names=binancepositions.columns.values, row_data=list(binancepositions.values.tolist()), link_column="My Positions", zip=zip)

    
# Gets current balance
def final_balance():
    
    result = request_client.get_balance_v2()

    df = pd.DataFrame([t.__dict__ for t in result])

    balance = df['balance'].values[0]
    crosspnl = df['crossUnPnl'].values[0]
    print(df['crossUnPnl'].values[0])
    print(df['balance'].values[0])

    finalBalance = float(balance) + float(crosspnl)
    print(finalBalance)

    return finalBalance
# Gets PNL
def mypnl():

    result = request_client.get_balance_v2()

    df = pd.DataFrame([t.__dict__ for t in result])

    crosspnl = df['crossUnPnl'].values[0]
    print(crosspnl)

    return crosspnl

# Gets Wallet balance 
def wallet_balance():
    result = request_client.get_balance_v2()

    df = pd.DataFrame([t.__dict__ for t in result])

    balance = df['balance'].values[0]

    return balance

# Gets all available active positions
def positions():
    result = request_client.get_account_information()
    PrintMix.print_data(result.assets)

    print("=== Positions ===")
    df = pd.DataFrame([t.__dict__ for t in result.positions])
    print(df)
    print("==============")

    #columnsNamesArr = df.columns.values

    initialMargin = df['initialMargin'].tolist()
    #unrealizedProfit = df['unrealizedProfit'].tolist()
    #print(initialMargin)
    #print(unrealizedProfit)
    #print(columnsNamesArr)



    #For all values that are not empty, finds the row ID
    #Then it append it to this data frame of the whole row
    #Removes random dataframe columns
    #Returns the value
    df_all = pd.DataFrame()
    for i in range(len(initialMargin)):
        if initialMargin[i] == 0.0:
            pass
        else:
            #print("ROW NUMBER: -> ", i)
            #print("INITIAL MARGIN", initialMargin[i])
            #active_positions.append(df.iloc[i, :])
            position_results = df.iloc[i, :]
            df_all = df_all.append(position_results)
            df_all = df_all.drop(['isolated'], axis=1)
            df_all = df_all.drop(['positionSide'], axis=1)
            df_all = df_all.drop(['maintMargin'], axis=1)
            first_column = df_all.pop('symbol')
            df_all.insert(0, 'symbol', first_column)
    #print(df_all) Print active positions here.
            
    return df_all
    
