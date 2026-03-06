import numpy as np
from scipy.stats import norm


class BS():
    def __init__(self, spot, strike, rate, days, volatility, multiplier=100):
        self.S     = spot
        self.K     = strike
        self.r     = rate / 100
        self.T     = days / 365
        self.sigma = volatility / 100
        self.mult  = multiplier

        
        # d1: z-score measuring how far ITM/OTM we are, adjusted for volatility and time.
        # N(d1) gives the probability-weighted chance of receiving the stock payoff. Cause we only receive the stock payoff if we expire ITM, and the payoff is S, not K.

        # d2: same as d1 but without the stock payoff adjustment.
        # N(d2) is the pure probability of expiring ITM, used for discounting the strike payoff.

        d1 = (np.log(self.S / self.K) + (self.r + 0.5 * self.sigma ** 2) * self.T) / (self.sigma * np.sqrt(self.T))
        d2 = d1 - self.sigma * np.sqrt(self.T)
        self.d1 = d1
        self.d2 = d2

    @property
    def call_price(self):
        return self.S * norm.cdf(self.d1) - self.K * np.exp(-self.r * self.T) * norm.cdf(self.d2) 

    @property
    def put_price(self):
        return self.K * np.exp(-self.r * self.T) * norm.cdf(-self.d2) - self.S * norm.cdf(-self.d1)
    #The Greeks


    @property
    def delta(self) -> tuple:
        call_delta = norm.cdf(self.d1)
        put_delta = norm.cdf(self.d1) - 1
        return call_delta, put_delta

    @property
    def gamma(self) -> float:
        return norm.pdf(self.d1) / (self.S * self.sigma * np.sqrt(self.T))
    

    @property
    def theta(self) -> float:
        call_theta = -self.S * self.sigma * norm.pdf(self.d1) / (2 * np.sqrt(self.T)) - self.r * self.K * np.exp(-self.r * self.T) * norm.cdf(self.d2)
        put_theta = -self.S * self.sigma * norm.pdf(self.d1) / (2 * np.sqrt(self.T)) + self.r * self.K * np.exp(-self.r * self.T) * norm.cdf(-self.d2)
        return call_theta/365

    @property
    def vega(self) -> float:
        return self.S * norm.pdf(self.d1) * np.sqrt(self.T) / 100

    @property
    def rho(self) -> float:
        call_rho = self.K * self.T * np.exp(-self.r * self.T) * norm.cdf(self.d2) / 100
        put_rho = -self.K * self.T * np.exp(-self.r * self.T) * norm.cdf(-self.d2) / 100
        return call_rho

    @property
    def intrinsic_value(self) -> float:
        return max(0.0, self.S - self.K)

    @property
    def put_call_parity(self) -> float:
        return self.call_price - self.put_price

    @property
    def moneyness(self) -> tuple:
        pct = (self.S / self.K - 1) * 100
        if abs(pct) < 1:
            return "ATM", pct
        elif self.S > self.K:
            return "ITM", pct
        else:
            return "OTM", pct
