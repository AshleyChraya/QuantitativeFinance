# -*- coding: utf-8 -*-
"""
Created on Wed Nov  1 11:12:04 2023

@author: Ajit
"""

import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt
from blackScholes import european_option
from datetime import datetime

# Replace 'AAPL' with the stock symbol you are interested in
stock_symbol = "AAPL"

def option_chain_data(stock_symbol):
    # Fetch the option chain data for the specified stock
    underlying = yf.Ticker(stock_symbol)
    option_expiries = underlying.options    
    # option_expiries=[option_expiries[0]]
    
    final_data = pd.DataFrame()
    for expiry in option_expiries:
        option = underlying.option_chain(date = expiry)
        data = option.calls
        data["OptionType"]= "Call"
        data["Expiry"] = expiry
        final_data = final_data._append(data)
        data = option.puts
        data["OptionType"]= "Put"
        data["Expiry"] = expiry
        final_data = final_data._append(data)
    final_data["Spot"] = underlying.history()['Close'].iloc[-1]
    return final_data
option_chain = option_chain_data(stock_symbol)
option_chain["ImpliedVol"]=0.0
option_chain["TimeToExpiry"]=0.0
for x in range(len(option_chain)):
    expiry = option_chain["Expiry"].iloc[x]
    expiry = datetime.strptime(expiry, '%Y-%m-%d').date()
    today_date = datetime.today().date()
    vol_guess = 0.30
    error = 0
    trial = 0
    temp_error=0
    while (error*temp_error>=0) and (trial < 100):
        # print(error)
        option1 = european_option(option_chain["Spot"].iloc[x],option_chain["strike"].iloc[x],interest_rate = 0.05,time_to_expiry = (expiry-today_date).days/365,vol_annual=vol_guess,option_type=option_chain["OptionType"].iloc[x])           
        temp_error = error
        error = option_chain["lastPrice"].iloc[x]-option1.option_price()
        # print(vol_guess)
        trial = trial +1
        if error>0:
            vol_guess = vol_guess*1.01
        else:
            vol_guess = vol_guess*0.99
    option_chain["ImpliedVol"].iloc[x]=vol_guess
    option_chain["TimeToExpiry"].iloc[x]= (expiry-today_date).days     
option_chain = option_chain[option_chain["OptionType"]=="Put"]
option_chain = option_chain[option_chain["strike"]>option_chain["Spot"]*0.8]
option_chain = option_chain[option_chain["strike"]<option_chain["Spot"]*1.2]
# plt.plot(option_chain["strike"], option_chain["ImpliedVol"],"go--")


import pandas as pd
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.tri as tri

# option_chain['Expiry'] = pd.to_datetime(option_chain['Expiry'])

# Create a 3D scatter plot (volatility surface)
fig = plt.figure(figsize=(8, 6))
ax = fig.add_subplot(111, projection='3d')
ax.scatter(option_chain['TimeToExpiry'], option_chain['strike'], option_chain['ImpliedVol'], c='b', marker='o')

# Set axis labels
ax.set_xlabel('TimeToExpiry')
ax.set_ylabel('Strike')
ax.set_zlabel('Implied Volatility')

# Set plot title
ax.set_title('Volatility Surface')

# Show the plot
plt.show()


#Code to plot surface
# triang = tri.Triangulation(option_chain['TimeToExpiry'], option_chain['strike'])
# fig = plt.figure(figsize=(8, 6))
# ax = fig.add_subplot(111, projection='3d')
# surf = ax.plot_trisurf(option_chain['TimeToExpiry'], option_chain['strike'], option_chain['ImpliedVol'], 
#                        triangles=triang.triangles, cmap='viridis')

# # Set axis labels
# ax.set_xlabel('Expiry')
# ax.set_ylabel('Strike')
# ax.set_zlabel('Implied Volatility')

# # Set plot title
# ax.set_title('Volatility Surface')

# # Add color bar
# fig.colorbar(surf, ax=ax, shrink=0.5, aspect=10)

# # Show the plot
# plt.show()

