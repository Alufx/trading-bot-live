import os, requests, random, json, websocket
from flask import Flask, jsonify
from datetime import datetime

app = Flask(__name__)

DERIV_WS = "wss://ws.binaryws.com/websockets/v3?app_id=1089"

SYMBOLS = {
    "Volatility 20": "R_20",
    "GainX400": "R_100",
    "Step 500": "stpRNG500",
    "Step 400": "stpRNG400"
}

def get_deriv_price(deriv_symbol):
    try:
        ws = websocket.create_connection(DERIV_WS, timeout=5)
        ws.send(json.dumps({"ticks": deriv_symbol}))
        for _ in range(5):
            resp = ws.recv()
            data = json.loads(resp)
            if "tick" in data:
                price = data["tick"]["quote"]
                ws.close()
                return float(price)
        ws.close()
    except Exception as e:
        print(f"Deriv error {deriv_symbol}: {e}")
    return None

def get_all_prices():
    prices = {}
    for name, deriv_sym in SYMBOLS.items():
        real = get_deriv_price(deriv_sym)
        if real:
            prices[name] = {"price": real, "real": True}
        else:
            base = {"Volatility 20":145, "GainX400":400, "Step 500":500, "Step 400":400}[name]
            prices[name] = {"price": base + random.uniform(-1,1), "real": False}
    return prices

@app.route('/')
def home():
    all_prices = get_all_prices()
    main_sig = random.choice(["BUY","SELL"])
    main_col = "#22c55e" if main_sig=="BUY" else "#ef4444"
    main_arrow = "▲" if main_sig=="BUY" else "▼"
    now = datetime.now().strftime('%H:%M:%S')

    cards_html = ""
    for name in ["Volatility 20","GainX400","Step 500","Step 400"]:
        data = all_prices.get(name, {"price":0,"real":False})
        price = data["price"]
        is_real = data["real"]
        sig = random.choice(["BUY","SELL"])
        col = "#22c55e" if sig=="BUY" else "#ef4444"
        arrow = "▲" if sig=="BUY" else "▼"
        profit = random.randint(12,89)
        badge = "● REAL" if is_real else "○ SIM"
        badge_col = "#22c55e" if is_real else "#64748b"
        price_str = f"{price:.2f}"
        
        cards_html += f"""
        <div class="stat">
            <div style="font-size:10px;color:{badge_col}">{badge} {name}</div>
            <span style="color:{col};font-size:16px">{arrow}
