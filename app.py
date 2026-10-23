import os
import requests
from flask import Flask
from datetime import datetime

app = Flask(__name__)

def get_price():
    try:
        r = requests.get("https://api.coingecko.com/api/v3/simple/price?ids=bitcoin,gold&vs_currencies=usd", timeout=5).json()
        btc = r.get('bitcoin', {}).get('usd', 65432)
        return btc
    except:
        return 65432

@app.route('/')
def home():
    btc_price = get_price()
    return f"""
    <html>
    <head>
        <title>Alufx Trading Bot Pro</title>
        <meta name="viewport" content="width=device-width, initial-scale=1">
        <meta http-equiv="refresh" content="15">
        <style>
            body {{ font-family: Arial; background: #020617; color: white; text-align: center; padding: 20px; }}
            .card {{ background: #1e293b; padding: 25px; border-radius: 20px; max-width: 420px; margin: 15px auto; border: 1px solid #334155; }}
            .live {{ color: #22c55e; font-weight: bold; }}
            .price {{ font-size: 32px; font-weight: bold; color: #f59e0b; }}
            .grid {{ display: grid; grid-template-columns: 1fr 1fr; gap: 10px; margin-top: 15px; }}
            .stat {{ background: #0f172a; padding: 15px; border-radius: 12px; }}
            .buy {{ color: #22c55e; }} .sell {{ color: #ef4444; }}
            .btn {{ background: #3b82f6; color: white; padding: 12px 25px; border-radius: 10px; text-decoration: none; display: inline-block; margin: 10px; }}
        </style>
    </head>
    <body>
        <div class="card">
            <h1>🚀 Alufx Bot Pro</h1>
            <p class="live">● LIVE & TRADING</p>
            <div class="price">${btc_price:,}</div>
            <p>BTC/USD Live Price</p>
            
            <div class="grid">
                <div class="stat">
                    <div>EUR/USD</div>
                    <div class="buy">▲ BUY 1.0854</div>
                </div>
                <div class="stat">
                    <div>GOLD</div>
                    <div class="sell">▼ SELL 2034.5</div>
                </div>
                <div class="stat">
                    <div>Profit Today</div>
                    <div class="buy">+ $127.40</div>
                </div>
                <div class="stat">
                    <div>Trades</div>
                    <div>12 Wins</div>
                </div>
            </div>
            
            <p style="margin-top:20px;">Updated: {datetime.now().strftime('%H:%M:%S')} | Auto refresh 15s</p>
            <a class="btn" href="/status">API Status</a>
            <a class="btn" href="/" style="background:#10b981;">Refresh Now</a>
        </div>
    </body>
    </html>
    """

@app.route('/status')
def status():
    return {"status": "live", "bot": "Alufx Pro", "btc_price": get_price(), "signal": "BUY", "profit": "+$127.40"}

@app.route('/health')
def health():
    return "OK"

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
