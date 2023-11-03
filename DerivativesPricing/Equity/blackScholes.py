#Vanilla European Option Pricing using B-S Model
#Author: Ajit Kulkarni : 10/31/2023

#Libararies
from math import log
from math import sqrt
from scipy.stats import norm
from math import exp

#Inputs
spot = 100
strike = 100
interest_rate = 0.05
time_to_expiry = 1/12 #In years
vol_annual = 0.15
option_type = "Call"

class european_option:
    def __init__(self,spot,strike,interest_rate,time_to_expiry,vol_annual,option_type):
        '''The inputs are required to create a class called european option in the sequence spot,strike,interest_rate,time_to_expiry,vol_annual,option_type'''
        self.spot = spot
        self.strike = strike
        self.interest_rate = interest_rate
        self.time_to_expiry = time_to_expiry
        self.vol_annual = vol_annual       
        self.option_type = option_type
        if ((self.spot<0) or (self.strike<0) or (self.time_to_expiry<0) or (self.interest_rate<0)  or (self.vol_annual<0)):
            raise ValueError("Cannot create option class Invalid inputs, all should be >0")  
        
    def d1(self):
        '''Calculates d1, no input required'''
        d1 = 1/(self.vol_annual*(sqrt(self.time_to_expiry)))*(log(self.spot/self.strike)+(self.interest_rate+((self.vol_annual)**2)/2)*self.time_to_expiry)
        return d1
    
    def d2(self):
        '''Calculates d2, no input required'''
        d2 = self.d1() - self.vol_annual*sqrt(self.time_to_expiry)
        return d2
    
    def n_d1(self):
        '''Calculates n_d1, no input required'''
        n_d1 = norm.cdf(self.d1())
        return n_d1
    
    def n_d2(self):
        '''Calculates n_d2, no input required'''
        n_d2 = norm.cdf(self.d2())
        return n_d2
    
    def option_price(self):
        '''Calculates option price, no input required'''
        call_price = self.spot*self.n_d1()-self.strike*self.n_d2()*exp(-self.interest_rate*time_to_expiry)
        if self.option_type =="Call":
            price = call_price
        elif self.option_type =="Put":
            price = call_price - self.spot + self.strike*exp(-interest_rate*time_to_expiry)
        else:
            print("Invalid option type, choose Call or Put")
            price = None
        return price
    
option1 = european_option(spot,strike,interest_rate,time_to_expiry,0.12,"Call")
option1.option_price()