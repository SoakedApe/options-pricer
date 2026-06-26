# pricer/black_scholes.py
import math
from scipy.stats import norm


def _d1(S, K, T, r, sigma):
    return (math.log(S / K) + (r + 0.5 * sigma ** 2) * T) / (sigma * math.sqrt(T))


def _d2(S, K, T, r, sigma):
    return _d1(S, K, T, r, sigma) - sigma * math.sqrt(T)


def bs_price(S: float, K: float, T: float, r: float, sigma: float,
             option_type: str = "call") -> float:
    """Black-Scholes option price. T in years."""
    if T <= 0:
        return max(0, S - K) if option_type == "call" else max(0, K - S)
    d1 = _d1(S, K, T, r, sigma)
    d2 = _d2(S, K, T, r, sigma)
    if option_type == "call":
        return S * norm.cdf(d1) - K * math.exp(-r * T) * norm.cdf(d2)
    return K * math.exp(-r * T) * norm.cdf(-d2) - S * norm.cdf(-d1)


def bs_delta(S, K, T, r, sigma, option_type="call") -> float:
    if T <= 0:
        return 1.0 if (option_type == "call" and S > K) else 0.0
    d1 = _d1(S, K, T, r, sigma)
    return norm.cdf(d1) if option_type == "call" else norm.cdf(d1) - 1


def bs_gamma(S, K, T, r, sigma) -> float:
    if T <= 0:
        return 0.0
    d1 = _d1(S, K, T, r, sigma)
    return norm.pdf(d1) / (S * sigma * math.sqrt(T))


def bs_theta(S, K, T, r, sigma, option_type="call") -> float:
    """Theta per calendar day."""
    if T <= 0:
        return 0.0
    d1 = _d1(S, K, T, r, sigma)
    d2 = _d2(S, K, T, r, sigma)
    term1 = -(S * norm.pdf(d1) * sigma) / (2 * math.sqrt(T))
    if option_type == "call":
        return (term1 - r * K * math.exp(-r * T) * norm.cdf(d2)) / 365
    return (term1 + r * K * math.exp(-r * T) * norm.cdf(-d2)) / 365


def bs_vega(S, K, T, r, sigma) -> float:
    """Vega — price change per 1% move in vol."""
    if T <= 0:
        return 0.0
    d1 = _d1(S, K, T, r, sigma)
    return S * norm.pdf(d1) * math.sqrt(T) * 0.01


def bs_rho(S, K, T, r, sigma, option_type="call") -> float:
    """Rho — price change per 1% move in rate."""
    if T <= 0:
        return 0.0
    d2 = _d2(S, K, T, r, sigma)
    if option_type == "call":
        return K * T * math.exp(-r * T) * norm.cdf(d2) * 0.01
    return -K * T * math.exp(-r * T) * norm.cdf(-d2) * 0.01


def all_greeks(S, K, T, r, sigma, option_type="call") -> dict:
    return {
        "price": bs_price(S, K, T, r, sigma, option_type),
        "delta": bs_delta(S, K, T, r, sigma, option_type),
        "gamma": bs_gamma(S, K, T, r, sigma),
        "theta": bs_theta(S, K, T, r, sigma, option_type),
        "vega":  bs_vega(S, K, T, r, sigma),
        "rho":   bs_rho(S, K, T, r, sigma, option_type),
    }
