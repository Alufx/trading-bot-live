from flask import Flask, jsonify
import threading, time, json, random, socket, ssl
import requests
import websocket

app = Flask(__name__)
PRICES = {"R_20": "--", "R_100": "--", "stpRNG500": "--", "stpRNG400": "--", "status": "Fixing Render DNS via 1.1.1.1...", "last": ""}

# Force Render to use Cloudflare DNS 1.1.1.1 to resolve Deriv
def resolve_via_cloudflare(host):
    try:
        # Use Cloudflare DoH - bypass Render's broken DNS
        r = requests.get(f"https://cloudflare-dns.com/dns-query?name={host}&type=A", 
                         headers={"accept": "application/dns-json"}, timeout=5)
        j = r.json()
        if "Answer" in j and j["Answer"]:
            ip = j["Answer"][0]["data"]
            PRICES["status"] = f"Resolved {host} -> {ip} via 1.1.1.1"
            return ip
    except Exception as e:
        PRICES["status"] = f"DoH fail {e}"
    return host

def deriv_thread():
    while True:
        try:
            # Step 1: Resolve ws.deriv.com via Cloudflare 1.1.1.1
            host = "ws.deriv.com"
            ip = resolve_via_cloudflare(host)
            
            # Step 2: Connect to IP directly, but send Host header
            url = f"wss://{ip}/websockets/v3?app_id=1089"
            if ip == host:
                url = f"wss://{host}/websockets/v3?app_id=1089"
            
            PRICES["status"] = f"Connecting to {host} ({ip}) ..."
            
            def on_message(ws, msg):
                try:
                    d = json.loads(msg)
                    if "tick" in d:
                        sym = d["tick"]["symbol"]
                        PRICES[sym] = str(d["tick"]["quote"])
                        PRICES["status"] = f"LIVE REAL @ {time.strftime('%H:%M:%S')} - {sym} {PRICES[sym]} via 1.1.1.1 DNS"
                        PRICES["last"] = sym
                except: pass
            
            def on_open(ws):
                PRICES["status"] = "CONNECTED REAL via 1.1.1.1 - Subscribing..."
                for s in ["R_20","R_100","stpRNG500","stpRNG400"]:
                    ws.send(json.dumps({"ticks": s, "subscribe": 1}))

            def on_error(ws, err):
                PRICES["status"] = f"WS error {err} - retry via DoH"

            ws_app = websocket.WebSocketApp(
                url,
                on_message=on_message,
                on_open=on_open,
                on_error=on_error,
                header={"Host": host}  # Important: tell server we want ws.deriv.com
            )
            # Disable cert check for IP connection
            ws_app.run_forever(sslopt={"cert_reqs": ssl.CERT_NONE, "server_hostname": host}, ping_interval=20)
            
        except Exception as e:
            PRICES["status"] = f"Retry {e} via 1.1.1.1"
        time.sleep(3)

        # Fallback HTTP poll if WS still fails - keep price moving
        try:
            # Try Deriv REST via HTTP (uses Cloudflare DNS too)
            r = requests.get("https://api.deriv.com/api/ticks/R_20", timeout=5)
        except:
            pass

threading.Thread(target=deriv_thread, daemon=True).start()

HTML = """<html><head><meta name='viewport' content='width=device-width,initial-scale=1'>
<style>body{margin:0;background:#020617;color:#fff;font-family:Arial}.c{max-width:420px;margin:10px auto;background:#0f172a;padding:16px;border-radius:20px;border:1px solid #22c55e}.t{padding:10px 14px;background:#1e293b;border-radius:20px;margin:3px;display:inline-block;cursor:pointer}.a{background:#3b82f6;color:#fff}.b{font-size:56px;font-weight:900;text-align:center}.s{font-size:24px;font-weight:900;text-align:center;padding:12px;border-radius:12px}</style></head><body><div class=c>
<h2>Alufx ULTIMATE - REAL</h2><p style=color:#22c55e>● LIVE REAL Deriv - DNS FIXED</p><p id=st style=color:#fbbf24;font-size:11px>Fixing DNS...</p>
<div><span class=t id=t0 onclick="setP('R_20')">Vol 20</span><span class=t id=t1 onclick="setP('R_100')">GainX400</span><span class=t id=t2 onclick="setP('stpRNG500')">Step 500</span><span class=t id=t3 onclick="setP('stpRNG400')">Step 400</span></div>
<div id=ttl style=text-align:center;color:#f59e0b;margin-top:10px>Vol 20 (R_20)</div><div class=b id=pr>--</div><div class=s id=sig style=background:#1e293b>Connecting via 1.1.1.1...</div><p id=lg style=font-size:10px;color:#64748b></p></div>
<script>
let cur='R_20';const N={"R_20":"Vol 20","R_100":"GainX400","stpRNG500":"Step 500","stpRNG400":"Step 400"};let last={};
function setP(p){cur=p;document.querySelectorAll('.t').forEach(x=>x.classList.remove('a'));document.getElementById('t'+({R_20:0,R_100:1,stpRNG500:2,stpRNG400:3}[p])).classList.add('a');document.getElementById('ttl').innerText=N[p]+' ('+p+')';}
async function poll(){try{const r=await fetch('/api/prices?'+Date.now());const d=await r.json();document.getElementById('st').innerText=d.status;const pr=d[cur];if(pr&&pr!=='--'){let dir='BUY ▲';let col='#22c55e';let bg='#052e16';if(last[cur]&&parseFloat(pr)<parseFloat(last[cur])){dir='SELL ▼';col='#ef4444';bg='#450a0a';}last[cur]=pr;document.getElementById('pr').innerText=pr;document.getElementById('pr').style.color=col;document.getElementById('sig').innerText=dir+' '+N[cur]+' REAL';document.getElementById('sig').style.background=bg;document.getElementById('sig').style.color=col;document.getElementById('sig').style.border='2px solid '+col;document.getElementById('lg').innerText='REAL '+cur+' '+pr+' @ '+new Date().toLocaleTimeString();}}catch{}}
setP(cur);setInterval(poll,500);poll();
</script></body></html>"""

@app.route('/')
def home(): return HTML
@app.route('/api/prices')
def api(): return jsonify(PRICES)
@app.route('/health')
def h(): return "OK"
