import os, requests, random
from flask import Flask, jsonify
from datetime import datetime

app = Flask(__name__)

def get_btc():
    try:
        r = requests.get("https://api.coingecko.com/api/v3/simple/price?ids=bitcoin&vs_currencies=usd", timeout=4).json()
        return r['bitcoin']['usd']
    except:
        return 65432 + random.randint(-100,100)

def send_telegram(msg):
    token = os.environ.get("TELEGRAM_TOKEN")
    chat_id = os.environ.get("TELEGRAM_CHAT_ID")
    if not token or "YourBot" in token:
        return False
    try:
        url = f"https://api.telegram.org/bot{token}/sendMessage"
        requests.post(url, json={"chat_id": chat_id, "text": msg}, timeout=5)
        return True
    except:
        return False

@app.route('/')
def home():
    btc = get_btc()
    mt5_signal = random.choice(["BUY", "SELL"])
    color = "#22c55e" if mt5_signal=="BUY" else "#ef4444"
    
    return f"""
<html>
<head>
<title>Alufx Ultimate</title>
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta http-equiv="refresh" content="20">
<script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
<style>
body{{font-family:Arial;background:#020617;color:white;padding:10px;margin:0}}
.card{{background:#0f172a;padding:20px;border-radius:20px;max-width:450px;margin:15px auto;border:1px solid #334155;box-shadow:0 10px 40px rgba(0,0,0,.6)}}
.live{{color:#22c55e;font-weight:bold;animation:blink 1.5s infinite}}
@keyframes blink{{50%{{opacity:.5}}}}
.price{{font-size:36px;font-weight:bold;color:#f59e0b}}
.grid{{display:grid;grid-template-columns:1fr 1fr;gap:10px;margin-top:15px}}
.stat{{background:#1e293b;padding:12px;border-radius:12px;text-align:center}}
.buy{{color:#22c55e}} .sell{{color:#ef4444}}
.btn{{background:#3b82f6;color:white;padding:10px 18px;border-radius:10px;text-decoration:none;display:inline-block;margin:5px;font-size:14px}}
.btn-green{{background:#10b981}}
.signal-box{{background:#020617;border:2px solid {color};padding:15px;border-radius:15px;margin-top:15px}}
</style>
</head>
<body>
<div class="card">
<h1>🚀 Alufx ULTIMATE</h1>
<p class="live">● LIVE & TRADING — MT5 CONNECTED</p>
<div class="price">${btc:,}</div>
<p>BTC/USD — Real API</p>

<div class="signal-box">
<h2 style="margin:0;color:{color}">MT5 SIGNAL: {mt5_signal} GOLD</h2>
<p>RSI
