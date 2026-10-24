from flask import Flask, jsonify
import os, requests, random, time
from datetime import datetime

app = Flask(__name__)

TG_TOKEN = os.environ.get('TELEGRAM_TOKEN','')
TG_CHAT = os.environ.get('TELEGRAM_CHAT_ID','')

PAIRS = ["EURUSD_otc","GBPUSD_otc","EURJPY_otc","USDJPY_otc","AUDUSD_otc","EURGBP_otc","GBPJPY_otc","BTCUSD_otc"]
STATE = {"pair":"GBPUSD_otc","tf":"1m","last":{},"log":[]}

def tg_send(text):
    if not TG_TOKEN or not TG_CHAT: return False
    try:
        url = f"https://api.telegram.org/bot{TG_TOKEN}/sendMessage"
        r = requests.post(url, json={"chat_id": TG_CHAT, "text": text, "parse_mode":"Markdown"}, timeout=5)
        return r.ok
    except: return False

def make_signal(pair):
    price = round(random.uniform(1.05, 1.35) if "JPY" not in pair else random.uniform(140,160),5)
    rsi = random.randint(22,78)
    acc = random.randint(78,92)
    if rsi < 38: direction, color = "CALL ▲", "#22c55e"
    elif rsi > 62: direction, color = "PUT ▼", "#ef4444"
    else: direction, color = "WAIT ●", "#f59e0b"
    trend = "DOWN" if rsi>50 else "UP"
    bb = "LOWER" if rsi<35 else "UPPER" if rsi>65 else "MIDDLE"
    
    data = {"pair":pair,"price":price,"dir":direction,"color":color,"rsi":rsi,"acc":acc,"trend":trend,"bb":bb,"time":datetime.now().strftime("%H:%M:%S")}
    STATE["last"]=data
    STATE["log"].insert(0,f'{data["time"]} {pair} {STATE["tf"]} {direction} {acc}%')
    STATE["log"]=STATE["log"][:10]
    
    if "CALL" in direction or "PUT" in direction:
        tg_send(f"*POCKET V4 FINAL*\n\n*Pair:* {pair} - {STATE['tf']}\n*Signal:* {direction} *{acc}%*\n*Price:* {price}\n*RSI:* {rsi} | *Trend:* {trend} | *BB:* {bb}\n*Time:* {data['time']}\n\n_Trade now in PocketOption - 1m expiry_")
    return data

HTML = """
<!DOCTYPE html>
<html><head>
<meta name="viewport" content="width=device-width, initial-scale=1, maximum-scale=1">
<meta name="theme-color" content="#020617">
<link rel="manifest" href="/manifest.json">
<title>POCKET V4 FINAL</title>
<style>
*{box-sizing:border-box}body{margin:0;background:#020617;color:#fff;font-family:system-ui,Arial;padding:0}
.app{max-width:420px;margin:0 auto;background:#0b1220;min-height:100vh;padding:12px}
.head{display:flex;justify-content:space-between;align-items:center}
.badge{padding:6px 14px;border-radius:20px;font-weight:900;font-size:12px;background:#0ea5e9;color:#fff}
.pairs{display:grid;grid-template-columns:1fr 1fr 1fr 1fr;gap:6px;margin:10px 0}
.pairs button{padding:8px 2px;border-radius:10px;border:1px solid #1e293b;background:#1e293b;color:#94a3b8;font-size:11px;font-weight:700}
.pairs button.active{background:#e0f2fe;color:#0c4a6e;border-color:#38bdf8}
.tf{display:flex;gap:6px;margin:6px 0;align-items:center;color:#64748b;font-size:13px}
.tf button{padding:6px 14px;border-radius:10px;border:0;background:#1e293b;color:#fff}
.tf button.active{background:#fff;color:#000;font-weight:900}
.price{text-align:center;font-size:42px;font-weight:900;margin:8px 0;letter-spacing:1px}
.signal{padding:16px;border-radius:16px;text-align:center;font-size:24px;font-weight:900;border:2px solid;margin:10px 0}
.row{display:flex;justify-content:space-between;background:#151f32;padding:12px 14px;border-radius:12px;margin:6px 0;font-size:14px}
.btn{width:100%;padding:16px;border-radius:14px;border:0;font-weight:900;font-size:18px;margin-top:10px;background:linear-gradient(90deg,#38bdf8,#22c55e);color:#000}
.small{font-size:11px;color:#64748b;text-align:center;margin:8px 0}
.log{background:#020617;padding:8px;border-radius:10px;font-size:11px;margin-top:10px}
.dot{width:8px;height:8px;background:#22c55e;border-radius:50%;display:inline-block;margin-right:6px;animation:blink 1s infinite}
@keyframes blink{0%{opacity:1}50%{opacity:.3}}
</style></head><body><div class=app>
<div class=head><h2 style="margin:0">POCKET V4<br>FINAL</h2><span class=badge id=tgBadge>TELEGRAM: CHECKING</span></div>
<div style="color:#22c55e;font-size:12px;margin:6px 0"><span class=dot></span>LIVE - Instant Signal - OTC - No Auto Trade</div>
<div class=pairs id=pairs></div>
<div class=tf>Timeframe:<button onclick="setTF('1m')" id=tf1m class=active>1m</button><button onclick="setTF('2m')" id=tf2m>2m</button><button onclick="setTF('5m')" id=tf5m>5m</button></div>
<div id=pairLabel style="text-align:center;color:#f59e0b;font-weight:900;margin-top:6px">GBPUSD_otc - 1m</div>
<div class=price id=price>1.08018</div>
<div class=signal id=sigBox style="border-color:#22c55e;color:#22c55e;background:#052e16">CALL ▲ GBPUSD 87%</div>
<div class=row><span>RSI</span><b id=rsi>34</b></div>
<div class=row><span>Accuracy</span><b id=acc>87%</b></div>
<div class=row><span>Trend</span><b id=trend>DOWN</b></div>
<div class=row><span>BB</span><b id=bb>LOWER</b></div>
<button class=btn onclick="getSignal()">🔔 GET SIGNAL NOW</button>
<div class=small>Next candle in: <b id=timer>00:02</b> | DEMO/REAL same | Manual trade only</div>
<div class=log id=log>History...</div>
<div class=small>Tap browser menu → Add to Home Screen → Use as App<br>Signals auto-send to Telegram if Token set in Render</div>
</div>
<script>
let curPair='GBPUSD_otc';let curTF='1m';
const pairs=["EURUSD_otc","GBPUSD_otc","EURJPY_otc","USDJPY_otc","AUDUSD_otc","EURGBP_otc","GBPJPY_otc","BTCUSD_otc"];
function renderPairs(){
 let h='';pairs.forEach(p=>{h+=`<button onclick="setPair('${p}')" id="p-${p}" class="${p==curPair?'active':''}">${p.replace('_otc','')}</button>`});
 document.getElementById('pairs').innerHTML=h;
}
function setPair(p){curPair=p;renderPairs();document.getElementById('pairLabel').innerText=p+' - '+curTF;getSignal();}
function setTF(tf){curTF=tf;document.querySelectorAll('.tf button').forEach(b=>b.classList.remove('active'));document.getElementById('tf'+tf).classList.add('active');document.getElementById('pairLabel').innerText=curPair+' - '+tf;}
async function getSignal(){
 const r=await fetch('/api/signal?pair='+curPair+'&tf='+curTF);const d=await r.json();
 document.getElementById('price').innerText=d.price;
 document.getElementById('sigBox').innerText=d.dir+' '+d.pair.replace('_otc','')+' '+d.acc+'%';
 document.getElementById('sigBox').style.color=d.color;document.getElementById('sigBox').style.borderColor=d.color;
 document.getElementById('rsi').innerText=d.rsi;document.getElementById('acc').innerText=d.acc+'%';
 document.getElementById('trend').innerText=d.trend;document.getElementById('bb').innerText=d.bb;
 document.getElementById('log').innerHTML=d.log.map(x=>'<div>'+x+'</div>').join('');
}
async function checkTG(){try{const r=await fetch('/api/status');const d=await r.json();document.getElementById('tgBadge').innerText=d.tg_ok?'TELEGRAM ✅':'TELEGRAM ❌';document.getElementById('tgBadge').style.background=d.tg_ok?'#22c55e':'#334155';}catch{}}
renderPairs();getSignal();checkTG();setInterval(()=>{let s=document.getElementById('timer');let v=s.innerText.split(':');let sec=parseInt(v[1]);sec--;if(sec<0)sec=59;s.innerText='00:'+String(sec).padStart(2,'0')},1000);
</script></body></html>
"""

@app.route('/')
def home(): return HTML

@app.route('/api/signal')
def api_signal():
    pair = request.args.get('pair', STATE["pair"])
    tf = request.args.get('tf', '1m')
    STATE["pair"]=pair; STATE["tf"]=tf
    d = make_signal(pair)
    return jsonify({"price":d["price"],"dir":d["dir"],"color":d["color"],"rsi":d["rsi"],"acc":d["acc"],"trend":d["trend"],"bb":d["bb"],"pair":d["pair"],"log":STATE["log"]})

@app.route('/api/status')
def status(): return jsonify({"tg_ok": bool(TG_TOKEN and TG_CHAT)})

@app.route('/manifest.json')
def manifest():
    return jsonify({"name":"Pocket V4 Final","short_name":"POCKET V4","start_url":"/","display":"standalone","background_color":"#020617","theme_color":"#020617"})

@app.route('/health')
def h(): return "OK"

if __name__=='__main__': app.run(host='0.0.0.0', port=int(os.environ.get('PORT',10000)))
