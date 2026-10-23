from flask import Flask, jsonify
import threading, time, json, ssl, socket
import requests
import websocket

app = Flask(__name__)
PRICES = {"R_20": "--", "R_100": "--", "stpRNG500": "--", "stpRNG400": "--", "status": "Starting REAL via 1.1.1.1...", "last": time.time()}

def get_ip_cloudflare(host):
    try:
        r = requests.get(f"https://cloudflare-dns.com/dns-query?name={host}&type=A", headers={"accept":"application/dns-json"}, timeout=5)
        data = r.json()
        if "Answer" in data:
            for ans in data["Answer"]:
                if ans["type"]==1:
                    return ans["data"]
    except Exception as e:
        PRICES["status"]=f"DoH err {e}"
    return host

def deriv_real():
    while True:
        try:
            host="ws.deriv.com"
            ip=get_ip_cloudflare(host)
            url=f"wss://{ip}/websockets/v3?app_id=1089"
            PRICES["status"]=f"Connecting REAL {host} -> {ip} ..."
            def on_message(ws, msg):
                try:
                    d=json.loads(msg)
                    if "tick" in d:
                        sym=d["tick"]["symbol"]
                        quote=str(d["tick"]["quote"])
                        PRICES[sym]=quote
                        PRICES["last"]=time.time()
                        PRICES["status"]=f"LIVE REAL @ {time.strftime('%H:%M:%S')} - {sym} {quote} via {ip}"
                except: pass
            def on_open(ws):
                PRICES["status"]="CONNECTED REAL - subscribing..."
                for s in ["R_20","R_100","stpRNG500","stpRNG400"]:
                    ws.send(json.dumps({"ticks":s,"subscribe":1}))
            def on_error(ws,err):
                PRICES["status"]=f"WS err {err} retry"
            wsapp=websocket.WebSocketApp(url, on_message=on_message, on_open=on_open, on_error=on_error, header={"Host":host})
            wsapp.run_forever(sslopt={"cert_reqs":ssl.CERT_NONE, "server_hostname":host, "check_hostname":False}, ping_interval=15, ping_timeout=10)
        except Exception as e:
            PRICES["status"]=f"Retry {e}"
            time.sleep(2)

threading.Thread(target=deriv_real, daemon=True).start()

HTML="""
<html><head><meta name='viewport' content='width=device-width,initial-scale=1'>
<style>body{margin:0;background:#020617;color:#fff;font-family:Arial}.c{max-width:430px;margin:12px auto;background:#0f172a;padding:16px;border-radius:20px;border:2px solid #22c55e}.t{padding:10px 14px;background:#1e293b;border-radius:20px;margin:3px;display:inline-block;cursor:pointer}.a{background:#3b82f6;color:#fff}.b{font-size:56px;font-weight:900;text-align:center;margin:10px 0}.s{font-size:20px;font-weight:900;text-align:center;padding:14px;border-radius:12px}</style></head><body><div class=c>
<h2>Alufx ULTIMATE - REAL V3</h2><p style=color:#22c55e>● LIVE REAL - Server via 1.1.1.1 (No WARP needed on phone)</p><p id=st style=color:#fbbf24;font-size:11px>Loading...</p>
<div><span class=t id=t0 onclick="setP('R_20')">Vol 20</span><span class=t id=t1 onclick="setP('R_100')">GainX400</span><span class=t id=t2 onclick="setP('stpRNG500')">Step 500</span><span class=t id=t3 onclick="setP('stpRNG400')">Step 400</span></div>
<div id=ttl style=text-align:center;color:#f59e0b;margin-top:12px;font-weight:bold>Vol 20 (R_20)</div><div class=b id=pr>--</div><div class=s id=sig style=background:#1e293b>Connecting REAL...</div><p id=lg style=font-size:10px;color:#64748b></p>
</div>
<script>
let cur='R_20';const N={"R_20":"Vol 20","R_100":"GainX400","stpRNG500":"Step 500","stpRNG400":"Step 400"};let last={};
function setP(p){cur=p;document.querySelectorAll('.t').forEach(x=>x.classList.remove('a'));document.getElementById('t'+({R_20:0,R_100:1,stpRNG500:2,stpRNG400:3}[p])).classList.add('a');document.getElementById('ttl').innerText=N[p]+' ('+p+')';}
async function poll(){try{const r=await fetch('/api/prices?'+Date.now());const d=await r.json();document.getElementById('st').innerText=d.status;const pr=d[cur];if(pr&&pr!='--'){let dir='BUY ▲';let col='#22c55e';let bg='#052e16';if(last[cur]&&parseFloat(pr)<parseFloat(last[cur])){dir='SELL ▼';col='#ef4444';bg='#450a0a';}last[cur]=pr;document.getElementById('pr').innerText=pr;document.getElementById('pr').style.color=col;document.getElementById('sig').innerText=dir+' '+N[cur]+' REAL';document.getElementById('sig').style.background=bg;document.getElementById('sig').style.color=col;document.getElementById('sig').style.border='2px solid '+col;document.getElementById('lg').innerText='REAL '+cur+' '+pr+' @ '+new Date().toLocaleTimeString();}}catch{}}setP(cur);setInterval(poll,600);poll();
</script></body></html>
"""
@app.route('/')
def home(): return HTML
@app.route('/api/prices')
def prices(): return jsonify(PRICES)
@app.route('/health')
def health(): return "OK"
