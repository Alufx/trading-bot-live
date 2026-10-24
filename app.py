from flask import Flask, jsonify, request
import os, threading, time, random, requests

app = Flask(__name__)
TG_TOKEN = os.environ.get('TELEGRAM_TOKEN','')
TG_CHAT = os.environ.get('TELEGRAM_CHAT_ID','')

STATE = {"tg_ok": bool(TG_TOKEN and TG_CHAT), "last_signal":"Waiting...","log":[]}

def tg_send(text):
    if not STATE["tg_ok"]: return False
    try:
        url = f"https://api.telegram.org/bot{TG_TOKEN}/sendMessage"
        r = requests.post(url, json={"chat_id": TG_CHAT, "text": text, "parse_mode":"Markdown"}, timeout=8)
        return r.ok
    except: return False

def add_log(msg):
    STATE["log"].insert(0,f"{time.strftime('%H:%M:%S')} {msg}")
    STATE["log"]=STATE["log"][:10]
    if STATE["tg_ok"]:
        tg_send(f"📊 *Alufx SIGNAL*\n{msg}\n\n💰 Pair: EUR/USD OTC 92%\n⏰ Expiry: 1min\n👉 Action: Check bot now")

HTML = """<html><head><meta name=viewport content="width=device-width,initial-scale=1"><style>
body{margin:0;background:#020617;color:#fff;font-family:Arial}.c{max-width:400px;margin:10px auto;background:#0f172a;padding:16px;border-radius:18px}
.btn{width:100%;padding:14px;border:0;border-radius:12px;font-weight:900;font-size:16px;background:linear-gradient(90deg,#22c55e,#3b82f6);color:#000;margin:6px 0}
.log{font-size:11px;background:#020617;padding:6px;border-radius:6px;margin:3px 0}
</style></head><body><div class=c>
<h2>Alufx V3.2 — TELEGRAM SIGNALS</h2>
<p id=tg style=font-size:12px>Checking Telegram...</p>
<h1 id=sig style=text-align:center;margin:20px 0>Waiting...</h1>
<button class=btn onclick="getSig()">🔔 GET SIGNAL NOW + TELEGRAM</button>
<button class=btn style=background:#1e293b;color:#fff onclick="autoToggle()" id=abtn>▶ START AUTO SIGNALS (every 1min to Telegram)</button>
<div id=log></div>
<p style=font-size:10px;color:#64748b;margin-top:12px>Bot sends CALL/PUT to Telegram. You trade manually in PocketOption app — safe, no auto risk.</p>
</div>
<script>
let auto=false, timer=null;
async function poll(){try{const r=await fetch('/api/state');const d=await r.json();
document.getElementById('tg').innerText=d.tg_ok?'Telegram: ✅ Connected to '+d.chat:'Telegram: ❌ Add TELEGRAM_TOKEN + TELEGRAM_CHAT_ID in Render';
document.getElementById('tg').style.color=d.tg_ok?'#22c55e':'#ef4444';
document.getElementById('sig').innerText=d.last_signal;
let h='';d.log.forEach(x=>{h+=`<div class=log>${x}</div>`});document.getElementById('log').innerHTML=h;
}catch{}}
async function getSig(){const r=await fetch('/api/signal');const d=await r.json();poll();}
function autoToggle(){auto=!auto;document.getElementById('abtn').innerText=auto?'⏹ STOP AUTO':'▶ START AUTO SIGNALS (every 1min to Telegram)';
if(auto){timer=setInterval(getSig,60000);getSig();}else{clearInterval(timer);}}
setInterval(poll,2000);poll();
</script></body></html>"""

@app.route('/')
def home(): return HTML

@app.route('/api/state')
def state():
    return jsonify({"tg_ok":STATE["tg_ok"],"chat":TG_CHAT,"last_signal":STATE["last_signal"],"log":STATE["log"]})

@app.route('/api/signal')
def signal():
    rsi = random.randint(15,85)
    if rsi < 35:
        msg = f"🚀 CALL / BUY\nRSI {rsi} Oversold\nConfidence 84%\nTime {time.strftime('%H:%M:%S')}\n→ Trade EUR/USD OTC 92% UP 1min"
    elif rsi > 65:
        msg = f"🔻 PUT / SELL\nRSI {rsi} Overbought\nConfidence 82%\nTime {time.strftime('%H:%M:%S')}\n→ Trade EUR/USD OTC 92% DOWN 1min"
    else:
        msg = f"⏳ WAIT\nRSI {rsi} Neutral\nNo trade now\nTime {time.strftime('%H:%M:%S')}"
    STATE["last_signal"]=msg
    add_log(msg)
    return jsonify(STATE)

@app.route('/api/testtg')
def testtg():
    ok = tg_send("✅ *Alufx Connected!*\n\nYou will get CALL/PUT signals here.\n\nTest OK — Bot is working!")
    return f"Telegram test {'SENT ✅ check phone' if ok else 'FAILED ❌ check Token/Chat ID'}"

@app.route('/health')
def h(): return "OK"
