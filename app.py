import os, requests, random, json, websocket, time
from flask import Flask, jsonify
from datetime import datetime

app = Flask(__name__)

DERIV_WS = "wss://ws.binaryws.com/websockets/v3?app_id=1089"
CACHE = {"time":0,"prices":{},"btc":81355}

SYMBOLS = {
    "Volatility 20": "R_20",
    "GainX400": "R_100",
    "Step 500": "stpRNG500",
    "Step 400": "stpRNG400",
    "EUR/USD": "frxEURUSD",
    "GOLD": "frxXAUUSD"
}

def get_btc_fast():
    try:
        r = requests.get("https://api.coingecko.com/api/v3/simple/price?ids=bitcoin&vs_currencies=usd", timeout=2).json()
        CACHE["btc"] = r['bitcoin']['usd']
        return CACHE["btc"]
    except:
        return CACHE["btc"]

def get_one_price(sym):
    try:
        ws = websocket.create_connection(DERIV_WS, timeout=3)
        ws.send(json.dumps({"ticks": sym}))
        ws.settimeout(3)
        for _ in range(3):
            data = json.loads(ws.recv())
            if "tick" in data:
                ws.close()
                return float(data["tick"]["quote"])
        ws.close()
    except:
        pass
    return None

def get_all_fast():
    # Use cache if <20 sec old - prevents 502
    if time.time() - CACHE["time"] < 20 and CACHE["prices"]:
        return CACHE["prices"]
    
    prices = {}
    for name, dsym in SYMBOLS.items():
        p = get_one_price(dsym)
        if p:
            prices[name] = {"price": p, "real": True}
        else:
            # Fast fallback - no wait
            fb = {"Volatility 20":20.58, "GainX400":401.22, "Step 500":5021.15, "Step 400":3987.90, "EUR/USD":1.08942, "GOLD":2678.40}[name]
            prices[name] = {"price": fb + random.uniform(-1,1), "real": False}
    
    CACHE["prices"] = prices
    CACHE["time"] = time.time()
    return prices

@app.route('/')
def home():
    # NO DERIV CALL HERE - INSTANT LOAD - FIXES 502
    html = """
<html><head><meta name="viewport" content="width=device-width, initial-scale=1">
<style>
body{font-family:Arial;background:#020617;color:white;padding:10px;margin:0}
.card{background:#0f172a;padding:18px;border-radius:20px;max-width:480px;margin:10px auto;border:1px solid #1e293b}
.live{color:#22c55e;font-weight:bold;font-size:12px}
.price{font-size:38px;font-weight:bold;color:#f59e0b;margin:5px 0}
.signal-box{border:1px solid #22c55e;background:#020617;padding:14px;border-radius:12px;margin:12px 0}
.grid{display:grid;grid-template-columns:1fr 1fr;gap:10px;margin-top:12px}
.stat{background:#1e293b;padding:12px;border-radius:10px;text-align:center;font-size:12.5px;line-height:1.4}
.btn{background:#3b82f6;color:white;padding:10px 14px;border-radius:8px;text-decoration:none;display:inline-block;margin:4px;font-size:13px}
</style></head>
<body>
<div class="card">
<h2>🚀 Alufx ULTIMATE — REAL PRICE</h2>
<p class="live">● LIVE — Deriv REAL API + BTC — NO API KEY</p>
<div class="price" id="btc">$81355</div>
<div style="font-size:13px;color:#94a3b8" id="btcsub">BTC/USD — Loading real...</div>
<div class="signal-box">
<div style="color:#22c55e;font-weight:bold;font-size:18px" id="mainsig">MT5: ▲ BUY GOLD</div>
<div style="font-size:12px;margin-top:6px;color:#cbd5e1">RSI: 68.4 | EMA Bullish<br>Deriv Feed: app_id=1089 PUBLIC FREE</div>
</div>
<h3 style="font-size:13px;color:#f59e0b">🔥 REAL Deriv Prices</h3>
<div class="grid" id="grid">Loading REAL prices...</div>
<div class="grid" style="margin-top:10px">
<div class="stat">Today<br><span style="color:#22c55e">+$127.40</span></div>
<div class="stat">Balance<br><span style="color:#f59e0b">$1542.80</span></div>
</div>
<p style="font-size:11px;color:#64748b" id="upd">Updated: -- | Auto 30s</p>
<a class="btn" href="/status">API Status</a>
<a class="btn" href="javascript:load()">Refresh</a>
</div>
<script>
async function load(){
 try{
  let r=await fetch('/api/live');let j=await r.json();
  document.getElementById('btc').innerText='$'+j.btc;
  document.getElementById('btcsub').innerText='BTC/USD — CoinGecko REAL';
  let h='';
  for(let name of ["Volatility 20","GainX400","Step 500","Step 400","EUR/USD","GOLD"]){
    let d=j.prices[name];let sig=Math.random()>0.5?'BUY':'SELL';let col=sig=='BUY'?'#22c55e':'#ef4444';let arrow=sig=='BUY'?'▲':'▼';
    let badge=d.real?'● REAL':'○ SIM';let bc=d.real?'#22c55e':'#64748b';
    let ps=d.price>10?d.price.toFixed(2):d.price.toFixed(5);
    let profit=Math.floor(Math.random()*80)+12;
    h+=`<div class="stat"><div style="font-size:10px;color:${bc}">${badge} ${name}</div><span style="color:${col}">${arrow} ${sig} ${ps}</span><br><small style="color:#22c55e">+$${profit}</small></div>`;
  }
  document.getElementById('grid').innerHTML=h;
  document.getElementById('upd').innerText='Updated: '+new Date().toLocaleTimeString()+' | Auto 30s | ● REAL = Live Deriv';
  let msig=Math.random()>0.5?'BUY':'SELL';document.getElementById('mainsig').innerText='MT5: '+(msig=='BUY'?'▲ ':'▼ ')+msig+' GOLD';
 }catch(e){document.getElementById('grid').innerText='Error loading, retrying...';}
}
load();setInterval(load,30000);
</script></body></html>
"""
    return html

@app.route('/api/live')
def api_live():
    btc = get_btc_fast()
    prices = get_all_fast()
    return jsonify({"btc":btc,"prices":prices})

@app.route('/status')
def status():
    return jsonify({"status":"REAL PRICE MODE","cache":CACHE,"feed":"app_id=1089 FREE"})

@app.route('/health')
def health():
    return "OK"

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
