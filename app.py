from flask import Flask, jsonify
import threading, time, json, random
import websocket

app = Flask(__name__)
PRICES = {"R_20": "--", "R_100": "--", "stpRNG500": "--", "stpRNG400": "--", "status": "Starting REAL Deriv...", "last": ""}

SYMBOLS = ["R_20", "R_100", "stpRNG500", "stpRNG400"]

def deriv_thread():
    # Try all Deriv WS endpoints - now WARP is on, DNS works
    endpoints = [
        "wss://ws.deriv.com/websockets/v3?app_id=1089",
        "wss://ws.derivws.com/websockets/v3?app_id=1089",
        "wss://ws.binaryws.com/websockets/v3?app_id=1089",
    ]
    def on_message(ws, msg):
        try:
            d = json.loads(msg)
            if "tick" in d:
                sym = d["tick"]["symbol"]
                quote = str(d["tick"]["quote"])
                PRICES[sym] = quote
                PRICES["status"] = f"LIVE REAL Deriv @ {time.strftime('%H:%M:%S')} via {PRICES.get('conn','deriv')}"
                PRICES["last"] = sym
        except: pass

    def on_open(ws):
        PRICES["status"] = "CONNECTED REAL - Subscribing..."
        for s in SYMBOLS:
            ws.send(json.dumps({"ticks": s, "subscribe": 1}))
        PRICES["conn"] = "ws.deriv.com"

    def on_error(ws, err):
        PRICES["status"] = f"WS error {err} - retrying"
    
    def run():
        idx = 0
        while True:
            try:
                url = endpoints[idx % len(endpoints)]
                PRICES["status"] = f"Connecting REAL to {url[8:22]} ..."
                PRICES["conn"] = url[8:22]
                ws = websocket.WebSocketApp(url, on_message=on_message, on_open=on_open, on_error=on_error)
                ws.run_forever(ping_interval=20)
            except Exception as e:
                PRICES["status"] = f"Reconnect {e}"
            idx += 1
            time.sleep(2)

    threading.Thread(target=run, daemon=True).start()

deriv_thread()

HTML = """<html><head><meta name='viewport' content='width=device-width,initial-scale=1'>
<style>body{margin:0;background:#020617;color:#fff;font-family:Arial}.c{max-width:420px;margin:10px auto;background:#0f172a;padding:16px;border-radius:20px;border:1px solid #22c55e}.t{padding:10px 14px;background:#1e293b;border-radius:20px;margin:3px;display:inline-block;cursor:pointer;color:#94a3b8;border:1px solid #334155}.a{background:#3b82f6;color:#fff}.b{font-size:56px;font-weight:900;text-align:center;margin:8px 0}.s{font-size:24px;font-weight:900;text-align:center;padding:12px;border-radius:12px}</style></head><body><div class=c>
<h2>Alufx ULTIMATE - REAL</h2><p style=color:#22c55e>● LIVE REAL Deriv - WARP ON</p><p id=st style=color:#22c55e;font-size:12px>Connecting REAL...</p>
<div><span class=t id=t0 onclick="setP('R_20')">Vol 20</span><span class=t id=t1 onclick="setP('R_100')">GainX400</span><span class=t id=t2 onclick="setP('stpRNG500')">Step 500</span><span class=t id=t3 onclick="setP('stpRNG400')">Step 400</span></div>
<div id=ttl style=text-align:center;color:#f59e0b;margin-top:10px;font-weight:bold>Vol 20 (R_20)</div><div class=b id=pr>--</div><div class=s id=sig style=background:#1e293b>Loading REAL tick...</div><p id=lg style=font-size:10px;color:#64748b></p><p style=font-size:9px;color:#22c55e>REAL Deriv feed via WARP - No simulation</p>
</div><script>
let cur=new URLSearchParams(location.search).get('pair')||'R_20';
const N={"R_20":"Vol 20","R_100":"GainX400","stpRNG500":"Step 500","stpRNG400":"Step 400"};
let last={};
function setP(p){cur=p;document.querySelectorAll('.t').forEach(x=>x.classList.remove('a'));document.getElementById('t'+({R_20:0,R_100:1,stpRNG500:2,stpRNG400:3}[p])).classList.add('a');document.getElementById('ttl').innerText=N[p]+' ('+p+')';history.replaceState(null,'','?pair='+p);}
async function poll(){
 try{
  const r=await fetch('/api/prices?'+Date.now());
  const d=await r.json();
  document.getElementById('st').innerText=d.status;
  const pr=d[cur];
  if(pr && pr!=='--'){
   let dir='BUY ▲';let col='#22c55e';let bg='#052e16';
   if(last[cur]&&parseFloat(pr)<parseFloat(last[cur])){dir='SELL ▼';col='#ef4444';bg='#450a0a';}
   last[cur]=pr;
   document.getElementById('pr').innerText=pr;
   document.getElementById('pr').style.color=col;
   document.getElementById('sig').innerText=dir+' '+N[cur]+' REAL';
   document.getElementById('sig').style.background=bg;
   document.getElementById('sig').style.color=col;
   document.getElementById('sig').style.border='2px solid '+col;
   document.getElementById('lg').innerText='REAL '+cur+' '+pr+' @ '+new Date().toLocaleTimeString()+' '+d.last;
  }
 }catch(e){}
}
setP(cur);
setInterval(poll,400);
poll();
</script></body></html>"""

@app.route('/')
def home(): return HTML
@app.route('/api/prices')
def api(): return jsonify(PRICES)
@app.route('/health')
def h(): return "OK"
