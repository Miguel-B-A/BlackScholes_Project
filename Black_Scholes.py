import numpy as np
from scipy.stats import stats

class BS():
     def __init__(self, spot, strike, rate, days, volatility, multiplier=100):
        self.spot = spot
        self.strike = strike
        self.rate = rate
        self.days = days / 365 # We divide by 365 because volatility and rate are annual
        self.volatility = volatility
        self.multiplier = multiplier