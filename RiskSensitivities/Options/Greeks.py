import os


#Libararies
from math import log
from math import sqrt
from scipy.stats import norm
from math import exp



###Code to reference the B;ackScholes option pricer of the library
# Specify the parent folder and the subfolder within it
parent_folder = "\\\QuantitativeFinance"
subfolder = r"\\DerivativesPricing\\Equity\\"

# Get the current directory
current_directory = str(os.getcwd())


# Construct the full path to the subfolder within the parent folder
subfolder_path = current_directory+parent_folder+subfolder

# Check if the subfolder exists
if os.path.exists(subfolder_path) and os.path.isdir(subfolder_path):
    # Change the current working directory to the subfolder
    os.chdir(subfolder_path)
    print("Current working directory changed to:", os.getcwd())
else:
    print("Specified subfolder not found.")

import blackScholes
os.chdir(current_directory)

#Inputs
spot = 100
strike = 100
interest_rate = 0.05
time_to_expiry = 1/12 #In years
vol_annual = 0.15
option_type = "Call"

option1 = blackScholes.european_option(spot,strike,interest_rate,time_to_expiry,vol_annual,"Call")
option1.option_price()
