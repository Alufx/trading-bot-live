from flask import Flask, jsonify
import threading, json, time
import websocket

app = Flask(__name__)
PRICES = {"R_20": "--", "R_100": "--", "stpRNG500": "--", "stpRNG400": "--", "last_id": 0, "status": "starting"}

def on_message(ws, message):
    try:
        d = json.loads(message)
        if "tick" in d:
            sym = d["tick"]["symbol"]
            price = str(d["tick"]["quote"])
            PRICES[sym] = price
            PRICES["last_id"] = d["tick"].get("id","")
            PRICES["status"] = "LIVE REAL @ " + time.strftime("%H:%M:%S")
    except: pass

def on_open(ws):
    for s in ["R_20","R_100","stpRNG500","stpRNG400"]:
        ws.send(json.dumps({"ticks": s, "subscribe": 1}))
    PRICES["status"] = "Connected to Deriv"

def run_ws():
    while True:
        try:
            ws = websocket.WebSocketApp("wss://ws.derivws.com/websockets/v3?app_id=1089", on_message=on_message, on_open=on_open)
            ws.run_forever()
        except: pass
        PRICES["status"] = "Reconnecting..."
        time.sleep(2)

threading.Thread(target=run_ws, daemon=True).start()

HTML = """
<html><head><meta name='viewport' content='width=device-width,initial-scale=1'><style>
body{font-family:Arial;background:#020617;color:#fff;padding:10px;margin:0}
.card{background:#0f172a;padding:18px;border-radius:20px;max-width:460px;margin:15px auto;border:1px solid #1e293b}
.tab{padding:9px 14px;border-radius:20px;background:#1e293b;color:#94a3b8;border:1px solid #334155;cursor:pointer;font-size:12px;margin:3px;display:inline-block}
.tab.active{background:#3b82f6;color:#fff;border-color:#3b82f6}
.big{font-size:54px;font-weight:bold;text-align:center;margin:12px 0}
.sig{font-size:24px;font-weight:bold;text-align:center;padding:14px;border-radius:12px}
</style></head><body><div class=card><h2>Alufx ULTIMATE</h2>
<p style=color:#22c55e>LIVE REAL Deriv - SERVER MODE - ONE PAIR</p>
<p id=status style=color:#fbbf24;font-size:11px>Loading...</p>
<div><span class=tab id=t0 onclick=setPair('R_20')>Vol 20</span><span class=tab id=t1 onclick=setPair('R_100')>GainX400</span><span class=tab id=t2 onclick=setPair('stpRNG500')>Step 500</span><span class=tab id=t3 onclick=setPair('stpRNG400')>Step 400</span></div>
<div id=title style=text-align:center;color:#f59e0b;margin-top:12px;font-weight:bold>Volatility 20</div>
<div class=big id=bigPrice>--</div>
<div class=sig id=bigSig style=background:#1e293b>Connecting to server...</div>
<p id=log style=font-size:10px;color:#64748b;margin-top:10px></p>
<p style=font-size:10px;color:#475569>Links: ?pair=R_20 | R_100 | stpRNG500 | stpRNG400 - This version cannot be blocked!</p>
</div><script>
let cur=new URLSearchParams(location.search).get('pair')||'R_20'; const names={"R_20":"Volatility 20 (R_20)","R_100":"GainX400 (R_100)","stpRNG500":"Step 500","stpRNG400":"Step 400"};
let last={};
function setPair(p){cur=p; document.querySelectorAll('.tab').forEach(t=>t.classList.remove('active')); const m={"R_20":0,"R_100":1,"stpRNG500":2,"stpRNG400":3}; document.getElementById('t'+m[p]).classList.add('active'); document.getElementById('title').innerText=names[p]; history.replaceState(null,'','?pair='+p); update();}
setPair(cur);
async function update(){
 try{
  const r=await fetch('/api/prices'); const d=await r.json();
  document.getElementById('status').innerText=d.status||'LIVE';
  const pr=d[cur]||'--';
  if(pr!=='--' && pr!==last[cur]){
    let dir='BUY ▲'; let col='#22c55e'; let bg='#052e16';
    if(last[cur] && parseFloat(pr)<parseFloat(last[cur])){dir='SELL ▼'; col='#ef4444'; bg='#450a0a';}
    last[cur]=pr;
    document.getElementById('bigPrice').innerText=pr;
    document.getElementById('bigPrice').style.color=col;
    document.getElementById('bigSig').innerText=dir+' '+names[cur];
    document.getElementById('bigSig').style.background=bg;
    document.getElementById('bigSig').style.color=col;
    document.getElementById('bigSig').style.border='2px solid '+col;
    document.getElementById('log').innerText='REAL SERVER: '+cur+' '+pr+' id '+d.last_id+' @ '+new Date().toLocaleTimeString();
  }
 }catch(e){document.getElementById('status').innerText='Fetch error '+e;}
}
setInterval(update, 800);
update();
</script></body></html>
"""

@app.route('/')
def home():
    return HTML

@app.route('/api/prices')
def prices():
    return jsonify(PRICES)

@app.route('/health')
def health():
    return "OK"
