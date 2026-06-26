# pricer/implied_vol.py
"""Implied volatility solver using Brent's method."""
from scipy.optimize import brentq
from pricer.black_scholes import bs_price


def implied_vol(market_price: float, S: float, K: float, T: float,
                r: float, option_type: str = "call",
                vol_low: float = 0.001, vol_high: float = 10.0) -> float:
    """
    Find implied volatility such that BS price == market_price.
    Uses Brent's method (bracketed, guaranteed convergence).
    Returns NaN if no solution found in [vol_low, vol_high].
    """
    if T <= 0:
        return float("nan")

    try:
        iv = brentq(
            lambda sigma: bs_price(S, K, T, r, sigma, option_type) - market_price,
            vol_low, vol_high,
            xtol=1e-6, maxiter=500
        )
        return iv
    except ValueError:
        return float("nan")
