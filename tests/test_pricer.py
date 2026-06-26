# tests/test_pricer.py
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

import pytest
from pricer.black_scholes import bs_price, bs_delta, bs_gamma, bs_theta, bs_vega, bs_rho


def test_call_price_known_value():
    # S=100, K=100, T=1yr, r=5%, sigma=20% → call ≈ 10.45
    price = bs_price(S=100, K=100, T=1.0, r=0.05, sigma=0.20, option_type="call")
    assert abs(price - 10.45) < 0.05


def test_put_price_known_value():
    # same params → put ≈ 5.57
    price = bs_price(S=100, K=100, T=1.0, r=0.05, sigma=0.20, option_type="put")
    assert abs(price - 5.57) < 0.05


def test_put_call_parity():
    import math
    S, K, T, r, sigma = 100, 100, 1.0, 0.05, 0.20
    call = bs_price(S, K, T, r, sigma, "call")
    put  = bs_price(S, K, T, r, sigma, "put")
    assert abs(call - put - (S - K * math.exp(-r * T))) < 0.01


def test_delta_call_between_0_and_1():
    delta = bs_delta(S=100, K=100, T=1.0, r=0.05, sigma=0.20, option_type="call")
    assert 0 < delta < 1


def test_delta_put_between_minus1_and_0():
    delta = bs_delta(S=100, K=100, T=1.0, r=0.05, sigma=0.20, option_type="put")
    assert -1 < delta < 0


def test_gamma_positive():
    gamma = bs_gamma(S=100, K=100, T=1.0, r=0.05, sigma=0.20)
    assert gamma > 0


def test_vega_positive():
    vega = bs_vega(S=100, K=100, T=1.0, r=0.05, sigma=0.20)
    assert vega > 0


def test_deep_itm_call_delta_near_1():
    delta = bs_delta(S=200, K=100, T=1.0, r=0.05, sigma=0.20, option_type="call")
    assert delta > 0.95
