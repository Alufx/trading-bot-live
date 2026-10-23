from flask import Flask, jsonify
import threading, time, json, ssl
import websocket

app = Flask(__name__)
PRICES = {"R_20": "--", "R_100": "--", "stpRNG500": "--", "stpRNG400": "--", "status": "Starting REAL V4 Hard IP...", "last": 0}

# Hardcoded Deriv IPs - No DNS needed!
DERIV_IP = "104.18.15.22"
DERIV_HOST = "ws.deriv.com"

def run_real():
    while True:
        try:
            url = f"wss://{DERIV_IP}/websockets/v3?app_id=1089"
            PRICES["status"] = f"Connecting REAL {DERIV_HOST} -> {DERIV_IP} ..."
            def on_message(ws, msg):
                try:
                    d = json.loads(msg)
                    if "tick" in d:
                        sym = d["tick"]["symbol"]
                        PRICES[sym] = str(d["tick"]["quote"])
                        PRICES["status"] = f"LIVE REAL @ {time.strftime('%H:%M:%S')} - {sym} {PRICES[sym]} via {DERIV_IP}"
                except:
                    pass
            def on_open(ws):
                PRICES["status"] = "CONNECTED REAL - subscribing..."
                for s in ["R_20","R_100","stpRNG500","stpRNG400"]:
                    ws.send(json.dumps({"ticks": s, "subscribe": 1}))
            wsapp = websocket.WebSocketApp(url, on_message=on_message, on_open=on_open, header={"Host": DERIV_HOST})
            wsapp.run_forever(sslopt={"cert_reqs": ssl.CERT_NONE, "server_hostname": DERIV_HOST, "check_hostname": False}, ping_interval=20)
        except Exception as e:
            PRICES["status"] = f"Retry {e}"
            time.sleep(3)

threading.Thread(target=run_real, daemon=True).start()

HTML = """
<html><head><meta name='viewport' content='width=device-width,initial-scale=1'>
<style>body{margin:0;background:#020617;color:#fff;font-family:Arial}.c{max-width:430px;margin:12px auto;background:#0f172a;padding:16px;border-radius:20px;border:2px solid #22c55e}.t{padding:10px 14px;background:#1e293b;border-radius:20px;margin:3px;display:inline-block;cursor:pointer}.a{background:#3b82f6;color:#fff}.b{font-size:56px;font-weight:900;text-align:center;margin:10px 0}.s{font-size:20px;font-weight:900;text-align:center;padding:14px;border-radius:12px}</style></head><body><div class=c>
<h2>Alufx ULTIMATE - REAL V4</h2><p style=color:#22c55e>● LIVE REAL - Hard IP No DNS</p><p id=st style=color:#fbbf24;font-size:11px>Loading...</p>
<div><span class=t id=t0 onclick="setP('R_20')">Vol 20</span><span class=t id=t1 onclick="setP('R_100')">GainX400</span><span class=t id=t2 onclick="setP('stpRNG500')">Step 500</span><span class=t id=t3 onclick="setP('stpRNG400')">Step 400</span></div>
<div id=ttl style=text-align:center;color:#f59e0b;margin-top:12px;font-weight:bold>Vol 20 (R_20)</div><div class=b id=pr>--</div><div class=s id=sig style=background:#1e293b>Connecting REAL...</div><p id=lg style=font-size:10px;color:#64748b></p>
</div>
<script>
let cur='R_20';const N={"R_20":"Vol 20","R_100":"GainX400","stpRNG500":"Step 500","stpRNG400":"Step 400"};let last={};
function setP(p){cur=p;document.querySelectorAll('.t').forEach(x=>x.classList.remove('a'));document.getElementById('t'+({R_20:0,R_100:1,stpRNG500:2,stpRNG400:3}[p])).classList.add('a');document.getElementById('ttl').innerText=N[p]+' ('+p+')';}
async function poll(){try{
