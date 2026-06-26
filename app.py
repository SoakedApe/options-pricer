# app.py
import os
from flask import Flask, render_template, request, jsonify
from pricer.black_scholes import all_greeks
from pricer.monte_carlo import mc_european
from pricer.implied_vol import implied_vol

app = Flask(__name__)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/price", methods=["POST"])
def price():
    data  = request.json
    S     = float(data["spot"])
    K     = float(data["strike"])
    T     = float(data["expiry_days"]) / 365
    r     = float(data["rate"]) / 100
    sigma = float(data["vol"]) / 100
    opt   = data.get("option_type", "call")

    greeks = all_greeks(S, K, T, r, sigma, opt)
    mc     = mc_european(S, K, T, r, sigma, opt, n_paths=50_000)

    return jsonify({
        "bs_price": round(greeks["price"], 4),
        "delta":    round(greeks["delta"], 4),
        "gamma":    round(greeks["gamma"], 6),
        "theta":    round(greeks["theta"], 4),
        "vega":     round(greeks["vega"], 4),
        "rho":      round(greeks["rho"], 4),
        "mc_price": round(mc["price"], 4),
        "mc_ci":    [round(mc["ci_low"], 4), round(mc["ci_high"], 4)],
    })


@app.route("/iv", methods=["POST"])
def iv():
    data = request.json
    iv_val = implied_vol(
        market_price=float(data["market_price"]),
        S=float(data["spot"]),
        K=float(data["strike"]),
        T=float(data["expiry_days"]) / 365,
        r=float(data["rate"]) / 100,
        option_type=data.get("option_type", "call"),
    )
    return jsonify({"implied_vol": round(iv_val * 100, 2) if iv_val == iv_val else None})


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5002))
    app.run(debug=True, port=port)
