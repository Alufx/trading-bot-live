import os, requests, random, json, time, threading, traceback
import websocket
from flask import Flask, jsonify

app = Flask(__name__)

PRICES = {"R_20": "--", "R_100": "--", "stpRNG500": "--", "stpRNG400": "--", "status": "starting...", "error": "", "last_id": 0}

ENDPOINTS = [
    "wss://ws.derivws.com/websockets/v3?app_id=1089",
    "wss://ws.binaryws.com/websockets/v3?app_id=1089",
    "wss://ws.deriv.com/websockets/v3?app_id=1089"
]

def on_message(ws, msg):
    try:
        d=json.loads(msg)
        if "tick" in d:
            sym=d["tick"]["symbol"]
            PRICES[sym]=str(d["tick"]["quote"])
            PRICES["last_id"]=d["tick"].get("id",0)
            PRICES["status"]=f"LIVE REAL @ {time.strftime('%H:%M:%S')} - {sym}"
            PRICES["error"]=""
    except Exception as e:
        PRICES["error"]=str(e)[:100]

def on_open(ws):
    PRICES["status"]="Connected - subscribing..."
    for s in ["R_20","R_100","stpRNG500","stpRNG400"]:
        ws.send(json.dumps({"ticks": s, "subscribe": 1}))

def on_error(ws, err):
    PRICES["error"]=f"WS error: {err}"
    PRICES["status"]=f"Error {str(err)[:50]}"

def on_close(ws, a, b):
    PRICES["status"]="Closed - retrying..."

def run_ws():
    idx=0
    while True:
        url=ENDPOINTS[idx%3]
        try:
            PRICES["status"]=f"Trying {url[8:22]} #{idx+1}"
            w=websocket.WebSocketApp(url, on_message=on_message, on_open=on_open, on_error=on_error, on_close=on_close)
            w.run_forever(sslopt={"cert_reqs": 0}, ping_interval=20, ping_timeout=10)
        except Exception as e:
            PRICES["error"]=traceback.format_exc()[-150:]
            PRICES["status"]=f"Exception {e}"
        idx+=1
        time.sleep(2)

threading.Thread(target=run_ws, daemon=True).start()

HTML = """
<html><head><meta name='viewport' content='width=device-width,initial-scale=1'>
<style>body{background:#020617;color:#fff;font-family:Arial;padding:10px}.card{background:#0f172a;padding:18px;border-radius:22px;max-width:460px;margin:15px auto;border:1px solid #1e293b}.tab{padding:10px 15px;background:#1e293b;border-radius:20px;margin:4px;display:inline-block;cursor:pointer;color:#94a3b8;border:1px solid #334155}.tab.active{background:#3b82f6;color:#fff}.big{font-size:58px;font-weight:900;text-align:center;margin:10px 0}.sig{font-size:26px;font-weight:900;text-align:center;padding:14px;border-radius:14px}</style></head><body>
<div class=card><h2>Alufx ULTIMATE</h2><p style=color:#22c55e>LIVE REAL Deriv - SERVER MODE - ONE PAIR</p><p id=status style=color:#fbbf24;font-size:11px>Loading...</p><p id=err style=color:#ef4444;font-size:9px;word-break:break-all></p><div><span class=tab id=t0 onclick="setPair('R_20')">Vol 20</span><span class=tab id=t1 onclick="setPair('R_100')">GainX400</span><span class=tab id=t2 onclick="setPair('stpRNG500')">Step 500</span><span class=tab id=t3 onclick="setPair('stpRNG400')">Step 400</span></div><div id=title style=text-align:center;color:#f59e0b;margin-top:12px;font-weight:bold>Volatility 20</div><div class=big id=price>--</div><div class=sig id=sig style=background:#1e293b>Connecting to server...</div><p id=log style=font-size:10px;color:#64748b></p><p style=font-size:9px;color:#475569>Links: ?pair=R_20 | R_100 | stpRNG500 | stpRNG400</p></div>
<script>
let cur=new URLSearchParams(location.search).get('pair')||'R_20'; const names={"R_20":"Volatility 20","R_100":"GainX400","stpRNG500":"Step 500","stpRNG400":"Step 400"}; let last={};
function setPair(p){cur=p; document.querySelectorAll('.tab').forEach(t=>t.classList.remove('active')); const m={"R_20":0,"R_100":1,"stpRNG500":2,"stpRNG400":3}; document.getElementById('t'+m[p]).classList.add('active'); document.getElementById('title').innerText=names[p]+' ('+p+')'; history.replaceState(null,'','?pair='+p);}
setPair(cur);
async function upd(){try{const r=await fetch('/api/prices'); const d=await r.json(); document.getElementById('status').innerText=d.status; document.getElementById('err').innerText=d.error||''; const pr=d[cur]||'--'; if(pr!=='--'){let dir='BUY ▲'; let col='#22c55e'; let bg='#052e16'; if(last[cur] && parseFloat(pr)<parseFloat(last[cur])){dir='SELL ▼'; col='#ef4444'; bg='#450a0a';} last[cur]=pr; document.getElementById('price').innerText=pr; document.getElementById('price').style.color=col; document.getElementById('sig').innerText=dir+' '+names[cur]; document.getElementById('sig').style.background=bg; document.getElementById('sig').style.color=col; document.getElementById('sig').style.border='2px solid '+col; document.getElementById('log').innerText='REAL: '+cur+' '+pr+' id:'+d.last_id+' @ '+new Date().toLocaleTimeString();}}catch(e){document.getElementById('status').innerText='Fetch err '+e;}} setInterval(upd,900); upd();
</script></body></html>
"""

@app.route('/')
def home(): return HTML

@app.route('/api/prices')
def prices(): return jsonify(PRICES)

@app.route('/health')
def health(): return "OK"
