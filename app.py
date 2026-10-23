from flask import Flask, jsonify
import threading, time, json, ssl, socket
import websocket

app = Flask(__name__)
PRICES = {"R_20": "--", "R_100": "--", "stpRNG500": "--", "stpRNG400": "--", "status": "Starting REAL V4.1 PATCH..."}

REAL_IP = "104.18.15.22"
HOSTS = ["ws.deriv.com", "ws.derivws.com", "ws.binaryws.com"]

# Patch DNS to bypass Errno -5
orig_getaddrinfo = socket.getaddrinfo
def patched_getaddrinfo(host, port, *args, **kwargs):
    if host in HOSTS:
        return [(socket.AF_INET, socket.SOCK_STREAM, 6, '', (REAL_IP, port))]
    return orig_getaddrinfo(host, port, *args, **kwargs)
socket.getaddrinfo = patched_getaddrinfo

def run():
    while True:
        for HOST in HOSTS:
            try:
                url = f"wss://{HOST}/websockets/v3?app_id=1089"
                PRICES["status"] = f"Trying REAL {HOST} -> {REAL_IP}..."
                def on_msg(ws, m):
                    try:
                        d=json.loads(m)
                        if "tick" in d:
                            s=d["tick"]["symbol"]; q=str(d["tick"]["quote"])
                            PRICES[s]=q
                            PRICES["status"]=f"LIVE REAL @ {time.strftime('%H:%M:%S')} {s} {q} via {HOST}"
                    except: pass
                def on_open(ws):
                    PRICES["status"]=f"CONNECTED REAL {HOST} - sub"
                    for sym in ["R_20","R_100","stpRNG500","stpRNG400"]:
                        ws.send(json.dumps({"ticks":sym,"subscribe":1}))
                def on_err(ws,e): PRICES["status"]=f"WS {HOST} err {e}"
                wa=websocket.WebSocketApp(url, on_message=on_msg, on_open=on_open, on_error=on_err)
                wa.run_forever(sslopt={"cert_reqs": ssl.CERT_NONE, "check_hostname": False}, ping_interval=15, ping_timeout=10)
            except Exception as e:
                PRICES["status"]=f"Retry {HOST} {e}"
                time.sleep(2)

threading.Thread(target=run, daemon=True).start()

@app.route('/')
def home():
    return '''
<html><head><meta name="viewport" content="width=device-width,initial-scale=1">
<style>body{margin:0;background:#020617;color:#fff;font-family:Arial}.c{max-width:430px;margin:auto;background:#0f172a;padding:16px;border-radius:20px;border:2px solid #22c55e}.t{padding:10px 14px;background:#1e293b;border-radius:20px;margin:3px;display:inline-block}.a{background:#3b82f6}.b{font-size:56px;font-weight:900;text-align:center}.s{font-size:20px;font-weight:900;text-align:center;padding:14px;border-radius:12px}</style></head><body><div class=c>
<h2>Alufx ULTIMATE REAL V4.1</h2><p style=color:#22c55e>● LIVE REAL - DNS Patch</p><p id=st style=color:#fbbf24;font-size:11px>Loading</p>
<div><span class=t id=t0 onclick="setP('R_20')">Vol 20</span><span class=t id=t1 onclick="setP('R_100')">GainX400</span><span class=t id=t2 onclick="setP('stpRNG500')">Step 500</span><span class=t id=t3 onclick="setP('stpRNG400')">Step 400</span></div>
<div id=ttl style=text-align:center;color:#f59e0b;margin-top:12px;font-weight:bold>Vol 20</div><div class=b id=pr>--</div><div class=s id=sig style=background:#1e293b>Connecting REAL...</div>
</div>
<script>
let cur='R_20';const N={"R_20":"Vol 20","R_100":"GainX400","stpRNG500":"Step 500","stpRNG400":"Step 400"};let last={};
function setP(p){cur=p;document.querySelectorAll('.t').forEach(x=>x.classList.remove('a'));document.getElementById('t'+({R_20:0,R_100:1,stpRNG500:2,stpRNG400:3}[p])).classList.add('a');document.getElementById('ttl').innerText=N[p]+' ('+p+')';}
async function poll(){try{const r=await fetch('/api/prices?'+Date.now());const d=await r.json();document.getElementById('st').innerText=d.status;const pr=d[cur];if(pr&&pr!='--'){let dir='BUY ▲';let col='#22c55e';let bg='#052e16';if(last[cur]&&parseFloat(pr)<parseFloat(last[cur])){dir='SELL ▼';col='#ef4444';bg='#450a0a';}last[cur]=pr;document.getElementById('pr').innerText=pr;document.getElementById('pr').style.color=col;document.getElementById('sig').innerText=dir+' '+N[cur]+' REAL';document.getElementById('sig').style.background=bg;document.getElementById('sig').style.color=col;}}catch{}}setP(cur);setInterval(poll,600);poll();
</script></body></html>
'''

@app.route('/api/prices')
def api(): return jsonify(PRICES)
@app.route('/health')
def h(): return "OK"
