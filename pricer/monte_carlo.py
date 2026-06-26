# pricer/monte_carlo.py
"""Monte Carlo option pricer — European, Asian, and barrier options."""
import numpy as np
import math


def mc_european(S, K, T, r, sigma, option_type="call", n_paths=100_000, seed=42) -> dict:
    rng = np.random.default_rng(seed)
    Z   = rng.standard_normal(n_paths)
    ST  = S * np.exp((r - 0.5 * sigma**2) * T + sigma * math.sqrt(T) * Z)

    if option_type == "call":
        payoffs = np.maximum(ST - K, 0)
    else:
        payoffs = np.maximum(K - ST, 0)

    price  = math.exp(-r * T) * payoffs.mean()
    stderr = payoffs.std() / math.sqrt(n_paths)
    return {
        "price":   price,
        "ci_low":  math.exp(-r * T) * (payoffs.mean() - 1.96 * stderr),
        "ci_high": math.exp(-r * T) * (payoffs.mean() + 1.96 * stderr),
        "n_paths": n_paths,
    }


def mc_asian(S, K, T, r, sigma, option_type="call", n_steps=252,
             n_paths=50_000, seed=42) -> dict:
    """Asian option — payoff based on arithmetic average price."""
    rng = np.random.default_rng(seed)
    dt  = T / n_steps
    Z   = rng.standard_normal((n_paths, n_steps))

    paths = np.zeros((n_paths, n_steps + 1))
    paths[:, 0] = S
    for t in range(1, n_steps + 1):
        paths[:, t] = paths[:, t-1] * np.exp(
            (r - 0.5 * sigma**2) * dt + sigma * math.sqrt(dt) * Z[:, t-1]
        )

    avg_price = paths[:, 1:].mean(axis=1)
    payoffs = (np.maximum(avg_price - K, 0) if option_type == "call"
               else np.maximum(K - avg_price, 0))

    price  = math.exp(-r * T) * payoffs.mean()
    stderr = payoffs.std() / math.sqrt(n_paths)
    return {
        "price":   price,
        "ci_low":  math.exp(-r * T) * (payoffs.mean() - 1.96 * stderr),
        "ci_high": math.exp(-r * T) * (payoffs.mean() + 1.96 * stderr),
    }


def mc_barrier_knockin(S, K, T, r, sigma, barrier, option_type="call",
                       n_steps=252, n_paths=50_000, seed=42) -> dict:
    """Down-and-in barrier option — only pays if price hits the barrier."""
    rng = np.random.default_rng(seed)
    dt  = T / n_steps
    Z   = rng.standard_normal((n_paths, n_steps))

    paths = np.zeros((n_paths, n_steps + 1))
    paths[:, 0] = S
    for t in range(1, n_steps + 1):
        paths[:, t] = paths[:, t-1] * np.exp(
            (r - 0.5 * sigma**2) * dt + sigma * math.sqrt(dt) * Z[:, t-1]
        )

    hit_barrier = (paths.min(axis=1) <= barrier)
    ST = paths[:, -1]
    payoffs = np.where(
        hit_barrier,
        np.maximum(ST - K, 0) if option_type == "call" else np.maximum(K - ST, 0),
        0
    )

    price = math.exp(-r * T) * payoffs.mean()
    return {"price": price, "barrier_hit_rate": float(hit_barrier.mean())}
