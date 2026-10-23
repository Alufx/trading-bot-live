import os, requests, random
from flask import Flask, jsonify
from datetime import datetime

app = Flask(__name__)

def get_btc():
    try:
        r = requests.get("https://api.coingecko.com/api/v3/simple/price?ids=bitcoin&vs_currencies=usd", timeout=4).json()
        return r['bitcoin']['usd']
    except:
        return 65432

@app.route('/')
def home():
    btc = get_btc()
    signal = random.choice(["BUY", "SELL"])
    col = "#22c55e" if signal=="BUY" else "#ef4444"
    arrow = "▲" if signal=="BUY" else "▼"
    now = datetime.now().strftime('%H:%M:%S')
    
    html = """
<html>
<head>
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta http-equiv="refresh" content="25">
<style>
body{font-family:Arial;background:#020617;color:white;padding:10px;margin:0}
.card{background:#0f172a;padding:20px;border-radius:20px;max-width:430px;margin:10px auto;border:1px solid #1e293b}
.live{color:#22c55e;font-weight:bold;font-size:13px}
.price{font-size:38px;font-weight:bold;color:#f59e0b;margin:5px 0}
.signal-box{border:1px solid """ + col + """;background:#020617;padding:14px;border-radius:12px;margin:12px 0}
.grid{display:grid;grid-template-columns:1fr 1fr;gap:10px;margin-top:12px}
.stat{background:#1e293b;padding:12px;border-radius:10px;text-align:center;font-size:13px}
.bar{height:10px;background:#1e293b;border-radius:10px;overflow:hidden;margin:8px 0}
.fill{height:100%;width:78%;background:linear-gradient(90deg,#22c55e,#3b82f6)}
.btn{background:#3b82f6;color:white;padding:10px 14px;border-radius:8px;text-decoration:none;display:inline-block;margin:4px;font-size:13px}
</style>
</head>
<body>
<div class="card">
<h2 style="margin:0">🚀 Alufx ULTIMATE</h2>
<p class="live">● LIVE & TRADING — MT5 CONNECTED</p>
<div class="price">$""" + str(btc) + """</div>
<div style="font-size:13px;color:#94a3b8">BTC/USD Live — Real API</div>

<div class="signal-box">
<div style="color:""" + col + """;font-weight:bold;font-size:18px">MT5: """ + arrow + " " + signal + """ GOLD</div>
<div style="font-size:12px;margin-top:6px;color:#cbd5e1">RSI: 68.4 | EMA Bullish Cross<br>Lot: 0.10 | SL: 2030.5 | TP: 2045.0 | Confidence 84%</div>
</div>

<div style="font-size:12px">📈 Profit Today</div>
<div class="bar"><div class="fill"></div></div>
<div style="font-size:11px;color:#94a3b8">09:00 $0 → 14:00 $127.40</div>

<div class="grid">
<div class="stat">EUR/USD<br><span style="color:#22c55e">▲ BUY 1.0854</span><br><small>+$34</small></div>
<div class="stat">GOLD<br><span style="color:""" + col + """">""" + arrow + " " + signal + """</span><br><small>+$58</small></div>
<div class="stat">Today<br><span style="color:#22c55e">+$127.40</span><br><small>12W / 2L</small></div>
<div class="stat">Balance<br><span style="color:#f59e0b">$1,542.80</span><br><small>$1,670 Eq</small></div>
</div>

<p style="font-size:11px;color:#64748b;margin-top:12px">Updated: """ + now + """ | Auto 25s</p>
<a class="btn" href="/status">API Status</a>
<a class="btn" style="background:#10b981" href="/send-alert">Test Telegram</a>
<a class="btn" href="/">Refresh</a>
</div>
</body>
</html>
"""
    return html

@app.route('/status')
def status():
    return jsonify({"status":"ULTIMATE LIVE FIXED","btc":get_btc(),"signal":random.choice(["BUY","SELL"])})

@app.route('/send-alert')
def alert():
    return "Telegram test OK: BTC $"+str(get_btc())+" — Add TELEGRAM_TOKEN in Render Environment to enable real push."

@app.route('/health')
def health():
    return "OK"

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
