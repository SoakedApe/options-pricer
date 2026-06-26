# options-pricer

Black-Scholes option pricer with Monte Carlo validation, full Greeks, and an implied volatility solver. Includes a web UI.

## What it prices

- **European options** (Black-Scholes closed-form + Monte Carlo)
- **Asian options** (Monte Carlo — arithmetic average payoff)
- **Barrier options** — down-and-in (Monte Carlo)

## Greeks

| Greek | Meaning |
|---|---|
| Delta | Price sensitivity to $1 move in spot |
| Gamma | Delta sensitivity to $1 move in spot |
| Theta | Time decay per calendar day |
| Vega  | Price sensitivity to 1% move in vol |
| Rho   | Price sensitivity to 1% move in risk-free rate |

## Quick start

```bash
pip install -r requirements.txt
python app.py   # open http://localhost:5002
```

## Example

```python
from pricer.black_scholes import all_greeks

result = all_greeks(S=100, K=100, T=30/365, r=0.05, sigma=0.20, option_type="call")
# {'price': 2.79, 'delta': 0.527, 'gamma': 0.0635, 'theta': -0.0176, 'vega': 0.116, 'rho': 0.012}
```

## Implied volatility

```python
from pricer.implied_vol import implied_vol

iv = implied_vol(market_price=3.50, S=100, K=100, T=30/365, r=0.05)
print(f"IV: {iv:.1%}")  # IV: 27.4%
```

## Monte Carlo vs Black-Scholes

For European options, Monte Carlo converges to the BS price (verified in tests). MC is required for path-dependent options (Asian, barrier) where no closed-form solution exists.

## Running tests

```bash
pytest tests/ -v
```

8 tests — call/put prices against known values, put-call parity, Greeks bounds, deep ITM delta.
